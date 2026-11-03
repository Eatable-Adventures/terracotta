"""taxonomia: el menú completo de ea_elementos, en dos ejes.

- Familia (la forma visual): un módulo por familia. Sirve para encontrar el código.
- Intención (lo que la slide tiene que decir): sirve para elegir. Un elemento responde a una o varias.

Regla de uso para la IA (y para cualquiera): se elige por intención, no por costumbre. Antes de decidir,
buscar(intencion) da todas las candidatas; se leen todas y se descarta con motivo. «Taxonomía de elementos.md»
es la versión legible de este archivo y la genera build_galeria_elementos.py, así que nunca se edita a mano.

Cada ficha: titulo, intenciones (la primera es la principal), datos (forma de lo que entra), escala
(S = pieza para una tarjeta o una celda, hasta ~360 px; M = media slide, 400 a 640 px; L = ancho de slide)
y alternativas (otros elementos que responden a lo mismo con otro matiz).
"""

import re

INTENCIONES = [
    ("cifra", "Una cifra que manda", "De 1 a 4 números protagonistas: KPI, tamaño, resultado"),
    ("comparar", "¿Cuánto, entre categorías?", "Magnitudes de varias categorías en la misma unidad"),
    ("ordenar", "¿Quién va primero?", "Ranking por valor, concentración, los pocos que pesan"),
    ("tendencia", "¿Cómo evoluciona?", "Serie temporal, previsión, adopción"),
    ("explicar_cambio", "¿Por qué cambia o de qué depende?", "Puente entre dos valores, drivers, sensibilidad"),
    ("parte_todo", "¿De qué se compone?", "Reparto de un total en partes"),
    ("brecha", "¿Cuánto falta?", "Frente a un objetivo, una referencia o un benchmark"),
    ("evaluar", "¿Qué opción es mejor?", "Alternativas frente a varios criterios, puntuación"),
    ("posicionar", "¿Dónde está cada uno?", "En dos ejes, en una escala de madurez o en cuadrantes"),
    ("distribucion", "¿Cómo se reparten los valores?", "Dispersión, rangos, incertidumbre de una población"),
    ("relacion", "¿Qué se conecta con qué?", "Flujos, redes, solapes, cruce de condiciones"),
    ("geografia", "¿Dónde ocurre?", "Países y regiones"),
    ("estructura", "¿Cómo se organiza?", "Jerarquías, marcos estratégicos, taxonomías, alcance"),
    ("cadena", "¿Cómo fluye el valor?", "Eslabones de la cadena, actores, modelo de negocio"),
    ("proceso", "¿En qué orden se hace?", "Pasos, fases, responsables"),
    ("calendario", "¿Cuándo?", "Cronograma, hitos, hoja de ruta, historial"),
    ("decidir", "¿Qué hacemos?", "Prioridades, escenarios, criterios y salidas de una decisión"),
    ("perfil", "¿Quién es?", "Empresa, persona, actor u opción en ficha"),
    ("evidencia", "¿De dónde sale y cuánto fiarse?", "Fuentes, confianza, citas, entrevistas"),
    ("estado", "¿Cómo va?", "Avance, cumplimiento, semáforo"),
    ("ilustrar", "Dar contexto visual", "Escenas isométricas, imágenes, antes y después"),
    ("resumir", "Sintetizar", "Resumen que remite a otras slides, mensajes clave"),
    ("apoyo", "Pieza auxiliar", "Leyendas, separadores, llaves, píldoras: nunca protagonistas"),
]
_CLAVES = {k for k, _, _ in INTENCIONES}

FAMILIAS = [  # (módulo, familia, lema, elementos)
    ("magnitud", "Magnitud", "Cuánto: comparar cantidades",
     "columnas barras_ranking barras_agrupadas barras_apiladas piruletas pictograma pareto comparador_unidad barras_variacion embudo ranking_logos"),
    ("evolucion", "Evolución", "Cómo cambia en el tiempo",
     "linea area_apilada pendiente cascada sparkline curva_s abanico bump pequenos_multiplos combo_financiero"),
    ("composicion", "Composición", "De qué está hecho un total",
     "donut waffle treemap marimekko sankey sunburst barra_desglose anillo_categorias"),
    ("comparacion", "Comparación", "Frente a un objetivo, una referencia o entre sí",
     "radar mancuerna bala tornado rangos indicador barra_dividida dimensionamiento deslizadores benchmark_rango "
     "criterios_puntos barras_objetivo barras_duelo regleta_objetivo escala_log score_dimensiones"),
    ("distribucion", "Relación y distribución", "Cómo se reparten, se relacionan o se sitúan",
     "dispersion mapa_calor histograma cajas red_nodos mapa_coropletico mapa_burbujas mapa_flujos mapa_madurez mapa_actores"),
    ("marcos", "Marcos y matrices", "Cómo se organiza una idea en un esquema",
     "matriz_2x2 venn circulos_concentricos radial piramide capas balanza lienzo_negocio mapa_alcance dafo cinco_fuerzas "
     "pilares nucleo_dos_lados escalera_prioridad columnas_evolucion convergencia"),
    ("arboles", "Árboles y descomposición", "De qué depende algo, rama a rama",
     "arbol espina_pescado organigrama formula arbol_drivers arbol_tramite abanico_foco arbol_opciones"),
    ("cadena", "Cadena de valor", "Cómo fluye el valor entre eslabones y actores, con escenas isométricas",
     "cadena_capas circuito_cadena cadena_isometrica escena_iso catalogo_escenas cadena_margen trayecto"),
    ("secuencia", "Secuencia y tiempo", "En qué orden y cuándo",
     "chevrones linea_tiempo ciclo carriles escalones calendario_calor linea_tiempo_vertical proceso_carriles proceso_flechas "
     "gantt lista_precedentes fases_gates"),
    ("cifras", "Cifras y KPI", "Una o pocas cifras que mandan",
     "cifra_delta icono_dato contadores tarjeta_cifra tarjeta_kpi panel_kpi fila_parametros"),
    ("fichas", "Fichas y texto", "Quién es, qué dice y qué sale, en tarjetas y bloques de texto",
     "ficha_empresa ficha_linea tarjeta_actor persona muro_logos ecosistema_logos grupo_fichas ficha_hipotesis tarjetas_salida cita "
     "lista_numerada aviso etiquetas_icono antes_despues_imagen columna_contexto bloque columnas_numeradas afirmacion_evidencia columnas_requisitos tarjetas_escenario grupo_logos ficha_startup categorias_chips"),
    ("marcas", "Marcas y apoyo", "Micro piezas para celdas, tarjetas y márgenes",
     "delta harvey marca semaforo barra_progreso valoracion etiqueta_evidencia chip_nota pill icono_caja llave separador leyenda"),
    ("tablas", "Tablas", "Comparar en filas y columnas",
     "tabla_comparativa tabla_con_barras tabla_referencia tabla_grafica matriz_puntuacion scorecard tabla_vigilancia "
     "tabla_drivers panel_entrevistas matriz_portfolio"),
    ("sintesis", "Síntesis", "Resumir y remitir a otras slides con miniaturas",
     "tarjetas_miniatura mini_barras_objetivo mini_conteo mini_iconos mini_escalera mini_flechas mini_bifurcacion"),
]
FAMILIAS = [(m, f, l, e.split()) for m, f, l, e in FAMILIAS]


def F(titulo, intenciones, datos, escala, alternativas=""):
    return dict(titulo=titulo, intenciones=intenciones.split(), datos=datos, escala=escala, alternativas=alternativas.split())


FICHAS = {
    # ---------------------------------------------------------------- magnitud
    "columnas": F("Columnas", "comparar tendencia", "1 serie de 3 a 10 categorías o periodos; previsión y CAGR opcionales", "M",
                  "barras_ranking piruletas linea pictograma"),
    "barras_ranking": F("Ranking en barras", "ordenar comparar", "1 serie de 5 a 15 elementos con rótulos largos", "M",
                        "piruletas tabla_con_barras pareto columnas ranking_logos"),
    "barras_agrupadas": F("Columnas agrupadas", "comparar", "2 o 3 series en 3 a 6 categorías", "M",
                          "mancuerna pendiente pequenos_multiplos mapa_calor"),
    "barras_apiladas": F("Barras apiladas al 100 %", "parte_todo comparar", "3 a 6 partes en 2 a 8 filas", "M",
                         "marimekko donut barra_desglose barra_dividida"),
    "piruletas": F("Piruletas (lollipop)", "ordenar brecha", "1 serie de valores parecidos, con referencia opcional", "M",
                   "barras_ranking mancuerna barras_objetivo"),
    "pictograma": F("Pictograma", "cifra parte_todo", "Un porcentaje como x de 10, 20 o 100 figuras", "S",
                    "waffle donut tarjeta_cifra"),
    "pareto": F("Pareto", "ordenar decidir", "1 serie de causas o elementos con su acumulado", "M",
                "barras_ranking treemap"),
    "comparador_unidad": F("Comparador por unidad", "comparar brecha", "Coste o precio por unidad de cada opción frente a una referencia", "M",
                           "escala_log barras_variacion tabla_con_barras"),
    "barras_variacion": F("Barras de variación", "explicar_cambio comparar", "Variaciones positivas y negativas por elemento", "M",
                          "pendiente cascada tornado"),
    "embudo": F("Embudo de discos", "proceso cifra", "3 a 6 etapas de un cribado con su recuento", "M",
                "dimensionamiento circulos_concentricos escalones"),
    # ---------------------------------------------------------------- evolución
    "linea": F("Líneas con serie destacada", "tendencia", "1 a 4 series en 5 o más periodos, con anotaciones y periodos sombreados", "M",
               "columnas area_apilada pequenos_multiplos abanico"),
    "area_apilada": F("Áreas apiladas", "tendencia parte_todo", "2 a 4 componentes de un total en el tiempo", "M",
                      "linea barras_apiladas"),
    "pendiente": F("Pendiente (slope)", "explicar_cambio ordenar", "3 a 8 elementos en dos momentos", "M",
                   "mancuerna bump barras_variacion"),
    "cascada": F("Cascada (waterfall)", "explicar_cambio", "Valor inicial, 3 a 8 variaciones y valor final; fila de evidencia opcional", "M",
                 "arbol_drivers barras_variacion formula tornado"),
    "sparkline": F("Minilínea (sparkline)", "tendencia apoyo", "Una serie corta, sin ejes", "S",
                   "cifra_delta pequenos_multiplos"),
    "curva_s": F("Curva en S de adopción", "tendencia posicionar", "Opciones situadas en las fases de adopción de una tecnología", "M",
                 "mapa_madurez linea_tiempo escalones"),
    "abanico": F("Abanico de escenarios", "tendencia distribucion", "Serie histórica más escenario bajo, central y alto", "M",
                 "linea rangos tarjetas_escenario"),
    "bump": F("Ranking en el tiempo (bump)", "ordenar tendencia", "Posiciones de 4 a 8 actores en 3 o más periodos", "M",
              "pendiente linea"),
    "pequenos_multiplos": F("Pequeños múltiplos", "tendencia comparar", "4 a 12 series cortas con escala común", "L",
                            "linea barras_agrupadas mapa_calor"),
    # ---------------------------------------------------------------- composición
    "donut": F("Anillo (donut)", "parte_todo cifra", "2 a 5 partes de un total, con cifra central", "S",
               "waffle barras_apiladas treemap pictograma"),
    "waffle": F("Gofre (waffle)", "parte_todo cifra", "Un porcentaje sobre 100 casillas", "S",
                "pictograma donut"),
    "treemap": F("Mapa de árbol (treemap)", "parte_todo ordenar", "5 a 15 partes de un total", "M",
                 "sunburst barras_ranking marimekko"),
    "marimekko": F("Marimekko", "parte_todo comparar", "Tamaño por columna y cuota por segmento", "M",
                   "barras_apiladas treemap"),
    "sankey": F("Flujos (Sankey)", "relacion parte_todo cadena", "Flujos de volumen entre dos clasificaciones", "M",
                "marimekko red_nodos cadena_capas"),
    "sunburst": F("Sunburst", "parte_todo estructura", "Un total con dos niveles (familia y subcategoría)", "M",
                  "treemap anillo_categorias"),
    "barra_desglose": F("Barra con desglose", "parte_todo explicar_cambio", "Tramos de un total con uno abierto en partidas", "M",
                        "barras_apiladas cascada treemap"),
    "anillo_categorias": F("Anillo de categorías", "estructura parte_todo", "Elementos agrupados en 2 a 5 categorías, con un estado transversal", "L",
                           "sunburst mapa_alcance treemap"),
    # ---------------------------------------------------------------- comparación
    "radar": F("Araña (radar)", "evaluar perfil", "1 o 2 perfiles en 5 a 8 criterios de la misma escala", "M",
               "criterios_puntos tabla_comparativa deslizadores score_dimensiones"),
    "mancuerna": F("Mancuerna (dumbbell)", "brecha comparar", "Dos valores por fila (actual y objetivo, nosotros y líder)", "M",
                   "pendiente barras_agrupadas piruletas"),
    "bala": F("Avance hacia objetivo", "brecha estado", "3 a 6 KPI con valor, objetivo y máximo", "M",
              "barras_objetivo indicador barra_progreso"),
    "tornado": F("Tornado (sensibilidad)", "explicar_cambio", "Resultado bajo y alto por variable de un modelo", "M",
                 "barras_variacion arbol_drivers rangos"),
    "rangos": F("Rangos (football field)", "distribucion comparar", "Mínimo y máximo por método o fuente sobre un eje común", "M",
                "escala_log cajas benchmark_rango dimensionamiento"),
    "indicador": F("Indicador (gauge)", "cifra estado", "Un KPI de avance con objetivo", "S",
                   "bala barra_progreso tarjeta_cifra"),
    "barra_dividida": F("Barra dividida (Likert)", "distribucion evidencia", "Respuestas en una escala de acuerdo por afirmación", "M",
                        "barras_apiladas"),
    "dimensionamiento": F("Dimensionamiento de arriba abajo", "cifra explicar_cambio", "Del mercado total al alcanzable en 3 a 5 pasos", "M",
                          "circulos_concentricos embudo formula"),
    "deslizadores": F("Deslizadores de valoración", "evaluar evidencia", "Valoraciones cualitativas de 0 a 1 con su razón", "M",
                      "radar harvey valoracion score_dimensiones"),
    "benchmark_rango": F("Benchmark en rango", "brecha posicionar", "Nuestro valor entre el peor y el mejor comparable, por KPI", "M",
                         "rangos mancuerna cajas"),
    "criterios_puntos": F("Criterios con puntos por actor", "evaluar", "Criterios por importancia y la nota de cada actor", "M",
                          "radar matriz_puntuacion tabla_comparativa"),
    "barras_objetivo": F("Barras frente a objetivo", "brecha comparar", "3 a 8 opciones con su valor y una línea de objetivo", "M",
                         "bala piruletas mancuerna"),
    "barras_duelo": F("Duelo de dos barras", "brecha", "Referencia y objetivo de un mismo KPI", "S",
                      "regleta_objetivo mancuerna indicador"),
    "regleta_objetivo": F("Regleta con zona objetivo", "brecha", "Un valor o rango negociable sobre una escala", "S",
                          "barras_duelo benchmark_rango"),
    "escala_log": F("Escala logarítmica", "comparar distribucion", "Alternativas con rangos que abarcan órdenes de magnitud", "L",
                    "rangos comparador_unidad"),
    # ---------------------------------------------------------------- relación y distribución
    "dispersion": F("Dispersión y burbujas", "posicionar relacion", "5 a 20 elementos en dos variables numéricas, tamaño opcional", "M",
                    "matriz_2x2 mapa_madurez"),
    "mapa_calor": F("Mapa de calor", "evaluar distribucion", "Matriz de valores de 4 × 4 a 10 × 12", "M",
                    "matriz_puntuacion tabla_comparativa pequenos_multiplos"),
    "histograma": F("Histograma", "distribucion", "Recuentos por tramo con una marca", "M",
                    "cajas rangos"),
    "cajas": F("Diagrama de cajas", "distribucion evidencia", "Observaciones por grupo (ensayos, paneles)", "M",
               "histograma rangos benchmark_rango"),
    "red_nodos": F("Red de nodos", "relacion cadena", "Actores y sus relaciones (ecosistema)", "M",
                   "radial sankey circuito_cadena"),
    "mapa_burbujas": F("Mapa de burbujas", "geografia comparar", "Un valor por lugar, con el área proporcional", "L", "mapa_coropletico mapa_actores barras_ranking"),
    "mapa_flujos": F("Mapa de flujos", "geografia relacion", "Un origen y de 2 a 12 destinos con su peso", "L", "sankey mapa_actores red_nodos"),
    "mapa_coropletico": F("Mapa coroplético", "geografia", "Un valor por país en una región", "M",
                          "barras_ranking mapa_calor mapa_actores"),
    "mapa_madurez": F("Mapa de madurez (TRL)", "posicionar distribucion", "Elementos por tramo de madurez, carril de evidencia y categoría", "M",
                      "curva_s dispersion escalones"),
    # ---------------------------------------------------------------- marcos y matrices
    "matriz_2x2": F("Matriz 2 × 2", "posicionar decidir", "Elementos en dos ejes cualitativos con cuadrantes", "M",
                    "dispersion escalera_prioridad"),
    "venn": F("Venn", "relacion estructura", "2 o 3 condiciones y su intersección", "M",
              "mapa_alcance circulos_concentricos"),
    "circulos_concentricos": F("Círculos concéntricos (TAM, SAM, SOM)", "cifra estructura", "2 a 4 niveles anidados con su cifra", "M",
                               "dimensionamiento embudo"),
    "radial": F("Radial (hub and spoke)", "estructura relacion", "Un centro y 4 a 8 componentes o relaciones", "M",
                "red_nodos capas lienzo_negocio convergencia"),
    "piramide": F("Pirámide", "estructura", "3 a 5 niveles jerárquicos", "M",
                  "capas escalones"),
    "capas": F("Capas (stack)", "estructura", "3 a 6 capas que se apoyan unas en otras", "M",
               "piramide pilares"),
    "balanza": F("Balanza", "decidir evaluar", "Argumentos a favor y en contra, o dos alternativas", "M",
                 "dafo tabla_comparativa nucleo_dos_lados"),
    "lienzo_negocio": F("Lienzo de modelo de negocio", "cadena perfil", "Las nueve cajas del business model canvas", "L",
                        "circuito_cadena ficha_empresa"),
    "mapa_alcance": F("Mapa de alcance", "estructura decidir", "Opciones por dimensión que entran, entran en parte o no", "L",
                      "anillo_categorias venn arbol"),
    "dafo": F("DAFO", "evaluar estructura", "Fortalezas, debilidades, oportunidades y amenazas", "M",
              "cinco_fuerzas balanza"),
    "cinco_fuerzas": F("Cinco fuerzas", "evaluar estructura", "Intensidad y explicación de las cinco fuerzas de un sector", "M",
                       "dafo tabla_drivers"),
    "pilares": F("Casa estratégica (pilares)", "estructura resumir", "Ambición, 3 a 5 pilares y bases", "L",
                 "capas lista_numerada"),
    "nucleo_dos_lados": F("Núcleo con dos lados", "estructura explicar_cambio", "Dos opciones que salen de un núcleo común, con efectos por fila", "L",
                          "balanza columnas_evolucion"),
    "escalera_prioridad": F("Escalera de prioridad", "decidir ordenar", "Hasta 3 niveles de prioridad con 5 focos cada uno", "L",
                            "matriz_2x2 pareto tabla_vigilancia"),
    "columnas_evolucion": F("De lo probado a lo nuevo", "explicar_cambio perfil", "2 a 4 columnas con lo probado, lo nuevo, quién y el reto", "L",
                            "ficha_hipotesis nucleo_dos_lados antes_despues_imagen"),
    # ---------------------------------------------------------------- árboles
    "arbol": F("Árbol de problemas", "estructura", "Una pregunta en ramas y hojas MECE", "M",
               "arbol_drivers espina_pescado mapa_alcance abanico_foco"),
    "espina_pescado": F("Espina de pescado (Ishikawa)", "explicar_cambio estructura", "Causas de un problema por categoría", "L",
                        "arbol arbol_drivers"),
    "organigrama": F("Organigrama", "estructura perfil", "Personas o unidades en 2 o 3 niveles", "L",
                     "arbol persona"),
    "formula": F("Fórmula de cálculo", "explicar_cambio evidencia", "Factores con cifra y fuente unidos por operadores", "L",
                 "arbol_drivers dimensionamiento cascada"),
    "arbol_drivers": F("Árbol de drivers", "explicar_cambio", "Un KPI descompuesto en factores con valor y variación", "L",
                       "formula cascada tornado"),
    "arbol_tramite": F("Árbol de trámite", "decidir proceso", "Una pregunta sí o no con una vía directa y un recorrido", "L",
                       "proceso_carriles chevrones arbol_opciones"),
    # ---------------------------------------------------------------- cadena de valor
    "cadena_capas": F("Cadena de valor en capas", "cadena evaluar", "4 a 7 eslabones con filas de análisis (actores, margen, tendencia)", "L",
                      "cadena_isometrica circuito_cadena sankey cadena_margen"),
    "circuito_cadena": F("Circuito de la cadena", "cadena relacion", "Eslabones con un actor que se engancha por dos flechas", "L",
                         "cadena_capas lienzo_negocio red_nodos"),
    "cadena_isometrica": F("Cadena de valor isométrica", "cadena ilustrar", "4 a 7 fases con escena, texto y dato", "L",
                           "cadena_capas chevrones"),
    "escena_iso": F("Escena isométrica suelta", "ilustrar", "Una escena del catálogo ESCENAS o una propia", "S",
                    "icono_caja antes_despues_imagen"),
    "catalogo_escenas": F("Catálogo de escenas", "ilustrar apoyo", "Todas las escenas registradas, con su clave", "L",
                          "escena_iso"),
    # ---------------------------------------------------------------- secuencia y tiempo
    "chevrones": F("Chevrones de proceso", "proceso", "3 a 6 etapas lineales, con la actual marcada", "L",
                   "proceso_flechas escalones linea_tiempo fases_gates"),
    "linea_tiempo": F("Línea de tiempo", "calendario", "Hitos con fecha, pasados, hoy y futuros", "L",
                      "linea_tiempo_vertical gantt lista_precedentes"),
    "ciclo": F("Ciclo", "proceso", "3 a 6 pasos que se repiten", "M",
               "chevrones radial"),
    "carriles": F("Hoja de ruta por carriles", "calendario proceso", "Iniciativas por carril y periodo", "L",
                  "gantt proceso_carriles"),
    "escalones": F("Escalones", "proceso estructura", "Etapas de madurez o ambición que suben", "M",
                   "piramide chevrones curva_s"),
    "calendario_calor": F("Calendario de calor", "calendario distribucion", "Actividad por día durante meses", "L",
                          "mapa_calor linea"),
    "linea_tiempo_vertical": F("Línea de tiempo vertical", "calendario perfil", "Hitos con texto largo", "M",
                               "linea_tiempo lista_precedentes"),
    "proceso_carriles": F("Proceso por carriles", "proceso", "Pasos repartidos por responsable con traspasos", "L",
                          "proceso_flechas carriles arbol_tramite"),
    "proceso_flechas": F("Proceso en flechas con entregables", "proceso", "3 a 5 pasos con qué se resuelve, qué sale y quién", "L",
                         "chevrones proceso_carriles"),
    "gantt": F("Gantt", "calendario", "Fases con barras por fechas, hoy y decisión", "L",
               "carriles linea_tiempo fases_gates"),
    "lista_precedentes": F("Lista de precedentes", "evidencia calendario", "4 a 8 decisiones pasadas con su estado", "S",
                           "linea_tiempo_vertical tabla_comparativa"),
    # ---------------------------------------------------------------- cifras y KPI
    "cifra_delta": F("KPI con variación", "cifra estado", "Cifra, variación y minilínea", "S",
                     "tarjeta_cifra indicador contadores"),
    "icono_dato": F("Dato con icono", "cifra", "2 a 4 cifras de contexto con icono", "S",
                    "contadores fila_parametros"),
    "contadores": F("Contadores", "cifra evidencia", "2 a 4 cifras grandes con de dónde salen", "S",
                    "icono_dato tarjeta_cifra columna_contexto"),
    "tarjeta_cifra": F("Tarjeta con cifra", "cifra", "Una cifra que hace de etiqueta del mensaje, con texto", "S",
                       "cifra_delta contadores"),
    "tarjeta_kpi": F("Tarjeta de KPI de éxito", "cifra brecha", "KPI con objetivo, referencia, visual y validación", "S",
                     "bala cifra_delta"),
    "panel_kpi": F("Panel de KPI", "cifra decidir", "KPI que deciden arriba y condiciones abajo", "L",
                   "bala tarjeta_kpi"),
    "fila_parametros": F("Fila de parámetros técnicos", "cifra estructura", "3 a 6 condiciones técnicas de partida", "L",
                         "icono_dato etiquetas_icono"),
    # ---------------------------------------------------------------- fichas y texto
    "ficha_empresa": F("Ficha de empresa de un vistazo", "perfil", "Datos clave, ingresos, diferenciadores, cita y madurez", "L",
                       "ficha_linea tarjeta_actor lienzo_negocio combo_financiero"),
    "ficha_startup": F("Ficha de startup sin ingresos", "perfil", "Datos clave y cuatro bloques de texto", "L",
                       "ficha_empresa ficha_linea tarjeta_actor"),
    "categorias_chips": F("Mapa de categorías con chips", "estructura perfil", "8 a 30 nombres en 3 a 9 categorías, con un estado transversal", "L",
                          "anillo_categorias muro_logos grupo_logos"),
    "ficha_linea": F("Ficha de una línea por empresa", "perfil ordenar", "10 a 20 empresas con madurez y frase", "L",
                     "tabla_con_barras muro_logos"),
    "tarjeta_actor": F("Tarjeta de empresa", "perfil", "Nombre, país y tipo, logo y una frase", "S",
                       "ficha_linea persona"),
    "persona": F("Persona con monograma", "perfil", "Nombre y cargo", "S",
                 "organigrama tarjeta_actor"),
    "ecosistema_logos": F("Ecosistema de logos por grupos", "perfil estructura", "De 10 a 70 actores (partners, aliados, candidatos) en 2 a 6 grupos, con logo o nombre", "L",
                          "muro_logos categorias_chips mapa_actores ficha_linea"),
    "muro_logos": F("Muro de logos", "perfil estructura", "Actores de un segmento, solo nombre o logo", "M",
                    "ficha_linea grupo_fichas grupo_logos"),
    "grupo_fichas": F("Grupo de fichas", "perfil evidencia", "2 a 6 casos con icono, dato y origen", "S",
                      "tarjeta_actor icono_dato"),
    "ficha_hipotesis": F("Ficha de hipótesis", "perfil evaluar", "Lo probado, la hipótesis, criterios con nota y ejemplos", "L",
                         "columnas_evolucion ficha_empresa"),
    "tarjetas_salida": F("Tarjetas de salida", "decidir", "2 a 4 escenarios o salidas con su alcance", "L",
                         "balanza arbol_tramite lista_numerada"),
    "cita": F("Cita destacada", "evidencia", "Una cita con autor", "S",
              "panel_entrevistas aviso afirmacion_evidencia"),
    "lista_numerada": F("Lista numerada", "decidir resumir", "3 a 5 recomendaciones o pasos", "M",
                        "tarjetas_salida pilares columnas_numeradas"),
    "aviso": F("Recuadro de llamada", "apoyo evidencia", "Un supuesto crítico o una advertencia", "S",
               "cita"),
    "etiquetas_icono": F("Etiquetas con icono", "apoyo estructura", "2 a 4 condiciones o capacidades", "S",
                         "fila_parametros icono_dato"),
    "antes_despues_imagen": F("Antes y después en imagen", "ilustrar explicar_cambio", "Dos imágenes con rótulo", "M",
                              "columnas_evolucion escena_iso"),
    # ---------------------------------------------------------------- marcas y apoyo
    "delta": F("Chip de variación", "estado apoyo", "Una variación con tono bueno, neutro o malo", "S", "cifra_delta"),
    "harvey": F("Bolas de Harvey", "evaluar apoyo", "Nivel de 0 a 4", "S", "valoracion marca"),
    "marca": F("Marcas sí, parcial y no", "estado apoyo", "Cumplimiento en celdas", "S", "harvey semaforo"),
    "semaforo": F("Semáforo de estado", "estado", "Estado ok, riesgo o bloqueo", "S", "marca barra_progreso"),
    "barra_progreso": F("Barra de progreso", "estado", "Avance sobre un total conocido", "S", "indicador bala"),
    "valoracion": F("Puntos de valoración", "evaluar apoyo", "Nota de n sobre 5", "S", "harvey"),
    "etiqueta_evidencia": F("Nivel de evidencia", "evidencia apoyo", "A, B o C junto a un dato", "S", "chip_nota"),
    "chip_nota": F("Nota 0 a 3 con confianza", "evaluar apoyo", "Nota y confianza de una celda de matriz", "S", "harvey valoracion"),
    "pill": F("Píldoras de estado", "apoyo estado", "Una etiqueta corta de estado o categoría", "S", "semaforo"),
    "icono_caja": F("Icono en caja", "apoyo", "Un icono de Material Symbols en su caja", "S", "escena_iso"),
    "llave": F("Llave de agrupación", "apoyo", "Una lectura común para un grupo de elementos", "S", ""),
    "separador": F("Separador de bloque", "apoyo", "Número y título de un bloque dentro de la slide", "S", ""),
    "leyenda": F("Leyenda", "apoyo", "Colores y formas de las series, solo si no cabe la etiqueta directa", "S", ""),
    # ---------------------------------------------------------------- tablas
    "tabla_comparativa": F("Tabla comparativa", "evaluar decidir", "2 a 5 opciones en 4 a 10 criterios", "L",
                           "criterios_puntos matriz_puntuacion radar"),
    "tabla_con_barras": F("Tabla con barras", "ordenar comparar", "Filas de texto con una columna numérica", "L",
                          "barras_ranking ficha_linea"),
    "tabla_referencia": F("Tabla con barra frente a referencia", "brecha evidencia", "Filas con una barra frente a objetivo y referencia", "L",
                          "tabla_con_barras barras_objetivo"),
    "tabla_grafica": F("Tabla gráfica", "parte_todo comparar", "Total, reparto en 100 % y destacados por fila, con panel lateral", "L",
                       "tabla_con_barras barras_apiladas"),
    "matriz_puntuacion": F("Matriz de puntuación", "evaluar decidir", "Opciones agrupadas por veredicto con notas de 0 a 3 y total", "L",
                           "mapa_calor tabla_comparativa criterios_puntos"),
    "scorecard": F("Scorecard", "decidir evaluar", "Criterios eliminatorios y comparativos con su peso", "L",
                   "criterios_puntos tabla_comparativa"),
    "tabla_vigilancia": F("Tabla de vigilancia", "decidir perfil", "Opciones no prioritarias con su disparador y actores", "L",
                          "escalera_prioridad tabla_comparativa"),
    "tabla_drivers": F("Tabla de drivers de mercado", "explicar_cambio tendencia", "Drivers con fuerza e impacto por periodo", "L",
                       "cinco_fuerzas arbol_drivers"),
    "panel_entrevistas": F("Panel de entrevistas", "evidencia", "Entrevistas por perspectiva y su detalle", "L",
                           "cita contadores"),
    # ---------------------------------------------------------------- síntesis
    "tarjetas_miniatura": F("Tarjetas con miniatura", "resumir", "2 a 4 conclusiones con una miniatura de la slide que resumen", "L",
                            "lista_numerada pilares"),
    "mini_barras_objetivo": F("Miniatura de barras", "resumir brecha", "Hasta 3 barras frente a referencia y objetivo", "S", "barras_objetivo"),
    "mini_conteo": F("Miniatura de conteo", "resumir cifra", "Hasta 10 círculos con los marcados", "S", "pictograma"),
    "mini_iconos": F("Miniatura de iconos", "resumir", "2 a 4 iconos con una palabra", "S", "etiquetas_icono"),
    "mini_escalera": F("Miniatura de escalera", "resumir decidir", "3 niveles con códigos", "S", "escalera_prioridad"),
    "mini_flechas": F("Miniatura de proceso", "resumir proceso", "Hasta 4 pasos", "S", "proceso_flechas chevrones"),
    "mini_bifurcacion": F("Miniatura de bifurcación", "resumir decidir", "Una etapa, un corte y dos ramas", "S", "arbol_tramite"),
    # ---------------------------------------------------------------- añadidos del 01-11-2026
    "ranking_logos": F("Ranking por logo", "ordenar evaluar", "Actores con su puntuación, reconocibles por el logo", "S",
                       "barras_ranking tabla_con_barras"),
    "combo_financiero": F("Métricas financieras (combo)", "tendencia perfil", "Ingresos, EBITDA y margen de una empresa en 3 a 6 periodos", "M",
                          "columnas linea ficha_empresa"),
    "score_dimensiones": F("Score por dimensiones", "evaluar perfil", "Valor de un actor en 4 a 8 dimensiones y su total", "M",
                           "radar deslizadores criterios_puntos"),
    "mapa_actores": F("Mapa con grupos de actores", "geografia relacion", "Grupos de actores con sus países y un punto en el mapa", "L",
                      "mapa_coropletico muro_logos"),
    "convergencia": F("Convergencia", "relacion explicar_cambio", "3 o 4 causas con texto que llevan a un concepto", "L",
                      "abanico_foco radial"),
    "abanico_foco": F("Abanico desde un foco", "estructura explicar_cambio", "Un foco y 3 a 6 filas de rótulo y texto", "L",
                 "arbol radial lista_numerada"),
    "arbol_opciones": F("Árbol de opciones", "decidir estructura", "Categorías con opciones numeradas y su explicación", "L",
                        "arbol_tramite tarjetas_salida mapa_alcance"),
    "cadena_margen": F("Cadena con margen y valor capturado", "cadena comparar", "3 a 7 eslabones con margen, valor capturado y posición del cliente", "L",
                       "cadena_capas cadena_isometrica"),
    "trayecto": F("Trayecto de hoy al destino", "decidir cadena", "2 a 4 etapas: hoy, destino y vía", "L",
                  "chevrones escalones fases_gates"),
    "fases_gates": F("Fases con gates", "proceso calendario decidir", "2 a 4 fases con plazo, acciones y gate", "L",
                     "chevrones gantt proceso_flechas"),
    "columna_contexto": F("Columna de contexto", "evidencia cifra", "Rótulo, 2 o 3 párrafos y una cifra ancla", "S",
                          "contadores tarjeta_cifra bloque"),
    "bloque": F("Bloque con filete superior", "apoyo estructura", "Título y texto corto o HTML", "S",
                "aviso tarjeta_cifra columna_contexto"),
    "columnas_numeradas": F("Columnas numeradas con cifras", "resumir cifra", "2 a 4 ideas con título, texto y una o dos cifras", "L",
                            "lista_numerada pilares tarjetas_miniatura"),
    "afirmacion_evidencia": F("Afirmación y evidencia", "evidencia resumir", "2 a 4 afirmaciones con su cita y autor", "L",
                              "cita panel_entrevistas"),
    "columnas_requisitos": F("Columnas de requisitos con coste y plazo", "decidir estructura", "2 a 4 dimensiones con requisitos, coste y plazo", "L",
                             "columnas_numeradas tabla_comparativa"),
    "tarjetas_escenario": F("Tarjetas de escenario", "decidir comparar", "2 o 3 escenarios con dato, texto y visual pequeño", "L",
                            "abanico tarjetas_salida balanza"),
    "grupo_logos": F("Grupo de logos", "perfil apoyo", "Logos o nombres de una columna (tier, vía, segmento)", "S",
                     "muro_logos tarjeta_actor"),
    "matriz_portfolio": F("Mapa de portfolio", "perfil estructura", "Productos de un actor por vía o segmento", "M",
                          "tabla_comparativa mapa_calor"),
}


def familia_de(nombre):
    for m, f, _, els in FAMILIAS:
        if nombre in els:
            return m, f
    return None, None


SINONIMOS = {"aliados": "actores", "aliado": "actores", "partners": "actores", "partner": "actores", "socios": "actores",
             "empresas": "actores", "ecosistema": "actores", "funnel": "embudo", "cronograma": "gantt", "timeline": "tiempo",
             "kpi": "cifra", "ranking": "ranking", "semaforo": "estado", "pais": "mapa", "paises": "mapa", "foto": "imagen",
             "proporcion": "reparto", "proporciones": "reparto", "porcentaje": "reparto", "porcentajes": "reparto", "composicion": "compone",
             "evolucion": "evoluciona", "comparar": "cuanto", "comparacion": "cuanto"}
_VACIAS = set("de del la el los las un una y o en por con para al a que".split())


def _norma(t):
    import unicodedata
    t = unicodedata.normalize("NFD", str(t).lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def _en(palabra, texto):
    """Por inicio de palabra: «actor» no debe encontrar «factores»."""
    return re.search(r"\b" + re.escape(palabra), texto) is not None


def _buscar_texto(consulta, escala=None):
    """Búsqueda en lenguaje natural: «cadena de valor», «logos», «partners». Primero lo que lo dice en el nombre."""
    palabras = [w for w in _norma(consulta).replace("_", " ").split() if w not in _VACIAS]
    claves = [SINONIMOS.get(w, w).rstrip("s") or w for w in palabras]
    nombres_int = {k: _norma(f"{a} {b}") for k, a, b in INTENCIONES}
    puntos = []
    for n, f in FICHAS.items():
        if escala and f["escala"] != escala:
            continue
        nombre = _norma(f"{n.replace('_', ' ')} {f['titulo']}")
        datos = _norma(f["datos"])
        ints = " ".join(nombres_int[i] for i in f["intenciones"]) + " " + _norma(next((b + " " + c for _, b, c, els in FAMILIAS if n in els), ""))
        p = 0
        if claves and all(_en(c, nombre) for c in claves):
            p = 4
        elif claves and all(_en(c, nombre + " " + datos) for c in claves):
            p = 3
        elif claves and all(_en(c, nombre + " " + datos + " " + ints) for c in claves):
            p = 2
        elif any(_en(c, nombre) for c in claves):
            p = 1
        elif any(_en(c, datos + " " + ints) for c in claves):
            p = .5
        if p:
            puntos.append((-p, n))
    if sum(-p >= 2 for p, _ in puntos) >= 3:
        puntos = [x for x in puntos if -x[0] >= 2]
    return [n for _, n in sorted(puntos)]


def buscar(intencion=None, escala=None):
    """Todas las candidatas para una intención (y una escala, S, M o L), las que la tienen como principal primero.
    Si lo que se pasa no es una clave de intención, busca en lenguaje natural: buscar("cadena de valor"), buscar("logos")."""
    if intencion and intencion not in _CLAVES:
        return _buscar_texto(intencion, escala)
    out = []
    for n, f in FICHAS.items():
        if intencion and intencion not in f["intenciones"]:
            continue
        if escala and f["escala"] != escala:
            continue
        out.append((0 if not intencion or f["intenciones"][0] == intencion else 1, n))
    return [n for _, n in sorted(out)]


def comprobar(paquete):
    """Errores de coherencia entre taxonomía y código: elementos sin ficha, fichas sin elemento, intenciones o
    alternativas que no existen. La galería no se genera si hay alguno."""
    err = []
    en_familias = [e for *_, els in FAMILIAS for e in els]
    for e in en_familias:
        if not callable(getattr(paquete, e, None)):
            err.append(f"{e}: está en FAMILIAS pero no existe en el paquete")
        if e not in FICHAS:
            err.append(f"{e}: sin ficha en FICHAS")
    for e, f in FICHAS.items():
        if e not in en_familias:
            err.append(f"{e}: tiene ficha pero no está en ninguna familia")
        for i in f["intenciones"]:
            if i not in _CLAVES:
                err.append(f"{e}: intención desconocida «{i}»")
        for a in f["alternativas"]:
            if a not in FICHAS:
                err.append(f"{e}: alternativa desconocida «{a}»")
        if f["escala"] not in ("S", "M", "L"):
            err.append(f"{e}: escala «{f['escala']}»")
    for m, _, _, els in FAMILIAS:
        mod = getattr(paquete, m)
        sueltos = [k for k in getattr(mod, "__all__", []) if callable(getattr(mod, k)) and not isinstance(getattr(mod, k), type)
                   and k not in els and k not in NO_ELEMENTOS]
        err += [f"{m}.{k}: función pública sin familia (añadirla a FAMILIAS y FICHAS, o a NO_ELEMENTOS)" for k in sueltos]
    if len(set(en_familias)) != len(en_familias):
        err.append("hay elementos repetidos en FAMILIAS")
    return err


NO_ELEMENTOS = {"escena"}   # funciones públicas que no son elementos (el decorador de escenas)
