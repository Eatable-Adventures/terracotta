#!/usr/bin/env python3
"""huella_slide: huella anónima de una slide de un PDF. Enseña cuánto contenido lleva, dónde está y qué visuales usa, no qué dice.

Variante máscara (decisión del 02-11-2026): quita de verdad el texto y las imágenes del PDF y conserva la forma de lo dibujado en
vector, para poder analizar cómo se usaron los gráficos. Cada línea de texto pasa a una barra gris, cada imagen a una caja gris y la
decoración «glow» de la cabecera desaparece. Como lo dibujado en vector pasa la limpieza, un filtro cambia por una caja gris lo que
parece un logo. Se quedan el wordmark de la base fija y los iconos sueltos.

Cómo decide el filtro. Mide el giro de cada trazo: cuánto se retuerce su contorno por encima de una vuelta. Un disco, una barra, una
tarjeta redondeada o un guion dan 0; una letra o un símbolo, bastante más. Se agrupan los trazos pequeños con giro y un grupo es un
logo si tiene giro suficiente para su tamaño (GIRO_* y DENSIDAD_MIN, calibrados con los decks de referencia y la galería).
Fallos posibles, y por eso una persona confirma la ficha antes de publicarla: un símbolo muy simple pasa por un icono, un logo muy
grande puede quedar bajo la densidad mínima, y un gráfico rasterizado entero sale como una sola caja.

Uso:
    python3 huella_slide.py deck.pdf PAGINA --out huella.png [--json datos.json] [--ancho 1280]

Imprime una línea JSON con residual_text, residual_images, logos, glow, imagenes, tipo y metrics (palabras, datos, ocupacion,
mayor_hueco y cuerpo, de medir_deck). Código de salida: 0 si no queda texto ni imágenes; 1 si queda algo, y entonces no deja el PNG;
2 si falla la entrada. Las huellas se dejan fuera de cualquier carpeta compartida hasta que una persona las confirme.
"""
import argparse, collections, json, math, pathlib, sys

import fitz
import numpy as np

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import medir_deck                # noqa: E402

GRIS, BORDE, BARRA = (.90, .90, .90), (.6, .6, .6), (.78, .78, .78)
W_NORM = 1280                    # todo el filtro trabaja en px de slide normalizada

# Trazos que entran en un grupo
PIEZA_W, PIEZA_H = 300, 160      # lo mayor ya no es parte de un logo: una forma grande o un país de un mapa
GIRO_PIEZA = .6                  # con menos giro, el trazo es liso: disco, barra, tarjeta, guion o sector de embudo
GLIFO_LADO = 80                  # hasta este lado, un trazo con curvas y dos o más contornos entra aunque sea liso (una «o»)
SEPARACION = 8.0                 # dos trazos a menos de esta distancia son del mismo grupo
RESTO_LADO = 40                  # trazos lisos pequeños pegados a un logo (la «I», el punto de la «i») van dentro de su caja
# Cuándo un grupo es un logo. Calibrado el 02-11-2026: las 15 apariciones de logos vectoriales en los 9 decks de referencia dan
# giro >= 11,3 y densidad >= 0,29; los iconos sueltos, giro <= 5,8; lo demás con varios trazos (anillos, marcos a trazos, radares), densidad <= 0,10
GIRO_VARIOS = 4.0                # dos o más trazos, con al menos este giro total
GIRO_UNICO = 8.0                 # un trazo solo: por debajo es un icono, que se queda
DENSIDAD_MIN = .15               # giro por px de lado (raíz del área)
GRANDE_GIRO = 5.0                # un trazo mayor que PIEZA_* con este giro es un mapa: sus islas, de su mismo color, no son un logo
# Firma del wordmark de la base fija, igual a cualquier escala: se queda. Si Chrome cambia cómo lo escribe, sale como caja: sin riesgo
WORDMARK_BASE = (250, 157)       # curvas y líneas de assets/logo-wordmark.svg
# Decoración «glow» de la cabecera: imagen casi cuadrada en la esquina superior izquierda
GLOW_X0, GLOW_Y0, GLOW_X1, GLOW_Y1 = 40, 60, 170, 190
GLOW_LADO_MIN = 90


def _contornos(items):
    """Polilíneas de puntos de control de un trazo, una por contorno."""
    out, act, fin = [], [], None
    for it in items:
        if it[0] == "re":
            r = it[1]
            pts = [r.tl, r.tr, r.br, r.bl, r.tl]
        elif it[0] == "qu":
            q = it[1]
            pts = [q.ul, q.ur, q.lr, q.ll, q.ul]
        else:
            pts = list(it[1:])
        if fin is None or abs(pts[0].x - fin.x) + abs(pts[0].y - fin.y) > .01:
            if act:
                out.append(act)
            act = list(pts)
        else:
            act += pts[1:]
        fin = pts[-1]
    if act:
        out.append(act)
    return out


def _giro(pts):
    """Vueltas que da un contorno, contando cada cambio de dirección en valor absoluto. Un contorno convexo da una; el giro de un
    trazo es lo que sus contornos dan por encima de esa vuelta."""
    p = [pts[0]]
    for q in pts[1:]:
        if abs(q.x - p[-1].x) + abs(q.y - p[-1].y) > 1e-3:
            p.append(q)
    if len(p) < 3:
        return 0.0
    if abs(p[0].x - p[-1].x) + abs(p[0].y - p[-1].y) > 1e-3:
        p.append(p[0])
    tot, n = 0.0, len(p) - 1
    for i in range(n):
        a, b, c = p[i], p[i + 1], p[(i + 2) % n]
        u, v = (b.x - a.x, b.y - a.y), (c.x - b.x, c.y - b.y)
        tot += abs(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1]))
    return tot / (2 * math.pi)


def _trazos(pg):
    """Dibujos de la página en px normalizados, con su detalle."""
    esc = W_NORM / pg.rect.width
    out = []
    for d in pg.get_drawings():
        r = d["rect"]
        cuenta = collections.Counter(i[0] for i in d["items"])
        gs = [_giro(c) for c in _contornos(d["items"])]
        out.append(dict(r=fitz.Rect(r.x0 * esc, r.y0 * esc, r.x1 * esc, r.y1 * esc), w=r.width * esc, h=r.height * esc, c=cuenta.get("c", 0), l=cuenta.get("l", 0),
                        cont=len(gs), giro=sum(max(0.0, g - 1) for g in gs), fill=tuple(round(x, 2) for x in d["fill"]) if d.get("fill") else None))
    return out


def _con_detalle(t):
    if t["w"] > PIEZA_W or t["h"] > PIEZA_H:
        return False
    return t["giro"] >= GIRO_PIEZA or (t["cont"] >= 2 and t["c"] > 0 and max(t["w"], t["h"]) <= GLIFO_LADO)


def _agrupar(piezas):
    pad = list(range(len(piezas)))

    def raiz(i):
        while pad[i] != i:
            pad[i] = pad[pad[i]]
            i = pad[i]
        return i
    for i, a in enumerate(piezas):
        caja = a["r"] + (-SEPARACION, -SEPARACION, SEPARACION, SEPARACION)
        for j in range(i + 1, len(piezas)):
            if caja.intersects(piezas[j]["r"]):
                pad[raiz(i)] = raiz(j)
    grupos = collections.defaultdict(list)
    for i, p in enumerate(piezas):
        grupos[raiz(i)].append(p)
    return list(grupos.values())


def _caja(grupo):
    r = fitz.Rect(grupo[0]["r"])
    for p in grupo[1:]:
        r |= p["r"]
    return r


def logos(pg):
    """Cajas (en px normalizados) de lo que parece un logo. Devuelve también los rasgos de cada grupo, para calibrar."""
    trazos = _trazos(pg)
    grandes = [t for t in trazos if (t["w"] > PIEZA_W or t["h"] > PIEZA_H) and t["giro"] >= GRANDE_GIRO]
    color_mapa = {t["fill"] for t in grandes}
    caja_mapa = None
    for t in grandes:
        caja_mapa = fitz.Rect(t["r"]) if caja_mapa is None else caja_mapa | t["r"]
    cajas, rasgos = [], []
    for g in _agrupar([t for t in trazos if _con_detalle(t)]):
        curvos = [p for p in g if p["c"]]
        if not curvos:
            continue
        r, giro = _caja(g), sum(p["giro"] for p in g)
        lado = math.sqrt(max(r.width, 1) * max(r.height, 1))
        firma = (sum(p["c"] for p in g), sum(p["l"] for p in g))
        es_mapa = caja_mapa is not None and r.intersects(caja_mapa) and bool({p["fill"] for p in g} & color_mapa)
        cumple = (giro >= GIRO_VARIOS if len(g) >= 2 else giro >= GIRO_UNICO) and giro / lado >= DENSIDAD_MIN
        es_logo = cumple and not es_mapa and firma != WORDMARK_BASE
        rasgos.append(dict(caja=[round(v) for v in r], trazos=len(g), curvos=len(curvos), curvas=firma[0], lineas=firma[1], giro=round(giro, 1), densidad=round(giro / lado, 2),
                           logo=es_logo, wordmark=firma == WORDMARK_BASE, mapa=es_mapa))
        if es_logo:
            for _ in range(3):             # lo liso pegado al grupo (una «I», el punto de una «i») va en la caja
                cerca = r + (-SEPARACION, -SEPARACION, SEPARACION, SEPARACION)
                for t in trazos:
                    if max(t["w"], t["h"]) <= RESTO_LADO and cerca.intersects(t["r"]):
                        r |= t["r"]
            cajas.append(r + (-2, -2, 2, 2))
    return cajas, rasgos


def _es_glow(r, esc):
    x0, y0, x1, y1 = r.x0 * esc, r.y0 * esc, r.x1 * esc, r.y1 * esc
    w, h = x1 - x0, y1 - y0
    return x0 <= GLOW_X0 and y0 <= GLOW_Y0 and x1 <= GLOW_X1 and y1 <= GLOW_Y1 and min(w, h) >= GLOW_LADO_MIN and .75 <= w / h <= 1.35


def _lineas(pg):
    for b in pg.get_text("dict")["blocks"]:
        if b["type"] == 0:
            for l in b["lines"]:
                if "".join(s["text"] for s in l["spans"]).strip():
                    yield fitz.Rect(l["bbox"])


def _barra(r):
    h = max(2.0, r.height * .5)
    return fitz.Rect(r.x0, (r.y0 + r.y1 - h) / 2, r.x1, (r.y0 + r.y1 + h) / 2)


def cifras(doc, n):
    """Cifras de medir_deck para la página n (1 es la primera). Vacío si no es de contenido."""
    p = medir_deck._pag(doc[n - 1], n - 1)
    return p["tipo"], {k: p[k] for k in ("palabras", "datos", "ocupacion", "mayor_hueco", "cuerpo") if k in p}


def _tapada(pm, r, z):
    """True si el interior de la caja r (en puntos del PDF) sale de un solo color en la imagen final."""
    x0, y0 = max(int(r.x0 * z) + 3, 0), max(int(r.y0 * z) + 3, 0)
    x1, y1 = min(int(r.x1 * z) - 3, pm.width), min(int(r.y1 * z) - 3, pm.height)
    if x1 <= x0 or y1 <= y0:
        return True                    # una línea de 1 px: el borde de la caja ya la cubre entera
    img = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width, pm.n)[y0:y1, x0:x1]
    return bool(np.ptp(img) <= 2)


def huella(ruta, n, ancho=W_NORM):
    """Devuelve (pixmap, datos). El texto y las imágenes salen del PDF en memoria, no solo se tapan. Lo que la limpieza no alcanza
    (una imagen usada como patrón de relleno) y los logos vectoriales van bajo una caja opaca, y esas imágenes se comprueban en píxeles."""
    doc = fitz.open(str(ruta))
    if not 1 <= n <= len(doc):
        raise ValueError(f"El PDF tiene {len(doc)} páginas y se pide la {n}")
    tipo, metrics = cifras(doc, n)
    pg = doc[n - 1]
    esc = W_NORM / pg.rect.width
    cajas, rasgos = logos(pg)
    lineas = list(_lineas(pg))
    imagenes = [fitz.Rect(i["bbox"]) for i in pg.get_image_info()]
    for r in lineas + imagenes:
        pg.add_redact_annot(r, fill=False)
    pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE, graphics=fitz.PDF_REDACT_LINE_ART_NONE, text=fitz.PDF_REDACT_TEXT_REMOVE)
    residual_text = len(pg.get_text().strip())
    quedan = [fitz.Rect(i["bbox"]) for i in pg.get_image_info()]
    glow = [r for r in imagenes if _es_glow(r, esc) and r not in quedan]
    resto = [r for r in imagenes if r not in glow and r not in quedan]
    for r in lineas:
        pg.draw_rect(_barra(r), color=None, fill=BARRA)
    for r in resto + [fitz.Rect(c.x0 / esc, c.y0 / esc, c.x1 / esc, c.y1 / esc) for c in cajas] + quedan:
        pg.draw_rect(r, color=BORDE, fill=GRIS, width=.6)
    z = ancho / pg.rect.width
    pm = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
    return pm, dict(residual_text=residual_text, residual_images=sum(not _tapada(pm, r, z) for r in quedan), logos=len(cajas), glow=len(glow),
                    imagenes=len(resto) + len(quedan), tipo=tipo, metrics=metrics, grupos=rasgos)


def main():
    ap = argparse.ArgumentParser(description="Huella anónima de una slide de un PDF")
    ap.add_argument("pdf")
    ap.add_argument("pagina", type=int, help="página del PDF; 1 es la primera")
    ap.add_argument("--out", required=True, help="PNG de salida")
    ap.add_argument("--json", help="guarda aquí también los rasgos de cada grupo de trazos")
    ap.add_argument("--ancho", type=int, default=W_NORM)
    a = ap.parse_args()
    try:
        pm, datos = huella(a.pdf, a.pagina, a.ancho)
    except (ValueError, RuntimeError, fitz.FileDataError, fitz.FileNotFoundError) as e:
        print(json.dumps(dict(error=str(e)), ensure_ascii=False))
        return 2
    grupos = datos.pop("grupos")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(dict(datos, grupos=grupos), ensure_ascii=False, indent=1), encoding="utf-8")
    limpio = datos["residual_text"] == 0 and datos["residual_images"] == 0
    if limpio:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pm.save(a.out)
    print(json.dumps(datos, ensure_ascii=False))
    return 0 if limpio else 1


if __name__ == "__main__":
    sys.exit(main())
