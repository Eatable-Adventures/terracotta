# Funnel (stacked discs), canonical design

**Approved 07-10-2026.** Use this design for every funnel (scouting, pipeline, conversion), not rounded bands or horizontal bars. Generator: `charts/funnel.py` (`funnel_svg(stages, goal, key)`), specimen: `charts/funnel.html`, catalogue card: `preview/chart-funnel.html`.

- **Shape:** stacked, centred discs (truncated cones) with a darker top ellipse as the rim and a curved base. Height 68px, ellipse vertical radius 10px, pitch between discs 80px.
- **Non-proportional steps:** width drops a fixed step per stage (340px at the top, 44px step), never as a function of the value. Numbers and conversion % are the real ones; the drawing is only visual hierarchy.
- **Colour:** one-hue ramp, reds from dark to light (`#7A1217`, `#A3201E`, `#BC2D29`, `#DE5A55`, `#EFA39F`), rim one tone darker. Number in white (on the lightest stage, burgundy `#5A0C10`). **Documented exception** to the chart relevance hierarchy in `DESIGN.md` §Charts, because the stages are sequential.
- **Disc number:** Rubik 700, 24px, centred on the visible part of the body (lowered from the geometric centre so it does not collide with the ellipse).
- **Left:** square numbered badge (1 to n) in the disc colour, plus a grey `#6B6B6B` pentagonal arrow.
- **Right:** dotted guide to a fixed column of grey dots, then a line to the label column. Two-line label: name (Rubik 600, 15px; 700 on the key stage) and subtitle (12px, `--fg3`) with the % over the previous stage and the detail.
- **Goal:** optional last row with a dashed Crimson box (2px) and Crimson text, no fill, and its badge with a Crimson border.
- **Limits:** at most 5 coloured stages plus 1 goal. If there are more, split into two funnels. No shadows or gradients.
- **In a slide:** funnel on the left (about 800px of 1280), reading panel on the right (secondary-metrics card plus a strategic-implication callout).

The ramp is available as tokens in `colors_and_type.css` (`--ramp-1` to `--ramp-5`). The code lives in `presentaciones/ea_elementos/embudo_canonico.py`; `charts/funnel.py` re-exports it. In a slide, use `ea_elementos.embudo()`.
