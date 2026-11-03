"""
EA funnel (stacked discs): canonical SVG generator.
Design approved 07-10-2026. Use it for EVERY funnel (scouting, pipeline, conversion).
Full spec in charts/funnel.md.

The code has one home: presentaciones/ea_elementos/embudo_canonico.py. This file only re-exports it, so the
funnel in the core and the one used in decks can never drift apart.

Usage:
    from funnel import funnel_svg
    svg = funnel_svg([("Universe", "unique companies", 63), ("Contacted", "95% of the universe", 60), ...],
                     goal=("Finalists", "target by 23-10", "2 to 3"), key=3)
    # `key` = 0-based index of the key stage, its label is set in weight 700.
Run `python3 funnel.py` to regenerate funnel.html (specimen) next to the script.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "presentaciones" / "ea_elementos"))
from embudo_canonico import RAMP, funnel_svg  # noqa: E402,F401


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
