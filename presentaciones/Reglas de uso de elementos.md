---
tags:
  - recurso
  - design-system
  - presentaciones
aliases:
  - Reglas de Terracotta
  - Reglas de maquetación de slides
  - Cómo usar ea_elementos en una slide
  - Criterios de EA para presentaciones
created: 01-11-2026
actualizado: 03-11-2026
description: >-
  Todas las reglas de Terracotta para montar y revisar una slide de Eatable Adventures, en un solo sitio: selección,
  maquetación, encaje, color, tipografía, peso visual, tono, contenido, base fija, ilustración, iconos y medición, con
  cómo se detecta y se arregla cada una. Funde las antiguas reglas de uso y los criterios de /taste (02-11-2026).
---

# Reglas de uso de elementos

> Parte de Terracotta V2, capa de presentaciones. **Es el único documento de reglas:** desde el 02-11-2026 recoge también los criterios de la antigua skill `/taste`, salvo lo que haya en la tabla de códigos retirados. [[Taxonomía de elementos]] dice qué elemento responde a cada mensaje, [[Formatos de slide]] cómo se estructura cada tipo de mensaje, y estas reglas cómo se monta y se revisa. Ejemplos aplicados: `Reglas de uso de elementos.html` (`build_reglas_uso.py`).

**Sin casos concretos (02-11-2026).** Estas reglas, los formatos, los microajustes y los ejemplos son generales: no nombran ningún cliente, proyecto ni caso, y sus ejemplos se inventan, sin adaptar cifras ni frases de un deck real. Lo que cita clientes está solo en [[Referencias de Terracotta]] y [[Medición de decks]], que son solo internas. Los nombres del equipo de EA sí se incluyen: en la autoría de las reglas y en cada deck, donde el equipo de la portada sale del PM de su proyecto (G1).

No hay composiciones fijas. Cada slide se monta con elementos sueltos siguiendo estas reglas, así que dos slides con el mismo mensaje pueden verse distintas si los datos lo piden.

**Cómo se lee.** Cada regla tiene un código estable y, cuando hace falta, por qué importa, cómo se detecta (`insp:tipo` es un aviso de `inspeccionar_dom.py`, `med:dimensión` una marca de `medir_deck.py`, ambos en `revisar_deck.py`; PNG o texto cuando hay que mirarlo), el arreglo por defecto y su modo.

**Precedencia.** Lo que pida quien encarga el deck manda sobre estas reglas; estas reglas mandan sobre los valores por defecto del núcleo (por ejemplo, el título va entero en negrita aunque el núcleo diga Regular).

**Modo: qué se aplica y qué se propone.** La frontera es si el cambio altera **lo que se dice** o solo **cómo se ve**.

- **Aplica sola (forma):** alturas, alineaciones, centrados, aire, tamaños de letra, mayúscula inicial, negritas, formatos numéricos y de fecha, unidades homogéneas, erratas, gris claro en lugar de crema o amarillo, esquinas, iconos de la familia correcta, logos del mismo alto, quitar referencias internas tipo «(slide 18)», y pasar las piezas fijas (portada, cabecera, pie, cierre) a las de `ea_deck` conservando el cuerpo de cada slide (G1). Lo aplica y lo lista.
- **Propone (contenido y estructura):** reescribir títulos, bandas o conclusiones, renombrar rótulos, quitar o añadir datos, eliminar o fusionar slides, cambiar el formato de una slide, cambiar colores con significado (categorías, estados), cualquier cosa que comprometa al equipo ante el cliente. Lo deja escrito y listo para aplicar con un ok.

El motivo: la forma es criterio de oficio y conviene resolverla sin fricción; el mensaje de un deck de cliente es responsabilidad de quien lo presenta y no se cambia sin que lo vea. En caso de duda, propón.

**Arreglar con la pieza, no con CSS.** Si la pieza tiene `W` o `H`, el ajuste se hace ahí (M3). Los arreglos con CSS de esta nota y de los [[Microajustes]] son para lo que no sea una pieza.

Orden habitual para revisar una slide (útil para priorizar): título y fragmento rojo → peso visual → alturas y aire → repetidos y centrado → alineación con la gráfica → color → mayúsculas y negritas → cifras y formatos → jerga → conclusión → logos → compromisos y contradicciones → desbordes.

## 1. Selección: por intención, no por costumbre

- **S1 · Frase primero.** Antes de elegir nada, escribir en una frase lo que la slide tiene que decir. Esa frase es el título (con su tramo rojo) y fija la intención.

- **S2 · Todas las candidatas.** `taxonomia.buscar(intención)` o la tabla de [[Taxonomía de elementos]] dan todas las piezas que responden a esa intención. Se leen todas, también las de «también sirven», y se descarta con un motivo concreto: forma de los datos, número de elementos, escala o «Cuándo no».

- **S3 · Lo genérico necesita razón.** Columnas, barras, anillo y tabla son la última opción, no la primera. Si se eligen, que sea porque las alternativas específicas (mancuerna, cascada, mapa de calor, árbol de drivers…) no encajan, y se puede decir por qué.

- **S4 · Variedad en el deck.** Ningún elemento aparece en más de tres slides del mismo deck, salvo las slides hermanas (fichas de candidato, territorios), que comparten plantilla a propósito (las hermanas sí comparten plantilla: un solo esqueleto, mismos ejes y misma escala). No se repite la misma rejilla de tarjetas en todo el deck. Dos slides seguidas no repiten familia si no son hermanas.
  - Modo: propone.

- **S5 · Sin pieza, se compone; no se improvisa.** Si ninguna pieza encaja, se combina con las existentes. Si de verdad falta una, se crea en el módulo de su familia con su ficha en la taxonomía y su ejemplo en la galería; nunca se dibuja a mano dentro del script de un deck. Lo mismo al revisar: si el defecto está en una pieza, se arregla en la pieza con un parámetro opcional (`CLAUDE.md` de la carpeta), no con CSS suelto en el deck.

- **S7 · Si la elección es de gusto, se enseñan opciones (03-11-2026).** Si varias piezas responden igual de bien al mensaje, no se decide a ciegas: de 2 a 5 opciones con los mismos datos, cada una con lo que gana y lo que pierde (`laboratorio.py`), y elige quien encarga el deck. Sin duda real, se elige y se dice por qué.
  - Modo: propone.

- **S6 · Mirar antes de maquetar (02-11-2026, al hacer oficiales las referencias).** Si el tipo de slide tiene referencia, se mira antes de componerla: `python3 referencias.py <tipo> --png <scratchpad>` ([[Referencias de Terracotta]]). Se toma la forma y la densidad, nunca el contenido ni el estilo antiguo. No es una plantilla: si los datos piden otra forma, manda S1.

## 2. Maquetación: rejillas, escala y jerarquía

**El lienzo.** Slide de 1280 × 720 con márgenes de 64 px: el cuerpo tiene **1152 px de ancho** (`ANCHO_CUERPO`). Bajo la cabecera y el subtítulo, y por encima de la banda y el pie, quedan unos 400 a 440 px de alto (unos 500 sin banda). `X.alto_cuerpo()` da ese alto exacto para pasárselo a las piezas (M11).

- **M1 · Una protagonista.** Cada slide tiene una pieza protagonista (escala M grande o L) y, como mucho, dos o tres piezas de apoyo (escala S). Si hay dos protagonistas que compiten, son dos slides.
- **M2 · Seis rejillas tipo.** El cuerpo se reparte con una de estas rejillas (`REJILLAS` y `fila()` en `ea_elementos`), separadas por 28 px entre columnas y 14 px entre filas (`HUECO`):

| Rejilla | Anchos (px) | Para qué |
|---|---|---|
| A · Pieza a todo ancho | 1152 | Una pieza L que lo dice todo: árbol de drivers, matriz de puntuación, cadena, Gantt |
| B · Pieza y lectura | 680 + 444 | Una gráfica M y, al lado, la lectura: contadores, tarjetas con cifra, lista numerada. La lectura puede ir a la izquierda |
| C · Dos hermanas | 562 + 562 | Dos piezas del mismo tipo o que se comparan, con rótulo de bloque cada una y la misma escala si comparten unidad |
| D · Cifras y pieza | 1152 (fila de 3 o 4 cifras) + 1152 | Una fila de KPI arriba y la pieza que los explica debajo |
| E · Tres columnas | 365 × 3 | Tres fichas, opciones o escenarios hermanos con la misma plantilla. Si son escenarios, el de referencia (normalmente el central) va destacado con `tarjetas_escenario` |
| F · Contexto y pieza | 360 + 764 | `columna_contexto` a la izquierda (rótulo en píldora, dos o tres párrafos y una cifra ancla al pie) y la pieza que explica a la derecha: un embudo, un Gantt, un mapa, un dimensionamiento |

- **M3 · La escala manda el sitio.** Una pieza S va dentro de una tarjeta, una celda o junto a otra pieza, nunca sola en medio de la slide. Una M ocupa una columna de las rejillas B o C. Una L va a todo ancho. El tamaño se ajusta con el parámetro `W` (y `H`) de cada función, **nunca escalando con CSS**, porque eso cambia el tamaño de la letra (C8).

- **M7 · Fuente en el pie, leyenda solo si hace falta.** La fuente va en el pie de `ea_deck`, no bajo la gráfica. La leyenda solo aparece cuando la etiqueta directa no cabe; si hay leyenda, va arriba a la izquierda de su pieza.

- **M9 · Bloques de texto con filete.** Cuando una slide tiene dos o tres bloques de texto que se leen por separado, cada uno va en un `bloque()` con filete superior: rojo para el bloque que importa y negro para los demás. Nunca más de tres bloques de texto sin un visual (D1).

- **M10 · Slides hermanas de actor en cuadrantes.** Para fichas de competidor, proveedor o candidato que se repiten (de 4 a 12 slides), rejilla C en dos filas con rótulo de bloque en cada cuadrante: arriba la descripción (`bloque` o puntos) y lo que ofrece (`matriz_portfolio`); abajo las cifras (`combo_financiero`) y la valoración (`score_dimensiones`). El logo del actor va en el título, a la derecha, y todas las fichas usan el mismo orden, los mismos ejes y la misma escala (S4, A5).

- **M11 · El cuerpo llena la slide, sin recargarla (02-11-2026).** La mayoría de las slides llenan el alto disponible: el visual empieza justo bajo el subtítulo y llega hasta la banda o el pie. Se hace con contenido y con el tamaño de las piezas (`H=X.alto_cuerpo(...)`, `columna(repartir=True)`, `fila(crecer=True)`), no estirando tarjetas vacías: si una caja se ve hueca, le falta contenido o sobra la caja. Referencia de densidad: los rangos de Q1 a Q4.
  - **Si la pieza no acepta `H`** (`X.llena("pieza")` lo dice; la galería las marca): su alto sale de `W`, de sus datos o del cuerpo. Primero se sube `W` y, si sobra alto, se acompaña: `X.fila(pieza, X.columna(a, b, repartir=True), anchos=..., crecer=True)`.
  - **Aceptar `H` no garantiza llenar:** con poco contenido sigue quedando hueco. Se mira en el PNG.
  - **Centrar es la excepción:** solo si la pieza no puede crecer y no hay nada útil que añadir, con `estilo_vis="align-items:center"`. El aviso `insp:llenado` sigue saliendo, y se justifica en la verificación.
  - Por qué: un cuerpo que flota o se queda a medias parece una slide a medio llenar.
  - Detección: `insp:llenado`, `med:llenado`; PNG.
  - Arreglo: dar a la pieza el alto disponible. Si sobra mucho (más de 120 px), no es un problema de colocación sino de contenido: suplementar con información útil, redistribuir, añadir un visual o proponer quitar la slide (F1). No se usa `align-items:center` en el cuerpo. Si de verdad una pieza no puede llenar (pocos datos y nada útil que añadir), se centra como excepción mirada, nunca pegada arriba con un hueco abajo. En slides hermanas manda que arranquen todas a la misma altura (S4).
  - Modo: aplica (tamaños y reparto); propone (contenido nuevo o quitar la slide).

## 3. Encaje

**A1 · Columnas del mismo alto.** Las columnas hermanas (izquierda y derecha, tres tarjetas en fila) acaban a la misma altura y empiezan a la misma altura. Dos gráficas lado a lado alinean su eje base (`fila(..., alinear="flex-end")`).
- Por qué: es el comentario que más se repite. Un desfase de 20 px se lee como descuido aunque nadie sepa decir por qué.
- Detección: `insp:alto`, `insp:arranque`; PNG.
- Arreglo: si el desfase es grande (más de 40 px), primero rebalancea los anchos de las columnas (la que sobra de alto se ensancha, la otra se estrecha) y el padding de sus filas; después, contenedor en fila con `align-items:stretch` y las tarjetas como columna flex con el contenido repartido (`justify-content:space-between`) o centrado; si una columna es lista, igualar el número de filas o el interlineado; en último caso, `min-height` igual al de la más alta. No estirar texto para rellenar: mejor centrar el bloque corto en su caja.
- Modo: aplica.

**A3 · Centrado a lo alto dentro de filas y tarjetas.** Pasos, iconos, logos, criterios y textos cortos van centrados en vertical en su fila o tarjeta.
- Detección: PNG.
- Arreglo: `align-items:center` en filas; tarjeta como columna flex con `justify-content:center`; en SVG, calcular `y` por el centro y usar `dominant-baseline:middle`.
- Modo: aplica.

**A4 · Alinear con el elemento de referencia.** Las tarjetas laterales acaban en el eje x de la gráfica (no en el final del SVG), una ficha lateral baja hasta la última fila de la tabla, dos listas paralelas empiezan y acaban a la misma altura.
- Por qué: el ojo alinea con la línea visible (el eje, la última fila), no con la caja invisible del gráfico.
- Detección: `insp:eje` (aviso informativo) y PNG.
- Arreglo: primero con `H` de la pieza; si no, calcular la coordenada del eje dentro del SVG y dar a la tarjeta `height = ejeY - top`; o mover el contenido del SVG para que su eje coincida con el final de la caja.
- Modo: aplica.

**A5 · Elementos repetidos idénticos.** Disparadores, tarjetas, píldoras, bloques de «reto» o «quién lo hace»: mismo ancho, mismo alto, mismo padding, centrados.
- Detección: `insp:repetidos`; PNG.
- Arreglo: tamaño fijo o `flex:1` con `min-height` común; contenido centrado.
- Modo: aplica.

**A6 · Separaciones claras.** Las partes de una slide se separan con claridad (en vertical, o con un panel de fondo propio para una columna de ejemplos). Las líneas separadoras no van más allá de su sección y no se dibuja una línea bajo el último elemento de una lista.
- Detección: PNG.
- Arreglo: `:last-child{border-bottom:0}`; ancho de la línea igual al de su bloque; panel `--surface-fill` con radio para separar una columna de apoyo.
- Modo: aplica.

**A7 · Sin desbordes, cortes ni solapes.** Ningún texto cortado, bajo la banda, fuera del margen ni pisando otro texto o el logo.
- Detección: `insp:fuera`, `insp:cortado`, `insp:pie`, `insp:banda`, `insp:solape`, `insp:logo`, `insp:margen`; PNG.
- Arreglo, en este orden: compactar (padding, interlineado), acortar el texto (si acortar cambia el mensaje, proponer) y, solo al final, bajar 1 px la letra sin pasar el mínimo de C8. Si una etiqueta de gráfica choca con la banda, se quita una de las dos (proponer cuál).
- Modo: aplica (compactar); propone (acortar o quitar).

**A8 · Menos carga cuando la slide pesa.** Como máximo unas 40 etiquetas de dato por slide. Si una pieza pide más (una matriz de 10 × 12), va sola en rejilla A y sin piezas de apoyo; si no cabe así, se parte o se pasa a anexo. En una slide densa sobran los pies de gráfica, las leyendas que repiten lo evidente, las notas al pie, los títulos de bloque que ya dice el título y las etiquetas redundantes (por ejemplo, la ubicación si ya está en la cabecera de la ficha).
- Por qué: la carga se percibe antes de leer; quitar un elemento alivia más que bajar la letra.
- Detección: `med:densidad` (rango de Q2); PNG.
- Arreglo: quitar lo redundante (propone, salvo pies y leyendas evidentes, que aplica); alargar en vertical la zona central si hay sitio (aplica). No se baja la letra para que quepa más (C8). Si aun así pesa, priorizar contenido (F1).
- Modo: aplica o propone según el caso.

## 4. Color y cifras en la slide

- **K1 · El rojo es el mensaje.** El elemento en rojo es justo lo que nombra el tramo rojo del título. Un solo foco rojo por pieza, salvo las rampas de categorías, y como mucho dos en la slide. Las piezas que pintan en rojo por defecto se ajustan con su parámetro (`contadores(destacado=)`, `destacado` en gráficas); el embudo canónico tiene su rampa propia y no cuenta.

- **K2 · La cifra del título está en el visual.** Si el título da una cifra, el visual la enseña como etiqueta, con la misma unidad y el mismo redondeo (C4, F7).

- **K3 · Verde y colores de estado, solo en sus usos (autorizados el 30-10-2026 y confirmados el 02-11-2026).** `--validacion` (#2F7D4A) para estados favorables, validados o aprobados; verde, amarillo y rojo de semáforo, check verde y chip de variación en piezas de estado. No para «ventajas», ni series, ni decoración. Fuera de esas piezas, la regla de Terracotta: gris más rojo y rampa de rojos para categorías (B1). Una celda de puntuación no es una pieza de estado (B9).
  - Detección: `insp:verde` avisa de un verde ajeno a estos; el buen uso del verde de validación se juzga en el PNG.
  - Arreglo: ventajas y limitaciones con el mismo color neutro y un icono que las distinga; o rojo y neutro.
  - Modo: aplica si es decorativo; propone si cambia la lectura.

**B1 · Gama uniforme.** Una sola familia: la rampa de rojos de Terracotta (`--chart-1` rojo, `--brand-strong`, `--burgundy`, `--brand-tint`) para niveles, más neutros. Nada de mezclar verdes, azules y naranjas «para distinguir» (los colores de estado van por K3).
- Por qué: varias familias a la vez se ven «llamativas y diferentes entre sí» y restan seriedad.
- Detección: `insp:gama`; PNG.
- Arreglo: pasar niveles a la rampa de rojos y neutros.
- Modo: propone si el color codifica categorías; aplica si es decorativo.

**B2 · Un color por categoría; el estado, con otro recurso.** Todos los elementos de una categoría llevan su color. El estado (no probado, en validación, descartado, bandera) se marca con un símbolo, una píldora, un borde discontinuo o un icono, nunca cambiando el color de la categoría ni solo con color.
- Por qué: si el color dice dos cosas, no dice ninguna; y el estado solo por color no se lee en impresión ni para todos los lectores.
- Detección: PNG.
- Arreglo: añadir el marcador de estado (si hay varias opciones razonables, laboratorio).
- Modo: propone.

**B3 · Gris claro, no crema ni amarillo claro, en los bloques de apoyo.** Bandas, callouts de implicación, tarjetas de apoyo, cabeceras de ficha: `--surface-fill` (#F3EFE7).
- Detección: `insp:crema`.
- Arreglo: `background:var(--surface-fill)`.
- Modo: aplica. Excepción: si el usuario pide expresamente el amarillo claro de EA para resaltar unas celdas concretas, se usa `--dark-cream` solo ahí.

**B4 · Granate de verdad.** Cuando se pide granate es `--burgundy` (#450E14), no un rojo apagado ni un rosa.
- Modo: aplica.

**B6 · Columnas de texto sin escala de color.** El color de nivel va en la celda del dato, no en el texto descriptivo de al lado.
- Modo: aplica.

**B7 · Amarillo solo como punto de luz**, detrás del texto (glow). Nunca como relleno de bloque ni delante de un título.
- Detección: `insp:amarillo`.
- Modo: aplica.

**B8 · Las alertas no ensucian.** Banderas rojas, avisos y «no negociable» se integran en el propio dato (un icono pequeño en la celda de la puntuación), sin columna aparte ni leyenda que lo explique. El dato marcado mantiene su color normal de nivel.
- Por qué: las marcas repetidas en rojo dominan la slide y tapan el resultado.
- Detección: PNG.
- Modo: propone.

**B9 · Escala de puntuación en celdas.** La celda lleva el ojo a lo que decide: tonos neutros o claros para las notas normales y rojo solo para el fallo; nunca semáforo verde y rojo. Una alerta (no negociable incumplido) se marca con un símbolo en la celda, no cambiando su color.
- Por qué: en una matriz todo en color se lee como ruido; el mensaje suele ser dónde falla cada uno.
- Detección: `insp:verde`, `insp:gama`; PNG.
- Arreglo: rampa neutra a roja (`X.chip_nota`, `X.matriz_puntuacion`); si hay varias lecturas posibles de la escala, laboratorio.
- Modo: propone (la escala cambia la lectura).

## 5. Tipografía y formato

**C1 · Título entero en negrita con fragmento rojo.** Todo el título a 700, y un fragmento en rojo (`.hl-red`) que es el mensaje de la slide. Máximo 2 líneas.
- Detección: `insp:titulo`.
- Arreglo: negrita (aplica). Si falta el fragmento rojo o el elegido no es el mensaje, proponer cuál.
- Modo: aplica / propone.

**C2 · Mayúscula inicial** en rótulos, leyendas, estados de KPI, etiquetas de gráfica, píldoras y encabezados de bloque («Validación», «Parcial», «Más de 80 %»). No aplica a unidades ni a sufijos que siguen a una cifra («sobre 100»).
- Detección: `insp:mayuscula`.
- Modo: aplica.

**C3 · Negrita puntual.** Destaca una parte, no todo. En tablas, negrita solo en los datos directos; en la banda, en la idea clave.
- Detección: PNG y texto.
- Modo: aplica.

**C4 · Formatos numéricos y unidades.** Multiplicadores «×20», rangos «×0,5 a ×4» (nunca «unas 20 veces»); puntos porcentuales «+3 a +5 %»; coma decimal; miles con punto («1.000 L»); fechas DD-MM-YYYY; una sola unidad por magnitud en toda la slide y el deck (todo «1.000 L» o todo «1 kL»; preferido el primero).
- Detección: `insp:formato`, `insp:unidades`.
- Modo: aplica.

**C5 · Formas.** Callouts, bandas y la caja del reto con esquinas rectas. Tarjetas de contenido, fichas y teselas de datos con bordes redondeados (`--radius-md`, 10 px).
- Modo: aplica.

**C7 · Rótulos de bloque visibles, solo si hay bloques.** Con dos o más piezas que dicen cosas distintas, cada una lleva su rótulo (`rotulo_bloque()`); con una sola pieza, el título de la slide ya hace de rótulo. Los títulos de sección dentro de la slide («Lo que dicen los números», «Ventajas») se tienen que ver: 700, en `--fg1` o rojo, a 13 o 14 px. No grises en versalitas de 10 px que desaparecen.
- Por qué: si el rótulo no se ve, la slide no tiene jerarquía y parece un bloque de texto.
- Modo: aplica.

**C8 · Letra legible.** Nada por debajo de 11 px en el cuerpo ni de 10 px en etiquetas de gráfica, desde la subida de letra del 02-11-2026. Las etiquetas de una gráfica van a la escala del texto vecino.
- Detección: `insp:letra`, `med:legibilidad`.
- Modo: aplica.

## 6. Peso visual

**D1 · Un visual con peso en cada slide clave.** No todo pueden ser recuadros y texto. Si la slide es solo cajas, hay que darle un visual que lleve el mensaje (diagrama, gráfica, embudo, cadena, matriz con logos) con las cifras como etiquetas.
- Detección: `insp:visual`; PNG.
- Arreglo: elegir formato en [[Formatos de slide]] según el mensaje. En fichas y listas que no admiten un gráfico, iconos Material Symbols con significado en cada fila o bloque dan ritmo visual sin cambiar el contenido.
- Modo: propone (con el formato concreto y, si hay duda, laboratorio); los iconos en listas, aplica.

**D2 · El visual explica el mecanismo, no decora.** Un diagrama vale si conecta causas (por qué el modelo depende, de dónde sale el costo). Iconos o números que no aportan, fuera.
- Modo: propone.

**D3 · Un solo embudo por bloque**, con el componente canónico de discos apilados (`X.embudo`, de `ea_elementos/embudo_canonico.py`). El resto de datos del proceso, en contadores o tablas. Sin nombres de candidatos ni rondas internas en el embudo.
- Modo: propone.

**D4 · Un ejemplo concreto bajo un mensaje abstracto.** Si el título promete algo general («el cambio está en el proceso»), la slide lo enseña con un caso (qué se probó, qué es nuevo, su cifra, quién lo hace).
- Modo: propone.

**D5 · Cifras como etiquetas del visual.** Una cifra por elemento; si hay rango, un valor central y el rango tenue detrás.
- Modo: aplica (formato) / propone (si cambia el dato mostrado).

**D6 · Logos siempre que se nombra una empresa.** A color, del mismo alto, alineados (a la derecha en tarjetas con el nombre a la izquierda), sin pixelar. Si falta el logo oficial, se busca en la web oficial o en Wikimedia y se registra su origen; si no aparece, se pide ayuda al usuario antes de dejar un hueco.
- Detección: `insp:logos`; PNG (calidad, color).
- Modo: aplica (alto y alineación) / propone (búsqueda de logos).

**D7 · Fotos con relación con el proyecto.** La foto muestra el objeto del proyecto, no un genérico del sector. Marcas de terceros en la foto, retocadas.
- Modo: propone.

## 7. Tono y redacción

**E1 · Rótulos profesionales, nunca los internos.** Los nombres de trabajo del equipo no llegan a la slide: se sustituyen por rótulos pensados para quien la lee.
- Modo: propone.

**E2 · Jerga explicada la primera vez.** Siglas y nombres propios del sector se despliegan en su primera mención; las siglas internas o de un proveedor que el cliente no conoce no se usan.
- Modo: propone.

**E3 · Cada cifra se puede explicar.** Rotular qué mide la métrica, marcar las estimaciones propias («(estimación)»), y sustituir el dato que no informa.
- Detección: texto (para cada cifra, ¿se entiende de dónde sale y de qué es?).
- Modo: propone.

**E4 · Frases cortas, una por elemento**, sin prefijos tipo «Ofrece:» o «Se sabe:».
- Modo: aplica si es solo quitar el prefijo; propone si hay que reescribir.

**E5 · Realista sin ser negativo.** Cada limitación va con la vía o la condición que la resuelve. El título no debe dar a entender que no hay salida si la hay.
- Modo: propone.

**E6 · Conclusiones que aportan.** La banda de `cuerpo_slide()` o la implicación saca una conclusión (qué significa, qué decide, qué cambia), con una parte en negrita; no describe lo que ya se ve. Compacta: una o dos frases. Si la conclusión ya está en el título y en el visual, la slide va sin banda y gana alto. Cuando la banda no es la conclusión sino otra cosa (un supuesto, una implicación, el patrón que se repite), lleva rótulo a la izquierda: `rotulo_banda="Asunción clave"`, «Implicación», «El patrón», «Conclusión».
- Detección: texto (si la banda se puede deducir mirando la slide, no aporta).
- Modo: propone, con la conclusión reescrita.

**E7 · Sin referencias internas ni avisos repetidos.** Fuera «(slide 18)» dentro de un texto (además se desfasa al renumerar) y los avisos repetidos en cada tarjeta: se dicen una vez, en el título o el subtítulo.
- Detección: `insp:formato` (referencias); texto.
- Modo: aplica (referencias) / propone (avisos).

**E8 · Todo en el idioma del cliente**, también las etiquetas de la portada, el pie y el cierre (`idioma=` en `ea_deck`, decisión del 01-11-2026).
- Modo: aplica.

**E9 · Nomenclatura consistente.** Sin subcódigos, familias numeradas seguidas, el mismo nombre para lo mismo en todo el deck.
- Modo: propone.

**E10 · Sin nombres que no aportan o comprometen.** En embudos, matrices de proceso o representaciones de conjunto no se nombra a quién declinó o a quién se descartó, salvo que sea el objeto de la slide.
- Modo: propone.

## 8. Contenido y coherencia

**F1 · Cada slide aporta valor.** Antes de pulir una slide floja, preguntarse si merece estar: si repite otra o es poco probable que sirva, proponer quitarla o fusionarla.
- Modo: propone.

**F2 · No comprometer lo que no se controla.** Cifras de contactos, número de agentes, plazos de terceros: mejor cualitativo («limitado») o con su aviso.
- Modo: propone.

**F3 · No invadir la experiencia del cliente.** La slide dice qué se resuelve, qué sale y quién lo hace; el cómo técnico del cliente (su protocolo de ensayo) no se dicta.
- Modo: propone.

**F4 · Solo lo que pide el alcance.** Lo que el contrato no pide no entra (o va como opcional, sin insistir).
- Modo: propone.

**F5 · Ejemplos que el cliente no tenga.** No mostrar proveedores que ya evaluó ni precios suyos o de su competidor.
- Modo: propone.

**F6 · Explicar antes de usar.** Un concepto se presenta antes de que otras slides lo citen; si se explica tarde, la slide está fuera de sitio.
- Modo: propone.

**F7 · Coherencia entre slides.** La misma cifra, el mismo recuento y el mismo nombre en todas las slides que lo citan (si una slide dice 40 y otra suma 39, una está mal). Al rehacer un bloque, revisar las que lo citan.
- Detección: `insp:coherencia` (cifras con la misma etiqueta que cambian entre páginas); texto.
- Modo: propone (con la cifra correcta si se puede verificar en la fuente).

**F8 · No pasar preguntas al cliente.** Lo que se pueda resolver se resuelve; si no, se supone con criterio y se anota el supuesto.
- Modo: propone.

**F9 · Fechas vigentes.** La portada, la línea de «hoy» de un calendario, los «próximos pasos» y las ventanas de plazo cuadran con la fecha en que se presenta el deck. Un deck montado días antes arrastra fechas que ya no valen y plazos que pueden haber caducado.
- Detección: `insp:fecha` (aviso de deck); texto.
- Arreglo: preguntar la fecha de presentación si no se sabe; actualizar portada y «hoy» (aplica); si mover «hoy» deja un plazo imposible, proponer cómo se reescribe (propone).
- Modo: aplica / propone. Va en la línea de «Urgente antes de presentar».

## 9. Base fija

**G1 · Portada, agenda, portadillas, cabecera, pie y cierre de `ea_deck`.** El deck usa `portada()`, `agenda()`, `portadilla()`, `cabecera()`, `slide()` y `cierre()` de `presentaciones/ea_deck.py`: fondo de portada oficial con las etiquetas en el idioma del deck y el equipo real, agenda con «AGENDA» a la izquierda, portadilla con foto relacionada o escena isométrica, eyebrow gris en frase normal, glow detrás del título, pie con la fuente a la izquierda y la confidencialidad sin «Eatable Adventures», cierre con «Let's Beat» y próximo paso opcional. No se rediseñan.
- Detección: `insp:base` (aviso de deck).
- Arreglo: migrar el generador a `ea_deck` (`portada()`, `agenda()`, `portadilla()`, `cabecera()`, `slide()`, `cierre()`) conservando el cuerpo de cada slide. Es forma: no cambia lo que se dice. El equipo de la portada sale de la sección «Equipo» del PM del proyecto (02-11-2026); «realizado para» y el resto, del deck actual. Lo que falte se deja marcado y se pregunta en la respuesta, nunca se inventa.
- Modo: aplica.

**G2 · Pie sin fechas** en la línea de fuente y sin «Eatable Adventures» a la derecha (el pie fijo ya no lo lleva desde el 01-11-2026).
- Modo: aplica.

## 10. Ilustración isométrica

Las escenas (`cadena_isometrica`, `escena_iso`, catálogo `ESCENAS`) dan contexto: dicen de qué eslabón o de qué tipo de instalación se habla. No sustituyen al dato.

- **I1 · Dónde sí.**
  - Apertura de un informe o una propuesta, con la cadena del sector y el eslabón del proyecto en rojo.
  - Contexto antes del análisis: la `cadena_isometrica` y, en la slide siguiente, `cadena_capas` con los márgenes y los actores.
  - Fichas de actor: una `escena_iso` pequeña que dice qué tipo de instalación tiene (planta de fermentación, granja vertical).
  - Portadillas de sección cuando no hay una foto que tenga relación con el proyecto (D7): la escena del eslabón de esa sección. Si la sección no es un eslabón, una transversal: `comunicacion`, `hoja_de_ruta` o `alianzas`.

- **I2 · Dónde no.** Nunca en la portada (norma de `ea_deck`). Nunca en slides de datos densos ni como decoración sin mensaje (D2). Nunca para representar algo que tiene una cifra mejor (una escena de fábrica no dice cuánto produce).

- **I3 · Una por slide.** Una sola ilustración isométrica por slide (la cadena cuenta como una), y nunca en el mismo bloque que iconos planos de Material Symbols: o volumen o plano.

- **I4 · El rojo es el eslabón del que se habla.** Solo la fase o la escena que nombra el título va en su versión destacada (`destacado=`). El resto, en gris.

- **I5 · Tamaño mínimo.** Una escena suelta mide al menos 120 px de ancho; por debajo el detalle es ruido y se usa `icono_caja`. La cadena isométrica va siempre en rejilla A, con 4 a 7 fases.

- **I6 · Coherencia en el deck.** El mismo eslabón usa siempre la misma escena y el mismo tamaño en todas las slides. Las slides hermanas usan el mismo `W`.

- **I7 · El texto, fuera del dibujo.** Nombre arriba, texto y dato debajo, como hace `cadena_isometrica`. Nada de rótulos encima de la escena.

- **I8 · Escenas nuevas en el catálogo.** Si falta un eslabón, se añade con `@escena(nombre, descripción, eslabón, alto)` en `ea_elementos/cadena.py` y aparece sola en el catálogo y en las cadenas. Se dibuja con el kit `Iso` y los tonos de `_paleta`, sin colores nuevos.

## 11. Iconos

- **N1 · Primero el catálogo.** Una sola familia: Material Symbols Outlined, peso 300, del mismo tamaño en cada grupo y con significado (lupa para características, mazo para regulación); nunca emojis (`insp:formato`). `buscar_icono("palabra")` en español. El icono tiene que significar lo que dice el texto de al lado, no solo parecerse. Modo: aplica; propone si hace falta añadir un icono al catálogo.

- **N2 · Si no hay uno apto, buscar más (01-11-2026).** No se conforma con el menos malo: `buscar_completo("english words")` busca en toda la familia por nombre y por las etiquetas oficiales de Google. Si aparece uno que encaja, se mira dibujado (no basta el nombre: `polymer` es un logo y `bubbles` una pantalla), se añade a `iconos.py` en su tema con palabras clave en español y se regenera con `build_galeria_elementos.py`.

- **N3 · Si tampoco está, buscar en la web dentro de la familia.** Google añade iconos a Material Symbols con frecuencia: se consulta fonts.google.com/icons y, si hay uno nuevo que encaja, se vuelven a descargar la fuente, los codepoints y las etiquetas del repositorio oficial (pasos en `assets/fonts/LICENCIA material-symbols.md`).

- **N4 · Nunca otra familia.** Si el concepto no existe en Material Symbols (no hay vaca, por ejemplo), se usa el concepto más cercano que sí exista (`pets` para ganado), una escena isométrica si hay sitio (I1) o texto; nunca iconos de otra familia, emojis ni dibujos sueltos.

## 12. Medición

`python3 revisar_deck.py deck.html` da en un solo informe el render, la inspección del HTML y la medición del PDF frente a los rangos de los decks de referencia ([[Medición de decks]]). Orienta, no sustituye al ojo: una marca se mira y se decide.

- **Q1 · Llenado (M11).** Lo habitual: ocupación del 41 % al 85 % del cuerpo (mediana 61 %), mayor hueco de hasta el 18 % y sin franjas vacías arriba ni abajo.

- **Q2 · Densidad (A8).** Lo habitual: de 79 a 270 palabras en el cuerpo (mediana 150) y hasta 38 etiquetas de dato (mediana 12).

- **Q3 · Legibilidad (C8).** Es lo que hay en las referencias; el mínimo para decks nuevos lo fija C8. Lo habitual: cuerpo de 12 a 18 px (mediana 14) y letra mínima de 10,5 px o más.

- **Q4 · Coherencia.** El deck no debería saltar de slides llenas a slides medio vacías (dispersión de ocupación hasta 23), y las slides hermanas tienen que parecerse entre sí.

## 13. Antes de dar la slide por montada

1. La intención está escrita y se han mirado todas sus candidatas (S1, S2).
2. Hay una protagonista y la rejilla es una de las seis (M1, M2).
3. Cada pieza tiene la escala de su sitio y ninguna está escalada con CSS (M3).
4. El rojo del visual es el tramo rojo del título y la cifra del título está en el visual (K1, K2).
5. Si hay escena isométrica: una, con el eslabón correcto en rojo, sin iconos planos en su bloque (I3, I4).
6. Cada icono significa lo que dice su texto y, si no había uno apto en el catálogo, se buscó en toda la familia antes de conformarse (N1, N2).
7. Se ha mirado la slide de referencia de su tipo, si la hay (S6), y el cuerpo llena el alto sin cajas huecas (M11).
8. La banda concluye, cada cifra se puede explicar y el texto no compromete al equipo (E3, E6, F2).
9. Revisión con `revisar_deck.py`, cada aviso mirado y cada PNG revisado.

## Códigos retirados (02-11-2026)

Eran la misma regla en dos sitios. Los documentos fechados los siguen citando: esta tabla dice dónde está cada una ahora.

| Código | Ahora en | Qué era |
|---|---|---|
| A2 | M11 | El cuerpo llena; centrar pasa a excepción |
| D8 | M11 y A8 | Ni vacía ni sobrecargada |
| D9 | S4 | Variedad y hermanas |
| M4 | A1 y A4 | Mismo alto y mismos ejes |
| M5 | C7 | Rótulo de bloque |
| M6 | A8 | Máximo de etiquetas |
| M8 | E6 | La banda concluye |
| B5 | K3 | Verde solo en sus usos |
| C6 | N1 | Una sola familia de iconos |
