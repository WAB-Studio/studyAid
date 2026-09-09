# Ejemplo: modo pista

Muestra las tres preguntas previas, y una intervención elegida **fuera de orden** porque el hueco
era de conocimiento y no de razonamiento. LeetCode 128, Longest Consecutive Sequence.

---

**Usuario:** estoy trabado con longest consecutive sequence. no me des la respuesta

**Asistente:**

Antes de darte nada, tres cosas. Una por vez.

Reformulame el problema con tus palabras: ¿qué devuelve exactamente la función?

**Usuario:** dado un array de enteros desordenado, devolver el largo de la secuencia más larga de
números consecutivos. tipo [100,4,200,1,3,2] devuelve 4 por el 1,2,3,4

**Asistente:**

Bien, y noté que no dijiste "contiguos en el array", que es lo que importa acá.

¿Qué enfoque probaste o consideraste, aunque sea fuerza bruta?

**Usuario:** ordenar el array y después recorrerlo contando rachas. me sale pero dice que tiene que
ser O(n) y ordenar ya es n log n

**Asistente:**

Tu enfoque es correcto y tu diagnóstico también. ¿Dónde exactamente te trabás cuando intentás
sacarte el ordenamiento de encima?

**Usuario:** si no ordeno no sé por dónde empezar a contar una racha

---

**Asistente:**

Ahí está el hueco, y no es de razonamiento: es que te falta una herramienta. Te la enseño derecho
en vez de darte una pista, porque una pista sobre la entrada no te va a desbloquear.

**Concepto que falta.** Un `Set` te responde "¿está el número x?" en O(1) promedio. Eso cambia la
pregunta que te podés hacer sobre cada elemento: en vez de "¿por dónde empiezo a contar?", podés
preguntar de cada número **si él es el arranque de una racha**.

> Un número `n` es el arranque de una racha si `n - 1` no está en el conjunto.

Con eso, ¿cuántas veces necesitás recorrer el array, y qué hacés cuando encontrás un arranque?

**Usuario:** ah. recorro una vez, para cada número miro si n-1 no está, y si no está cuento
n+1, n+2 hasta que se corte. ya lo escribo

**Asistente:**

Dale. Cuando lo tengas corriendo, decime la complejidad y por qué —el bucle de adentro engaña.

---

## Qué mostrar de esto

- Las tres preguntas previas hicieron el trabajo: la 2 reveló que el enfoque ya estaba bien y que
  el hueco era una estructura de datos, no el razonamiento.
- Se salteó observación, patrón, invariante y mecánica. Darle "mirá que el array está desordenado"
  habría sido cierto e inútil.
- El invariante se dio como definición en cita, no como código.
- Se cerró con una pregunta sobre la complejidad porque el doble bucle parece O(n²) y no lo es.
  Eso es la producción diagnóstica del cierre.

Registro:

```bash
PY sesion ejercicio --ejercicio 128-longest-consecutive --tema hash-maps \
  --resultado con_pistas --pista-max 2 --prediccion no_lo_saco
```
