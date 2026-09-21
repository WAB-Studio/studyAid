# sliding-window: Ventana deslizante

Abierto: 2026-09-21

## Modelo mental

Una ventana deslizante sirve cuando la respuesta vive en un **tramo contiguo** de la entrada y
lo que hay que calcular sobre ese tramo se puede actualizar al mover la ventana, en vez de
recalcularse desde cero. Eso es lo que baja el costo de n por k a n.

Hay dos variantes y cada una tiene su propia condición para ser correcta, que no es la misma.

**Ventana fija.** El tamaño viene dado. El puntero izquierdo avanza siempre, un paso por vuelta,
sin condiciones. La condición acá es sobre **la operación**: tiene que ser reversible. La suma se
deshace restando el que sale, el conteo también, el producto también mientras no haya ceros. El
máximo, el mínimo y la mediana no: cuando el máximo sale de la ventana no hay ninguna cuenta que
devuelva el máximo de lo que quedó, porque esa información se perdió al quedarse solo con el
máximo. Por eso el máximo de ventana móvil (LeetCode 239) no se resuelve con este esquema sino
con una deque monótona, que guarda todos los candidatos que todavía podrían ganar y descarta a
los que ya no, y llega a O(n) por argumento amortizado: cada elemento entra y sale una sola vez.

**Ventana variable.** El tamaño no viene dado. El puntero derecho crece y el izquierdo avanza
cuando la ventana deja de cumplir la condición, y **nunca retrocede**. Ese "nunca retrocede" es
una decisión irreversible: está afirmando que ninguna respuesta que empiece en ese índice sirve.
Solo es válido si **la validez es monótona**, o sea si una ventana inválida no puede volverse
válida al crecer. En "subcadena sin repetidos" se cumple, porque agregar letras nunca borra una
repetición que ya estaba. En "suma ≤ K" se cumple si todos los números son positivos, porque
agregar solo sube la suma. Con números negativos **no se cumple y el algoritmo da mal**: con K=3
sobre `[1, 5, -4, 2]` la respuesta es 3, pero al pasarse en `[1, 5]` descarta el índice 0 y pierde
`[1, 5, -4]`, que suma 2. Ahí hace falta prefix sums, no una ventana.

Es la misma idea que en `two-pointers`: la monotonía es lo que compra el derecho a no retroceder,
y sin ella el O(n) no es lento, es incorrecto.

## Subtemas
- [x] Condición de corrección de la ventana variable (monotonía de la validez)
- [x] Condición de la ventana fija (operación reversible)
- [x] Contraejemplo con negativos
- [ ] Implementar una ventana variable de punta a punta en TypeScript
- [ ] 121 Best Time to Buy and Sell Stock
- [ ] Reconocer el patrón en un enunciado sin etiqueta
- [ ] Deque monótona y 239 Sliding Window Maximum (CPH §8.3)

## Criterio de dominio

Dado un enunciado sin etiqueta, tiene que poder decir si sliding-window aplica y **por qué es
correcto**, no solo por qué es rápido. En concreto: nombrar qué propiedad del problema hace que
el puntero izquierdo pueda no retroceder, y dar un caso donde esa propiedad se rompa. Y resolver
un problema de ventana variable en TypeScript sin pistas, con la complejidad justificada.

## Fuentes usadas
- Sliding Window in 7 minutes, LeetCode Pattern. Visto completo el 2026-09-21, 8 min.
  https://www.youtube.com/watch?v=y2d0VHdvfdc
- Competitive Programmer's Handbook, Laaksonen, cap. 8 "Amortized analysis". §8.1 two pointers,
  §8.3 sliding window minimum. En `fuentes/competitive-programmers-handbook-laaksonen.pdf`.

## Historial

- 2026-09-21: tema abierto en sesión de fondo, intención enseñar. Se cubrió el modelo mental
  entero (las dos variantes y las dos condiciones) con el contraejemplo de los negativos.
  No se hizo ejercicio: la sesión se llevó una parte grande en cambios de metodología que él
  pidió. Falló la transferencia entre dominios: se le preguntó por "suma ≤ K" y contestó con el
  problema del string, sin ver que era la misma propiedad. Salió bien, y por primera vez en siete
  sesiones, que dio el mecanismo sin que se lo pidieran, y que detectó solo el n al cuadrado de
  su propia propuesta del segundo máximo. Pendiente: 121, que sigue sin gastarse, y las tarjetas
  del tema, que todavía no se generaron.
