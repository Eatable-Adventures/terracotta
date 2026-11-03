#!/usr/bin/env python3
"""Mide cada tarjeta de la galería en el navegador: textos que se solapan, que se salen de su tarjeta o que quedan cortados.
Sirve para que un defecto de una pieza no pase inadvertido entre más de 150 tarjetas. verificar.py lo ejecuta.

Ejecutar: python3 auditar_galeria.py   (por defecto, «Galería de elementos.html»)
"""
import base64, json, pathlib, re, subprocess, sys, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from inspeccionar_dom import CHROME  # noqa: E402

JS = r"""
(async()=>{try{await document.fonts.ready}catch(e){}await new Promise(r=>setTimeout(r,500));
const out=[];
for(const a of document.querySelectorAll('article[id]')){
 const vis=a.querySelector('.gx-vis')||a; const VR=vis.getBoundingClientRect(); const items=[];
 const tw=document.createTreeWalker(vis,NodeFilter.SHOW_TEXT);let n;const T=[];
 while((n=tw.nextNode())){const t=n.textContent.replace(/\s+/g,' ').trim();if(!t)continue;const el=n.parentElement;const s=getComputedStyle(el);
  if(s.visibility==='hidden'||s.display==='none'||el.closest('style,script'))continue;if(/Material Symbols/.test(s.fontFamily))continue;
  const r=document.createRange();r.selectNodeContents(n);const rs=[...r.getClientRects()].filter(q=>q.width>.5&&q.height>.5);if(rs.length)T.push({el,t,rs,fs:parseFloat(s.fontSize)});}
 let sol=[];for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){const A=T[i],B=T[j];if(A.el===B.el||A.el.contains(B.el)||B.el.contains(A.el))continue;
  if(A.rs.some(p=>B.rs.some(q=>Math.min(p.right,q.right)-Math.max(p.left,q.left)>2&&Math.min(p.bottom,q.bottom)-Math.max(p.top,q.top)>3)))sol.push(A.t.slice(0,24)+' × '+B.t.slice(0,24));}
 let fuera=[];for(const x of T)for(const q of x.rs){if(q.right>VR.right+2||q.left<VR.left-2||q.bottom>VR.bottom+2||q.top<VR.top-2){fuera.push(x.t.slice(0,30));break;}}
 let cort=[];for(const x of T){for(let e=x.el;e&&e!==vis;e=e.parentElement){const s=getComputedStyle(e);if(s.overflow==='visible')continue;const er=e.getBoundingClientRect();if(x.rs.some(q=>q.bottom>er.bottom+2||q.right>er.right+2)){cort.push(x.t.slice(0,30));break;}}}
 let peq=T.filter(x=>x.fs<11).map(x=>x.fs);
 // desborde de cajas respecto al visual
 let w=0;for(const e of vis.querySelectorAll('*')){const q=e.getBoundingClientRect();if(q.width&&q.right>VR.right+2)w=Math.max(w,q.right-VR.right);}
 out.push({id:a.id,sol:[...new Set(sol)].slice(0,6),fuera:[...new Set(fuera)].slice(0,4),cort:[...new Set(cort)].slice(0,4),min:peq.length?Math.min(...peq):null,sobra:Math.round(w)});
}
document.documentElement.setAttribute('data-audit',btoa(unescape(encodeURIComponent(JSON.stringify(out)))));
})();"""


def auditar(ruta=AQUI / "Galería de elementos.html"):
    """Devuelve [dict(id, sol, fuera, cort, min, sobra)] de todas las tarjetas."""
    html = pathlib.Path(ruta).read_text(encoding="utf-8").replace("</body>", "<script>" + JS + "</script></body>")
    with tempfile.TemporaryDirectory() as d:
        copia = pathlib.Path(d) / "galeria.html"
        copia.write_text(html, encoding="utf-8")
        r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--window-size=1500,1200", "--virtual-time-budget=25000",
                            "--dump-dom", copia.as_uri()], capture_output=True, text=True, timeout=300)
    return json.loads(base64.b64decode(re.search(r'data-audit="([^"]+)"', r.stdout).group(1)))


def defectos(res):
    """Las tarjetas con un defecto real: solape, texto fuera o texto cortado."""
    return [x for x in res if x["sol"] or x["fuera"] or x["cort"]]


if __name__ == "__main__":
    res = auditar(*sys.argv[1:2])
    malas = defectos(res)
    print(f"{len(res)} tarjetas medidas, {len(malas)} con defectos")
    for x in malas:
        print(x["id"], {k: v for k, v in x.items() if k != "id" and v})
    sys.exit(1 if malas else 0)
