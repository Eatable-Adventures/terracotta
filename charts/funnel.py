"""
EA funnel (stacked discs): canonical SVG generator.
Design approved 07-10-2026. Use it for EVERY funnel (scouting, pipeline, conversion).
Full spec in charts/funnel.md.

Usage:
    from funnel import funnel_svg
    svg = funnel_svg([("Universe", "unique companies", 63), ("Contacted", "95% of the universe", 60), ...],
                     goal=("Finalists", "target by 23-10", "2 to 3"), key=3)
    # `key` = 0-based index of the key stage, its label is set in weight 700.
Run `python3 funnel.py` to regenerate funnel.html (specimen) next to the script.
"""
import html, pathlib

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


def funnel_svg(stages, goal=None, key=None):
    """stages: lista de (nombre, subtítulo, valor), de mayor a menor. goal: (nombre, subtítulo, texto) opcional."""
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
        out.append(_t(LABEL_X, round(cy-2,1), name, 15, wgt, INK))
        out.append(_t(LABEL_X, round(cy+15,1), sub, 12, 400, FG3))
    h = 2 + total * PITCH
    return (f'<svg viewBox="0 0 {W} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" '
            f'style="font-family:Rubik,Inter,Helvetica Neue,Arial,sans-serif;overflow:visible">' + "".join(out) + '</svg>')


if __name__ == "__main__":
    demo = funnel_svg([("Detect", "startups identified", 240), ("Build", "40% of the previous", 96),
                       ("Test", "44% of the previous", 42), ("Scale", "43% of the previous", 18)],
                      goal=("Goal", "in 12 months", "25"), key=1)
    page = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>EA Funnel (specimen)</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&display=swap">
<style>body{{margin:0;padding:40px;font-family:Rubik,sans-serif;color:#1E1E1E;background:#fff}}.w{{max-width:820px}}
h1{{font-size:22px}}p{{font-size:13px;color:#574E48;max-width:70ch;line-height:1.5}}</style></head><body><div class="w">
<h1>EA funnel, stacked discs</h1>
<p>Canonical design approved 07-10-2026. Fixed-step widths (not proportional to the values), red ramp from dark to light, numbered badge with arrow on the left, dot column and aligned labels on the right. Max. 5 stages plus a dashed goal. Generator: <code>charts/funnel.py</code>. Spec: <code>charts/funnel.md</code>.</p>
{demo}</div></body></html>'''
    open(pathlib.Path(__file__).resolve().parent / "funnel.html", "w", encoding="utf-8").write(page)
    print("funnel.html generado")
