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

## Costos de operaciones en TypeScript

| Operación | Tiempo |
|---|---|
| `a[i]`, `a.at(-1)` | O(1) |
| `a.push(x)` / `a.pop()` | O(1) amortizado |
| `a.unshift(x)` / `a.shift()` | **O(n)** — reindexa todo el array |
| `a.slice(i, j)` | O(j - i) — devuelve un array nuevo |
| `a.splice(i, k)` | O(n) — desplaza la cola |
| `a.concat(b)`, `[...a, ...b]` | O(n + m) |
| `a.sort(cmp)` | O(n log n) |
| `a.indexOf(x)`, `a.includes(x)` (búsqueda lineal) | O(n) |
| `Map` / `Set`: `get`, `set`, `has`, `delete` | O(1) promedio |
| Objeto plano `{}` como diccionario: `obj[k]` | O(1) promedio, pero ver la nota de abajo |
| `s += c` sobre un string | O(1) amortizado — V8 usa *ropes* |
| `s = s.slice(1)` en un bucle | O(n²) — construye un string nuevo cada vez |
| `arr.map` / `filter` / `reduce` | O(n), y **alocan un array nuevo** (`reduce` no) |

**`shift()` es la trampa número uno.** Es lo que casi todo el mundo usa para escribir una cola en
BFS, y convierte un O(V + E) en O(V²). La cola correcta es un array con un índice de cabeza que
solo avanza:

```ts
const q: number[] = [start];
let head = 0;
while (head < q.length) {
  const nodo = q[head++];   // O(1), sin reindexar
  // ...
}
```

**Objeto plano vs `Map`.** Un `{}` convierte toda clave a string (`obj[1]` y `obj["1"]` son la
misma), hereda claves de `Object.prototype` (`obj["toString"]` no es `undefined`) y no tiene
`.size`. Para un diccionario de verdad, `Map`: acepta cualquier tipo de clave, conserva el orden
de inserción y tiene `.size` en O(1).

## Contar el espacio

- Separar espacio **auxiliar** (estructuras que allocás) del espacio de la **salida** y del
  de la **entrada**.
- **El stack de recursión cuenta como espacio.** Una recursión de profundidad n es O(n) aunque
  cada frame sea O(1). Un reverso "in-place" recursivo sigue siendo O(n) de espacio: la
  versión iterativa con dos punteros es la única genuinamente O(1).
- Una estructura auxiliar de tamaño k (heap de top-k, ventana fija) es O(k), sin importar n.
- **`Map` y `Set` pesan mucho más que sus datos.** Cada entrada es un objeto con hash y punteros;
  el factor contra los bytes crudos es de un orden de magnitud. Si las claves son enteros en un
  rango chico y conocido, un array —o un `Int32Array`— es mucho más barato.
- **Los intermedios de `map`/`filter` cuentan.** Encadenar tres `filter` sobre n elementos aloca
  tres arrays. Es O(n) de espacio aunque la respuesta sea un número.

## Análisis amortizado

- `push` es O(1) **amortizado**: casi todos son O(1), el crecimiento ocasional del array copia los
  n elementos, pero promediado sobre la secuencia da constante. `new Array(n)` reserva de entrada.
- Union-find con compresión de caminos y unión por rango es O(α(n)) amortizado por operación.
  α es el inverso de Ackermann: menor o igual a 4 para cualquier n práctico, o sea O(1).

## Órdenes de magnitud útiles en entrevista

Un juez online hace del orden de 10^8 operaciones simples por segundo. La tabla usa ese número
porque es el que se cita en entrevista; **en JavaScript conviene contar más cerca de 10^7**, así
que en el límite de cada fila hay menos margen que en un lenguaje compilado. Sirve para elegir el
orden, no para apurar una constante.

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
para TypeScript el 2026-09-15, al revertir el cambio de lenguaje.
