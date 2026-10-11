# Propuesta de poda del mazo

Activas: 33 (las otras 7 ya están retiradas: c0007, c0008, c0014, c0019, c0020, c0025, c0028).
Meta: menos de la mitad (16 o menos).

## Conservar

### c0029 (complejidad)
- Frente actual: Un bucle recorre el string y adentro llama a una función que también lo recorre, pero esa llamada ocurre como máximo una vez y devuelve ahí mismo. ¿Es cuadrático?
- Ya es una situación concreta con resultado concreto y registro neutral.

### c0031 (cpp)
- Frente actual: En C++, dado el vector v = [10, 20, 30, 40]: ¿a qué elemento apunta v.end(), y cuántos elementos tiene el rango [v.begin(), v.end())?
- Ya cumple. Absorbe a c0026 (rangos cerrado y medio abierto).

## Reescribir (retirar la vieja y agregar la nueva)

### c0001 (complejidad)
- Frente actual: Tenés dos bucles anidados, pero el de adentro recorre siempre las 26 letras del alfabeto. ¿Cuál es la complejidad en tiempo?
- Motivo: voseo y falta decir sobre qué itera el bucle externo.
- Frente nuevo: Dos bucles anidados: el externo recorre un string de largo n y el interno las 26 letras del alfabeto. ¿Complejidad en tiempo?
- Dorso nuevo: O(n): 26 no depende del input, así que O(26n) = O(n).
  Hay que mirar sobre qué itera cada bucle, no contarlos.

### c0003 (complejidad)
- Frente actual: El enunciado dice n <= 10^5. ¿Cuál es la complejidad más lenta que entra, y de dónde sale ese número?
- Motivo: dos preguntas en una; mejor un sí/no concreto.
- Frente nuevo: Un problema de LeetCode con n <= 10^5. ¿Entra en tiempo una solución O(n²)?
- Dorso nuevo: No: son 10^10 operaciones contra unas 10^8 por segundo.
  Lo más lento que entra es O(n log n).

### c0004 (complejidad)
- Frente actual: Escribís una función recursiva que no aloca ninguna estructura. ¿Cuál es su espacio auxiliar?
- Motivo: voseo y abstracta; pasar a un código concreto.
- Frente nuevo: `bool pal(const string& s, int i, int j) { return i >= j || (s[i] == s[j] && pal(s, i + 1, j - 1)); }` llamada con i = 0 y j = n - 1. ¿Espacio auxiliar?
- Dorso nuevo: O(n): la recursión llega a n/2 de profundidad y cada llamada ocupa un marco en la pila.
  No alocar estructuras no significa O(1) de espacio.

### c0009 (cpp)
- Frente actual: En C++, ¿qué diferencia hay entre void f(vector<int> v) y void f(vector<int>& v)?
- Motivo: pregunta de diferencia abierta; pasar a costo concreto.
- Frente nuevo: `int f(vector<int> v) { return v[0]; }` se llama n veces dentro de un bucle, con un vector de n elementos. ¿Complejidad total?
- Dorso nuevo: O(n²): sin & cada llamada copia el vector entero.
  Con `const vector<int>&` sería O(n).

### c0010 (cpp)
- Frente actual: ¿Qué pasa si leés m[k] de un unordered_map con una clave que no existe?
- Motivo: voseo; pasar a "qué imprime".
- Frente nuevo: `unordered_map<int, int> m; if (m[5] == 0) {} cout << m.size();` ¿Qué imprime?
- Dorso nuevo: 1: `m[5]` inserta la clave 5 con valor 0.
  Para consultar sin insertar: `m.count(5)` o `m.find(5)`.

### c0012 (cpp)
- Frente actual: ¿Qué tipo devuelve nums.size() y por qué es peligroso restarle 1?
- Motivo: pasar a qué hace un código concreto.
- Frente nuevo: `vector<int> v; for (int i = 0; i <= v.size() - 1; i++) cout << v[i];` ¿Qué pasa?
- Dorso nuevo: Lee fuera del vector: `size()` es `size_t` sin signo y 0 - 1 da 2^64 - 1.
  Escribir `i < (int)v.size()`.

### c0017 (arrays-strings)
- Frente actual: Estas leyendo un enunciado. Que frases te dicen que el problema quiere una solucion in-place con dos punteros?
- Motivo: abierta, sin tildes, tuteo.
- Frente nuevo: Enunciado: "remove all occurrences of val from nums in-place, the order may change, use O(1) extra memory, return k". ¿Qué patrón y por qué?
- Dorso nuevo: Dos punteros de lectura y escritura sobre el mismo array.
  In-place con O(1) extra y devolver k piden compactar lo que sobrevive al principio.

### c0018 (arrays-strings)
- Frente actual: En el patron lectura/escritura sobre un array, cual es el invariante que sostenes en cada vuelta del bucle?
- Motivo: abierta y sin tildes; pasar a una traza. Absorbe a c0033.
- Frente nuevo: Patrón lectura/escritura sobre [0, 1, 2, 2, 3, 0, 4, 2] quitando val = 2, con read y write desde 0. Cuando read terminó el índice 3, ¿cuánto vale write y qué hay en a[0..write-1]?
- Dorso nuevo: write = 2 y a[0..1] = [0, 1].
  a[0..write-1] es siempre la respuesta construida con lo leído hasta ahí.

### c0023 (arrays-strings)
- Frente actual: En 27, la variante que hace swap con el ultimo elemento: por que NO se avanza i despues del swap?
- Motivo: sin tildes y "por qué"; pasar a qué devuelve el código con el bug. Absorbe a c0021 y c0022.
- Frente nuevo: 27 Remove Element, variante: si a[i] == val, se hace a[i] = a[n-1], n--, y se avanza i; el bucle corre mientras i < n y devuelve n. ¿Qué devuelve con nums = [3, 3] y val = 3?
- Dorso nuevo: 1, y lo correcto es 0: el 3 traído del final queda sin revisar.
  Después del swap no se avanza i.

### c0032 (arrays-strings)
- Frente actual: 680 Valid Palindrome II pide decidir si un string es palíndromo o puede serlo borrando a lo sumo un carácter. Al primer par de extremos que no coincide, ¿por qué no sirve elegir qué lado borrar mirando un solo carácter más adentro?
- Motivo: "por qué" largo; pasar a una traza con el contraejemplo. Absorbe a c0027.
- Frente nuevo: 680 Valid Palindrome II (¿es palíndromo borrando a lo sumo un carácter?) con s = "abcbab". Una solución, al primer par distinto (s[0] = 'a', s[5] = 'b'), borra el izquierdo si s[1] == s[5]. ¿Qué devuelve y qué debería devolver?
- Dorso nuevo: Devuelve false (queda "bcbab"); lo correcto es true, porque borrar la 'b' final deja "abcba".
  Hay que probar los dos borrados.

### c0034 (hash-maps)
- Frente actual: Al leer el enunciado de un problema, ¿qué tres preguntas sobre los datos indican que conviene un hash map?
- Motivo: abierta; pasar a un enunciado concreto.
- Frente nuevo: 219 Contains Duplicate II: ¿existen i != j con nums[i] == nums[j] y |i - j| <= k?, con n <= 10^5. ¿Qué estructura, qué guarda y qué complejidad?
- Dorso nuevo: unordered_map de valor a último índice visto, en una pasada: O(n).
  "¿Ya apareció este valor y dónde?" pide hash map.

### c0038 (hash-maps)
- Frente actual: ¿Por qué unordered_map<vector<int>, T> no compila en C++ y unordered_map<string, T> sí?
- Motivo: pasar a "¿compila?" con contraste útil.
- Frente nuevo: `unordered_map<vector<int>, int> m;` ¿Compila? ¿Y `map<vector<int>, int> m;`?
- Dorso nuevo: El primero no: no existe `std::hash<vector<int>>`.
  El segundo sí: `map` solo necesita `operator<`, y vector lo tiene.

## Retirar

| id | Frente actual (resumido) | Motivo |
|---|---|---|
| c0002 | ¿Cuándo un número del input NO entra en la fórmula de complejidad? | Abierta; el caso útil queda cubierto por c0001 y c0003. |
| c0005 | Tres operaciones de array en JS que parecen O(1) y son O(n) | De JavaScript; ahora estudia C++. |
| c0006 | Tu solución da TLE, ¿primer movimiento? | Consejo abierto, sin respuesta única; cubierto por c0003. |
| c0011 | Diferencia entre map y unordered_map, ¿cuál querés? | Abierta y de bajo valor; c0038 ya contrasta los dos. |
| c0013 | Diferencia entre referencia y puntero | Definición abierta; el uso en entrevista queda en c0009. |
| c0015 | Por qué un unordered_set de 10^5 enteros pesa más de 400 KB | Bajo valor para entrevista de algoritmos. |
| c0016 | Dos familias para detectar duplicados | Bajo valor; el trade-off sale solo al resolver. |
| c0021 | Por qué write arranca en 1 en 26 y en 0 en 27 | Redundante con c0018 y c0023; detalle de un problema. |
| c0022 | Tercer eje de casos borde | Abierta; es hábito de prueba, no un dato para recuperar. |
| c0024 | Cuándo vale la pena una micro-optimización | Consejo abierto, bajo valor. |
| c0026 | Rango cerrado [i, j] contra medio abierto [i, j) | Redundante con c0031. |
| c0027 | 680: por qué no alcanza con contar diferencias | Redundante con c0032. |
| c0030 | Por qué i < j y no i <= j en dos punteros | Bajo valor; respuesta obvia una vez escrita. |
| c0033 | Por qué escribir en a[write] no destruye lo no leído | Redundante con c0018 reescrita. |
| c0035 | ¿Qué es una colisión? | Definición. |
| c0036 | Chaining contra open addressing | Definición y trivia de implementación. |
| c0037 | ¿Qué es el load factor? | Definición; bajo valor. |
| c0039 | 49 Group Anagrams: por qué la clave de conteos no es ambigua | Detalle de un solo problema, bajo valor. |
| c0040 | Peor caso de búsqueda en hash map | Bajo valor para el nivel actual. |

## Totales

- Conservar: 2
- Reescribir: 12 (12 retiradas de la vieja + 12 altas nuevas)
- Retirar: 19
- Mazo activo resultante: 14 de 33
