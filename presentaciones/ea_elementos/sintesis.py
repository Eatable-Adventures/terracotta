"""Síntesis: resumir y remitir a otras slides con miniaturas.

Familia 14 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
from .base import (
    BURG, CREAM, E, FG1, FG2, FG3, FG4, GREY, Lienzo, PAPER, RAMP, RED, _rampa_pasos, arrow, circle,
    icono, lin, line, md, rect, sobre, text,
)

__all__ = ["tarjetas_miniatura", "mini_barras_objetivo", "mini_conteo", "mini_iconos", "mini_escalera", "mini_flechas", "mini_bifurcacion"]


def tarjetas_miniatura(items, rotulo=None):
    """Tarjetas con una miniatura en un panel gris arriba (un mini visual que resume otra slide), título y texto.
    items: [(visual_html, título, texto)], con visual de 300 px de ancho (las funciones mini_*); rotulo: rótulo rojo
    sobre el texto («Nuestra propuesta»), o None.
    Cuándo usarlo: lo esencial al principio o las validaciones al final, 3 tarjetas que anuncian o cierran bloques.
    Cuándo no: con iconos o números decorativos en lugar de miniaturas; con más de 4 tarjetas."""
    if rotulo:
        tj = "".join(f'<div class="card" style="flex:1;padding:14px 16px 16px;display:flex;flex-direction:column;gap:10px">'
                     f'<div style="background:var(--surface-fill);border-radius:12px;padding:14px">{v}</div>'
                     f'<div style="display:flex;justify-content:space-between;align-items:center;margin:2px 6px 0"><h4 style="font-size:19px;margin:0">{E(t)}</h4></div>'
                     f'<div style="margin:0 6px"><span class="k2 red">{E(rotulo)}</span>'
                     f'<div style="font-size:15px;line-height:1.5;color:var(--fg1)">{md(x)}</div></div></div>' for v, t, x in items)
    else:
        tj = "".join(f'<div class="card" style="flex:1;padding:16px 16px 22px;display:flex;flex-direction:column;gap:14px">'
                     f'<div style="background:var(--surface-fill);border-radius:12px;padding:14px">{v}</div>'
                     f'<h4 style="font-size:19px;margin:4px 6px 0">{E(t)}</h4><div class="tx" style="font-size:15px;line-height:1.55;margin:0 6px">{md(x)}</div></div>'
                     for v, t, x in items)
    return f'<div class="row" style="width:100%">{tj}</div>'


def mini_barras_objetivo(filas, dominio, referencia, objetivo, titulo="", pie="", W=300, H=132):
    """Miniatura: barras grises frente a una referencia (línea negra) y un objetivo (rojo discontinuo).
    filas: [(rótulo, valor)] (3 como máximo); referencia y objetivo = (valor, texto)."""
    L = Lienzo(W, H)
    s = lin(dominio[0], dominio[1], 112, W - 4)
    for i, (f, v) in enumerate(filas):
        y = 34 + i * 28
        L.div(0, y + 7, 110, f'<b style="color:var(--fg1)">{E(f)}</b>', va="middle", style="font-size:13px")
        L.add(rect(112, y, s(v) - 112, 14, FG4, rx=4))
    L.add(line(s(referencia[0]), 24, s(referencia[0]), 112, FG2, 2), line(s(objetivo[0]), 24, s(objetivo[0]), 112, RED, 2, dash="4 3"),
          text(W, 16, objetivo[1], 12, 700, RED, "end"), text(s(referencia[0]), 127, referencia[1], 12, 600, FG2, "middle"))
    if titulo:
        L.add(text(0, 16, titulo, 11, 400, FG3))
    if pie:
        L.add(text(0, 127, pie, 11, 400, FG3))
    return L.render()


def mini_conteo(total, marcados, rotulo_html, texto_marcados, texto_resto, W=300, H=132):
    """Miniatura: una fila de círculos (marcados en rojo, el resto en blanco) y su leyenda en dos líneas.
    total y marcados: enteros (hasta 10); rotulo_html: línea de arriba."""
    L = Lienzo(W, H)
    L.div(0, 10, W, f'<span style="font-size:13px;color:var(--fg1)">{rotulo_html}</span>', va="middle")
    paso = (W - 28) / max(total - 1, 1)
    for i in range(total):
        L.add(circle(14 + i * paso, 48, 12, RED if i < marcados else PAPER, RED if i < marcados else FG4, 2))
    L.add(circle(8, 92, 6, RED), circle(8, 116, 6, PAPER, FG4, 2))
    L.div(22, 92, W - 22, f'<b style="color:var(--fg1)">{marcados}</b> {E(texto_marcados)}', va="middle", style="font-size:13px")
    L.div(22, 116, W - 22, f'<b style="color:var(--fg1)">{total - marcados}</b> {E(texto_resto)}', va="middle", style="font-size:13px")
    return L.render()


def mini_iconos(items, alto=132):
    """Miniatura: de 2 a 4 teselas blancas con un icono rojo y una palabra. items: [(icono, texto)]."""
    return (f'<div style="display:flex;gap:8px;height:{alto}px">' + "".join(
        f'<div class="tile" style="flex:1;flex-direction:column;justify-content:center;text-align:center;gap:8px;padding:8px">'
        f'{icono(ic, 30, RED)}<b>{E(t)}</b></div>' for ic, t in items) + '</div>')


def mini_escalera(niveles, W=300, H=118):
    """Miniatura de escalera_prioridad: tres franjas con chips de código. niveles: [(nivel, [códigos])]."""
    L = Lienzo(W, H)
    for k, (lab, cods) in enumerate(niveles):
        y, tono = 3 + k * 38, [RAMP[1], RAMP[3], RAMP[4]][min(k, 2)]
        L.add(rect(0, y, W, 32, tono, rx=8, op=0.14), rect(0, y, 56, 32, tono, rx=8))
        L.div(28, y + 16, 56, f'<b style="font-size:13px;color:{sobre(tono)}">{E(lab)}</b>', anchor="middle", va="middle")
        x = 64
        for c in cods:
            w = 38 if len(c) <= 3 else min(96, 10 + 7 * len(c))
            L.add(rect(x, y + 5, w, 22, PAPER, rx=6, stroke=GREY))
            L.div(x + w / 2, y + 16, w, f'<b style="font-size:12px;color:var(--fg1)">{E(c)}</b>', anchor="middle", va="middle")
            x += w + 6
    return L.render()


def mini_flechas(pasos, nota_html="", W=300, H=118):
    """Miniatura de proceso_flechas: hasta 4 flechas en rampa de rojos con una palabra y una nota debajo."""
    L = Lienzo(W, H)
    n = len(pasos)
    a, y0, h = 10, 4, 34
    w = (W - 8 * (n - 1) - a) / n
    cols = _rampa_pasos(n)
    for k, lab in enumerate(pasos):
        x0 = k * (w + 8)
        pts = [(x0, y0), (x0 + w, y0), (x0 + w + a, y0 + h / 2), (x0 + w, y0 + h), (x0, y0 + h)] + ([(x0 + a, y0 + h / 2)] if k else [])
        L.add(f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts)}" fill="{cols[k]}"/>')
        L.div(x0 + (a if k else 0) + (w - (a if k else 0)) / 2, y0 + h / 2, w, f'<b style="font-size:12px;color:{sobre(cols[k])}">{E(lab)}</b>',
              anchor="middle", va="middle")
    if nota_html:
        L.div(0, 62, W, f'<div style="font-size:12px;line-height:1.45;color:var(--fg2)">{nota_html}</div>')
    return L.render()


def mini_bifurcacion(etapa, corte, si, no, nota="", W=300, H=118):
    """Miniatura de una decisión en el tiempo: barra de etapa, rombo de corte y dos ramas (sí llena, no punteada)."""
    L = Lienzo(W, H)
    xc, yb, d = 140, 26, 16
    L.add(rect(0, yb, xc - 10, 26, RED, rx=6), line(xc, 16, xc, 92, FG1, 1, dash="3 4"))
    L.div(10, yb + 13, 120, f'<b style="font-size:12px;color:#fff">{E(etapa)}</b>', va="middle")
    L.div(xc, 0, 160, f'<b style="font-size:12px;color:var(--fg1)">{E(corte)}</b>', anchor="middle")
    L.add(f'<polygon points="{xc},{yb + 13 - d} {xc + d},{yb + 13} {xc},{yb + 13 + d} {xc - d},{yb + 13}" fill="{BURG}"/>',
          text(xc, yb + 17.5, "?", 13, 700, CREAM, "middle"))
    L.add(rect(xc + 24, yb, W - xc - 24, 26, FG1, rx=6))
    L.div(xc + 34, yb + 13, 120, f'<b style="font-size:12px;color:#fff">{E(si)}</b>', va="middle")
    yn = yb + 40
    L.add(arrow([(xc, yb + 13 + d), (xc, yn + 13), (xc + 20, yn + 13)], FG3, 1.2, dash="3 3", size=6))
    L.add(rect(xc + 24, yn, W - xc - 24, 26, PAPER, rx=6, stroke=FG3, dash="4 3"))
    L.div(xc + 34, yn + 13, 130, f'<b style="font-size:12px;color:var(--fg1)">{E(no)}</b>', va="middle")
    if nota:
        L.div(0, 100, W, f'<span style="font-size:12px;color:var(--fg2)">{E(nota)}</span>')
    return L.render()
