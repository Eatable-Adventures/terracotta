---
tags:
  - recurso
  - design-system
  - presentaciones
aliases:
  - Vocabulario de microajuste
description: >-
  De los comentarios de forma (baja un poco, mismo alto, que acabe en el eje) a un cambio concreto con su valor por defecto. Antes en la skill /taste.
---

# Microajustes: de la frase al cambio concreto

> Parte de Terracotta V2. Si la pieza tiene `W` o `H`, el ajuste se hace ahí (M3); el CSS de estas tablas es para lo demás.

Los comentarios de forma llegan en lenguaje natural. Esta tabla da el valor por defecto de cada uno. Dilo siempre en la respuesta («bajado 12 px»): si piden «un poco más», se sabe desde dónde se parte, y si una calibración se repite, se corrige aquí y se anota en [[Registro de criterios]].

Base de medidas en una slide de `ea_deck`: 1280 × 720 px, padding de `.slide-inner` 48 px arriba, 64 px a los lados, 24 px abajo; título a 28 px; cuerpo habitual de 13 a 15 px.

## Posición y espacio

| Frase | Interpretación | Cambio por defecto | Cómo, en CSS o SVG |
|---|---|---|---|
| «baja un poco», «sube un poco» | Desplazar el bloque | 12 px (rango 8 a 16) | `margin-top` del bloque, o `transform:translateY()` si no debe mover lo que tiene debajo |
| «baja bastante», «más abajo» | Desplazar claramente | 24 px | Igual |
| «un pelín» | Ajuste mínimo | 4 a 6 px | Igual |
| «el subtítulo en una línea, que cabe» | Quitar el salto | Reescribir corto hasta una línea; si no, ensanchar el subtítulo | Texto; `max-width` del subtítulo |
| «baja el cuerpo para que quede equilibrado», «mismo hueco arriba que abajo» | Que el cuerpo llene entre la cabecera y la banda o el pie (M11) | El alto de `X.alto_cuerpo`; si es de verdad una petición de centrar esa slide, la mitad de la diferencia de huecos | `H` de la pieza; `columna(repartir=True)`; como excepción, `justify-content:center` |
| «sube la conclusión, que haya hueco con la línea» | Separar la banda de lo que tiene encima o del pie | 16 px de separación | `margin-top` de la banda o `margin-bottom` del bloque anterior |
| «más hueco entre las dos filas» | Más separación vertical | +8 a +12 px | `row-gap` o `margin-bottom` de la fila |
| «que respire», «más aire» | Más espacio interior | +8 px de padding, o quitar un elemento | `padding` de la tarjeta |
| «que tenga hueco por los dos lados» | Margen simétrico alrededor de un elemento | Mismo hueco a izquierda y derecha | Reducir el ancho de las cajas vecinas o centrar con `justify-content:center` |
| «enviar al fondo» | Detrás del texto | Debajo en el orden de pintado | `z-index` menor; en SVG, dibujarlo antes |

## Tamaño

| Frase | Interpretación | Cambio por defecto | Cómo |
|---|---|---|---|
| «un pelín más ancho» | Ensanchar sin romper la rejilla | +6 a +8 % del ancho, o lo justo para que el texto quepa en una línea menos | `width`, `flex-basis` o columnas de la rejilla |
| «más largo», referido a una caja | Más alto | +15 a +20 % del alto | `min-height` |
| «más largo», referido a un texto («que sean dos líneas») | Más contenido | Reescribir hasta la longitud pedida | Propone si cambia el mensaje |
| «más alargado verticalmente» | Aprovechar el alto libre | Hasta llenar el alto (M11) | `flex:1` en la zona central |
| «un poco más grande» (texto) | +1 px | 1 px | `font-size` |
| «más grande» (texto) | +2 a +3 px | 2 px | `font-size` |
| «baja un poco la letra», «menos cargado» | Quitar lo que sobre; si lo pide explícitamente, −1 px | 1 px, nunca por debajo de 11 px (C8) | Primero A8; `font-size` |
| «filas más gordas» (roadmap, Gantt) | Más alto de fila | 36 px por carril con seis filas y otro bloque encima | `carriles(alto=…)` |
| «más compacto» | Menos interlineado y separación | `line-height` de 1,5 a 1,35; gaps −4 px | `line-height`, `gap` |
| «sube la letra en general» (presentación) | Letra de lectura a 15 o 16 px | Lectura de 13 a 16 px; nunca por debajo de 14 px (C8) | `tam=` de la pieza o `font-size` |
| «más hueco entre el título y el texto» (fases, bloques bajo una línea) | Más aire entre la línea, el título y los puntos | De 18 a 28 px entre la línea y el título; 12 px entre el título y los puntos | `padding` del título; parámetro `grande=` de la pieza |

## Alineación

| Frase | Interpretación | Cambio | Cómo |
|---|---|---|---|
| «centrado a lo alto», «centrado en vertical» | Centrado vertical en su fila o caja | Centro óptico = centro geométrico | `align-items:center`; tarjeta como columna flex con `justify-content:center`; SVG con `dominant-baseline:middle` |
| «que acabe en el eje» | El borde inferior coincide con la línea del eje x de la gráfica | `height = ejeY - top` | Calcular `ejeY` en coordenadas de la slide (posición del SVG + y del eje × escala) |
| «que baje hasta la última línea de la tabla» | Igual que el eje, con la última fila | `height` hasta el borde inferior de la última fila | Medir la fila con el inspector o en el PNG |
| «cuadra la tabla con el gráfico, arriba y abajo» | La línea bajo la cabecera, en el borde de arriba del dibujo; la última línea, en el eje (A4) | Gráfico desplazado el alto de la cabecera; alto de la tabla hasta el eje | `tabla_comparativa(H=…)`; `columna("<div></div>", grafico, gap=alto_cabecera)` |
| «que acabe con el texto de la izquierda» | Acabar con el último texto visible, no con la caja | Alto hasta la base del último texto | `H` de la pieza |
| «lo de dentro, más estrecho que el rótulo» (banda redondeada) | Meter el contenido hacia dentro | 8 a 12 px por cada lado (C7) | `W` 20 px menor y centrado |
| «mismo alto» | Igualar alturas de hermanos | Al de la más alta | `align-items:stretch` o `min-height` común |
| «mismo alto» con columnas muy desiguales (más de 40 px) | Repartir el contenido, no estirar | Ensanchar la columna alta y estrechar la otra hasta que acaben juntas | `flex-basis` o columnas de la rejilla; padding de filas −1 a −2 px |
| «mismo ancho» | Igualar anchos de repetidos | Al del más ancho, o `flex:1` | `flex:1 1 0` |
| «alineado con…» | Mismo eje que otro elemento | Mismo `left` o mismo borde | Medir y fijar |
| «logos a la derecha, nombre a la izquierda» | Fila con extremos | Mismo alto de logo (28 px por defecto en tarjeta) | `display:flex;justify-content:space-between;align-items:center`; logo `height:28px;width:auto;max-width:120px` |

## Color y estilo

| Frase | Cambio | Token |
|---|---|---|
| «gris claro» | Fondo de bloque de apoyo | `var(--surface-fill)` #F3F3F3 |
| «un gris más clarito» (KPI, propuesta) | Gris a medio tono entre el gris claro y el blanco | `bloque(fondo="claro")` |
| «la línea más fina y menos fuerte» | Separador de 1 px en gris tenue | `bloque(filete="fino")` o `border-top:1px solid var(--border-1)` |
| «granate» | Burgundy de marca | `var(--burgundy)` #450E14 |
| «amarillo claro de Eatable» (para resaltar celdas concretas) | Crema oscuro | `var(--dark-cream)` #F5EACE |
| «rojo de marca» | Rojo EAV | `var(--red)` #BC2D29 |
| «más llamativo» (rótulo o título de bloque) | 700, `--fg1` o rojo, +1 a +2 px, sin versalitas grises | Ver C7 |
| «verde» | Solo validación | `var(--validacion)` #2F7D4A |
| «bordes redondeados» | Radio de tarjeta | `var(--radius-md)` 10 px |
| «esquinas rectas» | Callout o banda | `border-radius:0` |
| «otro estilo de iconos», «como los de Google» | Material Symbols Outlined, peso 300 | Clase `.ms` de `ea_deck` |
