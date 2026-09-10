# arrays-strings — Recorridos, in-place y contenedores de C++

Abierto: 2026-09-10

## Modelo mental

Casi todo problema de entrevista entra por un array. Lo que decide si el código sale limpio no
es el algoritmo sino tres preguntas mecánicas: **¿esto copia o trabaja sobre el original?**,
**¿cuánto cuesta?**, y **¿qué me devuelve realmente?**.

En C++ la primera tiene una respuesta que sorprende viniendo de JS: **por defecto todo se
copia**. Un `vector` *es* los datos, no una flecha hacia los datos, así que pasarlo a una
función lo duplica entero — O(n) de tiempo y de espacio antes de la primera línea. El `&` en el
parámetro es lo que dice "trabajá sobre el original". La regla operativa es corta: `const T&`
para leer, `T&` para modificar, por valor casi nunca.

La segunda mitad del tema es el trabajo **in-place**: modificar la entrada en vez de construir
una salida nueva, para bajar el espacio auxiliar de O(n) a O(1). El patrón base es un puntero de
escritura que avanza más lento que el de lectura. Al revés que en JS, en C++ los `string` son
mutables (`s[0] = 'H'` es legal), así que los problemas de strings in-place son genuinamente
O(1) de espacio.

Se reconoce en el enunciado por frases como "in-place", "sin usar espacio extra", "modificar el
array de entrada" y "el orden de los elementos restantes puede cambiar".

## Subtemas
- [x] Semántica de valor: `T` vs `T&` vs `const T&`, y por qué pasar por valor cuesta O(n)
- [x] `unordered_set` / `unordered_map`: API, `count` vs `[]`, y por qué `[]` inserta al leer
- [x] `map` vs `unordered_map`: árbol O(log n) contra tabla hash O(1)
- [x] Costo real en memoria de un contenedor basado en nodos (8–10x los datos crudos)
- [x] Patrón de dos punteros lectura/escritura para in-place
- [ ] Strings mutables: `s[i] = c`, y por qué eso no se podía en JS
- [ ] `size()` sin signo y las restas que se desbordan
- [ ] Rangos medio abiertos: `[begin, end)` y por qué `end()` va después del último

## Criterio de dominio

Dada una firma de función, dice si copia o no y cuánto cuesta. Elige entre `vector`,
`unordered_set` y `unordered_map` justificando por lo que necesita guardar, no por costumbre.
Resuelve un problema in-place declarando el invariante del puntero de escritura y justificando
el espacio O(1).

## Fuentes usadas
- `.claude/skills/codigo/referencias-cpp/patrones.md` (trampas de C++)
- `.claude/skills/codigo/referencias-cpp/big-o.md`

## Historial

- 2026-09-10: tema abierto. Arrancó en TypeScript (mutan vs copian, `sort` devolviendo la misma
  referencia, `const` que no impide mutar) y **cambió a C++ a mitad de sesión**. Rehecho el tema
  con semántica de valor. Ejercicio **217 Contains Duplicate: Accepted, solo, 0 pistas**, con
  `unordered_set`. Después del Accepted se cubrió por qué el set pesa 8–10x los datos, `reserve()`,
  y la segunda familia válida (ordenar + comparar adyacentes) con el trade-off explícito.
  Bien: eligió el contenedor por lo que necesitaba guardar y declaró ambos costos antes de codear.
  Falló: errores de entorno de C++ (`#include`, `using namespace std;`, la clase adentro de
  `main()`) y un set nombrado `lookup` consultado como `s`. Pendiente: todo el bloque in-place,
  que es la mitad del tema y no se tocó.
- 2026-09-10 (micro, drill): sin ejercicio de este tema. En el drill de reconocimiento apareció
  que la lectura del enunciado sigue siendo el cuello de botella: invirtió el predicado en 1207
  (pidió "todas distintas", resolvió "todas iguales"). Las restricciones sí las leyó y las evaluó.
  El bloque in-place —dos punteros lectura/escritura, strings mutables, `size()` sin signo,
  rangos medio abiertos— sigue sin tocar. Es lo que falta para cerrar el tema.
- 2026-09-10 (fondo, in-place): abierto el bloque que faltaba. Ejemplo resuelto de punta a punta
  de **26 Remove Duplicates** en C++ (invariante `a[0..write-1]`, `write=1`, guarda de vacío,
  cast de `size()`), y después **27 Remove Element: Accepted, solo, 0 pistas** — predijo "con
  pistas". Razonó solo por qué acá `write` arranca en 0 y por qué no necesita la guarda `empty()`.
  Leyó las restricciones y notó que `val` puede no estar en ningún elemento. Se cubrió la segunda
  familia (swap con el último, trade-off n−k contra k escrituras, trampa del `i` que no avanza),
  a la que llegó él después de descartar ordenar por cara.
  Bien: la analogía del array nuevo viviendo encima del viejo la construyó solo; justificó la
  ausencia de la guarda por la razón correcta.
  Falló: casos borde solo por tamaño y por rango de valores, nunca por el extremo del resultado
  (todos `val` / ninguno `val`). No conocía la palabra "invariante" pese a estar usándolo.
  Confundió "una pasada" (tiempo) con "memoria constante" (espacio) como señal del patrón.
  Pendiente: strings mutables, `size()` sin signo, rangos medio abiertos. Es lo único que queda
  para cerrar el tema.
- 2026-09-10 (micro, 283 Move Zeroes): **Accepted, con pistas (máx 2)**, `error-clase: operador-js`.
  Reusó el swap-con-el-último del 27 sin releer que 283 exige preservar el orden relativo.
  Con el trace de `[1,0,2,3]` llegó solo a la reformulación correcta: mover los no-ceros al
  principio, no los ceros al final. Segunda versión limpia al primer intento, con loop de relleno.
  Bien: aplicó los tres ejes de casos borde por su cuenta, incluido el del extremo del resultado.
  Falló: invariante declarado demasiado débil (sin "exactamente" ni "en su orden original"), que
  es precisamente lo que su primera versión violaba.

