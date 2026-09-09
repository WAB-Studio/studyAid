# Sistema de estudio para entrevistas

Preparación para entrevistas de big tech. Ejercicios en TypeScript, resueltos en leetcode.com.

## Cómo se usa

Abrí Claude Code en esta carpeta y decí cualquier cosa. Un "hola" alcanza.

Yo leo el estado, veo qué tarjetas están vencidas y en qué quedamos, y te propongo qué hacer hoy.
Vos decís "listo" y arrancamos. No hay comandos que recordar.

Si preguntás algo que no es estudiar, te contesto eso y nada más.

## Los dos modos

**Micro** (10–15 min): tarjetas vencidas, ejercicios cortos o drill de reconocimiento de patrones.
Para ratos muertos. Se puede cortar a la mitad sin perder nada.

**Fondo** (45–90 min): tema nuevo, ejercicio largo, o medición. Para la noche.

Yo propongo uno según la hora y lo pendiente, pero siempre pregunto antes.

## Cómo trabajo

No te resuelvo los ejercicios. Mientras estás resolviendo doy la ayuda mínima que te devuelva
avance, y escalo sólo si sigue haciendo falta. Si el hueco es que te falta un concepto, te lo
enseño derecho en vez de darte pistas al costado.

Cada tema nuevo termina con vos explicándomelo con tus palabras. De ahí salen las tarjetas.

Cada sesión termina con una bitácora: qué hiciste, qué falló, qué sigue.

## Pendiente antes de empezar

**Ejecutar la forma A de `base/linea-base.md`** — unos 70 minutos. Es una medición de tu nivel de
partida: seis clasificaciones de enfoque, un problema de código sin ayuda y un ejercicio de diseño.
Sin eso, en dos meses no vamos a poder saber si mejoraste. La forma B queda reservada para repetir
la medición a las 4–6 semanas.

## Dónde está qué

```
CLAUDE.md          cómo trabajo yo
base/              perfil, temario, un archivo por tema, línea base, fuentes
bitacora/          una entrada por día
data/              tarjetas SM-2 y log de sesiones (los escribe la tool, no a mano)
tools/study.py     reloj, SM-2 y métricas
.claude/skills/    codigo, system-design, fuentes, metricas, teoria-del-aprendizaje
referencia/        repos ajenos de los que salió parte del método
```

## Si querés mirar sin mí

```bash
.venv/bin/python tools/study.py estado      # vencidas, racha, en qué quedamos
.venv/bin/python tools/study.py metricas    # minutos, racha, ejercicios, calibración, por tema
```

El venv no tiene dependencias: es stdlib. Si se rompe, `python3 -m venv .venv` y listo.
