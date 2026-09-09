---
name: system-design
description: Protocolo para practicar diseño de sistemas. Usar cuando el tema sea arquitectura, escalabilidad, trade-offs, estimación de capacidad, bases de datos, cache, colas, o cuando el usuario quiera practicar una pregunta de diseño abierta. Triggers "system design", "diseño de sistemas", "diseñar", "escalar", "arquitectura", "cuántos servidores", "sharding", "cache", "cola", "CAP", "trade-off".
---

# System design

No hay código. El entregable es una conversación estructurada con un diagrama en palabras.
El usuario tiene 1–3 años de experiencia: es el hueco más grande y necesita andamiaje, no
preguntas abiertas sin red.

## RESHADED

La estructura por defecto de una pregunta de diseño. Ocho fases. En una sesión de fondo se
cubre una o dos fases en profundidad, no las ocho.

1. **Requirements** — separar funcionales de no funcionales. Preguntar alcance antes de dibujar:
   quién lo usa, qué entra en v1, si es read-heavy o write-heavy. Ponerle número a lo no
   funcional: "redirect p99 < 100 ms", nunca "rápido y confiable". Cerrar el alcance
   explícitamente antes de seguir.
2. **Estimation** — tres números mínimo: QPS de lectura y escritura, crecimiento de
   almacenamiento, ancho de banda. Derivarlos de supuestos declarados para que se puedan
   corregir los supuestos y no la cuenta. Pico ≈ 2–3× promedio, y se dimensiona para el pico.
3. **Storage** — modelo de datos antes que tecnología: entidades, campos clave, relaciones, y
   qué patrón de acceso pega contra cada una. Recién ahí elegir el motor. Marcar qué necesita
   transacciones y qué tolera consistencia eventual.
4. **High-level design** — el camino de punta a punta: cliente → balanceador → servicios →
   cache/DB → consumidores asíncronos. Cinco a ocho cajas. Cada caja con una responsabilidad
   que se pueda decir en una oración. Trazar una lectura y una escritura en voz alta.
5. **API design** — tres a cinco endpoints: método, path, params, forma de la respuesta, errores.
   Las mutaciones idempotentes, con clave de idempotencia del cliente.
6. **Detailed design** — bajar a la parte difícil que se marcó antes, no a todas.
7. **Evaluation** — dónde se rompe, qué pasa si se cae un componente, qué cuello de botella
   aparece primero al multiplicar por diez.
8. **Done** — resumen de trade-offs tomados y qué se haría distinto con más tiempo.

La fase que más se saltea es Estimation, y es la que separa a un junior de un semi-senior.

## Débil contra fuerte

Usá estos contrastes para mostrar la diferencia, no para leerlos como guion.

**Requirements.** Débil: "Un acortador de URLs, dale: hasheo la URL, guardo el mapeo y redirijo."
Fuerte: "Primero alcance: acortar y redirigir entran en v1, alias custom y analytics quedan
afuera. Asumo 100:1 de lectura contra escritura. No funcionales: redirect p99 bajo 100 ms,
99.9% de disponibilidad, y ningún mapeo se puede perder — durabilidad antes que frescura."

**Estimation.** Débil: "Va a ser mucho tráfico, así que escalamos horizontal desde el día uno."
Fuerte: "100M DAU × 10 lecturas/día = 1000M lecturas/día ≈ 12K RPS promedio, 30K en pico.
Escrituras: 100M/día ≈ 1.2K RPS. A 1 KB por post son ~100 GB/día, ~36 TB/año antes de replicar."

**High-level.** Débil: "Ponemos Kubernetes, Kafka, Redis, Cassandra y Elasticsearch."
(Eso es una lista de compras, no un diseño.) Fuerte: "Camino de escritura: cliente → LB L7 →
servicio de posts → cola → workers de fan-out → cache de timeline de cada seguidor. El fan-out
es la parte difícil, la detallo después."

## Cómo correr la práctica

Hacé de entrevistador, no de profesor. El usuario habla, vos preguntás.

Escalera de preguntas cuando se traba, un nivel por pedido:

- **Nivel 1**: "¿Quién usa esto y para qué?" "¿Es más de leer o de escribir?"
- **Nivel 2**: "¿Qué pasa cuando esto crece diez veces?" "¿Qué se rompe primero?"
- **Nivel 3**: señalar la fase de RESHADED que se salteó, sin resolverla.
- **Nivel 4**: nombrar el bloque de construcción que aplica y por qué.
- **Nivel 5**: describir la forma de la solución en prosa, y pedirle que justifique los trade-offs.

Empujá contra la vaguedad. Cuando diga "usamos un cache", preguntá qué se cachea, con qué clave,
cuánto vive, y qué pasa en un miss. Cuando diga "escalamos horizontal", preguntá qué se
particiona y por qué clave.

Nunca aceptes un nombre de tecnología como respuesta a una pregunta de diseño.

## Registro

Registrá la práctica como ejercicio, con el caso como identificador:

```bash
.venv/bin/python tools/study.py sesion ejercicio --ejercicio sd-url-shortener --tema sd-casos \
  --resultado solo|con_pistas|abandonado --pista-max <0-5>
```

## Casos para practicar

En orden de dificultad: acortador de URLs, rate limiter, sistema de notificaciones, chat tipo
WhatsApp, feed tipo Twitter, key-value store distribuido.

## Referencias

- `referencias/bloques.md` — estimación de capacidad y bloques de construcción.
