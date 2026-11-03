"""Evolución: cómo cambia en el tiempo.

Familia 02 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (
    E, FG1, FG2, FG3, FG4, FONT, GREY, LGREY, Lienzo, PAPER, RAMP, RED, TINT, _paso, _set, _svg,
    arrow_eje, circle, fmt, lin, line, rampa, rect, text, uid,
)

from .base import (arrow, hatch, mezcla)  # añadidos el 01-11-2026

__all__ = ["linea", "area_apilada", "sparkline", "pendiente", "cascada", "curva_s", "abanico", "bump", "pequenos_multiplos", "combo_financiero"]


def _techo(maximo, n=4):
    p = _paso(maximo, n)
    return p * math.ceil(maximo / p - 1e-9), p


def _separar(ys, minimo=15):
    """Separa posiciones verticales de etiquetas para que no se pisen (conserva el orden)."""
    orden = sorted(range(len(ys)), key=lambda i: ys[i])
    out = list(ys)
    for a, b in zip(orden, orden[1:]):
        if out[b] - out[a] < minimo:
            out[b] = out[a] + minimo
    return out


def linea(eje_x, series, destacada=0, anotaciones=(), unidad="", W=520, H=270, minimo=0, fmt_valor=None, periodos=()):
    """Líneas con la serie que importa en rojo y el resto en gris, rotuladas al final (sin leyenda).
    eje_x: rótulos del eje (años, meses); series: [(nombre, [valores])];
    anotaciones: [(índice de serie, índice de punto, texto)] para marcar un hito sobre la línea.
    periodos: [(índice desde, índice hasta, rótulo)] para sombrear en gris un tramo del eje (crisis, cambio normativo).
    Cuándo usarlo: una tendencia en el tiempo con 1 a 4 series y al menos 5 puntos.
    Cuándo no: con 2 o 3 puntos (usa columnas o pendiente)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    izq, der, top, bot = 34, 136, 16, 28
    mx, p = _techo(max(max(v) for _, v in series))
    x = lin(0, len(eje_x) - 1, izq, W - der)
    y = lin(minimo, mx, H - bot, top)
    s = []
    for desde, hasta, rotulo in periodos:
        s.append(rect(x(desde), top, x(hasta) - x(desde), H - bot - top, mezcla(GREY, "#FFFFFF", .55)))
        s.append(text((x(desde) + x(hasta)) / 2, top + 13, rotulo, 12, 600, FG2, "middle"))
    v = minimo
    while v <= mx + 1e-9:
        s.append(line(izq, y(v), W - der, y(v), GREY if v > minimo else FG4, 1))
        s.append(text(izq - 8, y(v) + 4, fmt(v), 11, 400, FG3, "end"))
        v += p
    for i, r in enumerate(eje_x):
        s.append(text(x(i), H - bot + 17, r, 12, 400, FG3, "middle"))
    orden = [k for k in range(len(series)) if k != destacada] + [destacada]
    finales = _separar([y(series[k][1][-1]) for k in range(len(series))], 15)
    for k in orden:
        nom, vals = series[k]
        hot = k == destacada
        c = RED if hot else FG4
        d = "M" + " L".join(f"{x(i):.1f},{y(val):.1f}" for i, val in enumerate(vals))
        s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{3 if hot else 2}" stroke-linejoin="round" stroke-linecap="round"/>')
        s.append(circle(x(len(vals) - 1), y(vals[-1]), 4.5 if hot else 3.5, c))
        s.append(text(W - der + 10, finales[k] + 4, f"{nom} · {f(vals[-1])}", 13, 700 if hot else 400, RED if hot else FG2))
    for k, i, t in anotaciones:
        vy = y(series[k][1][i])
        s.append(circle(x(i), vy, 6, PAPER, RED if k == destacada else FG3, 2))
        s.append(line(x(i), vy - 8, x(i), vy - 26, FG3, 1))
        s.append(text(x(i), vy - 31, t, 12, 600, FG1, "middle", halo=True))
    return _svg(W, H, "".join(s))


def area_apilada(eje_x, series, W=520, H=260):
    """Áreas apiladas en la rampa de rojos, rotuladas a la derecha de cada banda.
    series: [(nombre, [valores])], de abajo arriba.
    Cuándo usarlo: cómo crece un total y cómo cambia su composición (2 a 4 componentes).
    Cuándo no: si interesa la evolución exacta de una banda intermedia (usa linea)."""
    izq, der, top, bot = 34, 118, 12, 28
    cols = rampa(len(series))
    acum = [[0] * len(eje_x)]
    for _, v in series:
        acum.append([a + b for a, b in zip(acum[-1], v)])
    mx, p = _techo(max(acum[-1]))
    x = lin(0, len(eje_x) - 1, izq, W - der)
    y = lin(0, mx, H - bot, top)
    s = []
    v = 0
    while v <= mx + 1e-9:
        s.append(text(izq - 8, y(v) + 4, fmt(v), 11, 400, FG3, "end"))
        v += p
    for k in range(len(series)):
        arriba = " L".join(f"{x(i):.1f},{y(val):.1f}" for i, val in enumerate(acum[k + 1]))
        abajo = " L".join(f"{x(i):.1f},{y(val):.1f}" for i, val in reversed(list(enumerate(acum[k]))))
        s.append(f'<path d="M{arriba} L{abajo} Z" fill="{cols[k]}" stroke="#fff" stroke-width="1"/>')
        ym = (y(acum[k][-1]) + y(acum[k + 1][-1])) / 2
        s.append(text(W - der + 10, ym + 4, series[k][0], 13, 600, FG1))
    s.append(line(izq, H - bot, W - der, H - bot, FG4, 1))
    for i, r in enumerate(eje_x):
        s.append(text(x(i), H - bot + 17, r, 12, 400, FG3, "middle"))
    return _svg(W, H, "".join(s))


def sparkline(valores, W=120, H=34, color=RED):
    """Minilínea sin ejes con el último punto marcado y un degradado del color de la línea por debajo.
    Para meter dentro de una tarjeta o una celda.
    Cuándo usarlo: dar la forma de una tendencia junto a una cifra (cifra_delta, tablas).
    Cuándo no: si hay que leer valores concretos (usa linea)."""
    x = lin(0, len(valores) - 1, 3, W - 4)
    y = lin(min(valores), max(valores), H - 4, 4)
    d = "M" + " L".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(valores))
    gid = uid("sg")
    grad = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{color}" stop-opacity=".28"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>')
    area = d + f" L{x(len(valores) - 1):.1f},{H} L{x(0):.1f},{H} Z"
    return _svg(W, H, f'<path d="{area}" fill="url(#{gid})"/><path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'
                + circle(x(len(valores) - 1), y(valores[-1]), 3.5, color), grad)


def pendiente(filas, periodos=("Antes", "Ahora"), destacado=None, unidad="", W=440, H=280, fmt_valor=None):
    """Gráfico de pendiente: cada elemento une su valor en dos momentos; el que importa en rojo.
    filas: [(rótulo, valor_antes, valor_ahora)].
    Cuándo usarlo: quién sube y quién baja entre dos fechas, con 3 a 8 elementos.
    Cuándo no: con más de dos momentos (usa linea)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    dest = _set(destacado)
    xa, xb, top, bot = 150, W - 150, 34, 12
    vals = [v for _, a, b in filas for v in (a, b)]
    y = lin(min(vals), max(vals), H - bot, top)
    s = [line(xa, top - 8, xa, H, FG4, 1), line(xb, top - 8, xb, H, FG4, 1),
         text(xa, 12, periodos[0], 12, 700, FG3, "middle", ls=1), text(xb, 12, periodos[1], 12, 700, FG3, "middle", ls=1)]
    ya = _separar([y(a) for _, a, _ in filas])
    yb = _separar([y(b) for _, _, b in filas])
    orden = sorted(range(len(filas)), key=lambda i: filas[i][0] in dest)
    for i in orden:
        r, a, b = filas[i]
        hot = r in dest
        c = RED if hot else FG4
        s.append(line(xa, y(a), xb, y(b), c, 3 if hot else 1.8, cap="round"))
        s.append(circle(xa, y(a), 4.5, c) + circle(xb, y(b), 4.5, c))
        s.append(text(xa - 12, ya[i] + 4, f"{r}  {f(a)}", 13, 700 if hot else 400, RED if hot else FG2, "end"))
        s.append(text(xb + 12, yb[i] + 4, f"{f(b)}  {r}", 13, 700 if hot else 400, RED if hot else FG2))
    return _svg(W, H, "".join(s))


def cascada(inicio, pasos, fin, unidad="", W=520, H=270, color_baja=RED, color_sube=RAMP[4], color_total=FG2, fmt_valor=None, evidencia=None):
    """Cascada (waterfall): de un valor de partida a uno final, paso a paso, con conectores entre barras.
    inicio = (rótulo, valor); pasos: [(rótulo, variación)]; fin: rótulo del total final (se calcula).
    Por defecto las bajadas van en rojo (la cascada típica es «cómo llegamos al objetivo de reducción»).
    evidencia: lista con el nivel 'A', 'B' o 'C' de cada paso (None en los totales); añade una fila bajo los rótulos.
    Cuándo usarlo: explicar un puente entre dos cifras (de 18 g a 12 g de azúcar, del coste actual al objetivo).
    Cuándo no: si las palancas no son sumables entre sí."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    barras = [(inicio[0], 0, inicio[1], "t")]
    acc = inicio[1]
    for r, d in pasos:
        barras.append((r, acc, acc + d, "b" if d < 0 else "s"))
        acc += d
    barras.append((fin, 0, acc, "t"))
    top, bot = 24, (76 if evidencia else 40)
    mx = max(max(a, b) for _, a, b, _ in barras)
    y = lin(0, mx, H - bot, top)
    paso = W / len(barras)
    bw = min(54, paso * .6)
    s = [line(0, H - bot, W, H - bot, FG4, 1)]
    for i, (r, a, b, t) in enumerate(barras):
        cx = paso * (i + .5)
        c = color_total if t == "t" else (color_baja if t == "b" else color_sube)
        y0, y1 = y(max(a, b)), y(min(a, b))
        s.append(rect(cx - bw / 2, y0, bw, max(y1 - y0, 1), c, rx=2))
        lab = f(b) if t == "t" else ("+" if b > a else "−") + f(abs(b - a))
        s.append(text(cx, y0 - 7, lab, 13, 700, FG1 if t == "t" else (RED if c == RED else FG2), "middle"))
        if i < len(barras) - 1:
            s.append(line(cx + bw / 2, y(b), cx + paso - bw / 2, y(b), FG4, 1, dash="3 3"))
        for j, trozo in enumerate(r.split("\n")):
            s.append(text(cx, H - bot + 17 + j * 13, trozo, 12, 600 if t == "t" else 400, FG1 if t == "t" else FG2, "middle"))
        if evidencia and i < len(evidencia) and evidencia[i]:
            s.append(_insignia(cx, H - 26, evidencia[i]))
    if evidencia:
        s.append(line(0, H - 40, W, H - 40, GREY, 1))
        s.append(text(0, H - 3, "Nivel de evidencia de cada paso: A verificado, B fuente secundaria, C indicio", 11, 400, FG3))
    return _svg(W, H, "".join(s))


def _insignia(cx, cy, nivel, lado=18):
    """Insignia A, B o C de etiqueta_evidencia dibujada en SVG, centrada en (cx, cy)."""
    x, y = cx - lado / 2, cy - lado / 2
    if nivel == "C":
        return rect(x, y, lado, lado, PAPER, rx=4, stroke=RAMP[3], sw=1.5) + text(cx, cy + 4, "C", 12, 700, RED, "middle")
    return rect(x, y, lado, lado, RAMP[0] if nivel == "A" else RAMP[3], rx=4) + text(cx, cy + 4, nivel, 12, 700, "#fff", "middle")


def curva_s(items, fases=("Innovadores", "Primeros adoptantes", "Mayoría temprana", "Mayoría tardía", "Rezagados"), W=520, H=290):
    """Curva en S de adopción: la adopción acumulada de una tecnología con sus cinco fases y dónde está
    cada opción. items: [(rótulo, posición de 0 a 1 en el eje del tiempo, destacado)].
    Cuándo usarlo: vigilancia tecnológica, para decir si una tecnología es temprana o ya está madura.
    Cuándo no: si hay datos reales de adopción por año (usa linea con los datos)."""
    izq, der, top, bot = 24, 10, 16, 58
    k = 10
    lg = lambda t: 1 / (1 + math.exp(-k * (t - .5)))
    a0, a1 = lg(0), lg(1)
    yv = lambda t: (lg(t) - a0) / (a1 - a0)
    x = lin(0, 1, izq, W - der)
    y = lin(0, 1, H - bot, top)
    cortes = [0] + [.5 + math.log(p / (1 - p)) / k for p in (.025, .16, .5, .84)] + [1]
    tonos = [RAMP[0], RAMP[1], RAMP[2], RAMP[3], RAMP[4]]
    L = Lienzo(W, H)
    for i in range(5):
        x0, x1 = x(cortes[i]), x(cortes[i + 1])
        L.add(rect(x0, H - bot + 8, x1 - x0 - 2, 8, tonos[i]))
        L.div((x0 + x1) / 2, H - bot + 22, max(x1 - x0, 60), f'<span style="font-size:11px;line-height:1.2;color:var(--fg2)">{E(fases[i])}</span>',
              anchor="middle")
        if i:
            L.add(line(x0, top, x0, H - bot, GREY, 1, dash="2 3"))
    d = "M" + " L".join(f"{x(t / 100):.1f},{y(yv(t / 100)):.1f}" for t in range(0, 101, 2))
    L.add(f'<path d="{d}" fill="none" stroke="{FG1}" stroke-width="2.5"/>')
    L.add(arrow_eje(izq, H - bot, W - der + 4, H - bot), arrow_eje(izq, H - bot, izq, top - 6))
    L.add(f'<text transform="translate(12,{top}) rotate(-90)" text-anchor="end" style="font-family:{FONT};font-size:11px;fill:{FG3}">Adopción acumulada</text>')
    for r, t, hot in items:
        cx, cy = x(t), y(yv(t))
        L.add(circle(cx, cy, 7, RED if hot else PAPER, RED if hot else FG1, 2))
        izqd = t > .55
        if yv(t) < .12:
            L.add(text(cx, cy - 14, r, 13, 700 if hot else 600, RED if hot else FG1, "middle", halo=True))
        else:
            L.add(text(cx + (-12 if izqd else 12), cy + 4, r, 13, 700 if hot else 600, RED if hot else FG1, "end" if izqd else "start", halo=True))
    return L.render()


def abanico(eje_x, historico, escenarios, unidad="", W=520, H=280, fmt_valor=None):
    """Abanico de escenarios (fan chart): la serie histórica y, desde hoy, una banda entre el escenario bajo
    y el alto con el central en rojo discontinuo.
    eje_x: rótulos de todo el periodo; historico: valores hasta hoy; escenarios = dict(bajo, base, alto),
    cada uno con los valores futuros (empiezan en el punto siguiente a hoy).
    Cuándo usarlo: previsiones de mercado o de volumen con incertidumbre explícita.
    Cuándo no: si solo hay un escenario (usa linea con la previsión discontinua)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    izq, der, top, bot = 34, 92, 16, 28
    n_h = len(historico)
    todos = historico + escenarios["alto"]
    mx, p = _techo(max(todos))
    x = lin(0, len(eje_x) - 1, izq, W - der)
    y = lin(0, mx, H - bot, top)
    s = []
    v = 0
    while v <= mx + 1e-9:
        s.append(line(izq, y(v), W - der, y(v), GREY if v else FG4, 1))
        s.append(text(izq - 8, y(v) + 4, fmt(v), 11, 400, FG3, "end"))
        v += p
    for i, r in enumerate(eje_x):
        s.append(text(x(i), H - bot + 17, r, 12, 400, FG3, "middle"))
    ult = (n_h - 1, historico[-1])
    serie = lambda vals: [ult] + [(n_h + i, val) for i, val in enumerate(vals)]
    arriba, abajo = serie(escenarios["alto"]), serie(escenarios["bajo"])
    d = "M" + " L".join(f"{x(i):.1f},{y(val):.1f}" for i, val in arriba) + " L" + " L".join(f"{x(i):.1f},{y(val):.1f}" for i, val in reversed(abajo)) + " Z"
    s.append(f'<path d="{d}" fill="{TINT}"/>')
    for nom, c, dash, sw in (("alto", RAMP[4], "4 3", 1.5), ("bajo", RAMP[4], "4 3", 1.5), ("base", RED, "6 4", 2.5)):
        pts = serie(escenarios[nom])
        s.append(f'<path d="M{" L".join(f"{x(i):.1f},{y(val):.1f}" for i, val in pts)}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')
    s.append(f'<path d="M{" L".join(f"{x(i):.1f},{y(val):.1f}" for i, val in enumerate(historico))}" fill="none" stroke="{FG1}" stroke-width="2.5" stroke-linejoin="round"/>')
    s.append(line(x(n_h - 1), top, x(n_h - 1), H - bot, FG3, 1, dash="2 3"))
    s.append(circle(x(n_h - 1), y(historico[-1]), 4.5, FG1))
    s.append(text(x(n_h - 1) - 6, top + 10, "Hoy", 11, 700, FG2, "end"))
    fin = len(eje_x) - 1
    ys = _separar([y(escenarios[k][-1]) for k in ("alto", "base", "bajo")], 15)
    for (k, nom), yy in zip((("alto", "Alto"), ("base", "Base"), ("bajo", "Bajo")), ys):
        s.append(text(x(fin) + 8, yy + 4, f"{nom} · {f(escenarios[k][-1])}", 12, 700 if k == "base" else 400, RED if k == "base" else FG2))
    return _svg(W, H, "".join(s))


def bump(eje_x, series, destacado=None, W=520, H=260):
    """Ranking en el tiempo (bump chart): la posición de cada actor periodo a periodo, con el nuestro en rojo.
    series: [(nombre, [posiciones, 1 = primero])].
    Cuándo usarlo: quién adelanta a quién en un ranking (cuota, patentes, ventas) en 4 a 8 periodos.
    Cuándo no: si importan las distancias entre puestos (usa linea con los valores)."""
    n = len(series)
    izq, der, top, bot = 120, 120, 14, 26
    x = lin(0, len(eje_x) - 1, izq, W - der)
    y = lin(1, n, top + 10, H - bot - 10)
    s = [text(x(i), H - 6, r, 12, 400, FG3, "middle") for i, r in enumerate(eje_x)]
    orden = sorted(range(n), key=lambda k: series[k][0] == destacado)
    for k in orden:
        nom, pos = series[k]
        hot = nom == destacado
        c = RED if hot else FG4
        d = "M" + " L".join(f"{x(i):.1f},{y(p):.1f}" for i, p in enumerate(pos))
        s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{4 if hot else 2.5}" stroke-linejoin="round"/>')
        for i, p in enumerate(pos):
            s.append(circle(x(i), y(p), 10 if hot else 8, c))
            s.append(text(x(i), y(p) + 4, str(p), 11 if hot else 10, 700, "#fff", "middle"))
        s.append(text(x(0) - 16, y(pos[0]) + 4, nom, 13, 700 if hot else 400, RED if hot else FG2, "end"))
        s.append(text(x(len(pos) - 1) + 16, y(pos[-1]) + 4, nom, 13, 700 if hot else 400, RED if hot else FG2))
    return _svg(W, H, "".join(s))


def pequenos_multiplos(items, eje_x, columnas=3, destacado=None, unidad="", W=520, alto=96):
    """Pequeños múltiplos: la misma minigráfica repetida por país o categoría, con una escala común.
    items: [(título, [valores])]; eje_x = (primer rótulo, último rótulo); destacado: título en rojo.
    Cuándo usarlo: comparar la forma de 4 a 12 series sin enredarlas en un solo gráfico.
    Cuándo no: si hay que leer valores exactos de cada punto (usa una tabla)."""
    mx = max(max(v) for _, v in items)
    cw = (W - 12 * (columnas - 1)) / columnas
    celdas = []
    for t, vals in items:
        hot = t == destacado
        c = RED if hot else FG2
        gw, gh = cw - 24, alto - 44
        xx = lin(0, len(vals) - 1, 0, gw)
        yy = lin(0, mx, gh, 4)
        d = "M" + " L".join(f"{xx(i):.1f},{yy(v):.1f}" for i, v in enumerate(vals))
        area = d + f" L{gw:.1f},{gh} L0,{gh} Z"
        g = _svg(gw, gh + 14, f'<path d="{area}" fill="{TINT if hot else LGREY}"/><path d="{d}" fill="none" stroke="{c}" stroke-width="2"/>'
                 + circle(xx(len(vals) - 1), yy(vals[-1]), 3.2, c) + line(0, gh, gw, gh, FG4, 1)
                 + text(0, gh + 12, eje_x[0], 10, 400, FG3) + text(gw, gh + 12, eje_x[1], 10, 400, FG3, "end"))
        celdas.append(f'<div style="background:#fff;border:1px solid {RED if hot else "var(--border-1)"};border-radius:10px;padding:8px 12px">'
                      f'<div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px"><b style="color:{RED if hot else FG1}">{E(t)}</b>'
                      f'<b style="color:{RED if hot else FG1}">{fmt(vals[-1])}{E(unidad)}</b></div>{g}</div>')
    return f'<div style="display:grid;grid-template-columns:repeat({columnas},1fr);gap:12px;width:{W}px">{"".join(celdas)}</div>'


def combo_financiero(periodos, ingresos, ebitda=None, unidad="", cagr=True, margen=True, rotulos=("Ingresos", "EBITDA", "Margen EBITDA"),
                     W=520, H=250, fmt_valor=None):
    """Métricas financieras de una empresa en el tiempo: ingresos en barras rojas, EBITDA en barras grises al lado,
    el margen EBITDA como línea con su porcentaje encima y el CAGR de los ingresos en una píldora sobre una flecha.
    Un periodo sin dato (None) sale rayado. periodos: rótulos; ingresos y ebitda: listas de valores o None.
    Cuándo usarlo: fichas de competidor, proveedor o candidato (3 a 6 periodos), sobre todo en slides hermanas.
    Cuándo no: para comparar varias empresas entre sí (usa barras_agrupadas o tabla_con_barras)."""
    f = fmt_valor or (lambda v: fmt(v))
    n = len(periodos)
    hid, hdefs = hatch()
    leg_y, cagr_y, m0, m1, b0 = 8, 40, 60, 92, 104
    base = H - 22
    mx = max(v for v in ingresos if v is not None) * 1.06
    y = lin(0, mx, base, b0)
    slot = W / n
    s = [line(0, base, W, base, FG4, 1)]
    for i, p in enumerate(periodos):
        cx = slot * (i + .5)
        s.append(text(cx, H - 6, p, 11, 400, FG3, "middle"))
        v = ingresos[i]
        bw = slot * .34
        if v is None:
            s.append(rect(cx - slot * .38, b0 + 30, slot * .76, base - b0 - 30, f"url(#{hid})"))
            s.append(text(cx, b0 + 22, "Sin dato", 11, 600, FG3, "middle"))
            continue
        xi = cx - bw - 2 if ebitda else cx - bw / 2
        s.append(rect(xi, y(v), bw, base - y(v), RED))
        dentro = base - y(v) > 22
        s.append(text(xi + bw / 2, y(v) + 14 if dentro else y(v) - 5, f(v), 11, 700, "#fff" if dentro else RED, "middle"))
        if ebitda and ebitda[i] is not None:
            eb = ebitda[i]
            ew = slot * .24
            s.append(rect(cx + 2, y(max(eb, 0)), ew, base - y(max(eb, 0)), GREY))
            s.append(text(cx + 2 + ew / 2, y(max(eb, 0)) - 5, f(eb), 11, 600, FG2, "middle"))
    if margen and ebitda:
        mg = [(i, ebitda[i] / ingresos[i] * 100) for i in range(n) if ingresos[i] and ebitda[i] is not None]
        if mg:
            lo, hi = min(v for _, v in mg), max(v for _, v in mg)
            ym = lin(lo - 1, hi + 1, m1, m0) if hi > lo else (lambda v: (m0 + m1) / 2)
            pts = [(slot * (i + .5), ym(v)) for i, v in mg]
            s.append(f'<path d="M{" L".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{FG3}" stroke-width="1.5"/>')
            for (a, b), (_, v) in zip(pts, mg):
                s.append(circle(a, b, 3, "#fff", FG3, 1.5) + text(a, b - 7, f"{fmt(round(v))} %", 11, 600, FG2, "middle"))
    if cagr:
        idx = [i for i in range(n) if ingresos[i] is not None]
        if len(idx) > 1 and ingresos[idx[0]] > 0:
            a, b = idx[0], idx[-1]
            c = ((ingresos[b] / ingresos[a]) ** (1 / (b - a)) - 1) * 100
            x0, x1 = slot * (a + .5), slot * (b + .5)
            s.append(arrow([(x0, cagr_y), (x1, cagr_y)], mezcla(RED, "#FFFFFF", .35), 1.5, size=7))
            s.append(rect((x0 + x1) / 2 - 52, cagr_y - 10, 104, 20, "#fff", rx=10, stroke=RED, sw=1.2))
            s.append(text((x0 + x1) / 2, cagr_y + 4, f"CAGR {'+' if c >= 0 else ''}{fmt(round(c, 1))} %", 11, 700, RED, "middle"))
    ley = [(RED, rotulos[0], "cuadro")] + ([(GREY, rotulos[1], "cuadro")] if ebitda else []) + ([(FG3, rotulos[2], "linea")] if ebitda and margen else [])
    x = 0
    for c, t, forma in ley:
        s.append(rect(x, leg_y, 14, 3, c) if forma == "linea" else rect(x, leg_y - 4, 10, 10, c, rx=2))
        s.append(text(x + 18, leg_y + 4, t, 11, 400, FG2))
        x += 30 + len(t) * 6
    if unidad:
        s.append(text(W, leg_y + 4, unidad, 11, 400, FG3, "end"))
    return _svg(W, H, "".join(s), hdefs)
