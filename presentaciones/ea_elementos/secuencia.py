"""Secuencia y tiempo: en qué orden y cuándo.

Familia 09 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math
import datetime

from .base import (
    BURG, CREAM, E, FG1, FG2, FG3, FG4, FILL, GREY, INPUT, LGREY, Lienzo, MESES, PAPER, RAMP, RED,
    VALIDACION, YELLOW, _arco, _bv, _rampa_pasos, _svg, arrow, calor, circle, head, icono, lin, line, md,
    mezcla, rampa, rect, sobre, text,
)

from .base import (oscuro)  # añadidos el 01-11-2026

__all__ = ["proceso_flechas", "lista_precedentes", "gantt", "chevrones", "linea_tiempo", "ciclo", "carriles", "escalones", "calendario_calor", "linea_tiempo_vertical", "proceso_carriles", "fases_gates"]


def _fecha(d):
    """Acepta datetime.date o 'DD-MM-YYYY'."""
    if isinstance(d, datetime.date):
        return d
    dd, mm, aa = (int(x) for x in d.split("-"))
    return datetime.date(aa, mm, dd)


def proceso_flechas(pasos, fases=None, destacado=None, rotulos=("Qué se resuelve", "Qué sale", "Quién"), W=1152):
    """Proceso en flechas encadenadas (rampa de rojos, de claro a oscuro) con una llave de fases encima y una tarjeta
    por paso: qué se resuelve (pregunta), qué sale y quién lo hace.
    pasos: [{"icono", "nombre", "pregunta", "sale", "quien"}], sin número en el nombre (numera sola); fases: [(primer paso, último paso, rótulo)] por índice;
    destacado: índice del paso con borde rojo (la decisión).
    Cuándo usarlo: un método de 3 a 5 pasos en el que importa quién hace qué y qué entrega cada paso.
    Cuándo no: si el proceso tiene ramas (usa arbol_tramite) o fechas (usa gantt); no dictar el protocolo del cliente."""
    n, gap = len(pasos), 16
    cw = (W - (n - 1) * gap) / n
    alto = 82 if fases else 60
    y0 = 26 if fases else 2
    L = Lienzo(W, alto)
    for i0, i1, txt in (fases or []):
        x0, x1 = i0 * (cw + gap), (W if i1 == n - 1 else (i1 + 1) * (cw + gap) - gap)
        L.add(line(x0 + 1, 12, x1 - 1, 12, FG4, 1.5), line(x0 + 1, 12, x0 + 1, 20, FG4, 1.5), line(x1 - 1, 12, x1 - 1, 20, FG4, 1.5))
        L.div((x0 + x1) / 2, 12, 320, f'<span style="background:var(--paper);padding:0 10px;font-size:13px;font-weight:600;color:var(--fg2)">{E(txt)}</span>',
              anchor="middle", va="middle")
    cols = _rampa_pasos(n)
    for k, p in enumerate(pasos):
        x0, a, h = k * (cw + gap), 16, 56
        xb = W - a if k == n - 1 else x0 + cw
        pts = [(x0, y0), (xb, y0), (xb + a, y0 + h / 2), (xb, y0 + h), (x0, y0 + h)] + ([(x0 + a, y0 + h / 2)] if k else [])
        tc = sobre(cols[k])
        L.add(f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts)}" fill="{cols[k]}"/>')
        L.div(x0 + (a if k else 0) + 16, y0 + h / 2, cw - 40, f'<div style="display:flex;gap:10px;align-items:center">{icono(p["icono"], 24, tc)}'
              f'<b style="font-size:16px;color:{tc}">{k + 1} · {E(p["nombre"])}</b></div>', va="middle")

    def tarjeta(k, p):
        hot = k == destacado
        return (f'<div class="card{" hot" if hot else ""}" style="flex:1;min-width:0;padding:14px 16px;display:flex;flex-direction:column;gap:6px;background:var(--paper)">'
                f'<span class="k2 {"red" if hot else ""}" style="margin:0">{E(rotulos[0])}</span>'
                f'<b style="font-size:15.5px;line-height:1.38;color:var(--fg1)">{E(p["pregunta"])}</b>'
                f'<div style="margin-top:auto;border-top:1px solid var(--border-2);padding-top:8px;display:flex;flex-direction:column;gap:6px">'
                f'<div><span class="k2" style="margin:0 0 2px">{E(rotulos[1])}</span><div style="font-size:14px;line-height:1.4;color:var(--fg1)">{md(p["sale"])}</div></div>'
                f'<div><span class="k2" style="margin:0 0 2px">{E(rotulos[2])}</span><div style="font-size:14px;line-height:1.4;color:var(--fg1)">{md(p["quien"])}</div></div></div></div>')
    return (f'<div class="col" style="flex:1;width:100%;gap:10px">{L.render()}'
            f'<div class="row" style="flex:1;width:100%;gap:{gap}px">{"".join(tarjeta(k, p) for k, p in enumerate(pasos))}</div></div>')


def lista_precedentes(items, titulo="Precedentes", ancho=330):
    """Lista cronológica de precedentes con icono de estado: favorable en el verde de validación (--validacion),
    desfavorable en gris. Una línea fina separa las filas y la última va sin línea.
    items: [(año, título, estado, favorable)].
    Cuándo usarlo: el historial de decisiones de un regulador, comité o cliente, de 4 a 8 entradas, junto a un árbol.
    Cuándo no: si no hay estado favorable o desfavorable (usa una lista simple); el verde no se usa para nada más."""
    return (f'<div class="col" style="width:{ancho}px;flex:none;gap:0;border-left:1px solid var(--border-1);padding-left:24px;align-self:center">'
            f'<span class="k2" style="margin:0 0 8px">{E(titulo)}</span>'
            + "".join(f'<div style="display:flex;gap:12px;align-items:center;padding:9px 0;{"border-bottom:1px solid var(--border-2)" if k < len(items) - 1 else ""}">'
                      f'<b style="width:40px;font-size:14px;color:var(--fg1)">{E(a)}</b>{icono("check_circle" if fav else "block", 22, VALIDACION if fav else FG4)}'
                      f'<div style="font-size:14px;line-height:1.3"><b style="color:var(--fg1)">{E(t)}</b><br><span style="color:{VALIDACION if fav else FG3}">{E(e)}</span></div></div>'
                      for k, (a, t, e, fav) in enumerate(items)) + '</div>')


def gantt(inicio, semanas, filas, hoy=None, decision=None, leyenda=None, ancho=978, ancho_rotulo=172):
    """Gantt por días: meses y semanas arriba, una fila por fase con barras (llena en rojo o pausa en crema oscuro),
    fechas clave bajo las barras, la línea de decisión con su píldora granate y la marca de «Hoy».
    inicio: fecha de la semana 1 (date o 'DD-MM-YYYY'); semanas: número de semanas; filas: [{"rotulo", "sub",
    "barras": [(desde, hasta, 'lleno' | 'pausa', texto)], "fechas": [(fecha, texto, 'inicio' | 'fin', dx)]}];
    hoy = (fecha, texto); decision = {"fecha", "titulo", "texto", "rotulo", "sub"} (añade su fila);
    leyenda: [(color css, texto, recto)].
    Cuándo usarlo: el cronograma de un proyecto de 8 a 30 semanas con 3 a 6 fases y una decisión.
    Cuándo no: para más de 6 filas o un plan de detalle por tareas (va en Excel o en el PM); sin fechas, usa proceso_flechas."""
    g0 = _fecha(inicio)
    ppd = ancho / (semanas * 7)
    fin = g0 + datetime.timedelta(days=semanas * 7 - 1)
    gx = lambda d: round((_fecha(d) - g0).days * ppd, 1)
    gxe = lambda d: round(((_fecha(d) - g0).days + 1) * ppd, 1)
    cols = f"grid-template-columns:{ancho_rotulo}px {ancho:g}px"

    def meses():
        out, d = [], g0
        while d <= fin:
            sig = datetime.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
            a, b = gx(d), gxe(min(sig - datetime.timedelta(days=1), fin))
            out.append(f'<div class="cg-mes" style="left:{a}px;width:{round(b - a, 1)}px">{MESES[d.month - 1]} {str(d.year)[2:]}</div>')
            d = sig
        return "".join(out)

    def rejilla():
        out = [f'<i class="cg-gl" style="left:{gx(g0 + datetime.timedelta(days=7 * k))}px"></i>' for k in range(semanas + 1)]
        d = g0
        while d <= fin:
            out.append(f'<i class="cg-gm" style="left:{gx(d)}px"></i>')
            d = datetime.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        return f'<div class="cg-grid">{"".join(out)}</div>'

    def barra(d1, d2, tipo, txt):
        cls = "pausa" if tipo == "pausa" else "prop"
        return f'<div class="cg-bar {cls}" style="left:{gx(d1)}px;width:{round(gxe(d2) - gx(d1), 1)}px;top:11px;height:24px">{E(txt)}</div>'

    def cap(f):
        d, t, modo, dx = (list(f) + ["inicio", 0])[:4] if len(f) < 4 else f
        if modo == "fin":
            return f'<span class="cg-cap r" style="left:{gxe(d)}px">{E(t)}</span>'
        return f'<span class="cg-cap" style="left:{round(gx(d) + dx, 1)}px">{E(t)}</span>'

    fila = lambda lab, sub, dentro: (f'<div class="cg-row" style="{cols}"><div class="cg-lab"><b>{E(lab)}</b>{E(sub)}</div>'
                                     f'<div class="cg-time">{rejilla()}{dentro}</div></div>')
    sems = "".join(f'<div class="cg-sem" style="left:{gx(g0 + datetime.timedelta(days=7 * (k - 1)))}px;width:{round(7 * ppd, 1)}px">{k}</div>'
                   for k in range(1, semanas + 1))
    cuerpo = "".join(fila(f["rotulo"], f.get("sub", ""), "".join(barra(*b) for b in f.get("barras", [])) + "".join(cap(c) for c in f.get("fechas", [])))
                     for f in filas)
    if decision:
        xd = round(gx(decision["fecha"]) + ppd / 2, 1)
        cuerpo += fila(decision.get("rotulo", "Decisión"), decision.get("sub", ""),
                       f'<div class="cg-pill" style="left:{round(xd + 14, 1)}px"><b>{E(decision["titulo"])}</b><span>{E(decision["texto"])}</span></div>')
        cuerpo += f'<div class="cg-dline" style="left:{xd}px;margin-left:{ancho_rotulo}px"><span class="dd"></span></div>'
    if hoy:
        cuerpo += (f'<div class="cg-hoy" style="left:{round(gx(hoy[0]) + ppd / 2, 1)}px;margin-left:{ancho_rotulo}px"><span class="pt"></span>'
                   f'<span class="tx">{E(hoy[1])}</span></div>')
    ley = ""
    if leyenda:
        ley = '<div class="cg-leg">' + "".join(f'<span><i class="sw" style="background:{c};{"border-radius:0" if recto else ""}"></i>{E(t)}</span>'
                                               for c, t, recto in leyenda) + '</div>'
    tabla = (f'<div class="cg"><div class="cg-head" style="{cols}"><div class="cg-lab"></div><div class="cg-time"><div class="cg-meses">{meses()}</div>'
             f'<div class="cg-sems">{sems}</div></div></div><div class="cg-body">{cuerpo}</div></div>')
    # con leyenda, un solo bloque: como hermanos, un contenedor en fila encogía el Gantt y lo cortaba (corregido el 03-11-2026)
    return f'<div style="flex:none;width:{ancho_rotulo + ancho:g}px">{tabla}{ley}</div>' if ley else tabla


def chevrones(pasos, activo=None, W=1100, alto=54, punta=20, H=None):
    """Chevrones de proceso: flechas encadenadas con el rótulo dentro y una explicación corta debajo.
    pasos: [(rótulo, texto)] o [(rótulo, texto, [puntos])]; activo: índice del paso actual (los anteriores en rojo claro, el actual en
    rojo y los siguientes en gris). Sin activo, rampa de rojos de claro a oscuro.
    H: sube el chevrón y el texto, y con puntos por paso gana alto, pero sigue siendo una pieza baja: para llenar una slide, proceso_flechas.
    Cuándo usarlo: un proceso lineal de 3 a 6 etapas, o dónde estamos dentro de él.
    Cuándo no: si cada etapa necesita más de dos líneas (usa proceso_flechas)."""
    n = len(pasos)
    tam, tam_rot, sep_txt = 13, 14, 12
    if H:
        alto = max(alto, min(110, int(H * .3)))
        tam, tam_rot, sep_txt = 15, 16, 20
    g = 6
    w = (W - g * (n - 1)) / n
    if activo is None:
        cols = _rampa_pasos(n)
    else:
        cols = [RAMP[4] if i < activo else (RED if i == activo else FILL) for i in range(n)]
    L = Lienzo(W, H or alto + 70)
    for i, (paso_, c) in enumerate(zip(pasos, cols)):
        r, tx, puntos = (tuple(paso_) + ([],))[:3]
        x0 = i * (w + g)
        pts = [(x0, 0), (x0 + w - punta, 0), (x0 + w, alto / 2), (x0 + w - punta, alto), (x0, alto)] + ([(x0 + punta, alto / 2)] if i else [])
        L.add(f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts)}" fill="{c}"/>')
        L.div(x0 + (punta if i else 10) + (w - punta - (punta if i else 10)) / 2, alto / 2, w - 2 * punta - 6,
              f'<b style="font-size:{tam_rot}px;color:{sobre(c)};line-height:1.2">{E(r)}</b>', anchor="middle", va="middle")
        L.div(x0 + (punta if i else 0) + 2, alto + sep_txt, w - punta - 8, f'<span style="font-size:{tam}px;line-height:1.4">{md(tx)}</span>'
              + "".join(f'<div style="display:flex;gap:8px;margin-top:10px;font-size:{tam - 1}px;line-height:1.35;color:var(--fg2)"><i style="flex:none;width:6px;height:6px;border-radius:50%;background:{RED};margin-top:7px"></i><span>{md(p)}</span></div>' for p in puntos))
    return L.render()


def linea_tiempo(hitos, hoy=None, W=1100, H=210):
    """Línea de tiempo horizontal con hitos alternos arriba y abajo; los pasados en negro, el de hoy con punto
    de luz y los futuros huecos.
    hitos: [(fecha, rótulo, texto)]; hoy: índice del hito actual.
    Cuándo usarlo: historia de un proyecto o calendario de hitos (5 a 9) sin duraciones.
    Cuándo no: si importan las duraciones y los solapes (usa gantt o carriles)."""
    n = len(hitos)
    ym = H / 2
    x = lin(0, n - 1, 70, W - 70)
    L = Lienzo(W, H)
    L.add(line(10, ym, W - 10, ym, FG4, 2))
    if hoy is not None:
        L.add(line(10, ym, x(hoy), ym, FG1, 3))
    for i, (fe, r, tx) in enumerate(hitos):
        cx = x(i)
        arriba = i % 2 == 0
        pasado = hoy is not None and i < hoy
        if hoy == i:
            L.add(circle(cx, ym, 13, YELLOW), circle(cx, ym, 7, RED))
        else:
            L.add(circle(cx, ym, 7, FG1 if pasado else PAPER, FG1 if pasado else FG3, 2))
        L.add(line(cx, ym + (-14 if arriba else 14), cx, ym + (-30 if arriba else 30), FG4, 1))
        cont = (f'<b style="font-size:12px;color:var(--red);letter-spacing:.04em">{md(fe)}</b>'
                f'<div style="font-size:14px;font-weight:600;color:var(--fg1);line-height:1.25">{E(r)}</div>'
                + (f'<div style="font-size:12px;line-height:1.35">{md(tx)}</div>' if tx else ""))
        L.div(cx, ym + (-34 if arriba else 34), 160, cont, anchor="middle", va="bottom" if arriba else "top")
    return L.render()


def ciclo(pasos, centro="", W=420, H=360):
    """Ciclo circular de 3 a 6 pasos con flechas entre ellos y un rótulo en el centro.
    pasos: [(icono, rótulo)].
    Cuándo usarlo: procesos que se repiten (mejora continua, ciclo de vida, rueda de innovación).
    Cuándo no: si el proceso tiene principio y fin (usa chevrones)."""
    cx, cy = W / 2, H / 2
    R = min(W, H) / 2 - 56
    n = len(pasos)
    L = Lienzo(W, H)
    angs = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
    hueco = 0.42
    for i in range(n):
        a0, a1 = angs[i] + hueco, angs[i] + 2 * math.pi / n - hueco
        L.add(f'<path d="{_arco(cx, cy, R, a0, a1)}" fill="none" stroke="{RAMP[3]}" stroke-width="3" stroke-linecap="round"/>')
        L.add(head(cx + R * math.cos(a1 + .04), cy + R * math.sin(a1 + .04), a1 + math.pi / 2 + .04, RAMP[3], 12))
    if centro:
        L.div(cx, cy, R * 1.2, f'<b style="font-size:15px;color:var(--fg1);line-height:1.25">{E(centro)}</b>', anchor="middle", va="middle")
    for i, (ic, r) in enumerate(pasos):
        x, y = cx + R * math.cos(angs[i]), cy + R * math.sin(angs[i])
        L.add(circle(x, y, 27, RED))
        L.div(x, y, 54, icono(ic, 26, "#fff"), anchor="middle", va="middle", style="line-height:0")
        c, sn = math.cos(angs[i]), math.sin(angs[i])
        if abs(c) < .3:
            L.div(x, y + (34 if sn > 0 else -34), 150, f'<b style="font-size:13px;color:var(--fg1)">{E(r)}</b>', anchor="middle",
                  va="top" if sn > 0 else "bottom")
        else:
            L.div(x + (34 if c > 0 else -34), y, 110, f'<b style="font-size:13px;color:var(--fg1);line-height:1.25">{E(r)}</b>',
                  anchor="start" if c > 0 else "end", va="middle")
    return L.render()


def carriles(carriles_, periodos, items, W=1100, ancho_rotulo=170, alto=56):
    """Hoja de ruta por carriles (swimlanes): un carril por equipo o línea de trabajo y periodos en columnas.
    carriles_: nombres; periodos: rótulos de columna (trimestres, horizontes); items: [(carril, desde, hasta,
    texto, destacado)] con desde y hasta en unidades de periodo (0 = inicio del primero; admite decimales).
    Cuándo usarlo: roadmap a 12 o 24 meses o horizontes H1, H2 y H3 con 3 a 6 carriles.
    Cuándo no: planificación semanal con dependencias (usa gantt)."""
    n = len(periodos)
    cw = (W - ancho_rotulo) / n
    H = 30 + alto * len(carriles_)
    cols = rampa(len(carriles_))
    L = Lienzo(W, H)
    for j, p in enumerate(periodos):
        x0 = ancho_rotulo + j * cw
        L.add(rect(x0 + 1, 0, cw - 2, 24, FILL, rx=6), text(x0 + cw / 2, 16, p, 12, 700, FG1, "middle", ls=.8))
        L.add(line(x0, 30, x0, H, GREY, 1))
    for i, c in enumerate(carriles_):
        y0 = 30 + i * alto
        L.add(line(0, y0, W, y0, GREY, 1))
        L.add(rect(0, y0 + 10, 4, alto - 20, cols[i], rx=2))
        L.div(14, y0 + alto / 2, ancho_rotulo - 20, f'<b style="font-size:14px;color:var(--fg1)">{E(c)}</b>', va="middle")
    L.add(line(0, H, W, H, GREY, 1))
    for ci, d, h, tx, hot in items:
        y0 = 30 + ci * alto + 10
        x0, x1 = ancho_rotulo + d * cw + 4, ancho_rotulo + h * cw - 4
        c = RED if hot else mezcla(cols[ci], "#FFFFFF", .68)
        L.add(rect(x0, y0, x1 - x0, alto - 20, c, rx=(alto - 20) / 2))
        L.div(x0 + 14, y0 + (alto - 20) / 2, x1 - x0 - 24, f'<span style="font-size:13px;font-weight:600;color:{sobre(c)};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block">{E(tx)}</span>', va="middle")
    return L.render()


def escalones(pasos, W=520, H=270):
    """Escalones ascendentes: etapas de madurez o de ambición que suben de izquierda a derecha.
    pasos: [(rótulo, texto)]; el último (la meta) en el rojo más oscuro.
    Cuándo usarlo: un modelo de madurez o un plan por fases donde cada fase se apoya en la anterior.
    Cuándo no: si las fases son paralelas (usa columnas de tarjetas)."""
    n = len(pasos)
    cols = list(reversed(rampa(n)))
    w = W / n
    L = Lienzo(W, H)
    for i, ((r, tx), c) in enumerate(zip(pasos, cols)):
        h = H * (.32 + .68 * (i + 1) / n) - 40
        x0, y0 = i * w, H - h
        L.add(_bv(x0 + 2, y0, w - 4, h, c, 8))
        L.div(x0 + 12, y0 + 12, w - 24, f'<b style="font-size:20px;color:{sobre(c)};opacity:.6">{i + 1:02d}</b>'
              f'<div style="font-size:14px;font-weight:700;color:{sobre(c)};margin-top:2px;line-height:1.2">{E(r)}</div>'
              f'<div style="font-size:12px;color:{sobre(c)};margin-top:4px;line-height:1.35">{md(tx)}</div>')
    return L.render()


def calendario_calor(inicio, valores, rotulo="", W=None, celda=13, sep=3):
    """Calendario de calor: un cuadro por día (columnas = semanas, filas = días de lunes a domingo),
    coloreado por actividad, con los meses arriba.
    inicio: 'DD-MM-YYYY' del primer valor; valores: un número por día (0 = sin actividad).
    Cuándo usarlo: ritmos de publicación, de producción o de entradas en un sistema a lo largo de meses.
    Cuándo no: menos de 8 semanas de datos (usa columnas por semana)."""
    d0 = _fecha(inicio)
    import datetime
    off = d0.weekday()
    mx = max(valores) or 1
    ncol = (off + len(valores) + 6) // 7
    izq, top = 26, 18
    Wt = izq + ncol * (celda + sep)
    s = []
    for k, nombre in ((0, "L"), (2, "X"), (4, "V")):
        s.append(text(0, top + k * (celda + sep) + celda - 2, nombre, 10, 400, FG3))
    mes_ant = None
    for i, v in enumerate(valores):
        p = off + i
        col, fila = p // 7, p % 7
        dia = d0 + datetime.timedelta(days=i)
        x0, y0 = izq + col * (celda + sep), top + fila * (celda + sep)
        s.append(rect(x0, y0, celda, celda, calor(v / mx) if v else FILL, rx=2.5))
        if dia.month != mes_ant and fila <= 3:
            s.append(text(x0, 11, MESES[dia.month - 1], 11, 700, FG2))
            mes_ant = dia.month
    Ht = top + 7 * (celda + sep) + 22
    leg = "".join(rect(Wt - 5 * (celda + sep) + k * (celda + sep), Ht - 14, celda, celda, calor(k / 4) if k else FILL, rx=2.5) for k in range(5))
    s.append(leg + text(Wt - 5 * (celda + sep) - 6, Ht - 4, "Menos", 10, 400, FG3, "end") + text(Wt + 2, Ht - 4, "Más", 10, 400, FG3))
    if rotulo:
        s.append(text(izq, Ht - 4, rotulo, 12, 400, FG2))
    return _svg(W or Wt + 30, Ht, "".join(s))


def linea_tiempo_vertical(hitos, hoy=None, W=520):
    """Línea de tiempo vertical: fecha a la izquierda, punto en la línea y título con texto largo a la derecha.
    hitos: [(fecha, título, texto)]; hoy: índice del hito actual (punto de luz).
    Cuándo usarlo: la historia de una empresa en una ficha, o hitos con más de una línea de explicación.
    Cuándo no: más de 7 hitos en una slide (usa linea_tiempo horizontal)."""
    filas = []
    for i, (fe, t, tx) in enumerate(hitos):
        pasado = hoy is not None and i < hoy
        if hoy == i:
            pt = f'<i style="width:13px;height:13px;border-radius:50%;background:{RED};box-shadow:0 0 0 5px {YELLOW}"></i>'
        else:
            pt = f'<i style="width:12px;height:12px;border-radius:50%;background:{FG1 if pasado else PAPER};box-shadow:inset 0 0 0 2px {FG1 if pasado else FG3}"></i>'
        ultimo = i == len(hitos) - 1
        linea_ = "" if ultimo else f'<span style="position:absolute;left:50%;top:16px;bottom:-6px;border-left:2px solid {FG1 if pasado else INPUT}"></span>'
        filas.append(f'<div style="display:flex;gap:14px;min-height:56px"><b style="width:86px;flex:none;text-align:right;font-size:13px;color:var(--red);padding-top:1px">{md(fe)}</b>'
                     f'<div style="position:relative;width:16px;flex:none;display:flex;justify-content:center;padding-top:3px">{pt}{linea_}</div>'
                     f'<div style="padding-bottom:12px"><b style="font-size:14px;color:var(--fg1)">{E(t)}</b>'
                     f'<div style="font-size:13px;line-height:1.4;color:var(--fg2);margin-top:2px">{md(tx)}</div></div></div>')
    return f'<div style="width:{W}px">{"".join(filas)}</div>'


def proceso_carriles(carriles_, pasos, flujos, columnas, W=1100, ancho_rotulo=130, alto=92, caja=(150, 46)):
    """Proceso por carriles (BPMN simple): pasos repartidos por responsable, con flechas entre carriles.
    pasos: [dict(id, carril, col, texto, tipo='tarea' | 'decision' | 'inicio' | 'fin', destacado=False)];
    flujos: [(id_origen, id_destino, rótulo)]; columnas: número de columnas.
    Cuándo usarlo: quién hace qué en un proceso con traspasos (homologar un proveedor, aprobar un claim).
    Cuándo no: procesos de un solo responsable (usa chevrones) o con más de 12 pasos."""
    cw = (W - ancho_rotulo) / columnas
    H = alto * len(carriles_)
    L = Lienzo(W, H)
    for i, c in enumerate(carriles_):
        L.add(rect(0, i * alto, W, alto, LGREY if i % 2 == 0 else PAPER), rect(0, i * alto, ancho_rotulo - 8, alto, FILL))
        L.div(14, i * alto + alto / 2, ancho_rotulo - 30, f'<b style="font-size:13px;color:var(--fg1)">{E(c)}</b>', va="middle")
    L.add(line(0, 0, W, 0, GREY, 1), line(0, H, W, H, GREY, 1))
    cw2, ch2 = caja[0] / 2, caja[1] / 2
    geo = {}
    for p in pasos:
        cx = ancho_rotulo + cw * (p["col"] + .5)
        cy = p["carril"] * alto + alto / 2
        tipo = p.get("tipo", "tarea")
        hw, hh = {"tarea": (cw2, ch2), "decision": (36, 34), "inicio": (13, 13), "fin": (13, 13)}[tipo]
        geo[p["id"]] = (cx, cy, hw, hh)
    for a, b, r in flujos:
        ax, ay, aw, ah = geo[a]
        bx, by, bw, bh = geo[b]
        if abs(ay - by) < 1:
            pts = [(ax + aw, ay), (bx - bw, by)]
            lx, ly = ax + aw + 6, ay - 6
        else:
            sg = 1 if by > ay else -1
            pts = [(ax, ay + sg * ah), (ax, by), (bx - bw, by)] if bx > ax + 1 else [(ax, ay + sg * ah), (bx, by - sg * bh)]
            lx, ly = ax + 6, ay + sg * (ah + 14)
        L.add(arrow(pts, FG2, 1.5, size=8))
        if r:
            L.add(text(lx, ly, r, 11, 700, FG2, halo=True))
    for p in pasos:
        cx, cy, hw, hh = geo[p["id"]]
        tipo = p.get("tipo", "tarea")
        hot = p.get("destacado")
        if tipo == "tarea":
            c = RED if hot else PAPER
            L.add(rect(cx - hw, cy - hh, 2 * hw, 2 * hh, c, rx=8, stroke=RED if hot else FG4, sw=1.2))
            L.div(cx, cy, 2 * hw - 14, f'<span style="font-size:12px;font-weight:600;line-height:1.25;color:{sobre(c)}">{E(p["texto"])}</span>', anchor="middle", va="middle")
        elif tipo == "decision":
            L.add(f'<polygon points="{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}" fill="{BURG}"/>')
            L.div(cx, cy, 2 * hw, f'<b style="font-size:11px;color:{CREAM}">{E(p["texto"])}</b>', anchor="middle", va="middle")
        else:
            L.add(circle(cx, cy, hw, PAPER if tipo == "inicio" else FG1, FG1, 2.5 if tipo == "inicio" else 0))
            L.div(cx, cy + hh + 4, 90, f'<span style="font-size:11px;color:var(--fg3)">{E(p["texto"])}</span>', anchor="middle")
    return L.render()


def fases_gates(fases, W=1100):
    """Fases en secuencia con su punto de parada: una línea con un punto por fase, la fase y su plazo, el título,
    lo que se hace y, al pie, el gate que hay que pasar para seguir. De claro a oscuro según se avanza.
    fases: [dict(nombre, plazo="", titulo, puntos=[...], gate)], de 2 a 4.
    Cuándo usarlo: próximos pasos con disciplina de decisión (validar demanda antes de invertir).
    Cuándo no: un calendario con fechas reales (usa gantt) o pasos sin punto de decisión (usa chevrones)."""
    n = len(fases)
    cols = rampa(n)[::-1]
    celdas = []
    for i, f in enumerate(fases):
        c = cols[i]
        flecha = (f'<i style="position:absolute;right:-4px;top:4px;width:0;height:0;border-left:7px solid {INPUT};border-top:5px solid transparent;border-bottom:5px solid transparent"></i>'
                  if i < n - 1 else "")
        celdas.append(f'<div style="position:relative;height:14px;margin-bottom:12px"><i style="position:absolute;left:0;right:{"-20px" if i < n - 1 else "0"};top:6px;height:2px;background:{INPUT}"></i>'
                      f'<i style="position:absolute;left:0;top:0;width:14px;height:14px;border-radius:50%;background:{c}"></i>{flecha}</div>')
    for i, f in enumerate(fases):
        celdas.append(f'<div style="font-size:12px;font-weight:700;color:{cols[i]};letter-spacing:.06em">{E(f["nombre"]).upper()}'
                      f'<span style="font-weight:400;color:var(--fg3);letter-spacing:0;margin-left:6px">{E(f.get("plazo", ""))}</span></div>')
    for i, f in enumerate(fases):
        celdas.append(f'<b style="display:block;font-size:15px;color:var(--fg1);padding:4px 0 8px;border-bottom:3px solid {cols[i]}">{E(f["titulo"])}</b>')
    for i, f in enumerate(fases):
        celdas.append('<div style="display:flex;flex-direction:column;gap:7px;padding:10px 0 12px">' + "".join(
            f'<div style="display:flex;gap:8px;font-size:13px;line-height:1.38;color:var(--fg2)"><i style="flex:none;width:6px;height:6px;border-radius:50%;'
            f'background:{cols[i]};margin-top:5px"></i><span>{md(p)}</span></div>' for p in f.get("puntos", [])) + '</div>')
    for i, f in enumerate(fases):
        c = cols[i]
        celdas.append(f'<div style="background:{mezcla(c, "#FFFFFF", .88)};box-shadow:inset 0 0 0 1px {mezcla(c, "#FFFFFF", .4)};border-radius:6px;padding:8px 12px;'
                      f'font-size:12px;font-weight:700;line-height:1.3;color:{c if oscuro(c) else FG1}">Gate: {md(f["gate"])}</div>')
    return f'<div style="width:{W}px;display:grid;grid-template-columns:repeat({n},1fr);column-gap:22px;align-items:start">{"".join(celdas)}</div>'
