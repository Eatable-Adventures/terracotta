#!/usr/bin/env python3
"""Inspector de geometría y forma de un deck HTML de EA. Inyecta un script de medición en una copia del deck,
la abre con Chrome headless (--dump-dom) y devuelve, slide a slide (n = página del PDF), lo que se puede medir:

  errores  · texto fuera de la slide o cortado, texto que invade el pie, textos que se solapan, título contra el logo
  avisos   · fecha de «hoy» o de portada distinta de la actual, columnas que acaban o empiezan a distinto alto, elementos repetidos de distinto tamaño, logos de distinto
             alto, cuerpo que no llena el alto (M11), título sin fragmento rojo o sin negrita o en 3+
             líneas, rótulos en minúscula, bloques en crema o amarillo claro, verde ajeno al de validación y estado (K3), gama de color
             no uniforme, letra por debajo del mínimo (C8), slide sin visual con peso, emojis, «N veces», decimal con
             punto, fechas con barras, unidades mezcladas, referencias internas «(slide N)»
  info     · cifras con la misma etiqueta que cambian entre slides (coherencia), deck sin la base fija de ea_deck

No corrige nada. Es la mitad de revisar_deck.py, que además mide el PDF: cada aviso hay que confirmarlo en el PNG. La carga de
texto la mide medir_deck frente a los rangos de los decks de referencia, no este inspector.

Uso:
  python3 inspeccionar_dom.py DECK.html [--paginas 3,5-7] [--json salida.json] [--tol 6]
Código de salida: 0 sin errores, 1 con errores (los avisos no cuentan).
"""
import argparse, base64, json, os, pathlib, re, shutil, subprocess, sys, tempfile


def ruta_chrome():
    """Chrome para exportar y medir: CHROME_PATH si está definida; si no, las rutas habituales de macOS, Linux y Windows. Si no hay
    ninguno, devuelve un texto que aparece en el error al intentar ejecutarlo: importar este módulo no exige tener Chrome."""
    if os.environ.get("CHROME_PATH"):
        return os.environ["CHROME_PATH"]
    for r in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium"):
        if os.path.exists(r):
            return r
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        if shutil.which(n):
            return shutil.which(n)
    for base in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")):
        r = os.path.join(base, "Google", "Chrome", "Application", "chrome.exe") if base else ""
        if r and os.path.exists(r):
            return r
    return "chrome (no encontrado: define CHROME_PATH)"


CHROME = ruta_chrome()

JS = r"""
(async () => {
const TOL = __TOL__;
try { await document.fonts.ready; } catch (e) {}
await new Promise(r => setTimeout(r, 400));
const cs = el => getComputedStyle(el);
const vis = el => { const s = cs(el); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false;
  const r = el.getBoundingClientRect(); return r.width > 0.5 && r.height > 0.5; };
const name = el => { let s = el.tagName.toLowerCase(); const c = el.getAttribute('class'); if (c) s += '.' + c.trim().split(/\s+/).join('.');
  const t = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 48); return t ? `${s} «${t}»` : s; };
const rgb = c => { const m = (c || '').match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
  if (p.length > 3 && p[3] === 0) return null; return p.slice(0, 3); };
const hsl = ([r, g, b]) => { r /= 255; g /= 255; b /= 255; const mx = Math.max(r, g, b), mn = Math.min(r, g, b); let h = 0, s = 0; const l = (mx + mn) / 2;
  if (mx !== mn) { const d = mx - mn; s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn);
    h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60; } return [h, s, l]; };
// K3: el verde de validación (#2F7D4A, tono 141°, saturación 45 %) y sus mezclas con blanco son de estados; su mal uso se juzga en el PNG
const familia = c => { if (!c) return null; const [h, s, l] = hsl(c); if (h >= 125 && h <= 158 && s <= .62) return null; if (s < .22 || l > .95 || l < .08) return null;
  if (h >= 345 || h < 15) return 'rojo'; if (h < 40) return 'naranja'; if (h < 66) return 'amarillo'; if (h < 170) return 'verde';
  if (h < 260) return 'azul'; return 'morado'; };
const painted = el => { const s = cs(el); const bg = rgb(s.backgroundColor);
  const bd = ['Top', 'Right', 'Bottom', 'Left'].some(k => parseFloat(s['border' + k + 'Width']) > 0 && s['border' + k + 'Style'] !== 'none' && rgb(s['border' + k + 'Color']));
  return !!bg || bd || (s.backgroundImage && s.backgroundImage !== 'none'); };
const inter = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
const ix = (a, b) => Math.min(a.right, b.right) - Math.max(a.left, b.left);
const iy = (a, b) => Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
const SKIP = '.glow,.logo-tr,.cv-bg,.spark';

const out = { slides: [], deck: [] };
const slides = [...document.querySelectorAll('section.slide')];
const cifras = {};
let baseEa = { cover: false, cabeceras: 0, contenido: 0, pies: 0 };

slides.forEach((sl, i) => {
  const n = i + 1, H = [], S = sl.getBoundingClientRect();
  try {
  const add = (nivel, tipo, msg) => H.push({ nivel, tipo, msg });
  for (const e of sl.querySelectorAll('.hueco')) add('aviso', 'pendiente', `Dato pendiente: «${e.textContent.trim()}»`);
  const cls = sl.getAttribute('class') || '';
  const esCover = /\bcover\b/.test(cls), esCierre = /\bclosing\b/.test(cls), esPortadilla = /\b(pd2|portadilla|divider)\b/.test(cls) || !!sl.querySelector('.agenda');
  const R = r => ({ left: r.left - S.left, top: r.top - S.top, right: r.right - S.left, bottom: r.bottom - S.top, width: r.width, height: r.height });
  const h2 = sl.querySelector('h2.t') || sl.querySelector('h2, h1, .title, .slide-title, .titulo');
  const titulo = esCover ? 'Portada' : esCierre ? 'Cierre' : (h2 ? h2.textContent.replace(/\s+/g, ' ').trim() : '(sin título)');
  if (esCover) { baseEa.cover = !!sl.querySelector('img.cv-bg'); out.slides.push({ n, titulo, hallazgos: H }); return; }
  if (esCierre || esPortadilla) { out.slides.push({ n, titulo: esCierre ? titulo : (sl.querySelector('.agenda') ? 'Agenda' : 'Portadilla'), hallazgos: H }); return; }
  baseEa.contenido++; if (sl.querySelector('h2.t') && sl.querySelector('.glow')) baseEa.cabeceras++; if (sl.querySelector('.slide-foot')) baseEa.pies++;

  const foot = sl.querySelector('.slide-foot, .foot, footer');
  const footR = foot && vis(foot) ? R(foot.getBoundingClientRect()) : null;
  const logo = sl.querySelector('.logo-tr');
  const logoR = logo && vis(logo) ? R(logo.getBoundingClientRect()) : null;
  const inFoot = el => foot && foot.contains(el);
  const skip = el => !!el.closest(SKIP);

  // --- cajas de texto reales (rangos sobre nodos de texto)
  const textos = [];
  const tw = document.createTreeWalker(sl, NodeFilter.SHOW_TEXT);
  let nd; while ((nd = tw.nextNode())) {
    const t = nd.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue;
    const el = nd.parentElement; if (!el || !vis(el) || skip(el) || el.closest('style,script')) continue;
    const rg = document.createRange(); rg.selectNodeContents(nd);
    const rs = [...rg.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5); if (!rs.length) continue;
    const u = rs.reduce((a, r) => ({ left: Math.min(a.left, r.left), top: Math.min(a.top, r.top), right: Math.max(a.right, r.right), bottom: Math.max(a.bottom, r.bottom) }),
      { left: 1e9, top: 1e9, right: -1e9, bottom: -1e9 });
    u.width = u.right - u.left; u.height = u.bottom - u.top;
    textos.push({ el, t, r: R(u), rs: rs.map(R), fs: parseFloat(cs(el).fontSize), svg: el instanceof SVGElement, icono: /Material Symbols/.test(cs(el).fontFamily) });
  }

  // --- 1. fuera de la slide, cortado, invade el pie
  const vistos = new Set();
  for (const x of textos) {
    const r = x.r;
    if (r.left < -1 || r.top < -1 || r.right > S.width + 1 || r.bottom > S.height + 1) { add('error', 'fuera', `Texto fuera de la slide: ${name(x.el)}`); continue; }
    let a = x.el.parentElement, cortado = false;
    for (let e = x.el; e && e !== sl; e = e.parentElement) {
      const s = cs(e); if (s.overflow === 'visible' && s.overflowX === 'visible' && s.overflowY === 'visible') continue;
      const er = R(e.getBoundingClientRect()); if (r.bottom > er.bottom + 2 || r.right > er.right + 2 || r.top < er.top - 2) { cortado = true; a = e; break; }
    }
    if (cortado && !vistos.has(a)) { vistos.add(a); add('error', 'cortado', `Texto cortado por ${name(a)}`); }
    if (footR && !inFoot(x.el) && r.bottom > footR.top + 1 && r.top < footR.bottom) add('error', 'pie', `Invade el pie: ${name(x.el)}`);
    if (!inFoot(x.el) && (r.left < 40 || r.right > S.width - 40)) add('aviso', 'margen', `Fuera del margen lateral (40 px): ${name(x.el)}`);
  }

  // --- 2. solapes entre textos de elementos distintos
  const sol = new Set();
  for (let a = 0; a < textos.length; a++) for (let b = a + 1; b < textos.length; b++) {
    const A = textos[a], B = textos[b]; if (A.el === B.el || A.el.contains(B.el) || B.el.contains(A.el)) continue;
    if (ix(A.r, B.r) > 2 && iy(A.r, B.r) > 4 && A.rs.some(p => B.rs.some(q => ix(p, q) > 2 && iy(p, q) > 4))) { const k = name(A.el) + '|' + name(B.el); if (!sol.has(k)) { sol.add(k); add('error', 'solape', `Se solapan ${name(A.el)} y ${name(B.el)}`); } }
  }
  if (h2 && logoR) { const tr = R(h2.getBoundingClientRect()); for (const x of textos) if (h2.contains(x.el) && inter(x.r, logoR) > 4) { add('error', 'logo', 'El título pasa por debajo del logo'); break; } }

  // --- 3. título
  if (h2) {
    const s = cs(h2), red = [...h2.querySelectorAll('*')].find(e => { const c = rgb(cs(e).color); return c && c[0] > 140 && c[1] < 90 && c[2] < 90; });
    if (!h2.matches('.t') ) add('aviso', 'base', 'La cabecera no es la de ea_deck (h2.t con glow)');
    if (!red) add('aviso', 'titulo', 'El título no tiene fragmento rojo (el mensaje)');
    if (parseInt(s.fontWeight) < 700 || (red && parseInt(cs(red).fontWeight) < 700)) add('aviso', 'titulo', 'El título no va entero en negrita (700)');
    const lh = parseFloat(s.lineHeight) || parseFloat(s.fontSize) * 1.15; const lineas = Math.round(h2.getBoundingClientRect().height / lh);
    if (lineas > 2) add('aviso', 'titulo', `Título en ${lineas} líneas (máximo 2)`);
  } else add('aviso', 'titulo', 'Slide de contenido sin título reconocible');

  // --- 4. elementos visuales: cajas pintadas, imágenes, svg
  const els = [...sl.querySelectorAll('*')].filter(e => vis(e) && !skip(e) && !inFoot(e) && !e.closest('style,script'));
  const html = els.filter(e => !(e instanceof SVGElement) || e.tagName.toLowerCase() === 'svg');

  // vertical: borde visual de un bloque (si está pintado, su caja; si no, lo que contiene)
  const visual = el => {
    if (painted(el) || /^(img|svg|canvas)$/i.test(el.tagName)) return R(el.getBoundingClientRect());
    let r = null;
    for (const x of textos) if (el.contains(x.el)) r = r ? { top: Math.min(r.top, x.r.top), bottom: Math.max(r.bottom, x.r.bottom) } : { top: x.r.top, bottom: x.r.bottom };
    for (const c of el.children) { if (!vis(c) || skip(c)) continue; if (painted(c) || /^(img|svg|canvas)$/i.test(c.tagName)) { const q = R(c.getBoundingClientRect());
      r = r ? { top: Math.min(r.top, q.top), bottom: Math.max(r.bottom, q.bottom) } : { top: q.top, bottom: q.bottom }; } else { const q = visual(c); if (q) r = r ? { top: Math.min(r.top, q.top), bottom: Math.max(r.bottom, q.bottom) } : q; } }
    return r;
  };

  // --- 5. columnas hermanas: mismo alto y mismo arranque
  for (const p of html) {
    if (/^(svg|table|tbody|thead|tr|ul|ol|p|span|b|i)$/i.test(p.tagName)) continue;
    const pr = R(p.getBoundingClientRect()); if (pr.width < 400) continue;
    const kids = [...p.children].filter(c => vis(c) && !skip(c) && !(c instanceof SVGElement && c.tagName.toLowerCase() !== 'svg'));
    if (kids.length < 2) continue;
    const kr = kids.map(c => R(c.getBoundingClientRect()));
    const fila = kr.every((r, j) => j === 0 || (ix(kr[j - 1], r) <= 1 && iy(kr[j - 1], r) > 0.5 * Math.min(r.height, kr[j - 1].height)));
    if (!fila || kr.some(r => r.width < 120)) continue;
    const vv = kids.map(visual).filter(Boolean); if (vv.length < 2) continue;
    const db = Math.max(...vv.map(v => v.bottom)) - Math.min(...vv.map(v => v.bottom));
    const dt = Math.max(...vv.map(v => v.top)) - Math.min(...vv.map(v => v.top));
    const conGrafico = kids.some(c => c.querySelector('svg, canvas') || /^(svg|canvas)$/i.test(c.tagName));
    if (conGrafico) { if (db > TOL && db < 320) add('info', 'eje', `Columna con gráfico: comprobar en el PNG que lo de al lado acaba en el eje o la última fila (Δ de cajas ${Math.round(db)} px) en ${name(p).slice(0, 60)}`); continue; }
    if (db > TOL && db < 320) add('aviso', 'alto', `Columnas que acaban a distinto alto (Δ ${Math.round(db)} px) en ${name(p).slice(0, 70)}`);
    if (dt > 10 && dt < 200) add('aviso', 'arranque', `Columnas que empiezan a distinto alto (Δ ${Math.round(dt)} px) en ${name(p).slice(0, 70)}`);
  }

  // --- 6. repetidos con el mismo formato
  for (const p of html) {
    const g = {};
    for (const c of p.children) { if (!vis(c) || skip(c)) continue; const k = c.getAttribute('class'); if (!k) continue; (g[k] = g[k] || []).push(R(c.getBoundingClientRect())); }
    for (const [k, rs] of Object.entries(g)) {
      if (rs.length < 2) continue;
      const enFila = rs.every(r => Math.abs(r.top - rs[0].top) < 4), enCol = rs.every(r => Math.abs(r.left - rs[0].left) < 4);
      const dh = Math.max(...rs.map(r => r.height)) - Math.min(...rs.map(r => r.height));
      const dw = Math.max(...rs.map(r => r.width)) - Math.min(...rs.map(r => r.width));
      if (enFila && dh > 3) add('aviso', 'repetidos', `.${k.split(/\s+/).join('.')} ×${rs.length} en fila con distinto alto (Δ ${Math.round(dh)} px)`);
      if (enCol && !enFila && dw > 3) add('aviso', 'repetidos', `.${k.split(/\s+/).join('.')} ×${rs.length} en columna con distinto ancho (Δ ${Math.round(dw)} px)`);
    }
  }
  const imgs = [...sl.querySelectorAll('img')].filter(e => vis(e) && !skip(e) && !inFoot(e));
  const porPadre = new Map(); for (const im of imgs) { const k = im.getAttribute('class') || '(img)'; if (!porPadre.has(k)) porPadre.set(k, []); porPadre.get(k).push(R(im.getBoundingClientRect())); }
  for (const [k, rs] of porPadre) if (rs.length >= 3) { const dh = Math.max(...rs.map(r => r.height)) - Math.min(...rs.map(r => r.height)); if (dh > 3) add('aviso', 'logos', `${rs.length} imágenes «${k}» con distinto alto (Δ ${Math.round(dh)} px)`); }

  // --- 7. llenado del cuerpo entre cabecera y banda/pie (M11)
  if (h2) {
    let hb = R(h2.getBoundingClientRect()).bottom;
    const sub = [...sl.querySelectorAll('p,div')].find(e => vis(e) && /(^|\s)(sub|subtitle|lead)(\s|$)/.test(e.getAttribute('class') || '') && R(e.getBoundingClientRect()).top - hb < 70 && R(e.getBoundingClientRect()).top >= hb - 2);
    if (sub) hb = Math.max(hb, R(sub.getBoundingClientRect()).bottom);
    const banda = [...sl.querySelectorAll('.banda, .callout, .strip-concl, .conclusion')].filter(vis).map(e => ({ e, r: R(e.getBoundingClientRect()) }))
      .filter(b => b.r.width > 500 && footR && footR.top - b.r.bottom < 60).sort((a, b) => b.r.bottom - a.r.bottom)[0];
    const fondo = banda ? banda.r.top : (footR ? footR.top : S.height - 40);
    if (banda) for (const x of textos) if (!banda.e.contains(x.el) && !inFoot(x.el) && ix(x.r, banda.r) > 2 && iy(x.r, banda.r) > 2) add('error', 'banda', `Tapado por la banda: ${name(x.el)}`);
    const cajas = [];
    for (const x of textos) if (!inFoot(x.el) && !h2.contains(x.el) && !(sub && sub.contains(x.el)) && !(banda && banda.e.contains(x.el)) && x.r.top > hb - 1 && x.r.bottom < fondo + 1) cajas.push(x.r);
    for (const e of html) if ((painted(e) || /^(img|svg|canvas)$/i.test(e.tagName)) && !(banda && (banda.e === e || banda.e.contains(e) || e.contains(banda.e))) && !e.contains(h2)) {
      const r = R(e.getBoundingClientRect()); if (r.top > hb - 1 && r.bottom < fondo + 1 && r.width < S.width - 10) cajas.push(r); }
    if (cajas.length) {
      const top = Math.min(...cajas.map(r => r.top)) - hb, bot = fondo - Math.max(...cajas.map(r => r.bottom));
      if (Math.max(top, bot) > 70 || (top + bot > 110 && Math.min(top, bot) > 30))   // la segunda condición, para que centrar la pieza no apague el aviso; por encima de casi todo lo visto en los decks de referencia (hasta 63 px, con un caso de 89)
 
        add('aviso', 'llenado', `M11: ${Math.round(top)} px libres bajo la cabecera y ${Math.round(bot)} px sobre ${banda ? 'la banda' : 'el pie'}: dar a la pieza el alto de X.alto_cuerpo o añadir contenido, sin centrar`);
    }
  }

  // --- 8. color
  const fams = new Set();
  for (const e of html) {
    const s = cs(e), bg = rgb(s.backgroundColor); const r = R(e.getBoundingClientRect());
    if (bg) { const [h, sa, l] = hsl(bg); const area = r.width * r.height;
      if (h >= 28 && h <= 62 && sa > 0.45 && l > 0.8 && area > 1500 && !e.closest('.hueco')) add('aviso', 'crema', `Bloque en crema o amarillo claro (${s.backgroundColor}): criterio EA, gris claro (--surface-fill) · ${name(e).slice(0, 60)}`);
      if (h >= 30 && h <= 45 && sa > 0.9 && l > 0.45 && l < 0.6 && area > 600) add('aviso', 'amarillo', `Amarillo de marca como relleno de bloque: el amarillo es solo punto de luz · ${name(e).slice(0, 60)}`);
      const f = familia(bg); if (f) fams.add(f); }
  }
  for (const sh of sl.querySelectorAll('svg rect, svg circle, svg path, svg ellipse, svg polygon')) { if (!vis(sh)) continue; const f = familia(rgb(cs(sh).fill)); if (f) fams.add(f); }
  for (const x of textos) { const f = familia(rgb(cs(x.el).color)); if (f) fams.add(f); }
  if (fams.has('verde')) add('aviso', 'verde', 'Verde ajeno al de validación y estado (--validacion #2F7D4A): K3');
  const ajenas = [...fams].filter(f => !['rojo', 'naranja', 'amarillo'].includes(f));
  if (ajenas.length >= 2 || ajenas.some(f => f === 'azul' || f === 'morado')) add('aviso', 'gama', `Gama no uniforme: familias ${[...fams].join(', ')} (Terracotta: rampa de rojos)`);

  // --- 9. tipografía, densidad y peso visual
  const cuerpo = textos.filter(x => !inFoot(x.el) && !x.icono);
  const peq = cuerpo.filter(x => x.fs < (x.svg ? 10 : 11)); if (peq.length) { const x = peq.sort((a, b) => a.fs - b.fs)[0]; add('aviso', 'letra', `Letra de ${x.fs} px (${peq.length} textos por debajo de ${x.svg ? 10 : 11} px): ${name(x.el).slice(0, 60)}`); }
  const bodyArea = S.width * (S.height - 200);
  const visArea = els.filter(e => /^(svg|img|canvas)$/i.test(e.tagName) && !e.closest('svg svg')).map(e => R(e.getBoundingClientRect()))
    .filter(r => r.width >= 40 && r.height >= 40).reduce((a, r) => a + r.width * r.height, 0)
    + html.filter(e => painted(e) && !/^(svg|img|canvas)$/i.test(e.tagName) && !(e.textContent || '').trim() && !e.closest('svg'))
      .map(e => R(e.getBoundingClientRect())).filter(r => r.width * r.height >= 60 && r.width < S.width - 10).reduce((a, r) => a + r.width * r.height, 0);
  const iconos = els.filter(e => /Material Symbols/.test(cs(e).fontFamily)).length;
  const formas = html.filter(e => painted(e) && !/^(img|canvas)$/i.test(e.tagName) && (!(e.textContent || '').trim() || (/clip-path|polygon/.test(cs(e).clipPath || '') ))).length
    + sl.querySelectorAll('svg rect, svg circle, svg path, svg polygon, svg line').length;
  const logos = imgs.filter(e => { const r = e.getBoundingClientRect(); return r.width >= 24 && r.height >= 14; }).length;
  if (visArea / bodyArea < 0.06 && formas < 4 && iconos < 6 && logos < 3) add('aviso', 'visual', `Sin visual con peso: ${Math.round(100 * visArea / bodyArea)} % de la superficie es gráfico o imagen${iconos ? `, ${iconos} iconos` : ''}`);

  // --- 10. texto: mayúscula inicial, formatos, referencias internas, emojis
  cuerpo.forEach((x, i) => {
    const el = x.el, own = x.t, todo = (el.textContent || '').replace(/\s+/g, ' ').trim(), prev = cuerpo[i - 1];
    // C2 no aplica a lo que sigue a una cifra ni a la segunda línea de un mismo rótulo de gráfica
    const tras = prev && !x.icono && /\d/.test(prev.t) && Math.abs(x.r.top - prev.r.bottom) < 40 && ix(x.r, prev.r) > -60;
    const segunda = prev && x.svg && prev.svg && Math.abs(x.r.top - prev.r.bottom) < 8 && ix(x.r, prev.r) > 0;
    if (!tras && !segunda && !x.icono && own === todo && own.length >= 2 && own.length <= 40 && own.split(' ').length <= 5 && /^[a-zñáéíóúü]/.test(own)
      && !/^(kl|kg|ml|mg|vs|de|del|y|o|en|a|con|por|para)\b/i.test(own) && !/uppercase|capitalize/.test(cs(el).textTransform)
      && !(el.parentElement && /\S/.test([...el.parentElement.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(''))))
      add('aviso', 'mayuscula', `Rótulo en minúscula: «${own}»`);
  });
  const plano = cuerpo.map(x => x.t).join(' · ');
  const m = (re, msg) => { const f = plano.match(re); if (f) add('aviso', 'formato', `${msg}: «${f.slice(0, 3).join('», «')}»`); };
  m(/\b\d+(?:,\d+)?\s+veces\b/gi, 'Multiplicador en palabras (usar ×N)');
  m(/(?<!art\.\s?)(?<![\w.,])\d{1,3}\.\d{1,2}(?![\d.])/g, 'Decimal con punto (coma decimal)');
  m(/\b\d{1,2}\/\d{1,2}\/\d{2,4}\b/g, 'Fecha con barras (DD-MM-YYYY)');
  m(/\(slide \d+\)|\bver slide \d+/gi, 'Referencia interna a otra slide');
  m(/\p{Extended_Pictographic}/gu, 'Emoji (sustituir por Material Symbols)');
  const u = new Set((plano.match(/\d[\d.,]*\s?(kL|L|mL|kg|g|t)\b/g) || []).map(s => s.replace(/^[\d.,\s]+/, '')));
  if ((u.has('L') && u.has('kL')) || (u.has('g') && u.has('kg')) || (u.has('mL') && u.has('L'))) add('aviso', 'unidades', `Unidades mezcladas en la slide: ${[...u].join(', ')}`);
  for (const mm of plano.matchAll(/\b(\d{1,4})\s+([a-záéíóúñ]{5,})\b/gi)) { const k = mm[2].toLowerCase(); (cifras[k] = cifras[k] || []).push([n, mm[1]]); }

  out.slides.push({ n, titulo, hallazgos: H });
  } catch (err) { H.push({ nivel: 'info', tipo: 'interno', msg: 'Inspección incompleta: ' + err.message }); out.slides.push({ n, titulo: '?', hallazgos: H }); }
});

// --- deck: base fija y coherencia de cifras
if (!baseEa.cover) out.deck.push({ nivel: 'info', tipo: 'base', msg: 'La portada no es la de ea_deck (img.cv-bg)' });
if (baseEa.contenido && baseEa.cabeceras < baseEa.contenido) out.deck.push({ nivel: 'info', tipo: 'base', msg: `${baseEa.contenido - baseEa.cabeceras} de ${baseEa.contenido} slides de contenido sin la cabecera de ea_deck` });
if (baseEa.contenido && baseEa.pies < baseEa.contenido) out.deck.push({ nivel: 'info', tipo: 'base', msg: `${baseEa.contenido - baseEa.pies} de ${baseEa.contenido} slides sin el pie de ea_deck (.slide-foot)` });
for (const [k, v] of Object.entries(cifras)) { const vals = new Set(v.map(x => x[1])); const pags = new Set(v.map(x => x[0]));
  if (vals.size > 1 && pags.size > 1) out.deck.push({ nivel: 'info', tipo: 'coherencia', msg: `«${k}» con cifras distintas: ${v.map(x => `${x[1]} (p. ${x[0]})`).join(', ')}` }); }
const enc = btoa(unescape(encodeURIComponent(JSON.stringify(out))));
document.documentElement.setAttribute('data-inspeccion', enc);
})();
"""


def rango(txt):
    if not txt:
        return None
    s = set()
    for p in txt.split(","):
        if "-" in p:
            a, b = p.split("-"); s.update(range(int(a), int(b) + 1))
        elif p.strip():
            s.add(int(p))
    return s


def inspeccionar(deck, tol=6):
    """Hallazgos del deck: {"slides": [{n, titulo, hallazgos: [{nivel, tipo, msg}]}], "deck": [...]}."""
    deck = pathlib.Path(deck).resolve()
    txt = deck.read_text(encoding="utf-8")
    base = f'<base href="{deck.parent.as_uri()}/">'
    script = "<script>" + JS.replace("__TOL__", str(tol)) + "</script>"
    txt = re.sub(r"<head>", "<head>" + base, txt, count=1)
    txt = txt.replace("</body>", script + "</body>") if "</body>" in txt else txt + script

    with tempfile.TemporaryDirectory() as tmp:
        copia = pathlib.Path(tmp) / "inspeccion.html"
        copia.write_text(txt, encoding="utf-8")
        r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--window-size=1400,1000",
                            "--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw", "--dump-dom",
                            copia.as_uri()], capture_output=True, text=True, timeout=240)
    m = re.search(r'data-inspeccion="([A-Za-z0-9+/=]+)"', r.stdout)
    if not m:
        raise RuntimeError("No se pudo leer la inspección (¿el deck tiene <section class=\"slide\">?).\n" + r.stderr[-1500:])
    res = json.loads(base64.b64decode(m.group(1)).decode("utf-8"))

    # fechas de «hoy» y de portada frente a la fecha actual (F9)
    import datetime, html as _h
    hoy = datetime.date.today()
    plano = _h.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"base64,[A-Za-z0-9+/=]+", "", deck.read_text(encoding="utf-8"))))
    for m in re.finditer(r"\b[Hh]oy\s*[·:,-]?\s*(\d{1,2})[-/](\d{1,2})(?:[-/](\d{4}))?", plano):
        d, mth = int(m.group(1)), int(m.group(2))
        if (d, mth) != (hoy.day, hoy.month):
            res["deck"].append({"nivel": "aviso", "tipo": "fecha", "msg": f"«{m.group(0).strip()}» no es hoy ({hoy:%d-%m}): confirmar la fecha de presentación"}); break
    portada = re.search(r'<section class="slide cover.*?</section>', deck.read_text(encoding="utf-8"), re.S)
    if portada:
        fp = re.search(r"\b(\d{2})-(\d{2})-(\d{4})\b", _h.unescape(re.sub(r"<[^>]+>", " ", portada.group(0))))
        if fp and datetime.date(int(fp.group(3)), int(fp.group(2)), int(fp.group(1))) != hoy:
            res["deck"].append({"nivel": "aviso", "tipo": "fecha", "msg": f"La portada dice {fp.group(0)}: confirmar que es la fecha de presentación"})
    # la cabecera ajena se dice una vez, en el deck, no en cada slide
    sin_base = any(h["tipo"] == "base" and "cabecera" in h["msg"] and h["msg"].split(" de ")[0] == h["msg"].split(" de ")[1].split()[0] for h in res["deck"])
    for s in res["slides"]:
        vistos, unicos = set(), []
        for h in s["hallazgos"]:
            if h["msg"] not in vistos and not (sin_base and h["tipo"] == "base"):
                vistos.add(h["msg"]); unicos.append(h)
        s["hallazgos"] = sorted(unicos, key=lambda h: {"error": 0, "aviso": 1, "info": 2}[h["nivel"]])
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--paginas")
    ap.add_argument("--json")
    ap.add_argument("--tol", type=int, default=6, help="tolerancia en px para «mismo alto» (por defecto 6)")
    a = ap.parse_args()
    try:
        res = inspeccionar(a.deck, a.tol)
    except RuntimeError as e:
        print(e)
        sys.exit(2)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    sel = rango(a.paginas)
    errores = avisos = 0
    for s in res["slides"]:
        if sel and s["n"] not in sel:
            continue
        unicos = s["hallazgos"]
        print(f"\np. {s['n']:>2} · {s['titulo'][:90]}")
        if not unicos:
            print("   (sin hallazgos medibles)")
        for h in sorted(unicos, key=lambda h: {"error": 0, "aviso": 1, "info": 2}[h["nivel"]]):
            marca = {"error": "✗", "aviso": "·", "info": "i"}[h["nivel"]]
            print(f"   {marca} [{h['tipo']}] {h['msg']}")
            errores += h["nivel"] == "error"; avisos += h["nivel"] == "aviso"
    if res["deck"]:
        print("\nDeck:")
        for h in res["deck"]:
            print(f"   {'·' if h['nivel'] == 'aviso' else 'i'} [{h['tipo']}] {h['msg']}")
    print(f"\n{len(res['slides'])} slides · {errores} errores · {avisos} avisos (confirmar cada aviso en el PNG)")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
