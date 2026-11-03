#!/usr/bin/env python3
"""medir_deck: mide cómo se distribuye un deck ya exportado a PDF, slide a slide y en conjunto, y lo compara con los
rangos calibrados sobre decks de referencia de EA (calibracion_decks.json).

Mide sobre el PDF, no sobre el HTML, para que sirva igual con decks de Terracotta y con los hechos a mano. Todo se
normaliza a una slide de 1280 × 720, así que los tamaños de letra se leen como px de Terracotta.

Por slide de contenido:
  - cuánto dice: palabras y etiquetas de dato del cuerpo (lo que hay entre la cabecera y el pie);
  - cómo de llena se ve: ocupación (celdas del cuerpo con algo), tinta (píxeles con contraste fuerte), huecos abajo,
    arriba y a los lados, mayor rectángulo vacío y desequilibrio entre izquierda y derecha;
  - cómo está escrita: tamaño de cuerpo, letra mínima, % de texto bajo 11 px, tamaños distintos, tamaño y líneas del título.
En conjunto: dispersión de densidad, tamaños de cuerpo y de título, posición del título y grupos de slides hermanas
(consecutivas con una huella parecida), con su dispersión interna de palabras y ocupación.

Mide, no opina: una marca es «esto se sale de lo habitual», para mirarla, no un error automático. Las marcas se agrupan
en cinco dimensiones (llenado, densidad, legibilidad, equilibrio y errores), para no contar varias veces lo mismo, y llevan
una tolerancia para que un roce (una fila de cuadrícula) no marque nada. Los errores son textos que se pisan o se salen.

Uso:
    python3 medir_deck.py deck.pdf [--md informe.md] [--json datos.json]
    python3 medir_deck.py --calibrar lista.txt     (una ruta de PDF por línea, relativa a la raíz del entorno interno; # comenta)
    python3 medir_deck.py --validar lista.txt [contraste.pdf]   (marca cada referencia con los rangos de las demás)
    desde código: import medir_deck; r = medir_deck.medir("deck.pdf"); print(medir_deck.informe(r))
"""
import json, pathlib, re, statistics as st, sys

import fitz
import numpy as np

AQUI = pathlib.Path(__file__).resolve().parent
CALIB = AQUI / "calibracion_decks.json"
W, H = 1280, 720            # slide normalizada
CELDA = 32                  # lado de la celda de la cuadrícula de ocupación, en px normalizados
X0, X1 = 40, 1240           # el cuerpo se mide entre estos márgenes

# métrica de slide -> (dimensión, lado que es el problema, nombre en el informe, tolerancia sobre el percentil)
METRICAS = {
    "ocupacion": ("Llenado", "bajo", "Ocupación baja", 3),
    "mayor_hueco": ("Llenado", "alto", "Gran hueco", 2),
    "hueco_abajo": ("Llenado", "alto", "Hueco abajo", 7),        # 7 puntos: una fila de cuadrícula no marca
    "hueco_arriba": ("Llenado", "alto", "Hueco arriba", 7),
    "palabras": ("Densidad", "alto", "Mucho texto", 15),
    "datos": ("Densidad", "alto", "Muchos datos", 3),
    "cuerpo": ("Legibilidad", "bajo", "Cuerpo pequeño", .5),
    "letra_min": ("Legibilidad", "bajo", "Letra mínima pequeña", .5),
    "bajo_11": ("Legibilidad", "alto", "Mucho texto bajo 11 px", 3),
    "n_tamanos": ("Legibilidad", "alto", "Muchos tamaños", 0),
    "desequilibrio": ("Equilibrio", "alto", "Desequilibrio", 5),
}
DIMENSIONES = ["Llenado", "Densidad", "Legibilidad", "Equilibrio", "Errores"]
# métricas de deck y de grupo de hermanas: en todas, lo alto es lo que se sale
METRICAS_DECK = {"cv_palabras": "Dispersión de palabras (CV, %)", "cv_datos": "Dispersión de datos (CV, %)",
                 "cv_ocupacion": "Dispersión de ocupación (CV, %)", "salto_ocupacion": "Salto medio de ocupación entre slides seguidas (puntos)",
                 "desv_inicio": "Desviación de dónde empieza el cuerpo (px)", "desv_fin": "Desviación de dónde acaba el cuerpo (px)",
                 "n_cuerpos": "Tamaños de cuerpo en uso", "n_titulos": "Tamaños de título en uso", "desv_titulo_x": "Desviación de la posición del título (px)"}
METRICAS_GRUPO = ["cv_palabras", "rango_ocupacion", "rango_cuerpo"]


def _lineas(pag, esc):
    """Líneas de texto con su caja y tamaño en px normalizados; el tamaño de la línea es el del tramo con más caracteres."""
    out = []
    for b in pag.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            sp = [s for s in l["spans"] if s["text"].strip()]
            if not sp:
                continue
            txt = "".join(s["text"] for s in sp).strip()
            x0, y0, x1, y1 = [v * esc for v in l["bbox"]]
            out.append(dict(txt=txt, x0=x0, y0=y0, x1=x1, y1=y1, size=max(sp, key=lambda s: len(s["text"]))["size"] * esc,
                            spans=[(len(s["text"].strip()), s["size"] * esc) for s in sp]))
    return sorted(out, key=lambda l: (l["y0"], l["x0"]))


def _cabecera(lineas):
    """Devuelve (líneas del título, y donde empieza el cuerpo). El título es el texto mayor del tercio superior; el
    subtítulo, una línea sola justo debajo, alineada con él a la izquierda."""
    # el título empieza arriba y es una frase; más abajo o suelto, un texto grande es una cifra
    arriba = [l for l in lineas if l["y0"] < 170 and (len(l["txt"].split()) >= 2 or len(l["txt"]) >= 8)]
    if not arriba:
        return [], 60.0
    s = max(l["size"] for l in arriba)
    if s < 18:
        return [], 60.0
    tit = [l for l in lineas if l["y0"] < 260 and l["size"] >= .9 * s and l["y0"] >= arriba[0]["y0"] and abs(l["x0"] - arriba[0]["x0"]) < 200]
    y = tit[0]["y1"]
    bloque = [tit[0]]
    for l in tit[1:]:                                       # solo líneas contiguas: un número grande más abajo no es título
        if l["y0"] - y > s * .9:
            break
        bloque.append(l); y = max(y, l["y1"])
    fondo = y
    bajo = [l for l in lineas if fondo - 2 <= l["y0"] <= fondo + 30]
    if bajo and 12 <= bajo[0]["size"] < .8 * s and abs(bajo[0]["x0"] - bloque[0]["x0"]) < 12 \
            and all(abs(l["y0"] - bajo[0]["y0"]) > 6 for l in bajo[1:]):
        fondo = bajo[0]["y1"]
    return bloque, fondo + 6


def _pie(lineas):
    """y donde acaba el cuerpo: lo que queda por debajo de 672 px, o un texto pequeño de fuente, confidencialidad o número."""
    candidatas = [l["y0"] for l in lineas if l["y0"] >= 672 or (l["y0"] >= 640 and l["size"] <= 11.5 and
                  re.search(r"confiden|fuente|source|©|^\s*\d+\s*(/\s*\d+)?\s*$", l["txt"], re.I))]
    return min(min(candidatas) - 6, 690.0) if candidatas else 690.0


def _tipo(n, lineas, palabras):
    t = " ".join(l["txt"] for l in lineas).lower()
    if n == 0:
        return "portada"
    if re.search(r"\bgracias\b|thank you|let.s beat", t) and palabras < 90:
        return "cierre"
    if re.search(r"\bagenda\b|estructura del documento", t) and palabras < 120:
        return "agenda"
    return "portadilla" if palabras <= 25 else "contenido"


def _solapes(lineas):
    """Pares de líneas de texto que se pisan, y líneas que se salen de la slide. La caja se recorta en alto, porque
    incluye el interlineado; dos líneas que solo se rozan no cuentan."""
    cajas = []
    for l in lineas:
        h = (l["y1"] - l["y0"]) * .2
        cajas.append((l["x0"], l["y0"] + h, l["x1"], l["y1"] - h, l["txt"]))
    pares = []
    for i, a in enumerate(cajas):
        for b in cajas[i + 1:]:
            ix, iy = min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1])
            if ix > 0 and iy > 0 and a[4] != b[4]:
                menor = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])) or 1
                if ix * iy / menor > .08:
                    pares.append((a[4][:40], b[4][:40]))
    fuera = [l["txt"][:40] for l in lineas if l["x1"] > W + 2 or l["y1"] > H + 2 or l["x0"] < -2]
    return pares, fuera


def _mayor_rectangulo(vacio):
    """Área (en celdas) del mayor rectángulo de celdas vacías."""
    alto = np.zeros(vacio.shape[1], dtype=int)
    mejor = 0
    for fila in vacio:
        alto = (alto + 1) * fila
        pila = []
        for i, h in enumerate(list(alto) + [0]):
            ini = i
            while pila and pila[-1][1] >= h:
                ini, hp = pila.pop()
                mejor = max(mejor, hp * (i - ini))
            pila.append((ini, h))
    return int(mejor)


def _tinta(pag, top, bot):
    """Cuadrícula del cuerpo: máscara de ocupación (se distingue del fondo, incluye tarjetas claras) y de tinta (contraste fuerte)."""
    pm = pag.get_pixmap(matrix=fitz.Matrix(.25 * W / pag.rect.width, .25 * W / pag.rect.width), alpha=False)
    img = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.h, pm.w, 3).astype(int)
    y0, y1, x0, x1 = int(top / 4), max(int(bot / 4), int(top / 4) + 8), int(X0 / 4), int(X1 / 4)
    z = img[y0:y1, x0:x1]
    claves, cuentas = np.unique((img // 8).reshape(-1, 3), axis=0, return_counts=True)
    fondo = claves[cuentas.argmax()] * 8 + 4
    dif = np.abs(z - fondo).max(axis=2)
    ocup, fuerte = dif > 14, dif > 70
    c = CELDA // 4
    filas, cols = ocup.shape[0] // c, ocup.shape[1] // c
    if not filas or not cols:
        return None, 0.0
    cel = np.array([[ocup[i * c:(i + 1) * c, j * c:(j + 1) * c].mean() > .04 for j in range(cols)] for i in range(filas)])
    return cel, float(fuerte.mean())


def _pag(pag, n):
    esc = W / pag.rect.width
    lineas = _lineas(pag, esc)
    palabras_tot = sum(len(l["txt"].split()) for l in lineas)
    r = dict(n=n + 1, tipo=_tipo(n, lineas, palabras_tot))
    if r["tipo"] != "contenido":
        return r
    pares, fuera = _solapes(lineas)
    r.update(solapes=len(pares), fuera=len(fuera), _solapes=pares[:4] + [("fuera de la slide", t) for t in fuera[:2]])
    tit, top = _cabecera(lineas)
    bot = _pie(lineas)
    cuerpo = [l for l in lineas if l["y0"] >= top - 2 and l["y1"] <= bot + 6]
    cel, tinta = _tinta(pag, top, bot)
    if cel is None:
        r["tipo"] = "portadilla"
        return r
    tam = {}
    for l in cuerpo:
        for c, s in l["spans"]:
            k = round(s * 2) / 2
            tam[k] = tam.get(k, 0) + c
    total = sum(tam.values()) or 1
    orden = sorted(tam.items())
    acum, letra_min = 0, orden[0][0] if orden else 0
    for k, c in orden:                                      # el 5 % de caracteres más pequeños no cuenta: notas al pie
        acum += c
        if acum >= .05 * total:
            letra_min = k
            break
    filas = cel.any(axis=1)
    cols = cel.any(axis=0)
    izq, der = cel[:, :cel.shape[1] // 2].sum(), cel[:, cel.shape[1] // 2:].sum()
    ini = int(filas.argmax()) if filas.any() else len(filas)
    fin = int(filas[::-1].argmax()) if filas.any() else len(filas)
    r.update(
        palabras=sum(len(l["txt"].split()) for l in cuerpo),
        datos=sum(len(re.findall(r"\S*\d\S*", l["txt"])) for l in cuerpo),
        ocupacion=round(100 * float(cel.mean()), 1),
        tinta=round(100 * tinta, 1),
        hueco_abajo=round(100 * fin / len(filas), 1),
        hueco_arriba=round(100 * ini / len(filas), 1),
        hueco_lados=round(100 * ((int(cols.argmax()) if cols.any() else 0) + (int(cols[::-1].argmax()) if cols.any() else 0)) / len(cols), 1),
        mayor_hueco=round(100 * _mayor_rectangulo(~cel) / cel.size, 1),
        desequilibrio=round(100 * abs(int(izq) - int(der)) / max(int(izq) + int(der), 1), 1),
        inicio_y=round(top + ini * CELDA), fin_y=round(top + (len(filas) - fin) * CELDA),
        cuerpo=max(tam, key=tam.get) if tam else 0,
        letra_min=letra_min,
        bajo_11=round(100 * sum(c for k, c in tam.items() if k < 11) / total, 1),
        n_tamanos=sum(1 for c in tam.values() if c / total >= .03),
        titulo=round(max((l["size"] for l in tit), default=0), 1),
        titulo_lineas=len(tit),
        titulo_palabras=sum(len(l["txt"].split()) for l in tit),
        titulo_x=round(tit[0]["x0"], 0) if tit else None,
        _huella=cel,
    )
    return r


def _iou(a, b):
    f, c = min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1])
    # se alinean por abajo: slides con títulos de 1 o 2 líneas tienen el cuerpo desplazado una fila
    x, y = a[-f:, :c], b[-f:, :c]
    u = (x | y).sum()
    return float((x & y).sum() / u) if u else 0.0


def _cv(v):
    return round(100 * st.pstdev(v) / st.mean(v), 1) if len(v) > 1 and st.mean(v) else 0.0


def _hermanas(cont, umbral=.62):
    """Grupos de 2 o más slides de contenido consecutivas con una huella parecida (mismo esqueleto)."""
    grupos, act = [], []
    for a, b in zip(cont, cont[1:] + [None]):
        act.append(a)
        if b is None or b["n"] != a["n"] + 1 or _iou(a["_huella"], b["_huella"]) < umbral:
            if len(act) >= 2:
                grupos.append(act)
            act = []
    return [dict(paginas=[p["n"] for p in g], cv_palabras=_cv([p["palabras"] for p in g]),
                 rango_ocupacion=round(max(p["ocupacion"] for p in g) - min(p["ocupacion"] for p in g), 1),
                 rango_cuerpo=max(p["cuerpo"] for p in g) - min(p["cuerpo"] for p in g)) for g in grupos]


def medir(ruta):
    """Devuelve dict(deck, paginas, conjunto, hermanas). Las páginas que no son de contenido solo llevan su tipo."""
    d = fitz.open(str(ruta))
    pags = [_pag(p, i) for i, p in enumerate(d)]
    cont = [p for p in pags if p["tipo"] == "contenido"]
    herm = _hermanas(cont) if cont else []
    conj = {}
    if cont:
        cuerpos, titulos = {}, {}
        for p in cont:
            cuerpos[p["cuerpo"]] = cuerpos.get(p["cuerpo"], 0) + 1
            titulos[round(p["titulo"])] = titulos.get(round(p["titulo"]), 0) + 1
        xs = [p["titulo_x"] for p in cont if p["titulo_x"] is not None]
        conj = dict(slides=len(pags), contenido=len(cont), palabras_mediana=st.median(p["palabras"] for p in cont),
                    ocupacion_mediana=st.median(p["ocupacion"] for p in cont),
                    cuerpo_mediana=st.median(p["cuerpo"] for p in cont), hueco_mediano=st.median(p["mayor_hueco"] for p in cont),
                    cv_palabras=_cv([p["palabras"] for p in cont]), cv_datos=_cv([p["datos"] for p in cont]), cv_ocupacion=_cv([p["ocupacion"] for p in cont]),
                    desv_inicio=round(st.pstdev(p["inicio_y"] for p in cont), 1), desv_fin=round(st.pstdev(p["fin_y"] for p in cont), 1),
                    salto_ocupacion=round(st.mean(abs(a["ocupacion"] - b["ocupacion"]) for a, b in zip(cont, cont[1:])), 1) if len(cont) > 1 else 0,
                    n_cuerpos=sum(1 for c in cuerpos.values() if c / len(cont) >= .1),
                    n_titulos=sum(1 for c in titulos.values() if c / len(cont) >= .1),
                    desv_titulo_x=round(st.pstdev(xs), 1) if len(xs) > 1 else 0, sin_titulo=len(cont) - len(xs))
    for p in cont:
        del p["_huella"]
    return dict(deck=pathlib.Path(ruta).name, paginas=pags, conjunto=conj, hermanas=herm)


def calibrar(rutas=None, medidos=None):
    """Rangos de referencia: percentiles 5, 50 y 95 por slide, por deck y por grupo de hermanas. Solo cifras agregadas:
    ni nombres de cliente ni texto de los decks."""
    res = medidos if medidos is not None else [medir(r) for r in rutas]
    cont = [p for r in res for p in r["paginas"] if p["tipo"] == "contenido"]
    pct = lambda v: dict(p5=round(float(np.percentile(v, 5)), 1), p50=round(float(np.percentile(v, 50)), 1), p95=round(float(np.percentile(v, 95)), 1))
    grupos = [g for r in res for g in r["hermanas"]]
    return dict(decks=len(res), slides_contenido=len(cont),
                slide={m: pct([p[m] for p in cont]) for m in METRICAS},
                deck={m: pct([r["conjunto"][m] for r in res]) for m in METRICAS_DECK},
                hermanas={m: pct([g[m] for g in grupos]) for m in METRICAS_GRUPO} if grupos else {}, grupos_hermanas=len(grupos))


def marcas(pag, cal):
    """Marcas de una slide: textos que se pisan o se salen (sin calibrar: uno ya se mira) y lo que se sale de los rangos.
    Devuelve [(dimensión, nombre, valor, límite)]."""
    out = []
    if pag["solapes"]:
        out.append(("Errores", "Textos que se pisan", pag["solapes"], 0))
    if pag["fuera"]:
        out.append(("Errores", "Texto fuera de la slide", pag["fuera"], 0))
    for m, (dim, lado, nombre, tol) in METRICAS.items():
        r = cal["slide"][m]
        if lado == "alto" and pag[m] > r["p95"] + tol:
            out.append((dim, nombre, pag[m], round(r["p95"] + tol, 1)))
        if lado == "bajo" and pag[m] < r["p5"] - tol:
            out.append((dim, nombre, pag[m], round(r["p5"] - tol, 1)))
    return out


def resumen_marcas(r, cal):
    """% de slides de contenido con marca, en total y por dimensión."""
    cont = [p for p in r["paginas"] if p["tipo"] == "contenido"]
    ms = [marcas(p, cal) for p in cont]
    n = len(cont) or 1
    return dict(total=round(100 * sum(bool(m) for m in ms) / n), **{d: round(100 * sum(any(x[0] == d for x in m) for m in ms) / n) for d in DIMENSIONES})


def informe(r, cal=None):
    """Informe en markdown de un deck medido, con marcas si hay calibración."""
    if cal is None and CALIB.exists():
        cal = json.loads(CALIB.read_text(encoding="utf-8"))
    c = r["conjunto"]
    o = [f"# Medición de {r['deck']}", ""]
    if not c:
        return "\n".join(o + ["Sin slides de contenido."])
    o += [f"{c['slides']} páginas, {c['contenido']} de contenido. Medianas: {c['palabras_mediana']:.0f} palabras, {c['ocupacion_mediana']:.0f} % de ocupación, cuerpo de {c['cuerpo_mediana']} px.", ""]
    if cal:
        rs = resumen_marcas(r, cal)
        o += [f"**Slides con alguna marca: {rs['total']} %** (" + ", ".join(f"{d.lower()} {rs[d]} %" for d in DIMENSIONES) + ").", ""]
    o += ["## Conjunto del deck", "", "| Medida | Valor | Referencia (p50 · máx. habitual) |", "|---|---|---|"]
    for m, nombre in METRICAS_DECK.items():
        ref = f"{cal['deck'][m]['p50']} · {cal['deck'][m]['p95']}" if cal else ""
        o.append(f"| {nombre} | {c[m]}{' ⚠' if cal and c[m] > cal['deck'][m]['p95'] else ''} | {ref} |")
    if c.get("sin_titulo"):
        o.append(f"| Slides sin título detectado | {c['sin_titulo']} | 0 |")
    o += ["", "## Slide a slide", "", "| Pág. | Palabras | Datos | Ocup. % | Mayor hueco % | Empieza y acaba (px) | Cuerpo | Mín. | Marcas |", "|---|---|---|---|---|---|---|---|---|"]
    for p in r["paginas"]:
        if p["tipo"] != "contenido":
            o.append(f"| {p['n']} | {p['tipo']} | | | | | | | |")
            continue
        ms = marcas(p, cal) if cal else []
        o.append(f"| {p['n']} | {p['palabras']} | {p['datos']} | {p['ocupacion']} | {p['mayor_hueco']} | {p['inicio_y']} a {p['fin_y']} | {p['cuerpo']} | {p['letra_min']} | "
                 + ", ".join(f"{n} {v} (ref. {l})" for _, n, v, l in ms) + " |")
    if r["hermanas"]:
        o += ["", "## Slides hermanas", "", "| Páginas | Dispersión de palabras (CV, %) | Rango de ocupación (puntos) | Rango de cuerpo (px) |", "|---|---|---|---|"]
        for g in r["hermanas"]:
            av = lambda m: " ⚠" if cal and cal.get("hermanas") and g[m] > cal["hermanas"][m]["p95"] else ""
            o.append(f"| {g['paginas'][0]} a {g['paginas'][-1]} | {g['cv_palabras']}{av('cv_palabras')} | {g['rango_ocupacion']}{av('rango_ocupacion')} | {g['rango_cuerpo']}{av('rango_cuerpo')} |")
    # cifras en formato español, salvo la primera línea, que lleva el nombre del archivo
    return o[0] + "\n" + re.sub(r"(?<=\d)\.(?=\d)", ",", "\n".join(o[1:])) + "\n"


def validar(rutas, contraste=None):
    """Validación dejando uno fuera: cada referencia se marca con los rangos de las demás, para no aprobarla consigo misma.
    Un contraste (un deck que no convenció) se marca con los rangos de todas. Devuelve [(deck, resumen, cv_ocupación)]."""
    res = [medir(r) for r in rutas]
    filas = []
    for i, r in enumerate(res):
        filas.append((r["deck"], resumen_marcas(r, calibrar(medidos=res[:i] + res[i + 1:])), r["conjunto"]))
    if contraste:
        r = medir(contraste)
        filas.append((r["deck"], resumen_marcas(r, calibrar(medidos=res)), r["conjunto"]))
    return filas


def _lista(ruta):
    raiz = AQUI.parents[2]
    lineas = [x.strip() for x in pathlib.Path(ruta).read_text(encoding="utf-8").splitlines()]
    return [raiz / x for x in lineas if x and not x.startswith("#")]


def main(a):
    if "--calibrar" in a:
        cal = calibrar(_lista(a[a.index("--calibrar") + 1]))
        CALIB.write_text(json.dumps(cal, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Calibrado con {cal['decks']} decks y {cal['slides_contenido']} slides de contenido: {CALIB.name}")
        return 0
    if "--validar" in a:
        i = a.index("--validar")
        for deck, rs, c in validar(_lista(a[i + 1]), a[i + 2] if len(a) > i + 2 else None):
            print(f"{deck[:44]:44} marcadas {rs['total']:3} % · llenado {rs['Llenado']:3} · densidad {rs['Densidad']:3} · legibilidad {rs['Legibilidad']:3} · equilibrio {rs['Equilibrio']:3}"
                  f" · CV ocup. {c['cv_ocupacion']:5} · desv. inicio {c['desv_inicio']:5}")
        return 0
    if not a or a[0].startswith("-"):
        print(__doc__)
        return 2
    r = medir(a[0])
    txt = informe(r)
    if "--md" in a:
        pathlib.Path(a[a.index("--md") + 1]).write_text(txt, encoding="utf-8")
    if "--json" in a:
        pathlib.Path(a[a.index("--json") + 1]).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
