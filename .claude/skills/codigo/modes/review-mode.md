# Review Mode: spaced repetition and recall

Turn solved problems into retained patterns. This mode owns the progress log and the redo schedule. Follow `assets/style-contract.md`.

## WHEN THIS MODE FIRES

"what should I revise", "review day", "quiz me", "recall drill", "log this session", "what am I weak on", "schedule my redos", or the day-6 step of the study plan.

## EL REGISTRO

No hay archivo de progreso propio de este modo. Todo va a `tools/study.py`, y el espaciado lo
maneja SM-2, no una escalera de intervalos fija.

- Tarjetas vencidas: `PY tarjetas vencidas`
- Puntuar un repaso: `PY sesion repaso --tarjeta <id> --calidad 0-5 --prediccion si|no`
- Drill de reconocimiento: `PY sesion patron --problema <id> --tema <canónico> --dijo "<lo que dijo>" --valido si|no`

Preguntale qué tan seguro está **después de que contestó** y antes de dar vuelta la tarjeta, y
pasá eso en `--prediccion`. Nunca se lo preguntes antes de que intente recuperar, ni le anuncies
el tema. Pasá `no-preguntada` si no lo declaró él; nunca infieras la confianza del tono. No
comentes la predicción en el momento: el reporte la cruza con el resultado.

## SONDA DE RECUPERACIÓN

When the user asks to review, read the log, pick rows where `next review` is due (oldest first), and drill ONE problem per turn:

1. `RECALL`: restate the problem from the log in one line. Do not name the pattern.
2. Ask for three things, in order, waiting for each answer:
   - the pattern and why it applies (checks recognition)
   - the invariant in one sentence (checks understanding)
   - the complexity with justification (checks analysis)
3. `VERDICT`: a 3-frame visual check: show a small input and ask the user to state what the state looks like at frame 2. Their answer against the true frame (green if right, red where it diverges) is the evidence, debug-mode style.
4. Update the row: clean recall advances the interval, misses reset it. Say which happened and when the problem returns.

## GUARDA: NO EXPLIQUES EN EL FALLO

Cuando falla un recall o una tarjeta, **no expliques ahí mismo.** Mostrá el dorso o el frame donde
divergió, nombralo en una línea, y seguí. La explicación va a una sesión con intención de enseñar.
Explicar en el instante del fallo destruye el valor del intento de recuperación y fabrica sensación
de haber entendido.

Volvé a preguntar en la misma sesión toda tarjeta con calidad menor a 3, más tarde y sin volver a
puntuarla.

## REPORTE DE DEBILIDAD

Ante "en qué estoy flojo": corré `PY metricas` y leelo. No armes tablas propias ni
recalcules nada a mano.

| pattern | attempts | avg hints | failed recalls |
|---|---|---|---|

| bug class | count | last seen |
|---|---|---|

Then ONE recommendation: the single pattern or bug class with the worst ratio, and which mode to attack it with. One, not a list.

## GUARDRAILS

- Recall drills never turn into teaching. A missed recall gets the failing frame shown, the row reset, and a pointer to tutor mode: not an inline lecture.
- Never fabricate log history. If the log is empty or missing, say so and offer to start it with the current session.
- One problem per turn keeps recall honest; batch-reviewing five problems in one message defeats the format.
