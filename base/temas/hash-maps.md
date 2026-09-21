# hash-maps: Comprar tiempo pagando memoria

Abierto: 2026-09-20 (bloque teórico el 2026-09-19 por la tarde)

## Modelo mental

Un **hash map** guarda pares clave → valor y responde "¿está esta clave? ¿qué vale?" en **O(1)
promedio**, sin importar cuántos elementos tenga. En TypeScript es `Map`. `Set` es el mismo
mecanismo sin valores: solo claves.

**Lo que compra siempre es el mismo bucle.** La fuerza bruta de esta familia tiene la forma "para
cada x, recorrer todo buscando algo que cumpla con x". Ese bucle de adentro es una **pregunta de
búsqueda**, y el hash map la responde en O(1). O(n²) → O(n). La señal estructural es exactamente
esa: un bucle interno que solo está ahí para buscar, no para calcular ni acumular.

**Lo que cuesta.** O(n) de espacio auxiliar. No es gratis y no es "estrictamente mejor": la fuerza
bruta gasta O(1). Si el enunciado pide O(1) auxiliar, el hash map queda descartado de entrada, y
cambiarlo por un `Set` no salva nada porque cuesta lo mismo. Lo que queda ahí son variables puras,
u ordenar y pasar a two pointers.

**Las cuatro señales, desde el enunciado y no desde la herramienta**: "¿ya lo vi?" (seen set),
"¿cuántas veces aparece?" (frequency count), "agrupar los que comparten algo" (grouping by key),
"¿existe otro que junto a este dé X?" (complement lookup). Y la condición que las habilita a todas:
**el orden y la posición no importan.** Si el problema depende del orden, el hash map solo no basta.

**Las trampas son de JavaScript, no del patrón.** `get` devuelve `undefined` cuando no hay clave,
no `0`. Preguntar presencia con `if (m.get(k))` rompe cuando el valor guardado es `0` (un índice
válido y falsy): presencia se pregunta con `m.has(k)`. Y `??` da valores por defecto
(`(m.get(k) ?? 0) + 1`), no responde presencia: `0 ?? false` sigue dando `0`.

## Subtemas

- [x] Qué compra un hash map y qué cuesta; el intercambio con los cuatro números sobre la mesa.
- [x] Frequency count con `Map` y `?? 0`.
- [x] Complement lookup (Two Sum), y por qué se consulta antes de guardar.
- [x] Las trampas de JS: `0` falsy, `has` vs `get`, `??` para default y no para presencia.
- [x] Cuándo NO sirve: restricción de O(1) auxiliar, y que un `Set` no la esquiva.
- [ ] Grouping by key. No tocado: es 49 Group Anagrams, con el truco de la clave canónica.
- [ ] Reconocer la señal desde un enunciado que no vio. Es lo que quedó flojo: ver abajo.

## Criterio de dominio

Dado un enunciado nuevo, nombra la señal **en términos del enunciado** (no "necesito un Map") antes
de escribir nada; da los cuatro números del intercambio contra la fuerza bruta; y escribe el
lookup sin caer en el `0` falsy. Y dice qué haría si le prohibieran el espacio extra.

## Fuentes usadas

- `.claude/skills/codigo/referencias-ts/patrones.md`, sección `hashing / frequency-map`.

## Historial

- 2026-09-20: **tema abierto.** Fondo, intención enseñar, partida en dos días (teoría el 19 a las
  17:43, ejercicio el 20 a las 10:53). Bitácora en `bitacora/2026-09-20.md`.
  - Bloque teórico 14 min, con traza numérica del frequency count. **242 Valid Anagram** como
    ejemplo resuelto de punta a punta, incluido el caso que corta en la primera vuelta.
  - **1 Two Sum: solo, cero pistas de algoritmo, Accepted 65/65.** El complement lookup entero fue
    suyo, incluido consultar antes de guardar.
  - Dos bugs, los dos de lenguaje y los dos encontrados por él con un nudge de región:
    **el `0` falsy** en `if (m.get(k))`, y **`i <= nums.length`**. No se acordaba de `has`.
  - **La submission aceptada de las 11:06 todavía tenía el off-by-one.** Lo vio en su propia
    pantalla: el juez no manda casos sin solución porque el enunciado promete que siempre hay una.
    Accepted no significa correcto: fue el momento más útil de la sesión.
  - **Dio las tres cotas correctas y agregó la cuarta sin que se la pidiera**: que la fuerza bruta
    gasta O(1) de espacio. Nombró el intercambio completo solo.
  - **Lo que quedó flojo: la señal.** Las dos veces que se la pedí arrancó por la herramienta
    ("necesito guardar clave-valor") en vez de por el enunciado. Lo que sí tiene es "no necesito
    saber el orden". Va a la tarjeta c0017.
  - **Error de fondo corregido:** propuso un `Set` como alternativa bajo restricción de O(1)
    espacio. Un `Set` cuesta O(n) igual. Tarjeta c0018.
  - Dijo "espacio vectorial" por **espacio auxiliar**. Vocabulario, corregido en el momento.
  - 6 tarjetas generadas (c0017–c0022).
- 2026-09-21: micro de repaso. c0017 calidad 3 (dos de las cuatro preguntas-señal; faltó la del
  par que suma X, la de agrupar y la señal estructural del bucle interno que solo busca).
  c0018 calidad 3: la restricción (O(1) de espacio) exacta, pero el habilitador lo respondió como
  "que se tenga espacio", que es la restricción al revés y no la propiedad estructural (orden y
  posición no importan). c0019 calidad 5 (el `0` falsy y `m.has`). En las dos de calidad 3 se
  declaró inseguro y acertó lo central: subestimación.
