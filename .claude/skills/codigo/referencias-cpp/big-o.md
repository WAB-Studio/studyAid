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
- **Un parámetro que viene en la entrada no es una constante.** `k`, `m`, `amount` y la
  longitud de las palabras entran en la fórmula. Solo se tira lo que no depende del input.

## Costos de operaciones en C++

| Operación | Tiempo |
|---|---|
| `v[i]`, `v.back()` | O(1) |
| `v.push_back(x)` / `v.pop_back()` | O(1) amortizado |
| `v.insert(v.begin(), x)` / `v.erase(v.begin())` | O(n) — desplaza todo |
| `sort(v.begin(), v.end())` | O(n log n) |
| `unordered_map` / `unordered_set`: `find`, `count`, `[]`, `insert` | O(1) promedio, O(n) peor caso |
| `map` / `set` (árbol rojo-negro): `find`, `insert` | **O(log n)**, no O(1) |
| `find(v.begin(), v.end(), x)` (búsqueda lineal) | O(n) |
| `binary_search`, `lower_bound` sobre un vector ordenado | O(log n) |
| `deque`: `push_front` / `push_back` / `pop_front` | O(1) |
| `priority_queue`: `push` / `pop` | O(log n); `top()` es O(1) |
| `s += c` sobre un `string` | O(1) amortizado |
| `s = s + t` en un bucle | O(n²) — construye un string nuevo cada vez |
| `v2 = v1` (copia de contenedor) | **O(n)** |
| Pasar un contenedor por valor a una función | **O(n)** — es una copia |

Las dos últimas filas son las que más sorprenden viniendo de un lenguaje con referencias.
Un `void f(vector<int> v)` copia el vector entero antes de ejecutar la primera línea.
Para leer sin copiar: `const vector<int>&`.

## Contar el espacio

- Separar espacio **auxiliar** (estructuras que allocás) del espacio de la **salida** y del
  de la **entrada**.
- **El stack de recursión cuenta como espacio.** Una recursión de profundidad n es O(n) aunque
  cada frame sea O(1). Un reverso "in-place" recursivo sigue siendo O(n) de espacio: la
  versión iterativa con dos punteros es la única genuinamente O(1).
- Una estructura auxiliar de tamaño k (heap de top-k, ventana fija) es O(k), sin importar n.
- **Los contenedores basados en nodos pesan mucho más que sus datos.** Un `unordered_set<int>`
  gasta del orden de 8 a 10 veces los bytes crudos: cada elemento es un nodo con un puntero al
  siguiente, más la cabecera del allocator, más el array de buckets. `vector<int>` es el único
  que se acerca a los 4 bytes por elemento.

## Análisis amortizado

- `push_back` es O(1) **amortizado**: casi todos son O(1), el resize ocasional copia los n
  elementos, pero promediado sobre la secuencia da constante. `reserve(n)` lo evita del todo.
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
para C++.
