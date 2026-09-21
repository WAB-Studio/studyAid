# Ejemplo: modo debug

Muestra el trace hasta el frame donde el estado divergió, sin reescribir el código.
LeetCode 3, con el bug clásico de la ventana que retrocede.

---

**Usuario:** mi sliding window falla en "abba", da 3 y tendría que dar 2

```ts
function largoSinRepetidos(s: string): number {
  const seen = new Map<string, number>();
  let left = 0, best = 0;
  for (let right = 0; right < s.length; right++) {
    if (seen.has(s[right])) left = seen.get(s[right])! + 1;
    seen.set(s[right], right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
```

**Asistente:**

**SÍNTOMA.** `"abba"` devuelve 3, esperado 2.

**TRACE.** Cuatro frames. `left` en azul, ventana válida en verde, el valor que rompe en rojo.

| right | char | seen antes | left | ventana | best |
|---|---|---|---|---|---|
| 0 | `a` | `{}` | 0 | `[a]` | 1 |
| 1 | `b` | `{a:0}` | 0 | `[a,b]` | 2 |
| 2 | `b` | `{a:0,b:1}` | **2** | `[b]` | 2 |
| 3 | `a` | `{a:0,b:2}` | **1** ← rojo | `[b,b,a]` | **3** |

**DIVERGENCIA.** Frame 3. En `right = 3` el char es `a`, y `seen` todavía tiene `a → 0` de la
primera vuelta. Tu línea hace `left = 0 + 1 = 1`, o sea **mueve `left` hacia atrás**, de 2 a 1.
La ventana se agranda para incluir caracteres que ya habías descartado.

El índice que leés de `seen` es de una aparición que quedó fuera de la ventana. El mapa recuerda
para siempre; tu ventana no.

¿Qué condición tendrías que chequear antes de confiar en ese índice?

**Usuario:** que el índice guardado esté dentro de la ventana, o sea que sea >= left

**Asistente:**

Eso. Agregalo y corré `"abba"`, `"pwwkew"` y `""` antes de someter.

---

## Qué mostrar de esto

- El bug se probó con un trace hasta el frame exacto de divergencia. No se dijo "te falta una
  guarda": se mostró `left` bajando de 2 a 1.
- No se reescribió el código ni se mostró la línea corregida. Se nombró la condición que falta
  como pregunta.
- Se pidieron los tres casos de prueba que importan, incluido el vacío.

Registro:

```bash
PY sesion ejercicio --ejercicio 3-longest-substring --tema sliding-window \
  --resultado con_pistas --pista-max 1 --prediccion solo \
  --error-clase "indice-fuera-de-ventana"
```
