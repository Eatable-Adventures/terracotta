#!/usr/bin/env python3
"""ea_deck: base fija de las presentaciones HTML de Eatable Adventures (pensadas para exportar a PDF).

Fija tres piezas que NO se rediseñan en cada presentación:
  - portada()  : ejecución del sistema de Fer (capas PNG + posiciones exactas) con la paleta de Terracotta.
  - cabecera() : eyebrow gris numerado + título semibold con tramo rojo + glow ámbar + logo arriba a la derecha.
  - cierre()   : "Gracias." + Mensaje clave | "Let's Beat" sobre el degradado de marca.

Lo demás (contenido de cada slide) se escribe encima con las variables de Terracotta.
Uso: ver README.md de esta carpeta. Todo queda embebido en base64 (HTML autocontenido, sin red).
"""
import base64, html, pathlib, re

AQUI = pathlib.Path(__file__).resolve().parent
DS = AQUI.parent                       # 03. Recursos/EA Design System
ASSETS = AQUI / "assets"
E = html.escape


def _b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def _uri(nombre, mime):
    return f"data:{mime};base64,{_b64(ASSETS / nombre)}"


PNG = lambda n: _uri(n, "image/png")
LOGO_SVG = _uri("logo-wordmark.svg", "image/svg+xml")      # wordmark vectorial (negro)
LOGO_CREMA = PNG("logo-ea-cream.png")                       # lockup con lema (crema)
GLOW = PNG("amber-glow.png")
LOCK = PNG("icon-lock.png")
FONDO = PNG("cover-background.png")                         # generado con generar_fondo_portada.py


def tokens_terracotta():
    css = (DS / "colors_and_type.css").read_text(encoding="utf-8")
    return re.sub(r"@import url\([^)]*\);", "", css)       # la Rubik va embebida, sin red


def fuentes():
    rubik = _b64(ASSETS / "fonts" / "rubik-latin.woff2")
    ms = _b64(ASSETS / "fonts" / "material-symbols-subset.woff2")
    return (
        "@font-face{font-family:'Rubik';font-style:normal;font-weight:300 800;font-display:block;"
        f"src:url(data:font/woff2;base64,{rubik}) format('woff2');}}\n"
        "@font-face{font-family:'Material Symbols Outlined';font-style:normal;font-weight:300;font-display:block;"
        f"src:url(data:font/woff2;base64,{ms}) format('woff2');}}"
    )


# ------------------------------------------------------------------ CSS fijo
CSS_BASE = """
html,body{margin:0;padding:0;background:#DCD6CC;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
*{box-sizing:border-box;}
body{font-family:'Rubik','Inter','Helvetica Neue',Arial,sans-serif;color:var(--fg1);}
.deck{padding:32px 0;}
.slide{width:1280px;height:720px;margin:0 auto 32px;background:var(--paper);position:relative;overflow:hidden;box-shadow:var(--shadow-md);}
@page{size:1280px 720px;margin:0;}
@media print{body{background:#fff;}.deck{padding:0;}.slide{margin:0;box-shadow:none;break-after:page;}.slide:last-child{break-after:auto;}}

/* iconos Material Symbols Outlined, peso 300 */
.ms{font-family:'Material Symbols Outlined';font-weight:300;font-style:normal;font-size:28px;line-height:1;display:inline-block;
white-space:nowrap;direction:ltr;-webkit-font-feature-settings:'liga';font-feature-settings:'liga';-webkit-font-smoothing:antialiased;
font-variation-settings:'FILL' 0,'wght' 300,'GRAD' 0,'opsz' 48;}

/* ---- slide de contenido: marco, cabecera y pie ---- */
.slide-inner{height:100%;padding:48px 64px 24px;display:flex;flex-direction:column;}
.slide-body{flex:1;min-height:0;display:flex;flex-direction:column;}
.slide-foot{margin-top:auto;padding-top:8px;display:flex;justify-content:space-between;align-items:center;
font-size:11px;color:var(--fg3);border-top:1px solid var(--border-2);}
.slide-foot b{color:var(--fg2);font-weight:500;}
.logo-tr{position:absolute;right:56px;top:20px;height:56px;}
.eyebrow-row{display:flex;align-items:center;gap:16px;margin:0 0 12px;}
.eyebrow2{font-size:var(--t-sm);font-weight:400;color:var(--fg3);letter-spacing:0;text-transform:none;}
.ttl{position:relative;padding-left:28px;margin:0 0 24px;}
.glow{position:absolute;left:-61px;top:-59px;width:150px;height:150px;background:url(__GLOW__) center/contain no-repeat;pointer-events:none;}
h2.t{position:relative;font-size:28px;font-weight:600;letter-spacing:-.015em;line-height:1.14;max-width:11.4in;margin:0;color:var(--fg1);}
h2.t .hl-red{color:var(--red);font-weight:700;}

/* ---- portada (ejecución del sistema de Fer, 10 x 5,625 in -> 1280 x 720 px = 128 px/in) ---- */
.slide.cover{background:var(--burgundy);color:var(--cream);}
.cover .cv-bg{position:absolute;left:-8px;top:-6px;width:1300px;height:732px;}
.cover .cv-logo{position:absolute;left:315px;top:35px;width:298px;height:60px;}
.cover .cv-title{position:absolute;left:319px;top:200px;width:836px;font-size:44px;font-weight:700;line-height:1.1;
color:var(--cream);text-transform:none;letter-spacing:-.005em;}
.cover .cv-title span{display:block;}
.cover .cv-sub{position:absolute;left:319px;top:347px;width:804px;font-size:27px;font-weight:400;line-height:1.25;color:var(--cream);}
.cover .cv-vline{position:absolute;left:655px;top:486px;width:1px;height:106px;background:#fff;}
.cover .cv-m{position:absolute;}
.cover .cv-m .l{display:block;font-size:12.5px;font-weight:700;color:var(--cream);line-height:1.3;}
.cover .cv-m .v{display:block;font-size:16px;font-weight:400;color:#fff;line-height:1.35;margin-top:4px;}
.cover .cv-m .v img{width:12px;height:13px;vertical-align:-1px;margin-right:6px;}
.cover .cv-copy{position:absolute;left:319px;top:672px;font-size:12.5px;color:var(--cream);}

/* ---- cierre ---- */
.slide.closing{display:grid;grid-template-columns:40% 60%;background:var(--paper);}
.cl-left{position:relative;}
.cl-thanks{position:absolute;left:64px;top:236px;font-size:54px;font-weight:700;letter-spacing:-.025em;line-height:1;color:var(--fg1);}
.cl-call{position:absolute;left:64px;top:322px;width:400px;background:var(--cream);border-left:3px solid var(--red);padding:16px 24px;}
.cl-call .k{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.2em;color:var(--red);margin-bottom:8px;}
.cl-call p{margin:0;font-size:var(--t-sm);line-height:1.5;color:var(--fg2);}
.cl-right{position:relative;background:var(--gradient-brand);color:var(--cream);}
.cl-right h2{position:absolute;left:64px;top:228px;font-size:64px;font-weight:700;letter-spacing:-.025em;line-height:1;margin:0;color:var(--cream);}
.cl-logo{position:absolute;right:56px;top:24px;height:64px;filter:brightness(0) invert(1);}
.cl-conf{position:absolute;right:64px;bottom:44px;font-size:12px;opacity:.85;}
""".replace("__GLOW__", GLOW)


# ------------------------------------------------------------------ piezas
def cabecera(eyebrow, titulo_html, pills=""):
    """eyebrow: 'NN. Sección' (gris). titulo_html: usa <span class="hl-red">tramo conclusivo</span>."""
    return (f'<img class="logo-tr" src="{LOGO_SVG}" alt="Eatable Adventures">'
            f'<div class="eyebrow-row"><span class="eyebrow2">{E(eyebrow)}</span>{pills}</div>'
            f'<div class="ttl"><span class="glow"></span><h2 class="t">{titulo_html}</h2></div>')


def pie(n, total, fuente, cliente):
    return (f'<div class="slide-foot"><span><b>{E(fuente)}</b></span>'
            f'<span>Eatable Adventures · Confidencial · Solo para uso de {E(cliente)} · <b>{n} / {total}</b></span></div>')


def slide(cuerpo_html, n, total, fuente, cliente):
    return (f'<section class="slide"><div class="slide-inner"><div class="slide-body">{cuerpo_html}</div>'
            f'{pie(n, total, fuente, cliente)}</div></section>')


def portada(linea1, linea2, subtitulo, realizado_para, equipo, fecha,
            clasificacion="Private & Confidential", anio=2026):
    """linea1: tipo de entregable. linea2: cliente o proyecto. Máx. ~22 caracteres por línea, en frase normal (no mayúsculas).
    subtitulo: una línea, bloques separados por ' · ', sin punto final.
    fecha: mes con mayúscula inicial y año ('Octubre 2026'). Las etiquetas se mantienen tal cual el template de marca."""
    return f"""<section class="slide cover">
<img class="cv-bg" src="{FONDO}" alt="">
<img class="cv-logo" src="{LOGO_CREMA}" alt="Eatable Adventures. The Beating Heart of Food Innovation">
<div class="cv-title"><span>{E(linea1)}</span><span>{E(linea2)}</span></div>
<div class="cv-sub">{E(subtitulo)}</div>
<span class="cv-vline"></span>
<div class="cv-m" style="left:323px;top:481px"><span class="l">Realizado para:</span><span class="v">{E(realizado_para)}</span></div>
<div class="cv-m" style="left:689px;top:481px"><span class="l">Date</span><span class="v">{E(fecha)}</span></div>
<div class="cv-m" style="left:323px;top:548px"><span class="l">Consultant Team</span><span class="v">{E(equipo)}</span></div>
<div class="cv-m" style="left:689px;top:548px"><span class="l">Classification</span><span class="v"><img src="{LOCK}" alt="">{E(clasificacion)}</span></div>
<div class="cv-copy">© {anio} Eatable Adventures - Consulting Firm. All rights reserved.</div>
</section>"""


def cierre(mensaje_clave, cliente):
    return f"""<section class="slide closing">
<div class="cl-left"><div class="cl-thanks">Gracias.</div>
<div class="cl-call"><span class="k">Mensaje clave</span><p>{E(mensaje_clave)}</p></div></div>
<div class="cl-right"><img class="cl-logo" src="{LOGO_SVG}" alt="Eatable Adventures"><h2>Let's Beat</h2>
<div class="cl-conf">Confidencial · Solo para uso de {E(cliente)}</div></div>
</section>"""


def documento(titulo, slides_html, css_extra=""):
    """slides_html: lista de strings (portada(), slide(), cierre())."""
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titulo)}</title>
<style>
{fuentes()}
{tokens_terracotta()}
{CSS_BASE}
{css_extra}
</style>
</head>
<body>
<div class="deck">
{chr(10).join(slides_html)}
</div>
</body>
</html>
"""
