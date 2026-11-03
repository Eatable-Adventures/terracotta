"""ea_elementos: todos los elementos visuales de Terracotta V2 para slides HTML de Eatable Adventures.

Capa de presentaciones (presentaciones/), junto a ea_deck.py, que fija portada, cabecera y cierre. Aquí está todo lo
que va en el cuerpo de una slide: 158 elementos en 14 familias, un módulo por familia, más las primitivas
(base.py). Cada función devuelve un fragmento HTML de tamaño fijo (SVG en línea, un Lienzo o HTML con flexbox),
sin JavaScript, así que el PDF sale igual que la pantalla. Desde el 01-11-2026 incluye lo que antes era
ea_visuals.py (composiciones de slide), integrado como elementos. El mismo día se sumaron 18 piezas (cadena_margen,
fichas de competidor, abanico_foco, fases_gates...).

Cómo elegir: por intención, no por costumbre. taxonomia.buscar("brecha") da todas las candidatas; la versión
legible es «Taxonomía de elementos.md». Cómo colocarlos en una slide: «Reglas de uso de elementos.md».
Cómo se ven: «Galería de elementos.html». Iconos: «Catálogo de iconos.html» (iconos.py, Material Symbols).

Uso:
    import os, sys; sys.path.insert(0, os.environ["TERRACOTTA_DIR"])   # la carpeta presentaciones/
    import ea_deck, ea_elementos as X
    cuerpo = ea_deck.cabecera("01. Sección", 'Título con <span class="hl-red">tramo rojo</span>') + \\
             X.cuerpo_slide("Subtítulo", X.cascada(...), banda="Conclusión con **una parte destacada**.")
    html = ea_deck.documento("Título", slides, css_extra=X.CSS + X.fuente_iconos())

Añadir un elemento: la función en el módulo de su familia, su ficha en taxonomia.FICHAS, su nombre en
taxonomia.FAMILIAS y un ejemplo en build_galeria_elementos.py. La galería no se genera si falta alguno.
Después de cualquier cambio: python3 verificar.py. Historial de versiones: Versiones de Terracotta.md.
"""
__version__ = "V2"   # Terracotta V2, 01-11-2026 (ver Versiones de Terracotta.md)
from .base import *          # noqa: F401,F403  tokens, primitivas, Lienzo, CSS, cuerpo_slide
from .marcas import *        # noqa: F401,F403
from .magnitud import *      # noqa: F401,F403
from .evolucion import *     # noqa: F401,F403
from .composicion import *   # noqa: F401,F403
from .comparacion import *   # noqa: F401,F403
from .distribucion import *  # noqa: F401,F403
from .marcos import *        # noqa: F401,F403
from .arboles import *       # noqa: F401,F403
from .cadena import *        # noqa: F401,F403
from .secuencia import *     # noqa: F401,F403
from .cifras import *        # noqa: F401,F403
from .fichas import *        # noqa: F401,F403
from .tablas import *        # noqa: F401,F403
from .sintesis import *      # noqa: F401,F403
from . import base, marcas, magnitud, evolucion, composicion, comparacion, distribucion, marcos, arboles, cadena  # noqa: E402
from . import secuencia, cifras, fichas, tablas, sintesis, taxonomia                                           # noqa: E402
from .taxonomia import FAMILIAS, INTENCIONES, FICHAS, buscar                                                   # noqa: E402
from . import iconos                                                                                            # noqa: E402
def llena(nombre):
    """True si la pieza acepta H. No garantiza que llene: con poco contenido sigue quedando hueco, así que hay que mirar el PNG."""
    import inspect
    return "H" in inspect.signature(globals()[nombre]).parameters


def ayuda(nombre):
    """Todo lo que hace falta para usar una pieza: parámetros, escala, si llena con H, cuándo usarla y alternativas."""
    import inspect
    f, fi = globals()[nombre], FICHAS[nombre]
    print(f"{nombre}{inspect.signature(f)}\n{fi['titulo']} · escala {fi['escala']} · datos: {fi['datos']}"
          f"\nAcepta H: {'sí (mira en el PNG que llene de verdad)' if llena(nombre) else 'no: su alto sale de W o de sus datos, o crece con el cuerpo; si sobra alto, acompáñala con columna(..., repartir=True)'}"
          f"\nAlternativas: {', '.join(fi['alternativas']) or 'ninguna'}\n\n{inspect.getdoc(f)}")


from .iconos import buscar_icono, buscar_completo, comprobar_iconos                                                              # noqa: E402
