"""Tablas: comparar en filas y columnas.

Familia 13 de ea_elementos. Cada función devuelve un fragmento HTML de tamaño fijo, sin JavaScript.
Qué elegir para cada mensaje: taxonomia.py y «Taxonomía de elementos.md».
"""
import math

from .base import (
    BORDER2, E, FG1, FG2, FG3, FG4, FILL, GREY, HEAT, INPUT, Lienzo, NEUTRO, PAPER, RED, _impacto,
    circle, fmt, icono, icono_caja, lin, line, md, rect, text,
)
from .fichas import (tarjeta_actor)
from .marcas import (harvey, marca)

from .base import (RAMP, TINT, mezcla, sobre)  # añadidos el 01-11-2026

__all__ = ["tabla_referencia", "tabla_grafica", "matriz_puntuacion", "scorecard", "tabla_vigilancia", "tabla_comparativa", "tabla_con_barras", "tabla_drivers", "panel_entrevistas", "matriz_portfolio"]


def _barra_ref(v, dominio, objetivo, referencia, w=170, h=22):
    s = lin(dominio[0], dominio[1], 0, w)
    out = [rect(0, 7, w, 8, FILL, rx=4)]
    if v is not None:
        out.append(rect(0, 7, s(v), 8, FG2 if v < referencia else RED, rx=4))
    out += [line(s(objetivo), 0, s(objetivo), h, RED, 1.5, dash="3 2"), line(s(referencia), 2, s(referencia), h - 2, FG3, 2)]
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible;display:block">{"".join(out)}</svg>'


def tabla_referencia(cabeceras, filas, col_barra, dominio, objetivo, referencia, nota=""):
    """Tabla con una columna de barra pequeña frente a un objetivo (rojo discontinuo) y una referencia (gris);
    la barra sale roja si supera la referencia. La leyenda va en la cabecera de esa columna.
    cabeceras: [str] sin la columna de barra; filas: [{"celdas": [str], "valor": número | None}];
    col_barra: posición de la barra; objetivo y referencia = (valor, texto). La primera celda va en negrita (nombre);
    en el resto, **negrita** solo para los datos directos.
    Cuándo usarlo: lo ya probado por familia, con su mejor resultado y por qué se paró; de 4 a 8 filas.
    Cuándo no: si la tabla tiene más de 5 columnas de texto o si la barra no aporta (tabla sin barra)."""
    ley = ('<div style="display:flex;flex-direction:column;gap:4px;text-transform:none;letter-spacing:0;font-weight:500;font-size:12px;color:var(--fg2)">'
           + "".join(f'<span style="display:inline-flex;align-items:center;gap:8px"><svg width="4" height="14" style="flex:none">'
                     f'<line x1="2" y1="0" x2="2" y2="14" stroke="{c}" stroke-width="{sw}"{d}/></svg>{E(t)}</span>'
                     for c, sw, d, t in ((RED, 1.5, ' stroke-dasharray="3 2"', objetivo[1]), (FG3, 2, "", referencia[1])))
           + '</div>')
    cab = list(map(E, cabeceras))
    cab.insert(col_barra, ley)
    th = "".join(f"<th>{c}</th>" for c in cab)
    trs = ""
    for f in filas:
        tds = [f'<td class="{"nm" if i == 0 else "dt"}">{md(c)}</td>' for i, c in enumerate(f["celdas"])]
        tds.insert(col_barra, f'<td style="width:180px">{_barra_ref(f.get("valor"), dominio, objetivo[0], referencia[0])}</td>')
        trs += f"<tr>{''.join(tds)}</tr>"
    return (f'<div style="flex:1"><table class="tb"><thead><tr style="vertical-align:bottom">{th}</tr></thead><tbody>{trs}</tbody></table>'
            + (f'<p class="gris it">{md(nota)}</p>' if nota else "") + '</div>')


def tabla_grafica(filas, rotulos=("Total", "% libre", "Destacados"), leyenda=("Libre", "No libre"), nota="", lateral="", W=1152, H=410):
    """Tabla gráfica de tres columnas visuales: barra absoluta (neutra), barra 100% partida (gris = parte libre,
    rojo = el resto) y círculo proporcional con la cifra destacada en rojo. A la derecha, un panel lateral (HTML)
    alineado con la tabla, para la ficha del caso que pesa.
    filas: [(código, nombre, total, pct_libre, destacados)].
    Cuándo usarlo: de 5 a 12 categorías con volumen, proporción y un recuento clave (patentes por territorio, cartera).
    Cuándo no: si solo hay una métrica (usa barras_objetivo); las columnas de texto no llevan escala de color."""
    L = Lienzo(W, H)
    xb, wb = 312, 150
    xp, wp = xb + wb + 60, 180
    xi = xp + wp + 84
    mx = max(f[2] for f in filas)
    mxa = max(f[4] for f in filas) or 1
    s = lin(0, mx, 0, wb)
    rh, y0 = 31, 34
    for x, lab, an in ((xb, rotulos[0], "start"), (xp, rotulos[1], "start"), (xi, rotulos[2], "middle")):
        L.add(text(x, 16, lab.upper(), 12, 700, FG3, an, ls=1.1))
    for k, (cod, nom, tot, pct, alto) in enumerate(filas):
        y = y0 + k * rh
        cy = y + rh / 2
        L.add(line(0, y + rh, xi + 44, y + rh, BORDER2))
        L.div(0, cy, xb - 16, f'<b style="color:var(--red)">{E(cod)}</b> {E(nom)}', va="middle", style="font-size:14px;color:var(--fg1)")
        L.add(rect(xb, cy - 6, max(s(tot), 2), 12, FG3, rx=3), text(xb + max(s(tot), 2) + 6, cy + 4.5, tot, 13, 500, FG1))
        L.add(rect(xp, cy - 6, wp, 12, RED, rx=3), rect(xp, cy - 6, wp * pct / 100, 12, GREY, rx=3))
        L.add(text(xp + wp + 8, cy + 4.5, f"{fmt(pct)}%", 13, 400, FG2))
        if alto:
            L.add(circle(xi - 14, cy, 3 + 9 * math.sqrt(alto / mxa), RED), text(xi + 4, cy + 4.5, alto, 14, 700, RED))
        else:
            L.add(text(xi + 4, cy + 4.5, "0", 14, 500, FG3))
    yl = y0 + len(filas) * rh + 14
    L.add(rect(xp, yl, 12, 12, GREY, rx=3), text(xp + 18, yl + 10, leyenda[0], 12, 400, FG2),
          rect(xp + 80, yl, 12, 12, RED, rx=3), text(xp + 98, yl + 10, leyenda[1], 12, 400, FG2))
    if nota:
        L.div(0, yl + 26, xi + 44, md(nota), style="font-size:13px;color:var(--fg3)")
    if lateral:
        L.div(xi + 70, 0, W - xi - 70, lateral)
    return L.render()


def matriz_puntuacion(filas, dimensiones, grupos, extra=("Extra", ""), total=("Total", "sobre 100"), grupo_foco=None,
                      leyenda=("No evaluable", "Confianza baja (sin marca: alta o media)"), W=1152, H=430, rh=28):
    """Mapa de calor de una matriz de puntuación: filas agrupadas por veredicto, notas de 0 a 3 en la rampa de rojos,
    NE en blanco discontinuo, solo la confianza baja marcada (aro) y total a la derecha.
    filas: [{"codigo", "nombre", "notas": {dim: (nota | None, conf)}, "extra", "total"}]; conf en 'A', 'M', 'B' o 'NE'.
    dimensiones: [(clave, etiqueta corta)], con la clave también impresa en la cabecera (dos o tres letras); grupos: [(veredicto, [códigos])]; extra = (clave, etiqueta) de una columna
    informativa que no suma (None para quitarla); grupo_foco: el veredicto que va en rojo (por defecto, el primero).
    Cuándo usarlo: de 6 a 14 opciones por 6 a 11 criterios, cuando hay que enseñar el porqué de la prioridad.
    Cuándo no: con menos de 6 opciones (usa mapa_calor o tabla_comparativa), con menos de 4 criterios (usa una tabla) o sin confianza que mostrar (mapa_calor)."""
    L = Lienzo(W, H)
    foco = grupo_foco or grupos[0][0]
    wname = 420
    x5 = wname
    xd = x5 + 74 if extra else wname
    cw, cg = 50, 6
    xt = xd + len(dimensiones) * (cw + cg) + 18
    rg, y0 = 5, 46
    if extra:
        L.add(text(x5 + 30, 18, extra[0], 12, 700, FG1, "middle"), text(x5 + 30, 33, extra[1], 11, 400, FG3, "middle"))
    for j, (d, lab) in enumerate(dimensiones):
        x = xd + j * (cw + cg) + cw / 2
        L.add(text(x, 18, d, 12, 700, FG1, "middle"), text(x, 33, lab, 11, 400, FG3, "middle"))
    L.add(text(xt + 30, 18, total[0], 12, 700, FG1, "middle"), text(xt + 30, 33, total[1], 11, 400, FG3, "middle"))
    porcod = {f["codigo"]: f for f in filas}
    y = y0
    for gi, (glab, cods) in enumerate(grupos):
        if gi:
            L.add(line(0, y + 3, xt + 60, y + 3, BORDER2))
            y += 10
        hh = len(cods) * (rh + rg) - rg
        es_foco = glab == foco
        L.div(0, y + hh / 2, 150, f'<b style="font-size:13px;color:{RED if es_foco else FG2}">{E(glab)}</b>', va="middle")
        for c in cods:
            f = porcod[c]
            L.div(160, y + rh / 2, wname - 170, f'<b style="color:var(--red)">{E(f["codigo"])}</b> {E(f["nombre"])}', va="middle",
                  style="font-size:13px;color:var(--fg1);line-height:1.15")
            if extra:
                L.add(text(x5 + 30, y + rh / 2 + 4, f.get("extra", ""), 13, 400, FG2, "middle"))
            for j, (d, _) in enumerate(dimensiones):
                x = xd + j * (cw + cg)
                cx_, cy_ = x + cw / 2, y + rh / 2
                v, cf = f["notas"][d]
                if v is None:
                    L.add(rect(x + .5, y + .5, cw - 1, rh - 1, PAPER, rx=6, stroke=INPUT, dash="3 3"))
                    L.add(text(cx_, cy_ + 3.5, "NE", 10, 600, FG4, "middle"))
                    continue
                L.add(rect(x, y, cw, rh, HEAT[v], rx=6))
                L.add(text(cx_, cy_ + 4.5, v, 14, 600, FG1 if v < 2 else "#fff", "middle"))
                if cf in ("B", "NE"):
                    L.add(circle(x + cw - 7, y + 7, 2.6, PAPER, FG1 if v < 2 else "#fff", 1.1))
            L.add(text(xt + 30, y + rh / 2 + 5, f["total"], 15, 700, RED if es_foco else FG1, "middle"))
            y += rh + rg
    yl = H - 16
    lx = 0
    L.add(text(lx, yl + 10, "Nota", 12, 700, FG3)); lx += 38
    for v in range(4):
        L.add(rect(lx, yl, 24, 14, HEAT[v], rx=3), text(lx + 12, yl + 11, v, 11, 600, FG1 if v < 2 else "#fff", "middle"))
        lx += 28
    lx += 14
    L.add(rect(lx + .5, yl + .5, 23, 13, PAPER, rx=3, stroke=INPUT, dash="2 2"), text(lx + 12, yl + 10.5, "NE", 10, 600, FG4, "middle"),
          text(lx + 30, yl + 10, leyenda[0], 12, 400, FG3)); lx += 130
    L.add(circle(lx + 4, yl + 6, 2.6, "none", FG1, 1.1), text(lx + 12, yl + 10, leyenda[1], 12, 400, FG3))
    return L.render()


def scorecard(eliminatorios, comparativos, iconos=("warning", "rate_review"), rotulos=("Criterios eliminatorios", "Criterios comparativos")):
    # comparativos admite dimensiones (nombre, peso, [(criterio, peso)]) y, con más de 8 criterios sueltos, pasa a tres columnas (03-11-2026)
    """Scorecard en dos bloques: criterios eliminatorios numerados y criterios comparativos con su peso en barra
    sobre 100%; cada bloque en dos columnas con filas compartidas y el hueco libre abajo a la derecha.
    eliminatorios: [(criterio, explicación)] (explicación puede ir vacía); comparativos: [(criterio, peso)] o, para agrupar,
    [(dimensión, peso, [(criterio, peso)])]; los pesos deben sumar 100.
    Cuándo usarlo: el filtro de evaluación de candidatos de un scouting o programa (EA lo usa en casi todos).
    Cuándo no: para enseñar resultados de la evaluación (usa matriz_puntuacion)."""
    por_dimension = bool(comparativos) and len(comparativos[0]) == 3
    assert sum(c[1] for c in comparativos) == 100, "los pesos comparativos deben sumar 100"
    if por_dimension:
        for dim, peso, subs in comparativos:
            assert sum(w for _, w in subs) == peso, f"los criterios de {dim} deben sumar {peso}"
    el = [(f'<div class="el"><b>{i + 1}. {E(t)}:</b> {E(x)}</div>' if x else f'<div class="el"><b>{i + 1}. {E(t)}</b></div>')
          for i, (t, x) in enumerate(eliminatorios)]
    if por_dimension:
        maximo = max(w for _, _, subs in comparativos for _, w in subs)
        cols = "".join(
            f'<div style="min-width:0"><div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.5px solid var(--fg1);padding-bottom:5px;margin-bottom:8px">'
            f'<b style="font-size:15px;color:var(--fg1)">{E(d)}</b><b style="font-size:20px;color:var(--red)">{p}%</b></div>'
            + "".join(f'<div style="margin-bottom:6px"><div style="font-size:13px;line-height:1.2;color:var(--fg2);margin-bottom:2px">{E(t)}</div>'
                      f'<div style="display:flex;align-items:center;gap:8px"><div class="cr-t" style="height:7px"><i style="width:{w / maximo * 100:.0f}%"></i></div>'
                      f'<span style="width:30px;text-align:right;font-size:13px;font-weight:700;color:var(--fg1)">{w}%</span></div></div>' for t, w in s)
            + '</div>' for d, p, s in comparativos)
        # sin explicaciones, los filtros caben en cuatro columnas y dejan el alto para las dimensiones
        c_el = 4 if not any(x for _, x in eliminatorios) else 2
        n_el = math.ceil(len(el) / c_el)
        filas_el = "".join(f'<div style="grid-column:{i // n_el + 2};grid-row:{i % n_el + 1};align-self:start">{x}</div>' for i, x in enumerate(el))
        bloque_el = (f'<div class="sc-b" style="grid-template-columns:40px repeat({c_el},1fr);column-gap:24px;grid-template-rows:repeat({n_el},auto);row-gap:5px;padding-top:9px;padding-bottom:9px">'
                     f'<div class="sc-i" style="grid-column:1;grid-row:1/{n_el + 1}">{icono(iconos[0], 34, RED)}</div>{filas_el}</div>') if el else ""
        return ((f'<div class="sc">' + (f'<div class="sc-h">{E(rotulos[0])}</div>{bloque_el}' if el else ""))
                + f'<div class="sc-h">{E(rotulos[1])}</div><div class="sc-b" style="flex:1;grid-template-columns:48px 1fr;column-gap:24px;align-items:center;padding-top:10px;padding-bottom:6px">'
                  f'<div class="sc-i">{icono(iconos[1], 48, RED)}</div>'
                  f'<div style="display:grid;grid-template-columns:repeat({len(comparativos)},minmax(0,1fr));column-gap:28px">{cols}</div></div></div>')
    co = [f'<div class="cr"><b>{E(t)}</b><div class="cr-b"><div class="cr-t"><i style="width:{w}%"></i></div><span>{w}%</span></div></div>'
          for t, w in comparativos]
    tres = len(comparativos) > 8

    def bloque(ic, items, flex):
        if tres and items is co:
            corte3 = math.ceil(len(items) / 3)
            trozos = [items[:corte3], items[corte3:2 * corte3], items[2 * corte3:]]
            n3 = max(len(t) for t in trozos)
            cel = "".join(f'<div style="grid-column:{c + 2};grid-row:{i + 1};align-self:start">{x}</div>' for c, t in enumerate(trozos) for i, x in enumerate(t))
            return (f'<div class="sc-b" style="flex:{flex};grid-template-columns:56px 1fr 1fr 1fr;column-gap:28px;grid-template-rows:repeat({n3},1fr);row-gap:8px">'
                    f'<div class="sc-i" style="grid-column:1;grid-row:1/{n3 + 1}">{icono(ic, 48, RED)}</div>{cel}</div>')
        corte = math.ceil(len(items) / 2)
        izq, der = items[:corte], items[corte:]
        n = max(len(izq), len(der))
        celdas = "".join(f'<div style="grid-column:{c};grid-row:{i + 1};align-self:start">{x}</div>'
                         for c, lista in ((2, izq), (3, der)) for i, x in enumerate(lista))
        return (f'<div class="sc-b" style="flex:{flex};grid-template-rows:repeat({n},1fr);row-gap:10px">'
                f'<div class="sc-i" style="grid-column:1;grid-row:1/{n + 1}">{icono(ic, 48, RED)}</div>{celdas}</div>')
    return (f'<div class="sc"><div class="sc-h">{E(rotulos[0])}</div>{bloque(iconos[0], el, 0.85)}'
            f'<div class="sc-h">{E(rotulos[1])}</div>{bloque(iconos[1], co, 1.15)}</div>')


def tabla_vigilancia(filas, cabeceras=("Opción", "Por qué se vigila", "Qué la haría subir"), cabecera_panel="Ejemplos",
                     nota_panel="", vacio="Ningún actor identificado: es un hallazgo", rotulo_actor="Producto"):
    """Tabla de vigilancia: por qué no se prioriza ahora, el disparador que la haría subir y, en un panel gris claro
    a la derecha, los actores en tarjetas compactas con logo.
    filas: [{"codigo", "nombre", "porque", "disparador", "actores": [dict de tarjeta_actor]}]; sin actores sale `vacio`.
    Cuándo usarlo: la prioridad baja de una recomendación, de 3 a 6 filas, con un disparador claro por fila.
    Cuándo no: para la prioridad alta (necesita su propia slide); si no hay disparador, no es vigilancia, es descarte."""
    panel = "background:var(--surface-fill);padding:5px 8px;"
    vac = (f'<div style="flex:1;border-radius:12px;border:1px dashed var(--fg4);padding:8px 12px;font-size:13px;color:var(--fg3);'
           f'display:flex;align-items:center">{E(vacio)}</div>')
    trs = "".join(
        f'<tr><td class="nm" style="width:168px"><b>{E(f["codigo"])}</b> {E(f["nombre"])}</td><td style="width:240px">{md(f["porque"])}</td>'
        f'<td style="width:196px;color:var(--fg1)">{md(f["disparador"])}</td>'
        f'<td style="{panel}border-bottom:2px solid #fff"><div style="display:flex;gap:8px">'
        f'{"".join(tarjeta_actor(**{"rotulo": rotulo_actor, **a}, compacta=True) for a in f.get("actores", [])) or vac}</div></td></tr>'
        for f in filas)
    nota = f'<span style="font-weight:400;text-transform:none;letter-spacing:0;margin-left:6px">{E(nota_panel)}</span>' if nota_panel else ""
    return (f'<table class="tb" style="font-size:14px"><thead><tr>{"".join(f"<th>{E(c)}</th>" for c in cabeceras)}'
            f'<th style="background:var(--surface-fill);padding:8px 10px;border-radius:12px 12px 0 0">{E(cabecera_panel)}{nota}</th></tr></thead>'
            f'<tbody>{trs}</tbody></table>')


def tabla_comparativa(columnas_, filas, destacada=None, W=520, ancho_criterio=180):
    """Tabla comparativa de opciones por criterio, con la columna recomendada sombreada en gris cálido.
    columnas_: nombres de las opciones; filas: [(criterio, [valores])], donde cada valor es 'si', 'no',
    'parcial', 'nd', un entero de 0 a 4 (bola de Harvey) o un texto corto.
    Cuándo usarlo: comparar 2 a 5 opciones en 4 a 10 criterios cualitativos.
    Cuándo no: si los criterios tienen pesos y notas (usa matriz_puntuacion)."""
    def celda(v):
        if v in ("si", "no", "parcial", "nd"):
            return marca(v)
        if isinstance(v, int):
            return harvey(v)
        return f'<span style="font-size:13px">{md(v)}</span>'
    hd = "".join(f'<th style="text-align:center;padding-top:8px;{f"color:{FG1};background:{FILL};border-radius:8px 8px 0 0;" if j == destacada else ""}">{E(c)}</th>'
                 for j, c in enumerate(columnas_))
    cuerpo = "".join(
        f'<tr><td class="nm" style="width:{ancho_criterio}px">{E(cr)}</td>' + "".join(
            f'<td style="text-align:center;{f"background:{FILL};" if j == destacada else ""}">{celda(v)}</td>' for j, v in enumerate(vals)) + '</tr>'
        for cr, vals in filas)
    return f'<table class="tb" style="width:{W}px"><thead><tr><th></th>{hd}</tr></thead><tbody>{cuerpo}</tbody></table>'


def tabla_con_barras(cabeceras, filas, col_valor, destacado=None, unidad="", W=520, ancho_barra=120, H=None):
    """Tabla con una barra en la columna numérica (y la cifra al lado), para leer y comparar a la vez.
    filas: [[celdas]]; col_valor: índice de la columna numérica; destacado: índice de fila en rojo. H: alto total (reparte las filas).
    Cuándo usarlo: rankings con varias columnas de texto (empresa, país, tipo) y una magnitud.
    Cuándo no: si hay objetivo y referencia por fila (usa tabla_referencia)."""
    mx = max(f[col_valor] for f in filas)
    def cel(i, j, v):
        if j == col_valor:
            c = RED if i == destacado else NEUTRO
            return (f'<td><div style="display:flex;align-items:center;gap:8px"><div style="width:{ancho_barra}px;height:10px;background:var(--light-grey)">'
                    f'<div style="width:{v / mx * 100:.1f}%;height:100%;background:{c}"></div></div>'
                    f'<b style="font-size:13px;color:{RED if i == destacado else FG1}">{fmt(v)}{E(unidad)}</b></div></td>')
        return f'<td class="{"nm" if j == 0 else ""}"{" style=\"color:var(--red)\"" if j == 0 and i == destacado else ""}>{E(str(v))}</td>'
    hd = "".join(f"<th>{E(c)}</th>" for c in cabeceras)
    cuerpo = "".join("<tr>" + "".join(cel(i, j, v) for j, v in enumerate(f)) + "</tr>" for i, f in enumerate(filas))
    return f'<table class="tb" style="width:{W}px;{f"height:{H}px;" if H else ""}"><thead><tr>{hd}</tr></thead><tbody>{cuerpo}</tbody></table>'


def tabla_drivers(filas, periodos=("Histórico", "Previsión"), W=1100):
    """Tabla de drivers de mercado: por driver, su grupo, la fuerza (bola de Harvey), una descripción y el impacto
    en cada periodo con flecha en círculo (verde sube, gris estable, rojo baja).
    filas: [dict(grupo, driver, fuerza 0 a 4, texto, impactos=[nivel por periodo de -2 a 2])].
    Cuándo usarlo: resumen de tendencias de un informe de vigilancia o de una slide de mercado.
    Cuándo no: con menos de 4 drivers (usa icono_dato)."""
    grupos = []
    for d in filas:
        if grupos and grupos[-1][0] == d["grupo"]:
            grupos[-1][1] += 1
        else:
            grupos.append([d["grupo"], 1])
    span, out, k = {}, [], 0
    for g, n in grupos:
        span[k] = (g, n)
        k += n
    for i, d in enumerate(filas):
        gc = (f'<td rowspan="{span[i][1]}" style="width:110px;background:var(--surface-fill);font-weight:700;color:var(--fg1);font-size:13px;'
              f'vertical-align:middle;border-bottom:2px solid #fff">{E(span[i][0])}</td>') if i in span else ""
        imp = "".join(f'<td style="text-align:center">{_impacto(n)}</td>' for n in d["impactos"])
        out.append(f'<tr>{gc}<td class="nm">{E(d["driver"])}</td><td style="text-align:center">{harvey(d["fuerza"], 18)}</td>'
                   f'<td>{md(d["texto"])}</td>{imp}</tr>')
    hd = "<th>Grupo</th><th>Driver</th><th style='text-align:center'>Fuerza</th><th>Descripción</th>" + "".join(f"<th style='text-align:center'>{E(p)}</th>" for p in periodos)
    ley = ('<div style="display:flex;gap:16px;align-items:center;font-size:12px;color:var(--fg3);margin-top:8px">'
           + "".join(f'<span style="display:inline-flex;gap:5px;align-items:center">{_impacto(n, 16)}{t}</span>' for n, t in
                     ((2, "Impulsa mucho"), (1, "Impulsa"), (0, "Neutro"), (-1, "Frena"), (-2, "Frena mucho"))) + '</div>')
    return f'<div style="width:{W}px"><table class="tb"><thead><tr>{hd}</tr></thead><tbody>{"".join(out)}</tbody></table>{ley}</div>'


def panel_entrevistas(filas, perspectivas, W=1100):
    """Panel de entrevistas: arriba, cuántas entrevistas hay por perspectiva (icono y cifra); debajo, la tabla con
    cada entrevistado (perfil anonimizado, organización, perspectiva, país y fecha).
    filas: [dict(perfil, organizacion, perspectiva, pais, fecha)]; perspectivas: {nombre: icono}.
    Cuándo usarlo: documentar la base de una investigación primaria (llamadas a candidatos, expertos, clientes).
    Cuándo no: si las entrevistas no se pueden mostrar ni anonimizadas (da solo el recuento)."""
    cuenta = {p: sum(1 for f in filas if f["perspectiva"] == p) for p in perspectivas}
    res = "".join(f'<div style="display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--border-1);border-radius:12px;padding:10px 14px;flex:1">'
                  f'{icono_caja(ic, 22, caja=42)}<div><b style="font-size:24px;color:var(--red);line-height:1">{cuenta[p]}</b>'
                  f'<div style="font-size:13px;color:var(--fg2)">{E(p)}</div></div></div>' for p, ic in perspectivas.items())
    tot = (f'<div style="display:flex;align-items:center;gap:12px;background:var(--fg1);border-radius:12px;padding:10px 16px;color:#fff">'
           f'<b style="font-size:24px;line-height:1">{len(filas)}</b><span style="font-size:13px">entrevistas<br>en total</span></div>')
    hd = "<th>Nº</th><th>Perfil</th><th>Organización</th><th>Perspectiva</th><th>País</th><th>Fecha</th>"
    cuerpo = "".join(f'<tr><td style="color:var(--fg3)">{i + 1:02d}</td><td class="nm">{E(f["perfil"])}</td><td>{E(f["organizacion"])}</td>'
                     f'<td><span style="display:inline-flex;align-items:center;gap:6px">{icono(perspectivas[f["perspectiva"]], 18, RED)}{E(f["perspectiva"])}</span></td>'
                     f'<td>{E(f["pais"])}</td><td><span class="nw">{E(f["fecha"])}</span></td></tr>' for i, f in enumerate(filas))
    return (f'<div style="width:{W}px;display:flex;flex-direction:column;gap:14px"><div style="display:flex;gap:10px">{tot}{res}</div>'
            f'<table class="tb"><thead><tr>{hd}</tr></thead><tbody>{cuerpo}</tbody></table></div>')


def matriz_portfolio(filas, max_items=3, W=540, ancho_rotulo=110, vacio="Sin producto"):
    """Mapa de portfolio: una fila por vía o segmento (rótulo en rojo claro) con los productos del actor en esa vía;
    si hay más de max_items, una píldora «+N». Sin productos, «Sin producto» en gris.
    filas: [(vía, [producto o (producto, detalle)])].
    Cuándo usarlo: qué ofrece cada competidor por vía de administración, aplicación o canal, en fichas hermanas.
    Cuándo no: para comparar varios actores en las mismas vías (usa tabla_comparativa o mapa_calor)."""
    fondo = RAMP[3]
    out = []
    for via, items in filas:
        vis = items[:max_items]
        extra = len(items) - len(vis)
        cel = []
        for it in vis:
            nomb, det = (it, "") if isinstance(it, str) else it
            det_html = f'<br><span style="color:var(--fg3)">{E(det)}</span>' if det else ""
            cel.append(f'<span style="display:inline-flex;align-items:center;gap:6px;min-width:0;flex:1"><i style="flex:none;width:12px;height:12px;border-radius:50%;'
                       f'background:{TINT};box-shadow:inset 0 0 0 1.5px {mezcla(RED, "#FFFFFF", .45)}"></i>'
                       f'<span style="font-size:12px;line-height:1.2;color:var(--fg1)"><b style="font-weight:600">{E(nomb)}</b>{det_html}</span></span>')
        if extra:
            cel.append(f'<span style="flex:none;font-size:11px;font-weight:700;color:var(--red);background:{TINT};border-radius:99px;padding:3px 8px">+{extra}</span>')
        cuerpo = "".join(cel) or f'<span style="font-size:12px;color:var(--fg4)">{E(vacio)}</span>'
        out.append(f'<div style="display:flex;min-height:42px"><div style="width:{ancho_rotulo}px;flex:none;background:{fondo};color:{sobre(fondo)};font-size:13px;'
                   f'font-weight:700;display:flex;align-items:center;padding:0 12px">{E(via)}</div>'
                   f'<div style="flex:1;min-width:0;display:flex;align-items:center;gap:10px;padding:6px 12px;border:1px solid var(--border-1);border-left:0">{cuerpo}</div></div>')
    return f'<div style="width:{W}px;display:flex;flex-direction:column;gap:4px">{"".join(out)}</div>'
