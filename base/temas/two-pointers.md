# two-pointers: Dos índices que se cruzan

Abierto: 2026-09-20 (tocado en frío por la línea base el 2026-09-15, sin enseñarse)

## Modelo mental

**Two pointers** es recorrer con dos índices que se mueven el uno hacia el otro en lugar de con un
bucle anidado. Cada movimiento **descarta un elemento con todos sus socios posibles**, no un par.
Por eso n pasos cubren n² combinaciones.

**La condición que lo hace válido es la monotonía**, no que la respuesta sea un par. Que la
respuesta sea un par es apenas el primer filtro: la fuerza bruta también mira pares. Lo que hace
falta es que **mover un puntero empuje el resultado en una sola dirección predecible**, porque eso
es lo que permite probar los dos movimientos y demostrar que uno es imposible que sirva.

**La monotonía tiene dos fuentes distintas, y confundirlas bloquea.**

1. **El arreglo está ordenado.** `lo++` solo puede caer en un número igual o mayor → la suma solo
   sube. `hi--` solo puede caer en uno igual o menor → la suma solo baja. Cada puntero es una
   perilla de una sola dirección. Caso: 167 Two Sum II.
2. **Una cantidad que solo se achica.** En 11 Container With Most Water el arreglo **no** está
   ordenado y el patrón sirve igual, porque el **ancho** baja de a 1 en cada vuelta y nunca vuelve.
   El invariante ahí es que el área está topeada por `min(izq, der)`: mientras la pared baja siga
   en su lugar el alto no puede mejorar y el ancho solo empeora, así que mover la pared alta nunca
   puede superar el área ya medida. Se mueve **siempre la pared más baja**.

**El costo**: O(n) tiempo, **O(1) espacio auxiliar**. Es la alternativa al hash map cuando el
enunciado prohíbe memoria extra ("constant extra space"), a cambio de exigir orden o monotonía.

**Por qué es O(n), que hay que saber demostrarlo**: un `while (lo < hi)` no declara su cantidad de
vueltas. La prueba es que `hi - lo` arranca en `n-1`, baja exactamente 1 por vuelta y termina en 0
: un `for` disfrazado. Se cae si algún puntero puede volver atrás.

**Ordenar como paso previo** tiene dos trampas: si los índices son parte de la respuesta, ordenar
destruye el problema (11); y si se puede ordenar, el `.sort()` impone un piso de O(n log n) y la
solución ya no es O(n).

## Subtemas

- [x] Extremos opuestos sobre arreglo ordenado (167 Two Sum II).
- [x] Deducir qué puntero mover probando los dos movimientos, en vez de memorizar la regla.
- [x] Monotonía por ancho decreciente, sin orden (11 Container With Most Water).
- [x] La demostración de O(n) por la distancia `hi - lo`.
- [x] Por qué ordenar no siempre se puede ni conviene.
- [ ] Mismo sentido / deduplicar in-place. No tocado.
- [ ] Rápido/lento. Vive en `linked-lists`, sin abrir.
- [ ] 125 Valid Palindrome y 15 3Sum (reservado para la línea base B). 42 sin tocar.

## Criterio de dominio

Ante un enunciado nuevo, dice si hay monotonía **y de dónde sale** antes de escribir; deduce qué
puntero mover probando los dos movimientos; demuestra el O(n) con la distancia entre punteros; y
detecta cuándo ordenar destruye el problema o le pone un piso de O(n log n).

## Fuentes usadas

- `.claude/skills/codigo/referencias-ts/patrones.md`, sección `two-pointers`.
- **Competitive Programmer's Handbook**, Antti Laaksonen, cap. 8 §8.1 (pág. 77), en
  `fuentes/competitive-programmers-handbook-laaksonen.pdf`. Consultado el 2026-09-21. Relevante
  porque **mete two pointers dentro del capítulo de análisis amortizado**, no dentro de "trucos
  de arrays": el argumento de por qué es O(n) es el contenido del tema, no un apéndice. Su frase
  de una línea: "Both pointers can move to one direction only, which ensures that the algorithm
  works efficiently": es la misma demostración de la distancia `hi - lo` que el 2026-09-20 no
  entendió hasta ver la traza numérica. El §8.3, sliding window minimum, cae justo sobre el
  próximo tema del temario.

## Historial

- 2026-09-15: A2 de la línea base. Resolvió 11 solo, sin pistas, en ~20 min, en TypeScript.
  O(n²) correcta, TLE 57/65. La solución de dos punteros no apareció ni como intuición.
  Registrado con `--resultado solo` porque no recibió ayuda; el TLE es resultado algorítmico,
  no fallo de ejecución.
- 2026-09-20: **tema abierto.** Fondo, intención enseñar. Bitácora en `bitacora/2026-09-20.md`.
  - **11 Container With Most Water: Accepted 65/65, 1 ms.** Cierra el TLE del 2026-09-15 sobre el
    mismo problema. Predijo "con pistas" y fue con pistas: calibración acertada.
  - Bloque teórico con traza numérica sobre `[1,3,4,6,8,11]`, target 10, y la regla de movimiento
    **deducida probando los dos movimientos** en vez de enunciada.
  - **Error mío que lo bloqueó:** dije "el orden es lo que fabrica la monotonía" como si fuera la
    única fuente. Aplicó bien esa regla y concluyó que en 11 había que ordenar, y después que dos
    punteros no servía. La regla completa está en `patrones.md`: ordenado **o** factibilidad
    monótona. Corregido en sesión.
  - **Quiso ordenar el arreglo en 11.** Lo descartó él mismo con una observación sobre la entrada:
    los índices son parte del dato y ordenar destruye las distancias.
  - **Calculó el área como `8 × 7` en vez de `min × ancho`.** Le dio 49 igual porque las dos
    cantidades valían 7 por casualidad. Cuarta aparición de "número correcto, mecanismo equivocado".
  - **Escribió `lo++` incondicional:** calculaba correctamente cuál era la pared baja y no usaba
    esa información para mover. Encontrado por él con un nudge de región. Después `hi++` por
    `hi--`, también corregido por él.
  - **Pidió simplificar el código y esta vez tenía razón**: la comparación estaba escrita dos
    veces. Contraste con el 2026-09-16, donde descartó una solución correcta por una peor.
  - **No entendió la demostración de O(n)** hasta ver la columna `hi - lo` bajando 8,7,6,...,0.
    Quinta confirmación de que la traza numérica comunica y el argumento verbal no.
  - **Su explicación final se quedó en "la respuesta es un par"** y no nombró la monotonía, que era
    justo lo que acababa de trabajar. Además dijo que los bucles anidados "limitan por espacio":
    es al revés, gastan O(1) y lo que pagan es tiempo.
  - 7 tarjetas generadas (c0023–c0029).
- 2026-09-21: micro de repaso. Cayó solo c0023 y **quedó en blanco por el frente, no por el
  contenido**: dijo dos veces que no entendía la pregunta, y al repreguntarla reformulada sostuvo
  que la tarjeta está mal hecha. Segunda tarjeta que él detecta mal escrita, después de c0016.
  Editada ese mismo día con su aprobación, no retirada: lo que hay que recuperar no cambia, así
  que conserva el ease de 1.7. El frente nuevo pide el mecanismo del movimiento y ya no admite
  "monotonía" como respuesta de una palabra. Pidió material externo sobre el tema: se indexó y
  descargó el CPH (ver Fuentes).
