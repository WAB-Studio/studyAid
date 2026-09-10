# Taxonomía de patrones

Un bloque por patrón: señal de reconocimiento, template en C++, complejidad,
problemas clásicos de LeetCode, errores típicos.

Los templates son para el bloque teórico de una sesión de fondo. Nunca se muestran mientras
el usuario está resolviendo un ejercicio.

Se asume el preámbulo que LeetCode ya provee: los headers de la librería estándar y
`using namespace std;`.

---

## two-pointers

**Señal**: array ordenado, "par/triple que suma a X", deduplicar in-place, palíndromo,
contenedor/agua atrapada.
**Usar cuando**: la entrada está ordenada, o la factibilidad del par cambia de forma monótona
al mover los punteros.

```cpp
vector<int> twoSumSorted(const vector<int>& a, int target) {
    int lo = 0, hi = (int)a.size() - 1;        // cast: size() es unsigned
    while (lo < hi) {
        int s = a[lo] + a[hi];
        if (s == target) return {lo, hi};
        if (s < target) lo++;
        else hi--;
    }
    return {};
}
```

**Complejidad**: O(n) tiempo, O(1) espacio.
**Clásicos**: 167 Two Sum II, 15 3Sum, 11 Container With Most Water, 125 Valid Palindrome,
42 Trapping Rain Water.
**Errores típicos**: aplicarlo sobre datos sin ordenar; si hay que ordenar primero, el
O(n log n) domina. Off-by-one en `lo < hi`. Olvidar saltear duplicados en 3Sum.
Comparar `int` con `a.size()` sin castear: el `int` se promueve a unsigned y `-1` se vuelve enorme.

## sliding-window

**Señal**: "subarray/substring **contiguo**", "el más largo/corto que cumple", "a lo sumo k
distintos", "suma máxima de tamaño k".
**Usar cuando**: la respuesta es un rango contiguo Y la validez es monótona: crecer solo puede
romperla, encoger solo puede arreglarla.

```cpp
int longestNoRepeat(const string& s) {
    unordered_map<char, int> ultimo;           // char -> ultimo indice visto
    int left = 0, best = 0;
    for (int right = 0; right < (int)s.size(); right++) {
        auto it = ultimo.find(s[right]);
        if (it != ultimo.end() && it->second >= left) {
            left = it->second + 1;             // guarda contra un indice viejo
        }
        ultimo[s[right]] = right;
        best = max(best, right - left + 1);
    }
    return best;
}
```

**Complejidad**: O(n) tiempo, O(k) espacio.
**Clásicos**: 3 Longest Substring Without Repeating, 424 Longest Repeating Character
Replacement, 567 Permutation in String, 76 Minimum Window Substring, 121 Best Time to Buy and Sell.
**Errores típicos**: mover `left` hacia atrás por un índice viejo (falta la guarda `>= left`);
confundir ventana fija con variable; usar `ultimo[c]` para consultar, que **inserta** la clave
con valor 0 si no estaba.

## fast-slow-pointers

**Señal**: detectar ciclo, nodo del medio, k-ésimo desde el final.

```cpp
bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {               // guarda ANTES de fast->next->next
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

**Complejidad**: O(n) tiempo, O(1) espacio.
**Clásicos**: 141 Linked List Cycle, 142 Cycle II, 876 Middle of the Linked List, 202 Happy Number.
**Errores típicos**: desreferenciar `fast->next` sin la guarda — en C++ eso no es `undefined`,
es un **segfault** o, peor, memoria basura; off-by-one sobre cuál puntero es la respuesta
en "el del medio".

## hashing / frequency-map

**Señal**: "¿ya lo vi?", contar ocurrencias, agrupar por clave.

```cpp
vector<vector<string>> groupAnagrams(vector<string>& words) {
    unordered_map<string, vector<string>> grupos;
    for (const string& w : words) {            // & : no copia cada string
        string key = w;
        sort(key.begin(), key.end());
        grupos[key].push_back(w);              // aca [] insertando esta BIEN: querés crearla
    }
    vector<vector<string>> res;
    for (auto& [_, v] : grupos) res.push_back(move(v));
    return res;
}
```

**Complejidad**: O(n·k log k) acá por el sort de cada palabra; lookups O(1) promedio, O(n) peor caso.
**Clásicos**: 1 Two Sum, 49 Group Anagrams, 242 Valid Anagram, 217 Contains Duplicate,
347 Top K Frequent, 128 Longest Consecutive Sequence.
**Errores típicos**: asumir que O(1) es el peor caso; usar `map` (árbol, O(log n)) cuando querías
`unordered_map`; consultar con `m[k]` en vez de `.count()` y ensuciar el mapa; recorrer con
`for (auto x : v)` y copiar cada elemento.

## prefix-sum

**Señal**: consultas repetidas de suma de rango, "subarray que suma k".

```cpp
int subarraySum(vector<int>& nums, int k) {
    unordered_map<long long, int> vistos;
    vistos[0] = 1;                             // semilla: subarrays que arrancan en el indice 0
    long long run = 0;                         // long long: la suma puede desbordar int
    int count = 0;
    for (int x : nums) {
        run += x;
        auto it = vistos.find(run - k);
        if (it != vistos.end()) count += it->second;
        vistos[run]++;
    }
    return count;
}
```

**Complejidad**: O(n) tiempo, O(n) espacio.
**Clásicos**: 560 Subarray Sum Equals K, 303 Range Sum Query, 724 Find Pivot Index,
238 Product of Array Except Self.
**Errores típicos**: olvidar la semilla `vistos[0] = 1` (se pierden los subarrays que arrancan
en 0); off-by-one entre prefijo inclusivo y exclusivo; acumular en `int` y desbordar.

## binary-search

**Señal**: "ordenado", "primera/última posición", "minimizar el máximo", array rotado,
o un predicado monótono ("¿alcanza con capacidad x?").
**Incluye buscar sobre la respuesta**: si podés chequear barato "¿x es factible?" y la
factibilidad es monótona en x, binaria sobre el rango de respuestas.

```cpp
int lowerBound(const vector<int>& a, int target) {   // primer indice con a[i] >= target
    int lo = 0, hi = (int)a.size();                  // intervalo [lo, hi)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;                // NO (lo + hi) / 2: puede desbordar
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

La stdlib ya lo trae: `lower_bound(a.begin(), a.end(), x)` y `upper_bound(...)`. Devuelven
iteradores; para el índice, restá `a.begin()`. En entrevista conviene saber escribirlo igual.

**Complejidad**: O(log n) por búsqueda, por el costo del predicado.
**Clásicos**: 704 Binary Search, 33 Search in Rotated Sorted Array, 153 Find Minimum in Rotated,
875 Koko Eating Bananas, 74 Search a 2D Matrix.
**Errores típicos**: mezclar convenciones `[lo, hi]` y `[lo, hi)` y colgarse en bucle infinito;
`(lo + hi) / 2` que desborda con índices grandes; quedarse con la mitad equivocada en el rotado;
devolver `mid` en vez de `lo`.

## intervalos

**Señal**: rangos que se solapan — mergear, insertar, contar eventos concurrentes.

```cpp
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());     // ordena por [0], despues por [1]
    vector<vector<int>> out;
    for (const auto& iv : intervals) {
        if (!out.empty() && iv[0] <= out.back()[1]) {
            out.back()[1] = max(out.back()[1], iv[1]);
        } else {
            out.push_back(iv);
        }
    }
    return out;
}
```

**Complejidad**: O(n log n) por el sort, O(n) el barrido.
**Clásicos**: 56 Merge Intervals, 57 Insert Interval, 435 Non-overlapping Intervals.
**Errores típicos**: ordenar por fin cuando iba por inicio; el test de solapamiento `<` vs `<=`
decide si los que se tocan se mergean; olvidar el `!out.empty()` y llamar `back()` sobre un
vector vacío, que es comportamiento indefinido.

## linked-list

**Señal**: splice, reverso, merge de nodos. Usá nodo dummy para que el primero no sea caso especial.

```cpp
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur) {
        ListNode* next = cur->next;   // guardar ANTES de reescribir
        cur->next = prev;
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
devolver `dummy` en vez de `dummy->next`; la versión recursiva NO es O(1) espacio;
desreferenciar un `nullptr` — acá el precio es un segfault, no un mensaje de error.

## stack y monotonic-stack

**Señal**: emparejar o anidar (paréntesis, undo) → pila común. "Próximo mayor/menor",
acotar un histograma → pila monótona.

```cpp
vector<int> dailyTemperatures(vector<int>& t) {
    int n = t.size();
    vector<int> res(n, 0);
    vector<int> st;                                // indices, temperaturas decrecientes
    for (int i = 0; i < n; i++) {
        while (!st.empty() && t[st.back()] < t[i]) {
            int j = st.back();
            st.pop_back();
            res[j] = i - j;
        }
        st.push_back(i);
    }
    return res;
}
```

Un `vector<int>` con `push_back`/`back`/`pop_back` es la pila idiomática en competitivo:
`std::stack` funciona igual pero no deja indexar.

**Complejidad**: O(n) tiempo (cada índice entra y sale una vez), O(n) espacio.
**Clásicos**: 20 Valid Parentheses, 155 Min Stack, 150 Evaluate RPN, 739 Daily Temperatures,
84 Largest Rectangle in Histogram.
**Errores típicos**: apilar valores cuando necesitabas índices; `pop_back()` **no devuelve** el
elemento, hay que leer `back()` antes; comparación estricta o no estricta que admite iguales
cuando no debe.

## bfs

**Señal**: camino más corto en grafo o grilla **sin pesos**, recorrido por niveles.

```cpp
int bfsGrid(vector<vector<int>>& grid, pair<int,int> start) {
    int R = grid.size(), C = grid[0].size();
    vector<vector<bool>> visto(R, vector<bool>(C, false));
    queue<pair<int,int>> q;                        // C++ SI trae cola: pop_front es O(1)
    q.push(start);
    visto[start.first][start.second] = true;

    int dist = 0;
    const int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        int nivel = q.size();                      // fijar el tamaño ANTES del bucle
        for (int i = 0; i < nivel; i++) {
            auto [r, c] = q.front();
            q.pop();
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
                if (visto[nr][nc] || grid[nr][nc] == 0) continue;
                visto[nr][nc] = true;              // marcar al ENCOLAR, no al desencolar
                q.push({nr, nc});
            }
        }
        dist++;
    }
    return dist;
}
```

**Complejidad**: O(V + E) tiempo, O(V) espacio.
**Clásicos**: 200 Number of Islands, 994 Rotting Oranges, 127 Word Ladder, 102 Level Order Traversal.
**Errores típicos**: marcar visitado al desencolar (el mismo nodo entra muchas veces);
leer `q.size()` dentro del `for` mientras la cola crece; `q.pop()` **no devuelve** nada, hay que
leer `q.front()` antes.

## dfs

**Señal**: componentes conexas, caminos en un árbol, alcanzabilidad. El camino más corto no importa.

```cpp
class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int R = grid.size(), C = grid[0].size(), count = 0;
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                if (grid[r][c] == '1') { dfs(grid, r, c); count++; }
        return count;
    }
private:
    void dfs(vector<vector<char>>& grid, int r, int c) {   // & : sin copiar la grilla
        int R = grid.size(), C = grid[0].size();
        if (r < 0 || r >= R || c < 0 || c >= C || grid[r][c] != '1') return;
        grid[r][c] = '0';                                  // marcar in-place
        dfs(grid, r + 1, c); dfs(grid, r - 1, c);
        dfs(grid, r, c + 1); dfs(grid, r, c - 1);
    }
};
```

**Complejidad**: O(V + E) tiempo, O(V) espacio de stack.
**Clásicos**: 200 Number of Islands, 133 Clone Graph, 695 Max Area of Island, 417 Pacific Atlantic.
**Errores típicos**: **pasar la grilla por valor** (sin `&`) — se copia en cada llamada y además
las marcas se pierden; no marcar visitado → recursión infinita con ciclos; el stack de recursión
cuenta como espacio y en C++ son ~1 MB, unos 10^5 frames.

## backtracking

**Señal**: enumerar todas las combinaciones, permutaciones, subconjuntos, o llenar un tablero.
Elegir, recursar, **deshacer**.

```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        bt(nums, 0);
        return res;
    }
private:
    vector<vector<int>> res;
    vector<int> path;
    void bt(vector<int>& nums, int start) {
        res.push_back(path);                    // copia por valor: en C++ es automatico
        for (int i = start; i < (int)nums.size(); i++) {
            path.push_back(nums[i]);            // elegir
            bt(nums, i + 1);
            path.pop_back();                    // deshacer
        }
    }
};
```

**Complejidad**: exponencial — O(2^n) subconjuntos, O(n!) permutaciones, por O(n) de copiar.
**Clásicos**: 78 Subsets, 46 Permutations, 39 Combination Sum, 79 Word Search, 51 N-Queens.
**Errores típicos**: olvidar el `pop_back()`; no podar y explorar ramas imposibles.
Nota: `res.push_back(path)` **copia** el vector, al revés que en JS donde había que escribir
`[...path]` a mano. Acá el riesgo es el opuesto: copiar sin querer en el camino caliente.

## dynamic-programming

**Señal**: subproblemas que se repiten y subestructura óptima — "contar formas", "costo
mínimo/máximo", "el más largo" con decisiones.

```cpp
int coinChange(vector<int>& coins, int amount) {          // 1-D
    const int INF = 1e9;                                  // centinela: NO INT_MAX
    vector<int> dp(amount + 1, INF);
    dp[0] = 0;
    for (int a = 1; a <= amount; a++)
        for (int c : coins)
            if (c <= a) dp[a] = min(dp[a], dp[a - c] + 1);
    return dp[amount] == INF ? -1 : dp[amount];
}

int uniquePaths(int m, int n) {                           // 2-D
    vector<vector<int>> dp(m, vector<int>(n, 1));
    for (int r = 1; r < m; r++)
        for (int c = 1; c < n; c++)
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1];
    return dp[m - 1][n - 1];
}
```

**Complejidad**: O(estados × transición).
**Clásicos**: 70 Climbing Stairs, 198 House Robber, 322 Coin Change, 300 LIS, 139 Word Break,
62 Unique Paths, 1143 LCS, 72 Edit Distance.
**Errores típicos**: usar `INT_MAX` como infinito y desbordar en `dp[a-c] + 1` — eso es
comportamiento indefinido, usá `1e9`; caso base mal o tabla con tamaño off-by-one; recorrer las
dimensiones en un orden que lee una celda todavía sin calcular; no ver que a veces alcanza con
la fila anterior.

## greedy

**Señal**: una elección localmente óptima lleva al óptimo global, y podés argumentar por qué.

```cpp
bool canJump(vector<int>& nums) {
    int reach = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        if (i > reach) return false;
        reach = max(reach, i + nums[i]);
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
**C++ trae `priority_queue` en la stdlib**, así que no hay que implementarla. Es una de las
ventajas concretas del lenguaje para entrevistas.

```cpp
int findKthLargest(vector<int>& nums, int k) {
    // min-heap de tamaño k: la cima es el k-esimo mas grande
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int x : nums) {
        pq.push(x);
        if ((int)pq.size() > k) pq.pop();       // saca el mas chico
    }
    return pq.top();
}
```

> **`priority_queue` es MAX-heap por defecto.** Para min-heap hay que escribir los tres
> parámetros: `priority_queue<T, vector<T>, greater<T>>`. Es el error número uno del contenedor.

Para pares, `priority_queue<pair<int,int>>` ordena por `.first` y desempata por `.second`.
Con un comparador propio: `priority_queue<T, vector<T>, decltype(cmp)> pq(cmp);`.

**Complejidad**: push/pop O(log n), `top()` O(1). Un heap de tamaño k sobre n elementos es
O(n log k), contra O(n log n) de ordenar todo.
**Clásicos**: 215 Kth Largest Element, 347 Top K Frequent, 23 Merge k Sorted Lists,
703 Kth Largest in a Stream, 295 Find Median from Data Stream.
**Errores típicos**: max-heap cuando querías min-heap; `pop()` no devuelve el elemento, hay que
leer `top()` antes; mantener el heap de tamaño n en vez de k y perder la ventaja.

## trie

**Señal**: muchas consultas por **prefijo** sobre un conjunto de strings.

```cpp
class Trie {
    struct Node {
        Node* hijo[26] = {};      // inicializa los 26 a nullptr
        bool fin = false;
    };
    Node* root = new Node();
public:
    void insert(const string& word) {
        Node* nodo = root;
        for (char ch : word) {
            int i = ch - 'a';
            if (!nodo->hijo[i]) nodo->hijo[i] = new Node();
            nodo = nodo->hijo[i];
        }
        nodo->fin = true;         // marca de fin de palabra
    }
    bool startsWith(const string& prefix) {
        Node* nodo = root;
        for (char ch : prefix) {
            int i = ch - 'a';
            if (!nodo->hijo[i]) return false;
            nodo = nodo->hijo[i];
        }
        return true;
    }
};
```

**Complejidad**: insert y search O(L). Espacio O(caracteres totales).
**Clásicos**: 208 Implement Trie, 211 Design Add and Search Words, 212 Word Search II.
**Errores típicos**: olvidar la marca de fin de palabra, así `"app"` matchea aunque solo se
haya insertado `"apple"`; `ch - 'a'` con entrada que no es minúscula, que indexa fuera del array.

---

# Trampas propias de C++

Estas no aparecen en los cheatsheets escritos para Python y son las que más rompen entrevistas en C++.

- **Pasar un contenedor por valor lo copia entero.** `void f(vector<int> v)` cuesta O(n) antes de
  la primera línea. Para leer: `const vector<int>&`. Para modificar el original: `vector<int>&`.
- **`m[k]` inserta si la clave no está.** Leer `if (m[k] > 0)` crea la entrada con valor 0 y
  ensucia el mapa y su tamaño. Para consultar: `.count(k)` o `.find(k)`.
- **`size()` devuelve `size_t`, sin signo.** `v.size() - 1` con el vector vacío da un número
  gigantesco, no `-1`. Y `for (int i = 0; i < v.size(); i++)` promueve `i` a unsigned.
  Castear: `(int)v.size()`.
- **`int` se desborda cerca de 2·10⁹.** Sumas acumuladas, productos y `mid = (lo+hi)/2` con
  índices grandes necesitan `long long`. El desborde de `int` con signo es comportamiento
  indefinido: no da un número raro, habilita al compilador a cualquier cosa.
- **`priority_queue` es MAX-heap por defecto.** Min-heap: `greater<T>` como tercer parámetro.
- **`map` no es `unordered_map`.** `map` es un árbol: O(log n) y ordenado. `unordered_map` es
  tabla hash: O(1) promedio. Casi siempre querés el segundo.
- **`pop()` no devuelve el elemento**, ni en `stack`, ni en `queue`, ni en `priority_queue`.
  Hay que leer `top()` o `front()` antes.
- **`push_back` puede invalidar todos los iteradores y referencias** al vector, porque realoca.
  Guardar `&v[i]` y después hacer `push_back` deja esa referencia colgando.
- **`for (auto x : v)` copia cada elemento.** Con `vector<string>` o `vector<vector<int>>` eso es
  O(n) extra por iteración. Usá `const auto&`, o `auto&` si vas a modificar.
- **La división entera trunca hacia cero**: `-5 / 2 == -2`, no `-3`. Y `%` puede dar negativo.
- **`vector<bool>` no es un vector de bool**: está empaquetado en bits y no devuelve referencias
  reales. Si necesitás punteros o referencias a los elementos, usá `vector<char>`.
- **El stack de recursión son ~1 MB**, unos 10^5 frames. Una DFS sobre una grilla de 10^6 celdas
  lo revienta con un stack overflow silencioso.
- **`sort` necesita `<algorithm>`** y los contenedores sus headers. LeetCode los incluye todos;
  un compilador online, no.

---

Estructura y contenido adaptados de `kirilxd/swe-interview-coach` (MIT) y
`swapnil5053/algotrace` (MIT). Los templates fueron portados a C++ y la sección de trampas
de C++ es propia.
