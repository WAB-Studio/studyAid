# Perfil

Quién es, qué sabe y cómo conviene trabajar con él. Lo mantengo yo.

Este archivo se escribió el 2026-09-10, desde cero. El anterior era de otra persona y se eliminó.
La fuente de los hechos de experiencia es `resume-tailor/knowledge/`, verificada contra
`_repos-audit.md`, que cruza los repos con sus commits reales.

**Regla de honestidad de este archivo:** lo que está aquí o sale de evidencia o está rotulado como
supuesto. La sección "Lo que voy aprendiendo" se llena sólo con lo observado en sesiones
registradas; lo que no tenga una sesión detrás no entra.

---

## Quién es

Wilson Parada. Colombia. 4+ años de experiencia profesional. Full-stack con peso en backend.
Estudiando Ingeniería de Software en Uniminuto desde 2024.

Trabaja full time. El sistema tiene que asumir sesiones cortas entre semana y ventanas más largas
cuando aparecen, nunca al revés.

Español nativo. Inglés B2 declarado, y es el cuello de botella medido del objetivo (ver más abajo).

---

## Lo que sabe, con respaldo

Ordenado por profundidad demostrada, no por lo que dice el CV.

### Fuerte, con código en producción detrás

- **PHP / Symfony**, lo más profundo que tiene. En Iridian sostuvo una plataforma iGaming
  multi-tenant regulada: 14+ bundles y servicios desplegados por separado, 130+ entidades Doctrine
  cubriendo casino, sportsbook y wallet, aislamiento por tenant en la capa ORM, Symfony Messenger
  para procesamiento asíncrono, Redis, JWT con jerarquías de roles, FrankenPHP en producción.
  También un builder drag-and-drop de 50+ componentes y un flujo de pagos con 2FA/OTP y cifrado
  de datos sensibles.
- **Node.js / TypeScript**, su segundo eje. NestJS, Express, TypeORM, GraphQL con Apollo. En
  Gamefort diseñó el esquema TypeORM desde cero y el motor de brackets de doble eliminación, que
  es el trabajo más algorítmico verificable de su historial.
- **AWS serverless con IaC**. En Citrux, 15+ Lambdas con runtimes mixtos Python y Node, API
  Gateway, RDS PostgreSQL, todo en Terraform con estado remoto.
- **PostgreSQL**, transversal a casi todo. También MongoDB y Redis.
- **Integraciones y sistemas en tiempo real**. Socket.io, Ratchet, WebSockets duales.

### Lo más raro que tiene, y lo menos aprovechado

**Ingeniería de LLM en producción.** Es el activo que lo diferencia y hoy está enterrado como un
bullet del CV:

- **MCP Server en Python/FastMCP** exponiendo herramientas respaldadas por Salesforce, con OAuth2
  y JWT, y logging de invocaciones de herramientas en una base de auditoría separada.
- **Plataforma de voz con IA (HEP / nineteen58)**: telefonía Vonage VCC, servidor Node.js de
  WebSocket dual para audio en tiempo real, OpenAI Realtime, diarización, y un receptor de
  webhooks en Symfony que sincroniza resultados de llamada contra Salesforce vía REST v60,
  verificando firmas HMAC-SHA256 sobre CloudEvents.
- **Generación de CV con IA** y normalización de listings por LLM en el pipeline de Citrux.
- N8N con GPT-4o-mini para chatbots.

Esto importa para el sistema de estudio por dos razones: es el material del objetivo E, y es la
materia prima de los ejercicios de la etapa 5: no hace falta inventar casos, ya construyó los
suyos.

### Presente pero menos profundo

Python (FastAPI, sobre todo alrededor de integraciones con OpenAI), React y Next.js, React Native,
Flutter, Docker. Declarados como "familiar, no profesional": Django, GraphQL fuera de Gamefort.

---

## Los huecos

Los cuatro primeros no los deduje: los escribió él en
`resume-tailor/jobs/2026-05-19-rocket-panama-telecom/gaps-to-learn.md`, comparando su perfil
contra una oferta real.

1. **Inglés hablado.** Declara B2, las ofertas del rango alto piden C1. Es el riesgo número uno del
   objetivo y puede cortar en la primera llamada sin importar nada de lo técnico. La fricción
   específica que él identificó no es hablar sino **entender acentos**, en particular de hablantes
   de India, por los equipos integradores.
2. **Narrar liderazgo técnico.** Tomó decisiones de arquitectura reales (modelado multi-tenant,
   elección de stack para servicios nuevos, integraciones Salesforce, estructura de módulos del
   ERP chileno) pero no las tiene contadas como decisiones propias.
3. **Mensajería y microservicios.** Su experiencia es polyglot y de integración, no event-driven a
   gran escala. Faltan saga, outbox, idempotencia, choreography vs orchestration, y brokers a
   nivel conceptual.
4. **Modelado visual.** Diagramas de secuencia, C4, Mermaid. Se lo pidieron explícitamente en un
   JD y se lo evaluaron en vivo. **Confirmado con evidencia el 2026-09-15** (A3): su diagrama del
   acortador fue un flujo de decisión, sin límites de sistema ni componentes.

Y dos que salen de comparar su perfil contra el mercado que trabaja:

5. **Fundamentos de algoritmos y estructuras.** **Medido** en la línea base (A1 el 2026-09-11,
   A2 el 2026-09-15; detalle en `base/linea-base.md`). La capacidad de razonar está (resolvió 11
   solo y sin pistas) pero no nombró un solo patrón en seis, y en el ejercicio nunca percibió que
   existiera una solución mejor que la fuerza bruta. Dos huecos: vocabulario y repertorio.
6. **Obra pública.** El GitHub no tiene nada que respalde el posicionamiento. Para el objetivo E
   eso convierte una demostración en una afirmación sobre uno mismo.

---

## Cómo conviene trabajar con él

**Casi todo esto es provisorio y se corrige con sesiones.** Lo que sigue es lo observado el
2026-09-10, en la conversación donde se rearmó el sistema. No es un perfil de aprendizaje: es
lo poco que se puede afirmar sin datos.

- **Decide rápido y corrige rápido.** En una sola conversación cambió el objetivo heredado, eligió
  cuatro objetivos, aceptó un cambio de lenguaje y revirtió una decisión mía sobre el stack de voz.
  No necesita que le presenten menús largos; necesita una recomendación con el motivo.
- **Pide el porqué y lo usa.** Cuando le di un número de costo se lo cuestionó, y tenía razón en
  cuestionarlo. Conviene mostrarle el razonamiento, no la conclusión sola.
- **Escribe corto.** Respuestas de una línea. No confundir brevedad con falta de interés ni con
  acuerdo total: conviene confirmar la interpretación cuando una respuesta corta es ambigua.
- **Le molesta el trabajo que se siente ritual.** Rechazó LeetCode como eje por "grindy" antes de
  tener el argumento; el argumento apareció después y le daba la razón. La intuición sobre qué le
  sirve merece que se la investigue, no que se la descarte.

**Lo que no se va a suponer:** nada sobre estilo de aprendizaje. El repo ya tiene registrada la
razón (Pashler et al. 2008: no hay respaldo para emparejar instrucción a estilo autodeclarado), y
el perfil anterior tenía una afirmación de ese tipo que había que rotular como preferencia de
adherencia. No se repite el error.

---

## Restricciones

- **Trabaja full time.** El presupuesto de tiempo es el recurso escaso, no la motivación.
- **Los ejercicios de código van en TypeScript**, en leetcode.com (decisión del 2026-09-15, que
  revierte la de C++ del 2026-09-10). No sabe C++; el motivo completo está en `temario.md`,
  "Cambios al plan". C++ queda como pista aparte, sin competir con los patrones. Python para
  datos o scripting.
- **Cuatro objetivos apilados** significa que ninguna semana avanza en todo. Ver
  `roadmap.md` §3.1.
- **Los hechos de su experiencia no se inventan.** Salen de `resume-tailor/knowledge/`. Si hace
  falta uno que no está ahí, se le pregunta.

---

## Lo que voy aprendiendo

- **2026-09-10. Material primero, intento después, para todo patrón nuevo.** Lo pidió
  explícitamente después de que una sesión en intención *practicar* lo dejara atascado en un
  patrón que no había visto: "me mandaste a pensar pero me gustaría investigar, ver problemas en
  YouTube y aprender en general, no darme cabezados".

  Es una **preferencia de adherencia**, no un estilo de aprendizaje (el repo ya registra por qué
  esa distinción importa (Pashler et al. 2008)) pero además coincide con la evidencia sobre
  ejemplos resueltos para quien no tiene conocimiento previo del dominio, que es justamente lo que
  `plan-de-fusion.md` §2 usó para anular la regla de "ningún ejemplo antes del intento".

  **Cómo aplicarlo:** patrón nuevo se abre en *enseñar* (video o lectura, más un ejemplo resuelto
  de punta a punta sobre un problema **distinto**) y el intento viene después. *Practicar* queda
  para patrones ya vistos. Elegir *practicar* para algo nuevo es el error que ya se cometió una vez.

- **2026-09-10. Se aburre y se frustra con el trabajo que no produce nada.** Pasamos un día entero
  en planeación y su reclamo fue exacto: "no veo ninguna metodología o si la hay me tienes
  perdido". Conviene cerrar cada tramo de construcción con algo ejecutable, y no encadenar dos
  sesiones seguidas de puro diseño.

- **2026-09-11. Confirma o descarta lo que anotaste, antes de sacarle conclusiones.** En A1 le
  presenté una devolución construida sobre un registro que incluía una respuesta que él no había
  escrito. La detectó él: "eso que dijiste de la 6 está mal, la llenaste tú". El resultado real
  era peor que el que le mostré.

  **Cómo aplicarlo:** en cualquier bloque de medición, mostrarle lo que quedó registrado y que lo
  confirme **antes** de interpretar nada. Cuesta un minuto y es lo único que separa una línea base
  útil de una inflada. Vale también para las bitácoras.

- **2026-09-11. Describe mecánicas correctas sin poder nombrarlas.** Observado dos veces en A1:
  reinventó la pila llamándola "set", y describió el merge de intervalos sin nombrarlo. Es una
  observación sobre dos casos, no un rasgo establecido: A2 la pone a prueba.

  **Cómo aplicarlo, con cuidado:** cuando describa bien una mecánica, darle el nombre en el
  momento, sin ceremonia. Pero no dar por hecho que el razonamiento está y sólo falta la etiqueta:
  en los otros cuatro problemas no pasó, y en dos de ellos lo que faltaba era la técnica entera.

- **2026-09-11. El inglés del enunciado ya bloquea trabajo técnico.** 875 Koko Eating Bananas no
  llegó a evaluarse porque no entendió el enunciado. El inglés estaba listado como hueco #1 por
  las entrevistas; esta es la primera evidencia de que también corta antes, en el ejercicio.

  **Cómo aplicarlo:** distinguir siempre "no reconozco el patrón" de "no entiendo el enunciado", y
  registrarlos aparte. Si se mezclan, las métricas de reconocimiento van a medir lectura en inglés.

- **2026-09-15. Se subestima, y la predicción lo muestra.** En A2 predijo "con pistas" y resolvió
  solo, sin una sola pista, en ~20 minutos. Es un caso, no un rasgo, pero apunta al revés de lo
  que se suele corregir.

  **Cómo aplicarlo:** seguir pidiendo la predicción antes de cada ejercicio y mirar la dirección
  del error, no sólo si acertó. Si se repite el sesgo a la baja, decírselo con los datos delante:
  creer que no lo va a sacar cambia cuánto pelea antes de pedir ayuda.

- **2026-09-15. No busca una solución mejor porque no se le ocurre que exista.** En A2 escribió
  una fuerza bruta O(n²) correcta y se detuvo ahí. Sus palabras: "no supe qué otra solución darle
  al problema". No es que buscó la optimización y no la encontró: nunca apareció la sensación de
  que hubiera algo que buscar. El TLE lo sorprendió.

  Esto **debilita la hipótesis del 2026-09-11** de que el hueco es de vocabulario. El razonamiento
  está (llegó solo a algo correcto) pero el repertorio de técnicas no. Son dos huecos distintos.

  **Cómo aplicarlo:** después de cada solución que funcione, preguntar por la cota antes de pasar
  a otra cosa (qué n aguanta esto) para que "¿habrá algo mejor?" se vuelva un paso del protocolo
  en vez de una intuición que todavía no tiene. Y no dar por sentado que con la etiqueta del
  patrón alcanza: en A2 la etiqueta no habría servido de nada.

- **2026-09-15. Dice que sabe menos de lo que el plan asumía, pero sólo si se le pregunta directo.**
  El cambio a C++ del 2026-09-10 se registró como decisión suya y estuvo cinco días en el plan sin
  que apareciera que no sabe C++. Salió recién al preguntarle por qué el ejercicio estaba en
  TypeScript.

  **Cómo aplicarlo:** cuando acepte una decisión que implica una habilidad que no está verificada
  en este archivo, preguntar por el nivel de partida en ese momento. Acepta rápido: ya está
  registrado arriba, y eso incluye aceptar cosas que le van a costar más de lo que parece.

- **2026-09-16. El álgebra no le comunica; contar casos concretos sí. Pero el vocabulario lo quiere
  exacto.** Dos observaciones de la misma sesión que parecen contradecirse y no se contradicen.

  `n(n-1)/2 → O(n²)` lo trabó dos veces seguidas, y la segunda fue explícita: "sigo sin entender
  las fórmulas". Se destrabó al instante cuando se reemplazó el álgebra por contar casillas de una
  matriz de pares y preguntarle qué pasa al doblar `n`: contestó bien y sin dudar. La mecánica
  estaba; la notación simbólica era el bloqueo.

  Y en la misma sesión rechazó las analogías con las que se había destrabado: "cuando dices orden
  te refieres a la complejidad, fila tablero no entiendo qué es, tal vez si buscas en internet las
  palabras exactas". Quiere el término canónico, no el nombre casero.

  **Cómo aplicarlo:** simplificar el **mecanismo** (números concretos, contar, "¿qué pasa si `n` se
  dobla?") y no el **vocabulario**. El término real va desde el principio, definido en una línea.
  Una analogía sirve para destrabar, pero se reemplaza por el nombre canónico apenas entendió, en
  la misma respuesta si se puede. Va a entrevistas en inglés: el nombre es parte del contenido, no
  un adorno. Es coherente con el hueco #5 del perfil, que es de vocabulario tanto como de técnica.

- **2026-09-16. Tiene huecos de contexto de LeetCode que nadie preguntó.** No sabía qué significaba
  `TLE 57/65`: cinco días después de haber recibido uno y de que se discutiera en una sesión.
  Tampoco sabía construir un `Set` ni un `Map` en TypeScript, en un lenguaje que usa hace 4 años.

  **Cómo aplicarlo:** no dar por sabido el andamiaje (veredictos del juez, API de la librería
  estándar, cómo se leen las constraints) por el hecho de que sea senior en otras cosas. Es la
  misma forma del hallazgo del 2026-09-15 sobre C++: acepta y sigue sin señalar lo que no sabe.
  Preguntar directo cuesta una línea.

- **2026-09-16. Desconfía de su solución correcta y la cambia por una más simple que está mal.**
  En la micro resolvió el ejercicio con dos `Set` (la estructura estándar para el problema) y
  después descubrió por su cuenta que un `Set` no admite duplicados. Con eso propuso una versión
  de cuatro líneas, la presentó como la buena y describió la suya anterior como "esa solución toda
  compleja". La nueva devolvía los valores distintos, no los repetidos: respondía otra pregunta.

  Es la misma dirección que el sesgo de predicción del 2026-09-15, pero sobre código ya escrito y
  funcionando: no es que no sepa, es que asume que si le costó está mal.

  **Cómo aplicarlo:** cuando descarte una solución suya que funciona, no discutir el juicio: 
  correr las dos contra los mismos casos y mostrarle la tabla de salidas. Y nombrarle explícitamente
  cuándo *no* hubo sobreingeniería, porque no lo va a ver solo. Ojo con el reverso: en esa misma
  sesión su segunda versión sí era mejor que la primera y también llegó a ella solo, así que el
  instinto de simplificar es bueno; lo que falla es verificar antes de reemplazar.

- **2026-09-17. "Tema con actividad" no es "tema enseñado", y él lo nota antes que yo.** Se le
  propuso un drill intercalado de patrones sobre "temas ya cubiertos". Al segundo enunciado
  contestó "solo me has enseñado dos, no sabría responderte", y tenía razón: el único tema abierto
  era `complejidad`. Los otros siete que `PY estado` lista aparecen ahí porque la línea base los
  tocó en frío, no porque se hayan enseñado: `base/temas/two-pointers.md` lo dice en la primera
  línea: **No abierto**.

  **Cómo aplicarlo:** antes de proponer cualquier actividad de reconocimiento o repaso sobre un
  tema, confirmar contra `base/temas/<tema>.md` que existe y que está abierto de verdad; la lista
  de `PY estado` no distingue enseñado de medido. El drill intercalado no tiene sentido hasta que
  haya al menos tres o cuatro patrones abiertos. Y nota aparte: esta vez sí corrigió la premisa en
  vez de aceptarla, que es lo contrario de las entradas del 2026-09-15 y 2026-09-16: conviene
  darle el espacio para hacerlo, no leerlo como que ya no hace falta preguntar.

- **2026-09-19. La predicción hay que pedirla antes de mostrar el frente.** Dos sesiones seguidas
  (2026-09-17 y hoy) se fue directo al contenido cuando se le pidió el sí/no junto con la
  pregunta. Invertir el orden ("¿te la vas a saber?", y recién después el frente) lo resolvió en
  el acto: contestó la predicción en las cinco tarjetas restantes.

  **Cómo aplicarlo:** anunciar el tema de la tarjeta en media línea, pedir la predicción, y mostrar
  el frente cuando conteste. Pedir las dos cosas juntas no funciona. Si igual se saltó la
  predicción, registrarla como `no-preguntada`: inventarla ensucia la calibración, que es el único
  dato que mide si se conoce a sí mismo.

- **2026-09-19. Recita la regla correcta y da el número equivocado.** Ante un array de 10⁶ con solo
  dos variables: *"O(n), porque ese millón es de entrada que no cuenta"*. El motivo es exacto y la
  respuesta es O(1). Es la tercera vez con la misma forma (2026-09-16, dos veces): tiene las
  piezas y no las combina.

  **Cómo aplicarlo:** no dar por sabido un concepto porque lo enunció bien. Pedirle siempre el
  número sobre un caso concreto antes de marcar un subtema como cerrado. Vale al revés también:
  hoy el `log n` se destrabó justo así, preguntando cuánto da para n=8.

- **2026-09-19. La hora del día no dice cuánta ventana tiene; el día de la semana sí.** Se le
  propuso una micro a las 09:58 de un **sábado**, justificándola en voz alta con "estás en horario
  laboral". Lo corrigió él. La regla de `AGENTS.md` miraba solo el reloj, y ese proxy únicamente
  vale de lunes a viernes: la mañana del fin de semana es la ventana más ancha que tiene, y la
  regla la gastaba en 15 minutos de tarjetas.

  El costo no fue solo el sábado: `arrays-strings` llevaba pendiente desde el 2026-09-17 porque
  toda propuesta anterior a las 18:00 se convertía en micro, y un tema nuevo no se abre en una
  micro. La regla estaba matando de hambre a las sesiones de fondo.

  **Cómo aplicarlo:** ya está arreglado en la regla y en `PY estado`, que ahora contempla el día.
  Lo que queda como advertencia es la forma del error: **no justificar una propuesta con un
  supuesto sobre su vida sin verificarlo.** Si el motivo que le doy incluye "estás trabajando",
  "no tenés tiempo" o similar, eso es una afirmación sobre él, y la verifico o no la digo.

- **2026-09-19. Creía que el sistema tenía dos modos, porque solo le anunciaba uno de los tres
  ejes.** Pidió "más cosas, no solo micro y macro". El sistema ya tenía tres intenciones y seis
  modos de trabajo en la skill `codigo`, pero la intención casi nunca se decía en voz alta y los
  modos se enrutan solos desde lo que él dice, así que nunca los vio.

  Encaja con lo del 2026-09-11 y el 2026-09-17: nombra bien lo que percibe, y lo que no se nombra
  no existe para él. No es un pedido de más funcionalidad, es un pedido de visibilidad.

  **Cómo aplicarlo:** decir la intención en voz alta en cada propuesta, y nombrar el modo de
  trabajo cuando se entra en uno ("esto es debug", "esto es un mock"). Antes de agregarle piezas
  nuevas al sistema, revisar si la pieza ya existe y lo que falta es que se vea.

- **2026-09-19. Una plantilla con un hueco de relleno no le enseña nada; una traza con números
  sí.** Presenté el write pointer como código genérico con un `meSirve()` de mentira y contestó
  "no entendí muy bien, está muy abstracto". La misma idea, trazada fila por fila sobre
  `[3,8,5,2,7,4]`, la entendió en un mensaje y media hora después la implementó solo.

  Es la tercera vez con la misma forma (2026-09-16 con `n(n-1)/2`, hoy con `log n` y con esto).
  Ya no es una observación suelta: **lo que no comunica es el símbolo que ocupa el lugar de un
  valor**: la variable algebraica, el placeholder, la plantilla.

  **Cómo aplicarlo:** nada de pseudocódigo con huecos. Todo concepto nuevo entra con un caso
  concreto ejecutado paso a paso, con números de verdad y el estado después de cada vuelta. La
  generalización va después, y recién cuando ya vio la mecánica moverse.

- **2026-09-19. Cuando el bloqueo es una palabra, pregunta: si se le dio permiso explícito.**
  Frenó el ejemplo de 242 para decir que no sabía qué era un anagrama (lo confundía con
  palíndromo). Le había dicho una línea antes que preguntar vocabulario no contaba como pista.
  Contrasta con 875 Koko el 2026-09-11, donde el enunciado en inglés lo bloqueó y no lo dijo.

  **Cómo aplicarlo:** dar ese permiso explícito cada vez que se entrega un enunciado en inglés, en
  una línea. Cuesta nada y convierte un bloqueo silencioso en una pregunta. Y registrar aparte
  "no entendí la palabra" de "no reconocí el patrón": son dos huecos distintos.

- **2026-09-20. El nudge de región le alcanza: no hace falta escalar a la línea exacta.** Dos bugs
  en el mismo ejercicio, los dos de JavaScript. En los dos le nombré la región ("está en tu `if`",
  "está en tu `for`") más la entrada que rompe y la fila donde diverge, y le devolví el control con
  una pregunta. Encontró el arreglo él las dos veces, y el primero lo resolvió con `!= null`, que
  es la forma canónica. El modo debug tiene un nivel 2 (mostrar el diff) y no hizo falta usarlo.

  **Cómo aplicarlo:** arrancar siempre en nivel 1 y no ofrecer el nivel 2 antes de que lo pida.
  Lo que hace que el nivel 1 funcione no es la pista, es la **traza con la entrada concreta**: la
  fila donde su código diverge del correcto es la evidencia, y con eso solo él cierra. Coherente
  con lo del 2026-09-19 sobre plantillas: el número concreto comunica, el símbolo no.

- **2026-09-20. Le pido la señal de un patrón y contesta con la herramienta.** Dos veces en la
  misma sesión, antes y después del ejercicio: "necesito guardar una clave de valor". Eso describe
  el `Map`, no el enunciado. Es circular: equivale a "uso un martillo cuando tengo que martillar": 
  y no le sirve frente a un problema que no vio.

  Lo que sí tiene es la condición: *"no tengo la necesidad de saber el orden"*, que es una
  propiedad del problema y sale antes de decidir la estructura. Esa la dijo solo.

  **Cómo aplicarlo:** al abrir un patrón, enseñar la señal como una lista de **frases del
  enunciado** y no como una descripción de la estructura, y verificarla siempre contra un enunciado
  que no haya visto. Es el hueco #5 del perfil (repertorio, no razonamiento) y explica por qué en
  A1 nombró 0 de 6 patrones: el nombre y la mecánica los tiene, lo que falta es el puente desde el
  texto del problema.

- **2026-09-20. No avisa cuando se va, pero cuenta con precisión cuando vuelve.** Se le entregó un
  enunciado a las 17:57 de un sábado y desapareció hasta las 10:53 del domingo, con la sesión
  abierta: 17 horas de reloj crudo. Nadie pausó.

  Lo que hizo bien fue al volver: lo dijo sin que se le preguntara ("anota eso porque me fui hasta
  el otro día") y después dio la hora exacta en que paró y los 3 minutos que estuvo leyendo. El AFK
  salió de datos suyos.

  **Cómo aplicarlo:** entregar un enunciado es el punto donde la sesión se puede quedar abierta sin
  que nadie lo note, porque el turno pasa entero a él y no hay señal de que se fue. Si no contesta
  en el mensaje siguiente, correr `PY sesion pausar` en vez de asumir que está trabajando. Y cuando
  el reloj no coincida, preguntarle: reconstruye bien y no maquilla.

- **2026-09-20 (tarde). Enuncio una regla de más y la aplica al pie de la letra hasta trabarse.**
  En el bloque teórico de `two-pointers` dije *"el orden es lo que fabrica la monotonía"*. Es cierto
  para el par que suma, pero el orden es **una** de las fuentes, no la única, y `patrones.md` ya
  decía la versión completa: ordenado **o** factibilidad monótona. Frente a 11 Container With Most
  Water aplicó mi regla correctamente, concluyó que había que ordenar (lo cual destruye el
  problema) y después que dos punteros no servía. Sus palabras: *"estoy intentando desarrollarlo
  con lo que me enseñaste pero no me entra en la cabeza"*.

  No es que no razone: **razonó bien sobre una premisa que le di mal.** Es la misma forma que el
  otro error mío del mismo día, cuando afirmé que TypeScript se iba a quejar sin verificar la
  configuración del juez.

  **Cómo aplicarlo:** cuando enuncie una condición de un patrón, chequearla contra la referencia
  antes de decirla, y si la referencia dice "A **o** B", no decir solo A por economía. Él no tiene
  cómo saber que la regla venía recortada, y una regla recortada se ve igual que una regla falsa
  desde su lado.

- **2026-09-20 (tarde). Explica el patrón por la forma de la respuesta, no por lo que lo hace
  válido.** Cerrando `two-pointers`, después de haber trabajado la monotonía toda la sesión (y de
  haberla nombrado él mismo al decir "el ancho siempre se reduce") su explicación final fue
  *"tengo que fijarme en dos números específicos y de ahí sacar algo"*. Eso es la forma de la
  respuesta. La fuerza bruta también mira pares.

  Es la misma forma que el 2026-09-20 por la mañana con `hash-maps`, donde contestó "necesito
  guardar clave-valor". **Dos temas seguidos: la explicación final se queda en lo observable y
  deja afuera la condición que hace correcto el patrón.**

  **Cómo aplicarlo:** no alcanza con que la condición aparezca en el bloque teórico ni con que él
  la diga al pasar mientras resuelve. Hay que **pedírsela explícitamente como pregunta aparte**
  ("¿qué tiene que ser cierto del problema para que esto sea correcto?") antes de la explicación
  libre, y verificarla contra un enunciado que no haya visto. Las tarjetas c0017 y c0023 atacan
  esto, pero la pregunta tiene que estar también en la sesión.

- **2026-09-20. ANULADA el 2026-09-21: la predicción de tarjeta ya no se pide. Se deja escrita
  porque explica por qué existía y qué costó sacarla. La predicción se pedía DESPUÉS de contestar,
  y eso reemplazaba a su vez la entrada del 2026-09-19.** Aquella decía: anunciar el tema en media línea, pedir la predicción, mostrar el
  frente. Resolvía el problema de que se saltaba la predicción, pero creaba uno peor: **con el tema
  anunciado, lo único que podía juzgar era si le sonaba la etiqueta.** Eso es familiaridad con el
  indicio, no recuperación, y está documentado como mal calibrado.

  El resultado se ve en los datos del día: **dijo "sí" en 14 de 14 tarjetas**. Una constante no es
  una medición, y el umbral de sobreconfianza del 25% que define `metricas` no se puede calcular
  sobre ella.

  **Cómo aplicarlo:** mostrar el frente sin decir de qué tema es, esperar la respuesta, y recién
  ahí preguntar **"¿qué tan seguro estás de lo que contestaste?"** antes de dar vuelta. Si el
  frente no se entiende sin el tema, la que está mal es la tarjeta: eso lo arregla la skill
  `tarjetas`, no un anuncio verbal. Si no declara la confianza, va `no-preguntada`: **nunca
  inferirla del tono.** La predicción de **ejercicio** no cambia y se sigue pidiendo antes: esa se
  hace sobre el enunciado real, no sobre una etiqueta.

- **2026-09-21. Tener que darle instrucciones al sistema lo agota, y eso le cuesta sesiones.**
  Ese día dijo, con la sesión a medias: "no tiene sentido que yo tenga que mandarte todas las
  instrucciones" y después "me tienes cansado de cómo quieres seguir todo". El problema no era
  ninguna pregunta en particular, era el volumen: confirmar la apertura de la sesión, elegir entre
  opciones, declarar confianza en cada tarjeta. Cada una por separado parecía barata.

  El costo fue medible. Entre un video, un recall y un bloque teórico entero de `sliding-window`
  corrieron más de veinte minutos de estudio real sin sesión abierta, mientras se negociaba si
  abrirla. Esos eventos no se pueden reconstruir.

  **Cómo aplicarlo:** proponer y arrancar, no preguntar y esperar. Abrir la sesión sin pedir
  permiso. Cuando haya una decisión de verdad, darle la recomendación primero y las alternativas
  después, en una línea, no una lista para que elija. Y lo que se pueda decidir con el criterio
  que ya está escrito en `AGENTS.md`, decidirlo.

- **2026-09-21. El estilo de la escritura le compite al contenido.** Se frenó en medio de una
  explicación de sliding-window para pedir que dejara de escribir "en cristiano", sin guiones
  largos y con palabras de uso diario. Su razón sobre los guiones fue literal: "es full a que uno
  se da cuenta", o sea que son la señal más visible de texto generado. No es una preferencia
  estética suelta: si el estilo lo distrae, está gastando atención que necesitaba para el tema.

  **Cómo aplicarlo:** está en `AGENTS.md`, sección "Cómo le escribís", y en la skill `tarjetas`.
  Todo el repo se limpió de guiones largos ese día.

- **2026-09-21. Primera vez que el mecanismo sale sin pedírselo, y primera vez que separa
  corrección de costo por su cuenta.** El hallazgo de "recupera el número y el mecanismo queda
  afuera" venía documentado seis veces. Ese día, describiendo la ventana fija, explicó solo que
  se resta el que sale y se suma el que entra, y de ahí dedujo el O(n). Más adelante propuso
  llevar máximo y segundo máximo para la ventana de máximos: el esquema es correcto, y **él mismo
  detectó que seguía siendo n al cuadrado** porque recalcular el segundo máximo obliga a recorrer
  la ventana. Al principio de esa misma sesión había contestado con eficiencia una pregunta sobre
  corrección.

  Es un caso, no un rasgo todavía. **Cómo aplicarlo:** seguir pidiendo el mecanismo explícito,
  pero mirar si esto se repite antes de dar el hallazgo viejo por vigente. Si en las próximas dos
  o tres sesiones el mecanismo sigue saliendo solo, la entrada de las seis apariciones se cierra.

- **2026-09-21. Lo que falla no es el mecanismo de cada patrón, es la transferencia entre
  problemas.** Se le preguntó por "subarreglo con suma ≤ K" y contestó con "subcadena sin
  repetidos". Tenía el mecanismo correcto de los dos, pero no vio que la propiedad que los hace
  correctos es la misma con otro disfraz.

  **Cómo aplicarlo:** al cerrar un patrón, darle un segundo problema del mismo patrón en otro
  dominio (números contra strings contra intervalos) y pedirle que nombre qué comparten. No
  alcanza con que resuelva bien cada uno por separado.

