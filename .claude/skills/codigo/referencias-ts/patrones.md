# Taxonomía de patrones

Un bloque por patrón: señal de reconocimiento, template en TypeScript, complejidad,
problemas clásicos de LeetCode, errores típicos.

Los templates son para el bloque teórico de una sesión de fondo. Nunca se muestran mientras
el usuario está resolviendo un ejercicio.

Se asume el preámbulo que LeetCode ya provee: la firma de la función con sus tipos.

---

## two-pointers

**Señal**: array ordenado, "par/triple que suma a X", deduplicar in-place, palíndromo,
contenedor/agua atrapada.
**Usar cuando**: la entrada está ordenada, o la factibilidad del par cambia de forma monótona
al mover los punteros.

```ts
function twoSumSorted(a: number[], target: number): number[] {
  let lo = 0, hi = a.length - 1;
  while (lo < hi) {
    const s = a[lo] + a[hi];
    if (s === target) return [lo, hi];
    if (s < target) lo++;
    else hi--;
  }
  return [];
}
```

**Complejidad**: O(n) tiempo, O(1) espacio.
**Clásicos**: 167 Two Sum II, 15 3Sum, 11 Container With Most Water, 125 Valid Palindrome,
42 Trapping Rain Water.
**Errores típicos**: aplicarlo sobre datos sin ordenar; si hay que ordenar primero, el
O(n log n) domina. Off-by-one en `lo < hi`. Olvidar saltear duplicados en 3Sum.
Escribir el doble bucle O(n²) sin notar que el array ordenado habilita el barrido en O(n).

## sliding-window

**Señal**: "subarray/substring **contiguo**", "el más largo/corto que cumple", "a lo sumo k
distintos", "suma máxima de tamaño k".
**Usar cuando**: la respuesta es un rango contiguo Y la validez es monótona: crecer solo puede
romperla, encoger solo puede arreglarla.

```ts
function longestNoRepeat(s: string): number {
  const ultimo = new Map<string, number>();   // char -> ultimo indice visto
  let left = 0, best = 0;
  for (let right = 0; right < s.length; right++) {
    const prev = ultimo.get(s[right]);
    if (prev !== undefined && prev >= left) {
      left = prev + 1;                        // guarda contra un indice viejo
    }
    ultimo.set(s[right], right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
```

**Complejidad**: O(n) tiempo, O(k) espacio.
**Clásicos**: 3 Longest Substring Without Repeating, 424 Longest Repeating Character
Replacement, 567 Permutation in String, 76 Minimum Window Substring, 121 Best Time to Buy and Sell.
**Errores típicos**: mover `left` hacia atrás por un índice viejo (falta la guarda `>= left`);
confundir ventana fija con variable; escribir `if (prev)` en vez de `if (prev !== undefined)`,
que trata el índice `0` como ausente.

## fast-slow-pointers

**Señal**: detectar ciclo, nodo del medio, k-ésimo desde el final.

```ts
function hasCycle(head: ListNode | null): boolean {
  let slow = head, fast = head;
  while (fast && fast.next) {          // guarda ANTES de fast.next.next
    slow = slow!.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}
```

**Complejidad**: O(n) tiempo, O(1) espacio.
**Clásicos**: 141 Linked List Cycle, 142 Cycle II, 876 Middle of the Linked List, 202 Happy Number.
**Errores típicos**: leer `fast.next.next` sin la guarda: `TypeError: Cannot read properties of
null`, que al menos dice dónde; off-by-one sobre cuál puntero es la respuesta en "el del medio".

## hashing / frequency-map

**Señal**: "¿ya lo vi?", contar ocurrencias, agrupar por clave.

```ts
function groupAnagrams(words: string[]): string[][] {
  const grupos = new Map<string, string[]>();
  for (const w of words) {
    const key = [...w].sort().join('');       // split, sort, join: no hay sort de string
    const lista = grupos.get(key);
    if (lista) lista.push(w);
    else grupos.set(key, [w]);
  }
  return [...grupos.values()];
}
```

**Complejidad**: O(n·k log k) acá por el sort de cada palabra; lookups O(1) promedio.
**Clásicos**: 1 Two Sum, 49 Group Anagrams, 242 Valid Anagram, 217 Contains Duplicate,
347 Top K Frequent, 128 Longest Consecutive Sequence.
**Errores típicos**: usar `{}` en vez de `Map` y chocar con `Object.prototype` o con la conversión
de claves a string; `w.sort()` sobre un string, que no existe: hay que pasar por array;
contar con `m[k]++` sobre un objeto donde la clave todavía no está, que da `NaN`.

## prefix-sum

**Señal**: consultas repetidas de suma de rango, "subarray que suma k".

```ts
function subarraySum(nums: number[], k: number): number {
  const vistos = new Map<number, number>();
  vistos.set(0, 1);                    // semilla: subarrays que arrancan en el indice 0
  let run = 0, count = 0;
  for (const x of nums) {
    run += x;
    count += vistos.get(run - k) ?? 0;
    vistos.set(run, (vistos.get(run) ?? 0) + 1);
  }
  return count;
}
```

**Complejidad**: O(n) tiempo, O(n) espacio.
**Clásicos**: 560 Subarray Sum Equals K, 303 Range Sum Query, 724 Find Pivot Index,
238 Product of Array Except Self.
**Errores típicos**: olvidar la semilla `vistos.set(0, 1)` (se pierden los subarrays que arrancan
en 0); off-by-one entre prefijo inclusivo y exclusivo; usar `||` en vez de `??` y tratar el
conteo `0` como ausente.

## binary-search

**Señal**: "ordenado", "primera/última posición", "minimizar el máximo", array rotado,
o un predicado monótono ("¿alcanza con capacidad x?").
**Incluye buscar sobre la respuesta**: si se puede chequear barato "¿x es factible?" y la
factibilidad es monótona en x, binaria sobre el rango de respuestas.

```ts
function lowerBound(a: number[], target: number): number {  // primer indice con a[i] >= target
  let lo = 0, hi = a.length;                                // intervalo [lo, hi)
  while (lo < hi) {
    const mid = (lo + hi) >> 1;                             // piso, sin Math.floor
    if (a[mid] < target) lo = mid + 1;
    else hi = mid;
  }
  return lo;
}
```

En TypeScript no hay `lower_bound` en la librería estándar: este template se escribe a mano y
conviene tenerlo memorizado.

**Complejidad**: O(log n) por búsqueda, por el costo del predicado.
**Clásicos**: 704 Binary Search, 33 Search in Rotated Sorted Array, 153 Find Minimum in Rotated,
875 Koko Eating Bananas, 74 Search a 2D Matrix.
**Errores típicos**: mezclar convenciones `[lo, hi]` y `[lo, hi)` y colgarse en bucle infinito;
`(lo + hi) / 2` sin `Math.floor`: en JS la división da decimales y `a[2.5]` es `undefined`;
quedarse con la mitad equivocada en el rotado; devolver `mid` en vez de `lo`.
Ojo con `>>` si los valores pueden pasar 2³¹: ahí va `Math.floor((lo + hi) / 2)`.

## intervalos

**Señal**: rangos que se solapan: mergear, insertar, contar eventos concurrentes.

```ts
function merge(intervals: number[][]): number[][] {
  intervals.sort((x, y) => x[0] - y[0]);      // comparador NUMERICO, obligatorio
  const out: number[][] = [];
  for (const iv of intervals) {
    const last = out[out.length - 1];
    if (last && iv[0] <= last[1]) {
      last[1] = Math.max(last[1], iv[1]);
    } else {
      out.push(iv);
    }
  }
  return out;
}
```

**Complejidad**: O(n log n) por el sort, O(n) el barrido.
**Clásicos**: 56 Merge Intervals, 57 Insert Interval, 435 Non-overlapping Intervals.
**Errores típicos**: **`sort()` sin comparador ordena como string**: `[10, 9, 100]` queda
`[10, 100, 9]`. Es el error más frecuente del patrón. Ordenar por fin cuando iba por inicio;
el test de solapamiento `<` vs `<=` decide si los que se tocan se mergean; olvidar la guarda
`last &&` y leer `last[1]` de `undefined`.

## linked-list

**Señal**: splice, reverso, merge de nodos. Usar nodo dummy para que el primero no sea caso especial.

```ts
function reverseList(head: ListNode | null): ListNode | null {
  let prev: ListNode | null = null;
  let cur = head;
  while (cur) {
    const next = cur.next;   // guardar ANTES de reescribir
    cur.next = prev;
    prev = cur;
    cur = next;
  }
  return prev;
}
```

**Complejidad**: O(n) tiempo, O(1) espacio en la versión iterativa.
**Clásicos**: 206 Reverse Linked List, 21 Merge Two Sorted Lists, 19 Remove Nth From End,
143 Reorder List, 146 LRU Cache.
**Errores típicos**: perder el resto de la lista por reasignar `next` antes de guardarlo;
devolver `dummy` en vez de `dummy.next`; la versión recursiva NO es O(1) espacio;
pelearse con `strictNullChecks` y tapar el problema con `!` en vez de con la guarda correcta.

## stack y monotonic-stack

**Señal**: emparejar o anidar (paréntesis, undo) → pila común. "Próximo mayor/menor",
acotar un histograma → pila monótona.

```ts
function dailyTemperatures(t: number[]): number[] {
  const n = t.length;
  const res = new Array<number>(n).fill(0);
  const st: number[] = [];                       // indices, temperaturas decrecientes
  for (let i = 0; i < n; i++) {
    while (st.length && t[st[st.length - 1]] < t[i]) {
      const j = st.pop()!;
      res[j] = i - j;
    }
    st.push(i);
  }
  return res;
}
```

En TypeScript la pila es un array con `push`/`pop`, que son O(1) amortizado. Sí devuelven el
elemento, al revés que en otros lenguajes.

**Complejidad**: O(n) tiempo (cada índice entra y sale una vez), O(n) espacio.
**Clásicos**: 20 Valid Parentheses, 155 Min Stack, 150 Evaluate RPN, 739 Daily Temperatures,
84 Largest Rectangle in Histogram.
**Errores típicos**: apilar valores cuando se necesitaban índices; olvidar `st.length` en la
guarda y comparar contra `undefined`; comparación estricta o no estricta que admite iguales
cuando no debe.

## bfs

**Señal**: camino más corto en grafo o grilla **sin pesos**, recorrido por niveles.

```ts
function bfsGrid(grid: number[][], start: [number, number]): number {
  const R = grid.length, C = grid[0].length;
  const visto = Array.from({ length: R }, () => new Array<boolean>(C).fill(false));
  const q: [number, number][] = [start];
  let head = 0;                                  // cola con indice: shift() seria O(n)
  visto[start[0]][start[1]] = true;

  let dist = 0;
  const dr = [1, -1, 0, 0], dc = [0, 0, 1, -1];
  while (head < q.length) {
    const nivel = q.length - head;               // fijar el tamaño ANTES del bucle
    for (let i = 0; i < nivel; i++) {
      const [r, c] = q[head++];
      for (let d = 0; d < 4; d++) {
        const nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
        if (visto[nr][nc] || grid[nr][nc] === 0) continue;
        visto[nr][nc] = true;                    // marcar al ENCOLAR, no al desencolar
        q.push([nr, nc]);
      }
    }
    dist++;
  }
  return dist;
}
```

**Complejidad**: O(V + E) tiempo, O(V) espacio.
**Clásicos**: 200 Number of Islands, 994 Rotting Oranges, 127 Word Ladder, 102 Level Order Traversal.
**Errores típicos**: **usar `q.shift()` como cola**: es O(n) porque reindexa el array, y convierte
el BFS en O(V²); marcar visitado al desencolar (el mismo nodo entra muchas veces); leer `q.length`
dentro del `for` mientras la cola crece; crear la matriz de vistos con
`new Array(R).fill(new Array(C).fill(false))`, que comparte **la misma fila** R veces.

## dfs

**Señal**: componentes conexas, caminos en un árbol, alcanzabilidad. El camino más corto no importa.

```ts
function numIslands(grid: string[][]): number {
  const R = grid.length, C = grid[0].length;
  let count = 0;

  function dfs(r: number, c: number): void {
    if (r < 0 || r >= R || c < 0 || c >= C || grid[r][c] !== '1') return;
    grid[r][c] = '0';                            // marcar in-place
    dfs(r + 1, c); dfs(r - 1, c);
    dfs(r, c + 1); dfs(r, c - 1);
  }

  for (let r = 0; r < R; r++)
    for (let c = 0; c < C; c++)
      if (grid[r][c] === '1') { dfs(r, c); count++; }

  return count;
}
```

**Complejidad**: O(V + E) tiempo, O(V) espacio de stack.
**Clásicos**: 200 Number of Islands, 133 Clone Graph, 695 Max Area of Island, 417 Pacific Atlantic.
**Errores típicos**: no marcar visitado → recursión infinita con ciclos; el stack de recursión
cuenta como espacio, y en Node se agota alrededor de 10⁴ frames: bastante antes que en un
lenguaje compilado, así que una grilla grande puede necesitar BFS iterativo.

## backtracking

**Señal**: enumerar todas las combinaciones, permutaciones, subconjuntos, o llenar un tablero.
Elegir, recursar, **deshacer**.

```ts
function subsets(nums: number[]): number[][] {
  const res: number[][] = [];
  const path: number[] = [];

  function bt(start: number): void {
    res.push([...path]);                    // COPIA: push(path) guardaria la referencia
    for (let i = start; i < nums.length; i++) {
      path.push(nums[i]);                   // elegir
      bt(i + 1);
      path.pop();                           // deshacer
    }
  }

  bt(0);
  return res;
}
```

**Complejidad**: exponencial: O(2^n) subconjuntos, O(n!) permutaciones, por O(n) de copiar.
**Clásicos**: 78 Subsets, 46 Permutations, 39 Combination Sum, 79 Word Search, 51 N-Queens.
**Errores típicos**: **`res.push(path)` sin copiar**: se guarda la referencia al mismo array, que
se sigue mutando, y al final todos los resultados son iguales (casi siempre vacíos). Hay que
escribir `[...path]` o `path.slice()`. Olvidar el `path.pop()`; no podar y explorar ramas
imposibles.

## dynamic-programming

**Señal**: subproblemas que se repiten y subestructura óptima: "contar formas", "costo
mínimo/máximo", "el más largo" con decisiones.

```ts
function coinChange(coins: number[], amount: number): number {          // 1-D
  const dp = new Array<number>(amount + 1).fill(Infinity);
  dp[0] = 0;
  for (let a = 1; a <= amount; a++)
    for (const c of coins)
      if (c <= a) dp[a] = Math.min(dp[a], dp[a - c] + 1);
  return dp[amount] === Infinity ? -1 : dp[amount];
}

function uniquePaths(m: number, n: number): number {                    // 2-D
  const dp = Array.from({ length: m }, () => new Array<number>(n).fill(1));
  for (let r = 1; r < m; r++)
    for (let c = 1; c < n; c++)
      dp[r][c] = dp[r - 1][c] + dp[r][c - 1];
  return dp[m - 1][n - 1];
}
```

**Complejidad**: O(estados × transición).
**Clásicos**: 70 Climbing Stairs, 198 House Robber, 322 Coin Change, 300 LIS, 139 Word Break,
62 Unique Paths, 1143 LCS, 72 Edit Distance.
**Errores típicos**: crear la tabla 2-D con `new Array(m).fill(new Array(n).fill(0))`, que repite
**la misma fila** m veces y hace que escribir en `dp[0][0]` cambie todas; caso base mal o tabla con
tamaño off-by-one; recorrer las dimensiones en un orden que lee una celda todavía sin calcular;
no ver que a veces alcanza con la fila anterior. `Infinity` como centinela es seguro en JS:
`Infinity + 1` sigue siendo `Infinity`, no desborda.

## greedy

**Señal**: una elección localmente óptima lleva al óptimo global, y se puede argumentar por qué.

```ts
function canJump(nums: number[]): boolean {
  let reach = 0;
  for (let i = 0; i < nums.length; i++) {
    if (i > reach) return false;
    reach = Math.max(reach, i + nums[i]);
  }
  return true;
}
```

**Complejidad**: O(n), o O(n log n) si hay sort.
**Clásicos**: 53 Maximum Subarray, 55 Jump Game, 45 Jump Game II, 134 Gas Station,
435 Non-overlapping Intervals.
**Errores típicos**: asumir que greedy funciona sin argumento de intercambio (muchos de estos
son DP); elegir la clave de ordenamiento equivocada; el `sort()` sin comparador otra vez.

## heap / top-k

**Señal**: los k más grandes, mediana móvil, "el mínimo hasta ahora" con inserciones.
**JavaScript no trae heap en la librería estándar**, así que hay que escribirlo. Es la desventaja
concreta del lenguaje para entrevistas, y la razón de tener este template memorizado.

```ts
class MinHeap {
  private a: number[] = [];
  get size(): number { return this.a.length; }
  peek(): number { return this.a[0]; }

  push(x: number): void {
    this.a.push(x);
    let i = this.a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.a[p] <= this.a[i]) break;
      [this.a[p], this.a[i]] = [this.a[i], this.a[p]];
      i = p;
    }
  }

  pop(): number {
    const top = this.a[0];
    const last = this.a.pop()!;
    if (this.a.length) {
      this.a[0] = last;
      let i = 0;
      for (;;) {
        const l = 2 * i + 1, r = l + 1;
        let m = i;
        if (l < this.a.length && this.a[l] < this.a[m]) m = l;
        if (r < this.a.length && this.a[r] < this.a[m]) m = r;
        if (m === i) break;
        [this.a[m], this.a[i]] = [this.a[i], this.a[m]];
        i = m;
      }
    }
    return top;
  }
}

function findKthLargest(nums: number[], k: number): number {
  const h = new MinHeap();                  // min-heap de tamaño k: la cima es el k-esimo
  for (const x of nums) {
    h.push(x);
    if (h.size > k) h.pop();                // saca el mas chico
  }
  return h.peek();
}
```

> **Antes de escribir el heap, preguntarse si hace falta.** Para un top-k de una sola pasada sobre
> un array que ya está entero en memoria, `nums.sort((a,b) => b-a)[k-1]` es O(n log n) contra
> O(n log k) y se escribe en una línea. El heap gana cuando k es mucho menor que n, cuando los
> datos llegan en stream, o cuando el enunciado pide mediana móvil.

**Complejidad**: push/pop O(log n), `peek()` O(1). Un heap de tamaño k sobre n elementos es
O(n log k), contra O(n log n) de ordenar todo.
**Clásicos**: 215 Kth Largest Element, 347 Top K Frequent, 23 Merge k Sorted Lists,
703 Kth Largest in a Stream, 295 Find Median from Data Stream.
**Errores típicos**: max-heap cuando se quería min-heap (invertir la comparación, o insertar `-x`);
`pop()` sobre el heap vacío; mantener el heap de tamaño n en vez de k y perder la ventaja;
equivocar el índice del padre: es `(i-1) >> 1`, no `i >> 1`.

## trie

**Señal**: muchas consultas por **prefijo** sobre un conjunto de strings.

```ts
class TrieNode {
  hijo = new Map<string, TrieNode>();
  fin = false;
}

class Trie {
  private root = new TrieNode();

  insert(word: string): void {
    let nodo = this.root;
    for (const ch of word) {
      let sig = nodo.hijo.get(ch);
      if (!sig) { sig = new TrieNode(); nodo.hijo.set(ch, sig); }
      nodo = sig;
    }
    nodo.fin = true;              // marca de fin de palabra
  }

  startsWith(prefix: string): boolean {
    let nodo = this.root;
    for (const ch of prefix) {
      const sig = nodo.hijo.get(ch);
      if (!sig) return false;
      nodo = sig;
    }
    return true;
  }
}
```

Con alfabeto fijo de 26 letras minúsculas, `new Array<TrieNode | null>(26).fill(null)` indexado
por `ch.charCodeAt(0) - 97` es más rápido y más difícil de escribir bien. El `Map` es la versión
segura para entrevista.

**Complejidad**: insert y search O(L). Espacio O(caracteres totales).
**Clásicos**: 208 Implement Trie, 211 Design Add and Search Words, 212 Word Search II.
**Errores típicos**: olvidar la marca de fin de palabra, así `"app"` matchea aunque solo se
haya insertado `"apple"`; declarar `hijo = new Map()` fuera de la clase y compartir el mismo
mapa entre todos los nodos.

---

# Trampas propias de JavaScript y TypeScript

Estas son las que más rompen entrevistas en JS/TS. Ninguna es un error de algoritmo, y por eso
se registran en `--error-clase`, aparte del resultado del ejercicio.

- **`sort()` sin comparador ordena como string.** `[10, 9, 100].sort()` da `[10, 100, 9]`.
  Siempre `sort((a, b) => a - b)`. Es la número uno.
- **`sort()` muta el array original** y devuelve la misma referencia. Si el original hace falta
  después, `[...a].sort(...)`.
- **`shift()` y `unshift()` son O(n).** Una cola escrita con `shift()` convierte un BFS O(V+E) en
  O(V²). La cola correcta es un array con índice de cabeza.
- **`new Array(n).fill([])` comparte el mismo array n veces.** Vale igual para `fill({})` y para
  las matrices 2-D. Para filas independientes: `Array.from({length: n}, () => [])`.
- **Guardar un array que se sigue mutando guarda la referencia.** En backtracking, `res.push(path)`
  termina con todos los resultados iguales. Va `[...path]`.
- **`||` trata `0` y `""` como ausentes.** Para valores por defecto sobre contadores e índices va
  `??`, que solo cubre `null` y `undefined`. Mismo problema con `if (x)` sobre un índice `0`.
- **`{}` no es un diccionario.** Convierte las claves a string, hereda de `Object.prototype` y no
  tiene `.size`. Usar `Map`.
- **`===` sobre objetos y arrays compara identidad**, no contenido. `[1,2] === [1,2]` es `false`,
  y un `Set` de arrays nunca deduplica.
- **No hay enteros: todo es `number` de 64 bits en punto flotante.** Los enteros son exactos hasta
  2⁵³ (`Number.MAX_SAFE_INTEGER`); pasado eso las sumas mienten en silencio. Los operadores de
  bits (`>>`, `|`, `&`) truncan a 32 bits con signo, así que `x | 0` rompe por encima de 2³¹.
  Si el enunciado habla de valores grandes, `BigInt`.
- **La división no trunca.** `7 / 2` es `3.5` y `a[3.5]` es `undefined`. Va `Math.floor(...)` o
  `>> 1`. `%` conserva el signo del dividendo: `-5 % 3` es `-2`, no `1`.
- **Los strings son inmutables.** `s[i] = 'x'` no hace nada y no tira error. Para modificar hay
  que pasar por array: `const cs = [...s]`, modificar, `cs.join('')`.
- **`for...in` recorre claves de objeto, `for...of` valores.** Sobre un array, `for...in` da los
  índices **como strings**, así que `i + 1` concatena en vez de sumar.
- **El stack de recursión en Node aguanta del orden de 10⁴ frames**, bastante menos que un
  lenguaje compilado. Una DFS profunda sobre una grilla grande revienta con
  `RangeError: Maximum call stack size exceeded`.
- **`map`/`filter` alocan un array nuevo cada vez.** Encadenarlos en un camino caliente es O(n)
  de espacio por eslabón.
- **TypeScript no chequea en runtime.** Los tipos desaparecen al compilar: un `!` que silencia a
  `strictNullChecks` no evita el `TypeError`, solo apaga el aviso.

---

Estructura y contenido adaptados de `kirilxd/swe-interview-coach` (MIT) y
`swapnil5053/algotrace` (MIT). Los templates fueron portados a TypeScript el 2026-09-15: 
antes estaban en C++, ver `base/temario.md`, "Cambios al plan", y la sección de trampas
de JS/TS es propia.
