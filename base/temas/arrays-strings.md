# arrays-strings: Recorridos, in-place e inmutabilidad en JS

Abierto: 2026-09-19

## Modelo mental

El tema parece trivial ("son arreglos, los uso hace años") y no lo es, porque los problemas de
arrays y strings se ganan o se pierden en tres cosas de JavaScript que no son obvias.

**El array se muta, el string no.** En JS los strings son inmutables: `s[0] = "z"` no hace nada, y
toda operación que "modifica" un string construye uno nuevo. La consecuencia que aparece en
entrevista es `out += c` dentro de un bucle: como no puede modificar, copia entero lo acumulado
antes de pegar la letra, y la suma 1+2+...+n da **O(n²)**. El idioma correcto es acumular en un
array y `join("")` al final, O(n). (Matiz: V8 lo optimiza con rope strings y muchas veces no se
nota, pero no es garantía del lenguaje y en entrevista se dice O(n²).)

**Asignar un array no lo copia, copia la referencia.** `const b = a` crea un alias: mutar `b` muta
`a`. La copia superficial real es `[...a]` o `a.slice()`. Importa porque el array de entrada llega
por referencia, y porque `sort()` ordena in-place y muta el original.

**In-place** es resolver modificando el array de entrada, con espacio auxiliar **O(1)**. Lo
implementa el idioma **write/read pointer**: `read` recorre y solo mira, `write` marca la próxima
casilla libre y avanza solo cuando escribió. Funciona porque `write` nunca le gana a `read`, así
que nunca se pisa un dato sin leer. Se reconoce en el enunciado por "in-place", "O(1) extra
memory", "without allocating extra space", y por pedir que se devuelva `k` diciendo que lo que
queda después no importa.

## Subtemas

- [x] Inmutabilidad del string; `+=` en bucle como O(n²) y el reemplazo con `push`/`join`.
- [x] Alias vs shallow copy; `sort()` muta el original.
- [x] In-place y el idioma write/read pointer.
- [x] Reconocer in-place en el enunciado.
- [ ] Recorridos con dos pasadas (prefijo/sufijo). No tocado: es 238 Product of Array Except Self.
- [ ] Inferencia de tipos de TypeScript: cuándo hay que anotar y cuándo no. Salió al pasar.

## Criterio de dominio

Dado un enunciado, dice si es in-place antes de escribir, implementa el write pointer sin
plantilla, y da tiempo y espacio correctos justificando por qué la entrada no cuenta. Y explica
sin ayuda por qué construir un string con `+=` en un bucle es cuadrático.

## Fuentes usadas

- `.claude/skills/codigo/referencias-ts/patrones.md` y `problemas.md` (internas).

## Historial

- 2026-09-19: **tema abierto.** Fondo, intención enseñar, 33 min efectivos (93 de reloj, 60 de
  almuerzo pausado con `sesion pausar`).
  - Bloque teórico en 16 min, dentro del tope.
  - **El write pointer presentado como plantilla con un `meSirve()` de relleno no comunicó.** Dijo
    textual: "no entendí muy bien el ejercicio de write read, está muy abstracto". Se destrabó al
    instante con una traza numérica fila por fila (dejar los pares de `[3,8,5,2,7,4]`).
  - **Confundía anagrama con palíndromo.** Paró el ejemplo resuelto de 242 para preguntarlo, que
    es lo correcto: estaba resolviendo otro problema. Es vocabulario en inglés, no algoritmo.
  - **Ejercicio 27 Remove Element: resuelto solo, cero pistas, aceptado.** Llegó al write pointer
    por su cuenta (lo llamó `counter`). Predijo "con pistas".
  - **El hueco de espacio auxiliar de la mañana quedó cerrado sobre dos casos nuevos.** Primero
    falló otra vez (dijo O(n) para el bloque del write pointer) y se destrabó al pedirle la lista
    de variables que nacen adentro. Después dio O(1) solo, sobre su propio código.
  - Creía que anotar `let counter: number = 0` era obligatorio y que LeetCode se lo permitía por
    ser laxo. Es inferencia estándar de TypeScript. No se registró como error de lenguaje porque
    nada se rompió.
  - **En su explicación final invirtió el reconocimiento de in-place:** dijo que se reconoce porque
    "quieren que no modifiquemos el array que nos mandan". Es al revés. Corregido en el momento y
    convertido en la tarjeta c0012.
  - También dijo "hacer un push en string". Los strings no tienen métodos mutadores.
  - 8 tarjetas generadas (c0009–c0016).
- 2026-09-20: micro de repaso, 2 tarjetas del tema. **c0010 falló (calidad 2) proponiendo `concat`
  como reemplazo de `out += c`**, que cuesta lo mismo; en la repetición llegó a `push` pero sin el
  `.join("")` y con el motivo equivocado. **c0009 en calidad 3**: acertó el valor y no nombró la
  inmutabilidad. Las dos fallas son del mecanismo, no del número. Quedan c0011–c0016 vencidas, y
  **c0012 sigue sin verificarse** desde la inversión del reconocimiento de in-place del 19.
- 2026-09-20 (micro de la tarde): 5 tarjetas del tema. **c0012 cerrada**: dio al derecho el
  reconocimiento de in-place que había invertido el 19. c0015 en calidad 5, c0011 y c0013 en 4.
  **c0014 falló (calidad 1)**: dijo O(n) de espacio para el write pointer, con argumento de tiempo
  ("el read pasa por cada elemento"). En la repetición dio O(1). **c0016 está mal escrita**: él
  detectó que la segunda mitad no se entiende; propuesto partirla en dos, pendiente su decisión.
- 2026-09-21: micro de repaso. c0009 calidad 5 (inmutabilidad de strings, y agregó el contraste
  con el array). c0010 calidad 4: número O(n²) y reemplazo `push` + `join` exactos, pero dijo que
  `+=` "crea uno nuevo" sin decir que **copia entero lo ya acumulado**, que es de dónde sale el
  n². Sexta aparición de "número correcto, mecanismo ausente".
