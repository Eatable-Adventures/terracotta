---
tags:
  - recurso
  - design-system
  - presentaciones
aliases:
  - Base fija de presentaciones HTML
  - ea_deck
  - ea_elementos
created: 15-10-2026
actualizado: 03-11-2026
description: >-
  Capa de presentaciones de Terracotta para presentaciones HTML de Eatable Adventures: base fija (portada, cabecera y
  cierre, ea_deck), los 158 elementos visuales del cuerpo de las slides (ea_elementos), su taxonomía por intención,
  las reglas de uso y las referencias oficiales. Es la puerta de entrada: quien no conozca Terracotta empieza aquí.
---

# Presentaciones HTML de Eatable Adventures

> Parte de Terracotta. Se publica en el repositorio con todo el sistema, salvo las notas que citan clientes o material de terceros (ver «Qué no está en el repositorio»). Dos capas: **`ea_deck`** fija las tres piezas que no se rediseñan (portada, cabecera de cada slide y cierre) y **`ea_elementos`** pone todo lo que va en el cuerpo. Desde el 01-11-2026 ya no hay catálogo de composiciones de slide: se eligen elementos por intención y se colocan con reglas generales.

**Versión: Terracotta V2 (01-11-2026), cerrada el 03-11-2026 con todos los elementos validados.** Qué trae, qué se retiró (la capa de PowerPoint), problemas conocidos y propuesta para el repositorio: [[Versiones de Terracotta]]. Para montar, revisar y aprender de un deck desde cualquier sesión, la skill `terracotta` (`~/.claude/skills/terracotta/`), que desde el 02-11-2026 incluye la antigua `/taste`. Tras cualquier cambio en esta carpeta: `python3 verificar.py`.

## Empieza aquí

**Qué es.** Terracotta es el sistema de diseño de Eatable Adventures. Tiene dos partes con una sola regla de color y un solo catálogo de gráficos y mapas, el de esta carpeta. Para hacer presentaciones solo hace falta esta carpeta:

| Parte | Dónde | Para qué | Quién la cambia |
|---|---|---|---|
| **Núcleo** | La carpeta superior: `colors_and_type.css` (tokens), `DESIGN.md` (marca y voz), `Brand Foundations.html`, `Navigation Guidelines.html`, `Charts Catalogue.html`, `Maps Catalogue.html`, `charts/`, `components/` y `ui_kits/` (producto) | La identidad: colores, tipografía, componentes de aplicaciones | Quien mantiene Terracotta, con historial en el repositorio |
| **Presentaciones** | Esta carpeta, `presentaciones/` | Decks, informes y slides en HTML y PDF | El equipo, con las normas de abajo |

**Qué hace falta.**
- Python 3.10 o superior con `pip install pypdf pymupdf numpy pillow pyyaml fonttools`.
- Google Chrome (lo busca en las rutas habituales; si no, `CHROME_PATH`).
- La variable `TERRACOTTA_DIR` con la ruta de esta carpeta. En Claude Code, la skill `terracotta` lleva todo el flujo.
- Para comprobar que todo funciona: `python3 verificar.py`, que tiene que acabar en «Terracotta V2 verificado.». Regenera la galería, la taxonomía y las reglas dentro de esta carpeta, y tarda unos minutos. Fuera del entorno interno omite las referencias, que necesitan sus decks.

**De cero a un deck, en seis pasos.**
1. **Guion antes que slides.** Un md con la historia en una frase y, por slide, el título de acción con su tramo rojo y la pieza prevista. Se valida con quien encarga el deck.
2. **Elegir cada pieza por lo que tiene que decir la slide.** `X.buscar("cadena de valor")`, `X.buscar("logos")` o una intención (`X.buscar("brecha")`) dan las candidatas, que se ven en `Galería de elementos.html`. `X.ayuda("donut")` da sus parámetros, si llena con `H`, cuándo usarla y sus alternativas.
3. **Mirar cómo se resolvió** ese tipo de slide en [[Formatos de slide]] y con `python3 referencias.py`.
4. **Montar con un script** (`build_<deck>.py`, en la carpeta del proyecto): el ejemplo de «Cómo crear una presentación» funciona tal cual.
5. **Revisar:** `python3 revisar_deck.py deck.html --out <carpeta>` da PDF, PNG e informe. Hay que mirar todos los PNG contra las [[Reglas de uso de elementos]]: el informe no ve todo, y cero errores no quiere decir que la slide esté bien. Las marcas de coherencia pueden ser subconjuntos legítimos.
6. **Al cerrar el deck, aprender:** lo que se haya corregido y sirva para el siguiente va a las reglas ([[Registro de criterios]]).

**Dudas frecuentes.**

| Quiero… | Voy a… |
|---|---|
| Saber qué pieza usar | `X.buscar(...)`, [[Taxonomía de elementos]] o `Galería de elementos.html` |
| Saber cómo se coloca y qué norma aplica | [[Reglas de uso de elementos]] (también en PDF, con slides de ejemplo) |
| Traducir un comentario como «baja un poco» | [[Microajustes]] |
| Encontrar un icono | `X.buscar_icono("palabra")` o `Catálogo de iconos.html` |
| Poner logos de empresas | «Logos» en esta nota: `X.muro_logos` y `X.ecosistema_logos` |
| Dudar entre varias opciones visuales | «Laboratorio de variantes» en esta nota |
| Marcar un dato que aún no tengo | `==Por incluir==` en cualquier texto, también en títulos, cifras y rótulos de gráficas: sale marcado y `revisar_deck.py` lo lista. Una gráfica necesita un número: se marca el rótulo y se da un valor provisional |
| Que la slide no quede a medias | «Llenar la slide» en esta nota |
| Saber qué ha cambiado o qué falla | [[Versiones de Terracotta]] |

**Llenar la slide (M11).** Es lo que más cuesta al empezar.

```python
H = X.alto_cuerpo(1, True, 1)                             # líneas de título, subtítulo, líneas de banda
X.fila(X.cascada(..., W=680, H=H),                        # la pieza principal recibe el alto, si acepta H
       X.columna(X.tarjeta_cifra(...), X.tarjeta_cifra(...), repartir=True),   # lo de al lado reparte su alto
       anchos=X.REJILLAS["B"], crecer=True)
```

No todas las piezas aceptan `H`: la galería las marca («acepta H») y `X.llena("pieza")` lo dice. Aceptarlo no garantiza llenar, porque con poco contenido sigue quedando hueco: hay que mirar el PNG. Las demás crecen con `W` (el embudo, además, con el número de etapas), con el cuerpo (`proceso_flechas`, `fases_gates`) o se acompañan con una columna. Centrar es la excepción, y una caja hueca indica que le falta contenido o que sobra la caja.

**Normas que no se negocian.** Títulos enteros en negrita con un tramo rojo y 2 líneas como máximo. Un visual con peso por bloque, con las cifras como etiquetas. El cuerpo llena la slide sin recargarla. Rojo solo para lo que nombra el título. Fechas DD-MM-YYYY y cifras en formato español. Datos que faltan, marcados y nunca inventados. Los datos de un cliente no se usan en material de otro.

## Qué no está en el repositorio

El repositorio `Eatable-Adventures/terracotta` es público. Solo existen en el entorno interno, y por eso sus enlaces no abren en GitHub: las notas de referencias, medición, registro y versiones, `catalogo/`, `referencia/` y `revision/`. Sin ellas, `verificar.py` omite las comprobaciones que las necesitan, `referencias.py` no tiene slides modelo y las tarjetas no llevan la etiqueta de su referencia. El resto funciona igual.

## Qué contiene

| Archivo | Para qué |
|---|---|
| `ea_deck.py` | Base fija: `portada()`, `agenda()`, `portadilla()`, `cabecera()`, `slide()`, `cierre()`, `documento()`, con `idioma="es"` o `"en"`. Todo embebido en base64 (HTML autocontenido) |
| `ea_elementos/` | Paquete con los 158 elementos visuales en 14 familias, un módulo por familia, más `base.py` (tokens, primitivas, `Lienzo`, CSS, `cuerpo_slide`, `fila`, `columna`), `taxonomia.py`, `iconos.py` y `embudo_canonico.py` (el embudo de discos apilados, antes `pptx/funnel.py`) |
| [[Taxonomía de elementos]] | Menú por intención (qué elemento para cada mensaje), con escala, datos y alternativas. Lo genera `build_galeria_elementos.py`; no se edita a mano |
| [[Reglas de uso de elementos]] | El único documento de reglas para montar y revisar: selección, maquetación, encaje, color, tipografía, peso visual, tono, contenido, base fija, ilustración, iconos y medición |
| [[Formatos de slide]] | Para cada tipo de mensaje: estructura, pieza, qué evitar y slide modelo |
| [[Microajustes]] | De los comentarios de revisión («baja un poco», «mismo alto») a un cambio con su valor |
| [[Registro de criterios]] | Una línea por cambio en las reglas y los criterios |
| `Catálogo de iconos.html` | Los 435 iconos del catálogo por temas, con buscador, nombre y palabras clave; versión de Obsidian en [[Catálogo de iconos]] |
| `Galería de elementos.html` | Todos los elementos con datos ficticios, índice por intención y, en cada tarjeta, escala, cuándo usarlo, cuándo no y alternativas |
| `Reglas de uso de elementos.html` | Nueve slides de ejemplo que aplican M11: una por rejilla (A a F), una ficha de actor en cuadrantes y dos de ilustración isométrica (`build_reglas_uso.py`) |
| `build_galeria_elementos.py` | Genera la galería y la taxonomía; se para si la taxonomía y el código no cuadran |
| `verificar.py` | Verificación de la versión: importación, taxonomía, galería e iconos, PDF de las reglas, prueba de humo de la base fija, medición y referencias |
| `build_nucleo.py` | Genera desde estas piezas las tarjetas de gráficos y mapas del panel (`preview/`) y `Charts Catalogue.html`, para que haya una sola fuente. No se editan a mano |
| `laboratorio.py` | Enseña varias opciones de una misma slide con los mismos datos, para que elija quien encarga el deck (ver «Laboratorio de variantes») |
| `auditar_galeria.py` | Mide cada tarjeta de la galería: textos que se solapan, se salen o quedan cortados. Lo ejecuta `verificar.py` |
| `revisar_deck.py` | La revisión objetiva en un comando: PDF, páginas, PNG, inspección del HTML (`inspeccionar_dom.py`) y medición del PDF, en un solo informe |
| `medir_deck.py` y [[Medición de decks]] | Mide un deck en PDF (llenado, densidad, legibilidad, equilibrio, coherencia y hermanas) frente a los rangos de `calibracion_decks.json`, sacados de decks de referencia |
| `huella_slide.py` | Huella anónima de una slide en PNG para la biblioteca de referencias del OS: quita texto e imágenes, cambia por una caja gris lo que parece un logo vectorial y da las cifras de `medir_deck.py`. Una persona confirma cada huella antes de publicarla |
| [[Versiones de Terracotta]] | Historial de versiones de esta capa (V1 y V2) |
| [[Referencias de Terracotta]] y `referencias.py` | Índice de todas las referencias oficiales y cuándo actúa cada una. Decks de densidad y slides modelo por tipo (`python3 referencias.py ficha --png <scratchpad>`). Cita clientes: es solo interna |
| `catalogo/` | Referencias externas fichadas (R01 a R16), solo como datos, con la pieza que salió de cada una: [[catalogo/Índice de referencias\|Índice de referencias]] |
| `generar_fondo_portada.py` | Regenera `assets/cover-background.png` desde los tokens de `colors_and_type.css` |
| `assets/` | Fondo de portada, lockup crema, glow, candado, wordmark, fuentes (Rubik y Material Symbols: base, catálogo y completa) y `geo/countries-110m.json` (world-atlas 2.0.2, para `mapa_coropletico`) |
| `referencia/` | Lista de decks para calibrar, zip original del sistema de referencia de la portada y plantilla de timelines |

## Elementos visuales (`ea_elementos`)

- **Familias y módulos:** magnitud, evolucion, composicion, comparacion, distribucion, marcos, arboles, cadena (cadena de valor y escenas isométricas), secuencia, cifras, fichas, marcas, tablas y sintesis. `import ea_elementos as X` da acceso a todo.
- **Elegir:** por intención, nunca por costumbre. `X.buscar("brecha")` da todas las candidatas de una intención y `X.buscar("cadena de valor")` busca en lenguaje natural. Detalle en [[Reglas de uso de elementos]], sección 1.
- **Colocar:** seis rejillas (`X.REJILLAS`, `X.fila()`), cuerpo de 1152 px de ancho, tamaño con el parámetro `W` de cada función y nunca con CSS.
- **Llenar (02-11-2026):** el cuerpo llena visualmente la mayoría de las slides sin recargarlas. `X.alto_cuerpo(líneas_de_título, subtítulo, banda, nota)` da el alto disponible para pasárselo a las piezas que aceptan `H`; `X.columna(..., repartir=True)` y `X.fila(..., crecer=True)` reparten el sobrante. Centrar con `align-items:center` es la excepción. Regla M11 de las [[Reglas de uso de elementos]].
- **Mirar la referencia (S6):** antes de maquetar un tipo de slide con referencia, verla con `referencias.py`. Se toma la forma, no el contenido.
- **Dato pendiente:** en cualquier texto, `==Por incluir==` sale marcado (`ea_deck.documento` lo resuelve, también en gráficas) y `revisar_deck.py` lo lista.
- **Añadir un elemento:** la función en el módulo de su familia (con docstring de cuándo usarlo y cuándo no), su ficha en `taxonomia.FICHAS`, su nombre en `taxonomia.FAMILIAS` y un ejemplo en `build_galeria_elementos.py`. La galería no se genera si falta algo.
- **Portadillas de secciones que no son un eslabón:** las escenas `comunicacion`, `hoja_de_ruta` y `alianzas`. Las fotos van con el proyecto, con licencia libre y su origen en `FUENTES.md`; no hay banco común porque una foto genérica no cumple D7.
- **Añadir una escena isométrica:** función con `@escena(nombre, descripción, eslabón, alto)` en `ea_elementos/cadena.py`; aparece sola en el catálogo y se puede usar en `cadena_isometrica` y `escena_iso`.
- **Historial:** `ea_visuals.py` (composiciones de slide) y `ea_elementos.py` se fundieron en el paquete el 01-11-2026, con salida idéntica comprobada byte a byte. Copia de los archivos anteriores en `04. Archivos/Terracotta presentaciones - copia 01-11-2026/`.

## Logos

- **Dónde viven.** Con el proyecto, en `assets/logos/` junto al generador, y cada uno con su origen en un `FUENTES.md` en esa carpeta. Nunca en `presentaciones/`: las piezas son generales.
- **De dónde salen.** Primero la web oficial o su kit de prensa; después Wikimedia Commons. A color, en SVG o PNG con fondo transparente o blanco (regla D6).
- **Cómo se ponen.** `X.muro_logos([("Empresa", "assets/logos/empresa.png"), ...], columnas=6, W=1152, H=H)` para un grupo, y `X.ecosistema_logos([dict(rotulo="Partners", actores=[...], estado="Firmados", destacado=True), ...], H=H)` para todo el universo por fases o tipos. Si falta un logo sale el nombre en texto, y se ve qué queda por conseguir sin romper la slide.
- **Sin logos todavía.** El muro sale con el nombre en teselas huecas: sirve como borrador, no para entregar. Si no van a llegar, mejor `X.categorias_chips` o `X.ficha_linea`.
- **Sin inventar quién está.** Una organización entra solo si una fuente del proyecto dice que está.

## Laboratorio de variantes

Cuando una slide admite varias soluciones razonables y la elección es de gusto, no se decide a ciegas: se enseñan de 2 a 5 opciones con los mismos datos y elige quien encarga el deck (regla S7).

```python
import laboratorio
variantes, descartadas = laboratorio.opciones_cadena(eslabones, destacado=1)   # las opciones de cadena de valor posibles con esos datos
if len(variantes) >= 2:
    laboratorio.generar("Cadena de valor", variantes, "Laboratorio visual — Cadena de valor (DD-MM-YYYY).html")
```

Si los datos solo dan una opción, no hace falta laboratorio: se usa esa y `descartadas` dice qué faltaba para las otras.

Para cualquier otra slide, `generar` recibe una lista de `dict(nombre, gana, pierde, html)`. El laboratorio va junto al generador, nunca dentro del deck. Cadena de valor: guía de elección en [[Formatos de slide]].

## Cómo crear una presentación

El ejemplo funciona tal cual (`verificar.py` lo ejecuta en cada comprobación).

```python
import os, sys
sys.path.insert(0, os.environ["TERRACOTTA_DIR"])   # la carpeta presentaciones/; el generador no lleva rutas de ninguna máquina
import ea_deck, ea_elementos as X

slides = [ea_deck.portada(linea1="Alineación de alcance", linea2="Cliente Demo",
                          subtitulo="Del diagnóstico al piloto",
                          realizado_para="Cliente Demo", equipo="Nombre Apellido",
                          fecha="Octubre 2026")]
H = X.alto_cuerpo(1, True, 1)                      # el alto disponible: líneas de título, subtítulo, líneas de banda
cuerpo = ea_deck.cabecera("01. Sección", 'Conclusión con <span class="hl-red">tramo en rojo</span>') + X.cuerpo_slide("Subtítulo", X.fila(X.embudo([("Universo", "Candidaturas", "120"), ("Filtro", "Encajan", "40"), ("Entrevistas", "Con el equipo", "12"), ("Comité", "Evaluados", "8"), ("Final", "Elegidos", "5")], clave=4, W=680), X.contadores([("120", "Candidatos", "Recibidos en la convocatoria"), ("40", "Pasan el filtro", "Encajan en los criterios"), ("5", "Finalistas", "Elegidos por el comité")], H=H, destacado=2), anchos=X.REJILLAS["B"], crecer=True), banda="Conclusión con **negrita**.")
slides.append(ea_deck.slide(cuerpo, n=2, total=3, fuente="Fuente: ...", cliente="Cliente Demo"))
slides.append(ea_deck.cierre("Mensaje clave en una frase.", "Cliente Demo"))
open("salida.html", "w", encoding="utf-8").write(ea_deck.documento("Título", slides, css_extra=X.CSS + X.fuente_iconos()))
```

Ejemplo completo: `build_reglas_uso.py`, con una slide por rejilla.

## Portada (L01), especificación

Tomada del sistema de referencia de la portada (10 × 5,625 in) y escalada a 1280 × 720 px (128 px por pulgada). Todo alineado en un único eje vertical a x ≈ 2,5 in, a la derecha del glow.

| Capa | Contenido | Posición y tamaño (px) |
|---|---|---|
| 1 | Fondo `cover-background.png`, a sangre | -8, -6 · 1300 × 732 |
| 2 | Logo crema | 315, 35 · 298 × 60 |
| 3 | Título, 2 líneas, Rubik 700, 44 px, frase normal (nunca en mayúsculas), crema | 319, 200 · 836 de ancho |
| 4 | Subtítulo, Rubik 400, 27 px, crema | 319, 347 · 804 de ancho |
| 5 | Metadatos 2 × 2, etiquetas 700 a 12,5 px y valores 400 a 16 px | columnas en x = 323 y 689; filas en y = 481 y 548 |
| 6 | Línea vertical blanca de 1 px | 655, 486 · alto 106 |
| 7 | Copyright 12,5 px | 319, 672 |

- **Título:** línea 1 = tipo de entregable; línea 2 = cliente o proyecto. Máximo ~22 caracteres por línea; si no cabe, acortar, no reducir el tamaño. **Norma (15-10-2026):** el título va en frase normal, nunca en mayúsculas, a 44 px y a 200 px del borde superior (antes 50 px, MAYÚSCULAS y 180 px). Cambiado en `ea_deck.py`: todas las portadas nuevas lo heredan.
- **Subtítulo:** una línea, bloques separados por ` · `, frase normal, sin punto final.
- **Etiquetas e idioma (01-11-2026):** todas en el idioma del deck, también el copyright: en español «Realizado para», «Fecha», «Equipo», «Clasificación» (por defecto «Confidencial») y «© 2026 Eatable Adventures. Todos los derechos reservados.»; en inglés («idioma="en"») «Prepared for», «Date», «Consultant Team», «Classification» y «Private & Confidential». Sustituye a la norma anterior de mezclar idiomas.
- **Fecha:** mes con la primera letra en mayúscula y año (`Octubre 2026`). Norma del 15-10-2026.
- **Equipo (01-11-2026 y 02-11-2026):** las personas reales del proyecto, tal como figuran en la sección «Equipo» de su PM, una por línea (`equipo=[...]`); si no consta, se pregunta; con más de dos líneas, el bloque de metadatos sube 24 px para dejar aire sobre el copyright. «Delivery Excellence» solo si quien encarga el deck lo pide.
- **Nunca en la portada:** fotos, logos de cliente, iconos, ilustraciones, colores extra (solo crema y blanco sobre burgundy), número de página, pie con sección, título de acción ni glow delante del título.
- No dibujar la portada con un degradado CSS ni con un relleno sólido: siempre `cover-background.png`. Sus franjas verticales son de marca, no un defecto.

## Cabecera de las slides de contenido

- Eyebrow gris en frase normal con número de sección (`01. Proteína funcional`), y a su derecha las píldoras de estado si hacen falta.
- Título entero en negrita (700), tanto la parte negra como el tramo conclusivo en rojo (`.hl-red`). Máximo 2 líneas. **Norma (28-10-2026):** los títulos van siempre en negrita completa; manda sobre la regla de Terracotta de titulares en Regular (antes 600 con el rojo en 700).
- Glow ámbar (`amber-glow.png`) a la izquierda del título, detrás del texto, nunca un punto sólido.
- **Alineación (28-10-2026):** eyebrow, título y subtítulo empiezan en el mismo eje vertical (margen izquierdo de la slide, sin sangría del título). El glow queda centrado unos 6 px a la izquierda de la primera letra (`.glow{left:-81px}`), no detrás de ella. La fila del eyebrow tiene altura fija (22 px), así que una píldora de estado o un eyebrow vacío no desplazan el título.
- Logo wordmark arriba a la derecha. El título no debe pasar por debajo del logo.
- Pie: fuente a la izquierda, sin fechas; a la derecha `Confidencial · Solo para uso de {cliente} · n / total`, sin «Eatable Adventures» (01-11-2026).

## Agenda (01-11-2026)

`agenda(secciones, subtitulo)`: el formato del Google Slides de EA (28-10-2026). A la izquierda, el rótulo rojo «Estructura del documento», «AGENDA» a 64 px con el glow y un subtítulo en cursiva; una línea vertical; a la derecha, las secciones numeradas en rojo con una línea de descripción y separadores. Sin pie. Con más de cinco secciones pasa a la versión densa.

## Portadillas de sección (01-11-2026)

`portadilla(numero, titulo, subtitulo, foto=... | visual_html=...)`: foto a sangre en color con la tarjeta blanca abajo a la izquierda (número a 72 px en rojo y peso 300, título en negrita y subtítulo). La foto tiene que mostrar el objeto del proyecto (D7) y registrar su origen. Si no hay una foto así, la misma tarjeta sobre fondo gris claro con una escena isométrica del eslabón a la derecha (`visual_html=ea_elementos.escena_iso(...)`), según la regla I1 de [[Reglas de uso de elementos]].

## Cierre

Izquierda blanca (40%): "Gracias." ("Thank you." en inglés), un próximo paso opcional (`siguiente="Siguiente entrega"`, 01-11-2026) y un callout con el mensaje en una o dos frases (gris claro `--surface-fill`, por B3, borde rojo de 3 px), sin la etiqueta "Mensaje clave" (29-10-2026) y con `**negrita**` para destacar una parte. Derecha (60%): degradado de marca de Terracotta, "Let's Beat", wordmark y confidencialidad. Va siempre como última slide, aparte de la slide de decisión.

- **Verde de validación (29-10-2026):** `--validacion: #2F7D4A`, definido en `CSS_BASE`. Solo para estados de validación (favorable, validado, aprobado), nunca como color de marca ni de series. Vive en esta capa de presentaciones y no en `colors_and_type.css`, que se sobrescribe al sincronizar con el repositorio de Terracotta.
- **"Let's Beat" centrado en altura (29-10-2026):** `.cl-right h2{top:50%;transform:translateY(-50%)}`, a 64 px del borde izquierdo de la mitad derecha. Antes estaba a la altura de "Gracias." (`top:228px`).

## De dónde sale la portada

- **Se toma:** la ejecución (fondo como imagen en capas, activos PNG, posiciones, jerarquía y reglas de qué no va en la portada) y los activos neutros de paleta (lockup crema, glow, candado).
- **No se toma:** su tabla de colores. En su SKILL el burgundy es `#5C0F0F` y el ámbar `#F39C2A`; en Terracotta son `#450E14` y `#FFA103`. El PNG de portada original ya usa en la práctica `#450E14` y un núcleo `#FD9E05`, pero el fondo se regenera desde nuestros tokens para que cualquier cambio de paleta se propague (diferencia media con el original: 2,9 sobre 255).
- Su cabecera de PowerPoint (spark a 0,24 in) se adapta a HTML.

## Verificación antes de entregar

0. Si se ha tocado algo de esta carpeta: `python3 verificar.py` (tiene que acabar en «Terracotta V2 verificado.»).
1. Exportar a PDF con Chrome headless: lo hace `revisar_deck.py` (paso 3).
2. Contar páginas del PDF y compararlas con las slides del HTML (el bug de páginas duplicadas aparece si `@page` lleva margen).
   - Medir el PDF con `python3 medir_deck.py deck.pdf` y mirar lo que marque: una marca es para mirarla, no un error ([[Medición de decks]]).
3. Renderizar cada página a PNG y revisarla (desbordes, logo contra título, cifras). `python3 revisar_deck.py deck.html --out <scratchpad>` hace los pasos 1 a 3 y da un solo informe.
4. Iconos: solo los del catálogo (`ea_elementos/iconos.py`, 435 de Material Symbols Outlined a peso 300, por temas y con palabras clave en español; página visual en `Catálogo de iconos.html`). `icono()` falla si el nombre no está, en vez de pintarlo como texto, y `comprobar_iconos(html)` revisa un HTML entero. Para añadir uno: buscarlo en fonts.google.com/icons, sumarlo a `iconos.py` y ejecutar `build_galeria_elementos.py`, que regenera en local `assets/fonts/material-symbols-ea.woff2` a partir de la fuente completa (`material-symbols-completo-300.woff2`, origen y licencia Apache 2.0 en `assets/fonts/LICENCIA material-symbols.md`). Ya no hace falta la API de Google Fonts.
   - `ea_deck.fuentes()` sigue incrustando el subconjunto base de 22 iconos (`material-symbols-subset.woff2`) para los documentos que no usan `ea_elementos`; con `X.fuente_iconos()` en el CSS se sustituye por el del catálogo.
