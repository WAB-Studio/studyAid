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
- `arrays-strings` — recorridos, in-place, semántica de valor y contenedores de C++.
- `hash-maps` — Map y Set, cuándo convierten O(n²) en O(n).

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

## Calendario de lectura

Desde el 2026-10-06. La lectura semanal es la "clase"; el **domingo es la fecha meta**. La
sesión de fondo sobre lo leído se abre el día que termina el mínimo, no necesariamente el domingo.
Cada semana tiene un **mínimo** (lo que entra en la sesión) y una **meta** (si engancha, seguir).

Libros: *The Algorithm Design Manual*, Skiena, 3.ª ed. (base, en `fuentes/skiena-algorithm-design-manual/skiena-3ed.pdf`) y *Algorithms*, Jeff Erickson
(gratis, en `fuentes/erickson-algorithms/`) para recursión, backtracking, DP, greedy y grafos.
System design: *Designing Data-Intensive Applications*, Kleppmann (numeración de la 1.ª ed.).
Patrones del bloque 01 y videos: NeetCode, pasivo y opcional.

Sesión de fondo sobre lo leído: explica con sus palabras lo leído, yo completo lo flojo con
explicaciones propias, y sigue el ejercicio del temario. El libro marca el tema, no el guion.

| Fecha meta | Mínimo | Meta | Extra |
|---|---|---|---|
| [ ] 11 oct | Skiena 1 | Skiena 2 | NeetCode: Two Pointers |
| [ ] 18 oct | Skiena 2 | Skiena 3 | NeetCode: Sliding Window · DDIA 1 |
| [ ] 25 oct | Skiena 3 | Skiena 4 | NeetCode: Linked List, Stack |
| [ ] 1 nov | Skiena 4 | Skiena 5 | NeetCode: Heap · DDIA 2 |
| [ ] 8 nov | Skiena 5 | Skiena 6 | NeetCode: Binary Search, Trees |
| [ ] 15 nov | Erickson 1 | Erickson 2 | NeetCode: Intervals · DDIA 3 |
| [ ] 22 nov | Erickson 2 | Skiena 9 | NeetCode: Backtracking |
| [ ] 29 nov | Skiena 7 | Erickson 5–6 | NeetCode: Graphs · DDIA 5 |
| [ ] 6 dic | Erickson 3 | Skiena 10 | NeetCode: 1-D DP |
| [ ] 13 dic | Erickson 4 | Skiena 8 | NeetCode: Greedy · DDIA 6 |

Skiena es la 3.ª ed. (2020); la numeración es de esa edición. Se lee solo la parte I (caps
1–13, págs. 1–436). La parte II es un catálogo de consulta y no se asigna. Los caps 11–12
(NP-completitud) y 13 quedan fuera del calendario. Ejercicios del final de capítulo: no; los
ejercicios salen de LeetCode. Skiena 1–2 consolidan `complejidad`; 3 abre el bloque 02; 5 trae
búsqueda binaria; 6 repasa `hash-maps`.

## Cambios al plan

- 2026-09-09: versión inicial.
- 2026-09-09: la línea base A confirma el orden, no lo cambia. `complejidad` sigue primero y
  ahora con motivo medido: sin la notación no puede usar las restricciones del enunciado como
  señal de patrón, que es exactamente donde falló 4 de 6 veces en A1.
- 2026-09-09: dentro de `arrays-strings`, agregar un rato corto de API de arrays de JS
  (argumentos de `map`/`filter`/`reduce`, `const` vs `let`). En A2 dos de los tres errores
  fueron de lenguaje, no de algoritmo.
- 2026-09-09: `prefix-sum` gana prioridad dentro del bloque 01. 238 quedó abandonado y es el
  caso canónico de acumulados por izquierda y por derecha.
- 2026-09-10: `complejidad` abierto y cubierto. No se toca más como tema propio: los subtemas
  que quedaron (recursión, amortizado) se enseñan cuando aparezcan en `recursion` y en las
  estructuras que los necesiten. La lectura restricción → orden pasa a ser un paso fijo del
  protocolo de cada ejercicio, no un tema.
- 2026-09-10: 1 Two Sum queda gastado como vehículo de `complejidad`. Al abrir `hash-maps`,
  arrancar por 49 Group Anagrams.
- 2026-09-10: **cambio de lenguaje a C++**, decidido por él a mitad de la segunda sesión del día.
  El orden de los bloques no cambia; el temario es de patrones, no de sintaxis. Dos consecuencias
  concretas: (a) `heaps` se abarata, porque `priority_queue` viene en la stdlib y ya no hay que
  escribir el heap a mano como habría hecho falta en JS; (b) `linked-lists` y `trees-bst` se
  vuelven más valiosos de lo que eran, porque ahí los punteros dejan de ser teoría. Mientras dure
  la rampa rige la regla de la carga cognitiva del AGENTS.md: tema nuevo y lenguaje nuevo no se
  estrenan en el mismo ejercicio.
- 2026-09-10: **el scheduler de tarjetas no se toca hasta el 2026-10-10**, por decisión suya.
  Hoy hay 16 tarjetas y cero repasos registrados: cualquier cambio sería contra una intuición.
  Qué revisar ese día, con un mes de datos: si el primer vencimiento conviene repartirse en 1-3
  días en vez de caer todo junto al día siguiente, y cuál es la tasa real de lapsos (calidad
  menor a 3), que es lo que apila la cola. La cantidad generada por tema (6 a 8) no está en
  discusión: cubre señal, complejidad, error típico y caso borde.
- 2026-09-14: el texto de `arrays-strings` decía "qué es inmutable en JS", herencia del lenguaje
  anterior. Corregido a semántica de valor y contenedores de C++, que es lo que efectivamente se
  trabajó. El orden de los bloques no cambia. `arrays-strings` queda a un ejercicio de cerrarse:
  falta solo rangos medio abiertos, y 680 Valid Palindrome II lo cubre.
- 2026-09-17: **`arrays-strings` cerrado** con 680. El orden no cambia: sigue `hash-maps`, y
  arranca por 49 Group Anagrams como quedó decidido el 09-10. El subtema `strings mutables`
  (`s[i] = c` sobre `string`) nunca se tocó y **no se le busca ejercicio propio**: es un hecho de
  una línea y se cubre cuando aparezca, igual que se hizo con los restos de `complejidad`.
  El bloque teórico de `hash-maps` tiene que atacar de frente `m[k]` que inserta al leer: falló
  dos veces (`c0010`, calidad 1 el 09-14) y es una creencia invertida, no un olvido.

- 2026-09-20: **`hash-maps` abierto** con 49 Group Anagrams, Accepted. El tema no se cierra
  todavía: falta un problema donde la clave **no** sea una transformación de la entrada. 49 se
  resuelve codificando cada palabra, que es el caso fácil de elegir clave; 128 Longest
  Consecutive Sequence obliga a usar el conjunto para preguntar por vecinos, que es donde el
  patrón se rompe si la clave se eligió por costumbre. Ese es el ejercicio de cierre.
- 2026-09-20: el modelo mental de un tema se escribe **al nivel del mecanismo**, no del uso.
  Lo pidió él con argumento y funcionó: con la tabla hash explicada por dentro contestó sin ayuda
  un control que no era repetición. Vale para los temas que vienen, empezando por `heaps`, donde
  la tentación de enseñar solo la API de `priority_queue` es la misma.
- 2026-10-06: **cambio de formato.** 16 días sin estudiar: las sesiones diarias frente al
  computador exigían esfuerzo máximo para todo. Ahora el input es pasivo (libro y videos, a su
  ritmo, con el calendario de arriba) y el esfuerzo va a la sesión de fondo, que se abre al
  terminar el mínimo de la semana. Libros densos por preferencia suya: Skiena 3.ª ed. y
  Erickson; DDIA para system design. Base: metas cercanas (Bandura y Schunk, 1981), plazos
  externos y parejos (Ariely y Wertenbroch, 2002), metas en rango mínimo–meta (Scott y Nowlis,
  2013) y recuperación después de leer (Roediger y Karpicke, 2006). El orden de bloques sigue
  siendo el mapa; el calendario manda en el ritmo.
