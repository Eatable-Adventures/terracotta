---
name: terracotta
description: Use this skill (Terracotta — the Eatable Adventures design system) to generate well-branded interfaces and assets for Eatable Adventures (the operating system for food innovation — "The Beating Heart of Food Innovation"), for production or throwaway prototypes/mocks. Contains the brand's colors, Rubik type, gradients, light point, assets, components and an app-shell template.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files (`DESIGN.md`, `colors_and_type.css`, `grid.css`, `assets/`, `preview/`, `Brand Foundations.html`, `Navigation Guidelines.html`, `templates/app-shell/`, `presentaciones/` for HTML decks, `charts/funnel.md` for funnels).

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, copy assets and read the rules here to become an expert in designing with this brand. For anything app-like, start from `templates/app-shell/`; to see the system whole, open `Brand Foundations.html`.

Key facts to internalize before you start:
- **Brand: "The Beating Heart of Food Innovation."** Warm, human, premium without arrogance — pulse · rhythm · impact. **Choose brand intensity first:** restrained for apps/data (white + cream + subtle red), higher only for covers/heroes.
- **Color — two mother colors, one warm system.** EAV Red `#BC2D29` is the representative color (identity, active, links, focus, CTAs). White predominates; EAV Cream `#FFF9EE` is the editorial block; EAV Black `#1E1E1E` is type/footers. Yellow `#FFA103` = light point **only**, Orange `#DE5533` = gradient transition **only**, Burgundy `#450E14` = depth/closings. Warm text ramp fg1–fg4. Charts: Red→Orange→Burgundy→Yellow→Dark Cream→Grey→Black.
- **Type — Rubik, and only Rubik** (Light/Regular/Medium/Bold/Extrabold + italics). Headlines are **Regular** with one **bold** (or red) fragment; body Regular with bold highlights; long-form Light + Medium. Left-aligned, never justified. 8px rhythm.
- **Shape:** rounded by rule — `radius-lg` (16px) cards, **pill** buttons & chips, rounded inputs; warm hairline dividers; soft shadows only when floating. The **CTA pulse** (soft same-color expansion) marks primary actions.
- **Icons:** Google Material Symbols (Outlined, weight 300), ~18–22px, functional & secondary. Never hand-roll SVG icons or use emoji.
- **Charts:** fixed hierarchy Red→Orange→Burgundy→Yellow→Dark Cream→Grey→Black, by relevance. 17 specified types in `Charts Catalogue.html` (KPI, bar, line, area, donut, stacked, funnel, progress, heatmap, sunburst, timeline, radar, scatter, waterfall, treemap, sankey). Max five series; no 3D/shadows/full pies.
- **Maps:** real Natural Earth geometry via `maps-brand.js` (d3-geo). Land grey, water paper, data in rank colours, HQ = yellow light point. 6 types in `Maps Catalogue.html` (hub network, coverage, choropleth, region focus, bubble, flow).
- **Navigation:** one nav list for every layout — white-paper sidebar (224px, or 64px rail) at 768px+, iPhone tab bar (four tabs + More) and More bottom sheet below. Exact-page highlight only; children open only in the current section; status marks are a red count, cream beta or grey lock, never amber/blue. Spec and demos in `Navigation Guidelines.html`.
- **Voice:** terse, concrete, proof-driven — confident, not arrogant. No empty words, no hype, no emoji. Brand names exact: Eatable Adventures · The Beating Heart of Food Innovation · Let's Beat.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.
