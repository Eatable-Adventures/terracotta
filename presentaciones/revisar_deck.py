#!/usr/bin/env python3
"""revisar_deck: la revisión objetiva de un deck, en un comando y un informe. Renderiza a PDF y PNG, comprueba las páginas,
inspecciona el HTML (qué elemento falla: inspeccionar_dom) y mide el PDF frente a los decks de referencia (medir_deck).

Dos medidores porque ven cosas distintas: el HTML dice qué elemento falla, colores, títulos y formatos; el PDF dice cómo queda
de verdad y lo compara con los rangos. Nada de esto sustituye a mirar cada PNG: un aviso se confirma o se descarta.

Uso:
    python3 revisar_deck.py deck.html [--out DIR] [--paginas 3,5-7] [--sin-png]
    python3 revisar_deck.py deck.pdf  [--out DIR]     (sin HTML: solo medición y PNG, para decks hechos a mano)

Deja en DIR (por defecto, <carpeta del deck>/_revision/<nombre>/; mejor un scratchpad): el PDF, p01.png..., mapa.txt e informe.md.
Código de salida: 0 sin errores, 1 con errores, 2 si las páginas no cuadran.
"""
import argparse, html, json, pathlib, re, subprocess, sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import inspeccionar_dom as I    # noqa: E402
import medir_deck as M          # noqa: E402

CHROME = I.CHROME


def _limpiar(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def titulos(txt):
    """Título visible de cada <section class="slide..."> en orden de documento."""
    out = []
    for sec in re.split(r'(?=<section class="slide)', txt)[1:]:
        cab = re.match(r'<section class="([^"]*)"', sec).group(1)
        if "cover" in cab:
            m = re.search(r'class="cv-title"[^>]*>(.*?)</div>', sec, re.S)
            out.append("Portada · " + _limpiar(m.group(1) if m else ""))
        elif "closing" in cab:
            out.append("Cierre")
        else:
            m = (re.search(r"<h2[^>]*>(.*?)</h2>", sec, re.S) or re.search(r"<h1[^>]*>(.*?)</h1>", sec, re.S)
                 or re.search(r'<div class="(?:title|slide-title|titulo)"[^>]*>(.*?)</div>', sec, re.S))
            out.append(_limpiar(m.group(1)) if m else "(sin título)")
    return out


def exportar(deck, out):
    """HTML a PDF con Chrome headless."""
    pdf = out / f"{deck.stem}.pdf"
    r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", f"--print-to-pdf={pdf}",
                        "--print-to-pdf-no-header-footer", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                        "--run-all-compositor-stages-before-draw", deck.as_uri()], capture_output=True, text=True, timeout=240)
    if not pdf.exists():
        raise RuntimeError("Fallo al generar el PDF:\n" + r.stderr[-2000:])
    return pdf


def pngs(pdf, out, paginas=None):
    import fitz
    doc = fitz.open(str(pdf))
    for n, pg in enumerate(doc, 1):
        if paginas is None or n in paginas:
            pg.get_pixmap(matrix=fitz.Matrix(1280 / pg.rect.width, 1280 / pg.rect.width)).save(str(out / f"p{n:02d}.png"))


def revisar(ruta, out=None, paginas=None, png=True):
    """Devuelve {"informe": md, "errores": n, "avisos": n, "marcadas": %, "paginas_ok": bool, "n_pdf": n, "n_html": n, "dir": ruta}."""
    deck = pathlib.Path(ruta).resolve()
    out = pathlib.Path(out).resolve() if out else deck.parent / "_revision" / deck.stem
    out.mkdir(parents=True, exist_ok=True)
    es_html = deck.suffix.lower() in (".html", ".htm")
    pdf = exportar(deck, out) if es_html else deck
    import pypdf
    n_pdf = len(pypdf.PdfReader(str(pdf)).pages)
    tit = titulos(deck.read_text(encoding="utf-8")) if es_html else []
    n_html = len(tit) if es_html else n_pdf
    if tit:
        (out / "mapa.txt").write_text("".join(f"p. {i:>2} · {t[:110]}\n" for i, t in enumerate(tit, 1)), encoding="utf-8")
    if png:
        pngs(pdf, out, paginas)

    cal = json.loads(M.CALIB.read_text(encoding="utf-8"))
    med = M.medir(pdf)
    (out / "medicion.md").write_text(M.informe(med, cal), encoding="utf-8")
    res = I.inspeccionar(deck) if es_html else {"slides": [], "deck": []}
    insp = {s["n"]: s for s in res["slides"]}

    errores = avisos = 0
    cuerpo = []
    for p in med["paginas"]:
        n = p["n"]
        if paginas is not None and n not in paginas:
            continue
        hs = insp.get(n, {}).get("hallazgos", [])
        lineas = [f"- {'**Error**' if h['nivel'] == 'error' else 'Mirar' if h['nivel'] == 'info' else 'Aviso'} [{h['tipo']}] {h['msg']}" for h in hs]
        errores += sum(h["nivel"] == "error" for h in hs)
        avisos += sum(h["nivel"] == "aviso" for h in hs)
        marcas = M.marcas(p, cal) if p["tipo"] == "contenido" else []
        for dim, nombre, val, lim in marcas:
            ya = (dim == "Errores" and any(h["tipo"] in ("solape", "fuera") for h in hs)) or (dim == "Legibilidad" and any(h["tipo"] == "letra" for h in hs) and "mín" in nombre.lower())
            if ya:
                continue
            if dim == "Errores":
                errores += 1
            else:
                avisos += 1
            lineas.append(f"- {'**Error**' if dim == 'Errores' else 'Aviso'} [PDF, {dim.lower()}] {nombre}: {val} (límite {lim})")
        if lineas:
            nombre = insp.get(n, {}).get("titulo") or (tit[n - 1] if n <= len(tit) else "")
            cuerpo += [f"### p. {n} · {nombre[:90]}".rstrip(" ·"), *lineas, ""]
    rs = M.resumen_marcas(med, cal)
    ok = n_pdf == n_html
    o = [f"# Revisión de {deck.name}", "",
         f"- **Páginas:** {n_pdf} en el PDF" + (f", {n_html} slides en el HTML" if es_html else "") + (" · cuadran" if ok else " · **NO CUADRAN** (causa habitual: @page con margen o una slide más alta que 720 px)"),
         f"- **Errores:** {errores} · **Avisos:** {avisos}",
         f"- **Frente a los decks de referencia:** {rs['total']} % de slides fuera de rango (llenado {rs['Llenado']} %, densidad {rs['Densidad']} %, legibilidad {rs['Legibilidad']} %, equilibrio {rs['Equilibrio']} %). Detalle: medicion.md"]
    if not es_html:
        o.append("- **Sin HTML:** solo se ha medido el PDF.")
    for h in res["deck"]:
        o.append(f"- Deck [{h['tipo']}] {h['msg']}")
    o += ["", "Cada aviso se confirma en el PNG. Para comparar la forma con una slide modelo: `python3 referencias.py <tipo> --png <carpeta>`.", ""] + (cuerpo or ["Sin hallazgos medibles."])
    md = "\n".join(o) + "\n"
    (out / "informe.md").write_text(md, encoding="utf-8")
    return dict(informe=md, errores=errores, avisos=avisos, marcadas=rs["total"], paginas_ok=ok, n_pdf=n_pdf, n_html=n_html, dir=out, tipos=res)


def _rango(txt):
    if not txt:
        return None
    s = set()
    for p in txt.split(","):
        a, _, b = p.strip().partition("-")
        s.update(range(int(a), int(b or a) + 1))
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--out")
    ap.add_argument("--paginas", help="p. ej. 3,5-7")
    ap.add_argument("--sin-png", action="store_true")
    a = ap.parse_args()
    r = revisar(a.deck, a.out, _rango(a.paginas), not a.sin_png)
    print(r["informe"])
    print(f"Archivos en {r['dir']}")
    return 2 if not r["paginas_ok"] else 1 if r["errores"] else 0


if __name__ == "__main__":
    sys.exit(main())
