#!/usr/bin/env python3
"""referencias: une las referencias de Terracotta con el código (índice en «Referencias de Terracotta.md»).

Hay dos tipos que se pueden comprobar:
  - decks y slides de referencia de EA, en las tablas de «Referencias de Terracotta.md»: fijan la densidad y dejan ver
    cómo se resolvió un tipo de slide. Se miran por su forma: su contenido es de un cliente y no se reutiliza.
  - patrones externos fichados (catalogo/R01 a R16): cada ficha dice en «elementos» qué piezas salieron de ella.

Uso:
    python3 referencias.py                     (lista los tipos de slide con referencia)
    python3 referencias.py ficha --png DIR     (deja en DIR, fuera del vault, las slides de ese tipo en PNG para mirarlas)
    python3 referencias.py --comprobar         (lo mismo que hace verificar.py)

Las referencias citan clientes y solo están en el entorno interno: fuera de él (en un clon del repositorio público) no hay slides modelo
y estas funciones devuelven listas vacías, sin error.
"""
import json, pathlib, re, sys

import yaml

AQUI = pathlib.Path(__file__).resolve().parent
BRAIN = AQUI.parents[2] if len(AQUI.parents) > 2 else AQUI
NOTA = AQUI / "Referencias de Terracotta.md"
CATALOGO = AQUI / "catalogo"
LISTA = AQUI / "referencia" / "decks_calibracion.txt"
TERMINOS = AQUI / "referencia" / "terminos_confidenciales.txt"
EN_EL_BRAIN = NOTA.exists() and LISTA.exists()


def fichas():
    """Las fichas del catálogo: [{ref, titulo, estado, elementos, ruta}]."""
    out = []
    for p in sorted(CATALOGO.glob("R[0-9][0-9] · *.md")):
        y = yaml.safe_load(re.match(r"---\n(.*?)\n---", p.read_text(encoding="utf-8"), re.S).group(1))
        out.append(dict(ref=p.name[:3], titulo=p.stem.split(" · ", 1)[1], estado=y.get("estado", ""), elementos=y.get("elementos") or [], ruta=p))
    return out


def origenes():
    """{pieza o variante de la galería: referencia de la que sale}."""
    return {e: f["ref"] for f in fichas() for e in f["elementos"]}


def _filas(seccion):
    """Filas de la tabla bajo un encabezado «## sección» de la nota, sin cabecera ni separador."""
    if not NOTA.exists():
        return []
    t = NOTA.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(seccion)}\n(.*?)(?=^## |\Z)", t, re.S | re.M)
    if not m:
        raise SystemExit(f"Falta la sección «{seccion}» en {NOTA.name}")
    filas = [[c.strip() for c in re.split(r"(?<!\\)\|", l.strip())[1:-1]] for l in m.group(1).splitlines() if l.startswith("|")]
    return filas[2:]


def decks():
    """{clave: ruta relativa a la raíz del entorno interno}."""
    return {f[0]: f[2].strip("`") for f in _filas("Decks de referencia")}


def slides(palabra=None):
    """[{tipo, nombre, deck, pagina, mirar, piezas}], filtradas por una palabra del tipo si se da."""
    out = []
    for f in _filas("Slides de referencia por tipo"):
        d = dict(tipo=f[0].strip("`"), nombre=f[1], deck=f[2], pagina=int(f[3]), mirar=f[4], piezas=re.findall(r"`([^`]+)`", f[5]))
        if not palabra or palabra.lower() in f"{d['tipo']} {d['nombre']}".lower():
            out.append(d)
    return out


def comprobar(X):
    """Errores de coherencia entre referencias y código. Vacío si todo cuadra. Mide los decks citados, tarda unos segundos."""
    import build_galeria_elementos as G, medir_deck
    err = []
    lista = [l.strip() for l in LISTA.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    cal = json.loads(medir_deck.CALIB.read_text(encoding="utf-8"))
    if cal["decks"] != len(lista):
        err.append(f"calibracion_decks.json usa {cal['decks']} decks y la lista tiene {len(lista)}: recalibrar")
    tabla = decks()
    for k, r in tabla.items():
        if r not in lista:
            err.append(f"Deck {k} no está en la lista de calibración: {r}")
    for r in lista:
        if not (BRAIN / r).exists():
            err.append(f"No existe el deck de referencia: {r}")
        if r not in tabla.values():
            err.append(f"Deck de calibración sin clave en la nota: {r}")
    medidos = {}
    for s in slides():
        if s["deck"] not in tabla or not (BRAIN / tabla[s["deck"]]).exists():
            err.append(f"Slide de referencia con deck desconocido: {s['deck']} p. {s['pagina']}")
            continue
        m = medidos.setdefault(s["deck"], medir_deck.medir(BRAIN / tabla[s["deck"]]))
        pags = {p["n"]: p for p in m["paginas"]}
        p = pags.get(s["pagina"])
        if not p or p["tipo"] != "contenido":
            err.append(f"{s['deck']} p. {s['pagina']} no es una slide de contenido")
        elif medir_deck.marcas(p, cal):
            err.append(f"{s['deck']} p. {s['pagina']} se sale de los rangos: no sirve de referencia")
        err += [f"Pieza inexistente en {s['tipo']}: {n}" for n in s["piezas"] if not hasattr(X, n)]
    conocidas = set(G.BASE) | set(X.FICHAS)
    for f in fichas():
        err += [f"{f['ref']} cita una pieza que no existe: {e}" for e in f["elementos"] if e not in conocidas]
        if not f["estado"]:
            err.append(f"{f['ref']} no tiene estado")
        for img in re.findall(r"!\[\[(.*?)\]\]", f["ruta"].read_text(encoding="utf-8")):
            if not (CATALOGO / img).exists():
                err.append(f"{f['ref']}: falta la captura {img}")
    return err


def comprobar_reglas(X, skill=None):
    """Que lo que citan formatos, microajustes, ejemplos y skill exista: códigos de regla vigentes, piezas y tipos de slide modelo."""
    reglas = (AQUI / "Reglas de uso de elementos.md").read_text(encoding="utf-8")
    cuerpo, _, tabla = reglas.partition("## Códigos retirados")
    vigentes = set(re.findall(r"^(?:- )?\*\*([A-GSMKINQ]\d+) · ", cuerpo, re.M))
    retirados = set(re.findall(r"^\| ([A-GSMKINQ]\d+) \|", tabla, re.M))
    err = []
    if vigentes & retirados:
        err.append(f"Códigos a la vez vigentes y retirados: {sorted(vigentes & retirados)}")
    textos = {n: (AQUI / n).read_text(encoding="utf-8") for n in ("Formatos de slide.md", "Microajustes.md")}
    textos["Reglas de uso de elementos.md"] = cuerpo
    if skill and pathlib.Path(skill).exists():
        textos["skill terracotta"] = pathlib.Path(skill).read_text(encoding="utf-8")
    for nombre, t in textos.items():
        for c in sorted(set(re.findall(r"\b([A-GSMKINQ]\d{1,2})\b", t)) - vigentes):
            err.append(f"{nombre} cita {c}, que {'está retirado' if c in retirados else 'no existe'}")
    ej = (AQUI / "build_reglas_uso.py").read_text(encoding="utf-8")
    for c in sorted(set(re.findall(r'"([A-GSMKINQ]\d{1,2})"', ej)) - vigentes):
        err.append(f"build_reglas_uso.py cita {c}, que no está vigente")
    formatos = textos["Formatos de slide.md"]
    tipos = {s["tipo"] for s in slides()}
    err += [f"Formatos de slide cita una pieza que no existe: {n}" for n in sorted(set(re.findall(r"X\.([a-z_]+)\b", formatos))) if not hasattr(X, n) and not n.endswith("_")]
    if EN_EL_BRAIN:
        err += [f"Formatos de slide cita un modelo que no existe: {t}" for t in sorted(set(re.findall(r"Modelo: `([a-z]+)`", formatos))) if t not in tipos]
    return err


def comprobar_confidencial(skill=None, palabras=5):
    """Que reglas, formatos, microajustes, ejemplos y código sean generales: sin términos de la lista y sin frases de 5 o más
    palabras seguidas iguales a las de un deck de referencia en los textos de los ejemplos. Es una red, no una garantía: las cifras
    copiadas no se detectan, y por eso los ejemplos se inventan desde cero."""
    if not TERMINOS.exists():
        return []
    import fitz
    terminos = [l.strip() for l in TERMINOS.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    limpios = ["Reglas de uso de elementos.md", "Formatos de slide.md", "Microajustes.md", "README.md", "Taxonomía de elementos.md", "Catálogo de iconos.md",
               "Galería de elementos.html", "Reglas de uso de elementos.html"]
    nucleo = AQUI.parent
    rutas = [AQUI / n for n in limpios] + sorted(AQUI.glob("*.py")) + sorted((AQUI / "ea_elementos").glob("*.py"))
    rutas += [nucleo / n for n in ("README.md", "DESIGN.md", "SKILL.md", "Charts Catalogue.html", "Maps Catalogue.html")]
    rutas += sorted((nucleo / "preview").glob("chart-*.html")) + sorted((nucleo / "preview").glob("map-*.html"))
    if skill and pathlib.Path(skill).exists():
        rutas.append(pathlib.Path(skill))
    err = []
    for r in rutas:
        t = re.sub(r"base64,[A-Za-z0-9+/=]+", "", r.read_text(encoding="utf-8"))
        err += [f"{r.name} cita «{w}»" for w in terminos if re.search(rf"(?<![\w-]){re.escape(w)}(?![\w-])", t)]
    norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\wáéíóúñü%]+", " ", s.lower())).strip()
    decks_txt = [norm(" ".join(p.get_text() for p in fitz.open(str(BRAIN / d)))) for d in decks().values() if (BRAIN / d).exists()]
    for n in ("build_galeria_elementos.py", "build_reglas_uso.py"):
        for c in re.findall(r'"((?:[^"\\\n]|\\.){10,400})"', (AQUI / n).read_text(encoding="utf-8")):
            w = norm(re.sub(r"\*\*|<[^>]+>", "", c)).split()
            if any(" ".join(w[i:i + palabras]) in t for i in range(len(w) - palabras + 1) for t in decks_txt):
                err.append(f"{n}: texto igual al de un deck de referencia: «{c[:60]}»")
    return err


def png(palabra, carpeta):
    import fitz
    d = pathlib.Path(carpeta).expanduser()
    if d.resolve().is_relative_to(BRAIN):
        raise SystemExit("Las capturas de decks de cliente no se guardan en el vault: usa el scratchpad.")
    d.mkdir(parents=True, exist_ok=True)
    tabla = decks()
    for s in slides(palabra):
        doc = fitz.open(str(BRAIN / tabla[s["deck"]]))
        pag = doc[s["pagina"] - 1]
        ruta = d / f"{s['tipo']}_{s['deck']}_p{s['pagina']}.png"
        pag.get_pixmap(matrix=fitz.Matrix(1280 / pag.rect.width, 1280 / pag.rect.width)).save(str(ruta))
        print(ruta, "·", s["mirar"])


def main(a):
    if "--comprobar" in a:
        import ea_elementos as X
        sk = pathlib.Path.home() / ".claude/skills/terracotta/SKILL.md"
        err = comprobar(X) + comprobar_reglas(X, sk) + comprobar_confidencial(sk)
        print("\n".join(err) or f"Referencias coherentes: {len(decks())} decks, {len(slides())} slides, {len(fichas())} fichas.")
        return 1 if err else 0
    if not EN_EL_BRAIN:
        print("Las slides modelo citan clientes y solo están en el entorno interno de EA: aquí no hay referencias que enseñar. Guíate por «Formatos de slide.md».")
        return 0
    palabra = a[0] if a and not a[0].startswith("--") else None
    if "--png" in a:
        png(palabra, a[a.index("--png") + 1])
        return 0
    for s in slides(palabra):
        print(f"{s['tipo']:<14} {s['deck']} p. {s['pagina']:<3} {s['nombre']} · {s['mirar']} · piezas: {', '.join(s['piezas'])}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(AQUI))
    sys.exit(main(sys.argv[1:]))
