"""Marcos y matrices: cómo se organiza una idea en un esquema.

Familia 06 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (
    BORDER2, E, FG1, FG2, FG3, FG4, FILL, FONT, GREY, INPUT, Lienzo, PAPER, RAMP, RED, TINT, arrow_eje,
    circle, flecha_svg, icono, line, md, mezcla, pill, rampa, rect, sobre, text,
)
from .marcas import (harvey, leyenda)

__all__ = ["nucleo_dos_lados", "escalera_prioridad", "columnas_evolucion", "matriz_2x2", "venn", "circulos_concentricos", "radial", "piramide", "capas", "balanza", "lienzo_negocio", "mapa_alcance", "dafo", "cinco_fuerzas", "pilares", "convergencia"]


_EFECTO = {"suma": RED, "cero": FG3, "resta": FG1}


def nucleo_dos_lados(izq, der, nucleo, nota_centro="", W=1152, ancho_lado=392, paso=64):
    """Dos mitades que se abren desde un núcleo común: a cada lado, una cabecera y filas con su efecto,
    unidas por curvas discontinuas a un anillo partido en dos alrededor del núcleo.
    izq y der: {"codigo", "nombre", "titular", "texto", "color", "filas": [(nombre, detalle, cifra, unidad, efecto)]}
    con efecto 'suma' (rojo), 'cero' (gris) o 'resta' (negro). nucleo = (título, texto). nota_centro: HTML arriba.
    Cuándo usarlo: dos capas o palancas complementarias que se combinan con una pieza central (proceso y conservación
    alrededor del ingrediente); de 3 a 6 filas por lado, el mismo número a los dos lados.
    Cuándo no: si las dos mitades no comparten núcleo (usa dos columnas) o si hay más de dos capas."""
    n = max(len(izq["filas"]), len(der["filas"]))
    y0 = 82
    H = y0 + n * paso + 6
    cx, cy = W / 2, y0 + ((n - 1) * paso + paso - 10) / 2
    L = Lienzo(W, H)
    for lado_, (x, anc) in ((izq, (0, "start")), (der, (W, "end"))):
        al = "left" if anc == "start" else "right"
        L.div(x, 0, ancho_lado, f'<div style="text-align:{al}"><span class="k2 red" style="margin:0 0 2px">{E(lado_["codigo"])} · {E(lado_["nombre"])}</span>'
                                f'<b style="display:block;font-size:24px;line-height:1.15;color:var(--fg1);letter-spacing:-.01em">{E(lado_["titular"])}</b>'
                                f'<span style="font-size:13px;color:var(--fg2)">{E(lado_["texto"])}</span></div>', anchor=anc)
    span = 104 / (n - 1) if n > 1 else 0
    for lado, d in ((-1, izq), (1, der)):
        for k, (nom, det, v, u, efecto) in enumerate(d["filas"]):
            y = y0 + k * paso
            x = 0 if lado < 0 else W - ancho_lado
            L.add(rect(x, y, ancho_lado, paso - 10, "#fff", rx=12, stroke=BORDER2))
            cifra = (f'<div style="width:92px;text-align:{"right" if lado < 0 else "left"}"><b style="display:block;font-size:17px;line-height:1.1;'
                     f'color:{_EFECTO[efecto]};white-space:nowrap">{E(v)}</b><span style="font-size:12px;color:var(--fg3)">{E(u)}</span></div>')
            txt = (f'<div style="flex:1;min-width:0;text-align:{"left" if lado < 0 else "right"}"><b style="display:block;font-size:14px;color:var(--fg1);line-height:1.25">{E(nom)}</b>'
                   f'<span style="font-size:13px;line-height:1.3">{E(det)}</span></div>')
            L.div(x + 14, y + (paso - 10) / 2, ancho_lado - 28, f'<div style="display:flex;align-items:center;gap:12px">{txt + cifra if lado < 0 else cifra + txt}</div>', va="middle")
            ang = math.radians(-52 + k * span)
            ax, ay = cx + lado * 128 * math.cos(ang), cy + 128 * math.sin(ang)
            x0 = ancho_lado if lado < 0 else W - ancho_lado
            L.add(f'<path d="M{x0},{y + (paso - 10) / 2:.1f} C{x0 - lado * 40:.1f},{y + (paso - 10) / 2:.1f} {ax + lado * 30:.1f},{ay:.1f} {ax:.1f},{ay:.1f}" '
                  f'fill="none" stroke="{FG4}" stroke-width="1.2" stroke-dasharray="3 3"/>', circle(ax, ay, 3, FG3))
    for lado, d in ((-1, izq), (1, der)):
        a0, a1 = (90, 270) if lado < 0 else (-90, 90)
        p = lambda r, a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p(128, a0), p(128, a1), p(80, a1), p(80, a0)
        L.add(f'<path d="M{x1:.1f},{y1:.1f} A128,128 0 0 1 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} A80,80 0 0 0 {x4:.1f},{y4:.1f} Z" fill="{d["color"]}" stroke="#fff" stroke-width="4"/>')
        L.div(cx + lado * 104, cy, 60, f'<b style="font-size:15px;color:{sobre(d["color"])}">{E(d["codigo"])}</b>', anchor="middle", va="middle")
    L.add(circle(cx, cy, 74, RED))
    L.div(cx, cy, 130, f'<b style="display:block;font-size:15px;color:#fff;line-height:1.2">{E(nucleo[0])}</b>'
                       f'<span style="font-size:13px;color:#fff">{E(nucleo[1])}</span>', anchor="middle", va="middle", style="text-align:center")
    if nota_centro:
        L.div(cx, 0, 300, f'<div style="font-size:13px;line-height:1.4;color:var(--fg2);text-align:center">{nota_centro}</div>', anchor="middle")
    return L.render()


def escalera_prioridad(niveles, W=1152, H=300):
    """Franjas de prioridad (alta, media, baja) del mismo alto, en rampa de rojos (oscuro arriba), con los focos
    como fichas y el perfil buscado bajo cada una.
    niveles: [(etiqueta, [(foco, perfil), ...])], de mayor a menor prioridad, hasta 3 niveles y 5 focos por nivel.
    Cuándo usarlo: la recomendación de dónde poner el esfuerzo y qué se busca en cada foco.
    Cuándo no: si la prioridad sale de una puntuación que hay que enseñar (usa antes matriz_puntuacion)."""
    tonos = [RAMP[1], RAMP[3], RAMP[4]]
    L = Lienzo(W, H)
    gap = 10
    h = (H - gap * (len(niveles) - 1)) / len(niveles)
    y = 0
    for k, (lab, focos) in enumerate(niveles):
        col = tonos[min(k, 2)]
        L.add(rect(0, y, W, h, col, rx=14, op=0.14), rect(0, y, 150, h, col, rx=14))
        L.div(20, y + h / 2, 120, f'<b style="font-size:17px;color:{sobre(col)}">{E(lab)}</b>', va="middle")
        n = len(focos)
        fw = (W - 150 - 16 - 12 * n) / n
        for j, (foco, perfil) in enumerate(focos):
            fx = 150 + 16 + j * (fw + 12)
            L.add(rect(fx, y + 10, fw, h - 20, PAPER, rx=12, stroke=GREY))
            L.div(fx + 16, y + h / 2, fw - 32, f'<b style="font-size:15px">{E(foco)}</b>'
                  f'<div style="font-size:14px;color:var(--fg2);line-height:1.4;margin-top:4px">{md(perfil)}</div>', va="middle")
        y += h + gap
    return L.render()


def columnas_evolucion(columnas, rotulo_flecha="mismo origen, otro producto", rotulos=("Ya probado", "Quién lo hace", "Reto")):
    """Columnas «de lo probado a lo nuevo»: arriba lo que ya se probó (gris), una flecha roja con el rótulo y debajo
    la tarjeta del producto nuevo con píldora, cifra, quién lo hace y su reto, todo al mismo alto en las columnas.
    columnas: [{"familia", "antes", "antes_dato", "nuevo", "pill", "cifra", "cifra_dato", "quien": [(logo_html, nombre,
    país, texto)], "reto"}]. Un solo actor por columna (o dos como máximo).
    Cuándo usarlo: hacer creíble con un ejemplo concreto un mensaje abstracto («lo nuevo es el producto»); 2 a 4 columnas.
    Cuándo no: si no hay una cifra por columna o si las columnas no comparten estructura."""
    def quien(lg, n, pa, t):
        return (f'<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;height:62px;padding:0 2px;border-top:1px solid var(--border-2)">'
                f'<div style="min-width:0;font-size:13px;line-height:1.35"><b style="color:var(--fg1);font-size:13px">{E(n)}</b>'
                + (f' <span style="color:var(--fg3)">({E(pa)})</span>' if pa else "") + f'<div>{E(t)}</div></div>'
                f'<div style="flex:none;display:flex;justify-content:flex-end;align-items:center">{lg or icono("groups", 22, FG3)}</div></div>')

    def col(k, c):
        return (f'<div class="col" style="flex:1;gap:0;min-width:0">'
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px"><span class="nb" style="width:28px;height:28px;font-size:13px">{k:02d}</span>'
                f'<span class="k2" style="margin:0;color:var(--fg1)">{E(c["familia"])}</span></div>'
                f'<div class="card cream" style="flex:none;padding:10px 16px"><span class="k2" style="margin:0 0 3px">{E(rotulos[0])}</span>'
                f'<b style="display:block;color:var(--fg1);font-size:14px;line-height:1.3">{E(c["antes"])}</b><span style="font-size:13px">{E(c["antes_dato"])}</span></div>'
                f'<div style="flex:none;display:flex;align-items:center;justify-content:center;gap:8px;height:34px;font-size:12px;color:var(--red);font-weight:600">'
                f'{flecha_svg(RED, 26, 20, 2.5, abajo=True)}{E(rotulo_flecha)}</div>'
                f'<div class="card hot" style="flex:1;padding:12px 16px;display:flex;flex-direction:column;gap:6px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><b style="color:var(--red);font-size:15px;line-height:1.25">{E(c["nuevo"])}</b>{pill(c["pill"], "rosa") if c.get("pill") else ""}</div>'
                f'<div style="display:flex;gap:12px;align-items:baseline;margin:2px 0 4px"><span class="big" style="font-size:34px;white-space:nowrap">{E(c["cifra"])}</span>'
                f'<span style="font-size:13px;line-height:1.35">{E(c["cifra_dato"])}</span></div>'
                f'<span class="k2" style="margin:2px 0 0">{E(rotulos[1])}</span>{"".join(quien(*q) for q in c["quien"])}'
                f'<div style="margin-top:auto;height:52px;display:flex;align-items:center;font-size:13px;line-height:1.4;color:var(--fg1);background:var(--surface-fill);padding:0 12px;border-radius:8px">'
                f'<span><b>{E(rotulos[2])}:</b> {md(c["reto"])}</span></div></div></div>')
    return f'<div class="row" style="flex:1;gap:18px;align-self:stretch">{"".join(col(k + 1, c) for k, c in enumerate(columnas))}</div>'


def matriz_2x2(ejes, cuadrantes, items=(), destacado=1, W=520, H=380):
    """Matriz 2 × 2: dos ejes cualitativos, cuatro cuadrantes con nombre y elementos colocados encima.
    ejes = ((x_bajo, x_alto, nombre_x), (y_bajo, y_alto, nombre_y)); cuadrantes: 4 × (título, texto) en orden
    sup_izq, sup_der, inf_izq, inf_der; items: [(rótulo, x 0 a 1, y 0 a 1, destacado)]; destacado: cuadrante en rosa.
    Cuándo usarlo: priorizar con dos criterios (impacto y esfuerzo, atractivo y capacidad).
    Cuándo no: si hay datos numéricos fiables en ambos ejes (usa dispersion)."""
    izq, bot = 34, 34
    gw, gh = (W - izq) / 2, (H - bot) / 2
    L = Lienzo(W, H)
    pos = [(izq, 0), (izq + gw, 0), (izq, gh), (izq + gw, gh)]
    for k, ((x0, y0), (t, tx)) in enumerate(zip(pos, cuadrantes)):
        hot = k == destacado
        L.add(rect(x0 + 2, y0 + 2, gw - 4, gh - 4, mezcla(TINT, "#FFFFFF", .4) if hot else mezcla(FILL, "#FFFFFF", .55), rx=10))
        L.div(x0 + 16, y0 + 12, gw - 32, f'<b style="color:{RED if hot else FG1};font-size:14px">{E(t)}</b>'
              f'<div style="font-size:12px;color:var(--fg2);margin-top:2px;line-height:1.35">{md(tx)}</div>')
    (xb, xa, xn), (yb, ya, yn) = ejes
    L.add(arrow_eje(izq - 6, H - bot + 8, W, H - bot + 8), arrow_eje(izq - 6, H - bot + 8, izq - 6, 0))
    L.add(text(izq + 4, H - 6, xb, 11, 400, FG3), text(W - 4, H - 6, xa, 11, 400, FG3, "end"),
          text((izq + W) / 2, H - 6, xn, 12, 700, FG1, "middle"))
    L.add(f'<text transform="translate(16,{H - bot}) rotate(-90)" style="font-family:{FONT};font-size:11px;fill:{FG3}">{E(yb)}</text>',
          f'<text transform="translate(16,4) rotate(-90)" text-anchor="end" style="font-family:{FONT};font-size:11px;fill:{FG3}">{E(ya)}</text>',
          f'<text transform="translate(16,{(H - bot) / 2}) rotate(-90)" text-anchor="middle" style="font-family:{FONT};font-size:12px;font-weight:700;fill:{FG1}">{E(yn)}</text>')
    for r, px, py, hot in items:
        cx, cy = izq + px * (W - izq), (1 - py) * (H - bot)
        L.add(circle(cx, cy, 7, RED if hot else FG1, "#fff", 2), text(cx + 11, cy + 4, r, 12, 700 if hot else 600, RED if hot else FG1, halo=True))
    return L.render()


def venn(conjuntos, interseccion="", W=520, H=320):
    """Diagrama de Venn de 2 o 3 conjuntos, con título y texto en cada uno y la intersección rotulada.
    conjuntos: [(título, texto)]; interseccion: texto corto del centro (el «punto dulce»).
    Cuándo usarlo: definir un hueco o un perfil como cruce de condiciones (técnica, mercado, regulación).
    Cuándo no: para cuantificar solapes (los tamaños no son proporcionales)."""
    n = len(conjuntos)
    L = Lienzo(W, H)
    cols = rampa(n)
    if n == 2:
        r = H / 2 - 10
        cs = [(W / 2 - r * .62, H / 2), (W / 2 + r * .62, H / 2)]
        tx = [(cs[0][0] - r * .45, H / 2), (cs[1][0] + r * .45, H / 2)]
    else:
        r = H * .3
        cx, cy = W / 2, H / 2 + 8
        d = r * .66
        cs = [(cx - d * .87, cy - d * .5 + 4), (cx + d * .87, cy - d * .5 + 4), (cx, cy + d)]
        tx = [(cs[0][0] - r * .44, cs[0][1] - r * .22), (cs[1][0] + r * .44, cs[1][1] - r * .22), (cs[2][0], cs[2][1] + r * .48)]
    for (x, y), c in zip(cs, cols):
        L.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}" fill-opacity=".22" stroke="{c}" stroke-width="2"/>')
    ancho = r * (1.0 if n == 2 else .8)
    for (t, d), (x, y) in zip(conjuntos, tx):
        L.div(x, y, ancho, f'<b style="font-size:14px;color:var(--fg1)">{E(t)}</b>'
              f'<div style="font-size:12px;line-height:1.35;margin-top:2px">{md(d)}</div>', anchor="middle", va="middle")
    if interseccion:
        ix = W / 2
        iy = H / 2 if n == 2 else (sum(y for _, y in cs) / 3)
        L.div(ix, iy, r * .62, f'<span class="pl pl-red" style="white-space:normal;line-height:1.2">{E(interseccion)}</span>', anchor="middle", va="middle")
    return L.render()


def circulos_concentricos(niveles, W=520, H=300):
    """Círculos concéntricos apoyados en la base (TAM, SAM, SOM o de lo general a lo concreto), con la cifra
    y su lectura a la derecha.
    niveles: [(sigla, cifra, texto)] de fuera adentro; el interior va en rojo.
    Cuándo usarlo: tamaño de mercado por capas o un embudo de alcance sin etapas de filtro.
    Cuándo no: si las capas no están contenidas unas en otras."""
    n = len(niveles)
    R = H / 2 - 4
    cx = R + 4
    cols = [mezcla(TINT, RAMP[4], i / max(n - 1, 1)) for i in range(n - 1)] + [RED]
    L = Lienzo(W, H)
    rs = [R * (1 - .3 * i) for i in range(n)]
    for (sig, cif, tx), r, c, i in zip(niveles, rs, cols, range(n)):
        cy = H - 4 - r
        L.add(circle(cx, cy, r, c))
        ytop = cy - r + 18
        L.add(text(cx, ytop + 4, sig, 13, 700, sobre(c), "middle"))
        L.add(line(cx + 22, ytop, 2 * cx + 20, ytop, FG4, 1, dash="2 3"), circle(cx + 22, ytop, 2.5, sobre(c)))
        L.div(2 * cx + 30, ytop, W - 2 * cx - 30, f'<b style="font-size:20px;color:{RED if i == n - 1 else FG1}">{E(cif)}</b> '
              f'<span style="font-size:13px;color:var(--fg2)">{md(tx)}</span>', va="middle")
    return L.render()


def radial(centro, satelites, W=520, H=360, radio=None):
    """Radial (hub and spoke): un centro y de 4 a 8 satélites con icono y rótulo, unidos por radios.
    centro: texto corto; satelites: [(icono, rótulo, texto)].
    Cuándo usarlo: un actor o una capacidad con sus relaciones o componentes (ecosistema, plataforma).
    Cuándo no: si hay relaciones entre satélites o un orden (usa ciclo o chevrones)."""
    cx, cy = W / 2, H / 2
    R = radio or min(W, H) / 2 - 66
    n = len(satelites)
    L = Lienzo(W, H)
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        L.add(line(cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), FG4, 1.2, dash="3 4"))
    L.add(circle(cx, cy, 58, RED), circle(cx, cy, 70, "none", RED, 1))
    L.div(cx, cy, 100, f'<b style="color:#fff;font-size:14px;line-height:1.2">{E(centro)}</b>', anchor="middle", va="middle")
    for i, (ic, r, tx) in enumerate(satelites):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        L.add(circle(x, y, 26, PAPER, GREY, 1.5))
        L.div(x, y, 52, icono(ic, 24, RED), anchor="middle", va="middle", style="line-height:0")
        c = math.cos(a)
        if abs(c) < .25:
            L.div(x, y + (34 if math.sin(a) > 0 else -34), 170, f'<b style="font-size:13px;color:var(--fg1)">{E(r)}</b>'
                  + (f'<div style="font-size:12px">{E(tx)}</div>' if tx else ""), anchor="middle", va="top" if math.sin(a) > 0 else "bottom")
        else:
            L.div(x + (34 if c > 0 else -34), y, 120, f'<b style="font-size:13px;color:var(--fg1)">{E(r)}</b>'
                  + (f'<div style="font-size:12px;line-height:1.3">{E(tx)}</div>' if tx else ""), anchor="start" if c > 0 else "end", va="middle")
    return L.render()


def piramide(niveles, W=520, H=300, ancho=320):
    """Pirámide de niveles (de la base a la cima) con el rótulo dentro y la explicación a la derecha.
    niveles: [(rótulo, texto)] de la cima a la base; la cima va en el rojo más oscuro.
    Cuándo usarlo: jerarquías de necesidad o de valor (higiene, diferenciación, liderazgo).
    Cuándo no: si los niveles no se apoyan unos en otros (usa capas o una lista)."""
    n = len(niveles)
    cols = rampa(n)
    g = 4
    h = (H - g * (n - 1)) / n
    L = Lienzo(W, H)
    mx = ancho / 2
    for i, ((r, tx), c) in enumerate(zip(niveles, cols)):
        y0 = i * (h + g)
        y1 = y0 + h
        w0, w1 = ancho * y0 / H / 2, ancho * y1 / H / 2
        L.add(f'<polygon points="{mx - w0:.1f},{y0:.1f} {mx + w0:.1f},{y0:.1f} {mx + w1:.1f},{y1:.1f} {mx - w1:.1f},{y1:.1f}" fill="{c}"/>')
        L.div(mx, y0 + h * (.7 if i == 0 else .5), max(w1 * 1.6, 70), f'<b style="font-size:{11.5 if i == 0 else 12}px;color:{sobre(c)}">{E(r)}</b>',
              anchor="middle", va="middle")
        ym = (y0 + y1) / 2
        L.add(line(mx + (w0 + w1) / 2 + 8, ym, ancho + 24, ym, FG4, 1, dash="2 3"))
        L.div(ancho + 32, ym, W - ancho - 32, f'<span style="font-size:13px;line-height:1.35">{md(tx)}</span>', va="middle")
    return L.render()


def capas(capas_, W=520):
    """Capas apiladas (stack): de la base, abajo, a la aplicación, arriba, con icono, rótulo y texto.
    capas_: [(icono, rótulo, texto)] de arriba abajo; la base en el rojo más oscuro.
    Cuándo usarlo: arquitecturas o modelos de capacidades que se apoyan unos en otros (datos, plataforma, servicios).
    Cuándo no: si no hay dependencia entre capas (usa lista_numerada)."""
    n = len(capas_)
    cols = list(reversed(rampa(n)))
    filas = "".join(
        f'<div style="display:flex;align-items:center;gap:14px;background:{c};border-radius:10px;padding:10px 16px;'
        f'margin:0 {(n - 1 - i) * 0}px">{icono(ic, 24, sobre(c))}'
        f'<b style="width:120px;flex:none;font-size:14px;color:{sobre(c)}">{E(r)}</b>'
        f'<span style="font-size:13px;line-height:1.35;color:{sobre(c)};opacity:.92">{md(tx)}</span></div>'
        for i, ((ic, r, tx), c) in enumerate(zip(capas_, cols)))
    return f'<div style="display:flex;flex-direction:column;gap:5px;width:{W}px">{filas}</div>'


def balanza(izquierda, derecha, inclinacion=7, W=520, H=270):
    """Balanza: dos platos con los argumentos de cada lado, inclinada hacia el que pesa más.
    izquierda y derecha = (título, [puntos]); inclinacion en grados (positivo: baja y pesa más la derecha).
    Cuándo usarlo: una decisión con pros y contras, o dos alternativas que se comparan en conjunto.
    Cuándo no: si los argumentos se pueden puntuar (usa tabla_comparativa o scorecard)."""
    cx, yb = W / 2, 64
    L = Lienzo(W, H)
    a = math.radians(inclinacion)
    lb = W / 2 - 70
    p1 = (cx - lb * math.cos(a), yb - lb * math.sin(a))
    p2 = (cx + lb * math.cos(a), yb + lb * math.sin(a))
    L.add(f'<polygon points="{cx},{yb} {cx - 22},{H - 4} {cx + 22},{H - 4}" fill="{FG2}"/>', rect(cx - 60, H - 8, 120, 6, FG2, rx=3))
    L.add(line(*p1, *p2, FG1, 4, cap="round"), circle(cx, yb, 7, RED))
    for (t, pts), (px, py), hot in ((izquierda, p1, inclinacion < 0), (derecha, p2, inclinacion > 0)):
        L.add(line(px, py, px - 50, py + 26, FG3, 1.2), line(px, py, px + 50, py + 26, FG3, 1.2))
        L.add(f'<path d="M{px - 62:.1f},{py + 26:.1f} Q{px:.1f},{py + 44:.1f} {px + 62:.1f},{py + 26:.1f} Z" fill="{RED if hot else FG4}"/>')
        L.div(px, py + 50, 200, f'<b style="font-size:14px;color:{RED if hot else FG1}">{E(t)}</b>' + "".join(
            f'<div style="font-size:13px;line-height:1.4;margin-top:3px">{md(p)}</div>' for p in pts), anchor="middle")
    return L.render()


def lienzo_negocio(bloques, destacado=None, W=1100, H=410):
    """Lienzo de modelo de negocio (business model canvas): las nueve cajas con icono, título y puntos.
    bloques: dict con las claves socios, actividades, recursos, propuesta, relaciones, canales, segmentos,
    costes e ingresos (listas de textos cortos); destacado: clave de la caja en rosa (la que cambia).
    Cuándo usarlo: el modelo de una startup candidata o el de un negocio nuevo del cliente, en una slide.
    Cuándo no: para análisis de detalle de una sola caja (sácala a su propia slide)."""
    cajas = {"socios": ("handshake", "Socios clave", "1 / 3", "1 / 3"), "actividades": ("checklist", "Actividades clave", "3 / 5", "1 / 2"),
             "recursos": ("inventory_2", "Recursos clave", "3 / 5", "2 / 3"), "propuesta": ("diamond", "Propuesta de valor", "5 / 7", "1 / 3"),
             "relaciones": ("groups", "Relación con clientes", "7 / 9", "1 / 2"), "canales": ("local_shipping", "Canales", "7 / 9", "2 / 3"),
             "segmentos": ("storefront", "Segmentos de clientes", "9 / 11", "1 / 3"), "costes": ("payments", "Estructura de costes", "1 / 6", "3 / 4"),
             "ingresos": ("savings", "Fuentes de ingresos", "6 / 11", "3 / 4")}
    out = []
    for k, (ic, t, col, row) in cajas.items():
        hot = k == destacado
        items = "".join(f'<li>{md(x)}</li>' for x in bloques.get(k, []))
        out.append(f'<div style="grid-column:{col};grid-row:{row};background:{TINT if hot else "#fff"};border:1px solid {RED if hot else "var(--border-1)"};'
                   f'border-radius:12px;padding:12px 14px;min-height:0;overflow:hidden">'
                   f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">{icono(ic, 20, RED)}'
                   f'<b style="font-size:13px;color:{RED if hot else FG1}">{E(t)}</b></div>'
                   f'<ul style="margin:0;padding-left:16px;font-size:12px;line-height:1.4;color:var(--fg2)">{items}</ul></div>')
    return (f'<div style="display:grid;grid-template-columns:repeat(10,1fr);grid-template-rows:1fr 1fr .8fr;gap:8px;width:{W}px;height:{H}px;'
            f'background:var(--surface-fill);padding:8px;border-radius:14px">{"".join(out)}</div>')


def mapa_alcance(dimensiones, rotulos=("Dentro del alcance", "En parte", "Fuera"), W=1100):
    """Mapa de alcance (taxonomía): una columna por dimensión (segmento, proceso, aplicación, región) con sus
    opciones en cajas que dicen si entran en el alcance, entran en parte o quedan fuera.
    dimensiones: [(nombre, [(opción, 'dentro' | 'parcial' | 'fuera')])].
    Cuándo usarlo: fijar el alcance de un scouting, una vigilancia o un dimensionamiento antes de empezar.
    Cuándo no: si el alcance es una sola lista (usa lista_numerada o pills)."""
    est = {"dentro": ("var(--red)", "#fff", "var(--red)"), "parcial": (TINT, RED, mezcla(RED, "#FFFFFF", .55)),
           "fuera": ("#fff", FG4, INPUT)}
    cols = []
    for i, (nom, ops) in enumerate(dimensiones):
        cajas = "".join(f'<div style="background:{est[e][0]};color:{est[e][1]};border:1px {"dashed" if e == "parcial" else "solid"} {est[e][2]};'
                        f'border-radius:8px;padding:7px 10px;font-size:13px;font-weight:{600 if e != "fuera" else 400};line-height:1.25">{E(o)}</div>'
                        for o, e in ops)
        cols.append(f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:6px">'
                    f'<div style="display:flex;align-items:center;gap:8px;border-bottom:1.5px solid var(--fg1);padding-bottom:6px;margin-bottom:4px">'
                    f'<span class="nb" style="width:24px;height:24px;font-size:13px;border-radius:7px">{i + 1}</span><b style="font-size:14px;color:var(--fg1)">{E(nom)}</b></div>{cajas}</div>')
    ley = leyenda([(RED, rotulos[0]), (TINT, rotulos[1]), (INPUT, rotulos[2])])
    return f'<div style="width:{W}px;display:flex;flex-direction:column;gap:14px">{ley}<div style="display:flex;gap:16px">{"".join(cols)}</div></div>'


def dafo(fortalezas, debilidades, oportunidades, amenazas, W=520):
    """DAFO: fortalezas y debilidades (internas) arriba, oportunidades y amenazas (externas) abajo, con la letra
    en rojo y puntos breves.
    Cada argumento: lista de textos cortos (3 a 5).
    Cuándo usarlo: diagnóstico rápido de una empresa, una tecnología o una opción de entrada.
    Cuándo no: como conclusión (el DAFO ordena, no decide; acompáñalo de la recomendación)."""
    def celda(letra, titulo, items):
        lis = "".join(f'<li>{md(t)}</li>' for t in items)
        return (f'<div style="background:{mezcla(FILL, "#FFFFFF", .45)};border-radius:12px;padding:12px 14px">'
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px"><span class="nb" style="width:28px;height:28px;font-size:14px;border-radius:8px">{letra}</span>'
                f'<b style="font-size:14px;color:var(--fg1)">{titulo}</b></div>'
                f'<ul style="margin:0;padding-left:18px;font-size:13px;line-height:1.45;color:var(--fg2)">{lis}</ul></div>')
    lat = lambda t: f'<div style="writing-mode:vertical-rl;transform:rotate(180deg);font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--fg3);text-align:center">{t}</div>'
    return (f'<div style="width:{W}px;display:grid;grid-template-columns:18px 1fr 1fr;gap:8px">'
            f'{lat("Interno")}{celda("F", "Fortalezas", fortalezas)}{celda("D", "Debilidades", debilidades)}'
            f'{lat("Externo")}{celda("O", "Oportunidades", oportunidades)}{celda("A", "Amenazas", amenazas)}</div>')


def cinco_fuerzas(fuerzas, W=520):
    """Cinco fuerzas de Porter: la rivalidad en el centro y las otras cuatro alrededor, cada una con su
    intensidad (bola de Harvey y palabra) y una línea de explicación.
    fuerzas: dict con las claves entrantes, proveedores, rivalidad, clientes y sustitutos = (intensidad 0 a 4, texto).
    Cuándo usarlo: atractivo de un sector o de un segmento en una propuesta o un diagnóstico.
    Cuándo no: si el análisis es de una sola empresa frente a sus competidores (usa tabla_comparativa)."""
    nivel = {0: "nula", 1: "baja", 2: "media", 3: "alta", 4: "muy alta"}
    tit = {"entrantes": "Nuevos entrantes", "proveedores": "Poder de los proveedores", "rivalidad": "Rivalidad del sector",
           "clientes": "Poder de los clientes", "sustitutos": "Productos sustitutos"}
    def caja(k):
        i, t = fuerzas[k]
        centro = k == "rivalidad"
        bg, fg, sub = (FG1, "#fff", "rgba(255,255,255,.8)") if centro else ("#fff", FG1, FG2)
        return (f'<div style="background:{bg};border:1px solid {FG1 if centro else "var(--border-1)"};border-radius:12px;padding:9px 11px;text-align:center">'
                f'<b style="font-size:13px;color:{fg};display:block;line-height:1.2">{tit[k]}</b>'
                f'<div style="display:flex;align-items:center;justify-content:center;gap:6px;margin:5px 0 3px">{harvey(i, 15, "#fff" if centro else RED)}'
                f'<span style="font-size:12px;font-weight:700;color:{fg}">Intensidad {nivel[i]}</span></div>'
                f'<div style="font-size:11px;line-height:1.3;color:{sub}">{md(t)}</div></div>')
    fl = lambda rot: f'<div style="display:flex;align-items:center;justify-content:center;transform:rotate({rot}deg)">{flecha_svg(FG3, 24, 14, 2)}</div>'
    vacio = "<div></div>"
    g = [vacio, vacio, caja("entrantes"), vacio, vacio,
         vacio, vacio, fl(90), vacio, vacio,
         caja("proveedores"), fl(0), caja("rivalidad"), fl(180), caja("clientes"),
         vacio, vacio, fl(-90), vacio, vacio,
         vacio, vacio, caja("sustitutos"), vacio, vacio]
    return (f'<div style="width:{W}px;display:grid;grid-template-columns:1fr 28px 1fr 28px 1fr;grid-template-rows:auto 26px auto 26px auto;'
            f'align-items:center">{"".join(g)}</div>')


def pilares(ambicion, pilares_, bases, W=1100, H=None):
    """Casa estratégica: la ambición en el tejado, los pilares de crecimiento debajo y las bases que los
    sostienen (capacidades, organización, datos).
    pilares_: [(icono, título, texto)] de 3 a 5; bases: textos cortos. H: alto total (los pilares crecen y el texto sube a 15 px).
    Cuándo usarlo: resumir un plan estratégico o una hoja de ruta de innovación en una sola imagen.
    Cuándo no: si los pilares no comparten una ambición común (usa lista_numerada)."""
    tejado = (f'<div style="position:relative;height:84px"><svg viewBox="0 0 {W} 84" width="{W}" height="84" style="position:absolute;inset:0">'
              f'<polygon points="0,84 {W / 2},4 {W},84" fill="{RED}"/></svg>'
              f'<div style="position:absolute;left:25%;right:25%;bottom:12px;text-align:center;color:#fff;font-size:14.5px;font-weight:700;line-height:1.25">{md(ambicion)}</div></div>')
    tt, tx = (18, 15) if H else (14, 13)
    cols = "".join(f'<div style="flex:1;background:var(--surface-fill);border-radius:0 0 10px 10px;padding:14px 16px;border-top:4px solid {FG1}">'
                   f'{icono(ic, 26, RED)}<b style="display:block;font-size:{tt}px;color:var(--fg1);margin:6px 0 4px">{E(t)}</b>'
                   f'<div style="font-size:{tx}px;line-height:1.4;color:var(--fg2)">{md(x)}</div></div>' for ic, t, x in pilares_)
    base = "".join(f'<span style="flex:1;text-align:center">{md(b)}</span>' for b in bases)
    return (f'<div style="width:{W}px;{f"height:{H}px;" if H else ""}display:flex;flex-direction:column;gap:8px">{tejado}'
            f'<div style="flex:1;display:flex;gap:10px;padding:0 24px">{cols}</div>'
            f'<div style="display:flex;gap:10px;background:{FG1};color:#fff;border-radius:10px;padding:11px 18px;font-size:13px;font-weight:600">{base}</div></div>')


def convergencia(causas, concepto, rotulos=None, W=1100, alto_fila=112, ancho_tile=110, ancho_col=320, D=132):
    """Convergencia: varias causas (tesela roja con icono, texto y un detalle opcional) que confluyen por líneas
    discontinuas en un concepto (círculo rojo a la derecha). causas: [dict(icono, rotulo, texto, detalle=None)];
    concepto = (icono, texto); rotulos: cabeceras de las columnas de texto, por ejemplo ("Voz del experto", "Implicación").
    Cuándo usarlo: decir que varias fuerzas llevan a lo mismo (regulación, industria y comercio exigen inversión).
    Cuándo no: si las causas se suman o se ordenan (usa abanico o lista_numerada)."""
    n = len(causas)
    dos = any(c.get("detalle") for c in causas)
    cab = 26 if rotulos else 0
    H = cab + n * alto_fila
    x1 = ancho_tile + 22
    x2 = x1 + ancho_col + 26
    fin = (x2 + ancho_col) if dos else (x1 + ancho_col)
    cx, cyc = W - D / 2 - 4, cab + n * alto_fila / 2
    L = Lienzo(W, round(H))
    if rotulos:
        for x, r in zip((x1, x2), rotulos):
            L.div(x, 0, ancho_col, f'<b style="font-size:13px;font-style:italic;color:var(--fg1)">{E(r)}</b>')
    for i, c in enumerate(causas):
        y0 = cab + i * alto_fila
        yc = y0 + alto_fila / 2
        ang = math.atan2(yc - cyc, (fin + 14) - cx)
        L.add(line(fin + 14, yc, cx + D / 2 * math.cos(ang), cyc + D / 2 * math.sin(ang), mezcla(RED, "#FFFFFF", .3), 1.3, dash="5 4"))
        L.add(rect(0, y0 + 8, ancho_tile, alto_fila - 16, RED, rx=10))
        L.div(ancho_tile / 2, yc, ancho_tile - 12, f'{icono(c["icono"], 24, "#fff")}<div style="font-size:14px;font-weight:700;color:#fff;line-height:1.2;margin-top:4px">{E(c["rotulo"])}</div>',
              anchor="middle", va="middle")
        L.div(x1, yc, ancho_col, f'<div style="font-size:13px;line-height:1.4">{md(c["texto"])}</div>', va="middle")
        if c.get("detalle"):
            L.div(x2, yc, ancho_col, f'<div style="font-size:13px;line-height:1.4">{md(c["detalle"])}</div>', va="middle")
    L.add(circle(cx, cyc, D / 2, RED))
    L.div(cx, cyc, D - 20, f'{icono(concepto[0], 28, "#fff")}<div style="font-size:15px;font-weight:700;color:#fff;line-height:1.2;margin-top:4px">{E(concepto[1])}</div>',
          anchor="middle", va="middle")
    return L.render()
