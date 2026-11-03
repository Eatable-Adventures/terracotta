"""base: tokens, primitivas SVG, lienzo, utilidades de color y escala y CSS común de ea_elementos.

Los colores se leen de colors_and_type.css (núcleo de Terracotta) al importar; la rampa de rojos sale de
embudo_canonico.py y el verde de validación de ea_deck.py. Nunca se copian a mano.

Reglas de color comunes (Terracotta):
- Una sola serie: gris neutro y lo que importa en rojo de marca. Nunca todo en rojo.
- Categorías de una misma familia: rampa de rojos, rampa(n).
- Dos cosas de distinta naturaleza (nosotros frente a referencia): rojo y gris oscuro.
- Verde de validación solo para estados de validación; amarillo solo como punto de luz.
- Excepción (30-10-2026) para piezas de estado: el semáforo usa verde, amarillo y rojo; las marcas
  de cumplimiento, el check en verde; el chip de variación, verde (bueno), gris (neutro) y rojo (malo).

Convenciones de los parámetros: los textos se escapan y admiten **negrita** puntual; los que acaban en
_html (o se documentan como HTML) se insertan tal cual. Los elementos de más de tres campos son dict.
"""
import base64, datetime, html, json, math, pathlib, re, sys

AQUI = pathlib.Path(__file__).resolve().parent.parent     # presentaciones/
DS = AQUI.parent                                          # 03. Recursos/EA Design System
E = html.escape

sys.path.insert(0, str(AQUI))
import ea_deck                                     # noqa: E402
from .iconos import NOMBRES as _ICONOS, parecidos as _parecidos   # noqa: E402
from .embudo_canonico import RAMP, funnel_svg     # noqa: E402  rampa canónica de rojos, de oscuro a claro

__all__ = ["ANCHO_CUERPO", "HUECO", "REJILLAS", "alto_cuerpo", "fila", "columna", "rotulo_bloque", "E", "AQUI", "DS", "RAMP", "funnel_svg", "ea_deck", "T", "RED", "CREAM", "BLACK", "PAPER", "DCREAM", "GREY", "LGREY", "BURG", "ORANGE", "FG1", "FG2", "FG3", "FG4", "TINT", "FILL", "BORDER2", "INPUT", "VALIDACION", "CATEGORIAS", "HEAT", "FONT", "MESES", "uid", "oscuro", "sobre", "md", "fuente_iconos", "lin", "log", "text", "rect", "line", "circle", "head", "arrow", "curve", "hatch", "flecha_svg", "Lienzo", "icono", "icono_caja", "pill", "logo", "cuerpo_slide", "CSS", "YELLOW", "fmt", "NEUTRO", "mezcla", "rampa", "calor", "arrow_eje"]


def _tokens():
    css = (DS / "colors_and_type.css").read_text(encoding="utf-8")
    root = css[css.index(":root"):css.index("}", css.index(":root"))]
    return dict(re.findall(r"--([\w-]+):\s*(#[0-9A-Fa-f]{6})", root))


T = _tokens()


RED, CREAM, BLACK, PAPER = T["red"], T["cream"], T["black"], T["paper"]


DCREAM, GREY, LGREY, BURG, ORANGE = T["dark-cream"], T["grey"], T["light-grey"], T["burgundy"], T["orange"]


FG1, FG2, FG3, FG4 = T["fg1"], T["fg2"], T["fg3"], T["fg4"]


TINT, FILL, BORDER2, INPUT = T["brand-tint"], T["surface-fill"], T["border-2"], T["input"]


VALIDACION = re.search(r"--validacion:\s*(#[0-9A-Fa-f]{6})", ea_deck.CSS_BASE).group(1)   # solo estados de validación


CATEGORIAS = [RAMP[0], RAMP[2], RAMP[3], RAMP[4]]   # hasta 4 categorías de una misma familia, en la rampa de rojos


HEAT = [FILL, RAMP[4], RAMP[3], RAMP[1]]            # notas 0 a 3


FONT = "Rubik,Inter,Helvetica Neue,Arial,sans-serif"


MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


_uid = [0]


def uid(p="v"):
    _uid[0] += 1
    return f"{p}{_uid[0]}"


def oscuro(color):
    """True si el color pide texto blanco encima (luminancia perceptual por debajo de 160)."""
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.299 * r + 0.587 * g + 0.114 * b < 160


def sobre(color):
    """Color del texto que va encima de un relleno."""
    return "#fff" if oscuro(color) else FG1


def _fmt_simple(x):
    """Número en formato español (coma decimal), sin ceros sobrantes."""
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def md(t):
    """Texto escapado con **negrita** puntual y ==dato pendiente== marcado; las fechas DD-MM-YYYY no se parten de línea."""
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", E(str(t)))
    t = re.sub(r"==(.+?)==", r'<span class="hueco">\1</span>', t)     # dato pendiente: ==Por incluir==
    return re.sub(r"(\d{2}-\d{2}-\d{4})", r'<span class="nw">\1</span>', t)


def fuente_iconos():
    """@font-face de Material Symbols Outlined con los iconos del catálogo (ea_elementos/iconos.py). Va después de
    ea_deck.fuentes() en el CSS, así que la sustituye. Catálogo visual: «Catálogo de iconos.html»."""
    b = base64.b64encode((AQUI / "assets/fonts/material-symbols-ea.woff2").read_bytes()).decode()
    return ("@font-face{font-family:'Material Symbols Outlined';font-style:normal;font-weight:300;font-display:block;"
            f"src:url(data:font/woff2;base64,{b}) format('woff2');}}")


def lin(d0, d1, r0, r1):
    return lambda v: r0 + (v - d0) * (r1 - r0) / (d1 - d0)


def log(d0, d1, r0, r1):
    a, b = math.log10(d0), math.log10(d1)
    return lambda v: r0 + (math.log10(v) - a) * (r1 - r0) / (b - a)


def text(x, y, s, size=13, weight=400, fill=FG2, anchor="start", italic=False, ls=None, halo=False):
    st = f"font-family:{FONT};font-size:{size}px;font-weight:{weight};fill:{fill};"
    if halo:
        st += "paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round;"
    if italic:
        st += "font-style:italic;"
    if ls is not None:
        st += f"letter-spacing:{ls}px;"
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="{st}">{E(str(s))}</text>'


def rect(x, y, w, h, fill, rx=0, stroke="none", sw=1, dash=None, op=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    extra += f' fill-opacity="{op}"' if op is not None else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{extra}/>')


def line(x1, y1, x2, y2, stroke=GREY, sw=1, dash=None, cap="butt"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')


def circle(cx, cy, r, fill, stroke="none", sw=1):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def head(x, y, ang, color, size=9):
    """Punta de flecha rellena con la punta en (x, y), apuntando en `ang` (radianes)."""
    bx, by = x - size * math.cos(ang), y - size * math.sin(ang)
    px, py = 0.55 * size * math.sin(ang), -0.55 * size * math.cos(ang)
    return f'<polygon points="{x:.1f},{y:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{color}"/>'


def arrow(pts, color=FG3, sw=2, dash=None, size=9, both=False):
    """Flecha por una polilínea de puntos [(x, y), ...]; la punta va en el último punto."""
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    ex, ey = x2 - (size - 1) * math.cos(ang), y2 - (size - 1) * math.sin(ang)
    seq = list(pts[:-1]) + [(ex, ey)]
    out = []
    if both:
        (a1, b1), (a2, b2) = pts[1], pts[0]
        ang0 = math.atan2(b2 - b1, a2 - a1)
        seq[0] = (a2 - (size - 1) * math.cos(ang0), b2 - (size - 1) * math.sin(ang0))
        out.append(head(a2, b2, ang0, color, size))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in seq)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    out.insert(0, f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"{da}/>')
    out.append(head(x2, y2, ang, color, size))
    return "".join(out)


def curve(p0, c1, c2, p1, color=RED, sw=2.5, dash=None, size=10):
    """Curva de Bézier cúbica con punta en p1."""
    ang = math.atan2(p1[1] - c2[1], p1[0] - c2[0])
    ex, ey = p1[0] - (size - 1) * math.cos(ang), p1[1] - (size - 1) * math.sin(ang)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{p0[0]},{p0[1]} C{c1[0]},{c1[1]} {c2[0]},{c2[1]} {ex:.1f},{ey:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{da}/>' + head(p1[0], p1[1], ang, color, size))


def hatch(color=INPUT, bg=LGREY):
    """Patrón rayado (para lo no evaluable). Devuelve (id, defs)."""
    i = uid("h")
    return i, (f'<pattern id="{i}" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
               f'<rect width="6" height="6" fill="{bg}"/><line x1="0" y1="0" x2="0" y2="6" stroke="{color}" stroke-width="2"/></pattern>')


def flecha_svg(color=RED, ancho=22, alto=14, grosor=2, abajo=False):
    """Flecha de línea en SVG en línea, para meter entre cajas HTML (derecha o abajo)."""
    if abajo:
        return (f'<svg width="{alto}" height="{ancho}" viewBox="0 0 {alto} {ancho}" style="flex:none"><path d="M{alto / 2} 1V{ancho - 3}'
                f'M{alto / 2 - 5} {ancho - 9}l5 6 5-6" stroke="{color}" stroke-width="{grosor}" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    m = alto / 2
    return (f'<svg width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}" style="flex:none"><path d="M1 {m}H{ancho - 3}'
            f'M{ancho - 8} {m - 5}l5 5-5 5" stroke="{color}" stroke-width="{grosor}" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


class Lienzo:
    """Lienzo de tamaño fijo: capa SVG debajo y cajas HTML posicionadas encima."""

    def __init__(self, w, h):
        self.w, self.h, self.defs, self.s, self.d = w, h, [], [], []

    def add(self, *svg):
        self.s.extend(svg)
        return self

    def div(self, x, y, w, inner, cls="", anchor="start", va="top", style=""):
        """anchor: start (x = borde izq.), middle (x = centro), end (x = borde der.). va: top, middle o bottom."""
        left = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
        tr = "transform:translateY(-50%);" if va == "middle" else ("transform:translateY(-100%);" if va == "bottom" else "")
        ta = {"start": "left", "middle": "center", "end": "right"}[anchor]
        self.d.append(f'<div class="lz-t {cls}" style="left:{left:.1f}px;top:{y:.1f}px;width:{w:.1f}px;text-align:{ta};{tr}{style}">{inner}</div>')
        return self

    def render(self, extra_style=""):
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (f'<div class="lz" style="width:{self.w}px;height:{self.h}px;{extra_style}">'
                f'<svg class="lz-svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'xmlns="http://www.w3.org/2000/svg">{defs}{"".join(self.s)}</svg>{"".join(self.d)}</div>')


def icono(nombre, size=28, color=FG2):
    """Icono Material Symbols Outlined (peso 300). Siempre la misma familia; el icono tiene que significar algo.
    Falla si el nombre no está en el catálogo (iconos.py), porque la fuente incrustada lo pintaría como texto."""
    if nombre not in _ICONOS:
        raise ValueError(f"Icono «{nombre}» fuera del catálogo. Parecidos: {', '.join(_parecidos(nombre)) or 'ninguno'}. "
                         f"Busca en el catálogo con iconos.buscar_icono(), en toda la familia con iconos.buscar_completo() (en inglés) "
                         f"y añade el que encaje a ea_elementos/iconos.py.")
    return f'<span class="ms" style="font-size:{size}px;color:{color}">{nombre}</span>'


def icono_caja(nombre, size=22, color=None, fondo=None, caja=40, radio=10):
    """Icono dentro de un cuadrado redondeado (rojo sobre rosa por defecto)."""
    return (f'<span style="flex:none;width:{caja}px;height:{caja}px;border-radius:{radio}px;background:{fondo or TINT};'
            f'display:inline-flex;align-items:center;justify-content:center">{icono(nombre, size, color or RED)}</span>')


def pill(txt, kind="neutral"):
    """Píldora de estado. kind: red, rosa, neutral, sand, out, burg."""
    return f'<span class="pl pl-{kind}">{E(txt)}</span>'


def logo(ruta, alto=28, lado="right", max_ancho=120):
    """Logo (svg, png o jpg) como <img> en línea, del mismo alto en toda la slide; None si el archivo no existe.
    Regla: a color, alineado a la derecha de la tarjeta y con su origen registrado en un FUENTES.md."""
    p = pathlib.Path(ruta)
    if not p.exists():
        return None
    mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}[p.suffix.lower()]
    return (f'<img src="data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}" alt="" '
            f'style="height:{alto}px;max-width:{max_ancho}px;object-fit:contain;object-position:{lado} center;display:block;flex:none">')


def cuerpo_slide(subtitulo, visual, banda=None, estilo_vis="", estilo_banda="", pre_pie=None, rotulo_banda=None):
    """Cuerpo estándar bajo ea_deck.cabecera(): subtítulo, visual que llena el espacio libre (alto_cuerpo da su alto; 02-11-2026) y banda de conclusión (una conclusión que aporta, no un resumen de lo que se ve; **negrita** en una parte).
    rotulo_banda: rótulo a la izquierda de la banda («Conclusión», «Asunción clave», «Implicación»)."""
    if banda and rotulo_banda:
        b = (f'<div class="banda banda-r" style="{estilo_banda}"><b class="br">{E(rotulo_banda)}</b><div>{md(banda)}</div></div>')
    else:
        b = f'<div class="banda" style="{estilo_banda}">{md(banda)}</div>' if banda else ""
    return ((f'<p class="sub">{E(subtitulo)}</p>' if subtitulo else "") +
            f'<div class="vis" style="{estilo_vis}">{visual}</div>' +
            (f'<p class="pre-foot">{pre_pie}</p>' if pre_pie else "") + b)


CSS = """
/* ---- ea_visuals: lienzo y texto ---- */
.lz{position:relative;flex:none;}
.lz-svg{position:absolute;left:0;top:0;overflow:visible;}
.lz-t{position:absolute;font-size:14px;line-height:1.35;color:var(--fg2);}
.lz-t b{color:var(--fg1);font-weight:600;}
.lz-t .k{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--fg3);margin-bottom:3px;}
.lz-t.red{color:var(--red);} .lz-t.red b{color:var(--red);}
.lz-t.on-red{color:#fff;} .lz-t.on-red b{color:#fff;}
.lz-t.big{font-size:15px;}
/* ---- píldoras ---- */
.pl{display:inline-block;font-size:12px;font-weight:600;line-height:1;padding:5px 10px;border-radius:999px;white-space:nowrap;}
.pl-red{background:var(--red);color:#fff;}
.pl-rosa{background:var(--brand-tint);color:var(--red);}
.pl-neutral{background:var(--surface-fill);color:var(--fg2);}
.pl-sand{background:var(--dark-cream);color:var(--fg1);}
.pl-out{background:#fff;color:var(--fg2);box-shadow:inset 0 0 0 1px var(--input);}
.pl-burg{background:var(--burgundy);color:var(--cream);}
/* ---- cuerpo de slide: subtítulo, visual y banda (gris claro, esquinas rectas) ---- */
.sub{font-size:16px;color:var(--fg2);line-height:1.4;margin:-12px 0 18px;max-width:1040px;}
.vis{flex:1;min-height:0;display:flex;gap:28px;align-items:stretch;margin-bottom:14px;}
.banda{margin-top:auto;margin-bottom:16px;background:var(--surface-fill);border-left:3px solid var(--red);border-radius:0;padding:15px 20px;
font-size:15px;color:var(--fg1);line-height:1.4;}
.banda b{font-weight:600;}
.banda-r{display:grid;grid-template-columns:120px 1fr;column-gap:18px;align-items:center;}
.banda-r .br{font-size:14px;font-weight:700;color:var(--fg1);}
.pre-foot{font-size:12px;color:var(--fg3);margin:8px 0 0;}
.hueco{background:#FFF1B8;color:var(--fg1);font-weight:600;padding:1px 6px;border-radius:4px;white-space:nowrap;}
/* ---- tarjetas, rótulos y cifras ---- */
.row{display:flex;gap:20px;align-items:stretch;}
.col{display:flex;flex-direction:column;gap:14px;min-width:0;}
.card{border:1px solid var(--border-1);border-radius:16px;padding:16px 18px;background:#fff;font-size:14px;line-height:1.45;color:var(--fg2);}
.card h4{font-size:15px;font-weight:600;margin:0 0 6px;color:var(--fg1);letter-spacing:-.005em;}
.card b,.tx b{color:var(--fg1);font-weight:600;}
.card.cream{background:var(--surface-fill);border-color:var(--surface-fill);}
.card.hot{border-color:var(--red);}
.nb{flex:none;width:34px;height:34px;border-radius:9px;background:var(--red);color:#fff;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;}
.nhead{display:flex;align-items:center;gap:12px;margin-bottom:10px;}
.nhead h4{margin:0;}
.k2{display:block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--fg3);margin-bottom:6px;}
.k2.red{color:var(--red);}
.big{font-size:40px;font-weight:600;letter-spacing:-.03em;line-height:1;color:var(--red);font-variant-numeric:tabular-nums;}
.gris{font-size:13px;color:var(--fg3);margin:10px 0 0;line-height:1.4;}
.it{font-style:italic;}
.nw{white-space:nowrap;}
.tile{background:#fff;border-radius:12px;display:flex;align-items:center;gap:10px;padding:10px 12px;font-size:14px;line-height:1.3;color:var(--fg1);}
.tile b{font-weight:600;}
.it3{display:flex;gap:12px;align-items:baseline;font-size:14px;line-height:1.45;color:var(--fg2);}
.it3 .dot{flex:none;width:40px;display:flex;justify-content:center;}
.it3 .dot i{width:7px;height:7px;border-radius:99px;background:var(--red);display:block;transform:translateY(-2px);}
/* ---- tablas ---- */
table.tb{width:100%;border-collapse:separate;border-spacing:0;font-size:14px;line-height:1.35;}
table.tb th{text-align:left;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--fg3);padding:0 10px 8px;border-bottom:1.5px solid var(--fg1);}
table.tb td{padding:9px 10px;border-bottom:1px solid var(--border-2);vertical-align:middle;color:var(--fg2);}
table.tb td.nm{color:var(--fg1);font-weight:600;}
table.tb td.nm b{color:var(--red);}
table.tb td.dt b{color:var(--fg1);font-weight:700;}
/* ---- KPI ---- */
.mB-l{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--red);margin:0 0 4px;}
.mB-l.g{color:var(--fg3);}
.mB-c{flex:1;border:1px solid var(--border-1);border-radius:16px;background:#fff;padding:13px 18px;display:flex;flex-direction:column;gap:7px;}
.mB-c.hot{border-color:var(--red);}
.mB-val{font-size:13px;color:var(--fg2);border-top:1px solid var(--border-2);padding-top:7px;margin-top:auto;}
.mB-val b{color:var(--fg1);font-weight:600;}
/* ---- scorecard ---- */
.sc{flex:1;align-self:stretch;width:100%;display:flex;flex-direction:column;background:#fff;border:1px solid var(--border-1);box-shadow:var(--shadow-sm);}
.sc-h{background:var(--red);color:#fff;font-size:14px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:7px 24px;}
.sc-b{display:grid;grid-template-columns:56px 1fr 1fr;column-gap:40px;align-items:stretch;padding:18px 32px 20px 28px;}
.sc-i{display:flex;align-items:center;justify-content:center;}
.sc .el{font-size:14px;line-height:1.4;color:var(--fg2);}
.sc .el b{color:var(--fg1);font-weight:700;}
.cr b{display:block;font-size:14px;font-weight:700;color:var(--fg1);margin-bottom:6px;}
.cr-b{display:flex;align-items:center;gap:14px;}
.cr-t{flex:1;height:10px;background:var(--surface-fill);position:relative;}
.cr-t i{position:absolute;left:0;top:0;bottom:0;background:var(--red);}
.cr-b span{width:40px;text-align:right;font-size:14px;font-weight:700;color:var(--red);}
/* ---- Gantt (prefijo cg-) ---- */
.cg{position:relative;width:100%;border:1px solid var(--border-1);border-radius:var(--radius-lg);overflow:hidden;background:var(--paper);}
.cg-head,.cg-row{display:grid;}
.cg-lab{padding:0 16px;display:flex;flex-direction:column;justify-content:center;font-size:13px;color:var(--fg2);line-height:1.3;}
.cg-lab b{font-size:14px;font-weight:700;color:var(--fg1);}
.cg-head{background:var(--cream);border-bottom:1px solid var(--dark-cream);}
.cg-time{position:relative;}
.cg-meses{position:relative;height:24px;}
.cg-mes{position:absolute;top:0;height:24px;display:flex;align-items:center;padding-left:8px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.10em;color:var(--fg1);border-left:1px solid var(--dark-cream);}
.cg-sems{position:relative;height:18px;}
.cg-sem{position:absolute;top:0;height:18px;display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--fg3);font-variant-numeric:tabular-nums;}
.cg-row{height:54px;border-top:1px solid var(--border-2);position:relative;}
.cg-cap{position:absolute;top:37px;font-size:12px;font-weight:700;color:var(--fg1);white-space:nowrap;font-variant-numeric:tabular-nums;}
.cg-cap.r{transform:translateX(-100%);}
.cg-grid{position:absolute;inset:0;pointer-events:none;}
.cg-gl{position:absolute;top:0;bottom:0;width:1px;background:var(--border-2);opacity:.7;}
.cg-gm{position:absolute;top:0;bottom:0;width:1px;background:var(--dark-cream);}
.cg-bar{position:absolute;border-radius:var(--radius-pill);display:flex;align-items:center;padding:0 10px;font-size:12px;font-weight:500;color:var(--brand-fg);white-space:nowrap;overflow:hidden;}
.cg-bar.prop{background:var(--red);}
.cg-bar.pausa{background:var(--dark-cream);color:var(--fg2);justify-content:center;border-radius:0;}
.cg-body{position:relative;}
.cg-hoy{position:absolute;top:0;bottom:0;width:0;border-left:1px dashed var(--fg3);z-index:3;pointer-events:none;}
.cg-hoy .pt{position:absolute;left:-6px;top:-5px;width:11px;height:11px;border-radius:50%;background:var(--yellow);box-shadow:0 0 0 5px rgba(255,161,3,.22);}
.cg-hoy .tx{position:absolute;left:10px;top:37px;white-space:nowrap;font-size:12px;font-weight:700;color:var(--fg1);background:var(--paper);padding:0 6px;border-radius:var(--radius-pill);}
.cg-dline{position:absolute;top:0;bottom:0;width:0;border-left:1.5px dotted var(--burgundy);z-index:2;pointer-events:none;}
.cg-dline .dd{position:absolute;left:-7px;bottom:21px;width:12px;height:12px;border-radius:50%;background:var(--burgundy);}
.cg-pill{position:absolute;top:7px;background:var(--burgundy);color:var(--cream);border-radius:var(--radius-pill);padding:6px 16px;display:flex;flex-direction:column;gap:1px;z-index:3;}
.cg-pill b{font-size:13px;font-weight:700;}
.cg-pill span{font-size:12px;opacity:.9;white-space:nowrap;}
.cg-leg{display:flex;align-items:center;gap:24px;margin-top:8px;font-size:13px;color:var(--fg2);}
.cg-leg .sw{display:inline-block;width:28px;height:10px;border-radius:var(--radius-pill);margin-right:8px;vertical-align:middle;}
"""


def _rampa_pasos(n):
    base = [RAMP[4], RAMP[3], RAMP[1], BURG] if n == 4 else ([RAMP[4], RAMP[3], RAMP[2], RAMP[1], RAMP[0], BURG])
    if n == 4:
        return base
    idx = [round(i * (len(base) - 1) / max(n - 1, 1)) for i in range(n)]
    return [base[i] for i in idx]


YELLOW = T["yellow"]


def fmt(x):
    """Número en formato español: coma decimal y punto de miles (4.200, 1.150), como en los informes de EA."""
    t = _fmt_simple(x)
    signo, t = ("-", t[1:]) if t.startswith("-") else ("", t)
    ent, _, dec = t.partition(",")
    if len(ent) > 3:
        ent = f"{int(ent):,}".replace(",", ".")
    return signo + ent + ("," + dec if dec else "")


NEUTRO = INPUT        # barras y puntos que no son el foco


def _hex(c):
    return [int(c[i:i + 2], 16) for i in (1, 3, 5)]


def mezcla(c1, c2, t):
    """Color intermedio entre c1 y c2 (t de 0 a 1)."""
    a, b = _hex(c1), _hex(c2)
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def rampa(n):
    """n colores de la rampa de rojos, de oscuro a claro. Hasta 5 salen de la rampa canónica; con más se
    interpola (a partir de 6 categorías conviene agrupar)."""
    sel = {1: [2], 2: [1, 4], 3: [0, 2, 4], 4: [0, 2, 3, 4], 5: [0, 1, 2, 3, 4]}
    if n <= 5:
        return [RAMP[i] for i in sel[max(n, 1)]]
    out = []
    for i in range(n):
        p = i * 4 / (n - 1)
        k = min(int(p), 3)
        out.append(mezcla(RAMP[k], RAMP[k + 1], p - k))
    return out


def calor(t):
    """Color continuo de 0 (gris cálido) a 1 (rojo oscuro), para mapas de calor."""
    stops = [FILL, RAMP[4], RAMP[3], RAMP[1], RAMP[0]]
    t = max(0, min(1, t)) * (len(stops) - 1)
    k = min(int(t), len(stops) - 2)
    return mezcla(stops[k], stops[k + 1], t - k)


def _svg(w, h, cuerpo, defs=""):
    d = f"<defs>{defs}</defs>" if defs else ""
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" '
            f'style="display:block;overflow:visible;flex:none">{d}{cuerpo}</svg>')


def _paso(maximo, n=4):
    """Paso de eje «redondo» para unas n divisiones."""
    bruto = maximo / n
    mag = 10 ** math.floor(math.log10(bruto))
    for m in (1, 2, 2.5, 5, 10):
        if m * mag >= bruto - 1e-12:
            return m * mag


def _bv(x, y, w, h, c, r=3):
    """Barra vertical con las esquinas de arriba redondeadas."""
    r = max(0, min(r, w / 2, h))
    return (f'<path d="M{x:.1f},{y + h:.1f}V{y + r:.1f}Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f}H{x + w - r:.1f}'
            f'Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f}V{y + h:.1f}Z" fill="{c}"/>')


def _arco(cx, cy, r, a0, a1):
    """Arco de a0 a a1 (radianes, 0 a la derecha, sentido horario en pantalla)."""
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    grande = 1 if (a1 - a0) % (2 * math.pi) > math.pi else 0
    return f"M{x0:.1f},{y0:.1f} A{r:.1f},{r:.1f} 0 {grande} 1 {x1:.1f},{y1:.1f}"


def _set(x):
    if x is None:
        return set()
    return set(x) if isinstance(x, (list, tuple, set)) else {x}


def arrow_eje(x1, y1, x2, y2):
    """Eje con punta de flecha fina."""
    return line(x1, y1, x2, y2, FG2, 1.2) + head(x2, y2, math.atan2(y2 - y1, x2 - x1), FG2, 7)


def _impacto(nivel, tam=22):
    """Flecha de impacto en círculo: 2 sube fuerte, 1 sube, 0 estable, -1 baja, -2 baja fuerte (verde, gris y rojo)."""
    c = {2: VALIDACION, 1: mezcla(VALIDACION, "#FFFFFF", .4), 0: FG4, -1: mezcla(RED, "#FFFFFF", .35), -2: RED}[nivel]
    ang = {2: -90, 1: -45, 0: 0, -1: 45, -2: 90}[nivel]
    r = tam / 2
    fl = (f'<g transform="rotate({ang} {r} {r})"><path d="M{r - 5},{r} H{r + 5} M{r + 1},{r - 4} L{r + 5},{r} L{r + 1},{r + 4}" fill="none" '
          f'stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return f'<span style="display:inline-block;vertical-align:middle;line-height:0">{_svg(tam, tam, circle(r, r, r, c) + fl)}</span>'

# ================================================================== maquetación (Reglas de uso de elementos.md, sección 2)
ANCHO_CUERPO = 1152     # ancho útil del cuerpo de una slide de ea_deck (1280 menos dos márgenes de 64)
HUECO = 28              # separación entre columnas; entre filas, 14
REJILLAS = {            # anchos de columna de las cinco rejillas tipo
    "A": (1152,),               # una pieza a todo ancho
    "B": (680, 444),            # pieza y lectura (o 444 y 680, la lectura a la izquierda)
    "C": (562, 562),            # dos piezas hermanas
    "D": (1152,),               # fila de cifras arriba y pieza debajo (las dos a todo ancho)
    "E": (365, 365, 366),       # tres columnas hermanas
    "F": (360, 764),            # columna de contexto (columna_contexto) y pieza
}


def alto_cuerpo(lineas_titulo=2, subtitulo=True, banda=0, nota=0):
    """Alto en px que queda para el visual de una slide de contenido, para dárselo a las piezas (H) y que el cuerpo
    llene la slide (02-11-2026). lineas_titulo: 1 o 2. banda y nota: número de líneas de cada una (0, sin ella)."""
    alto = 720 - 48 - 34 - 32 * lineas_titulo - 24 - 14 - 47      # márgenes, eyebrow, título, su margen, .vis y pie
    alto -= 29 if subtitulo else 0
    alto -= 46 + 21 * banda if banda else 0
    alto -= 8 + 16 * nota if nota else 0
    return int(alto)


def fila(*piezas, anchos=None, gap=HUECO, alinear="stretch", vertical="center", crecer=False):
    """Piezas en fila, cada una en una columna de ancho fijo (px) y todas del mismo alto (A1).
    anchos: tupla de REJILLAS o propia; None reparte a partes iguales. alinear: stretch, center o flex-end
    (flex-end alinea las bases, para gráficas con eje). vertical: dónde va el contenido dentro de cada columna
    (center, o flex-start cuando las columnas llevan rótulo de bloque y tienen que arrancar a la misma altura).
    crecer: dentro de una columna, la fila ocupa el alto que sobre (para tarjetas que tienen que llegar al pie del bloque)."""
    anchos = anchos or [None] * len(piezas)
    cols = "".join(f'<div style="{f"width:{a}px;flex:none;" if a else "flex:1;"}min-width:0;display:flex;flex-direction:column;'
                   f'justify-content:{vertical}">{p}</div>' for p, a in zip(piezas, anchos))
    return f'<div style="display:flex;gap:{gap}px;align-items:{alinear};width:100%;{"flex:1;" if crecer else ""}">{cols}</div>'


def columna(*piezas, gap=14, ancho=None, centrar=False, repartir=False):
    """Piezas apiladas con separación fija; centrar: centra cada pieza a lo ancho; repartir: reparte el alto sobrante
    entre las piezas, para que la columna llene el cuerpo sin estirarlas."""
    st = (f"width:{ancho}px;flex:none;" if ancho else "flex:1;") + ("align-items:center;" if centrar else "") + ("justify-content:space-between;height:100%;" if repartir else "")
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px;min-width:0;{st}">{"".join(piezas)}</div>'


def rotulo_bloque(texto, rojo=False):
    """Rótulo de un bloque dentro de la slide, visible (C7): 700, 13,5 px, negro o rojo."""
    return f'<div style="font-size:14px;font-weight:700;color:var(--{"red" if rojo else "fg1"});margin:0 0 8px">{E(texto)}</div>'


def _logo_html(x, alto=26):
    """Logo como HTML: se pasa tal cual si ya es HTML (un <img> de logo()) y, si es un nombre, sale en texto como monograma."""
    if str(x).lstrip().startswith("<"):
        return x
    return (f'<span style="display:inline-flex;align-items:center;height:{alto}px;font-size:{alto * .5:.0f}px;font-weight:700;'
            f'letter-spacing:.02em;color:var(--fg2);white-space:nowrap">{E(x)}</span>')
