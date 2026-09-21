# Temario

Mapa de bloques. La profundidad de cada tema no está acá: se escribe en
`base/temas/<tema>.md` el día que se abre el tema, y crece con el uso.

Quién lo actualiza: yo (Claude), al cerrar sesiones. Si un bloque queda frío o el orden
deja de tener sentido para lo que está pasando, lo reordeno y lo anoto abajo.

El estado real de cada tema no se declara acá: sale de `study.py estado`, que muestra
qué temas tienen actividad y hace cuánto. Este archivo dice qué falta tocar.

## Orden

Bloques 00 a 04 en orden. El 05 corre en paralelo desde el bloque 02, un tema cada dos semanas.

Un tema está cubierto cuando se cumplen las dos cosas: lo explicó con sus palabras y
resolvió al menos un ejercicio del tema. Leer no alcanza.

## 00 Fundamentos

- `complejidad` — Big-O de tiempo y espacio sin mirar la tabla.
- `arrays-strings` — recorridos, in-place, qué es inmutable en JS, copia vs referencia.
- `hash-maps` — `Map` y `Set`, cuándo convierten O(n²) en O(n).

## 01 Patrones core

Es el bloque que más mueve la aguja en reconocimiento de patrón, la debilidad principal.

- `two-pointers` — extremos opuestos, mismo sentido, rápido/lento.
- `sliding-window` — ventana fija y variable.
- `prefix-sum` — sumas acumuladas y conteo con hash map.
- `binary-search` — sobre índices y sobre el espacio de respuestas.
- `intervalos` — ordenar como paso previo, solapamientos, merge.

## 02 Estructuras

Acá arranca system design en paralelo.

- `linked-lists` — reverso, ciclo, nodo dummy.
- `stacks-queues` — incluida la pila monótona.
- `heaps` — top-k y merge de k listas.
- `trees-bst` — recorridos, propiedades de BST, LCA.
- `tries` — prefijos.

## 03 Recursión y grafos

- `recursion` — caso base, confianza recursiva, pila de llamadas.
- `backtracking` — permutaciones, combinaciones, poda.
- `graphs-bfs-dfs` — representación, camino mínimo, componentes.
- `topological-sort` — orden y detección de ciclos.
- `union-find` — con compresión de caminos.

## 04 Programación dinámica

El bloque más duro. No adelantarlo aunque tiente.

- `dp-1d` — escaleras, robo de casas, coin change.
- `dp-2d` — grillas, subsecuencias, edit distance.
- `greedy` — y cuándo no alcanza, frente a DP.

## 05 System design

Dosis chicas y sostenidas, nunca un bloque al final.

- `sd-fundamentos` — latencia, throughput, consistencia, CAP.
- `sd-almacenamiento` — SQL vs NoSQL, índices, sharding, replicación.
- `sd-cache` — niveles, invalidación, políticas de desalojo.
- `sd-apis` — diseño, rate limiting, idempotencia.
- `sd-async` — colas, workers, backpressure.
- `sd-casos` — acortador de URLs, feed, chat, notificaciones.

## Cambios al plan

- 2026-09-09: versión inicial.
- 2026-09-11: **se purgó el historial anterior de esta sección.** Citaba mediciones de una
  "línea base A" (A1, A2, problemas abandonados, conteos de fallos) que no tienen ningún archivo
  detrás: `base/linea-base.md` no existe y la única sesión registrada era de `hash-maps`. Eran
  conclusiones sin datos. Lo que sobrevive abajo es lo que sí tiene respaldo: decisiones que él
  tomó explícitamente en conversación.
- 2026-09-10: **cambio de lenguaje a C++**, decidido por él. ~~Revertido el 2026-09-15~~ — ver
  la entrada de ese día. Se deja anotado porque explica por qué varios archivos del repo hablan
  de C++.
- 2026-09-10: **el scheduler de tarjetas no se toca hasta el 2026-10-10**, por decisión suya.
  No hay tarjetas ni repasos todavía, así que cualquier cambio sería contra una intuición. Qué
  revisar ese día, con un mes de datos: si el primer vencimiento conviene repartirse en 1-3 días
  en vez de caer todo junto al día siguiente, y cuál es la tasa real de lapsos (calidad menor a
  3), que es lo que apila la cola. La cantidad generada por tema (4 a 8) no está en discusión:
  cubre señal, complejidad, error típico y caso borde.
- 2026-09-11: nada del bloque 00 está cubierto. `complejidad` vuelve a ser el primer tema a
  abrir, después de la línea base.
- 2026-09-11: **A1 de la línea base ejecutado.** 2 de 6 enfoques válidos y 0 de 6 patrones
  nombrados. El orden de bloques no cambia: el 01 ya estaba justificado como el que más mueve la
  aguja en reconocimiento, y A1 lo respalda. Lo que sí queda anotado para decidir después de A2:
  si conviene nombrar la familia del patrón explícitamente en cada ejercicio, porque en los dos
  aciertos describió la mecánica correcta sin tener la etiqueta.
- 2026-09-15: **vuelta a TypeScript**, revirtiendo el cambio del 2026-09-10. Decidido sobre
  evidencia de A2: escribió el ejercicio en TypeScript porque no sabe C++, y aun así reportó
  errores de sintaxis —iteraciones, declaraciones, signos de comparación— en un lenguaje que usa
  hace 4 años. La regla de carga cognitiva del `AGENTS.md` asumía que había algo de C++ que
  dosificar; partiendo de cero no es una rampa sino dos currículos en paralelo, contra un
  presupuesto de tiempo que ya es el recurso escaso. Justificación: carga cognitiva (Sweller), la
  sintaxis desconocida es carga extrínseca y compite con la adquisición del esquema. Costo de
  mercado bajo: Google, Meta y Amazon aceptan TypeScript; C++ sólo es obligatorio en nichos.
  **El orden de los bloques no cambia** — el temario es de patrones, no de sintaxis. Consecuencias:
  (a) `heaps` se encarece, porque en TS no hay `priority_queue` en la stdlib y hay que escribir el
  heap o traer librería; (b) `linked-lists` y `trees-bst` pierden el beneficio de que los punteros
  dejen de ser teoría. C++ queda como pista aparte, a retomar cuando los patrones estén firmes.
- 2026-09-15: **forma A de la línea base cerrada.** A2 resuelto solo pero sólo la ingenua, sin
  percibir que existiera algo mejor; A3 no salió. El orden de bloques sigue sin cambiar. Se cierra
  el pendiente que A1 había dejado abierto —si conviene nombrar la familia del patrón explícito—
  con un **sí parcial**: A1+A2 juntos muestran dos huecos, no uno. Nombrar la familia ataca el
  de vocabulario; el de repertorio de técnicas sólo lo cierra cubrir los temas. Hacer lo primero
  y no confundirlo con lo segundo.
- 2026-09-15: **referencias portadas.** `referencias-cpp/` pasó a `referencias-ts/`: `big-o.md` con
  los costos de las operaciones de JS, `patrones.md` con los catorce templates en TypeScript y una
  sección de trampas propias de JS/TS que reemplaza a la de C++. `problemas.md` no cambió, es
  agnóstico del lenguaje. El 11 quedó marcado ahí como gastado por A2.
- 2026-09-15: **`study.py` aprendió a corregir.** `sesion eventos` numera lo registrado y
  `sesion corregir` cambia un campo guardando el valor anterior con su motivo, también en sesiones
  ya cerradas. Sale del error del 2026-09-11, que se había arreglado editando `data/` a mano. La
  calidad de un repaso queda fuera a propósito: el scheduler ya avanzó a partir de ella y
  deshacerlo no es confiable.
- 2026-09-16: **`complejidad` abierto y cubierto según el criterio de este archivo** —lo explicó
  con palabras propias y resolvió 217— **pero con cinco subtemas pendientes** anotados en
  `base/temas/complejidad.md`: `log n`, los costos de las operaciones de TypeScript, complejidad de
  recursión, amortizado, y que un parámetro de la entrada no es constante. El orden de bloques no
  cambia y `arrays-strings` sigue siendo lo próximo del bloque 00. Queda anotado que el criterio
  de cobertura ("lo explicó y resolvió un ejercicio") no distingue un tema agotado de uno abierto
  con pendientes; no se toca el criterio hoy, pero si el patrón se repite en el próximo tema hay
  que revisarlo contra la skill `teoria-del-aprendizaje` y no por intuición.
- 2026-09-16: 217 Contains Duplicate quedó **usado como vehículo de `complejidad`**, no como
  apertura de `arrays-strings`. Cuando se abra ese tema, el ejemplo resuelto va sobre otro:
  quedan 242, 27 y 238.
- 2026-09-19: `arrays-strings` abierto. 242 gastado como ejemplo resuelto y 27 como ejercicio;
  queda 238 Product of Array Except Self, que además es el subtema de dos pasadas sin tocar.
- 2026-09-20: **bloque 00 cerrado.** `complejidad`, `arrays-strings` y `hash-maps` cumplen las dos
  condiciones: explicados con sus palabras y con al menos un ejercicio resuelto. De `hash-maps`
  quedan 49 Group Anagrams (grouping by key) y 128, sin abrir; 1 Two Sum gastado como ejercicio y
  242 como ejemplo resuelto. El orden no cambia: sigue el bloque 01 por `two-pointers`.
- 2026-09-20: **`two-pointers` aparece en `PY estado` con actividad del 2026-09-15 y no está
  abierto.** Esa fecha es 11 Container With Most Water de la línea base A2, medido en frío. El
  archivo `base/temas/two-pointers.md` dice "No abierto" en la primera línea y manda él. La fondo
  que lo abra necesita un ejemplo resuelto que no sea ni 11 (gastado) ni 15 3Sum (reservado para la
  línea base B): quedan 125 Valid Palindrome y 167 Two Sum II. **167 conviene**, porque es
  literalmente Two Sum con el arreglo ordenado, y la comparación contra lo que acaba de resolver
  hoy hace visible el eje entero: el hash map compra tiempo con memoria O(n), los dos punteros
  compran lo mismo con O(1) a cambio de exigir orden.
- 2026-09-20: **`two-pointers` abierto**, con 167 como ejemplo resuelto y **11 Container With Most
  Water como ejercicio** — el mismo que dio TLE en A2 el 2026-09-15, ahora Accepted. La restricción
  de "11 está gastado" del archivo del tema queda **cumplida y cerrada**: volvió como ejercicio,
  que era exactamente lo previsto. Quedan sin usar 125 Valid Palindrome y 42; 15 sigue reservado
  para la línea base B.
- 2026-09-20: **el lenguaje se vuelve a confirmar en TypeScript, esta vez a pedido suyo.** Preguntó
  si convenía moverse a algo de más bajo nivel. Evidencia contra el cambio: TS se acepta en las
  entrevistas de código de big tech, su objetivo son empresas de su stack, y el argumento de carga
  cognitiva del 2026-09-15 sigue valiendo — hoy mismo el bloqueo fue conceptual (el invariante del
  contenedor) y habría competido con la sintaxis. **La única contra honesta, que se le dijo:**
  TypeScript no trae heap ni priority queue en la librería estándar, así que en `heaps` (bloque 02)
  va a tener que escribirlo a mano. **Criterio para reabrirlo:** cuando llegue a ese tema y la
  fricción sea real. Antes no, y su propia propuesta —aprender el lenguaje aparte, no dentro de
  LeetCode— es la correcta.
- 2026-09-20: **`tools/study.py` acepta corregir `afk_declarado` en una sesión cerrada**, con
  recálculo de `minutos_efectivos`. Motivo: el AFK casi siempre se sabe tarde —el que se fue es él
  y solo lo puede contar al volver, a veces después del cierre— y hasta ahora `--afk` existía solo
  en `sesion cerrar`. Dos incidentes en dos días: el 19 la sesión corrió toda la noche, el 20
  avisó 30 min de AFK después de cerrar. Justificación: es la misma excepción ya sancionada de
  `externo agregar` —ningún reloj cubrió el hueco, el número lo pone él— y no colisiona con el veto
  sobre `calidad`, porque ahí SM-2 ya consumió el valor y acá `minutos_efectivos` es un recálculo
  puro. **Contra, anotada en el código y en `AGENTS.md`:** la medición concurrente es más exacta
  que la retrospectiva, así que `pausar`/`reanudar` siguen siendo el camino y esto es la red.
- 2026-09-20: **c0007 y c0016 retiradas y reemplazadas** (→ c0030, c0031, c0032), a decisión suya
  delegada y justificado con `teoria-del-aprendizaje`. Dos criterios que valen para toda tarjeta
  futura: **(1)** una tarjeta, un hecho — si mezcla dos, la calidad que se le pone no describe
  ninguno y el `ease` se calcula sobre un número falso; **(2)** el frente tiene que pedir lo que se
  quiere retener, porque solo se retiene lo que se recupera. Un frente que pide el número entrena
  el número, y en este caso estaba reforzando un patrón ya documentado en el perfil. **Hueco de la
  herramienta:** no hay `tarjetas editar`, así que arreglar la redacción de una tarjeta cuesta su
  historial SM-2. Candidato a revisar el 2026-10-10 junto con el scheduler.
- 2026-09-20: **`tools/study.py` tiene `tarjetas editar`**, que corrige frente, dorso o tema
  conservando el historial SM-2, exige `--motivo` y guarda el texto anterior en `ediciones`.
  Justificación: el `ease` es específico del ítem, así que si la tarjeta sigue pidiendo lo mismo
  esos números siguen valiendo y tirarlos pierde datos caros; hoy c0016 y c0007 costaron 4 repasos
  entre las dos. **El límite, escrito en el docstring y en `AGENTS.md`:** editar es para la
  redacción. Si el frente pasa a exigir otra recuperación es otro ítem y corresponde retirar más
  una nueva. La tool no puede juzgar semántica, así que no lo intenta — deja la decisión visible y
  auditable e imprime la advertencia en cada uso. No toca el scheduler, así que el freno del
  2026-10-10 no aplica.
- 2026-09-20: **traídas tres cosas de `origin/main`**, que es una línea paralela del proyecto (sigue
  en C++, con bitácoras y tarjetas propias e incompatibles con estas). Se copiaron **a mano, nunca
  con merge**: `main` versiona `data/`, que acá está en `.gitignore`, así que un merge sobrescribe
  las tarjetas vivas. Lo traído: (1) la skill `tarjetas`, con su regla central "la tarjeta no asume
  nada que no diga" y la prueba de leer el frente solo, sin dorso y sin tema — **adaptada**: el
  original prohibía el tuteo y acá el registro es tuteo, español neutro de Colombia, por pedido
  suyo; (2) el protocolo de confianza posterior a la respuesta; (3) `.claude/settings.json`.
- 2026-09-20: **la confianza en tarjetas se pide después de contestar.** Justificado con
  `teoria-del-aprendizaje`: un juicio previo hecho sobre la etiqueta del tema mide familiaridad con
  el indicio, no recuperación, y el dato propio lo confirma — 14 de 14 "sí" en un día. Un juicio
  retrospectivo se calibra mejor porque usa la experiencia real de recuperar, y pregunta lo que
  importa en entrevista: si sabe cuándo está equivocado. **Corte de serie el 2026-09-21**, anotado
  en la skill `metricas`: las predicciones de tarjeta anteriores no se mezclan con las posteriores.
  La predicción de ejercicio no cambió — se hace sobre el enunciado real y su serie sigue entera.
