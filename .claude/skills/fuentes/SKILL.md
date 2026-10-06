---
name: fuentes
description: Asignar lectura o video a cada tema antes de su sesión de fondo, decidir cuándo hace falta material externo, buscarlo, descargarlo si es de acceso libre, catalogar los PDFs que aporte el usuario, e indexar todo en base/fuentes.md. Usar al cerrar una sesión de fondo, al abrir un tema, cuando el usuario pida una referencia, un libro, un paper o dónde leer más; cuando una explicación necesite una fuente que no está en el proyecto; o cuando deje un archivo en fuentes/. Triggers "dónde leo", "alguna fuente", "un libro", "un paper", "referencia", "buscá en internet", "descargá", "te dejé un PDF", "qué leo", "qué toca leer", "terminé el capítulo".
---

# Fuentes

## Asignar contenido

- Asigná a cada tema una lectura o un video antes de su sesión de fondo, sin esperar a que lo pida.
- Tomá la asignación del "Calendario de lectura" de `base/temario.md`.
- Cubrí con un video de NeetCode el tema que el libro base no trae.
- Escribí capítulos o videos concretos, con mínimo y meta. Nunca "leé sobre X".
- Cuando el calendario se corra, actualizá `base/temario.md` y la colección `semanas` de la página
  de lectura (URL en `AGENTS.md`).
- Usá el libro como guía de temas. No repitas sus explicaciones ni uses sus ejercicios en sesión.
- Elegí libros densos y rigurosos: alta proporción de ideas por página, con formalismo y
  demostraciones cuando aportan. Descartá libros tipo "for dummies" que dedican páginas a explicar
  una sola frase.
- Aceptá videos más verbosos: se consumen de forma pasiva.

## Cuándo buscar afuera

Buscá material externo solo en estos casos:

- El usuario pide una referencia o dónde leer más.
- El tema tiene una fuente canónica que es mejor que cualquier explicación propia: un paper
  original, la documentación oficial, el capítulo de un libro de acceso libre.
- Una explicación propia saldría vaga o insegura sobre un dato factual.
- Hay que verificar un número, una API o un comportamiento del lenguaje.

No busques afuera para explicar un patrón que ya está en `.claude/skills/codigo/referencias-cpp/`.
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
Buscá en los libros con `grep` sobre el `.txt` de su carpeta en `fuentes/`; el índice de capítulos está en `base/fuentes.md`.
Citá siempre la fuente y la fecha cuando uses un dato que salió de ahí.

## Fuentes libres ya conocidas

No hace falta buscarlas: usalas directo.

**Lenguaje**
- cppreference.com — la referencia de C++ y su librería estándar. La canónica.
- learncpp.com — tutorial largo y gratuito, bueno para el modelo de memoria.
- C++ Core Guidelines, de Stroustrup y Sutter — qué es idiomático y por qué.

**Algoritmos y estructuras**
- "Algorithms", de Jeff Erickson — libro completo y gratuito del autor, en jeffe.cs.illinois.edu. Descargado en
  `fuentes/erickson-algorithms/`; complemento del calendario para recursión, backtracking, DP y grafos.
- "Open Data Structures" — libro abierto, en opendatastructures.org.
- MIT OpenCourseWare 6.006, Introduction to Algorithms — clases y apuntes.
- NeetCode — roadmap de patrones, gratis.

**System design**
- "The System Design Primer" — repositorio en GitHub, licencia abierta.
- "Site Reliability Engineering" de Google — libro completo y gratuito, en sre.google/books.
- Centros de arquitectura de AWS y Google Cloud.
- Papers originales de libre acceso: MapReduce, Bigtable, Dynamo, Raft.

**Libros pagos que valen y no se descargan**
- "The Algorithm Design Manual", 3.ª ed., de Steven Skiena. Libro base del calendario de lectura.
  PDF y texto aportados por el usuario en `fuentes/skiena-algorithm-design-manual/skiena-3ed.*`.
- "System Design Interview", vol. 1, de Alex Xu. Solo para practicar el formato de entrevista.
- "Designing Data-Intensive Applications", de Martin Kleppmann. Lectura de system design del calendario.
  Las charlas del autor y sus papers sí son libres.
- "Cracking the Coding Interview".

## Formato del índice

Anotá cada fuente como una fila en `base/fuentes.md`:

| Fuente | Tipo | Temas | Ubicación | Fecha |
|---|---|---|---|---|

`Tipo`: `descargada`, `consultada` o `aportada-por-el-usuario`.
`Ubicación`: la ruta en `fuentes/` o la URL.
`Fecha`: cuándo se descargó o consultó.
