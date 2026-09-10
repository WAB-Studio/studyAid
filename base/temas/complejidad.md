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
- [x] Espacio auxiliar vs entrada vs salida; el stack de recursión cuenta
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
