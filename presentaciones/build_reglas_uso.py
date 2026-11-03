#!/usr/bin/env python3
"""Ejemplos aplicados de «Reglas de uso de elementos.md»: una slide por rejilla tipo (A a F), una ficha de actor en
cuadrantes y dos usos de la ilustración isométrica, montadas solo con ea_deck y ea_elementos y con datos ficticios. Bajo cada slide, solo
en pantalla, la rejilla, los elementos y las reglas que aplica. No es un catálogo de composiciones: el mismo
mensaje con otros datos puede pedir otra rejilla.

Ejecutar: python3 build_reglas_uso.py [--pdf] [--png DIR]
"""
import html, pathlib, subprocess, sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import ea_deck                  # noqa: E402
import ea_elementos as X        # noqa: E402

E = html.escape
OUT = AQUI / "Reglas de uso de elementos.html"
FUENTE = "Datos ficticios de ejemplo"
SLIDES = []      # (cuerpo, rejilla, elementos, reglas)


def nueva(eyebrow, titulo, sub, visual, rejilla, elementos, reglas, banda=None, estilo_vis="", rotulo_banda=None):
    SLIDES.append((ea_deck.cabecera(eyebrow, titulo) + X.cuerpo_slide(sub, visual, banda, estilo_vis, rotulo_banda=rotulo_banda), rejilla, elementos, reglas))


AN = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
ALTO = X.alto_cuerpo(1, True, 1)     # título de una línea, subtítulo y banda de una línea: M11, el cuerpo llena la slide

# ---------------------------------------------------------------- A · pieza a todo ancho
nueva("01. Mercado", 'Las ventas crecen por <span class="hl-red">rotación</span>, no por precio',
      "De qué depende el resultado de la gama reducida en azúcar, 2026 frente a 2025",
      X.arbol_drivers(dict(rotulo="Ventas de la gama reducida", valor="31 M€", delta="+12 %", tono="bueno", op="×", hijos=[
          dict(rotulo="Volumen", valor="21 M litros", delta="+15 %", tono="bueno", op="×", hijos=[
              dict(rotulo="Puntos de venta", valor="8.400", delta="+6 %", tono="bueno"),
              dict(rotulo="Rotación por punto", valor="2.500 l", delta="+9 %", tono="bueno", destacado=True)]),
          dict(rotulo="Precio medio", valor="1,48 €/l", delta="−3 %", sube=False, tono="malo", op="−", hijos=[
              dict(rotulo="Precio de lista", valor="1,62 €/l", delta="0 %", sube=None),
              dict(rotulo="Promociones", valor="0,14 €/l", delta="+40 %", tono="malo")])]), W=1152, bw=240, bh=(ALTO - 54) // 4, sep=18),
      "A · 1152", ["arbol_drivers"], ["S1", "M1", "M2", "M11", "K1", "K2", "E6"],
      banda="La palanca es **la rotación en el punto de venta**: subir precio frenaría justo lo que está funcionando.")

# ---------------------------------------------------------------- B · pieza y lectura
lectura = X.columna(
    X.tarjeta_cifra("−5,5 g", "por ración", "Lo que suman las tres palancas", "Edulcorante, fibra y enzima bajan de 18 a 12,5 g sin tocar la línea UHT."),
    X.tarjeta_cifra("+0,5 g", "ajuste", "El sabor cuesta medio gramo", "El ajuste de sabor devuelve azúcar: es el precio de mantener la aceptación."),
    X.tarjeta_cifra("0,5 g", "por encima", "Falta muy poco", "Para llegar a 12 g basta optimizar la dosis de fibra en el piloto."), repartir=True)
nueva("02. Formulación", 'Tres palancas llevan la ración a <span class="hl-red">12,5 g</span>, casi el objetivo',
      "Gramos de azúcar por ración de 200 mL, de la fórmula actual al objetivo de 12 g",
      X.fila(X.cascada(("Actual", 18), [("Edulcorante", -3.5), ("Fibra", -1.5), ("Enzima", -1.0), ("Ajuste\nsabor", 0.5)], "Objetivo",
                       unidad=" g", W=680, H=ALTO), lectura, anchos=X.REJILLAS["B"], crecer=True),
      "B · 680 + 444", ["cascada", "tarjeta_cifra ×3", "fila", "columna"], ["S3", "M2", "M3", "A1", "M11", "K2"],
      banda="El objetivo está al alcance **sin cambiar la línea**: el piloto solo tiene que afinar la dosis de fibra.")

# ---------------------------------------------------------------- C · dos hermanas
nueva("01. Mercado", 'El mercado crece y el <span class="hl-red">discount</span> gana peso en todos los países',
      "Ventas de lácteos reducidos en azúcar y reparto por canal",
      X.fila(X.rotulo_bloque("Ventas en Europa, millones de euros") +
             X.columnas([("2022", 42), ("2023", 51), ("2024", 58), ("2025", 66), ("2026", 81)], destacado=4, unidad=" M€", W=562, H=ALTO - 34),
             X.rotulo_bloque("Reparto por canal, 2026") +
             X.barras_apiladas(["España", "Portugal", "Francia", "Italia"],
                               [("Súper", [52, 48, 41, 45]), ("Discount", [28, 30, 22, 25]), ("Online", [12, 9, 21, 14]), ("Otros", [8, 13, 16, 16])], W=562, alto=58, sep=30),
             anchos=X.REJILLAS["C"], vertical="flex-start"),
      "C · 562 + 562", ["columnas", "barras_apiladas", "rotulo_bloque"], ["M2", "C7", "A1", "M11", "K1"],
      banda="Crecer en reducidos pasa por **negociar con el discount**, no solo con el súper.")

# ---------------------------------------------------------------- D · cifras y pieza
cifras = X.fila(X.cifra_delta("31 %", "Cuota en reducidos", "+4 pp", "vs 2025", [18, 20, 22, 24, 27, 31], W=270),
                X.cifra_delta("12,5 g", "Azúcar por ración", "−5,5 g", "vs actual", [18, 17, 16, 15, 13.5, 12.5], sube=False, tono="bueno", W=270),
                X.cifra_delta("74 %", "Aceptación del panel", "−4 pp", "vs fórmula actual", [78, 78, 77, 76, 75, 74], sube=False, tono="malo", W=270),
                X.cifra_delta("4", "Cadenas que lo piden", "+2", "vs 2025", [1, 1, 2, 2, 3, 4], W=270), gap=24)
nueva("03. Seguimiento", 'La cuota sube <span class="hl-red">cuatro puntos</span> y adelanta a la marca blanca',
      "Indicadores del trimestre y evolución de la cuota en lácteos reducidos en azúcar",
      X.columna(cifras, X.linea(AN, [("Cliente Demo", [12, 13, 15, 18, 22, 27, 31]), ("Líder", [20, 22, 23, 25, 26, 27, 28]),
                                     ("Marca blanca", [8, 9, 11, 12, 13, 15, 16])], anotaciones=[(0, 3, "Lanzamiento 0 %")], unidad=" %", W=1152, H=ALTO - 176),
                gap=18),
      "D · fila de 4 cifras + 1152", ["cifra_delta ×4", "linea", "columna"], ["M1", "M2", "M11", "K2", "K3"],
      banda="El único indicador en rojo es **la aceptación**: es lo que tiene que resolver el piloto.")

# ---------------------------------------------------------------- E · tres columnas hermanas
def opcion(nombre, sub, parte, pesos, centro, texto):
    return X.columna(X.rotulo_bloque(nombre, rojo=parte == 0) + f'<div style="font-size:13px;color:var(--fg3);margin:-14px 0 4px">{E(sub)}</div>',
                     X.donut(list(zip(("Coste", "Dulzor", "Textura"), pesos)), centro=centro, destacado=parte, W=365, D=222, grosor=34),
                     f'<div style="font-size:15px;line-height:1.45;color:var(--fg2)">{X.md(texto)}</div>', gap=10, repartir=True)


nueva("02. Formulación", 'Cada vía pesa por un motivo distinto: <span class="hl-red">la estevia, por coste</span>',
      "Peso de cada criterio en la nota final de las tres vías candidatas",
      X.fila(opcion("Estevia y fibra", "Edulcorante vegetal", 0, (45, 30, 25), ("45 %", "pesa el coste"), "La más barata por ración: **×0,7 el azúcar**. El sabor residual se corrige con aroma, sin coste añadido en la línea."),
             opcion("Alulosa y aroma", "Azúcar raro", 1, (20, 50, 30), ("50 %", "pesa el dulzor"), "El perfil más parecido al azúcar, con suministro inestable: **dos proveedores** en Europa y plazos de hasta 16 semanas."),
             opcion("Fibra y enzima", "Proceso", 2, (25, 20, 55), ("55 %", "pesa la textura"), "Mejora la textura, pero sola no llega al dulzor: **sirve de complemento** de cualquiera de las otras dos vías."),
             anchos=X.REJILLAS["E"], vertical="flex-start"),
      "E · 365 × 3", ["donut ×3", "rotulo_bloque", "fila", "columna"], ["M2", "M3", "C7", "M11", "S4", "K1"],
      banda="Ninguna vía gana en todo: **la estevia se elige por coste**, y la textura la aporta la fibra.")

# ---------------------------------------------------------------- isométrica: apertura con la cadena
nueva("01. Contexto", 'El valor se concentra en <span class="hl-red">ingredientes</span> y en el lineal',
      "Cadena de los lácteos reducidos en azúcar, del campo al consumidor",
      X.columna(X.cadena_isometrica([
          dict(nombre="Materia prima", tipo="granja", texto="Leche cruda y azúcar de cooperativas.", dato="Margen ~5 %"),
          dict(nombre="Ingredientes", tipo="ingredientes", texto="Edulcorantes, fibras y aromas para **reducir azúcar**.", dato="Margen ~32 %"),
          dict(nombre="Transformación", tipo="fabrica", texto="Formulación, UHT y envasado.", dato="Margen ~14 %"),
          dict(nombre="Distribución", tipo="logistica", texto="Logística refrigerada hasta tienda.", dato="Margen ~6 %"),
          dict(nombre="Retail", tipo="retail", texto="Lineal, promoción y marca blanca.", dato="Margen ~28 %"),
          dict(nombre="Consumidor", tipo="consumidor", texto="Familias que buscan menos azúcar.", dato="62 % de hogares")], destacado=1, W=1152),
          X.fila(X.contadores([("~32 %", "Margen en ingredientes", "El mayor de la cadena")]), X.contadores([("~28 %", "Margen en retail", "Por lineal y marca blanca")]),
                 anchos=X.REJILLAS["C"]),
          repartir=True),
      "A · 1152 con la cadena", ["cadena_isometrica"], ["I1", "I3", "I4", "I5", "I7", "M11", "K1"],
      banda="El proyecto actúa en el eslabón **que más margen captura**: por eso el ingrediente decide el caso.")

# ---------------------------------------------------------------- isométrica: ficha de actor
def ficha_actor(tipo, nombre, sub, frase, datos, nivel, rojo=False):
    cab = (f'<div style="display:flex;gap:16px;align-items:center;height:165px">{X.escena_iso(tipo, rojo, W=230)}'
           f'<div>{X.tarjeta_actor(nombre, sub, frase)}</div></div>')
    return X.columna(cab, X.icono_dato(datos, W=562), X.etiqueta_evidencia(nivel, "Fuente: web del titular y entrevista"), gap=22, repartir=True)


nueva("04. Candidatos", 'Dos perfiles opuestos: <span class="hl-red">planta propia</span> frente a red de socios',
      "Los dos candidatos de la lista corta, por el tipo de instalación con la que producen",
      X.fila(ficha_actor("fermentacion", "Beta Biotech", "Países Bajos · Startup", "Proteína dulce por fermentación de precisión, con **planta propia** de 20 m³.",
                         [("factory", "20 m³", "de capacidad de fermentación propia"), ("verified", "TRL 6", "piloto con un fabricante lácteo")], "B", rojo=True),
             ficha_actor("oficina", "Alfa Ingredientes", "Suiza · Proveedor", "Extracto de estevia fabricado **por terceros** en tres países.",
                         [("handshake", "3", "fabricantes asociados en Europa y Asia"), ("payments", "×0,7", "el coste del azúcar por ración")], "A"),
             anchos=X.REJILLAS["C"], vertical="flex-start"),
      "C · 562 + 562 con escena en la ficha", ["escena_iso", "tarjeta_actor", "icono_dato", "etiqueta_evidencia"], ["I1", "I4", "I5", "I6", "M2", "A1", "M11"],
      banda="Con planta propia, **el riesgo es de escala**; con socios, de control de la calidad.")


# ---------------------------------------------------------------- F · contexto y pieza
nueva("01. Mercado", 'El mercado accesible para el cliente supera los <span class="hl-red">450 M€ en 2030</span>',
      "De la venta total de lácteos al valor que captura el ingrediente en Europa",
      X.fila(X.columna(X.columna_contexto("Metodología", ["Se parte de la venta total de lácteos y se aplican **filtros sucesivos** hasta llegar al valor del ingrediente.",
                                                          "Las cifras de partida promedian **tres fuentes** de mercado, para no depender de una sola."],
                                          ("480 M€", "valor accesible en 2030")),
                       X.columna_contexto("Qué no incluye", ["Solo bebidas y yogures: **los postres quedan fuera**, porque usan otro tipo de ingrediente.",
                                                             "Tampoco Asia: el cliente solo vende en el mercado europeo."]), repartir=True),
             X.dimensionamiento([("Venta total de lácteos", 42000), ("Bebidas y yogures", 12600), ("Gama con menos azúcar", 5200),
                                 ("Valor del ingrediente", 640), ("Accesible en Europa", 480)], unidad=" M€", W=764, H=ALTO),
             anchos=X.REJILLAS["F"], crecer=True),
      "F · 360 + 764", ["columna_contexto", "dimensionamiento", "fila"], ["M2", "E6", "M11", "K2"],
      banda="El total se valida por otra vía: la categoría de ingredientes valió **900 M€ en 2025**.", rotulo_banda="Validación")

# ---------------------------------------------------------------- C en dos filas · ficha de actor en cuadrantes
ficha = X.columna(
    X.fila(X.rotulo_bloque("Descripción") + X.bloque("Empresa familiar europea, unos 600 empleados",
                                                     "Especialista en edulcorantes de origen vegetal para lácteos. Planta nueva en Portugal desde 2023: **el competidor más directo** del cliente. Vende sobre todo a marcas de bebidas y yogures, sin presencia en postres, y suma dos ampliaciones de capacidad en tres años.",
                                                     filete=None, fondo="gris"),
           X.rotulo_bloque("Mapa de portfolio") + X.matriz_portfolio([("Bebidas", [("Alfa B1", "Estevia"), ("Alfa B2", "Fibra"), ("Alfa B3", "Alulosa"), "Alfa 48", "Alfa 50"]),
                                                                      ("Postres", []), ("Yogures", [("Alfa Y1", "Enzima"), ("Alfa Y2", "Aroma")])], W=562),
           anchos=X.REJILLAS["C"], vertical="flex-start"),
    X.fila(X.rotulo_bloque("Métricas financieras, M€") + X.combo_financiero(["2020", "2021", "2022", "2023", "2024"], [32, 37, 44, 49, 58],
                                                                         [5.2, 5.9, 7.1, None, 10.4], W=562, H=272),
           X.rotulo_bloque("Score de capacidad para entrar") + X.score_dimensiones([("Receta", 8), ("Etiquetado", 9), ("Lineal", 8.5),
                                                                                   ("Planta", 6), ("Suministro", 8), ("Coste", 8.5)],
                                                                                  W=562),
           anchos=X.REJILLAS["C"], vertical="flex-start"), gap=20)
nueva("02. Competidores", 'Perfil del competidor: <span class="hl-red">Alfa Dulzor</span>, el más directo',
      "Ficha hermana: el mismo orden, los mismos ejes y la misma escala para los diez competidores",
      ficha, "C en dos filas · ficha en cuadrantes", ["bloque", "matriz_portfolio", "combo_financiero", "score_dimensiones", "rotulo_bloque"], ["M10", "C7", "M9", "A5"])


# ---------------------------------------------------------------- página
def franja(n, rejilla, elementos, reglas):
    return (f'<div class="rv"><div class="rv-n">{n:02d}</div><div><b>Rejilla:</b> {E(rejilla)} · <b>Elementos:</b> '
            + ", ".join(f"<code>{E(e)}</code>" for e in elementos)
            + f' · <b>Reglas:</b> {" · ".join(reglas)}</div></div>')


def slide(cuerpo, n, total):
    return (f'<section class="slide"><div class="slide-inner"><div class="slide-body">{cuerpo}</div>'
            f'<div class="slide-foot"><span><b>Fuente: {E(FUENTE)}</b></span>'
            f'<span>Reglas de uso de elementos · Uso interno · <b>{n} / {total}</b></span></div></div></section>')


CSS_R = """
h2.t{text-wrap:balance;}
.rv{width:1280px;margin:-20px auto 44px;display:flex;gap:18px;background:#fff;border-left:3px solid var(--red);padding:12px 18px;
font-size:13px;line-height:1.5;color:var(--fg2);box-shadow:var(--shadow-sm);}
.rv-n{flex:none;width:30px;font-size:15px;font-weight:700;color:var(--red);}
.rv b{color:var(--fg1);font-weight:600;} .rv code{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--fg1);}
@media print{.rv{display:none;}}
"""


def construir():
    total = len(SLIDES)
    out = []
    for i, (cuerpo, rej, els, regs) in enumerate(SLIDES):
        out += [slide(cuerpo, i + 1, total), franja(i + 1, rej, els, regs)]
    OUT.write_text(ea_deck.documento("Reglas de uso de elementos", out, X.CSS + X.fuente_iconos() + CSS_R), encoding="utf-8")
    return total


def pdf(n, png_dir=None):
    from inspeccionar_dom import CHROME as chrome
    out = OUT.with_suffix(".pdf")
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox", f"--print-to-pdf={out}",
                    "--print-to-pdf-no-header-footer", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    "--run-all-compositor-stages-before-draw", OUT.as_uri()], check=True, capture_output=True)
    import pypdf, fitz
    pags = len(pypdf.PdfReader(str(out)).pages)
    print(f"PDF: {pags} páginas (esperadas {n})", "OK" if pags == n else "ERROR")
    if png_dir:
        d = pathlib.Path(png_dir); d.mkdir(parents=True, exist_ok=True)
        for i, p in enumerate(fitz.open(str(out))):
            p.get_pixmap(dpi=110).save(str(d / f"p{i + 1:02d}.png"))


if __name__ == "__main__":
    n = construir()
    print("HTML:", OUT.name, n, "slides", OUT.stat().st_size // 1024, "KB")
    if "--pdf" in sys.argv:
        pdf(n, sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None)
