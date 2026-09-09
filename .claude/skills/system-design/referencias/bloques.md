# Bloques de construcción y estimación

## Atajos de estimación

- 86.400 segundos por día. Redondear a 100.000 para la cuenta mental.
- 1M de requests por día ≈ 12 RPS.
- Pico ≈ 2–3× el promedio. Se dimensiona para el pico.
- Ancho de banda = RPS × tamaño del objeto. En sistemas con media pesa más que el conteo de requests.
- Un año son ~30M de segundos.

Latencias que hay que tener en la cabeza:

| Operación | Orden |
|---|---|
| Referencia a memoria | 100 ns |
| Lectura de SSD | 100 µs |
| Round-trip dentro del datacenter | 500 µs |
| Lectura de disco rotacional | 10 ms |
| Round-trip intercontinental | 150 ms |

La conclusión práctica: una llamada de red dentro del datacenter cuesta como 5.000 accesos a
memoria, y cruzar el océano cuesta como 1.500 llamadas dentro del datacenter.

## Bloques

**Balanceador de carga.** Reparte tráfico. L4 mira IP y puerto, L7 mira el contenido HTTP y
puede rutear por path. Da también health checks y terminación TLS.

**Cache.** Guarda lo caro cerca de quien lo pide. Niveles: cliente, CDN, capa de aplicación,
base de datos. Lo difícil nunca es guardar, es invalidar. Políticas de desalojo: LRU por
defecto, LFU si hay un núcleo caliente estable. Decisiones que hay que poder responder: qué se
cachea, con qué clave, cuánto vive, y qué pasa en un miss.

**Cola de mensajes.** Desacopla productor de consumidor y absorbe picos. Da reintentos y
procesamiento asíncrono. Trae de regalo: entrega al menos una vez (o sea, hay que ser
idempotente), orden solo dentro de una partición, y backpressure cuando el consumidor no da abasto.

**Sharding.** Partir los datos horizontalmente por una clave. La elección de la clave es la
decisión: una mala clave crea particiones calientes. El hashing consistente minimiza cuántas
claves se mueven al agregar o sacar un nodo.

**Replicación.** Copias de los mismos datos. Líder-seguidor da lecturas escalables y
consistencia eventual en los seguidores. Multi-líder da escrituras locales y conflictos que
alguien tiene que resolver.

**CDN.** Copias del contenido estático cerca del usuario. Baja latencia y saca carga del origen.

## CAP, en la versión que se usa

Ante una partición de red hay que elegir entre consistencia y disponibilidad. Sin partición no
hay que elegir nada. La pregunta útil en una entrevista no es "¿CP o AP?" sino "cuando este
componente se parte, ¿prefiero devolver un dato viejo o devolver un error?".

- Un saldo bancario: error. Consistencia.
- Un contador de likes: dato viejo. Disponibilidad.

## ACID contra BASE

ACID: atomicidad, consistencia, aislamiento, durabilidad. Lo que da una relacional.
BASE: básicamente disponible, estado blando, consistencia eventual. Lo que da mucha NoSQL.

No es una elección de religión sino por dato: en el mismo sistema, los pagos van en ACID y el
feed va en BASE.

## Trade-offs que aparecen siempre

- Consistencia contra disponibilidad y latencia.
- Normalizar (escrituras baratas, lecturas con joins) contra desnormalizar (lecturas baratas,
  escrituras que actualizan varias copias).
- Push contra pull en un feed: fan-out en escritura es rápido para leer y caro para usuarios con
  millones de seguidores; fan-out en lectura es al revés. Los sistemas reales hacen híbrido.
- Sincrónico contra asincrónico: la cola baja la latencia percibida y sube la complejidad
  operativa.

## Anti-patrones

- Listar tecnologías en vez de diseñar responsabilidades.
- Diseñar para 100M de usuarios cuando el enunciado dijo 100.000.
- Saltear la estimación y descubrir el cuello de botella recién cuando el entrevistador pregunta.
- Decir "usamos cache" sin decir qué, con qué clave, ni qué pasa en un miss.
- Un único punto de falla que no se nombra.

---

Adaptado de `kirilxd/swe-interview-coach` (MIT).
