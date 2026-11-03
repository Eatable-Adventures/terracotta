#!/usr/bin/env python3
"""Galería de elementos: todos los elementos de ea_elementos en una página web por familias (no en slides), con
un índice para elegir por intención. Cada tarjeta lleva el elemento con datos ficticios, el nombre de la
función, la escala, a qué intenciones responde, cuándo usarlo y cuándo no (de los docstrings) y sus alternativas.

También regenera la fuente de iconos y «Catálogo de iconos.html» (iconos.py), genera «Taxonomía de elementos.md»
(el menú legible de taxonomia.py) y no genera nada si la
taxonomía y el código no cuadran (elemento sin ficha, ficha sin ejemplo, alternativa que no existe).

Ejecutar: python3 build_galeria_elementos.py [--png DIR]   (--png: captura de página completa en trozos)
"""
import html, inspect, pathlib, re, subprocess, sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import ea_deck                  # noqa: E402
import ea_elementos as X        # noqa: E402
from ea_elementos import taxonomia as TX   # noqa: E402
import referencias                        # noqa: E402
import laboratorio                        # noqa: E402

E = html.escape
OUT = AQUI / "Galería de elementos.html"
OUT_MD = AQUI / "Taxonomía de elementos.md"
OUT_ICONOS = AQUI / "Catálogo de iconos.html"
OUT_ICONOS_MD = AQUI / "Catálogo de iconos.md"

VARIANTES = {"columnas": ["columnas_cagr"], "cascada": ["cascada_evidencia"], "cadena_isometrica": ["cadena_isometrica_proteina"], "linea": ["linea_periodos"]}
TX_RAMPA = list(X.RAMP)
_filas_cadena = "".join(
    f'<tr><td style="padding:7px 12px"><a href="#{pz}"><code>{pz}()</code></a></td><td style="padding:7px 12px"><b>{para}</b></td>'
    f'<td style="padding:7px 12px">{gana}</td><td style="padding:7px 12px">{pierde}</td></tr>' for pz, para, gana, pierde in laboratorio.GUIA_CADENA)
GUIA_FAMILIA = {"cadena": (
    '<div class="reglas" style="margin:0 0 18px"><b>¿Qué cadena de valor uso?</b> Cada una responde a una pregunta distinta. Si el mensaje no decide, se enseñan '
    'varias con los mismos datos y elige quien encarga el deck: <code>laboratorio.opciones_cadena()</code> y <code>laboratorio.generar()</code> las montan.'
    '<table style="width:100%;border-collapse:collapse;margin-top:10px;font-size:13px;text-align:left"><tr style="font-weight:700"><td style="padding:7px 12px">Pieza</td>'
    '<td style="padding:7px 12px">Para</td><td style="padding:7px 12px">Gana</td><td style="padding:7px 12px">Pierde</td></tr>' + _filas_cadena + '</table></div>')}
BASE = {"columnas_cagr": "columnas", "cascada_evidencia": "cascada", "cadena_isometrica_proteina": "cadena_isometrica", "linea_periodos": "linea"}
TITULOS_VARIANTE = {"columnas_cagr": "Columnas con previsión y CAGR", "cascada_evidencia": "Cascada con fila de evidencia", "linea_periodos": "Líneas con periodos sombreados",
                    "cadena_isometrica_proteina": "Cadena isométrica: otra cadena con las mismas piezas"}
CODIGO_VARIANTE = {"columnas_cagr": "columnas(prevision_desde, cagr)", "cascada_evidencia": "cascada(evidencia)", "linea_periodos": "linea(periodos)",
                   "cadena_isometrica_proteina": "cadena_isometrica(fases)"}
# Origen en las referencias externas fichadas en catalogo/ (datos, no plantillas): lo dice cada ficha en su campo «elementos»
REF = referencias.origenes()
ESCALA = {"S": "pieza", "M": "media slide", "L": "ancho de slide"}

# ================================================================== ejemplos (datos ficticios)
ING = [("Estevia", 74), ("Alulosa", 71), ("Fibras", 66), ("Enzimas", 52), ("Aromas", 45), ("Proceso", 64)]
AN = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
G = ' '.join


def ej(nombre):
    """Ejemplo de cada elemento (None si no está aquí, y entonces lo da ej2)."""
    return {
        "columnas": lambda: X.columnas([("2022", 42), ("2023", 51), ("2024", 58), ("2025", 66), ("2026", 81)], destacado=4, unidad=" M€",
                                       eje="Ventas de lácteos reducidos en azúcar, millones de euros"),
        "barras_ranking": lambda: X.barras_ranking([("Edulcorantes vegetales", 71), ("Fibras solubles", 66), ("Proceso", 64),
                                                    ("Envase y formato", 52), ("Azúcares raros", 49), ("Enzimas in situ", 47),
                                                    ("Moduladores de sabor", 45)], destacado="Proceso", ancho_rotulo=160),
        "barras_agrupadas": lambda: X.barras_agrupadas(["Dulzor", "Textura", "Sabor residual", "Coste"],
                                                       [("Producto actual", [8.1, 7.6, 7.9, 6.0]), ("Prototipo", [7.4, 7.2, 6.8, 7.1])]),
        "barras_apiladas": lambda: X.barras_apiladas(["España", "Portugal", "Francia", "Italia"],
                                                     [("Súper", [52, 48, 41, 45]), ("Discount", [28, 30, 22, 25]), ("Online", [12, 9, 21, 14]), ("Otros", [8, 13, 16, 16])]),
        "piruletas": lambda: X.piruletas(ING, referencia=(60, "Media 60"), destacado="Proceso"),
        "pictograma": lambda: X.pictograma(10, 7, "7 de 10", "consumidores **reduce el azúcar** de su dieta y lo mira en la etiqueta"),
        "linea": lambda: X.linea(AN, [("Cliente Demo", [12, 13, 15, 18, 22, 27, 31]), ("Líder", [20, 22, 23, 25, 26, 27, 28]),
                                      ("Marca blanca", [8, 9, 11, 12, 13, 15, 16])], anotaciones=[(0, 3, "Lanzamiento 0 %")], unidad=" %"),
        "area_apilada": lambda: X.area_apilada(AN, [("Estevia", [10, 12, 14, 15, 17, 18, 20]), ("Alulosa", [2, 3, 5, 7, 10, 13, 16]),
                                                    ("Fibras", [6, 6, 7, 8, 8, 9, 10]), ("Otros", [3, 3, 4, 4, 5, 5, 6])]),
        "pendiente": lambda: X.pendiente([("Estevia", 61, 74), ("Alulosa", 40, 71), ("Fibras", 66, 66), ("Enzimas", 58, 52), ("Aromas", 49, 45)],
                                         periodos=("2024", "2026"), destacado="Alulosa"),
        "cascada": lambda: X.cascada(("Actual", 18), [("Edulcorante", -3.5), ("Fibra", -1.5), ("Enzima", -1.0), ("Ajuste\nsabor", 0.5)],
                                     "Objetivo", unidad=" g"),
        "sparkline": lambda: X.sparkline([12, 13, 15, 14, 18, 22, 21, 27, 31], 200, 44),
        "donut": lambda: X.donut([("Supermercado", 52), ("Discount", 28), ("Online", 12), ("Otros", 8)], centro=("52 %", "de las ventas en supermercado"), destacado=0),
        "waffle": lambda: X.waffle(31, "31 %", "de los lanzamientos lácteos de 2026 **declara menos azúcar**"),
        "treemap": lambda: X.treemap([("Estevia", 34), ("Alulosa", 18), ("Fibras", 14), ("Monk fruit", 11), ("Enzimas", 8), ("Aromas", 7),
                                      ("Tagatosa", 5), ("Otros", 3)], destacado="Alulosa"),
        "marimekko": lambda: X.marimekko([("Europa", 46, [40, 35, 25]), ("Norteamérica", 32, [30, 45, 25]), ("Latam", 14, [55, 25, 20]),
                                          ("Asia", 8, [20, 30, 50])], ["Edulcorantes", "Fibras", "Otros"], rotulo_ancho="cuota del mercado total"),
        "sankey": lambda: X.sankey(["Estevia", "Alulosa", "Fibras"], ["Bebidas", "Yogur", "Postres"],
                                   [("Estevia", "Bebidas", 30), ("Estevia", "Yogur", 12), ("Estevia", "Postres", 6), ("Alulosa", "Bebidas", 8),
                                    ("Alulosa", "Yogur", 14), ("Alulosa", "Postres", 9), ("Fibras", "Yogur", 10), ("Fibras", "Postres", 11)],
                                   destacado=("Alulosa", "Yogur")),
        "radar": lambda: X.radar(["Dulzor", "Coste", "Regulación", "Madurez", "Vida útil", "Etiqueta limpia"],
                                 [("Alulosa", [4.5, 2.5, 3, 3.5, 4, 3]), ("Media de opciones", [3.5, 3.2, 3.6, 3.2, 3.4, 3.8])]),
        "mancuerna": lambda: X.mancuerna([("Batido de cacao", 9.8, 6.5), ("Yogur bebible", 11.2, 7.5), ("Leche de fresa", 10.4, 7.0),
                                          ("Kéfir de sabores", 8.6, 6.2)], dominio=(5, 12), unidad=" g"),
        "bala": lambda: X.bala([dict(rotulo="Reducción de azúcar", sub="% sobre la receta actual", valor=28, objetivo=33, maximo=40, unidad=" %"),
                                dict(rotulo="Aceptación", sub="panel, sobre 9", valor=7.1, objetivo=7, maximo=9),
                                dict(rotulo="Sobrecoste", sub="céntimos por litro", valor=2.4, objetivo=3, maximo=5, menor_mejor=True)]),
        "tornado": lambda: X.tornado([("Precio del edulcorante", 1.2, 3.1), ("Volumen anual", 1.6, 2.6), ("Merma de proceso", 1.9, 2.4),
                                      ("Coste de envase", 2.0, 2.3)], 2.1, unidad=" M€"),
        "rangos": lambda: X.rangos([("Proveedor A", 2.8, 3.6), ("Proveedor B", 3.1, 4.2), ("Proveedor C", 2.2, 3.0), ("Referencia sector", 2.5, 3.9)],
                                   marca=(3.2, "Objetivo 3,2 €/kg"), destacado="Proveedor C", unidad=" €"),
        "indicador": lambda: X.indicador(68, 0, 100, "68 %", "del objetivo de reducción", objetivo=(80, "Meta 2027")),
        "dispersion": lambda: X.dispersion([dict(rotulo="Estevia", x=8, y=7.5, tam=34), dict(rotulo="Alulosa", x=5.5, y=8.2, tam=18, destacado=True),
                                            dict(rotulo="Fibras", x=7, y=4.5, tam=14), dict(rotulo="Enzimas", x=3.5, y=5.8, tam=8),
                                            dict(rotulo="Aromas", x=6.4, y=3, tam=7), dict(rotulo="Fermentación", x=2, y=8.6, tam=5)],
                                           ("Madurez técnica", "Encaje con el reto"), (0, 10), (0, 10), umbrales=(5, 5),
                                           cuadrantes=["Explorar", "Priorizar", "Descartar", "Vigilar"]),
        "mapa_calor": lambda: X.mapa_calor(["Estevia", "Alulosa", "Fibras", "Enzimas", "Aromas"], ["2021", "2022", "2023", "2024", "2025", "2026"],
                                           [[12, 15, 18, 20, 22, 25], [2, 4, 9, 14, 21, 30], [8, 8, 9, 11, 10, 12], [3, None, 5, 6, 8, 9], [5, 6, 6, 7, 7, 8]],
                                           destacado=(1, 5)),
        "histograma": lambda: X.histograma(["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90"],
                                           [4, 11, 26, 41, 52, 38, 21, 9, 3], marca=(6, "Nuestra puntuación: 64")),
        "matriz_2x2": lambda: X.matriz_2x2((("Bajo", "Alto", "Impacto"), ("Baja", "Alta", "Facilidad")),
                                           [("Mejoras rápidas", "Poco impacto, pero se prueban solas"), ("Prioridad", "Mucho impacto y **fácil de probar**"),
                                            ("Descartar", "Poco impacto y difícil"), ("Proyectos de fondo", "Mucho impacto, mucho esfuerzo")],
                                           [("Estevia", .78, .7, False), ("Alulosa", .62, .74, True), ("Fibras", .3, .62, False), ("Fermentación", .66, .24, False),
                                            ("Aromas", .22, .3, False)]),
        "venn": lambda: X.venn([("Técnica", "Funciona en la matriz láctea"), ("Mercado", "El consumidor lo compra"), ("Regulación", "Se puede declarar en etiqueta")],
                               "Punto dulce"),
        "circulos_concentricos": lambda: X.circulos_concentricos([("TAM", "4.200 M€", "bebidas lácteas en Europa"),
                                                                  ("SAM", "1.150 M€", "segmento **reducido en azúcar**"),
                                                                  ("SOM", "85 M€", "alcanzable en 3 años")]),
        "radial": lambda: X.radial("Cliente Demo", [("science", "I+D", "Laboratorio propio"), ("factory", "Planta", "2 líneas UHT"),
                                                    ("local_shipping", "Proveedores", "12 homologados"), ("storefront", "Retail", "4 cadenas"),
                                                    ("gavel", "Regulador", "Etiquetado"), ("groups", "Consumidor", "Panel interno")]),
        "arbol": lambda: X.arbol("¿Cómo bajar un 33 % el azúcar?", [("Sustituir azúcar", ["Edulcorantes vegetales", "Azúcares raros"]),
                                                                     ("*Generar dulzor in situ", ["Enzimas sobre la lactosa", "Fermentación"]),
                                                                     ("Engañar a la percepción", ["Aromas moduladores", "Temperatura de consumo"])]),
        "piramide": lambda: X.piramide([("Liderar", "Producto **sin azúcar añadido** con el mismo sabor"), ("Diferenciar", "Reducción visible en etiqueta"),
                                        ("Cumplir", "Perfil nutricional que exige la norma"), ("Higiene", "Seguridad y vida útil sin cambios")]),
        "capas": lambda: X.capas([("storefront", "Producto", "Bebida láctea con 33 % menos azúcar"), ("tune", "Formulación", "Mezcla de edulcorante, fibra y aroma"),
                                  ("precision_manufacturing", "Proceso", "UHT y homogeneización ajustadas"), ("inventory_2", "Materia prima", "Leche, ingredientes homologados")]),
        "espina_pescado": lambda: X.espina_pescado("Sabor residual amargo en el prototipo", [
            ("Ingrediente", ["Dosis de estevia alta", "Pureza del extracto"]), ("Proceso", ["Temperatura UHT", "Tiempo de mezcla"]),
            ("Formulación", ["Sin enmascarante", "pH bajo"]), ("Medición", ["Panel poco entrenado", "Una sola sesión"]),
            ("Envase", ["Luz y oxidación"]), ("Materia prima", ["Variación de la leche"])]),
        "balanza": lambda: X.balanza(("Licenciar", ["Llega antes al mercado", "Menos inversión"]),
                                     ("Desarrollar", ["**Propiedad del proceso**", "Margen a largo plazo", "Know-how interno"]), inclinacion=7),
        "chevrones": lambda: X.chevrones([("Diagnóstico", "Reto, norma y punto de partida"), ("Búsqueda", "Opciones en patentes y mercado"),
                                          ("Priorización", "Matriz con 9 criterios"), ("Validación", "Ensayos con el cliente"), ("Piloto", "Escala industrial")], activo=2),
        "linea_tiempo": lambda: X.linea_tiempo([("Ene 2026", "Kick-off", "Alcance y criterios"), ("Mar 2026", "Informe E1", "8 opciones"),
                                                ("May 2026", "Gate 1", "3 opciones pasan"), ("Sep 2026", "Ensayos", "Panel sensorial"),
                                                ("Dic 2026", "Gate 2", "Elegir solución"), ("Abr 2027", "Piloto", "Planta del cliente")], hoy=3),
        "ciclo": lambda: X.ciclo([("search", "Vigilar"), ("science", "Ensayar"), ("fact_check", "Validar"), ("factory", "Escalar"), ("query_stats", "Medir")],
                                 "Mejora continua del portfolio"),
        "carriles": lambda: X.carriles(["Ingredientes", "Proceso", "Regulatorio", "Comercial"], ["T1 2026", "T2 2026", "T3 2026", "T4 2026", "T1 2027"],
                                       [(0, 0, 1.5, "Búsqueda de proveedores", False), (0, 1.5, 3, "Ensayos de mezcla", True), (1, 1, 2.5, "Ajuste UHT", False),
                                        (1, 3, 5, "Piloto industrial", False), (2, 0.5, 2, "Revisión de claims", False), (2, 3.5, 4.5, "Etiqueta", False),
                                        (3, 2.5, 4, "Test con retail", False), (3, 4, 5, "Lanzamiento", True)]),
        "escalones": lambda: X.escalones([("Explorar", "Mapa de opciones"), ("Probar", "Ensayos de banco"), ("Validar", "Panel y vida útil"), ("Escalar", "Piloto en planta")]),
        "cifra_delta": lambda: '<div style="display:flex;gap:14px">' + X.cifra_delta("31 %", "Cuota en reducidos", "+4 pp", "vs 2025", [18, 20, 22, 24, 27, 31], W=255)
                               + X.cifra_delta("12 g", "Azúcar por ración", "−6 g", "vs actual", None, sube=False, tono="bueno", W=255) + '</div>',
        "delta": lambda: '<div style="display:flex;gap:10px;align-items:center">' + X.delta("+12 %") + X.delta("0 pp", sube=None, tono="neutro") + X.delta("−2 pp", sube=False, tono="malo") + '</div>',
        "icono_dato": lambda: X.icono_dato([("groups", "62 %", "de los hogares compra lácteos **reducidos en azúcar**"),
                                            ("storefront", "4", "cadenas ya piden la versión reducida"), ("gavel", "2027", "entra en vigor el nuevo perfil nutricional")]),
        "harvey": lambda: '<div style="display:flex;gap:18px;align-items:center">' + "".join(
            f'<span style="display:inline-flex;gap:6px;align-items:center;font-size:12px;color:var(--fg2)">{X.harvey(n, 22)}{n}/4</span>' for n in range(5)) + '</div>',
        "marca": lambda: '<div style="display:flex;gap:22px;align-items:center;font-size:12px;color:var(--fg2)">' + "".join(
            f'<span style="display:inline-flex;gap:7px;align-items:center">{X.marca(t, 22)}{r}</span>' for t, r in
            (("si", "Cumple"), ("parcial", "Parcial"), ("no", "No cumple"), ("nd", "Sin dato"))) + '</div>',
        "semaforo": lambda: '<div style="display:flex;gap:22px">' + X.semaforo("ok") + X.semaforo("riesgo") + X.semaforo("bloqueo") + '</div>',
        "barra_progreso": lambda: '<div style="display:flex;flex-direction:column;gap:14px">' + X.barra_progreso(42, 60, "Fuentes revisadas", "42 de 60", W=420)
                                  + X.barra_progreso(68, 100, "Avance del objetivo de reducción", W=420) + '</div>',
        "valoracion": lambda: '<div style="display:flex;flex-direction:column;gap:10px;font-size:12.5px;color:var(--fg2)">' + "".join(
            f'<span style="display:flex;gap:14px;align-items:center"><span style="width:110px">{r}</span>{X.valoracion(n)}</span>'
            for r, n in (("Dulzor", 4), ("Coste", 2), ("Madurez", 5))) + '</div>',
        "etiqueta_evidencia": lambda: '<div style="display:flex;gap:22px">' + X.etiqueta_evidencia("A") + X.etiqueta_evidencia("B") + X.etiqueta_evidencia("C") + '</div>',
        "cita": lambda: X.cita("Si el yogur sabe a edulcorante, **el consumidor no repite**, por mucho que diga menos azúcar.", "Responsable de I+D", "fabricante lácteo europeo", W=500),
        "lista_numerada": lambda: X.lista_numerada([("Ensayar alulosa y fibra juntas", "Es la única mezcla que llega al 33 % sin perder dulzor."),
                                                    ("Pedir muestras a 3 proveedores", "Con ficha técnica y precio por kilo antes del 15-01-2027."),
                                                    ("Fijar el panel sensorial", "Mismo protocolo que el producto actual.")], W=500),
        "aviso": lambda: '<div style="display:flex;flex-direction:column;gap:10px">' + X.aviso("La alulosa **no está autorizada** aún como nuevo alimento en la UE.", "aviso", 500)
                         + X.aviso("Supuesto crítico: el cliente mantiene **el mismo envase**.", "clave", 500) + X.aviso("Datos de 2025; se actualizan en el informe final.", "nota", 500) + '</div>',
        "llave": lambda: '<div style="display:flex;align-items:center;gap:10px"><div style="display:flex;flex-direction:column;gap:8px">' + "".join(
            f'<div class="tile" style="background:var(--surface-fill);width:200px;height:38px">{t}</div>' for t in ("Estevia", "Monk fruit", "Alulosa")) + '</div>'
            + X.llave(130, "Las tres ya tienen **proveedor en Europa**", W=230) + '</div>',
        "persona": lambda: '<div style="display:flex;gap:28px;flex-wrap:wrap">' + X.persona("Ana Ruiz", "Directora de I+D, Cliente Demo") + X.persona("Marta Ortega", "Innovation Consultant, EA", destacada=True) + '</div>',
        "muro_logos": lambda: X.muro_logos(_marcas("Alfa Beta Delta Gamma Omega Sigma Kappa Theta"), W=500),
        "ecosistema_logos": lambda: X.ecosistema_logos([
            dict(rotulo="Finalistas", estado="En negociación", destacado=True, actores=_marcas("Alfa Beta Gamma")),
            dict(rotulo="En validación", estado="Activos", actores=_marcas("Delta Omega Sigma Kappa Theta Zeta Lambda Tau Rho")),
            dict(rotulo="Han declinado", estado="Cerrado", actores=["Iota", "Nu", "Xi", "Pi", "Chi", "Psi", "Eta", "Mu", "Fi", "Ro", "Ka"])], W=1120, alto_logo=24),
        "separador": lambda: X.separador("01", "Qué hay en el mercado", "8 opciones en 4 familias", W=500),
        "leyenda": lambda: X.leyenda([(X.RED, "Nosotros", "linea"), (X.REFERENCIA, "Referencia", "discontinua"), (X.NEUTRO, "Resto", "cuadro"), (X.RED, "Destacado", "punto")]),
        "tabla_comparativa": lambda: X.tabla_comparativa(["Estevia", "Alulosa", "Fibras"], [("Mantiene el dulzor", ["si", "si", "parcial"]),
                                                         ("Autorizado en la UE", ["si", "no", "si"]), ("Etiqueta limpia", [3, 2, 4]),
                                                         ("Coste por litro", ["+1,2 cént.", "+3,4 cént.", "+0,8 cént."]), ("Proveedor homologado", ["si", "nd", "si"])],
                                                         destacada=0, W=500, ancho_criterio=170),
        "tabla_con_barras": lambda: X.tabla_con_barras(["Empresa", "País", "Tipo", "Patentes"], [["Alfa Ingredientes", "Suiza", "Proveedor", 42],
                                                       ["Beta Biotech", "Países Bajos", "Startup", 31], ["Delta Foods", "España", "Fabricante", 18],
                                                       ["Gamma Labs", "EE. UU.", "Startup", 11]], 3, destacado=1, W=500),
        "pareto": lambda: X.pareto([("Sobrellenado", 38), ("Roturas", 22), ("Caducidad", 14), ("Formato", 9), ("Arranques", 7), ("Limpieza", 5),
                                    ("Otros", 5)], unidad=" t"),
        "comparador_unidad": lambda: X.comparador_unidad([("Alfa Ingredientes", 3.1), ("Beta Biotech", 3.8), ("Delta Foods", 2.6), ("Gamma Labs", 3.4)],
                                                         (3.3, "Actual 3,3"), destacado="Delta Foods"),
        "curva_s": lambda: X.curva_s([("Fermentación", .1, False), ("Alulosa", .34, True), ("Fibras", .64, False), ("Estevia", .8, False)]),
        "abanico": lambda: X.abanico([str(a) for a in range(2020, 2031)], [12, 13, 15, 18, 22, 27, 31],
                                     dict(bajo=[32, 33, 34, 35], base=[35, 39, 43, 47], alto=[38, 45, 52, 59]), unidad=" M€"),
        "bump": lambda: X.bump(["2022", "2023", "2024", "2025", "2026"], [("Cliente Demo", [5, 4, 3, 2, 1]), ("Líder", [1, 1, 1, 1, 2]),
                                ("Alfa", [2, 2, 2, 3, 3]), ("Beta", [3, 3, 4, 4, 5]), ("Gamma", [4, 5, 5, 5, 4])], destacado="Cliente Demo"),
        "pequenos_multiplos": lambda: X.pequenos_multiplos([("España", [8, 10, 13, 17, 22, 28]), ("Francia", [15, 16, 18, 19, 21, 22]),
                                                            ("Alemania", [20, 21, 21, 22, 23, 23]), ("Italia", [6, 7, 7, 9, 10, 12]),
                                                            ("Portugal", [4, 5, 7, 8, 11, 14]), ("Países Bajos", [18, 17, 18, 17, 18, 19])],
                                                           ("2021", "2026"), destacado="España", unidad=" %"),
        "sunburst": lambda: X.sunburst([("Edulcorantes", [("Estevia", 34), ("Alulosa", 18), ("Monk fruit", 11)]), ("Fibras", [("Inulina", 9), ("Polidextrosa", 5)]),
                                        ("Sabor", [("Aromas", 7), ("Enmascarantes", 4)]), ("Proceso", [("Enzimas", 8), ("Otros", 4)])],
                                       centro=("100 M€", "mercado de soluciones"), destacado="Alulosa"),
        "barra_dividida": lambda: X.barra_dividida([("Lo compraría", [5, 10, 20, 40, 25]), ("Sabe igual que el original", [12, 23, 25, 28, 12]),
                                                    ("Confío en el edulcorante", [18, 22, 30, 20, 10]), ("Pagaría más por él", [25, 30, 25, 15, 5])]),
        "cajas": lambda: X.cajas([("Actual", [7.2, 7.5, 7.8, 7.4, 7.9, 8.1, 7.6, 7.3, 7.7, 8.0, 7.5, 7.8]),
                                  ("Estevia", [6.1, 6.8, 5.9, 6.5, 7.0, 6.2, 6.6, 5.5, 6.9, 6.4, 6.0, 6.7]),
                                  ("Alulosa", [7.0, 7.4, 6.8, 7.6, 7.2, 7.9, 7.1, 6.9, 7.5, 7.3, 7.7, 7.0]),
                                  ("Mezcla", [6.5, 7.1, 6.9, 7.4, 6.6, 7.2, 7.0, 6.8, 7.3, 6.4, 7.5, 6.9])],
                                 destacado="Alulosa", dominio=(5, 8.5), eje="Dulzor percibido (1 a 9)"),
        "red_nodos": lambda: X.red_nodos([dict(id="c", rotulo="Cliente Demo", grupo=0, tam=3, destacado=True), dict(id="l", rotulo="Líder", grupo=0, tam=2),
                                          dict(id="a", rotulo="Alfa", grupo=1, tam=2), dict(id="b", rotulo="Beta", grupo=2), dict(id="d", rotulo="Delta", grupo=1),
                                          dict(id="g", rotulo="Gamma", grupo=2), dict(id="u1", rotulo="Univ. Norte", grupo=3), dict(id="u2", rotulo="Centro Tec.", grupo=3),
                                          dict(id="k", rotulo="Kappa", grupo=2), dict(id="s", rotulo="Sigma", grupo=1)],
                                         [("c", "a"), ("c", "b"), ("c", "u1"), ("l", "a"), ("l", "d"), ("l", "u2"), ("a", "u1"), ("b", "u1"), ("g", "u2"),
                                          ("d", "u2"), ("k", "u1"), ("s", "l"), ("g", "l"), ("k", "c")],
                                         grupos=["Fabricantes", "Proveedores", "Startups", "Academia"]),
        "mapa_burbujas": lambda: X.mapa_burbujas({"España": 58, "Colombia": 71, "Argentina": 24, "México": 19, "Chile": 15, "Perú": 14, "Uruguay": 4, "Ecuador": 5},
                                                 region="hispano", destacado="Colombia", rotular=4, leyenda_txt="Candidaturas ficticias por país", W=1100),
        "mapa_flujos": lambda: X.mapa_flujos("España", [("México", "México", 30), ("Colombia", "Colombia", 45), ("Chile", "Chile", 12), ("Alemania", "Alemania", 8), ("Suecia", "Suecia", 6), ("Marruecos", "Marruecos", 5)],
                                             region="mundo", rotulo_origen="Origen", W=1100),
        "mapa_coropletico": lambda: X.mapa_coropletico({"España": 18, "Francia": 34, "Alemania": 41, "Italia": 15, "Países Bajos": 22, "Bélgica": 9,
                                                        "Reino Unido": 27, "Suiza": 31, "Dinamarca": 19, "Suecia": 8, "Polonia": 6, "Portugal": 7,
                                                        "Irlanda": 11, "Austria": 10, "Finlandia": 5, "Noruega": 4},
                                                       destacado="España", etiquetas=["España", "Francia", "Alemania", "Italia", "Reino Unido", "Polonia", "Suecia"],
                                                       leyenda_txt="patentes sobre edulcorantes, 2021 a 2026"),
        "cadena_capas": lambda: X.cadena_capas([
            dict(nombre="Materia prima", descripcion="Leche cruda, azúcar y otras materias primas.", actores=["Cooperativas", "Ganaderos"], margen=(3, 8, 5), tendencia=-1, oportunidad=.15),
            dict(nombre="Ingredientes", descripcion="Edulcorantes, fibras y aromas para **reducir azúcar**.", actores=["Alfa", "Beta Biotech", "Delta"], margen=(25, 40, 32), tendencia=1, oportunidad=.9),
            dict(nombre="Transformación", descripcion="Formulación, UHT y envasado.", actores=["Cliente Demo", "Líder", "Copackers"], margen=(10, 18, 14), tendencia=-1, oportunidad=.55),
            dict(nombre="Distribución", descripcion="Logística refrigerada a tienda.", actores=["Operadores 3PL"], margen=(4, 8, 6), tendencia=0, oportunidad=.2),
            dict(nombre="Retail", descripcion="Lineal, promoción y marca blanca.", actores=["4 cadenas"], margen=(20, 35, 28), tendencia=1, oportunidad=.35)], destacado=1),
        "cadena_isometrica": lambda: X.cadena_isometrica([
            dict(nombre="Materia prima", tipo="granja", texto="Leche cruda y azúcar de cooperativas.", dato="Margen ~5 %"),
            dict(nombre="Ingredientes", tipo="ingredientes", texto="Edulcorantes, fibras y aromas para **reducir azúcar**.", dato="Margen ~32 %"),
            dict(nombre="Transformación", tipo="fabrica", texto="Formulación, UHT y envasado en la planta del cliente.", dato="Margen ~14 %"),
            dict(nombre="Distribución", tipo="logistica", texto="Logística refrigerada hasta tienda.", dato="Margen ~6 %"),
            dict(nombre="Retail", tipo="retail", texto="Lineal, promoción y marca blanca.", dato="Margen ~28 %"),
            dict(nombre="Consumidor", tipo="consumidor", texto="Familias que buscan menos azúcar.", dato="62 % de hogares")], destacado=1),
        "cadena_isometrica_proteina": lambda: X.cadena_isometrica([
            dict(nombre="I+D", tipo="laboratorio", texto="Selección de cepas y proteína dulce."),
            dict(nombre="Fermentación", tipo="fermentacion", texto="Biorreactores de **precisión** a escala.", dato="Cuello de botella"),
            dict(nombre="Planta piloto", tipo="planta_piloto", texto="Validación con el cliente."),
            dict(nombre="Envasado", tipo="envasado", texto="Formato y vida útil."),
            dict(nombre="Venta online", tipo="ecommerce", texto="Lanzamiento directo al consumidor."),
            dict(nombre="Subproductos", tipo="valorizacion", texto="Biomasa a pienso o biogás.")], destacado=1),
        "escena_iso": lambda: '<div style="display:flex;gap:18px;align-items:flex-end">' + "".join(
            X.escena_iso(t, h, W=150, rotulo=r) for t, h, r in (("invernadero", False, "Invernadero"), ("fermentacion", True, "Fermentación"), ("frio", False, "Frigorífico"))) + '</div>',
        "catalogo_escenas": lambda: X.catalogo_escenas(columnas=6, destacado="fermentacion"),
        "lienzo_negocio": lambda: X.lienzo_negocio(dict(
            socios=["Proveedores de edulcorante", "Centro tecnológico"], actividades=["Formulación", "Ensayos sensoriales"],
            recursos=["Planta piloto", "Panel entrenado"], propuesta=["**33 % menos azúcar** con el mismo sabor", "Etiqueta limpia"],
            relaciones=["Desarrollo conjunto con la cadena"], canales=["Supermercado", "Online"], segmentos=["Familias con niños", "Consumidor saludable"],
            costes=["Ingrediente (+1,2 cént. por litro)", "Ensayos y piloto"], ingresos=["Venta con precio premium del 5 %", "Licencia de la fórmula"]),
            destacado="propuesta"),
        "organigrama": lambda: X.organigrama(("Ana Ruiz", "Directora de I+D", [("Luis Pardo", "Formulación", [("Eva Sanz", "Sensorial", []), ("Raúl Gil", "Laboratorio", [])]),
                                                                              ("Marta Vidal", "Regulatorio", [("Iñigo Sola", "Etiquetado", [])], True),
                                                                              ("Jorge Ramos", "Compras", [("Sara León", "Homologación", [])]),
                                                                              ("Claudia Mena", "Calidad", [])])),
        "calendario_calor": lambda: X.calendario_calor("05-01-2026", [0 if (i % 7) >= 5 else (i * 7 + i // 9) % 5 for i in range(182)], "Publicaciones del equipo"),
        "linea_tiempo_vertical": lambda: X.linea_tiempo_vertical([("2019", "Fundación", "Dos investigadoras de la Universidad Norte crean Beta Biotech."),
                                                                  ("2021", "Primera ronda", "1,5 M€ para la planta piloto de fermentación."),
                                                                  ("2024", "Primer cliente", "Acuerdo con un fabricante de **postres lácteos**."),
                                                                  ("2026", "Escala industrial", "Línea de 200 t al año en Países Bajos."),
                                                                  ("2027", "Entrada en bebidas", "Prueba con Cliente Demo, por confirmar.")], hoy=3, W=500),
        "proceso_carriles": lambda: X.proceso_carriles(["Cliente", "EA", "Proveedor"], [
            dict(id="i", carril=0, col=0, texto="Inicio", tipo="inicio"), dict(id="t1", carril=0, col=1, texto="Envía reto y criterios"),
            dict(id="t2", carril=1, col=2, texto="Busca y filtra opciones", destacado=True), dict(id="t3", carril=2, col=3, texto="Envía muestra y ficha"),
            dict(id="d", carril=1, col=4, texto="¿Cumple?", tipo="decision"), dict(id="t5", carril=0, col=5, texto="Ensaya en su planta"),
            dict(id="t6", carril=2, col=5, texto="Ajusta y reenvía"), dict(id="f", carril=0, col=6, texto="Decisión", tipo="fin")],
            [("i", "t1", ""), ("t1", "t2", ""), ("t2", "t3", ""), ("t3", "d", ""), ("d", "t5", "Sí"), ("d", "t6", "No"), ("t5", "f", "")], 7, caja=(122, 46)),
        "antes_despues_imagen": lambda: X.antes_despues_imagen(dict(imagen=None, rotulo="Antes", texto="Botella de 250 ml con **18 g** de azúcar por ración."),
                                                               dict(imagen=None, rotulo="Después", texto="Misma botella, **12 g** y sello de reducción en el frontal.")),
        "ficha_linea": lambda: X.ficha_linea([dict(nombre="Alfa Ingredientes", pais="Suiza", tipo="Proveedor", madurez=5, frase="Extracto de estevia de alta pureza con planta en Europa."),
                                              dict(nombre="Beta Biotech", pais="Países Bajos", tipo="Startup", madurez=3, frase="Proteína dulce por fermentación; **piloto con un lácteo** en 2026.", destacada=True),
                                              dict(nombre="Delta Foods", pais="España", tipo="Fabricante", madurez=4, frase="Fibras de fruta para textura en bebidas reducidas."),
                                              dict(nombre="Gamma Labs", pais="EE. UU.", tipo="Startup", madurez=2, frase="Enzimas que generan dulzor en la propia leche; sin registro UE.")]),
        "linea_periodos": lambda: X.linea(AN, [("Cliente Demo", [12, 13, 15, 18, 22, 27, 31]), ("Líder", [20, 22, 23, 25, 26, 27, 28])],
                                          periodos=[(2, 4, "Nuevo impuesto")], unidad=" %"),
        "columnas_cagr": lambda: X.columnas([("2022", 42), ("2023", 51), ("2024", 58), ("2025", 66), ("2026", 81), ("2027P", 92), ("2028P", 104)],
                                            destacado=4, unidad=" M€", prevision_desde=5, cagr=[(0, 4, "+18 % CAGR"), (4, 6, "+13 %")]),
        "cascada_evidencia": lambda: X.cascada(("Actual", 18), [("Edulcorante", -3.5), ("Fibra", -1.5), ("Enzima", -1.0), ("Ajuste\nsabor", 0.5)],
                                               "Objetivo", unidad=" g", H=300, evidencia=[None, "A", "B", "C", "B", None]),
        "barras_variacion": lambda: X.barras_variacion([("Alfa Ingredientes", 2.4), ("Beta Biotech", 1.6), ("Delta Foods", .8), ("Gamma Labs", -.4),
                                                        ("Sigma", -1.1), ("Kappa", -2.3)], unidad=" pp"),
        "barra_desglose": lambda: X.barra_desglose([("Materia prima", 48), ("Envase", 18), ("Energía", 12), ("Personal", 14), ("Otros", 8)], 0,
                                                   [("Leche", 30), ("Azúcar", 8), ("Edulcorante", 6), ("Otros", 4)], unidad=" cént.", rotulo_total="Coste por litro"),
        "dimensionamiento": lambda: X.dimensionamiento([("Bebidas lácteas UE", 4200), ("Con azúcar añadido", 2300), ("Segmento reducido", 1150),
                                                        ("Canal moderno", 610), ("Alcanzable 3 años", 85)], unidad=" M€"),
        "deslizadores": lambda: X.deslizadores([dict(grupo="Barreras de entrada", rotulo="Regulación", valor=.8, texto="Autorización de nuevo alimento: **2 a 3 años**."),
                                                dict(grupo="Barreras de entrada", rotulo="Capital", valor=.45, texto="Planta piloto alquilable."),
                                                dict(grupo="Barreras de entrada", rotulo="Acceso al canal", valor=.65, texto="4 cadenas concentran el 70 %."),
                                                dict(grupo="Riesgos", rotulo="Sabor residual", valor=.55, texto="Se corrige con enmascarantes."),
                                                dict(grupo="Riesgos", rotulo="Coste", valor=.3, texto="+1,2 céntimos por litro.")]),
        "benchmark_rango": lambda: X.benchmark_rango([dict(kpi="Crecimiento 3 años", propio=7.8, peor=2.6, mejor=27.7, mediana=9.5, unidad=" %"),
                                                      dict(kpi="Coste materia prima", propio=27.5, peor=35.9, mejor=14.9, mediana=24, unidad=" %"),
                                                      dict(kpi="Margen EBITDA", propio=28, peor=11.8, mejor=28, mediana=17, unidad=" %"),
                                                      dict(kpi="Ventas por empleado", propio=99, peor=45, mejor=297, mediana=120, unidad=" k€")]),
        "criterios_puntos": lambda: X.criterios_puntos([("Mantiene el dulzor", [4.5, 3.8, 3.2, 4.1, 2.9]), ("Coste por litro", [3.2, 4.4, 3.9, 2.8, 4.0]),
                                                        ("Etiqueta limpia", [4.0, 3.1, 4.4, 3.6, 2.5]), ("Autorizado en la UE", [5, 2, 5, 4, 3]),
                                                        ("Capacidad de suministro", [3.6, 4.2, 2.8, 3.3, 4.5])],
                                                       ["Alulosa", "Estevia", "Fibras", "Monk fruit", "Aromas"], "Alulosa"),
        "formula": lambda: X.formula([("4.200 M€", "Bebidas lácteas en la UE", "informe sectorial 2025"), ("27 %", "Parte reducida en azúcar", "panel de consumo"),
                                      ("54 %", "Canal moderno", "datos de distribución"), ("14 %", "Cuota alcanzable", "supuesto EA")],
                                     ("85 M€", "Mercado alcanzable", "cálculo EA")),
        "arbol_drivers": lambda: X.arbol_drivers(dict(rotulo="Ventas de la gama reducida", valor="31 M€", delta="+12 %", tono="bueno", op="×", hijos=[
            dict(rotulo="Volumen", valor="21 M litros", delta="+15 %", tono="bueno", op="×", hijos=[
                dict(rotulo="Puntos de venta", valor="8.400", delta="+6 %", tono="bueno"), dict(rotulo="Rotación por punto", valor="2.500 l", delta="+9 %", tono="bueno", destacado=True)]),
            dict(rotulo="Precio medio", valor="1,48 €/l", delta="−3 %", sube=False, tono="malo", op="−", hijos=[
                dict(rotulo="Precio de lista", valor="1,62 €/l", delta="0 %", sube=None), dict(rotulo="Promociones", valor="0,14 €/l", delta="+40 %", tono="malo")])])),
        "mapa_alcance": lambda: X.mapa_alcance([("Categoría", [("Bebidas lácteas", "dentro"), ("Yogur", "dentro"), ("Postres", "parcial"), ("Quesos", "fuera")]),
                                                ("Tecnología", [("Edulcorantes", "dentro"), ("Fibras", "dentro"), ("Enzimas", "parcial"), ("Fermentación", "parcial"), ("Envase", "fuera")]),
                                                ("Madurez", [("Comercial", "dentro"), ("Piloto", "dentro"), ("Laboratorio", "parcial"), ("Idea", "fuera")]),
                                                ("Región", [("Unión Europea", "dentro"), ("Reino Unido", "dentro"), ("EE. UU.", "parcial"), ("Asia", "fuera")])]),
        "dafo": lambda: X.dafo(["Panel sensorial propio", "Planta con capacidad libre"], ["Sin experiencia en edulcorantes", "Coste por litro alto"],
                               ["Nuevo perfil nutricional en 2027", "Cadenas piden reducidos"], ["Marca blanca más barata", "Alulosa sin autorizar en la UE"]),
        "cinco_fuerzas": lambda: X.cinco_fuerzas(dict(entrantes=(2, "Planta y canal frenan a startups"), proveedores=(3, "Pocos productores de alulosa"),
                                                      rivalidad=(3, "4 marcas y marca blanca"), clientes=(4, "Cadenas muy concentradas"), sustitutos=(2, "Bebidas vegetales"))),
        "pilares": lambda: X.pilares("Liderar los lácteos **reducidos en azúcar** en España en 2028",
                                     [("science", "Formulación", "Mezclas de edulcorante y fibra sin sabor residual."), ("factory", "Industrialización", "Piloto en planta y escala en 2027."),
                                      ("storefront", "Canal", "Lanzamiento con 2 cadenas y marca propia."), ("verified", "Regulación", "Claims validados y etiqueta clara.")],
                                     ["Panel sensorial", "Datos de consumo", "Alianzas con proveedores"]),
        "ficha_startup": lambda: X.ficha_startup(dict(datos=[("Localización", "Países Bajos"), ("Fundación", "2019"), ("TRL", "7"), ("Patentes", "Sí, 3 concedidas"), ("Web", "beta.example")],
                                                      bloques=[("Qué hace", "Proteínas dulces por fermentación de precisión para lácteos y bebidas."),
                                                               ("Oportunidad y ventaja", "Dulzor **2.000 veces** el del azúcar, sin sabor residual y con planta propia de 200 t al año."),
                                                               ("Modelo de negocio", "B2B: venta del ingrediente a fabricantes y licencias a escala."),
                                                               ("Clientes y tracción", "Piloto con un fabricante de postres lácteos; ==cifras por incluir==.")], destacado=1), H=330),
        "categorias_chips": lambda: X.categorias_chips([("Edulcorantes", ["Alfa", ("Beta", True), "Gamma", "Delta"]), ("Fibras", ["Omega", ("Sigma", True)]), ("Enzimas", ["Kappa", "Theta", "Zeta"]),
                                                        ("Aromas", ["Lambda"]), ("Proceso", ["Rho", "Tau"]), ("Envase", ["Psi"])]),
        "ficha_empresa": lambda: X.ficha_empresa(dict(nombre="Beta Biotech", frase="Proteínas dulces por fermentación de precisión para lácteos y bebidas.",
                                                      etiquetas=["Países Bajos", "Startup", "Serie A"], datos=[("Fundación", "2019"), ("Sede", "Delft"), ("Empleados", "38"),
                                                      ("Financiación", "14 M€")], ingresos=[("2023", .4), ("2024", 1.1), ("2025", 2.6), ("2026", 4.8)], unidad=" M€",
                                                      diferenciadores=["Dulzor **2.000 veces** el del azúcar, sin sabor residual", "Planta propia de 200 t al año",
                                                                       "Piloto con un fabricante de postres lácteos"],
                                                      cita=("Podemos sustituir hasta el 70 % del azúcar en bebidas sin cambiar el proceso.", "Directora técnica, entrevista del 12-09-2026"),
                                                      madurez=3, evidencia="B")),
        "tabla_drivers": lambda: X.tabla_drivers([dict(grupo="Volumen", driver="Demanda de reducidos", fuerza=4, texto="El 62 % de los hogares ya compra versiones reducidas.", impactos=[2, 2]),
                                                  dict(grupo="Volumen", driver="Nuevo perfil nutricional", fuerza=3, texto="Obliga a reformular desde 2027.", impactos=[0, 2]),
                                                  dict(grupo="Volumen", driver="Bebidas vegetales", fuerza=2, texto="Sustituto en el segmento joven.", impactos=[-1, -1]),
                                                  dict(grupo="Precio", driver="Coste de edulcorantes", fuerza=3, texto="La alulosa baja un 20 % al escalar.", impactos=[-2, 1]),
                                                  dict(grupo="Precio", driver="Presión de la marca blanca", fuerza=3, texto="Precio un 25 % inferior.", impactos=[-1, -2])]),
        "panel_entrevistas": lambda: X.panel_entrevistas([dict(perfil="Responsable de I+D", organizacion="Fabricante lácteo europeo", perspectiva="Cliente", pais="Francia", fecha="12-09-2026"),
                                                          dict(perfil="Directora técnica", organizacion="Beta Biotech", perspectiva="Proveedor", pais="Países Bajos", fecha="15-09-2026"),
                                                          dict(perfil="Comprador de categoría", organizacion="Cadena de supermercados", perspectiva="Cliente", pais="España", fecha="18-09-2026"),
                                                          dict(perfil="Investigador", organizacion="Centro tecnológico", perspectiva="Experto", pais="España", fecha="22-09-2026"),
                                                          dict(perfil="Product manager", organizacion="Alfa Ingredientes", perspectiva="Proveedor", pais="Suiza", fecha="25-09-2026")],
                                                         {"Cliente": "storefront", "Proveedor": "local_shipping", "Experto": "science"}),
    }.get(nombre)


# ================================================================== ejemplos de las piezas que venían de ea_visuals (caso ficticio de azúcar en lácteos)
def mono(txt, alto=22):
    """Monograma neutro en lugar de un logo real (la galería no usa marcas)."""
    return (f'<span style="flex:none;display:inline-flex;align-items:center;justify-content:center;height:{alto}px;padding:0 {alto * .35:.0f}px;'
            f'border-radius:{alto * .25:.0f}px;background:var(--fg1);color:#fff;font-size:{alto * .5:.0f}px;font-weight:700;letter-spacing:.04em">{E(txt)}</span>')


OPC = [("A01", "Edulcorantes vegetales", "Estevia, monk fruit y otros extractos de planta", True, 0),
       ("A02", "Azúcares raros", "Alulosa, tagatosa y otros azúcares de bajo aporte calórico", False, 0),
       ("A03", "Fibras solubles", "Inulina, polidextrosa y fibras de fruta", False, 0),
       ("A04", "Enzimas in situ", "Lactasa y otras enzimas que generan dulzor en la propia leche", False, 1),
       ("A05", "Fermentación de precisión", "Proteínas dulces producidas por fermentación", True, 1),
       ("A06", "Moduladores de sabor", "Aromas que refuerzan la percepción dulce", True, 2),
       ("A07", "Proceso", "Filtración, concentración y tratamiento térmico", True, 3),
       ("A08", "Envase y formato", "Ración, temperatura de consumo y envase", True, 3)]
CATS = ["Ingredientes", "Biotecnología", "Sabor", "Proceso y formato"]
DIMS = [("C1", "Dulzor"), ("C2", "Regulat."), ("C3", "Proceso"), ("C4", "Coste"), ("C5", "Libertad"),
        ("C6", "Actividad"), ("C7", "Madurez"), ("C8", "Vida útil"), ("C9", "Acceso")]
MATRIZ = {"A01": ("Media", "3A 2M 3A 3M 2B 3A 3A 2M 3A", 71), "A03": ("Alta", "2A 3A 2M 2A 3A 2M 3A 2M 2M", 66),
          "A02": ("Alta", "2M 1B 2A 1M 2M 2M 2A 2M 1B", 49), "A04": ("Media", "1M 2A 2M 2M 3A 1B 2M 2A 2M", 47),
          "A05": ("No", "3B NE 1B 0M 1B 2M 0A NE 1B", 38), "A06": ("Media", "1M 3A 3A 2M 2M 1B 2A 2M 1M", 45),
          "A07": ("Media", "1M 3A 1M 1M 3A 2M 3A 2M 2M", 64), "A08": ("Alta", "1A 3A 2M 3A 3A 1M 3A 2M 3A", 52)}
NOM = {c: n for c, n, *_ in OPC}


def notas(cod):
    return dict(zip([d for d, _ in DIMS], [(None, "NE") if t == "NE" else (int(t[0]), t[1:]) for t in MATRIZ[cod][1].split()]))


def caja(html_, w=None, h=None, extra=""):
    """Contenedor flex de ancho fijo para las piezas que en una slide se estiran (flex:1)."""
    st = (f"width:{w}px;" if w else "width:100%;") + (f"height:{h}px;" if h else "") + extra
    return f'<div style="display:flex;flex-direction:column;{st}">{html_}</div>'


pct1 = lambda x: X.fmt(round(x, 1))
CUENTA = [(0, "6", "otra", 3), (0, "6", "lacteo", 2), (0, "4-5", "lacteo", 4), (0, "1-3", "ninguna", 2), (1, "4-5", "otra", 3), (1, "1-3", "ninguna", 6),
          (1, "1-3", "otra", 2), (2, "4-5", "lacteo", 2), (2, "1-3", "otra", 3), (3, "6", "otra", 2), (3, "4-5", "otra", 4), (3, "1-3", "ninguna", 3),
          (0, "1-3", "otra", 4)]
ITEMS = [(f"T{k}{j}", cat, t, c) for k, (cat, t, c, n) in enumerate(CUENTA) for j in range(n)]
NT = {t: sum(1 for i in ITEMS if i[2] == t) for t in ("1-3", "4-5", "6")}


def ej2(nombre):
    duelo = lambda: X.barras_duelo(0, 20, (18, "18 g"), (12, "12 g"), X.base._fmt_simple, rotulos=("Actual", "Objetivo"), pie="gramos por ración, menos es mejor")
    kpi = [dict(numero="01", titulo="Dulzor percibido", medida="Panel sensorial, escala de 9 puntos", valor="7 o más",
                referencia="Referencia actual: 7,4", validacion="Panel de 40 consumidores en el centro sensorial del cliente",
                visual=X.barras_duelo(5, 9, (7.4, None), (7, "7 o más"), pct1, rotulos=("Actual", "Objetivo"), pie="escala desde 5")),
           dict(numero="02", titulo="Azúcar añadido", medida="Gramos por ración de 200 mL", valor="Menos de 12 g",
                referencia="Referencia actual: 18 g", validacion="Análisis en un laboratorio acreditado",
                visual=X.barras_duelo(0, 20, (18, "18 g"), (12, "menos de 12 g"), X.base._fmt_simple, rotulos=("Actual", "Objetivo"), pie="menos es mejor"))]
    kpi2 = [dict(numero="03", titulo="Operatividad en planta", valor="Sin cambios de línea", validacion="Prueba en la línea UHT del cliente",
                 visual=X.etiquetas_icono([("device_thermostat", "Estable a 140 °C"), ("speed", "Sin pérdida de velocidad")])),
            dict(numero="04", titulo="Coste del ingrediente", valor="Máximo 0,04 €", referencia="Objetivo: 0,02 a 0,03 € por ración",
                 validacion="Escandallo con el proveedor y condiciones de suministro",
                 visual=X.regleta_objetivo(0, 0.06, (0.02, 0.03), "objetivo", [(0.04, "Máximo 0,04")], [(0, "0"), (0.06, "0,06 €")]))]
    actores = [dict(nombre="Alfa Ingredientes", sub="Alemania · Proveedor", frase="Glucósido minoritario de estevia para lácteos; su ficha da dulzor igual al azúcar al 30% (dato del titular).", logo_html=mono("AI")),
               dict(nombre="Zeta Botanicals", sub="China · Proveedor", frase="Extracto de monk fruit al 50%, con claim de bajo regusto, sin ensayo en lácteo UHT.", logo_html=mono("ZB")),
               dict(nombre="Universidad Ejemplo", sub="Países Bajos · Universidad, codesarrollo", frase="Mezcla de estevia y fibra de cítrico en bebida de avena: 78% de aceptación (laboratorio).", logo_html=mono("UE"))]
    N = notas("A01")
    return {
        # cifras
        "contadores": lambda: caja(X.contadores([("3.100", "artículos científicos", "410 estudian justo el problema: reducir azúcar sin perder dulzor ni textura"),
                                                 ("85", "resoluciones del regulador", "todas las de 2010 a 2026 sobre edulcorantes en bebidas"),
                                                 ("18", "documentos del cliente", "más su registro de 40 ingredientes evaluados")]), 420),
        "tarjeta_cifra": lambda: caja(X.tarjeta_cifra("−30%", "", "", "de azúcar añadido exige la norma en 2028", apilada=True)
                                      + '<div style="height:12px"></div>'
                                      + X.tarjeta_cifra("+5 a +8", "puntos", "Lo que aporta la fibra", "La fibra soluble suma de 5 a 8 puntos de aceptación a cualquier edulcorante."), 480),
        "tarjeta_kpi": lambda: caja(X.tarjeta_kpi(**kpi[1], destacada=True), 560, 300),
        "panel_kpi": lambda: caja(X.panel_kpi(kpi, kpi2, "Deciden el Go o No-Go · prioridad 1, no negociables", "Requisitos para el ensayo · prioridad 2 y 3"), 1150, 480),
        "fila_parametros": lambda: caja(X.fila_parametros([("Tratamiento térmico", "UHT, 140 °C", ""), ("pH de trabajo", "6,6 a 6,8", ""), ("Vida útil", "9 meses", ""),
                                                           ("Viscosidad", "Menos de 30 cP", ""), ("Formato", "Brik de 1 L", "")]), 1150),
        # magnitud y comparación
        "embudo": lambda: f'<div style="width:420px">{X.embudo([("Documentos", "4 fuentes", "9.200"), ("Familias", "", "4.150"), ("Relevantes", "", "190"), ("Analizadas", "", "42")], clave=3)}</div>',
        "barras_duelo": lambda: X.barras_duelo(0, 20, (18, "18 g"), (12, "12 g"), X.base._fmt_simple, rotulos=("Actual", "Objetivo"), pie="gramos por ración, menos es mejor", W=360),
        "regleta_objetivo": lambda: X.regleta_objetivo(0, 0.06, (0.02, 0.03), "objetivo", [(0.04, "Máximo 0,04")], [(0, "0"), (0.06, "0,06 €")], W=360),
        "barras_objetivo": lambda: X.barras_objetivo([("Actual con azúcar", 78, "78%", "ref"), ("Estevia y fibra", 74, "74%", "mix"), ("Alulosa y aroma", 71, "71%", "mix"),
                                                      ("Monk fruit y fibra", 66, "66%", "mix"), ("Estevia sola", 58, "58%", "solo"), ("Alulosa sola", 55, "55%", "solo")],
                                                     (50, 86), (80, "Objetivo, 80%"), {"ref": X.FG1, "mix": X.HEAT[2], "solo": X.FG3}, (50, 60, 70, 80), W=540,
                                                     pie_eje="Aceptación del panel sensorial (eje desde 50%)", leyenda=[(X.HEAT[2], "Mezclas"), (X.FG3, "Un ingrediente")]),
        "escala_log": lambda: X.escala_log([("Estevia", 0.3, 1.8, "×0,7"), ("Fibras solubles", 0.4, 2.5, "×1"), ("Aromas moduladores", 1.2, 4, "×2,2"),
                                            ("Alulosa", 3, 8, "×4,9"), ("Enzima en línea", 6, None, "×6"), ("Monk fruit", 2.5, 15, "×6,1"),
                                            ("Filtración de membrana", 12, 40, "×22"), ("Proteína dulce", 20, 400, "×89")],
                                           referencia=(1, "1 vez el azúcar"), umbral=(10, "10 veces"),
                                           titulo_eje="Veces el coste del azúcar por ración (escala logarítmica)", rotulo_columna="Veces el azúcar, media"),
        # composición y distribución
        "anillo_categorias": lambda: X.anillo_categorias([(cat, [(c, n, d, m) for c, n, d, m, g in OPC if g == k]) for k, cat in enumerate(CATS)],
                                                         ("8", "opciones"), ("science", "No probado por el cliente"),
                                                         "Se dejan fuera los polioles, los jarabes y los edulcorantes artificiales: ya ensayados o vetados."),
        "mapa_madurez": lambda: X.mapa_madurez(ITEMS, [("1-3", (1, 3), "TRL 1 a 3", f"{NT['1-3']} tecnologías"), ("4-5", (4, 5), "TRL 4 a 5", f"{NT['4-5']} tecnologías"),
                                                       ("6", (6, 6), "TRL 6", f"{NT['6']} tecnologías")],
                                               [("lacteo", "Lácteo"), ("otra", "Otra bebida"), ("ninguna", "Ninguna")], CATS, W=570, x1=540),
        # marcos
        "nucleo_dos_lados": lambda: X.nucleo_dos_lados(
            {"codigo": "A07", "nombre": "Proceso: cómo se elabora", "titular": "Hasta −4 g de azúcar", "texto": "con ultrafiltración; hasta −2 g si ya se concentra",
             "color": X.HEAT[2], "filas": [("Ultrafiltración de la leche", "Retira lactosa antes de formular", "−3 a −4 g", "de azúcar", "suma"),
                                           ("Lactasa en línea", "Más dulzor con el mismo azúcar", "+8 %", "de dulzor", "suma"),
                                           ("UHT directo", "Menos caramelización", "0 %", "de dulzor", "cero"),
                                           ("Concentración por evaporación", "Sube la nota de cocido", "Resta", "", "resta")]},
            {"codigo": "A08", "nombre": "Formato: cuánto se toma", "titular": "La ración primero", "texto": "en dulzor, neutro o con un aporte leve",
             "color": X.HEAT[1], "filas": [("Ración de 200 mL", "Menos azúcar por toma", "−25 %", "por ración", "suma"),
                                           ("Aroma de vainilla", "Refuerza la percepción dulce", "+6 %", "de dulzor", "suma"),
                                           ("Servir más frío", "El dulzor se percibe menos", "−5 %", "de dulzor", "resta"),
                                           ("Envase opaco", "Protege el aroma 9 meses", "Sin efecto", "", "cero")]},
            ("Ingrediente", "A01 o A03: decide el resultado"),
            '<b style="color:var(--fg1)">Las capas no se suman.</b> El mismo proceso aporta mucho a una fórmula floja y casi nada a una buena.'),
        "escalera_prioridad": lambda: X.escalera_prioridad(
            [("Alta", [("A01, edulcorantes vegetales", "Fabricantes de extractos de estevia y monk fruit de bajo amargor"),
                       ("A03, fibras solubles", "Fabricantes de inulina y polidextrosa de baja viscosidad")]),
             ("Media", [("Palancas A07 y A08", "Fabricantes de membranas y de equipos de lactasa en línea"),
                        ("A02, con reservas", "Productores de alulosa con suministro estable en la región")]),
             ("Baja", [("A04 · Enzimas", "Una enzima que actúe a 4 °C"), ("A05 · Fermentación", "Un precio por kg publicado"),
                       ("A06 · Moduladores", "Un ensayo en lácteo")])], H=330),
        "columnas_evolucion": lambda: caja(X.columnas_evolucion([
            {"familia": "Fibras solubles", "antes": "Inulina de achicoria", "antes_dato": "3 productos; sube la viscosidad", "nuevo": "Fibra de cítrico",
             "pill": "TRL 5", "cifra": "−40%", "cifra_dato": "de viscosidad frente a la inulina a la misma dosis",
             "quien": [(mono("EF", 24), "Eta Fibres", "España", "Fibra de cítrico a escala piloto")], "reto": "Color y turbidez en bebidas claras."},
            {"familia": "Enzimas", "antes": "Lactasa estándar", "antes_dato": "Solo cubre el azúcar de la leche", "nuevo": "Lactasa activa en frío",
             "pill": "TRL 3", "cifra": "4 °C", "cifra_dato": "temperatura a la que mantiene el 80% de su actividad",
             "quien": [(None, "Proveedores de su agenda", "", "Su catálogo se revisa sin contactarlos")], "reto": "Sin autorización todavía en la región."},
            {"familia": "Proteínas", "antes": "Proteína láctea en polvo", "antes_dato": "Aporta cuerpo, no dulzor", "nuevo": "Proteína dulce fermentada",
             "pill": "TRL 2", "cifra": "×2.000", "cifra_dato": "el dulzor del azúcar, a igual peso (laboratorio)",
             "quien": [(mono("BB", 24), "Beta Biotech", "EE. UU.", "Proteína dulce en autorización")], "reto": "Nadie la fabrica aún a escala."}]), 1150),
        # árboles, cadena y secuencia
        "arbol_tramite": lambda: X.arbol_tramite("Ingrediente candidato", "¿Está en la lista positiva de aditivos?", ("Se ensaya directamente", "Ejemplo: inulina"),
                                                 [("Consulta al regulador", ""), ("Dossier", "ficha técnica, composición, estabilidad y justificación tecnológica"),
                                                  ("Autorización por uso y dosis", "")],
                                                 ("De 3 a 9 meses", "Caso de referencia: siete meses, cinco por completar el dossier"),
                                                 [("gavel", "La lista autorizada manda sobre el reglamento general y marca la dosis de cada categoría."),
                                                  ("policy", "Para extractos de planta se exige la pureza mínima del glucósido principal."),
                                                  ("warning", "Sin precedente para proteínas dulces ni para enzimas activas en el producto final.")],
                                                 "Lo que ya aplica el regulador"),
        "circuito_cadena": lambda: X.circuito_cadena(["Granja", "Recogida", "Quesería", "Formulación", "Envasado", "Retail"],
                                                     ["agriculture", "local_shipping", "factory", "science", "inventory_2", "storefront"], 2, 3,
                                                     {"logo_html": mono("DELTA", 44), "pill": "Delta Foods · sin patentes, know-how propio",
                                                      "texto": "Planta de secado propia · convierte el suero en un ingrediente dulce en polvo · dos autorizaciones del regulador"},
                                                     {"logo_html": mono("CLIENTE", 34), "texto": "Paga el ingrediente en dinero y no recibe el suero"},
                                                     '<b>Suero</b><br><span style="font-variant-numeric:normal;letter-spacing:0">(subproducto)</span>', "<b>Ingrediente</b>",
                                                     [("La quesería", "Aprovecha un residuo y cubre con él parte de la compra"),
                                                      ("Delta Foods", "Asegura su insumo y fideliza al comprador: quien cambia de proveedor debe recolocar el suero")],
                                                     titulo_cadena="Cadena láctea · planta del cliente"),
        "proceso_flechas": lambda: X.proceso_flechas([
            {"icono": "gavel", "nombre": "Filtro regulatorio", "pregunta": "¿Está autorizado o necesita una autorización previa?",
             "sale": "Si cada opción necesita permiso o no", "quien": "EA, opción por opción"},
            {"icono": "science", "nombre": "Ensayo comparativo", "pregunta": "¿Mejora la receta vigente según el indicador del cliente?",
             "sale": "Un resultado por opción, comparado con la receta base", "quien": "El cliente, en su laboratorio y con la muestra recibida"},
            {"icono": "fact_check", "nombre": "Decisión", "pregunta": "¿Sustituye todo el azúcar o una parte?",
             "sale": "Las opciones que siguen adelante", "quien": "El cliente decide y EA recomienda"},
            {"icono": "factory", "nombre": "Piloto en planta", "pregunta": "¿Llega a 7 de dulzor con menos de 12 g de azúcar?",
             "sale": "Seguir, ajustar o parar: la decisión final", "quien": "El cliente, con apoyo semanal del equipo"}],
            fases=[(0, 2, "Segunda fase, hasta decidir en abril"), (3, 3, "Fase 3")], destacado=2),
        "gantt": lambda: X.gantt("04-01-2027", 24,
                                 [{"rotulo": "Fase 1", "sub": "Set Up", "barras": [("04-01-2027", "26-02-2027", "lleno", "Final de la primera fase · febrero")]},
                                  {"rotulo": "Fase 2", "sub": "Scouting de soluciones", "barras": [("24-02-2027", "16-04-2027", "lleno", "Etapa 1 · scouting · 24-02 a 16-04")]},
                                  {"rotulo": "Fase 3", "sub": "Pilotos y PoC", "barras": [("19-04-2027", "07-05-2027", "lleno", "Kick-off"), ("10-05-2027", "21-05-2027", "pausa", "Pausa"),
                                                                                         ("24-05-2027", "18-06-2027", "lleno", "Ejecución del piloto")],
                                   "fechas": [("19-04-2027", "19-04", "inicio", 8), ("24-05-2027", "24-05"), ("18-06-2027", "~18-06", "fin", 0)]}],
                                 hoy=("10-02-2027", "Hoy · 10-02"),
                                 decision={"fecha": "16-04-2027", "titulo": "Decisión conjunta · 16-04", "texto": "¿Funciona? Si es que sí, tercera fase; si no, se revisa el alcance",
                                           "rotulo": "Decisión", "sub": "de continuidad"},
                                 leyenda=[("var(--red)", "Cronograma de referencia", False), ("var(--dark-cream)", "Pausa", True)]),
        "lista_precedentes": lambda: caja(X.lista_precedentes([("2011", "Glucósidos de estevia", "Autorizados", True), ("2014", "Ciclamato en bebidas", "No autorizado", False),
                                                               ("2017", "Inulina como fibra", "Favorable", True), ("2019", "Taumatina en lácteos", "Rechazada", False),
                                                               ("2022", "Alulosa", "En evaluación", False), ("2025", "Extracto de monk fruit", "Favorable", True)],
                                                              "Precedentes del regulador"), 360),
        # fichas
        "tarjeta_actor": lambda: f'<div style="background:var(--surface-fill);padding:12px;width:380px;display:flex">{X.tarjeta_actor("Alfa Ingredientes", "Suiza · Proveedor", "Extracto de estevia de **alta pureza** con planta en Europa.", mono("AI"))}</div>',
        "etiquetas_icono": lambda: f'<div style="width:300px">{X.etiquetas_icono([("device_thermostat", "Estable a 140 °C"), ("eco", "Origen vegetal"), ("verified", "Autorizado UE")])}</div>',
        "grupo_fichas": lambda: caja(X.grupo_fichas("Señales emergentes", [("biotech", "Proteína dulce", "Dulzor ×2.000 el del azúcar, estable a 90 °C", "EE. UU."),
                                                                           ("labs", "Alulosa enzimática", "Rendimiento de 38% desde fructosa", "Corea del Sur"),
                                                                           ("ac_unit", "Lactasa en frío", "Funciona en frío; falta probarla en línea", "Dinamarca"),
                                                                           ("eco", "Fibra de cítrico", "Textura sin viscosidad extra", "España")], True), 520),
        "ficha_hipotesis": lambda: caja(X.ficha_hipotesis(
            '<div style="font-size:13px;line-height:1.45;color:var(--fg1)"><b>Extracto de estevia estándar</b></div>'
            '<div style="font-size:12.5px;line-height:1.45;color:var(--fg1)">74% de aceptación al 30% de reducción</div>'
            '<div style="font-size:12.5px;line-height:1.45;color:var(--red);font-weight:600;margin-top:2px">Frenado por el regusto amargo</div>',
            '<div style="font-size:15px;font-weight:600;color:var(--fg1);line-height:1.35;text-wrap:balance">Glucósidos minoritarios de bajo amargor, monk fruit y mezclas con fibra</div>',
            [("water_drop", "Dulzor", "7,2 sobre 9", "Panel de un proveedor con glucósido minoritario al 0,02%", N["C1"]),
             ("factory", "Operatividad", "Estable", "Soporta UHT a 140 °C; a dosis altas puede espumar en el llenado", N["C3"]),
             ("gavel", "Regulación", "Autorizado", "En la lista positiva, con dosis máxima por categoría", N["C2"]),
             ("payments", "Coste", "×0,3 a ×1,8", "Frente al azúcar, por ración, según pureza del extracto", N["C4"])],
            actores,
            {"antes": "Lo que el cliente ya probó", "despues": "Lo que falta por ensayar", "criterios": "Frente a los criterios del cliente",
             "criterios_nota": "Puntuación sobre 3", "ejemplos": "Ejemplos que el cliente no tiene mapeados",
             "ejemplos_nota": "Sin contacto aún; ejemplos orientativos"}), 1150, 410),
        "tarjetas_salida": lambda: caja(X.tarjetas_salida([("Fase 3", "Alcance actual", True, "Si funciona: prueba industrial", "Acuerdo en primavera y prueba en la fábrica del cliente."),
                                                           ("Etapa 2", "Fuera del alcance actual", False, "Si no funciona: desarrollo conjunto", "Partiendo del listado inicial y con el acuerdo de ambas partes."),
                                                           ("Etapa 3", "Proyecto independiente", False, "Planta propia de ingrediente", "Caso de negocio e ingeniería, fuera de este proyecto.")]), 1150),
        # marcas
        "chip_nota": lambda: '<div style="display:flex;gap:8px">' + "".join(X.chip_nota(n) for n in ((0, "A"), (1, "M"), (2, "B"), (3, "A"), (None, "NE"))) + '</div>',
        "pill": lambda: '<div style="display:flex;gap:8px;flex-wrap:wrap">' + "".join(X.pill(t, k) for t, k in (("Prioridad", "red"), ("En curso", "rosa"), ("Neutral", "neutral"), ("Fase 2", "sand"), ("Fuera de alcance", "out"), ("Decisión", "burg"))) + '</div>',
        "icono_caja": lambda: '<div style="display:flex;gap:10px">' + "".join(X.icono_caja(i) for i in ("science", "factory", "gavel", "eco", "payments")) + '</div>',
        # tablas
        "tabla_referencia": lambda: caja(X.tabla_referencia(["Familia", "Qué se probó", "Mejor aceptación", "Por qué se paró"],
                                                            [{"celdas": ["Estevia", "6 extractos, 20 fórmulas", "**74%** (amargor residual)", "Regusto amargo por encima del 0,03%"], "valor": 74},
                                                             {"celdas": ["Alulosa", "2 proveedores, 8 fórmulas", "**71%**", "Precio y suministro inestables"], "valor": 71},
                                                             {"celdas": ["Fibras solubles", "Inulina y polidextrosa", "**79%**", "Sube la viscosidad por encima de 30 cP"], "valor": 79},
                                                             {"celdas": ["Proteínas dulces", "1 muestra de laboratorio", "Sin muestra estable", "Sin suministro industrial"], "valor": None}],
                                                            2, (50, 85), (80, "Objetivo 80%"), (78, "Actual 78%"),
                                                            nota="Además, fuera del registro: aromas moduladores, miel en polvo y concentrados de fruta."), 1150),
        "tabla_grafica": lambda: X.tabla_grafica([("A01", "Edulcorantes vegetales", 84, 72, 12), ("A02", "Azúcares raros", 41, 65, 9), ("A03", "Fibras solubles", 37, 88, 4),
                                                  ("A04", "Enzimas in situ", 22, 81, 5), ("A05", "Fermentación de precisión", 18, 56, 6), ("A06", "Moduladores de sabor", 29, 90, 3)],
                                                 ("Familias", "% libres", "Interés alto"), ("Libres", "No libres"),
                                                 "Titulares con más familias: cinco grupos de ingredientes y dos universidades.", H=300),
        "matriz_puntuacion": lambda: X.matriz_puntuacion([{"codigo": c, "nombre": NOM[c], "notas": notas(c), "extra": MATRIZ[c][0], "total": MATRIZ[c][2]} for c in MATRIZ],
                                                         DIMS, [("Buscar primero", ["A01", "A03"]), ("Explorar con reservas", ["A02"]), ("Vigilar", ["A04", "A05", "A06"]), ("Palanca", ["A07", "A08"])],
                                                         extra=("C0", "Novedad"), H=380),
        "scorecard": lambda: caja(X.scorecard([("Aplicación en lácteos", "bebida o postre lácteo."), ("Madurez alta (TRL 7+)", "ya ensayada en planta y con resultados medidos."),
                                               ("Estable en proceso", "a 140 °C y a pH neutro, sin precipitar."),
                                               ("Viabilidad regulatoria", "permitido hoy o con permiso previsto antes de un año.")],
                                              [("Ajuste al objetivo técnico", 30), ("Madurez tecnológica (TRL)", 20), ("Viabilidad de implementación", 15),
                                               ("Impacto en costes", 15), ("Perfil regulatorio", 10), ("Capacidad operativa", 5), ("Modelo de colaboración", 5)]), 1150),
        "tabla_vigilancia": lambda: caja(X.tabla_vigilancia(
            [{"codigo": "A02", "nombre": "Azúcares raros", "porque": "Coste de 3 a 8 veces el azúcar; suministro inestable", "disparador": "Un segundo productor en la región",
              "actores": [dict(nombre="Gamma Sweet", sub="Corea del Sur · Proveedor", frase="alulosa cristalina a escala industrial", logo_html=mono("GS", 20))]},
             {"codigo": "A04", "nombre": "Enzimas in situ", "porque": "Solo cubre el azúcar propio de la leche", "disparador": "Una enzima activa a 4 °C",
              "actores": [dict(nombre="Delta Enzymes", sub="Dinamarca · Proveedor", frase="lactasa de alta actividad", logo_html=mono("DE", 20))]},
             {"codigo": "A05", "nombre": "Fermentación de precisión", "porque": "Ningún proveedor con precio publicado", "disparador": "Un precio por kg y una autorización", "actores": []}],
            ("Opción", "Por qué se vigila", "Qué la haría subir"), "Ejemplos que el cliente no tiene mapeados", "ninguno contactado",
            vacio="Ninguno con dato en lácteo: es un hallazgo"), 1150),
        # síntesis
        "tarjetas_miniatura": lambda: caja(X.tarjetas_miniatura([
            (X.mini_barras_objetivo([("Estevia", 74), ("Alulosa", 71), ("Fibras", 79)], (60, 84), (78, "Actual 78%"), (80, "Objetivo 80%"), "Mejor resultado por familia", "eje desde 60%"),
             "Lo que ya se sabe", "Los ensayos internos y los estudios publicados apuntan a lo mismo: **hace falta combinar ingredientes**."),
            (X.mini_conteo(8, 5, "<b>8 opciones</b> de búsqueda", "sin ningún ensayo del cliente", "probadas"),
             "Lo que sigue abierto", "Quedan **vías sin ensayar** y proveedores por identificar."),
            (X.mini_iconos([("travel_explore", "Opciones"), ("science", "Validación técnica"), ("alt_route", "Plan del primer tramo")]),
             "Lo que validamos hoy", "Qué se prueba en la Fase 2, cómo se valida y cómo se organiza el primer tramo.")]), 1150),
        "mini_barras_objetivo": lambda: X.mini_barras_objetivo([("Estevia", 74), ("Alulosa", 71), ("Fibras", 79)], (60, 84), (78, "Actual 78%"), (80, "Objetivo 80%"), "Mejor resultado por familia", "eje desde 60%"),
        "mini_conteo": lambda: X.mini_conteo(8, 5, "<b>8 opciones</b> de búsqueda", "sin ensayo del cliente", "probadas"),
        "mini_iconos": lambda: X.mini_iconos([("travel_explore", "Opciones"), ("science", "Validación"), ("alt_route", "Plan")]),
        "mini_escalera": lambda: X.mini_escalera([("Alta", ["A01", "A03"]), ("Media", ["A07", "A08", "A02"]), ("Baja", ["A04", "A05"])]),
        "mini_flechas": lambda: X.mini_flechas(["Norma", "Ensayo", "Decisión", "Piloto"], "El cliente ensaya con su protocolo"),
        "mini_bifurcacion": lambda: X.mini_bifurcacion("Etapa 1", "Corte · 16-04-2027", "Si sí · Fase 3", "Si no · Etapa 2", "EA recomienda, el cliente decide"),
        # añadidos del 01-11-2026, con un caso inventado (lácteos con menos azúcar)
        "ranking_logos": lambda: X.ranking_logos([("ALFA", 8.4), ("BETA", 7.2), ("GAMMA", 6.1), ("DELTA", 5.5, "Incluye una planta en construcción"), ("ÉPSILON", 4.3),
                                                  ("Cliente Demo", 3.9)], destacado="Cliente Demo", W=380),
        "combo_financiero": lambda: X.combo_financiero(["2020", "2021", "2022", "2023", "2024"], [None, 38, 44, 47, 55],
                                                       [None, 6.1, 6.8, 5.9, 9.2], unidad="M€"),
        "score_dimensiones": lambda: X.score_dimensiones([("Receta", 7.5), ("Etiquetado", 9), ("Lineal", 7), ("Planta", 8.5),
                                                          ("Suministro", 6.5), ("Coste", 7)], referencia=[3, 4, 5, 3, 8, 6]),
        "mapa_actores": lambda: X.mapa_actores([
            dict(rotulo="Proveedores europeos", paises=["Alemania", "Países Bajos", "Suiza", "Bélgica", "Reino Unido"], punto=(8, 51), lado="der",
                 actores=["ALFA", "BETA", "GAMMA", "DELTA"]),
            dict(rotulo="Demanda: marcas lácteas", paises=["México", "Colombia", "Perú", "Chile", "Argentina"], punto=(-70, 2), lado="izq", destacado=True,
                 actores=["Cliente Demo", "OMEGA"]),
            dict(rotulo="Proveedores asiáticos", paises=["Japón", "China", "South Korea", "Malaysia"], punto=(125, 33), lado="der",
                 actores=["SIGMA", "KAPPA", "THETA"])], W=1150),
        "convergencia": lambda: X.convergencia([
            dict(icono="gavel", rotulo="Etiquetado", texto="«Lo que frena hoy es la **etiqueta**: qué se puede declarar y cómo.»",
                 detalle="Decir «sin azúcar añadido» exige cumplir **la norma de alegaciones**, y cada país la aplica a su modo."),
            dict(icono="factory", rotulo="Planta", texto="«La línea aguanta el cambio; lo que cuesta es **repetir el sabor** lote a lote.»",
                 detalle="La fábrica sirve como está, pero pide **ajustes de dosificación** y ensayos por referencia."),
            dict(icono="handshake", rotulo="Lineal", texto="«La cadena mira la **rotación**, no la receta.»",
                 detalle="Sin cifras de venta por tienda no se consigue más espacio en el lineal.")],
            ("payments", "Margen"), rotulos=("Voz del experto", "Implicación"), W=1150),
        "abanico_foco": lambda: X.abanico_foco(("4 frenos", "al cambio"), [
            ("El sabor manda", "El panel rechaza cualquier regusto, aunque el azúcar baje."),
            ("La etiqueta limita", "Las alegaciones admitidas cambian de un país a otro."),
            ("El coste sube", "Los edulcorantes naturales encarecen la ración **entre 1 y 3 céntimos**."),
            ("La línea no se toca", "La planta pide recetas que no alteren los tiempos de proceso.")], W=1150),
        "arbol_opciones": lambda: X.arbol_opciones([
            dict(rotulo="Ingrediente nuevo", opciones=[dict(titulo="Licenciar a una startup", texto="Acceso a una proteína dulce aún en desarrollo. **Exclusividad posible**, riesgo técnico alto.")]),
            dict(rotulo="Ingrediente probado", opciones=[dict(titulo="Comprar a un proveedor regional", texto="Extracto ya en el mercado: se adapta **la receta** y poco más."),
                                                         dict(titulo="Aliarse con un gran proveedor", texto="Suministro asegurado a cambio de **un volumen mínimo** anual.")])], W=1150),
        "cadena_margen": lambda: X.cadena_margen([
            dict(fase="Fase 1", nombre="Ganadería", icono="agriculture", margen=(2, 4), captura=3),
            dict(fase="Fase 2", nombre="Ingredientes", icono="science", margen=(18, 26), captura=9),
            dict(fase="Fase 2.5", nombre="Mezclas a medida", icono="experiment", margen=(10, 16), captura=6, hipotetico=True),
            dict(fase="Fase 3", nombre="Transformación", icono="precision_manufacturing", margen=(8, 12), captura=22),
            dict(fase="Fase 4", nombre="Retail", icono="storefront", margen=(20, 28), captura=31)],
            destacado=1, posicion=3, W=1150),
        "trayecto": lambda: X.trayecto([dict(etiqueta="Hoy", titulo="Lácteos de receta clásica", dato="Margen ~9 %", texto="Yogures y bebidas con azúcar: el **negocio actual**."),
                                        dict(etiqueta="Destino", titulo="Gama con menos azúcar", dato="Margen ~15 %", texto="La misma marca con un 30 % menos de azúcar."),
                                        dict(etiqueta="Vía de entrada", titulo="Alianza con un proveedor", dato="Probar antes de invertir", texto="Un piloto con un proveedor y decisión tras el panel.")], W=1150),
        "fases_gates": lambda: X.fases_gates([
            dict(nombre="Fase 1", plazo="Meses 0 a 2", titulo="Medir la aceptación", puntos=["Panel con 40 consumidores", "Comparar con la receta actual", "Si el panel rechaza, parar"], gate="Nota de 7 o más"),
            dict(nombre="Fase 2", plazo="Meses 2 a 4", titulo="Probar en línea", puntos=["Lote corto en planta", "Control de estabilidad", "Coste por ración"], gate="Lote sin incidencias"),
            dict(nombre="Fase 3", plazo="Antes de fin de año", titulo="Lanzar en una cadena", puntos=["Acuerdo con una cadena", "Etiquetado revisado", "Plan de reposición"], gate="Referencia en el lineal")], W=1150),
        "columna_contexto": lambda: caja(X.columna_contexto("Metodología", ["Se parte de la venta total de lácteos y se aplican **filtros sucesivos** hasta llegar al valor del ingrediente.",
                                                                            "Promedio de **tres estudios** de mercado."],
                                                            ("480 M€", "valor accesible en 2030")), 360, 330),
        "bloque": lambda: '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;width:540px">' + X.bloque("La brecha", "Los hogares piden **menos azúcar** y la oferta del lineal apenas cambia.") + X.bloque("La ventana", "El nuevo etiquetado entra en vigor en **dos años**.", filete="negro", fondo="gris") + '</div>',
        "columnas_numeradas": lambda: X.columnas_numeradas([
            dict(titulo="El hogar pide menos azúcar", texto="La mayoría de los hogares dice **mirar la etiqueta** antes de comprar.", icono="bar_chart", cifras=[("62 %", "hogares"), ("+12 %", "ventas de la gama")]),
            dict(titulo="Cambia la etiqueta", texto="La **norma nueva** obliga a declarar el azúcar añadido en el frontal.", icono="gavel", cifras=[("2 años", "para adaptarse"), ("3", "países afectados")]),
            dict(titulo="La distribución aprieta", texto="Dos cadenas ya piden **gama reducida** en sus condiciones de compra.", icono="groups", cifras=[("4", "cadenas interesadas"), ("31 %", "cuota objetivo")])], W=1150),
        "afirmacion_evidencia": lambda: X.afirmacion_evidencia([
            dict(afirmacion="La gama reducida crece **tres veces más** que la clásica.", cita="En el lineal ya no se discute si hacerlo, sino cuándo.", autor="Compras, cadena de supermercados"),
            dict(afirmacion="El sabor sigue siendo **el primer freno**.", cita="Se prueba una vez; si no gusta, no se repite.", autor="Consumo, marca láctea"),
            dict(afirmacion="La **receta se puede cambiar** sin tocar la línea.", cita="Con la dosis bien ajustada, la planta ni lo nota.", autor="Dirección de planta, fabricante lácteo")], W=1150),
        "columnas_requisitos": lambda: X.columnas_requisitos([
            dict(titulo="Receta", puntos=["Ingrediente **compatible** con UHT", ("Ajuste de dosis en laboratorio", True), ("Panel sensorial completo", True)], coste="0,2 a 0,4 M€", plazo="6 a 9 meses"),
            dict(titulo="Etiquetado", puntos=["Alegación **revisada** por asesoría", "Cambio de envase", "Registro en cada país"], coste="0,1 a 0,3 M€", plazo="3 a 6 meses"),
            dict(titulo="Planta", puntos=["Dosificador **nuevo**", "Pruebas de estabilidad"], coste="0,5 a 1 M€", plazo="9 a 12 meses")], W=1150),
        "tarjetas_escenario": lambda: X.tarjetas_escenario([
            dict(nombre="Escenario conservador", dato="Cuota 2 a 4 %", texto="Solo una cadena y lanzamiento por fases.", visual=X.columnas([("2030", 18), ("2032", 35)], unidad=" M€", W=220, H=130)),
            dict(nombre="Escenario base", dato="Cuota 5 a 8 %", texto="Dos cadenas y receta **ya validada**.", visual=X.columnas([("2030", 42), ("2032", 88)], destacado=1, unidad=" M€", W=220, H=130)),
            dict(nombre="Escenario optimista", dato="Cuota 9 a 13 %", texto="Todas las cadenas desde el primer año.", visual=X.columnas([("2030", 70), ("2032", 150)], unidad=" M€", W=220, H=130))],
            destacado=1, W=1150),
        "grupo_logos": lambda: '<div style="display:flex;gap:14px">' + X.grupo_logos(["ALFA", "BETA", "GAMMA", "DELTA"], "Competidores", W=250) + X.grupo_logos(["Cliente Demo", "OMEGA"], "Comparables", destacado=True, W=250) + '</div>',
        "matriz_portfolio": lambda: X.matriz_portfolio([("Bebidas", [("Alfa B1", "Estevia"), ("Alfa B2", "Fibra"), ("Alfa B3", "Alulosa"), "Alfa 44", "Alfa 48"]),
                                                        ("Postres", []), ("Yogures", [("Alfa Y1", "Enzima"), ("Alfa Y2", "Aroma")]), ("Otros", [("Alfa C1", "Cacao")])]),
    }.get(nombre)


# ================================================================== página
def doc(fn):
    d = " ".join((inspect.getdoc(getattr(X, fn)) or "").split())
    g = lambda pat: (re.search(pat, d) or [None, ""])[1].strip()
    return g(r"^(.*?)(?:Cuándo usarlo:|$)"), g(r"Cuándo usarlo:(.*?)(?:Cuándo no:|Origen:|$)"), g(r"Cuándo no:(.*?)(?:Origen:|$)")


NOMBRE_INT = {k: p for k, p, _ in TX.INTENCIONES}


def ejemplo(fn):
    f = ej(fn) or ej2(fn)
    if f is None:
        raise SystemExit(f"Falta el ejemplo de {fn} en build_galeria_elementos.py")
    return f()


def _marcas(nombres):
    """Logos inventados para los ejemplos: un símbolo y el nombre, en la rampa de rojos."""
    out = []
    for i, n in enumerate(nombres.split()):
        c = TX_RAMPA[i % len(TX_RAMPA)]
        forma = ('<circle cx="11" cy="12" r="8" fill="{c}"/>', '<rect x="3" y="4" width="16" height="16" rx="4" fill="{c}"/>',
                 '<path d="M11 3 L20 21 L2 21 Z" fill="{c}"/>')[i % 3].format(c=c)
        out.append(dict(nombre=n, logo_html=f'<svg width="{30 + 10 * len(n)}" height="24" viewBox="0 0 {30 + 10 * len(n)} 24">{forma}'
                                            f'<text x="25" y="17" style="font-family:Rubik;font-size:14px;font-weight:700;fill:#1E1E1E">{n}</text></svg>'))
    return out


def tarjeta(fn):
    base = BASE.get(fn, fn)
    fi = TX.FICHAS[base]
    _, si, no = doc(base)
    titulo = TITULOS_VARIANTE.get(fn, fi["titulo"])
    modulo = getattr(X, base).__module__.split(".")[-1]
    tags = f'<span class="tg esc">{ESCALA[fi["escala"]]}</span>'
    if X.llena(base):
        tags += '<span class="tg esc" title="Se le puede dar el alto de X.alto_cuerpo">acepta H</span>'
    if fn in REF:
        tags += f'<span class="tg ref" title="Patrón tomado de la referencia {REF[fn]} de catalogo/">de {REF[fn]}</span>'
    ints = "".join(f'<a class="it{" p" if k == 0 else ""}" href="#i-{i}">{E(NOMBRE_INT[i])}</a>' for k, i in enumerate(fi["intenciones"]))
    alts = " · ".join(f'<a href="#{a}">{E(TX.FICHAS[a]["titulo"])}</a>' for a in fi["alternativas"])
    pie = (f'<div class="gx-doc"><div class="gx-int">Responde a: {ints}</div>'
           + (f'<b>Cuándo usarlo:</b> {E(si)}' if si else "") + (f'<br><b>Cuándo no:</b> {E(no)}' if no else "")
           + (f'<div class="gx-alt"><b>Alternativas:</b> {alts}</div>' if alts else "") + '</div>')
    codigo = CODIGO_VARIANTE.get(fn, f"{fn}()")
    ancha = fi["escala"] == "L"
    return (f'<article class="gx{" ancha" if ancha else ""}" id="{fn}"><header><h3>{E(titulo)}</h3><code>{codigo}</code>'
            f'<span class="mod">{modulo}.py</span>{tags}</header><div class="gx-vis">{ejemplo(fn)}</div>{pie}</article>')


def indice_intenciones():
    filas = []
    for k, preg, desc in TX.INTENCIONES:
        cands = TX.buscar(k)
        prin = [c for c in cands if TX.FICHAS[c]["intenciones"][0] == k]
        sec = [c for c in cands if c not in prin]
        enl = lambda cs, cls: "".join(f'<a class="{cls}" href="#{c}">{E(TX.FICHAS[c]["titulo"])}</a>' for c in cs)
        filas.append(f'<div class="ii" id="i-{k}"><div class="ii-q"><b>{E(preg)}</b><span>{E(desc)}</span><code>buscar("{k}")</code></div>'
                     f'<div class="ii-c">{enl(prin, "c1")}{enl(sec, "c2")}</div></div>')
    return ('<section id="intenciones"><div class="fam"><b>00</b><h2>Elegir por intención</h2><p>Qué tiene que decir la slide y todas las '
            'piezas que lo dicen. En negro, las que lo tienen como intención principal; en gris, las que también sirven</p></div>'
            f'<div class="iis">{"".join(filas)}</div></section>')


def markdown():
    """Taxonomía legible para la IA y para Obsidian: por intención (para elegir) y por familia (para encontrar el código)."""
    L = ["---", "tags:", "  - recurso", "  - design-system", "  - presentaciones", "aliases:", "  - Menú de elementos visuales",
         "description: >-", "  Menú completo de ea_elementos generado desde taxonomia.py: qué elemento elegir para cada intención,",
         "  con su escala, sus datos y sus alternativas. No se edita a mano (lo regenera build_galeria_elementos.py).", "---", "",
         "# Taxonomía de elementos", "",
         f"> Generado por `build_galeria_elementos.py` desde `ea_elementos/taxonomia.py`. {len(TX.FICHAS)} elementos en {len(TX.FAMILIAS)} familias. "
         "Para verlos: «Galería de elementos.html» en esta carpeta. Para colocarlos en una slide: [[Reglas de uso de elementos]].", "",
         "## Cómo se usa", "",
         "1. Escribir en una frase lo que la slide tiene que decir y elegir su intención en la tabla de abajo.",
         "2. Leer **todas** las candidatas de esa intención (también las de la columna «también sirven»), no solo la primera que suene.",
         "3. Descartar con un motivo concreto (forma de los datos, escala, número de elementos). Barras, anillo y tabla son la última opción, no la primera.",
         "4. Comprobar «Cuándo no» en el docstring y mirar las alternativas antes de cerrar.", "",
         "Escala: **S** pieza para una tarjeta o una celda (hasta ~360 px), **M** media slide (400 a 640 px), **L** ancho de slide.", "",
         "## Por intención", ""]
    for k, preg, desc in TX.INTENCIONES:
        cands = TX.buscar(k)
        L += [f"### {preg} (`{k}`)", "", desc + ".", "", "| Elemento | Función | Escala | Datos | Alternativas |", "|---|---|---|---|---|"]
        for c in cands:
            f = TX.FICHAS[c]
            marca = "" if f["intenciones"][0] == k else " (también)"
            L.append(f"| {f['titulo']}{marca} | `{c}` | {f['escala']} | {f['datos']} | {', '.join(f'`{a}`' for a in f['alternativas'])} |")
        L.append("")
    L += ["## Por familia (dónde está el código)", ""]
    for m, fam, lema, els in TX.FAMILIAS:
        L += [f"### {fam} · `ea_elementos/{m}.py`", "", lema + ".", ""]
        for e in els:
            _, si, no = doc(e)
            L.append(f"- **`{e}`** ({TX.FICHAS[e]['titulo']}). {si}" + (f" *Cuándo no:* {no}" if no else ""))
        L.append("")
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


def construir():
    err = TX.comprobar(X)
    if err:
        raise SystemExit("La taxonomía no cuadra con el código:\n- " + "\n- ".join(err))
    secciones, indice = [indice_intenciones()], ['<a href="#intenciones"><b>00</b> Por intención <span>23</span></a>']
    n = 0
    for i, (m, fam, lema, fns) in enumerate(TX.FAMILIAS):
        lista = [k for fn in fns for k in [fn] + VARIANTES.get(fn, [])]
        cards = "".join(tarjeta(fn) for fn in lista)
        n += len(fns)
        ide = f"f{i + 1}"
        indice.append(f'<a href="#{ide}"><b>{i + 1:02d}</b> {E(fam)} <span>{len(fns)}</span></a>')
        secciones.append(f'<section id="{ide}"><div class="fam"><b>{i + 1:02d}</b><h2>{E(fam)}</h2><p>{E(lema)} · <code>{m}.py</code></p></div>'
                         f'{GUIA_FAMILIA.get(m, "")}<div class="grid">{cards}</div></section>')
    cab = (f'<div class="top"><img src="data:image/svg+xml;base64,{ea_deck._b64(ea_deck.ASSETS / "logo-wordmark.svg")}" alt="" class="wm">'
           f'<span class="eb">Terracotta · capa de presentaciones · presentaciones/ea_elementos</span>'
           f'<h1>Galería de <span class="hl-red">elementos visuales</span></h1>'
           f'<p class="lead"><b>{n} elementos</b> en {len(TX.FAMILIAS)} familias para montar el cuerpo de cualquier slide. Se elige <b>por intención</b> '
           f'(qué tiene que decir la slide), no por costumbre: el índice 00 da todas las candidatas para cada mensaje. Datos ficticios. Es el único catálogo de Terracotta: las tarjetas del panel y el índice de gráficos salen de estas mismas piezas. '
           f'Cada tarjeta da la función, su escala, cuándo usarla, cuándo no y sus alternativas. Cómo colocarlos en una slide: «Reglas de uso de elementos.md».</p>'
           f'<nav>{"".join(indice)}</nav>'
           f'<div class="reglas"><b>Reglas de color comunes</b> · una serie en gris con lo importante en rojo · categorías de una familia en la rampa '
           f'de rojos · nosotros frente a referencia en rojo y gris oscuro · verde solo para validaciones y piezas de estado · amarillo solo como punto de luz '
           f'y en el semáforo</div></div>')
    cuerpo = f'<main>{cab}{"".join(secciones)}<p class="fin">Generado con build_galeria_elementos.py</p></main>'
    css = X.CSS + X.fuente_iconos() + CSS_GAL
    page = ea_deck.documento("Galería de elementos", [cuerpo], css).replace('<div class="deck">', '<div>')
    OUT.write_text(page, encoding="utf-8")
    markdown()
    return n


def catalogo_iconos():
    """Página con todos los iconos del catálogo (iconos.py) por temas: icono, nombre y palabras clave."""
    secs, nav = [], []
    for i, (tema, desc, items) in enumerate(X.iconos.TEMAS):
        tiles = "".join(f'<div class="ic" data-k="{E(X.iconos._norm(n.replace("_", " ") + " " + n + " " + tema + " " + kw))}" data-n="{E(n)}" title="Copiar el nombre">'
                        f'<div class="ic-v">{X.icono(n, 30, X.FG1)}</div><code>{E(n)}</code><span>{E(kw)}</span></div>' for n, kw in items)
        secs.append(f'<section id="t{i + 1}" class="tema"><div class="fam"><b>{i + 1:02d}</b><h2>{E(tema)}</h2><p>{E(desc)} · {len(items)} iconos</p></div><div class="ics">{tiles}</div></section>')
        nav.append(f'<a href="#t{i + 1}"><b>{i + 1:02d}</b> {E(tema)} <span>{len(items)}</span></a>')
    cab = (f'<div class="top"><img src="data:image/svg+xml;base64,{ea_deck._b64(ea_deck.ASSETS / "logo-wordmark.svg")}" alt="" class="wm">'
           f'<span class="eb">Terracotta · capa de presentaciones · presentaciones/ea_elementos/iconos.py</span>'
           f'<h1>Catálogo de <span class="hl-red">iconos</span></h1>'
           f'<p class="lead"><b>{len(X.iconos.NOMBRES)} iconos</b> de Material Symbols Outlined a peso 300, una sola familia (N1), agrupados por tema '
           f'con palabras clave en español. Se usan con <code>icono("nombre")</code> o <code>icono_caja("nombre")</code>; un nombre fuera del catálogo da error '
           f'en vez de salir como texto. Para buscar: <code>buscar_icono("vaca")</code>. Para añadir uno: se busca en fonts.google.com/icons, se suma a '
           f'<code>iconos.py</code> con sus palabras clave y se vuelve a ejecutar <code>build_galeria_elementos.py</code>. Licencia Apache 2.0.</p>'
           f'<div class="buscador"><input id="q" type="search" placeholder="Buscar: pesca, regulación, fábrica, reloj, factory…" autocomplete="off">'
           f'<span id="cuenta">{len(X.iconos.NOMBRES)} iconos</span></div>'
           f'<nav>{"".join(nav)}</nav>'
           f'<div class="reglas"><b>Uso</b> · el icono tiene que significar algo (lupa para buscar, mazo para regulación) · mismo tamaño dentro de un grupo · '
           f'nunca emojis ni iconos de otra familia · nunca en la portada · no se mezclan con escenas isométricas en el mismo bloque (I3)</div></div>')
    cuerpo = (f'<main>{cab}{"".join(secs)}<p class="vacio" id="vacio">Ningún icono del catálogo coincide. Prueba en inglés o busca en fonts.google.com/icons '
              f'y añádelo a iconos.py.</p><p class="fin">Generado con build_galeria_elementos.py</p></main><div id="aviso"></div>{JS_ICONOS}')
    css = X.CSS + X.fuente_iconos() + CSS_GAL + CSS_ICONOS
    page = ea_deck.documento("Catálogo de iconos", [cuerpo], css).replace('<div class="deck">', '<div>')
    OUT_ICONOS.write_text(page, encoding="utf-8")
    nota_iconos()


def nota_iconos():
    """Nota de Obsidian con el catálogo de iconos, para buscarlo desde el entorno interno. No se edita a mano."""
    L = ["---", "tags:", "  - recurso", "  - design-system", "  - presentaciones", "aliases:", "  - Iconos de Terracotta", "  - Buscador de iconos",
         "description: >-", "  Catálogo de iconos de Terracotta (Material Symbols Outlined, peso 300) por temas, con su nombre y palabras clave",
         "  en español. Generado desde ea_elementos/iconos.py por build_galeria_elementos.py; no se edita a mano.", "---", "",
         "# Catálogo de iconos", "",
         f"> {len(X.iconos.NOMBRES)} iconos de una sola familia (la selección curada; si no hay uno apto, `buscar_completo()` busca en los ~3.900 de la familia: regla N2 de las reglas de uso). Versión visual con buscador: «Catálogo de iconos.html» en esta carpeta. "
         "En código: `icono(\"nombre\")` o `icono_caja(\"nombre\")`; un nombre fuera del catálogo da error. Para añadir uno: buscarlo en "
         "fonts.google.com/icons (estilo Outlined), sumarlo a `ea_elementos/iconos.py` con sus palabras clave y ejecutar `build_galeria_elementos.py`. "
         "Relacionado: [[Reglas de uso de elementos]], [[Taxonomía de elementos]].", ""]
    for tema, desc, items in X.iconos.TEMAS:
        L += [f"## {tema}", "", desc + ".", "", "| Icono | Palabras clave |", "|---|---|"]
        L += [f"| `{n}` | {kw} |" for n, kw in items]
        L.append("")
    OUT_ICONOS_MD.write_text("\n".join(L), encoding="utf-8")


JS_ICONOS = """<script>
(function(){
  var q=document.getElementById('q'), cuenta=document.getElementById('cuenta'), vacio=document.getElementById('vacio'), aviso=document.getElementById('aviso');
  var tiles=[].slice.call(document.querySelectorAll('.ic')), temas=[].slice.call(document.querySelectorAll('section.tema'));
  function norm(t){return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}
  function filtrar(){
    var pal=norm(q.value).split(/\\s+/).filter(Boolean), vistos={}, n=0;
    tiles.forEach(function(t){var ok=pal.every(function(p){return t.dataset.k.indexOf(p)>=0;}); t.style.display=ok?'':'none'; if(ok&&!vistos[t.dataset.n]){vistos[t.dataset.n]=1;n++;}});
    temas.forEach(function(s){s.style.display=[].some.call(s.querySelectorAll('.ic'),function(t){return t.style.display!=='none';})?'':'none';});
    cuenta.textContent=n+(n===1?' icono':' iconos'); vacio.style.display=n?'none':'block';
  }
  q.addEventListener('input',filtrar);
  tiles.forEach(function(t){t.addEventListener('click',function(){
    var nombre=t.dataset.n, hecho=function(){aviso.textContent='Copiado: '+nombre; aviso.className='on'; setTimeout(function(){aviso.className='';},1400);};
    try{navigator.clipboard.writeText(nombre).then(hecho,function(){aviso.textContent=nombre; aviso.className='on';});}catch(e){aviso.textContent=nombre; aviso.className='on';}
  });});
  try{var h=decodeURIComponent(location.hash.slice(1)); if(h&&h.indexOf('t')!==0){q.value=h; filtrar();}}catch(e){}
})();
</script>"""


CSS_ICONOS = """
.ics{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;}
.ic{background:#fff;border:1px solid var(--border-1);border-radius:12px;padding:12px 10px 10px;display:flex;flex-direction:column;align-items:center;gap:5px;text-align:center;min-width:0;}
.ic-v{height:34px;display:flex;align-items:center;}
.ic code{font-family:ui-monospace,Menlo,monospace;font-size:10.5px;color:var(--fg1);word-break:break-all;}
.ic span{font-size:10.5px;line-height:1.3;color:var(--fg3);}
.lead code{font-family:ui-monospace,Menlo,monospace;font-size:13px;background:var(--surface-fill);padding:1px 5px;border-radius:5px;}
.buscador{position:sticky;top:12px;z-index:5;display:flex;align-items:center;gap:14px;margin:0 0 16px;}
.buscador input{flex:1;font:inherit;font-size:16px;padding:12px 18px;border:1.5px solid var(--border-1);border-radius:999px;background:#fff;color:var(--fg1);outline:none;}
.buscador input:focus{border-color:var(--red);}
.buscador span{font-size:13px;color:var(--fg3);white-space:nowrap;}
.ic{cursor:pointer;transition:border-color .12s;} .ic:hover{border-color:var(--red);}
.vacio{display:none;text-align:center;color:var(--fg3);font-size:14px;margin:30px 0;}
#aviso{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);opacity:0;background:var(--fg1);color:#fff;font-size:13px;padding:9px 16px;border-radius:999px;transition:all .2s;pointer-events:none;}
#aviso.on{opacity:1;transform:translateX(-50%) translateY(0);}
"""


CSS_GAL = """
html,body{background:var(--light-grey);}
main{width:1240px;margin:0 auto;padding:48px 0 80px;}
.top{position:relative;background:#fff;border:1px solid var(--border-1);border-radius:20px;padding:36px 44px 30px;margin-bottom:40px;}
.top .wm{position:absolute;right:44px;top:34px;height:34px;}
.eb{font-size:13px;color:var(--fg3);}
h1{font-size:38px;font-weight:700;letter-spacing:-.02em;margin:8px 0 10px;color:var(--fg1);}
.hl-red{color:var(--red);}
.lead{font-size:16px;line-height:1.5;color:var(--fg2);max-width:900px;margin:0 0 20px;} .lead b{color:var(--fg1);}
nav{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px;}
nav a{display:inline-flex;gap:8px;align-items:center;text-decoration:none;font-size:13px;color:var(--fg1);background:var(--surface-fill);border-radius:999px;padding:7px 14px;}
nav a b{color:var(--red);} nav a span{color:var(--fg3);font-size:12px;}
.reglas{font-size:12.5px;color:var(--fg2);border-left:3px solid var(--red);background:var(--surface-fill);padding:10px 16px;line-height:1.5;}
.reglas b{color:var(--fg1);}
section{margin-bottom:46px;}
.fam{display:flex;align-items:baseline;gap:14px;border-bottom:1.5px solid var(--fg1);padding-bottom:10px;margin-bottom:18px;}
.fam b{font-size:28px;color:var(--red);font-weight:700;letter-spacing:-.02em;}
.fam h2{font-size:24px;margin:0;font-weight:700;color:var(--fg1);}
.fam p{margin:0 0 0 auto;font-size:13px;color:var(--fg3);max-width:520px;text-align:right;}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;}
.gx{background:#fff;border:1px solid var(--border-1);border-radius:16px;padding:18px 22px 16px;display:flex;flex-direction:column;min-width:0;}
.gx.ancha{grid-column:1 / -1;}
.gx header{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:16px;}
.gx h3{font-size:15.5px;margin:0;color:var(--fg1);font-weight:700;}
.gx code{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--fg2);background:var(--surface-fill);padding:2px 7px;border-radius:6px;}
.tg{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:3px 9px;}
.tg.esc{background:var(--surface-fill);color:var(--fg2);} .tg.ref{background:var(--brand-tint);color:var(--red);}
.tg.nuc{background:#fff;color:var(--fg3);box-shadow:inset 0 0 0 1px var(--input);}
.gx-vis{flex:1;display:flex;align-items:center;justify-content:center;padding:6px 0 14px;min-height:120px;}
.gx-doc{font-size:12px;line-height:1.5;color:var(--fg2);border-top:1px solid var(--border-2);padding-top:10px;}
.gx-doc b{color:var(--fg1);font-weight:600;}
.gx .mod{font-size:11px;color:var(--fg3);}
.gx-int{margin-bottom:6px;display:flex;flex-wrap:wrap;gap:5px;align-items:center;}
.gx-int a.it{font-size:11px;text-decoration:none;color:var(--fg2);background:var(--surface-fill);border-radius:999px;padding:2px 8px;}
.gx-int a.it.p{background:var(--fg1);color:#fff;}
.gx-alt{margin-top:6px;} .gx-alt a{color:var(--red);text-decoration:none;}
.fam p code{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;}
.iis{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.ii{background:#fff;border:1px solid var(--border-1);border-radius:14px;padding:12px 16px;display:flex;flex-direction:column;gap:8px;}
.ii-q b{display:block;font-size:14.5px;color:var(--fg1);} .ii-q span{font-size:12px;color:var(--fg3);}
.ii-q code{float:right;font-family:ui-monospace,Menlo,monospace;font-size:10.5px;color:var(--fg3);margin-top:-18px;}
.ii-c{display:flex;flex-wrap:wrap;gap:5px;}
.ii-c a{font-size:11.5px;text-decoration:none;border-radius:999px;padding:3px 9px;}
.ii-c a.c1{background:var(--fg1);color:#fff;} .ii-c a.c2{background:var(--surface-fill);color:var(--fg2);}
.fin{font-size:12px;color:var(--fg3);text-align:center;}
"""


def capturas(d):
    """Captura de página completa con Chrome headless, partida en trozos de 1600 px para revisarla."""
    from PIL import Image
    d = pathlib.Path(d); d.mkdir(parents=True, exist_ok=True)
    full = d / "galeria_full.png"
    from inspeccionar_dom import CHROME as chrome
    subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars", f"--screenshot={full}", "--window-size=1320,60000",
                    "--virtual-time-budget=20000", OUT.as_uri()], check=True, capture_output=True)
    im = Image.open(full).convert("RGB")
    px = im.load()
    fondo = px[5, im.height - 5]
    alto = im.height
    while alto > 100 and all(px[x, alto - 1] == fondo for x in range(0, im.width, 7)):
        alto -= 1
    for k, y in enumerate(range(0, alto, 1600)):
        im.crop((0, y, im.width, min(y + 1600, alto))).save(d / f"g{k + 1:02d}.png")
    print("Captura:", alto, "px,", (alto + 1599) // 1600, "trozos")


if __name__ == "__main__":
    k, kb = X.iconos.generar_fuente()
    print(f"Fuente de iconos: {k} iconos, {kb} KB")
    n = construir()
    catalogo_iconos()
    print("HTML:", OUT.name, n, "elementos,", OUT.stat().st_size // 1024, "KB ·", OUT_MD.name, "·", OUT_ICONOS.name)
    if "--png" in sys.argv:
        capturas(sys.argv[sys.argv.index("--png") + 1])
