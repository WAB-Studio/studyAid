# Taxonomía de patrones

Un bloque por patrón: señal de reconocimiento, template en TypeScript, complejidad,
problemas clásicos de LeetCode, errores típicos.

Los templates son para el bloque teórico de una sesión de fondo. Nunca se muestran mientras
el usuario está resolviendo un ejercicio.

---

## two-pointers

**Señal**: array ordenado, "par/triple que suma a X", deduplicar in-place, palíndromo,
contenedor/agua atrapada.
**Usar cuando**: la entrada está ordenada, o la factibilidad del par cambia de forma monótona
al mover los punteros.

```ts
function twoSumSorted(a: number[], target: number): [number, number] | null {
  let lo = 0, hi = a.length - 1;
  while (lo < hi) {
    const s = a[lo] + a[hi];
    if (s === target) return [lo, hi];
    if (s < target) lo++; else hi--;
  }
  return null;
}
```

**Complejidad**: O(n) tiempo, O(1) espacio.
**Clásicos**: 167 Two Sum II, 15 3Sum, 11 Container With Most Water, 125 Valid Palindrome,
42 Trapping Rain Water.
**Errores típicos**: aplicarlo sobre datos sin ordenar; si hay que ordenar primero, el
O(n log n) domina. Off-by-one en `lo < hi`. Olvidar saltear duplicados en 3Sum.

## sliding-window

**Señal**: "subarray/substring **contiguo**", "el más largo/corto que cumple", "a lo sumo k
distintos", "suma máxima de tamaño k".
**Usar cuando**: la respuesta es un rango contiguo Y la validez es monótona: crecer solo puede
romperla, encoger solo puede arreglarla.

```ts
function longestNoRepeat(s: string): number {
  const seen = new Map<string, number>();
  let left = 0, best = 0;
  for (let right = 0; right < s.length; right++) {
    const prev = seen.get(s[right]);
    if (prev !== undefined && prev >= left) left = prev + 1;  // guarda contra índice viejo
    seen.set(s[right], right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
```

**Complejidad**: O(n) tiempo, O(k) espacio.
**Clásicos**: 3 Longest Substring Without Repeating, 424 Longest Repeating Character
Replacement, 567 Permutation in String, 76 Minimum Window Substring, 121 Best Time to Buy and Sell.
**Errores típicos**: mover `left` hacia atrás por un índice viejo (falta la guarda `prev >= left`);
confundir ventana fija con variable.

## fast-slow-pointers

**Señal**: detectar ciclo, nodo del medio, k-ésimo desde el final.

```ts
function hasCycle(head: ListNode | null): boolean {
  let slow = head, fast = head;
  while (fast?.next) {          // guarda antes de .next.next
    slow = slow!.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}
```

**Complejidad**: O(n) tiempo, O(1) espacio.
**Clásicos**: 141 Linked List Cycle, 142 Cycle II, 876 Middle of the Linked List, 202 Happy Number.
**Errores típicos**: desreferenciar `fast.next` sin la guarda; off-by-one sobre cuál puntero es
la respuesta en "el del medio".

## hashing / frequency-map

**Señal**: "¿ya lo vi?", contar ocurrencias, agrupar por clave.

```ts
function groupAnagrams(words: string[]): string[][] {
  const groups = new Map<string, string[]>();
  for (const w of words) {
    const key = [...w].sort().join("");
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(w);
  }
  return [...groups.values()];
}
```

**Complejidad**: O(n·k log k) acá por el sort de cada palabra; lookups O(1) promedio, O(n) peor caso.
**Clásicos**: 1 Two Sum, 49 Group Anagrams, 242 Valid Anagram, 217 Contains Duplicate,
347 Top K Frequent, 128 Longest Consecutive Sequence.
**Errores típicos**: asumir que O(1) es el peor caso; usar objeto plano en vez de `Map` cuando la
clave no es string (el objeto la convierte); usar array y `includes` (O(n)) donde va un `Set`.

## prefix-sum

**Señal**: consultas repetidas de suma de rango, "subarray que suma k".

```ts
function subarraySum(nums: number[], k: number): number {
  const seen = new Map<number, number>([[0, 1]]);   // semilla para subarrays desde el índice 0
  let run = 0, count = 0;
  for (const x of nums) {
    run += x;
    count += seen.get(run - k) ?? 0;
    seen.set(run, (seen.get(run) ?? 0) + 1);
  }
  return count;
}
```

**Complejidad**: O(n) tiempo, O(n) espacio.
**Clásicos**: 560 Subarray Sum Equals K, 303 Range Sum Query, 724 Find Pivot Index,
238 Product of Array Except Self.
**Errores típicos**: olvidar la semilla `{0: 1}` (se pierden los subarrays que arrancan en 0);
off-by-one entre prefijo inclusivo y exclusivo.

## binary-search

**Señal**: "ordenado", "primera/última posición", "minimizar el máximo", array rotado,
o un predicado monótono ("¿alcanza con capacidad x?").
**Incluye buscar sobre la respuesta**: si podés chequear barato "¿x es factible?" y la
factibilidad es monótona en x, binaria sobre el rango de respuestas.

```ts
function lowerBound(a: number[], target: number): number {   // primer índice con a[i] >= target
  let lo = 0, hi = a.length;                                  // intervalo [lo, hi)
  while (lo < hi) {
    const mid = lo + ((hi - lo) >> 1);
    if (a[mid] < target) lo = mid + 1;
    else hi = mid;
  }
  return lo;
}
```

**Complejidad**: O(log n) por búsqueda, por el costo del predicado.
**Clásicos**: 704 Binary Search, 33 Search in Rotated Sorted Array, 153 Find Minimum in Rotated,
875 Koko Eating Bananas, 74 Search a 2D Matrix.
**Errores típicos**: mezclar convenciones `[lo, hi]` y `[lo, hi)` y colgarse en bucle infinito;
quedarse con la mitad equivocada en el rotado; devolver `mid` en vez de `lo`.

## intervalos

**Señal**: rangos que se solapan — mergear, insertar, contar eventos concurrentes.

```ts
function merge(intervals: number[][]): number[][] {
  intervals.sort((x, y) => x[0] - y[0]);      // sin comparador el sort es LEXICOGRÁFICO
  const out: number[][] = [intervals[0]];
  for (const [s, e] of intervals.slice(1)) {
    const last = out[out.length - 1];
    if (s <= last[1]) last[1] = Math.max(last[1], e);
    else out.push([s, e]);
  }
  return out;
}
```

**Complejidad**: O(n log n) por el sort, O(n) el barrido.
**Clásicos**: 56 Merge Intervals, 57 Insert Interval, 435 Non-overlapping Intervals.
**Errores típicos**: ordenar por fin cuando iba por inicio; el test de solapamiento `<` vs `<=`
decide si los que se tocan se mergean.

## linked-list

**Señal**: splice, reverso, merge de nodos. Usá nodo dummy para que el primero no sea caso especial.

```ts
function reverseList(head: ListNode | null): ListNode | null {
  let prev: ListNode | null = null, cur = head;
  while (cur) {
    const next = cur.next;    // guardar ANTES de reescribir
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
devolver `dummy` en vez de `dummy.next`; la versión recursiva NO es O(1) espacio.

## stack y monotonic-stack

**Señal**: emparejar o anidar (paréntesis, undo) → pila común. "Próximo mayor/menor",
acotar un histograma → pila monótona.

```ts
function dailyTemperatures(t: number[]): number[] {
  const res = new Array(t.length).fill(0);
  const stack: number[] = [];                  // índices, temperaturas decrecientes
  for (let i = 0; i < t.length; i++) {
    while (stack.length && t[stack[stack.length - 1]] < t[i]) {
      const j = stack.pop()!;
      res[j] = i - j;
    }
    stack.push(i);
  }
  return res;
}
```

**Complejidad**: O(n) tiempo (cada índice entra y sale una vez), O(n) espacio.
**Clásicos**: 20 Valid Parentheses, 155 Min Stack, 150 Evaluate RPN, 739 Daily Temperatures,
84 Largest Rectangle in Histogram.
**Errores típicos**: apilar valores cuando necesitabas índices; comparación estricta o no
estricta que admite iguales cuando no debe.

## bfs

**Señal**: camino más corto en grafo o grilla **sin pesos**, recorrido por niveles.

```ts
function bfsShortest(start: string, goal: string, vecinos: (n: string) => string[]): number {
  const cola: Array<[string, number]> = [[start, 0]];
  const visto = new Set([start]);
  let head = 0;                                  // índice: Array.shift() es O(n) en JS
  while (head < cola.length) {
    const [nodo, d] = cola[head++];
    if (nodo === goal) return d;
    for (const sig of vecinos(nodo)) {
      if (!visto.has(sig)) {                     // marcar al ENCOLAR, no al desencolar
        visto.add(sig);
        cola.push([sig, d + 1]);
      }
    }
  }
  return -1;
}
```

**Complejidad**: O(V + E) tiempo, O(V) espacio.
**Clásicos**: 200 Number of Islands, 994 Rotting Oranges, 127 Word Ladder, 102 Level Order Traversal.
**Errores típicos**: marcar visitado al desencolar (el mismo nodo entra muchas veces);
usar `shift()` en vez de un índice, que convierte el O(V+E) en O(V²).

## dfs

**Señal**: componentes conexas, caminos en un árbol, alcanzabilidad. El camino más corto no importa.

```ts
function numIslands(grid: string[][]): number {
  const R = grid.length, C = grid[0].length;
  const dfs = (r: number, c: number): void => {
    if (r < 0 || r >= R || c < 0 || c >= C || grid[r][c] !== "1") return;
    grid[r][c] = "0";                            // marcar in-place
    dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1);
  };
  let count = 0;
  for (let r = 0; r < R; r++)
    for (let c = 0; c < C; c++)
      if (grid[r][c] === "1") { dfs(r, c); count++; }
  return count;
}
```

**Complejidad**: O(V + E) tiempo, O(V) espacio de stack.
**Clásicos**: 200 Number of Islands, 133 Clone Graph, 695 Max Area of Island, 417 Pacific Atlantic.
**Errores típicos**: no marcar visitado → recursión infinita con ciclos; el stack de recursión
cuenta como espacio.

## backtracking

**Señal**: enumerar todas las combinaciones, permutaciones, subconjuntos, o llenar un tablero.
Elegir, recursar, **deshacer**.

```ts
function subsets(nums: number[]): number[][] {
  const res: number[][] = [], path: number[] = [];
  const bt = (start: number): void => {
    res.push([...path]);                    // COPIA, no alias
    for (let i = start; i < nums.length; i++) {
      path.push(nums[i]);                   // elegir
      bt(i + 1);
      path.pop();                           // deshacer
    }
  };
  bt(0);
  return res;
}
```

**Complejidad**: exponencial — O(2^n) subconjuntos, O(n!) permutaciones, por O(n) de copiar.
**Clásicos**: 78 Subsets, 46 Permutations, 39 Combination Sum, 79 Word Search, 51 N-Queens.
**Errores típicos**: hacer `push(path)` en vez de `push([...path])` (todos los resultados
apuntan al mismo array); olvidar el `pop()`; no podar y explorar ramas imposibles.

## dynamic-programming

**Señal**: subproblemas que se repiten y subestructura óptima — "contar formas", "costo
mínimo/máximo", "el más largo" con decisiones.

```ts
function coinChange(coins: number[], amount: number): number {   // 1-D
  const dp = new Array(amount + 1).fill(Infinity);
  dp[0] = 0;
  for (let a = 1; a <= amount; a++)
    for (const c of coins)
      if (c <= a) dp[a] = Math.min(dp[a], dp[a - c] + 1);
  return dp[amount] === Infinity ? -1 : dp[amount];
}

function uniquePaths(m: number, n: number): number {             // 2-D
  const dp = Array.from({ length: m }, () => new Array(n).fill(1));
  for (let r = 1; r < m; r++)
    for (let c = 1; c < n; c++)
      dp[r][c] = dp[r - 1][c] + dp[r][c - 1];
  return dp[m - 1][n - 1];
}
```

**Complejidad**: O(estados × transición).
**Clásicos**: 70 Climbing Stairs, 198 House Robber, 322 Coin Change, 300 LIS, 139 Word Break,
62 Unique Paths, 1143 LCS, 72 Edit Distance.
**Errores típicos**: caso base mal o tabla con tamaño off-by-one; recorrer las dimensiones en un
orden que lee una celda todavía sin calcular; no ver que a veces alcanza con la fila anterior;
`Array.from({length: m}, () => ...)` en vez de `new Array(m).fill([])`, que comparte la misma fila.

## greedy

**Señal**: una elección localmente óptima lleva al óptimo global, y podés argumentar por qué.

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
son DP); elegir la clave de ordenamiento equivocada.

## heap / top-k

**Señal**: los k más grandes, mediana móvil, "el mínimo hasta ahora" con inserciones.
**JS no tiene heap en la librería estándar.** En una entrevista en JS hay que escribirlo o
justificar usar sort.

```ts
class MinHeap {
  private a: number[] = [];
  get size() { return this.a.length; }
  push(v: number): void {
    this.a.push(v);
    let i = this.a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.a[p] <= this.a[i]) break;
      [this.a[p], this.a[i]] = [this.a[i], this.a[p]];
      i = p;
    }
  }
  pop(): number | undefined {
    if (!this.a.length) return undefined;
    const top = this.a[0], last = this.a.pop()!;
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
```

**Complejidad**: push/pop O(log n). Un heap de tamaño k sobre n elementos es O(n log k),
contra O(n log n) de ordenar todo.
**Clásicos**: 215 Kth Largest Element, 347 Top K Frequent, 23 Merge k Sorted Lists,
703 Kth Largest in a Stream, 295 Find Median from Data Stream.
**Errores típicos**: ordenar todo cuando alcanzaba un heap de tamaño k; en un max-heap sobre
este template, negar los valores.

## topological-sort

**Señal**: ordenar tareas con dependencias sobre un DAG, o detectar ciclos.

```ts
function topoSort(n: number, edges: Array<[number, number]>): number[] {
  const indeg = new Array(n).fill(0);
  const adj: number[][] = Array.from({ length: n }, () => []);
  for (const [u, v] of edges) { adj[u].push(v); indeg[v]++; }

  const cola: number[] = [];
  for (let i = 0; i < n; i++) if (indeg[i] === 0) cola.push(i);

  const orden: number[] = [];
  let head = 0;
  while (head < cola.length) {
    const u = cola[head++];
    orden.push(u);
    for (const v of adj[u]) if (--indeg[v] === 0) cola.push(v);
  }
  return orden.length === n ? orden : [];        // [] significa que hay ciclo
}
```

**Complejidad**: O(V + E).
**Clásicos**: 207 Course Schedule, 210 Course Schedule II, 269 Alien Dictionary.
**Errores típicos**: no detectar el ciclo (`orden.length < n`); confundir la dirección de la arista.

## union-find

**Señal**: consultar o unir componentes conexas de forma incremental.

```ts
class DSU {
  private parent: number[];
  private rank: number[];
  constructor(n: number) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.rank = new Array(n).fill(0);
  }
  find(x: number): number {
    if (this.parent[x] !== x) this.parent[x] = this.find(this.parent[x]);  // compresión
    return this.parent[x];
  }
  union(a: number, b: number): boolean {
    const ra = this.find(a), rb = this.find(b);
    if (ra === rb) return false;
    if (this.rank[ra] < this.rank[rb]) this.parent[ra] = rb;
    else if (this.rank[rb] < this.rank[ra]) this.parent[rb] = ra;
    else { this.parent[rb] = ra; this.rank[ra]++; }
    return true;
  }
}
```

**Complejidad**: O(α(n)) amortizado por operación, efectivamente O(1).
**Clásicos**: 547 Number of Provinces, 684 Redundant Connection, 721 Accounts Merge.
**Errores típicos**: sin compresión de caminos degenera en cadenas O(n); olvidar que `union`
devuelve si hubo merge (clave para detectar la arista redundante).

## trie

**Señal**: muchas consultas por **prefijo** sobre un conjunto de strings.

```ts
class Trie {
  private root: Record<string, any> = {};
  insert(word: string): void {
    let node = this.root;
    for (const ch of word) node = (node[ch] ??= {});
    node["$"] = true;                            // marca de fin de palabra
  }
  startsWith(prefix: string): boolean {
    let node = this.root;
    for (const ch of prefix) {
      if (!(ch in node)) return false;
      node = node[ch];
    }
    return true;
  }
}
```

**Complejidad**: insert y search O(L). Espacio O(caracteres totales).
**Clásicos**: 208 Implement Trie, 211 Design Add and Search Words, 212 Word Search II.
**Errores típicos**: olvidar la marca de fin de palabra, así `"app"` matchea aunque solo se
haya insertado `"apple"`.

---

# Trampas propias de JavaScript/TypeScript

Estas no aparecen en los cheatsheets escritos para Python y son las que más rompen entrevistas en JS.

- **`arr.sort()` sin comparador ordena como strings.** `[10, 9, 1].sort()` da `[1, 10, 9]`.
  Siempre `sort((a, b) => a - b)`.
- **`Array.shift()` es O(n).** Una BFS con `shift()` pasa de O(V+E) a O(V²). Usá un índice `head`.
- **No hay heap ni deque en la stdlib.** Hay que implementarlos o justificar la alternativa.
- **Los operadores bit a bit truncan a 32 bits con signo.** `1 << 31` es negativo. Para
  desplazamiento sin signo, `>>>`.
- **`Number` pierde precisión sobre 2^53.** Si el enunciado habla de enteros de 64 bits, `BigInt`.
- **Objeto plano vs `Map`**: el objeto convierte toda clave a string, así que `obj[1]` y `obj["1"]`
  son la misma. `Map` acepta cualquier tipo y preserva orden de inserción.
- **`new Array(n)` deja huecos**, y `.map()` los saltea. Hacé `.fill(0)` primero.
- **`Array(m).fill([])` comparte el mismo array en todas las filas.** Usá
  `Array.from({length: m}, () => [])`.
- **Comparar objetos con `===` compara referencias.** Dos nodos con el mismo valor no son iguales.
- **El stack de Node aguanta ~10.000 frames.** Más holgado que Python, pero una DFS sobre una
  grilla grande igual lo revienta.

---

Estructura y contenido adaptados de `kirilxd/swe-interview-coach` (MIT) y
`swapnil5053/algotrace` (MIT). Los templates fueron portados de Python a TypeScript y la
sección de trampas de JS/TS es propia.
