"""Relación y distribución: cómo se reparten, se relacionan o se sitúan.

Familia 05 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math
import json

from .base import (
    AQUI, CATEGORIAS, E, FG1, FG2, FG3, FG4, FILL, FONT, GREY, LGREY, Lienzo, NEUTRO, PAPER, RED, TINT,
    YELLOW, _paso, _svg, arrow_eje, calor, circle, fmt, hatch, lin, line, rampa, rect, sobre, text, uid,
)
from .marcas import (_con_leyenda)

from .base import (INPUT, _logo_html, mezcla)  # añadidos el 01-11-2026

__all__ = ["mapa_burbujas", "mapa_flujos", "mapa_madurez", "dispersion", "mapa_calor", "histograma", "cajas", "red_nodos", "NOMBRES_PAIS", "REGIONES", "mapa_coropletico", "mapa_burbujas", "mapa_flujos", "CENTROS", "mapa_actores"]


def mapa_madurez(items, tramos, carriles, nombres, colores=None, escala=(0.5, 6.5), W=610, H=410, x1=600, carril=102, leyenda=True):
    """Mapa de madurez: eje continuo (TRL u otra escala ordinal) con franjas suaves por tramo y carriles por
    evidencia; una burbuja por tramo, carril y categoría, con el área proporcional al número de elementos.
    items: [(id, categoría, tramo, carril)] con categoría = índice en `nombres`; tramos: [(clave, (desde, hasta),
    rótulo, subrótulo)]; carriles: [(clave, rótulo)]; colores: uno por categoría (rampa de rojos por defecto).
    leyenda: categorías bajo el eje.
    Cuándo usarlo: una cartera de 20 a 80 tecnologías o candidatos por madurez y evidencia; con fichas a la derecha.
    Cuándo no: si hay que leer cada elemento por su nombre (usa una tabla) o con dos ejes cuantitativos (usa dispersion)."""
    colores = colores or CATEGORIAS
    L = Lienzo(W, H)
    x0, y0 = 110, 50
    s = lin(escala[0], escala[1], x0, x1)
    tr = {k: ab for k, ab, _, _ in tramos}
    yb = y0 + carril * len(carriles)
    for k, (key, (a, b), lab, sub) in enumerate(tramos):
        xa, xb = s(a - 0.5), s(b + 0.5)
        L.add(rect(xa, y0, xb - xa, yb - y0, LGREY if k % 2 == 0 else PAPER))
        L.add(text((xa + xb) / 2, 18, lab, 13, 600, FG1, "middle"), text((xa + xb) / 2, 34, sub, 12, 400, FG3, "middle"))
    for i, (key, lab) in enumerate(carriles):
        yc = y0 + i * carril + carril / 2
        L.add(line(x0, y0 + (i + 1) * carril, x1, y0 + (i + 1) * carril, GREY, 1, dash="2 4" if i < len(carriles) - 1 else None))
        L.div(x0 - 14, yc, 100, f'<b>{E(lab)}</b>', anchor="end", va="middle", style="font-size:14px")
    for v in range(math.ceil(escala[0]), math.floor(escala[1]) + 1):
        L.add(line(s(v), yb, s(v), yb + 5, FG3), text(s(v), yb + 18, v, 12, 400, FG3, "middle"))
    ri = {k: i for i, (k, _) in enumerate(carriles)}
    celdas = {}
    for _id, cat, t, c in items:
        celdas.setdefault((t, c), {}).setdefault(cat, 0)
        celdas[(t, c)][cat] += 1
    for (t, c), cnt in celdas.items():
        its = sorted(cnt.items())
        rs = [7 + 15 * math.sqrt(v / 10) for _, v in its]
        totalw = sum(2 * q for q in rs) + 6 * (len(rs) - 1)
        a, b = tr[t]
        px = s((a + b) / 2) - totalw / 2
        py = y0 + ri[c] * carril + carril / 2
        for (m, v), q in zip(its, rs):
            L.add(circle(px + q, py, q, colores[m], PAPER, 1.5))
            big = q > 10
            L.add(text(px + q, py + 4.5 if big else py + q + 13, v, 12 if big else 11, 700, sobre(colores[m]) if big else FG1, "middle"))
            px += 2 * q + 6
    if leyenda:
        ley = ('<div style="display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center;font-size:12px;color:var(--fg2)">'
               + "".join(f'<span style="display:inline-flex;align-items:center;gap:6px"><i style="width:11px;height:11px;border-radius:99px;background:{c};display:inline-block"></i>{E(m)}</span>'
                         for m, c in zip(nombres, colores)) + '</div>')
        L.div(x0, yb + 32, W - x0, ley)
    return L.render()


def dispersion(puntos, ejes, dominio_x, dominio_y, umbrales=None, cuadrantes=None, W=520, H=340, valores=False, fmt_x=None, fmt_y=None):
    """Dispersión o burbujas: dos variables por elemento, con umbrales y nombres de cuadrante opcionales.
    puntos: [dict(rotulo, x, y, tam=None, destacado=False)]; ejes = (nombre_x, nombre_y);
    umbrales = (x, y); cuadrantes = [sup_izq, sup_der, inf_izq, inf_der]; valores: escribe los valores de los ejes
    (fmt_x y fmt_y dan su formato), para cuando la posición exacta importa.
    Cuándo usarlo: posicionar 5 a 20 elementos en dos variables numéricas (coste frente a madurez).
    Cuándo no: si las variables son cualitativas (usa matriz_2x2)."""
    izq, bot, top, der = (56, 44, 10, 14) if valores else (30, 34, 10, 14)
    x = lin(*dominio_x, izq, W - der)
    y = lin(*dominio_y, H - bot, top)
    s = [rect(izq, top, W - der - izq, H - bot - top, LGREY)]
    if umbrales:
        s.append(line(x(umbrales[0]), top, x(umbrales[0]), H - bot, FG4, 1, dash="4 4"))
        s.append(line(izq, y(umbrales[1]), W - der, y(umbrales[1]), FG4, 1, dash="4 4"))
    if cuadrantes:
        pos = [(izq + 10, top + 18, "start"), (W - der - 10, top + 18, "end"),
               (izq + 10, H - bot - 10, "start"), (W - der - 10, H - bot - 10, "end")]
        for (px, py, anc), t in zip(pos, cuadrantes):
            s.append(text(px, py, t.upper(), 11, 700, RED if t == cuadrantes[1] else FG3, anc, ls=1))
    s.append(arrow_eje(izq, H - bot, W - der + 6, H - bot) + arrow_eje(izq, H - bot, izq, top - 6))
    if valores:
        def marcas(a, b, n=4):
            bruto = (b - a) / n
            base = 10 ** math.floor(math.log10(bruto))
            paso_ = next(k * base for k in (1, 2, 2.5, 5, 10) if k * base >= bruto)
            v = math.ceil(a / paso_) * paso_
            out = []
            while v <= b + 1e-9:
                out.append(round(v, 6))
                v += paso_
            return out
        for v in marcas(*dominio_x):
            s.append(line(x(v), H - bot, x(v), H - bot + 4, FG3))
            s.append(text(x(v), H - bot + 16, (fmt_x or fmt)(v), 11, 400, FG3, "middle"))
        for v in marcas(*dominio_y):
            s.append(line(izq - 4, y(v), izq, y(v), FG3))
            s.append(text(izq - 7, y(v) + 4, (fmt_y or fmt)(v), 11, 400, FG3, "end"))
    s.append(text(W - der, H - 8 if not valores else H - 4, ejes[0], 12, 600, FG2, "end"))
    s.append(f'<text transform="translate(12,{top}) rotate(-90)" text-anchor="end" style="font-family:{FONT};font-size:12px;'
             f'font-weight:600;fill:{FG2}">{E(ejes[1])}</text>')
    tams = [p.get("tam") or 1 for p in puntos]
    rmax = max(tams)
    for p, t in sorted(zip(puntos, tams), key=lambda z: -z[1]):
        r = 6 + 16 * math.sqrt(t / rmax) if any(q.get("tam") for q in puntos) else 7
        hot = p.get("destacado")
        s.append(circle(x(p["x"]), y(p["y"]), r, RED if hot else FG4, "#fff", 1.5))
        s.append(text(x(p["x"]) + r + 5, y(p["y"]) + 4, p["rotulo"], 12, 700 if hot else 400, RED if hot else FG1, halo=True))
    return _svg(W, H, "".join(s))


def mapa_calor(filas, columnas, valores, escala=None, fmt_valor=None, ancho_rotulo=140, celda=(62, 34), destacado=None):
    """Mapa de calor: matriz de valores con color continuo de gris cálido a rojo oscuro y la cifra en cada celda.
    filas y columnas: nombres; valores: lista de listas (None = sin dato, rayado); destacado: (fila, columna).
    Cuándo usarlo: patrones en una tabla de 4 × 4 a 10 × 12 (actividad por país y año, notas por criterio).
    Cuándo no: si cada celda necesita texto (usa tabla_comparativa)."""
    f = fmt_valor or fmt
    planos = [v for fila in valores for v in fila if v is not None]
    d0, d1 = escala or (min(planos), max(planos))
    cw, ch = celda
    W, H = ancho_rotulo + cw * len(columnas), 26 + ch * len(filas)
    hid, hdef = hatch()
    s = []
    for j, c in enumerate(columnas):
        s.append(text(ancho_rotulo + cw * j + cw / 2, 14, c, 12, 700, FG3, "middle"))
    for i, fr in enumerate(filas):
        y0 = 26 + i * ch
        s.append(text(ancho_rotulo - 10, y0 + ch / 2 + 4.5, fr, 13, 400, FG2, "end"))
        for j, v in enumerate(valores[i]):
            x0 = ancho_rotulo + cw * j
            if v is None:
                s.append(rect(x0 + 1.5, y0 + 1.5, cw - 3, ch - 3, f"url(#{hid})", rx=4))
                continue
            c = calor((v - d0) / (d1 - d0))
            s.append(rect(x0 + 1.5, y0 + 1.5, cw - 3, ch - 3, c, rx=4,
                          stroke=FG1 if destacado == (i, j) else "none", sw=2))
            s.append(text(x0 + cw / 2, y0 + ch / 2 + 4.5, f(v), 13, 600, sobre(c), "middle"))
    return _svg(W, H, "".join(s), hdef)


def histograma(tramos, valores, marca=None, W=520, H=240, unidad=""):
    """Histograma: cuántos elementos caen en cada tramo, con una marca (la media, nuestro caso) encima.
    tramos: rótulos de los tramos; valores: recuentos; marca = (índice del tramo, texto).
    Cuándo usarlo: enseñar la distribución de una población (precios, edades, puntuaciones de 200 candidatos).
    Cuándo no: con menos de 30 observaciones (mejor dar los valores)."""
    top, bot = 30, 32
    paso = W / len(tramos)
    y = lin(0, max(valores), H - bot, top)
    s = [line(0, H - bot, W, H - bot, FG4, 1)]
    for i, (t, v) in enumerate(zip(tramos, valores)):
        hot = marca and marca[0] == i
        s.append(rect(i * paso + 1, y(v), paso - 2, H - bot - y(v), RED if hot else NEUTRO))
        s.append(text(i * paso + paso / 2, y(v) - 6, f"{v}{unidad}", 12, 700 if hot else 400, RED if hot else FG2, "middle"))
        s.append(text(i * paso + paso / 2, H - bot + 16, t, 11, 400, FG3, "middle"))
    if marca:
        cx = marca[0] * paso + paso / 2
        s.append(text(cx, 10, marca[1], 12, 700, RED, "middle"))
        s.append(line(cx, 14, cx, y(valores[marca[0]]) - 18, RED, 1.2))
    return _svg(W, H, "".join(s))


def _cuantil(xs, q):
    s = sorted(xs)
    p = (len(s) - 1) * q
    i = int(p)
    return s[i] + (s[min(i + 1, len(s) - 1)] - s[i]) * (p - i)


def cajas(grupos, destacado=None, dominio=None, eje="", W=520, H=280):
    """Diagrama de cajas: mediana, cuartiles y extremos por grupo, con cada observación como un punto.
    grupos: [(rótulo, [valores])]; los bigotes van del mínimo al máximo.
    Cuándo usarlo: resultados de paneles sensoriales, ensayos repetidos o precios por canal.
    Cuándo no: con menos de 8 observaciones por grupo (enseña los puntos sin caja)."""
    vals = [v for _, vs in grupos for v in vs]
    d0, d1 = dominio or (min(vals), max(vals))
    izq, top, bot = 36, 12, 30
    y = lin(d0, d1, H - bot, top)
    paso = (W - izq) / len(grupos)
    bw = min(56, paso * .45)
    s = []
    p = _paso(d1 - d0, 4)
    v = math.ceil(d0 / p) * p
    while v <= d1 + 1e-9:
        s.append(line(izq, y(v), W, y(v), GREY, 1))
        s.append(text(izq - 8, y(v) + 4, fmt(v), 11, 400, FG3, "end"))
        v += p
    for i, (r, vs) in enumerate(grupos):
        cx = izq + paso * (i + .5)
        hot = r == destacado
        q1, q2, q3 = (_cuantil(vs, q) for q in (.25, .5, .75))
        c = RED if hot else FG2
        s.append(line(cx, y(min(vs)), cx, y(q3), c, 1.5) + line(cx, y(q1), cx, y(max(vs)), c, 1.5))
        s.append(line(cx - bw / 4, y(min(vs)), cx + bw / 4, y(min(vs)), c, 1.5) + line(cx - bw / 4, y(max(vs)), cx + bw / 4, y(max(vs)), c, 1.5))
        s.append(rect(cx - bw / 2, y(q3), bw, y(q1) - y(q3), TINT if hot else FILL, rx=3, stroke=c, sw=1.5))
        s.append(line(cx - bw / 2, y(q2), cx + bw / 2, y(q2), c, 3))
        for j, val in enumerate(vs):
            jit = ((j * 37) % 11 - 5) / 5 * bw * .7
            s.append(f'<circle cx="{cx + bw / 2 + 10 + abs(jit) * .4:.1f}" cy="{y(val):.1f}" r="2.3" fill="{c}" fill-opacity=".45"/>')
        s.append(text(cx, H - bot + 18, r, 13, 700 if hot else 400, RED if hot else FG2, "middle"))
        s.append(text(cx - bw / 2 - 6, y(q2) + 4, fmt(round(q2, 1)), 11, 700, c, "end"))
    if eje:
        s.append(f'<text transform="translate(8,{top}) rotate(-90)" text-anchor="end" style="font-family:{FONT};font-size:11px;fill:{FG3}">{E(eje)}</text>')
    return _svg(W, H, "".join(s))


def red_nodos(nodos, enlaces, grupos=None, W=520, H=340, iteraciones=400):
    """Red de nodos: actores y sus relaciones, colocados por fuerzas (los conectados se acercan). Determinista.
    nodos: [dict(id, rotulo, grupo=0, tam=1, destacado=False)]; enlaces: [(id_a, id_b)];
    grupos: nombres de los grupos para la leyenda (rampa de rojos); el destacado lleva aro negro.
    Cuándo usarlo: ecosistemas (quién colabora con quién, coautorías de patentes, inversores comunes).
    Cuándo no: más de 30 nodos o redes muy densas (se vuelve una madeja; usa una matriz)."""
    n = len(nodos)
    idx = {nd["id"]: i for i, nd in enumerate(nodos)}
    m = 46
    pos = [[W / 2 + (W / 3) * math.cos(2 * math.pi * i / n), H / 2 + (H / 3) * math.sin(2 * math.pi * i / n)] for i in range(n)]
    k = math.sqrt((W - 2 * m) * (H - 2 * m) / n) * .95
    t = W / 8
    ej = [(idx[a], idx[b]) for a, b in enlaces]
    for _ in range(iteraciones):
        disp = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                dx, dy = pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]
                d = max(math.hypot(dx, dy), .01)
                f = k * k / d
                disp[i][0] += dx / d * f; disp[i][1] += dy / d * f
                disp[j][0] -= dx / d * f; disp[j][1] -= dy / d * f
        for i, j in ej:
            dx, dy = pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]
            d = max(math.hypot(dx, dy), .01)
            f = d * d / k
            disp[i][0] -= dx / d * f; disp[i][1] -= dy / d * f
            disp[j][0] += dx / d * f; disp[j][1] += dy / d * f
        for i in range(n):
            disp[i][0] -= (pos[i][0] - W / 2) * .06 * k / 10
            disp[i][1] -= (pos[i][1] - H / 2) * .06 * k / 10
            dx, dy = disp[i]
            d = max(math.hypot(dx, dy), .01)
            pos[i][0] = min(W - m - 30, max(m + 10, pos[i][0] + dx / d * min(d, t)))
            pos[i][1] = min(H - m, max(m - 10, pos[i][1] + dy / d * min(d, t)))
        t *= .985
    ng = max(nd.get("grupo", 0) for nd in nodos) + 1
    cols = rampa(ng)
    s = []
    for i, j in ej:
        hot = nodos[i].get("destacado") or nodos[j].get("destacado")
        s.append(line(*pos[i], *pos[j], FG3 if hot else GREY, 1.6 if hot else 1.2))
    for nd, (px, py) in zip(nodos, pos):
        r = 7 + 6 * math.sqrt(nd.get("tam", 1))
        hot = nd.get("destacado")
        s.append(circle(px, py, r, cols[nd.get("grupo", 0)], FG1 if hot else "#fff", 3 if hot else 1.5))
        s.append(text(px, py + r + 13, nd["rotulo"], 12, 700 if hot else 400, FG1, "middle", halo=True))
    g = _svg(W, H, "".join(s))
    return _con_leyenda(g, list(zip(cols, grupos))) if grupos else g


NOMBRES_PAIS = {"España": "Spain", "Portugal": "Portugal", "Francia": "France", "Alemania": "Germany", "Italia": "Italy",
                "Países Bajos": "Netherlands", "Bélgica": "Belgium", "Reino Unido": "United Kingdom", "Irlanda": "Ireland",
                "Suiza": "Switzerland", "Austria": "Austria", "Polonia": "Poland", "Suecia": "Sweden", "Noruega": "Norway",
                "Dinamarca": "Denmark", "Finlandia": "Finland", "Grecia": "Greece", "Chequia": "Czechia", "Hungría": "Hungary",
                "Rumanía": "Romania", "Bulgaria": "Bulgaria", "Croacia": "Croatia", "Eslovaquia": "Slovakia", "Eslovenia": "Slovenia",
                "Israel": "Israel", "Marruecos": "Morocco", "Turquía": "Turkey", "Estados Unidos": "United States of America",
                "Canadá": "Canada", "México": "Mexico", "Colombia": "Colombia", "Chile": "Chile", "Perú": "Peru", "Argentina": "Argentina",
                "Brasil": "Brazil", "Ecuador": "Ecuador", "Uruguay": "Uruguay", "Bolivia": "Bolivia", "Paraguay": "Paraguay",
                "Venezuela": "Venezuela", "Guatemala": "Guatemala", "Costa Rica": "Costa Rica", "Panamá": "Panama",
                "China": "China", "Japón": "Japan", "India": "India"}


_GEO = {}


def _geo():
    """Países de world-atlas 110m (assets/geo/countries-110m.json, la misma fuente que maps-brand.js)
    decodificados de TopoJSON a anillos de coordenadas (lon, lat)."""
    if not _GEO:
        t = json.loads((AQUI / "assets/geo/countries-110m.json").read_text())
        (sx, sy), (tx, ty) = t["transform"]["scale"], t["transform"]["translate"]
        arcs = []
        for a in t["arcs"]:
            x = y = 0
            pts = []
            for dx, dy in a:
                x += dx
                y += dy
                pts.append((x * sx + tx, y * sy + ty))
            arcs.append(pts)

        def anillo(ids):
            out = []
            for i in ids:
                seg = arcs[i] if i >= 0 else arcs[~i][::-1]
                out.extend(seg if not out else seg[1:])
            for k in range(1, len(out)):          # desenrolla el antimeridiano (Rusia cruza de 180 a −180)
                x, y = out[k]
                while x - out[k - 1][0] > 180:
                    x -= 360
                while x - out[k - 1][0] < -180:
                    x += 360
                out[k] = (x, y)
            return out
        for g in t["objects"]["countries"]["geometries"]:
            polys = [g["arcs"]] if g["type"] == "Polygon" else (g["arcs"] if g["type"] == "MultiPolygon" else [])
            _GEO[g["properties"]["name"]] = [[anillo(r) for r in p] for p in polys]
    return _GEO


REGIONES = {"europa": ((-17, 37, 34.5, 68), (10, 52)), "iberia": ((-10, 4.5, 35.5, 44.2), (-3.5, 40)),
            "latam": ((-118, -34, -56, 33), (-75, -12)), "mundo": ((-170, 180, -58, 84), None),
            "hispano": ((-125, 8, -57, 46), None)}      # Latinoamérica y la península ibérica, en una sola vista


def _proyeccion(centro):
    """Acimutal equivalente de Lambert centrada en `centro` (la de los mapas oficiales de la UE); sin centro,
    equirectangular (mapa mundi)."""
    if centro is None:
        return lambda lon, lat: (lon, -lat)
    l0, p0 = math.radians(centro[0]), math.radians(centro[1])

    def pr(lon, lat):
        p, dl = math.radians(lat), math.radians(lon) - l0
        k = math.sqrt(2 / (1 + math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(dl)))
        return k * math.cos(p) * math.sin(dl), -k * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(dl))
    return pr


def mapa_coropletico(valores, region="europa", escala=None, destacado=None, etiquetas=None, fmt_valor=None, leyenda_txt="", W=520, H=None):
    """Mapa coroplético: países coloreados por valor (gris cálido a rojo oscuro), sin JavaScript.
    Proyección acimutal equivalente de Lambert (proporciones reales en Europa); el alto sale de la región.
    valores: {país: valor} con el nombre en español (NOMBRES_PAIS) o en inglés del atlas; region: 'europa',
    'iberia', 'latam', 'hispano' (Latinoamérica e Iberia) o 'mundo'; destacado: país con borde negro; etiquetas: países que llevan la cifra encima
    (por defecto, todos los que tienen valor); leyenda_txt: qué mide la escala.
    Cuándo usarlo: actividad, mercado o presencia por país (dónde están los proveedores, las patentes, la demanda).
    Cuándo no: si el valor depende del tamaño del país (usa valores por habitante) o con menos de 4 países (usa barras)."""
    f = fmt_valor or fmt
    geo = _geo()
    nom = lambda p: NOMBRES_PAIS.get(p, p)
    val = {nom(k): v for k, v in valores.items()}
    d0, d1 = escala or (min(val.values()), max(val.values()))
    (lon0, lon1, lat0, lat1), centro = REGIONES[region]
    pr0 = _proyeccion(centro)
    if centro:
        # encuadre por los ejes centrales de la caja lon/lat (paralelo medio y meridiano central)
        latm = (lat0 + lat1) / 2
        bx0, bx1 = pr0(lon0, latm)[0], pr0(lon1, latm)[0]
        by0, by1 = pr0(centro[0], lat1)[1], pr0(centro[0], lat0)[1]
    else:
        bx0, bx1, by0, by1 = lon0, lon1, -lat1, -lat0
    s_ = W / (bx1 - bx0)
    hm = (by1 - by0) * s_
    H = H or hm + 34
    hm = H - 34
    pr = lambda lon, lat: ((pr0(lon, lat)[0] - bx0) * s_, (pr0(lon, lat)[1] - by0) * s_)
    clip = uid("clip")
    paths, etq = [], []
    eti = {nom(e) for e in etiquetas} if etiquetas is not None else set(val)
    for pais, polys in geo.items():
        dentro = [p for p in polys if any(lon0 - 8 <= x <= lon1 + 8 and lat0 - 8 <= y <= lat1 + 8 for x, y in p[0])]
        if not dentro:
            continue
        d = "".join("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in (pr(x, y) for x, y in ring)) + "Z" for p in dentro for ring in p)
        c = calor((val[pais] - d0) / (d1 - d0)) if pais in val else FILL
        hot = destacado and nom(destacado) == pais
        paths.append(f'<path d="{d}" fill="{c}" stroke="{FG1 if hot else "#fff"}" stroke-width="{2 if hot else .8}" fill-rule="evenodd" stroke-linejoin="round"/>')
        if pais in val and pais in eti:
            ring = max((p[0] for p in dentro), key=len)
            cx, cy = CENTROS.get(pais) or (sum(x for x, _ in ring) / len(ring), sum(y for _, y in ring) / len(ring))
            px, py = pr(cx, cy)
            etq.append(text(px, py + 4, f(val[pais]), 11, 700, sobre(c), "middle"))
    gid = uid("g")
    grad = f'<linearGradient id="{gid}">' + "".join(f'<stop offset="{t / 4}" stop-color="{calor(t / 4)}"/>' for t in range(5)) + '</linearGradient>'
    defs = f'<clipPath id="{clip}"><rect x="0" y="0" width="{W}" height="{hm}"/></clipPath>{grad}'
    ley = (rect(0, hm + 12, 140, 8, f"url(#{gid})", rx=4) + text(0, hm + 32, f(d0), 11, 400, FG3) + text(140, hm + 32, f(d1), 11, 400, FG3, "end")
           + text(152, hm + 20, leyenda_txt, 12, 400, FG2))
    return _svg(W, round(H), f'<g clip-path="url(#{clip})">{"".join(paths)}{"".join(etq)}</g>{ley}', defs)


def _base_mapa(region, W, H, reserva=0, color=None):
    """Tierra de una región, lista para dibujar encima. Devuelve (trazos, proyección, alto del mapa, recorte, defs)."""
    geo = _geo()
    (lon0, lon1, lat0, lat1), centro = REGIONES[region]
    pr0 = _proyeccion(centro)
    if centro:
        latm = (lat0 + lat1) / 2
        bx0, bx1 = pr0(lon0, latm)[0], pr0(lon1, latm)[0]
        by0, by1 = pr0(centro[0], lat1)[1], pr0(centro[0], lat0)[1]
    else:
        bx0, bx1, by0, by1 = lon0, lon1, -lat1, -lat0
    s_ = W / (bx1 - bx0)
    hm = (H - reserva) if H else (by1 - by0) * s_
    pr = lambda lon, lat: ((pr0(lon, lat)[0] - bx0) * s_, (pr0(lon, lat)[1] - by0) * s_)
    trazos = []
    for pais, polys in geo.items():
        dentro = [p for p in polys if any(lon0 - 8 <= x <= lon1 + 8 and lat0 - 8 <= y <= lat1 + 8 for x, y in p[0])]
        if dentro:
            d = "".join("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in (pr(x, y) for x, y in ring)) + "Z" for p in dentro for ring in p)
            trazos.append(f'<path d="{d}" fill="{(color or (lambda _: FILL))(pais)}" stroke="#fff" stroke-width=".8" fill-rule="evenodd" stroke-linejoin="round"/>')
    clip = uid("clip")
    return "".join(trazos), pr, hm, clip, f'<clipPath id="{clip}"><rect x="0" y="0" width="{W}" height="{hm}"/></clipPath>'


def _punto_geo(lugar):
    """(lon, lat) de un país en español o en inglés del atlas, o el propio par si ya lo es."""
    if isinstance(lugar, (tuple, list)):
        return lugar
    pais = NOMBRES_PAIS.get(lugar, lugar)
    if pais in CENTROS:
        return CENTROS[pais]
    polys = _geo().get(pais)
    if not polys:
        raise ValueError(f"País desconocido: «{lugar}». Usa su nombre en inglés o un par (lon, lat).")
    ring = max((p[0] for p in polys), key=len)
    return (sum(x for x, _ in ring) / len(ring), sum(y for _, y in ring) / len(ring))


def mapa_burbujas(valores, region="mundo", destacado=None, rotular=3, fmt_valor=None, leyenda_txt="", W=1100, H=None):
    """Mapa de burbujas: el área de cada círculo es proporcional al valor del lugar; tierra en gris cálido.
    valores: {país o (lon, lat, rótulo): valor}; destacado: la burbuja en rojo (por defecto, la mayor); rotular: cuántas llevan
    rótulo y cifra, de mayor a menor; region: 'europa', 'iberia', 'latam', 'hispano' o 'mundo'.
    Cuándo usarlo: magnitudes por lugar cuando el tamaño del país engañaría (candidaturas, oficinas, inversión).
    Cuándo no: un valor relativo a cada país (usa mapa_coropletico) o si importa la conexión entre lugares (usa mapa_flujos)."""
    f = fmt_valor or fmt
    filas = sorted(valores.items(), key=lambda kv: -kv[1])
    foco = destacado if destacado is not None else filas[0][0]
    tierra, pr, hm, clip, defs = _base_mapa(region, W, H, 24 if leyenda_txt else 0)
    vmax = filas[0][1]
    circulos, rotulos = [], []
    for i, (lugar, v) in enumerate(filas):
        lon, lat = lugar[:2] if isinstance(lugar, tuple) else _punto_geo(lugar)
        nombre = lugar[2] if isinstance(lugar, tuple) else lugar
        x, y = pr(lon, lat)
        r = 5 + 27 * math.sqrt(v / vmax)
        hot = lugar == foco
        circulos.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{RED if hot else FG4}" fill-opacity="{.85 if hot else .55}" stroke="#fff" stroke-width="1"/>')
        if i < rotular or hot:
            rotulos.append(text(x + r + 5, y + 4, f"{nombre} · {f(v)}", 12, 700 if hot else 600, RED if hot else FG1, halo=True))
    pie = text(0, hm + 18, leyenda_txt, 12, 400, FG2) if leyenda_txt else ""
    return _svg(W, round(hm + (24 if leyenda_txt else 0)), f'<g clip-path="url(#{clip})">{tierra}{"".join(circulos)}{"".join(rotulos)}</g>{pie}', defs)


def mapa_flujos(origen, destinos, region="mundo", rotulo_origen=None, W=1100, H=None):
    """Mapa de flujos: arcos desde un solo origen, con el grosor según el peso. El origen lleva el punto de luz.
    origen: país o (lon, lat); destinos: [(rótulo, país o (lon, lat), peso)]; region: como en mapa_coropletico.
    Cuándo usarlo: de dónde sale algo y adónde llega (expansión, exportación, suministro), con un solo origen.
    Cuándo no: varios orígenes cruzados (usa sankey o red_nodos) o sin una dirección clara (usa mapa_burbujas)."""
    tierra, pr, hm, clip, defs = _base_mapa(region, W, H)
    x0, y0 = pr(*_punto_geo(origen))
    pmax = max(d[2] for d in destinos)
    arcos, puntos = [], []
    for nombre, lugar, peso in destinos:
        x, y = pr(*_punto_geo(lugar))
        cx, cy = (x0 + x) / 2, (y0 + y) / 2 - math.hypot(x - x0, y - y0) * .22
        arcos.append(f'<path d="M{x0:.1f},{y0:.1f} Q{cx:.1f},{cy:.1f} {x:.1f},{y:.1f}" fill="none" stroke="{RED}" stroke-opacity=".55" stroke-width="{1.5 + 4.5 * peso / pmax:.1f}" stroke-linecap="round"/>')
        puntos.append(circle(x, y, 4, FG1, "#fff", 1.2) + text(x + 8, y + 4, nombre, 12, 600, FG1, halo=True))
    luz = circle(x0, y0, 14, YELLOW) .replace("/>", ' fill-opacity=".25"/>') + circle(x0, y0, 5.5, YELLOW, "#fff", 1.2)
    rot = text(x0 + 12, y0 - 10, rotulo_origen, 13, 700, FG1, halo=True) if rotulo_origen else ""
    return _svg(W, round(hm), f'<g clip-path="url(#{clip})">{tierra}{"".join(arcos)}{"".join(puntos)}{luz}{rot}</g>', defs)


CENTROS = {"France": (2.5, 46.6), "Norway": (9, 61), "United Kingdom": (-1.6, 52.6), "Sweden": (15, 60.5), "Finland": (26, 62.5),
           "Italy": (12.5, 43), "Croatia": (16, 45.4), "Greece": (22, 39.5), "Denmark": (9.2, 56), "Portugal": (-8, 39.7)}


def mapa_actores(grupos, region="mundo", W=1100, ancho_caja=230, H=None):
    """Mapa con grupos de actores: los países de cada grupo coloreados y, a los lados, una caja discontinua por grupo
    con sus logos, unida por una línea al punto del mapa donde están.
    grupos: [dict(rotulo, paises=[...], punto=(lon, lat), actores=[logo o nombre], lado='izq' | 'der', destacado=False)];
    los países van en español (NOMBRES_PAIS) o en inglés del atlas. El grupo destacado va en rojo y el resto en rampa clara.
    Cuándo usarlo: dónde están los fabricantes frente a dónde está la demanda, o un ecosistema por región.
    Cuándo no: si lo que importa es un valor por país (usa mapa_coropletico)."""
    geo = _geo()
    nom = lambda p: NOMBRES_PAIS.get(p, p)
    (lon0, lon1, lat0, lat1), centro = REGIONES[region]
    pr0 = _proyeccion(centro)
    if centro:
        latm = (lat0 + lat1) / 2
        bx0, bx1 = pr0(lon0, latm)[0], pr0(lon1, latm)[0]
        by0, by1 = pr0(centro[0], lat1)[1], pr0(centro[0], lat0)[1]
    else:
        bx0, bx1, by0, by1 = lon0, lon1, -lat1, -lat0
    wm = W - 2 * (ancho_caja + 40)
    s_ = wm / (bx1 - bx0)
    hm = (by1 - by0) * s_
    alto_caja = lambda g: 44 + ((len(g["actores"]) + 1) // 2) * 34
    lados = {l: [g for g in grupos if g.get("lado", "der") == l] for l in ("izq", "der")}
    H = H or max(hm, *(sum(alto_caja(g) + 16 for g in gs) for gs in lados.values() if gs))
    ox, oy = ancho_caja + 40, (H - hm) / 2
    pr = lambda lon, lat: (ox + (pr0(lon, lat)[0] - bx0) * s_, oy + (pr0(lon, lat)[1] - by0) * s_)
    claros = [mezcla(RED, "#FFFFFF", t) for t in (.45, .62, .3, .75)]
    color, k = {}, 0
    for g in grupos:
        if g.get("destacado"):
            color[id(g)] = RED
        else:
            color[id(g)] = claros[k % len(claros)]
            k += 1
    pais_color = {nom(p): color[id(g)] for g in grupos for p in g["paises"]}
    L = Lienzo(W, round(H))
    clip = uid("clip")
    L.defs.append(f'<clipPath id="{clip}"><rect x="{ox:.1f}" y="{oy:.1f}" width="{wm:.1f}" height="{hm:.1f}"/></clipPath>')
    paths = []
    for pais, polys in geo.items():
        dentro = [p for p in polys if any(lon0 - 8 <= x <= lon1 + 8 and lat0 - 8 <= y <= lat1 + 8 for x, y in p[0])]
        if not dentro:
            continue
        d = "".join("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in (pr(x, y) for x, y in ring)) + "Z" for p in dentro for ring in p)
        paths.append(f'<path d="{d}" fill="{pais_color.get(pais, FILL)}" stroke="#fff" stroke-width=".7" fill-rule="evenodd" stroke-linejoin="round"/>')
    L.add(f'<g clip-path="url(#{clip})">{"".join(paths)}</g>')
    for lado, gs in lados.items():
        tot = sum(alto_caja(g) for g in gs) + 16 * (len(gs) - 1)
        y = (H - tot) / 2
        for g in gs:
            h = alto_caja(g)
            x = 0 if lado == "izq" else W - ancho_caja
            px, py = pr(*g["punto"])
            ex = x + ancho_caja if lado == "izq" else x
            L.add(line(ex, y + h / 2, px, py, color[id(g)] if g.get("destacado") else FG3, 1.2, dash="4 3"), circle(px, py, 4, FG1, "#fff", 1.5))
            logos = "".join(f'<div style="display:flex;align-items:center;justify-content:center;height:30px">{_logo_html(a, 22)}</div>' for a in g["actores"])
            L.div(x, y, ancho_caja, f'<div style="height:{h}px;box-sizing:border-box;border:1.5px dashed {RED if g.get("destacado") else INPUT};border-radius:14px;'
                                    f'background:#fff;padding:10px 12px"><div style="font-size:12px;font-weight:700;color:{"var(--red)" if g.get("destacado") else "var(--fg1)"};'
                                    f'text-align:center;margin-bottom:6px">{E(g["rotulo"])}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 8px">{logos}</div></div>')
            y += h + 16
    return L.render()
