"""Marcas y apoyo: micro piezas para celdas, tarjetas y márgenes.

Familia 12 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (
    E, FG1, FG2, FG3, FG4, FILL, HEAT, INPUT, Lienzo, PAPER, RAMP, RED, TINT, VALIDACION, YELLOW, _svg,
    circle, line, md, mezcla,
)

__all__ = ["chip_nota", "leyenda", "delta", "harvey", "marca", "semaforo", "barra_progreso", "valoracion", "etiqueta_evidencia", "llave", "separador"]


def chip_nota(nota, rampa=None):
    """Nota de 0 a 3 (o None = NE) en la rampa de la matriz; un aro marca la confianza baja ('B' o 'NE').
    nota = (valor | None, confianza)."""
    rampa = rampa or HEAT
    v, cf = nota
    base = ("display:inline-flex;align-items:center;justify-content:center;width:30px;height:22px;border-radius:6px;"
            "font-size:13px;font-weight:600;position:relative;flex:none;")
    if v is None:
        return f'<span style="{base}background:var(--paper);box-shadow:inset 0 0 0 1px {INPUT};color:{FG4};font-size:11px">NE</span>'
    aro = (f'<i style="position:absolute;top:3px;right:3px;width:5px;height:5px;border-radius:9px;box-shadow:inset 0 0 0 1.1px '
           f'{FG1 if v < 2 else "#fff"};background:{PAPER if v < 2 else "transparent"}"></i>' if cf in ("B", "NE") else "")
    return f'<span style="{base}background:{rampa[v]};color:{FG1 if v < 2 else "#fff"}">{v}{aro}</span>'


def leyenda(items, gap=18):
    """Leyenda en línea. items: [(color, rótulo, forma)] con forma 'cuadro', 'linea', 'discontinua' o 'punto'.
    Cuándo usarlo: solo cuando la etiqueta directa no cabe (dos o más series en un mismo gráfico).
    Cuándo no: si se puede rotular cada serie al final de su línea o dentro de su barra."""
    def marca(c, f):
        if f == "linea":
            return f'<i style="display:inline-block;width:18px;height:3px;border-radius:2px;background:{c}"></i>'
        if f == "discontinua":
            return f'<i style="display:inline-block;width:18px;border-top:2px dashed {c}"></i>'
        if f == "marca":
            return f'<i style="display:inline-block;width:3px;height:14px;background:{c}"></i>'
        if f == "punto":
            return f'<i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{c}"></i>'
        return f'<i style="display:inline-block;width:12px;height:12px;border-radius:3px;background:{c}"></i>'
    return (f'<div style="display:flex;flex-wrap:wrap;gap:6px {gap}px;font-size:13px;color:var(--fg2);align-items:center">' + "".join(
        f'<span style="display:inline-flex;align-items:center;gap:7px">{marca(c, f[0] if f else "cuadro")}{E(r)}</span>'
        for c, r, *f in items) + '</div>')


def _con_leyenda(grafico, items):
    return f'<div style="display:flex;flex-direction:column;gap:12px;flex:none">{leyenda(items)}{grafico}</div>'


def delta(texto_, sube=True, tono="bueno"):
    """Chip de variación con flecha (▲ sube, ▼ baja, = sin cambio si sube es None). tono: 'bueno' (verde),
    'neutro' (gris) o 'malo' (rojo).
    El tono lo decide el significado, no la dirección: bajar el azúcar es bueno aunque la flecha baje.
    Cuándo usarlo: junto a una cifra, para dar el cambio frente al periodo anterior o al objetivo.
    Cuándo no: sin un punto de comparación explícito («vs 2025»)."""
    bg, fg = {"bueno": (mezcla(VALIDACION, "#FFFFFF", .86), VALIDACION), "neutro": (FILL, FG2), "malo": (TINT, RED)}[tono]
    return (f'<span style="display:inline-flex;align-items:center;gap:4px;background:{bg};color:{fg};border-radius:999px;'
            f'padding:3px 9px;font-size:13px;font-weight:700;white-space:nowrap">{"=" if sube is None else ("▲" if sube else "▼")} {E(texto_)}</span>')


def harvey(nivel, tam=18, color=RED):
    """Bola de Harvey: nivel de 0 a 4 (vacía, un cuarto, media, tres cuartos, llena).
    Cuándo usarlo: grado de cumplimiento cualitativo en tablas comparativas.
    Cuándo no: si hay un valor numérico que se pueda dar (da la cifra)."""
    r = tam / 2
    s = circle(r, r, r - 1, PAPER, color, 1.5)
    if nivel >= 4:
        s += circle(r, r, r - 1, color)
    elif nivel > 0:
        a1 = -math.pi / 2 + 2 * math.pi * nivel / 4
        x1, y1 = r + (r - 1) * math.cos(a1), r + (r - 1) * math.sin(a1)
        s += f'<path d="M{r},{r} L{r},1 A{r - 1},{r - 1} 0 {1 if nivel > 2 else 0} 1 {x1:.2f},{y1:.2f} Z" fill="{color}"/>'
    return f'<span style="display:inline-block;vertical-align:middle;line-height:0">{_svg(tam, tam, s)}</span>'


def marca(tipo, tam=20):
    """Marca de cumplimiento para tablas: 'si' (check verde), 'parcial' (media luna roja), 'no' (aspa gris)
    o 'nd' (guion, sin dato).
    Cuándo usarlo: tablas de características o de cumplimiento de requisitos.
    Cuándo no: si el matiz importa (usa harvey o texto)."""
    r = tam / 2
    if tipo == "si":
        s = circle(r, r, r, mezcla(VALIDACION, "#FFFFFF", .86)) + f'<path d="M{r * .55:.1f},{r * 1.02:.1f} L{r * .88:.1f},{r * 1.35:.1f} L{r * 1.48:.1f},{r * .68:.1f}" fill="none" stroke="{VALIDACION}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    elif tipo == "parcial":
        s = circle(r, r, r - 1, PAPER, RED, 1.5) + f'<path d="M{r},1 A{r - 1},{r - 1} 0 0 0 {r},{tam - 1} Z" fill="{RED}"/>'
    elif tipo == "no":
        k = r * .42
        s = circle(r, r, r, FILL) + line(r - k, r - k, r + k, r + k, FG3, 1.8, cap="round") + line(r + k, r - k, r - k, r + k, FG3, 1.8, cap="round")
    else:
        s = line(r - 5, r, r + 5, r, FG4, 2, cap="round")
    return f'<span style="display:inline-block;vertical-align:middle;line-height:0">{_svg(tam, tam, s)}</span>'


def semaforo(estado, texto_=""):
    """Estado de seguimiento en tres niveles: 'ok' (verde), 'riesgo' (amarillo) y 'bloqueo' (rojo).
    Cuándo usarlo: estado de proyectos, hitos o requisitos en una tabla de seguimiento.
    Cuándo no: en entregables de contenido (el semáforo es de gestión, no de hallazgos)."""
    c, t = {"ok": (VALIDACION, "En plazo"), "riesgo": (YELLOW, "En riesgo"), "bloqueo": (RED, "Bloqueado")}[estado]
    return (f'<span style="display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:600;color:var(--fg1);'
            f'white-space:nowrap"><i style="width:10px;height:10px;border-radius:50%;background:{c};box-shadow:0 0 0 3px {mezcla(c, "#FFFFFF", .8)}"></i>{E(texto_ or t)}</span>')


def barra_progreso(valor, maximo, rotulo, cifra=None, W=260):
    """Barra de progreso con rótulo y cifra (avance de un hito, cobertura de una búsqueda).
    Cuándo usarlo: avance sobre un total conocido, en tarjetas o tablas.
    Cuándo no: si no hay un máximo real (sin denominador, la barra engaña)."""
    p = max(0, min(1, valor / maximo))
    return (f'<div style="width:{W}px"><div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px">'
            f'<span style="color:var(--fg2)">{E(rotulo)}</span><b style="color:var(--red)">{E(cifra or f"{round(p * 100)} %")}</b></div>'
            f'<div style="height:8px;background:var(--surface-fill);border-radius:99px;overflow:hidden">'
            f'<div style="width:{p * 100:.1f}%;height:100%;background:var(--red);border-radius:99px"></div></div></div>')


def valoracion(n, de=5, tam=10):
    """Puntos de valoración (n de 5) en rojo y gris.
    Cuándo usarlo: una nota cualitativa compacta dentro de una ficha o una tabla.
    Cuándo no: si la escala no es ordinal o hay decimales (da la cifra)."""
    return ('<span style="display:inline-flex;gap:4px;vertical-align:middle">' + "".join(
        f'<i style="width:{tam}px;height:{tam}px;border-radius:50%;background:{RED if i < n else INPUT}"></i>' for i in range(de)) + '</span>')


def etiqueta_evidencia(nivel, texto_=""):
    """Etiqueta de nivel de evidencia: A (verificada en fuente primaria), B (fuente secundaria fiable) o
    C (indicio o declaración). Regla: B y C se aceptan si van etiquetadas.
    Cuándo usarlo: junto a cada dato de un informe de vigilancia o una ficha.
    Cuándo no: en slides de síntesis para dirección (se explica una vez y se omite)."""
    st = {"A": f"background:{RAMP[0]};color:#fff", "B": f"background:{RAMP[3]};color:#fff", "C": f"background:#fff;color:{RED};box-shadow:inset 0 0 0 1.5px {RAMP[3]}"}[nivel]
    t = texto_ or {"A": "Verificado", "B": "Fuente secundaria", "C": "Indicio"}[nivel]
    return (f'<span style="display:inline-flex;align-items:center;gap:7px;font-size:13px;color:var(--fg2)">'
            f'<b style="{st};width:20px;height:20px;border-radius:5px;display:inline-flex;align-items:center;justify-content:center;font-size:12px">{nivel}</b>{E(t)}</span>')


def llave(alto, texto_, W=260, lado="derecha"):
    """Llave (corchete curvo) que agrupa varios elementos y les pone una lectura común.
    Cuándo usarlo: junto a una lista o un grupo de barras, para decir qué tienen en común.
    Cuándo no: si el grupo ya tiene un contenedor visible."""
    m = alto / 2
    d = f"M2,2 Q12,2 12,14 V{m - 10} Q12,{m} 22,{m} Q12,{m} 12,{m + 10} V{alto - 14} Q12,{alto - 2} 2,{alto - 2}"
    L = Lienzo(W, alto).add(f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="2" stroke-linecap="round"/>')
    L.div(32, m, W - 32, f'<span style="font-size:14px;line-height:1.4;color:var(--fg1)">{md(texto_)}</span>', va="middle")
    return L.render()


def separador(numero, titulo, texto_="", W=520):
    """Separador de bloque dentro de una slide: número grande en rojo, título y una línea.
    Cuándo usarlo: dividir una slide densa en dos o tres bloques numerados.
    Cuándo no: como portadilla de sección (esa es una slide propia)."""
    return (f'<div style="display:flex;align-items:center;gap:16px;width:{W}px;border-bottom:1.5px solid var(--fg1);padding-bottom:10px">'
            f'<b style="font-size:44px;line-height:1;color:var(--red);letter-spacing:-.03em">{E(numero)}</b>'
            f'<div><b style="font-size:16px;color:var(--fg1)">{E(titulo)}</b>'
            + (f'<div style="font-size:13px;color:var(--fg3)">{md(texto_)}</div>' if texto_ else "") + '</div></div>')
