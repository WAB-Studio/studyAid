# Plan de fusión: algotrace + swe-interview-coach sobre nuestro sistema

Fecha: 2026-09-09. Basado en la lectura completa de los 41 archivos de
`.claude/skills/algotrace/`, los 62 de `referencia/swe-interview-coach/`, y el sistema actual
(`CLAUDE.md`, `tools/study.py`, `base/`, las cuatro skills propias).

No es un ensayo comparativo. Cada recomendación dice: de dónde sale, a qué archivo nuestro va,
qué principio la respalda, y qué se rompe si no la ponemos.

---

## 0. Cómo leer este documento

### Los tres niveles

Todo mecanismo del ecosistema cae en uno de tres niveles. Lo digo explícito en cada caso porque
la mayor parte de los dos repos —y parte del nuestro— se queda en el primero.

- **Retórica**: el archivo lo nombra. Depende de que el agente se acuerde en el turno 40.
- **Mecanismo**: el sistema obliga a cumplirlo. Un comando falla, un gate corta, un archivo no
  se puede cerrar sin el dato.
- **Medición**: queda registro de si funcionó, agregable en el tiempo.

### La base de evidencia

Dunlosky et al. 2013 evalúa **cómo estudiar material declarativo**. El usuario está adquiriendo
una **habilidad procedimental con transferencia**: dado un enunciado nuevo, reconocer qué técnica
aplica. Esa es otra literatura, y es la más pertinente acá. Uso ambas y digo cuál respalda qué:

| Sigla | Línea | Referencias |
|---|---|---|
| **INT** | Intercalado y discriminación | Rohrer & Taylor 2007; Rohrer, Dedrick & Stershic 2015 |
| **WE** | Ejemplos resueltos, carga cognitiva, reversión por pericia | Sweller & Cooper 1985; Kalyuga et al. 2003; Renkl (desvanecimiento) |
| **FB** | Timing del feedback | Butler, Karpicke & Roediger 2007; Kulik & Kulik 1988 |
| **CAL** | Calibración e ilusión de fluidez | Koriat & Bjork 2005 |
| **GEN** | Generación y pretesting con error | Slamecka & Graf 1978; Kornell, Hays & Bjork 2009 |
| **DD** | Dificultades deseables | Bjork & Bjork 2011 (almacenamiento vs recuperación) |
| **ESP** | Espaciado | Cepeda et al. 2006 |
| **TR** | Transferencia | Barnett & Ceci 2002 |
| **SE** | Autoexplicación | Chi et al. 1989, 1994 |
| **DP** | Práctica deliberada | Ericsson et al. 1993, **con** Macnamara, Hambrick & Oswald 2014 |
| **EST** | Estilos de aprendizaje | Pashler et al. 2008 |
| **DUN** | Dunlosky et al. 2013 | recuperación y distribuida = utilidad alta |

**Reglas de honestidad que me impuse**: no invento tamaños de efecto. Donde no estoy seguro, lo
digo. Y separo siempre lo que la evidencia respalda de lo que es criterio de diseño nuestro
(marcado como **[criterio propio]**).

### El criterio que gana sobre todos

**La adherencia gana a la optimalidad.** Trabaja full time y hace 3–4 sesiones de fondo por
semana. Un sistema que hace todas las semanas vale más que uno mejor en el papel que abandona en
tres. Cada recomendación tiene una línea de **Fricción**. Donde una mejora el aprendizaje pero
sube la fricción, lo digo con esa tensión adelante, no la recomiendo a secas.

---

## 1. Inventario: qué es real hoy en cada repo

### Nuestro sistema

| Mecanismo | Nivel | Nota |
|---|---|---|
| Reloj real de sesión | **Medición** | `study.py` mide, corta por inactividad a 4h. Sólido. |
| Gate de bitácora al cerrar | **Mecanismo** | `cerrar` falla si el archivo no existe. El gate más fuerte del sistema. |
| SM-2 en JSON | **Mecanismo + Medición** | Mal parametrizado para 6–12 meses (ver R9). |
| Calibración predicción/resultado | **Mecanismo parcial + Medición** | El flag es opcional: degrada en silencio si me olvido. |
| Drill intercalado de patrón | **Medición** | El comando existe; que la micro-sesión lo corra es retórica. |
| Guarda de no explicar en el fallo | **Mecanismo** | `study.py` imprime la orden en el momento exacto. Es la mejor implementación del repo. |
| Clases de error | **Medición** | Vocabulario libre: se fragmenta (ver §5). |
| Escalera de 5 pistas | **Retórica** + medición del nivel máximo | El nivel no está definido por problema: cada vez significa algo distinto. |
| "Nunca resuelvas el ejercicio" | **Retórica** | Y con una colisión activa contra el router de algotrace (ver R13). |
| Repartir tarjetas a lo largo de la sesión | **Retórica** | |

### algotrace

| Mecanismo | Nivel | Nota |
|---|---|---|
| Escalera de 5 pistas, un nivel por turno | **Retórica** | Bien especificada (observación → patrón → invariante → técnica → esqueleto). |
| Debug: probar el bug con un trace hasta el frame divergente | **Retórica** de alto valor | Es la mejor idea del repo. |
| Contrato de estilo visual | **Retórica** | Cuatro colores, sin decoración. Bien escrito, irrelevante para aprender. |
| Log de progreso `.algotrace/progress.md` | **Retórica** | "Offer, never nag": opcional por diseño. Con eso no hay medición. |
| Intervalos +3/+7/+21 | **Retórica** | Y `prompts/` dice 1/3/7/16/35. Se contradicen entre sí. |
| Reloj de interview-mode | **Retórica, y peor: inventado** | "No real clock exists — track elapsed time by phase budget". |
| Rúbrica de interview-mode | **Retórica** | 5 ejes 1–4, sin fuente de datos. |
| `scripts/testgen.py` | **Mecanismo** | El único código ejecutable del repo. Genera formas de caso borde. |
| Progress Score con barras ASCII | **Retórica disfrazada de medición** | Números sin referente. Lo peor del repo. |

### swe-interview-coach

| Mecanismo | Nivel | Nota |
|---|---|---|
| Reloj: `date +%s` antes de cada turno, "never guess times" | **Mecanismo** | Coincide con nuestra restricción dura. |
| Harness que corre el código y devuelve `{passed,total}` | **Mecanismo + Medición** | La única señal objetiva de corrección en los dos repos. |
| `library/coding/*.md`: escalera de pistas **por problema** | **Mecanismo** | Convierte la escalera genérica en algo reproducible. |
| `library/sysdesign/*.md`: 8 diseños canónicos con números | **Mecanismo** | El activo más valioso de los dos repos. |
| Session file obligatorio por comando | **Mecanismo + Medición** | El comando lo escribe, no se ofrece. |
| Marcador de yield entre persona y post-proceso | **Mecanismo** | Separa la entrevista del scoring. Idea limpia. |
| Split mock / practice (tono, pistas, reloj, curveball) | **Mecanismo** | Uniforme en los tres dominios. |
| `weak-patterns.md` tracker | **Medición débil** | Calcula "señal de debilidad" sobre 2–3 reps por sesión. Sin poder estadístico. |
| Rúbricas 6 ejes 1–5 | **Retórica con un eje anclado** | Sólo `correctness` sale del harness; los otros cinco son juicio del modelo. |
| Degradación elegante (sin runtime, sin canvas → seguí) | **Mecanismo** | Principio de adherencia bien implementado. |

**Conclusión del inventario**: swe-interview-coach tiene tres veces más mecanismos reales que
algotrace. algotrace tiene mejores ideas pedagógicas sueltas (la escalera, el trace probatorio,
el decodificador de jerga) y casi ninguna forma de obligarlas. Nosotros tenemos el mejor
sistema de medición de los tres y el peor catálogo de contenido.

---

## 2. Recomendaciones, por impacto esperado

### R1 — Separar el eje "soporte" del eje "duración": modo `simulacro`

**De dónde**: `referencia/swe-interview-coach/agents/coding-interviewer.md` y
`agents/sysdesign-interviewer.md`, tabla "Mode behavior" (mock: tono neutro, pistas rechazadas,
dos avisos de reloj, un follow-up, nunca enseñar; practice: tono cálido, pistas libres, sin
reloj). Uniforme en los tres dominios.

**A dónde**: `CLAUDE.md` §"Elegir el modo"; `tools/study.py` — agregar `simulacro` a `MODES`, o
un flag `--soporte guiado|simulacro` en `sesion iniciar`, propagado al registro de sesión y a
`metricas`.

**Qué lo respalda**:
- **DD** (Bjork & Bjork 2011): practicar en condiciones que se parecen al test construye fuerza
  de recuperación. Un ejercicio con un tutor disponible no es la condición del test.
- **Validez de medición [criterio propio]**: nuestro número titular —"resueltos solo"— hoy se
  mide en condiciones de soporte y se reporta como si predijera desempeño sin soporte. Es el
  problema más caro del sistema actual y no es de contenido, es de diseño experimental.

**Qué se rompe si no la ponemos**: `metricas` dice que "resueltos solo es la métrica que de
verdad mide si mejora". Hoy no lo mide: mide "resuelto solo mientras había alguien mirando que
podía intervenir". A los 6 meses vamos a tener una curva ascendente y ninguna evidencia de que
signifique algo.

**Fricción**: baja para él (no elige el modo, lo propongo yo). Media para el sistema: hay que
tocar `study.py`, el arranque y el reporte. Sugerencia de adherencia: **un simulacro por
semana**, no más — el simulacro es caro emocionalmente y si lo hacemos default se abandona.

---

### R2 — Forzar el paso de discriminación: candidatos → por qué descarto → por qué elijo

**De dónde**: `.claude/skills/algotrace/prompts/universal-system-prompt.md` §11 "Algorithm
Selection Matrix" (`Constraint → Candidate algorithms → Why reject each → Why choose one`) y el
comando `/why-not X`. Reforzado por la fase **Match** de UMPIRE en
`referencia/swe-interview-coach/skills/coding-frameworks/SKILL.md` (contraste débil/fuerte).

**A dónde**: `CLAUDE.md` §"Micro-sesión" (drill intercalado) y
`.claude/skills/algotrace/OVERRIDES.md` §"Drill intercalado de patrones". En `study.py`,
extender `sesion patron` con `--dijo <tema>` en vez de sólo `--acerto si|no`.

**Qué lo respalda**: **INT** — Rohrer & Taylor 2007 y Rohrer, Dedrick & Stershic 2015 son la
evidencia más directa que existe sobre la debilidad declarada número uno del usuario:
estudiaron problemas de matemática e midieron específicamente la capacidad de **identificar qué
tipo de problema es**, y el mecanismo propuesto es la discriminación entre problemas
superficialmente parecidos. Nombrar el patrón correcto no obliga a discriminar. Nombrar qué
*no* es y por qué, sí.

**Qué se rompe si no la ponemos**: el drill actual mide reconocimiento pero no lo entrena por el
mecanismo que la evidencia identifica. Y perdemos la matriz de confusión: saber que confunde
`sliding-window` con `prefix-sum` es infinitamente más accionable que saber que acierta 60%.

**Nota de diseño [criterio propio]**: los pares de confusión tienen que ser **curados**, no
aleatorios. `sliding-window` vs `prefix-sum`; `two-pointers` vs `binary-search`; `dp-1d` vs
`greedy`; `backtracking` vs `dfs`; `heap` vs `sort completo`. Mezclar temas lejanos es más fácil
de armar y enseña menos: la discriminación sólo se entrena donde hay algo que discriminar.

**Fricción**: +10–20 segundos por ítem del drill. La mejor relación valor/fricción del plan.

---

### R3 — Importar la biblioteca de system design (8 diseños canónicos)

**De dónde**: `referencia/swe-interview-coach/library/sysdesign/*.md` — url-shortener,
rate-limiter, twitter-feed, whatsapp-chat, uber-dispatch, video-streaming, notification-system,
distributed-kv-store. Ocho secciones fijas cada uno: Requirements, Capacity estimation,
High-level architecture, API design, Storage choices, Key components & deep dives, Common
tradeoffs, Curveballs.

**A dónde**: `.claude/skills/system-design/referencias/casos/<id>.md`, más un índice corto en
español en `.claude/skills/system-design/SKILL.md` (la sección "Casos para practicar" hoy lista
seis casos sin ningún contenido detrás).

**Qué lo respalda**:
- **WE** (Sweller & Cooper 1985): para un aprendiz novato en un dominio, estudiar ejemplos
  resueltos es más eficiente que resolver problemas. En system design el usuario está más cerca
  de novato que en algoritmos: es su hueco más grande y el que menos andamiaje tiene hoy.
- La calidad de estos archivos no es genérica: cada tradeoff está *steel-manned* (la opción no
  elegida se defiende bien antes de descartarse), y cada número está derivado de supuestos
  declarados. Eso es exactamente el comportamiento que queremos que él imite en la fase
  Estimation, que nuestro propio `SKILL.md` identifica como "la fase que más se saltea".

**Qué se rompe si no la ponemos**: nuestro `referencias/bloques.md` son dos páginas de
generalidades. Sin casos canónicos, cada sesión de sysdesign es una improvisación mía: sin
estándar fijo no hay forma de saber si mejoró entre marzo y septiembre. Y hoy nuestro
`system-design/SKILL.md` ya dice "Adaptado de kirilxd/swe-interview-coach": nos trajimos el
resumen y dejamos la sustancia.

**Caveat obligatorio — reversión por pericia (Kalyuga et al. 2003)**: el mismo ejemplo resuelto
que ayuda a un novato **estorba** a alguien con más pericia. Estos archivos tienen que
retirarse progresivamente. Regla concreta: primera vez con un tema, lee el caso entero;
segunda vez, sólo Requirements y produce él la estimación y los tradeoffs; tercera vez, sólo el
enunciado. Sin esa regla, a los cuatro meses el archivo lo está frenando.

**Fricción**: cero para él. Costo de importación una sola vez.

---

### R4 — Escalera de pistas *por problema*, no genérica

**De dónde**: `referencia/swe-interview-coach/library/coding/<id>.md`. Adoptamos **tres**
secciones: `## Clarifying questions to expect`, `## Hint ladder` (4 peldaños específicos del
problema), `## Follow-ups & variations`.

**Explícitamente NO adoptamos**: `## Reference solution`, `## Test cases`, `## Starter stub`.
Violan "nunca se le resuelve un ejercicio" y "los ejercicios se resuelven en leetcode.com y no
se replican en markdown". El enunciado tampoco se copia: sigue en LeetCode.

**A dónde**: `.claude/skills/algotrace/referencias-ts/problemas/<slug>.md`, empezando por los ~12
problemas marcados con `*` en `referencias-ts/problemas.md`.

**Qué lo respalda**: **WE / Renkl** — una escalera de pistas es guía desvanecida. Con una
escalera genérica de 5 niveles yo improviso el peldaño cada vez, y en la práctica improvisar
hacia abajo es fácil y hacia arriba es difícil: se termina dando de más. Una escalera escrita de
antemano es el mecanismo que convierte "un nivel por pedido" de retórica en mecanismo.

**Qué se rompe si no la ponemos**: la métrica "nivel de pista promedio" de `metricas/SKILL.md`
—que declaramos como señal de internalización— es ininterpretable, porque el nivel 3 significa
algo distinto en cada problema. Estamos promediando unidades que no son la misma unidad.

**Fricción**: cero para él. Costo de autoría para mí. Mitigación de adherencia: **escribirlas
perezosamente**, una por tema el día que se abre el tema, nunca las 12 de golpe.

---

### R5 — Fase de verificación: predecir la salida en casos borde ANTES de someter

**De dónde**: `prompts/universal-system-prompt.md` §16 ("only *after* the student has predicted
what each case should return. Predicting first is the skill; running is just confirmation") +
la fase **Review** de UMPIRE en `skills/coding-frameworks/SKILL.md` + las formas de caso borde
de `.claude/skills/algotrace/scripts/testgen.py` (`[]`, `[x]`, todos duplicados, ya ordenado,
ordenado al revés, negativos con cero, extremos de 32 bits).

**A dónde**: `CLAUDE.md` — un paso nuevo de cierre de ejercicio. La lista de formas de caso
borde, a `referencias-ts/patrones.md` o a un archivo propio.

**Qué lo respalda**:
- **GEN** (Slamecka & Graf 1978; Kornell, Hays & Bjork 2009): producir una respuesta antes de
  verla mejora el aprendizaje posterior, incluso cuando el intento falla.
- **CAL**: predecir y contrastar contra el veredicto de LeetCode es una señal de calibración a
  nivel ejercicio, complementaria a la que ya tenemos a nivel tarjeta.
- Ataca directamente "implementar sin bugs bajo presión", su debilidad declarada número tres,
  que hoy **ningún mecanismo del sistema toca**. `--error-clase` sólo se dispara cuando el bug
  ya ocurrió y yo lo noté.

**Qué se rompe si no la ponemos**: seguimos midiendo bugs a posteriori y nunca entrenamos la
anticipación, que es la habilidad que el entrevistador realmente evalúa cuando dice "dale, ahora
probalo".

**Fricción — la más alta del plan**: +2 a 4 minutos por ejercicio. Mitigación: **sólo en
sesiones de fondo, y tres casos, no cinco**. Si en tres semanas veo que corta ejercicios por
tiempo, este es el primer candidato a recortar.

---

### R6 — Sonda fría antes del bloque teórico (y la verdad sobre "teoría primero")

**De dónde**: no sale de ningún repo. Sale de la evidencia y choca con `base/perfil.md`.

**El problema**: `base/perfil.md` dice "Aprende con teoría primero: necesita el modelo mental
armado antes de practicar", y `CLAUDE.md` construyó el ritual de fondo alrededor de eso ("Abrí
con el modelo mental del tema antes de cualquier ejercicio").

**Hay que decirlo explícito**: eso es una **decisión de adherencia, no una decisión basada en
evidencia**. Pashler et al. 2008 revisó la hipótesis de emparejar la instrucción al estilo
autodeclarado y no encontró respaldo. Que él prefiera teoría primero es una razón legítima para
hacerlo —si es lo que lo hace sentarse un martes a las diez de la noche, vale— pero **no** es
razón para creer que produce mejor aprendizaje. Hoy el sistema lo trata como si fuera lo
segundo.

**Y además hay evidencia en contra del orden**: **GEN** — Kornell, Hays & Bjork 2009 muestra que
intentar y fallar *antes* de estudiar mejora el aprendizaje posterior. El orden preferido por la
evidencia está más cerca de: intento fallido corto → teoría → práctica.

**Cambio concreto y chico**: mantener el bloque teórico, pero anteponerle una **sonda de 5
minutos**: un problema del tema nuevo, sin ninguna ayuda, explícitamente encuadrado como "vas a
fallar, es a propósito, no se puntúa". Después la teoría. El tope de 15 minutos del bloque
teórico que ya está en `CLAUDE.md` es correcto y hay que defenderlo (carga cognitiva).

**Bonus**: la sonda también es un instrumento de calibración. Su perfil declara el riesgo de
"leer de más y practicar de menos", y **CAL** (Koriat & Bjork 2005, sesgo de previsión) dice que
esa ilusión se corrige con contacto con el resultado. La sonda es el contacto más barato.

**Fricción**: +5 minutos por tema nuevo (no por sesión). Baja en volumen, alta en incomodidad.
Riesgo de adherencia real: un fracaso forzado al inicio de cada tema desmotiva si se encuadra
mal. El encuadre no es opcional, es parte del mecanismo.

---

### R7 — Reconocimiento de patrón medido *bajo carga*, no sólo en el drill

**De dónde**: `referencia/swe-interview-coach/commands/debrief-coding.md` paso 2.2 ("Looking
back, which pattern(s) did it turn out to be?", capturado como slugs de la taxonomía) y el
`weak-patterns.md` tracker.

**A dónde**: `study.py` — agregar `--patron-dicho <tema>` a `sesion ejercicio`, comparado contra
`--tema`. En `metricas`, partir "Reconocimiento de patrón" en dos números: **en drill** y **en
ejercicio**.

**Qué lo respalda**: **TR** (Barnett & Ceci 2002). Un drill de 30 segundos donde sólo hay que
etiquetar, y un ejercicio frío de 40 minutos con carga de implementación encima, están separados
por varias dimensiones de contexto. Hoy medimos el extremo fácil y lo reportamos como si fuera
readiness. La transferencia lejana es difícil y no hay que asumirla.

**Qué se rompe si no la ponemos**: la métrica más importante del sistema —la de su debilidad
principal— se alimenta sólo de la condición más fácil.

**Fricción**: prácticamente cero. Ya le pregunto la predicción al arrancar el ejercicio; la
pregunta de patrón va en la misma frase.

---

### R8 — Ritual de restricciones antes de elegir enfoque

**De dónde**: `.claude/skills/algotrace/docs/constraints-to-complexity.md` (la tabla n → cota, y
el procedimiento: leé la restricción, tachá de la hoja de patrones todos los que no entran,
quedan 2–3, *recién ahí* leé la historia) + Appendix D del universal prompt + la fase
**Understand** de UMPIRE.

**A dónde**: `.claude/skills/algotrace/OVERRIDES.md`, una línea: antes de dar cualquier pista,
pedirle la fila de la tabla y qué patrones elimina. La tabla ya está en
`referencias-ts/big-o.md`; hoy está ahí y no se usa como ritual.

**Qué lo respalda**: **INT** — es discriminación operacionalizada en el dominio: reduce el
conjunto candidato *antes* de que él haga pattern-matching sobre la historia. Y **carga
cognitiva**: achica el espacio de búsqueda antes de la fase pesada.

**Qué se rompe si no la ponemos**: sigue emparejando por rasgos superficiales del enunciado, que
es el modo de falla clásico del novato y es literalmente "no reconozco el patrón".

**Nota de transferencia**: esto y R2 son, probablemente, **lo único del temario que transfiere
entre patrones**. Dominar sliding-window no transfiere a prefix-sum; leer restricciones, generar
candidatos y discriminar, sí. Por eso no son drills accesorios: son el contenido portante.

**Fricción**: ~30 segundos. La segunda mejor relación valor/fricción del plan.

---

### R9 — Reparametrizar SM-2 y el techo de dominio para un horizonte de 6–12 meses

**De dónde**: de ningún repo — los dos son peores que nosotros acá (algotrace propone +3/+7/+21
en un archivo y 1/3/7/16/35 en otro; swe-interview-coach no tiene espaciado en absoluto). Es una
corrección de evidencia sobre lo nuestro.

**A dónde**: `tools/study.py`:
1. `dominio_por_tema()` usa `min(c["sm2"]["interval"] / 21.0, 1.0)`. Ese 21 declara que un
   intervalo de tres semanas es dominio pleno.
2. `sm2()` arranca en 1 día, después 6, después `interval × ease`.

**Qué lo respalda**: **ESP** — Cepeda et al. 2006: el intervalo óptimo escala con el intervalo
de retención buscado. Con la entrevista a 6–12 meses, un sistema que satura el crédito de
retención a los 21 días va a dejar de programar justamente lo que necesita seguir sabiendo en el
mes nueve. **No estoy seguro de la proporción exacta** —la regla de "10–20% del intervalo de
retención" que se cita habitualmente es un resumen grueso de esa literatura, ajustado sobre
material declarativo, no procedimental—, así que no propongo una fórmula: propongo **subir el
techo a ~60 días** y revisar con datos reales en tres meses.

**Y una honestidad más**: SM-2 es una heurística de los años 80, no un hallazgo. Sus intervalos
son una decisión de diseño nuestra, no evidencia. Conviene que `teoria-del-aprendizaje/SKILL.md`
lo diga, porque hoy el sistema lo trata como si fuera canónico.

**Qué se rompe si no la ponemos**: a las tres semanas todos los temas se ven "sólidos", el
reporte le dice que avance, y la evidencia dice que para la fecha de la entrevista ya decayó.

**Fricción**: cero. Dos líneas.

---

### R10 — Desvanecimiento del ejemplo resuelto, con regla de retirada

**De dónde**: `referencia/swe-interview-coach/commands/coding-explain.md`, modo `problem`: enseña
la **derivación** (clarify → pattern-match → plan → complexity → edge cases → un follow-up) y
prohíbe explícitamente volcar la `## Reference solution` ("the whole point of explain is to
derive the approach, not hand over the code"). Más la escalera de profundidad de
`.claude/skills/algotrace/modes/tutor-mode.md`.

**A dónde**: `.claude/skills/algotrace/OVERRIDES.md` §"Ejemplo resuelto de un patrón nuevo".
Hoy la regla es binaria: primera vez, ejemplo completo; después, nada. Sin condición de retirada.

**Etapas concretas**:
1. Primer contacto con el patrón: problema **distinto** resuelto de punta a punta (como hoy).
2. Segundo: el mismo ejemplo con los dos pasos difíciles en blanco — *problema de completar*.
3. Tercero en adelante: sólo la señal de reconocimiento. Si pide el ejemplo, eso es la señal de
   que el tema se abrió antes de tiempo, y se anota en `base/temas/<tema>.md`.

**Qué lo respalda**: **WE** en las tres referencias a la vez — Sweller & Cooper 1985 (el ejemplo
ayuda al novato), Renkl (desvanecer hacia problemas de completar), Kalyuga et al. 2003 (el mismo
ejemplo estorba cuando ya hay pericia).

**Qué se rompe si no la ponemos**: dos cosas opuestas y las dos malas — o lo sobre-apoyamos en el
mes 6, o lo dejamos sin andamiaje en la semana 1.

**Y acá está la tensión honesta del pliego de restricciones**: "nunca se le resuelve un
ejercicio" es una restricción dura y la respeto. Pero sin un contrapeso de ejemplos resueltos,
lo que queda es **descubrimiento puro**, y la literatura de carga cognitiva es bastante clara en
que eso es ineficiente para novatos. El ejemplo resuelto sobre *otro* problema es el
contrapeso, y por eso R10 no es un adorno: es lo que hace que la restricción sea sostenible.

---

### R11 — La sonda de recuperación como cierre estándar, con el trace producido por él

**De dónde**: `.claude/skills/algotrace/modes/review-mode.md`, RECALL DRILLS: patrón y por qué /
invariante en una oración / complejidad con justificación. Y el paso VERDICT: "show a small
input and ask the user to state what the state looks like at frame 2" — el trace lo produce
**él**, yo marco dónde diverge.

**A dónde**: `OVERRIDES.md` ya dice que la sonda "se mantiene tal cual", pero no está en
`CLAUDE.md` ni atada a ningún comando: es retórica pura. Mover al cierre de ejercicio en
`CLAUDE.md`, fusionada con R5 en un único ritual (patrón / invariante / complejidad / predicción
de tres casos borde).

**Qué lo respalda**: **SE** (Chi et al. 1989, 1994) — la autoexplicación funciona cuando la
produce el aprendiz. Enunciar el invariante es un acto generativo.

**Y acá hay que anular una regla de algotrace**: su contrato de estilo obliga a que *toda*
respuesta lleve un visual producido por el tutor. En modo tutor está bien. En recall es
directamente contraproducente: hace por él el trabajo generativo que estamos midiendo. El propio
algotrace se contradice en esto (review-mode le pide a él el frame 2, el style-contract se lo da
servido). Escribir en `OVERRIDES.md`: el visual lo produce el tutor en tutor-mode; en recall y
en debug lo produce él.

**Fricción**: +2 minutos, y se solapa con R5 y con "explicá con tus palabras". Por eso van
fusionados en un solo ritual de cierre, no en tres.

---

### R12 — Extender la guarda de feedback diferido a los ejercicios, con un corte

**De dónde**: `referencia/swe-interview-coach/agents/coding-interviewer.md`: en mock, "report
ONLY the raw pass/fail tally... NEVER diagnose the bug, name a line, or suggest the fix — that's
the candidate's job and post-processing's job, not yours".

**A dónde**: `OVERRIDES.md` §"No enseñar en el fallo", hoy alcanzado sólo a tarjetas y recall.

**Qué lo respalda**: **FB** — Butler, Karpicke & Roediger 2007; Kulik & Kulik 1988.

**Honestidad sobre esta evidencia**: la ventaja del feedback diferido **no es universal**. Es más
clara para retención de material conceptual evaluado después, y el panorama para adquisición de
habilidad procedimental es más mixto; hay un argumento razonable de que para un bug mecánico el
feedback inmediato es mejor. Así que propongo un corte, no una regla ciega:

- **Fallo conceptual** (patrón equivocado, invariante mal enunciado) → diferido a la próxima
  sesión de fondo, anotado en `--sigue`.
- **Bug mecánico** (off-by-one visto en un trace) → inmediato. Es más barato y es el caso donde
  la evidencia del diferido es más floja.

Este corte, además, es el que gana en adherencia: diferir *todo* es frustrante.

**Y hay que resolver una contradicción interna nuestra**: `CLAUDE.md` dice "No comentes la
predicción en el momento", pero `study.py` imprime "SOBRECONFIANZA: dijo que la sabía y falló"
al instante. Mi posición: **son objetos distintos y hay que separarlos**. El feedback de
*calibración* (acertaste o no tu propia predicción) conviene que sea inmediato — **CAL**, el
sesgo de previsión se corrige con contacto con el resultado, y no revela contenido. El feedback
de *contenido* es el que se difiere. Reescribir esa línea de `CLAUDE.md` con esa distinción.

---

### R13 — Follow-up de variación al cierre

**De dónde**: `## Follow-ups & variations` de cada entrada de `library/coding/`, los
`## Curveballs interviewers throw` de `library/sysdesign/`, y la Escalation Ladder del universal
prompt §17 ("reducí la complejidad", "y si es un stream", "y si no entra en memoria").

**A dónde**: cierre de ejercicio, verbal, sin código.

**Qué lo respalda**: **TR** parcialmente — variar la superficie manteniendo la estructura
profunda es la palanca estándar para transferencia. **Marco esto como criterio propio en buena
medida**: la evidencia sobre esta implementación concreta es más débil que la de R2 o R5, y
Barnett & Ceci advierten justamente que la transferencia lejana no se da sola.

**Fricción**: +1 minuto. Bajo costo, valor probable pero no probado.

---

## 3. Qué SACAR de lo que ya tenemos

### S1 — La colisión de `solution-mode` (urgente, es defensivo, no una ganancia)

`.claude/skills/algotrace/SKILL.md` línea 19 dice: *"a clear request for the complete solution
ALWAYS routes to solution-mode, **even mid-conversation in another mode**"*. Nuestro
`OVERRIDES.md` lo deshabilita. Pero la instrucción del router es más específica, más enfática y
está en el archivo que se carga primero. En una sesión larga esa es la que gana.

Es el único lugar del sistema donde una **restricción dura** está a una colisión de
instrucciones de romperse. Recomendación: **borrar `modes/solution-mode.md` y la fila del router**.
Eso obliga a relajar nuestra regla de "no edites los archivos del clon" — y hay que relajarla:
esa regla existe para facilitar un sync con upstream que nunca vamos a hacer. Cambiala en
`CLAUDE.md`.

### S2 — `docs/study-plan.md` (plan de 8 semanas, 90 min/día, 6 días/semana)

Contradice frontalmente `base/temario.md` y su disponibilidad real (full time, 3–4 sesiones de
fondo por semana, horizonte 6–12 meses). Dos planes en competencia en el mismo contexto
significa que voy a seguir el que tenga más cerca. Sacarlo o neutralizarlo en `OVERRIDES.md`.

**Rescatar antes de tirar**: su regla de escalada es buena y es una dificultad deseable bien
calibrada — *trabado menos de 20 minutos: no toques la skill; 20–30 minutos: pista nivel 1 o 2*.
Va a `OVERRIDES.md`.

### S3 — `prompts/universal-system-prompt.md` (31 KB)

Es el archivo más grande de algotrace, está escrito para ChatGPT y Gemini, y contiene tres cosas
que contradicen la evidencia o la honestidad de medición:

- §8 "Learning Style Detection" — emparejar instrucción a estilo inferido. **EST**: Pashler et
  al. 2008, sin respaldo.
- §9 "Your idea is approximately X% correct" — precisión fabricada. El número no tiene referente,
  y arriesga descalibrarlo justo en la dimensión que estamos midiendo. **Rescatar la
  estructura** (nombrar la parte correcta y la pieza faltante), **tirar el porcentaje**.
- §20 "Thinking Progress Score" con barras ASCII y porcentajes por dimensión sin fuente de
  datos. Es retórica disfrazada de medición y compite con `study.py metricas`, que sí mide.

**Cosechar antes de borrar**: §11 (matriz de selección → R2), §12 (tabla de invariantes por
patrón, buena y corta), §16 (verificación → R5), Apéndice B (misconceptions: "binary search
necesita array ordenado" → *necesita un predicado monótono"; "hash lookup es O(1)" → amortizado;
"greedy funciona porque se siente bien" → necesita argumento de intercambio), Apéndice D
(presupuesto de complejidad → R8).

### S4 — El sistema de progreso paralelo de `modes/review-mode.md`

`.algotrace/progress.md` con intervalos +3/+7/+21 ya está anulado por `OVERRIDES.md`, pero el
archivo sigue describiendo un segundo sistema de progreso completo. Neutralizarlo por nombre.
Su regla "Offer, never nag" es incompatible con nuestro gate de bitácora, y con razón: **el gate
gana**. Un log opcional produce cero medición.

### S5 — El contrato "todo response lleva un visual" en contextos de recall

Ver R11. Scoping, no borrado.

### S6 — Referencia rota

`.claude/skills/fuentes/SKILL.md` dice "No busques afuera para explicar un patrón que ya está en
`.claude/skills/leetcode/referencias/`". Ese path no existe: es `algotrace/referencias-ts/`.

### S7 — Descripción engañosa en `metricas/SKILL.md`

Dice que dominio combina "retención de tarjetas (40%), precisión en repasos (20%), ratio de
ejercicios resueltos solo (40%)". `study.py` renormaliza por `sum(pesos)`, así que si un tema no
tiene ejercicios registrados, las tarjetas pasan a pesar 100%. No está mal el código; está mal
la descripción, y esa descripción es la que uso para interpretarle el número.

---

## 4. Dónde se contradicen los dos repos entre sí

| Tema | algotrace | swe-interview-coach | Quién gana y por qué |
|---|---|---|---|
| **Reloj** | "No real clock exists — track elapsed by phase budget" (interview-mode) | `date +%s` antes de cada turno; "never guess times" | **swe-coach, sin discusión.** Coincide con nuestra restricción dura. algotrace directamente inventa el tiempo. |
| **Entregar la solución** | Escape hatch explícito; el README se enorgullece: "solution mode is one sentence away" | mock nunca da pistas ni muestra la referencia; practice camina la escalera | **swe-coach.** Y algotrace además contradice nuestra restricción dura (S1). |
| **Feedback en el fallo** | debug-mode: explicación elaborada inmediata sobre el frame divergente | mock: sólo pass/fail crudo, cero diagnóstico, todo al debrief | **swe-coach para lo conceptual, algotrace para lo mecánico** (R12). Ninguno de los dos hace el corte; nosotros sí. |
| **Espaciado** | +3/+7/+21 en `review-mode.md`; 1/3/7/16/35 en `prompts/`. **Se contradice consigo mismo.** | No tiene espaciado | **Ninguno.** Nuestro SM-2 es mejor que los dos, aunque mal parametrizado (R9). |
| **Registro** | "Offer, never nag" — opcional | El comando escribe el session file siempre | **swe-coach + nosotros.** La opcionalidad destruye la capa de medición entera. |
| **Puntuación** | Progress Score con barras y % sin fuente | Rúbrica 6 ejes 1–5 con una oración de evidencia cada uno; `correctness` anclado al harness | **swe-coach**, y nosotros por encima de los dos: `dominio_por_tema` sale de datos. |
| **Quién dibuja** | Contrato: el tutor dibuja siempre | practice: el agente escribe lo que él describe; mock: él dibuja y el agente sólo observa | **swe-coach.** Y algotrace se contradice consigo mismo (review-mode le pide el frame a él). |
| **Cadencia** | 90 min/día × 6 días × 8 semanas | Sin cadencia prescrita | **Ninguno sirve.** Nuestra realidad son 3–4 fondos por semana con horizonte de 6–12 meses. |

## 5. Dónde algún repo contradice la evidencia

- **algotrace, universal prompt §8**: emparejar instrucción a estilo de aprendizaje. **EST**
  (Pashler et al. 2008): sin respaldo. Y nos toca de cerca: nuestro `perfil.md` está construido
  alrededor de "aprende con teoría primero" (ver R6).
- **algotrace, universal prompt §9**: el porcentaje de corrección fabricado.
- **algotrace, `assets/style-contract.md`**: visual producido por el tutor en todo contexto,
  incluido el de recuperación. Contra **SE** (Chi): el trabajo generativo tiene que ser de él.
- **swe-coach, `commands/coding-drill.md` paso 4**: calcula "señal de debilidad" con la tasa de
  acierto de 2–3 reps de una sesión y la escribe en un tracker persistente. Sin poder
  estadístico. Nuestra agregación de `patron` sobre todas las sesiones es mejor.
- **swe-coach, rúbricas de 6 ejes**: cinco de los seis ejes son juicio del modelo presentado con
  la misma tipografía que el eje anclado al harness. No es fatal, pero hay que etiquetarlo si
  adoptamos algo parecido.
- **Los dos**: ninguno tiene recuperación espaciada de contenido de system design. Con horizonte
  de 6–12 meses eso es un agujero real, y también es nuestro: nuestra skill de system design
  registra ejercicios pero nunca genera tarjetas.

**Sobre práctica deliberada**: todo nuestro sistema está construido sobre el marco de Ericsson et
al. 1993 (apuntar a la debilidad, feedback, repetición, esfuerzo). El criterio de diseño es
sensato y barato. Pero Macnamara, Hambrick & Oswald 2014, en meta-análisis, encontró que la
práctica deliberada explica una porción **sustancialmente menor** de la varianza de desempeño de
lo que se afirma, y la menor de todas en dominios profesionales poco estructurados. **No cito
números porque no los puedo sostener con precisión.** La implicación práctica: `metricas` no
puede insinuar que la racha y los minutos sean la palanca causal. Hoy resiste bien esa tentación
("resueltos solo es la métrica que de verdad mide si mejora"); conviene agregarle una línea
explícita de que las horas son un insumo, no evidencia de progreso.

---

## 6. Sobre las cuatro cosas ya implementadas: están bien, pero

No las propongo de nuevo. Digo dónde están mal implementadas.

**Calibración predicción-contra-resultado**
- `--prediccion` es opcional (`default=None`): si me olvido, degrada en silencio y no queda
  rastro de que faltó. Debería ser requerido cuando el modo es `fondo`.
- Contradicción con `CLAUDE.md` (ya tratada en R12): separar calibración de contenido.
- Los tres números del reporte no particionan: `ok` usa igualdad exacta, así que predecir
  `con_pistas` y lograr `solo` cuenta como fallo de calibración; `sobre` y `sub` usan otras
  reglas. Van a leerse raro juntos. Arreglar la aritmética o etiquetarla.
- `resultado` está contaminado por el nivel de soporte (R1). La calibración medida en condición
  guiada no predice la calibración en condición de entrevista.

**Drill intercalado de reconocimiento de patrón**
- Es sólo de micro-sesión: nunca corre bajo carga de implementación (R7).
- No tiene paso de discriminación/rechazo (R2), que es el mecanismo que la evidencia identifica.
- `--acerto si|no` no guarda **qué dijo**: no hay matriz de confusión. El dato accionable
  ("los confunde con prefix-sum") se pierde y queda sólo el porcentaje.
- "Mezclá enunciados de temas ya cubiertos" sin regla de curación: por defecto voy a elegir
  pares fáciles de discriminar sin darme cuenta, y eso no entrena nada.
- Nada lo obliga a ocurrir. Una micro-sesión puede ser toda de tarjetas y el sistema no se
  entera. Es medición sin mecanismo.

**Guarda de no explicar en el momento del fallo**
- **Es la mejor implementación del repo**: `study.py` imprime la orden en el instante exacto de
  la decisión. Ese patrón —el mecanismo en el punto de decisión, no en un documento— es el que
  hay que replicar para las otras tres.
- Pero está alcanzada sólo a tarjetas. El camino de ejercicio no imprime nada equivalente.
- No hay dónde estacionar la explicación diferida. "Va a una sesión de fondo" es una promesa que
  nadie cumple si no queda escrita: agregar una sección `## Pendiente de explicar` a
  `base/temas/PLANTILLA.md` y forzar que se escriba ahí antes de seguir.

**Registro de clases de error**
- Vocabulario libre en texto: `off-by-one`, `offbyone`, `off_by_one` son tres claves distintas y
  la agregación es por string exacto. Los conteos se fragmentan en silencio. Necesita un
  vocabulario controlado en archivo y que `study.py` avise cuando aparece una etiqueta nueva.
- Sólo se captura en ejercicios; nunca en tarjetas ni en el drill.
- No distingue error **predicho** de **no predicho** (R5). Esa distinción es la que convierte el
  registro en medida de anticipación en vez de medida de daño.
- El reporte muestra conteo y última fecha, pero no tendencia: "¿está mejorando en off-by-one?"
  es hoy incontestable con nuestros propios datos.

**Dos bugs de adherencia que encontré de paso, fuera de las cuatro**
- `due_cards()` ordena por vencimiento y **después** hace `random.shuffle`, destruyendo el orden
  que acaba de calcular. Para intercalar está bien; pero con `--limite` las tarjetas más
  atrasadas pueden no aparecer nunca. Sugerencia: barajar dentro del conjunto, pero anteponer las
  que estén vencidas más de 2× su intervalo.
- No hay tope diario de tarjetas. Después de una semana sin estudiar se va a encontrar con un
  muro, y el muro es la causa número uno de abandono en cualquier sistema de espaciado. Tope
  duro y política de "lapsadas primero".

---

## 7. Lo que decidimos NO traer, y por qué

- **El canvas de Excalidraw** (`scripts/canvas-server.js`, `viewer/canvas.html`,
  `agents/sysdesign-interviewer.md` element JSON). Requiere `node` + `lsof` + navegador, y
  nuestro `system-design/SKILL.md` ya define el entregable como "una conversación estructurada
  con un diagrama en palabras". No lo propongan de nuevo.
- **El harness de Python** (`scripts/run-solution.sh`, `harness/python_runner.py`). Viola "los
  ejercicios se resuelven en leetcode.com". **Pero admitamos qué perdemos**: es la única señal
  objetiva de corrección de los dos repos. Nuestro sustituto es el veredicto de LeetCode, que en
  realidad es mejor (juez real, tests ocultos). Sólo que **hoy no lo registramos**:
  `resultado solo|con_pistas|abandonado` no guarda si fue Accepted, Wrong Answer o TLE. Vale
  agregarlo, prioridad baja, porque ataría cada clase de error a un veredicto.
- **`/coding-import`** (fetch de LeetCode). Innecesario: `referencias-ts/problemas.md` ya tiene
  el índice y él resuelve en el sitio.
- **Toda la maquinaria behavioral** (`story-add`, `story-map`, `mock-behavioral`,
  `story-rehearse`, los dos subagentes). Ver §8.
- **El patrón `${CLAUDE_PLUGIN_ROOT}` vs `$CLAUDE_PROJECT_DIR`**: irrelevante, somos un repo solo.
- **Sí traer, como una línea**: el principio de **degradación elegante** de swe-coach ("never
  abort coaching over canvas trouble" / "degrades gracefully to a read-only review"). Hoy
  `CLAUDE.md` hace de `PY estado` un gate duro al arranque; si la tool falla, la sesión queda
  varada. Adherencia: si `study.py` rompe, la sesión sigue y se registra después.

---

## 8. Un agujero conocido que este plan no cierra: behavioral

Los loops de big tech puntúan behavioral. Nuestro sistema no lo toca en absoluto.
swe-interview-coach lo tiene completo y bien hecho (`skills/behavioral-frameworks/SKILL.md` con
STAR/SBI/CARL, anti-patrones y follow-ups estándar, todo con contraste débil/fuerte).

**Recomendación: no ahora.** Adoptar el sistema entero es una segunda maquinaria compitiendo por
sus 3–4 sesiones semanales, y las cuatro debilidades que él declaró son técnicas. Eso es
adherencia, no desprecio por el behavioral.

**La pieza más barata con valor real**, si quiere: un solo archivo `base/historias.md` con 4–6
historias STAR, armado una vez, y después repasado con el sistema de tarjetas que ya existe.
Las historias behavioral **son contenido declarativo**, y es el único lugar de todo el proyecto
donde la práctica de recuperación de **DUN** aplica en su forma más directa y donde nuestro SM-2
es exactamente la herramienta correcta. Costo: una sesión de fondo para armarlas, después cero.

Decisión de él, no mía.

---

## 9. Orden de ejecución sugerido

Ordenado por impacto arriba, pero para hacerlo conviene otro orden, por costo y dependencias:

**Ahora, en una sentada (cero fricción para él)**
1. S1 — sacar `solution-mode` y la fila del router. Es defensivo, pero si falla lo demás no
   importa.
2. S6, S7 — referencia rota y descripción engañosa.
3. R9 — techo de dominio a ~60 días. Dos líneas.
4. S2, S3, S4 — neutralizar los planes y sistemas de progreso en competencia, cosechando primero.

**Esta semana (cambios de ritual, sin código)**
5. R8 — ritual de restricciones. 30 segundos, va en `OVERRIDES.md`.
6. R2 — paso de discriminación en el drill (la parte de prompt; el flag después).
7. R10 — regla de retirada del ejemplo resuelto.
8. R12 — corte conceptual/mecánico en el feedback diferido, y separar calibración de contenido.

**Próximas dos semanas (código en `study.py`)**
9. R7 — `--patron-dicho`. Barato y arregla qué significa la métrica principal.
10. R2 — `--dijo` en `sesion patron`, matriz de confusión en `metricas`.
11. R1 — modo `simulacro`. El más caro de los de código y el de mayor impacto.

**Cuando haya rato (contenido)**
12. R3 — importar los 8 casos de sysdesign. Una tarde.
13. R4 — escaleras por problema, perezosamente, una por tema al abrirlo.

**A prueba, con salida**
14. R5 — predicción de casos borde. Es el de más fricción. Probar tres semanas; si empieza a
    cortar ejercicios por tiempo, bajarlo a un caso o sacarlo.
15. R6 — sonda fría antes de la teoría. Misma lógica: el encuadre es parte del mecanismo, y si
    desmotiva, se saca.
16. R11, R13 — cierre fusionado y follow-up de variación.

---

## 10. Resumen de una línea

Los dos repos aportan cosas distintas y casi no se pisan: **swe-interview-coach aporta contenido
canónico y mecanismos que obligan** (biblioteca de sysdesign, escaleras por problema, split
mock/practice, reloj real), **algotrace aporta ideas pedagógicas sueltas sin forma de obligarlas**
(la escalera de 5 niveles, el trace probatorio del bug, la tabla de restricciones) **y un archivo
de 31 KB que hay que cosechar y tirar**. Lo nuestro sigue siendo lo mejor de los tres en
medición, y es donde hay que gastar el esfuerzo: el problema más caro no es que falte contenido,
es que la métrica titular se mide en la condición equivocada.
