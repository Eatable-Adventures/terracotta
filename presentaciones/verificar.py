#!/usr/bin/env python3
"""Verificación de Terracotta V2 (capa de presentaciones): se ejecuta después de cualquier cambio en ea_deck o
ea_elementos y antes de dar por buena una versión.

Comprueba, en orden:
  1. Que el paquete importa y que código y taxonomía cuadran (taxonomia.comprobar).
  2. Que la galería, la taxonomía y el catálogo de iconos se regeneran (build_galeria_elementos.py).
  3. Que las slides de ejemplo de las reglas de uso salen en PDF con el número de páginas esperado.
  4. Una prueba de humo de la base fija (portada, agenda, portadilla, slide con elementos y cierre) en PDF.
  5. Que medir_deck funciona: la calibración carga y mide las reglas de uso sin slides sin título. No exige que no haya marcas.
  6. Que las referencias cuadran: decks y páginas citados, dentro de los rangos, y piezas que existen (referencias.comprobar).
  7. Que las reglas cuadran: códigos, piezas y modelos que citan formatos, microajustes, ejemplos y skill (referencias.comprobar_reglas).
  8. Que la revisión funciona: revisar_deck sobre las reglas de uso, con las páginas bien y sin errores.
  9. Que reglas, ejemplos y código no citan clientes ni proyectos, ni copian frases de un deck de referencia (referencias.comprobar_confidencial).
 10. Que la huella anónima funciona (sin texto ni imágenes, y sin confundir los gráficos con logos) y que la clave de slide solo se escribe si viene.
 11. Que el ejemplo del README se ejecuta tal cual y sale en PDF con sus páginas.
 12. Que la búsqueda en lenguaje natural responde y que el laboratorio de variantes monta sus opciones en PDF.
 15. Que el núcleo se genera desde las piezas (tarjetas e índice) y que las cifras que cita la documentación cuadran.
 14. Que los tokens del núcleo cuadran con el código (rampa y verde) y que charts/funnel.py da lo mismo que embudo_canonico.
 13. Que ninguna tarjeta de la galería tiene textos que se solapan, se salen o quedan cortados (auditar_galeria).

Ejecutar: python3 verificar.py [--png DIR]   (con --png deja la prueba de humo en PNG para mirarla)
"""
import os, pathlib, re, subprocess, sys, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from inspeccionar_dom import CHROME  # noqa: E402  CHROME_PATH o las rutas habituales de macOS, Linux y Windows
FALLOS = []


def paso(nombre, ok, detalle=""):
    print(f"{'OK   ' if ok else 'FALLO'} {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def pdf(html_path, pdf_path):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", f"--print-to-pdf={pdf_path}",
                    "--print-to-pdf-no-header-footer", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    "--run-all-compositor-stages-before-draw", pathlib.Path(html_path).as_uri()], check=True, capture_output=True)
    import pypdf
    return len(pypdf.PdfReader(str(pdf_path)).pages)


def main():
    import ea_deck
    import ea_elementos as X
    paso("Importación", True, f"Terracotta {X.__version__}, {len(X.FICHAS)} elementos, {len(X.iconos.NOMBRES)} iconos")
    try:
        X.taxonomia.comprobar(X)
        paso("Código y taxonomía cuadran", True)
    except Exception as e:  # noqa: BLE001
        paso("Código y taxonomía cuadran", False, str(e)[:200])

    r = subprocess.run([sys.executable, str(AQUI / "build_galeria_elementos.py")], capture_output=True, text=True, cwd=AQUI)
    paso("Galería, taxonomía y catálogo de iconos", r.returncode == 0, (r.stdout.strip().splitlines() or [r.stderr.strip()[-200:]])[-1])

    r = subprocess.run([sys.executable, str(AQUI / "build_nucleo.py")], capture_output=True, text=True, cwd=AQUI)
    import build_nucleo
    tarjetas = [AQUI.parent / "preview" / f"{a}.html" for a, *_ in build_nucleo.GRAFICOS + build_nucleo.MAPAS]
    paso("Núcleo generado desde las piezas", r.returncode == 0 and all("Generada por presentaciones/build_nucleo.py" in t.read_text(encoding="utf-8") for t in tarjetas), (r.stdout.strip().splitlines() or [r.stderr.strip()[-200:]])[-1])
    n = len(X.FICHAS)
    citas = {"README.md": f"{n} elementos", "Formatos de slide.md": f"{n} elementos", "../DESIGN.md": f"{n} visual elements", "../README.md": f"{n} visual elements", "../SKILL.md": f"{n} visual elements"}
    mal = [a for a, t in citas.items() if t not in (AQUI / a).read_text(encoding="utf-8")]
    paso("Cifras de la documentación", not mal, f"no dicen {n} elementos: {mal}" if mal else f"{n} elementos")

    r = subprocess.run([sys.executable, str(AQUI / "build_reglas_uso.py"), "--pdf"], capture_output=True, text=True, cwd=AQUI)
    paso("Reglas de uso en PDF", r.returncode == 0 and "OK" in r.stdout, (r.stdout.strip().splitlines() or [r.stderr.strip()[-200:]])[-1])

    cuerpo = ea_deck.cabecera("01. Prueba", f'Una slide de prueba con <span class="hl-red">{X.__version__}</span>') + X.cuerpo_slide(
        "Datos ficticios", X.fila(X.embudo([("Universo", "", "120"), ("Filtro", "", "40"), ("Final", "", "5")], clave=2),
                                  X.contadores([("5", "Finalistas", "de 120 candidatos")]), anchos=X.REJILLAS["B"]),
        banda="La prueba de humo **pasa** si esta slide se ve entera.")
    paginas = [ea_deck.portada("Prueba de", "Terracotta V2", "Verificación · Base fija", "Uso interno", ["Equipo EA"], "Noviembre 2026"),
               ea_deck.agenda([("Uno", "Primera sección"), ("Dos", "Segunda sección")], "Prueba"),
               ea_deck.portadilla("01", "Prueba", "Sección de prueba", visual_html=X.escena_iso("laboratorio", True, W=520)),
               ea_deck.slide(cuerpo, 4, 5, "Fuente: datos ficticios", "el equipo de EA"),
               ea_deck.cierre("Mensaje de **prueba**.", "el equipo de EA")]
    html_ = ea_deck.documento("Prueba Terracotta V2", paginas, X.CSS + X.fuente_iconos())
    X.comprobar_iconos(html_)
    d = pathlib.Path(tempfile.mkdtemp())
    (d / "prueba.html").write_text(html_, encoding="utf-8")
    n = pdf(d / "prueba.html", d / "prueba.pdf")
    paso("Prueba de humo de la base fija en PDF", n == len(paginas), f"{n} páginas de {len(paginas)}")

    import json, medir_deck
    cal = json.loads(medir_deck.CALIB.read_text(encoding="utf-8"))
    m = medir_deck.medir(AQUI / "Reglas de uso de elementos.pdf")
    rs = medir_deck.resumen_marcas(m, cal)
    paso("Medición de decks", m["conjunto"]["contenido"] > 0 and m["conjunto"]["sin_titulo"] == 0,
         f"{cal['decks']} decks de calibración; reglas de uso con {rs['total']} % de slides marcadas (informativo)")

    import referencias
    if referencias.EN_EL_BRAIN and (referencias.BRAIN / "01. Proyectos").exists():
        err = referencias.comprobar(X)
        paso("Referencias", not err, "; ".join(err)[:300] or f"{len(referencias.decks())} decks, {len(referencias.slides())} slides por tipo, {len(referencias.fichas())} fichas del catálogo")
    else:
        print("OMITIDO Referencias · fuera del entorno interno no están sus decks")
    err = referencias.comprobar_reglas(X, pathlib.Path.home() / ".claude/skills/terracotta/SKILL.md")
    paso("Reglas, formatos y microajustes", not err, "; ".join(err)[:400])

    import revisar_deck
    rv = revisar_deck.revisar(AQUI / "Reglas de uso de elementos.html", d / "revision", png=False)
    paso("Revisión de un deck", rv["paginas_ok"] and rv["errores"] == 0, f"reglas de uso: {rv['n_pdf']} páginas, {rv['errores']} errores, {rv['avisos']} avisos (informativo)")
    if referencias.TERMINOS.exists():
        err = referencias.comprobar_confidencial(pathlib.Path.home() / ".claude/skills/terracotta/SKILL.md")
        paso("Sin casos concretos", not err, "; ".join(err)[:400])
    else:
        print("OMITIDO Sin casos concretos · la lista de términos solo está en el entorno interno")

    import huella_slide
    _, hu = huella_slide.huella(d / "prueba.pdf", 4)
    clave_ok = 'data-slide-key="s01"' in ea_deck.slide("", 1, 1, "F", "C", clave="s01") and "data-slide-key" not in ea_deck.slide("", 1, 1, "F", "C")
    paso("Huella y clave de slide", hu["residual_text"] == 0 and hu["residual_images"] == 0 and hu["logos"] == 0 and clave_ok,
         f"texto {hu['residual_text']}, imágenes {hu['residual_images']}, logos {hu['logos']}, clave {'bien' if clave_ok else 'MAL'}")
    ejemplo = re.search(r"## Cómo crear una presentación.*?```python\n(.*?)```", (AQUI / "README.md").read_text(encoding="utf-8"), re.S).group(1)
    dr = d / "readme"; dr.mkdir()
    (dr / "ejemplo.py").write_text(ejemplo, encoding="utf-8")
    r = subprocess.run([sys.executable, "ejemplo.py"], capture_output=True, text=True, cwd=dr, env={**os.environ, "TERRACOTTA_DIR": str(AQUI)})
    n = pdf(dr / "salida.html", dr / "salida.pdf") if r.returncode == 0 and (dr / "salida.html").exists() else 0
    if n == 3:
        rv = revisar_deck.revisar(dr / "salida.html", dr / "revision", png=False)
        informe = (dr / "revision" / "informe.md").read_text(encoding="utf-8")
        paso("Ejemplo del README", rv["errores"] == 0 and "llenado]" not in informe, f"3 páginas, {rv['errores']} errores y sin avisos de llenado en su propia revisión")
    else:
        paso("Ejemplo del README", False, f"{n} páginas de 3" if r.returncode == 0 else r.stderr.strip()[-200:])

    tapado = ea_deck.documento("T", [ea_deck.slide(ea_deck.cabecera("01. Prueba", 'Slide <span class="hl-red">sembrada</span>') + X.cuerpo_slide("Sub", X.contadores([(str(i), "Cifra", "Texto") for i in range(8)]), banda="Banda."), 1, 1, "F", "EA")], X.CSS + X.fuente_iconos())
    (d / "tapado.html").write_text(tapado, encoding="utf-8")
    rt = revisar_deck.revisar(d / "tapado.html", d / "rev_tapado", png=False)
    paso("El revisor caza lo tapado por la banda", rt["errores"] > 0, f"{rt['errores']} errores en una slide sembrada")

    pend = ea_deck.documento("P", [ea_deck.portada("==Linea==", "Dos", "==Sub==", "Uso interno", ["Equipo EA"], "Noviembre 2026"),
                                   ea_deck.slide(ea_deck.cabecera("==Eyebrow==", "Título ==x==") + X.cuerpo_slide("==Sub==", X.embudo([("==A==", "", "==1=="), ("B", "", "2")])), 2, 2, "==F==", "EA")],
                             X.CSS + X.fuente_iconos())
    cuerpo_p = pend.split("<body>")[1]
    paso("Dato pendiente en cualquier texto", "==" not in re.sub(r"base64,[A-Za-z0-9+/=]+", "", cuerpo_p) and cuerpo_p.count('class="hueco"') >= 7, f"{cuerpo_p.count(chr(34) + 'hueco' + chr(34))} marcados")

    faltan = [q for q in ("cadena de valor", "logos", "partners", "embudo") if not X.buscar(q)]
    claves_ok = all(X.buscar(k) == X.taxonomia.buscar(k) and X.buscar(k) for k, _, _ in X.taxonomia.INTENCIONES)
    faltan += [q for q in ("proporción", "composición", "reparto por país") if not X.buscar(q)]
    paso("Búsqueda", not faltan and claves_ok and "ecosistema_logos" in X.buscar("partners") and "donut" in X.buscar("reparto por país"), f"sin resultado: {faltan}" if faltan else "lenguaje natural e intenciones")
    import laboratorio
    var, _ = laboratorio.demo_cadena()
    salida = laboratorio.generar("Prueba", var, d / "lab.html", pdf=False)
    n = pdf(salida, d / "lab.pdf")
    paso("Laboratorio de variantes", n == len(var) == 4, f"{n} opciones en PDF")
    css = (AQUI.parent / "colors_and_type.css").read_text(encoding="utf-8")
    tokens = re.findall(r"--ramp-\d:\s*(#[0-9A-Fa-f]{6})", css)
    import importlib.util
    espec = importlib.util.spec_from_file_location("funnel_nucleo", AQUI.parent / "charts" / "funnel.py")
    nucleo = importlib.util.module_from_spec(espec); espec.loader.exec_module(nucleo)
    etapas = [("A", "a", 9), ("B", "b", 5), ("C", "c", 2)]
    paso("Núcleo y código cuadran", tokens == list(X.RAMP) and f"--validacion:     {X.VALIDACION}" in css and f"--chart-neutral:   {X.NEUTRO}" in css and nucleo.funnel_svg(etapas) == X.funnel_svg(etapas), "rampa, verde y embudo")
    import auditar_galeria
    res = auditar_galeria.auditar()
    malas = auditar_galeria.defectos(res)
    paso("Tarjetas de la galería", not malas, f"{len(res)} medidas, {len(malas)} con defectos" + (": " + ", ".join(x["id"] for x in malas[:8]) if malas else ""))
    if "--png" in sys.argv:
        import fitz
        out = pathlib.Path(sys.argv[sys.argv.index("--png") + 1]); out.mkdir(parents=True, exist_ok=True)
        for i, p in enumerate(fitz.open(str(d / "prueba.pdf"))):
            p.get_pixmap(dpi=80).save(str(out / f"prueba_{i + 1}.png"))
        print("PNG en", out)

    print("\n" + ("Terracotta V2 verificado." if not FALLOS else f"{len(FALLOS)} fallos: {', '.join(FALLOS)}"))
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
