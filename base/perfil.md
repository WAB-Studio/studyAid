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

- 2026-09-12 (micro 344): **el invariante le suena a ceremonia, no a herramienta.** Preguntó
  derecho para qué sirve y si se lo piden en entrevistas. Es la tercera sesión que el invariante
  aparece como el hueco. Dejar de pedírselo como ritual: cada vez que se pida, mostrar qué
  decisión concreta resuelve —dónde corta el loop, qué caso borde queda cubierto— antes o
  inmediatamente después de pedirlo.
- 2026-09-12: **cuando el esquema aprendido no encaja, se queda sin nada en vez de razonar de
  cero.** Intentó meter el write buffer de 26/27/283 en un problema que no descarta elementos, vio
  que no calzaba y se detuvo. Distinto de aplicarlo mal (283): acá el problema fue no tener un
  plan B. Vale preguntarle "¿qué hace este problema con cada elemento?" para que reconstruya en
  lugar de buscar en su catálogo.
- 2026-09-12: **pregunta por los tipos del lenguaje en el momento en que le estorban, y ahí lo
  absorbe.** La duda de división entera y flotantes salió sola, con el código escrito. La rampa de
  C++ rinde más contestando estas preguntas cuando aparecen que dando un bloque de sintaxis aparte.
- 2026-09-14 (micro 125): **la pregunta "qué hace este problema con cada elemento" funcionó.**
  Se la pedí antes de codear, en vez de dejar que buscara el patrón, y salió el enfoque completo
  —filtrar y comparar desde los extremos— con el invariante bien declarado y el caso borde
  resuelto. Es la contramedida directa a la observación del 09-12 y conviene volver a usarla.
- 2026-09-14: **elige los casos de prueba mirando su código, no el enunciado.** Ya prueba antes de
  mandar, que es progreso real, pero los tres casos que eligió cubrían las ramas del segundo loop
  y ninguno tocaba la decisión de qué carácter filtrar, que era donde estaba el bug. El pedido
  útil no es "probá casos borde" sino **"un caso por cada decisión que toma el enunciado"**.
- 2026-09-14: **re-preguntar una tarjeta fallada en la misma sesión no mide nada acá, y lo dijo.**
  El dorso queda scrolleable dos mensajes arriba. La regla sirve para un canal donde la respuesta
  no queda a la vista; en texto, la repetición conviene dejarla al calendario del SRS.
- 2026-09-14: **un concepto marcado como cubierto puede estar invertido, no olvidado.** `m[k]` que
  inserta al leer se vio el 09-10 y contestó "fuera de rango": no es falta de repaso, es un modelo
  mental al revés. Vale distinguir la tarjeta que falla por olvido de la que falla por creencia
  contraria: la segunda necesita una corrección explícita, no otro repaso.
- 2026-09-15 (micro 125 rehecho): **pedir "un caso por decisión" no alcanza; hay que pedir el
  contrafáctico.** Nombró las decisiones del enunciado bien y aun así eligió para el filtrado un
  caso que no lo probaba. La pregunta que lo destrabó en un solo turno fue **"si cambiaras esa
  decisión por la contraria, ¿este caso da distinto?"**. Con eso llegó solo al input exacto que
  lo había roto el día anterior. Es la forma operativa de la observación del 09-14.
- 2026-09-15: **el tilde de un subtema no es evidencia de retención.** `map` contra
  `unordered_map` estaba marcado como cubierto desde el 09-10 y salió en blanco. Se dio en una
  sesión donde se cubrieron otras cuatro cosas alrededor de un ejercicio. Vale tildar el subtema
  recién cuando haya una tarjeta suya aprobada, no cuando se explicó.

- 2026-09-17: **refuta sus propios criterios si se le pide verificarlos, sin ver el contraejemplo.**
  Las tres intervenciones de 680 fueron preguntas —"construí un caso de tres letras que dé false",
  "¿qué hacés si los dos chequeos dan verdadero?"— y en las tres se corrigió solo. Guardar el
  contraejemplo mínimo para cuando la pregunta no alcance: con él suele alcanzar.
- 2026-09-17: **primera predicción acertada** en cinco ejercicios registrados. Las anteriores
  fallaban hacia abajo. Todavía no es tendencia, pero la brecha dejó de ser sistemática.
- 2026-09-17: **encontró su propio bug antes de correr el código, por segunda sesión seguida.**
  Y lo nombró bien: "error de C++, estaba comparando índices y no valores". La distinción entre
  error de lenguaje y error de algoritmo ya la hace él.
- 2026-09-17: **cansado, saltea el protocolo y manda.** Se le dio el marco de casos de prueba
  antes de codear y aun así mandó con dos casos que ya tenía usados, declarando cansancio. Dar el
  marco no alcanza: hay que **pedirle los casos y esperar la respuesta** antes del submit. Y si
  dice que está cansado, cerrar en vez de estirar.
- 2026-09-17: **critica el material que se le da, y conviene verificarlo contra los datos antes
  de aceptarlo o rechazarlo.** Pidió retirar `c0014` por mal escrita: tenía razón (el frente era
  un acertijo). El diagnóstico que dio —"las otras están sin voseo"— no se sostiene; el voseo es
  mayoría y lo que está partido son las tildes. Ambas cosas se le dijeron, y quedó conforme.

- 2026-09-18 (micro de tarjetas): **primera sobreconfianza registrada, y en tarjeta, no en
  ejercicio.** Dijo que se sabía `c0004` y contestó `O(1)`. La brecha de calibración venía siendo
  siempre hacia abajo en ejercicios; en tarjetas apunta al otro lado. Son dos instrumentos
  distintos: predecir si vas a resolver un problema no es lo mismo que predecir si tenés un hecho
  en la cabeza, y en el segundo confunde "me suena el tema" con "sé la respuesta".
- 2026-09-18: **no contesta la pregunta de predicción, contesta la tarjeta.** Las tres veces que
  se le preguntó "¿te la sabés?" pasó derecho al contenido, y después objetó la pregunta entera:
  "me parece inútil, es una molestia". **Resuelto el mismo día**: la confianza se pide después de
  su respuesta y antes del dorso, y se omite si no la declara. Justificación y corte de serie en
  `bitacora/2026-09-18.md`.
- 2026-09-18: **el input que no se imagina es el que tiene signo.** En 977 dio por hecho que
  ordenado implica cuadrados ordenados: leyó "enteros" sin instanciar un negativo. Es la misma
  raíz del 09-09 (no usar el enunciado como señal) pero más barata de atacar: pedirle que escriba
  un input concreto de tres elementos antes de declarar el enfoque, no después.

- 2026-09-18 (micro de mediodía): **la calibración se dio vuelta en una sesión.** 6 de 6
  predicciones sin una sola sobreconfianza fallada, y **dos subestimaciones**: dijo "poco" y
  "medio" y acertó las dos. Contra el patrón de la mañana. Si se sostiene, el riesgo cambia de
  lado: deja de ser estudiar de menos lo que cree sabido y pasa a ser no confiar en una respuesta
  correcta, que en una entrevista se lee como titubeo. Dos sesiones no son tendencia; mirar la
  serie en `metricas` dentro de una semana antes de tocar nada.
- 2026-09-18: **el protocolo nuevo de confianza funcionó a la primera.** Preguntada después de
  su respuesta y antes del dorso, la declaró las seis veces, en una palabra y sin resistencia.
  No hubo que inferir nada del tono. La objeción del 09-18 a la mañana era al instrumento, no a
  la métrica.
- 2026-09-18: **el patrón no se activa cuando el enunciado no se parece al ejercicio donde se
  aprendió.** Tercera repetición (línea base 09-09, 977 a la mañana, 88 al mediodía). En 88 llegó
  solo al obstáculo correcto y se detuvo; antes de eso lo había clasificado como problema de
  ordenamiento, un tema que no está abierto. **El diagnóstico no es que le falte el patrón: es
  que la etiqueta del problema la busca en el dominio del enunciado, no en la forma de los datos.**
  Los drills intercalados son el instrumento correcto y hay que sostenerlos; lo que conviene
  agregar es pedirle, cuando diga que no sabe, qué operación necesita en vez de qué tema es.
- 2026-09-18: **audita los efectos secundarios de lo que la tool hace con sus datos.** Pidió
  reescribir una tarjeta y acto seguido preguntó si los números se habían mantenido; se habían
  movido (`ease` 2.6 → 2.5, `reps` a 0). Corresponde **decir el costo antes de ejecutar**, no
  después, cada vez que una operación sobre `data/` no sea reversible o pierda historial.

- 2026-09-20 (fondo hash-maps): **el bloque teórico corto no le sirve, y el pedido es legítimo.**
  Objetó la primera versión del modelo mental —"cero profundidad, una cosa muy por encima"—
  nombrando exactamente lo que faltaba: función hash, colisiones, memoria. Con el bloque rehecho
  al nivel del mecanismo contestó el control sin ayuda y encadenó tres causas. No es un pedido de
  más texto: es que **sin el mecanismo no puede defender la complejidad**, y el perfil ya decía
  que aprende con teoría primero. Al abrir un tema, el modelo mental va al nivel de cómo funciona
  la estructura por dentro, no al de cómo se usa.
- 2026-09-20: **los errores ya son todos de lenguaje.** Cuatro en 49 —clave `int` por `string`,
  `find` como bool, `push_back` asignado, funciones sin `return`— y cero de algoritmo. Es un
  cambio respecto de la línea base, donde el enfoque mismo fallaba. Lo que queda por bajar es la
  rampa de C++, no el razonamiento.
- 2026-09-20: **la creencia invertida se corrige enseñándola de frente, y el efecto se ve el
  mismo día.** `c0010` (`m[k]` inserta al leer) venía de calidad 1 con la respuesta contraria;
  se atacó explícitamente en el bloque teórico y esa tarde la contestó completa, con los tres
  tipos de ejemplo y confianza alta. Confirma la distinción del 09-14: olvido pide repaso,
  creencia contraria pide corrección explícita.
- 2026-09-20: **un concepto recién enseñado no se transfiere solo a su propio código.** Sabía que
  `m[k]` inserta al leer y aun así escribió el `if/else` que eso vuelve innecesario; con la
  pregunta dijo "no entiendo de qué me estás hablando", y lo vio recién con el trace frame por
  frame. La pieza que faltaba era que `m[k]` devuelve una **referencia**. Refuerza el 09-10: el
  trace le rinde más que la explicación, y conviene ir al trace antes y no después de la pregunta.
- 2026-09-20: **pide el input concreto y aun así contesta en abstracto.** Pedido explícitamente,
  dijo "tres palabras en minúscula cualquiera". Hay que pedirle **las letras**, no el input: la
  formulación general le sale sola y es justamente la que le deja el caso sin instanciar.
- 2026-09-20: **por primera vez buscó una segunda idea sin que se la pidieran.** Propuso modificar
  `strs` in-place para ahorrar memoria, con un argumento de costo, y se dio cuenta solo de por qué
  no servía al preguntarle qué aparecía en el output. Contra la observación del 09-09. Si se
  sostiene, dejar de pedirle "dame una segunda opción" como paso fijo.
