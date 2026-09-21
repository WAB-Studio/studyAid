# complejidad: Análisis de costo en tiempo y espacio

Abierto: 2026-09-16

## Modelo mental

La complejidad no es una etiqueta que se busca al final: es una cuenta que se hace **antes de
escribir código**. El enunciado dice hasta cuánto llega `n` (las *constraints*); tu idea tiene una
forma de crecer; comparar las dos cosas decide si escribes esa solución o sigues pensando. Ese
paso es el que faltó en A2 de la línea base, donde el TLE 57/65 era calculable en treinta segundos
sin correr nada.

Big-O describe **cómo crece** el costo cuando `n` crece, no cuántas operaciones son. Por eso se
descartan el factor constante y los términos menores: a partir de cierto `n` no cambian nada.
Formalmente, `f(n)` es `O(g(n))` si existen `c > 0` y `n₀` tales que `f(n) ≤ c·g(n)` para todo
`n ≥ n₀`: el `c` se traga las constantes y el `n₀` vuelve irrelevantes los términos menores.
Consecuencia práctica: media matriz de pares sigue siendo cuadrática, y optimizar el factor 2 no
saca a nadie de un TLE.

El espacio se cuenta igual, separando entrada (no cuenta), **auxiliar** (lo que crea tu función: 
esto es lo que se reporta) y salida. Como tiempo y espacio se pagan uno con otro, no existe "la
solución óptima" a secas: existe cuál de los dos recursos aprieta. La pila de recursión cuenta
como espacio aunque no se declare ninguna estructura.

## Subtemas

- [x] Orden de crecimiento: contar el costo y ver qué le pasa al doblar `n`.
- [x] Descartar constantes y términos menores; término dominante en código secuencial.
- [x] Vocabulario canónico: constante, logarítmica, lineal, linearítmica, cuadrática, cúbica,
      exponencial, factorial.
- [x] Usar las constraints para descartar una idea antes de escribirla.
- [ ] **Complejidad espacial: reabierto el 2026-09-19.** Enseñado, pero no lo aplica a un caso
      concreto. Ver Historial.
- [x] **`log n`**: cerrado el 2026-09-19 al cuarto intento. Ver Historial.
- [x] Costos de las operaciones de TypeScript (`shift()`, `slice`, `splice`, `Map` vs objeto plano),
      y bucles hermanos vs anidados. Cerrado en la micro del 2026-09-16.
- [x] Complejidad de recursión: nodos del árbol de llamadas × trabajo por nodo. Cerrado el 2026-09-16.
- [x] Análisis amortizado (`push`, union-find), y amortizado vs promedio. Cerrado el 2026-09-16.
- [ ] Un parámetro de la entrada (`k`, `m`, `amount`) no es una constante.

## Criterio de dominio

Dado un enunciado con sus constraints y una idea suya, dice la complejidad temporal y espacial
de esa idea y si entra o no, **antes** de escribir código, y sin que se lo pregunten. Y dada una
función de 10 líneas con bucles anidados, un `sort()` y una recursión, da el orden correcto
justificando cuál es el término dominante.

## Fuentes usadas

- `.claude/skills/codigo/referencias-ts/big-o.md` (interna).
- Video, indexados en `base/fuentes.md` el 2026-09-17 a pedido suyo: Abdul Bari 1.5.1/1.5.2
  (análisis de bucles, de donde sale el `log n` del bucle que multiplica), el short de por qué
  binary search es `log n`, y el Big-O de NeetCode para consolidar con vocabulario de entrevista.
  Él ya había visto por su cuenta 1.11 Best/Worst/Average Case (18 min), que no toca el hueco.

## Historial

- 2026-09-16: **tema abierto.** Fondo, intención enseñar. Bloque teórico de 26 min: 
  me pasé del tope de 15.
  - **Trabó dos veces con las fórmulas.** `n(n-1)/2 → O(n²)` no se entendió, ni el álgebra de
    descartar términos. Se destrabó al pasar a contar casillas de una matriz de pares y preguntar
    "¿qué pasa si `n` se dobla?". Respondió bien (100 → 10.000, 200 → 40.000).
  - **Pidió explícitamente el vocabulario real.** "Fila" y "tablero" le sonaron raros: quiere los
    términos que va a oír en una entrevista, no analogías. Se le dio la tabla de traducción y los
    nombres canónicos. Ver `base/perfil.md`, entrada del 2026-09-16.
  - **`log n` sigue flojo.** Primero dijo "es cuando vamos a hacer el orden de nuestro bucle";
    después de la explicación con el árbol de merge sort dijo "partimos para ordenar, de esta
    manera sacamos pares". Sigue sin ser "cuántas veces parto `n` a la mitad". Tarjeta c0001.
  - **No sabía qué era un TLE.** Se explicaron los veredictos de LeetCode.
  - Su explicación con palabras propias cubrió bien el protocolo de constraints y el término
    dominante ("la función siempre tendrá la complejidad más alta"). Falló solo en `n log n`.
  - **Ejercicio 217 Contains Duplicate, resuelto solo, sin pistas.** Usado como vehículo: el tema
    no tiene problemas propios. Ejecutó el protocolo de tres pasos explícito y **fue directo a la
    solución O(n) con `Set`, sin escribir la fuerza bruta.** Contraste con A2, donde nunca percibió
    que existiera algo mejor. Un caso, no una tendencia.
  - Predijo "con pistas" ("por si acaso") y lo sacó solo: segundo sesgo a la baja consecutivo.
  - **`api-set-map`:** no sabía construir un `Set` ni un `Map` en TypeScript. Registrado como error
    de lenguaje, no de algoritmo. Él lo confirmó antes de registrarlo.
  - El espacio se enseñó recién al final, después de que él señalara (con razón) que nunca se lo
    había explicado. Quedó cubierto pero sin ejercitar.
  - 8 tarjetas generadas (c0001–c0008).
- 2026-09-16 (micro, 47 min, segunda del día): **costos de las operaciones de TypeScript cerrados.**
  `shift`/`unshift` O(n) por reindexado, `slice`/`splice`/`concat`, `includes` dentro de un bucle,
  y la cola de BFS con índice de cabeza en vez de `shift()`.
  - Se cubrió además **bucles hermanos vs anidados** (suman contra multiplican), a pedido suyo.
    Buena pregunta, no estaba en el plan.
  - **Hueco real encontrado: creía que `set.has()` recorre el array.** Enseñada la tabla hash. Es
    la razón por la que dudaba de su propia solución O(n). Tampoco sabía que un `Set` no admite
    duplicados, ni distinguía deduplicar de detectar duplicados.
  - Ejercicio propio (`custom-repetidos`, reescribir en O(n) una función con `slice` + `includes`):
    con 4 pistas. Encontró él mismo el bug de la estructura leída y nunca escrita, con un caso que
    falla. Versión final verificada: 200.000 elementos en 21 ms.
  - Predicción "con pistas" acertada; corta la racha de dos subestimaciones.
  - `api-set-map` por segunda vez en el día.
- 2026-09-16 (micro, tercera del día, 20:15): **recursión y amortizado cerrados.** `fib` ingenuo
  contra memoizado como trace; `push` amortizado con la tabla de duplicación de capacidad; y la
  distinción amortizado (garantía sobre la secuencia) vs promedio (depende del hash).
  - **Patrón del día:** tiene las piezas correctas y falla al combinarlas. Ante ramificación 3 con
    O(n) de trabajo por nodo dio `O(n²)`: los nodos los tenía (`3ⁿ`) y el trabajo por nodo también
    (O(n)), pero no los multiplicó. Pedirle la multiplicación explícita, no solo las partes.
  - En el check de amortizado estimó 500 pushes caros de 1.000; son ~10. La intuición cualitativa
    estaba, la magnitud no.
  - Sin ejercicio ni tarjetas a propósito: c0001–c0008 vencen el 17 y tocarlas rompía el espaciado.
- 2026-09-17 (micro, 17 min): **primer repaso espaciado de c0001–c0008.** Cuatro falladas en el
  primer pase (c0003, c0004, c0006, c0007); las tres repetidas al final salieron correctas, así
  que el material está y lo que falta es el primer pase de recuperación.
  - **`log n`, tercera vez con la misma desviación.** "Parte en varios pares hasta saber cuántos
    pares salen de n": cuenta las partes que salen, no las veces que partió. Al reabrirlo, atacar
    directamente esa confusión (número de partidas vs número de partes) y no repetir el árbol de
    merge sort, que ya se probó dos veces y produce esta misma respuesta.
  - **Trade-off tiempo/espacio: concepto sí, disparador no.** Lo respondió en c0006 (que pregunta
    qué memoria se cuenta) y dijo "no sé" en c0008, que es exactamente el trade-off. No hace falta
    reenseñarlo; hace falta que la pregunta lo evoque.
  - Pila de recursión como espacio (c0007) → "O(1)". Se corrigió en la repetición.
  - `.sort()` como piso O(n log n) (c0003) → dijo O(n). Se corrigió en la repetición.
  - Sin ejercicio: la micro fue sólo repaso.
- 2026-09-19 (micro, 21 min): **segundo pase de c0001–c0008.** Cuatro en calidad 4, una en 3,
  dos falladas.
  - **`log n` cerrado.** "Las veces que partimos n"; n=8 → 3, al instante. Lo que funcionó fue
    pedir el número concreto, después de que el árbol de merge sort fallara dos veces. Confirma
    lo del 2026-09-16: el mecanismo se simplifica con casos contados, no con álgebra.
  - **Espacio auxiliar: reabierto.** c0006 en calidad 1, y la repetición mostró por qué. Ante un
    array de 10⁶ con solo `i` y `j` respondió *"O(n), porque ese millón es de entrada que no
    cuenta"*: el motivo correcto y el número equivocado en la misma oración; es O(1). Sabe la
    regla y no la aplica a un caso. Tercera aparición de la forma "tiene las piezas y no las
    combina" (2026-09-16: ramificación 3 × O(n) por nodo → dijo O(n²)).
    **Cómo reabrirlo:** no redefinir auxiliar vs entrada, que lo recita. Darle funciones cortas y
    pedir el orden espacial de cada una.
  - **c0008: el problema es el frente, no el contenido.** Segunda sesión seguida igual: dijo "no
    me la sé" y con la pista "el Set te baja el tiempo, ¿qué te sube?" produjo el trade-off
    completo. **Propuesta pendiente de su decisión:** reescribir el frente de c0008 en esa forma,
    o retirarla y reemplazarla. No decidido.
  - c0007 (pila de recursión) pasó de O(1) el 17 a O(n) hoy, sin nombrar los frames. Calidad 3.
  - Calibración: tres sobreconfianzas seguidas (c0006–c0008), primera vez que el sesgo va hacia
    arriba; el registro previo era todo a la baja.
- 2026-09-20: micro de repaso. c0003 y c0004 en calidad 5; **c0006 en calidad 4, viniendo de
  calidad 1 el 2026-09-19**: el espacio auxiliar salió completo y al instante. Quedan c0007 y
  c0008 sin tocar en esta ronda.
- 2026-09-20 (micro de la tarde): **c0007 en calidad 3, tercera vez con el mismo hueco**: da O(n)
  correcto y nunca nombra la pila de llamadas ni los frames. Propuesto reescribir el frente para
  que pida el mecanismo y no el número. Y el hallazgo transversal del día: aplica "¿depende de n?"
  cuando el enunciado le **da** el tope (c0015, calidad 5) y no lo dispara cuando tiene que
  **notarlo** él (c0014, calidad 1). El criterio está; el disparador, no.
- 2026-09-21: micro de repaso. c0006 calidad 4 (dijo que la salida "no se cuenta"; se reporta
  aparte si es grande), c0008 calidad 5 (nombró el trade-off tiempo/espacio sin que se lo
  pidieran). c0030, el reemplazo de c0007 que pide el mecanismo de la pila, no llegó a caer.
