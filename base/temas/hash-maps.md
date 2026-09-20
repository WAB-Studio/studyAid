# hash-maps — Mapas y conjuntos hash

Abierto: 2026-09-20

## Modelo mental

Un hash map es una caja de casilleros donde la clave dice directamente en qué casillero mirar.
La función hash convierte la clave en un número de 64 bits, el módulo contra la cantidad de
buckets lo convierte en una posición, y adentro del bucket el `operator==` decide cuál de los
elementos que cayeron ahí es el que se busca. Por eso una clave necesita las dos cosas: `hash`
y `==`.

Se reconoce en el enunciado por tres preguntas: "¿ya vi este valor?", "¿cuántas veces aparece?"
y "¿qué elementos comparten esta propiedad?". Las tres se contestan en una sola pasada en vez
de comparar todos los pares, que es la forma en que el patrón tumba un O(n²) a O(n).

El costo es O(1) **promedio** y O(n) en el peor caso, cuando todas las claves caen en el mismo
bucket. Se paga en memoria: `unordered_map` de C++ resuelve colisiones por chaining —obligado de
hecho por el estándar, que promete referencias estables tras un rehash— así que cada elemento es
un nodo alocado aparte. Un `unordered_map<int,int>` gasta del orden de 40 bytes por par contra
los 8 que ocupan los datos crudos, más el array de buckets, más un fallo de caché por búsqueda
que no aparece en ninguna notación.

## Subtemas

- [x] Señal de reconocimiento en el enunciado: ya lo vi / contar / agrupar por clave.
- [x] `m[k]` inserta al leer, y devuelve una **referencia**. Las dos mitades del mismo hecho.
- [x] `find` contra `.end()`, `count`, y cuándo cada uno.
- [x] Función hash: contrato, `std::hash<int>` como identidad, `h(k) % B` con B primo.
- [x] Colisiones: chaining contra open addressing, y por qué C++ usa chaining.
- [x] Load factor, rehash amortizado, `reserve`.
- [x] Costo de memoria del contenedor.
- [x] Claves compuestas: `vector<int>` no es hasheable, codificar a `string`.
- [ ] `unordered_set` y cuándo alcanza con el conjunto sin valor.
- [ ] Hash map como índice de posiciones, no como transformación de la entrada (128).
- [ ] Peor caso adversarial y mezcla de bits como defensa. Visto de pasada, sin ejercitar.

## Criterio de dominio

Resolver un problema del tema sin pistas de algoritmo, declarando O(1) promedio **y** el peor
caso con su motivo, y eligiendo la clave sin ayuda cuando no es el elemento crudo sino una
transformación de él.

## Fuentes usadas

- `.claude/skills/codigo/referencias-cpp/patrones.md`, sección hashing / frequency-map.

## Historial

- 2026-09-20 (fondo): tema abierto. Bloque teórico rehecho a pedido suyo con el mecanismo
  completo —hash, módulo, colisiones, load factor, memoria— después de objetar que la primera
  versión no tenía profundidad. 49 Group Anagrams Accepted con 4 pistas, todas de reformulación
  salvo la última. Los cuatro errores del intento fueron de C++, ninguno de algoritmo.
  Quedó flojo open addressing, explicado al cierre y sin ejercitar.
