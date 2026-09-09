# Plan de fusión v3

Documento operativo. Cuatro secciones. La evidencia, el historial de versiones y la respuesta a
las dos revisiones externas están en `base/plan-de-fusion-apendice.md`.

**Por qué esta versión es más corta que las anteriores.** La v1 y la v2 diseñaban un sistema
tutorial completo antes de tener una sola sesión: `data/sessions.jsonl` está vacío y
`data/cards.json` no tiene tarjetas. La segunda revisión externa lo señaló y tiene razón: no hace
falta una v3 más sofisticada, hace falta una poda, arreglar las contradicciones que ya existen en
el repo, y empezar a estudiar. Lo que sigue es lo mínimo para eso.

---

## 1. Objetivo

Preparar entrevistas de big tech a 6–12 meses, trabajando full time, con 3–4 sesiones de fondo
por semana más micro-sesiones.

Las cuatro debilidades declaradas: reconocer el patrón, estructuras y complejidad, implementar sin
bugs bajo presión, system design.

**El riesgo que el sistema tiene que evitar** está medido: en un experimento de campo con ~1000
alumnos, el brazo con ChatGPT sin guardas subió el desempeño **con** la ayuda presente y lo bajó
**17%** en el examen posterior sin ayuda; el brazo con guardas (pistas en vez de respuestas)
evitó ese daño (Bastani et al. 2025, PNAS). De ahí salen dos decisiones, y sólo dos:

1. **No interpretar desempeño asistido como aprendizaje independiente.**
2. **No entregar respuestas de forma irrestricta.**

Todo lo demás de este documento es criterio de diseño, no evidencia.

---

## 2. Política: enseñar / practicar / medir

Tres intenciones. Son **independientes de la duración**: `micro` y `fondo` siguen existiendo como
presupuestos de tiempo, no definen qué se puede hacer.

| Intención | Conducta |
|---|---|
| **Enseñar** | Explicación, ejemplos resueltos y práctica guiada permitidos. La IA puede ir primero. |
| **Practicar** | Intento primero, ayuda contingente. |
| **Medir** | Problema nuevo, IA en silencio hasta que termine. |

La regla anterior —"ninguna explicación precede a un intento"— queda anulada. Era una restricción
absoluta que contradecía la evidencia sobre ejemplos resueltos: para alguien sin conocimiento
previo, forzar un intento produce ruido y frustración.

### Ayuda contingente y suficiente, no mínima

> **Dar la menor ayuda que restablezca progreso productivo, y escalar rápido cuando lo que falta
> es conocimiento y no razonamiento.**

"Ayuda mínima" es mala política y hay evidencia en contra: comparando andamiaje mínimo contra
máximo en un tutor conversacional, los alumnos necesitan más que una pista mínimamente informativa
para inferir el paso siguiente en problemas difíciles (Rus et al.). Y el feedback elaborado rinde
mucho más que dar la respuesta pelada o el mero correcto/incorrecto (Van der Kleij et al. 2015).

### Escalera de ayuda

Cuando deja de progresar, **no se salta de una pista a la solución completa**. Estas son las
intervenciones disponibles, no una secuencia que se recorra entera: elegí la menos invasiva que
probablemente le devuelva progreso, y si lo que falta es conocimiento y no razonamiento, salteá
peldaños sin culpa.

1. Pista sobre lo que se le pasó.
2. Enseñar el concepto que falta, si lo que falta es conocimiento.
3. Un subproblema resuelto, o comparar dos enfoques, o completar una parte que ya está armada.
4. Pseudocódigo, o el mismo patrón enseñado sobre **otro** problema.
5. La solución del problema objetivo, explicada: por qué ese enfoque, cuál es el invariante, dónde
   divergió el suyo.

Escalá cuando la intervención actual dejó de mover la aguja. **No le digas "acá ya no estás
aprendiendo"** —no lo sabés—. Decí: *"parece más útil cambiar de estrategia y enseñarte la pieza
que falta"*.

Llegar a mostrar la solución objetivo crea una **prioridad de repaso**, no una deuda de un problema análogo
uno a uno: el tema vuelve antes y con un problema variado, y un mismo ejercicio posterior puede
verificar varias piezas.

### Cómo elegir el enfoque (reemplaza "primero el patrón")

El nombre del patrón va **último**, no primero. Leer las cotas antes que la semántica enseña un
heurístico superficial y específico de LeetCode.

1. Reformular el problema y acordar el contrato de entrada/salida.
2. Ejemplos y propiedades.
3. Solución ingenua y su costo.
4. Restricciones, para descartar complejidades.
5. Estructuras candidatas.
6. Invariante y argumento de corrección.
7. Recién ahí, si ayuda, el nombre del patrón.

**Contraste discriminativo**: cuando hay confusión, baja confianza o patrón nuevo, pedir por qué
**no** el otro candidato — y contrastar principalmente contra el candidato que él realmente
consideró, no contra una taxonomía fija. Pares útiles como ejemplo, no como catálogo:
`sliding-window`/`prefix-sum`, `two-pointers`/`binary-search`, `dp-1d`/`greedy`,
`backtracking`/`dfs`. Es el mecanismo con mejor evidencia para su debilidad principal
(Rohrer et al. 2015; Chen, Paas & Sweller 2021).

### Errores y cierre

- **Los errores importantes se corrigen en la misma sesión.** La secuencia: resultado crudo →
  una oportunidad breve de trace y autodiagnóstico suyos, mientras siga produciendo información
  útil → ayuda si sigue bloqueado → corrección conceptual completa, dentro de la sesión.
- Lo que se mantiene de la guarda vieja es **el orden, no la demora**: producción antes de
  explicación. No es timing de feedback, es generación y autoexplicación.
- **Al cierre, pedí una producción diagnóstica cuando ayude a comprobar o consolidar lo
  trabajado** — el patrón y por qué, o el invariante, o la complejidad justificada, o el trace.
  Una, nunca las cuatro, y no en toda sesión: es contextual, no un ritual de cierre.
- El trace y el diagrama los produce **él**; yo marco dónde diverge. (Anula el contrato de
  algotrace que obliga al tutor a dibujar en toda respuesta; en modo enseñar está bien.)

### Soporte que se retira según evidencia del intento

Los ejemplos resueltos y el andamiaje se retiran **según cómo le fue** —intento independiente,
calidad de la explicación, errores, ayuda pedida—, no por número de exposición ni por una regla
fija.

### Medición fría

Un problema nuevo, sin ayuda disponible durante el intento, programado con separación suficiente
para que un cambio sea observable. La primera repetición de la línea base va a las 4–6 semanas;
esa separación es un default para arrancar, no una cadencia permanente.

**Se reporta desagregada por tema, dificultad y novedad. No se resume en una sola curva.** Si yo
elijo la dificultad y después juzgo mi propio éxito con un único porcentaje, el número no sirve:
sube eligiendo fácil y baja eligiendo difícil, en los dos casos sin relación con el progreso.

### System design

El entregable sigue siendo conversación estructurada, pero **el diagrama se dibuja**: papel, ASCII
o Mermaid. No hace falta instalar nada, y "diagrama en palabras" deja una brecha de transferencia
si la entrevista exige dibujar.

Los ocho diseños canónicos de `referencia/swe-interview-coach/library/sysdesign/` se usan **desde
donde están**, sin copiarlos, y **como ejemplos múltiples, no como respuestas**: su mejor
propiedad es que cada sección de tradeoffs defiende bien la opción que no eligió.

---

## 3. Datos mínimos

Un registro por ejercicio. Nada más hasta que haya sesiones reales.

```
ejercicio
tema
visto:       si | no | desconocido
soporte:     ninguno | pista | explicacion | solucion
veredicto:   accepted | wrong-answer | tle | no-sometido
prediccion:  opcional
```

**Sin escala numérica de pistas.** Los niveles no son una escala ordinal comparable: una
reformulación puede revelar casi todo, nombrar "sliding window" puede ser más decisivo que dar el
invariante, una pista de debugging no entra en la escala, y system design necesita otras clases de
ayuda. Si más adelante sirve, se guarda el **tipo** de pista como nota (comprensión, estrategia,
implementación, debugging) — nunca como `/3` ni `/5`.

**Procedencia declarada en el reporte, todavía no en el esquema.** El campo `fuente:` por
registro queda en backlog hasta que haya un consumidor: agregarlo ahora es otra pieza sin uso.
Lo que sí es obligatorio desde el día uno es que el reporte y la documentación digan de dónde
sale cada número — el veredicto de LeetCode lo reporta él, los tiempos salen del reloj, las
evaluaciones las produzco yo. La forma futura del campo, cuando haga falta:

```
fuente: plataforma | reloj | usuario | IA
```

Y el registro **no se llama "objetivo"**. Que un dato se haya guardado automáticamente no lo hace
válido. En particular: el veredicto de LeetCode es `fuente: usuario` mientras yo no vea la página;
"problema visto" es objetivo sólo respecto del historial del repo; y "tiempo hasta el enfoque
correcto" tiene un timestamp real pero decidir *cuándo* el enfoque se volvió correcto es juicio
mío, así que por ahora no se registra.

**Nada de puntajes compuestos.** Ya se eliminó `dominio_por_tema()`. No vuelve en otra forma.

**Tarjetas**: se generan por lo que efectivamente falló o quedó marcado, no por cuota de 4–8 por
tema. Con el tope de 20 vencidas por sesión, una cuota fija produce 80–160 tarjetas antes de saber
si aportan.

---

## 4. Cambios de ahora, y backlog

### Ahora — unas pocas horas, y el momento más barato porque no hay datos que migrar

0. **Fijar la línea base y ejecutar la forma A.** Es la única tarea que pierde valor por
   postergarse: no existe una observación del nivel de partida, y esa observación no se
   reconstruye después. Formas A y B especificadas en `base/linea-base.md`; los problemas de B
   están marcados `[RESERVADO]` en el índice y no se usan para enseñar ni practicar. Ejecutar A
   **antes** de la primera sesión de estudio.

1. **Sincronizar CLI y documentación.** El repo hoy es incoherente:
   - `study.py sesion patron` exige `--dijo` y `--valido`; `CLAUDE.md:40`, `CLAUDE.md:142` y
     `OVERRIDES.md:66` todavía documentan `--acerto si|no`.
   - `metricas/SKILL.md:35` explica el puntaje de dominio que ya no existe, y su `description`
     todavía lo promete.
   - `metricas/SKILL.md:31` explica el "nivel de pista promedio" sobre una escala `/5` que este
     plan elimina.
2. **Reemplazar "nunca soluciones" y el gate largo** por la política corta de §2, en `CLAUDE.md`
   (líneas 57–60) y en `OVERRIDES.md`.
3. **Reducir el registro de ejercicios** al esquema de §3: sacar `--pista-max`, agregar `--visto`,
   `--soporte` y `--veredicto`.
4. **Hacer que las sesiones cuenten aunque falte bitácora** (ver la decisión pendiente abajo).
5. **Corregir dos cosas menores**: la ruta rota a `.claude/skills/leetcode/referencias/` en
   `fuentes/SKILL.md`, y `base/perfil.md`, donde "aprende con teoría primero" tiene que quedar
   rotulado como **preferencia de adherencia**, no como hallazgo — no hay respaldo para emparejar
   instrucción a estilo autodeclarado (Pashler et al. 2008).
6. **Rotular el umbral de 21 días de "temas fríos"** como heurística de interfaz, no como frontera
   científica.

### Después — estudiar 6–10 sesiones antes de decidir nada más

Nada de esto se construye ahora. Se decide con datos:

- conteo o tipología de pistas;
- tiempo hasta el enfoque correcto;
- problemas análogos programados;
- más tarjetas, o cambios al espaciado;
- biblioteca de problemas propia;
- métricas de confusión de patrones;
- predicción de casos borde antes de someter, hipótesis de 60–90 s antes del bloque teórico, y la
  producción diagnóstica de cierre — **son intervenciones disponibles para usar cuando vengan al
  caso, no features a implementar**;
- behavioral.

### Decisiones que son del usuario, no mías

Tres cosas de este plan tocan restricciones que él declaró. No las cambio por mi cuenta:

1. **El gate de bitácora.** "Toda sesión cierra con bitácora o no cuenta" es una restricción suya.
   El problema: una sesión real con metadata incompleta se vuelve una sesión que no existe para la
   racha y los minutos, lo que sesga justamente la métrica de adherencia. Y peor —es la misma
   trampa que ya identificamos con los flags obligatorios— si la única salida honesta está
   bloqueada, el camino barato es escribir una bitácora de compromiso. Propuesta: inicio, fin y
   actividad cuentan siempre; la sesión puede quedar marcada `metadata-incompleta`; la bitácora
   cualitativa es opcional o se genera después.
2. **El arranque automático.** "La sesión arranca sin que el usuario pida nada" es una restricción
   suya, y es buena. Pero correr `estado` y desplegar el ritual de seis líneas ante un saludo o una
   consulta suelta es intrusivo. La restricción es que no tenga que acordarse de comandos, no que
   se le abra una sesión cada vez que escribe. Propuesta: el ritual cuando parece una sesión de
   estudio; una respuesta normal cuando no.
3. **Behavioral.** Sigue siendo un agujero: los loops de big tech lo puntúan. Corrección a lo que
   dije antes: **no es sólo contenido declarativo**. Repasar historias con SM-2 no practica
   selección de historia, comunicación oral ni follow-ups. Si se hace, una práctica mensual sirve
   más que tarjetas.

### Churn documental

Dejar de actualizar `perfil.md` y `temario.md` en todo cierre. Se tocan cuando aparece información
realmente nueva.

---

*Evidencia, citas verificadas, historial de versiones y respuesta a las revisiones externas:*
*`base/plan-de-fusion-apendice.md`.*
