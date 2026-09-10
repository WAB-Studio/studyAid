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
- `arrays-strings` — recorridos, in-place, qué es inmutable en JS.
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
