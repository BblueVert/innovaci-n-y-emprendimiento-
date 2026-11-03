// Plantillas en blanco (SVG editable al arrastrar a Figma) para los instrumentos
// que faltan en el tablero: 2.1.3.1, 2.1.3.2, 2.1.3.3 y 2.1.4.4.
// Mismo estilo que las láminas del tablero: Bebas Neue / DM Mono / Plus Jakarta Sans.
// Uso: node figma_svg.js  →  ../figma/*.svg
const fs = require('fs');
const path = require('path');

const C = { bg: '#F7F6FB', ink: '#14142B', orange: '#FF6B35', tint: '#FFF1EA', line: '#E4E2EE', mute: '#8A8799', ph: '#B9B6C8', white: '#FFFFFF', navy: '#1B1F3B', lav: '#D9D2FF', peach: '#FFD6C2' };
const W = 3000, PAD = 140, IW = W - 2 * PAD;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function wrap(str, width, size, k = 0.52) {
  const max = Math.floor(width / (size * k));
  const out = [];
  for (const para of str.split('\n')) {
    let line = '';
    for (const w of para.split(' ')) {
      if ((line + ' ' + w).trim().length > max) { out.push(line); line = w; } else line = (line + ' ' + w).trim();
    }
    out.push(line);
  }
  return out;
}

class Svg {
  constructor() { this.els = []; }
  rect(x, y, w, h, { fill = C.white, stroke = C.line, r = 24, dash = false, sw = 3, name } = {}) {
    this.els.push(`<rect${name ? ` id="${esc(name)}"` : ''} x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}"${stroke ? ` stroke="${stroke}" stroke-width="${sw}"` : ''}${dash ? ' stroke-dasharray="18 14"' : ''}/>`);
  }
  text(x, y, str, { font = 'Plus Jakarta Sans', size = 32, weight = 400, color = C.ink, ls = 0, italic = false, width = 0, anchor = 'start', lh = 1.35, k = 0.52 } = {}) {
    const lines = width ? wrap(str, width, size, k) : str.split('\n');
    const tspans = lines.map((l, i) => `<tspan x="${x}" dy="${i ? size * lh : 0}">${esc(l)}</tspan>`).join('');
    this.els.push(`<text x="${x}" y="${y}" font-family="${font}" font-size="${size}" font-weight="${weight}"${italic ? ' font-style="italic"' : ''} fill="${color}"${ls ? ` letter-spacing="${(ls / 100) * size}"` : ''} text-anchor="${anchor}">${tspans}</text>`);
    return lines.length * size * lh;
  }
  label(x, y, str, color = C.orange, size = 30) { return this.text(x, y, str.toUpperCase(), { font: 'DM Mono', size, color, ls: 8 }); }
  ph(x, y, str, size = 34, width = 0, color = C.ph) { return this.text(x, y, str, { size, italic: true, color, width }); }
  card(x, y, w, h, title, prompt, { fill = C.white, lc = C.orange, pc = C.ph, dash = false, name } = {}) {
    this.rect(x, y, w, h, { fill, dash, name: name || title });
    this.label(x + 48, y + 78, title, lc);
    if (prompt) this.ph(x + 48, y + 140, prompt, 32, w - 96, pc);
  }
  header(lbl, title, sub) {
    this.label(PAD, PAD + 34, lbl, C.orange, 34);
    const th = this.text(PAD, PAD + 200, title.toUpperCase(), { font: 'Bebas Neue', size: 150, width: IW, k: 0.42, lh: 0.95 });
    const sy = PAD + 200 + th - 150 * 0.95 + 90;
    const h = this.text(PAD, sy, sub, { size: 38, color: C.mute, width: IW });
    return sy + h + 40;
  }
  section(y, title) {
    this.rect(PAD, y, 10, 64, { fill: C.orange, stroke: null, r: 0 });
    this.text(PAD + 34, y + 48, title, { size: 52, weight: 600 });
    return y + 104;
  }
  desafio(y) {
    this.rect(PAD, y, IW, 130, { r: 20, name: 'Desafío' });
    this.label(PAD + 40, y + 76, 'Desafío');
    this.ph(PAD + 260, y + 78, 'Pega aquí el desafío redefinido en la UA1', 36);
    return y + 170;
  }
  footer(y) {
    this.rect(PAD, y, IW, 150, { r: 20, name: 'Pie · Integrantes / Curso / Profesor' });
    const cols = [['Integrantes', 'Francisco Ahumada · Claudia Cifuentes · Néstor Rivera · Benjamín Vera Yáñez', 1300], ['Curso', 'Innovación y Emprendimiento III · Sección ____', 860], ['Profesor', '________________', 560]];
    let x = PAD + 40;
    cols.forEach(([l, v, w], i) => { this.label(x, y + 58, l, C.mute, 24); this.text(x, y + 108, v, { size: 30, color: i ? C.ph : C.ink }); x += w; });
    return y + 150 + PAD;
  }
  out(h, title) {
    h = Math.ceil(h);
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${h}" viewBox="0 0 ${W} ${h}"><title>${esc(title)}</title><rect width="${W}" height="${h}" fill="${C.bg}"/>${this.els.join('')}</svg>`;
  }
}

// ---------- 23 · Tabla con perfil de usuario y requerimientos ----------
function tabla() {
  const s = new Svg();
  let y = s.header('Técnica · Perfil de usuario y estudio de requerimientos', 'Instrumento 2.1.3.1 — Tabla con perfil de usuario y requerimientos',
    'Primero el desafío, luego el perfil (mapa de empatía) y al final cada insight con los requerimientos que debe considerar la solución.');
  y = s.desafio(y);
  y = s.section(y + 40, 'Perfil de usuario');
  s.rect(PAD, y, IW, 130, { r: 20, name: 'Usuario' }); s.label(PAD + 40, y + 76, 'Usuario'); s.ph(PAD + 260, y + 78, '¿Quién es? Nombre, rol y contexto', 36);
  y += 170;
  const emp = [['¿Qué piensa y qué siente?', 'Lo que realmente le interesa aunque no lo diga; preocupaciones e inquietudes.'], ['¿Qué ve?', 'Quiénes la rodean y qué ofertas la rodean.'], ['¿Qué oye?', 'Lo que dicen quienes la rodean y las personas influyentes para ella.'], ['¿Qué dice y qué hace?', 'Su actitud y lo que dice en público.'], ['¿Qué le duele?', 'Principales frustraciones y obstáculos.'], ['¿A qué aspira?', 'Qué desea lograr, sus objetivos y cómo los logrará.']];
  const cw = (IW - 64) / 3;
  emp.forEach(([q, h], i) => s.card(PAD + (i % 3) * (cw + 32), y + Math.floor(i / 3) * 552, cw, 520, q, h));
  y += 2 * 552 + 40;
  y = s.section(y, 'Insights y requerimientos');
  y += s.text(PAD, y + 30, 'Retomar la matriz de categorización de insights (UA1). Un insight por fila; a la derecha, los requerimientos que la solución debe cumplir.', { size: 34, color: C.mute, width: IW }) + 20;
  for (let i = 1; i <= 6; i++) {
    s.card(PAD, y, 1260, 230, 'Insight ' + i, '“Cita o hallazgo de la usuaria”', { fill: C.tint });
    s.text(PAD + 1310, y + 140, '→', { size: 72, weight: 700, color: C.orange });
    s.card(PAD + 1400, y, IW - 1400, 230, 'Requerimientos ' + i, '· …   · …');
    y += 254;
  }
  y += 20;
  s.rect(PAD, y, IW, 220, { fill: C.navy, stroke: null, r: 28, name: 'Solución' });
  s.label(PAD + 56, y + 84, 'Solución'); s.ph(PAD + 56, y + 150, 'Dirección preliminar de la solución según los requerimientos', 38, 0, '#9A98B5');
  y += 260;
  return s.out(s.footer(y), '23_2.1.3.1_Tabla_perfil_usuario_requerimientos');
}

// ---------- 24 · Mapa de categorías ----------
function categorias() {
  const s = new Svg();
  let y = s.header('Técnica · Categorización y jerarquización', 'Instrumento 2.1.3.2 — Mapa de categorías',
    'Izquierda: categorías que surgen por saturación al agrupar los requerimientos. Derecha: las necesidades de la UA1 asociadas a cada categoría.');
  for (let i = 1; i <= 6; i++) {
    s.rect(PAD, y, IW, 300, { name: 'Categoría ' + i });
    s.rect(PAD, y, 820, 300, { fill: C.navy, stroke: null, name: 'Categoría ' + i + ' · nombre' });
    s.label(PAD + 48, y + 80, 'Categoría ' + i);
    s.text(PAD + 48, y + 170, 'Nombre de la categoría', { size: 48, weight: 700, color: '#6E6B8A' });
    s.label(PAD + 868, y + 80, 'Necesidad(es)', C.mute, 26);
    s.ph(PAD + 868, y + 140, '· …\n· …\n· …', 34);
    y += 332;
  }
  return s.out(s.footer(y + 20), '24_2.1.3.2_Mapa_categorias');
}

// ---------- 25 · Mapa de jerarquías ----------
function jerarquias() {
  const s = new Svg();
  let y = s.header('Técnica · Categorización y jerarquización', 'Instrumento 2.1.3.3 — Mapa de jerarquías',
    'Definir la variable de cada eje, ubicar necesidades y requerimientos ya categorizados y consensuar su posición. Un color para necesidades y otro para requerimientos.');
  const hw = (IW - 40) / 2;
  s.card(PAD, y, hw, 200, 'Eje 1 (horizontal) · variable', 'Ej: impacto en la usuaria');
  s.card(PAD + hw + 40, y, hw, 200, 'Eje 2 (vertical) · variable', 'Ej: urgencia o frecuencia del dolor');
  y += 240;
  [['Necesidad', C.lav], ['Requerimiento', C.peach]].forEach(([n, c], i) => {
    const x = PAD + i * 420;
    s.rect(x, y, 380, 90, { r: 45 }); s.rect(x + 24, y + 25, 40, 40, { fill: c, stroke: null, r: 6 }); s.text(x + 84, y + 57, n, { size: 32, weight: 500 });
  });
  s.text(PAD + 880, y + 57, 'Usa post-its de dos colores y suéltalos libremente en el plano.', { size: 30, color: C.mute });
  y += 130;
  const pw = IW, ph = 1900;
  s.rect(PAD, y, pw, ph, { name: 'Plano' });
  s.rect(PAD + 160, y + ph / 2 - 3, pw - 320, 6, { fill: C.navy, stroke: null, r: 0 });
  s.rect(PAD + pw / 2 - 3, y + 120, 6, ph - 240, { fill: C.navy, stroke: null, r: 0 });
  const m = { font: 'DM Mono', size: 32, ls: 8 };
  s.text(PAD + pw - 180, y + ph / 2 + 60, 'EJE 1 (+) →', { ...m, anchor: 'end' });
  s.text(PAD + 170, y + ph / 2 + 60, '(−)', m);
  s.text(PAD + pw / 2 + 24, y + 170, '↑ EJE 2 (+)', m);
  s.text(PAD + pw / 2 + 24, y + ph - 140, '(−)', m);
  s.text(PAD + pw - 200, y + 240, 'PRIORIDAD ALTA', { size: 30, weight: 700, color: '#C9C6D6', anchor: 'end' });
  s.text(PAD + 200, y + ph - 200, 'PRIORIDAD BAJA', { size: 30, weight: 700, color: '#C9C6D6' });
  y += ph + 40;
  return s.out(s.footer(y), '25_2.1.3.3_Mapa_jerarquias');
}

// ---------- 26 · Panel de propuesta de valor y métricas claves ----------
function propuesta() {
  const s = new Svg();
  let y = s.header('Técnica · Diseño de propuesta de valor y métricas claves', 'Instrumento 2.1.4.4 — Panel de propuesta de valor y métricas claves',
    'Retomar necesidades (2.1.3.x) y atributos (2.1.4.3). Definir situación actual y futura, redactar la propuesta de valor con la fórmula y fijar métricas de eficiencia, eficacia y efectividad.');
  const hw = (IW - 40) / 2;
  s.card(PAD, y, hw, 240, 'Situación actual de la usuaria', '¿Cómo opera hoy? (dolor, tiempo, herramientas)');
  s.card(PAD + hw + 40, y, hw, 240, 'Situación futura deseada', '¿Qué cambia después de usar la solución?', { fill: C.tint });
  y += 280;
  s.card(PAD, y, hw, 400, 'Necesidades', 'Desde mapa de categorías y jerarquías (UA2) · …');
  s.card(PAD + hw + 40, y, hw, 400, 'Atributos', 'Desde el panel de metáforas y atributos · …');
  y += 440;
  s.rect(PAD, y, IW, 330, { fill: C.navy, stroke: null, r: 28, name: 'Fórmula propuesta de valor' });
  s.label(PAD + 48, y + 74, 'Fórmula de la propuesta de valor');
  const fq = [['¿Qué es?', 'Sustantivo'], ['¿Cómo es?', 'Atributos según el perfil'], ['¿Por qué?', 'Requerimientos que resuelve'], ['¿Para qué?', 'Fin respecto a la usuaria']];
  const fw = (IW - 96 - 72) / 4;
  fq.forEach(([q, h], i) => {
    const x = PAD + 48 + i * (fw + 24);
    s.rect(x, y + 110, fw, 180, { fill: '#272C52', stroke: null, r: 16, name: q });
    s.text(x + 28, y + 170, q, { size: 38, weight: 700, color: C.white });
    s.ph(x + 28, y + 230, h, 30, fw - 56, '#9A98B5');
  });
  y += 370;
  // Lean canvas (plantilla oficial 2.1.4.4)
  const g = 24, cw = (IW - 4 * g) / 5, full = 1360, half = (full - g) / 2;
  const X = (i) => PAD + i * (cw + g);
  s.card(X(0), y, cw, full, 'Problema', 'Problemas top 3');
  s.card(X(1), y, cw, half, 'Solución', 'Mejores 3 características del producto/servicio');
  s.card(X(1), y + half + g, cw, half, 'Métricas clave', 'Actividades clave a medir: eficiencia · eficacia · efectividad');
  s.card(X(2), y, cw, full, 'Propuesta de valor', 'Una frase simple, clara y convincente que explique por qué tu propuesta es diferente y vale la pena', { fill: C.tint });
  s.card(X(3), y, cw, half, 'Ventaja especial', 'Qué lo hace especial / diferente');
  s.card(X(3), y + half + g, cw, half, 'Canales', 'Cómo llega a la usuaria');
  s.card(X(4), y, cw, full, 'Segmento de clientes', 'Segmento objetivo · early adopters');
  y += full + g;
  s.card(PAD, y, hw, 380, 'Estructura de costes', 'Costos de adquisición del cliente, distribución, recursos humanos, etc.');
  s.card(PAD + hw + 40, y, hw, 380, 'Flujo de ingresos', 'Modelo de ingresos, valor del tiempo de vida del cliente, margen.');
  y += 420;
  return s.out(s.footer(y), '26_2.1.4.4_Panel_propuesta_valor');
}

const outDir = path.join(__dirname, '..', 'figma');
fs.mkdirSync(outDir, { recursive: true });
const files = [['23_2.1.3.1_Tabla_perfil_usuario_requerimientos', tabla], ['24_2.1.3.2_Mapa_categorias', categorias], ['25_2.1.3.3_Mapa_jerarquias', jerarquias], ['26_2.1.4.4_Panel_propuesta_valor', propuesta]];
for (const [n, fn] of files) fs.writeFileSync(path.join(outDir, n + '.svg'), fn());
console.log(files.map(([n]) => n + '.svg').join('\n'));
