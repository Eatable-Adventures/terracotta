"""Árboles y descomposición: de qué depende algo, rama a rama.

Familia 07 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
from .base import (
    E, FG1, FG3, FG4, FILL, INPUT, Lienzo, PAPER, RED, circle, flecha_svg, head, icono_caja, line, md,
    rect,
)
from .marcas import (delta)

from .base import (BORDER2, arrow, text, uid)  # añadidos el 01-11-2026

__all__ = ["arbol_tramite", "arbol", "espina_pescado", "organigrama", "formula", "arbol_drivers", "abanico_foco", "arbol_opciones"]


def arbol_tramite(entrada, pregunta, si, pasos, duracion=None, datos=None, rotulo_datos="", ancho_entrada=190):
    """Árbol de una pregunta sí o no: entrada → pregunta (caja granate); «Sí» lleva a la vía directa y «No» baja a
    un recorrido numerado con barra de duración. Debajo, hasta tres datos de contexto con icono.
    entrada: texto; pregunta: texto; si = (título, ejemplo); pasos: [(título, detalle)]; duracion = (rótulo, nota);
    datos: [(icono, texto)].
    Cuándo usarlo: un trámite o criterio de paso con una sola bifurcación (regulación, aprobación, compra).
    Cuándo no: con más de una pregunta encadenada (el árbol deja de leerse); para fases en el tiempo usa gantt."""
    wq = 270
    fila = ('<div style="display:flex;align-items:center;gap:8px">'
            f'<div class="card" style="width:{ancho_entrada}px;flex:none;background:var(--surface-fill);border-color:var(--surface-fill);padding:12px 16px;font-size:14px"><b style="color:var(--fg1)">{E(entrada)}</b></div>'
            f'{flecha_svg(FG3, 30, 14)}<div style="background:var(--burgundy);color:#fff;border-radius:12px;padding:12px 18px;font-size:14px;font-weight:700;line-height:1.3;width:{wq}px;flex:none;text-align:center">'
            f'{E(pregunta)}</div>'
            f'<b style="font-size:14px;color:var(--fg1)">Sí</b>{flecha_svg(FG1, 30, 14)}'
            f'<div class="card" style="flex:1;padding:10px 16px;font-size:14px;border-color:var(--fg1)"><b style="color:var(--fg1)">{E(si[0])}</b>'
            + (f'<div style="font-size:13px;color:var(--fg3)">{E(si[1])}</div>' if si[1] else "") + '</div></div>')
    sangria = ancho_entrada + 8 + 30 + 8 + wq / 2 - 7
    pas = "".join(f'<div style="flex:1;display:flex;gap:10px;align-items:center;padding:0 14px;{"border-left:1px solid var(--border-2);" if k else ""}">'
                  f'<span class="nb" style="width:28px;height:28px;font-size:14px">{k + 1}</span><div style="font-size:13px;line-height:1.4">'
                  f'<b style="color:var(--fg1);font-size:14px">{E(t)}</b>' + (f'<br>{E(d)}' if d else "") + '</div></div>' for k, (t, d) in enumerate(pasos))
    dur = ""
    if duracion:
        dur = ('<div style="margin:12px 14px 0;height:8px;border-radius:4px;background:linear-gradient(90deg,var(--brand-tint),var(--red))"></div>'
               f'<div style="display:flex;justify-content:space-between;margin:6px 14px 0;font-size:13px"><b style="color:var(--red)">{E(duracion[0])}</b>'
               f'<span style="color:var(--fg3)">{E(duracion[1])}</span></div>')
    rama = ('<div style="display:flex;flex-direction:column">'
            f'<div style="display:flex;align-items:center;gap:6px;padding-left:{sangria:.0f}px;height:30px;margin:-8px 0 2px">'
            f'{flecha_svg(RED, 26, 14, abajo=True)}<b style="color:var(--red);font-size:14px">No</b></div>'
            f'<div class="card hot" style="background:var(--paper);padding:14px 4px 12px"><div style="display:flex">{pas}</div>{dur}</div></div>')
    dat = ""
    if datos:
        dat = (f'<div style="margin-top:12px">' + (f'<span class="k2" style="margin:0 0 6px">{E(rotulo_datos)}</span>' if rotulo_datos else "")
               + '<div class="row" style="gap:10px">' + "".join(
                   f'<div style="flex:1;display:flex;gap:10px;align-items:center;background:var(--light-grey);box-shadow:inset 0 0 0 1px var(--border-2);'
                   f'border-radius:12px;padding:10px 12px">{icono_caja(ic, 18, caja=30, radio=8)}<div style="font-size:13px;line-height:1.4;color:var(--fg1)">{md(t)}</div></div>'
                   for ic, t in datos) + '</div></div>')
    return f'<div class="col" style="flex:1;gap:12px;justify-content:center">{fila}{rama}{dat}</div>'


def arbol(raiz, ramas, W=520, ancho_raiz=130, ancho_rama=150, alto_hoja=24, sep=12):
    """Árbol de problemas (issue tree) horizontal: raíz, ramas y hojas con conectores en codo.
    ramas: [(rótulo, [hojas])]; una rama con rótulo que empieza por «*» se marca en rojo (la que importa).
    Cuándo usarlo: descomponer una pregunta en sub-preguntas MECE, o un organigrama de responsabilidades.
    Cuándo no: más de 3 niveles o de 12 hojas (partir en dos slides)."""
    alturas = [max(len(h), 1) * alto_hoja for _, h in ramas]
    H = sum(alturas) + sep * (len(ramas) - 1)
    L = Lienzo(W, H)
    xr = ancho_raiz + 30
    xh = xr + ancho_rama + 30
    L.add(rect(0, H / 2 - 30, ancho_raiz, 60, FG1, rx=10))
    L.div(ancho_raiz / 2, H / 2, ancho_raiz - 20, f'<b style="color:#fff;font-size:14px;line-height:1.25">{E(raiz)}</b>', anchor="middle", va="middle")
    y = 0
    for (r, hojas), h in zip(ramas, alturas):
        hot = r.startswith("*")
        r = r.lstrip("*")
        cy = y + h / 2
        L.add(f'<path d="M{ancho_raiz},{H / 2:.1f} H{ancho_raiz + 15} V{cy:.1f} H{xr}" fill="none" stroke="{FG4}" stroke-width="1.5"/>')
        L.add(rect(xr, cy - 17, ancho_rama, 34, RED if hot else FILL, rx=8))
        L.div(xr + 12, cy, ancho_rama - 20, f'<b style="font-size:13px;color:{"#fff" if hot else FG1};line-height:1.2">{E(r)}</b>', va="middle")
        for k, hj in enumerate(hojas):
            hy = y + alto_hoja * k + alto_hoja / 2
            L.add(f'<path d="M{xr + ancho_rama},{cy:.1f} H{xr + ancho_rama + 15} V{hy:.1f} H{xh - 6}" fill="none" stroke="{RED if hot else FG4}" stroke-width="1.2"/>')
            L.add(circle(xh - 2, hy, 3, RED if hot else FG3))
            L.div(xh + 6, hy, W - xh - 6, f'<span style="font-size:13px;color:var(--fg1)">{md(hj)}</span>', va="middle")
        y += h + sep
    return L.render()


def espina_pescado(efecto, categorias, W=1100, H=320):
    """Espina de pescado (Ishikawa): las causas de un problema agrupadas por categoría a lo largo de una espina.
    efecto: el problema (cabeza, en rojo); categorias: [(rótulo, [causas])], hasta 6 (la mitad arriba, la mitad abajo).
    Cuándo usarlo: diagnóstico de causas raíz de un fallo de producto o de proceso.
    Cuándo no: si las causas ya están priorizadas (usa barras_ranking o arbol)."""
    L = Lienzo(W, H)
    ym, cab = H / 2, 190
    xf = W - cab - 14
    L.add(line(20, ym, xf, ym, FG1, 3), head(xf + 12, ym, 0, FG1, 14))
    L.add(rect(xf + 16, ym - 36, cab - 2, 72, RED, rx=10))
    L.div(xf + 16 + (cab - 2) / 2, ym, cab - 26, f'<b style="color:#fff;font-size:14px;line-height:1.25">{E(efecto)}</b>', anchor="middle", va="middle")
    arriba = categorias[0::2]
    abajo = categorias[1::2]
    ncol = max(len(arriba), len(abajo))
    paso = (xf - 40) / ncol
    for grupo, signo in ((arriba, -1), (abajo, 1)):
        for k, (r, causas) in enumerate(grupo):
            xb = 40 + paso * (k + 1) - 20
            xt, yt = xb - 70, ym + signo * (ym - 26)
            L.add(line(xt, yt, xb, ym, FG3, 1.8))
            L.div(xt, yt + (-4 if signo < 0 else 4), 170, f'<b style="font-size:13px;color:var(--red);text-transform:uppercase;letter-spacing:.06em">{E(r)}</b>',
                  anchor="middle", va="bottom" if signo < 0 else "top")
            for j, c in enumerate(causas):
                t = (j + 1) / (len(causas) + 1)
                px, py = xt + (xb - xt) * t, yt + (ym - yt) * t
                L.add(line(px - 40, py, px, py, FG4, 1))
                L.div(px - 46, py, paso - 90, f'<span style="font-size:12px;color:var(--fg1)">{E(c)}</span>', anchor="end", va="middle")
    return L.render()


def organigrama(raiz, W=1100, alto=50, sep_v=40, ancho_max=170, gap=14):
    """Organigrama en árbol: cada nivel en una fila, cada caja centrada sobre las suyas y conectores en ángulo
    recto. El peso baja con el nivel (raíz en negro, segundo nivel en gris, el resto en blanco con borde).
    raiz = (nombre, cargo, [hijos], destacado) con hijos del mismo formato; destacado en rojo.
    Cuándo usarlo: equipo del cliente y sus interlocutores, o la estructura del proyecto con EA.
    Cuándo no: más de 8 cajas en el nivel más ancho (agrupar por áreas o partir en dos)."""
    def hojas(n):
        return max(1, sum(hojas(h) for h in n[2])) if n[2] else 1
    total = hojas(raiz)
    slot = min(ancho_max + gap, W / total)
    bw = slot - gap
    x_ini = (W - total * slot) / 2
    cajas_, aristas = [], []

    def colocar(n, x0, d):
        if n[2]:
            xs, xi = [], x0
            for h in n[2]:
                xs.append(colocar(h, xi, d + 1))
                xi += hojas(h) * slot
            cx = (xs[0] + xs[-1]) / 2
            aristas.append((cx, d, xs))
        else:
            cx = x0 + slot / 2
        cajas_.append((cx, d, n))
        return cx
    colocar(raiz, x_ini, 0)
    prof = max(d for _, d, _ in cajas_)
    H = (prof + 1) * alto + prof * sep_v
    L = Lienzo(W, H)
    for cx, d, xs in aristas:
        yb = d * (alto + sep_v) + alto
        ym = yb + sep_v / 2
        L.add(line(cx, yb, cx, ym, FG4, 1.5))
        if len(xs) > 1:
            L.add(line(min(xs), ym, max(xs), ym, FG4, 1.5))
        for x in xs:
            L.add(line(x, ym, x, ym + sep_v / 2, FG4, 1.5))
    for cx, d, n in cajas_:
        nom, cargo, _, *h = n
        hot = bool(h and h[0])
        bg, fg, bd = (RED, "#fff", RED) if hot else [(FG1, "#fff", FG1), (FILL, FG1, FILL)][d] if d < 2 else (PAPER, FG1, INPUT)
        w = min(max(bw, 200), W) if d == 0 else bw
        y0 = d * (alto + sep_v)
        L.add(rect(cx - w / 2, y0, w, alto, bg, rx=10, stroke=bd, sw=1.2))
        L.div(cx, y0 + alto / 2, w - 16, f'<b style="font-size:{13 if d < 2 else 12}px;color:{fg};display:block;line-height:1.2">{E(nom)}</b>'
              f'<span style="font-size:11px;color:{fg};opacity:.8">{E(cargo)}</span>', anchor="middle", va="middle")
    return L.render()


def formula(factores, resultado, operadores=None, W=1100):
    """Fórmula de cálculo: cajas con cada factor (rótulo, cifra y fuente) unidas por operadores (×, +, −, ÷) y
    el resultado en rojo.
    factores: [(cifra, rótulo, fuente)]; resultado = (cifra, rótulo, fuente); operadores: uno menos que factores
    (por defecto «×»).
    Cuándo usarlo: enseñar el método de una cifra (tamaño de mercado, ahorro, business case) en una línea.
    Cuándo no: si hay más de 5 factores o varios niveles (usa arbol_drivers)."""
    ops = operadores or ["×"] * (len(factores) - 1)
    def caja(c, r, fu, n=None, final=False):
        bg, fg, sub = ("var(--red)", "#fff", "rgba(255,255,255,.85)") if final else ("#fff", FG1, FG3)
        num = f'<span style="width:20px;height:20px;border-radius:50%;background:var(--surface-fill);color:var(--red);font-size:12px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;margin-bottom:6px">{n}</span>' if n else ""
        return (f'<div style="flex:1;min-width:0;background:{bg};border:1px solid {"var(--red)" if final else "var(--border-1)"};border-radius:14px;padding:14px 16px">'
                f'{num}<div style="font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:{sub};line-height:1.3">{E(r)}</div>'
                f'<div style="font-size:28px;font-weight:700;letter-spacing:-.02em;color:{fg};margin:4px 0">{E(c)}</div>'
                f'<div style="font-size:12px;color:{sub};line-height:1.3">Fuente: {E(fu)}</div></div>')
    op = lambda o: f'<div style="flex:none;width:34px;align-self:center;text-align:center;font-size:32px;font-weight:300;color:var(--fg3)">{E(o)}</div>'
    partes = []
    for i, (c, r, fu) in enumerate(factores):
        partes.append(caja(c, r, fu, i + 1))
        partes.append(op(ops[i]) if i < len(factores) - 1 else op("="))
    partes.append(caja(*resultado, final=True))
    return f'<div style="display:flex;align-items:stretch;gap:6px;width:{W}px">{"".join(partes)}</div>'


def arbol_drivers(raiz, W=1100, bw=200, bh=58, sep=14):
    """Árbol de drivers: un KPI descompuesto de izquierda a derecha en sus factores, con valor, variación y el
    operador que los une (× o +) sobre el conector.
    raiz = dict(rotulo, valor, delta=None, tono='neutro', sube=True, destacado=False, op='×', hijos=[...]).
    Cuándo usarlo: explicar qué mueve un resultado (ingresos = volumen × precio) o dónde actuar.
    Cuándo no: si los factores no se combinan aritméticamente (usa arbol)."""
    def hojas(n):
        return max(1, sum(hojas(h) for h in n.get("hijos", []))) if n.get("hijos") else 1
    prof = lambda n: 1 + max((prof(h) for h in n.get("hijos", [])), default=0)
    total, niveles = hojas(raiz), prof(raiz)
    gx = (W - niveles * bw) / max(niveles - 1, 1)
    H = total * (bh + sep) - sep
    L = Lienzo(W, H)
    def colocar(n, y0, d):
        hs = n.get("hijos", [])
        x0 = d * (bw + gx)
        if hs:
            ys, yy = [], y0
            for h in hs:
                ys.append(colocar(h, yy, d + 1))
                yy += hojas(h) * (bh + sep)
            cy = (ys[0] + ys[-1]) / 2
            xm = x0 + bw + gx / 2
            L.add(line(x0 + bw, cy, xm, cy, FG4, 1.5), line(xm, ys[0], xm, ys[-1], FG4, 1.5))
            for yc in ys:
                L.add(line(xm, yc, x0 + bw + gx, yc, FG4, 1.5))
            for a, b in zip(ys, ys[1:]):
                L.add(circle(xm, (a + b) / 2, 11, PAPER, FG3, 1.2))
                L.div(xm, (a + b) / 2, 22, f'<b style="font-size:14px;color:var(--fg2)">{E(n.get("op", "×"))}</b>', anchor="middle", va="middle")
        else:
            cy = y0 + bh / 2
        raiz_ = d == 0
        hot = n.get("destacado")
        bg = FG1 if raiz_ else PAPER
        L.add(rect(x0, cy - bh / 2, bw, bh, bg, rx=10, stroke=RED if hot else (FG1 if raiz_ else INPUT), sw=2 if hot else 1.2))
        fg = "#fff" if raiz_ else FG1
        ch = delta(n["delta"], n.get("sube", True), n.get("tono", "neutro")) if n.get("delta") else ""
        L.div(x0 + 12, cy, bw - 24, f'<div style="font-size:11px;color:{"#fff" if raiz_ else FG3};opacity:{.8 if raiz_ else 1}">{E(n["rotulo"])}</div>'
              f'<div style="display:flex;align-items:center;justify-content:space-between;gap:6px"><b style="font-size:17px;color:{fg}">{E(n["valor"])}</b>{ch}</div>',
              va="middle")
        return cy
    colocar(raiz, 0, 0)
    return L.render()


def abanico_foco(foco, filas, forma="circulo", W=1000, D=150, ancho_rotulo=170, alto_fila=58):
    """Abanico: un foco (círculo o caja roja) que se abre en filas de rótulo y texto, con el haz en degradado.
    foco: texto o (titulo, subtitulo); filas: [(rótulo, texto)], de 3 a 6; forma: 'circulo' o 'caja'.
    Cuándo usarlo: las partes de una idea que salen de un mismo origen (cinco barreras de entrada, lo que implica una vía).
    Cuándo no: si las filas son pasos en orden (usa chevrones) o se descomponen a su vez (usa arbol)."""
    n = len(filas)
    H = max(D + 20, n * alto_fila)
    cy = H / 2
    alto_foco = D if forma == "circulo" else D * .62
    x_lista = D + 70
    gid = uid("ab")
    L = Lienzo(W, round(H))
    L.defs.append(f'<linearGradient id="{gid}"><stop offset="0" stop-color="{RED}" stop-opacity=".30"/>'
                  f'<stop offset="1" stop-color="{RED}" stop-opacity=".04"/></linearGradient>')
    L.add(f'<polygon points="{D / 2:.1f},{cy - alto_foco * .32:.1f} {x_lista:.1f},2 {x_lista:.1f},{H - 2:.1f} {D / 2:.1f},{cy + alto_foco * .32:.1f}" fill="url(#{gid})"/>')
    L.add(circle(D / 2, cy, D / 2, RED) if forma == "circulo" else rect(0, cy - alto_foco / 2, D, alto_foco, RED, rx=10))
    tit, sub = foco if isinstance(foco, (tuple, list)) else (foco, "")
    L.div(D / 2, cy, D - 24, f'<b style="font-size:15px;line-height:1.2;color:#fff">{E(tit)}</b>'
          + (f'<div style="font-size:12px;color:#fff;opacity:.9;margin-top:3px">{E(sub)}</div>' if sub else ""), anchor="middle", va="middle")
    y0 = (H - n * alto_fila) / 2
    xt = x_lista + 16
    for i, (r, t) in enumerate(filas):
        yc = y0 + (i + .5) * alto_fila
        if i:
            L.add(line(xt, y0 + i * alto_fila, W, y0 + i * alto_fila, BORDER2, 1))
        L.div(xt, yc, ancho_rotulo, f'<b style="font-size:13px;line-height:1.25;color:var(--fg1)">{E(r)}</b>', va="middle")
        L.div(xt + ancho_rotulo + 16, yc, W - xt - ancho_rotulo - 16, f'<div style="font-size:13px;line-height:1.4">{md(t)}</div>', va="middle")
    return L.render()


def arbol_opciones(grupos, W=1100, ancho_grupo=140, ancho_opcion=210, alto_opcion=58, sep=22):
    """Árbol de opciones: categorías a la izquierda (cajas rojas), opciones numeradas en el centro y, a la derecha,
    qué significa cada opción, todo unido por conectores en codo.
    grupos: [dict(rotulo, opciones=[dict(titulo, texto)])]; la numeración sigue entre grupos.
    Cuándo usarlo: rutas o alternativas agrupadas por una condición (IP temprana o madura, con o sin planta).
    Cuándo no: si hay una pregunta sí o no con un recorrido (usa arbol_tramite)."""
    ops = [(g, o) for g, gr in enumerate(grupos) for o in gr["opciones"]]
    m = len(ops)
    top = 14
    H = top + m * alto_opcion + (m - 1) * sep + 4
    xo = ancho_grupo + 90
    xt = xo + ancho_opcion + 64
    espina = ancho_grupo + 42
    L = Lienzo(W, round(H))
    cy = [top + i * (alto_opcion + sep) + alto_opcion / 2 for i in range(m)]
    for g, gr in enumerate(grupos):
        ys = [cy[i] for i, (gg, _) in enumerate(ops) if gg == g]
        gy = sum(ys) / len(ys)
        L.add(line(ancho_grupo, gy, espina, gy, FG3, 1.3), line(espina, min(ys), espina, max(ys), FG3, 1.3))
        for yy in ys:
            L.add(arrow([(espina, yy), (xo - 2, yy)], FG3, 1.3, size=7))
        L.add(rect(0, gy - 34, ancho_grupo, 68, RED, rx=8))
        L.div(ancho_grupo / 2, gy, ancho_grupo - 16, f'<b style="font-size:15px;line-height:1.2;color:#fff">{E(gr["rotulo"])}</b>', anchor="middle", va="middle")
    for i, (_, o) in enumerate(ops):
        y0 = cy[i] - alto_opcion / 2
        L.add(rect(xo, y0, ancho_opcion, alto_opcion, "#fff", rx=10, stroke=RED, sw=1.3))
        L.add(circle(xo + ancho_opcion / 2, y0, 12, "#fff", RED, 1.3), text(xo + ancho_opcion / 2, y0 + 4.5, str(i + 1), 13, 700, RED, "middle"))
        L.div(xo + ancho_opcion / 2, cy[i] + 3, ancho_opcion - 20, f'<div style="font-size:14px;line-height:1.25;color:var(--fg1)">{E(o["titulo"])}</div>', anchor="middle", va="middle")
        L.add(arrow([(xo + ancho_opcion + 4, cy[i]), (xt - 12, cy[i])], FG3, 1.3, size=7))
        L.add(line(xt, y0 + 2, W, y0 + 2, BORDER2, 1))
        L.div(xt, cy[i] + 2, W - xt, f'<div style="font-size:13px;line-height:1.4">{md(o["texto"])}</div>', va="middle")
    return L.render()
