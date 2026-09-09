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

STALE_HOURS = 4
# Tope por defecto de tarjetas vencidas por sesion, para que una pausa no genere un muro.
TOPE_VENCIDAS = 20
RESULTS = ("solo", "con_pistas", "abandonado")
MODES = ("micro", "fondo")


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
        die("no hay sesion abierta. Corre: study.py sesion iniciar --modo micro|fondo")
    return cur


def last_activity(cur: dict) -> datetime:
    return max(parse_dt(s) for s in [cur["iniciada"]] + [e["ts"] for e in cur.get("eventos", [])])


def is_stale(cur: dict) -> bool:
    return (now() - last_activity(cur)) > timedelta(hours=STALE_HOURS)


def push_event(cur: dict, event: dict) -> None:
    event["ts"] = now().isoformat(timespec="seconds")
    cur.setdefault("eventos", []).append(event)
    save(CURRENT_FILE, cur)


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


def cmd_cerrar(args) -> None:
    cur = require_current()
    started = parse_dt(cur["iniciada"])
    ended = last_activity(cur) if is_stale(cur) else now()
    minutos = max(1, round((ended - started).total_seconds() / 60))

    bitacora = None
    if args.bitacora:
        bpath = Path(args.bitacora)
        bpath = bpath if bpath.is_absolute() else ROOT / bpath
        if not bpath.exists():
            die(f"la bitacora {args.bitacora} no existe. Escribila antes de cerrar la sesion.")
        bitacora = str(bpath.relative_to(ROOT))
    elif not args.sin_bitacora:
        die("falta --bitacora RUTA. Sin bitacora la sesion no cuenta; "
            "usa --sin-bitacora para dejarla incompleta.")

    eventos = cur.get("eventos", [])
    record = {
        "id": cur["id"],
        "modo": cur["modo"],
        "iniciada": cur["iniciada"],
        "terminada": ended.isoformat(timespec="seconds"),
        "minutos": minutos,
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

    print(f"Sesion {record['id']} cerrada: {minutos} min reales, "
          f"{len(record['ejercicios'])} ejercicios, {len(record['repasos'])} repasos, "
          f"estado {record['estado']}.")
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
    vencidas = [c for c in cards_db()["cards"] if c["sm2"]["due"] <= hoy]
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


# ----------------------------------------------------------------- agregado

def completas() -> list:
    return [s for s in sessions() if s.get("estado") == "completa"]


def racha() -> int:
    dias = {parse_dt(s["iniciada"]).date() for s in completas()}
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
    acc = defaultdict(int)
    for s in completas():
        acc[parse_dt(s["iniciada"]).date()] += s["minutos"]
    return acc


def ultimo_contacto() -> dict:
    """tema -> fecha del ultimo evento registrado sobre ese tema."""
    acc = {}
    for s in completas():
        d = parse_dt(s["iniciada"]).date().isoformat()
        for tema in s.get("temas", []):
            if tema not in acc or d > acc[tema]:
                acc[tema] = d
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
    for s in completas():
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
    sem = [s for s in completas() if parse_dt(s["iniciada"]).date().isocalendar()[:2] == (y, w)]
    print(f"\nRacha: {racha()} dia(s). Hoy: {mpd.get(today(), 0)} min. "
          f"Esta semana: {sum(s['minutos'] for s in sem)} min en {len(sem)} sesiones.")

    ss = completas()
    if ss:
        u = ss[-1]
        print(f"\nUltima sesion: {u['id']} ({u['modo']}, {u['minutos']} min, "
              f"temas: {', '.join(u['temas']) or '-'})")
        if u.get("sigue"):
            print(f"  Dejaste anotado: {u['sigue']}")
    else:
        print("\nNo hay sesiones completas todavia. Esta seria la primera.")

    print(f"\nModo sugerido por hora: {'micro' if ahora.hour < 18 else 'fondo'}. "
          "Preguntaselo antes de arrancar.")


def cmd_metricas(args) -> None:
    ss = completas()
    incompletas = [s for s in sessions() if s.get("estado") != "completa"]

    print("=" * 58 + "\n  METRICAS\n" + "=" * 58)
    if not ss:
        print("\nTodavia no hay sesiones completas registradas.")
        if incompletas:
            print(f"Hay {len(incompletas)} sesion(es) cerradas sin bitacora, que no cuentan.")
        return

    mpd = minutos_por_dia()
    total = sum(mpd.values())
    print(f"\nRacha actual: {racha()} dia(s) seguidos")
    print(f"Total: {total} min en {len(ss)} sesiones ({round(total / len(ss))} min promedio)")

    print("\nUltimos 14 dias:")
    for i in range(13, -1, -1):
        d = today() - timedelta(days=i)
        m = mpd.get(d, 0)
        print(f"  {d.isoformat()} {m:>4} min {'#' * min(30, m // 5)}"
              f"{'  <- hoy' if i == 0 else ''}")

    semanas, sesiones_semana = defaultdict(int), defaultdict(int)
    for s in ss:
        y, w, _ = parse_dt(s["iniciada"]).date().isocalendar()
        semanas[(y, w)] += s["minutos"]
        sesiones_semana[(y, w)] += 1
    print("\nPor semana (ultimas 8):")
    for k in sorted(semanas)[-8:]:
        print(f"  {k[0]}-S{k[1]:02d}  {semanas[k]:>4} min  {sesiones_semana[k]} sesiones")

    por_modo = defaultdict(lambda: [0, 0])
    for s in ss:
        por_modo[s["modo"]][0] += 1
        por_modo[s["modo"]][1] += s["minutos"]
    print("\nPor modo:")
    for modo, (n, m) in sorted(por_modo.items()):
        print(f"  {modo:<7} {n} sesiones, {m} min")

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
    if incompletas:
        print(f"{len(incompletas)} sesion(es) sin bitacora. No cuentan para racha ni minutos.")


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

    d = ss_.add_parser("cerrar")
    d.add_argument("--bitacora", default=None)
    d.add_argument("--sigue", default=None)
    d.add_argument("--sin-bitacora", action="store_true", dest="sin_bitacora")
    d.set_defaults(func=cmd_cerrar)

    t = sub.add_parser("tarjetas")
    ts = t.add_subparsers(dest="sub", required=True)

    e = ts.add_parser("agregar")
    e.add_argument("--archivo", required=True)
    e.set_defaults(func=cmd_agregar)

    f = ts.add_parser("vencidas")
    f.add_argument("--limite", type=int, default=None)
    f.add_argument("--todas", action="store_true")
    f.set_defaults(func=cmd_vencidas)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
