# Presentaciones HTML (slide format)

Fixed base for Eatable Adventures HTML presentations, built to export to PDF. This folder fixes **three pieces that are not redesigned in each deck**: the cover, the content-slide header and the closing. Everything else is built on top with Terracotta variables (`colors_and_type.css`).

## What is here

| File | Purpose |
|---|---|
| `ea_deck.py` | Library: `portada()`, `cabecera()`, `slide()`, `cierre()`, `documento()`. Everything is embedded in base64 (self-contained HTML, no network). Reads tokens from `../colors_and_type.css`. |
| `generar_fondo_portada.py` | Regenerates `assets/cover-background.png` from the Terracotta tokens (`--burgundy`, `--red`, `--orange`, `--yellow`). |
| `assets/cover-background.png` | Cover background in the Terracotta palette (2048 × 1152). |
| `assets/logo-ea-cream.png` | Cream lockup with the "The Beating Heart of Food Innovation" line. |
| `assets/amber-glow.png` | Amber glow placed behind each slide title. |
| `assets/icon-lock.png` | Lock icon for "Private & Confidential". |
| `assets/logo-wordmark.svg` | Vector wordmark (top right and on the closing). |
| `assets/fonts/` | Rubik (variable, latin) and a Material Symbols Outlined subset. |

## Build a deck

```python
import sys
sys.path.insert(0, "presentaciones")   # path to this folder
import ea_deck

slides = [ea_deck.portada(linea1="Scope alignment", linea2="Client name",
                          subtitulo="Close the gap · From diagnosis to pilot",
                          realizado_para="Client name", equipo="Name Surname · Name Surname",
                          fecha="October 2026")]
body = ea_deck.cabecera("01. Section", 'Conclusion with a <span class="hl-red">red span</span>') + "<div>...content...</div>"
slides.append(ea_deck.slide(body, n=2, total=3, fuente="Source: ...", cliente="Client name"))
slides.append(ea_deck.cierre("Key message in one sentence.", "Client name"))
open("out.html", "w", encoding="utf-8").write(ea_deck.documento("Title", slides, css_extra=""))
```

The slide canvas is **1280 × 720 px** (`.slide`), `@page` margin 0. For funnels use `charts/funnel.py` and place the SVG in the slide body.

## Cover (L01)

Taken from the EA PowerPoint cover (10 × 5.625 in) and scaled to 1280 × 720 px (128 px per inch). Everything aligns on one vertical axis at x ≈ 2.5 in, to the right of the glow.

| Layer | Content | Position and size (px) |
|---|---|---|
| 1 | Background `cover-background.png`, full bleed | -8, -6 · 1300 × 732 |
| 2 | Cream logo | 315, 35 · 298 × 60 |
| 3 | Title, 2 lines, Rubik 700, 44px, sentence case (never uppercase), cream | 319, 200 · 836 wide |
| 4 | Subtitle, Rubik 400, 27px, cream | 319, 347 · 804 wide |
| 5 | 2 × 2 metadata, labels 700 at 12.5px and values 400 at 16px | columns at x = 323 and 689; rows at y = 481 and 548 |
| 6 | 1px white vertical line | 655, 486 · height 106 |
| 7 | Copyright 12.5px | 319, 672 |

- **Title:** line 1 = deliverable type; line 2 = client or project. About 22 characters per line at most; if it does not fit, shorten, do not shrink the size.
- **Subtitle:** one line, blocks separated by ` · `, sentence case, no final full stop.
- **Labels:** `Realizado para:`, `Date`, `Consultant Team`, `Classification`, value `Private & Confidential`. Kept as is (mixed languages on purpose, it is the brand template).
- **Date:** month with initial capital and year (`October 2026`).
- **Team:** the real people on the project.
- **Never on the cover:** photos, client logos, icons, illustrations, extra colours (only cream and white on burgundy), page number, section footer, action title, or a glow in front of the title.
- Never draw the cover with a CSS gradient or a solid fill: always `cover-background.png`.

## Content-slide header

- Grey eyebrow in sentence case with the section number (`01. Section`), and status pills to its right if needed.
- Title in semibold (600), with the concluding span in red bold (`.hl-red`). Two lines at most.
- Amber glow (`amber-glow.png`) to the left of the title, behind the text, never a solid dot.
- Wordmark logo top right. The title must not run under the logo.
- Footer: source on the left; on the right `Eatable Adventures · Confidencial · Solo para uso de {client} · n / total`.

## Closing

Left, white (40%): "Gracias." and a "Mensaje clave" callout (cream, 3px red border, one or two sentences). Right (60%): Terracotta brand gradient, "Let's Beat", wordmark and confidentiality line. Always the last slide, apart from a decision slide.

## Export to PDF and check

1. Chrome headless: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-sandbox --print-to-pdf=out.pdf --print-to-pdf-no-header-footer --no-pdf-header-footer --virtual-time-budget=15000 --run-all-compositor-stages-before-draw file:///path/out.html`
2. Count PDF pages against the slides in the HTML (duplicated pages appear if `@page` carries a margin).
3. Render every page to PNG and review it (overflow, logo against title, figures).
4. If a new icon is needed, regenerate the Material Symbols subset (`icon_names` in alphabetical order) with Google's CSS API and replace `assets/fonts/material-symbols-subset.woff2`.
