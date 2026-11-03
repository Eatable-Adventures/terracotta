---
tags:
  - recurso
  - design-system
  - presentaciones
aliases:
  - Qué formato para qué mensaje
created: 30-10-2026
actualizado: 03-11-2026
description: >-
  Qué formato de slide usar para cada tipo de mensaje: estructura, pieza de ea_elementos, qué evitar y slide modelo. Antes en la skill /taste; sin datos de cliente.
---

# Formatos de slide: qué formato para qué mensaje

> Parte de Terracotta V2. Para cada tipo de mensaje: cuándo usarlo, su estructura en esquema, la pieza con la que se construye, qué evitar y, si la hay, su slide modelo (`Modelo: tipo` se ve con `python3 referencias.py tipo --png <carpeta>`). Se usa al montar y al revisar. Sin casos concretos: las slides modelo y sus decks están en [[Referencias de Terracotta]], que es solo interna.

**Dónde están las piezas.** En esta carpeta:
- `ea_elementos/` (paquete, importado como `X`): los 158 elementos en 14 familias, un módulo por familia. Ejemplo de cada uno en `Galería de elementos.html`.
- `Taxonomía de elementos.md` (generada desde `ea_elementos/taxonomia.py`): qué elementos responden a cada intención, con escala y alternativas. **Antes de proponer una pieza, mira todas las candidatas de la intención** (`X.buscar("brecha")`), no solo la que se cita aquí.
- `Reglas de uso de elementos.md`: rejillas, escala, jerarquía, color e ilustración isométrica todas las reglas de montar y revisar.
- `ea_elementos/embudo_canonico.py` (desde Terracotta V2, antes `pptx/funnel.py`): el embudo canónico, que `X.embudo` envuelve.

El catálogo crece, así que antes de citar una pieza **comprueba que existe con ese nombre** (`X.FICHAS` o la taxonomía) y mira su docstring. Si el formato que encaja no está aquí, busca en la taxonomía y en la galería antes de inventar uno. «Sin pieza» significa que la composición está validada pero se monta a mano con los elementos y `X.fila()` y `X.columna()`.

Para el cuerpo de cualquier slide, `X.cuerpo_slide(subtítulo, visual, banda=...)`, con el visual a la altura que da `X.alto_cuerpo(...)`: el cuerpo llena el espacio libre (M11).

---

## Proceso y estado

**Embudo de un proceso de selección.** Cuántos entraron y cuántos quedan en cada fase.
- Estructura: discos apilados con rampa de rojos, escalones no proporcionales, etiquetas alineadas con la cifra y el nombre de la fase.
- Pieza: `X.embudo` (envuelve `embudo_canonico.py`).
- Evitar: más de un embudo por bloque, nombres de candidatos, rondas internas, un embudo hecho como tabla de tres filas.
- Modelo: `embudo`.

**Universo completo de candidatos o actores.** Que el cliente vea todo lo que se ha mirado, no solo los finalistas.
- Estructura: slide tipo ecosistema a página completa, logos a color del mismo alto en una rejilla agrupada por fase alcanzada o estado (no por categoría técnica); cada grupo con su rótulo y su recuento; el estado (activo, cerrado, en validación) con píldora o símbolo además del grupo. Cada actor aparece una sola vez.
- Pieza: `X.ecosistema_logos` (grupos con rótulo, recuento y estado; logos de `assets/logos/` del proyecto). Para un solo grupo, `X.muro_logos`. Si no van a llegar los logos, `X.categorias_chips` con `rojo=False`: el muro sin logos sirve solo como borrador.
- Evitar: tres bloques separados que fragmentan el universo, recuadro de «implicación» que roba espacio, logos en gris o pixelados.

**Dónde estamos en el calendario.** Fases hechas, en curso y pendientes con la fecha de hoy.
- Estructura: Gantt con una fila por fase, barras de estado, línea vertical de «hoy», hitos como rombos.
- Pieza: `X.gantt`; para algo más ligero, `linea_tiempo` o `X.carriles`.
- Evitar: leyenda de colores larga; la línea de «hoy» con una fecha que ya no es hoy.
- Modelo: `cronograma`.

**Proceso de N pasos con entregables.** Qué se hace en cada paso, qué sale y quién lo hace.
- Estructura: flechas encadenadas en rampa de rojos, una llave que agrupa pasos en fases y, por paso, «qué se resuelve, qué sale, quién».
- Pieza: `X.proceso_flechas` o `X.fases_gates`, que crecen con el cuerpo y llenan la slide; `X.chevrones` si es solo la secuencia, que es una pieza baja y necesita algo debajo.
- Evitar: cuatro tarjetas de texto iguales sin dirección; dictar el protocolo técnico del cliente (F3).
- Modelo: `proceso`.

**Decisión en el tiempo o trámite con bifurcación.**
- Pieza: `X.arbol_tramite` (pregunta sí o no con dos vías); `X.tarjetas_salida` para escenarios.

## Comparar y decidir

**Comparativa de candidatos con puntuación.** Quién gana en qué y por qué ninguno es perfecto.
- Estructura: matriz criterios × candidatos con los logos en la cabecera de columna, la puntuación en celdas con la escala de B9 (tonos neutros o claros y rojo solo para el fallo), las alertas (criterio no negociable incumplido) marcadas en la propia celda con un icono pequeño, total abajo; una lectura breve que diga qué candidato sirve para qué.
- Pieza: `X.mapa_calor` o `X.tabla_comparativa` con pocos candidatos; `X.matriz_puntuacion` con 6 a 14 opciones; `X.chip_nota` para la celda.
- Evitar: semáforo verde y rojo en las celdas (B9), columna o leyenda aparte para las banderas (B8), pie de tabla.
- Modelo: `puntuacion`.

**Criterios de evaluación (scorecard).** Qué se pide y cuánto pesa cada cosa.
- Pieza: `X.scorecard` (eliminatorios numerados y comparativos con su peso en barra).
- Modelo: `puntuacion`.

**Ficha de perfil de candidato (top N).** Entender a cada finalista con el mismo formato.
- Estructura: cabecera con teselas grises redondeadas de datos clave (tipo, ubicación, escala, certificación, puntuación); cuerpo con capacidades frente a cada etapa del proceso del cliente, con ventajas y limitaciones integradas en esas capacidades (no en dos listas genéricas); abajo, lo que falta por demostrar. Las fichas hermanas comparten plantilla exacta y arrancan a la misma altura.
- Pieza: si las fichas son de competidores con cifras, ficha en cuadrantes (M10 de las reglas): `X.bloque`, `X.matriz_portfolio`, `X.combo_financiero` y `X.score_dimensiones`; si no, `X.fila_parametros`, `X.etiquetas_icono` y `X.grupo_fichas` como bloques.
- Evitar: títulos de bloque redundantes, datos repetidos (la ubicación arriba y en la tabla), letra por debajo de 12 px en el cuerpo, demasiados colores, lo de due diligence mezclado con lo que ya se sabe.
- Modelo: `ficha`.

**Cobertura de un proceso por candidatos.** Quién cubre qué etapa (y por qué ninguno lo cubre todo).
- Estructura: etapas en columnas, candidatos en filas, celdas llenas, parciales o vacías, y franjas que agrupan etapas (piloto, industrial).
- Pieza: `mapa_calor` o `X.carriles`.

**Priorización.** Qué se hace primero, después y en vigilancia.
- Pieza: `X.escalera_prioridad`; lo que no se prioriza, con su disparador, en `X.tabla_vigilancia`.
- Modelo: `recomendacion`.

**Madurez tecnológica.** Dónde está cada tecnología en una escala ordinal (TRL).
- Pieza: `X.mapa_madurez`.
- Modelo: `cartera`.

**Costo con rangos amplios.** Cuánto cuesta cada alternativa frente a la referencia.
- Estructura: escala logarítmica, un valor central por alternativa (media geométrica) y el rango tenue detrás.
- Pieza: `X.escala_log`.

**Volumen y reparto de una base documental.**
- Pieza: `X.tabla_grafica` (barra absoluta, barra 100 % partida y dato) con una ficha lateral alineada con la última fila.

## Explicar un mecanismo

**Cadena de valor o modelo de negocio.** Cada pieza responde a una pregunta distinta. Por defecto, `X.cadena_isometrica` para abrir y `X.cadena_capas` para analizar (30-10-2026). Si el mensaje no decide, se enseñan opciones con los mismos datos: `laboratorio.opciones_cadena()` (S7).

| Pieza | Para | Gana | Pierde |
|---|---|---|---|
| `X.cadena_isometrica` | Presentar el sector de un vistazo | Peso visual: se entiende sin leer y abre bien un informe | Solo admite un dato por eslabón; no analiza |
| `X.cadena_capas` | Decir dónde está el valor y dónde entrar | Análisis completo por eslabón: actores, margen, tendencia y oportunidad | Densa; necesita datos de todas las filas |
| `X.cadena_margen` | Enseñar quién captura el margen y dónde está el cliente | La cifra manda y la posición del cliente se ve al momento | No dice quién opera en cada eslabón ni hacia dónde va |
| `X.circuito_cadena` | Explicar por qué un actor gana con un modelo circular o de dependencia | Enseña el mecanismo: lo que sale y lo que vuelve | Necesita un actor que se engancha; no sirve para describir un sector |

- Estructura de `circuito_cadena`: camino con estaciones e iconos, conectado a la cadena del cliente, con las flechas de lo que sale y lo que entra.
- Para la recomendación de hoy al destino, `X.trayecto`; para el modelo de negocio de un actor, `X.lienzo_negocio`.
- Evitar: una cadena suelta que no se conecta con la del cliente (decora, no explica).
- Modelo: `cadena`.

**Categorías con un estado transversal.** Opciones agrupadas por mecanismo, donde algunas cumplen una condición.
- Estructura: anillo por categorías, un color por categoría, el estado marcado aparte (símbolo o píldora).
- Pieza: `X.anillo_categorias`.

**Dos opciones que salen de un núcleo común.**
- Pieza: `X.nucleo_dos_lados`.

**De lo ya probado a lo nuevo.**
- Estructura: una columna por familia, lo probado → mismo origen, otro producto, con su cifra, quién lo hace y su reto; tarjetas de «quién» y de «reto» del mismo alto en todas las columnas.
- Pieza: `X.columnas_evolucion`.

**Slides hermanas de opción u oportunidad (territorio, línea, candidato).**
- Estructura: lo probado → la hipótesis sin probar arriba, los criterios fijos en filas con su nota y un panel gris con ejemplos.
- Pieza: `X.ficha_hipotesis`.
- Modelo: `ficha`.

**Precedentes o histórico con estado.**
- Pieza: `X.lista_precedentes` (el favorable en verde de validación).

## Resumir

**Resumen ejecutivo o cierre de sección que remite a otras slides.**
- Estructura: tarjetas con una miniatura del visual de la slide que resumen arriba y la conclusión debajo.
- Pieza: `X.tarjetas_miniatura` con `X.mini_*`.
- Modelo: `resumen`.

**KPI o métricas de éxito.** Pocos números que deciden.
- Estructura: la cifra como protagonista, el rótulo debajo con mayúscula inicial y de dónde sale; o barras frente a una línea de objetivo. Nunca una lista de texto.
- Pieza: `X.contadores`, `X.tarjeta_cifra`, `X.panel_kpi`, `X.barras_objetivo`, `X.regleta_objetivo`; `indicador` y `X.cifra_delta`.
- Evitar: un gráfico ilegible por querer meterlo todo (prima que se lea).

- Modelo: `cifra`.

**Solo texto.** Cuando el mensaje no admite gráfica.
- Estructura: dos o tres bloques con cabecera que llegan hasta el pie, con una idea por bloque.
- Pieza: `X.bloque`, `X.columna_contexto`.
- Modelo: `texto`.
- Evitar: más de tres bloques sin un visual (D1, M9).

## Situar y contrastar

**Mapa con una brecha geográfica.** Dónde está cada cosa y qué falta en cada sitio.
- Estructura: mapa en el centro, lectura a un lado y actores al otro.
- Pieza: `X.mapa_coropletico`, `X.muro_logos`.
- Modelo: `mapa`.

**Tabla comparativa con conclusión.** Pocas opciones frente a pocos criterios.
- Estructura: pocas columnas, filas con aire y conclusión al pie.
- Pieza: `X.tabla_comparativa`; con una barra por fila, `X.tabla_referencia`.
- Modelo: `comparacion`.

**Escenarios.** Tres futuros con la misma plantilla.
- Estructura: tres tarjetas iguales, el escenario de referencia destacado y una gráfica abajo.
- Pieza: `X.tarjetas_escenario`.
- Modelo: `escenarios`.

**Voz de experto.** La cita sostiene la tesis.
- Estructura: citas por dimensión, con su implicación al lado.
- Pieza: `X.cita`.
- Modelo: `citas`.
- Evitar: citas sueltas sin lo que significan para el cliente.
