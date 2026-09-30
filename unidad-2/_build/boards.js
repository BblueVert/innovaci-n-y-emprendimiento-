// Genera los tableros estilo MIRO (HTML → PNG) de los instrumentos S6 y S7.
const fs = require('fs');
const path = require('path');
const D = require('./data');

const ORANGE = '#FF6B35';
const NAVY = '#1B1F3B';
const autor = Object.fromEntries(D.equipo.map((m) => [m.key, m]));
const ideaById = Object.fromEntries(D.ideas.map((i) => [i.id, i]));

const base = (w, h, title, code, body, extraCss = '') => `<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:${w}px;font-family:'Liberation Sans',Arial,sans-serif;color:${NAVY};
background:#F4F3EF;background-image:radial-gradient(#d6d3cb 1.2px,transparent 1.2px);background-size:24px 24px;padding:40px 48px}
.frame{display:flex;flex-direction:column}
.hd{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:4px solid ${NAVY};padding-bottom:14px;margin-bottom:26px}
.hd .code{font-family:'Liberation Mono',monospace;font-size:17px;letter-spacing:1px;color:${ORANGE};font-weight:700}
.hd h1{font-size:40px;letter-spacing:-.5px;margin-top:4px}
.hd .tag{text-align:right;font-family:'Liberation Mono',monospace;font-size:14px;line-height:1.5;color:#555}
.hd .tag b{color:${NAVY};font-size:18px;letter-spacing:4px}
.post{border-radius:3px;box-shadow:0 2px 0 rgba(0,0,0,.08),0 6px 14px rgba(0,0,0,.08);padding:12px 12px 10px;font-size:15px;line-height:1.3;position:relative}
.post .id{font-family:'Liberation Mono',monospace;font-size:12px;font-weight:700;opacity:.65;display:block;margin-bottom:4px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}
${extraCss}
</style></head><body><div class="frame">
<div class="hd"><div><div class="code">${code}</div><h1>${title}</h1></div>
<div class="tag"><b>HORIZON</b><br>Innovación y Emprendimiento III · Caso InMotion</div></div>
${body}</div></body></html>`;

const post = (i, extra = '') => {
  const m = autor[i.a];
  return `<div class="post" style="background:${m.color};${extra}"><span class="id">${i.id} · ${m.nombre.split(' ')[0]}</span>${i.t}</div>`;
};

const leyenda = () => `<div style="display:flex;gap:22px;font-size:15px;margin-top:18px;flex-wrap:wrap">${D.equipo
  .map((m) => `<span><span class="dot" style="width:16px;height:16px;border-radius:3px;background:${m.color};border:1px solid #0002"></span>${m.nombre}${m.secretario ? ' <b style="color:#D62828">(secretario técnico)</b>' : ''}</span>`)
  .join('')}</div>`;

// ---------- S6-01 Fichas de referentes ----------
function fichas() {
  const cards = D.referentes.map((r) => {
    const ini = r.nombre.replace(/[^A-Za-zÁÉÍÓÚ]/g, '').slice(0, 2).toUpperCase();
    return `<div class="card">
      <div class="img"><span>${ini}</span><em>${r.ambito}</em></div>
      <div class="bd"><div class="n">CASO ${String(r.n).padStart(2, '0')}</div><h3>${r.nombre}</h3>
      <p>${r.desc}</p>
      <div class="rel"><b>Aspecto relevante</b>${r.novedad}</div>
      <div class="src">Fuente: ${r.fuente} · Tendencia: ${r.tendencia}</div></div></div>`;
  }).join('');
  return base(1800, 1500, 'Fichas de referentes', 'INSTRUMENTO 2.1.2.1.A · SEMANA 6',
    `<div class="grid">${cards}</div>`,
    `.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;flex:1}
     .card{background:#fff;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.08);display:flex;overflow:hidden}
     .img{width:150px;flex:none;background:${NAVY};color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:16px}
     .img span{font-size:52px;font-weight:700;color:${ORANGE};letter-spacing:-2px}
     .img em{font-style:normal;font-family:'Liberation Mono',monospace;font-size:12px;line-height:1.4;opacity:.85}
     .bd{padding:16px 18px;display:flex;flex-direction:column;gap:8px}
     .n{font-family:'Liberation Mono',monospace;font-size:12px;color:${ORANGE};font-weight:700}
     h3{font-size:24px}
     p{font-size:14.5px;line-height:1.4;color:#333}
     .rel{background:#FFF1EA;border-left:4px solid ${ORANGE};padding:8px 10px;font-size:14px;line-height:1.35}
     .rel b{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}
     .src{margin-top:auto;font-family:'Liberation Mono',monospace;font-size:11.5px;color:#777}`);
}

// ---------- S6-02 Matriz de referentes ----------
function matriz() {
  const vs = D.variables;
  const head = `<tr><th class="c0">Caso</th>${vs.map((v) => `<th${v.k === 'novedad' ? ' class="hl"' : ''}>${v.t}</th>`).join('')}</tr>`;
  const rows = D.referentes.map((r) => `<tr><td class="c0"><b>${r.n}. ${r.nombre}</b><span>${r.ambito}</span></td>${vs
    .map((v) => {
      const val = r[v.k];
      const na = val === 'No aplica.';
      if (v.k === 'tendencia') return `<td><span class="pill">${val}</span></td>`;
      return `<td class="${v.k === 'novedad' ? 'hl' : ''}${na ? ' na' : ''}">${na ? '—' : val}</td>`;
    }).join('')}</tr>`).join('');
  return base(1800, 1500, 'Matriz de referentes', 'INSTRUMENTO 2.1.2.1.B · SEMANA 6',
    `<div style="font-size:16px;margin-bottom:14px"><b>Desafío:</b> ${D.desafio}</div><table>${head}${rows}</table>`,
    `table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,.08);font-size:16px;line-height:1.4}
     th{background:${NAVY};color:#fff;text-align:left;padding:12px;font-size:14px;text-transform:uppercase;letter-spacing:.4px}
     th.hl{background:${ORANGE}}
     td{padding:10px 12px;border-bottom:1px solid #eee;vertical-align:top}
     td.hl{background:#FFF1EA;font-weight:700}
     td.na{color:#bbb;text-align:center}
     .c0{width:190px}.c0 b{display:block;font-size:16px}.c0 span{font-size:12px;color:#777;font-family:'Liberation Mono',monospace}
     .pill{display:inline-block;background:${NAVY};color:#fff;border-radius:20px;padding:4px 10px;font-size:12.5px}`);
}

// ---------- S6-03 Tendencias ----------
function tendencias() {
  const cards = D.tendencias.map((t, i) => `<div class="t"><div class="num">T${i + 1}</div><h3>${t.t}</h3>
    <div class="casos">${t.casos}</div><p>${t.ins}</p></div>`).join('');
  return base(1800, 1100, 'Tendencias y elementos novedosos', 'ANÁLISIS 2.1.2.1.B · SEMANA 6',
    `<div class="grid">${cards}</div>
     <div class="concl"><b>Conclusión para la ideación →</b> La solución para Joselyn no debe ser “un Excel más ordenado”, sino un sistema donde cada reserva y cada cobro generen el dato por sí solos, y donde la proyección se lea como un tablero. Las tendencias T1, T3 y T4 atacan el dolor financiero; T2 ataca la estacionalidad; T5 y T6 protegen su diferenciador: el trato 1:1.</div>`,
    `.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
     .t{background:#fff;border-radius:8px;padding:22px;box-shadow:0 4px 16px rgba(0,0,0,.08);border-top:6px solid ${ORANGE}}
     .num{font-family:'Liberation Mono',monospace;font-weight:700;color:${ORANGE};font-size:18px}
     h3{font-size:26px;margin:6px 0 8px}
     .casos{font-family:'Liberation Mono',monospace;font-size:13px;color:#666;margin-bottom:10px}
     p{font-size:17px;line-height:1.45}
     .concl{margin-top:26px;background:${NAVY};color:#fff;border-radius:8px;padding:24px 28px;font-size:19px;line-height:1.5}
     .concl b{color:${ORANGE}}`);
}

// ---------- S7-01 Canvas brainstorming ----------
function brainstorming() {
  const col = (k) => D.ideas.filter((i) => i.a === k).map((i) => post(i, 'transform:rotate(' + ((i.id.charCodeAt(1) % 3) - 1) * 0.8 + 'deg)')).join('');
  const zone = (k) => `<div class="zone"><div class="zh"><span class="dot" style="background:${autor[k].color};border:1px solid #0003;width:14px;height:14px"></span>${autor[k].nombre}${autor[k].secretario ? ' <b style="color:#D62828">· secretario técnico</b>' : ''}</div><div class="ps">${col(k)}</div></div>`;
  return base(1800, 1400, 'Canvas brainstorming', 'INSTRUMENTO 2.1.4.1 · SEMANA 7',
    `<div class="wrap">${zone('F')}${zone('C')}
      <div class="center"><div class="lbl">DESAFÍO</div>${D.desafio}<div class="meta">36 ideas · 4 integrantes · 45 min · sin juicio</div></div>
      ${zone('N')}${zone('B')}</div>`,
    `.wrap{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr auto 1fr;gap:20px}
     .center{grid-column:1/3;background:${NAVY};color:#fff;border-radius:10px;padding:24px 34px;font-size:24px;line-height:1.35;font-weight:700;text-align:center}
     .center .lbl{font-family:'Liberation Mono',monospace;color:${ORANGE};font-size:15px;letter-spacing:3px;margin-bottom:8px}
     .center .meta{font-family:'Liberation Mono',monospace;font-size:13px;font-weight:400;opacity:.7;margin-top:10px}
     .zone{background:rgba(255,255,255,.55);border:2px dashed #c9c5ba;border-radius:10px;padding:14px}
     .zh{font-weight:700;font-size:16px;margin-bottom:10px}
     .ps{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
     .post{min-height:92px}`);
}

// ---------- S7-02 Mapa de clasificación ----------
function clasificacion() {
  const q = (k) => D.ideas.filter((i) => D.cuadrante(i) === k).map((i) => post(i)).join('');
  const box = (k, title, cls) => `<div class="q ${cls}"><div class="qh">${title}</div><div class="ps">${q(k)}</div></div>`;
  return base(1800, 1500, 'Mapa de clasificación de ideas', 'INSTRUMENTO 2.1.4.2 · SEMANA 7',
    `<div class="board">
      <div class="ylab top">(+) FACTIBLE</div><div class="ylab bot">(−) FACTIBLE</div>
      <div class="xlab lft">(−) ORIGINAL</div><div class="xlab rgt">(+) ORIGINAL</div>
      <div class="grid">
        ${box('-O+F', 'Factibles pero conocidas · base operativa', '')}
        ${box('+O+F', '★ Más originales y factibles · foco de la solución', 'star')}
        ${box('-O-F', 'Descartadas', 'low')}
        ${box('+O-F', 'Originales, poco factibles hoy · banco de ideas futuras', '')}
      </div></div>
      <div style="font-size:14px;margin-top:10px;color:#555">Ejes definidos en consenso: originalidad frente a lo que hoy usa Joselyn y su competencia · factibilidad con herramientas existentes, presupuesto bajo y 1 mes de implementación. Umbral: puntaje ≥ 6/10.</div>${leyenda()}`,
    `.board{height:860px;position:relative;padding:34px 44px}
     .grid{height:100%;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0;border:3px solid ${NAVY};background:#fff}
     .q{padding:16px;border:1px solid #d9d6cf}
     .q.star{background:#FFF1EA;outline:4px solid ${ORANGE};outline-offset:-4px;z-index:1}
     .q.low{background:#f3f3f3}.q.low .post{opacity:.55}
     .qh{font-weight:700;font-size:16px;margin-bottom:12px;text-transform:uppercase;letter-spacing:.4px}
     .q.star .qh{color:${ORANGE}}
     .ps{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
     .post{font-size:13.5px;min-height:84px;padding:10px}
     .ylab,.xlab{position:absolute;font-family:'Liberation Mono',monospace;font-weight:700;font-size:15px;letter-spacing:2px}
     .ylab{left:50%;transform:translateX(-50%)}.top{top:6px}.bot{bottom:6px}
     .xlab{top:50%}.lft{left:-34px;transform:translateY(-50%) rotate(-90deg)}.rgt{right:-38px;transform:translateY(-50%) rotate(90deg)}`);
}

// ---------- S7-03 Categorías y concepto directriz ----------
function categorias() {
  const cols = D.grupos.map((g) => `<div class="g" style="border-top-color:${D.categorias[g.cat].c}">
     <h3 style="color:${D.categorias[g.cat].c}">${g.t}</h3>
     <div class="ps">${g.ideas.map((id) => post(ideaById[id])).join('')}</div>
     <div class="sin"><b>Síntesis</b>${g.sintesis}</div></div>`).join('');
  return base(1800, 1400, 'Categorías y concepto directriz', 'SÍNTESIS 2.1.4.2 · SEMANA 7',
    `<div class="cols">${cols}</div>
     <div class="arrow">▼</div>
     <div class="concept"><div class="lbl">CONCEPTO DIRECTRIZ</div><h2>${D.conceptoNombre}</h2><p>${D.concepto}</p></div>`,
    `.cols{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
     .g{background:#fff;border-radius:8px;border-top:6px solid;padding:18px;box-shadow:0 4px 16px rgba(0,0,0,.08);display:flex;flex-direction:column;gap:12px}
     h3{font-size:24px}
     .ps{display:flex;flex-direction:column;gap:10px}
     .sin{margin-top:auto;background:#F4F3EF;border-radius:6px;padding:12px;font-size:15px;line-height:1.4}
     .sin b{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.6px;margin-bottom:4px}
     .arrow{text-align:center;font-size:34px;color:${ORANGE};margin:10px 0}
     .concept{background:${NAVY};color:#fff;border-radius:10px;padding:26px 34px}
     .concept .lbl{font-family:'Liberation Mono',monospace;color:${ORANGE};letter-spacing:3px;font-size:15px}
     .concept h2{font-size:40px;margin:6px 0 10px}
     .concept p{font-size:21px;line-height:1.45}`);
}

// ---------- S7-04 Panel de metáforas y atributos ----------
function collageSvg() {
  // Collage ilustrado: tablero (velocímetro + combustible), semáforo, ruta con pines y globo de chat.
  return `<svg viewBox="0 0 760 520" xmlns="http://www.w3.org/2000/svg" font-family="Liberation Sans, Arial">
  <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9A62"/><stop offset="1" stop-color="#FF6B35"/></linearGradient></defs>
  <rect width="760" height="520" rx="14" fill="url(#sky)"/>
  <path d="M0 300 C160 250 260 340 400 290 S640 230 760 270 L760 520 L0 520Z" fill="#E4572E"/>
  <path d="M-10 470 C120 380 260 470 380 400 S600 330 770 360" stroke="#1B1F3B" stroke-width="34" fill="none"/>
  <path d="M-10 470 C120 380 260 470 380 400 S600 330 770 360" stroke="#fff" stroke-width="3" stroke-dasharray="18 14" fill="none"/>
  ${[[120, 418], [300, 436], [470, 368], [650, 340]].map(([x, y], i) => `<g transform="translate(${x},${y - 46})"><path d="M0 0c-14 0-24 10-24 23 0 17 24 37 24 37s24-20 24-37C24 10 14 0 0 0z" fill="#fff"/><text x="0" y="29" text-anchor="middle" font-size="16" font-weight="700" fill="#1B1F3B">${i + 1}</text></g>`).join('')}
  <g transform="translate(40,40)">
    <rect width="420" height="230" rx="18" fill="#1B1F3B"/>
    <g transform="translate(120,150)">
      <path d="M-90 0 A90 90 0 0 1 90 0" stroke="#3A3F63" stroke-width="16" fill="none"/>
      <path d="M-90 0 A90 90 0 0 1 55 -71" stroke="#FF6B35" stroke-width="16" fill="none"/>
      <line x1="0" y1="0" x2="48" y2="-62" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle r="9" fill="#fff"/>
      <text y="42" text-anchor="middle" fill="#fff" font-size="15">META MES 78%</text>
    </g>
    <g transform="translate(300,150)">
      <path d="M-70 0 A70 70 0 0 1 70 0" stroke="#3A3F63" stroke-width="12" fill="none"/>
      <path d="M-70 0 A70 70 0 0 1 20 -67" stroke="#8BE3B4" stroke-width="12" fill="none"/>
      <line x1="0" y1="0" x2="16" y2="-52" stroke="#fff" stroke-width="4" stroke-linecap="round"/><circle r="7" fill="#fff"/>
      <text y="42" text-anchor="middle" fill="#fff" font-size="15">FONDO RESERVA</text>
    </g>
    <text x="24" y="36" fill="#FF6B35" font-family="Liberation Mono" font-size="15" font-weight="700">TABLERO INMOTION</text>
  </g>
  <g transform="translate(510,40)">
    <rect width="80" height="200" rx="16" fill="#1B1F3B"/>
    <circle cx="40" cy="42" r="24" fill="#3A3F63"/><circle cx="40" cy="100" r="24" fill="#FFD23F"/><circle cx="40" cy="158" r="24" fill="#3A3F63"/>
    <text x="40" y="232" text-anchor="middle" fill="#1B1F3B" font-size="14" font-weight="700">ALERTA: JULIO</text>
  </g>
  <g transform="translate(610,60)">
    <rect width="130" height="120" rx="16" fill="#fff"/>
    <path d="M24 120 l0 26 l26 -26z" fill="#fff"/>
    <text x="16" y="36" font-size="14" fill="#1B1F3B" font-weight="700">Joselyn</text>
    <text x="16" y="62" font-size="14" fill="#1B1F3B">Voy en camino</text>
    <text x="16" y="84" font-size="14" fill="#1B1F3B">llego 10:40</text>
    <text x="16" y="108" font-size="12" fill="#12A37F">✓✓ automático</text>
  </g>
  <text x="380" y="505" text-anchor="middle" fill="#fff" font-family="Liberation Mono" font-size="14" letter-spacing="2">RUTA DEL DÍA · DOMICILIOS AGRUPADOS POR SECTOR</text>
</svg>`;
}

function metafora() {
  const at = D.atributos.map((a, i) => `<div class="at"><div class="an">ATRIBUTO ${i + 1}</div><h3>${a.t}</h3><p>${a.en}</p>
     <div class="nr"><span><b>Necesidad</b>${a.nec}</span><span><b>Requerimiento</b>${a.req}</span></div></div>`).join('');
  return base(1800, 1500, 'Panel de metáforas y atributos', 'INSTRUMENTO 2.1.4.3 · SEMANA 7',
    `<div class="top">
       <div class="met"><div class="lbl">METÁFORA</div><h2>“${D.metafora.titulo}”</h2><p>${D.metafora.bajada}</p><p class="why">${D.metafora.porque}</p>
       <div class="otras"><b>Metáforas descartadas</b>${D.metafora.otras.map((o) => `<div>· ${o}</div>`).join('')}</div></div>
       <div class="col"><div class="lbl dark">COLLAGE</div>${collageSvg()}</div>
     </div>
     <div class="ats">${at}</div>`,
    `.top{display:grid;grid-template-columns:1fr 1.15fr;gap:24px}
     .met{background:${NAVY};color:#fff;border-radius:10px;padding:28px}
     .lbl{font-family:'Liberation Mono',monospace;color:${ORANGE};letter-spacing:3px;font-size:15px;font-weight:700;margin-bottom:8px}
     .lbl.dark{color:${NAVY}}
     .met h2{font-size:36px;line-height:1.15;margin-bottom:14px}
     .met p{font-size:18px;line-height:1.5;margin-bottom:12px}
     .met .why{opacity:.8;font-size:16px}
     .otras{border-top:1px solid #ffffff33;padding-top:12px;font-size:15px;line-height:1.5;opacity:.85}
     .otras b{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:${ORANGE}}
     .col{background:#fff;border-radius:10px;padding:18px;box-shadow:0 4px 16px rgba(0,0,0,.08)}
     .col svg{width:100%;height:auto;display:block}
     .ats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:24px}
     .at{background:#fff;border-radius:8px;padding:20px;border-top:6px solid ${ORANGE};box-shadow:0 4px 16px rgba(0,0,0,.08);display:flex;flex-direction:column}
     .an{font-family:'Liberation Mono',monospace;font-size:13px;color:${ORANGE};font-weight:700}
     .at h3{font-size:28px;margin:6px 0 8px}
     .at p{font-size:16.5px;line-height:1.45;margin-bottom:14px}
     .nr{margin-top:auto;display:flex;flex-direction:column;gap:8px;font-size:14px;line-height:1.35}
     .nr span{background:#F4F3EF;border-radius:6px;padding:8px 10px}
     .nr b{display:block;font-size:11.5px;text-transform:uppercase;letter-spacing:.6px}`);
}

const boards = [
  { file: 'S6_01_fichas_referentes', w: 1800, h: 1000, html: fichas },
  { file: 'S6_02_matriz_referentes', w: 1800, h: 1000, html: matriz },
  { file: 'S6_03_tendencias', w: 1800, h: 800, html: tendencias },
  { file: 'S7_01_canvas_brainstorming', w: 1800, h: 1000, html: brainstorming },
  { file: 'S7_02_mapa_clasificacion', w: 1800, h: 1150, html: clasificacion },
  { file: 'S7_03_categorias_concepto', w: 1800, h: 900, html: categorias },
  { file: 'S7_04_panel_metaforas', w: 1800, h: 900, html: metafora },
];

async function render(outDir) {
  const { chromium } = require('playwright');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1.5 });
  for (const b of boards) {
    await page.setViewportSize({ width: b.w, height: 400 });
    const html = b.html();
    fs.writeFileSync(path.join(outDir, b.file + '.html'), html);
    await page.setContent(html, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(outDir, b.file + '.png'), fullPage: true });
  }
  await browser.close();
  return boards;
}

module.exports = { render, boards };
