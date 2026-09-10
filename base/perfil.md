# Perfil

Actualizado: 2026-09-10

## Datos fijos

- Experiencia: 1–3 años escribiendo software profesionalmente.
- Stack profesional: TypeScript/JavaScript. **Los ejercicios se resuelven en C++** desde el
  2026-09-10, por decisión suya: quiere entender el manejo de memoria, no solo pasar entrevistas.
- Objetivo: big tech, horizonte 6–12 meses.
- Disponibilidad: trabaja full time. 3–4 sesiones de fondo por semana, de noche.
  Micro-sesiones en ratos muertos durante el día.
- Aprende con teoría primero: necesita el modelo mental armado antes de practicar.
- Huecos declarados al arrancar, los cuatro a la vez: reconocer el patrón del problema,
  estructuras de datos y complejidad, implementar sin bugs bajo presión, system design.

## Cómo trabajar con él

- Riesgo conocido de su estilo: leer de más y practicar de menos. Un tema no cuenta como
  cubierto hasta que lo explicó con sus palabras y resolvió un ejercicio.
- No quiere acordarse de comandos. Todo arranca conversando.
- **Habla, no escribe.** Dicta por voz y no puede editar lo que ya dijo, así que se autocorrige
  dentro de la misma oración ("no me diste restricciones, o por lo menos ninguna fuerte").
  Juzgá siempre la oración completa, nunca el primer fragmento, y no registres como error algo
  que él ya corrigió al hablar. Esperá lo mismo en enunciados largos: repite y se reencauza en
  voz alta, y eso es pensar, no titubear.
- Le importa mucho la métrica de tiempo real y la racha, pero pidió explícitamente que la
  cobertura del temario no se pierda de vista por perseguir la racha.

## Lo que voy aprendiendo

Esta sección la actualizo yo al cerrar sesiones. Una línea por observación, con fecha.
Sirve para que la próxima sesión no proponga cosas sin sentido.

- 2026-09-09: sistema recién armado. Sin datos de sesiones todavía.
- 2026-09-09 (línea base A): no maneja la notación de complejidad. Lo dijo explícitamente.
  No es que calcule mal: no tiene la herramienta. Hasta cerrar `complejidad`, no tiene sentido
  pedirle que justifique un enfoque por su costo.
- 2026-09-09: su respuesta por defecto ante un problema nuevo es fuerza bruta, y se queda ahí.
  No busca una segunda idea salvo que se la pidan. Vale pedir explícitamente "dame una segunda
  opción" antes de dejarlo avanzar.
- 2026-09-09: no lee las restricciones del enunciado como señal de enfoque. Enseñarle a leer
  `O(log n)`, "sin división" o los límites de `n` como parte del problema, no como decoración.
- 2026-09-09: manda a juzgar sin probar ningún caso propio. Instalar el hábito de escribir dos
  o tres casos borde antes del primer submit.
- 2026-09-09: pierde tiempo en errores de lenguaje, no de algoritmo (argumentos del callback de
  `map`, `const` que pretende reasignar). Vale un repaso corto de API de arrays de JS.
- 2026-09-09: es honesto cuando no sabe y lo dice sin adornar. Eso hace confiable la medición;
  no hace falta sondear si entendió.
- 2026-09-09: pregunta por el propósito del protocolo mientras corre (para qué la predicción,
  cuándo arranca el reloj). Conviene explicar las reglas completas al abrir el tramo, una vez.
- 2026-09-09: tiende a decir "en una entrevista lo dejaría acá". Hay que recordarle que la
  entrevista no permite abandonar: se sigue hasta el final o se negocia una solución peor.
- 2026-09-10: absorbe teoría rápido cuando está bien trazada. Contestó los tres controles del
  bloque de complejidad sin ayuda, incluido el bucle escondido en `includes`. El hueco declarado
  ("no manejo la notación") era de herramienta, no de capacidad.
- 2026-09-10: generaliza de más con las constantes. Pasó de "no es un array" a "no entra en la
  complejidad" y se comió que `k` viene en el input. Vale chequear explícitamente "¿este valor
  hace que el algoritmo trabaje más?" cada vez que aparezca un segundo parámetro.
- 2026-09-10: no tenía método para buscar casos borde, y lo dijo derecho. No alcanza con pedirle
  que pruebe: hay que darle de dónde salen (extremos del contrato, ramas del propio código,
  valores que rompen la estructura elegida). Con el método puesto, los encontró.
- 2026-09-10: defiende su código con argumento correcto cuando lo cuestiono mal. Le dije que
  `[3,3]` era el caso que rompía y me respondió que no, porque consulta antes de insertar.
  Tenía razón. No acepta la autoridad sin verificar, lo que hace que sus "sí, entendí" valgan.
- 2026-09-10: objeta el trabajo mecánico. Cuando le di la corrección con el código ya escrito y
  después le pedí que lo reescribiera, preguntó para qué servía. Tiene razón: o se da la
  dirección sin el código listo, o se admite que el tipeo es trámite y no aprendizaje.
- 2026-09-10: trató un enunciado nuevo y autocontenido como algo que tenía que recordar ("no me
  acuerdo del ejercicio"). Al dar un problema inventado, aclarar que no es de LeetCode y que
  todo lo necesario está escrito.
- 2026-09-10: se subestima. Segunda predicción seguida errada, ahora hacia abajo: dijo "con
  pistas" y sacó Two Sum solo, sin una sola pista de algoritmo.
- 2026-09-10: lo que se lee incompleto es el **predicado**, no las restricciones. En 1207 invirtió
  "todas distintas" por "todas iguales"; las cotas sí las leyó y las evaluó bien. Con la lectura
  corregida sacó el canónico solo. Vale pedirle que reformule el contrato en voz alta antes del
  enfoque, siempre, no solo en ejercicios.
- 2026-09-10: no reconoce una solución correcta como correcta. Dio el enfoque canónico completo de
  167 y cerró con "creo que tiene un bug, no se me ocurre nada más". Es la misma raíz que las
  predicciones falladas hacia abajo. Vale devolverle la pregunta "¿qué te haría dudar de eso?"
  en vez de confirmar de una: el hueco es de criterio de validación, no de ideas.
- 2026-09-10 (fondo in-place): **no se le puede pedir notación de complejidad hablada.** Dicta por
  voz y el micrófono transcribe cualquier cosa cuando dice "O de n". Pedile el razonamiento en
  palabras ("una sola pasada", "nada que crezca con el input") y dejá la notación para el editor.
- 2026-09-10: **subestima sistemáticamente lo que puede.** Segunda predicción fallada hacia abajo
  en dos sesiones: predijo "con pistas" en 27 y lo sacó solo con cero. El motivo que declara es el
  lenguaje, no el algoritmo, y después no pregunta nada de sintaxis. Vale nombrárselo cuando la
  brecha se sostenga unas sesiones más, con los datos en la mano.
- 2026-09-10: **ya busca casos borde, pero solo en dos ejes**: tamaño de la entrada y rango de
  valores. No mira el extremo del resultado (respuesta 0, respuesta n), que es el que ejercita
  las ramas que nunca se toman. Se le dio el método de los tres ejes; chequear si lo aplica solo.
- 2026-09-10: **le faltaba el vocabulario, no el razonamiento.** No sabía qué era un "invariante"
  después de haberlo aplicado bien toda la sesión. Vale nombrar los términos técnicos cuando
  aparezcan en vez de suponerlos: el hueco es de léxico y se tapa en una oración.
- 2026-09-10: **razona los detalles cuando se le pregunta por ellos.** Explicó por qué `write`
  arranca en 0 acá y en 1 en el 26, y por qué no necesita la guarda de vector vacío, sin ayuda.
  Preguntar "¿por qué esta línea y no la otra?" le rinde más que explicarle.
- 2026-09-10 (micro 283): **reusa un patrón recién aprendido sin releer qué cambió el enunciado.**
  Aplicó la variante swap del 27 a un problema que exige preservar el orden. Al abrir un problema
  parecido a uno reciente, vale pedirle explícitamente qué restricción cambió antes de que codee.
- 2026-09-10: **declara invariantes débiles.** Enuncia una propiedad verdadera pero insuficiente
  para demostrar el problema. Chequear que el invariante mencione todo lo que el enunciado exige,
  no solo lo que el código hace.
- 2026-09-10: **el trace le rinde más que la explicación.** Nivel 1 de debug (input que falla +
  frames hasta la divergencia, sin decirle la corrección) le alcanzó para reformular el problema
  solo. No hace falta escalar rápido con él.
- 2026-09-10: **desconfía de soluciones correctas cuando le parecen poco elegantes.** Trató su
  segundo loop de relleno como una deuda ("no supe hacerlo en el mismo loop"). Es la misma raíz
  que las predicciones falladas hacia abajo: no reconoce lo correcto como correcto.

