"""embudo_canonico: generador SVG del embudo de discos apilados de Eatable Adventures.

Diseño aprobado el 07-10-2026: escalones de ancho fijo (no proporcionales a
los valores), rampa de rojos de oscuro a claro, insignia numerada con flecha a la izquierda y etiquetas alineadas
a la derecha; máximo 5 etapas más un objetivo discontinuo. Su RAMP es la rampa canónica de rojos de ea_elementos.

Integrado en ea_elementos en Terracotta V2 (01-11-2026), desde pptx/funnel.py, al retirar la capa de PowerPoint
(archivada en 04. Archivos/Terracotta V1 - PowerPoint (archivado 01-11-2026)/, con la spec original en components.md).
Para slides se usa X.embudo(), que lo envuelve. Sin imports relativos: también se puede importar suelto.

    from embudo_canonico import funnel_svg
    svg = funnel_svg([("Universo", "empresas únicas", 63), ("Contactadas", "95% del universo", 60)],
                     goal=("Finalistas", "objetivo a 23-10", "2 a 3"), key=1)   # key: etapa clave en negrita
"""
import html

RAMP = ["#7A1217", "#A3201E", "#BC2D29", "#DE5A55", "#EFA39F"]   # relleno, oscuro a claro
RIM  = ["#5A0C10", "#80171A", "#9C231F", "#C23F3B", "#DC8581"]   # elipse superior (borde)
TXT  = ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#5A0C10"]   # número dentro del disco
RED, GRAPHITE, MIST, INK, FG3 = "#BC2D29", "#6B6B6B", "#D9D4CE", "#1E1E1E", "#857B72"

CX, MAXW, MINW = 265, 340, 120        # eje del embudo y anchos (px, lienzo 800 de ancho)
H, RY, PITCH = 68, 10, 80             # alto del disco, radio vertical de la elipse, paso entre discos
LABEL_X = 504                         # columna de etiquetas
W = 800


def _t(x, y, txt, size, weight, fill, anchor="start", ls=None):
    """Texto SVG con estilos en línea (los CSS de página con `svg text{...}` no deben poder pisarlos)."""
    sp = f"letter-spacing:{ls}px;" if ls is not None else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'style="font-family:Rubik,Inter,Helvetica Neue,Arial,sans-serif;font-size:{size}px;font-weight:{weight};fill:{fill};{sp}">{html.escape(str(txt))}</text>')


def _palette_idx(n):
    """Reparte los 5 tonos de la rampa entre n etapas (n <= 5), de oscuro a claro."""
    if n == 1:
        return [0]
    return [round(i * 4 / (n - 1)) for i in range(n)]


def funnel_svg(stages, goal=None, key=None, label_size=15, sub_size=12):
    """stages: lista de (nombre, subtítulo, valor), de mayor a menor. goal: (nombre, subtítulo, texto) opcional.
    label_size y sub_size: tamaño de las etiquetas en unidades del lienzo de 800 (opcional, 28-10-2026,
    las sube cuando el funnel se muestra reducido junto a texto de cuerpo)."""
    n = len(stages)
    assert 2 <= n <= 5, "Máx. 5 etapas coloreadas (+1 objetivo). Si hay más, dividir en dos funnels."
    step = min(44, (MAXW - MINW) / (n - 1))
    idx = _palette_idx(n)
    dot_x = CX + MAXW / 2 + 16
    out = []
    total = n + (1 if goal else 0)
    for i in range(total):
        y = 2 + i * PITCH
        is_goal = i >= n
        cy = y + H / 2 + 4
        if not is_goal:
            name, sub, val = stages[i]
            k = idx[i]
            wt = MAXW - step * i
            wb = wt * 0.93
            l, r, l2, r2 = CX - wt / 2, CX + wt / 2, CX - wb / 2, CX + wb / 2
            yb = y + H - RY
            out.append(f'<path d="M{l:.1f},{y+RY} L{l2:.1f},{yb} A{wb/2:.1f},{RY} 0 0 0 {r2:.1f},{yb} L{r:.1f},{y+RY} Z" fill="{RAMP[k]}"/>')
            out.append(f'<ellipse cx="{CX}" cy="{y+RY}" rx="{wt/2:.1f}" ry="{RY}" fill="{RIM[k]}"/>')
            out.append(_t(CX, y+H/2+13, val, 24, 700, TXT[k], "middle", -0.5))
            bfill, btxt, bstroke = RAMP[k], TXT[k] if k == 4 else "#FFFFFF", "none"
        else:
            name, sub, val = goal
            wt = 112
            l, r = CX - wt / 2, CX + wt / 2
            out.append(f'<rect x="{l:.1f}" y="{y+14}" width="{wt}" height="{H-22}" rx="8" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/>')
            out.append(_t(CX, y+H/2+11, val, 19, 700, RED, "middle"))
            bfill, btxt, bstroke = "#FFFFFF", RED, RED
        # insignia numerada + flecha gris
        out.append(f'<rect x="0" y="{cy-13:.1f}" width="26" height="26" fill="{bfill}" stroke="{bstroke}" stroke-width="1.5"/>')
        out.append(_t(13, round(cy+5,1), i+1, 14, 600, btxt, "middle"))
        out.append(f'<polygon points="30,{cy-12:.1f} 64,{cy-12:.1f} 78,{cy:.1f} 64,{cy+12:.1f} 30,{cy+12:.1f}" fill="{GRAPHITE}"/>')
        # conector: guía punteada hasta una columna fija de puntos, y línea a la etiqueta
        out.append(f'<line x1="{r+8:.1f}" y1="{cy:.1f}" x2="{dot_x:.1f}" y2="{cy:.1f}" stroke="{MIST}" stroke-dasharray="2 3"/>')
        out.append(f'<circle cx="{dot_x:.1f}" cy="{cy:.1f}" r="3.2" fill="{GRAPHITE}"/>')
        out.append(f'<line x1="{dot_x+4:.1f}" y1="{cy:.1f}" x2="{LABEL_X-14}" y2="{cy:.1f}" stroke="{GRAPHITE}"/>')
        wgt = 700 if (key is not None and i == key) else 600
        out.append(_t(LABEL_X, round(cy-2*label_size/15,1), name, label_size, wgt, INK))
        out.append(_t(LABEL_X, round(cy+15*sub_size/12,1), sub, sub_size, 400, FG3))
    h = 2 + total * PITCH
    return (f'<svg viewBox="0 0 {W} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" '
            f'style="font-family:Rubik,Inter,Helvetica Neue,Arial,sans-serif;overflow:visible">' + "".join(out) + '</svg>')

