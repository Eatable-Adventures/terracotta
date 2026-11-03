"""Fichas y texto: quién es, qué dice y qué sale, en tarjetas y bloques de texto.

Familia 11 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (E, FG1, FG2, FG3, FG4, FILL, LGREY, ORANGE, RED, TINT, flecha_svg, icono, icono_caja, logo, md, pill)
from .magnitud import (columnas)
from .marcas import (chip_nota, etiqueta_evidencia, valoracion)

from .base import (INPUT, _logo_html, mezcla)  # añadidos el 01-11-2026

__all__ = ["tarjeta_actor", "etiquetas_icono", "grupo_fichas", "ficha_hipotesis", "tarjetas_salida", "cita", "lista_numerada", "aviso", "persona", "muro_logos", "ecosistema_logos", "antes_despues_imagen", "ficha_linea", "ficha_empresa", "columnas_numeradas", "afirmacion_evidencia", "columnas_requisitos", "columna_contexto", "tarjetas_escenario", "grupo_logos", "bloque", "ficha_startup", "categorias_chips"]


def tarjeta_actor(nombre, sub="", frase="", logo_html="", rotulo=None, compacta=False):
    """Tarjeta blanca de una empresa u organización: nombre y «país · tipo» a la izquierda, logo a la derecha
    y una sola frase debajo (sin «Ofrece:» ni «Se sabe:»). Va sobre un panel gris claro.
    compacta: versión de tabla (letra un punto menor); rotulo: prefijo en negrita de la frase («Producto»)."""
    if compacta:
        rot = f'<b style="color:var(--fg1)">{E(rotulo)}:</b> ' if rotulo else ""
        return (f'<div style="flex:1;min-width:0;background:#fff;border-radius:12px;padding:7px 12px;display:flex;flex-direction:column;justify-content:center;gap:2px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;gap:8px">'
                f'<div style="min-width:0"><b style="color:var(--fg1);font-size:13px;line-height:1.25">{E(nombre)}</b>'
                f'<div style="font-size:11px;color:var(--fg3)">{E(sub)}</div></div>{logo_html}</div>'
                f'<div style="font-size:12px;line-height:1.35">{rot}{md(frase)}</div></div>')
    rot = f'<b style="color:var(--fg1)">{E(rotulo)}:</b> ' if rotulo else ""
    return (f'<div style="flex:1;background:#fff;border-radius:12px;padding:7px 14px;display:flex;flex-direction:column;justify-content:center;gap:2px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;gap:10px">'
            f'<div><b style="color:var(--fg1);font-size:14px">{E(nombre)}</b><div style="font-size:12px;color:var(--fg3)">{E(sub)}</div></div>'
            f'{logo_html}</div>'
            f'<div style="font-size:13px;line-height:1.38;margin-top:3px">{rot}{md(frase)}</div></div>')


def etiquetas_icono(items, vertical=True):
    """Etiquetas pequeñas con icono en caja (condiciones, capacidades). items: [(icono, texto)]."""
    d = "column" if vertical else "row"
    return (f'<div style="display:flex;flex-direction:{d};gap:6px">' + "".join(
        f'<div class="tile" style="flex:1;background:var(--light-grey);box-shadow:inset 0 0 0 1px var(--border-2);padding:6px 10px">'
        f'{icono_caja(ic, 17, caja=28, radio=8)}<b>{E(t)}</b></div>' for ic, t in items) + '</div>')


def grupo_fichas(titulo, fichas, destacado=False):
    """Grupo de fichas pequeñas en rejilla de dos columnas: icono en caja, nombre, una cifra o dato y origen.
    fichas: [(icono, nombre, dato, origen)]; destacado: título e iconos en rojo.
    Cuándo usarlo: al lado de mapa_madurez (o de cualquier gráfico) para nombrar los casos que importan; de 2 a 6 fichas.
    Cuándo no: como lista suelta sin visual al lado; una sola cifra por ficha."""
    def ficha(ic, n, d, o):
        return (f'<div class="card" style="padding:8px 12px;display:flex;gap:10px;align-items:center">'
                f'{icono_caja(ic, 20, RED if destacado else FG1, None if destacado else "var(--surface-fill)", caja=34, radio=9)}'
                f'<div style="min-width:0"><b style="display:block;color:var(--fg1);font-size:14px;line-height:1.25">{E(n)}</b>'
                f'<div style="font-size:13px;line-height:1.35;margin-top:2px">{md(d)}'
                + (f'<span style="color:var(--fg3)"> · {E(o)}</span>' if o else "") + '</div></div></div>')
    return (f'<div class="k2" style="color:{RED if destacado else FG1};margin:0 0 6px">{E(titulo)}</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">{"".join(ficha(*f) for f in fichas)}</div>')


def ficha_hipotesis(antes, despues, criterios, ejemplos, rotulos=None, sin_dato="Sin dato"):
    """Plantilla de una opción: arriba, lo ya probado → la hipótesis sin probar; debajo, los criterios fijos en filas
    (icono, cifra, texto y nota de la matriz) y, a la derecha, un panel gris con tres ejemplos en tarjeta_actor.
    antes y despues: HTML; criterios: [(icono, criterio, cifra, texto, nota | None)] con nota = (valor, conf) de chip_nota;
    ejemplos: [dict de tarjeta_actor]; rotulos: dict con antes, despues, criterios, criterios_nota, ejemplos, ejemplos_nota.
    La cifra igual a `sin_dato` sale en gris. Mismos criterios y en el mismo orden en todas las slides hermanas.
    Cuándo usarlo: slides hermanas, una por opción priorizada (dos a cuatro), con la misma plantilla.
    Cuándo no: para una sola opción sin hermanas (sobra la estructura) o sin ejemplos reales que mostrar."""
    r = {"antes": "Lo que ya se probó", "despues": "La hipótesis sin probar", "criterios": "Frente a los criterios",
         "criterios_nota": "Puntuación sobre 3", "ejemplos": "Ejemplos", "ejemplos_nota": "", **(rotulos or {})}
    cab = lambda ic, col, txt, cls: (f'<div style="display:flex;gap:8px;align-items:center;margin-bottom:6px">{icono(ic, 19, col)}'
                                     f'<span class="k2 {cls}" style="margin:0">{E(txt)}</span></div>')
    fila1 = ('<div style="display:flex;align-items:stretch">'
             f'<div class="card" style="flex:1.15;background:var(--surface-fill);border-color:var(--surface-fill);padding:10px 16px">'
             f'{cab("check_circle", FG3, r["antes"], "")}{antes}</div>'
             f'<div style="flex:none;width:44px;display:flex;align-items:center;justify-content:center">{flecha_svg(RED, 34, 20, 2.5)}</div>'
             f'<div class="card hot" style="flex:1;background:var(--paper);padding:10px 16px">'
             f'{cab("science", RED, r["despues"], "red")}{despues}</div></div>')
    filas = "".join(
        f'<div style="flex:1;display:grid;grid-template-columns:30px 104px 158px 1fr 34px;align-items:center;align-content:center;column-gap:10px;padding:5px 0;'
        f'{"border-top:1px solid var(--border-2);" if k else ""}">'
        f'<span style="display:inline-flex;width:30px;height:30px;border-radius:8px;background:var(--surface-fill);align-items:center;justify-content:center">'
        f'{icono(ic, 18, FG2)}</span>'
        f'<b style="font-size:14px;color:var(--fg1)">{E(lab)}</b>'
        f'<span class="big" style="font-size:19px;white-space:nowrap;{"color:var(--fg3);" if c == sin_dato else ""}">{E(c)}</span>'
        f'<span style="font-size:13px;line-height:1.36">{md(t)}</span>'
        f'<span style="justify-self:end">{chip_nota(nota) if nota else ""}</span></div>'
        for k, (ic, lab, c, t, nota) in enumerate(criterios))
    fila2 = ('<div class="card" style="padding:9px 16px 6px;flex:1;display:flex;flex-direction:column">'
             '<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2px">'
             f'<span class="k2 red" style="margin:0">{E(r["criterios"])}</span>'
             f'<span style="font-size:12px;color:var(--fg3)">{E(r["criterios_nota"])}</span></div>'
             f'<div style="flex:1;display:flex;flex-direction:column">{filas}</div></div>')
    izq = f'<div class="col" style="flex:1;gap:10px;min-width:0">{fila1}{fila2}</div>'
    head = (f'<div style="padding:2px 4px 2px"><div style="display:flex;gap:8px;align-items:center">{icono("storefront", 19, FG2)}'
            f'<span class="k2" style="margin:0;color:var(--fg1)">{E(r["ejemplos"])}</span></div>'
            + (f'<div style="font-size:12px;color:var(--fg3);margin-top:2px">{E(r["ejemplos_nota"])}</div>' if r["ejemplos_nota"] else "") + '</div>')
    der = (f'<div style="flex:none;width:384px;background:var(--surface-fill);border-radius:16px;padding:10px;display:flex;flex-direction:column;gap:6px">'
           f'{head}{"".join(tarjeta_actor(**e) for e in ejemplos)}</div>')
    return f'<div style="display:flex;gap:22px;width:100%;align-self:stretch">{izq}{der}</div>'


def tarjetas_salida(items):
    """Tarjetas de escenario o salida con borde izquierdo (rojo si está dentro del alcance, gris si no), etapa,
    píldora de alcance, título y texto.
    items: [(etapa, alcance, dentro, título, texto)].
    Cuándo usarlo: las salidas de una decisión (si sí, si no, fuera de alcance) bajo un gantt o un árbol; 2 a 4.
    Cuándo no: como lista de recomendaciones sin decisión detrás (usa tarjetas_miniatura)."""
    return ('<div class="row" style="width:100%;gap:16px">' + "".join(
        f'<div class="card" style="flex:1;border-left:4px solid {"var(--red)" if dentro else "var(--fg4)"};padding:10px 18px;display:flex;flex-direction:column;gap:3px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><span class="k2 {"red" if dentro else ""}" style="margin:0">{E(et)}</span>'
        f'<span style="font-size:12px;font-weight:500;border-radius:99px;padding:2px 11px;white-space:nowrap;'
        f'{"background:var(--burgundy);color:var(--cream)" if dentro else "background:var(--light-grey);color:var(--fg2);box-shadow:inset 0 0 0 1px var(--border-2)"}">{E(al)}</span></div>'
        f'<b style="font-size:15px;color:var(--fg1);line-height:1.3">{E(ti)}</b><span style="font-size:14px;line-height:1.4">{md(tx)}</span></div>'
        for et, al, dentro, ti, tx in items) + '</div>')


def cita(texto_, autor, cargo="", W=520):
    """Cita destacada de una entrevista o un experto, con comillas en rojo y atribución.
    Cuándo usarlo: voz del cliente o del mercado que respalda una conclusión (una por slide).
    Cuándo no: citas sin autor identificable o que solo repiten el título."""
    return (f'<div style="width:{W}px;position:relative;padding:14px 0 0 54px">'
            f'<span style="position:absolute;left:0;top:-14px;font-size:84px;line-height:1;font-weight:700;color:var(--red)">“</span>'
            f'<div style="font-size:18px;line-height:1.45;color:var(--fg1);font-weight:500">{md(texto_)}</div>'
            f'<div style="margin-top:12px;font-size:13px;color:var(--fg3)"><b style="color:var(--fg1)">{E(autor)}</b>'
            f'{" · " + E(cargo) if cargo else ""}</div></div>')


def lista_numerada(items, W=520, H=None):
    """Lista numerada con el número en cuadro rojo, título en negrita y una línea de texto.
    items: [(título, texto)]. H: alto total (reparte el aire entre los puntos).
    Cuándo usarlo: recomendaciones, próximos pasos o conclusiones (3 a 5).
    Cuándo no: si el orden no significa nada (usa icono_dato o viñetas)."""
    return (f'<div style="display:flex;flex-direction:column;gap:14px;width:{W}px;{f"height:{H}px;justify-content:space-between;" if H else ""}">' + "".join(
        f'<div style="display:flex;gap:14px;align-items:flex-start"><span class="nb">{i + 1}</span>'
        f'<div><b style="font-size:14px;color:var(--fg1)">{E(t)}</b><div style="font-size:13px;line-height:1.4;color:var(--fg2);margin-top:2px">{md(x)}</div></div></div>'
        for i, (t, x) in enumerate(items)) + '</div>')


def aviso(texto_, tipo="clave", W=520):
    """Recuadro de llamada: 'clave' (rosa con borde rojo), 'aviso' (icono de alerta) o 'nota' (gris).
    Cuándo usarlo: una advertencia, un supuesto crítico o una idea que no puede perderse, dentro del cuerpo.
    Cuándo no: para la conclusión de la slide (eso es la banda de cuerpo_slide)."""
    bg, bd, ic = {"clave": (TINT, RED, "new_releases"), "aviso": ("#fff", ORANGE, "warning"), "nota": (FILL, FG4, "rate_review")}[tipo]
    return (f'<div style="width:{W}px;display:flex;gap:12px;align-items:flex-start;background:{bg};border-left:3px solid {bd};'
            f'padding:12px 16px;font-size:14px;line-height:1.45;color:var(--fg1)">{icono(ic, 22, bd)}<div>{md(texto_)}</div></div>')


def persona(nombre, cargo, iniciales=None, destacada=False):
    """Persona con monograma: iniciales en círculo, nombre y cargo. Sin fotos salvo que el cliente las aporte.
    Cuándo usarlo: equipo del proyecto, interlocutores o expertos entrevistados.
    Cuándo no: en portadas (la norma de portada prohíbe fotos e iconos)."""
    ini = iniciales or "".join(p[0] for p in nombre.split()[:2]).upper()
    bg = RED if destacada else FG1
    return (f'<div style="display:flex;align-items:center;gap:12px"><span style="width:44px;height:44px;border-radius:50%;background:{bg};'
            f'color:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;flex:none">{E(ini)}</span>'
            f'<div><b style="font-size:14px;color:var(--fg1)">{E(nombre)}</b><div style="font-size:13px;color:var(--fg3)">{E(cargo)}</div></div></div>')


def _actor_logo(a, alto, ancho):
    """Contenido de una tesela: el logo si lo hay; si no, el nombre en texto, para que se vea qué falta sin romper la slide.
    a: nombre; (nombre, ruta); o dict(nombre, logo=ruta, logo_html=HTML ya hecho)."""
    if isinstance(a, dict):
        nombre, ruta, hecho = a.get("nombre", ""), a.get("logo"), a.get("logo_html")
    elif isinstance(a, (tuple, list)):
        nombre, ruta, hecho = a[0], a[1] if len(a) > 1 else None, None
    else:
        nombre, ruta, hecho = a, None, None
    if hecho:
        return hecho
    im = logo(ruta, alto, "center", ancho) if ruta else None
    return im or E(nombre)


def muro_logos(nombres, columnas=4, W=520, H=None, alto_logo=34):
    """Muro de logos en teselas iguales. nombres: nombre (sale en texto), (nombre, ruta del logo) o
    dict(nombre, logo=ruta, logo_html=HTML). Si un logo no existe, sale el nombre. H: alto total (reparte las filas).
    Regla: a color, del mismo alto y con su origen registrado en un FUENTES.md junto a los logos (D6).
    Cuándo usarlo: quién está en un segmento (startups, proveedores, partners, aliados, clientes de referencia).
    Cuándo no: si hace falta decir algo de cada empresa (usa grupo_fichas o tarjeta_actor); si los actores van por
    fases, estados o tipos (usa ecosistema_logos)."""
    ancho = (W - 8 * (columnas - 1)) / columnas - 20
    alto_fila = "grid-auto-rows:1fr;" if H else ""
    alto_caja = f"height:{H}px;" if H else ""
    alto_tesela = "min-height:0" if H else "height:54px"
    return (f'<div style="display:grid;grid-template-columns:repeat({columnas},1fr);{alto_fila}gap:8px;width:{W}px;{alto_caja}">'.replace(";;", ";").replace(';">', '">') + "".join(
        f'<div style="{alto_tesela};background:#fff;border:1px solid var(--border-1);border-radius:10px;display:flex;align-items:center;'
        f'justify-content:center;font-size:14px;font-weight:700;color:var(--fg2);letter-spacing:.02em">{_actor_logo(n, alto_logo, ancho)}</div>' for n in nombres) + '</div>')


def ecosistema_logos(grupos, W=1152, H=None, por_fila=None, alto_logo=26):
    """Ecosistema a toda la slide: todos los actores en teselas iguales, agrupados por fase, estado o tipo, con el rótulo,
    el recuento y un estado opcional a la izquierda de cada grupo. Cada actor aparece una sola vez.
    grupos: [dict(rotulo, actores=[como en muro_logos], estado=None, destacado=False)]; H: alto total (reparte por filas de teselas);
    por_fila: teselas por fila (por defecto, las que caben a unos 112 px).
    Cuándo usarlo: que se vea el universo entero (de 10 a 70 actores en 2 a 6 grupos): candidatos por fase, partners y aliados.
    Cuándo no: un solo grupo (usa muro_logos); si importa dónde están (usa mapa_actores); si hay que decir algo de cada uno (usa ficha_linea)."""
    ancho_rotulo, sep = 176, 7
    util = W - ancho_rotulo - 40
    n = por_fila or max(3, int((util + sep) // (112 + sep)))
    tesela = (util - sep * (n - 1)) / n
    filas = [max(1, math.ceil(len(g["actores"]) / n)) for g in grupos]
    bloques = []
    for g, k in zip(grupos, filas):
        hot = g.get("destacado")
        teselas = "".join(
            f'<div style="background:#fff;border:1px solid var(--border-1);border-radius:8px;display:flex;align-items:center;justify-content:center;'
            f'padding:4px 6px;{"" if H else "height:46px;"}min-height:0;min-width:0;font-size:12px;font-weight:700;line-height:1.15;text-align:center;color:var(--fg2)">'
            f'{_actor_logo(a, alto_logo, tesela - 14)}</div>' for a in g["actores"])
        bloques.append(
            f'<div style="{f"flex:{k} 1 0;" if H else ""}display:grid;grid-template-columns:{ancho_rotulo}px 1fr;gap:16px;align-items:stretch;background:var(--surface-fill);'
            f'border-radius:10px;padding:10px 12px;{"border-left:3px solid var(--red);" if hot else ""}min-height:{94 if g.get("estado") else 72}px">'
            f'<div style="display:flex;flex-direction:column;justify-content:center;gap:4px">'
            f'<b style="font-size:26px;line-height:1;color:var(--{"red" if hot else "fg1"})">{len(g["actores"])}</b>'
            f'<b style="font-size:14px;line-height:1.25;color:var(--fg1)">{E(g["rotulo"])}</b>'
            + (f'<div>{pill(g["estado"], "red" if hot else "out")}</div>' if g.get("estado") else "") +
            f'</div><div style="display:grid;grid-template-columns:repeat({n},minmax(0,1fr));{"grid-auto-rows:1fr;" if H else ""}gap:{sep}px;min-height:0">{teselas}</div></div>')
    alto = f"height:{H}px;" if H else ""
    return f'<div style="width:{W}px;{alto}display:flex;flex-direction:column;gap:8px">{"".join(bloques)}</div>'


def _foto(img, ancho, alto):
    if img:
        im = logo(img, alto, "center", ancho)
        if im:
            return (f'<div style="width:{ancho}px;height:{alto}px;border-radius:10px;overflow:hidden">'
                    + im.replace("object-fit:contain", "object-fit:cover").replace(f"max-width:{ancho}px", f"width:{ancho}px") + '</div>')
    return (f'<div style="width:{ancho}px;height:{alto}px;border-radius:10px;background:repeating-linear-gradient(45deg,{LGREY} 0 8px,{FILL} 8px 16px);'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:var(--fg3);font-size:12px">'
            f'{icono("visibility", 28, FG4)}Foto del cliente</div>')


def antes_despues_imagen(antes, despues, W=520, alto=170):
    """Antes y después en imagen: dos fotos del producto (o del proceso) con su rótulo y una flecha entre ellas.
    antes y despues = dict(imagen=ruta o None, rotulo, texto). Sin imagen, un hueco rayado «Foto del cliente».
    Cuándo usarlo: el cambio visible de un producto, envase o proceso, con material del cliente.
    Cuándo no: con fotos de banco de imágenes (si no es el producto real, no aporta)."""
    ancho = (W - 56) / 2
    def lado(d, kind):
        return (f'<div style="width:{ancho}px;display:flex;flex-direction:column;gap:8px">{_foto(d.get("imagen"), ancho, alto)}'
                f'<div>{pill(d["rotulo"], kind)}</div><div style="font-size:13px;line-height:1.4;color:var(--fg2)">{md(d["texto"])}</div></div>')
    return (f'<div style="display:flex;align-items:flex-start;gap:14px;width:{W}px">{lado(antes, "neutral")}'
            f'<div style="height:{alto}px;display:flex;align-items:center">{flecha_svg(RED, 28, 18, 2.5)}</div>{lado(despues, "red")}</div>')


def ficha_linea(empresas, W=1100, escala_madurez=5, H=None):
    """Ficha de una línea por empresa: logo, nombre, país y tipo, madurez en puntos y una frase.
    empresas: [dict(nombre, pais, tipo, madurez=None, frase, logo_html=None, destacada=False)]. H: alto total (reparte las filas).
    Sin madurez no hay columna de puntos, para usarla en media slide.
    Cuándo usarlo: listas largas de candidatos (10 a 20) en una o dos slides, antes de las fichas completas.
    Cuándo no: si hay que comparar varias dimensiones con nota (usa matriz_puntuacion)."""
    filas = []
    for e in empresas:
        hot = e.get("destacada")
        ini = "".join(p[0] for p in e["nombre"].split()[:2]).upper()
        lg = e.get("logo_html") or (f'<span style="width:40px;height:40px;border-radius:10px;background:{RED if hot else FG1};color:#fff;'
                                    f'display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">{E(ini)}</span>')
        con_mad = e.get("madurez") is not None
        filas.append(f'<div style="display:grid;grid-template-columns:48px {"230px 150px" if con_mad else "190px"} 1fr;gap:16px;align-items:center;padding:{4 if H else 9}px 12px;'
                     f'border-bottom:1px solid var(--border-2);{f"background:{TINT};" if hot else ""}">'
                     f'<div>{lg}</div><div><b style="font-size:14px;color:{RED if hot else FG1}">{E(e["nombre"])}</b>'
                     f'<div style="font-size:12px;color:var(--fg3)">{E(e["pais"])} · {E(e["tipo"])}</div></div>'
                     + (f'<div style="display:flex;flex-direction:column;gap:3px"><span style="font-size:11px;font-weight:700;letter-spacing:.08em;color:var(--fg3)">MADUREZ</span>'
                        f'{valoracion(e["madurez"], escala_madurez)}</div>' if con_mad else "") +
                     f'<div style="font-size:13px;line-height:1.4;color:var(--fg2)">{md(e["frase"])}</div></div>')
    alto = f"height:{H}px;display:grid;grid-auto-rows:1fr;" if H else ""
    return f'<div style="width:{W}px;{alto}border-top:1.5px solid var(--fg1)">{"".join(filas)}</div>'


def ficha_startup(e, W=1152, H=None, tam_texto=15):
    """Ficha de startup a toda la slide, sin ingresos: fila de datos clave arriba y cuatro bloques de texto que llenan el resto.
    e = dict(datos=[(rótulo, valor)], bloques=[(título, texto)], destacado=índice del bloque con filete rojo).
    Cuándo usarlo: fichas de finalistas o candidatos cuando no hay cifras de ingresos que enseñar (una por slide, hermanas).
    Cuándo no: si hay ingresos y una cita (usa ficha_empresa); para listas largas (usa ficha_linea)."""
    datos = "".join(f'<div style="flex:1;min-width:0;padding:10px 16px;background:var(--surface-fill);border-radius:10px"><span class="k2" style="margin-bottom:3px">{E(r)}</span>'
                    f'<b style="display:block;font-size:15px;line-height:1.25;color:var(--fg1)">{E(v)}</b></div>' for r, v in e["datos"])
    bloques = "".join(bloque(t, f'<div style="font-size:{tam_texto}px;line-height:1.5;color:var(--fg2)">{md(x)}</div>', filete="rojo" if i == e.get("destacado") else "negro")
                      for i, (t, x) in enumerate(e["bloques"]))
    return (f'<div style="width:{W}px;{f"height:{H}px;" if H else ""}display:flex;flex-direction:column;gap:16px"><div style="display:flex;gap:10px">{datos}</div>'
            f'<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:16px 20px">{bloques}</div></div>')


def categorias_chips(grupos, columnas=3, marca="Finalista", W=1152, H=None, rojo=True):
    """Mapa de categorías: un bloque por categoría con su recuento y un chip por elemento; los marcados, en rojo.
    grupos: [(categoría, [nombre o (nombre, True si marcado)])]; marca: texto de la leyenda (None, sin leyenda).
    rojo=False: recuentos en negro, para que el rojo quede solo en los marcados (K1). H baja la leyenda; no agranda los chips.
    Cuándo usarlo: una shortlist o un universo de 8 a 30 nombres repartidos en 3 a 9 categorías, con un estado transversal.
    Cuándo no: de 6 a 12 elementos con definición (usa anillo_categorias) o si no hay categorías (usa muro_logos)."""
    def chip(n):
        nom, on = n if isinstance(n, tuple) else (n, False)
        return (f'<span style="font-size:13px;font-weight:600;padding:5px 11px;border-radius:999px;white-space:nowrap;'
                f'{"background:var(--red);color:#fff" if on else "background:var(--surface-fill);color:var(--fg1)"}">{E(nom)}</span>')
    cel = "".join(f'<div style="border-top:3px solid var(--fg1);padding-top:8px"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:9px">'
                  f'<b style="font-size:14px;color:var(--fg1)">{E(c)}</b><b style="font-size:20px;color:var(--{"red" if rojo else "fg1"})">{len(ns)}</b></div>'
                  f'<div style="display:flex;flex-wrap:wrap;gap:6px">{"".join(chip(n) for n in ns)}</div></div>' for c, ns in grupos)
    ley = f'<div style="display:flex;align-items:center;gap:8px;margin-top:10px">{chip((marca, True))}</div>' if marca else ""
    return (f'<div style="width:{W}px;{f"height:{H}px;" if H else ""}display:flex;flex-direction:column"><div style="flex:1;display:grid;'
            f'grid-template-columns:repeat({columnas},1fr);grid-auto-rows:1fr;gap:16px 22px">{cel}</div>{ley}</div>')


def ficha_empresa(e, W=1100):
    """Ficha de empresa de un vistazo: cabecera con monograma o logo, frase y etiquetas; datos clave, ingresos
    en columnas, diferenciadores y una cita; al pie, madurez y nivel de evidencia.
    e = dict(nombre, frase, etiquetas=[...], datos=[(rótulo, valor)], ingresos=[(año, valor)], unidad,
    diferenciadores=[...], cita=(texto, autor), madurez=1 a 5, evidencia='A' | 'B' | 'C', logo_html=None).
    Cuándo usarlo: perfil de una startup, un proveedor o un candidato antes de la entrevista (una por slide).
    Cuándo no: para listas largas (usa ficha_linea)."""
    ini = "".join(p[0] for p in e["nombre"].split()[:2]).upper()
    lg = e.get("logo_html") or (f'<span style="width:54px;height:54px;border-radius:14px;background:var(--fg1);color:#fff;display:inline-flex;'
                                f'align-items:center;justify-content:center;font-weight:700;font-size:18px;flex:none">{E(ini)}</span>')
    cab = (f'<div style="display:flex;align-items:center;gap:16px;padding-bottom:14px;border-bottom:1.5px solid var(--fg1)">{lg}'
           f'<div style="flex:1"><b style="font-size:22px;color:var(--fg1);letter-spacing:-.01em">{E(e["nombre"])}</b>'
           f'<div style="font-size:14px;color:var(--fg2);margin-top:2px">{md(e["frase"])}</div></div>'
           f'<div style="display:flex;gap:6px">{"".join(pill(t, "neutral") for t in e.get("etiquetas", []))}</div></div>')
    datos = "".join(f'<div><span class="k2" style="margin-bottom:2px">{E(r)}</span><b style="font-size:15px;color:var(--fg1)">{E(v)}</b></div>' for r, v in e["datos"])
    ingresos = columnas(e["ingresos"], destacado=len(e["ingresos"]) - 1, unidad=e.get("unidad", ""), W=320, H=170)
    difs = "".join(f'<div class="it3" style="font-size:13px;gap:8px"><span class="dot" style="width:12px"><i></i></span><span>{md(d)}</span></div>' for d in e["diferenciadores"])
    cuerpo = (f'<div style="display:grid;grid-template-columns:250px 340px 1fr;gap:28px;padding-top:16px">'
              f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px 12px;align-content:start">{datos}</div>'
              f'<div><span class="k2">Ingresos</span>{ingresos}</div>'
              f'<div><span class="k2">Qué la diferencia</span><div style="display:flex;flex-direction:column;gap:6px">{difs}</div>'
              + (f'<div style="margin-top:14px;padding-left:12px;border-left:3px solid var(--red);font-size:14px;line-height:1.4;color:var(--fg1)">«{md(e["cita"][0])}»'
                 f'<div style="font-size:12px;color:var(--fg3);margin-top:4px">{E(e["cita"][1])}</div></div>' if e.get("cita") else "") + '</div></div>')
    pie = (f'<div style="display:flex;align-items:center;gap:28px;margin-top:14px;padding-top:10px;border-top:1px solid var(--border-2);font-size:13px;color:var(--fg2)">'
           f'<span style="display:flex;align-items:center;gap:10px"><b style="color:var(--fg1)">Madurez</b>{valoracion(e.get("madurez", 3))}</span>'
           f'{etiqueta_evidencia(e.get("evidencia", "B"))}</div>')
    return f'<div style="width:{W}px">{cab}{cuerpo}{pie}</div>'


def columnas_numeradas(items, W=1100, H=None, tam_texto=13, tam_cifra=15, rojo=True):
    """Columnas numeradas: 01, 02 y 03 en rojo con icono, título, texto y, al pie, una caja con una o dos cifras;
    separadores verticales finos entre columnas. items: [dict(titulo, texto, icono=None, cifras=[(cifra, rótulo)])].
    H: alto total (las cajas de cifras bajan al pie). tam_texto y tam_cifra: px del texto y de las cifras.
    rojo=False: números y cifras en negro (K1), y el foco se pone en el texto con **negrita**.
    Cuándo usarlo: el resumen ejecutivo o la síntesis de evidencia en 2 a 4 ideas, cada una con su dato.
    Cuándo no: recomendaciones o pasos que se leen en orden de arriba abajo (usa lista_numerada)."""
    n = len(items)
    cols = []
    for i, it in enumerate(items):
        ic = icono(it["icono"], 18, RED) if it.get("icono") else ""
        cif = ""
        if it.get("cifras"):
            cif = ('<div style="margin-top:auto;display:flex;border:1px solid var(--border-1);border-radius:10px;padding:10px 4px">' + "".join(
                f'<div style="flex:1;text-align:center;padding:0 8px;{"border-left:1px solid var(--border-2);" if k else ""}">'
                f'<b style="display:block;font-size:{tam_cifra}px;color:var(--{"red" if rojo else "fg1"});white-space:nowrap">{E(c)}</b>'
                f'<span style="font-size:11px;line-height:1.25;color:var(--fg2);font-weight:600">{E(r)}</span></div>' for k, (c, r) in enumerate(it["cifras"])) + '</div>')
        cols.append(f'<div style="display:flex;flex-direction:column;padding:0 22px;{"border-left:1px solid var(--border-2);" if i else "padding-left:0;"}{"padding-right:0;" if i == n - 1 else ""}">'
                    f'<div style="display:flex;align-items:center;gap:10px"><span style="font-size:28px;font-weight:700;color:var(--{"red" if rojo else "fg1"});letter-spacing:-.02em">{i + 1:02d}</span>{ic}</div>'
                    f'<b style="font-size:14px;line-height:1.3;color:var(--fg1);margin:8px 0">{E(it["titulo"])}</b>'
                    f'<div style="font-size:{tam_texto}px;line-height:1.45;color:var(--fg2);margin-bottom:14px">{md(it["texto"])}</div>{cif}</div>')
    return f'<div style="width:{W}px;{f"height:{H}px;" if H else ""}display:grid;grid-template-columns:repeat({n},1fr);align-items:stretch">{"".join(cols)}</div>'


def afirmacion_evidencia(items, rotulo_evidencia="Voz del experto", W=1100):
    """Afirmación y su evidencia: por columna, lo que se afirma arriba, un chevrón rojo y debajo la cita que lo
    respalda con su autor. items: [dict(afirmacion, cita, autor)], de 2 a 4.
    Cuándo usarlo: validar con entrevistas lo que dijo un entregable anterior (lo que afirmamos frente a lo que dicen).
    Cuándo no: una sola cita (usa cita) o el registro de todas las entrevistas (usa panel_entrevistas)."""
    n = len(items)
    chev = (f'<svg width="140" height="18" viewBox="0 0 140 18" style="display:block;margin:0 auto"><polygon points="0,0 70,14 140,0 70,6" '
            f'fill="{RED}" fill-opacity=".85"/></svg>')
    celdas = [f'<div style="font-size:14px;line-height:1.4;color:var(--fg1);padding-bottom:18px">{md(it["afirmacion"])}</div>' for it in items]
    celdas += [f'<div>{chev}<div style="text-align:center;font-size:12px;font-weight:700;color:var(--red);margin:10px 0 12px">{E(rotulo_evidencia)}</div></div>' for _ in items]
    celdas += [f'<div style="font-size:13px;line-height:1.45;color:var(--fg2)">«{md(it["cita"])}»'
               f'<div style="font-size:12px;font-style:italic;color:var(--fg3);margin-top:6px">{E(it["autor"])}</div></div>' for it in items]
    return f'<div style="width:{W}px;display:grid;grid-template-columns:repeat({n},1fr);column-gap:34px;align-items:start">{"".join(celdas)}</div>'


def columnas_requisitos(columnas, titulo_pie="Coste y plazo", rotulos_pie=("Coste", "Plazo"), W=1100):
    """Columnas de requisitos: cabecera en píldora roja, la lista de lo que hace falta (los secundarios en gris) y, al
    pie y alineados entre columnas, el coste y el plazo. columnas: [dict(titulo, puntos=[texto o (texto, True si
    secundario)], coste, plazo)].
    Cuándo usarlo: capacidades mínimas o recomendables por dimensión, con lo que cuestan y tardan.
    Cuándo no: si no hay coste ni plazo (usa columnas_numeradas o bloque)."""
    n = len(columnas)
    celdas = [f'<div style="background:var(--red);color:#fff;border-radius:99px;text-align:center;font-size:14px;font-weight:700;padding:7px 12px">{E(c["titulo"])}</div>'
              for c in columnas]
    for c in columnas:
        pts = ""
        for p in c.get("puntos", []):
            txt, sec = (p, False) if isinstance(p, str) else p
            pts += (f'<div style="display:flex;gap:7px;font-size:13px;line-height:1.38;color:var(--{"fg3" if sec else "fg2"})">'
                    f'<span style="color:{mezcla(RED, "#FFFFFF", .4) if sec else RED};flex:none">▸</span><span>{md(txt)}</span></div>')
        celdas.append(f'<div style="display:flex;flex-direction:column;gap:8px;padding:14px 4px 16px">{pts}</div>')
    celdas += [f'<div style="border-top:1px solid var(--border-2);padding-top:10px"><div style="font-size:12px;font-weight:700;color:var(--red);margin-bottom:4px">{E(titulo_pie)}</div>'
               f'<div style="font-size:14px;font-weight:700;color:var(--fg1)"><span style="font-size:12px;font-weight:400;color:var(--fg3);margin-right:6px">{E(rotulos_pie[0])}</span>{E(c["coste"])}</div>'
               f'<div style="font-size:14px;font-weight:700;color:var(--fg1);margin-top:2px"><span style="font-size:12px;font-weight:400;color:var(--fg3);margin-right:6px">{E(rotulos_pie[1])}</span>{E(c["plazo"])}</div></div>'
               for c in columnas]
    return f'<div style="width:{W}px;display:grid;grid-template-columns:repeat({n},1fr);column-gap:26px;align-items:stretch">{"".join(celdas)}</div>'


def columna_contexto(etiqueta, parrafos, cifra=None, W=360):
    """Columna de contexto: barra roja con el rótulo, dos o tres párrafos cortos y, al pie, una cifra ancla en un
    recuadro gris con filete rojo. Va al lado del visual (rejilla F de las reglas de uso), en una X.fila(..., crecer=True)
    y con vertical="flex-start": así la cifra baja al pie.
    parrafos: [texto con **negrita**]; cifra = (cifra, texto) o None.
    Cuándo usarlo: explicar el método o el contexto de la pieza vecina (un embudo, un Gantt, un mapa) y dejar una cifra.
    Cuándo no: si la columna solo repite lo que ya dice el visual; mejor dar más ancho a la pieza."""
    ps = "".join(f'<p style="margin:10px 0 0;font-size:13px;line-height:1.45;color:var(--fg2)">{md(t)}</p>' for t in parrafos)
    cif = (f'<div style="margin-top:auto;background:var(--surface-fill);border-left:3px solid var(--red);padding:12px 16px;display:flex;align-items:center;gap:14px">'
           f'<b style="font-size:32px;color:var(--red);letter-spacing:-.02em;white-space:nowrap;font-variant-numeric:tabular-nums">{E(cifra[0])}</b>'
           f'<span style="font-size:13px;line-height:1.35;color:var(--fg2)">{md(cifra[1])}</span></div>' if cifra else "")
    return (f'<div style="width:{W}px;display:flex;flex-direction:column;align-self:stretch;gap:0">'
            f'<div style="background:var(--red);color:#fff;border-radius:99px;font-size:12px;font-weight:700;padding:5px 14px">{E(etiqueta)}</div>'
            f'{ps}<div style="height:16px"></div>{cif}</div>')


def tarjetas_escenario(escenarios, destacado=None, W=1100):
    """Escenarios hermanos en tarjetas del mismo alto, con el de referencia destacado (fondo gris y filete rojo arriba):
    nombre, dato clave, texto y un visual pequeño al pie (minigráfica, score). escenarios: [dict(nombre, dato=None,
    texto, visual="")]; destacado: índice (normalmente el central, el escenario base).
    Cuándo usarlo: conservador, base y optimista, o dos o tres alternativas que se comparan con la misma plantilla.
    Cuándo no: si los escenarios son una serie continua (usa abanico de escenarios)."""
    n = len(escenarios)
    cards = []
    for i, e in enumerate(escenarios):
        hot = i == destacado
        st = ("background:var(--surface-fill);box-shadow:inset 0 3px 0 var(--red);" if hot else "background:#fff;box-shadow:inset 0 0 0 1px var(--border-1);")
        dato = f'<div style="font-size:13px;font-weight:700;color:var(--red);margin:3px 0 8px">{E(e["dato"])}</div>' if e.get("dato") else '<div style="height:8px"></div>'
        cards.append(f'<div style="{st}border-radius:14px;padding:16px 18px;display:flex;flex-direction:column">'
                     f'<b style="font-size:15px;color:var(--{"red" if hot else "fg1"})">{E(e["nombre"])}</b>{dato}'
                     f'<div style="font-size:13px;line-height:1.42;color:var(--fg2);margin-bottom:12px">{md(e["texto"])}</div>'
                     f'<div style="margin-top:auto;display:flex;justify-content:center">{e.get("visual", "")}</div></div>')
    return f'<div style="width:{W}px;display:grid;grid-template-columns:repeat({n},1fr);gap:16px;align-items:stretch">{"".join(cards)}</div>'


def grupo_logos(logos, rotulo="Actores", columnas=2, destacado=False, W=320):
    """Grupo de logos en una caja discontinua con su rótulo arriba. logos: [logo de logo() o nombre].
    Cuándo usarlo: los actores de una columna (tier, vía, segmento), al pie de su texto, en rejillas de tres columnas.
    Cuándo no: un universo grande de actores sin columnas (usa muro_logos)."""
    celdas = "".join(f'<div style="display:flex;align-items:center;justify-content:center;height:34px">{_logo_html(l, 22)}</div>' for l in logos)
    return (f'<div style="width:{W}px;box-sizing:border-box;border:1.5px dashed {RED if destacado else INPUT};border-radius:14px;padding:10px 14px 12px">'
            f'<div style="text-align:center;font-size:12px;font-weight:700;color:var(--{"red" if destacado else "fg1"});margin-bottom:6px">{E(rotulo)}</div>'
            f'<div style="display:grid;grid-template-columns:repeat({columnas},1fr);gap:4px 10px">{celdas}</div></div>')


def bloque(titulo, contenido, filete="rojo", fondo="blanco", W=None):
    """Bloque con filete superior: la tarjeta base de las slides de texto, con una raya de 3 px arriba (roja para lo
    que importa, negra para el resto) y el título en negrita. contenido: texto con **negrita** o HTML;
    filete: 'rojo', 'negro' o None; fondo: 'blanco' (con sombra suave) o 'gris'.
    Cuándo usarlo: dos o tres bloques de texto que se leen por separado (contexto, brecha, implicación).
    Cuándo no: si el texto se puede convertir en un visual (D1); para la conclusión de la slide (usa la banda)."""
    col = {"rojo": RED, "negro": FG1}.get(filete)
    cuerpo = contenido if str(contenido).lstrip().startswith("<") else f'<div style="font-size:13px;line-height:1.45;color:var(--fg2)">{md(contenido)}</div>'
    fondo_css = "background:var(--surface-fill);" if fondo == "gris" else "background:#fff;box-shadow:var(--shadow-sm);"
    return (f'<div style="{f"width:{W}px;" if W else ""}{fondo_css}{f"border-top:3px solid {col};" if col else ""}padding:14px 18px 16px;display:flex;flex-direction:column;gap:8px">'
            f'<b style="font-size:14px;color:var(--fg1)">{E(titulo)}</b>{cuerpo}</div>')
