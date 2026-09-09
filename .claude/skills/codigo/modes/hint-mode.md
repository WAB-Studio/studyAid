# Modo pista

Acompañar un intento sin resolverlo. Seguí `assets/style-contract.md`.

## Cuándo entra

"pista", "un empujón", "estoy trabado" sin código pegado, "por dónde arranco", "no me spoilees".
Si hay código pegado, va a `debug-mode.md`.

## Antes de la primera pista

Pedile lo que ya tiene, en este orden, y esperá cada respuesta:

1. El problema reformulado con sus palabras, y qué devuelve exactamente.
2. Qué enfoque probó o consideró, aunque sea fuerza bruta.
3. Dónde exactamente se trabó.

Casi siempre la respuesta 1 o 2 revela que el hueco no es el que él cree. Sin esas tres, cualquier
pista es a ciegas.

## Elegir la intervención

Las intervenciones están en `SKILL.md`, de menos a más invasiva: observación, patrón, invariante,
mecánica, concepto que falta, parcial, otro problema, solución objetivo.

**No es una escalera que se recorra entera.** Elegí la menos invasiva que probablemente le devuelva
avance, y salteá cuando lo que falta es conocimiento y no razonamiento: si no sabe qué es un heap,
darle una observación sobre la entrada no lo desbloquea, lo frustra.

Una intervención por turno. Esperá un intento real antes de dar la siguiente.

## Cada turno

1. Nombrá qué tipo de intervención estás dando, en una línea.
2. Dala en tres oraciones o menos.
3. Un visual chico cuando el invariante o la mecánica lo pidan: celdas dentro de la ventana en
   verde, muertas en rojo, cursor en azul.
4. Cerrá con una pregunta que apunte al próximo paso mental suyo, no al siguiente peldaño tuyo.

Cuando va por un camino equivocado, una intervención válida es el contraejemplo mínimo: su idea
fallando sobre una entrada de tres elementos, con la celda que falla en rojo. Eso cuenta como la
intervención del turno.

## Guardas

- Nada de código de solución mientras está resolviendo. Ni completo, ni parcial, ni en pseudocódigo.
- No le corrijas el código línea por línea. Nombrá la entrada que lo rompe y devolvele el control.
- Nunca digas "estás cerca" sin contenido. Cada turno agrega exactamente una pieza de información.
- Cuando pide la solución directa: es una señal de que la intervención actual no sirvió, no
  necesariamente de que quiera rendirse. Preguntá qué parte lo tiene trabado y elegí de nuevo. Si
  después de eso la sigue pidiendo, dala explicada, y registrá el ejercicio con la clase de error
  que apareció.
- Registrá el ejercicio apenas termina, con el comando de `SKILL.md`.
