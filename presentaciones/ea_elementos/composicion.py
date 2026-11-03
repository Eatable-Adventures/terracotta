"""Composición: de qué está hecho un total.

Familia 03 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (
    CATEGORIAS, E, FG1, FG2, FG3, FG4, FILL, GREY, INPUT, LGREY, Lienzo, NEUTRO, RED, TINT, _svg, circle,
    fmt, icono, line, md, mezcla, oscuro, rampa, rect, sobre, text,
)
from .marcas import (_con_leyenda, leyenda)

__all__ = ["anillo_categorias", "donut", "waffle", "treemap", "marimekko", "sankey", "sunburst", "barra_desglose"]


def anillo_categorias(grupos, centro, marca=("science", "Marcado"), franja="", colores=None, W=1152, H=466):
    """Anillo de dos niveles: categorías dentro, elementos fuera (todos los de una categoría del mismo color), con
    etiquetas a los dos lados unidas por guías. Un estado transversal se marca con un icono junto al nombre, nunca
    cambiando el color de la categoría. El anillo empieza arriba con el segundo grupo y cierra con el primero; cada
    etiqueta va al lado (izquierda o derecha) en el que cae su segmento.
    grupos: [(categoría, [(código, nombre, definición, marcado)])]; centro = (cifra, rótulo); marca = (icono, texto de la
    leyenda); franja: texto de lo que queda fuera (se omite si está vacío); colores: uno por categoría.
    Cuándo usarlo: una taxonomía de 6 a 12 elementos en 2 a 4 categorías, cuando importa ver el todo y un estado.
    Cuándo no: con más de 12 elementos (no caben las etiquetas) o si el orden importa (usa escalera_prioridad)."""
    colores = colores or CATEGORIAS
    L = Lienzo(W, H)
    cxr, cyr, r0, r1, r2, r3 = W / 2, 166, 54, 88, 92, 148
    ters = [(g, t) for g, (_, ts) in enumerate(grupos) for t in ts]
    der = [x for x in ters if x[0] != 0]
    izq = [x for x in ters if x[0] == 0]
    orden = der + izq[::-1]
    step = 2 * math.pi / len(ters)
    simb = f'<span style="display:inline-flex;vertical-align:-3px;margin:0 3px">{icono(marca[0], 17, RED)}</span>'

    def arco(a0, a1, ri, ro):
        p = lambda rr, a: (cxr + rr * math.cos(a), cyr + rr * math.sin(a))
        x0, y0 = p(ro, a0); x1, y1 = p(ro, a1); x2, y2 = p(ri, a1); x3, y3 = p(ri, a0)
        lg = 1 if a1 - a0 > math.pi else 0
        return f"M{x0:.1f},{y0:.1f} A{ro},{ro} 0 {lg} 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} A{ri},{ri} 0 {lg} 0 {x3:.1f},{y3:.1f} Z"

    a, mids, gspan = -math.pi / 2, {}, {}
    for g, t in orden:
        a0, a1 = a, a + step
        L.add(f'<path d="{arco(a0 + 0.012, a1 - 0.012, r2, r3)}" fill="{colores[g]}" stroke="none" stroke-width="1"/>')
        am = (a0 + a1) / 2
        mids[t[0]] = am
        gspan.setdefault(g, [a0, a1])[1] = a1
        L.add(text(cxr + (r2 + r3) / 2 * math.cos(am), cyr + (r2 + r3) / 2 * math.sin(am) + 4, t[0], 13, 700, sobre(colores[g]), "middle"))
        a = a1
    for g, (a0, a1) in gspan.items():
        L.add(f'<path d="{arco(a0 + 0.012, a1 - 0.012, r0, r1)}" fill="{colores[g]}"/>')
    L.add(text(cxr, cyr + 2, centro[0], 30, 600, FG1, "middle"), text(cxr, cyr + 20, centro[1], 13, 400, FG3, "middle"))

    def lado(items, xlab, anchor):
        obj = sorted([[cyr + (r3 + 16) * math.sin(mids[t[0]]) - 20, g, t] for g, t in items], key=lambda o: o[0])
        obj[0][0] = max(obj[0][0], 0)
        for k in range(1, len(obj)):
            obj[k][0] = max(obj[k][0], obj[k - 1][0] + 62)
        for y, g, t in obj:
            s_ = simb if t[3] else ""
            cc = colores[g] if oscuro(colores[g]) else FG2
            cab = (f'{s_}<b style="color:{cc}">{E(t[0])}</b> <b>{E(t[1])}</b>' if anchor == "start" else
                   f'<b style="color:{cc}">{E(t[0])}</b> <b>{E(t[1])}</b>{s_}')
            L.div(xlab, y, 340, cab + f'<div style="font-size:13px;color:var(--fg3);line-height:1.3;margin-top:2px">{E(t[2])}</div>', anchor=anchor)
            am = mids[t[0]]
            px, py = cxr + (r3 + 4) * math.cos(am), cyr + (r3 + 4) * math.sin(am)
            ex = xlab + (-6 if anchor == "start" else 6)
            kx = px + (18 if anchor == "start" else -18)
            L.add(f'<path d="M{px:.1f},{py:.1f} L{kx:.1f},{y + 9:.1f} L{ex:.1f},{y + 9:.1f}" fill="none" stroke="{FG4}" stroke-width="1"/>',
                  circle(px, py, 2.5, FG3))
    lado([x for x in orden if math.cos(mids[x[1][0]]) > 1e-9], cxr + r3 + 58, "start")
    lado([x for x in orden if math.cos(mids[x[1][0]]) <= 1e-9], cxr - r3 - 58, "end")
    sw = lambda c: f'<i style="width:11px;height:11px;border-radius:3px;background:{c};"></i>'
    it = lambda inner: f'<span style="display:inline-flex;align-items:center;gap:5px;margin:0 9px">{inner}</span>'
    leg = ("".join(it(sw(c) + E(m)) for (m, _), c in zip(grupos, colores)) + '<span style="color:#DCD6CC;margin:0 6px">|</span>'
           + it(f'<span style="display:inline-flex">{icono(marca[0], 15, RED)}</span>' + E(marca[1])))
    yl = H - 70 if franja else H - 24
    L.div(cxr, yl, W, leg, anchor="middle", style="font-size:12px;white-space:nowrap")
    if franja:
        yf = H - 44
        L.add(rect(0, yf, W, 44, LGREY, rx=12, stroke=GREY))
        L.div(18, yf + 22, W - 36, md(franja), va="middle", style="font-size:14px")
    return L.render()


def donut(partes, centro=None, destacado=None, W=520, D=200, grosor=30):
    """Anillo con la cifra clave en el centro y la leyenda con valores a la derecha.
    partes: [(rótulo, valor)]; centro = (cifra, texto); destacado: índice en rojo y el resto en grises
    (si es None, todas en la rampa de rojos).
    Cuándo usarlo: una parte de un total con 2 a 5 partes, cuando la cifra central es el mensaje.
    Cuándo no: más de 5 partes o partes parecidas entre sí (usa barras_ranking)."""
    tot = sum(v for _, v in partes)
    if destacado is None:
        cols = rampa(len(partes))
    else:
        grises = [FG4, INPUT, GREY, FILL]
        g = iter(grises)
        cols = [RED if i == destacado else next(g, FILL) for i in range(len(partes))]
    r = (D - grosor) / 2
    c = math.pi * 2 * r
    s, off = [], 0
    for (_, v), col in zip(partes, cols):
        ln = c * v / tot
        s.append(f'<circle cx="{D / 2}" cy="{D / 2}" r="{r:.1f}" fill="none" stroke="{col}" stroke-width="{grosor}" '
                 f'stroke-dasharray="{max(ln - 2, 0.1):.2f} {c:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 {D / 2} {D / 2})"/>')
        off += ln
    L = Lienzo(D, D).add(*s)
    if centro:
        L.div(D / 2, D / 2, D - 2 * grosor - 16, f'<div class="big" style="font-size:30px">{E(centro[0])}</div>'
              f'<div style="font-size:12px;line-height:1.3;margin-top:4px">{E(centro[1])}</div>', anchor="middle", va="middle")
    filas = "".join(f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid var(--border-2)">'
                    f'<i style="width:12px;height:12px;border-radius:3px;background:{col};flex:none"></i>'
                    f'<span style="flex:1;font-size:13px;color:var(--fg2)">{E(n)}</span>'
                    f'<b style="font-size:14px;color:{RED if col == RED else FG1}">{round(v / tot * 100)} %</b></div>'
                    for (n, v), col in zip(partes, cols))
    return f'<div style="display:flex;align-items:center;gap:32px;width:{W}px">{L.render()}<div style="flex:1">{filas}</div></div>'


def waffle(valor, cifra, texto, total=100, lado=15, sep=3):
    """Gofre de 10 × 10 casillas con las marcadas en rojo; la cifra y su lectura al lado.
    valor: casillas marcadas (sobre 100).
    Cuándo usarlo: un porcentaje que tiene que verse como proporción física («31 de cada 100»).
    Cuándo no: porcentajes muy pequeños (menos de 3) o con decimales."""
    s = []
    for i in range(total):
        fila, col = 9 - i // 10, i % 10
        s.append(rect(col * (lado + sep), fila * (lado + sep), lado, lado, RED if i < valor else NEUTRO, rx=2))
    g = 10 * (lado + sep) - sep
    return (f'<div style="display:flex;align-items:center;gap:26px">{_svg(g, g, "".join(s))}'
            f'<div style="max-width:220px"><div class="big">{E(cifra)}</div>'
            f'<div style="font-size:14px;color:var(--fg2);line-height:1.4;margin-top:8px">{md(texto)}</div></div></div>')


def _squarify(vals, x, y, w, h):
    rects, vals = [], list(vals)
    while vals:
        lado = min(w, h)

        def peor(fl):
            sm = sum(fl)
            return max(max(lado * lado * v / (sm * sm), (sm * sm) / (lado * lado * v)) for v in fl)
        fila, i = [vals[0]], 1
        while i < len(vals) and peor(fila + [vals[i]]) <= peor(fila):
            fila.append(vals[i])
            i += 1
        sm = sum(fila)
        if w >= h:
            cw, yy = sm / h, y
            for v in fila:
                rects.append((x, yy, cw, v / cw))
                yy += v / cw
            x, w = x + cw, w - cw
        else:
            rh, xx = sm / w, x
            for v in fila:
                rects.append((xx, y, v / rh, rh))
                xx += v / rh
            y, h = y + rh, h - rh
        vals = vals[i:]
    return rects


def treemap(items, destacado=None, unidad="%", W=520, H=290):
    """Mapa de árbol (treemap): rectángulos proporcionales al valor, ordenados de mayor a menor.
    items: [(rótulo, valor)]; destacado: rótulo en rojo (el resto en rampa clara); si es None, rampa de rojos.
    Cuándo usarlo: el peso relativo de 5 a 15 partes de un total (cuota de mercado, gasto por partida).
    Cuándo no: si hay que comparar partes pequeñas entre sí (usa barras_ranking)."""
    its = sorted(items, key=lambda d: -d[1])
    tot = sum(v for _, v in its)
    rs = _squarify([v * W * H / tot for _, v in its], 0, 0, W, H)
    cols = rampa(len(its)) if destacado is None else [RED if r == destacado else mezcla(INPUT, FILL, i / max(len(its) - 1, 1)) for i, (r, _) in enumerate(its)]
    L = Lienzo(W, H)
    for (r, v), (x, y, w, h), c in zip(its, rs, cols):
        L.add(rect(x, y, w, h, c, stroke="#fff", sw=3))
        if w > 64 and h > 38:
            col = sobre(c)
            L.div(x + 10, y + 9, w - 20, f'<b style="color:{col};font-size:{13 if w > 120 else 11.5}px">{E(r)}</b>'
                  f'<div style="color:{col};font-size:13px;opacity:.9">{fmt(round(v / tot * 100, 1))} {E(unidad)}</div>',
                  style="line-height:1.25")
    return L.render()


def marimekko(columnas, segmentos, W=520, H=290, rotulo_ancho=""):
    """Marimekko: columnas de ancho proporcional a su tamaño, partidas por la cuota de cada segmento.
    columnas: [(rótulo, tamaño, [valor por segmento])]; segmentos: nombres, en la rampa de rojos.
    Cuándo usarlo: tamaño de mercado por región y cuota por categoría en una sola figura.
    Cuándo no: con más de 5 columnas o 4 segmentos (se vuelve ilegible)."""
    cols = rampa(len(segmentos))
    tot = sum(t for _, t, _ in columnas)
    bot = 34
    L = Lienzo(W, H)
    x = 0
    for r, t, vals in columnas:
        w = W * t / tot
        sv = sum(vals)
        y = 0
        for k, v in enumerate(vals):
            h = (H - bot) * v / sv
            L.add(rect(x, y, w, h, cols[k], stroke="#fff", sw=2))
            if h > 18 and w > 40:
                L.add(text(x + w / 2, y + h / 2 + 4, f"{round(v / sv * 100)} %", 12, 600, sobre(cols[k]), "middle"))
            y += h
        L.add(text(x + w / 2, H - bot + 16, r, 13, 600, FG1, "middle"),
              text(x + w / 2, H - bot + 30, f"{round(t / tot * 100)} %", 11, 400, FG3, "middle"))
        x += w
    nota = f'<div style="font-size:11px;color:var(--fg3)">Ancho de cada columna: {E(rotulo_ancho)}</div>' if rotulo_ancho else ""
    return _con_leyenda(L.render() + nota, [(c, n) for c, n in zip(cols, segmentos)])


def sankey(izquierda, derecha, flujos, destacado=None, W=520, H=280, ancho_nodo=12, sep=10, margen=118):
    """Diagrama de flujos (Sankey) de dos columnas: de dónde viene y a dónde va un volumen.
    izquierda y derecha: listas de nombres; flujos: [(origen, destino, valor)]; destacado: (origen, destino) en rojo.
    Cuándo usarlo: repartos de volumen entre dos clasificaciones (canal de origen a uso final, 6 a 12 flujos).
    Cuándo no: más de dos etapas o flujos muy pequeños (se convierten en hilos ilegibles)."""
    def totales(nodos, idx):
        return {n: sum(v for *p, v in flujos if p[idx] == n) for n in nodos}
    ti, td = totales(izquierda, 0), totales(derecha, 1)
    tot = sum(v for *_, v in flujos)
    esc = (H - sep * (max(len(izquierda), len(derecha)) - 1)) / tot
    def posiciones(nodos, t):
        y, out = 0, {}
        hueco = (H - sum(t[n] * esc for n in nodos)) / max(len(nodos) - 1, 1)
        for n in nodos:
            out[n] = y
            y += t[n] * esc + hueco
        return out
    pi, pd = posiciones(izquierda, ti), posiciones(derecha, td)
    oi, od, y0s, y1s = dict(pi), dict(pd), {}, {}
    for o, d, v in sorted(flujos, key=lambda f: (izquierda.index(f[0]), derecha.index(f[1]))):
        y0s[(o, d)] = oi[o]
        oi[o] += v * esc
    for o, d, v in sorted(flujos, key=lambda f: (derecha.index(f[1]), izquierda.index(f[0]))):
        y1s[(o, d)] = od[d]
        od[d] += v * esc
    xl, xr = margen, W - margen
    cols = dict(zip(izquierda, rampa(len(izquierda))))
    s = []
    for o, d, v in sorted(flujos, key=lambda f: (f[0], f[1]) == destacado):
        h = v * esc
        y0, y1 = y0s[(o, d)], y1s[(o, d)]
        xm = (xl + xr) / 2
        hot = (o, d) == destacado
        s.append(f'<path d="M{xl + ancho_nodo},{y0:.1f} C{xm},{y0:.1f} {xm},{y1:.1f} {xr},{y1:.1f} L{xr},{y1 + h:.1f} '
                 f'C{xm},{y1 + h:.1f} {xm},{y0 + h:.1f} {xl + ancho_nodo},{y0 + h:.1f} Z" fill="{RED if hot else cols[o]}" '
                 f'fill-opacity="{.75 if hot else .28}"/>')
    for n in izquierda:
        h = ti[n] * esc
        s.append(rect(xl, pi[n], ancho_nodo, h, cols[n]))
        s.append(text(xl - 10, pi[n] + h / 2 + 4, f"{n} · {fmt(ti[n])}", 13, 600, FG1, "end"))
    for n in derecha:
        h = td[n] * esc
        s.append(rect(xr, pd[n], ancho_nodo, h, FG2))
        s.append(text(xr + ancho_nodo + 10, pd[n] + h / 2 + 4, f"{n} · {fmt(td[n])}", 13, 600, FG1))
    return _svg(W, H, "".join(s))


def _sector(cx, cy, r0, r1, a0, a1):
    p = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
    g = 1 if a1 - a0 > math.pi else 0
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p(r1, a0), p(r1, a1), p(r0, a1), p(r0, a0)
    return (f"M{x0:.1f},{y0:.1f} A{r1},{r1} 0 {g} 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} "
            f"A{r0},{r0} 0 {g} 0 {x3:.1f},{y3:.1f} Z")


def sunburst(jerarquia, centro=None, destacado=None, W=520, R=118):
    """Sunburst: anillo interior por categoría y anillo exterior por subcategoría, proporcionales al valor.
    Estructura en grises y la subcategoría que importa en rojo; las subcategorías se rotulan fuera del anillo
    y las categorías en la leyenda de debajo.
    jerarquia: [(categoría, [(subcategoría, valor)])]; centro = (cifra, texto); destacado: subcategoría en rojo.
    Cuándo usarlo: un total con dos niveles (familia y producto, región y país), de 3 a 5 categorías.
    Cuándo no: si hay que comparar subcategorías de familias distintas (usa barras_ranking)."""
    H = 2 * R + 56
    cx, cy = W / 2, R + 28
    tot = sum(v for _, subs in jerarquia for _, v in subs)
    grises = [FG2, FG3, FG4, INPUT, GREY]
    L = Lienzo(W, H)
    a = -math.pi / 2
    ley = []
    for k, (cat, subs) in enumerate(jerarquia):
        c = grises[k % len(grises)]
        tc = sum(v for _, v in subs)
        a_fin = a + 2 * math.pi * tc / tot
        L.add(f'<path d="{_sector(cx, cy, R * .42, R * .68, a, a_fin)}" fill="{c}" stroke="#fff" stroke-width="2.5"/>')
        b = a
        for sub, v in subs:
            e = b + 2 * math.pi * v / tot
            hot = sub == destacado
            cs = RED if hot else mezcla(c, "#FFFFFF", .55)
            L.add(f'<path d="{_sector(cx, cy, R * .72, R, b, e)}" fill="{cs}" stroke="#fff" stroke-width="2.5"/>')
            am = (b + e) / 2
            if e - b > .14:
                ca, sa = math.cos(am), math.sin(am)
                L.add(line(cx + (R + 3) * ca, cy + (R + 3) * sa, cx + (R + 12) * ca, cy + (R + 12) * sa, FG4, 1))
                L.add(text(cx + (R + 16) * ca, cy + (R + 16) * sa + 4, f"{sub} {round(v / tot * 100)} %", 12, 700 if hot else 400,
                           RED if hot else FG2, "start" if ca > .15 else ("end" if ca < -.15 else "middle")))
            b = e
        ley.append((c, f"{cat} · {round(tc / tot * 100)} %"))
        a = a_fin
    if centro:
        L.div(cx, cy, R * .78, f'<div class="big" style="font-size:22px">{E(centro[0])}</div><div style="font-size:11px;line-height:1.2">{E(centro[1])}</div>',
              anchor="middle", va="middle")
    return f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;width:{W}px">{L.render()}{leyenda(ley)}</div>'


def barra_desglose(tramos, abierto, desglose, unidad="", rotulo_total="Total", W=520, H=300, fmt_valor=None):
    """Barra con desglose: el total en una barra apilada y uno de sus tramos «abierto» en sus partidas.
    tramos: [(rótulo, valor)] de arriba abajo; abierto: índice del tramo que se abre; desglose: [(rótulo, valor)].
    Cuándo usarlo: estructuras de coste o de ingresos donde una partida concentra el análisis.
    Cuándo no: si todas las partidas pesan igual (usa barras_apiladas)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    top, bot = 30, 8
    hb = H - top - bot
    tot = sum(v for _, v in tramos)
    xl, xr, bw = 150, W - 210, 56
    L = Lienzo(W, H)
    y = top
    ya = yb = None
    for i, (r, v) in enumerate(tramos):
        h = hb * v / tot
        hot = i == abierto
        L.add(rect(xl, y, bw, h - 1.5, RED if hot else mezcla(INPUT, FILL, .5 * (i % 2))))
        L.add(text(xl - 10, y + h / 2 + 4, f"{r} · {f(v)}", 12, 700 if hot else 400, RED if hot else FG2, "end"))
        if hot:
            ya, yb = y, y + h - 1.5
        y += h
    sub = sum(v for _, v in desglose)
    cols = rampa(len(desglose))
    L.add(f'<polygon points="{xl + bw},{ya:.1f} {xr},{top} {xr},{top + hb:.1f} {xl + bw},{yb:.1f}" fill="{TINT}" fill-opacity=".7"/>')
    y = top
    for (r, v), c in zip(desglose, cols):
        h = hb * v / sub
        L.add(rect(xr, y, bw, h - 1.5, c))
        if h > 16:
            L.add(text(xr + bw / 2, y + h / 2 + 4, f"{round(v / sub * 100)} %", 11, 700, sobre(c), "middle"))
        L.add(text(xr + bw + 10, y + h / 2 + 4, f"{r} · {f(v)}", 12, 400, FG2))
        y += h
    L.add(text(xl + bw / 2, top - 10, f"{rotulo_total} {f(tot)}", 12, 700, FG1, "middle"))
    L.add(text(xr + bw / 2, top - 10, f"{tramos[abierto][0]} {f(tramos[abierto][1])}", 12, 700, RED, "middle"))
    return L.render()
