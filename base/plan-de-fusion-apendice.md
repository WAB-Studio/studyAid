# Apéndice del plan de fusión

Material de respaldo de `base/plan-de-fusion.md`. **No hace falta leerlo para operar el sistema.**
Está acá para que las decisiones sean auditables y para no re-litigar el mismo debate en tres
meses.

Contiene: la evidencia verificada, la respuesta a las dos revisiones externas, lo que se descartó
de los dos repos, y las preguntas abiertas.

---

## 1. Evidencia verificada

Verifiqué con búsqueda. No acepté nada por autoridad, ni mío ni de los revisores.

### Sobre sistemas de estudio asistidos por IA

| Hallazgo | Fuente | Qué dice, con precisión |
|---|---|---|
| IA sin guardas daña el desempeño posterior | Bastani, Bastani, Sungu, Ge, Kabakcı & Mariman 2025, *PNAS* 122(26) e2422633122 | ~1000 alumnos de secundaria, Turquía, 4 sesiones de 90 min. **GPT Base**: +48% en práctica, **−17% en el examen sin acceso**. **GPT Tutor** (pistas en vez de respuestas): +127% en práctica, **≈0 en el examen — igual que el control, no mejor**. |
| El diseño pedagógico decide el resultado | Kestin et al. 2025, *Scientific Reports* | RCT, N=194, física intro en Harvard. Tutor a medida vs **clase presencial de aprendizaje activo**: más del doble de aprendizaje en menos tiempo. |
| Los ITS funcionan y se acercan a tutoría individual | Ma, Adesope, Nesbit & Liu 2014, *JEP* 106(4), doi 10.1037/a0037123 | 107 efectos, 14.321 participantes. g=.42 vs grupo grande, g=.57 vs instrucción computarizada no-ITS, g=.35 vs libro. **Sin diferencia significativa vs tutoría humana individual (g=−.11).** |
| La pista mínima no es la mejor política | Rus, Banjade, Niraula & Gire, *A Study on Two Hint-Level Policies in Conversational ITS* (digitalcommons.memphis.edu/facpubs/2424) | RCT, andamiaje mínimo vs máximo en DeepTutor. Ganancias significativas en ambos, y: los alumnos **necesitan más que una pista mínimamente informativa** para inferir el paso siguiente en problemas desafiantes. |
| Las pistas bajo demanda ayudan condicionalmente | Aleven, Roll, McLaren & Koedinger 2016, *IJAIED* 26(1), doi 10.1007/s40593-015-0089-1 | El título es la conclusión: *"Help Helps, But Only So Much"*. El pedido de ayuda puede evitarse o abusarse. |
| Los traces no son válidos por ser automáticos | Winne 2020, doi 10.1016/j.chb.2020.106457 | **Tomado del segundo revisor, no verificado por mí.** Es una advertencia metodológica modesta y la acepto como tal. |

### Sobre aprendizaje

| Línea | Fuente | Estado tras verificar |
|---|---|---|
| **Intercalado / discriminación** | Rohrer, Dedrick & Stershic 2015, *JEP* 107(3), 900–908 | Confirmado. 126 alumnos de 7.º, 3 meses. El diseño requiere **elegir la estrategia a partir del problema mismo**. Es lo más cercano a su debilidad principal. |
| **Mecanismo del intercalado** | Chen, Paas & Sweller 2021, *Educ. Psych. Rev.*, doi 10.1007/s10648-021-09613-w | Revisión sistemática. Espaciado e intercalado tienen bases distintas: el intercalado opera por **contraste discriminativo** ⇒ rinde donde las categorías son confundibles. |
| **Reversión por pericia** | Tetzlaff, Simonsmeier, Peters & Brod 2025, *Learning and Instruction* 98, doi 10.1016/j.learninstruc.2025.102142 | 176 efectos, 60 estudios, 5924 participantes. El efecto existe, moderado por nivel educativo y dominio. Y: *"dar asistencia a los novatos parece más importante que retirarla a los expertos"*. **Pero es un promedio meta-analítico: no determina la decisión de un tutor individual** (ver §2). |
| **Feedback: timing** | Meta-análisis 2026, *Educ. Psych. Rev.*, doi 10.1007/s10648-026-10117-8 | 51 estudios (1988–2024), 160 efectos, RVE. **g = 0.03, IC95% [−0.08, 0.13], p = .61.** Demoras estudiadas: 1 segundo a **7 días**. |
| **Feedback: tipo** | Van der Kleij, Feskens & Eggen 2015, *RER* | Elaborado g=0.49 ≫ respuesta correcta 0.32 ≫ correcto/incorrecto 0.05. El timing diferido afecta **negativamente** en entornos computarizados. |
| **Feedback diferido, el caso a favor** | Butler, Karpicke & Roediger 2007, *JEP:Applied* 13(4), 273–281 | Existe, **y está acotado**: prosa y multiple-choice de conocimiento general, 24 h. No licencia diferir un error conceptual de algoritmo. |
| **Espaciado** | Cepeda, Vul, Rohrer, Wixted & Pashler 2008, *Psych. Science* 19, 1095–1102 | Gap óptimo ~20–40% de un intervalo de retención de 1 semana; **~5–10% de uno de 1 año** ⇒ ~18–36 días. |
| **Pretesting** | Kornell, Hays & Bjork 2009, *JEP:LMC*; Pan & Carpenter 2023, doi 10.1007/s10648-023-09814-5 | Confirmado **y muy acotado**: los materiales fueron trivia ficticia y asociados de una palabra. El beneficio requiere estudiar la respuesta correcta después. |
| **Estilos de aprendizaje** | Pashler, McDaniel, Rohrer & Bjork 2008, *PSPI* | No lograron respaldar la hipótesis de emparejamiento. "No hay base de evidencia adecuada." |
| **Práctica deliberada** | Ericsson et al. 1993 **con** Macnamara, Hambrick & Oswald 2014, *Psych. Science* 25 | 88 estudios, N=11.135. Explica **26%** de la varianza en juegos, 21% música, 18% deportes, **4% educación, <1% profesiones**. Las horas son un insumo, no evidencia de progreso. |
| **Ejemplos resueltos** | Sweller & Cooper 1985; Renkl (desvanecimiento); Kalyuga et al. 2003 | Vigentes. Renkl es de dónde salen los peldaños intermedios de la escalera de ayuda (completar, subproblema resuelto). |
| **Autoexplicación** | Chi et al. 1989, 1994 | Vigente. Es el fundamento correcto de "producí antes de que yo explique". |
| **Transferencia** | Barnett & Ceci 2002 | Vigente como advertencia: la transferencia lejana es difícil. |
| **Dunlosky et al. 2013** | | Vigente **pero acotado a lo declarativo**. No es la literatura principal acá: el usuario adquiere una habilidad procedimental con transferencia. |

### Sin verificar

- No pude abrir el texto de Cepeda et al. 2008 (certificado vencido en un mirror, PDF binario en
  ERIC). **No sostengo** que la función alrededor del óptimo sea ancha ni que errar hacia gaps
  largos sea más seguro.
- Winne 2020: tomado del revisor.

---

## 2. Respuesta a la segunda revisión externa

Veredicto del revisor: base científica 8/10, disciplina al extrapolar 6/10, arquitectura 5/10,
**practicidad 3/10**. "La v2 corrigió rituales, pero respondió agregando nuevas taxonomías,
invariantes, registros, métricas y un gate muy elaborado. Creció de 740 a 816 líneas."

**Coincido con el diagnóstico y con el remedio.** El defecto es real: cada crítica a un ritual la
respondí con una abstracción nueva. Y la observación de fondo es la que más pesa — el sistema no
tuvo una sola sesión. Podé el documento a cuatro secciones y moví esto acá.

### Aceptado

| # | Qué acepté | Por qué |
|---|---|---|
| 1 | **"El aprendiz produce primero" no puede ser absoluto.** Split enseñar / practicar / medir. | Es el mejor punto de la revisión y es una **autocontradicción de la v2**: escribí esa invariante como absoluta mientras argumentaba con Sweller, Renkl y Tetzlaff que el ejemplo resuelto debe *preceder* al intento en un novato. No se puede tener las dos. |
| 2 | **La v2 le atribuye a PNAS más de lo que prueba.** | Verificado punto por punto. No muestra que la presencia silenciosa perjudique (los brazos difieren en lo que la IA *hace*, no en si está); no valida "ayuda mínima"; no valida el problema análogo como única verificación; y el GPT Tutor terminó **igual que el control**, dato que yo mismo reporté y después usé retóricamente como si fuera una victoria. Quedan las dos conclusiones modestas de §1 del plan. |
| 3 | **"Ayuda mínima" es mala política; va "contingente y suficiente".** | Verifiqué las dos citas y las dos aguantan (Rus et al.; Aleven et al. 2016). Peor para mí: **mi propia evidencia ya lo decía** — Van der Kleij tiene feedback elaborado en 0.49 contra 0.32 y 0.05. Cité eso en la v2 y aun así escribí "mínima ayuda necesaria" como invariante. |
| 4 | **El gate saltaba de pista a solución completa.** | Correcto, y otra vez es inconsistencia interna: los peldaños que propone —enseñar el concepto faltante, subproblema resuelto, comparar enfoques, completar una parte, pseudocódigo, otro ejemplo— son exactamente el desvanecimiento de Renkl que la v2 citaba en R10 y no usaba en el gate. |
| 5 | **No decirle "acá ya no estás aprendiendo".** | Epistémicamente correcto: no lo sé. La frase alternativa es mejor y además no suena a sentencia. |
| 6 | **"Evento observable" ≠ "dato objetivo"**, y la solución es un campo `fuente:`, no otra taxonomía. | Correcto en los cinco casos que lista. El más importante: **el veredicto de LeetCode es autorreporte** mientras yo no vea la página, y en nuestro setup no la veo. Su fix es más chico y mejor que mis tres registros: mi "regla del origen del dato" estaba bien, mi implementación era pesada. |
| 7 | **Tres niveles de pista tampoco son una escala ordinal.** | Correcto, y me deja sin el argumento con el que defendí R4 en la v2. Reemplacé una escala mala de 5 por una escala mala de 3. Va `soporte: ninguno\|pista\|explicación\|solución`. |
| 8 | **"Nuevos resueltos sin ayuda" no es longitudinal por sí sola.** | Correcto y filoso: **yo elijo la dificultad y después juzgo mi propio éxito**. Es el mismo problema de validez que le critiqué al sistema, cometido por mí. Se reporta desagregado. La batería fría estratificada es la solución completa, pero construirla ahora sería exactamente el sobrediseño que la revisión critica: queda en backlog. |
| 9 | **`micro`/`fondo` mezclan dimensiones.** Intención pedagógica ⟂ duración. | Correcto, y explica de dónde salían las reglas arbitrarias (micro antes de las 18:00, nunca teoría nueva en micro). Se unifica con el punto 1. |
| 10 | **El sistema sobrevalora el pattern matching.** Su secuencia de 7 pasos, con el nombre del patrón al final. | Correcto, y absorbe además la corrección que ya había aceptado en la ronda anterior (comprender antes que restricciones). "Adivinar la etiqueta de LeetCode" es un riesgo real. |
| 11 | **Contrastar contra el candidato que el usuario realmente consideró**, no contra pares fijos. | Mejora concreta sobre mis "pares curados". Los pares quedan como ejemplos. |
| 12 | **R3: apuntar a `referencia/…/library/sysdesign/`, no copiar ocho archivos.** | Obviamente mejor. Ya están en el repo. |
| 13 | **R5, R6, R11 como intervenciones disponibles, no features.** | Correcto. Eran justamente las tres que yo mismo había marcado "a prueba, con salida"; convertirlas en política adaptable es la conclusión coherente. |
| 14 | **R13: prioridad de repaso, no deuda uno a uno.** | Correcto. Un ejercicio posterior puede verificar varias piezas. |
| 15 | **El umbral de 21 días de "temas fríos"**: heurística de interfaz rotulada, no frontera. | Correcto. Sobrevivía disfrazado a mi propia crítica en R9. |
| 16 | **Los seis puntos de "otros fundamentos del repo"**: ritual sobre un saludo, micro/fondo por hora, cuota de tarjetas, churn documental, diagrama dibujado, behavioral. | Todos correctos. Los tres que tocan restricciones declaradas por el usuario van como decisiones suyas, no mías. |
| 17 | **Behavioral no es sólo contenido declarativo.** | **Corrección directa a lo que yo escribí.** SM-2 sobre historias no practica selección, comunicación oral ni follow-ups. Una práctica mensual sirve más. |
| 18 | **Podar el documento a cuatro secciones.** | Hecho. El agente operativo necesita reglas, no reconstruir el debate cada sesión. |
| 19 | **El refactor mínimo de cinco puntos, y estudiar 6–10 sesiones antes de decidir más.** | Adoptado tal cual como §4 del plan. |

### Corregido o matizado

| # | Qué | Fundamento |
|---|---|---|
| A | **"El gate de bitácora transforma una sesión real en una sesión inexistente."** Corrección fáctica menor. | La sesión **sí se persiste**: `cmd_cerrar` escribe siempre en `sessions.jsonl` con `estado: incompleta`; lo que hace es excluirla de `completas()`. El dato no se borra, la métrica se sesga. **Pero el argumento de fondo es correcto y le agrego una versión más fuerte**: `CLAUDE.md` dice "nunca uses `--sin-bitacora` por tu cuenta", así que la salida honesta está bloqueada y el camino barato es escribir una bitácora de compromiso. Es la misma trampa de fabricación que ya habíamos identificado en los flags obligatorios, aplicada al contenido cualitativo. |
| B | **"Ante la duda, mantener el andamiaje" (mi enmienda de la v2 a R10).** El revisor la retira. | **Acepto retirarla como regla**, y la razón que él da es correcta: un promedio meta-analítico no determina la decisión de un tutor sobre una persona en un momento. Lo que queda de Tetzlaff et al. 2025 es una **advertencia sobre el sesgo de un sistema orgulloso de no ayudar**, no una regla de decisión. Queda anotada acá, no en la política. |
| C | **El drill de discriminación.** El revisor lo subsume en su secuencia de 7 pasos. | De acuerdo con reordenarlo y con que el nombre del patrón vaya último. **Defiendo que el drill se quede** como intervención: el usuario declaró el reconocimiento como debilidad #1, y Rohrer et al. 2015 es la evidencia más cercana que existe a eso. La corrección que acepto es *qué* se contrasta: enfoques, no etiquetas — que es exactamente su punto. |

### Lo que este apéndice conserva y el plan no

Por pedido explícito del revisor, el documento operativo no lleva tamaños de efecto repetidos,
historiales "era/ahora", ni la defensa de cada decisión. Todo eso está acá.

---

## 3. Respuesta a la primera revisión externa (resumen)

Veredicto: "base científica ~7/10, traducción a mecanismos ~4/10". Diagnóstico: la v1 convertía
cada buena idea en un gate, con números arbitrarios presentados como si se desprendieran de la
evidencia.

**Acepté**: política adaptable sobre gates; contrastes por disparador; ejemplos múltiples en vez
de respuestas canónicas; escaleras enlatadas por problema como sobreingeniería; casos borde
selectivos; hipótesis corta en vez de 5 minutos de pelea; registrar la explicación en vez de
comparar strings; comprender antes que restricciones; eliminar el compuesto de dominio; desvanecer
por desempeño; una sola producción diagnóstica; no diferir errores conceptuales; el split de
registros; las métricas propuestas.

**Errores míos que salieron de esa ronda**, y que dejo anotados porque son el tipo de error que
tiende a repetirse:

1. **R9, verificable y en dirección contraria a la que yo creía.** Argumenté que el techo de 21
   días era corto para un horizonte de 6–12 meses y lo subí a 60. Cepeda et al. 2008 da ~5–10% del
   intervalo de retención para un año ⇒ ~18–36 días: **el 21 original estaba más cerca**. Había
   escrito "no estoy seguro de la proporción exacta" y usé esa incertidumbre para mover el número
   donde me convenía.
2. **R8, irónico.** Mi justificación era que él empareja por rasgos superficiales del enunciado, y
   propuse reemplazar un heurístico superficial por otro (leer las cotas antes que la semántica),
   además específico de LeetCode.
3. **R12, la peor.** Cité Butler/Karpicke/Roediger para diferir errores conceptuales por días. El
   meta-análisis 2026 da g=0.03 IC[−0.08,0.13] p=.61, la demora máxima estudiada es 7 días, y el
   material de Butler es prosa con multiple-choice.

**Lo que defendí en esa ronda y sobrevivió a la segunda**: que la guarda de "no expliques en el
instante del fallo" se queda, pero como regla de **orden dentro de la sesión** (producción antes de
explicación), respaldada por generación y autoexplicación, no por timing de feedback. El mecanismo
estaba bien; la cita estaba mal.

**Lo que defendí en esa ronda y la segunda derribó**: que la mera disponibilidad de ayuda invalida
el intento. PNAS no lo muestra. Lo que sobrevive es la conclusión modesta: no interpretar desempeño
asistido como aprendizaje independiente. La medición fría se queda por esa razón, no por la mía.

---

## 4. Los dos repos: qué se toma y qué no

Esto no cambió a lo largo de las tres versiones.

**swe-interview-coach** aporta contenido canónico y mecanismos que obligan: los ocho diseños de
sysdesign (que ahora se usan **in situ**, sin copiar), el reloj real (`date +%s`, "never guess
times"), el split mock/practice, la degradación elegante ("nunca abortes el coaching por un
problema de tooling"). Su `weak-patterns.md` infiere debilidad de 2–3 reps y no sirve; sus rúbricas
de 6 ejes mezclan un eje anclado con cinco inferidos en la misma tipografía, que es el error a no
copiar.

**algotrace** aporta ideas pedagógicas sueltas sin forma de obligarlas: la escalera semántica de
pistas, el trace probatorio del bug (su mejor idea), el decodificador de jerga, las formas de caso
borde de `testgen.py`. Su reloj de interview-mode está **inventado** ("no real clock exists"); su
log de progreso es opcional por diseño y por lo tanto no mide; sus intervalos se contradicen entre
dos archivos (+3/+7/+21 vs 1/3/7/16/35); su Progress Score con barras ASCII es retórica disfrazada
de medición — y la v1 y la v2 lo criticaron mientras construían un `dominio` compuesto que era la
misma falta con mejor tipografía.

**Descartado, con razón registrada**:

- **Canvas de Excalidraw**: requiere node + lsof + navegador. El diagrama se hace en papel, ASCII o
  Mermaid.
- **Harness de Python**: los ejercicios se resuelven en leetcode.com. Lo que se pierde es la única
  señal objetiva de corrección de los dos repos; el reemplazo es el veredicto de LeetCode, mejor
  como juez pero **autorreportado** en nuestro setup.
- **`/coding-import`**: `referencias-ts/problemas.md` ya es el índice.
- **`prompts/universal-system-prompt.md`** (31 KB): cosechar §11 (matriz de selección), §12
  (invariantes por patrón), §16 (verificación), Apéndice B (misconceptions), Apéndice D
  (presupuesto de complejidad); borrar §8 (estilos de aprendizaje, contradice Pashler et al. 2008),
  §9 (el "X% correcto" fabricado) y §20 (barras ASCII sin fuente).
- **`docs/study-plan.md`** (90 min/día × 6 días × 8 semanas): incompatible con su disponibilidad.
  Rescatar su regla de escalada, que es una dificultad deseable bien calibrada: *trabado menos de
  20 minutos, no toques la skill*.
- **El sistema de progreso paralelo de `modes/review-mode.md`** y su "offer, never nag".
- **La maquinaria behavioral completa**: compite por las 3–4 sesiones semanales.

---

## 5. Preguntas abiertas

1. ¿SM-2 con los intervalos por defecto es adecuado para un horizonte de 6–12 meses? Cepeda sugiere
   gaps del orden de semanas para ese horizonte, pero es sobre hechos. Sobre las tarjetas aplica
   razonablemente; sobre los ejercicios no aplica. **Decidir con datos, no ahora.**
2. ¿La función de Cepeda alrededor del óptimo es ancha? No lo pude verificar, así que no se puede
   argumentar sobre si conviene errar largo o corto.
3. ¿Cuánto de lo que se aprende en un patrón transfiere a otro? Barnett & Ceci advierte que poco.
   Si es así, lo único portante es reformular, generar candidatos y discriminar — y eso hay que
   medirlo, no suponerlo.
4. Las tres decisiones que son del usuario: gate de bitácora, arranque automático, behavioral.
