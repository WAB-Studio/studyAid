# Plan de fusión v2: algotrace + swe-interview-coach sobre nuestro sistema

Fecha: 2026-09-09. Segunda versión, después de una revisión externa (Codex) que leyó la v1
completa y del cambio de la restricción de solución decidido por el usuario.

Base: lectura completa de los 41 archivos de `.claude/skills/algotrace/`, los 62 de
`referencia/swe-interview-coach/`, y el sistema actual.

**Qué cambió respecto de v1**: la revisión tenía razón en lo esencial. La v1 tenía base
científica decente y una traducción a mecanismos mala: convertía cada buena idea en un gate, con
números inventados presentados como si se desprendieran de la evidencia. La v2 conserva casi
todos los principios y tira casi todos los rituales. Además, verifiqué las citas de los dos
lados y **encontré un error mío verificable en R9** que iba en dirección contraria a la que yo
creía. El detalle punto por punto está en §11.

---

## 0. La restricción que cambió

**Antes**: "nunca se le resuelve un ejercicio", absoluta.

**Ahora**: gate de agotamiento.
1. No hay solución antes de un intento significativo.
2. Cuando seguir peleando ya no produce aprendizaje —lo juzga el asistente y **se lo dice al
   usuario**— se muestra la solución y se analiza.
3. Queda un problema análogo, sin ayuda, días después.

Esto reordena el plan entero, y hay una razón empírica para tomarlo en serio y no como una
relajación cómoda. Bastani et al. 2025 (PNAS 122(26) e2422633122) corrieron un experimento de
campo con ~1000 estudiantes de secundaria en Turquía, tres brazos: control, **GPT Base**
(ChatGPT pelado) y **GPT Tutor** (con guardas diseñadas por docentes, la principal: dar pistas
en vez de respuestas). Resultados:

| Brazo | Durante la práctica (con acceso) | Examen posterior SIN acceso |
|---|---|---|
| GPT Base | **+48%** vs control | **−17%** vs control |
| GPT Tutor | **+127%** vs control | ≈ 0, indistinguible del control |

Eso es exactamente el modo de falla que este sistema tiene que evitar, medido. La lectura
correcta no es "la IA arruina el aprendizaje": es que **la disponibilidad de respuestas sube el
desempeño observado mientras está y baja el desempeño real cuando no está**, y que el diseño
pedagógico es lo que decide cuál de los dos pasa. Relajar la restricción es defendible; relajarla
sin gate real es reproducir GPT Base.

Tres consecuencias, y las tres son estructurales:

- **El gate de agotamiento es ahora el mecanismo más crítico del sistema.** No puede quedar en
  retórica.
- **Mostrar la solución tiene que dejar rastro objetivo**: un booleano por ejercicio, no una
  impresión mía.
- **El problema análogo días después deja de ser un adorno y pasa a ser la verificación.** Es lo
  único que distingue "le mostré la solución y aprendió" de "le mostré la solución y quedó una
  muleta". En la v1 esto era la recomendación de menor prioridad (R13); en la v2 es parte del
  gate.

**Reescrituras obligatorias**: `OVERRIDES.md` §"solution-mode está deshabilitado" pasa a ser
"Gate de agotamiento" (§8 de este documento tiene el texto); `CLAUDE.md` líneas 57 y 60; la regla
de retirada del ejemplo resuelto (R10).

---

## 1. Los tres niveles, y la regla nueva sobre de dónde sale el dato

### Retórica / mecanismo / medición

Sigue valiendo y es el eje de la §2:

- **Retórica**: el archivo lo nombra. Depende de que yo me acuerde en el turno 40.
- **Mecanismo**: el sistema obliga. Un comando falla, un gate corta.
- **Medición**: queda registro agregable.

### La regla del origen del dato

Esto es nuevo, y sale de cruzar la crítica de la revisión al modelo de datos con una corrección
del coordinador (la revisión creyó que los flags los tipea el usuario; los tipeo yo).

> **Un flag obligatorio es un mecanismo cuando su valor viene de afuera del asistente** —el
> reloj, el veredicto del juez, un evento discreto que ocurrió o no ocurrió, una respuesta que
> dio el usuario. **Es una invitación a fabricar cuando su valor es un juicio del asistente.**

El costo de un flag no es la memoria del usuario: es que si yo no tengo el dato, la sesión se
traba, y el camino más barato para destrabarla es inventar un valor plausible. Un `--error-clase`
obligatorio no produce taxonomía de errores: produce taxonomía de errores verosímiles.

De ahí sale el modelo de datos de §9: los juicios míos se registran, pero **etiquetados como
inferidos, opcionales, y nunca como requisito para avanzar**. Y toda opción obligatoria cuyo
valor viene del usuario debe aceptar un valor explícito `no-preguntada`, para que el camino
honesto sea más barato que el camino fabricado.

---

## 2. Inventario: qué es real hoy en cada repo

### Nuestro sistema (estado a hoy, ya con los arreglos aplicados)

| Mecanismo | Nivel | Nota |
|---|---|---|
| Reloj real de sesión | **Medición** dura | Sólido. Dato externo. |
| Gate de bitácora al cerrar | **Mecanismo** | El gate más fuerte del sistema. Conservar. |
| SM-2 en JSON | **Mecanismo + Medición** | Bien como *programador*. Mal usado como medida de dominio (§ R9). |
| Tope de 20 vencidas + `--todas` | **Mecanismo** | Puro triunfo de adherencia. Conservar. |
| `due_cards` round-robin por tema | **Mecanismo** | Es nuestro mecanismo de intercalado de tarjetas. Conservar. |
| Calibración predicción/resultado | **Mecanismo + Medición** | Dato del usuario ⇒ obligatorio es legítimo. Falta valor `no-preguntada`. |
| Drill con `--dijo` y matriz de confusión | **Medición contaminada** | El dato es bueno; la comparación por igualdad de strings no (§ R2/R7). |
| Guarda de no explicar en el fallo | **Mecanismo** | La mejor implementación del repo: la orden se imprime en el punto de decisión. Pero su fundamento citado era el equivocado (§ R12). |
| Clases de error normalizadas | **Medición inferida** | Conservar la normalización, bajar de rango: es juicio mío. |
| `dominio_por_tema` compuesto | **Retórica disfrazada de medición** | **A eliminar.** Es nuestra versión sofisticada de las barras ASCII de algotrace. |
| Escalera de 5 pistas | **Retórica** + un número no comparable | `--pista-max` promedia unidades distintas (§ R4). |

### algotrace

| Mecanismo | Nivel | Nota |
|---|---|---|
| Escalera de 5 pistas | **Retórica** | Bien especificada semánticamente. Ese es su valor, no el número. |
| Debug: probar el bug con un trace hasta el frame divergente | **Retórica** de alto valor | La mejor idea del repo. |
| Log `.algotrace/progress.md`, "offer, never nag" | **Retórica** | Opcional por diseño ⇒ cero medición. |
| Intervalos +3/+7/+21 vs 1/3/7/16/35 en otro archivo | **Retórica contradictoria consigo misma** | |
| Reloj de interview-mode | **Inventado** | "No real clock exists — track elapsed by phase budget". |
| Progress Score con barras ASCII | **Retórica disfrazada de medición** | Lo peor del repo, y nuestro `dominio` cae en la misma trampa. |
| `scripts/testgen.py` | **Mecanismo** | El único código del repo. Formas de caso borde, útiles. |
| `docs/jargon-decoder.md` | Contenido | Barato y bueno. Conservar. |

### swe-interview-coach

| Mecanismo | Nivel | Nota |
|---|---|---|
| `date +%s` antes de cada turno, "never guess times" | **Mecanismo** | Coincide con nuestra restricción. |
| Harness que corre el código | **Mecanismo + Medición** | Única señal objetiva de corrección de los dos repos. Nuestro equivalente es el veredicto de LeetCode, que es mejor. |
| `library/sysdesign/*.md`: 8 diseños con números y tradeoffs steel-manned | **Contenido, el mejor activo de los dos repos** | |
| `library/coding/*.md`: escalera por problema | **Mecanismo** | Sobreingeniería para nosotros (§ R4). |
| Session file escrito siempre por el comando | **Mecanismo** | |
| Split mock/practice | **Mecanismo** | La idea correcta; mi traducción a "un simulacro semanal" no lo era. |
| Degradación elegante (sin runtime → seguí) | **Mecanismo** de adherencia | Adoptar como principio. |
| `weak-patterns.md` | **Medición sin poder** | Infiere debilidad de 2–3 reps. |
| Rúbricas 6 ejes | **Un eje anclado, cinco inferidos, misma tipografía** | El error que no hay que copiar. |

**Conclusión**: swe-interview-coach tiene más mecanismos reales; algotrace tiene mejores ideas
pedagógicas sueltas sin forma de obligarlas; nosotros teníamos la mejor medición de los tres y
la estábamos arruinando con un compuesto inventado.

---

## 3. La base de evidencia, verificada

Verifiqué con búsqueda las citas de los dos lados. No acepté ninguna por autoridad.

### Lo que aportó la revisión y yo no tenía (todo verificado)

| Hallazgo | Fuente | Qué dice, con precisión |
|---|---|---|
| **IA sin guardas daña el aprendizaje posterior** | Bastani, Bastani, Sungu, Ge, Kabakcı & Mariman 2025, PNAS 122(26) e2422633122 | ~1000 alumnos, Turquía, 4 sesiones de 90 min. GPT Base: +48% en práctica, **−17% en el examen sin acceso**. GPT Tutor (pistas en vez de respuestas): +127% en práctica, ≈0 en el examen. |
| **El diseño pedagógico decide el resultado** | Kestin et al. 2025, *Scientific Reports* | RCT, N=194, física intro en Harvard. Tutor de IA a medida ("PS2 Pal") vs clase de aprendizaje activo: aprendieron **más del doble en menos tiempo** con el tutor. **Corrección**: el brazo de comparación fue clase presencial activa, **no** "acceso libre a un chatbot". Esa segunda mitad de la afirmación de la revisión es del estudio de PNAS, no de Kestin. |
| **Los ITS funcionan y se acercan a tutoría individual** | Ma, Adesope, Nesbit & Liu 2014, *J. Educ. Psych.* 106(4), doi 10.1037/a0037123 | 107 tamaños de efecto, 14.321 participantes. g=.42 vs instrucción grupal, g=.57 vs instrucción computarizada no-ITS, g=.35 vs libro. **Sin diferencia significativa vs tutoría humana individual (g=−.11).** |
| **El intercalado opera por contraste discriminativo** | Chen, Paas & Sweller 2021, *Educ. Psych. Rev.*, doi 10.1007/s10648-021-09613-w | Revisión sistemática. Sostiene que espaciado e intercalado tienen bases teóricas **distintas**: el espaciado se explica por carga cognitiva, el intercalado por la hipótesis de contraste discriminativo. Corolario directo: **el intercalado ayuda cuando las categorías son confundibles**. |
| **Reversión por pericia, con una asimetría clave** | Tetzlaff, Simonsmeier, Peters & Brod 2025, *Learning and Instruction* 98, doi 10.1016/j.learninstruc.2025.102142 | 176 tamaños de efecto, 60 estudios, 5924 participantes. El efecto existe y está moderado por nivel educativo y dominio. **Y: "dar asistencia a los novatos parece más importante que retirarla a los expertos."** |
| **Pretesting: qué está probado y qué no** | Pan & Carpenter 2023, *Educ. Psych. Rev.*, doi 10.1007/s10648-023-09814-5 | >60 artículos desde Kornell et al. 2009. El beneficio requiere **oportunidad de estudiar la respuesta correcta después**. |
| **Feedback inmediato vs diferido: nulo en promedio** | Meta-análisis 2026, *Educ. Psych. Rev.*, doi 10.1007/s10648-026-10117-8 | 51 estudios (1988–2024), 160 tamaños de efecto, meta-regresión con RVE. **g = 0.03, IC95% [−0.08, 0.13], p = .61.** Las demoras estudiadas van de 1 segundo a **7 días** (o 1–60 ítems intercalados). |
| **Y el tipo de feedback importa más que el timing** | Van der Kleij, Feskens & Eggen 2015, *Rev. Educ. Research* | Feedback elaborado g=0.49 ≫ dar la respuesta correcta 0.32 ≫ sólo correcto/incorrecto 0.05. Y los efectos se ven **negativamente** afectados por el timing diferido en entornos computarizados. |

### Lo mío, verificado (con las correcciones que aparecieron)

| Sigla | Fuente | Estado tras verificar |
|---|---|---|
| **INT** | Rohrer, Dedrick & Stershic 2015, *J. Educ. Psych.* 107(3), 900–908 | Confirmado. 126 alumnos de 7.º grado, 3 meses. El diseño **explícitamente** requiere elegir la estrategia a partir del problema mismo. Es la evidencia más cercana a su debilidad principal. |
| **ESP** | Cepeda, Vul, Rohrer, Wixted & Pashler 2008, *Psych. Science* 19, 1095–1102 | Confirmado, **y me contradice**: el gap óptimo es ~20–40% de un intervalo de retención de 1 semana, y cae a **~5–10% de un intervalo de 1 año**. Ver R9. |
| **EST** | Pashler, McDaniel, Rohrer & Bjork 2008, *PSPI* | Confirmado. No lograron respaldar la hipótesis de emparejamiento; "no hay base de evidencia adecuada". |
| **DP** | Ericsson et al. 1993 **con** Macnamara, Hambrick & Oswald 2014, *Psych. Science* 25 | Confirmado con números: 88 estudios, N=11.135. La práctica deliberada explica **26%** de la varianza en juegos, 21% música, 18% deportes, **4% educación, <1% profesiones**. |
| **GEN** | Kornell, Hays & Bjork 2009, *JEP:LMC* | Confirmado, **y acota mucho lo que yo extrapolé**: los materiales fueron preguntas de trivia ficticias y asociados débiles de una palabra clave. Nada parecido a pelear un algoritmo. |
| **FB** | Butler, Karpicke & Roediger 2007, *JEP:Applied* 13(4), 273–281 | Confirmado que existe, **y acotado**: pasajes de prosa y multiple-choice de conocimiento general, demora de 24 h. No licencia diferir un error conceptual de algoritmo por días. |
| **WE** | Sweller & Cooper 1985; Renkl (desvanecimiento); Kalyuga et al. 2003 | Vigentes, y ahora con el meta-análisis de Tetzlaff 2025 encima, que agrega la asimetría. |
| **SE** | Chi et al. 1989, 1994 | Vigente. Es el fundamento correcto para la guarda de "producí antes de que yo explique". |
| **TR** | Barnett & Ceci 2002 | Vigente como advertencia: la transferencia lejana es difícil. |
| **DUN** | Dunlosky et al. 2013 | Vigente **pero acotado a lo declarativo**: tarjetas e historias behavioral. No es la literatura principal acá. |

### Lo que quedó sin verificar

No pude abrir el texto de Cepeda et al. 2008 (certificado vencido en el mirror, PDF binario en
ERIC), así que **no puedo sostener** la afirmación de que la función alrededor del óptimo es
ancha ni que errar hacia gaps más largos sea más seguro que hacia gaps más cortos. Lo dejo
anotado como pregunta abierta, no como argumento.

### Los dos criterios que gobiernan todo

**La adherencia gana a la optimalidad.** Trabaja full time. Un sistema que hace todas las semanas
vale más que uno mejor en el papel que abandona en tres.

**Pocas invariantes duras, mucha política adaptable** — con una enmienda que la revisión no hizo
y que hago yo: **la política adaptable tiene que estar escrita como criterio de decisión.** Ma et
al. 2014 mide sistemas tutoriales *diseñados*, con modelo de dominio y política explícita; no
mide un modelo de lenguaje improvisando. "Adaptativo" sin criterio escrito no es adaptación, es
improvisación, y la improvisación no sobrevive al turno 40. Menos gates, sí; menos criterios
escritos, no.

---

## 4. Las invariantes duras

Ocho. Todo lo demás es política adaptable. Las seis primeras son de la revisión, tal cual; las
dos últimas las agrego yo.

1. **El aprendiz produce primero.** Ninguna explicación mía precede a un intento suyo.
2. **La IA entrega la mínima ayuda necesaria, adaptada al desempeño.** Ésta es la invariante que
   PNAS convierte en crítica: es la diferencia medida entre GPT Tutor y GPT Base.
3. **Los errores importantes se corrigen en la misma sesión.**
4. **El cierre tiene UNA sola producción diagnóstica**, elegida por mí según lo que pasó.
5. **Los temas reaparecen espaciados y con problemas variados.**
6. **Periódicamente se mide desempeño frío, nuevo y sin ayuda.** El problema análogo posterior a
   una solución mostrada es un caso particular de esto.
7. **Toda sesión cierra con bitácora, y el tiempo sale del reloj.** No es pedagogía: es
   integridad de datos y es la única forma de medir adherencia, que es la métrica que la revisión
   pone —con razón— entre las principales.
8. **La política adaptativa está escrita.** Cada decisión adaptativa (cuándo cortar, cuánto
   ayudar, cuándo medir frío) tiene su criterio en un archivo, no en mi criterio del momento.

---

## 5. Recomendaciones, v2

Reescritas: casi todas pasaron de gate a política. Cada una dice qué cambió respecto de la v1.

### R1 — Medición fría periódica (era "modo simulacro semanal")

**De dónde**: el split mock/practice de `agents/coding-interviewer.md` y
`agents/sysdesign-interviewer.md`.

**Qué cambió**: la v1 proponía un simulacro fijo por semana y justificaba que "la presencia del
tutor invalida el intento". La revisión pidió medir la ayuda realmente recibida y hacer la
cadencia adaptativa (cada 1–2 semanas). **Acepto la cadencia adaptativa y acepto medir la ayuda
recibida** —es más barato y más informativo—, **y defiendo que hace falta igual una condición
sin ayuda disponible**, porque PNAS lo demuestra: en GPT Base la ayuda estaba *disponible*, y el
daño apareció en el examen sin acceso. La disponibilidad es en sí un tratamiento: cambia cómo se
asigna el esfuerzo antes de que se pida una sola pista. Medir pistas recibidas no captura eso.

**Forma final**: no es un role-play de entrevista, es una **medición fría** — un problema nuevo,
con el asistente explícitamente no disponible durante la ventana de intento. Cadencia adaptativa,
del orden de cada 1–2 semanas, y obligatoria como segunda mitad del gate de agotamiento.

**Respaldo**: Bastani et al. 2025 (directo); **DD** (Bjork & Bjork 2011) para el argumento de
condiciones de recuperación.

**Qué se rompe si no está**: "resueltos solo" se sigue midiendo en condición asistida y
reportando como si predijera desempeño sin asistencia. PNAS midió exactamente ese sesgo y le
puso número.

**Fricción**: baja. No elige él; y con cadencia adaptativa deja de ser una cita fija en el
calendario, que es lo que se abandona.

---

### R2 — Contraste discriminativo, disparado por confusión (era: ritual en cada ítem)

**De dónde**: `prompts/universal-system-prompt.md` §11 (Algorithm Selection Matrix) y `/why-not X`;
fase Match de UMPIRE.

**Qué cambió**: la v1 lo ponía como ritual del drill. La revisión dice: pedir contrastes cuando
haya confusión, baja confianza o patrón nuevo. **Acepto**, y la evidencia que aportó la revisión
es la que me convence: Chen, Paas & Sweller 2021 sostienen que el intercalado opera por
**contraste discriminativo**, o sea que rinde cuando las categorías son confundibles. Pedir "¿por
qué no X?" sobre un problema que él ya clasificó bien y con confianza no tiene contra qué
contrastar: es fricción sin mecanismo.

**Forma final**: disparadores explícitos —confusión previa registrada, baja confianza declarada,
patrón nuevo— y pares curados: `sliding-window` vs `prefix-sum`; `two-pointers` vs
`binary-search`; `dp-1d` vs `greedy`; `backtracking` vs `dfs`; `heap` vs `sort completo`.

**Respaldo**: **INT** (Rohrer et al. 2015) para el efecto; Chen et al. 2021 para *cuándo* aplica.

**Qué se rompe si no está**: seguimos midiendo reconocimiento sin entrenar el mecanismo que la
evidencia identifica, y sin saber con qué confunde cada patrón.

**Fricción**: ahora casi nula, porque no corre siempre.

---

### R3 — Biblioteca de system design como **ejemplos múltiples**, no como respuestas canónicas

**De dónde**: `referencia/swe-interview-coach/library/sysdesign/*.md` — los 8 diseños.

**Qué cambió**: la v1 hablaba de "casos canónicos". La revisión pide usarlos como ejemplos
múltiples y mostrar que una consigna admite más de un diseño defendible. **Acepto sin reservas**,
y además es lo que estos archivos hacen mejor: cada sección `## Common tradeoffs` defiende bien
la opción **no** elegida antes de descartarla ("steel-man SQL: 3 TB y 12K RPS entran en un
Postgres bien afinado…"). Usarlos como "la respuesta" desperdicia justamente su mejor propiedad.

**Respaldo**: **WE** (Sweller & Cooper 1985) para el ejemplo resuelto con un casi-novato;
Tetzlaff et al. 2025 para la advertencia de retirada — con la asimetría, ver R10.

**Qué se rompe si no está**: nuestro `bloques.md` son dos páginas de generalidades y cada sesión
de sysdesign es una improvisación mía sin estándar fijo, así que no hay forma de saber si mejoró
entre marzo y septiembre.

**Fricción**: cero para él. Una tarde de importación.

---

### R4 — Tres niveles semánticos de ayuda, generados desde el intento real (era: escalera por problema)

**De dónde**: la escalera de `modes/hint-mode.md` (la parte semántica); la contra viene de la
revisión.

**Qué cambió**: la v1 proponía escribir escaleras de 4 peldaños por problema. La revisión lo
llama sobreingeniería clara. **Acepto**: escribir 12 escaleras a mano para que un modelo que ya
entiende el problema lea el peldaño 2 es trabajo muerto, y peor, congela la ayuda en un guion en
vez de ajustarla a lo que él realmente escribió.

**Pero acepto con una consecuencia que la revisión no nombró**: mi razón para las escaleras
enlatadas era que `--pista-max` no es comparable entre problemas. Si tiramos las escaleras hay
que tirar también la pretensión de que el número sea comparable. Reemplazo:

| Nivel | Qué revela | Comparable entre problemas porque… |
|---|---|---|
| 1 **Reformular** | una propiedad de la entrada o de la salida que se le pasó | no nombra técnica |
| 2 **Clase de estructura** | qué tipo de estructura/patrón resuelve esta forma | nombra familia, no aplicación |
| 3 **Invariante** | qué tiene que mantenerse cierto en *este* problema | nombra el invariante, no la implementación |
| — **Solución mostrada** | evento aparte, booleano | no es un peldaño: es cruzar el gate |

Tres niveles semánticos sí son comparables entre problemas, porque están definidos por *qué tipo
de información revelan*, no por cuánto avanzan hacia el código.

**Respaldo**: Bastani et al. 2025 — la guarda que funcionó fue "pistas en vez de respuestas". El
mecanismo que importó fue *pistas*, no *pistas enlatadas*. Van der Kleij et al. 2015 agrega que
el feedback **elaborado** (g=0.49) supera con holgura a dar la respuesta correcta (0.32): la
ayuda que explica el porqué vale más que la que resuelve.

**Fricción**: negativa. Elimina trabajo de autoría.

---

### R5 — Casos borde predichos, selectivos (era: tres casos siempre)

**Qué cambió**: la v1 decía "tres casos, siempre, en fondo". La revisión dice: útil, pero la cita
no prueba esa implementación; selectivo, uno a tres casos elegidos por la IA. **Acepto.** El
número tres era mío y no salía de ningún lado.

**Forma final**: uno a tres casos, elegidos por mí según el problema y según qué clases de error
ya aparecieron en su historial. Predice él, después se somete.

**Respaldo honesto**: **CAL** (Koriat & Bjork 2005) respalda que predecir y contrastar corrige el
sesgo de previsión. Que eso reduzca bugs en implementación bajo presión es **extrapolación mía**,
no un resultado. Y `scripts/testgen.py` da las formas de caso a usar: vacío, un elemento, todos
duplicados, ya ordenado, ordenado al revés, negativos con cero, extremos de 32 bits.

**Fricción**: la más alta que queda, ahora bastante menor. Sigue con criterio de salida.

---

### R6 — Hipótesis de 60–90 segundos antes de la teoría (era: sonda fría de 5 minutos)

**Qué cambió**: la v1 proponía 5 minutos peleando un problema del tema nuevo. **Acepto la
crítica, y la verificación la refuerza más de lo que la revisión sabía.** Kornell, Hays & Bjork
2009 usó **preguntas de trivia ficticias y asociados débiles de una palabra**; Pan & Carpenter
2023 subraya que el beneficio requiere estudiar la respuesta correcta después. Lo que está
probado es *arriesgar una respuesta corta y después ver la correcta*. Cinco minutos de pelea
contra un algoritmo desconocido es una extrapolación mía de varios saltos, y Tetzlaff et al. 2025
la empeora: con un casi-novato, dar asistencia importa más que retirarla.

**Forma final**: 60–90 segundos. "Antes de que te cuente nada: ¿de qué te suena esto y qué
harías?" Después la teoría, que sigue con su tope de 15 minutos.

**Y lo que la v1 decía sobre "teoría primero" se sostiene y no cambia**: que él se declare
"aprendo con teoría primero" es una **decisión de adherencia, no de evidencia**. Pashler et al.
2008 no logró respaldar la hipótesis de emparejamiento y concluye que no hay base adecuada para
incorporar evaluaciones de estilo a la práctica educativa. Que él lo prefiera es razón legítima
para hacerlo —si es lo que lo hace sentarse un martes a las diez de la noche, vale— y **no** es
razón para creer que produce mejor aprendizaje. Hoy `base/perfil.md` lo trata como si fuera lo
segundo, y eso hay que corregirlo en el archivo.

---

### R7 — Reconocimiento bajo carga, registrado como texto (era: comparación `dijo == tema`)

**Qué cambió**: la revisión objeta comparar mecánicamente. **Acepto, y es la regla del origen del
dato aplicada**: muchos problemas admiten más de un patrón válido (Trapping Rain Water es
two-pointers *y* monotonic-stack; Top K Frequent es heap *y* bucket sort). Una igualdad de
strings convierte una respuesta correcta en un fallo registrado, y después ese fallo alimenta una
matriz de confusión que dice cualquier cosa.

**Forma final**: se registra **lo que dijo, en texto**, y su explicación del enfoque. La
evaluación de si era válido es un campo **inferido**, separado, opcional. La matriz de confusión
se arma sobre pares que yo marqué como confusión real, no sobre desigualdad de strings.

**Esto obliga a modificar código ya aplicado**: el `--dijo` con comparación por igualdad que se
implementó después de la v1.

**Respaldo**: **TR** (Barnett & Ceci 2002) para el punto de fondo, que sigue en pie: el drill de
30 segundos y el solve frío de 40 minutos están separados por varias dimensiones de contexto, y
hoy medimos el extremo fácil y lo reportamos como readiness.

---

### R8 — Comprender y reformular primero; las restricciones después, para podar

**Qué cambió**: la v1 decía "ritual de restricciones **antes** de elegir enfoque", tomado de
`docs/constraints-to-complexity.md`, que literalmente instruye leer la restricción y tachar
patrones *antes* de leer la historia. **La revisión tiene razón y el error es mío, y es irónico**:
mi propia justificación era que él empareja por rasgos superficiales del enunciado, y yo estaba
proponiendo reemplazar un heurístico superficial por otro —uno específico de LeetCode, que en una
entrevista real donde nadie te da `n ≤ 10^5` no sirve.

**Forma final**: (1) reformular el problema con sus palabras y acordar el contrato de
entrada/salida; (2) recién entonces usar las cotas para descartar complejidades. Es el orden de
UMPIRE (Understand antes que Match): swe-interview-coach lo tenía bien y yo lo invertí.

**Respaldo**: **TR** — lo único que plausiblemente transfiere entre patrones es reformular,
generar candidatos y discriminar. Por eso R2 y R8 no son drills accesorios: son el contenido
portante. Dominar sliding-window no transfiere a prefix-sum.

**Fricción**: la misma que antes, ~30 segundos, en el orden correcto.

---

### R9 — Sacar el intervalo del cálculo de dominio (era: subir el techo a 60 días)

**Acepto la objeción entera, y encima el número estaba mal en la dirección opuesta a la que yo
creía.**

**El error verificable**: mi argumento era "con horizonte de 6–12 meses, un techo de 21 días es
demasiado corto, subilo a 60". Cepeda, Vul, Rohrer, Wixted & Pashler 2008 dice que el gap óptimo
es ~20–40% de un intervalo de retención de una semana y cae a **~5–10% de un intervalo de un
año** — o sea, del orden de **18–36 días** para un horizonte de un año. El 21 original estaba más
cerca de esa literatura que mi 60. Escribí "no estoy seguro de la proporción exacta" y después
usé esa incertidumbre para mover el número en la dirección que me convenía. Eso es exactamente lo
que le critiqué a algotrace.

**Y la objeción de fondo es más importante que el número**: **el intervalo programado es una
propiedad del algoritmo, no de la persona.** SM-2 le da 92 días a una tarjeta porque acertó tres
veces seguidas, no porque sepamos que domina el tema. Usar eso como 40% de un puntaje de
"dominio" convierte un parámetro de scheduling en una afirmación sobre él. Es nuestra versión
sofisticada de las barras ASCII de algotrace, que critiqué en la v1 sin ver que estábamos
haciendo lo mismo con mejor tipografía.

**Forma final**:
- **Eliminar `dominio_por_tema()` y el puntaje compuesto.** No reparametrizarlo: sacarlo.
- **Conservar SM-2 como programador de tarjetas**, sin tocar. Ahí sí Cepeda aplica razonablemente
  bien, porque las tarjetas *son* material declarativo (señal de reconocimiento, complejidad,
  caso borde). Sobre los ejercicios no aplica en absoluto.
- La cobertura por tema se mira con lo que ya existe: último contacto, temas fríos, y
  `base/temario.md`. Y el dominio real se mide con R1.

**Nota abierta**: no pude verificar si la función de Cepeda alrededor del óptimo es ancha, así que
no argumento sobre si conviene errar largo o corto.

---

### R10 — Desvanecimiento por desempeño, y sesgado a desvanecer tarde

**Qué cambió**: la v1 fijaba tres etapas por número de exposición (1.ª vez ejemplo completo, 2.ª
con huecos, 3.ª nada). La revisión dice: decidirlo por desempeño —intento independiente, calidad
de la explicación, errores, ayuda pedida— no por conteo. **Acepto.**

**Y agrego una enmienda que sale de la cita que trajo la revisión**: el meta-análisis de Tetzlaff
et al. 2025 (176 efectos, 60 estudios, 5924 participantes) concluye que **dar asistencia a los
novatos importa más que retirarla a los expertos**. Es decir: la penalidad de desvanecer
demasiado tarde es menor que la de desvanecer demasiado temprano. Entonces la regla adaptativa no
es simétrica — **ante la duda, mantener el andamiaje**. Eso es lo contrario del sesgo natural de
un sistema que se enorgullece de no ayudar, que era el sesgo de la v1.

**Y ahora que la restricción se relajó, R10 pierde una carga que llevaba de más.** En la v1 el
ejemplo resuelto era el único contrapeso al descubrimiento puro, y por eso yo lo defendía con
tanta fuerza. Con el gate de agotamiento, el contrapeso principal es el gate; el ejemplo resuelto
vuelve a ser lo que debe ser: andamiaje inicial, retirado según desempeño.

---

### R11 — Una sola producción diagnóstica al cierre

**Qué cambió**: la v1 fusionaba cuatro cosas en el cierre (patrón, invariante, complejidad,
predicción de casos borde). La revisión advierte fatiga. **Acepto**: una sola, elegida por mí
según lo que pasó en el ejercicio. Si el problema fue de reconocimiento, pido el patrón y por
qué. Si fue de implementación, pido el trace. Si fue de análisis, la complejidad justificada.

**Respaldo**: **SE** (Chi et al. 1989, 1994) — la autoexplicación funciona cuando la produce el
aprendiz, y no hace falta producir cuatro para que funcione.

**Y una regla que se mantiene de la v1**: el visual lo produce él, no yo. El contrato de estilo de
algotrace obliga a que *toda* respuesta lleve un visual producido por el tutor; en modo tutor está
bien, en recuperación hace por él el trabajo generativo que estamos midiendo. El propio algotrace
se contradice acá (review-mode le pide a él el frame 2, el style-contract se lo sirve). Va escrito
en `OVERRIDES.md`.

**Fricción**: baja, y bajó respecto de la v1.

---

### R12 — Producción antes de explicación, corrección **dentro** de la sesión

**Ésta era mi recomendación más débil y la evidencia lo confirma.** La v1 proponía diferir los
errores conceptuales a la sesión siguiente, citando Butler/Karpicke/Roediger 2007 y Kulik & Kulik
1988.

**Lo que encontré al verificar**:
- El meta-análisis 2026 (51 estudios, 160 efectos): **g = 0.03, IC95% [−0.08, 0.13], p = .61**. No
  hay diferencia promedio.
- Las demoras estudiadas llegan como máximo a **7 días**, y las de días son escasas. "La próxima
  sesión de fondo" cae en el extremo peor cubierto de esa literatura.
- Butler et al. 2007 usó pasajes de prosa y multiple-choice de conocimiento general con 24 h de
  demora. Es material declarativo; no licencia diferir un error conceptual de algoritmo.
- Van der Kleij et al. 2015 encontró que en entornos computarizados el timing diferido afecta
  **negativamente**, y que el feedback **elaborado** (g=0.49) rinde mucho más que dar la respuesta
  correcta (0.32) o el mero correcto/incorrecto (0.05).

**Acepto la secuencia de la revisión, tal cual**:
1. Resultado crudo.
2. 5–10 minutos de trace y autodiagnóstico **suyos**.
3. Pista mínima si sigue bloqueado (niveles de R4).
4. **Corrección conceptual completa dentro de la sesión.**
5. Problema análogo sin ayuda, días después.

**Lo único que defiendo, y con otro fundamento**: la guarda de "no expliques en el instante del
fallo" **se queda**. Pero no es una regla de *timing a través de días* —eso era mi error—: es una
regla de **orden dentro de la sesión**, producción antes de explicación. Su respaldo correcto es
generación y autoexplicación (**GEN**, **SE**), no timing de feedback. El mecanismo estaba bien y
la cita estaba mal, que es distinto de que el mecanismo estuviera mal.

**Consecuencia en archivos**: `OVERRIDES.md` §"No enseñar en el fallo" dice hoy "la explicación
va a una sesión de fondo". Esa frase se elimina y se reemplaza por la secuencia de arriba.

---

### R13 — El problema análogo, promovido de adorno a mecanismo

**Qué cambió**: en la v1 esto era la recomendación de menor prioridad (variación al cierre). Con
la restricción relajada, **el problema análogo días después es la segunda mitad del gate de
agotamiento** y no es opcional: es lo único que distingue haber enseñado de haber dado una
muleta. PNAS le pone el número a esa distinción (+48% con la ayuda presente, −17% sin ella).

**Acepto la acotación de la revisión**: después de un abandono sin solución mostrada, un
follow-up de variación probablemente sólo agrega carga. La variación va donde hay algo que
consolidar.

**Forma final**: cada vez que se cruza el gate (solución mostrada), queda agendado un problema
análogo, sin ayuda, a los pocos días, y su resultado se registra como dato **objetivo**. Ese
registro es a la vez la verificación pedagógica y una de las métricas principales de §9.

---

## 6. Qué sacar (actualizado)

**Ya hecho y que hay que revisar a la luz del cambio de restricción**
- **S1** — se borró `modes/solution-mode.md`, la fila del router y la regla ALWAYS. **La
  eliminación se conserva**: no queremos la versión de algotrace, que entrega código completo a
  pedido. Lo que hay que reescribir es nuestro override, que hoy dice "Nunca escribas código de
  solución... si insiste, nivel 5 y registrá como abandonado". Texto nuevo en §8.

**Sigue vigente de la v1**
- `docs/study-plan.md` (90 min/día × 6 días × 8 semanas). Contradice `base/temario.md` y su
  disponibilidad real. Rescatar antes de tirar su regla de escalada, que es una dificultad
  deseable bien calibrada: *trabado menos de 20 minutos, no toques la skill; 20–30 minutos, pista
  1 o 2*. Encaja perfecto como criterio escrito del gate de agotamiento.
- `prompts/universal-system-prompt.md` (31 KB). Cosechar §11 (matriz de selección → R2), §12
  (tabla de invariantes por patrón), §16 (verificación → R5), Apéndice B (misconceptions),
  Apéndice D (presupuesto de complejidad → R8). Después borrar: §8 (estilos de aprendizaje,
  contradice Pashler et al. 2008), §9 (el "X% correcto" fabricado) y §20 (barras ASCII sin fuente).
- El sistema de progreso paralelo de `modes/review-mode.md` y su "offer, never nag".
- El contrato "todo response lleva un visual" en contextos de recuperación (scoping, no borrado).
- `.claude/skills/fuentes/SKILL.md` apunta a `.claude/skills/leetcode/referencias/`, que no
  existe.

**Nuevo en la v2**
- **`dominio_por_tema()` y todo el puntaje compuesto** (R9). Y con él, la sección de
  `metricas/SKILL.md` que lo explica, que además ya era engañosa: describe pesos fijos 40/20/40
  cuando el código renormaliza y, sin ejercicios registrados, las tarjetas pasan a pesar 100%.
- **La comparación `dijo == tema`** del drill (R7). El campo se conserva, la comparación
  automática se va.
- **La constante `HORIZONTE_DOMINIO_DIAS`** queda huérfana al sacar el compuesto.

---

## 7. Qué NO traer (sin cambios respecto de v1)

- **El canvas de Excalidraw**. Requiere `node` + `lsof` + navegador; nuestro entregable de
  sysdesign es una conversación estructurada con un diagrama en palabras.
- **El harness de Python**. Los ejercicios se resuelven en leetcode.com. **Pero lo que perdemos
  tiene reemplazo y es mejor**: el veredicto de LeetCode es un juez real con tests ocultos. Hoy
  no lo registramos, y en la v2 pasa a ser un campo objetivo de primera línea (§9).
- **`/coding-import`**. `referencias-ts/problemas.md` ya es el índice.
- **La maquinaria behavioral completa**. Ver §10.
- **Sí traer como una línea**: el principio de **degradación elegante** de swe-coach. Hoy
  `CLAUDE.md` hace de `PY estado` un gate duro al arranque; si la tool rompe, la sesión queda
  varada. Si `study.py` falla, la sesión sigue y se registra después.

---

## 8. El gate de agotamiento, escrito

Texto para reemplazar `OVERRIDES.md` §"solution-mode está deshabilitado". Es la invariante 2 y la
pieza más crítica del sistema, así que va con criterios explícitos (invariante 8), no a mi
criterio del momento.

> ## Gate de agotamiento
>
> No hay solución antes de un intento significativo. "Significativo" quiere decir: reformuló el
> problema, propuso un enfoque, y lo intentó.
>
> Mientras siga produciendo —cambia de enfoque, encuentra un caso que rompe, corrige una
> hipótesis— seguí con la ayuda mínima de los tres niveles. No cruces el gate.
>
> Cruzá el gate cuando pelear ya no produce aprendizaje. Señales, cualquiera de éstas:
> - repite el mismo enfoque fallido dos veces sin cambiar nada;
> - pidió el nivel 3 y sigue sin poder avanzar;
> - lo que falta es un conocimiento que no tiene, no un razonamiento que no hizo;
> - el reloj de la sesión se comió el presupuesto y el cansancio se nota en las respuestas.
>
> **Decíselo antes de cruzarlo**, en una línea: "acá ya no estás aprendiendo peleando, te muestro
> la solución y la analizamos". No es una capitulación ni un premio: es una decisión declarada.
>
> Al cruzar:
> 1. Mostrá la solución **y analizala**: por qué ese patrón, cuál es el invariante, dónde
>    divergió su enfoque. Explicación elaborada, no el código pelado.
> 2. Registrá `--solucion-mostrada si`.
> 3. Agendá un problema análogo, sin ayuda, a los pocos días. Anotalo en `--sigue` y en
>    `base/temas/<tema>.md`.
>
> El problema análogo no es opcional. Es lo único que distingue haber enseñado de haber dejado
> una muleta.

Y en `CLAUDE.md`, las líneas 57 y 60 se reescriben para apuntar acá en vez de prohibir.

---

## 9. Modelo de datos: tres registros

Adopto el split de la revisión y le aplico la regla del origen del dato (§1).

### Registro OBJETIVO — obligatorio, viene de afuera de mí

Ninguno de estos requiere que yo juzgue nada.

| Campo | Origen |
|---|---|
| Veredicto: `accepted` / `wrong-answer` / `tle` / `no-sometido` | LeetCode |
| Minutos hasta el enfoque correcto, y hasta Accepted | reloj |
| Problema **nuevo** o ya visto | historial |
| Pista pedida: cuántas, nivel máximo (1–3) | evento discreto |
| **Solución mostrada** (sí/no) | evento discreto |
| Resultado del problema análogo posterior | evento discreto |
| Minutos de sesión, sesión iniciada/terminada, bitácora | reloj + gate |

### Registro INFERIDO POR IA — opcional, etiquetado, nunca requisito para avanzar

Calidad del razonamiento, clase del error, claridad de la explicación, patrón probable, nivel de
comprensión. Se registran para leerlos como notas, **no se agregan en porcentajes** y **no
alimentan ningún puntaje compuesto**. Ésta es la lección de las barras ASCII de algotrace, que la
v1 criticó mientras cometía la misma falta con `dominio`.

### Registro AUTORREPORTE — del usuario

Confianza (la predicción que ya tenemos), esfuerzo, dificultad percibida. Obligatorio es legítimo
porque el valor viene de él —pero **tiene que aceptar `no-preguntada`**, para que el camino
honesto cuando me olvidé de preguntar sea más barato que inventar un valor plausible.

### Métricas principales

En este orden:

1. **Proporción de problemas NUEVOS resueltos sin ayuda.** La métrica titular.
2. **Tiempo hasta el enfoque correcto** y tiempo hasta Accepted.
3. **Cantidad y severidad de la ayuda** (pistas por nivel, soluciones mostradas).
4. **Desempeño en el problema análogo a 1–4 semanas.**
5. **Adherencia**: sesiones iniciadas y terminadas.

Tarjetas, etiquetas de error y drills pasan a ser **instrumentos auxiliares**: sirven para decidir
qué hacer en la próxima sesión, no son componentes de un porcentaje de dominio.

---

## 10. El agujero que este plan no cierra: behavioral

Sin cambios respecto de la v1. Los loops de big tech lo puntúan; nuestro sistema no lo toca;
swe-interview-coach lo tiene completo y bien hecho (`skills/behavioral-frameworks/SKILL.md`).

**No ahora**: adoptarlo entero es una segunda maquinaria compitiendo por sus 3–4 sesiones
semanales, y las cuatro debilidades que declaró son técnicas. Es adherencia, no desprecio.

**La pieza barata, si quiere**: un `base/historias.md` con 4–6 historias STAR, armado una vez y
repasado con las tarjetas que ya existen. Es el único lugar de todo el proyecto donde **DUN**
(Dunlosky et al. 2013) aplica en forma directa, porque las historias behavioral **sí** son
material declarativo, y donde SM-2 es exactamente la herramienta correcta. Decisión de él.

---

## 11. Respuesta a la revisión externa

Veredicto de la revisión: "no implementaría el plan tal como está; base científica ~7/10,
traducción a mecanismos ~4/10". **Coincido con el diagnóstico.** El defecto que nombra —convertir
cada buena idea en un gate, con números arbitrarios presentados como si se desprendieran de la
evidencia— es real y lo cometí en seis lugares que la revisión enumera correctamente: cinco
minutos, tres casos borde, 60 días, un simulacro semanal, escalera fija por problema, diferir
errores conceptuales.

### Aceptado

| # | Qué acepté | Fundamento |
|---|---|---|
| 1 | **Política adaptable > gates.** Pocas invariantes duras, todo lo demás adaptativo. | Ma et al. 2014 (g≈.42–.57, sin diferencia vs tutoría humana) respalda soporte adaptativo. Y el argumento de adherencia: cada gate es un segundo trabajo. |
| 2 | **R2**: contrastes por disparador, no ritual por ítem. | Chen, Paas & Sweller 2021: el intercalado opera por contraste discriminativo ⇒ rinde donde hay confundibilidad. Sobre un ítem bien clasificado y con alta confianza no hay contra qué contrastar. |
| 3 | **R3**: ejemplos múltiples, no respuestas canónicas. | Es además lo que estos archivos hacen mejor: cada `## Common tradeoffs` steel-manea la opción no elegida. |
| 4 | **R4**: escalera fija por problema es sobreingeniería. | Correcto. Congela la ayuda en un guion en vez de ajustarla al intento real. Acepté con una consecuencia que la revisión no nombró: obliga a rediseñar `--pista-max` como tres niveles semánticos. |
| 5 | **R5**: selectivo, 1–3 casos elegidos por la IA. | El "tres siempre" era mío y no salía de ninguna cita. |
| 6 | **R6**: 60–90 segundos de hipótesis, no 5 minutos de pelea. | **Aceptado con más fuerza de la que pidió la revisión.** Verifiqué Kornell/Hays/Bjork 2009: los materiales eran trivia ficticia y asociados de una palabra. Pan & Carpenter 2023 exige estudiar la respuesta después. Mi extrapolación era de varios saltos. Y Tetzlaff 2025 la empeora para un casi-novato. |
| 7 | **R7**: registrar la explicación, no comparar `dijo == tema`. | Correcto y grave: muchos problemas admiten varios patrones válidos (Trapping Rain Water, Top K Frequent). La igualdad de strings convierte aciertos en fallos y después alimenta la matriz de confusión con basura. |
| 8 | **R8**: comprender y reformular primero, restricciones después. | **Error mío, y es irónico.** Mi justificación era que él empareja por rasgos superficiales; propuse reemplazar un heurístico superficial por otro, específico de LeetCode. UMPIRE lo tenía bien (Understand antes que Match) y yo lo invertí. |
| 9 | **R9**: 60 días no está respaldado, y el intervalo no mide dominio. | **Aceptado dos veces.** El número: Cepeda et al. 2008 da ~5–10% del intervalo de retención para un año ⇒ ~18–36 días. **El 21 original estaba más cerca que mi 60: me equivoqué en la dirección opuesta a la que creía.** El concepto, más grave: el intervalo es propiedad del algoritmo, no de la persona. Sale el compuesto entero. |
| 10 | **R10**: desvanecer por desempeño, no por conteo. | Correcto. Y le agregué la asimetría de Tetzlaff 2025 (ver "enmiendas"). |
| 11 | **R11**: una sola producción diagnóstica. | Fatiga es costo de adherencia, y adherencia gana. |
| 12 | **R12**: no diferir errores conceptuales; secuencia dentro de la sesión. | **Aceptado casi entero, y la verificación lo respalda más de lo que la revisión citó.** g=0.03 IC[−0.08,0.13] p=.61; máxima demora estudiada 7 días; Butler et al. 2007 es prosa + multiple-choice; Van der Kleij 2015 encuentra el diferido *negativo* en entornos computarizados y el feedback elaborado (0.49) muy por encima de dar la respuesta (0.32). |
| 13 | **R13**: sin variación después de un abandono. | Correcto: ahí no hay nada que consolidar. |
| 14 | **Modelo de datos de tres registros.** | La crítica es certera: la v1 criticó las barras de algotrace y después construía un `dominio` compuesto que es la misma falta con mejor tipografía. |
| 15 | **Métricas principales propuestas.** | Adoptadas tal cual, en §9. |
| 16 | **Las seis invariantes.** | Adoptadas tal cual, más dos mías. |

### Rechazado o defendido

| # | Qué no acepté | Fundamento |
|---|---|---|
| A | **"Medir la ayuda recibida en vez de asumir que la presencia del tutor invalida el intento"** (R1). Acepté la primera mitad, rechacé la segunda. | La evidencia que trajo la propia revisión me da la razón: en Bastani et al. 2025 la ayuda estaba *disponible* y el daño (−17%) apareció en el examen sin acceso. La disponibilidad es un tratamiento: cambia la asignación de esfuerzo **antes** de que se pida una pista, y por eso contar pistas no la captura. Se mantiene una condición periódica sin ayuda disponible — pero como **medición fría**, no como role-play semanal. Cadencia adaptativa: aceptada. |
| B | **La guarda de "no expliques en el instante del fallo"** — la revisión la barre junto con el resto de R12. | Se queda, con **otro fundamento**. No es timing de feedback a través de días (ahí la revisión tiene razón y mi cita estaba mal): es **orden dentro de la sesión**, producción antes de explicación, y lo respaldan generación y autoexplicación (Kornell/Hays/Bjork; Chi et al.), no Butler/Kulik. El mecanismo estaba bien; la cita estaba mal, que no es lo mismo. |
| C | **"Política adaptable" a secas.** | Enmienda, no rechazo: **la política adaptativa tiene que estar escrita como criterio de decisión** (invariante 8). Ma et al. 2014 mide sistemas tutoriales *diseñados*, con política explícita, no un modelo improvisando. Sin criterio escrito no hay nada que auditar y nada sobrevive al turno 40. Menos gates sí; menos criterios escritos no. |
| D | **La atribución a Kestin et al.** | La revisión dice "grandes ganancias con un tutor cuidadosamente diseñado, ninguna con acceso libre a un chatbot". La primera mitad es correcta (RCT, N=194, Harvard, más del doble de aprendizaje en menos tiempo). La segunda no es de Kestin: su brazo de comparación fue **clase presencial de aprendizaje activo**, no un chatbot libre. Ese hallazgo es de Bastani et al. 2025. La conclusión conjunta se sostiene; la atribución no. |
| E | **La asimetría del desvanecimiento** (R10). | No es rechazo sino agregado que sale de la cita de la revisión: Tetzlaff et al. 2025 concluye que **dar asistencia a los novatos importa más que retirarla a los expertos**. Entonces la regla adaptativa no es simétrica: **ante la duda, mantener el andamiaje**. Es lo contrario del sesgo natural de un sistema orgulloso de no ayudar, que era el sesgo de la v1. |

### Las dos objeciones del coordinador a la revisión

**1. "Pide menos mecanismo y más juicio adaptativo, y a la vez dice que la IA no debe ser juez
único de la medición. Si casi todo pasa a política adaptable, casi toda la métrica pasa a ser
inferida."**

**Coincido con el coordinador, y su lectura de la salida es la correcta.** La tensión es real
pero no es contradicción, y la resolución está en el propio split de tres registros de la
revisión — con la consecuencia que efectivamente no explicita: **la instrumentación no se
adelgaza, se mueve.**

Mirado campo por campo, el registro OBJETIVO que propone la revisión está compuesto casi
enteramente de cosas que `study.py` puede capturar **sin que yo juzgue nada**: veredicto de
LeetCode, reloj, problema nuevo o visto, pista pedida (evento), solución mostrada (evento),
resultado del análogo (evento). Ninguna es un juicio. Entonces "menos ritual" y "más
instrumentación objetiva" son compatibles: **lo que se borra son los juicios míos disfrazados de
datos** —`--acerto` por igualdad de strings, `--error-clase` como taxonomía canónica, el `dominio`
compuesto— **y lo que se agrega es captura de eventos.** El saldo del lado objetivo es más
instrumentación, no menos. Lo confirmo y lo escribí así en §9.

Le agrego el mecanismo que hace que eso funcione, que es la regla del origen del dato (§1): un
flag obligatorio es un mecanismo cuando su valor viene de afuera de mí, y una invitación a
fabricar cuando es juicio mío.

**2. "Leyó mal la arquitectura: los flags los pasa el asistente, no el usuario."**

**Correcto, y corregí todos los puntos donde el argumento dependía de esa premisa** — sobre todo
la parte de R4 donde la revisión califica de sobreingeniería lo que en realidad no le cuesta nada
al usuario. (R4 igual cae, pero por la razón buena: la escalera enlatada congela la ayuda en un
guion, no porque él tenga que recordar nada.)

**Y agrego un costo que el coordinador no nombró y que es peor que el que nombró.** Que la sesión
se trabe si no tengo el dato es la mitad del problema. La otra mitad: **cuando un flag obligatorio
me traba, el camino más barato para destrabarlo es inventar un valor plausible.** `--prediccion`
pasó a `required=True` después de la v1; si me olvido de preguntarle, el sistema no me deja
avanzar, y el gradiente apunta a que complete una predicción verosímil en vez de admitir que no
la pedí. Un flag obligatorio cuyo valor sólo yo puedo suplir no es un mecanismo: es un generador
de datos sintéticos con apariencia de registro.

Por eso la mitigación no es sacar la obligatoriedad —el valor de `--prediccion` viene de él, así
que obligarlo es legítimo— sino **agregar el valor explícito `no-preguntada`**, de modo que
declarar el hueco sea más barato que rellenarlo. Esa regla se generaliza a todo campo obligatorio
del registro de autorreporte.

---

## 12. Orden de ejecución

**Ahora (revierten o simplifican lo ya hecho)**
1. Reescribir `OVERRIDES.md` §solution-mode como el gate de §8; ajustar `CLAUDE.md` 57 y 60.
2. Eliminar `dominio_por_tema()`, el compuesto y `HORIZONTE_DOMINIO_DIAS`; sacar la sección
   correspondiente de `metricas/SKILL.md`.
3. Sacar la comparación automática de `--dijo`; conservar el campo como texto.
4. Agregar `no-preguntada` a `--prediccion`.
5. Corregir la ruta rota en `fuentes/SKILL.md`.
6. Corregir `base/perfil.md`: "teoría primero" pasa a estar rotulada como preferencia de
   adherencia, no como hallazgo.

**Campos objetivos nuevos en `study.py`** (esto es el grueso del trabajo, y es todo captura de
eventos, sin juicio)
7. `--veredicto accepted|wrong-answer|tle|no-sometido`.
8. `--problema-nuevo si|no`.
9. `--solucion-mostrada si|no` y `--analogo-de <ejercicio>` para cerrar el ciclo del gate.
10. `--pista-nivel 1|2|3` reemplazando `--pista-max 0-5`.
11. Reporte reescrito sobre las cinco métricas de §9.

**Cambios de ritual, sin código**
12. R8 en el orden correcto; R12 con la secuencia dentro de la sesión; R11 con una sola
    producción; R10 con desvanecimiento por desempeño y sesgo a mantener.
13. R2 con disparadores y pares curados.
14. Los criterios escritos del gate (§8), incluida la regla de los 20 minutos rescatada de
    `study-plan.md`.

**Contenido**
15. R3 — importar los 8 casos de sysdesign como ejemplos múltiples. Una tarde.

**A prueba, con criterio de salida**
16. R5 (casos borde selectivos) y R6 (hipótesis de 60–90 s). Si en tres semanas cortan ejercicios
    por tiempo o le bajan las ganas, se sacan.

---

## 13. Resumen

Los dos repos siguen aportando cosas distintas y casi no se pisan: **swe-interview-coach aporta
contenido canónico y mecanismos que obligan**; **algotrace aporta ideas pedagógicas sueltas sin
forma de obligarlas** y un archivo de 31 KB para cosechar y tirar. Eso no cambió entre v1 y v2.

Lo que cambió es qué hacer con nuestro sistema. La v1 decía que el problema más caro era que la
métrica titular se mide en la condición equivocada. **Eso sigue siendo cierto y ahora tiene
respaldo empírico** (Bastani et al. 2025: +48% con ayuda, −17% sin ella). Pero la v1 respondía a
ese problema con más rituales, y ése era el error: la respuesta correcta es **menos gates, más
captura de eventos objetivos, y una política adaptativa escrita**. La única invariante que se
endurece es la que la evidencia señala como crítica —ayuda mínima adaptada, nunca respuestas a
pedido— y ésa es exactamente la que el cambio de restricción pone en juego.
