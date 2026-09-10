# Línea base

Dos formas paralelas. **A se ejecuta antes de empezar a entrenar. B queda reservada** y no se
usa ni para enseñar ni para practicar hasta que se ejecute, a las 4–6 semanas.

Lo irreversible no es quedarse sin problemas vírgenes —LeetCode tiene de sobra— sino no tener
una observación del nivel de partida. Esa observación no se puede reconstruir después.

## Cómo se compara

**No se resume en una nota única.** Se comparan cinco dimensiones por separado:

1. Reconocimiento del enfoque.
2. Calidad del enfoque propuesto.
3. Corrección del código.
4. Anticipación de bugs y casos borde.
5. Desempeño en diseño.

Con dos mediciones hay mucho ruido. Sirve para detectar cambios grandes y descubrir huecos,
no para demostrar causalidad. A y B están emparejadas por familia y dificultad pero **no son
idénticas**: cualquier lectura tiene que decirlo.

## Forma A — ejecutar ahora

### A1. Clasificación de enfoque, sin resolver

Seis enunciados, uno por vez. Se pide el enfoque y una oración de justificación. No se escribe
código y no se dice de qué familia es antes de preguntar.

| # | Problema | Familia | Dif |
|---|---|---|---|
| 1 | 49 Group Anagrams | hash-maps | M |
| 2 | 11 Container With Most Water | two-pointers | M |
| 3 | 739 Daily Temperatures | stacks-queues | M |
| 4 | 153 Find Minimum in Rotated Sorted Array | binary-search | M |
| 5 | 322 Coin Change | dp-1d | M |
| 6 | 200 Number of Islands | graphs-bfs-dfs | M |

### A2. Problema de código, 35–45 min, sin ayuda disponible

**238 Product of Array Except Self** (M). Sin pistas durante el intento, ni siquiera preguntas.
Se registra: reformulación, enfoque, complejidad declarada, veredicto de LeetCode, casos de
prueba que probó, y tiempo total.

### A3. System design, ~20 min

**Rate limiter.** Requisitos, una estimación, y los trade-offs de dos enfoques.

## Forma B — reservada, ejecutar en 4–6 semanas

Misma estructura. **Estos problemas no se usan para enseñar ni practicar.**

### B1. Clasificación de enfoque

| # | Problema | Familia | Dif |
|---|---|---|---|
| 1 | 347 Top K Frequent Elements | hash-maps | M |
| 2 | 15 3Sum | two-pointers | M |
| 3 | 150 Evaluate Reverse Polish Notation | stacks-queues | M |
| 4 | 33 Search in Rotated Sorted Array | binary-search | M |
| 5 | 198 House Robber | dp-1d | M |
| 6 | 695 Max Area of Island | graphs-bfs-dfs | M |

### B2. Problema de código

**560 Subarray Sum Equals K** (M). Mismo protocolo que A2.

### B3. System design

**Acortador de URLs.** Mismo protocolo que A3.

## Registro

Forma A: ejecutada el **2026-09-09**.
Forma B: reservada, a ejecutar a partir del **2026-10-07**.

Los resultados de cada forma se escriben acá abajo, crudos, sin interpretación agregada.

---

## Resultados — Forma A, 2026-09-09

Crudo, sin interpretación agregada. Detalle completo en `bitacora/2026-09-09.md`.

### A1. Clasificación de enfoque — 2 de 6 válidos

| # | Problema | Familia | Qué dijo | Válido |
|---|---|---|---|---|
| 1 | 49 Group Anagrams | hash-maps | Conteo de letras: vector de tamaño fijo si el alfabeto es acotado, diccionario si no. Agrupar por conteo igual. | sí |
| 2 | 11 Container With Most Water | two-pointers | Solo fuerza bruta, doble loop sobre todos los pares. | no |
| 3 | 739 Daily Temperatures | stacks-queues | Para cada i, escanear hacia adelante hasta el primero mayor. | no |
| 4 | 153 Find Min in Rotated Sorted Array | binary-search | Recorrer de izquierda a derecha hasta `a[i+1] < a[i]`. Preguntó qué significa "rotado". | no |
| 5 | 322 Coin Change | dp-1d | Greedy de mayor a menor denominación. Declaró que sabía que no era correcta. | no |
| 6 | 200 Number of Islands | graphs-bfs-dfs | Diccionario de tierras, unir claves adyacentes en grupos, contar grupos. | sí |

Enunciados dados parafraseados, sin número ni título.

### A2. 238 Product of Array Except Self — abandonado

- Predicción previa: **con pistas**. Resultado: **abandonado**. Pistas dadas: **0**.
- Reformulación: correcta.
- Enfoque declarado: producto total y después dividir por cada elemento.
  **No registró la restricción "sin división"** que estaba en el enunciado.
- Complejidad declarada: no pudo. Dijo no manejar la notación y razonó que dos recorridos
  no pueden ser lineales.
- Casos de prueba propios antes de mandar: **ninguno**.
- Veredicto LeetCode: **Wrong Answer** en `[-1,1,0,-3,3]` — esperado `[0,0,9,0,0]`,
  obtenido `[0,0,0,0,0]`.
- Errores no algorítmicos: usar el primer argumento del callback de `map` como índice
  (detectado y corregido por él solo); `const zerocount = 0` que nunca se actualiza.
- Al ver el fallo, diagnosticó correctamente por qué el cero rompe la división y esbozó
  guardar las posiciones de los ceros. Declaró que en una entrevista lo dejaría ahí.
- Tiempo: dentro del tramo de la sesión de fondo; el login a LeetCode no se contó.

### A3. System design — rate limiter

- Requisitos: **ninguno**. Declaró no saber qué preguntar ni tener experiencia con
  este tipo de sistemas.
- Estimación: **ninguna**.
- Enfoques: **uno solo**, sin alternativa ni trade-offs. Mirar la IP en cada request contra
  un store en memoria tipo Redis, acumular las requests del cliente y rechazar al llegar
  al límite.

### Las cinco dimensiones, resumidas

1. **Reconocimiento del enfoque** — 2/6.
2. **Calidad del enfoque** — fuerza bruta por defecto en 4 de 6. No usa las restricciones
   del enunciado (`O(log n)`, "sin división") como señal para elegir enfoque.
3. **Corrección del código** — no llegó a un submit correcto. Dos bugs de lenguaje, no de
   algoritmo; uno lo encontró solo.
4. **Anticipación de bugs y casos borde** — no probó nada antes de mandar. El borde lo
   encontró el juez. Diagnóstico posterior correcto.
5. **Diseño** — sin método. Intuición razonable, cero estructura.

**Calibración:** 1 predicción, 0 aciertos.
