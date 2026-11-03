#!/usr/bin/env python3
"""Laboratorio de variantes: cuando una slide admite varias soluciones razonables y la elección es de gusto, se enseñan
opciones con los mismos datos y quien encarga el deck elige. Nunca dentro del deck de producción.

generar(titulo, variantes, salida): una slide por variante, rotuladas A, B, C..., con qué gana y qué pierde cada una.
opciones_cadena(eslabones, ...): las variantes de una cadena de valor a partir de un solo juego de datos.

Prueba: python3 laboratorio.py cadena <salida.html>   (con datos inventados)
"""
import pathlib, subprocess, sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import ea_deck                  # noqa: E402
import ea_elementos as X        # noqa: E402
from inspeccionar_dom import CHROME  # noqa: E402

# Qué pregunta responde cada cadena de valor. La guía de «Formatos de slide.md» y de la galería dice lo mismo.
GUIA_CADENA = [
    ("cadena_isometrica", "Presentar el sector de un vistazo", "Peso visual: se entiende sin leer y abre bien un informe", "Solo admite un dato por eslabón; no analiza"),
    ("cadena_capas", "Decir dónde está el valor y dónde entrar", "Análisis completo por eslabón: actores, margen, tendencia y oportunidad", "Densa; necesita datos de todas las filas"),
    ("cadena_margen", "Enseñar quién captura el margen y dónde está el cliente", "La cifra manda y la posición del cliente se ve al momento", "No dice quién opera en cada eslabón ni hacia dónde va"),
    ("circuito_cadena", "Explicar por qué un actor gana con un modelo circular o de dependencia", "Enseña el mecanismo: lo que sale y lo que vuelve", "Necesita un actor que se engancha; no sirve para describir un sector"),
]


def opciones_cadena(eslabones, destacado=None, posicion=None, circuito=None, W=1150):
    """Las opciones de cadena de valor que se pueden montar con estos datos, listas para generar().
    eslabones: [dict(nombre, descripcion, escena=clave de X.ESCENAS, icono, actores=[...], margen=(mín, máx, típico),
    captura=%, tendencia=-2 a 2, oportunidad=0 a 1)]. Una opción sin sus datos no sale, y no se inventan.
    circuito: argumentos de X.circuito_cadena, solo si hay un actor que se engancha a la cadena.
    Devuelve (variantes, descartadas), con descartadas = [(pieza, qué dato falta)]."""
    variantes, descartadas = [], []

    def con(pieza, campos):
        faltan = sorted({c for e in eslabones for c in campos if e.get(c) is None})
        if faltan:
            descartadas.append((pieza, ", ".join(faltan)))
        return not faltan

    guia = {g[0]: g for g in GUIA_CADENA}

    def sumar(pieza, html_):
        _, para, gana, pierde = guia[pieza]
        variantes.append(dict(nombre=para, gana=gana, pierde=pierde, pieza=pieza, html=html_))

    if con("cadena_isometrica", ["nombre", "escena", "descripcion"]):
        fases = [dict(nombre=e["nombre"], tipo=e["escena"], texto=e["descripcion"],
                      dato=f"Margen ~{e['margen'][2]} %" if e.get("margen") else None) for e in eslabones]
        sumar("cadena_isometrica", X.cadena_isometrica(fases, destacado=destacado, W=W))
    if con("cadena_capas", ["nombre", "descripcion", "actores", "margen", "tendencia", "oportunidad"]):
        sumar("cadena_capas", X.cadena_capas(eslabones, destacado=destacado, W=W))
    if con("cadena_margen", ["nombre", "icono", "margen", "captura"]):
        filas = [dict(nombre=e["nombre"], icono=e["icono"], margen=e["margen"][:2], captura=e["captura"]) for e in eslabones]
        sumar("cadena_margen", X.cadena_margen(filas, destacado=destacado, posicion=posicion, W=W, alto=300))
    if circuito:
        sumar("circuito_cadena", X.circuito_cadena(**circuito))
    else:
        descartadas.append(("circuito_cadena", "un actor que se engancha a la cadena"))
    return variantes, descartadas


def generar(titulo, variantes, salida, cliente="uso interno", pdf=True):
    """Un HTML, y su PDF si pdf, con una slide por variante. variantes: [dict(nombre, gana, pierde, html, pieza=None)].
    Devuelve la ruta del HTML."""
    if len(variantes) < 2:
        raise ValueError(f"Con {len(variantes)} opción no hace falta laboratorio: se usa esa y se dice por qué (S7). "
                         "Si faltan datos para otras, opciones_cadena los lista en descartadas.")
    if len(variantes) > 5:
        raise ValueError("Un laboratorio enseña como mucho 5 opciones: descarta antes las que no encajen.")
    salida = pathlib.Path(salida).resolve()
    n = len(variantes)
    slides = []
    for i, v in enumerate(variantes):
        letra = "ABCDE"[i]
        cuerpo = ea_deck.cabecera(f"Laboratorio · {titulo}", f'Opción <span class="hl-red">{letra}</span>: {X.E(v["nombre"])}') + X.cuerpo_slide(
            f'Gana: {v["gana"]}. Pierde: {v["pierde"]}.', v["html"])
        slides.append(ea_deck.slide(cuerpo, i + 1, n, f'Pieza: {v.get("pieza") or "composición"}', cliente))
    salida.write_text(ea_deck.documento(f"Laboratorio visual · {titulo}", slides, X.CSS + X.fuente_iconos()), encoding="utf-8")
    if pdf:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", f"--print-to-pdf={salida.with_suffix('.pdf')}",
                        "--print-to-pdf-no-header-footer", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                        "--run-all-compositor-stages-before-draw", salida.as_uri()], check=True, capture_output=True)
    return salida


def demo_cadena():
    """Cadena inventada para la prueba, con las cuatro opciones."""
    e = [dict(nombre="Cultivo", descripcion="Fruta de productores asociados.", escena="cultivo", icono="agriculture", actores=["Cooperativas"],
              margen=(4, 9, 6), captura=8, tendencia=-1, oportunidad=.2),
         dict(nombre="Conserva", descripcion="Frío y atmósfera controlada.", escena="frio", icono="ac_unit", actores=["Alfa", "Beta"],
              margen=(10, 18, 14), captura=12, tendencia=1, oportunidad=.8),
         dict(nombre="Envasado", descripcion="Bandejas y control de calidad.", escena="envasado", icono="inventory_2", actores=["Gamma"],
              margen=(6, 12, 9), captura=15, tendencia=0, oportunidad=.5),
         dict(nombre="Distribución", descripcion="Transporte refrigerado.", escena="logistica", icono="local_shipping", actores=["Operadores"],
              margen=(3, 7, 5), captura=10, tendencia=-1, oportunidad=.3),
         dict(nombre="Tienda", descripcion="Lineal y marca propia.", escena="retail", icono="storefront", actores=["Cadenas"],
              margen=(18, 30, 24), captura=55, tendencia=1, oportunidad=.6)]
    circuito = dict(cadena=[x["nombre"] for x in e], iconos=[x["icono"] for x in e], i_sale=1, i_entra=2,
                    socio={"logo_html": '<b style="font-size:20px">ALFA</b>', "pill": "Alfa · frío compartido", "texto": "Alquila cámaras al productor y le compra la merma para zumo"},
                    externo={"logo_html": '<b style="font-size:16px">CLIENTE</b>', "texto": "Compra fruta con más vida útil"},
                    flecha_sale="<b>Merma</b>", flecha_entra="<b>Fruta conservada</b>",
                    lecturas=[("El productor", "Convierte en ingreso lo que antes tiraba"), ("Alfa", "Asegura su insumo y fideliza al productor")],
                    titulo_cadena="Cadena de fruta fresca")
    return opciones_cadena(e, destacado=1, posicion=2, circuito=circuito)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "cadena":
        var, desc = demo_cadena()
        print(generar("Cadena de valor", var, sys.argv[2]), f"· {len(var)} opciones", f"· descartadas: {desc}" if desc else "")
    else:
        print(__doc__)
