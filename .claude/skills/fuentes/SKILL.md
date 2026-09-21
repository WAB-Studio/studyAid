---
name: fuentes
description: Decidir cuándo hace falta material externo, buscarlo, descargarlo si es de acceso libre, catalogar los PDFs que aporte el usuario, e indexar todo en base/fuentes.md. Usar cuando el usuario pida una referencia, un libro, un paper o dónde leer más; cuando una explicación necesite una fuente que no está en el proyecto; o cuando deje un archivo en fuentes/. Triggers "dónde leo", "alguna fuente", "un libro", "un paper", "referencia", "buscá en internet", "descargá", "te dejé un PDF".
---

# Fuentes

## Cuándo buscar afuera

Buscá material externo solo en estos casos:

- El usuario pide una referencia o dónde leer más.
- El tema tiene una fuente canónica que es mejor que cualquier explicación propia: un paper
  original, la documentación oficial, el capítulo de un libro de acceso libre.
- Una explicación propia saldría vaga o insegura sobre un dato factual.
- Hay que verificar un número, una API o un comportamiento del lenguaje.

No busques afuera para explicar un patrón que ya está en `.claude/skills/codigo/referencias-ts/`.
No busques afuera en una micro-sesión.
No interrumpas un ejercicio en curso para buscar una fuente: anotalo y buscá al cerrar.

## Qué es aceptable traer

Descargá a `fuentes/` únicamente material de acceso libre: documentación oficial, libros
publicados gratis por sus autores, apuntes de cursos universitarios abiertos, papers,
repositorios con licencia abierta.

No busques copias pirata de libros pagos. Cuando la mejor fuente sea un libro pago, decilo,
nombralo, y ofrecé la alternativa libre más cercana.

Cuando el usuario deje un PDF en `fuentes/`, catalogalo sin preguntar de dónde salió.

## Qué hacer con lo que traés

Guardá los archivos en `fuentes/` con nombre descriptivo en kebab-case.
Anotá toda fuente en la tabla de `base/fuentes.md`, incluidas las que solo consultaste sin descargar.
Enlazá la fuente desde `base/temas/<tema>.md` en su sección de fuentes.
Pasá al usuario el extracto relevante, no el archivo entero.
Si dice que ya consumió el material por su cuenta, preguntale cuántos minutos le dedicó y
registralo con `PY externo agregar`. Indexarlo en `base/fuentes.md` no es registrarlo como tiempo:
son dos cosas distintas y hacen falta las dos.
Citá siempre la fuente y la fecha cuando uses un dato que salió de ahí.

## Fuentes libres ya conocidas

No hace falta buscarlas: usalas directo.

**Lenguaje**
- MDN Web Docs — la referencia de JavaScript y su librería estándar. La canónica.
- El handbook de TypeScript (typescriptlang.org/docs/handbook) — tipos, `strictNullChecks`.
- "You Don't Know JS Yet", de Kyle Simpson (gratis en GitHub) — coerción, tipos, `this`.

**Algoritmos y estructuras**
- "Algorithms", de Jeff Erickson — libro completo y gratuito del autor, en jeffe.cs.illinois.edu.
- "Open Data Structures" — libro abierto, en opendatastructures.org.
- MIT OpenCourseWare 6.006, Introduction to Algorithms — clases y apuntes.
- NeetCode — roadmap de patrones, gratis.

**System design**
- "The System Design Primer" — repositorio en GitHub, licencia abierta.
- "Site Reliability Engineering" de Google — libro completo y gratuito, en sre.google/books.
- Centros de arquitectura de AWS y Google Cloud.
- Papers originales de libre acceso: MapReduce, Bigtable, Dynamo, Raft.

**Libros pagos que valen y no se descargan**
- "Designing Data-Intensive Applications", de Martin Kleppmann. Para system design es el mejor.
  Las charlas del autor y sus papers sí son libres.
- "Cracking the Coding Interview".

## Formato del índice

Anotá cada fuente como una fila en `base/fuentes.md`:

| Fuente | Tipo | Temas | Ubicación | Fecha |
|---|---|---|---|---|

`Tipo`: `descargada`, `consultada` o `aportada-por-el-usuario`.
`Ubicación`: la ruta en `fuentes/` o la URL.
`Fecha`: cuándo se descargó o consultó.
