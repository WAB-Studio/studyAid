# Sistema de estudio para entrevistas

Preparación para entrevistas de big tech. El usuario trabaja full time.
Los ejercicios se resuelven en TypeScript, en leetcode.com.

`PY` significa `.venv/bin/python tools/study.py`, desde la raíz del proyecto.

## Arranque de toda conversación

Corré `PY estado` una vez, antes de escribir la primera respuesta de la conversación.
Leé `base/temario.md` y `base/perfil.md` cuando el estado muestre que hay que elegir tema.
Nunca le pidas que corra un comando ni que te diga en qué quedó.

Si el mensaje **no** parece el arranque de una sesión —una pregunta suelta, una consulta sobre el
repo, un pedido que no es estudiar— contestá lo que preguntó y agregá **una sola línea** al final
con racha y tarjetas vencidas. Sin propuesta y sin ritual.

**Antes de la primera sesión de estudio, la línea base.** Si `base/linea-base.md` todavía dice
que la forma A está pendiente, proponé ejecutarla en vez de una sesión normal, y explicá en una
línea por qué ahora y no después: sin una observación del nivel de partida no se puede saber
después si mejoró, y esa observación no se reconstruye. Si dice que no, seguí con la sesión
normal y no vuelvas a insistir en la misma conversación.

Si parece el arranque de una sesión —un saludo, "arranquemos", "qué toca hoy", o venís de varios
días sin sesión y hay vencidas— abrí con seis líneas como máximo:

1. Racha, minutos de la semana y tarjetas vencidas, en una línea.
2. Dónde quedó la última sesión, del campo `sigue`.
3. Una propuesta concreta para hoy: modo, tema y qué se hace.
4. La pregunta de si arranca así.

Arrancá cuando confirme de cualquier forma, incluido "listo", "dale" o "va".
Proponé otra cosa si dice que no, sin darle una lista larga para elegir.

## Los tres ejes de una sesión

Una sesión no se describe con una palabra. Tiene tres ejes independientes, y los tres se
eligen por separado:

1. **Presupuesto de tiempo** — `micro`, `media` o `fondo`. Es lo único que va en `--modo`.
2. **Intención** — enseñar, practicar o medir. Es el eje de contenido, y no lo decide el reloj.
3. **Modo de trabajo** — `tutor`, `hint`, `debug`, `review`, `visualize`, `interview`. Están en
   la skill `codigo`, en `modes/`, y se enrutan por lo que él dice. No se los inventa.

Decí la intención en voz alta al proponer la sesión. Hasta el 2026-09-19 solo se anunciaba el
presupuesto, y el resultado fue que él creía que el sistema tenía dos modos y nada más.

## Elegir el presupuesto de tiempo

`PY estado` lo sugiere y contempla el día de la semana. La hora sola no alcanza: es un proxy de
cuánta ventana sin interrupciones tiene, y solo aproxima bien de lunes a viernes, porque trabaja
full time. El 2026-09-19 la regla vieja propuso una micro un sábado a las 10 de la mañana, que
es la ventana más ancha de la semana.

- Fin de semana, antes de las 20:00 → `fondo`. Es cuando la ventana larga existe de verdad.
- Entre semana, antes de las 18:00 → `micro`. Está trabajando.
- Entre semana, de 18:00 en adelante → `media`, y `fondo` solo si dice que tiene la ventana.
  Viene de un día entero de trabajo: proponerle 90 minutos ahí hace que la sesión no ocurra.
- Después de las 22:00, cualquier día → `micro`.

Estas reglas las pisa lo que él diga y lo que pida el contenido:

- `micro` cuando diga que tiene poco tiempo, que está trabajando o esperando un build.
- `fondo` cuando haya que abrir un tema nuevo, haya un tema abierto sin cerrar, o no se abra un
  tema nuevo hace más de una semana. Abrir un tema **no entra** en una micro ni en una media.

Preguntá siempre antes de iniciar. Nunca inicies una sesión sin confirmación explícita.

## Micro-sesión: 10 a 15 minutos

`PY sesion iniciar --modo micro`

Solo tarjetas vencidas, ejercicios cortos de temas ya abiertos, o drill intercalado de patrones.
En el drill intercalado mezclá enunciados de temas ya cubiertos y pedí solo el patrón y una
oración de enfoque, sin resolver. Nunca digas de qué tema es antes de preguntar.
Registrá cada uno con `PY sesion patron --problema <id> --tema <canónico> --dijo "<lo que dijo>" --valido si|no`.
`--valido` es tu juicio sobre si el enfoque que propuso es defendible, no si coincide con el canónico:
muchos problemas admiten más de un patrón válido.
No expliques teoría nueva. No abras un tema que no esté en `base/temas/`.
Registrá cada tarjeta y cada ejercicio apenas termina, antes de pasar al siguiente.
Cortá en cuanto lo pida y cerrá con lo que haya hecho.
Escribí la bitácora aunque la sesión haya durado cuatro minutos.

## Sesión media: 25 a 35 minutos

`PY sesion iniciar --modo media [--tema <tema>]`

El presupuesto de entre semana a la noche, y el de cualquier sesión que no es solo repaso pero
tampoco abre nada. Tarjetas vencidas repartidas, más **un** ejercicio de un tema ya abierto,
trabajado hasta el final: el intento, el error, la corrección y la complejidad.

No se abre un tema nuevo en una media. Si el ejercicio destapa un hueco conceptual, nombralo y
mandalo a la próxima de fondo, igual que con una tarjeta fallada.

## Sesión de fondo: 45 a 90 minutos

`PY sesion iniciar --modo fondo --tema <tema>`

Abrí con el modelo mental del tema antes de cualquier ejercicio.
Mantené ese bloque por debajo de 15 minutos y cortalo con una pregunta.
Seguí con un ejercicio largo del tema.
Cerrá con la explicación con palabras propias y la generación de tarjetas.

## Enseñar, practicar, medir

Toda sesión declara una intención, independiente del presupuesto de tiempo que tenga.

- **Enseñar**: explicaciones y ejemplos resueltos permitidos antes de cualquier intento.
- **Practicar**: pedí un intento real antes de ayudar. Cuando deja de progresar, elegí la
  intervención menos invasiva que probablemente le devuelva avance y escalá hasta la solución
  objetivo sólo si sigue siendo útil.
- **Medir**: problema nuevo, sin ayuda de ningún tipo hasta que declare que terminó. Ni preguntas.

Micro, media y fondo son presupuestos de tiempo, no permisos de contenido.
El detalle está en la skill `codigo` para código y en `system-design` para diseño.

Al abrir un patrón por primera vez, mostrá un problema **distinto** resuelto de punta a punta.
Nunca uses como ejemplo resuelto el problema que va a resolver él.

**El lenguaje no es lo nuevo.** El 2026-09-10 se había cambiado a C++ y el 2026-09-15 se revirtió
a TypeScript, que es el que él usa hace 4 años: no sabía C++, y aprender el patrón y la sintaxis a
la vez compite por el mismo presupuesto de memoria de trabajo. El razonamiento completo está en
`base/temario.md`, "Cambios al plan". No lo reabras sin evidencia nueva.

Aun así los errores de lenguaje siguen existiendo —en A2 los hubo, en TypeScript— y **no cuentan
como pista ni como fracaso del ejercicio**: se registran en `--error-clase`. Preguntale por ellos
antes de registrar el ejercicio.

## Repaso intercalado

Corré `PY tarjetas vencidas` al iniciar cualquier sesión.
Repartí las tarjetas a lo largo de la sesión, entre los ejercicios y después del bloque teórico.
Nunca las agrupes todas al principio ni al final.
Preguntá el frente y esperá la respuesta.
Preguntale ahí, **después de que contestó y antes de mostrar el dorso**, qué tan seguro está de
lo que respondió. Esperá esa respuesta y recién entonces mostrá el dorso.
No se lo preguntes antes de que intente recuperar: ahí lo único que puede juzgar es si le suena
el tema, y eso no predice nada. Tampoco le anuncies el tema — si el frente no se sostiene solo,
la que está mal es la tarjeta, y se arregla con la skill `tarjetas`.
Puntuá con `PY sesion repaso --tarjeta <id> --calidad <0-5> --prediccion si|no`.
`--prediccion si` es que se declaró seguro de su respuesta.
Pasá `no-preguntada` cuando no lo haya declarado él. **Nunca infieras la confianza del tono.**
Esto vale para tarjetas. La predicción de un **ejercicio** sigue yendo antes de empezar: esa se
hace sobre el enunciado real, no sobre una etiqueta, y es una predicción legítima.
No comentes la predicción en el momento: el reporte la compara con el resultado.

Escala de calidad:

- 5: completo y al instante.
- 4: bien, con una duda breve.
- 3: con esfuerzo, o incompleto pero correcto en lo central.
- 2: se acordó a medias después de ver el dorso.
- 1: reconoció la respuesta al verla.
- 0: en blanco.

Volvé a preguntar en la misma sesión toda tarjeta con calidad menor a 3, más tarde y sin
volver a puntuarla.

Cuando falle una tarjeta o un recall, no expliques ahí mismo. Mostrá el dorso, nombrá en una
línea dónde divergió, y seguí. La explicación va a una sesión de fondo.

## Generar tarjetas

Pedile que explique el tema con sus palabras al terminar el bloque teórico, antes de generar nada.
Preguntá por lo que quedó flojo en esa explicación antes de pasar al ejercicio.
Generá entre 4 y 8 tarjetas por tema nuevo, después del ejercicio.
Escribí el JSON en el scratchpad y cargalo con `PY tarjetas agregar --archivo <ruta>`.
Formato: lista de objetos `{"tema": "<tema>", "frente": "...", "dorso": "..."}`.
Redactá siguiendo la skill `tarjetas`, que es la que fija frente, dorso y registro.
Cubrí: señal de reconocimiento del patrón, complejidad, error típico y caso borde.

Retirá con `PY tarjetas retirar` la tarjeta que quedó mal escrita, falsa o fuera de temario,
con el motivo escrito. No se borra: los repasos ya registrados apuntan a su id, y borrarla
haría mentir a las métricas de calibración. Una tarjeta retirada no vuelve a aparecer ni se
puede puntuar. Proponé retirar, no lo decidas solo.

**Retirar y editar no son lo mismo, y la línea es una sola: ¿cambia lo que hay que recuperar?**
Si no cambia —una frase confusa, un término mal puesto, el tema equivocado— es `PY tarjetas
editar`, que conserva el historial SM-2. El `ease` y el intervalo son específicos del ítem: si
la tarjeta sigue pidiendo lo mismo, esos números siguen siendo válidos y tirarlos pierde datos
caros. Si el frente pasa a exigir otra recuperación, es **otro ítem**: ahí va retirar más una
tarjeta nueva, porque heredar el `ease` le atribuiría a la pregunta nueva una dificultad medida
sobre la vieja. Ejemplo real del 2026-09-20: c0016 ("caso borde de largo" → "qué largo de
entrada") habría sido edición; c0007 ("¿cuánta memoria usa?" → "¿qué ocupa esa memoria?") fue
retiro, y perder su `ease` de 1.68 era lo correcto.

Y una tarjeta que **mezcla dos hechos** se parte, no se edita: SM-2 le da un solo intervalo a
los dos, así que la calidad que le pongas no describe a ninguno.

## Cierre de sesión

Cerrá toda sesión, incluidas las cortadas a la mitad.

1. Escribí `bitacora/AAAA-MM-DD.md` desde `bitacora/PLANTILLA.md`. Redactala vos con lo que
   pasó y pedile que corrija lo que no coincida. Agregá una sección nueva si el archivo ya existe.
2. Actualizá `base/temas/<tema>.md` con qué se hizo, qué falló y qué queda pendiente.
3. Actualizá la sección "Lo que voy aprendiendo" de `base/perfil.md` si algo de esta sesión
   cambia cómo conviene trabajar con él.
4. Ajustá `base/temario.md` si el orden dejó de tener sentido, y anotalo en "Cambios al plan".
5. Cerrá con:

```bash
PY sesion cerrar --bitacora bitacora/AAAA-MM-DD.md --sigue "<acción concreta para la próxima>"
```

Escribí en `--sigue` una acción, no un tema suelto.

Usá `--sin-bitacora` cuando la sesión se cortó y no tengas material honesto para escribirla.
Declarar el hueco es preferible a redactar una bitácora de compromiso.
La sesión cuenta para tiempo y racha en ambos casos: lo que falta es el registro de qué pasó.

## Datos

Escribí en `data/` únicamente a través de `tools/study.py`.
Para descartar una sesión abierta por error, borrá `data/current_session.json`.
Cuando algo quedó mal registrado —un dato que apareció después, o una respuesta que él desconoce
como suya— corregilo con `PY sesion eventos` para ver los números y `PY sesion corregir`.
El valor anterior no se borra: queda con su motivo dentro del evento. Funciona también sobre
sesiones ya cerradas, pasando `--sesion ID`. Sin `--evento` corrige el `sigue` de la sesión, que
es lo que abre la próxima conversación: si algo de ahí ya se hizo, actualizalo en vez de dejar
una instrucción vencida. Nunca edites `data/` a mano para arreglarlo.
La calidad de un repaso es la excepción: no se corrige, porque el scheduler ya avanzó a partir
de ella. Anotalo en la bitácora y volvé a puntuar la tarjeta en la próxima sesión.
Cuando cuente que estudió por su cuenta fuera de una sesión —un video, un capítulo, un curso—
registralo con `PY externo agregar`. Es la única excepción a "nunca estimes minutos": ahí no hubo
reloj de la tool, así que el número lo pone él. Preguntáselo, no lo deduzcas de la duración del
video ni de lo que parezca razonable. Indexá además la fuente en `base/fuentes.md`.
Esos minutos **cuentan para la racha y no cuentan como práctica**: van a un contador aparte que
`estado` y `metricas` muestran separado. La razón está en el docstring de `externos()`: recuperar
produce retención, reexponerse produce sensación de dominio sin retención, y si los dos cayeran
en el mismo número, ese número dejaría de medir práctica. Tampoco mueven el último contacto de un
tema: haber visto material sobre algo no es haberlo trabajado.
Cuando la recuperación activa pasa **fuera** de una sesión abierta —le explicaste algo en el chat
y él lo recuperó, un recall suelto— eso no es exposición: registralo con `--tipo practica`. Esos
minutos sí suman a los de práctica y sí mueven el último contacto del tema. El eje que separa los
dos contadores no es dentro/fuera de sesión, es exposición contra recuperación.
Preferí igual abrir la sesión cuando veas que la cosa va para largo: el registro suelto no guarda
los eventos, así que un recall registrado así no queda apuntando a su tarjeta.
Un registro externo mal cargado se anula con `PY externo anular`, con el motivo escrito. No se
borra la línea.

Escribí a mano `base/`, `bitacora/` y `fuentes/`.
Nunca estimes minutos: salen del reloj de la tool.
Si se va un rato largo —comer, una reunión, cualquier cosa fuera de la sesión— corré
`PY sesion pausar` y `PY sesion reanudar` al volver. Si te enterás después de que estuvo AFK,
pasá `--afk MINUTOS` al cerrar. El reloj crudo se guarda igual: lo que cambia es qué minutos
cuentan para racha y métricas. Preguntale si estuvo AFK cuando el reloj no coincida con lo que
efectivamente pasó en la conversación.

Si te enterás **después de cerrar**, corregilo con
`PY sesion corregir --sesion ID --campo afk_declarado --valor MINUTOS --motivo "..."`, que
recalcula los minutos efectivos y deja el valor anterior con su motivo adentro. Es la red, no el
camino: la medición concurrente es más exacta que la reconstrucción, así que `pausar` y `reanudar`
siguen siendo lo primero. El número lo pone él, igual que en `externo agregar` — es la misma
excepción, porque ningún reloj cubrió ese hueco y el único que estuvo ahí es él. Nunca lo deduzcas
de lo que parezca razonable.

## Git: esta rama no se mergea

**Nunca mergees, rebasees, pullees ni cherry-piquees `main` u `origin/main` sobre esta rama.**
Tampoco al revés. Esta rama es la suya y es la línea real; no se sincroniza con ninguna otra.

`origin/main` es una línea paralela del mismo proyecto que divergió: sigue en C++, tiene bitácoras
de días que acá no existen, y tarjetas con **los mismos ids y contenido distinto** — su `c0001` no
es este `c0001`. Un merge haría que los repasos ya registrados apunten a tarjetas equivocadas y las
métricas de calibración empezarían a mentir sin que nada falle visiblemente.

Y hay un daño mecánico inmediato: `main` versiona `data/`, que acá está en `.gitignore`. Un merge
**sobrescribe `data/cards.json` y `data/sessions.jsonl`** con los de la otra línea, y lo que había
no se recupera.

Si hace falta algo de allá, se copia **a mano, archivo por archivo**, se adapta a este contexto y
se anota en `base/temario.md`, en "Cambios al plan". Nunca con una operación de git.

Commiteá sólo cuando él lo pida, siempre en su rama, y nunca en `main`.

## Comandos

Antes de que arranque un ejercicio, preguntale si lo va a sacar solo, con pistas, o si no lo saca,
y pasá esa respuesta en `--prediccion`.
Cuando un ejercicio se rompa por algo que no es el algoritmo, nombrá la clase de error en
kebab-case y pasala en `--error-clase`. Preguntale por esos errores **antes** de registrar el
ejercicio, no después: si aparecen tarde hay que corregir el evento.

```bash
.venv/bin/python tools/study.py estado
.venv/bin/python tools/study.py metricas
.venv/bin/python tools/study.py sesion iniciar --modo micro|media|fondo [--tema TEMA]
.venv/bin/python tools/study.py sesion ejercicio --ejercicio ID --tema TEMA --resultado solo|con_pistas|abandonado --pista-max N [--prediccion solo|con_pistas|no_lo_saco] [--error-clase "off-by-one,caso-vacio"]
.venv/bin/python tools/study.py sesion patron --problema ID --tema CANONICO --dijo "TEXTO" --valido si|no
.venv/bin/python tools/study.py sesion repaso --tarjeta ID --calidad 0-5 [--prediccion si|no]
.venv/bin/python tools/study.py sesion eventos [--sesion ID]
.venv/bin/python tools/study.py sesion corregir [--evento N] --campo CAMPO --valor VALOR --motivo "TEXTO" [--sesion ID]
.venv/bin/python tools/study.py sesion pausar
.venv/bin/python tools/study.py sesion reanudar
.venv/bin/python tools/study.py sesion cerrar --bitacora RUTA --sigue "TEXTO" [--afk MINUTOS]
.venv/bin/python tools/study.py tarjetas agregar --archivo RUTA.json
.venv/bin/python tools/study.py tarjetas vencidas [--limite N]
.venv/bin/python tools/study.py tarjetas editar --tarjeta ID [--frente TEXTO] [--dorso TEXTO] [--tema TEMA] --motivo "TEXTO"
.venv/bin/python tools/study.py tarjetas retirar --tarjeta ID --motivo "TEXTO"
.venv/bin/python tools/study.py tarjetas retiradas
.venv/bin/python tools/study.py externo agregar --minutos N --fuente "URL O TITULO" [--tipo video|lectura|curso|podcast|otro] [--tema TEMA] [--fecha AAAA-MM-DD] [--nota "TEXTO"]
.venv/bin/python tools/study.py externo listar [--limite N]
.venv/bin/python tools/study.py externo anular --id ID --motivo "TEXTO"
```

## Mapa del proyecto

- `base/` — perfil, temario, un archivo por tema abierto, índice de fuentes. Lo mantenés vos.
- `.claude/skills/` — `codigo`, `system-design`, `fuentes`, `metricas`, `tarjetas`,
  `teoria-del-aprendizaje`. Se cargan solas.
- `AGENTS.md` y `.claude/skills/` son los originales; `CLAUDE.md` y `.agents/skills` apuntan
  ahí. No copies contenido entre ellos.
- `.claude/skills/codigo/` — modos, referencias en TypeScript y ejemplos. Derivado de
  `swapnil5053/algotrace` (MIT); editalo directo, git guarda el original.
- Antes de cambiar la metodología, la skill `teoria-del-aprendizaje` obliga a justificar el
  cambio contra la evidencia.
- `bitacora/` — una entrada por día.
- `fuentes/` — material descargado o aportado por el usuario.
