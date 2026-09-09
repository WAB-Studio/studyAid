# Complejidad

Referencia factual. Los números tienen que estar bien.

## Leer la complejidad del código

- Sentencias secuenciales se suman: O(a) + O(b) → domina la mayor.
- Bucles anidados sobre el mismo n se multiplican: dos anidados O(n²), tres O(n³).
- Partir el espacio de búsqueda a la mitad en cada paso → O(log n). Hacerlo dentro de un
  bucle sobre n → O(n log n).
- Recursión: tiempo ≈ (nodos del árbol de llamadas) × (trabajo por nodo). Factor de
  ramificación 2 y profundidad n → O(2^n). Divide y vencerás que parte a la mitad y hace
  trabajo lineal al mergear (`T(n) = 2T(n/2) + O(n)`) → O(n log n).

## Costos de operaciones en JavaScript

| Operación | Tiempo |
|---|---|
| `arr.sort(cmp)` (Timsort en V8) | O(n log n) |
| `map.get` / `map.set` / `set.has` | O(1) promedio, O(n) peor caso |
| `arr.includes` / `arr.indexOf` | O(n) |
| `arr.push` / `arr.pop` | O(1) amortizado |
| `arr.shift` / `arr.unshift` / `arr.splice(0,1)` | O(n) — desplaza todo |
| `arr[i]` | O(1) |
| `arr.slice(a, b)` | O(b - a) — copia |
| `str + str` en un bucle | O(n²) si se rearma; juntar en array y `join("")` |
| Push/pop en un heap propio | O(log n) |
| Búsqueda binaria | O(log n) |
| `Object.keys(o)` | O(n) |

## Contar el espacio

- Separar espacio **auxiliar** (estructuras que allocás) del espacio de la **salida** y del
  de la **entrada**.
- **El stack de recursión cuenta como espacio.** Una recursión de profundidad n es O(n) aunque
  cada frame sea O(1). Un reverso "in-place" recursivo sigue siendo O(n) de espacio: la
  versión iterativa con dos punteros es la única genuinamente O(1).
- Una estructura auxiliar de tamaño k (heap de top-k, ventana fija) es O(k), sin importar n.

## Análisis amortizado

- `arr.push` es O(1) **amortizado**: casi todos los push son O(1), el resize ocasional copia
  los n elementos, pero promediado sobre la secuencia da constante.
- Union-find con compresión de caminos y unión por rango es O(α(n)) amortizado por operación.
  α es el inverso de Ackermann: menor o igual a 4 para cualquier n práctico, o sea O(1).

## Órdenes de magnitud útiles en entrevista

Un juez online hace del orden de 10^8 operaciones simples por segundo. De ahí sale qué
complejidad tolera cada tamaño de entrada:

| n hasta | Complejidad que entra |
|---|---|
| 10 | O(n!) |
| 20–25 | O(2^n) |
| 500 | O(n³) |
| 5.000 | O(n²) |
| 10^6 | O(n log n) |
| 10^8 | O(n) |

Si el enunciado dice `n <= 10^5`, la restricción te está diciendo que la respuesta es
O(n log n) o mejor. Leerla es parte de la fase Match.

---

Adaptado de `kirilxd/swe-interview-coach` (MIT). Los costos de operaciones fueron reescritos
para JavaScript.
