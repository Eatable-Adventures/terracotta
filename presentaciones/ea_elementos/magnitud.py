"""Magnitud: cuánto: comparar cantidades.

Familia 01 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (
    E, FG1, FG2, FG3, FG4, INPUT, LGREY, Lienzo, NEUTRO, PAPER, RED, _bv, _set, _svg, circle, fmt,
    funnel_svg, hatch, head, lin, line, md, mezcla, rampa, rect, sobre, text,
)
from .marcas import (_con_leyenda, delta)

from .base import (_logo_html, flecha_svg)  # añadidos el 01-11-2026

__all__ = ["embudo", "columnas", "barras_ranking", "barras_agrupadas", "barras_apiladas", "piruletas", "pictograma", "pareto", "comparador_unidad", "barras_variacion", "ranking_logos"]


def embudo(etapas, clave=None, objetivo=None, label_size=15, sub_size=12, W=None):
    """Embudo canónico de discos apilados (embudo_canonico.py, no se duplica aquí). etapas: [(nombre, subtítulo, valor)].
    clave: índice de la etapa cuya etiqueta se refuerza (solo sube el peso, de 600 a 700; los discos no cambian).
    label_size y sub_size: a la escala del texto vecino.
    W: ancho en px; si se da, label_size y sub_size son los px reales de la slide, sea cual sea el ancho.
    El alto sale de W y del número de etapas (proporción fija del embudo canónico): para llenar, 4 o 5 etapas y lectura al lado.
    Cuándo usarlo: un cribado con etapas (documentos, candidatos), uno por bloque como máximo.
    Cuándo no: si las etapas no son un filtro sucesivo, o si ya hay otro embudo en el bloque (pasa los datos a contadores)."""
    if W:                            # el SVG se escala al ancho: se compensa para que la letra salga a su tamaño real
        label_size, sub_size = label_size * 800 / W, sub_size * 800 / W
        return f'<div style="width:{W}px">{funnel_svg(etapas, goal=objetivo, key=clave, label_size=label_size, sub_size=sub_size)}</div>'
    return funnel_svg(etapas, goal=objetivo, key=clave, label_size=label_size, sub_size=sub_size)


def _bh(x, y, w, h, c, r=3):
    """Barra horizontal con las esquinas de la derecha redondeadas."""
    r = max(0, min(r, h / 2, w))
    return (f'<path d="M{x:.1f},{y:.1f}H{x + w - r:.1f}Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f}V{y + h - r:.1f}'
            f'Q{x + w:.1f},{y + h:.1f} {x + w - r:.1f},{y + h:.1f}H{x:.1f}Z" fill="{c}"/>')


def columnas(datos, destacado=None, unidad="", eje="", W=520, H=260, fmt_valor=None, prevision_desde=None, cagr=()):
    """Columnas verticales con el valor encima de cada una, sin eje Y (la etiqueta directa lo sustituye).
    datos: [(rótulo, valor)]; destacado: índice o lista de índices en rojo, el resto en gris.
    prevision_desde: índice de la primera columna prevista (rayada; en rosa si está destacada).
    cagr: [(índice desde, índice hasta, texto)] para las flechas de crecimiento anual sobre las columnas.
    Cuándo usarlo: comparar de 3 a 8 magnitudes de una misma unidad, o una serie temporal corta con su previsión y CAGR.
    Cuándo no: más de 10 categorías o rótulos largos (usa barras_ranking)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    dest = _set(destacado)
    top, bot = (64 if cagr else 24), 34
    paso = W / len(datos)
    bw = min(58, paso * .62)
    y = lin(0, max(v for _, v in datos), H - bot, top)
    hid, hdef = hatch(INPUT, LGREY)
    s = [line(0, H - bot, W, H - bot, FG4, 1)]
    for i, (r, v) in enumerate(datos):
        cx, hot = paso * (i + .5), i in dest
        prev = prevision_desde is not None and i >= prevision_desde
        c = (mezcla(RED, "#FFFFFF", .45) if prev else RED) if hot else (f"url(#{hid})" if prev else NEUTRO)
        s.append(_bv(cx - bw / 2, y(v), bw, H - bot - y(v), c))
        s.append(text(cx, y(v) - 8, f(v), 14, 700, RED if hot else FG1, "middle"))
        s.append(text(cx, H - bot + 18, r, 13, 600 if hot else 400, FG1 if hot else FG2, "middle"))
    if prevision_desde is not None:
        xp = paso * prevision_desde
        s.append(line(xp, top - 10, xp, H - bot, FG4, 1, dash="3 3"))
        s.append(text(xp + 6, H - bot - 6, "Previsión", 11, 600, FG3))
    for i0, i1, t in cagr:
        x0, x1 = paso * (i0 + .5), paso * (i1 + .5)
        yl = min(y(datos[k][1]) for k in range(i0, i1 + 1)) - 30
        s.append(line(x0, yl, x1, yl, FG2, 1.2) + line(x0, yl, x0, yl + 6, FG2, 1.2) + head(x1, yl + 7, math.pi / 2, FG2, 7))
        w = 14 + 6.6 * len(t)
        s.append(rect((x0 + x1) / 2 - w / 2, yl - 10, w, 20, PAPER, rx=10, stroke=FG2, sw=1))
        s.append(text((x0 + x1) / 2, yl + 4, t, 12, 700, FG1, "middle"))
    if eje:
        s.append(text(0, H, eje, 11, 400, FG3))
    return _svg(W, H, "".join(s), hdef)


def barras_ranking(datos, destacado=None, unidad="", W=520, ancho_rotulo=150, alto=18, sep=11, ordenar=True, fmt_valor=None, H=None):
    """Ranking en barras horizontales, ordenado de mayor a menor, con el valor al final de cada barra.
    datos: [(rótulo, valor)]; destacado: rótulo o lista de rótulos en rojo (sobrevive a la ordenación).
    H: alto total; si se da, calcula el grueso y la separación de las barras (máximo 30 px de barra) y sobreescribe alto y sep.
    Cuándo usarlo: ordenar de 5 a 15 elementos con rótulos largos (mercados, empresas, ingredientes).
    Cuándo no: series temporales (usa columnas o linea) o si el orden no importa."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    dest = _set(destacado)
    filas = sorted(datos, key=lambda d: -d[1]) if ordenar else list(datos)
    if H:
        paso_ = (H + 4) / len(filas)
        alto, sep = min(paso_ * .62, 30), paso_ - min(paso_ * .62, 30)
    H = len(filas) * (alto + sep) - sep
    x = lin(0, max(v for _, v in filas), ancho_rotulo, W - 48)
    s = []
    for i, (r, v) in enumerate(filas):
        y0, hot = i * (alto + sep), r in dest
        s.append(text(ancho_rotulo - 10, y0 + alto / 2 + 4.5, r, 13, 600 if hot else 400, FG1 if hot else FG2, "end"))
        s.append(_bh(ancho_rotulo, y0, x(v) - ancho_rotulo, alto, RED if hot else NEUTRO))
        s.append(text(x(v) + 7, y0 + alto / 2 + 4.5, f(v), 13, 700, RED if hot else FG1))
    s.append(line(ancho_rotulo, -4, ancho_rotulo, H + 4, FG4, 1))
    return _svg(W, H, "".join(s))


def barras_agrupadas(categorias, series, colores=None, unidad="", W=520, H=260, fmt_valor=None):
    """Columnas agrupadas: dos o tres series por categoría, con leyenda arriba.
    series: [(nombre, [valores por categoría])]. Con dos series, la primera en gris y la segunda en rojo
    (antes y ahora, referencia y nosotros); con más, rampa de rojos.
    Cuándo usarlo: comparar dos momentos o dos actores en 3 a 6 categorías.
    Cuándo no: más de tres series (pasa a mapa_calor o a pequeños múltiplos)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    cols = colores or ([NEUTRO, RED] if len(series) == 2 else rampa(len(series)))
    top, bot = 20, 30
    paso = W / len(categorias)
    gw = paso * .72
    bw = gw / len(series)
    y = lin(0, max(max(v) for _, v in series), H - bot, top)
    s = [line(0, H - bot, W, H - bot, FG4, 1)]
    for i, cat in enumerate(categorias):
        x0 = paso * i + (paso - gw) / 2
        for k, (_, vals) in enumerate(series):
            v = vals[i]
            s.append(_bv(x0 + k * bw + 1.5, y(v), bw - 3, H - bot - y(v), cols[k]))
            s.append(text(x0 + k * bw + bw / 2, y(v) - 6, f(v), 12, 700, RED if cols[k] == RED else FG1, "middle"))
        s.append(text(paso * (i + .5), H - bot + 18, cat, 13, 400, FG2, "middle"))
    return _con_leyenda(_svg(W, H, "".join(s)), [(c, n) for c, (n, _) in zip(cols, series)])


def barras_apiladas(categorias, series, porcentaje=True, W=520, ancho_rotulo=120, alto=26, sep=12):
    """Barras horizontales apiladas al 100% (o absolutas), con el porcentaje dentro de cada tramo si cabe.
    series: [(nombre, [valores por categoría])] en la rampa de rojos.
    Cuándo usarlo: la composición de 3 a 6 elementos (mezcla de canales, reparto de un gasto).
    Cuándo no: si lo que importa es comparar un tramo intermedio entre filas (cuesta leerlo; usa barras_agrupadas)."""
    cols = rampa(len(series))
    tot = [sum(v[i] for _, v in series) for i in range(len(categorias))]
    mx = max(tot)
    H = len(categorias) * (alto + sep) - sep
    s = []
    for i, cat in enumerate(categorias):
        y0, x0 = i * (alto + sep), ancho_rotulo
        ancho = W - ancho_rotulo - (0 if porcentaje else 40)
        s.append(text(ancho_rotulo - 10, y0 + alto / 2 + 4.5, cat, 13, 400, FG2, "end"))
        for k, (_, vals) in enumerate(series):
            share = vals[i] / tot[i]
            w = ancho * (share if porcentaje else vals[i] / mx)
            s.append(rect(x0, y0, max(w - 2, 0), alto, cols[k]))
            if w > 34:
                lab = f"{round(share * 100)} %" if porcentaje else fmt(vals[i])
                s.append(text(x0 + w / 2 - 1, y0 + alto / 2 + 4.5, lab, 12, 600, sobre(cols[k]), "middle"))
            x0 += w
        if not porcentaje:
            s.append(text(x0 + 6, y0 + alto / 2 + 4.5, fmt(tot[i]), 13, 700, FG1))
    return _con_leyenda(_svg(W, H, "".join(s)), [(c, n) for c, (n, _) in zip(cols, series)])


def piruletas(datos, referencia=None, destacado=None, unidad="", W=520, ancho_rotulo=150, paso=30, fmt_valor=None):
    """Piruletas (lollipop): una línea fina y un punto por elemento, con una línea de referencia opcional.
    datos: [(rótulo, valor)]; referencia = (valor, texto), por ejemplo la media o el umbral legal.
    Cuándo usarlo: muchas barras de valores parecidos, donde la barra llena pesa demasiado.
    Cuándo no: si los valores tienen que sumarse visualmente (usa barras)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    dest = _set(destacado)
    H = len(datos) * paso + 18
    mx = max([v for _, v in datos] + ([referencia[0]] if referencia else []))
    x = lin(0, mx, ancho_rotulo, W - 50)
    s = []
    if referencia:
        s.append(line(x(referencia[0]), 14, x(referencia[0]), H, FG2, 1.2, dash="4 3"))
        s.append(text(x(referencia[0]), 9, referencia[1], 12, 600, FG2, "middle"))
    for i, (r, v) in enumerate(datos):
        yc, hot = 18 + i * paso + paso / 2, r in dest
        c = RED if hot else FG4
        s.append(text(ancho_rotulo - 10, yc + 4.5, r, 13, 600 if hot else 400, FG1 if hot else FG2, "end"))
        s.append(line(ancho_rotulo, yc, x(v), yc, c, 2))
        s.append(circle(x(v), yc, 6.5, c))
        s.append(text(x(v) + 12, yc + 4.5, f(v), 13, 700, RED if hot else FG1))
    return _svg(W, H, "".join(s))


def _persona(x, y, c, k=1):
    return (circle(x, y + 5 * k, 5 * k, c) +
            f'<path d="M{x - 8 * k:.1f},{y + 26 * k:.1f}V{y + 19 * k:.1f}Q{x - 8 * k:.1f},{y + 12 * k:.1f} {x:.1f},{y + 12 * k:.1f}'
            f'Q{x + 8 * k:.1f},{y + 12 * k:.1f} {x + 8 * k:.1f},{y + 19 * k:.1f}V{y + 26 * k:.1f}Z" fill="{c}"/>')


def pictograma(total, marcados, cifra, texto, por_fila=10, W=520):
    """Pictograma: figuras repetidas con las marcadas en rojo, y la cifra y su lectura al lado.
    total y marcados: enteros (10, 20 o 100 como máximo); cifra: «7 de 10».
    Cuándo usarlo: traducir un porcentaje a personas u objetos («7 de cada 10 consumidores»).
    Cuándo no: para valores con decimales o comparaciones entre varios grupos (usa columnas)."""
    filas = math.ceil(total / por_fila)
    k = 1.35 if por_fila <= 10 else .8
    dx, dy = 24 * k, 34 * k
    gw, gh = por_fila * dx, filas * dy
    s = "".join(_persona(10 * k + (i % por_fila) * dx, (i // por_fila) * dy, RED if i < marcados else NEUTRO, k) for i in range(total))
    return (f'<div style="display:flex;align-items:center;gap:26px;width:{W}px">{_svg(gw, gh, s)}'
            f'<div><div class="big" style="font-size:36px">{E(cifra)}</div>'
            f'<div style="font-size:14px;color:var(--fg2);line-height:1.4;margin-top:6px">{md(texto)}</div></div></div>')


def pareto(datos, corte=80, unidad="", W=520, H=290, fmt_valor=None):
    """Pareto: barras ordenadas de mayor a menor con la línea del acumulado y el corte (80 % por defecto).
    Las barras que suman hasta el corte van en rojo («los pocos vitales»).
    Cuándo usarlo: decir dónde concentrar el esfuerzo (causas de merma, partidas de coste, motivos de rechazo).
    Cuándo no: si las categorías no son sumables o el reparto es plano (no hay un 80/20 que contar)."""
    f = fmt_valor or (lambda v: fmt(v) + unidad)
    ds = sorted(datos, key=lambda d: -d[1])
    tot = sum(v for _, v in ds)
    izq, der, top, bot = 8, 40, 24, 36
    paso = (W - izq - der) / len(ds)
    bw = paso * .66
    y = lin(0, ds[0][1], H - bot, top)
    yp = lin(0, 100, H - bot, top)
    s = [line(izq, H - bot, W - der, H - bot, FG4, 1)]
    acum, pts, vital = 0, [], True
    for i, (r, v) in enumerate(ds):
        cx = izq + paso * (i + .5)
        c = RED if vital else NEUTRO
        s.append(_bv(cx - bw / 2, y(v), bw, H - bot - y(v), c))
        s.append(text(cx, y(v) - 6, f(v), 12, 700, RED if vital else FG2, "middle"))
        s.append(text(cx, H - bot + 16, r, 11, 600 if vital else 400, FG1 if vital else FG3, "middle"))
        acum += v
        pts.append((izq + paso * (i + 1), yp(acum / tot * 100)))
        if vital and acum / tot * 100 >= corte - 1e-9:
            vital = False
            xc = izq + paso * (i + 1)
            s.append(line(xc, top - 8, xc, H - bot, FG2, 1, dash="3 3"))
    s.append(line(izq, yp(corte), W - der, yp(corte), FG3, 1, dash="4 4"))
    s.append(text(W - der + 6, yp(corte) + 4, f"{corte} %", 12, 700, FG2))
    s.append(text(W - der + 6, yp(100) + 4, "100 %", 11, 400, FG3))
    d = f"M{izq},{H - bot} L" + " L".join(f"{x:.1f},{yy:.1f}" for x, yy in pts)
    s.append(f'<path d="{d}" fill="none" stroke="{FG1}" stroke-width="2" stroke-linejoin="round"/>')
    s.extend(circle(x, yy, 3.2, FG1) for x, yy in pts)
    return _con_leyenda(_svg(W, H, "".join(s)), [(RED, f"Suman el {corte} %"), (NEUTRO, "Resto"), (FG1, "Acumulado", "linea")])


def comparador_unidad(filas, referencia, unidad="€/kg", menor_mejor=True, destacado=None, W=520, ancho_rotulo=150, alto=20, sep=14):
    """Comparador por unidad: precio o coste por kilo (o por litro, por dosis) de cada opción frente a una
    referencia, con la diferencia en porcentaje en un chip verde (mejor) o rojo (peor).
    filas: [(rótulo, valor)]; referencia = (valor, texto); menor_mejor: si el valor bajo es el bueno (precio).
    Cuándo usarlo: propuestas de proveedor, sustitución de ingredientes, coste por dosis o por ración.
    Cuándo no: si las opciones no son equivalentes por unidad (rendimientos distintos sin normalizar)."""
    dest = _set(destacado)
    mx = max([v for _, v in filas] + [referencia[0]])
    x = lin(0, mx, ancho_rotulo, W - 150)
    H = 22 + len(filas) * (alto + sep) - sep
    L = Lienzo(W, H)
    L.add(line(x(referencia[0]), 14, x(referencia[0]), H, FG1, 1.5, dash="4 3"))
    L.add(text(x(referencia[0]), 9, referencia[1], 12, 700, FG1, "middle"))
    for i, (r, v) in enumerate(filas):
        y0, hot = 22 + i * (alto + sep), r in dest
        L.add(text(ancho_rotulo - 10, y0 + alto / 2 + 4.5, r, 13, 600 if hot else 400, FG1 if hot else FG2, "end"))
        L.add(_bh(ancho_rotulo, y0, x(v) - ancho_rotulo, alto, RED if hot else NEUTRO))
        L.add(text(x(v) + 7, y0 + alto / 2 + 4.5, f"{fmt(v)} {unidad}", 13, 700, RED if hot else FG1, halo=True))
        dif = (v - referencia[0]) / referencia[0] * 100
        bueno = (dif < 0) == menor_mejor
        tono = "neutro" if abs(dif) < .5 else ("bueno" if bueno else "malo")
        L.div(W, y0 + alto / 2, 80, delta(f"{'+' if dif > 0 else '−' if dif < 0 else ''}{fmt(round(abs(dif)))} %", dif > 0, tono),
              anchor="end", va="middle")
    return L.render()


def barras_variacion(datos, unidad="", colores=(FG3, RED), W=520, ancho_rotulo=150, alto=18, sep=10, fmt_valor=None):
    """Barras de variación: cambios positivos a la derecha y negativos a la izquierda de un eje, ordenados.
    datos: [(rótulo, variación)]; colores = (subidas, bajadas), por defecto gris oscuro y rojo.
    Cuándo usarlo: cambios de cuota, precio o volumen entre dos fechas para 5 a 20 elementos.
    Cuándo no: si importan los valores de partida y llegada (usa pendiente o mancuerna)."""
    f = fmt_valor or (lambda v: ("+" if v > 0 else "−" if v < 0 else "") + fmt(abs(v)) + unidad)
    ds = sorted(datos, key=lambda d: -d[1])
    mpos = max([v for _, v in ds] + [0])
    mneg = -min([v for _, v in ds] + [0])
    x = lin(-mneg, mpos, ancho_rotulo + (70 if mneg else 10), W - 60)
    H = len(ds) * (alto + sep) - sep
    cs, cb = colores
    s = []
    for i, (r, v) in enumerate(ds):
        y0 = i * (alto + sep)
        s.append(text(ancho_rotulo - 10, y0 + alto / 2 + 4.5, r, 13, 400, FG2, "end"))
        x0, x1 = sorted((x(0), x(v)))
        s.append(rect(x0, y0, max(x1 - x0, 1), alto, cs if v > 0 else cb, rx=2))
        s.append(text(x1 + 6 if v >= 0 else x0 - 6, y0 + alto / 2 + 4.5, f(v), 13, 700, FG1 if v > 0 else cb, "start" if v >= 0 else "end"))
    s.append(line(x(0), -4, x(0), H + 4, FG1, 1.2))
    return _svg(W, H, "".join(s))


def ranking_logos(filas, destacado=None, W=420, ancho_logo=170, fmt_valor=None, ordenar=True):
    """Ranking de actores por logo: logo, flecha y puntuación, de mayor a menor. El destacado (por defecto, el
    primero) en rojo y el resto en negro; una nota opcional sale como asterisco.
    filas: [(logo o nombre, valor, nota=None)]; destacado: nombre o índice tras ordenar.
    Cuándo usarlo: el resultado consolidado de un scoring cuando el lector reconoce a los actores por su logo.
    Cuándo no: si interesa la distancia entre valores (usa barras_ranking o tabla_con_barras)."""
    f = fmt_valor or fmt
    fs = sorted(filas, key=lambda r: -r[1]) if ordenar else list(filas)
    hot = lambda i, r: (destacado is None and i == 0) or destacado == i or (isinstance(destacado, str) and destacado == r[0])
    out = []
    for i, r in enumerate(fs):
        h = hot(i, r)
        nota = '<sup style="font-size:11px;color:var(--fg3)">*</sup>' if len(r) > 2 and r[2] else ""
        out.append(f'<div style="display:flex;align-items:center;gap:16px;height:38px;{"border-top:1px solid var(--border-2);" if i else ""}">'
                   f'<div style="width:{ancho_logo}px;flex:none;display:flex;align-items:center">{_logo_html(r[0], 24)}</div>'
                   f'{flecha_svg(RED if h else FG4, 22, 12, 2)}<b style="font-size:17px;color:{"var(--red)" if h else "var(--fg1)"};font-variant-numeric:tabular-nums">{f(r[1])}{nota}</b></div>')
    notas = [r[2] for r in fs if len(r) > 2 and r[2]]
    pie = f'<div style="font-size:11px;color:var(--fg3);margin-top:6px">* {md(notas[0])}</div>' if notas else ""
    return f'<div style="width:{W}px">{"".join(out)}{pie}</div>'
