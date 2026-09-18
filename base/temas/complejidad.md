# complejidad — Notación Big-O de tiempo y espacio

Abierto: 2026-09-10

## Modelo mental

Big-O no mide segundos: mide **cómo crece el trabajo cuando crece la entrada**. Es una
herramienta de decisión, no de reporte. Sirve para dos cosas concretas en una entrevista:
descartar enfoques antes de escribirlos, y leer las restricciones del enunciado (`n <= 10^5`,
"en O(log n)", "sin división") como una pista de qué familia de solución se espera.

Se reconoce en el enunciado por las cotas de `n` y por cualquier orden pedido explícitamente.
Se calcula leyendo la estructura del código: secuencias se suman y domina la mayor, bucles
anidados sobre el mismo `n` se multiplican, partir a la mitad da `log n`, y en recursión es
(nodos del árbol de llamadas) × (trabajo por nodo).

El espacio se cuenta aparte del tiempo, y se separa el **auxiliar** (lo que uno aloca) de la
entrada y de la salida. El stack de recursión cuenta como espacio auxiliar. En C++ hay dos
costos que no se ven en el código: pasar un contenedor por valor lo copia (O(n)), y los
contenedores basados en nodos pesan del orden de 8 a 10 veces sus datos crudos.

## Subtemas
- [x] Leer la complejidad de un bloque de código (secuencia, anidado, mitades)
- [ ] Complejidad de recursión: nodos × trabajo por nodo
- [ ] Espacio auxiliar vs entrada vs salida; el stack de recursión cuenta — la separación
      sí está; **el stack de recursión no**: `c0004` falló el 09-18 y al ver el dorso dijo
      que no lo entendía. Reabierto.
- [x] Costos reales de las operaciones (visto en JS el 2026-09-10; rehecho en C++: copia de
      contenedores, `unordered_map` vs `map`, `insert` al frente de un `vector`)
- [ ] Amortizado: por qué `push` es O(1)
- [x] De la restricción al orden: tabla de `n` → complejidad tolerable
- [ ] Usar la restricción para podar enfoques antes de escribir código — enseñado, una sola rep

## Criterio de dominio

Dado un fragmento de código de 10–15 líneas, dice tiempo y espacio correctos y justifica
por qué en una oración. Dado un enunciado con su cota de `n`, nombra el orden objetivo y
descarta al menos un enfoque por ser demasiado lento, sin escribir código.

## Fuentes usadas
- `.claude/skills/codigo/referencias-cpp/big-o.md`
- `.claude/skills/codigo/docs/constraints-to-complexity.md`

## Historial

- 2026-09-10: tema abierto y cubierto en lo esencial (explicó con sus palabras + resolvió 1 Two
  Sum declarando los costos antes de codear). Bien: leer el orden desde la estructura del código,
  detectar bucles escondidos en la stdlib (`includes`), separar espacio auxiliar de entrada y
  salida. Falló: tratar `k` como constante cuando viene en el input — calculó `O(n·k)` y lo tiró
  a `O(n)`. Pendiente: recursión (nodos × trabajo por nodo) y amortizado, ninguno de los dos se
  tocó. La lectura restricción → orden tiene una sola repetición: hay que ejercitarla dentro de
  los problemas de los temas que siguen, no como tema aparte.

- 2026-09-18 (micro): `c0004` (espacio auxiliar de una recursiva que no aloca) salió **calidad 1**,
  respondió `O(1)` y dijo que se la sabía. Al ver el dorso: "no entiendo". No es olvido, es un
  concepto que nunca estuvo: no cuenta los marcos de llamada como memoria porque no los declaró
  él. Se le dio una sola línea en el momento (cada llamada pendiente ocupa un marco; `n` niveles
  = `n` marcos vivos = `O(n)`) y la re-pregunta al final de la sesión salió correcta, pero eso
  mide repetición a diez minutos. **Pendiente para la próxima de fondo**: entra por el bloque
  teórico, con un árbol de llamadas dibujado, no como repaso de tarjeta. Encadena natural con el
  subtema de recursión (nodos × trabajo por nodo), que también sigue abierto desde el 09-10.

- 2026-09-18 (micro de mediodía, solo tarjetas): `c0001` (bucle anidado sobre las 26 letras)
  calidad 5 e instantáneo; `c0003` (`n <= 10^5` → la complejidad más lenta que entra) calidad 4,
  dio los 10^8 del juez y `n log n` sin hacer explícita la cuenta que descarta `n²`.
  La lectura restricción → orden ya tiene tres repeticiones y sale sola. Lo que sigue pendiente
  es lo de siempre desde el 09-10: recursión (nodos × trabajo por nodo, más la pila como espacio
  auxiliar) y amortizado.
