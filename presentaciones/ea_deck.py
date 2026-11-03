#!/usr/bin/env python3
"""ea_deck: base fija de las presentaciones HTML de Eatable Adventures (pensadas para exportar a PDF).

Fija las piezas que NO se rediseñan en cada presentación:
  - portada()    : ejecución del sistema de referencia de la portada (capas PNG + posiciones exactas) con la paleta de Terracotta.
  - agenda()     : «AGENDA» con glow a la izquierda, línea vertical y secciones numeradas a la derecha, sin pie.
  - portadilla() : foto a sangre (o una escena isométrica si no hay foto con relación con el proyecto) y tarjeta blanca.
  - cabecera()   : eyebrow gris numerado + título en negrita con tramo rojo + glow ámbar + logo arriba a la derecha.
  - cierre()     : "Gracias." + mensaje (y próximo paso opcional) | "Let's Beat" sobre el degradado de marca.
Idioma: todas las etiquetas fijas salen en el idioma del deck (idioma="es" por defecto, o "en"). Decisiones del 01-11-2026.

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


TXT = {
    "es": dict(para="Realizado para", fecha="Fecha", equipo="Equipo", clas="Clasificación", conf_def="Confidencial",
               copy="© {anio} Eatable Adventures. Todos los derechos reservados.", pie="Confidencial · Solo para uso de {c}",
               gracias="Gracias.", siguiente="Próximo paso", agenda="Estructura del documento"),
    "en": dict(para="Prepared for", fecha="Date", equipo="Consultant Team", clas="Classification", conf_def="Private & Confidential",
               copy="© {anio} Eatable Adventures - Consulting Firm. All rights reserved.", pie="Confidential · For use by {c} only",
               gracias="Thank you.", siguiente="Next step", agenda="Document structure"),
}


# ------------------------------------------------------------------ CSS fijo
CSS_BASE = """
/* Verde de validación (29-10-2026): solo para estados de validación (favorable, validado, aprobado). No es color de marca ni de series de datos */
:root{--validacion:#2F7D4A;}
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
.eyebrow-row{display:flex;align-items:center;gap:16px;height:22px;margin:0 0 12px;}
.eyebrow2{font-size:var(--t-sm);font-weight:400;color:var(--fg3);letter-spacing:0;text-transform:none;}
.ttl{position:relative;padding-left:0;margin:0 0 24px;}
.glow{position:absolute;left:-81px;top:-59px;width:150px;height:150px;background:url(__GLOW__) center/contain no-repeat;pointer-events:none;}
h2.t{position:relative;font-size:28px;font-weight:700;letter-spacing:-.015em;line-height:1.14;max-width:11.4in;margin:0;color:var(--fg1);}
h2.t .hl-red{color:var(--red);font-weight:700;}

/* ---- portada (ejecución del sistema de referencia de la portada, 10 x 5,625 in -> 1280 x 720 px = 128 px/in) ---- */
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
.cover .cv-m .v.eq{font-size:14.5px;line-height:1.45;}

/* ---- agenda (formato del Google Slides de EA, 28-10-2026) ---- */
.agenda{position:absolute;inset:0;display:grid;grid-template-columns:450px 1px 1fr;align-items:center;padding:0 96px 0 108px;}
.ag-l{position:relative;}
.ag-ey{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--red);margin:0 0 14px;}
.ag-tt{position:relative;}
.ag-tt .glow{left:-81px;top:-43px;}
.ag-t{position:relative;font-size:64px;font-weight:700;letter-spacing:-.01em;line-height:1;margin:0;color:var(--fg1);}
.ag-s{font-size:18px;font-style:italic;color:var(--fg1);margin:22px 0 0;}
.ag-v{align-self:stretch;margin:120px 0;background:var(--border-1);}
.ag-r{padding-left:30px;}
.ag-i{padding:22px 0 24px;border-bottom:1px solid var(--border-1);}
.ag-i:last-child{border-bottom:0;}
.ag-i h3{margin:0;font-size:19px;font-weight:700;color:var(--fg1);letter-spacing:-.005em;}
.ag-i h3 span{color:var(--red);}
.ag-i p{margin:14px 0 0;font-size:13px;color:var(--fg2);}
.agenda.densa .ag-v{margin:60px 0;}
.agenda.densa .ag-i{padding:12px 0 13px;}
.agenda.densa .ag-i h3{font-size:17px;}
.agenda.densa .ag-i p{margin:5px 0 0;font-size:12px;}

/* ---- portadilla de sección (foto a sangre o escena isométrica, y tarjeta blanca) ---- */
.slide.pd2{background:var(--fg1);}
.pd2.esc{background:var(--surface-fill);}
.pd2 .pd-img{position:absolute;inset:0;background-size:cover;background-position:center;}
.pd2 .pd-vis{position:absolute;right:40px;top:50%;transform:translateY(-50%);}
.pd2 .pd-logo{position:absolute;right:56px;top:20px;height:56px;filter:brightness(0) invert(1);}
.pd2.esc .pd-logo{filter:none;}
.pd2 .pd-card{position:absolute;left:64px;bottom:64px;width:600px;background:#fff;border-radius:16px;padding:32px 40px 34px;box-shadow:var(--shadow-md);}
.pd2 .pd-num{font-size:72px;font-weight:300;line-height:.9;color:var(--red);letter-spacing:-.04em;margin:0 0 18px;}
.pd2 .pd-t{font-size:34px;font-weight:700;letter-spacing:-.015em;line-height:1.12;margin:0 0 12px;color:var(--fg1);text-wrap:balance;}
.pd2 .pd-s{font-size:17px;color:var(--fg2);line-height:1.4;margin:0;}

/* ---- cierre ---- */
.slide.closing{display:grid;grid-template-columns:40% 60%;background:var(--paper);}
.cl-left{position:relative;}
.cl-thanks{position:absolute;left:64px;top:236px;font-size:54px;font-weight:700;letter-spacing:-.025em;line-height:1;color:var(--fg1);}
.cl-call{position:absolute;left:64px;top:322px;width:400px;background:var(--surface-fill);border-left:3px solid var(--red);padding:16px 24px;}
.cl-next{position:absolute;left:64px;top:300px;width:400px;font-size:15px;color:var(--fg2);}
.cl-next b{color:var(--fg1);font-weight:600;}
.cl-next+.cl-call{top:346px;}
.cl-call .k{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.2em;color:var(--red);margin-bottom:8px;}
.cl-call p{margin:0;font-size:var(--t-sm);line-height:1.5;color:var(--fg2);}
.cl-call p b{color:var(--fg1);font-weight:700;}
.cl-right{position:relative;background:var(--gradient-brand);color:var(--cream);}
.cl-right h2{position:absolute;left:64px;top:50%;transform:translateY(-50%);font-size:64px;font-weight:700;letter-spacing:-.025em;line-height:1;margin:0;color:var(--cream);}
.cl-logo{position:absolute;right:56px;top:24px;height:64px;filter:brightness(0) invert(1);}
.cl-conf{position:absolute;right:64px;bottom:44px;font-size:12px;opacity:.85;}
""".replace("__GLOW__", GLOW)


# ------------------------------------------------------------------ piezas
def cabecera(eyebrow, titulo_html, pills=""):
    """eyebrow: 'NN. Sección' (gris). titulo_html: usa <span class="hl-red">tramo conclusivo</span>."""
    return (f'<img class="logo-tr" src="{LOGO_SVG}" alt="Eatable Adventures">'
            f'<div class="eyebrow-row"><span class="eyebrow2">{E(eyebrow)}</span>{pills}</div>'
            f'<div class="ttl"><span class="glow"></span><h2 class="t">{titulo_html}</h2></div>')


def pie(n, total, fuente, cliente, idioma="es"):
    """Pie de slide: la fuente a la izquierda (sin fechas concretas) y la confidencialidad con el número a la derecha,
    sin «Eatable Adventures» (decisión del 01-11-2026)."""
    return (f'<div class="slide-foot"><span><b>{E(fuente)}</b></span>'
            f'<span>{E(TXT[idioma]["pie"].format(c=cliente))} · <b>{n} / {total}</b></span></div>')


def slide(cuerpo_html, n, total, fuente, cliente, idioma="es", clave=None):
    """clave: identificador estable de la slide entre versiones («s07»), para anclar comentarios. Sin clave, la salida no cambia."""
    attr = f' data-slide-key="{E(str(clave), quote=True)}"' if clave else ""
    return (f'<section class="slide"{attr}><div class="slide-inner"><div class="slide-body">{cuerpo_html}</div>'
            f'{pie(n, total, fuente, cliente, idioma)}</div></section>')


def agenda(secciones, subtitulo="", idioma="es"):
    """Agenda: «AGENDA» con glow y un subtítulo a la izquierda, línea vertical y las secciones a la derecha, sin pie.
    secciones: [(título, descripción)] o [(número, título, descripción)]; con más de cinco, versión densa."""
    items = [(f"{i + 1:02d}", *s) if len(s) == 2 else s for i, s in enumerate(secciones)]
    filas = "".join(f'<div class="ag-i"><h3><span>{E(n)}.</span> {E(t)}</h3>' + (f'<p>{E(d)}</p>' if d else "") + '</div>' for n, t, d in items)
    return (f'<section class="slide"><img class="logo-tr" src="{LOGO_SVG}" alt="Eatable Adventures">'
            f'<div class="agenda{" densa" if len(items) > 5 else ""}"><div class="ag-l"><p class="ag-ey">{E(TXT[idioma]["agenda"])}</p>'
            f'<div class="ag-tt"><span class="glow"></span><h2 class="ag-t">AGENDA</h2></div>'
            + (f'<p class="ag-s">{E(subtitulo)}</p>' if subtitulo else "") + f'</div><div class="ag-v"></div><div class="ag-r">{filas}</div></div></section>')


def portadilla(numero, titulo, subtitulo="", foto=None, visual_html=None):
    """Portadilla de sección: foto a sangre (en color; ruta a un .jpg o .png con su origen registrado) con la tarjeta
    blanca abajo a la izquierda (número, título y subtítulo). Si no hay una foto con relación con el proyecto (D7), visual_html pone una escena isométrica a la derecha sobre fondo gris claro, por ejemplo
    ea_elementos.escena_iso("fermentacion", True, W=600). Nunca un genérico del sector."""
    tarjeta = (f'<div class="pd-card"><div class="pd-num">{E(numero)}</div><h2 class="pd-t">{E(titulo)}</h2>'
               + (f'<p class="pd-s">{E(subtitulo)}</p>' if subtitulo else "") + '</div>')
    if foto:
        mime = "image/png" if str(foto).lower().endswith(".png") else "image/jpeg"
        return (f'<section class="slide pd2"><div class="pd-img" style="background-image:url(data:{mime};base64,{_b64(foto)})"></div>'
                f'<img class="pd-logo" src="{LOGO_SVG}" alt="Eatable Adventures">{tarjeta}</section>')
    return (f'<section class="slide pd2 esc"><div class="pd-vis">{visual_html or ""}</div>'
            f'<img class="pd-logo" src="{LOGO_SVG}" alt="Eatable Adventures">{tarjeta}</section>')


def portada(linea1, linea2, subtitulo, realizado_para, equipo, fecha, clasificacion=None, anio=2026, idioma="es"):
    """linea1: tipo de entregable. linea2: cliente o proyecto. Máx. ~22 caracteres por línea, en frase normal (no mayúsculas).
    subtitulo: una línea, bloques separados por ' · ', sin punto final. fecha: mes con mayúscula inicial y año ('Octubre 2026').
    equipo: las personas reales del proyecto (texto o lista, una por línea); «Delivery Excellence» solo si se pide para
    un deck concreto. Las etiquetas y el copyright salen en el idioma del deck (decisiones del 01-11-2026)."""
    t = TXT[idioma]
    lineas = equipo if isinstance(equipo, (list, tuple)) else [equipo]
    eq = "<br>".join(E(x) for x in lineas)
    sube = 24 if len(lineas) > 2 else 0          # con un equipo largo, todo más arriba para dejar aire sobre el copyright
    y1, y2 = 481 - sube, 548 - sube
    return f"""<section class="slide cover">
<img class="cv-bg" src="{FONDO}" alt="">
<img class="cv-logo" src="{LOGO_CREMA}" alt="Eatable Adventures. The Beating Heart of Food Innovation">
<div class="cv-title"><span>{E(linea1)}</span><span>{E(linea2)}</span></div>
<div class="cv-sub">{E(subtitulo)}</div>
<span class="cv-vline" style="top:{486 - sube}px"></span>
<div class="cv-m" style="left:323px;top:{y1}px"><span class="l">{t["para"]}</span><span class="v">{E(realizado_para)}</span></div>
<div class="cv-m" style="left:689px;top:{y1}px"><span class="l">{t["fecha"]}</span><span class="v">{E(fecha)}</span></div>
<div class="cv-m" style="left:323px;top:{y2}px"><span class="l">{t["equipo"]}</span><span class="v{" eq" if len(lineas) > 1 else ""}">{eq}</span></div>
<div class="cv-m" style="left:689px;top:{y2}px"><span class="l">{t["clas"]}</span><span class="v"><img src="{LOCK}" alt="">{E(clasificacion or t["conf_def"])}</span></div>
<div class="cv-copy">{t["copy"].format(anio=anio)}</div>
</section>"""


def cierre(mensaje_clave, cliente, siguiente=None, idioma="es"):
    """Cierre fijo. El mensaje va sin la etiqueta «Mensaje clave» (29-10-2026) y admite **negrita** para destacar una parte.
    siguiente: próximo paso o entregable opcional bajo «Gracias.» («E3, Veredicto estratégico»)."""
    t = TXT[idioma]
    txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", E(mensaje_clave))
    sig = f'<div class="cl-next">{t["siguiente"]}: <b>{E(siguiente)}</b></div>' if siguiente else ""
    return f"""<section class="slide closing">
<div class="cl-left"><div class="cl-thanks">{t["gracias"]}</div>{sig}
<div class="cl-call"><p>{txt}</p></div></div>
<div class="cl-right"><img class="cl-logo" src="{LOGO_SVG}" alt="Eatable Adventures"><h2>Let's Beat</h2>
<div class="cl-conf">{E(t["pie"].format(c=cliente))}</div></div>
</section>"""


def _marcar_pendientes(cuerpo):
    """==dato pendiente== sale marcado en cualquier texto del documento, también en SVG; sin marcadores, no cambia nada."""
    html_ = '<span class="hueco" style="background:#FFF1B8;color:#1E1E1E;font-weight:600;padding:1px 6px;border-radius:4px">\\1</span>'
    svg = '<tspan class="hueco" style="fill:#9A6B00;font-weight:700">\\1</tspan>'
    patron = r"==([^=<>]{1,80}?)=="
    if not re.search(patron, cuerpo):
        return cuerpo
    cuerpo = re.sub(r"(<text\b[^>]*>)([^<]*==[^<]*)", lambda m: m.group(1) + re.sub(patron, svg, m.group(2)), cuerpo)
    return re.sub(r">([^<]*==[^<]*)<", lambda m: ">" + re.sub(patron, html_, m.group(1)) + "<", cuerpo)


def documento(titulo, slides_html, css_extra="", idioma="es"):
    """slides_html: lista de strings (portada(), agenda(), portadilla(), slide(), cierre()).
    ==dato pendiente== sale marcado en cualquier texto (lo lista revisar_deck.py)."""
    slides_html = [_marcar_pendientes(s) for s in slides_html]
    return f"""<!doctype html>
<html lang="{idioma}">
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
