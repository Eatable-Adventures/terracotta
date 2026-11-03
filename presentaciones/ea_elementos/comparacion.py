"""Comparación: frente a un objetivo, una referencia o entre sí.

Familia 04 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (
    E, FG1, FG2, FG3, FG4, FILL, FONT, GREY, INPUT, LGREY, Lienzo, NEUTRO, PAPER, RAMP, RED, VALIDACION,
    _arco, _bv, _paso, _set, _svg, arrow_eje, circle, fmt, lin, line, log, md, mezcla, rect, sobre, text,
)
from .marcas import (_con_leyenda)

__all__ = ["barras_duelo", "regleta_objetivo", "barras_objetivo", "escala_log", "REFERENCIA", "radar", "mancuerna", "bala", "tornado", "rangos", "indicador", "barra_dividida", "dimensionamiento", "deslizadores", "benchmark_rango", "criterios_puntos", "score_dimensiones"]


def barras_duelo(d0, d1, referencia, objetivo, fmt_valor, rotulos=("Referencia", "Objetivo"), pie="", W=290):
    """Dos barras: la referencia (gris) frente al objetivo (rojo). referencia y objetivo = (valor, texto | None);
    si el texto es None se formatea con fmt_valor. pie: nota del eje («eje desde 70%», «menos es mejor»).
    Cuándo usarlo: dentro de una tarjeta_kpi, para enseñar la distancia a un umbral.
    Cuándo no: con más de dos valores (usa barras_objetivo)."""
    L = Lienzo(W, 78)
    s = lin(d0, d1, 78, W - 78)
    for i, (lab, (v, t), col) in enumerate([(rotulos[0], referencia, FG4), (rotulos[1], objetivo, RED)]):
        y = 6 + i * 30
        L.div(0, y + 9, 74, f'<b style="color:{FG1 if i else FG2}">{E(lab)}</b>', va="middle", style="font-size:13px")
        L.add(rect(78, y, s(v) - 78, 18, col, rx=5), text(s(v) + 7, y + 14, t if t is not None else fmt_valor(v), 14, 700, RED if i else FG1))
    if pie:
        L.add(text(78, 75, pie, 11, 400, FG3))
    return L.render()


def regleta_objetivo(d0, d1, zona, zona_txt, marcas=(), ticks=(), W=260):
    """Regleta con la zona objetivo en rojo, marcas de referencia en negro y ticks del eje.
    zona = (desde, hasta); marcas = [(valor, texto)]; ticks = [(valor, texto)].
    Cuándo usarlo: un precio o rango negociable dentro de una tarjeta_kpi.
    Cuándo no: para un umbral único (usa barras_duelo)."""
    L = Lienzo(W, 76)
    s = lin(d0, d1, 0, W)
    L.add(rect(0, 28, W, 14, FILL, rx=7), rect(s(zona[0]), 28, s(zona[1]) - s(zona[0]), 14, RED, rx=7))
    for v, t in marcas:
        L.add(line(s(v), 20, s(v), 50, FG1, 2), text(s(v), 13, t, 12, 600, FG1, "middle"))
    for v, t in ticks:
        L.add(text(s(v), 66, t, 11, 400, FG3, "middle"))
    L.add(text((s(zona[0]) + s(zona[1])) / 2, 66, zona_txt, 12, 700, RED, "middle"))
    return L.render()


def barras_objetivo(filas, dominio, objetivo, colores, ticks, pie_eje="", leyenda=None, fmt_tick=lambda v: f"{fmt(v)}%",
                    W=600, ancho_rotulo=150, paso=58, alto_barra=32):
    """Barras horizontales frente a una línea de objetivo, con la cifra dentro de la barra.
    filas: [(rótulo, valor, texto, categoría)]; colores: {categoría: color}; objetivo = (valor, rótulo);
    ticks: valores del eje (fmt_tick los formatea, en % por defecto); leyenda: [(color, texto)] arriba a la izquierda.
    Cuándo usarlo: de 3 a 8 opciones en la misma métrica y lo que importa es la distancia al objetivo.
    Cuándo no: si las opciones tienen rangos (usa escala_log) o si las métricas son varias (usa tabla_referencia)."""
    n = len(filas)
    yb = 40 + n * paso - 16
    H = yb + 54
    L = Lienzo(W, H)
    s = lin(dominio[0], dominio[1], ancho_rotulo, W - 20)
    for v in ticks:
        L.add(line(s(v), 28, s(v), yb, GREY, 1, dash="2 4"), text(s(v), yb + 20, fmt_tick(v), 12, 400, FG3, "middle"))
    L.add(line(s(objetivo[0]), 24, s(objetivo[0]), yb, RED, 2, dash="6 4"), text(s(objetivo[0]), 14, objetivo[1], 13, 700, RED, "middle"))
    for i, (lab, v, t, k) in enumerate(filas):
        y = 40 + i * paso
        col = colores[k]
        L.div(ancho_rotulo - 10, y + alto_barra / 2, ancho_rotulo - 10, E(lab), anchor="end", va="middle", style="font-size:14px;color:var(--fg1)")
        L.add(rect(ancho_rotulo, y, s(v) - ancho_rotulo, alto_barra, col, rx=6), text(s(v) - 10, y + 21.5, t, 15, 700, sobre(col), "end"))
    if pie_eje:
        L.add(text(ancho_rotulo, H - 2, pie_eje, 12, 400, FG3))
    if leyenda:
        L.div(0, 0, W / 2, "".join(f'<span style="display:inline-flex;gap:5px;align-items:center;font-size:12px;color:var(--fg3);margin-right:14px">'
                                   f'<i style="width:10px;height:10px;border-radius:3px;background:{c};display:inline-block"></i>{E(t)}</span>' for c, t in leyenda))
    return L.render()


def escala_log(filas, referencia=(1, "Referencia"), umbral=(10, "10 veces"), dominio=(0.1, 1000),
               ticks=((0.1, "0,1"), (1, "1"), (10, "10"), (100, "100"), (1000, "1.000")),
               titulo_eje="Veces la referencia (escala logarítmica)", rotulo_columna="Veces la referencia, media",
               W=830, rh=40, ancho_rotulo=268):
    """Escala logarítmica de veces una referencia: un punto por alternativa en la media geométrica de su rango
    (el centro en escala log), el rango tenue detrás, el umbral en rojo discontinuo y las cifras en una columna a
    la derecha, sin líneas que las crucen. En rojo lo que supera el umbral.
    filas: [(alternativa, mínimo, máximo | None, etiqueta)]; referencia y umbral = (valor, rótulo).
    Cuándo usarlo: costes o magnitudes que cruzan dos o tres órdenes de magnitud frente a una referencia.
    Cuándo no: si todo cae en el mismo orden de magnitud (usa barras_objetivo); el lector no técnico necesita el «×» en la etiqueta."""
    xl, x1 = ancho_rotulo, W - 92
    top = 30
    yb = top + len(filas) * rh
    H = yb + 44
    L = Lienzo(W, H)
    s = log(dominio[0], dominio[1], xl, x1)
    u = umbral[0]
    for v, lab in ticks:
        L.add(line(s(v), top - 8, s(v), yb, GREY, 1, dash="2 4"), text(s(v), yb + 18, lab, 12, 400, FG3, "middle"))
    L.add(text(xl, yb + 36, titulo_eje, 12, 400, FG3))
    L.add(line(s(referencia[0]), top - 14, s(referencia[0]), yb, FG1, 1.5), line(s(u), top - 14, s(u), yb, RED, 1.5, dash="5 4"))
    L.add(text(s(referencia[0]), top - 18, referencia[1], 12, 600, FG1, "middle"), text(s(u), top - 18, umbral[1], 12, 600, RED, "middle"))
    for k, (alt, a, b, etq) in enumerate(filas):
        y = top + k * rh + rh / 2
        L.div(xl - 14, y, xl - 14, E(alt), anchor="end", va="middle", style="font-size:14px;color:var(--fg1);line-height:1.2")
        if b is None:
            m = a
            L.add(circle(s(a), y, 6, RED if a > u else FG2))
        else:
            m = math.sqrt(a * b)
            L.add(line(s(a), y, s(b), y, GREY, 4, cap="round"), circle(s(m), y, 7.5, RED if m > u else FG1, "#fff", 2))
        alto = m > u
        L.add(text(W - 2, y + 4.5, etq, 14, 700 if alto else 600, RED if alto else FG1, "end"))
    L.add(text(W - 2, top - 18, rotulo_columna, 12, 600, FG3, "end"))
    return L.render()


REFERENCIA = FG3      # segunda serie de otra naturaleza (referencia, competidor, año anterior)


def radar(ejes, series, maximo=5, niveles=5, W=440, H=340, rotulo_nivel=True):
    """Gráfico de araña (radar): el perfil de una o dos opciones sobre 5 a 8 criterios de la misma escala.
    ejes: nombres de los criterios; series: [(nombre, [valores])]. La primera serie va en rojo con relleno;
    la segunda, en gris discontinuo (la referencia).
    Cuándo usarlo: comparar perfiles (nosotros frente a la media del sector, candidato A frente a B).
    Cuándo no: más de dos series o criterios con escalas distintas (usa matriz_puntuacion o tabla_comparativa)."""
    cx, cy = W / 2, H / 2 + 6
    R = min(W, H) / 2 - 58
    n = len(ejes)
    ang = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
    pt = lambda i, v: (cx + R * v / maximo * math.cos(ang[i]), cy + R * v / maximo * math.sin(ang[i]))
    s = []
    for k in range(1, niveles + 1):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, maximo * k / niveles) for i in range(n)))
        s.append(f'<polygon points="{pts}" fill="{LGREY if k == niveles else "none"}" stroke="{GREY}" stroke-width="1"/>')
    for i, e in enumerate(ejes):
        x, y = pt(i, maximo)
        s.append(line(cx, cy, x, y, GREY, 1))
        lx, ly = pt(i, maximo * 1.13)
        c = math.cos(ang[i])
        anc = "middle" if abs(c) < .3 else ("start" if c > 0 else "end")
        s.append(text(lx, ly + 4, e, 13, 600, FG1, anc))
    if rotulo_nivel:
        for k in range(1, niveles + 1):
            s.append(text(cx + 4, pt(0, maximo * k / niveles)[1] + 10, fmt(maximo * k / niveles), 10, 400, FG3))
    for k, (_, vals) in reversed(list(enumerate(series))):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, v) for i, v in enumerate(vals)))
        if k == 0:
            s.append(f'<polygon points="{pts}" fill="{RED}" fill-opacity=".16" stroke="{RED}" stroke-width="2.5" stroke-linejoin="round"/>')
            s.extend(circle(*pt(i, v), 4, RED) for i, v in enumerate(vals))
        else:
            s.append(f'<polygon points="{pts}" fill="none" stroke="{REFERENCIA}" stroke-width="2" stroke-dasharray="5 4" stroke-linejoin="round"/>')
    items = [(RED, series[0][0], "linea")] + ([(REFERENCIA, series[1][0], "discontinua")] if len(series) > 1 else [])
    return _con_leyenda(_svg(W, H, "".join(s)), items)


def mancuerna(filas, rotulos=("Actual", "Objetivo"), dominio=None, unidad="", W=520, ancho_rotulo=140, paso=34, fmt_valor=None, H=None):
    """Mancuerna (dumbbell): dos puntos por fila unidos por una línea; la distancia es el mensaje.
    Fondo gris claro único para toda la zona del gráfico, sin separadores.
    filas: [(rótulo, valor_a, valor_b)]; el punto b va en rojo.
    Cuándo usarlo: brecha entre dos estados por elemento (actual frente a objetivo, nosotros frente al líder).
    Cuándo no: si interesan los valores absolutos más que la distancia (usa barras_agrupadas)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    vals = [v for _, a, b in filas for v in (a, b)]
    d0, d1 = dominio or (min(vals), max(vals))
    x = lin(d0, d1, ancho_rotulo + 44, W - 52)
    paso = (H - 24) / len(filas) if H else paso        # H: alto total, leyenda incluida
    H = len(filas) * paso
    s = [rect(ancho_rotulo, 0, W - ancho_rotulo, H, LGREY, rx=8)]
    for i, (r, a, b) in enumerate(filas):
        yc = i * paso + paso / 2
        s.append(text(ancho_rotulo - 10, yc + 4.5, r, 13, 400, FG2, "end"))
        s.append(line(x(a), yc, x(b), yc, FG4, 3))
        s.append(circle(x(a), yc, 7, REFERENCIA) + circle(x(b), yc, 7, RED))
        lo, hi = (a, b) if a <= b else (b, a)
        s.append(text(x(lo) - 13, yc + 4.5, f(lo), 13, 700, RED if lo == b else FG2, "end"))
        s.append(text(x(hi) + 13, yc + 4.5, f(hi), 13, 700, RED if hi == b else FG2))
    return _con_leyenda(_svg(W, H, "".join(s)), [(REFERENCIA, rotulos[0], "punto"), (RED, rotulos[1], "punto")])


def bala(filas, unidad="", W=520, ancho_rotulo=140, fmt_valor=None):
    """Avance hacia objetivo (sustituye al gráfico de bala clásico): por KPI, una pista gris hasta el máximo de la
    escala, la barra roja hasta el valor real y una marca negra con la cifra del objetivo encima; a la derecha,
    el valor y el porcentaje del objetivo alcanzado (verde si lo cumple).
    filas: [dict(rotulo, valor, objetivo, maximo, sub=None, menor_mejor=False, unidad=None)].
    Cuándo usarlo: cuadros de mando con 3 a 6 KPI frente a su objetivo, en poco espacio.
    Cuándo no: un único KPI protagonista (usa indicador o cifra_delta)."""
    der, alto, sep = 112, 10, 40
    H = len(filas) * (alto + sep) + 4
    L = Lienzo(W, H)
    for i, d in enumerate(filas):
        y0 = 22 + i * (alto + sep)
        x = lin(0, d["maximo"], ancho_rotulo, W - der)
        f = fmt_valor or (lambda v, u=d.get("unidad", unidad): fmt(v) + u)
        L.add(rect(ancho_rotulo, y0, W - der - ancho_rotulo, alto, FILL, rx=5))
        L.add(rect(ancho_rotulo, y0, x(d["valor"]) - ancho_rotulo, alto, RED, rx=5))
        xo = x(d["objetivo"])
        L.add(line(xo, y0 - 6, xo, y0 + alto + 6, FG1, 2.5))
        L.add(text(xo, y0 - 10, f"Objetivo {f(d['objetivo'])}", 11, 600, FG1, "middle"))
        L.div(ancho_rotulo - 12, y0 + alto / 2, ancho_rotulo - 12, f'<b style="font-size:13px;color:var(--fg1)">{E(d["rotulo"])}</b>'
              + (f'<div style="font-size:11px;color:var(--fg3)">{E(d["sub"])}</div>' if d.get("sub") else ""), anchor="end", va="middle")
        pct = (d["objetivo"] / d["valor"] if d.get("menor_mejor") else d["valor"] / d["objetivo"]) * 100
        ok = pct >= 99.5
        L.div(W - der + 14, y0 + alto / 2, der - 14, f'<b style="font-size:15px;color:var(--red)">{E(f(d["valor"]))}</b>'
              f'<div style="font-size:11px;font-weight:600;color:{VALIDACION if ok else FG2}">{round(pct)} % del objetivo</div>', va="middle")
    return L.render()


def tornado(filas, base, rotulos=("Escenario bajo", "Escenario alto"), unidad="", W=520, ancho_rotulo=150, alto=20, sep=10, fmt_valor=None):
    """Tornado (sensibilidad): cuánto mueve cada variable el resultado hacia abajo y hacia arriba.
    filas: [(variable, resultado_bajo, resultado_alto)], se ordenan por amplitud; base: resultado central.
    Cuándo usarlo: decir qué supuesto del modelo pesa más (precio, coste de materia prima, volumen).
    Cuándo no: si las variables no son independientes o no hay un caso base."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    fs = sorted(filas, key=lambda r: -(r[2] - r[1]))
    lo = min(r[1] for r in fs)
    hi = max(r[2] for r in fs)
    m = max(base - lo, hi - base) * 1.05
    x = lin(base - m, base + m, ancho_rotulo + 40, W - 40)
    H = len(fs) * (alto + sep) - sep + 26
    s = []
    for i, (r, a, b) in enumerate(fs):
        y0 = 22 + i * (alto + sep)
        s.append(text(ancho_rotulo - 10, y0 + alto / 2 + 4.5, r, 13, 400, FG2, "end"))
        s.append(rect(x(a), y0, x(base) - x(a), alto, RAMP[4]))
        s.append(rect(x(base), y0, x(b) - x(base), alto, RED))
        s.append(text(x(a) - 6, y0 + alto / 2 + 4.5, f(a), 12, 600, FG2, "end"))
        s.append(text(x(b) + 6, y0 + alto / 2 + 4.5, f(b), 12, 700, RED))
    s.append(line(x(base), 14, x(base), H, FG1, 1.5))
    s.append(text(x(base), 9, f"Caso base {f(base)}", 12, 700, FG1, "middle"))
    return _con_leyenda(_svg(W, H, "".join(s)), [(RAMP[4], rotulos[0]), (RED, rotulos[1])])


def rangos(filas, marca=None, destacado=None, unidad="", W=520, ancho_rotulo=150, alto=20, sep=14, fmt_valor=None):
    """Rangos flotantes (football field): el mínimo y el máximo de cada método o fuente sobre un mismo eje.
    filas: [(rótulo, mínimo, máximo)]; marca = (valor, texto) como línea vertical (precio ofertado, objetivo).
    Cuándo usarlo: valoraciones, horquillas de precio o de coste según la fuente.
    Cuándo no: si cada fila es un valor único (usa piruletas)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    dest = _set(destacado)
    vals = [v for _, a, b in filas for v in (a, b)] + ([marca[0]] if marca else [])
    p = _paso(max(vals) - min(vals), 5)
    d0, d1 = math.floor(min(vals) / p) * p, math.ceil(max(vals) / p) * p
    x = lin(d0, d1, ancho_rotulo + 36, W - 40)
    fin = 22 + len(filas) * (alto + sep) - sep
    H = fin + 34
    s = []
    for i, (r, a, b) in enumerate(filas):
        y0, hot = 22 + i * (alto + sep), r in dest
        s.append(text(ancho_rotulo - 10, y0 + alto / 2 + 4.5, r, 13, 600 if hot else 400, FG1 if hot else FG2, "end"))
        s.append(rect(x(a), y0, x(b) - x(a), alto, RED if hot else NEUTRO, rx=3))
        s.append(text(x(a) - 6, y0 + alto / 2 + 4.5, f(a), 12, 600, FG2, "end"))
        s.append(text(x(b) + 6, y0 + alto / 2 + 4.5, f(b), 12, 600, FG2))
    yb = fin + 22
    s.append(line(ancho_rotulo + 36, yb - 8, W - 40, yb - 8, FG4, 1))
    v = d0
    while v <= d1 + 1e-9:
        s.append(text(x(v), yb + 6, fmt(v), 11, 400, FG3, "middle"))
        v += p
    if marca:
        s.append(line(x(marca[0]), 14, x(marca[0]), yb - 8, RED, 1.5, dash="4 3"))
        s.append(text(x(marca[0]), 9, marca[1], 12, 700, RED, "middle"))
    return _svg(W, H, "".join(s))


def indicador(valor, minimo, maximo, cifra, rotulo, objetivo=None, W=280):
    """Indicador semicircular (gauge) con la cifra en el centro y una marca de objetivo opcional.
    objetivo = (valor, texto).
    Cuándo usarlo: un único KPI de avance o de grado de cumplimiento, como pieza de portada de un bloque.
    Cuándo no: varios KPI juntos (usa bala); ocupa mucho para un solo número."""
    cx, R, g = W / 2, W / 2 - 22, 22
    cy = R + 20
    a = lambda v: math.pi + math.pi * (v - minimo) / (maximo - minimo)
    s = [f'<path d="{_arco(cx, cy, R, math.pi, 2 * math.pi - 1e-6)}" fill="none" stroke="{FILL}" stroke-width="{g}"/>',
         f'<path d="{_arco(cx, cy, R, math.pi, a(valor))}" fill="none" stroke="{RED}" stroke-width="{g}"/>']
    if objetivo:
        ao = a(objetivo[0])
        s.append(line(cx + (R - g / 2 - 4) * math.cos(ao), cy + (R - g / 2 - 4) * math.sin(ao),
                      cx + (R + g / 2 + 4) * math.cos(ao), cy + (R + g / 2 + 4) * math.sin(ao), FG1, 2.5))
        s.append(text(cx + (R + g / 2 + 10) * math.cos(ao), cy + (R + g / 2 + 10) * math.sin(ao), objetivo[1], 12, 700, FG1,
                      "start" if math.cos(ao) > 0.1 else ("end" if math.cos(ao) < -0.1 else "middle")))
    s.append(text(cx - R, cy + 18, fmt(minimo), 11, 400, FG3, "middle"))
    s.append(text(cx + R, cy + 18, fmt(maximo), 11, 400, FG3, "middle"))
    H = cy + 26
    L = Lienzo(W, H).add(*s)
    L.div(cx, cy - 8, R * 1.3, f'<div class="big" style="font-size:34px">{E(cifra)}</div>'
          f'<div style="font-size:13px;margin-top:4px">{E(rotulo)}</div>', anchor="middle", va="bottom")
    return L.render()


def barra_dividida(filas, escala=("Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"),
                   W=520, ancho_rotulo=160, alto=24, sep=12):
    """Barra dividida (diverging): respuestas de una escala Likert centradas en el neutro; el desacuerdo a la
    izquierda en grises y el acuerdo a la derecha en rojos.
    filas: [(afirmación, [5 porcentajes])].
    Cuándo usarlo: encuestas a consumidores o paneles internos (aceptación, intención de compra).
    Cuándo no: escalas que no son simétricas (usa barras_apiladas)."""
    cols = [FG3, FG4, GREY, RAMP[4], RED]
    lado = max(max(v[0] + v[1] + v[2] / 2, v[3] + v[4] + v[2] / 2) for _, v in filas)
    cx = ancho_rotulo + (W - ancho_rotulo) / 2
    u = (W - ancho_rotulo) / 2 / lado
    H = len(filas) * (alto + sep) - sep
    s = [line(cx, -6, cx, H + 6, FG1, 1)]
    for i, (r, v) in enumerate(filas):
        y0 = i * (alto + sep)
        s.append(text(ancho_rotulo - 12, y0 + alto / 2 + 4.5, r, 13, 400, FG2, "end"))
        x0 = cx - (v[0] + v[1] + v[2] / 2) * u
        for k, val in enumerate(v):
            w = val * u
            s.append(rect(x0, y0, max(w - 1.5, 0), alto, cols[k]))
            if w > 26:
                s.append(text(x0 + w / 2, y0 + alto / 2 + 4.5, f"{val}", 12, 600, sobre(cols[k]), "middle"))
            x0 += w
    return f'<div style="flex:none;width:{W}px">{_con_leyenda(_svg(W, H, "".join(s)), list(zip(cols, escala)))}</div>'


def dimensionamiento(pasos, unidad="", W=520, H=290, fmt_valor=None):
    """Dimensionamiento de arriba abajo: del mercado total al alcanzable en columnas decrecientes, con lo que
    queda en cada paso (porcentaje del anterior) y el último nivel en rojo con su peso sobre el total.
    pasos: [(rótulo, valor)] de mayor a menor (TAM, SAM, SOM o los filtros del Modelo de Mercado).
    Cuándo usarlo: explicar cómo se llega a la cifra de mercado relevante desde una fuente amplia.
    Cuándo no: si los pasos no son filtros sucesivos sobre la misma base (usa cascada)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    top, bot = 44, 48
    n = len(pasos)
    paso = W / n
    bw = min(70, paso * .5)
    y = lin(0, pasos[0][1], H - bot, top)
    L = Lienzo(W, H)
    s = [line(0, H - bot, W, H - bot, FG4, 1)]
    for i, (r, v) in enumerate(pasos):
        cx = paso * (i + .5)
        ult = i == n - 1
        if i < n - 1:
            nx = paso * (i + 1.5)
            v2 = pasos[i + 1][1]
            s.append(f'<polygon points="{cx + bw / 2:.1f},{y(v):.1f} {nx - bw / 2:.1f},{y(v2):.1f} {nx - bw / 2:.1f},{H - bot} {cx + bw / 2:.1f},{H - bot}" fill="{LGREY}"/>')
            pct = f"{round(v2 / v * 100)} %"
            mx_ = (cx + nx) / 2
            my_ = (y(v) + y(v2)) / 2 - 16
            s.append(rect(mx_ - 24, my_ - 10, 48, 20, PAPER, rx=10, stroke=FG4, sw=1) + text(mx_, my_ + 4, pct, 12, 700, FG2, "middle"))
        s.append(_bv(cx - bw / 2, y(v), bw, H - bot - y(v), RED if ult else (FG3 if i == 0 else NEUTRO)))
        s.append(text(cx, y(v) - 8, f(v), 14, 700, RED if ult else FG1, "middle"))
        extra = f'<div style="font-size:11px;color:var(--fg3)">{fmt(round(v / pasos[0][1] * 100, 1))} % del total</div>' if ult else ""
        L.div(cx, H - bot + 7, paso - 6, f'<span style="font-size:12px;line-height:1.2;font-weight:{700 if ult else 400};'
              f'color:{RED if ult else FG2}">{E(r)}</span>{extra}', anchor="middle")
    return L.add(*s).render()


def deslizadores(filas, extremos=("Bajo", "Alto"), W=520, ancho_rotulo=130, ancho_pista=150):
    """Deslizadores de valoración: por fila, una regleta de «bajo» a «alto» con un punto rojo y la razón al lado.
    filas: [dict(rotulo, valor de 0 a 1, texto, grupo=None)]; un cambio de grupo abre un subtítulo.
    Cuándo usarlo: valoraciones cualitativas argumentadas (barreras de entrada, riesgos, madurez, atractivo).
    Cuándo no: si hay un dato numérico comparable (usa benchmark_rango o barras)."""
    out, grupo = [], None
    for d in filas:
        if d.get("grupo") and d["grupo"] != grupo:
            grupo = d["grupo"]
            out.append(f'<div class="k2" style="margin:8px 0 2px">{E(grupo)}</div>')
        pos = max(0, min(1, d["valor"])) * 100
        out.append(f'<div style="display:flex;align-items:center;gap:12px;padding:7px 0;border-bottom:1px solid var(--border-2)">'
                   f'<b style="width:{ancho_rotulo}px;flex:none;font-size:13px;color:var(--fg1)">{E(d["rotulo"])}</b>'
                   f'<span style="font-size:11px;color:var(--fg3)">{E(extremos[0])}</span>'
                   f'<span style="position:relative;width:{ancho_pista}px;height:8px;flex:none;border-radius:99px;background:var(--surface-fill)">'
                   f'<i style="position:absolute;left:0;top:0;bottom:0;width:{pos:.0f}%;border-radius:99px;background:{mezcla(RED, "#FFFFFF", .7)}"></i>'
                   f'<i style="position:absolute;left:calc({pos:.0f}% - 8px);top:-4px;width:16px;height:16px;border-radius:50%;background:var(--red);box-shadow:0 0 0 2px #fff"></i></span>'
                   f'<span style="font-size:11px;color:var(--fg3)">{E(extremos[1])}</span>'
                   f'<span style="flex:1;font-size:13px;line-height:1.35;color:var(--fg2);padding-left:6px">{md(d.get("texto", ""))}</span></div>')
    return f'<div style="width:{W}px">{"".join(out)}</div>'


def benchmark_rango(filas, rotulos=("KPI", "Nosotros", "Peor", "Posición en el rango", "Mejor"), W=520):
    """Benchmark en rango: por KPI, nuestro valor y su posición entre el peor y el mejor de los comparables
    (cada fila con su propia escala), con la mediana marcada.
    filas: [dict(kpi, propio, peor, mejor, mediana=None, unidad='')]; si el mejor es el menor (costes),
    se pasa así y la regleta se orienta sola.
    Cuándo usarlo: benchmarking financiero u operativo frente a 5 a 15 comparables.
    Cuándo no: si hay que ver a cada comparable por separado (usa barras_ranking)."""
    def pista(d):
        t = lambda v: max(0, min(1, (v - d["peor"]) / (d["mejor"] - d["peor"]))) * 100
        med = (f'<i style="position:absolute;left:{t(d["mediana"]):.0f}%;top:-3px;height:14px;border-left:2px solid var(--fg3)"></i>'
               if d.get("mediana") is not None else "")
        return (f'<span style="position:relative;display:block;height:8px;border-radius:99px;background:linear-gradient(90deg,{FILL},{INPUT})">{med}'
                f'<i style="position:absolute;left:calc({t(d["propio"]):.0f}% - 7px);top:-9px;width:0;height:0;border-left:7px solid transparent;'
                f'border-right:7px solid transparent;border-top:10px solid var(--red)"></i></span>')
    u = lambda d, v: fmt(v) + d.get("unidad", "")
    hd = "".join(f'<th style="{"text-align:center;" if k else ""}">{E(r)}</th>' for k, r in enumerate(rotulos))
    cuerpo = "".join(f'<tr><td class="nm">{E(d["kpi"])}</td><td style="text-align:center;white-space:nowrap"><b style="color:var(--red);font-size:14px">{E(u(d, d["propio"]))}</b></td>'
                     f'<td style="text-align:center;white-space:nowrap">{E(u(d, d["peor"]))}</td><td style="width:34%;padding-top:16px">{pista(d)}</td>'
                     f'<td style="text-align:center;white-space:nowrap">{E(u(d, d["mejor"]))}</td></tr>' for d in filas)
    pie = ('<div style="font-size:11px;color:var(--fg3);margin-top:6px">Triángulo rojo: nuestra posición · trazo gris: mediana de los comparables</div>')
    return f'<div style="width:{W}px"><table class="tb"><thead><tr>{hd}</tr></thead><tbody>{cuerpo}</tbody></table>{pie}</div>'


def criterios_puntos(criterios, actores, destacado, escala=(1, 5), W=520, ancho_rotulo=170, paso=34):
    """Criterios por importancia con la nota de cada actor como puntos sobre una misma escala; el actor que
    importa en rojo con su nota, el resto en gris.
    criterios: [(nombre, [nota por actor])] ordenados de más a menos importante; actores: nombres.
    Cuándo usarlo: candidatos frente a los criterios del cliente, o marca frente a competidores en un estudio.
    Cuándo no: más de 8 actores (los puntos se amontonan; usa tabla_comparativa)."""
    k = actores.index(destacado)
    x = lin(escala[0], escala[1], ancho_rotulo + 20, W - 40)
    H = 26 + len(criterios) * paso
    s = [text(x(v), 12, fmt(v), 11, 400, FG3, "middle") for v in range(escala[0], escala[1] + 1)]
    s.append(arrow_eje(8, 34, 8, H - 6).replace(f'fill="{FG2}"', f'fill="{FG3}"'))
    s.append(f'<text transform="translate(20,{26 + paso / 2}) rotate(90)" style="font-family:{FONT};font-size:10px;fill:{FG3}">Más importante</text>')
    for i, (nom, notas) in enumerate(criterios):
        yc = 26 + i * paso + paso / 2
        s.append(text(ancho_rotulo, yc + 4.5, nom, 13, 400, FG1, "end"))
        s.append(line(x(escala[0]), yc, x(escala[1]), yc, GREY, 6, cap="round"))
        for j, v in enumerate(notas):
            if j != k:
                s.append(f'<circle cx="{x(v):.1f}" cy="{yc}" r="5.5" fill="{FG4}" fill-opacity=".85" stroke="#fff" stroke-width="1.5"/>')
        s.append(circle(x(notas[k]), yc, 7.5, RED, "#fff", 2) + text(x(notas[k]) + 12, yc - 7, fmt(notas[k]), 12, 700, RED))
    return _con_leyenda(_svg(W, H, "".join(s)), [(RED, destacado, "punto"), (FG4, "Resto de actores", "punto")])


def score_dimensiones(dimensiones, total=None, escala=(0, 10), referencia=None, rotulo_total="Total", W=520, ancho_rotulo=150):
    """Puntuación por dimensiones: una pista por dimensión con el punto rojo en su valor y, a la derecha, el total
    grande sobre la escala (por defecto la media). Con referencia, un aro gris marca otro actor en cada pista.
    dimensiones: [(nombre, valor)]; referencia: [valores] en el mismo orden, o None.
    Cuándo usarlo: el score de un actor en fichas hermanas (RTW, scoring de candidatos) o de un escenario.
    Cuándo no: para comparar muchos actores a la vez (usa matriz_puntuacion o criterios_puntos)."""
    a, b = escala
    tot = total if total is not None else sum(v for _, v in dimensiones) / len(dimensiones)
    pos = lambda v: max(0, min(1, (v - a) / (b - a))) * 100
    filas = ""
    for k, (nom, v) in enumerate(dimensiones):
        ref = (f'<i style="position:absolute;left:calc({pos(referencia[k]):.1f}% - 6px);top:-3px;width:12px;height:12px;border-radius:50%;'
               f'box-shadow:inset 0 0 0 2px {FG3};background:#fff"></i>' if referencia else "")
        filas += (f'<div style="display:flex;align-items:center;gap:12px;height:30px"><span style="width:{ancho_rotulo}px;flex:none;font-size:13px;color:var(--fg1)">{E(nom)}</span>'
                  f'<span style="position:relative;flex:1;height:6px;border-radius:99px;background:var(--surface-fill)">{ref}'
                  f'<i style="position:absolute;left:calc({pos(v):.1f}% - 7px);top:-4px;width:14px;height:14px;border-radius:50%;background:var(--red);box-shadow:0 0 0 2px #fff"></i></span></div>')
    return (f'<div style="width:{W}px;display:flex;align-items:center;gap:22px"><div style="flex:1;min-width:0">{filas}</div>'
            f'<div style="flex:none;width:96px;border-left:1px solid var(--border-2);padding-left:18px">'
            f'<div style="white-space:nowrap"><b style="font-size:30px;color:var(--red);letter-spacing:-.02em">{fmt(round(tot, 1))}</b>'
            f'<span style="font-size:14px;font-weight:700;color:var(--fg1)">/{fmt(b)}</span></div>'
            f'<div style="font-size:13px;font-weight:700;color:var(--fg1);margin-top:2px">{E(rotulo_total)}</div></div></div>')
