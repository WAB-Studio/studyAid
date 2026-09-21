#!/usr/bin/env python3
"""Registro del sistema de estudio. Solo stdlib.

Hace unicamente lo que es caro o poco confiable de hacer leyendo archivos:
reloj real, aritmetica de fechas sobre el log, floats de SM-2 y agregacion.
Todo lo demas vive en Markdown y lo mantiene Claude.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CARDS_FILE = DATA / "cards.json"
SESSIONS_FILE = DATA / "sessions.jsonl"
CURRENT_FILE = DATA / "current_session.json"
EXTERNOS_FILE = DATA / "externos.jsonl"

STALE_HOURS = 4
# Tope por defecto de tarjetas vencidas por sesion, para que una pausa no genere un muro.
TOPE_VENCIDAS = 20
RESULTS = ("solo", "con_pistas", "abandonado")
MODES = ("micro", "media", "fondo")
PREDICCIONES_EJ = ("solo", "con_pistas", "no_lo_saco", "no-preguntada")
PREDICCIONES_SN = ("si", "no", "no-preguntada")
CORREGIBLES = ("ejercicio", "patron", "repaso")
TIPOS_EXTERNO = ("video", "lectura", "curso", "podcast", "practica", "otro")
# "practica" es la excepcion: recuperacion activa que paso fuera de una sesion abierta
# (una explicacion en el chat, un recall suelto). Esos minutos SI son practica y suman
# con los de sesion; el resto de los tipos es exposicion y va aparte. El eje que importa
# no es dentro/fuera de sesion, es exposicion contra recuperacion.
TIPOS_ACTIVOS = ("practica",)
# Tope de un registro externo suelto. Mas que esto casi siempre es un error de tipeo,
# y si de verdad fueron seis horas conviene partirlas por fuente.
MAX_MIN_EXTERNO = 360

# Campos de la sesion misma, corregibles sin --evento. "sigue" es lo que abre la proxima
# conversacion, asi que uno desactualizado desorienta igual que un evento mal registrado.
# "afk_declarado" esta porque el AFK casi siempre se sabe tarde: el que se fue es el usuario y
# solo lo puede contar al volver, a veces despues de cerrar. Es la misma excepcion que
# externos() -- ningun reloj cubrio ese hueco, asi que el numero lo pone el -- y no colisiona
# con la prohibicion sobre "calidad": minutos_efectivos es un recalculo puro, sin nada aguas
# abajo que ya se haya consumido. Preferi igual pausar/reanudar mientras pasa: la medicion
# concurrente es mas exacta que la retrospectiva, y esto es la red, no el camino.
CAMPOS_SESION = ("sigue", "afk_declarado")

# Que campos se pueden corregir por tipo de evento, y como se valida cada uno.
# "calidad" no esta y no es un olvido: ver cmd_corregir.
CAMPOS = {
    "ejercicio": {
        "ejercicio": "texto", "tema": "texto", "resultado": RESULTS,
        "pista_max": "entero", "prediccion": PREDICCIONES_EJ, "errores": "lista",
    },
    "patron": {
        "problema": "texto", "tema": "texto", "dijo": "texto", "acerto": "bool",
    },
    "repaso": {
        "tema": "texto", "prediccion": PREDICCIONES_SN,
    },
}


def now() -> datetime:
    return datetime.now().astimezone()


def today() -> date:
    return date.today()


def load(path: Path, default):
    if not path.exists():
        return default
    content = path.read_text(encoding="utf-8").strip()
    return json.loads(content) if content else default


def save(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def cards_db() -> dict:
    return load(CARDS_FILE, {"version": 1, "next_id": 1, "cards": []})


def sessions() -> list:
    if not SESSIONS_FILE.exists():
        return []
    return [json.loads(l) for l in SESSIONS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def die(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


# --------------------------------------------------------------------- sm-2

def sm2(sched: dict, quality: int) -> dict:
    ease = float(sched.get("ease", 2.5))
    reps = int(sched.get("reps", 0))
    interval = int(sched.get("interval", 0))
    lapses = int(sched.get("lapses", 0))

    ease = max(1.3, round(ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)), 4))

    if quality < 3:
        reps, interval, lapses = 0, 1, lapses + 1
    else:
        reps += 1
        interval = 1 if reps == 1 else 6 if reps == 2 else max(1, round(interval * ease))

    return {
        "ease": ease,
        "reps": reps,
        "interval": interval,
        "lapses": lapses,
        "due": (today() + timedelta(days=interval)).isoformat(),
    }


# ----------------------------------------------------------------- sesiones

def current_session():
    return load(CURRENT_FILE, None)


def require_current() -> dict:
    cur = current_session()
    if not cur:
        die("no hay sesion abierta. Corre: study.py sesion iniciar --modo micro|media|fondo")
    return cur


def last_activity(cur: dict) -> datetime:
    return max(parse_dt(s) for s in [cur["iniciada"]] + [e["ts"] for e in cur.get("eventos", [])])


def is_stale(cur: dict) -> bool:
    return (now() - last_activity(cur)) > timedelta(hours=STALE_HOURS)


def push_event(cur: dict, event: dict) -> None:
    event["ts"] = now().isoformat(timespec="seconds")
    cur.setdefault("eventos", []).append(event)
    save(CURRENT_FILE, cur)


def cerrar_pausa(cur: dict, hasta: datetime) -> int:
    """Cierra una pausa abierta y acumula los minutos en afk_medido. Devuelve lo acumulado ahora."""
    desde = cur.get("pausa_desde")
    if not desde:
        return 0
    minutos = max(0, round((hasta - parse_dt(desde)).total_seconds() / 60))
    cur["afk_medido"] = cur.get("afk_medido", 0) + minutos
    cur.pop("pausa_desde", None)
    return minutos


def efectivos(s: dict) -> int:
    """Minutos de estudio real de una sesion cerrada. Las sesiones viejas no tienen el campo."""
    return max(1, s.get("minutos_efectivos", s["minutos"]))


def cmd_pausar(args) -> None:
    cur = require_current()
    if cur.get("pausa_desde"):
        desde = parse_dt(cur["pausa_desde"]).strftime("%H:%M")
        die(f"la sesion ya estaba pausada desde las {desde}.")
    cur["pausa_desde"] = now().isoformat(timespec="seconds")
    push_event(cur, {"tipo": "pausa"})
    print(f"Sesion pausada a las {now().strftime('%H:%M')}. "
          "El reloj sigue corriendo pero estos minutos no cuentan. "
          "Reanudala con: study.py sesion reanudar")


def cmd_reanudar(args) -> None:
    cur = require_current()
    if not cur.get("pausa_desde"):
        die("la sesion no esta pausada. Nada que reanudar.")
    minutos = cerrar_pausa(cur, now())
    push_event(cur, {"tipo": "reanudacion", "afk_min": minutos})
    print(f"Sesion reanudada a las {now().strftime('%H:%M')}. "
          f"{minutos} min descontados, {cur['afk_medido']} min de AFK medido en total.")


def cmd_iniciar(args) -> None:
    cur = current_session()
    if cur:
        die(f"ya hay una sesion abierta ({cur['id']}, modo {cur['modo']}). Cierrala, "
            "o borra data/current_session.json para descartarla.")
    started = now()
    save(CURRENT_FILE, {
        "id": started.strftime("s%Y%m%d-%H%M"),
        "modo": args.modo,
        "iniciada": started.isoformat(timespec="seconds"),
        "tema_previsto": args.tema,
        "eventos": [],
    })
    print(f"Sesion abierta en modo {args.modo} a las {started.strftime('%H:%M')}.")


def cmd_ejercicio(args) -> None:
    cur = require_current()
    errores = [e.strip().lower().replace(" ", "-")
               for e in (args.error_clase or "").split(",") if e.strip()]
    push_event(cur, {
        "tipo": "ejercicio",
        "ejercicio": args.ejercicio,
        "tema": args.tema,
        "resultado": args.resultado,
        "pista_max": args.pista_max,
        "prediccion": args.prediccion,
        "errores": errores,
    })
    msg = f"Registrado: {args.ejercicio} ({args.resultado}, pista maxima {args.pista_max})."
    if args.prediccion:
        acerto = args.prediccion == args.resultado
        msg += f" Predijo {args.prediccion}: calibracion {'ok' if acerto else 'fallada'}."
    if errores:
        msg += f" Errores: {', '.join(errores)}."
    print(msg)


def cmd_patron(args) -> None:
    cur = require_current()
    dijo = args.dijo.strip().lower()
    tema = args.tema.strip().lower()
    valido = args.valido == "si"
    push_event(cur, {
        "tipo": "patron",
        "problema": args.problema,
        "tema": tema,           # patron canonico del indice
        "dijo": dijo,           # lo que dijo el usuario, textual
        "acerto": valido,       # JUICIO DEL ASISTENTE, no igualdad de strings
        "juicio": True,
    })
    if valido:
        extra = "" if dijo == tema else f" (dijo {dijo}, tambien valido)"
        print(f"Reconocimiento: {args.problema} valido{extra}.")
    else:
        print(f"Reconocimiento: {args.problema} no valido: dijo {dijo}, era {tema}.")


def cmd_repaso(args) -> None:
    db = cards_db()
    card = next((c for c in db["cards"] if c["id"] == args.tarjeta), None)
    if card is None:
        die(f"no existe la tarjeta {args.tarjeta}")
    if card.get("retirada"):
        die(f"la tarjeta {args.tarjeta} esta retirada desde el "
            f"{card['retirada']['fecha']} ({card['retirada']['motivo']}). No se puntua.")
    if not 0 <= args.calidad <= 5:
        die("calidad fuera de rango (0-5)")

    card["sm2"] = sm2(card.get("sm2", {}), args.calidad)
    card.setdefault("historial", []).append({"fecha": today().isoformat(), "calidad": args.calidad})
    save(CARDS_FILE, db)

    cur = current_session()
    if cur:
        push_event(cur, {"tipo": "repaso", "tarjeta": card["id"], "tema": card["tema"],
                         "calidad": args.calidad, "prediccion": args.prediccion})

    print(f"{card['id']}: proxima en {card['sm2']['interval']}d ({card['sm2']['due']}), "
          f"ease {card['sm2']['ease']}.")
    if args.prediccion:
        dijo_si = args.prediccion == "si"
        if dijo_si and args.calidad < 3:
            print("SOBRECONFIANZA: dijo que la sabia y fallo. Anotado.")
        elif not dijo_si and args.calidad >= 3:
            print("SUBESTIMACION: dijo que no la sabia y la acerto. Anotado.")
    if args.calidad < 3:
        print("FALLADA: volve a preguntarla mas tarde en esta misma sesion, sin volver a puntuarla.")
        print("No expliques ahora. Mostra el dorso, nombra en una linea donde divergio, y segui.")


def eventos_numerados(src: dict) -> list:
    """Eventos corregibles de una sesion, en orden cronologico y con el mismo numero
    este la sesion abierta o cerrada. Una cerrada los guarda repartidos en tres listas."""
    if "eventos" in src:
        ev = [e for e in src["eventos"] if e.get("tipo") in CORREGIBLES]
    else:
        ev = src.get("ejercicios", []) + src.get("patrones", []) + src.get("repasos", [])
    return sorted(ev, key=lambda e: e.get("ts", ""))


def describir_evento(e: dict) -> str:
    if e["tipo"] == "ejercicio":
        extra = f", errores: {', '.join(e['errores'])}" if e.get("errores") else ""
        return (f"ejercicio {e['ejercicio']} ({e['tema']}) -> {e['resultado']}, "
                f"pista_max {e.get('pista_max', 0)}, predijo {e.get('prediccion')}{extra}")
    if e["tipo"] == "patron":
        return (f"patron {e['problema']} (canonico: {e['tema']}) -> "
                f"{'valido' if e.get('acerto') else 'no valido'}, dijo: {e.get('dijo')}")
    return (f"repaso {e['tarjeta']} ({e['tema']}) -> calidad {e['calidad']}, "
            f"predijo {e.get('prediccion')}")


def buscar_sesion(sid: str):
    """Devuelve (registro, indice_en_jsonl) de una sesion cerrada."""
    ss = sessions()
    for i, s_ in enumerate(ss):
        if s_["id"] == sid:
            return s_, i, ss
    die(f"no existe la sesion cerrada {sid}. Corre 'estado' o mira data/sessions.jsonl.")


def cmd_eventos(args) -> None:
    if args.sesion:
        src, _, _ = buscar_sesion(args.sesion)
        cab = f"Sesion {src['id']} (cerrada, {src['minutos']} min)"
    else:
        src = require_current()
        cab = f"Sesion {src['id']} (abierta)"
    ev = eventos_numerados(src)
    print(f"{cab}: {len(ev)} evento(s) corregible(s).\n")
    if not ev:
        print("Nada registrado todavia.")
        return
    for i, e in enumerate(ev, 1):
        hora = e.get("ts", "")[11:16]
        print(f"  {i}. [{hora}] {describir_evento(e)}")
        for c in e.get("correcciones", []):
            print(f"       corregido {c['fecha']}: {c['campo']} {c['de']!r} -> {c['a']!r} "
                  f"({c['motivo']})")
    print("\nCorregir uno: study.py sesion corregir --evento N --campo CAMPO "
          "--valor VALOR --motivo \"...\"")


def cmd_corregir(args) -> None:
    if args.sesion:
        src, idx, todas = buscar_sesion(args.sesion)
        abierta = False
    else:
        src, idx, todas = require_current(), None, None
        abierta = True

    if args.evento is None:
        if args.campo not in CAMPOS_SESION:
            die(f"sin --evento solo se corrigen campos de la sesion: "
                f"{', '.join(CAMPOS_SESION)}. Para un evento, pasa --evento N.")
        if args.campo == "afk_declarado":
            if abierta:
                die("el AFK de una sesion abierta no se corrige aca: usa 'sesion pausar' y "
                    "'sesion reanudar' mientras pasa, o pasa --afk al cerrar. Medir el hueco "
                    "mientras ocurre es mas exacto que reconstruirlo despues.")
            try:
                valor_s = int(args.valor)
            except ValueError:
                die(f"--valor tiene que ser un entero de minutos, llego {args.valor!r}.")
            if valor_s < 0:
                die("el AFK no puede ser negativo.")
            afk_medido = src.get("afk_medido", 0)
            if afk_medido + valor_s >= src["minutos"]:
                die(f"el AFK ({afk_medido + valor_s} min) se come toda la sesion "
                    f"({src['minutos']} min de reloj). Revisa el numero.")
        else:
            valor_s = args.valor
        anterior_s = src.get(args.campo)
        if anterior_s == valor_s:
            die(f"{args.campo} ya vale {valor_s!r}. Nada que corregir.")
        src[args.campo] = valor_s
        if args.campo == "afk_declarado":
            src["minutos_efectivos"] = src["minutos"] - src.get("afk_medido", 0) - valor_s
        src.setdefault("correcciones", []).append({
            "fecha": today().isoformat(), "campo": args.campo,
            "de": anterior_s, "a": valor_s, "motivo": args.motivo,
        })
        if abierta:
            save(CURRENT_FILE, src)
        else:
            todas[idx] = src
            tmp = SESSIONS_FILE.with_name(SESSIONS_FILE.name + ".tmp")
            tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in todas),
                           encoding="utf-8")
            os.replace(tmp, SESSIONS_FILE)
        print(f"Sesion {src['id']} corregida: {args.campo} {anterior_s!r} -> {valor_s!r}.")
        print(f"  Motivo: {args.motivo}")
        if args.campo == "afk_declarado":
            print(f"  Recalculado: {src['minutos']} min de reloj - "
                  f"{src.get('afk_medido', 0)} medidos - {valor_s} declarados = "
                  f"{src['minutos_efectivos']} min efectivos.")
        print("El valor anterior no se borra: queda en 'correcciones' dentro de la sesion.")
        return

    ev = eventos_numerados(src)
    if not 1 <= args.evento <= len(ev):
        die(f"evento {args.evento} fuera de rango: hay {len(ev)}. "
            "Corre 'sesion eventos' para verlos numerados.")
    e = ev[args.evento - 1]

    if e["tipo"] == "repaso" and args.campo == "calidad":
        die("la calidad de un repaso no se corrige: el scheduler SM-2 ya avanzo el intervalo, "
            "el ease y los lapsos a partir de ella, y eso no se deshace de forma confiable. "
            "Anota la correccion en la bitacora y, si la tarjeta quedo mal calibrada, "
            "volve a puntuarla en la proxima sesion.")

    campos = CAMPOS[e["tipo"]]
    if args.campo not in campos:
        die(f"'{args.campo}' no es corregible en un evento de tipo {e['tipo']}. "
            f"Campos: {', '.join(campos)}.")

    regla = campos[args.campo]
    if regla == "entero":
        try:
            valor = int(args.valor)
        except ValueError:
            die(f"--valor tiene que ser un entero, llego {args.valor!r}.")
    elif regla == "lista":
        valor = [x.strip().lower().replace(" ", "-")
                 for x in args.valor.split(",") if x.strip()]
    elif regla == "bool":
        if args.valor not in ("si", "no"):
            die("--valor para un campo si/no tiene que ser 'si' o 'no'.")
        valor = args.valor == "si"
    elif isinstance(regla, tuple):
        if args.valor not in regla:
            die(f"--valor para {args.campo} tiene que ser uno de: {', '.join(regla)}.")
        valor = args.valor
    else:
        valor = args.valor.strip()

    anterior = e.get(args.campo)
    if anterior == valor:
        die(f"{args.campo} ya vale {valor!r}. Nada que corregir.")

    e[args.campo] = valor
    e.setdefault("correcciones", []).append({
        "fecha": today().isoformat(),
        "campo": args.campo,
        "de": anterior,
        "a": valor,
        "motivo": args.motivo,
    })

    if abierta:
        save(CURRENT_FILE, src)
    else:
        src["temas"] = sorted({x["tema"] for x in eventos_numerados(src) if x.get("tema")})
        todas[idx] = src
        tmp = SESSIONS_FILE.with_name(SESSIONS_FILE.name + ".tmp")
        tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in todas),
                       encoding="utf-8")
        os.replace(tmp, SESSIONS_FILE)

    print(f"Evento {args.evento} corregido: {args.campo} {anterior!r} -> {valor!r}.")
    print(f"  Motivo: {args.motivo}")
    print(f"  Queda: {describir_evento(e)}")
    print("El valor anterior no se borra: queda en 'correcciones' dentro del evento.")


def cmd_cerrar(args) -> None:
    cur = require_current()
    started = parse_dt(cur["iniciada"])
    ended = last_activity(cur) if is_stale(cur) else now()
    cerrar_pausa(cur, ended)
    minutos = max(1, round((ended - started).total_seconds() / 60))

    afk_medido = cur.get("afk_medido", 0)
    afk_declarado = max(0, args.afk or 0)
    if afk_medido + afk_declarado >= minutos:
        die(f"el AFK ({afk_medido + afk_declarado} min) se come toda la sesion "
            f"({minutos} min de reloj). Revisa el numero.")
    minutos_efectivos = minutos - afk_medido - afk_declarado

    bitacora = None
    if args.bitacora:
        bpath = Path(args.bitacora)
        bpath = bpath if bpath.is_absolute() else ROOT / bpath
        if not bpath.exists():
            die(f"la bitacora {args.bitacora} no existe. Escribila antes de cerrar la sesion.")
        bitacora = str(bpath.relative_to(ROOT))
    elif not args.sin_bitacora:
        die("falta --bitacora RUTA, o --sin-bitacora si la sesion se corto y no hay "
            "material honesto para escribirla. La sesion cuenta igual en ambos casos.")

    eventos = cur.get("eventos", [])
    record = {
        "id": cur["id"],
        "modo": cur["modo"],
        "iniciada": cur["iniciada"],
        "terminada": ended.isoformat(timespec="seconds"),
        "minutos": minutos,
        "afk_medido": afk_medido,
        "afk_declarado": afk_declarado,
        "minutos_efectivos": minutos_efectivos,
        "estado": "completa" if bitacora else "incompleta",
        "temas": sorted({e["tema"] for e in eventos if e.get("tema")}),
        "bitacora": bitacora,
        "sigue": args.sigue,
        "ejercicios": [e for e in eventos if e["tipo"] == "ejercicio"],
        "repasos": [e for e in eventos if e["tipo"] == "repaso"],
        "patrones": [e for e in eventos if e["tipo"] == "patron"],
        "cortada_por_inactividad": is_stale(cur),
    }
    SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SESSIONS_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    CURRENT_FILE.unlink(missing_ok=True)

    reloj = (f"{minutos} min de reloj, {minutos_efectivos} min efectivos"
             if afk_medido or afk_declarado else f"{minutos} min")
    print(f"Sesion {record['id']} cerrada: {reloj}, "
          f"{len(record['ejercicios'])} ejercicios, {len(record['repasos'])} repasos, "
          f"bitacora {"si" if bitacora else "NO"}.")
    if afk_medido or afk_declarado:
        partes = []
        if afk_medido:
            partes.append(f"{afk_medido} medidos con pausar/reanudar")
        if afk_declarado:
            partes.append(f"{afk_declarado} declarados al cerrar")
        print(f"  AFK descontado: {' + '.join(partes)}. El reloj crudo queda guardado igual.")
    if record["cortada_por_inactividad"]:
        print(f"Se conto hasta el ultimo evento por inactividad mayor a {STALE_HOURS}h.")


# ----------------------------------------------------------------- tarjetas

def cmd_agregar(args) -> None:
    payload = json.loads(Path(args.archivo).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        die("el archivo debe contener una lista de objetos {tema, frente, dorso}")

    db = cards_db()
    creadas = []
    for item in payload:
        for campo in ("tema", "frente", "dorso"):
            if not item.get(campo):
                die(f"falta el campo '{campo}' en una de las tarjetas")
        cid = f"c{db['next_id']:04d}"
        db["next_id"] += 1
        db["cards"].append({
            "id": cid,
            "tema": item["tema"],
            "frente": item["frente"].strip(),
            "dorso": item["dorso"].strip(),
            "creada": today().isoformat(),
            "sm2": {"ease": 2.5, "reps": 0, "interval": 1, "lapses": 0,
                    "due": (today() + timedelta(days=1)).isoformat()},
            "historial": [],
        })
        creadas.append(cid)
    save(CARDS_FILE, db)
    print(f"{len(creadas)} tarjeta(s) creada(s): {', '.join(creadas)}. Vencen manana.")


def due_cards(limit=None) -> list:
    """Mas atrasadas primero, intercaladas por tema.

    El orden por vencimiento decide la prioridad; el round-robin entre temas evita
    que salgan en bloque por tema, que es lo que anula el efecto de intercalado.
    """
    hoy = today().isoformat()
    vencidas = [c for c in cards_db()["cards"]
                if c["sm2"]["due"] <= hoy and not c.get("retirada")]
    vencidas.sort(key=lambda c: (c["sm2"]["due"], c["id"]))

    por_tema: dict = {}
    for c in vencidas:
        por_tema.setdefault(c["tema"], []).append(c)

    salida = []
    while any(por_tema.values()):
        for tema in list(por_tema):
            if por_tema[tema]:
                salida.append(por_tema[tema].pop(0))
    return salida[:limit] if limit else salida


def cmd_vencidas(args) -> None:
    total = len(due_cards())
    tope = None if args.todas else (args.limite or TOPE_VENCIDAS)
    vencidas = due_cards(tope)
    if tope and total > tope:
        print(f"Hay {total} vencidas. Mostrando {tope}, las mas atrasadas primero. "
              "Usa --todas para verlas todas.\n")
    if not vencidas:
        print("No hay tarjetas vencidas.")
        return
    print(f"{len(vencidas)} tarjeta(s) vencida(s):\n")
    for c in vencidas:
        print(f"[{c['id']}] ({c['tema']}) {c['frente']}")
        print(f"    -> {c['dorso']}\n")


def cmd_retirar(args) -> None:
    """Retira una tarjeta sin borrarla.

    Borrarla dejaria los repasos ya registrados en sessions.jsonl apuntando a un id
    inexistente, y las metricas de calibracion empezarian a mentir. Retirada sale de
    circulacion pero conserva su historial y el motivo.
    """
    db = cards_db()
    card = next((c for c in db["cards"] if c["id"] == args.tarjeta), None)
    if card is None:
        die(f"no existe la tarjeta {args.tarjeta}")
    if card.get("retirada"):
        die(f"la tarjeta {args.tarjeta} ya estaba retirada el {card['retirada']['fecha']}: "
            f"{card['retirada']['motivo']}")
    if not args.motivo.strip():
        die("--motivo no puede estar vacio: el registro tiene que decir por que salio.")

    card["retirada"] = {"fecha": today().isoformat(), "motivo": args.motivo.strip()}
    save(CARDS_FILE, db)
    repasos = len(card.get("historial", []))
    print(f"Tarjeta {card['id']} ({card['tema']}) retirada: {args.motivo.strip()}")
    print(f"  Se conservan sus {repasos} repaso(s). Deja de aparecer en vencidas.")


def cmd_editar(args) -> None:
    """Corrige la redaccion de una tarjeta conservando su historial SM-2.

    La linea que decide entre esto y 'retirar' es una sola: **cambia lo que hay que
    recuperar?** El ease y el intervalo son especificos del item -- miden lo dificil que le
    resulta recuperar *eso*. Si la tarjeta sigue pidiendo lo mismo y solo se arregla como esta
    escrita, esos numeros siguen siendo validos y tirarlos pierde datos caros por nada.

    Si el frente pasa a exigir otra recuperacion, es OTRO item: heredar el ease le atribuiria a
    la pregunta nueva una dificultad medida sobre la vieja, que es precision falsa. Eso se
    resuelve con 'retirar' y una tarjeta nueva, no con esto. Caso real, el 2026-09-20: c0016
    ("caso borde de largo" -> "que largo de entrada") habria sido edicion; c0007 ("cuanta
    memoria usa" -> "que ocupa esa memoria") fue retiro, y perder su ease de 1.68 fue correcto.

    La tool no puede juzgar semantica, asi que no intenta: exige --motivo, guarda el texto
    anterior en 'ediciones' y imprime la advertencia cada vez. La decision queda visible y
    auditable, que es lo unico que la protege de disfrazar un cambio de item de arreglo de tipeo.
    """
    db = cards_db()
    card = next((c for c in db["cards"] if c["id"] == args.tarjeta), None)
    if card is None:
        die(f"no existe la tarjeta {args.tarjeta}")
    if card.get("retirada"):
        die(f"la tarjeta {args.tarjeta} esta retirada desde el {card['retirada']['fecha']} "
            f"({card['retirada']['motivo']}). Una tarjeta fuera de circulacion no se edita: "
            "si la queres de vuelta, creala nueva.")
    if not args.motivo.strip():
        die("--motivo no puede estar vacio: el registro tiene que decir que se cambio y por que.")

    cambios = []
    for campo in ("frente", "dorso", "tema"):
        valor = getattr(args, campo, None)
        if valor is None:
            continue
        valor = valor.strip()
        if not valor:
            die(f"--{campo} no puede quedar vacio.")
        if valor == card[campo]:
            die(f"{campo} ya dice exactamente eso. Nada que editar.")
        cambios.append((campo, card[campo], valor))

    if not cambios:
        die("pasa al menos uno de --frente, --dorso o --tema.")

    for campo, antes, despues in cambios:
        card[campo] = despues
        card.setdefault("ediciones", []).append({
            "fecha": today().isoformat(), "campo": campo,
            "de": antes, "a": despues, "motivo": args.motivo.strip(),
        })

    save(CARDS_FILE, db)
    repasos = len(card.get("historial", []))
    sm2_actual = card["sm2"]
    print(f"Tarjeta {card['id']} ({card['tema']}) editada: "
          f"{', '.join(c[0] for c in cambios)}.")
    print(f"  Motivo: {args.motivo.strip()}")
    for campo, antes, despues in cambios:
        print(f"  {campo}: {antes!r}")
        print(f"       -> {despues!r}")
    print(f"  Historial INTACTO: {repasos} repaso(s), ease {sm2_actual['ease']}, "
          f"vence {sm2_actual['due']}.")
    print("  El texto anterior no se borra: queda en 'ediciones' dentro de la tarjeta.")
    print("OJO: esto es para la REDACCION. Si el frente pasa a pedir otra recuperacion, es otro")
    print("     item y corresponde 'tarjetas retirar' mas una nueva: el ease viejo mide la")
    print("     dificultad de la pregunta vieja y heredarlo seria precision falsa.")


def cmd_retiradas(args) -> None:
    fuera = [c for c in cards_db()["cards"] if c.get("retirada")]
    if not fuera:
        print("No hay tarjetas retiradas.")
        return
    fuera.sort(key=lambda c: (c["retirada"]["fecha"], c["id"]))
    print(f"{len(fuera)} tarjeta(s) retirada(s):\n")
    for c in fuera:
        print(f"[{c['id']}] ({c['tema']}) retirada el {c['retirada']['fecha']}")
        print(f"    {c['frente']}")
        print(f"    motivo: {c['retirada']['motivo']}")
        print(f"    repasos conservados: {len(c.get('historial', []))}\n")


# ----------------------------------------------------------------- estudio externo

def externos() -> list:
    """Estudio autonomo registrado fuera de una sesion: video, lectura, un curso.

    Vive en su propio log y en su propio contador a proposito. Reexponerse a una
    explicacion produce sensacion de dominio sin retencion -- la ilusion de fluidez --,
    y recuperar produce retencion. Si los dos cayeran en el mismo numero de minutos,
    ese numero dejaria de medir practica y el camino mas barato para subirlo seria
    el que menos ensena. Cuenta para racha (es contacto real con el material) y no
    cuenta como minutos de practica.
    """
    if not EXTERNOS_FILE.exists():
        return []
    out = []
    for line in EXTERNOS_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            if not r.get("anulado"):
                out.append(r)
    return out


def externos_todos() -> list:
    if not EXTERNOS_FILE.exists():
        return []
    return [json.loads(l) for l in EXTERNOS_FILE.read_text(encoding="utf-8").splitlines()
            if l.strip()]


def minutos_externos_por_dia() -> dict:
    """Solo exposicion. Lo registrado como 'practica' suma en minutos_por_dia."""
    acc = defaultdict(int)
    for r in externos():
        if r["tipo"] not in TIPOS_ACTIVOS:
            acc[date.fromisoformat(r["fecha"])] += r["minutos"]
    return acc


def minutos_activos_sueltos() -> dict:
    acc = defaultdict(int)
    for r in externos():
        if r["tipo"] in TIPOS_ACTIVOS:
            acc[date.fromisoformat(r["fecha"])] += r["minutos"]
    return acc


def cmd_externo_agregar(args) -> None:
    if args.minutos < 1 or args.minutos > MAX_MIN_EXTERNO:
        die(f"minutos fuera de rango (1-{MAX_MIN_EXTERNO}). Recibido: {args.minutos}.")
    fecha = today() if not args.fecha else date.fromisoformat(args.fecha)
    if fecha > today():
        die(f"la fecha {fecha.isoformat()} es futura. No se registra lo que todavia no paso.")

    # Correlativo por dia de registro, no reloj: dos registros cargados en el mismo
    # segundo salian con el mismo id y 'anular' se volvia ambiguo.
    prefijo = f"x{now().strftime('%Y%m%d')}-"
    usados = [r["id"] for r in externos_todos() if r["id"].startswith(prefijo)]
    record = {
        "id": f"{prefijo}{len(usados) + 1:02d}",
        "fecha": fecha.isoformat(),
        "minutos": args.minutos,
        "tipo": args.tipo,
        "fuente": args.fuente,
        "tema": args.tema,
        "nota": args.nota,
        "registrado_en": now().isoformat(timespec="seconds"),
    }
    EXTERNOS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with EXTERNOS_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Externo {record['id']} registrado: {args.minutos} min de {args.tipo} "
          f"el {fecha.isoformat()}" + (f", tema {args.tema}" if args.tema else "") + ".")
    print(f"  Fuente: {args.fuente}")
    if args.tipo in TIPOS_ACTIVOS:
        print("Cuenta para la racha Y como minutos de practica: hubo recuperacion activa, "
              "aunque haya pasado fuera de una sesion abierta.")
    else:
        print("Cuenta para la racha. NO cuenta como minutos de practica: se reporta aparte, "
              "porque exponerse a una explicacion y recuperarla no son lo mismo.")
    if args.tema and args.tipo not in TIPOS_ACTIVOS:
        print(f"  No mueve el ultimo contacto de {args.tema}: haber visto material sobre un "
              "tema no es haberlo trabajado. Eso lo mueve una sesion o una practica.")


def cmd_externo_listar(args) -> None:
    rs = externos_todos()
    if not rs:
        print("No hay estudio externo registrado todavia.")
        return
    rs.sort(key=lambda r: (r["fecha"], r["registrado_en"]))
    for r in rs[-(args.limite or 30):]:
        marca = "  [ANULADO]" if r.get("anulado") else ""
        tema = f" ({r['tema']})" if r.get("tema") else ""
        print(f"[{r['id']}] {r['fecha']}  {r['minutos']:>3} min  {r['tipo']}{tema}{marca}")
        print(f"    {r['fuente']}")
        if r.get("nota"):
            print(f"    nota: {r['nota']}")
        if r.get("anulado"):
            print(f"    anulado: {r['anulado']}")
    vivos = [r for r in rs if not r.get("anulado")]
    print(f"\nTotal vivo: {sum(r['minutos'] for r in vivos)} min en {len(vivos)} registro(s).")


def cmd_externo_anular(args) -> None:
    rs = externos_todos()
    hits = [r for r in rs if r["id"] == args.id]
    if not hits:
        die(f"no existe el registro externo {args.id}. Mira 'externo listar'.")
    if len(hits) > 1:
        die(f"{args.id} esta repetido {len(hits)} veces en el log. Arreglalo antes de anular: "
            "no se puede saber a cual te referis.")
    hit = hits[0]
    if hit.get("anulado"):
        die(f"{args.id} ya estaba anulado: {hit['anulado']}")
    hit["anulado"] = args.motivo
    hit["anulado_en"] = now().isoformat(timespec="seconds")
    tmp = EXTERNOS_FILE.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs),
                   encoding="utf-8")
    os.replace(tmp, EXTERNOS_FILE)
    print(f"{args.id} anulado: {args.motivo}")
    print("No se borra la linea: queda con su motivo, igual que una tarjeta retirada.")


# ----------------------------------------------------------------- agregado

def cerradas() -> list:
    """Todas las sesiones cerradas cuentan para tiempo y racha.

    Falta de bitacora es metadata incompleta, no una sesion inexistente:
    borrarla sesgaba la adherencia y hacia que inventar una bitacora de
    compromiso fuera mas barato que declarar el hueco.
    """
    return sessions()


def incompletas() -> list:
    return [s for s in sessions() if s.get("estado") != "completa"]


def racha() -> int:
    """Dias seguidos con contacto: una sesion, o estudio externo registrado.

    Decision del usuario el 2026-09-17. La racha mide el habito, y un dia de semana
    en que solo alcanza para un video en el bus es habito. Los minutos siguen
    separados: ver 'minutos_externos_por_dia'.
    """
    dias = {parse_dt(s["iniciada"]).date() for s in cerradas()}
    dias |= set(minutos_externos_por_dia())
    if not dias:
        return 0
    cursor = today()
    if cursor not in dias:
        cursor -= timedelta(days=1)
        if cursor not in dias:
            return 0
    n = 0
    while cursor in dias:
        n += 1
        cursor -= timedelta(days=1)
    return n


def minutos_por_dia() -> dict:
    """Minutos de practica: sesiones mas los registros sueltos de tipo 'practica'."""
    acc = defaultdict(int)
    for s in cerradas():
        acc[parse_dt(s["iniciada"]).date()] += efectivos(s)
    for d, m in minutos_activos_sueltos().items():
        acc[d] += m
    return acc


def ultimo_contacto() -> dict:
    """tema -> fecha del ultimo evento registrado sobre ese tema."""
    acc = {}
    for s in cerradas():
        d = parse_dt(s["iniciada"]).date().isoformat()
        for tema in s.get("temas", []):
            if tema not in acc or d > acc[tema]:
                acc[tema] = d
    # La practica suelta tambien es trabajo sobre el tema. La exposicion no: ver un video
    # sobre algo no lo deja trabajado, y contarlo como contacto esconderia un tema frio.
    for r in externos():
        if r["tipo"] in TIPOS_ACTIVOS and r.get("tema"):
            if r["tema"] not in acc or r["fecha"] > acc[r["tema"]]:
                acc[r["tema"]] = r["fecha"]
    return acc


def resumen_por_tema() -> dict:
    """Componentes crudos por tema. Sin puntaje compuesto.

    No se combina nada en un solo numero: el intervalo SM-2 mide cuando toca
    preguntar, no cuanto sabe la persona, y mezclarlo con ratios de ejercicios
    fabrica una medicion que no existe.
    """
    cards_by_topic = defaultdict(list)
    for c in cards_db()["cards"]:
        cards_by_topic[c["tema"]].append(c)

    ej_by_topic = defaultdict(lambda: {"intentados": 0, "solo": 0})
    for s in cerradas():
        for e in s.get("ejercicios", []):
            b = ej_by_topic[e["tema"]]
            b["intentados"] += 1
            if e["resultado"] == "solo":
                b["solo"] += 1

    contacto = ultimo_contacto()
    out = {}
    for tid in sorted(set(cards_by_topic) | set(ej_by_topic)):
        cards = cards_by_topic.get(tid, [])
        revs = [h for c in cards for h in c["historial"]]
        ej = ej_by_topic.get(tid, {"intentados": 0, "solo": 0})
        out[tid] = {
            "ejercicios": ej["intentados"],
            "sin_ayuda": ej["solo"],
            "tarjetas": len(cards),
            "repasos": len(revs),
            "aciertos": sum(1 for h in revs if h["calidad"] >= 3),
            "ultimo": contacto.get(tid, "-"),
        }
    return out


def cmd_estado(args) -> None:
    ahora = now()
    print(f"Hoy es {today().isoformat()}, son las {ahora.strftime('%H:%M')}.")

    cur = current_session()
    if cur:
        transcurrido = round((ahora - parse_dt(cur["iniciada"])).total_seconds() / 60)
        print(f"\nSESION ABIERTA: {cur['id']} (modo {cur['modo']}, {transcurrido} min, "
              f"{len(cur.get('eventos', []))} eventos).")
        if cur.get("pausa_desde"):
            desde = parse_dt(cur["pausa_desde"])
            print(f"  PAUSADA desde las {desde.strftime('%H:%M')} "
                  f"({round((ahora - desde).total_seconds() / 60)} min). "
                  "Reanudala antes de seguir.")
        if cur.get("afk_medido"):
            print(f"  AFK descontado hasta ahora: {cur['afk_medido']} min.")
        print("  Quedo colgada por inactividad: cierrala o descartala."
              if is_stale(cur) else "  Retomala donde quedo o cierrala.")

    vencidas = due_cards()
    if vencidas:
        por_tema = defaultdict(int)
        for c in vencidas:
            por_tema[c["tema"]] += 1
        detalle = ", ".join(f"{t} ({n})" for t, n in sorted(por_tema.items(), key=lambda x: -x[1]))
        print(f"\nTarjetas vencidas: {len(vencidas)} -> {detalle}")
    else:
        print("\nTarjetas vencidas: ninguna.")

    contacto = ultimo_contacto()
    if contacto:
        print("\nTemas con actividad (ultimo contacto):")
        frios = []
        for tema, fecha in sorted(contacto.items(), key=lambda x: x[1], reverse=True):
            dias = (today() - date.fromisoformat(fecha)).days
            marca = "  <- frio" if dias >= 21 else ""
            print(f"  {tema:<22} {fecha} ({dias}d){marca}")
            if dias >= 21:
                frios.append(tema)
    else:
        print("\nTemas con actividad: ninguno todavia.")
    print("Lee base/temario.md para saber que sigue sin tocar.")

    mpd = minutos_por_dia()
    y, w, _ = today().isocalendar()
    sem = [s for s in cerradas() if parse_dt(s["iniciada"]).date().isocalendar()[:2] == (y, w)]
    act_sem = sum(m for d, m in minutos_activos_sueltos().items()
                  if d.isocalendar()[:2] == (y, w))
    sueltos = f" + {act_sem} sueltos" if act_sem else ""
    print(f"\nRacha: {racha()} dia(s). Hoy: {mpd.get(today(), 0)} min. "
          f"Esta semana: {sum(efectivos(s) for s in sem) + act_sem} min "
          f"({len(sem)} sesiones{sueltos}).")

    mxd = minutos_externos_por_dia()
    ext_sem = [r for r in externos()
               if r["tipo"] not in TIPOS_ACTIVOS
               and date.fromisoformat(r["fecha"]).isocalendar()[:2] == (y, w)]
    if mxd:
        print(f"Estudio autonomo (aparte, no es practica): hoy {mxd.get(today(), 0)} min, "
              f"esta semana {sum(r['minutos'] for r in ext_sem)} min.")
        if mxd.get(today()) and not mpd.get(today()):
            print("  Hoy hubo contacto pero todavia ninguna recuperacion activa.")

    ss = cerradas()
    if ss:
        u = ss[-1]
        print(f"\nUltima sesion: {u['id']} ({u['modo']}, {efectivos(u)} min, "
              f"temas: {', '.join(u['temas']) or '-'})")
        if u.get("sigue"):
            print(f"  Dejaste anotado: {u['sigue']}")
    else:
        print("\nNo hay sesiones completas todavia. Esta seria la primera.")

    print(f"\nModo sugerido: {sugerir_modo(ahora)}. Preguntaselo antes de arrancar.")


def sugerir_modo(ahora) -> str:
    """Sugiere un presupuesto de tiempo a partir del reloj y del dia.

    La hora sola no alcanza: hasta el 2026-09-19 la regla era "micro antes de las 18:00",
    y esa manana era un sabado. El proxy que se queria medir no es la hora, es cuanta ventana
    sin interrupciones tiene, y la hora solo lo aproxima bien de lunes a viernes, porque
    trabaja full time. El fin de semana la manana es la ventana mas ancha de la semana y la
    regla vieja la gastaba en una micro.

    Entre semana de noche existe `media` porque viene de un dia entero de trabajo: proponer
    45-90 min ahi hace que la sesion no ocurra, y una sesion que no ocurre pierde contra una
    mas corta que si ocurre (Cepeda et al. 2006: lo que sostiene la retencion es la
    distribucion en el tiempo, no la duracion de cada bloque).

    Es una sugerencia, no una decision: las reglas de contenido de AGENTS.md la pisan, y el
    tiene la ultima palabra.
    """
    finde = ahora.weekday() >= 5
    if ahora.hour >= 22:
        return "micro (es tarde)"
    if finde:
        return "fondo (finde, ventana ancha)" if ahora.hour < 20 else "media"
    if ahora.hour < 18:
        return "micro (dia laboral)"
    return "media (post-jornada; fondo si dice que tiene la ventana)"


def cmd_metricas(args) -> None:
    ss = cerradas()
    sin_bitacora = incompletas()

    print("=" * 58 + "\n  METRICAS\n" + "=" * 58)
    if not ss:
        print("\nTodavia no hay sesiones completas registradas.")
        if sin_bitacora:
            print(f"Hay {len(sin_bitacora)} sesion(es) sin bitacora.")
        return

    mpd = minutos_por_dia()
    total = sum(mpd.values())
    print(f"\nRacha actual: {racha()} dia(s) seguidos")
    sueltos = sum(minutos_activos_sueltos().values())
    detalle = f" ({sueltos} de ellos sueltos, fuera de sesion)" if sueltos else ""
    print(f"Practica: {total} min, {len(ss)} sesiones "
          f"({round((total - sueltos) / len(ss))} min promedio por sesion){detalle}")

    mxd = minutos_externos_por_dia()
    print("\nUltimos 14 dias  (# practica, . estudio autonomo):")
    for i in range(13, -1, -1):
        d = today() - timedelta(days=i)
        m, x = mpd.get(d, 0), mxd.get(d, 0)
        barra = "#" * min(30, m // 5) + "." * min(30, x // 5)
        extra = f"  +{x} ext" if x else ""
        print(f"  {d.isoformat()} {m:>4} min {barra}{extra}"
              f"{'  <- hoy' if i == 0 else ''}")

    semanas, sesiones_semana = defaultdict(int), defaultdict(int)
    for s in ss:
        y, w, _ = parse_dt(s["iniciada"]).date().isocalendar()
        semanas[(y, w)] += efectivos(s)
        sesiones_semana[(y, w)] += 1
    print("\nPor semana (ultimas 8):")
    for k in sorted(semanas)[-8:]:
        print(f"  {k[0]}-S{k[1]:02d}  {semanas[k]:>4} min  {sesiones_semana[k]} sesiones")

    por_modo = defaultdict(lambda: [0, 0])
    for s in ss:
        por_modo[s["modo"]][0] += 1
        por_modo[s["modo"]][1] += efectivos(s)
    print("\nPor modo:")
    for modo, (n, m) in sorted(por_modo.items()):
        print(f"  {modo:<7} {n} sesiones, {m} min")

    ext = [r for r in externos() if r["tipo"] not in TIPOS_ACTIVOS]
    if ext:
        tot_x = sum(r["minutos"] for r in ext)
        print(f"\nEstudio autonomo: {tot_x} min en {len(ext)} registro(s). "
              f"No esta sumado arriba.")
        por_tipo = defaultdict(lambda: [0, 0])
        for r in ext:
            por_tipo[r["tipo"]][0] += 1
            por_tipo[r["tipo"]][1] += r["minutos"]
        for tipo, (n, m) in sorted(por_tipo.items(), key=lambda kv: -kv[1][1]):
            print(f"  {tipo:<9} {n} registro(s), {m} min")
        solo_pasivos = sorted(set(mxd) - set(mpd))
        if solo_pasivos:
            print(f"  Dias de contacto sin practica: {len(solo_pasivos)} "
                  f"(ultimo: {solo_pasivos[-1].isoformat()})")
        print(f"  Proporcion: {round(100 * tot_x / (tot_x + total))}% del tiempo total "
              "fue exposicion, no recuperacion.")

    ejercicios = [e for s in ss for e in s.get("ejercicios", [])]
    if ejercicios:
        solo = sum(1 for e in ejercicios if e["resultado"] == "solo")
        pistas = sum(1 for e in ejercicios if e["resultado"] == "con_pistas")
        aband = sum(1 for e in ejercicios if e["resultado"] == "abandonado")
        print(f"\nEjercicios: {len(ejercicios)} intentados")
        print(f"  resueltos solo:       {solo:>3}  ({round(100 * solo / len(ejercicios))}%)")
        print(f"  resueltos con pistas: {pistas:>3}")
        print(f"  abandonados:          {aband:>3}")
        cp = [e for e in ejercicios if e["resultado"] == "con_pistas" and e.get("pista_max")]
        if cp:
            print(f"  nivel de pista promedio cuando pediste ayuda: "
                  f"{sum(e['pista_max'] for e in cp) / len(cp):.1f}/5")
    else:
        print("\nEjercicios: ninguno registrado todavia.")

    revs = [h for c in cards_db()["cards"] for h in c["historial"]]
    if revs:
        ok = sum(1 for h in revs if h["calidad"] >= 3)
        print(f"\nTarjetas: {len(revs)} repasos, precision {round(100 * ok / len(revs))}%")
        corte = (today() - timedelta(days=7)).isoformat()
        rec = [h for h in revs if h["fecha"] >= corte]
        if rec:
            ok7 = sum(1 for h in rec if h["calidad"] >= 3)
            print(f"  ultimos 7 dias: {len(rec)} repasos, precision {round(100 * ok7 / len(rec))}%")
        print(f"  vencidas hoy: {len(due_cards())}")
    else:
        print("\nTarjetas: ningun repaso registrado todavia.")

    preds_ej = [e for s in ss for e in s.get("ejercicios", [])
                if e.get("prediccion") and e["prediccion"] != "no-preguntada"]
    preds_tar = [r for s in ss for r in s.get("repasos", [])
                 if r.get("prediccion") and r["prediccion"] != "no-preguntada"]
    if preds_ej or preds_tar:
        print("\nCalibracion (lo que predijiste contra lo que paso):")
    if preds_ej:
        ok = sum(1 for e in preds_ej if e["prediccion"] == e["resultado"])
        sobre = sum(1 for e in preds_ej if e["prediccion"] == "solo" and e["resultado"] != "solo")
        sub = sum(1 for e in preds_ej
                  if e["prediccion"] == "no_lo_saco" and e["resultado"] != "abandonado")
        print(f"  ejercicios: {ok}/{len(preds_ej)} acertados "
              f"({round(100 * ok / len(preds_ej))}%), {sobre} sobreestimados, {sub} subestimados")
    if preds_tar:
        dijo_si = [r for r in preds_tar if r["prediccion"] == "si"]
        dijo_no = [r for r in preds_tar if r["prediccion"] == "no"]
        if dijo_si:
            fallo = sum(1 for r in dijo_si if r["calidad"] < 3)
            print(f"  tarjetas que dijiste saber: {len(dijo_si)}, fallaste {fallo} "
                  f"({round(100 * fallo / len(dijo_si))}% de sobreconfianza)")
        if dijo_no:
            acerto = sum(1 for r in dijo_no if r["calidad"] >= 3)
            print(f"  tarjetas que dijiste no saber: {len(dijo_no)}, acertaste {acerto}")

    patrones = [x for s in ss for x in s.get("patrones", [])]
    if patrones:
        ok = sum(1 for x in patrones if x["acerto"])
        print(f"\nReconocimiento de patron: {ok}/{len(patrones)} "
              f"({round(100 * ok / len(patrones))}%)")
        fallos = defaultdict(int)
        for x in patrones:
            if not x["acerto"]:
                fallos[x["tema"]] += 1
        if fallos:
            peor = sorted(fallos.items(), key=lambda kv: -kv[1])[:3]
            print("  mas fallados: " + ", ".join(f"{k} ({v})" for k, v in peor))
        confusiones = defaultdict(int)
        for x in patrones:
            if not x["acerto"] and x.get("dijo"):
                confusiones[(x["dijo"], x["tema"])] += 1
        if confusiones:
            print("  confusiones (dijo -> era):")
            for (dijo, era), n in sorted(confusiones.items(), key=lambda kv: -kv[1])[:5]:
                print(f"    {dijo} -> {era}  x{n}")

    errores = defaultdict(lambda: {"n": 0, "ultimo": ""})
    for s in ss:
        d = parse_dt(s["iniciada"]).date().isoformat()
        for e in s.get("ejercicios", []):
            for cls in e.get("errores", []):
                errores[cls]["n"] += 1
                if d > errores[cls]["ultimo"]:
                    errores[cls]["ultimo"] = d
    if errores:
        print("\nClases de error (lo que se repite entre temas):")
        for cls, d in sorted(errores.items(), key=lambda kv: -kv[1]["n"]):
            print(f"  {cls:<24} {d['n']:>3}  ultimo: {d['ultimo']}")

    resumen = resumen_por_tema()
    if resumen:
        print(f"\nPor tema ({len(resumen)} con actividad). Sin puntaje compuesto: "
              "cada columna es lo que se midio, no una estimacion de dominio.")
        print(f"  {'tema':<22} {'ejerc':>6} {'s/ayuda':>8} {'repasos':>8} {'aciertos':>9}  ultimo")
        for tid, d in sorted(resumen.items(), key=lambda kv: kv[1]["ultimo"], reverse=True):
            print(f"  {tid:<22} {d['ejercicios']:>6} {d['sin_ayuda']:>8} "
                  f"{d['repasos']:>8} {d['aciertos']:>9}  {d['ultimo']}")

    contacto = ultimo_contacto()
    frios = [(t, f) for t, f in contacto.items()
             if (today() - date.fromisoformat(f)).days >= 21]
    if frios:
        print("\nTemas tocados y frios hace 21 dias o mas:")
        for t, f in sorted(frios, key=lambda x: x[1]):
            print(f"  {t} (ultimo: {f})")

    print("\nCompara esto contra base/temario.md para juzgar cobertura.")
    if sin_bitacora:
        print(f"\n{len(sin_bitacora)} de {len(ss)} sesion(es) sin bitacora. Cuentan para tiempo y "
              "racha; lo que falta es el registro cualitativo de que paso.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="study.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("estado").set_defaults(func=cmd_estado)
    sub.add_parser("metricas").set_defaults(func=cmd_metricas)

    s = sub.add_parser("sesion")
    ss_ = s.add_subparsers(dest="sub", required=True)

    a = ss_.add_parser("iniciar")
    a.add_argument("--modo", required=True, choices=MODES)
    a.add_argument("--tema", default=None)
    a.set_defaults(func=cmd_iniciar)

    b = ss_.add_parser("ejercicio")
    b.add_argument("--ejercicio", required=True)
    b.add_argument("--tema", required=True)
    b.add_argument("--resultado", required=True, choices=RESULTS)
    b.add_argument("--pista-max", type=int, default=0, dest="pista_max")
    b.add_argument("--prediccion", required=True,
                   choices=["solo", "con_pistas", "no_lo_saco", "no-preguntada"])
    b.add_argument("--error-clase", default=None, dest="error_clase",
                   help="etiquetas kebab-case separadas por coma")
    b.set_defaults(func=cmd_ejercicio)

    bp = ss_.add_parser("patron")
    bp.add_argument("--problema", required=True)
    bp.add_argument("--tema", required=True)
    bp.add_argument("--dijo", required=True, help="lo que dijo el usuario, textual")
    bp.add_argument("--valido", required=True, choices=["si", "no"],
                    help="juicio del asistente: el enfoque es defendible, aunque no sea el canonico")
    bp.set_defaults(func=cmd_patron)

    c = ss_.add_parser("repaso")
    c.add_argument("--tarjeta", required=True)
    c.add_argument("--calidad", type=int, required=True)
    c.add_argument("--prediccion", required=True, choices=["si", "no", "no-preguntada"])
    c.set_defaults(func=cmd_repaso)

    ce = ss_.add_parser("eventos", help="lista numerada de lo registrado, para corregir")
    ce.add_argument("--sesion", default=None,
                    help="id de una sesion cerrada; por defecto, la abierta")
    ce.set_defaults(func=cmd_eventos)

    cc = ss_.add_parser("corregir", help="corrige un campo de un evento ya registrado")
    cc.add_argument("--evento", type=int, default=None,
                    help="numero que muestra 'sesion eventos'; sin esto se corrige "
                         f"un campo de la sesion ({', '.join(CAMPOS_SESION)})")
    cc.add_argument("--campo", required=True)
    cc.add_argument("--valor", required=True)
    cc.add_argument("--motivo", required=True,
                    help="por que se corrige; queda guardado junto al valor anterior")
    cc.add_argument("--sesion", default=None,
                    help="id de una sesion cerrada; por defecto, la abierta")
    cc.set_defaults(func=cmd_corregir)

    ss_.add_parser("pausar").set_defaults(func=cmd_pausar)
    ss_.add_parser("reanudar").set_defaults(func=cmd_reanudar)

    d = ss_.add_parser("cerrar")
    d.add_argument("--bitacora", default=None)
    d.add_argument("--sigue", default=None)
    d.add_argument("--sin-bitacora", action="store_true", dest="sin_bitacora")
    d.add_argument("--afk", type=int, default=0,
                   help="minutos AFK declarados a posteriori, cuando no se uso pausar/reanudar")
    d.set_defaults(func=cmd_cerrar)

    t = sub.add_parser("tarjetas")
    ts = t.add_subparsers(dest="sub", required=True)

    e = ts.add_parser("agregar")
    e.add_argument("--archivo", required=True)
    e.set_defaults(func=cmd_agregar)

    g = ts.add_parser("retirar")
    g.add_argument("--tarjeta", required=True)
    g.add_argument("--motivo", required=True,
                   help="por que sale de circulacion; queda guardado con la tarjeta")
    g.set_defaults(func=cmd_retirar)

    ed = ts.add_parser("editar", help="corregir la REDACCION de una tarjeta, sin perder su historial")
    ed.add_argument("--tarjeta", required=True)
    ed.add_argument("--frente")
    ed.add_argument("--dorso")
    ed.add_argument("--tema")
    ed.add_argument("--motivo", required=True,
                    help="que se cambio y por que; queda guardado en 'ediciones'")
    ed.set_defaults(func=cmd_editar)

    ts.add_parser("retiradas").set_defaults(func=cmd_retiradas)

    f = ts.add_parser("vencidas")
    f.add_argument("--limite", type=int, default=None)
    f.add_argument("--todas", action="store_true")
    f.set_defaults(func=cmd_vencidas)

    x = sub.add_parser("externo", help="estudio autonomo fuera de sesion: video, lectura, curso")
    xs = x.add_subparsers(dest="sub", required=True)

    xa = xs.add_parser("agregar")
    xa.add_argument("--minutos", type=int, required=True)
    xa.add_argument("--fuente", required=True,
                    help="URL o titulo. Indexala tambien en base/fuentes.md")
    xa.add_argument("--tipo", choices=TIPOS_EXTERNO, default="video")
    xa.add_argument("--tema", default=None, help="tema canonico, si aplica a uno solo")
    xa.add_argument("--fecha", default=None, help="AAAA-MM-DD; por defecto hoy")
    xa.add_argument("--nota", default=None, help="que se llevo de ahi, en una linea")
    xa.set_defaults(func=cmd_externo_agregar)

    xl = xs.add_parser("listar")
    xl.add_argument("--limite", type=int, default=None)
    xl.set_defaults(func=cmd_externo_listar)

    xn = xs.add_parser("anular")
    xn.add_argument("--id", required=True)
    xn.add_argument("--motivo", required=True)
    xn.set_defaults(func=cmd_externo_anular)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
