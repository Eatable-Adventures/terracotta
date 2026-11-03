#!/usr/bin/env python3
"""Genera lo que el núcleo enseña de gráficos y mapas a partir de ea_elementos, para que haya una sola fuente:
  - preview/chart-*.html y preview/map-*.html, las tarjetas del panel del sistema de diseño;
  - Charts Catalogue.html, el índice de gráficos: qué tipo, para qué, qué pieza y su ejemplo en la galería.

No se editan a mano. Se ejecuta tras cambiar una de estas piezas (verificar.py lo hace).
Ejecutar: python3 build_nucleo.py
"""
import html, pathlib, re, subprocess, sys, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
NUCLEO = AQUI.parent
sys.path.insert(0, str(AQUI))
import ea_deck                                      # noqa: E402
import ea_elementos as X                            # noqa: E402
import build_galeria_elementos as G                 # noqa: E402
from inspeccionar_dom import CHROME                 # noqa: E402

# archivo, grupo, nombre, para qué sirve, pieza, ejemplo propio (None: el de la galería)
GRAFICOS = [
    ("chart-kpi", "KPI tiles", "One number, its change and its trend", "cifra_delta", None),
    ("chart-bar", "Bar chart", "Compare categories or periods", "columnas", None),
    ("chart-hbar", "Horizontal bars", "Ranked lists with long labels", "barras_ranking", None),
    ("chart-line", "Line chart", "Trend over time", "linea", None),
    ("chart-area", "Area chart", "Volume over time, by part", "area_apilada", None),
    ("chart-donut", "Donut", "Part of a whole, up to five segments", "donut", None),
    ("chart-stacked", "Stacked bars", "Composition by group", "barras_apiladas", None),
    ("chart-funnel", "Funnel", "Successive stages of a filter", "embudo", None),
    ("chart-progress", "Progress vs target", "How far from the goal", "bala", None),
    ("chart-heatmap", "Heatmap", "Intensity across two dimensions", "mapa_calor", None),
    ("chart-sunburst", "Sunburst", "Nested hierarchy, two rings", "sunburst", None),
    ("chart-timeline", "Timeline / Gantt", "Phases, dates and today", "gantt", None),
    ("chart-radar", "Radar", "Profile against several criteria", "radar", None),
    ("chart-scatter", "Scatter / bubble", "Two variables per element", "dispersion", None),
    ("chart-waterfall", "Waterfall", "Bridge between two values", "cascada", None),
    ("chart-treemap", "Treemap", "Share of a total, up to 15 parts", "treemap", None),
    ("chart-sankey", "Sankey", "Flows from sources to destinations", "sankey", None),
]
MAPAS = [
    ("map-hubs", "Hub network", "Where the actors are, in groups", "mapa_actores", None),
    ("map-coverage", "Coverage", "Presence by country, up to three states", "mapa_coropletico",
     lambda: X.mapa_coropletico({"España": 2, "México": 2, "Colombia": 2, "Chile": 1, "Perú": 1, "Argentina": 1, "Uruguay": 1},
                                region="hispano", etiquetas=[], escala=(0, 2), leyenda_txt="Grey: no presence · light: partners · dark: active", W=820)),
    ("map-choropleth", "Choropleth", "One value per country", "mapa_coropletico", None),
    ("map-region", "Region focus", "One value per country, within a region", "mapa_coropletico",
     lambda: X.mapa_coropletico({"España": 34, "Portugal": 12}, region="iberia", escala=(0, 60), leyenda_txt="Projects per country", W=640)),
    ("map-bubbles", "Bubble map", "Amounts by place, proportional area", "mapa_burbujas", None),
    ("map-flows", "Flow map", "From one origin to several destinations", "mapa_flujos", None),
]
ICONOS_CSS = re.search(r"\.ms\{.*?\}\s*\n?.*?\}", ea_deck.CSS_BASE, re.S).group(0)


def _tarjeta(archivo, grupo, nombre, para, pieza, propio, viewport="760x420"):
    cuerpo = propio() if propio else G.ejemplo(pieza)
    css = X.CSS + (X.fuente_iconos() + ICONOS_CSS if 'class="ms' in cuerpo else "")
    return (f'<!-- @dsCard group="{grupo}" viewport="{viewport}" name="{html.escape(nombre)}" subtitle="{html.escape(para)}" -->\n'
            f'<!-- Generada por presentaciones/build_nucleo.py desde ea_elementos.{pieza}. No se edita a mano. -->\n'
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<link rel="stylesheet" href="../colors_and_type.css">\n'
            f'<style>html,body{{margin:0;background:var(--paper);color:var(--fg1);font-family:var(--font-sans);}}*{{box-sizing:border-box;}}{css}</style>\n'
            f'</head>\n<body>\n<div id="pieza" style="display:inline-block;padding:16px">{cuerpo}</div>\n</body>\n</html>\n')


def _medir(ruta):
    """Ancho y alto reales de la tarjeta, para su viewport."""
    txt = ruta.read_text(encoding="utf-8").replace("</body>", """<script>document.fonts.ready.then(()=>{const r=document.getElementById('pieza').getBoundingClientRect();
document.documentElement.setAttribute('data-m',Math.ceil(r.width)+'x'+Math.ceil(r.height));});</script></body>""")
    with tempfile.TemporaryDirectory(dir=ruta.parent) as d:
        c = pathlib.Path(d) / "m.html"
        c.write_text(txt.replace('href="../colors_and_type.css"', f'href="{(NUCLEO / "colors_and_type.css").as_uri()}"'), encoding="utf-8")
        r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--window-size=1400,1000", "--virtual-time-budget=6000", "--dump-dom", c.as_uri()],
                           capture_output=True, text=True, timeout=60)
    m = re.search(r'data-m="(\d+)x(\d+)"', r.stdout)
    return m.group(1) + "x" + m.group(2) if m else "760x420"


def tarjetas():
    for grupo, lista in (("Charts", GRAFICOS), ("Maps", MAPAS)):
        for archivo, nombre, para, pieza, propio in lista:
            ruta = NUCLEO / "preview" / f"{archivo}.html"
            ruta.write_text(_tarjeta(archivo, grupo, nombre, para, pieza, propio), encoding="utf-8")
            ruta.write_text(_tarjeta(archivo, grupo, nombre, para, pieza, propio, _medir(ruta)), encoding="utf-8")


def indice():
    fila = lambda a, n, p, f: (f'<tr><td><b>{html.escape(n)}</b></td><td>{html.escape(p)}</td><td><a href="presentaciones/Galer%C3%ADa%20de%20elementos.html#{f}"><code>{f}()</code></a></td>'
                               f'<td><a href="preview/{a}.html">Card</a></td></tr>')
    muestra = lambda c, t: f'<span class="m"><i style="background:{c}"></i>{t}</span>'
    page = f"""<!-- Generada por presentaciones/build_nucleo.py. No se edita a mano. -->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Charts &amp; Data Visualization · Terracotta</title>
<link rel="stylesheet" href="colors_and_type.css">
<style>
*{{box-sizing:border-box;}}
body{{margin:0;background:var(--paper);color:var(--fg1);font-family:var(--font-sans);}}
.page{{max-width:1080px;margin:0 auto;padding:48px 32px 80px;}}
h1{{font-size:38px;font-weight:400;letter-spacing:-.02em;margin:0 0 10px;line-height:1.08;}}
h2{{font-size:20px;font-weight:700;margin:40px 0 12px;}}
.eyebrow{{font-size:12px;text-transform:uppercase;letter-spacing:.16em;color:var(--red);margin-bottom:14px;}}
.lead{{font-size:16px;line-height:1.55;color:var(--fg2);max-width:70ch;margin:0;}}
.reglas{{list-style:none;padding:0;margin:0;display:grid;gap:10px;}}
.reglas li{{background:var(--surface-fill);border-radius:10px;padding:12px 16px;font-size:14px;line-height:1.45;color:var(--fg2);}}
.reglas b{{color:var(--fg1);}}
.ms-c{{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:8px;}}
.m{{display:inline-flex;align-items:center;gap:6px;font-size:13px;}}
.m i{{width:13px;height:13px;border-radius:3px;display:inline-block;}}
table{{width:100%;border-collapse:collapse;font-size:14px;}}
th{{text-align:left;font-size:12px;color:var(--fg3);padding:0 12px 8px 0;border-bottom:1.5px solid var(--fg1);}}
td{{padding:9px 12px 9px 0;border-bottom:1px solid var(--border-2);color:var(--fg2);vertical-align:middle;}}
td b{{color:var(--fg1);font-weight:600;}}
a{{color:var(--red);}}
code{{font-size:13px;}}
</style>
</head>
<body>
<div class="page">
<div class="eyebrow">Data visualization</div>
<h1>Charts on <b>one system</b></h1>
<p class="lead">Every chart in Terracotta comes from one set of pieces: <code>presentaciones/ea_elementos/</code>. The full catalogue, with an example, when to use each piece and when not to, is the <a href="presentaciones/Galer%C3%ADa%20de%20elementos.html">gallery of elements</a>. This page is the index by chart type.</p>
<h2>Colour rule</h2>
<ul class="reglas">
<li><b>One series:</b> neutral grey, and the element the message is about in EAV Red. Never everything in red.
<div class="ms-c">{muestra(X.RED, "Focus · --chart-1")}{muestra(X.NEUTRO, "Neutral · --chart-neutral")}</div></li>
<li><b>Categories of one family:</b> the red ramp, dark to light.
<div class="ms-c">{"".join(muestra(c, f"--ramp-{i + 1}") for i, c in enumerate(X.RAMP))}</div></li>
<li><b>Two things of a different nature</b> (us against a benchmark): red and dark grey.</li>
<li><b>Status:</b> green only for validation and status pieces. Yellow only as the light point and in the traffic light. Orange only inside the brand gradient.</li>
</ul>
<h2>Chart types</h2>
<table><tr><th>Type</th><th>Use it for</th><th>Piece, in the gallery</th><th>Panel</th></tr>
{"".join(fila(a, n, p, f) for a, n, p, f, _ in GRAFICOS)}</table>
<h2>Maps</h2>
<table><tr><th>Type</th><th>Use it for</th><th>Piece, in the gallery</th><th>Panel</th></tr>
{"".join(fila(a, n, p, f) for a, n, p, f, _ in MAPAS)}</table>
<p class="lead" style="margin-top:16px">In decks and static documents, use these pieces. In live apps, <code>maps-brand.js</code> draws the same maps in the browser: see <a href="Maps%20Catalogue.html">Maps Catalogue</a>.</p>
</div>
</body>
</html>
"""
    (NUCLEO / "Charts Catalogue.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    tarjetas()
    indice()
    print(f"Núcleo generado: {len(GRAFICOS)} gráficos y {len(MAPAS)} mapas en preview/, e índice en Charts Catalogue.html")
