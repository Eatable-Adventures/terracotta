/* Eatable Adventures — maps-brand.js
   Brand map renderers on real geometry (world-atlas TopoJSON via d3-geo).
   Requires d3 + topojson-client loaded first. Exposes window.EAMaps. */
(function(){
const P={red:'#BC2D29',orange:'#DE5533',burgundy:'#450E14',yellow:'#FFA103',darkCream:'#F5EACE',cream:'#FFF9EE',grey:'#E8E8E8',lightGrey:'#FAFAFA',black:'#1E1E1E',fg2:'#574E48',fg3:'#857B72',fg4:'#ABA197',border:'#DCD6CC'};
P.soft='#DE5A55';P.fill='#F3EFE7';P.dark='#7A1217'; // la misma regla de color que los gráficos: rampa de rojos sobre neutros
const RANK=[P.red,P.dark,P.soft,'#EFA39F','#A3201E'];
const ATLAS='https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json';
let _p;
function load(){
  return _p||(_p=fetch(ATLAS).then(r=>r.json()).then(t=>{
    const countries=topojson.feature(t,t.objects.countries);
    countries.features=countries.features.filter(f=>f.id!=='010'); // drop Antarctica
    return {countries,borders:topojson.mesh(t,t.objects.countries,(a,b)=>a!==b)};
  }));
}
const box=c=>({type:'Polygon',coordinates:[[c[0],c[3],c[2],c[1],c[0]]]}); // clockwise for d3 spherical winding
const EUROPE=box([[-24,34],[42,34],[42,71],[-24,71]]);
const IBERIA=box([[-10,35.5],[4.5,35.5],[4.5,44],[-10,44]]);
const ATLANTIC={type:'MultiPoint',coordinates:[[-112,-40],[46,-40],[46,60],[-112,60]]};
const HUBS=[{name:'Madrid',c:[-3.70,40.42],hq:true},{name:'Verona',c:[10.99,45.44]},{name:'Bogotá',c:[-74.07,4.71]},{name:'Lisbon',c:[-9.14,38.72]}];
const ID={ES:'724',IT:'380',CO:'170',PT:'620',FR:'250',DE:'276',NL:'528',GB:'826',MX:'484',BR:'076',CL:'152',AR:'032',PE:'604',US:'840',IL:'376',CH:'756',BE:'056',DK:'208',IE:'372',PL:'616',SE:'752',AT:'040',NO:'578',FI:'246',CZ:'203',GR:'300'};

function svg(el,w,h){
  const s=d3.select(el);s.selectAll('*').remove();
  s.attr('viewBox',`0 0 ${w} ${h}`).attr('width','100%').attr('height',null)
   .style('display','block').style('overflow','hidden').style('font-family',"'Rubik',system-ui,sans-serif");
  return s;
}
function land(s,path,geo,fill){
  s.append('g').selectAll('path').data(geo.countries.features).join('path').attr('d',path).attr('fill',typeof fill==='function'?fill:(fill||P.grey));
  s.append('path').datum(geo.borders).attr('d',path).attr('fill','none').attr('stroke','#fff').attr('stroke-width',.7).attr('stroke-linejoin','round');
}
function world(el,w,h,geo){
  const s=svg(el,w,h);
  const proj=d3.geoNaturalEarth1().fitSize([w,h],geo.countries);
  return {s,proj,path:d3.geoPath(proj)};
}
function region(el,w,h,extent){
  const s=svg(el,w,h);
  const proj=d3.geoMercator().fitSize([w,h],extent);
  return {s,proj,path:d3.geoPath(proj)};
}
function label(s,x,y,t,o={}){
  return s.append('text').attr('x',x).attr('y',y).text(t)
    .attr('font-size',o.size||12).attr('font-weight',o.weight||500).attr('fill',o.fill||P.black)
    .attr('text-anchor',o.anchor||'start').attr('paint-order','stroke').attr('stroke',o.halo||'#fff').attr('stroke-width',3).attr('stroke-linejoin','round');
}
function legend(s,x,y,items){
  const g=s.append('g').attr('transform',`translate(${x},${y})`);
  items.forEach((it,i)=>{
    const r=g.append('g').attr('transform',`translate(0,${i*18})`);
    r.append('rect').attr('width',12).attr('height',12).attr('rx',3).attr('fill',it.fill).attr('stroke',it.stroke||'none');
    r.append('text').attr('x',18).attr('y',10).text(it.label).attr('font-size',11).attr('fill',P.fg2);
  });
}
function lightPoint(s,x,y){
  s.append('circle').attr('cx',x).attr('cy',y).attr('r',13).attr('fill',P.yellow).attr('opacity',.22);
  s.append('circle').attr('cx',x).attr('cy',y).attr('r',5).attr('fill',P.yellow);
}

const render={
  /* 1 — Hub network: grey world, red hubs, light point on HQ */
  hubs(el,geo){
    const {s,proj,path}=world(el,900,430,geo);
    land(s,path,geo,P.grey);
    HUBS.forEach(h=>{
      const [x,y]=proj(h.c);
      if(h.hq){lightPoint(s,x,y);}
      else{s.append('circle').attr('cx',x).attr('cy',y).attr('r',11).attr('fill',P.red).attr('opacity',.16);
           s.append('circle').attr('cx',x).attr('cy',y).attr('r',5).attr('fill',P.red);}
      const lis=h.name==='Lisbon', mad=h.hq;
      label(s,x+(lis||mad?-10:10),y+(lis?16:mad?-9:-9),h.name,{anchor:lis||mad?'end':'start',weight:h.hq?700:500});
    });
    legend(s,16,380,[{fill:P.yellow,label:'Headquarters'},{fill:P.red,label:'Hub'}]);
  },

  /* 2 — Coverage: categorical status per country */
  coverage(el,geo){
    const {s,path}=world(el,900,430,geo);
    const active=new Set([ID.ES,ID.IT,ID.CO,ID.PT]);
    const pipeline=new Set([ID.MX,ID.BR,ID.CL,ID.FR,ID.DE,ID.NL,ID.GB,ID.IL,ID.US]);
    land(s,path,geo,f=>active.has(f.id)?P.red:pipeline.has(f.id)?P.soft:P.grey);
    legend(s,16,362,[{fill:P.red,label:'Active hub country'},{fill:P.soft,label:'Partner network'},{fill:P.grey,label:'No presence'}]);
  },

  /* 3 — Choropleth: sequential warm ramp, Europe */
  choropleth(el,geo){
    const {s,path}=region(el,560,440,EUROPE);
    const v={[ID.ES]:64,[ID.IT]:48,[ID.PT]:31,[ID.NL]:26,[ID.FR]:22,[ID.GB]:20,[ID.DE]:18,[ID.CH]:14,[ID.DK]:12,[ID.BE]:11,[ID.IE]:9,[ID.SE]:7,[ID.PL]:6,[ID.AT]:5,[ID.NO]:4,[ID.FI]:3,[ID.CZ]:3,[ID.GR]:2};
    const scale=d3.scaleThreshold().domain([5,15,30,50]).range([P.fill,'#EFA39F',P.soft,P.red,P.dark]);
    const fill=f=>v[f.id]==null?P.lightGrey:v[f.id]<5?P.fill:scale(v[f.id]);
    s.append('g').selectAll('path').data(geo.countries.features).join('path').attr('d',path).attr('fill',fill);
    s.append('path').datum(geo.borders).attr('d',path).attr('fill','none').attr('stroke','#fff').attr('stroke-width',.8);
    legend(s,16,330,[{fill:P.dark,label:'50+ startups'},{fill:P.red,label:'30–49'},{fill:P.soft,label:'15–29'},{fill:'#EFA39F',label:'1–14'},{fill:P.lightGrey,stroke:P.grey,label:'No data'}]);
  },

  /* 4 — Bubble map: sized by value, ranked color */
  bubbles(el,geo){
    const {s,proj,path}=world(el,900,430,geo);
    land(s,path,geo,P.grey);
    const data=[[ID.ES,64,'Spain'],[ID.IT,48,'Italy'],[ID.CO,36,'Colombia'],[ID.PT,31,'Portugal'],[ID.NL,26,'Netherlands'],[ID.BR,22,'Brazil'],[ID.FR,22,'France'],[ID.GB,20,'UK'],[ID.MX,18,'Mexico'],[ID.DE,18,'Germany'],[ID.US,14,'USA'],[ID.IL,11,'Israel'],[ID.CL,9,'Chile'],[ID.AR,6,'Argentina'],[ID.PE,4,'Peru']];
    const byId=new Map(geo.countries.features.map(f=>[f.id,f]));
    const r=d3.scaleSqrt().domain([0,64]).range([0,26]);
    const g=s.append('g');
    data.forEach(([id,val,name],i)=>{
      const f=byId.get(id);if(!f)return;
      const [x,y]=path.centroid(f);
      const col=i<3?RANK[i]:P.fg4;
      g.append('circle').attr('cx',x).attr('cy',y).attr('r',r(val)).attr('fill',col).attr('opacity',i<3?.85:.45).attr('stroke','#fff').attr('stroke-width',1.5);
      if(i<3){const left=name==='Spain';label(s,x+(left?-(r(val)+4):r(val)+4),y+4,`${name} · ${val}`,{anchor:left?'end':'start'});}
    });
    legend(s,16,380,[{fill:P.red,label:'Top three markets'},{fill:P.fg4,label:'Other markets · area = startups'}]);
  },

  /* 5 — Flows: great-circle arcs from HQ */
  flows(el,geo){
    const {s,proj,path}=region(el,900,430,ATLANTIC);
    land(s,path,geo,P.grey);
    const hq=[-3.70,40.42];
    const to=[{n:'Bogotá',c:[-74.07,4.71],w:5},{n:'Mexico City',c:[-99.13,19.43],w:3},{n:'São Paulo',c:[-46.63,-23.55],w:3},{n:'Santiago',c:[-70.67,-33.45],w:2},{n:'Verona',c:[10.99,45.44],w:4},{n:'Lisbon',c:[-9.14,38.72],w:3},{n:'Amsterdam',c:[4.90,52.37],w:2},{n:'London',c:[-0.13,51.51],w:2},{n:'Tel Aviv',c:[34.78,32.08],w:2},{n:'New York',c:[-74.01,40.71],w:2}];
    const arcs=s.append('g').attr('fill','none').attr('stroke',P.red).attr('stroke-linecap','round');
    to.forEach(t=>arcs.append('path').datum({type:'LineString',coordinates:[hq,t.c]}).attr('d',path).attr('stroke-width',t.w*.7).attr('opacity',.55));
    to.forEach(t=>{const [x,y]=proj(t.c);s.append('circle').attr('cx',x).attr('cy',y).attr('r',3.5).attr('fill',P.burgundy);
      const left=(t.c[0]<hq[0]&&t.n!=='Lisbon')||t.n==='London';
      const dy=t.n==='London'?4:t.n==='Amsterdam'?-8:t.n==='Lisbon'?14:t.n==='Verona'?14:4;
      label(s,x+(left?-7:7),y+dy,t.n,{anchor:left?'end':'start',size:11,fill:P.fg2,weight:400});});
    const [hx,hy]=proj(hq);lightPoint(s,hx,hy);label(s,hx-12,hy+16,'Madrid HQ',{weight:700,anchor:'end'});
    legend(s,16,392,[{fill:P.red,label:'Flow · width = active projects'}]);
  },

  /* 6 — Region focus: Iberia with cities */
  region(el,geo){
    const {s,proj,path}=region(el,560,440,IBERIA);
    const iberia=new Set([ID.ES,ID.PT]);
    s.append('rect').attr('width',560).attr('height',440).attr('fill',P.cream);
    land(s,path,geo,f=>iberia.has(f.id)?P.fill:P.lightGrey);
    const cities=[{n:'Madrid',c:[-3.70,40.42],hq:true},{n:'Barcelona',c:[2.17,41.39]},{n:'Valencia',c:[-0.38,39.47]},{n:'Bilbao',c:[-2.93,43.26]},{n:'Sevilla',c:[-5.99,37.39]},{n:'Lisbon',c:[-9.14,38.72],hub:true},{n:'Porto',c:[-8.61,41.15]},{n:'Zaragoza',c:[-0.88,41.65]}];
    cities.forEach(ct=>{const [x,y]=proj(ct.c);
      if(ct.hq){lightPoint(s,x,y);}
      else s.append('circle').attr('cx',x).attr('cy',y).attr('r',ct.hub?5:3.5).attr('fill',ct.hub?P.red:P.burgundy);
      label(s,x+8,y+4,ct.n,{weight:ct.hq||ct.hub?700:400,size:ct.hq?13:11,fill:ct.hq||ct.hub?P.black:P.fg2,halo:P.cream});});
    legend(s,16,386,[{fill:P.yellow,label:'Headquarters'},{fill:P.red,label:'Hub'},{fill:P.burgundy,label:'Partner city'}]);
  }
};
window.EAMaps={P,load,render,HUBS};
})();
