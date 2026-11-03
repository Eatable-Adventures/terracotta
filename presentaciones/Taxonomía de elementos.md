---
tags:
  - recurso
  - design-system
  - presentaciones
aliases:
  - Menú de elementos visuales
description: >-
  Menú completo de ea_elementos generado desde taxonomia.py: qué elemento elegir para cada intención,
  con su escala, sus datos y sus alternativas. No se edita a mano (lo regenera build_galeria_elementos.py).
---

# Taxonomía de elementos

> Generado por `build_galeria_elementos.py` desde `ea_elementos/taxonomia.py`. 158 elementos en 14 familias. Para verlos: «Galería de elementos.html» en esta carpeta. Para colocarlos en una slide: [[Reglas de uso de elementos]].

## Cómo se usa

1. Escribir en una frase lo que la slide tiene que decir y elegir su intención en la tabla de abajo.
2. Leer **todas** las candidatas de esa intención (también las de la columna «también sirven»), no solo la primera que suene.
3. Descartar con un motivo concreto (forma de los datos, escala, número de elementos). Barras, anillo y tabla son la última opción, no la primera.
4. Comprobar «Cuándo no» en el docstring y mirar las alternativas antes de cerrar.

Escala: **S** pieza para una tarjeta o una celda (hasta ~360 px), **M** media slide (400 a 640 px), **L** ancho de slide.

## Por intención

### Una cifra que manda (`cifra`)

De 1 a 4 números protagonistas: KPI, tamaño, resultado.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| KPI con variación | `cifra_delta` | S | Cifra, variación y minilínea | `tarjeta_cifra`, `indicador`, `contadores` |
| Círculos concéntricos (TAM, SAM, SOM) | `circulos_concentricos` | M | 2 a 4 niveles anidados con su cifra | `dimensionamiento`, `embudo` |
| Contadores | `contadores` | S | 2 a 4 cifras grandes con de dónde salen | `icono_dato`, `tarjeta_cifra`, `columna_contexto` |
| Dimensionamiento de arriba abajo | `dimensionamiento` | M | Del mercado total al alcanzable en 3 a 5 pasos | `circulos_concentricos`, `embudo`, `formula` |
| Fila de parámetros técnicos | `fila_parametros` | L | 3 a 6 condiciones técnicas de partida | `icono_dato`, `etiquetas_icono` |
| Dato con icono | `icono_dato` | S | 2 a 4 cifras de contexto con icono | `contadores`, `fila_parametros` |
| Indicador (gauge) | `indicador` | S | Un KPI de avance con objetivo | `bala`, `barra_progreso`, `tarjeta_cifra` |
| Panel de KPI | `panel_kpi` | L | KPI que deciden arriba y condiciones abajo | `bala`, `tarjeta_kpi` |
| Pictograma | `pictograma` | S | Un porcentaje como x de 10, 20 o 100 figuras | `waffle`, `donut`, `tarjeta_cifra` |
| Tarjeta con cifra | `tarjeta_cifra` | S | Una cifra que hace de etiqueta del mensaje, con texto | `cifra_delta`, `contadores` |
| Tarjeta de KPI de éxito | `tarjeta_kpi` | S | KPI con objetivo, referencia, visual y validación | `bala`, `cifra_delta` |
| Columna de contexto (también) | `columna_contexto` | S | Rótulo, 2 o 3 párrafos y una cifra ancla | `contadores`, `tarjeta_cifra`, `bloque` |
| Columnas numeradas con cifras (también) | `columnas_numeradas` | L | 2 a 4 ideas con título, texto y una o dos cifras | `lista_numerada`, `pilares`, `tarjetas_miniatura` |
| Anillo (donut) (también) | `donut` | S | 2 a 5 partes de un total, con cifra central | `waffle`, `barras_apiladas`, `treemap`, `pictograma` |
| Embudo de discos (también) | `embudo` | M | 3 a 6 etapas de un cribado con su recuento | `dimensionamiento`, `circulos_concentricos`, `escalones` |
| Miniatura de conteo (también) | `mini_conteo` | S | Hasta 10 círculos con los marcados | `pictograma` |
| Gofre (waffle) (también) | `waffle` | S | Un porcentaje sobre 100 casillas | `pictograma`, `donut` |

### ¿Cuánto, entre categorías? (`comparar`)

Magnitudes de varias categorías en la misma unidad.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Columnas agrupadas | `barras_agrupadas` | M | 2 o 3 series en 3 a 6 categorías | `mancuerna`, `pendiente`, `pequenos_multiplos`, `mapa_calor` |
| Columnas | `columnas` | M | 1 serie de 3 a 10 categorías o periodos; previsión y CAGR opcionales | `barras_ranking`, `piruletas`, `linea`, `pictograma` |
| Comparador por unidad | `comparador_unidad` | M | Coste o precio por unidad de cada opción frente a una referencia | `escala_log`, `barras_variacion`, `tabla_con_barras` |
| Escala logarítmica | `escala_log` | L | Alternativas con rangos que abarcan órdenes de magnitud | `rangos`, `comparador_unidad` |
| Barras apiladas al 100 % (también) | `barras_apiladas` | M | 3 a 6 partes en 2 a 8 filas | `marimekko`, `donut`, `barra_desglose`, `barra_dividida` |
| Barras frente a objetivo (también) | `barras_objetivo` | M | 3 a 8 opciones con su valor y una línea de objetivo | `bala`, `piruletas`, `mancuerna` |
| Ranking en barras (también) | `barras_ranking` | M | 1 serie de 5 a 15 elementos con rótulos largos | `piruletas`, `tabla_con_barras`, `pareto`, `columnas`, `ranking_logos` |
| Barras de variación (también) | `barras_variacion` | M | Variaciones positivas y negativas por elemento | `pendiente`, `cascada`, `tornado` |
| Cadena con margen y valor capturado (también) | `cadena_margen` | L | 3 a 7 eslabones con margen, valor capturado y posición del cliente | `cadena_capas`, `cadena_isometrica` |
| Mancuerna (dumbbell) (también) | `mancuerna` | M | Dos valores por fila (actual y objetivo, nosotros y líder) | `pendiente`, `barras_agrupadas`, `piruletas` |
| Mapa de burbujas (también) | `mapa_burbujas` | L | Un valor por lugar, con el área proporcional | `mapa_coropletico`, `mapa_actores`, `barras_ranking` |
| Marimekko (también) | `marimekko` | M | Tamaño por columna y cuota por segmento | `barras_apiladas`, `treemap` |
| Pequeños múltiplos (también) | `pequenos_multiplos` | L | 4 a 12 series cortas con escala común | `linea`, `barras_agrupadas`, `mapa_calor` |
| Rangos (football field) (también) | `rangos` | M | Mínimo y máximo por método o fuente sobre un eje común | `escala_log`, `cajas`, `benchmark_rango`, `dimensionamiento` |
| Tabla con barras (también) | `tabla_con_barras` | L | Filas de texto con una columna numérica | `barras_ranking`, `ficha_linea` |
| Tabla gráfica (también) | `tabla_grafica` | L | Total, reparto en 100 % y destacados por fila, con panel lateral | `tabla_con_barras`, `barras_apiladas` |
| Tarjetas de escenario (también) | `tarjetas_escenario` | L | 2 o 3 escenarios con dato, texto y visual pequeño | `abanico`, `tarjetas_salida`, `balanza` |

### ¿Quién va primero? (`ordenar`)

Ranking por valor, concentración, los pocos que pesan.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Ranking en barras | `barras_ranking` | M | 1 serie de 5 a 15 elementos con rótulos largos | `piruletas`, `tabla_con_barras`, `pareto`, `columnas`, `ranking_logos` |
| Ranking en el tiempo (bump) | `bump` | M | Posiciones de 4 a 8 actores en 3 o más periodos | `pendiente`, `linea` |
| Pareto | `pareto` | M | 1 serie de causas o elementos con su acumulado | `barras_ranking`, `treemap` |
| Piruletas (lollipop) | `piruletas` | M | 1 serie de valores parecidos, con referencia opcional | `barras_ranking`, `mancuerna`, `barras_objetivo` |
| Ranking por logo | `ranking_logos` | S | Actores con su puntuación, reconocibles por el logo | `barras_ranking`, `tabla_con_barras` |
| Tabla con barras | `tabla_con_barras` | L | Filas de texto con una columna numérica | `barras_ranking`, `ficha_linea` |
| Escalera de prioridad (también) | `escalera_prioridad` | L | Hasta 3 niveles de prioridad con 5 focos cada uno | `matriz_2x2`, `pareto`, `tabla_vigilancia` |
| Ficha de una línea por empresa (también) | `ficha_linea` | L | 10 a 20 empresas con madurez y frase | `tabla_con_barras`, `muro_logos` |
| Pendiente (slope) (también) | `pendiente` | M | 3 a 8 elementos en dos momentos | `mancuerna`, `bump`, `barras_variacion` |
| Mapa de árbol (treemap) (también) | `treemap` | M | 5 a 15 partes de un total | `sunburst`, `barras_ranking`, `marimekko` |

### ¿Cómo evoluciona? (`tendencia`)

Serie temporal, previsión, adopción.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Abanico de escenarios | `abanico` | M | Serie histórica más escenario bajo, central y alto | `linea`, `rangos`, `tarjetas_escenario` |
| Áreas apiladas | `area_apilada` | M | 2 a 4 componentes de un total en el tiempo | `linea`, `barras_apiladas` |
| Métricas financieras (combo) | `combo_financiero` | M | Ingresos, EBITDA y margen de una empresa en 3 a 6 periodos | `columnas`, `linea`, `ficha_empresa` |
| Curva en S de adopción | `curva_s` | M | Opciones situadas en las fases de adopción de una tecnología | `mapa_madurez`, `linea_tiempo`, `escalones` |
| Líneas con serie destacada | `linea` | M | 1 a 4 series en 5 o más periodos, con anotaciones y periodos sombreados | `columnas`, `area_apilada`, `pequenos_multiplos`, `abanico` |
| Pequeños múltiplos | `pequenos_multiplos` | L | 4 a 12 series cortas con escala común | `linea`, `barras_agrupadas`, `mapa_calor` |
| Minilínea (sparkline) | `sparkline` | S | Una serie corta, sin ejes | `cifra_delta`, `pequenos_multiplos` |
| Ranking en el tiempo (bump) (también) | `bump` | M | Posiciones de 4 a 8 actores en 3 o más periodos | `pendiente`, `linea` |
| Columnas (también) | `columnas` | M | 1 serie de 3 a 10 categorías o periodos; previsión y CAGR opcionales | `barras_ranking`, `piruletas`, `linea`, `pictograma` |
| Tabla de drivers de mercado (también) | `tabla_drivers` | L | Drivers con fuerza e impacto por periodo | `cinco_fuerzas`, `arbol_drivers` |

### ¿Por qué cambia o de qué depende? (`explicar_cambio`)

Puente entre dos valores, drivers, sensibilidad.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Árbol de drivers | `arbol_drivers` | L | Un KPI descompuesto en factores con valor y variación | `formula`, `cascada`, `tornado` |
| Barras de variación | `barras_variacion` | M | Variaciones positivas y negativas por elemento | `pendiente`, `cascada`, `tornado` |
| Cascada (waterfall) | `cascada` | M | Valor inicial, 3 a 8 variaciones y valor final; fila de evidencia opcional | `arbol_drivers`, `barras_variacion`, `formula`, `tornado` |
| De lo probado a lo nuevo | `columnas_evolucion` | L | 2 a 4 columnas con lo probado, lo nuevo, quién y el reto | `ficha_hipotesis`, `nucleo_dos_lados`, `antes_despues_imagen` |
| Espina de pescado (Ishikawa) | `espina_pescado` | L | Causas de un problema por categoría | `arbol`, `arbol_drivers` |
| Fórmula de cálculo | `formula` | L | Factores con cifra y fuente unidos por operadores | `arbol_drivers`, `dimensionamiento`, `cascada` |
| Pendiente (slope) | `pendiente` | M | 3 a 8 elementos en dos momentos | `mancuerna`, `bump`, `barras_variacion` |
| Tabla de drivers de mercado | `tabla_drivers` | L | Drivers con fuerza e impacto por periodo | `cinco_fuerzas`, `arbol_drivers` |
| Tornado (sensibilidad) | `tornado` | M | Resultado bajo y alto por variable de un modelo | `barras_variacion`, `arbol_drivers`, `rangos` |
| Abanico desde un foco (también) | `abanico_foco` | L | Un foco y 3 a 6 filas de rótulo y texto | `arbol`, `radial`, `lista_numerada` |
| Antes y después en imagen (también) | `antes_despues_imagen` | M | Dos imágenes con rótulo | `columnas_evolucion`, `escena_iso` |
| Barra con desglose (también) | `barra_desglose` | M | Tramos de un total con uno abierto en partidas | `barras_apiladas`, `cascada`, `treemap` |
| Convergencia (también) | `convergencia` | L | 3 o 4 causas con texto que llevan a un concepto | `abanico_foco`, `radial` |
| Dimensionamiento de arriba abajo (también) | `dimensionamiento` | M | Del mercado total al alcanzable en 3 a 5 pasos | `circulos_concentricos`, `embudo`, `formula` |
| Núcleo con dos lados (también) | `nucleo_dos_lados` | L | Dos opciones que salen de un núcleo común, con efectos por fila | `balanza`, `columnas_evolucion` |

### ¿De qué se compone? (`parte_todo`)

Reparto de un total en partes.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Barra con desglose | `barra_desglose` | M | Tramos de un total con uno abierto en partidas | `barras_apiladas`, `cascada`, `treemap` |
| Barras apiladas al 100 % | `barras_apiladas` | M | 3 a 6 partes en 2 a 8 filas | `marimekko`, `donut`, `barra_desglose`, `barra_dividida` |
| Anillo (donut) | `donut` | S | 2 a 5 partes de un total, con cifra central | `waffle`, `barras_apiladas`, `treemap`, `pictograma` |
| Marimekko | `marimekko` | M | Tamaño por columna y cuota por segmento | `barras_apiladas`, `treemap` |
| Sunburst | `sunburst` | M | Un total con dos niveles (familia y subcategoría) | `treemap`, `anillo_categorias` |
| Tabla gráfica | `tabla_grafica` | L | Total, reparto en 100 % y destacados por fila, con panel lateral | `tabla_con_barras`, `barras_apiladas` |
| Mapa de árbol (treemap) | `treemap` | M | 5 a 15 partes de un total | `sunburst`, `barras_ranking`, `marimekko` |
| Gofre (waffle) | `waffle` | S | Un porcentaje sobre 100 casillas | `pictograma`, `donut` |
| Anillo de categorías (también) | `anillo_categorias` | L | Elementos agrupados en 2 a 5 categorías, con un estado transversal | `sunburst`, `mapa_alcance`, `treemap` |
| Áreas apiladas (también) | `area_apilada` | M | 2 a 4 componentes de un total en el tiempo | `linea`, `barras_apiladas` |
| Pictograma (también) | `pictograma` | S | Un porcentaje como x de 10, 20 o 100 figuras | `waffle`, `donut`, `tarjeta_cifra` |
| Flujos (Sankey) (también) | `sankey` | M | Flujos de volumen entre dos clasificaciones | `marimekko`, `red_nodos`, `cadena_capas` |

### ¿Cuánto falta? (`brecha`)

Frente a un objetivo, una referencia o un benchmark.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Avance hacia objetivo | `bala` | M | 3 a 6 KPI con valor, objetivo y máximo | `barras_objetivo`, `indicador`, `barra_progreso` |
| Duelo de dos barras | `barras_duelo` | S | Referencia y objetivo de un mismo KPI | `regleta_objetivo`, `mancuerna`, `indicador` |
| Barras frente a objetivo | `barras_objetivo` | M | 3 a 8 opciones con su valor y una línea de objetivo | `bala`, `piruletas`, `mancuerna` |
| Benchmark en rango | `benchmark_rango` | M | Nuestro valor entre el peor y el mejor comparable, por KPI | `rangos`, `mancuerna`, `cajas` |
| Mancuerna (dumbbell) | `mancuerna` | M | Dos valores por fila (actual y objetivo, nosotros y líder) | `pendiente`, `barras_agrupadas`, `piruletas` |
| Regleta con zona objetivo | `regleta_objetivo` | S | Un valor o rango negociable sobre una escala | `barras_duelo`, `benchmark_rango` |
| Tabla con barra frente a referencia | `tabla_referencia` | L | Filas con una barra frente a objetivo y referencia | `tabla_con_barras`, `barras_objetivo` |
| Comparador por unidad (también) | `comparador_unidad` | M | Coste o precio por unidad de cada opción frente a una referencia | `escala_log`, `barras_variacion`, `tabla_con_barras` |
| Miniatura de barras (también) | `mini_barras_objetivo` | S | Hasta 3 barras frente a referencia y objetivo | `barras_objetivo` |
| Piruletas (lollipop) (también) | `piruletas` | M | 1 serie de valores parecidos, con referencia opcional | `barras_ranking`, `mancuerna`, `barras_objetivo` |
| Tarjeta de KPI de éxito (también) | `tarjeta_kpi` | S | KPI con objetivo, referencia, visual y validación | `bala`, `cifra_delta` |

### ¿Qué opción es mejor? (`evaluar`)

Alternativas frente a varios criterios, puntuación.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Nota 0 a 3 con confianza | `chip_nota` | S | Nota y confianza de una celda de matriz | `harvey`, `valoracion` |
| Cinco fuerzas | `cinco_fuerzas` | M | Intensidad y explicación de las cinco fuerzas de un sector | `dafo`, `tabla_drivers` |
| Criterios con puntos por actor | `criterios_puntos` | M | Criterios por importancia y la nota de cada actor | `radar`, `matriz_puntuacion`, `tabla_comparativa` |
| DAFO | `dafo` | M | Fortalezas, debilidades, oportunidades y amenazas | `cinco_fuerzas`, `balanza` |
| Deslizadores de valoración | `deslizadores` | M | Valoraciones cualitativas de 0 a 1 con su razón | `radar`, `harvey`, `valoracion`, `score_dimensiones` |
| Bolas de Harvey | `harvey` | S | Nivel de 0 a 4 | `valoracion`, `marca` |
| Mapa de calor | `mapa_calor` | M | Matriz de valores de 4 × 4 a 10 × 12 | `matriz_puntuacion`, `tabla_comparativa`, `pequenos_multiplos` |
| Matriz de puntuación | `matriz_puntuacion` | L | Opciones agrupadas por veredicto con notas de 0 a 3 y total | `mapa_calor`, `tabla_comparativa`, `criterios_puntos` |
| Araña (radar) | `radar` | M | 1 o 2 perfiles en 5 a 8 criterios de la misma escala | `criterios_puntos`, `tabla_comparativa`, `deslizadores`, `score_dimensiones` |
| Score por dimensiones | `score_dimensiones` | M | Valor de un actor en 4 a 8 dimensiones y su total | `radar`, `deslizadores`, `criterios_puntos` |
| Tabla comparativa | `tabla_comparativa` | L | 2 a 5 opciones en 4 a 10 criterios | `criterios_puntos`, `matriz_puntuacion`, `radar` |
| Puntos de valoración | `valoracion` | S | Nota de n sobre 5 | `harvey` |
| Balanza (también) | `balanza` | M | Argumentos a favor y en contra, o dos alternativas | `dafo`, `tabla_comparativa`, `nucleo_dos_lados` |
| Cadena de valor en capas (también) | `cadena_capas` | L | 4 a 7 eslabones con filas de análisis (actores, margen, tendencia) | `cadena_isometrica`, `circuito_cadena`, `sankey`, `cadena_margen` |
| Ficha de hipótesis (también) | `ficha_hipotesis` | L | Lo probado, la hipótesis, criterios con nota y ejemplos | `columnas_evolucion`, `ficha_empresa` |
| Ranking por logo (también) | `ranking_logos` | S | Actores con su puntuación, reconocibles por el logo | `barras_ranking`, `tabla_con_barras` |
| Scorecard (también) | `scorecard` | L | Criterios eliminatorios y comparativos con su peso | `criterios_puntos`, `tabla_comparativa` |

### ¿Dónde está cada uno? (`posicionar`)

En dos ejes, en una escala de madurez o en cuadrantes.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Dispersión y burbujas | `dispersion` | M | 5 a 20 elementos en dos variables numéricas, tamaño opcional | `matriz_2x2`, `mapa_madurez` |
| Mapa de madurez (TRL) | `mapa_madurez` | M | Elementos por tramo de madurez, carril de evidencia y categoría | `curva_s`, `dispersion`, `escalones` |
| Matriz 2 × 2 | `matriz_2x2` | M | Elementos en dos ejes cualitativos con cuadrantes | `dispersion`, `escalera_prioridad` |
| Benchmark en rango (también) | `benchmark_rango` | M | Nuestro valor entre el peor y el mejor comparable, por KPI | `rangos`, `mancuerna`, `cajas` |
| Curva en S de adopción (también) | `curva_s` | M | Opciones situadas en las fases de adopción de una tecnología | `mapa_madurez`, `linea_tiempo`, `escalones` |

### ¿Cómo se reparten los valores? (`distribucion`)

Dispersión, rangos, incertidumbre de una población.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Barra dividida (Likert) | `barra_dividida` | M | Respuestas en una escala de acuerdo por afirmación | `barras_apiladas` |
| Diagrama de cajas | `cajas` | M | Observaciones por grupo (ensayos, paneles) | `histograma`, `rangos`, `benchmark_rango` |
| Histograma | `histograma` | M | Recuentos por tramo con una marca | `cajas`, `rangos` |
| Rangos (football field) | `rangos` | M | Mínimo y máximo por método o fuente sobre un eje común | `escala_log`, `cajas`, `benchmark_rango`, `dimensionamiento` |
| Abanico de escenarios (también) | `abanico` | M | Serie histórica más escenario bajo, central y alto | `linea`, `rangos`, `tarjetas_escenario` |
| Calendario de calor (también) | `calendario_calor` | L | Actividad por día durante meses | `mapa_calor`, `linea` |
| Escala logarítmica (también) | `escala_log` | L | Alternativas con rangos que abarcan órdenes de magnitud | `rangos`, `comparador_unidad` |
| Mapa de calor (también) | `mapa_calor` | M | Matriz de valores de 4 × 4 a 10 × 12 | `matriz_puntuacion`, `tabla_comparativa`, `pequenos_multiplos` |
| Mapa de madurez (TRL) (también) | `mapa_madurez` | M | Elementos por tramo de madurez, carril de evidencia y categoría | `curva_s`, `dispersion`, `escalones` |

### ¿Qué se conecta con qué? (`relacion`)

Flujos, redes, solapes, cruce de condiciones.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Convergencia | `convergencia` | L | 3 o 4 causas con texto que llevan a un concepto | `abanico_foco`, `radial` |
| Red de nodos | `red_nodos` | M | Actores y sus relaciones (ecosistema) | `radial`, `sankey`, `circuito_cadena` |
| Flujos (Sankey) | `sankey` | M | Flujos de volumen entre dos clasificaciones | `marimekko`, `red_nodos`, `cadena_capas` |
| Venn | `venn` | M | 2 o 3 condiciones y su intersección | `mapa_alcance`, `circulos_concentricos` |
| Circuito de la cadena (también) | `circuito_cadena` | L | Eslabones con un actor que se engancha por dos flechas | `cadena_capas`, `lienzo_negocio`, `red_nodos` |
| Dispersión y burbujas (también) | `dispersion` | M | 5 a 20 elementos en dos variables numéricas, tamaño opcional | `matriz_2x2`, `mapa_madurez` |
| Mapa con grupos de actores (también) | `mapa_actores` | L | Grupos de actores con sus países y un punto en el mapa | `mapa_coropletico`, `muro_logos` |
| Mapa de flujos (también) | `mapa_flujos` | L | Un origen y de 2 a 12 destinos con su peso | `sankey`, `mapa_actores`, `red_nodos` |
| Radial (hub and spoke) (también) | `radial` | M | Un centro y 4 a 8 componentes o relaciones | `red_nodos`, `capas`, `lienzo_negocio`, `convergencia` |

### ¿Dónde ocurre? (`geografia`)

Países y regiones.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Mapa con grupos de actores | `mapa_actores` | L | Grupos de actores con sus países y un punto en el mapa | `mapa_coropletico`, `muro_logos` |
| Mapa de burbujas | `mapa_burbujas` | L | Un valor por lugar, con el área proporcional | `mapa_coropletico`, `mapa_actores`, `barras_ranking` |
| Mapa coroplético | `mapa_coropletico` | M | Un valor por país en una región | `barras_ranking`, `mapa_calor`, `mapa_actores` |
| Mapa de flujos | `mapa_flujos` | L | Un origen y de 2 a 12 destinos con su peso | `sankey`, `mapa_actores`, `red_nodos` |

### ¿Cómo se organiza? (`estructura`)

Jerarquías, marcos estratégicos, taxonomías, alcance.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Abanico desde un foco | `abanico_foco` | L | Un foco y 3 a 6 filas de rótulo y texto | `arbol`, `radial`, `lista_numerada` |
| Anillo de categorías | `anillo_categorias` | L | Elementos agrupados en 2 a 5 categorías, con un estado transversal | `sunburst`, `mapa_alcance`, `treemap` |
| Árbol de problemas | `arbol` | M | Una pregunta en ramas y hojas MECE | `arbol_drivers`, `espina_pescado`, `mapa_alcance`, `abanico_foco` |
| Capas (stack) | `capas` | M | 3 a 6 capas que se apoyan unas en otras | `piramide`, `pilares` |
| Mapa de categorías con chips | `categorias_chips` | L | 8 a 30 nombres en 3 a 9 categorías, con un estado transversal | `anillo_categorias`, `muro_logos`, `grupo_logos` |
| Mapa de alcance | `mapa_alcance` | L | Opciones por dimensión que entran, entran en parte o no | `anillo_categorias`, `venn`, `arbol` |
| Núcleo con dos lados | `nucleo_dos_lados` | L | Dos opciones que salen de un núcleo común, con efectos por fila | `balanza`, `columnas_evolucion` |
| Organigrama | `organigrama` | L | Personas o unidades en 2 o 3 niveles | `arbol`, `persona` |
| Casa estratégica (pilares) | `pilares` | L | Ambición, 3 a 5 pilares y bases | `capas`, `lista_numerada` |
| Pirámide | `piramide` | M | 3 a 5 niveles jerárquicos | `capas`, `escalones` |
| Radial (hub and spoke) | `radial` | M | Un centro y 4 a 8 componentes o relaciones | `red_nodos`, `capas`, `lienzo_negocio`, `convergencia` |
| Árbol de opciones (también) | `arbol_opciones` | L | Categorías con opciones numeradas y su explicación | `arbol_tramite`, `tarjetas_salida`, `mapa_alcance` |
| Bloque con filete superior (también) | `bloque` | S | Título y texto corto o HTML | `aviso`, `tarjeta_cifra`, `columna_contexto` |
| Cinco fuerzas (también) | `cinco_fuerzas` | M | Intensidad y explicación de las cinco fuerzas de un sector | `dafo`, `tabla_drivers` |
| Círculos concéntricos (TAM, SAM, SOM) (también) | `circulos_concentricos` | M | 2 a 4 niveles anidados con su cifra | `dimensionamiento`, `embudo` |
| Columnas de requisitos con coste y plazo (también) | `columnas_requisitos` | L | 2 a 4 dimensiones con requisitos, coste y plazo | `columnas_numeradas`, `tabla_comparativa` |
| DAFO (también) | `dafo` | M | Fortalezas, debilidades, oportunidades y amenazas | `cinco_fuerzas`, `balanza` |
| Ecosistema de logos por grupos (también) | `ecosistema_logos` | L | De 10 a 70 actores (partners, aliados, candidatos) en 2 a 6 grupos, con logo o nombre | `muro_logos`, `categorias_chips`, `mapa_actores`, `ficha_linea` |
| Escalones (también) | `escalones` | M | Etapas de madurez o ambición que suben | `piramide`, `chevrones`, `curva_s` |
| Espina de pescado (Ishikawa) (también) | `espina_pescado` | L | Causas de un problema por categoría | `arbol`, `arbol_drivers` |
| Etiquetas con icono (también) | `etiquetas_icono` | S | 2 a 4 condiciones o capacidades | `fila_parametros`, `icono_dato` |
| Fila de parámetros técnicos (también) | `fila_parametros` | L | 3 a 6 condiciones técnicas de partida | `icono_dato`, `etiquetas_icono` |
| Mapa de portfolio (también) | `matriz_portfolio` | M | Productos de un actor por vía o segmento | `tabla_comparativa`, `mapa_calor` |
| Muro de logos (también) | `muro_logos` | M | Actores de un segmento, solo nombre o logo | `ficha_linea`, `grupo_fichas`, `grupo_logos` |
| Sunburst (también) | `sunburst` | M | Un total con dos niveles (familia y subcategoría) | `treemap`, `anillo_categorias` |
| Venn (también) | `venn` | M | 2 o 3 condiciones y su intersección | `mapa_alcance`, `circulos_concentricos` |

### ¿Cómo fluye el valor? (`cadena`)

Eslabones de la cadena, actores, modelo de negocio.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Cadena de valor en capas | `cadena_capas` | L | 4 a 7 eslabones con filas de análisis (actores, margen, tendencia) | `cadena_isometrica`, `circuito_cadena`, `sankey`, `cadena_margen` |
| Cadena de valor isométrica | `cadena_isometrica` | L | 4 a 7 fases con escena, texto y dato | `cadena_capas`, `chevrones` |
| Cadena con margen y valor capturado | `cadena_margen` | L | 3 a 7 eslabones con margen, valor capturado y posición del cliente | `cadena_capas`, `cadena_isometrica` |
| Circuito de la cadena | `circuito_cadena` | L | Eslabones con un actor que se engancha por dos flechas | `cadena_capas`, `lienzo_negocio`, `red_nodos` |
| Lienzo de modelo de negocio | `lienzo_negocio` | L | Las nueve cajas del business model canvas | `circuito_cadena`, `ficha_empresa` |
| Red de nodos (también) | `red_nodos` | M | Actores y sus relaciones (ecosistema) | `radial`, `sankey`, `circuito_cadena` |
| Flujos (Sankey) (también) | `sankey` | M | Flujos de volumen entre dos clasificaciones | `marimekko`, `red_nodos`, `cadena_capas` |
| Trayecto de hoy al destino (también) | `trayecto` | L | 2 a 4 etapas: hoy, destino y vía | `chevrones`, `escalones`, `fases_gates` |

### ¿En qué orden se hace? (`proceso`)

Pasos, fases, responsables.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Chevrones de proceso | `chevrones` | L | 3 a 6 etapas lineales, con la actual marcada | `proceso_flechas`, `escalones`, `linea_tiempo`, `fases_gates` |
| Ciclo | `ciclo` | M | 3 a 6 pasos que se repiten | `chevrones`, `radial` |
| Embudo de discos | `embudo` | M | 3 a 6 etapas de un cribado con su recuento | `dimensionamiento`, `circulos_concentricos`, `escalones` |
| Escalones | `escalones` | M | Etapas de madurez o ambición que suben | `piramide`, `chevrones`, `curva_s` |
| Fases con gates | `fases_gates` | L | 2 a 4 fases con plazo, acciones y gate | `chevrones`, `gantt`, `proceso_flechas` |
| Proceso por carriles | `proceso_carriles` | L | Pasos repartidos por responsable con traspasos | `proceso_flechas`, `carriles`, `arbol_tramite` |
| Proceso en flechas con entregables | `proceso_flechas` | L | 3 a 5 pasos con qué se resuelve, qué sale y quién | `chevrones`, `proceso_carriles` |
| Árbol de trámite (también) | `arbol_tramite` | L | Una pregunta sí o no con una vía directa y un recorrido | `proceso_carriles`, `chevrones`, `arbol_opciones` |
| Hoja de ruta por carriles (también) | `carriles` | L | Iniciativas por carril y periodo | `gantt`, `proceso_carriles` |
| Miniatura de proceso (también) | `mini_flechas` | S | Hasta 4 pasos | `proceso_flechas`, `chevrones` |

### ¿Cuándo? (`calendario`)

Cronograma, hitos, hoja de ruta, historial.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Calendario de calor | `calendario_calor` | L | Actividad por día durante meses | `mapa_calor`, `linea` |
| Hoja de ruta por carriles | `carriles` | L | Iniciativas por carril y periodo | `gantt`, `proceso_carriles` |
| Gantt | `gantt` | L | Fases con barras por fechas, hoy y decisión | `carriles`, `linea_tiempo`, `fases_gates` |
| Línea de tiempo | `linea_tiempo` | L | Hitos con fecha, pasados, hoy y futuros | `linea_tiempo_vertical`, `gantt`, `lista_precedentes` |
| Línea de tiempo vertical | `linea_tiempo_vertical` | M | Hitos con texto largo | `linea_tiempo`, `lista_precedentes` |
| Fases con gates (también) | `fases_gates` | L | 2 a 4 fases con plazo, acciones y gate | `chevrones`, `gantt`, `proceso_flechas` |
| Lista de precedentes (también) | `lista_precedentes` | S | 4 a 8 decisiones pasadas con su estado | `linea_tiempo_vertical`, `tabla_comparativa` |

### ¿Qué hacemos? (`decidir`)

Prioridades, escenarios, criterios y salidas de una decisión.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Árbol de opciones | `arbol_opciones` | L | Categorías con opciones numeradas y su explicación | `arbol_tramite`, `tarjetas_salida`, `mapa_alcance` |
| Árbol de trámite | `arbol_tramite` | L | Una pregunta sí o no con una vía directa y un recorrido | `proceso_carriles`, `chevrones`, `arbol_opciones` |
| Balanza | `balanza` | M | Argumentos a favor y en contra, o dos alternativas | `dafo`, `tabla_comparativa`, `nucleo_dos_lados` |
| Columnas de requisitos con coste y plazo | `columnas_requisitos` | L | 2 a 4 dimensiones con requisitos, coste y plazo | `columnas_numeradas`, `tabla_comparativa` |
| Escalera de prioridad | `escalera_prioridad` | L | Hasta 3 niveles de prioridad con 5 focos cada uno | `matriz_2x2`, `pareto`, `tabla_vigilancia` |
| Lista numerada | `lista_numerada` | M | 3 a 5 recomendaciones o pasos | `tarjetas_salida`, `pilares`, `columnas_numeradas` |
| Scorecard | `scorecard` | L | Criterios eliminatorios y comparativos con su peso | `criterios_puntos`, `tabla_comparativa` |
| Tabla de vigilancia | `tabla_vigilancia` | L | Opciones no prioritarias con su disparador y actores | `escalera_prioridad`, `tabla_comparativa` |
| Tarjetas de escenario | `tarjetas_escenario` | L | 2 o 3 escenarios con dato, texto y visual pequeño | `abanico`, `tarjetas_salida`, `balanza` |
| Tarjetas de salida | `tarjetas_salida` | L | 2 a 4 escenarios o salidas con su alcance | `balanza`, `arbol_tramite`, `lista_numerada` |
| Trayecto de hoy al destino | `trayecto` | L | 2 a 4 etapas: hoy, destino y vía | `chevrones`, `escalones`, `fases_gates` |
| Fases con gates (también) | `fases_gates` | L | 2 a 4 fases con plazo, acciones y gate | `chevrones`, `gantt`, `proceso_flechas` |
| Mapa de alcance (también) | `mapa_alcance` | L | Opciones por dimensión que entran, entran en parte o no | `anillo_categorias`, `venn`, `arbol` |
| Matriz 2 × 2 (también) | `matriz_2x2` | M | Elementos en dos ejes cualitativos con cuadrantes | `dispersion`, `escalera_prioridad` |
| Matriz de puntuación (también) | `matriz_puntuacion` | L | Opciones agrupadas por veredicto con notas de 0 a 3 y total | `mapa_calor`, `tabla_comparativa`, `criterios_puntos` |
| Miniatura de bifurcación (también) | `mini_bifurcacion` | S | Una etapa, un corte y dos ramas | `arbol_tramite` |
| Miniatura de escalera (también) | `mini_escalera` | S | 3 niveles con códigos | `escalera_prioridad` |
| Panel de KPI (también) | `panel_kpi` | L | KPI que deciden arriba y condiciones abajo | `bala`, `tarjeta_kpi` |
| Pareto (también) | `pareto` | M | 1 serie de causas o elementos con su acumulado | `barras_ranking`, `treemap` |
| Tabla comparativa (también) | `tabla_comparativa` | L | 2 a 5 opciones en 4 a 10 criterios | `criterios_puntos`, `matriz_puntuacion`, `radar` |

### ¿Quién es? (`perfil`)

Empresa, persona, actor u opción en ficha.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Ecosistema de logos por grupos | `ecosistema_logos` | L | De 10 a 70 actores (partners, aliados, candidatos) en 2 a 6 grupos, con logo o nombre | `muro_logos`, `categorias_chips`, `mapa_actores`, `ficha_linea` |
| Ficha de empresa de un vistazo | `ficha_empresa` | L | Datos clave, ingresos, diferenciadores, cita y madurez | `ficha_linea`, `tarjeta_actor`, `lienzo_negocio`, `combo_financiero` |
| Ficha de hipótesis | `ficha_hipotesis` | L | Lo probado, la hipótesis, criterios con nota y ejemplos | `columnas_evolucion`, `ficha_empresa` |
| Ficha de una línea por empresa | `ficha_linea` | L | 10 a 20 empresas con madurez y frase | `tabla_con_barras`, `muro_logos` |
| Ficha de startup sin ingresos | `ficha_startup` | L | Datos clave y cuatro bloques de texto | `ficha_empresa`, `ficha_linea`, `tarjeta_actor` |
| Grupo de fichas | `grupo_fichas` | S | 2 a 6 casos con icono, dato y origen | `tarjeta_actor`, `icono_dato` |
| Grupo de logos | `grupo_logos` | S | Logos o nombres de una columna (tier, vía, segmento) | `muro_logos`, `tarjeta_actor` |
| Mapa de portfolio | `matriz_portfolio` | M | Productos de un actor por vía o segmento | `tabla_comparativa`, `mapa_calor` |
| Muro de logos | `muro_logos` | M | Actores de un segmento, solo nombre o logo | `ficha_linea`, `grupo_fichas`, `grupo_logos` |
| Persona con monograma | `persona` | S | Nombre y cargo | `organigrama`, `tarjeta_actor` |
| Tarjeta de empresa | `tarjeta_actor` | S | Nombre, país y tipo, logo y una frase | `ficha_linea`, `persona` |
| Mapa de categorías con chips (también) | `categorias_chips` | L | 8 a 30 nombres en 3 a 9 categorías, con un estado transversal | `anillo_categorias`, `muro_logos`, `grupo_logos` |
| De lo probado a lo nuevo (también) | `columnas_evolucion` | L | 2 a 4 columnas con lo probado, lo nuevo, quién y el reto | `ficha_hipotesis`, `nucleo_dos_lados`, `antes_despues_imagen` |
| Métricas financieras (combo) (también) | `combo_financiero` | M | Ingresos, EBITDA y margen de una empresa en 3 a 6 periodos | `columnas`, `linea`, `ficha_empresa` |
| Lienzo de modelo de negocio (también) | `lienzo_negocio` | L | Las nueve cajas del business model canvas | `circuito_cadena`, `ficha_empresa` |
| Línea de tiempo vertical (también) | `linea_tiempo_vertical` | M | Hitos con texto largo | `linea_tiempo`, `lista_precedentes` |
| Organigrama (también) | `organigrama` | L | Personas o unidades en 2 o 3 niveles | `arbol`, `persona` |
| Araña (radar) (también) | `radar` | M | 1 o 2 perfiles en 5 a 8 criterios de la misma escala | `criterios_puntos`, `tabla_comparativa`, `deslizadores`, `score_dimensiones` |
| Score por dimensiones (también) | `score_dimensiones` | M | Valor de un actor en 4 a 8 dimensiones y su total | `radar`, `deslizadores`, `criterios_puntos` |
| Tabla de vigilancia (también) | `tabla_vigilancia` | L | Opciones no prioritarias con su disparador y actores | `escalera_prioridad`, `tabla_comparativa` |

### ¿De dónde sale y cuánto fiarse? (`evidencia`)

Fuentes, confianza, citas, entrevistas.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Afirmación y evidencia | `afirmacion_evidencia` | L | 2 a 4 afirmaciones con su cita y autor | `cita`, `panel_entrevistas` |
| Cita destacada | `cita` | S | Una cita con autor | `panel_entrevistas`, `aviso`, `afirmacion_evidencia` |
| Columna de contexto | `columna_contexto` | S | Rótulo, 2 o 3 párrafos y una cifra ancla | `contadores`, `tarjeta_cifra`, `bloque` |
| Nivel de evidencia | `etiqueta_evidencia` | S | A, B o C junto a un dato | `chip_nota` |
| Lista de precedentes | `lista_precedentes` | S | 4 a 8 decisiones pasadas con su estado | `linea_tiempo_vertical`, `tabla_comparativa` |
| Panel de entrevistas | `panel_entrevistas` | L | Entrevistas por perspectiva y su detalle | `cita`, `contadores` |
| Recuadro de llamada (también) | `aviso` | S | Un supuesto crítico o una advertencia | `cita` |
| Barra dividida (Likert) (también) | `barra_dividida` | M | Respuestas en una escala de acuerdo por afirmación | `barras_apiladas` |
| Diagrama de cajas (también) | `cajas` | M | Observaciones por grupo (ensayos, paneles) | `histograma`, `rangos`, `benchmark_rango` |
| Contadores (también) | `contadores` | S | 2 a 4 cifras grandes con de dónde salen | `icono_dato`, `tarjeta_cifra`, `columna_contexto` |
| Deslizadores de valoración (también) | `deslizadores` | M | Valoraciones cualitativas de 0 a 1 con su razón | `radar`, `harvey`, `valoracion`, `score_dimensiones` |
| Fórmula de cálculo (también) | `formula` | L | Factores con cifra y fuente unidos por operadores | `arbol_drivers`, `dimensionamiento`, `cascada` |
| Grupo de fichas (también) | `grupo_fichas` | S | 2 a 6 casos con icono, dato y origen | `tarjeta_actor`, `icono_dato` |
| Tabla con barra frente a referencia (también) | `tabla_referencia` | L | Filas con una barra frente a objetivo y referencia | `tabla_con_barras`, `barras_objetivo` |

### ¿Cómo va? (`estado`)

Avance, cumplimiento, semáforo.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Barra de progreso | `barra_progreso` | S | Avance sobre un total conocido | `indicador`, `bala` |
| Chip de variación | `delta` | S | Una variación con tono bueno, neutro o malo | `cifra_delta` |
| Marcas sí, parcial y no | `marca` | S | Cumplimiento en celdas | `harvey`, `semaforo` |
| Semáforo de estado | `semaforo` | S | Estado ok, riesgo o bloqueo | `marca`, `barra_progreso` |
| Avance hacia objetivo (también) | `bala` | M | 3 a 6 KPI con valor, objetivo y máximo | `barras_objetivo`, `indicador`, `barra_progreso` |
| KPI con variación (también) | `cifra_delta` | S | Cifra, variación y minilínea | `tarjeta_cifra`, `indicador`, `contadores` |
| Indicador (gauge) (también) | `indicador` | S | Un KPI de avance con objetivo | `bala`, `barra_progreso`, `tarjeta_cifra` |
| Píldoras de estado (también) | `pill` | S | Una etiqueta corta de estado o categoría | `semaforo` |

### Dar contexto visual (`ilustrar`)

Escenas isométricas, imágenes, antes y después.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Antes y después en imagen | `antes_despues_imagen` | M | Dos imágenes con rótulo | `columnas_evolucion`, `escena_iso` |
| Catálogo de escenas | `catalogo_escenas` | L | Todas las escenas registradas, con su clave | `escena_iso` |
| Escena isométrica suelta | `escena_iso` | S | Una escena del catálogo ESCENAS o una propia | `icono_caja`, `antes_despues_imagen` |
| Cadena de valor isométrica (también) | `cadena_isometrica` | L | 4 a 7 fases con escena, texto y dato | `cadena_capas`, `chevrones` |

### Sintetizar (`resumir`)

Resumen que remite a otras slides, mensajes clave.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Columnas numeradas con cifras | `columnas_numeradas` | L | 2 a 4 ideas con título, texto y una o dos cifras | `lista_numerada`, `pilares`, `tarjetas_miniatura` |
| Miniatura de barras | `mini_barras_objetivo` | S | Hasta 3 barras frente a referencia y objetivo | `barras_objetivo` |
| Miniatura de bifurcación | `mini_bifurcacion` | S | Una etapa, un corte y dos ramas | `arbol_tramite` |
| Miniatura de conteo | `mini_conteo` | S | Hasta 10 círculos con los marcados | `pictograma` |
| Miniatura de escalera | `mini_escalera` | S | 3 niveles con códigos | `escalera_prioridad` |
| Miniatura de proceso | `mini_flechas` | S | Hasta 4 pasos | `proceso_flechas`, `chevrones` |
| Miniatura de iconos | `mini_iconos` | S | 2 a 4 iconos con una palabra | `etiquetas_icono` |
| Tarjetas con miniatura | `tarjetas_miniatura` | L | 2 a 4 conclusiones con una miniatura de la slide que resumen | `lista_numerada`, `pilares` |
| Afirmación y evidencia (también) | `afirmacion_evidencia` | L | 2 a 4 afirmaciones con su cita y autor | `cita`, `panel_entrevistas` |
| Lista numerada (también) | `lista_numerada` | M | 3 a 5 recomendaciones o pasos | `tarjetas_salida`, `pilares`, `columnas_numeradas` |
| Casa estratégica (pilares) (también) | `pilares` | L | Ambición, 3 a 5 pilares y bases | `capas`, `lista_numerada` |

### Pieza auxiliar (`apoyo`)

Leyendas, separadores, llaves, píldoras: nunca protagonistas.

| Elemento | Función | Escala | Datos | Alternativas |
|---|---|---|---|---|
| Recuadro de llamada | `aviso` | S | Un supuesto crítico o una advertencia | `cita` |
| Bloque con filete superior | `bloque` | S | Título y texto corto o HTML | `aviso`, `tarjeta_cifra`, `columna_contexto` |
| Etiquetas con icono | `etiquetas_icono` | S | 2 a 4 condiciones o capacidades | `fila_parametros`, `icono_dato` |
| Icono en caja | `icono_caja` | S | Un icono de Material Symbols en su caja | `escena_iso` |
| Leyenda | `leyenda` | S | Colores y formas de las series, solo si no cabe la etiqueta directa |  |
| Llave de agrupación | `llave` | S | Una lectura común para un grupo de elementos |  |
| Píldoras de estado | `pill` | S | Una etiqueta corta de estado o categoría | `semaforo` |
| Separador de bloque | `separador` | S | Número y título de un bloque dentro de la slide |  |
| Catálogo de escenas (también) | `catalogo_escenas` | L | Todas las escenas registradas, con su clave | `escena_iso` |
| Nota 0 a 3 con confianza (también) | `chip_nota` | S | Nota y confianza de una celda de matriz | `harvey`, `valoracion` |
| Chip de variación (también) | `delta` | S | Una variación con tono bueno, neutro o malo | `cifra_delta` |
| Nivel de evidencia (también) | `etiqueta_evidencia` | S | A, B o C junto a un dato | `chip_nota` |
| Grupo de logos (también) | `grupo_logos` | S | Logos o nombres de una columna (tier, vía, segmento) | `muro_logos`, `tarjeta_actor` |
| Bolas de Harvey (también) | `harvey` | S | Nivel de 0 a 4 | `valoracion`, `marca` |
| Marcas sí, parcial y no (también) | `marca` | S | Cumplimiento en celdas | `harvey`, `semaforo` |
| Minilínea (sparkline) (también) | `sparkline` | S | Una serie corta, sin ejes | `cifra_delta`, `pequenos_multiplos` |
| Puntos de valoración (también) | `valoracion` | S | Nota de n sobre 5 | `harvey` |

## Por familia (dónde está el código)

### Magnitud · `ea_elementos/magnitud.py`

Cuánto: comparar cantidades.

- **`columnas`** (Columnas). comparar de 3 a 8 magnitudes de una misma unidad, o una serie temporal corta con su previsión y CAGR. *Cuándo no:* más de 10 categorías o rótulos largos (usa barras_ranking).
- **`barras_ranking`** (Ranking en barras). ordenar de 5 a 15 elementos con rótulos largos (mercados, empresas, ingredientes). *Cuándo no:* series temporales (usa columnas o linea) o si el orden no importa.
- **`barras_agrupadas`** (Columnas agrupadas). comparar dos momentos o dos actores en 3 a 6 categorías. *Cuándo no:* más de tres series (pasa a mapa_calor o a pequeños múltiplos).
- **`barras_apiladas`** (Barras apiladas al 100 %). la composición de 3 a 6 elementos (mezcla de canales, reparto de un gasto). *Cuándo no:* si lo que importa es comparar un tramo intermedio entre filas (cuesta leerlo; usa barras_agrupadas).
- **`piruletas`** (Piruletas (lollipop)). muchas barras de valores parecidos, donde la barra llena pesa demasiado. *Cuándo no:* si los valores tienen que sumarse visualmente (usa barras).
- **`pictograma`** (Pictograma). traducir un porcentaje a personas u objetos («7 de cada 10 consumidores»). *Cuándo no:* para valores con decimales o comparaciones entre varios grupos (usa columnas).
- **`pareto`** (Pareto). decir dónde concentrar el esfuerzo (causas de merma, partidas de coste, motivos de rechazo). *Cuándo no:* si las categorías no son sumables o el reparto es plano (no hay un 80/20 que contar).
- **`comparador_unidad`** (Comparador por unidad). propuestas de proveedor, sustitución de ingredientes, coste por dosis o por ración. *Cuándo no:* si las opciones no son equivalentes por unidad (rendimientos distintos sin normalizar).
- **`barras_variacion`** (Barras de variación). cambios de cuota, precio o volumen entre dos fechas para 5 a 20 elementos. *Cuándo no:* si importan los valores de partida y llegada (usa pendiente o mancuerna).
- **`embudo`** (Embudo de discos). un cribado con etapas (documentos, candidatos), uno por bloque como máximo. *Cuándo no:* si las etapas no son un filtro sucesivo, o si ya hay otro embudo en el bloque (pasa los datos a contadores).
- **`ranking_logos`** (Ranking por logo). el resultado consolidado de un scoring cuando el lector reconoce a los actores por su logo. *Cuándo no:* si interesa la distancia entre valores (usa barras_ranking o tabla_con_barras).

### Evolución · `ea_elementos/evolucion.py`

Cómo cambia en el tiempo.

- **`linea`** (Líneas con serie destacada). una tendencia en el tiempo con 1 a 4 series y al menos 5 puntos. *Cuándo no:* con 2 o 3 puntos (usa columnas o pendiente).
- **`area_apilada`** (Áreas apiladas). cómo crece un total y cómo cambia su composición (2 a 4 componentes). *Cuándo no:* si interesa la evolución exacta de una banda intermedia (usa linea).
- **`pendiente`** (Pendiente (slope)). quién sube y quién baja entre dos fechas, con 3 a 8 elementos. *Cuándo no:* con más de dos momentos (usa linea).
- **`cascada`** (Cascada (waterfall)). explicar un puente entre dos cifras (de 18 g a 12 g de azúcar, del coste actual al objetivo). *Cuándo no:* si las palancas no son sumables entre sí.
- **`sparkline`** (Minilínea (sparkline)). dar la forma de una tendencia junto a una cifra (cifra_delta, tablas). *Cuándo no:* si hay que leer valores concretos (usa linea).
- **`curva_s`** (Curva en S de adopción). vigilancia tecnológica, para decir si una tecnología es temprana o ya está madura. *Cuándo no:* si hay datos reales de adopción por año (usa linea con los datos).
- **`abanico`** (Abanico de escenarios). previsiones de mercado o de volumen con incertidumbre explícita. *Cuándo no:* si solo hay un escenario (usa linea con la previsión discontinua).
- **`bump`** (Ranking en el tiempo (bump)). quién adelanta a quién en un ranking (cuota, patentes, ventas) en 4 a 8 periodos. *Cuándo no:* si importan las distancias entre puestos (usa linea con los valores).
- **`pequenos_multiplos`** (Pequeños múltiplos). comparar la forma de 4 a 12 series sin enredarlas en un solo gráfico. *Cuándo no:* si hay que leer valores exactos de cada punto (usa una tabla).
- **`combo_financiero`** (Métricas financieras (combo)). fichas de competidor, proveedor o candidato (3 a 6 periodos), sobre todo en slides hermanas. *Cuándo no:* para comparar varias empresas entre sí (usa barras_agrupadas o tabla_con_barras).

### Composición · `ea_elementos/composicion.py`

De qué está hecho un total.

- **`donut`** (Anillo (donut)). una parte de un total con 2 a 5 partes, cuando la cifra central es el mensaje. *Cuándo no:* más de 5 partes o partes parecidas entre sí (usa barras_ranking).
- **`waffle`** (Gofre (waffle)). un porcentaje que tiene que verse como proporción física («31 de cada 100»). *Cuándo no:* porcentajes muy pequeños (menos de 3) o con decimales.
- **`treemap`** (Mapa de árbol (treemap)). el peso relativo de 5 a 15 partes de un total (cuota de mercado, gasto por partida). *Cuándo no:* si hay que comparar partes pequeñas entre sí (usa barras_ranking).
- **`marimekko`** (Marimekko). tamaño de mercado por región y cuota por categoría en una sola figura. *Cuándo no:* con más de 5 columnas o 4 segmentos (se vuelve ilegible).
- **`sankey`** (Flujos (Sankey)). repartos de volumen entre dos clasificaciones (canal de origen a uso final, 6 a 12 flujos). *Cuándo no:* más de dos etapas o flujos muy pequeños (se convierten en hilos ilegibles).
- **`sunburst`** (Sunburst). un total con dos niveles (familia y producto, región y país), de 3 a 5 categorías. *Cuándo no:* si hay que comparar subcategorías de familias distintas (usa barras_ranking).
- **`barra_desglose`** (Barra con desglose). estructuras de coste o de ingresos donde una partida concentra el análisis. *Cuándo no:* si todas las partidas pesan igual (usa barras_apiladas).
- **`anillo_categorias`** (Anillo de categorías). una taxonomía de 6 a 12 elementos en 2 a 4 categorías, cuando importa ver el todo y un estado. *Cuándo no:* con más de 12 elementos (no caben las etiquetas) o si el orden importa (usa escalera_prioridad).

### Comparación · `ea_elementos/comparacion.py`

Frente a un objetivo, una referencia o entre sí.

- **`radar`** (Araña (radar)). comparar perfiles (nosotros frente a la media del sector, candidato A frente a B). *Cuándo no:* más de dos series o criterios con escalas distintas (usa matriz_puntuacion o tabla_comparativa).
- **`mancuerna`** (Mancuerna (dumbbell)). brecha entre dos estados por elemento (actual frente a objetivo, nosotros frente al líder). *Cuándo no:* si interesan los valores absolutos más que la distancia (usa barras_agrupadas).
- **`bala`** (Avance hacia objetivo). cuadros de mando con 3 a 6 KPI frente a su objetivo, en poco espacio. *Cuándo no:* un único KPI protagonista (usa indicador o cifra_delta).
- **`tornado`** (Tornado (sensibilidad)). decir qué supuesto del modelo pesa más (precio, coste de materia prima, volumen). *Cuándo no:* si las variables no son independientes o no hay un caso base.
- **`rangos`** (Rangos (football field)). valoraciones, horquillas de precio o de coste según la fuente. *Cuándo no:* si cada fila es un valor único (usa piruletas).
- **`indicador`** (Indicador (gauge)). un único KPI de avance o de grado de cumplimiento, como pieza de portada de un bloque. *Cuándo no:* varios KPI juntos (usa bala); ocupa mucho para un solo número.
- **`barra_dividida`** (Barra dividida (Likert)). encuestas a consumidores o paneles internos (aceptación, intención de compra). *Cuándo no:* escalas que no son simétricas (usa barras_apiladas).
- **`dimensionamiento`** (Dimensionamiento de arriba abajo). explicar cómo se llega a la cifra de mercado relevante desde una fuente amplia. *Cuándo no:* si los pasos no son filtros sucesivos sobre la misma base (usa cascada).
- **`deslizadores`** (Deslizadores de valoración). valoraciones cualitativas argumentadas (barreras de entrada, riesgos, madurez, atractivo). *Cuándo no:* si hay un dato numérico comparable (usa benchmark_rango o barras).
- **`benchmark_rango`** (Benchmark en rango). benchmarking financiero u operativo frente a 5 a 15 comparables. *Cuándo no:* si hay que ver a cada comparable por separado (usa barras_ranking).
- **`criterios_puntos`** (Criterios con puntos por actor). candidatos frente a los criterios del cliente, o marca frente a competidores en un estudio. *Cuándo no:* más de 8 actores (los puntos se amontonan; usa tabla_comparativa).
- **`barras_objetivo`** (Barras frente a objetivo). de 3 a 8 opciones en la misma métrica y lo que importa es la distancia al objetivo. *Cuándo no:* si las opciones tienen rangos (usa escala_log) o si las métricas son varias (usa tabla_referencia).
- **`barras_duelo`** (Duelo de dos barras). dentro de una tarjeta_kpi, para enseñar la distancia a un umbral. *Cuándo no:* con más de dos valores (usa barras_objetivo).
- **`regleta_objetivo`** (Regleta con zona objetivo). un precio o rango negociable dentro de una tarjeta_kpi. *Cuándo no:* para un umbral único (usa barras_duelo).
- **`escala_log`** (Escala logarítmica). costes o magnitudes que cruzan dos o tres órdenes de magnitud frente a una referencia. *Cuándo no:* si todo cae en el mismo orden de magnitud (usa barras_objetivo); el lector no técnico necesita el «×» en la etiqueta.
- **`score_dimensiones`** (Score por dimensiones). el score de un actor en fichas hermanas (RTW, scoring de candidatos) o de un escenario. *Cuándo no:* para comparar muchos actores a la vez (usa matriz_puntuacion o criterios_puntos).

### Relación y distribución · `ea_elementos/distribucion.py`

Cómo se reparten, se relacionan o se sitúan.

- **`dispersion`** (Dispersión y burbujas). posicionar 5 a 20 elementos en dos variables numéricas (coste frente a madurez). *Cuándo no:* si las variables son cualitativas (usa matriz_2x2).
- **`mapa_calor`** (Mapa de calor). patrones en una tabla de 4 × 4 a 10 × 12 (actividad por país y año, notas por criterio). *Cuándo no:* si cada celda necesita texto (usa tabla_comparativa).
- **`histograma`** (Histograma). enseñar la distribución de una población (precios, edades, puntuaciones de 200 candidatos). *Cuándo no:* con menos de 30 observaciones (mejor dar los valores).
- **`cajas`** (Diagrama de cajas). resultados de paneles sensoriales, ensayos repetidos o precios por canal. *Cuándo no:* con menos de 8 observaciones por grupo (enseña los puntos sin caja).
- **`red_nodos`** (Red de nodos). ecosistemas (quién colabora con quién, coautorías de patentes, inversores comunes). *Cuándo no:* más de 30 nodos o redes muy densas (se vuelve una madeja; usa una matriz).
- **`mapa_coropletico`** (Mapa coroplético). actividad, mercado o presencia por país (dónde están los proveedores, las patentes, la demanda). *Cuándo no:* si el valor depende del tamaño del país (usa valores por habitante) o con menos de 4 países (usa barras).
- **`mapa_burbujas`** (Mapa de burbujas). magnitudes por lugar cuando el tamaño del país engañaría (candidaturas, oficinas, inversión). *Cuándo no:* un valor relativo a cada país (usa mapa_coropletico) o si importa la conexión entre lugares (usa mapa_flujos).
- **`mapa_flujos`** (Mapa de flujos). de dónde sale algo y adónde llega (expansión, exportación, suministro), con un solo origen. *Cuándo no:* varios orígenes cruzados (usa sankey o red_nodos) o sin una dirección clara (usa mapa_burbujas).
- **`mapa_madurez`** (Mapa de madurez (TRL)). una cartera de 20 a 80 tecnologías o candidatos por madurez y evidencia; con fichas a la derecha. *Cuándo no:* si hay que leer cada elemento por su nombre (usa una tabla) o con dos ejes cuantitativos (usa dispersion).
- **`mapa_actores`** (Mapa con grupos de actores). dónde están los fabricantes frente a dónde está la demanda, o un ecosistema por región. *Cuándo no:* si lo que importa es un valor por país (usa mapa_coropletico).

### Marcos y matrices · `ea_elementos/marcos.py`

Cómo se organiza una idea en un esquema.

- **`matriz_2x2`** (Matriz 2 × 2). priorizar con dos criterios (impacto y esfuerzo, atractivo y capacidad). *Cuándo no:* si hay datos numéricos fiables en ambos ejes (usa dispersion).
- **`venn`** (Venn). definir un hueco o un perfil como cruce de condiciones (técnica, mercado, regulación). *Cuándo no:* para cuantificar solapes (los tamaños no son proporcionales).
- **`circulos_concentricos`** (Círculos concéntricos (TAM, SAM, SOM)). tamaño de mercado por capas o un embudo de alcance sin etapas de filtro. *Cuándo no:* si las capas no están contenidas unas en otras.
- **`radial`** (Radial (hub and spoke)). un actor o una capacidad con sus relaciones o componentes (ecosistema, plataforma). *Cuándo no:* si hay relaciones entre satélites o un orden (usa ciclo o chevrones).
- **`piramide`** (Pirámide). jerarquías de necesidad o de valor (higiene, diferenciación, liderazgo). *Cuándo no:* si los niveles no se apoyan unos en otros (usa capas o una lista).
- **`capas`** (Capas (stack)). arquitecturas o modelos de capacidades que se apoyan unos en otros (datos, plataforma, servicios). *Cuándo no:* si no hay dependencia entre capas (usa lista_numerada).
- **`balanza`** (Balanza). una decisión con pros y contras, o dos alternativas que se comparan en conjunto. *Cuándo no:* si los argumentos se pueden puntuar (usa tabla_comparativa o scorecard).
- **`lienzo_negocio`** (Lienzo de modelo de negocio). el modelo de una startup candidata o el de un negocio nuevo del cliente, en una slide. *Cuándo no:* para análisis de detalle de una sola caja (sácala a su propia slide).
- **`mapa_alcance`** (Mapa de alcance). fijar el alcance de un scouting, una vigilancia o un dimensionamiento antes de empezar. *Cuándo no:* si el alcance es una sola lista (usa lista_numerada o pills).
- **`dafo`** (DAFO). diagnóstico rápido de una empresa, una tecnología o una opción de entrada. *Cuándo no:* como conclusión (el DAFO ordena, no decide; acompáñalo de la recomendación).
- **`cinco_fuerzas`** (Cinco fuerzas). atractivo de un sector o de un segmento en una propuesta o un diagnóstico. *Cuándo no:* si el análisis es de una sola empresa frente a sus competidores (usa tabla_comparativa).
- **`pilares`** (Casa estratégica (pilares)). resumir un plan estratégico o una hoja de ruta de innovación en una sola imagen. *Cuándo no:* si los pilares no comparten una ambición común (usa lista_numerada).
- **`nucleo_dos_lados`** (Núcleo con dos lados). dos capas o palancas complementarias que se combinan con una pieza central (proceso y conservación alrededor del ingrediente); de 3 a 6 filas por lado, el mismo número a los dos lados. *Cuándo no:* si las dos mitades no comparten núcleo (usa dos columnas) o si hay más de dos capas.
- **`escalera_prioridad`** (Escalera de prioridad). la recomendación de dónde poner el esfuerzo y qué se busca en cada foco. *Cuándo no:* si la prioridad sale de una puntuación que hay que enseñar (usa antes matriz_puntuacion).
- **`columnas_evolucion`** (De lo probado a lo nuevo). hacer creíble con un ejemplo concreto un mensaje abstracto («lo nuevo es el producto»); 2 a 4 columnas. *Cuándo no:* si no hay una cifra por columna o si las columnas no comparten estructura.
- **`convergencia`** (Convergencia). decir que varias fuerzas llevan a lo mismo (regulación, industria y comercio exigen inversión). *Cuándo no:* si las causas se suman o se ordenan (usa abanico o lista_numerada).

### Árboles y descomposición · `ea_elementos/arboles.py`

De qué depende algo, rama a rama.

- **`arbol`** (Árbol de problemas). descomponer una pregunta en sub-preguntas MECE, o un organigrama de responsabilidades. *Cuándo no:* más de 3 niveles o de 12 hojas (partir en dos slides).
- **`espina_pescado`** (Espina de pescado (Ishikawa)). diagnóstico de causas raíz de un fallo de producto o de proceso. *Cuándo no:* si las causas ya están priorizadas (usa barras_ranking o arbol).
- **`organigrama`** (Organigrama). equipo del cliente y sus interlocutores, o la estructura del proyecto con EA. *Cuándo no:* más de 8 cajas en el nivel más ancho (agrupar por áreas o partir en dos).
- **`formula`** (Fórmula de cálculo). enseñar el método de una cifra (tamaño de mercado, ahorro, business case) en una línea. *Cuándo no:* si hay más de 5 factores o varios niveles (usa arbol_drivers).
- **`arbol_drivers`** (Árbol de drivers). explicar qué mueve un resultado (ingresos = volumen × precio) o dónde actuar. *Cuándo no:* si los factores no se combinan aritméticamente (usa arbol).
- **`arbol_tramite`** (Árbol de trámite). un trámite o criterio de paso con una sola bifurcación (regulación, aprobación, compra). *Cuándo no:* con más de una pregunta encadenada (el árbol deja de leerse); para fases en el tiempo usa gantt.
- **`abanico_foco`** (Abanico desde un foco). las partes de una idea que salen de un mismo origen (cinco barreras de entrada, lo que implica una vía). *Cuándo no:* si las filas son pasos en orden (usa chevrones) o se descomponen a su vez (usa arbol).
- **`arbol_opciones`** (Árbol de opciones). rutas o alternativas agrupadas por una condición (IP temprana o madura, con o sin planta). *Cuándo no:* si hay una pregunta sí o no con un recorrido (usa arbol_tramite).

### Cadena de valor · `ea_elementos/cadena.py`

Cómo fluye el valor entre eslabones y actores, con escenas isométricas.

- **`cadena_capas`** (Cadena de valor en capas). explicar un sector y decir dónde está el valor y dónde entrar, en una slide completa. *Cuándo no:* si solo hay un dato por eslabón (usa cadena_isometrica o chevrones).
- **`circuito_cadena`** (Circuito de la cadena). explicar por qué un competidor o socio gana con un modelo (circular, de dependencia), no con un producto. *Cuándo no:* para una cadena de valor sin actor que se engancha (usa proceso_flechas o una cadena simple).
- **`cadena_isometrica`** (Cadena de valor isométrica). abrir un informe o una propuesta presentando la cadena del sector con peso visual (4 a 7 fases). *Cuándo no:* para el análisis detallado por eslabón (usa cadena_capas, que puede ir justo después).
- **`escena_iso`** (Escena isométrica suelta). ilustrar un eslabón, un actor o un tipo de instalación junto a texto o datos. *Cuándo no:* como decoración sin significado (cada escena tiene que corresponder a lo que se cuenta).
- **`catalogo_escenas`** (Catálogo de escenas). 
- **`cadena_margen`** (Cadena con margen y valor capturado). decir en qué eslabón está el valor y dónde se sitúa el cliente, con 3 a 7 eslabones. *Cuándo no:* si hacen falta actores, tendencia y oportunidad por eslabón (usa cadena_capas).
- **`trayecto`** (Trayecto de hoy al destino). la recomendación en una slide (de materia prima a excipiente, de proveedor a socio). *Cuándo no:* si el camino tiene pasos con plazos y entregables (usa fases_gates o chevrones).

### Secuencia y tiempo · `ea_elementos/secuencia.py`

En qué orden y cuándo.

- **`chevrones`** (Chevrones de proceso). un proceso lineal de 3 a 6 etapas, o dónde estamos dentro de él. *Cuándo no:* si cada etapa necesita más de dos líneas (usa proceso_flechas).
- **`linea_tiempo`** (Línea de tiempo). historia de un proyecto o calendario de hitos (5 a 9) sin duraciones. *Cuándo no:* si importan las duraciones y los solapes (usa gantt o carriles).
- **`ciclo`** (Ciclo). procesos que se repiten (mejora continua, ciclo de vida, rueda de innovación). *Cuándo no:* si el proceso tiene principio y fin (usa chevrones).
- **`carriles`** (Hoja de ruta por carriles). roadmap a 12 o 24 meses o horizontes H1, H2 y H3 con 3 a 6 carriles. *Cuándo no:* planificación semanal con dependencias (usa gantt).
- **`escalones`** (Escalones). un modelo de madurez o un plan por fases donde cada fase se apoya en la anterior. *Cuándo no:* si las fases son paralelas (usa columnas de tarjetas).
- **`calendario_calor`** (Calendario de calor). ritmos de publicación, de producción o de entradas en un sistema a lo largo de meses. *Cuándo no:* menos de 8 semanas de datos (usa columnas por semana).
- **`linea_tiempo_vertical`** (Línea de tiempo vertical). la historia de una empresa en una ficha, o hitos con más de una línea de explicación. *Cuándo no:* más de 7 hitos en una slide (usa linea_tiempo horizontal).
- **`proceso_carriles`** (Proceso por carriles). quién hace qué en un proceso con traspasos (homologar un proveedor, aprobar un claim). *Cuándo no:* procesos de un solo responsable (usa chevrones) o con más de 12 pasos.
- **`proceso_flechas`** (Proceso en flechas con entregables). un método de 3 a 5 pasos en el que importa quién hace qué y qué entrega cada paso. *Cuándo no:* si el proceso tiene ramas (usa arbol_tramite) o fechas (usa gantt); no dictar el protocolo del cliente.
- **`gantt`** (Gantt). el cronograma de un proyecto de 8 a 30 semanas con 3 a 6 fases y una decisión. *Cuándo no:* para más de 6 filas o un plan de detalle por tareas (va en Excel o en el PM); sin fechas, usa proceso_flechas.
- **`lista_precedentes`** (Lista de precedentes). el historial de decisiones de un regulador, comité o cliente, de 4 a 8 entradas, junto a un árbol. *Cuándo no:* si no hay estado favorable o desfavorable (usa una lista simple); el verde no se usa para nada más.
- **`fases_gates`** (Fases con gates). próximos pasos con disciplina de decisión (validar demanda antes de invertir). *Cuándo no:* un calendario con fechas reales (usa gantt) o pasos sin punto de decisión (usa chevrones).

### Cifras y KPI · `ea_elementos/cifras.py`

Una o pocas cifras que mandan.

- **`cifra_delta`** (KPI con variación). filas de 3 o 4 KPI de seguimiento en una slide de situación o de resultados. *Cuándo no:* KPI de un Stage-Gate con umbral y validación (usa tarjeta_kpi).
- **`icono_dato`** (Dato con icono). datos de contexto en el lateral o la cabecera de un bloque (mercado, equipo, alcance). *Cuándo no:* si las cifras se comparan entre sí (usa columnas).
- **`contadores`** (Contadores). de 2 a 4 magnitudes que dan base a un mensaje (alcance de una búsqueda, tamaño de una muestra), al lado de un visual. *Cuándo no:* si las cifras se comparan entre sí (usa barras_objetivo) o si son más de 4 (pasa a tabla).
- **`tarjeta_cifra`** (Tarjeta con cifra). lecturas de apoyo junto a una gráfica (columna derecha) o tres o cuatro datos de contexto de mercado. *Cuándo no:* como adorno; si la cifra no se puede explicar o no tiene origen, no va. Sin números de orden decorativos.
- **`tarjeta_kpi`** (Tarjeta de KPI de éxito). métricas de éxito y criterios de un Stage-Gate, de 2 a 4 tarjetas. *Cuándo no:* para KPIs de seguimiento con serie temporal (usa cifra_delta).
- **`panel_kpi`** (Panel de KPI). la slide de métricas de éxito de un proyecto con Stage-Gate. *Cuándo no:* si todas las métricas pesan igual (una sola fila de tarjetas).
- **`fila_parametros`** (Fila de parámetros técnicos). las condiciones de partida de un reto (temperatura, pH, viscosidad), de 3 a 6 valores. *Cuándo no:* para resultados o KPIs (usa tarjeta_kpi); el rojo pleno pesa mucho, una fila por slide como máximo.

### Fichas y texto · `ea_elementos/fichas.py`

Quién es, qué dice y qué sale, en tarjetas y bloques de texto.

- **`ficha_empresa`** (Ficha de empresa de un vistazo). perfil de una startup, un proveedor o un candidato antes de la entrevista (una por slide). *Cuándo no:* para listas largas (usa ficha_linea).
- **`ficha_linea`** (Ficha de una línea por empresa). listas largas de candidatos (10 a 20) en una o dos slides, antes de las fichas completas. *Cuándo no:* si hay que comparar varias dimensiones con nota (usa matriz_puntuacion).
- **`tarjeta_actor`** (Tarjeta de empresa). 
- **`persona`** (Persona con monograma). equipo del proyecto, interlocutores o expertos entrevistados. *Cuándo no:* en portadas (la norma de portada prohíbe fotos e iconos).
- **`muro_logos`** (Muro de logos). quién está en un segmento (startups, proveedores, partners, aliados, clientes de referencia). *Cuándo no:* si hace falta decir algo de cada empresa (usa grupo_fichas o tarjeta_actor); si los actores van por fases, estados o tipos (usa ecosistema_logos).
- **`ecosistema_logos`** (Ecosistema de logos por grupos). que se vea el universo entero (de 10 a 70 actores en 2 a 6 grupos): candidatos por fase, partners y aliados. *Cuándo no:* un solo grupo (usa muro_logos); si importa dónde están (usa mapa_actores); si hay que decir algo de cada uno (usa ficha_linea).
- **`grupo_fichas`** (Grupo de fichas). al lado de mapa_madurez (o de cualquier gráfico) para nombrar los casos que importan; de 2 a 6 fichas. *Cuándo no:* como lista suelta sin visual al lado; una sola cifra por ficha.
- **`ficha_hipotesis`** (Ficha de hipótesis). slides hermanas, una por opción priorizada (dos a cuatro), con la misma plantilla. *Cuándo no:* para una sola opción sin hermanas (sobra la estructura) o sin ejemplos reales que mostrar.
- **`tarjetas_salida`** (Tarjetas de salida). las salidas de una decisión (si sí, si no, fuera de alcance) bajo un gantt o un árbol; 2 a 4. *Cuándo no:* como lista de recomendaciones sin decisión detrás (usa tarjetas_miniatura).
- **`cita`** (Cita destacada). voz del cliente o del mercado que respalda una conclusión (una por slide). *Cuándo no:* citas sin autor identificable o que solo repiten el título.
- **`lista_numerada`** (Lista numerada). recomendaciones, próximos pasos o conclusiones (3 a 5). *Cuándo no:* si el orden no significa nada (usa icono_dato o viñetas).
- **`aviso`** (Recuadro de llamada). una advertencia, un supuesto crítico o una idea que no puede perderse, dentro del cuerpo. *Cuándo no:* para la conclusión de la slide (eso es la banda de cuerpo_slide).
- **`etiquetas_icono`** (Etiquetas con icono). 
- **`antes_despues_imagen`** (Antes y después en imagen). el cambio visible de un producto, envase o proceso, con material del cliente. *Cuándo no:* con fotos de banco de imágenes (si no es el producto real, no aporta).
- **`columna_contexto`** (Columna de contexto). explicar el método o el contexto de la pieza vecina (un embudo, un Gantt, un mapa) y dejar una cifra. *Cuándo no:* si la columna solo repite lo que ya dice el visual; mejor dar más ancho a la pieza.
- **`bloque`** (Bloque con filete superior). dos o tres bloques de texto que se leen por separado (contexto, brecha, implicación). *Cuándo no:* si el texto se puede convertir en un visual (D1); para la conclusión de la slide (usa la banda).
- **`columnas_numeradas`** (Columnas numeradas con cifras). el resumen ejecutivo o la síntesis de evidencia en 2 a 4 ideas, cada una con su dato. *Cuándo no:* recomendaciones o pasos que se leen en orden de arriba abajo (usa lista_numerada).
- **`afirmacion_evidencia`** (Afirmación y evidencia). validar con entrevistas lo que dijo un entregable anterior (lo que afirmamos frente a lo que dicen). *Cuándo no:* una sola cita (usa cita) o el registro de todas las entrevistas (usa panel_entrevistas).
- **`columnas_requisitos`** (Columnas de requisitos con coste y plazo). capacidades mínimas o recomendables por dimensión, con lo que cuestan y tardan. *Cuándo no:* si no hay coste ni plazo (usa columnas_numeradas o bloque).
- **`tarjetas_escenario`** (Tarjetas de escenario). conservador, base y optimista, o dos o tres alternativas que se comparan con la misma plantilla. *Cuándo no:* si los escenarios son una serie continua (usa abanico de escenarios).
- **`grupo_logos`** (Grupo de logos). los actores de una columna (tier, vía, segmento), al pie de su texto, en rejillas de tres columnas. *Cuándo no:* un universo grande de actores sin columnas (usa muro_logos).
- **`ficha_startup`** (Ficha de startup sin ingresos). fichas de finalistas o candidatos cuando no hay cifras de ingresos que enseñar (una por slide, hermanas). *Cuándo no:* si hay ingresos y una cita (usa ficha_empresa); para listas largas (usa ficha_linea).
- **`categorias_chips`** (Mapa de categorías con chips). una shortlist o un universo de 8 a 30 nombres repartidos en 3 a 9 categorías, con un estado transversal. *Cuándo no:* de 6 a 12 elementos con definición (usa anillo_categorias) o si no hay categorías (usa muro_logos).

### Marcas y apoyo · `ea_elementos/marcas.py`

Micro piezas para celdas, tarjetas y márgenes.

- **`delta`** (Chip de variación). junto a una cifra, para dar el cambio frente al periodo anterior o al objetivo. *Cuándo no:* sin un punto de comparación explícito («vs 2025»).
- **`harvey`** (Bolas de Harvey). grado de cumplimiento cualitativo en tablas comparativas. *Cuándo no:* si hay un valor numérico que se pueda dar (da la cifra).
- **`marca`** (Marcas sí, parcial y no). tablas de características o de cumplimiento de requisitos. *Cuándo no:* si el matiz importa (usa harvey o texto).
- **`semaforo`** (Semáforo de estado). estado de proyectos, hitos o requisitos en una tabla de seguimiento. *Cuándo no:* en entregables de contenido (el semáforo es de gestión, no de hallazgos).
- **`barra_progreso`** (Barra de progreso). avance sobre un total conocido, en tarjetas o tablas. *Cuándo no:* si no hay un máximo real (sin denominador, la barra engaña).
- **`valoracion`** (Puntos de valoración). una nota cualitativa compacta dentro de una ficha o una tabla. *Cuándo no:* si la escala no es ordinal o hay decimales (da la cifra).
- **`etiqueta_evidencia`** (Nivel de evidencia). junto a cada dato de un informe de vigilancia o una ficha. *Cuándo no:* en slides de síntesis para dirección (se explica una vez y se omite).
- **`chip_nota`** (Nota 0 a 3 con confianza). 
- **`pill`** (Píldoras de estado). 
- **`icono_caja`** (Icono en caja). 
- **`llave`** (Llave de agrupación). junto a una lista o un grupo de barras, para decir qué tienen en común. *Cuándo no:* si el grupo ya tiene un contenedor visible.
- **`separador`** (Separador de bloque). dividir una slide densa en dos o tres bloques numerados. *Cuándo no:* como portadilla de sección (esa es una slide propia).
- **`leyenda`** (Leyenda). solo cuando la etiqueta directa no cabe (dos o más series en un mismo gráfico). *Cuándo no:* si se puede rotular cada serie al final de su línea o dentro de su barra.

### Tablas · `ea_elementos/tablas.py`

Comparar en filas y columnas.

- **`tabla_comparativa`** (Tabla comparativa). comparar 2 a 5 opciones en 4 a 10 criterios cualitativos. *Cuándo no:* si los criterios tienen pesos y notas (usa matriz_puntuacion).
- **`tabla_con_barras`** (Tabla con barras). rankings con varias columnas de texto (empresa, país, tipo) y una magnitud. *Cuándo no:* si hay objetivo y referencia por fila (usa tabla_referencia).
- **`tabla_referencia`** (Tabla con barra frente a referencia). lo ya probado por familia, con su mejor resultado y por qué se paró; de 4 a 8 filas. *Cuándo no:* si la tabla tiene más de 5 columnas de texto o si la barra no aporta (tabla sin barra).
- **`tabla_grafica`** (Tabla gráfica). de 5 a 12 categorías con volumen, proporción y un recuento clave (patentes por territorio, cartera). *Cuándo no:* si solo hay una métrica (usa barras_objetivo); las columnas de texto no llevan escala de color.
- **`matriz_puntuacion`** (Matriz de puntuación). de 6 a 14 opciones por 6 a 11 criterios, cuando hay que enseñar el porqué de la prioridad. *Cuándo no:* con menos de 6 opciones (usa mapa_calor o tabla_comparativa), con menos de 4 criterios (usa una tabla) o sin confianza que mostrar (mapa_calor).
- **`scorecard`** (Scorecard). el filtro de evaluación de candidatos de un scouting o programa (EA lo usa en casi todos). *Cuándo no:* para enseñar resultados de la evaluación (usa matriz_puntuacion).
- **`tabla_vigilancia`** (Tabla de vigilancia). la prioridad baja de una recomendación, de 3 a 6 filas, con un disparador claro por fila. *Cuándo no:* para la prioridad alta (necesita su propia slide); si no hay disparador, no es vigilancia, es descarte.
- **`tabla_drivers`** (Tabla de drivers de mercado). resumen de tendencias de un informe de vigilancia o de una slide de mercado. *Cuándo no:* con menos de 4 drivers (usa icono_dato).
- **`panel_entrevistas`** (Panel de entrevistas). documentar la base de una investigación primaria (llamadas a candidatos, expertos, clientes). *Cuándo no:* si las entrevistas no se pueden mostrar ni anonimizadas (da solo el recuento).
- **`matriz_portfolio`** (Mapa de portfolio). qué ofrece cada competidor por vía de administración, aplicación o canal, en fichas hermanas. *Cuándo no:* para comparar varios actores en las mismas vías (usa tabla_comparativa o mapa_calor).

### Síntesis · `ea_elementos/sintesis.py`

Resumir y remitir a otras slides con miniaturas.

- **`tarjetas_miniatura`** (Tarjetas con miniatura). lo esencial al principio o las validaciones al final, 3 tarjetas que anuncian o cierran bloques. *Cuándo no:* con iconos o números decorativos en lugar de miniaturas; con más de 4 tarjetas.
- **`mini_barras_objetivo`** (Miniatura de barras). 
- **`mini_conteo`** (Miniatura de conteo). 
- **`mini_iconos`** (Miniatura de iconos). 
- **`mini_escalera`** (Miniatura de escalera). 
- **`mini_flechas`** (Miniatura de proceso). 
- **`mini_bifurcacion`** (Miniatura de bifurcación). 
