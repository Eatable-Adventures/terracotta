"""Cifras y KPI: una o pocas cifras que mandan.

Familia 10 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
from .base import (E, icono_caja, md)
from .evolucion import (sparkline)
from .marcas import (delta)

__all__ = ["contadores", "tarjeta_cifra", "tarjeta_kpi", "panel_kpi", "fila_parametros", "cifra_delta", "icono_dato"]


def contadores(items, ancho=None, H=None, destacado=None):
    """Contadores apilados: cifra grande en rojo, rótulo en negro y una línea que explica de dónde sale.
    items: [(cifra, rótulo, texto)]. H: alto total (reparte las filas). destacado: índice de la única cifra en rojo, y
    el resto en negro (K1: lo que nombra el título); sin él, todas en rojo.
    Cuándo usarlo: de 2 a 4 magnitudes que dan base a un mensaje (alcance de una búsqueda, tamaño de una muestra), al lado de un visual.
    Cuándo no: si las cifras se comparan entre sí (usa barras_objetivo) o si son más de 4 (pasa a tabla)."""
    w = f"width:{ancho}px;flex:none;" if ancho else "flex:1;"
    alto = f"height:{H}px;" if H else ""
    fl = "flex:1;display:flex;flex-direction:column;justify-content:center;" if H else ""
    color = lambda i: "" if destacado is None or i == destacado else ";color:var(--fg1)"
    filas = "".join(f'<div style="{fl}padding:16px 0;border-bottom:1px solid var(--border-1)"><div><span class="big" style="font-size:38px{color(i)}">{E(a)}</span>'
                    f'<span style="font-size:17px;font-weight:600;color:var(--fg1);margin-left:10px">{E(b)}</span></div>'
                    f'<div style="font-size:14px;margin-top:4px">{md(c)}</div></div>' for i, (a, b, c) in enumerate(items))
    return f'<div class="col" style="{w}{alto}gap:0;border-top:1.5px solid var(--fg1)">{filas}</div>'


def tarjeta_cifra(cifra, unidad, titulo, texto, visual="", apilada=False, tam_cifra=None):
    """Tarjeta con una cifra que hace de etiqueta del mensaje. Lateral: cifra y unidad a la izquierda, separador,
    título y texto a la derecha. Apilada: cifra grande arriba, texto y un visual pequeño opcional debajo.
    Cuándo usarlo: lecturas de apoyo junto a una gráfica (columna derecha) o tres o cuatro datos de contexto de mercado.
    Cuándo no: como adorno; si la cifra no se puede explicar o no tiene origen, no va. Sin números de orden decorativos."""
    if apilada:
        tc = f' style="font-size:{tam_cifra}px"' if tam_cifra else ""
        mt = "6px 0 14px" if visual else "6px 0 0"
        return (f'<div class="card" style="flex:1;padding:20px 22px;display:flex;flex-direction:column;justify-content:center">'
                f'<div class="big"{tc}>{E(cifra)}</div>' + (f'<h4 style="margin:6px 0 0">{E(titulo)}</h4>' if titulo else "")
                + f'<div style="margin:{mt}">{md(texto)}</div>{visual}</div>')
    return (f'<div class="card" style="flex:1;display:flex;align-items:center;gap:18px;padding:12px 20px">'
            f'<div style="width:104px;flex:none"><div class="big" style="font-size:{tam_cifra or 30}px;white-space:nowrap">{E(cifra)}</div>'
            f'<div style="font-size:13px;color:var(--fg3);margin-top:5px">{E(unidad)}</div></div>'
            f'<div style="flex:1;border-left:1px solid var(--border-2);padding-left:18px"><h4 style="margin:0 0 5px">{E(titulo)}</h4>'
            f'<div style="font-size:14px;line-height:1.45">{md(texto)}</div></div></div>')


def tarjeta_kpi(numero, titulo, valor, referencia="", medida="", validacion="", visual="", destacada=False,
                rotulo_validacion="Validación"):
    """Tarjeta de KPI: número, título, valor objetivo, referencia, un visual pequeño y cómo se valida.
    destacada: borde rojo y cifra roja (los que deciden el Go o No-Go); si no, cifra en negro.
    Cuándo usarlo: métricas de éxito y criterios de un Stage-Gate, de 2 a 4 tarjetas.
    Cuándo no: para KPIs de seguimiento con serie temporal (usa cifra_delta)."""
    cab = (f'<div class="nhead" style="margin:0"><span class="nb">{E(numero)}</span><div><h4 style="margin:0">{E(titulo)}</h4>'
           + (f'<div style="font-size:13px;color:var(--fg3);margin-top:2px">{E(medida)}</div>' if medida and destacada else "") + '</div></div>')
    val = f'<div class="mB-val"><b>{E(rotulo_validacion)}:</b> {md(validacion)}</div>' if validacion else ""
    if destacada:
        return (f'<div class="mB-c hot">{cab}<div style="display:flex;align-items:center;gap:24px;flex:1">'
                f'<div style="width:205px;flex:none"><div class="big" style="font-size:31px;white-space:nowrap">{E(valor)}</div>'
                f'<div style="font-size:14px;color:var(--fg2);margin-top:4px">{E(referencia)}</div></div>{visual}</div>{val}</div>')
    return (f'<div class="mB-c">{cab}<div style="display:flex;align-items:center;gap:20px">'
            f'<div style="width:230px;flex:none"><div class="big" style="font-size:26px;white-space:nowrap;color:var(--fg1)">{E(valor)}</div>'
            + (f'<div style="font-size:13px;color:var(--fg2);margin-top:4px">{E(referencia)}</div>' if referencia else "")
            + f'</div><div style="flex:1">{visual}</div></div>{val}</div>')


def panel_kpi(principales, secundarios, rotulo_principales, rotulo_secundarios):
    """Panel de KPI en dos filas: arriba los que deciden (tarjeta_kpi destacada) y abajo las condiciones.
    principales y secundarios: listas de dict con los argumentos de tarjeta_kpi.
    Cuándo usarlo: la slide de métricas de éxito de un proyecto con Stage-Gate.
    Cuándo no: si todas las métricas pesan igual (una sola fila de tarjetas)."""
    fila = lambda xs, d: "".join(tarjeta_kpi(**x, destacada=d) for x in xs)
    return ('<div style="width:100%;align-self:stretch;display:flex;flex-direction:column;gap:6px">'
            f'<p class="mB-l">{E(rotulo_principales)}</p><div class="row" style="gap:16px;flex:1.1">{fila(principales, True)}</div>'
            f'<p class="mB-l g" style="margin-top:18px">{E(rotulo_secundarios)}</p><div class="row" style="gap:16px;flex:1">{fila(secundarios, False)}</div></div>')


def fila_parametros(items, color=None):
    """Fila de parámetros técnicos en teselas rojas con texto blanco, centrados en vertical.
    items: [(rótulo, valor, nota | "")].
    Cuándo usarlo: las condiciones de partida de un reto (temperatura, pH, viscosidad), de 3 a 6 valores.
    Cuándo no: para resultados o KPIs (usa tarjeta_kpi); el rojo pleno pesa mucho, una fila por slide como máximo."""
    bg = color or "var(--red)"
    return ('<div class="row" style="gap:12px">' + "".join(
        f'<div style="flex:1;background:{bg};border-radius:16px;padding:12px 16px;min-height:96px;display:flex;flex-direction:column;justify-content:center;color:#fff">'
        f'<span style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;opacity:.85;margin-bottom:6px;line-height:1.3">{E(a)}</span>'
        f'<div style="font-size:19px;font-weight:700;line-height:1.15">{E(b)}</div>'
        + (f'<div style="font-size:13px;margin-top:4px;opacity:.9">({E(c)})</div>' if c else "") + '</div>' for a, b, c in items) + '</div>')


def cifra_delta(cifra, rotulo, variacion=None, comparacion="", valores=None, sube=True, tono="bueno", W=250):
    """Tarjeta de KPI de seguimiento: rótulo, cifra grande, chip de variación y minilínea opcional.
    variacion: texto del chip («+12 %»); comparacion: contra qué («vs 2025»); valores: serie para la minilínea.
    Cuándo usarlo: filas de 3 o 4 KPI de seguimiento en una slide de situación o de resultados.
    Cuándo no: KPI de un Stage-Gate con umbral y validación (usa tarjeta_kpi)."""
    chip = (f'<div style="display:flex;align-items:center;gap:8px;margin-top:8px">{delta(variacion, sube, tono)}'
            f'<span style="font-size:12px;color:var(--fg3)">{E(comparacion)}</span></div>') if variacion else ""
    sp = f'<div style="margin-top:12px">{sparkline(valores, W - 40, 30)}</div>' if valores else ""
    return (f'<div class="card" style="width:{W}px;flex:none"><span class="k2">{E(rotulo)}</span>'
            f'<div class="big" style="color:var(--fg1)">{E(cifra)}</div>{chip}{sp}</div>')


def icono_dato(items, W=520, horizontal=False):
    """Fila de datos con icono: icono en caja, cifra en rojo y una línea de lectura.
    items: [(icono, cifra, texto)], de 2 a 4. horizontal: en fila, repartidos a lo ancho.
    Cuándo usarlo: datos de contexto en el lateral o la cabecera de un bloque (mercado, equipo, alcance).
    Cuándo no: si las cifras se comparan entre sí (usa columnas)."""
    dir_ = "display:grid;grid-template-columns:repeat(%d,1fr);" % len(items) if horizontal else "display:flex;flex-direction:column;"
    return (f'<div style="{dir_}gap:14px;width:{W}px">' + "".join(
        f'<div style="display:flex;align-items:center;gap:14px">{icono_caja(ic, 24, caja=46, radio=12)}'
        f'<b style="font-size:24px;color:var(--red);{"" if horizontal else "width:92px;"}flex:none;letter-spacing:-.02em">{E(c)}</b>'
        f'<span style="font-size:14px;line-height:1.4;color:var(--fg2)">{md(t)}</span></div>' for ic, c, t in items) + '</div>')
