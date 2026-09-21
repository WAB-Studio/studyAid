# Línea base

Una medición del nivel de partida, para que dentro de dos meses se pueda decir si mejoró.
No es una sesión de estudio: no se enseña nada, no se dan pistas, no se corrige durante.

Escrita el 2026-09-11. El archivo estaba referenciado por `AGENTS.md`, `README.md`,
`base/plan-de-fusion.md` y la skill `codigo`, pero nunca se había redactado.

## Estado

- **Forma A: cerrada el 2026-09-15.** A1 el 11; A2 y A3 el 15.
  **Medida en TypeScript**, no en C++: el cambio de lenguaje se decidió el 2026-09-15, a partir
  de lo que se vio en A2. La forma B tiene que ejecutarse en TypeScript para que la comparación
  valga.
- **Forma B: reservada.** Se ejecuta 4 a 6 semanas después de A, con los problemas marcados
  `[RESERVADO: línea base B]` en `.claude/skills/codigo/referencias-ts/problemas.md`, que hasta entonces no se usan
  para enseñar ni practicar.

## Reglas que valen para las dos formas

- Intención **medir**. Ninguna ayuda, ni siquiera preguntas socráticas, hasta que declare que
  terminó cada bloque.
- No se comenta si va bien o mal mientras ocurre. La devolución va entera al final.
- Se registra lo que pasó, no lo que se esperaba. Un resultado malo es un dato útil; uno
  maquillado arruina la comparación con B.
- **Errores de lenguaje:** un error de compilación o de API de la librería estándar no cuenta como
  fallo del algoritmo. Se anota aparte, en `--error-clase`, preguntando por ellos **antes** de
  registrar el ejercicio; si aparecen después, `PY sesion corregir`. Distinguir esto es el punto: si se comparan A y B sin separarlo, la
  mejora en sintaxis se va a leer como mejora en algoritmos. Sigue valiendo en TypeScript: en A2
  hubo errores de sintaxis en un lenguaje que él conoce bien.
- Si se corta a la mitad, se anota hasta dónde llegó. Media medición honesta sirve; una
  completada a las apuradas, no.

## Forma A

Tres bloques, unos 70 minutos en total. Se pueden partir en dos días si no hay ventana larga,
anotando la partición.

### A1: Reconocimiento de patrón (~20 min)

Seis enunciados, de temas variados y en orden mezclado. **No se resuelven.** Por cada uno pide
solo dos cosas: el nombre del patrón o la familia, y una oración de cómo lo encararía.
Nunca digas de qué tema es antes de que conteste.

Mide la debilidad principal declarada en el perfil: reconocer qué clase de problema es.

| # | Problema | Patrón canónico |
|---|---|---|
| 1 | 121 Best Time to Buy and Sell Stock | sliding-window / un solo paso con mínimo |
| 2 | 20 Valid Parentheses | stacks-queues |
| 3 | 200 Number of Islands | graphs-bfs-dfs |
| 4 | 875 Koko Eating Bananas | binary-search sobre el espacio de respuestas |
| 5 | 56 Merge Intervals | intervalos, ordenar como paso previo |
| 6 | 70 Climbing Stairs | dp-1d |

Registrar cada uno apenas contesta:

```bash
PY sesion patron --problema <n> --tema <canónico> --dijo "<lo que dijo>" --valido si|no
```

`--valido` es si el enfoque que propuso es defendible, no si coincide con la tabla.

### A2: Código en frío (~35 min)

**11 Container With Most Water** (`M`, two-pointers), en leetcode.com. Ejecutado en
TypeScript el 2026-09-15; ver "Registro de ejecuciones".
Sin ayuda de ningún tipo hasta que declare que terminó o que abandona.

Elegido porque admite una solución ingenua O(n²) que se puede escribir sin saber el patrón: deja
ver si llega a *algo* aunque no llegue a lo óptimo, que es la información que hace falta para
ubicar el punto de partida.

Pedir la predicción antes de arrancar. Registrar al terminar:

```bash
PY sesion ejercicio --ejercicio 11 --tema two-pointers \
  --resultado solo|con_pistas|abandonado --pista-max 0 \
  --prediccion solo|con_pistas|no_lo_saco [--error-clase "..."]
```

Anotar también, en la bitácora: si llegó a la ingenua, si vio la optimización, cuánto tardó en
cada cosa, y qué parte fue del lenguaje y no del algoritmo.

### A3: Diseño (~15 min)

**Diseñar un acortador de URLs.** Conversación estructurada, y **un diagrama dibujado por él**
(papel, ASCII o Mermaid), no descrito en palabras.

No se le corrige nada durante. Observar y anotar: si pregunta por requisitos antes de diseñar,
si estima capacidad, si nombra trade-offs con su contra, y si el diagrama tiene límites de
sistema claros.

Elegido porque es el caso canónico más documentado: en B se puede usar otro distinto sin que la
comparación pierda sentido.

## Forma B

Misma estructura, a las 4 a 6 semanas. Problemas:

- **B1**, reconocimiento: seis enunciados nuevos, mismos temas que A1, uno por tema.
- **B2**, código en frío: 15 3Sum, o el reservado que mejor corresponda al avance real.
  **En TypeScript**, como A2.
- **B3**, diseño: un caso distinto del acortador.

No mirar los resultados de A antes de ejecutar B.

## Qué se compara, y qué no

Se compara **desagregado**: aciertos de reconocimiento por tema, si llegó a la ingenua y a la
óptima en código, y la calidad del diseño por separado.

**No se resume en un único número ni en un puntaje compuesto.** `plan-de-fusion.md` §3 ya
descartó `dominio_por_tema()` y no vuelve en otra forma: una sola curva sube o baja según qué
dificultad se eligió, sin relación con el progreso.

## Registro de ejecuciones

### Forma A

- **A1: 2026-09-11.** 2 de 6 enfoques válidos (20 Valid Parentheses, 56 Merge Intervals).
  **0 de 6 patrones nombrados.** Detalle por problema en `bitacora/2026-09-11.md`.
  - Observación principal: en los dos válidos describió la mecánica correcta sin tener la
    etiqueta. Hipótesis a confirmar con A2, no conclusión.
  - 875 Koko no llegó a evaluarse: bloqueo de comprensión del enunciado en inglés, no de
    reconocimiento. **No se cuenta en el denominador al comparar contra B1.**
  - Advertencia para quien compare con B: el registro del problema 70 se corrigió durante la
    sesión. Se había anotado como suya una respuesta que él no escribió; quedó en "no sabe".
    El resultado publicado ya está corregido.
- **A2: 2026-09-15.** 11 Container With Most Water. **Resuelto solo, sin pistas, en ~20 min.**
  O(n²) correcta; **TLE 57/65**. Había predicho "con pistas": se subestimó.
  - **La optimización nunca apareció, ni como intuición.** Sus palabras: "no supe qué otra
    solución darle al problema". No hubo búsqueda fallida; no hubo búsqueda.
  - **Escrito en TypeScript, no en C++**, porque no sabe C++. Ese hecho disparó el cambio de
    lenguaje del mismo día (ver `temario.md`, "Cambios al plan"). **Consecuencia para B:** la
    forma A quedó medida en TypeScript, así que B2 va en TypeScript o la comparación se rompe.
  - **Errores de lenguaje, reportados por él:** iteraciones, declaraciones, signos de comparación
: en un lenguaje que usa hace 4 años. Salieron después de registrar el ejercicio; quedaron en
    el dato crudo el mismo día, vía `PY sesion corregir`, como
    `sintaxis-iteracion, sintaxis-declaracion, operador-comparacion`. La corrección queda visible
    en el evento con su motivo.
  - **Qué le hace a la hipótesis de A1.** A1 sugirió que el hueco era de vocabulario y no de
    razonamiento. A2 la debilita: el razonamiento está (llegó solo a una solución correcta) pero
    no percibió que hubiera un enfoque mejor, y eso no es una etiqueta que falta sino la técnica
    entera. Lectura de A1+A2: **dos huecos distintos**, vocabulario de patrones y repertorio de
    técnicas, no uno solo.
- **A3: 2026-09-15.** Acortador de URLs. **No salió.** Confirmado por él antes de interpretarlo.
  - No preguntó requisitos antes de diseñar; arrancó directo al diagrama.
  - No estimó capacidad: ni escrituras/lecturas, ni longitud de clave, ni almacenamiento.
  - No nombró ningún trade-off.
  - El diagrama es un flujo de decisión, no una arquitectura: sin límites de sistema, sin
    componentes, sin dónde vive el mapeo corta↔larga.
  - Falta el caso de creación. Sólo cubre "alguien hace click"; acortar no aparece.
  - Confirma con evidencia los huecos #3 y #4 del perfil, hasta hoy sólo autoevaluados.

**Forma A cerrada el 2026-09-15.** Partida en dos días: A1 el 11, A2 y A3 el 15.

### Forma B

- Pendiente. No antes del 2026-10-09.
