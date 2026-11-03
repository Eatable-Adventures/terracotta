"""Cadena de valor: cómo fluye el valor entre eslabones y actores, con escenas isométricas.

Familia 08 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (
    BORDER2, DCREAM, E, FG1, FG2, FG3, FG4, FILL, GREY, INPUT, LGREY, Lienzo, PAPER, RAMP, RED, TINT,
    _impacto, _svg, calor, circle, fmt, head, icono, line, md, mezcla, pill, rect, sobre, uid,
)

from .base import (arrow, flecha_svg)  # añadidos el 01-11-2026

__all__ = ["circuito_cadena", "cadena_capas", "Iso", "ESCENAS", "escena", "escena_iso", "catalogo_escenas", "cadena_isometrica", "cadena_margen", "trayecto"]


def circuito_cadena(cadena, iconos, i_sale, i_entra, socio, externo, flecha_sale, flecha_entra, lecturas,
                    titulo_lecturas="Conclusión estratégica", titulo_cadena="", W=1152, H=420):
    """Cadena de valor como camino con estaciones e iconos; un actor (bloque rojo) se engancha por dos flechas
    (lo que saca de una estación y lo que devuelve a otra) y un actor externo llega con una flecha curva punteada.
    A la izquierda, un recuadro gris claro con la lectura estratégica.
    cadena: [paso] (5 a 7); iconos: uno por paso; i_sale, i_entra: índices de las estaciones enganchadas;
    socio = {"logo_html", "pill", "texto"}; externo = {"logo_html", "texto"}; flecha_sale y flecha_entra: HTML;
    lecturas: [(quién, texto)].
    Cuándo usarlo: explicar por qué un competidor o socio gana con un modelo (circular, de dependencia), no con un producto.
    Cuándo no: para una cadena de valor sin actor que se engancha (usa proceso_flechas o una cadena simple)."""
    L = Lienzo(W, H)
    n, ys, r = len(cadena), 104, 33
    xs = [62 + i * (W - 124) / (n - 1) for i in range(n)]
    if titulo_cadena:
        L.div(0, 0, 600, f'<span class="k">{E(titulo_cadena)}</span>')
    L.add(line(14, ys, W - 22, ys, FILL, 22, cap="round"), line(14, ys, W - 30, ys, PAPER, 2, dash="10 9"))
    L.add(head(W - 2, ys, 0, FILL, 20))
    xa, xb = xs[i_sale], xs[i_entra]
    by0, by1 = H - 176, H - 8
    bx0, bx1 = xa - 150, xb + 150
    ym = (ys + r + by0) / 2
    for i, (paso, ic) in enumerate(zip(cadena, iconos)):
        hot = i in (i_sale, i_entra)
        L.add(f'<ellipse cx="{xs[i]:.1f}" cy="{ys + r + 6}" rx="{r + 6}" ry="7" fill="{GREY}" fill-opacity=".7"/>')
        L.add(circle(xs[i], ys, r, PAPER, RED if hot else INPUT, 2.5 if hot else 1.5))
        L.div(xs[i], ys, 2 * r, icono(ic, 32, RED if hot else FG2), anchor="middle", va="middle", style="line-height:0")
        L.div(xs[i], ys - r - 10, 170, f'<b>{E(paso)}</b>', anchor="middle", va="bottom", style="font-size:14px;line-height:1.2")
    for x, y0, y1 in ((xa, ys + r + 3, by0), (xb, by0, ys + r + 3)):
        d = 1 if y1 > y0 else -1
        base = y1 - d * 22
        L.add(line(x, y0, x, base + d, RED, 12), head(x, y1, d * math.pi / 2, RED, 24))
        y = y0 + d * 14
        while (base - y) * d > 8:
            L.add(f'<path d="M{x - 3.5},{y - d * 2.5} L{x},{y + d * 1.5} L{x + 3.5},{y - d * 2.5}" fill="none" stroke="#fff" '
                  'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
            y += d * 13
    cy = (by0 + by1) / 2
    L.add(rect(bx0, by0, bx1 - bx0, by1 - by0, RED, rx=18), rect(bx0 + 24, cy - 42, 164, 84, PAPER, rx=12))
    L.div(bx0 + 24, cy, 164, f'<div style="display:flex;justify-content:center">{socio["logo_html"]}</div>', va="middle", style="line-height:0")
    L.div(bx0 + 212, cy, bx1 - bx0 - 236, f'{pill(socio["pill"], "burg")}<div style="margin-top:10px">{md(socio["texto"])}</div>', cls="on-red",
          va="middle", style="font-size:14px;line-height:1.45")
    L.div(xa - 20, ym, 200, flecha_sale, cls="red big", anchor="end", va="middle")
    L.div(xb - 20, ym, xb - xa - 44, flecha_entra, cls="red big", anchor="end", va="middle")
    gx0 = W - 220
    L.add(rect(gx0, by0, W - gx0 - 1, by1 - by0, PAPER, rx=18, stroke=INPUT, sw=1.5))
    L.div(gx0 + (W - gx0) / 2, cy, W - gx0 - 40, f'<div style="display:flex;justify-content:center">{externo["logo_html"]}</div>'
          f'<div style="margin-top:14px;font-size:14px;line-height:1.4;color:var(--fg2)">{md(externo["texto"])}</div>', anchor="middle", va="middle")
    x0, xe, ye = gx0 + 40, xb + 28, ys + r + 12
    c2 = (xb + 60, ys + r + 50)
    L.add(f'<path d="M{x0},{by0 - 2} C{x0},{by0 - 74} {c2[0]},{c2[1]} {xe + 3},{ye + 4}" fill="none" stroke="{FG3}" stroke-width="2" stroke-dasharray="6 5"/>')
    L.add(head(xe, ye, math.atan2(ye - c2[1], xe - c2[0]), FG3, 14))
    lx1, ly0 = bx0 - 34, by0 - 48
    L.add(rect(0, ly0, lx1, by1 - ly0, LGREY, stroke=BORDER2, sw=1))
    L.div(18, ly0 + 16, lx1 - 36, f'<span class="k" style="color:var(--red)">{E(titulo_lecturas)}</span>' + "".join(
        f'<div style="margin-top:{18 if i else 4}px;font-size:14px;line-height:1.4"><b style="color:var(--fg1)">{E(q)}</b><br>{md(t)}</div>'
        for i, (q, t) in enumerate(lecturas)))
    return L.render()


def _chevron(nombre, hot=False, primero=False, punta=16, alto=44, tam=13):
    """Chevrón HTML (clip-path) para cabeceras de cadena en rejilla CSS; los contiguos encajan solos."""
    clip = (f"polygon(0 0,calc(100% - {punta}px) 0,100% 50%,calc(100% - {punta}px) 100%,0 100%"
            + ("" if primero else f",{punta}px 50%") + ")")
    return (f'<div style="height:{alto}px;clip-path:{clip};background:{RED if hot else FG1};color:#fff;display:flex;align-items:center;'
            f'justify-content:center;text-align:center;padding:0 {punta + 6}px;font-size:{tam}px;font-weight:700;line-height:1.15">{E(nombre)}</div>')


def cadena_capas(eslabones, filas=None, destacado=None, rotulos=None, W=1100, ancho_rotulo=130):
    """Cadena de valor en capas (opción 1): chevrones arriba y, debajo, una fila por dimensión del análisis:
    qué ocurre, actores, margen (rango y valor típico), tendencia del margen y oportunidad para el cliente
    (en calor). El eslabón destacado se sombrea en toda la columna.
    eslabones: [dict(nombre, descripcion, actores=[...], margen=(mín, máx, típico), tendencia=-2 a 2,
    oportunidad=0 a 1)]; filas: subconjunto y orden de las filas; rotulos: para renombrar filas.
    Cuándo usarlo: explicar un sector y decir dónde está el valor y dónde entrar, en una slide completa.
    Cuándo no: si solo hay un dato por eslabón (usa cadena_isometrica o chevrones)."""
    filas = filas or ["descripcion", "actores", "margen", "tendencia", "oportunidad"]
    rot = {"descripcion": "Qué ocurre", "actores": "Actores clave", "margen": "Margen", "tendencia": "Tendencia del margen",
           "oportunidad": "Oportunidad para el cliente"} | (rotulos or {})
    n = len(eslabones)
    mx = max((e["margen"][1] for e in eslabones if e.get("margen")), default=1) * 1.1
    palabra = {2: "Sube mucho", 1: "Sube", 0: "Estable", -1: "Baja", -2: "Baja mucho"}

    def celda(k, e):
        if k == "descripcion":
            return f'<div style="font-size:13px;line-height:1.35;color:var(--fg2)">{md(e["descripcion"])}</div>'
        if k == "actores":
            return ('<div style="display:flex;flex-wrap:wrap;gap:4px">' + "".join(
                f'<span style="background:#fff;border:1px solid var(--border-1);border-radius:6px;padding:3px 7px;font-size:12px;font-weight:600;color:var(--fg1)">{E(a)}</span>'
                for a in e.get("actores", [])) + '</div>')
        if k == "margen":
            a, b, m = e["margen"]
            return (f'<div style="font-size:15px;font-weight:700;color:var(--fg1)">~{fmt(m)} %<span style="font-size:11px;font-weight:400;color:var(--fg3)"> · {fmt(a)} a {fmt(b)} %</span></div>'
                    f'<div style="position:relative;height:8px;border-radius:99px;background:var(--surface-fill);margin-top:6px">'
                    f'<i style="position:absolute;left:{a / mx * 100:.1f}%;width:{(b - a) / mx * 100:.1f}%;top:0;bottom:0;border-radius:99px;background:{FG4}"></i>'
                    f'<i style="position:absolute;left:calc({m / mx * 100:.1f}% - 6px);top:-2px;width:12px;height:12px;border-radius:50%;background:var(--red);box-shadow:0 0 0 2px #fff"></i></div>')
        if k == "tendencia":
            return f'<div style="display:flex;align-items:center;gap:7px;font-size:13px;font-weight:600;color:var(--fg1)">{_impacto(e["tendencia"], 20)}{palabra[e["tendencia"]]}</div>'
        if k == "oportunidad":
            t = e["oportunidad"]
            c = calor(t)
            nivel = "Alta" if t >= .67 else ("Media" if t >= .34 else "Baja")
            return f'<div style="background:{c};color:{sobre(c)};border-radius:8px;padding:8px 10px;font-size:13px;font-weight:700;text-align:center">{nivel}</div>'
        return ""
    sombra = mezcla(TINT, "#FFFFFF", .45)
    cab = f'<div></div>' + "".join(f'<div style="padding-bottom:6px">{_chevron(e["nombre"], i == destacado, i == 0)}</div>' for i, e in enumerate(eslabones))
    cuerpo = ""
    for k in filas:
        cuerpo += f'<div style="border-top:1px dashed var(--input);padding:10px 8px 10px 0" class="k2">{E(rot[k])}</div>'
        cuerpo += "".join(f'<div style="border-top:1px dashed var(--input);padding:10px 10px;{f"background:{sombra};" if i == destacado else ""}">{celda(k, e)}</div>'
                          for i, e in enumerate(eslabones))
    return f'<div style="width:{W}px;display:grid;grid-template-columns:{ancho_rotulo}px repeat({n},1fr);column-gap:4px;align-items:stretch">{cab}{cuerpo}</div>'


_C30, _S30 = math.cos(math.pi / 6), .5


class Iso:
    """Kit isométrico mínimo (vista desde arriba a 30°): cajas con ventanas, tejados a dos aguas, cilindros,
    cúpulas, planos, ruedas y líneas en 3D, con caras sombreadas a partir de un color base.
    Coordenadas de mundo (x, y, z) en unidades; s = px por unidad. Se dibuja de atrás adelante (x + y creciente):
    las caras visibles son el techo, la izquierda (lado y + d) y la derecha (lado x + w)."""

    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s, self.out, self.defs = ox, oy, s, [], []

    def p(self, x, y, z=0):
        return self.ox + (x - y) * _C30 * self.s, self.oy + (x + y) * _S30 * self.s - z * self.s

    def _pol(self, pts, c, borde="#fff", ancho=.6):
        q = " ".join(f"{a:.1f},{b:.1f}" for a, b in (self.p(*t) for t in pts))
        self.out.append(f'<polygon points="{q}" fill="{c}" stroke="{borde}" stroke-width="{ancho}" stroke-linejoin="round"/>')

    @staticmethod
    def tonos(c):
        return mezcla(c, "#FFFFFF", .35), c, mezcla(c, FG1, .18)        # techo, cara izquierda, cara derecha

    def caja(self, x, y, z, w, d, h, c, borde="#fff", ventanas=0):
        """Caja; ventanas: número de filas de ventanas en las dos caras visibles (True = 1)."""
        t, l, r = self.tonos(c)
        self._pol([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], l, borde)
        self._pol([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], r, borde)
        self._pol([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], t, borde)
        filas = int(ventanas)
        if filas and h >= 1.6:
            cv = mezcla(c, FG1, .35)
            alto_v = min(.8, h / (filas * 2.2))
            for f in range(filas):
                z0 = z + h * (f + .45) / filas if filas > 1 else z + h * .45
                z1 = z0 + alto_v
                nw, nd = int(w / 1.1), int(d / 1.1)
                for k in range(nw):
                    xa = x + .5 + k * (w - 1) / max(nw - 1, 1)
                    self._pol([(xa, y + d, z0), (xa + .45, y + d, z0), (xa + .45, y + d, z1), (xa, y + d, z1)], cv, cv)
                for k in range(nd):
                    ya = y + .5 + k * (d - 1) / max(nd - 1, 1)
                    self._pol([(x + w, ya, z0), (x + w, ya + .45, z0), (x + w, ya + .45, z1), (x + w, ya, z1)], mezcla(cv, FG1, .15), cv)

    def dos_aguas(self, x, y, z, w, d, h, c, borde="#fff"):
        """Tejado a dos aguas sobre una caja (cumbrera a lo largo de x)."""
        t, l, r = self.tonos(c)
        zc = z + h
        self._pol([(x, y, z), (x + w, y, z), (x + w, y + d / 2, zc), (x, y + d / 2, zc)], t, borde)
        self._pol([(x, y + d, z), (x + w, y + d, z), (x + w, y + d / 2, zc), (x, y + d / 2, zc)], l, borde)
        self._pol([(x + w, y, z), (x + w, y + d, z), (x + w, y + d / 2, zc)], r, borde)

    def cilindro(self, cx, cy, z, rad, h, c):
        t, l, r = self.tonos(c)
        g = uid("cy")
        self.defs.append(f'<linearGradient id="{g}"><stop offset="0" stop-color="{l}"/><stop offset="1" stop-color="{r}"/></linearGradient>')
        (tx, ty), (bx, by) = self.p(cx, cy, z + h), self.p(cx, cy, z)
        rx, ry = 1.2247 * rad * self.s, .7071 * rad * self.s
        self.out.append(f'<path d="M{tx - rx:.1f},{ty:.1f} L{bx - rx:.1f},{by:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {bx + rx:.1f},{by:.1f} '
                        f'L{tx + rx:.1f},{ty:.1f} Z" fill="url(#{g})" stroke="#fff" stroke-width=".6"/>')
        self.out.append(f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{t}" stroke="#fff" stroke-width=".6"/>')

    def cupula(self, cx, cy, z, rad, c, alto=1.0):
        """Cúpula sobre la tapa de un cilindro (depósitos, digestores, sombrillas)."""
        t, l, r = self.tonos(c)
        g = uid("cu")
        self.defs.append(f'<linearGradient id="{g}"><stop offset="0" stop-color="{t}"/><stop offset="1" stop-color="{r}"/></linearGradient>')
        tx, ty = self.p(cx, cy, z)
        rx, ry = 1.2247 * rad * self.s, .7071 * rad * self.s
        self.out.append(f'<path d="M{tx - rx:.1f},{ty:.1f} A{rx:.1f},{rad * alto * self.s:.1f} 0 0 1 {tx + rx:.1f},{ty:.1f} '
                        f'A{rx:.1f},{ry:.1f} 0 0 1 {tx - rx:.1f},{ty:.1f} Z" fill="url(#{g})" stroke="#fff" stroke-width=".6"/>')

    def plano(self, pts, c, borde="#fff", ancho=.6):
        self._pol(pts, c, borde, ancho)

    def linea(self, a, b, c, ancho=2):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        self.out.append(line(x1, y1, x2, y2, c, ancho, cap="round"))

    def rueda(self, x, y, z, rad=.32):
        cx, cy = self.p(x, y, z)
        self.out.append(circle(cx, cy, rad * self.s, FG1, "#fff", .8))


def _paleta(hot):
    """Colores de una escena: fase normal en grises cálidos; fase destacada con tejados y acentos en rojo."""
    return dict(muro=mezcla(INPUT, "#FFFFFF", .25), techo=RED if hot else FG4, acento=RAMP[3] if hot else mezcla(FG4, "#FFFFFF", .2),
                oscuro=FG2, tierra=mezcla(DCREAM, FG4, .3), cristal=mezcla(GREY, "#FFFFFF", .45), agua=mezcla(FG4, "#FFFFFF", .5),
                base=TINT if hot else FILL)


ESCENAS = {}


def escena(nombre, descripcion, eslabon, alto=6):
    """Registra una escena isométrica: ESCENAS[nombre] = (función(k, c), descripción, eslabón típico, alto máximo).
    Para añadir una nueva basta con decorar una función que dibuje sobre una plataforma de 0 a 10 unidades;
    alto es la cota más alta del dibujo (en unidades), para reservar el espacio justo encima."""
    def reg(f):
        ESCENAS[nombre] = (f, descripcion, eslabon, alto)
        return f
    return reg


@escena("granja", "Ganadería: establo con silo", "Producción primaria", alto=7)
def _e_granja(k, c):
    k.cilindro(2.2, 2.4, 0, 1.2, 6, c["acento"])
    k.cupula(2.2, 2.4, 6, 1.2, c["acento"], .6)
    k.caja(4, 1.4, 0, 4.4, 4.2, 3, c["muro"], ventanas=1)
    k.dos_aguas(4, 1.4, 3, 4.4, 4.2, 2, c["techo"])
    k.caja(1.2, 6.4, 0, 2.6, 2.4, 1.4, c["muro"])
    for i in range(5):
        k.caja(4.2 + i * 1.1, 8.6, 0, .12, .12, .8, c["oscuro"])
    k.caja(4.2, 8.6, .6, 4.5, .1, .08, c["oscuro"])


@escena("cultivo", "Cultivo extensivo: surcos y tractor", "Producción primaria", alto=3.5)
def _e_cultivo(k, c):
    for i in range(6):
        k.caja(.8, .8 + i * 1.45, 0, 8.4, .8, .35, c["tierra"])
    k.caja(4.6, 3, .35, 3.2, 1.8, 1.4, c["techo"])
    k.caja(6.2, 3, 1.75, 1.6, 1.8, 1.3, c["muro"])
    k.caja(3.4, 3.2, .35, 1.2, 1.4, .4, c["oscuro"])
    k.rueda(5.2, 4.8, .7, .7)
    k.rueda(7.3, 4.8, .5, .45)


@escena("invernadero", "Invernadero de alta tecnología", "Producción primaria", alto=3.5)
def _e_invernadero(k, c):
    for j in range(2):
        k.caja(1, 1.4 + j * 3.2, 0, 7, 3, 2.2, c["cristal"], borde=FG4)
        k.dos_aguas(1, 1.4 + j * 3.2, 2.2, 7, 3, 1.2, c["cristal"], borde=FG4)
    k.caja(8.4, 1.6, 0, 1.2, 1.6, 1.4, c["techo"])


@escena("granja_vertical", "Granja vertical en interior", "Producción primaria", alto=7.6)
def _e_vertical(k, c):
    k.caja(2.4, 2, 0, 4.2, 4.2, 7.2, c["muro"], ventanas=4)
    k.caja(2.4, 2, 7.2, 4.2, 4.2, .3, c["techo"])
    k.caja(7.2, 5.6, 0, 1.8, 2.4, 1.4, c["acento"])


@escena("acuicultura", "Acuicultura: estanques y nave", "Producción primaria", alto=3.6)
def _e_acuicultura(k, c):
    k.caja(5.6, 1.2, 0, 3.4, 3, 2.4, c["muro"], ventanas=1)
    k.dos_aguas(5.6, 1.2, 2.4, 3.4, 3, 1.1, c["techo"])
    for cx, cy in ((2.2, 2.4), (2.4, 6.2), (6.4, 6.8)):
        k.cilindro(cx, cy, 0, 1.6, .7, c["acento"])
        k.cilindro(cx, cy, .1, 1.35, .62, c["agua"])


@escena("puerto", "Pesca y puerto", "Producción primaria", alto=3.2)
def _e_puerto(k, c):
    k.caja(1, 1, 0, 4.2, 3.4, 2.6, c["muro"], ventanas=1)
    k.caja(1, 1, 2.6, 4.2, 3.4, .3, c["techo"])
    k.plano([(0, 5.6, .02), (10, 5.6, .02), (10, 10, .02), (0, 10, .02)], c["agua"])
    k.caja(5.6, 1, 0, 1.2, 4.6, .4, c["oscuro"])
    k.caja(2, 7, .02, 5.2, 1.6, .7, c["techo"])
    k.caja(3, 7.2, .72, 1.8, 1.2, 1, c["muro"])
    k.linea((5.6, 7.8, .7), (5.6, 7.8, 3), c["oscuro"], 1.5)


@escena("silos", "Almacén de grano: silos y elevador", "Ingredientes", alto=7.4)
def _e_silos(k, c):
    for cx in (2, 4.4, 6.8):
        k.cilindro(cx, 2.4, 0, 1.1, 5.4, c["acento"])
        k.cupula(cx, 2.4, 5.4, 1.1, c["acento"], .5)
    k.caja(8.4, 1.6, 0, 1, 1, 7.4, c["techo"])
    k.caja(2.2, 5.6, 0, 5.2, 3, 2.4, c["muro"], ventanas=1)
    k.caja(2.2, 5.6, 2.4, 5.2, 3, .3, c["techo"])


@escena("ingredientes", "Planta de ingredientes", "Ingredientes", alto=4.6)
def _e_ingredientes(k, c):
    k.cilindro(2.1, 2.1, 0, 1.3, 4.6, c["acento"])
    k.cilindro(2.1, 5.4, 0, 1.3, 4.6, c["acento"])
    k.caja(4.6, 1.4, 0, 4, 5.4, 3.4, c["muro"], ventanas=1)
    k.caja(5.6, 2.4, 3.4, 2, 2, 1.2, c["techo"])
    k.caja(5.4, 7.6, 0, 2.6, 1.4, 1, c["techo"])


@escena("fermentacion", "Fermentación de precisión: biorreactores", "Ingredientes", alto=5.1)
def _e_fermentacion(k, c):
    k.caja(1, 1, 0, 8, 2.6, 3.4, c["muro"], ventanas=1)
    k.caja(1, 1, 3.4, 8, 2.6, .3, c["techo"])
    k.linea((2.4, 6, 3.6), (7.6, 6, 3.6), c["oscuro"], 2.5)
    for cx in (2.4, 5, 7.6):
        k.cilindro(cx, 6, 0, 1.15, 4.4, c["acento"])
        k.cupula(cx, 6, 4.4, 1.15, c["acento"], .55)
    k.caja(1, 8.4, 0, 8, .6, .3, c["oscuro"])


@escena("laboratorio", "I+D y laboratorio", "Ingredientes", alto=5.9)
def _e_laboratorio(k, c):
    k.caja(1.6, 1.6, 0, 5.4, 5, 3.6, c["muro"], ventanas=1)
    k.caja(1.6, 1.6, 3.6, 5.4, 5, .3, c["techo"])
    k.cilindro(4.3, 4.1, 3.9, 1, 1.2, c["acento"])
    k.cupula(4.3, 4.1, 5.1, 1, c["acento"], .8)
    k.cilindro(8, 3, 0, .9, 3, c["acento"])


@escena("planta_piloto", "Planta piloto con equipos a escala", "Ingredientes", alto=4)
def _e_piloto(k, c):
    k.caja(1, 1, 0, 4, 3.4, 3, c["muro"], ventanas=1)
    k.dos_aguas(1, 1, 3, 4, 3.4, 1, c["techo"])
    k.caja(4.4, 5.2, 0, 4.8, 3.8, .3, c["oscuro"])
    k.linea((5.4, 6.4, 1.8), (8.4, 6.4, 1.8), c["oscuro"], 2)
    for cx, h in ((5.4, 2.4), (6.9, 1.8), (8.4, 2.4)):
        k.cilindro(cx, 6.4, .3, .6, h, c["acento"])
    k.caja(5, 7.8, .3, 2.2, .9, .9, c["muro"])


@escena("fabrica", "Planta de transformación alimentaria", "Transformación", alto=9)
def _e_fabrica(k, c):
    k.cilindro(2.6, 1.8, 0, .55, 9, c["acento"])
    k.caja(6.2, 1, 0, 2.8, 2.2, 2.4, c["muro"])
    k.caja(1.4, 3, 0, 6, 4.6, 4, c["muro"], ventanas=1)
    k.caja(1.4, 3, 4, 6, 4.6, .35, c["techo"])
    k.cilindro(8.2, 6.6, 0, .9, 2.6, c["acento"])
    k.cilindro(8.2, 8.6, 0, .9, 2.6, c["acento"])


@escena("lacteo", "Central láctea: nave y silos de leche", "Transformación", alto=6.1)
def _e_lacteo(k, c):
    k.caja(1, 2, 0, 5.6, 5.6, 3.4, c["muro"], ventanas=1)
    k.caja(1, 2, 3.4, 5.6, 5.6, .3, c["techo"])
    k.linea((6.6, 4.2, 2.8), (7.3, 4.2, 2.8), c["oscuro"], 3)
    for cy in (1.4, 3.4, 5.4):
        k.cilindro(8.2, cy, 0, .9, 5.6, c["acento"])
        k.cupula(8.2, cy, 5.6, .9, c["acento"], .45)


@escena("envasado", "Envasado: línea y palés", "Transformación", alto=4.3)
def _e_envasado(k, c):
    k.caja(1, 1, 0, 5, 4.6, 3.2, c["muro"], ventanas=1)
    k.dos_aguas(1, 1, 3.2, 5, 4.6, 1.1, c["techo"])
    k.caja(6, 2.6, .8, 3.6, 1, .25, c["oscuro"])
    for i in range(3):
        k.caja(6.4 + i * 1.1, 2.75, 1.05, .7, .7, .6, c["acento"])
    for i in range(3):
        k.caja(2 + i * 2.2, 7.2, 0, 1.6, 1.6, .2, c["tierra"])
        k.caja(2.2 + i * 2.2, 7.4, .2, 1.2, 1.2, 1, c["acento"])


@escena("logistica", "Centro logístico con camión", "Distribución", alto=3.3)
def _e_logistica(k, c):
    k.caja(1.4, 1.2, 0, 5.4, 4.4, 3, c["muro"], ventanas=1)
    k.caja(1.4, 1.2, 3, 5.4, 4.4, .3, c["techo"])
    k.caja(7.8, 2, 0, 1.4, 1.4, .9, c["muro"])
    k.caja(7.8, 4, 0, 1.4, 1.4, .9, c["muro"])
    k.caja(1.6, 7, .3, 4.2, 1.9, 2.1, c["acento"])
    k.caja(5.9, 7, .3, 1.5, 1.9, 1.6, c["techo"])
    for x in (2.4, 4.6, 6.6):
        k.rueda(x, 8.9, .3)


@escena("frio", "Almacén frigorífico", "Distribución", alto=4.5)
def _e_frio(k, c):
    k.caja(1, 1, 0, 7, 5, 3.4, c["muro"])
    k.caja(1, 1, 3.4, 7, 5, .3, c["techo"])
    for x in (2, 4.2, 6.4):
        k.caja(x, 2.2, 3.7, 1.4, 1.4, .7, c["acento"])
        k.cilindro(x + .7, 2.9, 4.4, .45, .05, c["oscuro"])
    for i in range(3):
        k.caja(2 + i * 2, 6, 0, 1.4, .6, 1.8, c["oscuro"])
    k.caja(8.6, 2, 0, .9, .9, 2.2, c["acento"])


@escena("ecommerce", "Última milla y comercio electrónico", "Distribución", alto=3.1)
def _e_ecommerce(k, c):
    k.caja(1.2, 1.2, 0, 5.2, 4, 2.8, c["muro"], ventanas=1)
    k.caja(1.2, 1.2, 2.8, 5.2, 4, .3, c["techo"])
    for x0 in (1.6, 5.4):
        k.caja(x0, 7, .25, 2.4, 1.4, 1.3, c["acento"])
        k.caja(x0 + 2.4, 7, .25, .8, 1.4, .9, c["muro"])
        k.rueda(x0 + .6, 8.4, .25, .25)
        k.rueda(x0 + 2.6, 8.4, .25, .25)
    for i in range(3):
        k.caja(7.4, 1.6 + i * 1.2, 0, .9, .9, .7, c["tierra"])


@escena("retail", "Supermercado", "Retail", alto=4.6)
def _e_retail(k, c):
    k.caja(2, 1.6, 0, 6, 5.2, 3.2, c["muro"], ventanas=1)
    k.caja(2, 1.6, 3.2, 6, 5.2, .3, c["techo"])
    k.caja(3, 2.4, 3.5, 3.2, .5, 1.1, c["acento"])
    k.plano([(2, 6.8, 2.6), (8, 6.8, 2.6), (8, 8, 2.0), (2, 8, 2.0)], c["acento"])


@escena("horeca", "Restauración (HORECA)", "Retail", alto=4.1)
def _e_horeca(k, c):
    k.caja(1.4, 1.2, 0, 5, 4.2, 2.8, c["muro"], ventanas=1)
    k.dos_aguas(1.4, 1.2, 2.8, 5, 4.2, 1.3, c["techo"])
    k.plano([(1.4, 5.4, 2.2), (6.4, 5.4, 2.2), (6.4, 6.4, 1.7), (1.4, 6.4, 1.7)], c["acento"])
    for cx, cy in ((3, 7.8), (5.6, 7.8), (8, 5.6)):
        k.cilindro(cx, cy, 0, .5, .7, c["muro"])
        k.linea((cx, cy, .7), (cx, cy, 2.1), c["oscuro"], 1.5)
        k.cupula(cx, cy, 2.1, 1, c["acento"], .35)


@escena("consumidor", "Hogar del consumidor", "Consumo", alto=4.6)
def _e_consumidor(k, c):
    k.caja(2.4, 2, 0, 4.6, 4.4, 2.6, c["muro"], ventanas=1)
    k.dos_aguas(2.4, 2, 2.6, 4.6, 4.4, 2, c["techo"])
    k.caja(7.4, 4.6, 0, 1.8, 2.4, 1.6, c["acento"])


@escena("valorizacion", "Valorización de subproductos: biodigestor", "Circularidad", alto=3.4)
def _e_valorizacion(k, c):
    for cx, cy in ((2.6, 2.6), (6.4, 2.6)):
        k.cilindro(cx, cy, 0, 1.6, 2.2, c["muro"])
        k.cupula(cx, cy, 2.2, 1.6, c["acento"], .7)
    k.caja(1.4, 6, 0, 3.4, 2.6, 2.2, c["muro"], ventanas=1)
    k.caja(1.4, 6, 2.2, 3.4, 2.6, .3, c["techo"])
    for i in range(2):
        k.caja(6 + i * 1.8, 6.4, 0, 1.4, 2.2, 1.2, c["acento"])


@escena("energia", "Energía renovable: placas y aerogenerador", "Circularidad", alto=10.8)
def _e_energia(k, c):
    k.cilindro(2, 2, 0, .2, 8, c["muro"])
    hx, hy = k.p(2, 2, 8.2)
    for a in (-90, 30, 150):
        k.out.append(line(hx, hy, hx + 2.6 * k.s * math.cos(math.radians(a)), hy + 2.6 * k.s * math.sin(math.radians(a)), FG3, 3, cap="round"))
    k.out.append(circle(hx, hy, 3, FG2))
    for fila in range(3):
        for col in range(2):
            x, y = 3.8 + col * 2.9, 3.2 + fila * 2.1
            k.caja(x + .2, y + .5, 0, .15, .15, .5, c["oscuro"])
            k.plano([(x, y, 1.1), (x + 2.5, y, 1.1), (x + 2.5, y + 1.4, .5), (x, y + 1.4, .5)], c["techo"] if c["techo"] == RED else FG2)


@escena("oficina", "Oficinas, startup o inversor", "Institucional", alto=7.9)
def _e_oficina(k, c):
    k.caja(4.4, 1.4, 0, 3.6, 3.6, 7.6, c["muro"], ventanas=5)
    k.caja(4.4, 1.4, 7.6, 3.6, 3.6, .3, c["techo"])
    k.caja(1.2, 4, 0, 4, 4.6, 2.6, c["muro"], ventanas=1)
    k.caja(1.2, 4, 2.6, 4, 4.6, .3, c["acento"])


@escena("regulador", "Administración y regulación", "Institucional", alto=4.6)
def _e_regulador(k, c):
    k.caja(1.4, 1.4, 0, 7, 4.6, 3.4, c["muro"], ventanas=1)
    k.dos_aguas(1.4, 1.4, 3.4, 7, 4.6, 1.2, c["techo"])
    k.caja(1.2, 6.4, 0, 7.4, 1.6, .4, c["tierra"])
    for i in range(6):
        k.cilindro(1.8 + i * 1.3, 6.5, .4, .22, 2.9, c["muro"])
    k.caja(1.2, 6, 3.3, 7.4, .9, .3, c["techo"])


@escena("comunicacion", "Comunicación y difusión: estudio con antena y pantalla", "Transversal", alto=8.4)
def _e_comunicacion(k, c):
    k.caja(1.2, 3.6, 0, 6, 5, 2.8, c["muro"], ventanas=1)
    k.caja(1.2, 3.6, 2.8, 6, 5, .3, c["techo"])
    k.plano([(2, 8.62, .7), (6.4, 8.62, .7), (6.4, 8.62, 2.3), (2, 8.62, 2.3)], c["oscuro"])
    k.caja(6.6, 1, 0, 1.6, 1.6, .5, c["tierra"])
    k.cilindro(7.4, 1.8, .5, .14, 7.4, c["oscuro"])
    for z, ancho_ in ((6.9, .9), (5.9, 1.25), (4.9, 1.6)):
        k.linea((7.4 - ancho_, 1.8, z), (7.4 + ancho_, 1.8, z), c["techo"], 2.4)
    k.cupula(3.2, 5.4, 3.1, .85, c["acento"], .9)


@escena("hoja_de_ruta", "Próximos pasos: camino con hitos hacia una meta", "Transversal", alto=5.6)
def _e_hoja_de_ruta(k, c):
    tramos = [(.8, 7.6, 3.6, 1.3), (3.2, 4.6, 1.3, 4.3), (3.2, 4.6, 3.8, 1.3), (5.9, 2.2, 1.3, 2.9)]
    for x, y, w, d in tramos:
        k.caja(x, y, 0, w, d, .12, c["tierra"])
    for x, y, alto_ in ((1.5, 8.2, 1.7), (3.8, 6.2, 2.1), (6.4, 4.4, 2.5)):
        k.cilindro(x, y, .12, .09, alto_, c["oscuro"])
        k.plano([(x, y, alto_ - .55 + .12), (x + 1.05, y, alto_ - .3 + .12), (x, y, alto_ + .12)], c["acento"])
    k.caja(6.6, .9, 0, 2.6, 2.2, 2.6, c["muro"], ventanas=1)
    k.dos_aguas(6.6, .9, 2.6, 2.6, 2.2, 1, c["techo"])


@escena("alianzas", "Alianzas y partners: dos edificios unidos por un puente", "Transversal", alto=6.4)
def _e_alianzas(k, c):
    k.caja(.9, 5.2, 0, 3.2, 3.6, 5.2, c["muro"], ventanas=3)
    k.caja(.9, 5.2, 5.2, 3.2, 3.6, .3, c["techo"])
    k.caja(5.9, 1.2, 0, 3.2, 3.6, 6, c["muro"], ventanas=4)
    k.caja(5.9, 1.2, 6, 3.2, 3.6, .3, c["techo"])
    k.caja(4.1, 3.6, 2.8, 1.8, 2, .7, c["acento"])
    k.caja(.9, 1.2, 0, 3.8, 3.2, .35, c["tierra"])
    k.cilindro(2.2, 2.6, .35, .55, .9, c["acento"])


def escena_iso(tipo, destacado=False, W=200, P=10, rotulo=None):
    """Escena isométrica suelta sobre su plataforma, para usar como ilustración (portadillas, fichas, iconos grandes).
    tipo: clave de ESCENAS o una función(k, c) propia; destacado: tejados y acentos en rojo.
    Cuándo usarlo: ilustrar un eslabón, un actor o un tipo de instalación junto a texto o datos.
    Cuándo no: como decoración sin significado (cada escena tiene que corresponder a lo que se cuenta)."""
    s = W * .8 / (2 * P * _C30)
    oy = max((ESCENAS[tipo][3] if not callable(tipo) else 9) - 1.8, 3) * s + 4
    H = oy + P * s + .7 * s + 6
    k = Iso(W / 2, oy, s)
    c = _paleta(destacado)
    k.caja(0, 0, -.7, P, P, .7, c["base"], borde=c["base"])
    (tipo if callable(tipo) else ESCENAS[tipo][0])(k, c)
    svg = _svg(W, round(H), "".join(k.out), "".join(k.defs))
    if rotulo is None:
        return svg
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;width:{W}px">{svg}'
            f'<b style="font-size:13px;color:{RED if destacado else FG1};text-align:center;line-height:1.2">{E(rotulo)}</b></div>')


def catalogo_escenas(columnas=5, W=1100, destacado=None):
    """Catálogo de todas las escenas registradas en ESCENAS, agrupadas por eslabón, con su clave para usarla.
    destacado: clave de una escena que se enseña en su versión roja."""
    cw = (W - 12 * (columnas - 1)) / columnas
    grupos = {}
    for clave, (_, desc, esl, _a) in ESCENAS.items():
        grupos.setdefault(esl, []).append((clave, desc))
    out = []
    for esl, items in grupos.items():
        out.append(f'<div class="k2" style="grid-column:1 / -1;margin:10px 0 0">{E(esl)}</div>')
        for clave, desc in items:
            out.append(f'<div style="background:#fff;border:1px solid var(--border-1);border-radius:12px;padding:8px 8px 10px;display:flex;flex-direction:column;align-items:center;gap:4px">'
                       f'{escena_iso(clave, clave == destacado, W=cw - 30)}'
                       f'<b style="font-size:13px;color:var(--fg1);text-align:center;line-height:1.2">{E(desc)}</b>'
                       f'<code style="font-family:ui-monospace,Menlo,monospace;font-size:11px;color:var(--fg3)">{clave}</code></div>')
    return f'<div style="display:grid;grid-template-columns:repeat({columnas},1fr);gap:12px;width:{W}px">{"".join(out)}</div>'


def cadena_isometrica(fases, destacado=None, W=1100, P=10):
    """Cadena de valor isométrica: cada fase en su plataforma con una escena en 3D vista desde arriba, unidas por
    una tubería con flechas de flujo. Encima, número y nombre de la fase; debajo, una línea de texto y un dato
    opcional. No es un diagrama fijo: cada fase usa cualquier escena del catálogo (ESCENAS) o una propia.
    fases: [dict(nombre, tipo = clave de ESCENAS o función(k, c), texto, dato=None)]; destacado: índice en rojo.
    P: tamaño de la plataforma en unidades del kit Iso; no se baja de 10, porque las escenas se salen de ella.
    Cuándo usarlo: abrir un informe o una propuesta presentando la cadena del sector con peso visual (4 a 7 fases).
    Cuándo no: para el análisis detallado por eslabón (usa cadena_capas, que puede ir justo después)."""
    n = len(fases)
    slot = W / n
    s = slot * .8 / (2 * P * _C30)
    alto = max((ESCENAS[f.get("tipo", "laboratorio")][3] if not callable(f.get("tipo")) else 9) for f in fases)
    oy_loc = 50 + max(alto - 1.8, 3) * s          # esquina trasera de cada plataforma: solo el alto que hace falta
    ycen = oy_loc + P * _S30 * s                  # centro de las plataformas en pantalla
    H = ycen + P * _S30 * s + .7 * s + 96
    out, defs, centros = [], [], []
    for i, f in enumerate(fases):
        hot = i == destacado
        cx = slot * (i + .5)
        k = Iso(cx, oy_loc, s)
        k.out, k.defs = out, defs
        c = _paleta(hot)
        k.caja(0, 0, -.7, P, P, .7, c["base"], borde=c["base"])
        tipo = f.get("tipo", "laboratorio")
        (tipo if callable(tipo) else ESCENAS[tipo][0])(k, c)
        centros.append((cx, ycen))
    tubos = []
    for i in range(n - 1):
        (a, y), (b, _) = centros[i], centros[i + 1]
        xa, xb = a + P * _C30 * s - 6, b - P * _C30 * s + 6
        tubos.append(line(xa, y, xb, y, FG4, 8, cap="round") + line(xa, y - 1.5, xb, y - 1.5, "#FFFFFF", 2, cap="round"))
        xm = (xa + xb) / 2
        tubos.append(f'<path d="M{xm - 5:.1f},{y - 7:.1f} L{xm + 4:.1f},{y:.1f} L{xm - 5:.1f},{y + 7:.1f}" fill="none" stroke="{RED}" stroke-width="2.5" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>')
    L = Lienzo(W, round(H))
    L.defs.extend(defs)
    L.add(*tubos[0::2], *out, *tubos[1::2])
    for i, f in enumerate(fases):
        hot = i == destacado
        cx, cy = centros[i]
        L.div(cx, 0, slot - 16, f'<div style="display:flex;align-items:center;justify-content:center;gap:8px">'
              f'<span class="nb" style="width:26px;height:26px;font-size:14px;border-radius:50%;{"" if hot else "background:var(--fg1);"}">{i + 1}</span>'
              f'<b style="font-size:14px;color:{RED if hot else FG1};line-height:1.15">{E(f["nombre"])}</b></div>', anchor="middle")
        yb = cy + P * _S30 * s + .7 * s + 12
        L.div(cx, yb, slot - 24, f'<div style="font-size:13px;line-height:1.35;color:var(--fg2)">{md(f.get("texto", ""))}</div>'
              + (f'<div style="margin-top:6px"><span class="pl {"pl-red" if hot else "pl-neutral"}">{E(f["dato"])}</span></div>' if f.get("dato") else ""),
              anchor="middle")
    return L.render()


def _tarta(pct, r=9, color=RED):
    """Tarta mínima: el porcentaje en color sobre un círculo gris."""
    t = max(0, min(100, pct)) / 100
    s = circle(r, r, r, FILL)
    if t >= .999:
        s = circle(r, r, r, color)
    elif t > 0:
        a = -math.pi / 2 + 2 * math.pi * t
        s += f'<path d="M{r},{r} L{r},0 A{r},{r} 0 {1 if t > .5 else 0} 1 {r + r * math.cos(a):.2f},{r + r * math.sin(a):.2f} Z" fill="{color}"/>'
    return f'<span style="display:inline-block;line-height:0;vertical-align:middle">{_svg(2 * r, 2 * r, s)}</span>'


def cadena_margen(eslabones, destacado=None, posicion=None, posicion_txt="Posición del cliente en esta ruta",
                  rotulos=("Margen", "Valor capturado"), W=1100, alto=214):
    """Cadena de valor con el margen de cada eslabón (cifra y tarta) y el valor que captura del precio final (cifra y
    barra). Un eslabón hipotético va en contorno discontinuo y una marca debajo dice dónde está o entraría el cliente.
    eslabones: [dict(nombre, icono, margen = número o (mín, máx), captura = número, fase=None, hipotetico=False)],
    en %; destacado: índice en rojo; posicion: índice que señala la marca de posición.
    Cuándo usarlo: decir en qué eslabón está el valor y dónde se sitúa el cliente, con 3 a 7 eslabones.
    Cuándo no: si hacen falta actores, tendencia y oportunidad por eslabón (usa cadena_capas)."""
    n = len(eslabones)
    sep, p = 8, 14
    w = (W - sep * (n - 1)) / n
    H = alto + (66 if posicion is not None else 0)
    L = Lienzo(W, H)
    mxc = max(e.get("captura", 0) for e in eslabones) * 1.15 or 1
    for i, e in enumerate(eslabones):
        x0 = i * (w + sep)
        hot, hip = i == destacado, e.get("hipotetico")
        pts = [(x0, 0), (x0 + w - p, 0), (x0 + w, alto / 2), (x0 + w - p, alto), (x0, alto)] + ([] if i == 0 else [(x0 + p, alto / 2)])
        q = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        borde = RED if hot or hip else INPUT
        fondo = mezcla(TINT, "#FFFFFF", .35) if hot else "#fff"
        L.add(f'<polygon points="{q}" fill="{fondo}" stroke="{borde}" stroke-width="{1.8 if hot else 1.3}" stroke-linejoin="round"'
              + (' stroke-dasharray="5 4"' if hip else "") + '/>')
        xl = x0 + (p if i else 0) + 12
        iw = w - p - 24 - (p if i else 0)
        m = e["margen"]
        mtxt = f"{fmt(m[0])} a {fmt(m[1])} %" if isinstance(m, (tuple, list)) else f"{fmt(m)} %"
        mval = sum(m) / 2 if isinstance(m, (tuple, list)) else m
        col = RED if hot else FG1
        if e.get("fase"):
            L.div(xl, 12, iw, f'<span style="font-size:11px;color:var(--fg3)">{E(e["fase"])}</span>')
        L.div(xl, 27, iw, f'<b style="font-size:13px;line-height:1.2;color:{col}">{E(e["nombre"])}</b>')
        L.div(x0 + (p / 2 if i else 0) + (w - (p if i else 0)) / 2 - p / 2, 68, 40, icono(e.get("icono", "label"), 26, RED if hot or hip else FG2), anchor="middle")
        L.add(line(xl, 108, xl + iw, 108, BORDER2, 1))
        L.div(xl, 116, iw, f'<div style="display:flex;justify-content:space-between;align-items:center"><div><span class="k" style="margin:0">{E(rotulos[0])}</span>'
                           f'<b style="font-size:15px;color:{col}">{E(mtxt)}</b></div>{_tarta(mval, 10, RED if hot else FG3)}</div>')
        L.div(xl, 160, iw, f'<span class="k" style="margin:0">{E(rotulos[1])}</span><b style="font-size:13px;color:var(--fg1)">{fmt(e.get("captura", 0))} %</b>')
        L.add(rect(xl, 194, iw, 5, FILL, rx=2.5), rect(xl, 194, max(2, iw * e.get("captura", 0) / mxc), 5, RED if hot else FG3, rx=2.5))
    if posicion is not None:
        cx = posicion * (w + sep) + w / 2
        L.add(arrow([(cx, alto + 30), (cx, alto + 6)], RED, 2, size=8))
        ancho = min(320, max(220, w * 1.6))
        L.add(rect(cx - ancho / 2, alto + 32, ancho, 30, "#fff", rx=15, stroke=RED, sw=1.3, dash="5 4"))
        L.div(cx, alto + 47, ancho, f'<b style="font-size:14px;color:var(--red)">{E(posicion_txt)}</b>', anchor="middle", va="middle")
    return L.render()


def trayecto(etapas, destacado=-1, W=1100, escalon=34):
    """Trayecto de hoy al destino: cajas que suben de izquierda a derecha (dónde está el cliente hoy, adónde va y por
    qué vía), unidas por flechas sobre una línea base. La de hoy en gris; las siguientes con filete rojo.
    etapas: [dict(etiqueta, titulo, dato=None, texto="")], de 2 a 4; destacado: índice con fondo rosa (por defecto la última).
    Cuándo usarlo: la recomendación en una slide (de materia prima a excipiente, de proveedor a socio).
    Cuándo no: si el camino tiene pasos con plazos y entregables (usa fases_gates o chevrones)."""
    n = len(etapas)
    destacado = destacado % n if destacado is not None else None
    cajas = []
    for i, e in enumerate(etapas):
        hoy = i == 0
        fondo = "var(--surface-fill)" if hoy else (mezcla(TINT, "#FFFFFF", .4) if i == destacado else mezcla(FILL, "#FFFFFF", .55))
        dato = (f'<div style="font-size:14px;font-weight:700;color:{"var(--fg2)" if hoy else "var(--red)"};margin:8px 0 4px">{md(e["dato"])}</div>'
                if e.get("dato") else "")
        cajas.append(f'<div style="flex:1;min-width:0;min-height:{120 + i * escalon}px;background:{fondo};border-top:3px solid {FG3 if hoy else RED};'
                     f'padding:12px 16px 14px;display:flex;flex-direction:column;justify-content:flex-end">'
                     f'<span class="k2" style="margin:0 0 2px;font-size:11px">{E(e["etiqueta"])}</span>'
                     f'<b style="font-size:15px;line-height:1.25;color:var(--fg1)">{E(e["titulo"])}</b>{dato}'
                     f'<div style="font-size:13px;line-height:1.4;color:var(--fg2)">{md(e.get("texto", ""))}</div></div>')
    fl = f'<div style="flex:none;align-self:center">{flecha_svg(FG3, 22, 14, 1.8)}</div>'
    return (f'<div style="width:{W}px;display:flex;align-items:flex-end;gap:10px;border-bottom:1.5px solid var(--fg1)">'
            + fl.join(cajas) + '</div>')
