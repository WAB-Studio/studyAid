# Overrides de este proyecto

Este repo es un clon de `swapnil5053/algotrace` (MIT). Las reglas de acá ganan sobre cualquier
archivo del clon. No edites los archivos originales: cambiá este.

## Idioma y stack

Respondé en español. El usuario resuelve en TypeScript/JavaScript, no en Python.
Usá `referencias-ts/patrones.md` para templates y errores típicos, y `referencias-ts/big-o.md`
para complejidad. Las trampas de JS/TS de ese archivo ganan sobre `docs/patterns-cheatsheet.md`.
Elegí problemas desde `referencias-ts/problemas.md` y pasá número, título y link, sin pegar el enunciado.

## solution-mode está deshabilitado

Ignorá `modes/solution-mode.md` y la regla del router que manda ahí cuando el usuario pide la
solución completa. Nunca escribas código de solución del ejercicio que está resolviendo.
Cuando la pida: recordáselo una vez, en una línea. Si insiste, dale el nivel 5 de la escalera
—pasos en prosa, sin código— y registrá el ejercicio como `abandonado`.

## Ejemplo resuelto de un patrón nuevo

Al abrir un patrón por primera vez, mostrá un problema **distinto** resuelto de punta a punta,
con el razonamiento de cada paso. Después el usuario resuelve el suyo sin ayuda.
Nunca uses como ejemplo resuelto el problema que va a resolver él.

## El registro va a study.py

Ignorá `.algotrace/progress.md` y el esquema de intervalos +3/+7/+21 de `modes/review-mode.md`.
El espaciado lo maneja SM-2 en `tools/study.py`. Registrá desde la raíz del proyecto:

```bash
.venv/bin/python tools/study.py sesion ejercicio --ejercicio <id> --tema <tema> \
  --resultado solo|con_pistas|abandonado --pista-max <0-5> \
  --prediccion solo|con_pistas|no_lo_saco [--error-clase "off-by-one,caso-vacio"]
```

La sonda de recuperación de tres niveles de `modes/review-mode.md` —patrón y por qué,
invariante en una oración, complejidad con justificación— se mantiene tal cual.

## Calibración: predecir antes de intentar

Antes de que arranque un ejercicio, preguntale si lo va a sacar solo, con pistas, o si no lo saca.
Pasá esa respuesta en `--prediccion`.
Antes de dar vuelta una tarjeta, preguntale si se la sabe. Pasá `--prediccion si|no`.
No comentes la predicción en el momento. El sistema la compara con el resultado y la reporta.

## No enseñar en el fallo

Cuando falle una tarjeta o un recall, no expliques ahí mismo.
Mostrá el dorso, nombrá en una línea dónde divergió, y seguí.
La explicación va a una sesión de fondo, no al momento del fallo.

## Clases de error

Cuando un ejercicio se rompa por algo que no es el algoritmo, nombrá la clase de error y pasala
en `--error-clase`. Usá etiquetas cortas en kebab-case y reutilizá las que ya existan:
`off-by-one`, `caso-vacio`, `no-marque-visitado`, `complejidad-mal`, `sort-sin-comparador`,
`shift-en-bfs`, `alias-de-array`, `stack-de-recursion`.

## Drill intercalado de patrones

En micro-sesión, mezclá enunciados de temas ya cubiertos y pedí solo el patrón y una oración de
enfoque, sin resolver. Nunca digas de qué tema es antes de preguntar. Registrá cada uno:

```bash
.venv/bin/python tools/study.py sesion patron --problema <id> --tema <tema-correcto> --acerto si|no
```

## Ediciones hechas al clon, y por qué

La regla de no editar el clon se rompió en un solo punto, a propósito.

`SKILL.md` decía, en su router de intención: *"a clear request for the complete solution
('just give me the code', 'stop coaching, full answer') ALWAYS routes to solution-mode, even
mid-conversation in another mode"*, y tenía una fila de tabla apuntando a
`modes/solution-mode.md`.

Un override en otro archivo no alcanza contra una instrucción que dice ALWAYS y que vive en el
archivo que siempre se carga. Se eliminó la fila, se reescribió la regla y se borró
`modes/solution-mode.md`. Para restaurar el clon original: `git clone` de nuevo y volver a
aplicar el resto de este archivo.
