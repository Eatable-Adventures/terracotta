# Terracotta — the Eatable Adventures Design System

**Terracotta** is the reusable design system for **Eatable Adventures' apps and proprietary products**, adapted directly from the **2026 Brandbook** (brand refresh). *(Terracotta is the name of the system; Eatable Adventures is the brand it expresses.)* Eatable Adventures is the operating system for food innovation — accelerator, consultancy and fund in one — built to turn ambition into measurable business results.

This folder gives a design agent everything needed to produce on-brand interfaces, mockups, prototypes and slides: design tokens (color + Rubik type), a flexible grid, the brand assets, written tone/voice guidance, specimen cards, a brand foundations one-pager, and a ready-to-use app-shell template.

> **Brand: "The Beating Heart of Food Innovation."** From the heartbeat comes a visual system built on three ideas — **pulse, rhythm and impact**. It is warm, human and premium without arrogance. Type is **Rubik** (the only family), color is **EAV Red + warm creams**, surfaces are **rounded**, and energy is **contained**: red, the light point and gradients activate a composition without making it noisy.

---

## Brand intensity — restrained, intermediate, high

The identity is **not** applied the same way everywhere. There is an expression scale:

- **Restrained** — consulting, data pages, reports, **proprietary products & apps**. White, creams, Rubik, structure and subtle accents dominate; reading takes priority over the brand gesture.
- **Intermediate** — internal/sales decks, methodology pages. Photography, modules, dividers and a more visible use of the system.
- **High** — covers, campaigns, web heroes. Darker backgrounds, dominant red, hero photography, the main gradient, a strong claim.

**This system is tuned for the restrained end** (apps and product UI), with the higher-expression devices available for hero/brand moments. Lower the intensity as information density rises; raise it when a piece needs to position or sell.

---

## Design principles

1. **Operational clarity** — through typography and composition. Direct headlines, clean modules, clear hierarchy and enough air. Sophistication lies in judgment, not complexity.
2. **Contained energy** — through color and graphic elements. Intensity, but precise, not chaotic. The red, light point and gradients activate without noise.
3. **Real humanity** — through photography and tone. People, contexts, processes and decisions feel close, in action and tangible — never cold or abstract.

Together: **structure with movement**, a **premium presence without arrogance**. The brand does not shout, but it does not disappear either.

---

## VISUAL FOUNDATIONS

### Color — two mother colors, one warm system
The palette is born from **EAV Red** and **EAV Cream** and expands into a warm, functional set. Color is **structural, not decorative**, applied with a clear hierarchy.

- **EAV Red `#BC2D29`** — the brand's representative color: identity, active state, links, focus, CTAs. Used as a field or marker, never a soft tint.
- **White `#FFFFFF`** — the most predominant color; balances the gradients with cleanliness and air.
- **EAV Cream `#FFF9EE`** — highlighted/editorial blocks and product grounds.
- **EAV Black `#1E1E1E`** — footers and typography (primary text).
- **Secondary:** Dark Cream `#F5EACE` (secondary gradients), Light Grey `#FAFAFA` & Grey `#E8E8E8` (consulting blocks/dividers), **Yellow `#FFA103` (light point only)**, **Orange `#DE5533` (gradient transition only)**, **Burgundy `#450E14` (closings, CTAs, depth)**.
- **Warm text ramp (derived):** fg1 `#1E1E1E` · fg2 `#574E48` · fg3 `#857B72` · fg4 `#ABA197`.

Don't introduce colors outside the approved palette, don't use yellow/orange as hero colors outside the gradient, and don't oversaturate a piece with reds.

### Type — Rubik, and only Rubik
- **One family:** Rubik (Light 300 · Regular 400 · Medium 500 · Bold 700 · Extrabold 800 + italics). There is **no secondary typeface**. A system mono is kept *only* as a functional fallback for code/tabular data.
- **Headlines** are Rubik **Regular** with an initial capital, emphasis carried by a single **bold fragment** — and at most one word may turn **red** (headlines only). **Eyebrows** are Regular, UPPERCASE, tracked. **Body** is Regular with bold highlights; long-form moves to Light with Medium highlights.
- Hierarchy comes from **weight + size + position**, not from a second face. Paragraphs are left-aligned, never justified.
- **Scale (base 16):** 12 · 13 · 14 · 16 · 18 · 22 · 28 · 36 · 46 · 60 · 76.

### Grid, spacing & layout
- A **flexible grid, 1–4 columns by content hierarchy** (a 12-column backbone subdivides cleanly and stays useful for data-dense product UI). `.swiss-container` → `.swiss-grid` → `.col-N` / `.start-N`.
- **8px baseline.** All spacing is a multiple of 8 (`--b1…--b12`; 4 is the half-step). Consistent margins, well-separated blocks, **enough air**.

### Borders, elevation & shape
- **Rounded by rule.** Cards, boxes, inputs and pills curve (`--radius-sm 6 · md 10 · lg 16 · xl 24 · pill 999`). Rounding drops only when a block bleeds to the format edge.
- **Soft, warm elevation.** Flat or `--shadow-sm` at rest; lift only when floating (dialog/popover). Warm hairline dividers (`--border-1`); the structural ink keyline is reserved for emphasis.

### Graphic elements — pulse, rhythm, impact
The heartbeat in the form of light. **Pulse** activates (CTAs); **Rhythm** organises movement (programs, activity); **Impact** shows change (results, proof). Concretely in this system:
- **Main brand gradient** — radial Yellow→Orange→Red→Burgundy. **Hero / brand moments only.**
- **Secondary cream gradient** — a clean, soft pause for product surfaces.
- **CTA pulse** — a soft same-color expansion on action (the button's heartbeat).
- **Light point** — an EAV Yellow pulse that activates one focus; over white, cream or photography only. Signals, never decorates.

### Charts & data visualization
Color is assigned by **relevance**, in a fixed order: **Red → Orange → Burgundy → Yellow → Dark Cream → Grey (neutral) → Black (axes/text)**. Seventeen chart types are specified in `Charts Catalogue.html` (and as `preview/chart-*` cards): KPI tiles, bar, horizontal bars, line, area, donut, stacked bars, funnel, progress-vs-target, heatmap, sunburst, timeline/Gantt, radar, scatter, waterfall, treemap, sankey. Max five series; no 3D, shadows or full pies; the only in-chart gradients are the area fade and heatmap ramp.

### Maps & geography
Maps render **real Natural Earth geometry** (never freehand outlines) with a quiet base — land EAV Grey, water paper — and spend colour only on the data layer, in chart rank order. The yellow light point marks headquarters. Six types are specified in `Maps Catalogue.html` (and as `preview/map-*` cards): hub network, coverage, choropleth, region focus, bubble map, flow map. `maps-brand.js` provides the renderers.

### Navigation
One nav list drives every layout. At **768px and up** (iPad portrait included) apps use the **white-paper sidebar**, 224px or a 64px icon rail. Below 768px they use an **iPhone tab bar** (four tabs + More) and a **More bottom sheet**. Only the exact current page gets the active pill, children open only inside the current section, and status marks (red count, cream beta, grey lock) shrink to corner dots in the rail. Safe-area insets are paid back with `max(floor, env(...))`. Full spec, live demos and the iOS home-screen setup: `Navigation Guidelines.html` (and the `preview/nav-*` cards).

### Motion
Quick and contained: short fades, the CTA pulse, soft hover lifts. **No** bounces, springs, parallax or looping decoration — interaction changes color/elevation, not size.

### Interaction states
- **Hover:** ground shift / soft lift; links turn red.
- **Active nav:** `--brand-tint` pill + **3px red marker** + red label, on a **white-paper** nav ground (navigation never sits on cream).
- **Press:** red → `--brand-strong`; burgundy deepens. **Focus:** red ring. **Disabled:** ~40% + `not-allowed`.

---

## CONTENT FUNDAMENTALS — voice & copy

Terse, concrete and proof-driven — **confident, not arrogant**. The register of a working operating system, not a consumer brand.

- **No empty words.** Nothing any other company could say; if it isn't concrete information, it isn't published.
- **Grounded in reality.** Real data and cases, not aspirations. Every message answers: *what does this provide in business terms?*
- **Casing:** eyebrows/section dividers UPPERCASE & tracked; titles sentence/Title case; buttons sentence case; table headers UPPERCASE 11px bold.
- **Brand names, written exactly:** **Eatable Adventures** · **The Beating Heart of Food Innovation** · **Let's Beat**.

**Do:** "We work from challenge to validated pilot. In 6 to 12 months." · "70 companies have executed real projects with us."
**Don't:** "We catalyze the global food ecosystem to co-create holistic impact 🚀"

---

## ICONOGRAPHY

- **Google Material Symbols (Outlined)** — `Weight 300`, `Grade 0`, `Optical Size 48`, outline. Rendered ~18–22px in UI, as **functional support** placed near the content it introduces — secondary in scale, never hero or decorative. Load from Google Fonts; do **not** hand-roll SVG icons or use emoji.
- **Logo:** `assets/logo.svg` — the single-color "Eatable Adventures" wordmark. Positive (black or EAV Red on white/cream) or negative (white on black, red or approved gradients). In compact product chrome the identity is an **app mark**: a rounded EAV Red tile with `EA` in Rubik bold, paper-white.
- **Imagery:** warm or neutral, natural light, authentic; people in action (researching, producing, validating, deciding). Avoid generic stock and cold, abstract tech imagery. Use subtly-striped placeholders with a short label where a real image will drop in.

---

## CONTENTS — file index

| Path | What it is |
|---|---|
| `README.md` | This file — brand context, foundations, voice, iconography, index. |
| `DESIGN.md` | Condensed, code-ready guide for AI coding agents — tokens, type, components, charts, voice, checklist. |
| `styles.css` | **Single entry point** — `@import`s `colors_and_type.css` + `grid.css`. Link this one file to get everything. |
| `colors_and_type.css` | All design tokens (EAV palette, warm text ramp, **Rubik** type scale, rounded radii, gradients & light point, chart hierarchy, 8px spacing) + semantic element styles. Import first. |
| `grid.css` | The flexible / 12-column backbone grid + 8px baseline utilities and specimen overlays. Import after `colors_and_type.css`. |
| `Brand Foundations.html` | One-page brand showcase — palette, type, gradients, light point, components, principles. |
| `Charts Catalogue.html` | Data-visualization catalogue — 17 chart types on the brand hierarchy, with rules. |
| `Maps Catalogue.html` | Maps &amp; geography catalogue — 6 map types on real Natural Earth geometry. |
| `Navigation Guidelines.html` | Navigation spec with live demos — sidebar & rail, iPhone tab bar, More sheet, iOS install, rules. |
| `presentaciones/` | **Slide format for HTML decks** (cover, content-slide header, closing; 1280 × 720, PDF export). `ea_deck.py` builds them on Terracotta tokens. See its README. |
| `charts/` | Canonical **funnel** (stacked discs): generator `funnel.py`, spec `funnel.md`, specimen `funnel.html`. |
| `maps-brand.js` | Brand map renderers (`EAMaps.load()` / `EAMaps.render.*`) on d3-geo + world-atlas. |
| `components/` | Exported React components (see Components below). |
| `templates/app-shell/` | Reusable product **app-shell** template (`AppShell.dc.html`) on the restrained brand — sidebar, top bar, metrics, table, highlight block. |
| `preview/` | Standalone specimen cards that populate the Design System tab (Type, Colors, Components, Navigation, Charts, Maps, Spacing, Brand). |
| `assets/` | Brand assets — `logo.svg` (Eatable Adventures wordmark). |
| `ui_kits/ecosystem-db/` | A high-fidelity app recreation kept on the **previous** (Swiss) visual language — self-contained on its own local CSS. *Not yet re-skinned to the refreshed brand.* |

> **Fonts:** Rubik loads from Google Fonts in `colors_and_type.css` (weights 300/400/500/700/800 + italics). Material Symbols (Outlined, weight 300) loads where icons are used. No local font files required.

## Components

- **Button** — the EAV pill button (`primary` red with CTA pulse, `cta` burgundy, `outline`, `ghost`; `md`/`sm`; optional Material Symbols icon).

---

## How to use this system

1. **Link the tokens, then the grid:** `<link rel="stylesheet" href="colors_and_type.css">` then `<link rel="stylesheet" href="grid.css">` (or just `styles.css`).
2. **Choose your brand intensity first** — restrained for apps/data, higher for covers/heroes.
3. **EAV Red + warm creams + Rubik.** Red as the mark; cream blocks for emphasis; the neutral ramp for hierarchy. Yellow only as the light point, orange only inside the gradient, burgundy for depth.
4. **Rounded surfaces, pill buttons, the CTA pulse on action.** Soft warm dividers; shadows only when floating.
5. **Start from `templates/app-shell/`** for anything app-like, and from `Brand Foundations.html` to see the system whole.
6. **Icons:** Material Symbols Outlined (weight 300), functional and secondary.
