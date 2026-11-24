// Iteración v3 · verificación del prototipo v3 antes de la sesión con Josselyn (ciclo 4).
// Recorre las 11 tareas base (regresión) + 10 tareas nuevas trazadas a la retroalimentación del 12/11,
// compara los cálculos con una referencia independiente, audita WCAG 2.1 AA (axe-core), objetivos táctiles y letra,
// y guarda las capturas del mock-up iterado.
// Uso: node verificar_v3.js ../prototipo/copiloto-kine.html resultados_v3.json ../prototipo/capturas_v3
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const FILE = path.resolve(process.argv[2]), OUT = process.argv[3], SHOTS = process.argv[4];
const num = t => +String(t).replace(/[^\d]/g, '') * (String(t).includes('−') ? -1 : 1);

// Referencia independiente (hoja de cálculo del equipo) con los valores por defecto del v3
const REF = { RET: 0.1525, KM: 180, VH: 15000,
  S: { home: [30000, 1200, 60], pool: [35000, 8000, 45], gym: [22000, 1500, 60] },
  A: { a4: ['home', 3, 8], a5: ['home', 14, 28], a6: ['pool', 17, 30], a7: ['gym', 7, 12] },
  net(id) { const [k, km] = this.A[id], [p, c] = this.S[k]; return p - km * this.KM - c - p * this.RET; },
  perh(id) { const [k, , tm] = this.A[id]; return this.net(id) / ((this.S[k][2] + tm) / 60); },
  hidden(id) { return this.A[id][2] / 60 * this.VH; },
  clinic() { return 25000 * 0.7 * (1 - this.RET); } };

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, acceptDownloads: true });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  const u = 'file://' + FILE;
  const R = { archivo: path.basename(FILE), fecha: new Date().toISOString().slice(0, 10), tasks: [], calculos: [], axe: {}, targets: {}, fonts: {}, errores: errs };
  let taps = 0;
  const tap = async s => { taps++; await p.click(s, { timeout: 3000 }); await p.waitForTimeout(120); };
  const fresh = async (h = 'inicio') => { await p.goto(u + '#' + h); await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForTimeout(250); };
  const task = async (id, origen, name, fn) => {
    await fresh(); taps = 0; let ok = true, obs = '';
    try { obs = (await fn()) || ''; } catch (e) { ok = false; obs = e.message.split('\n')[0]; }
    R.tasks.push({ id, origen, name, taps, ok, obs: String(obs).replace(/\s+/g, ' ').trim() });
  };
  const txt = async s => (await p.textContent(s)).replace(/\s+/g, ' ').trim();

  // ---- regresión: tareas del ciclo 1 adaptadas al v3
  await task('T1', 'EV2', 'Saber cuánto ganó en el mes y si va bien', async () => `${await txt('#mNet')} · ${await txt('#mLight')}`);
  await task('T2', 'EV2', 'Registrar una atención como realizada', async () => { await tap('a[data-nav=agenda]'); await tap('[data-done=a4]'); return 'Hoja visible: ' + await p.isVisible('#scrim'); });
  await task('T3', 'EV2', 'Entender de qué se compone la ganancia de una atención', async () => { await tap('a[data-nav=agenda]'); await tap('[data-done=a5]'); return (await p.$$eval('#sRows .row', r => r.map(x => x.innerText.replace(/\n/g, ' ')))).join(' · '); });
  await task('T4', 'EV2', 'Corregir una atención marcada por error', async () => { await tap('a[data-nav=agenda]'); await tap('[data-done=a4]'); await tap('#sClose'); await tap('[data-undo=a4]'); return 'Deshecha'; });
  await task('T5', 'EV2', 'Ver la ruta y avisar al primer paciente', async () => { await tap('a[data-nav=ruta]'); await tap('[data-notify=a4]'); return await txt('#toast'); });
  await task('T6', 'EV2', 'Comparar la ruta sugerida con el orden original', async () => { await tap('a[data-nav=ruta]'); await tap('#rOrig'); return await txt('#savingTxt'); });
  await task('T7', 'EV2', 'Saber cuánto falta para enero y febrero y agregar una acción', async () => { await tap('a[data-nav=proyeccion]'); const a = await txt('#gapNote'); await tap('[data-k=packs]'); return a + ' → ' + await txt('#gapNote'); });
  await task('T8', 'EV2', 'Saber cuánto tiene separado para impuestos', async () => { await tap('a[data-nav=impuestos]'); return 'Impuestos: ' + await txt('#j2'); });
  await task('T9', 'EV2', 'Cambiar el costo por km', async () => { await tap('a[data-nav=impuestos]'); await p.fill('#cKm', '200'); await p.dispatchEvent('#cKm', 'change'); taps++; return 'Costo por km = 200'; });
  await task('T10', 'EV2', 'Marcar que un paciente no asistió', async () => { await tap('a[data-nav=agenda]'); await tap('[data-noshow=a7]'); return await txt('#dCount'); });
  await task('T11', 'EV2', 'Preparar la información para la contadora', async () => { await tap('a[data-nav=impuestos]'); const [d] = await Promise.all([p.waitForEvent('download'), tap('[data-export]')]); return 'Descarga: ' + d.suggestedFilename(); });

  // ---- tareas nuevas: una por cambio de la retroalimentación del 12/11
  await task('N1', 'RF3 · cambio 1', 'Saber de qué agenda viene cada cita', async () => { await tap('a[data-nav=agenda]'); const s = await p.$$eval('.appt .src', x => [...new Set(x.map(e => e.textContent))]); if (!s.includes('AgendaPro') || !s.includes('Agenda clínica')) throw new Error('Falta el origen de las citas'); return 'Orígenes: ' + s.join(' + '); });
  await task('N2', 'RF5 · cambio 2', 'Saber qué canal le rinde más por hora', async () => { const r = await p.$$eval('#rank .r', x => x.map(e => e.querySelector('b').textContent + ' ' + e.querySelector('.v').textContent)); return 'Sin tocar nada: ' + r.join(' > '); });
  await task('N3', 'RF6 · cambio 3', 'Ver cuánto le cuesta en tiempo el domicilio de Aguas Buenas y qué cobrar', async () => { await tap('a[data-nav=agenda]'); await tap('[data-done=a5]'); return await txt('#sExtra .hidden-cost'); });
  await task('N4', 'RF4 · cambio 4', 'Registrar la clínica como monto fijo mensual', async () => { await tap('a[data-nav=impuestos]'); const before = await p.getAttribute('#cmF', 'aria-pressed'); if (before !== 'true') await tap('#cmF'); await tap('a[data-nav=agenda]'); await tap('[data-done=a1]'); return (before === 'true' ? 'Ya activo por defecto · ' : '') + await txt('#sNote'); });
  await task('N5', 'RF7 · cambio 5', 'Cambiar el valor de la sesión en piscina', async () => { await tap('a[data-nav=impuestos]'); await p.fill('#sp-pool', '38000'); await p.dispatchEvent('#sp-pool', 'change'); taps++; await tap('a[data-nav=agenda]'); await tap('[data-done=a6]'); return 'Piscina a $38.000 → ' + await txt('#sRows .row.total'); });
  await task('N6', 'RF10 · cambio 6', 'Armar una clase grupal y saber desde cuántas personas conviene', async () => { await tap('a[data-nav=proyeccion]'); await tap('[data-k=grupo]'); await tap('#gPlus'); return await txt('#grpCard .insight') + ' · ' + await txt('#gapNote'); });
  await task('N7', 'Mabel · Ariel · cambio 7', 'Ver el resumen del mes por canal y descargarlo para Excel', async () => { await tap('a[data-nav=impuestos]'); await tap('#pM'); const n = await txt('#repNote'); const [d] = await Promise.all([p.waitForEvent('download'), tap('[data-export]')]); return n + ' · ' + d.suggestedFilename(); });
  await task('N8', 'RF8 · cambio 8', 'Reconocer su territorio en la ruta', async () => { await tap('a[data-nav=ruta]'); const t = await txt('#stops'); for (const w of ['San Fernando', 'Aguas Buenas', 'Roma']) if (!t.includes(w)) throw new Error('Falta ' + w); return 'San Fernando · Aguas Buenas · camino a Roma · ' + await txt('#tripCost'); });
  await task('N9', 'Planilla de otro equipo', 'Registrar el medio de pago de una atención', async () => { await tap('a[data-nav=agenda]'); await tap('[data-done=a4]'); await tap('[data-pay=a4][data-m=Transferencia]'); await tap('#sClose'); return 'Etiqueta en agenda: ' + await p.isVisible('.appt .tag:text("Transferencia")'); });
  await task('N10', 'RF2', 'Cerrar el día completo con resumen (reemplaza la nota de la noche)', async () => {
    await tap('a[data-nav=agenda]');
    for (const id of ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']) { await tap(`[data-done=${id}]`); await tap('#sClose'); }
    await tap('#closeDay'); return (await p.$$eval('#sRows .row', r => r.map(x => x.innerText.replace(/\n/g, ' ')))).join(' · '); });

  // ---- cálculos contra referencia
  await fresh('agenda');
  for (const id of ['a4', 'a5', 'a6', 'a7']) {
    await p.click(`[data-done=${id}]`); await p.waitForTimeout(100);
    const net = num(await p.textContent('#sRows .row.total span:last-child')), perh = num(await p.textContent('#sExtra .perh b'));
    const hid = num((await p.textContent('#sExtra .hidden-cost')).split('≈')[1].split('de')[0]);
    R.calculos.push({ id, net_app: net, net_ref: Math.round(REF.net(id)), perh_app: perh, perh_ref: Math.round(REF.perh(id)), viaje_app: hid, viaje_ref: Math.round(REF.hidden(id)),
      ok: Math.abs(net - REF.net(id)) <= 1 && Math.abs(perh - REF.perh(id)) <= 1 && Math.abs(hid - REF.hidden(id)) <= 1 });
    await p.click('#sClose');
  }
  await p.goto(u + '#impuestos'); await p.click('#cmA'); await p.goto(u + '#agenda'); await p.waitForTimeout(150);
  await p.click('[data-done=a2]'); const cn = num(await p.textContent('#sRows .row.total span:last-child'));
  R.calculos.push({ id: 'a2 (clínica por atención)', net_app: cn, net_ref: Math.round(REF.clinic()), ok: Math.abs(cn - REF.clinic()) <= 1 }); await p.click('#sClose');

  // ---- accesibilidad, objetivos táctiles y letra por vista (estado con hojas y grupo abiertos)
  const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
  for (const v of ['inicio', 'ruta', 'agenda', 'proyeccion', 'impuestos']) {
    await fresh(v);
    if (v === 'proyeccion') await p.click('[data-k=grupo]');
    await p.addScriptTag({ content: axeSrc });
    R.axe[v] = await p.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa'] })).violations.map(x => ({ id: x.id, impact: x.impact, n: x.nodes.length, help: x.help, ej: x.nodes.slice(0, 3).map(n => n.target.join(' ')) })));
    R.targets[v] = await p.evaluate(() => [...document.querySelectorAll('button,a,input,select')].filter(e => e.offsetParent && !e.closest('[hidden]')).map(e => { const r = e.getBoundingClientRect(); return { t: (e.innerText || e.getAttribute('aria-label') || e.id || '').trim().replace(/\s+/g, ' ').slice(0, 32), w: Math.round(r.width), h: Math.round(r.height) }; }).filter(x => x.h < 44 || x.w < 44));
    R.fonts[v] = await p.evaluate(() => { const s = {}; [...document.querySelectorAll('body *')].filter(e => e.offsetParent && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())).forEach(e => { const f = parseFloat(getComputedStyle(e).fontSize); s[f] = (s[f] || 0) + 1; }); return s; });
  }
  await fresh('agenda'); await p.click('[data-done=a5]'); await p.waitForTimeout(500); await p.addScriptTag({ content: axeSrc });
  R.axe['hoja-atencion'] = await p.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa'] })).violations.map(x => ({ id: x.id, n: x.nodes.length, help: x.help })));
  R.peso_kb = +(fs.statSync(FILE).size / 1024).toFixed(1);

  // ---- capturas del mock-up iterado (390 × 844 a 2×)
  if (SHOTS) {
    fs.mkdirSync(SHOTS, { recursive: true });
    const shot = async (name, view, prep, scrollTo) => {
      await fresh(view); if (prep) await prep();
      if (scrollTo) await p.evaluate(s => { const e = document.querySelector(s); window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - 70); }, scrollTo);
      await p.waitForTimeout(250); await p.screenshot({ path: path.join(SHOTS, name) });
    };
    const doneAll = async () => { for (const id of ['a1', 'a2', 'a3']) { await p.click(`[data-done=${id}]`); await p.click('#sClose'); } };
    await shot('01_tablero.png', 'inicio');
    await shot('02_ganancia_por_hora.png', 'inicio', null, '#rank');
    await shot('03_ruta.png', 'ruta');
    await shot('04_paradas_tramos.png', 'ruta', null, '#stops');
    await shot('05_agenda.png', 'agenda', doneAll, '#agendaList .slot:nth-child(3)');
    await shot('06_atencion_agua_buena.png', 'agenda', async () => { await p.click('[data-done=a5]'); await p.click('[data-pay=a5][data-m=Transferencia]'); });
    await shot('07_clase_grupal.png', 'proyeccion', async () => { await p.click('[data-k=grupo]'); }, '#grpCard');
    await shot('08_resumen_canal.png', 'impuestos');
    await shot('09_clinica_factura.png', 'impuestos', null, '#cmA');
    await shot('10_servicios.png', 'impuestos', null, '#svc');
    await shot('11_cierre_dia.png', 'agenda', async () => { for (const id of ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']) { await p.click(`[data-done=${id}]`); await p.click('#sClose'); } await p.click('#closeDay'); });
  }
  fs.writeFileSync(OUT, JSON.stringify(R, null, 1));
  const ok = R.tasks.filter(t => t.ok).length, ax = Object.values(R.axe).flat().reduce((s, x) => s + x.n, 0), tg = Object.values(R.targets).flat().length;
  console.log(`tareas ${ok}/${R.tasks.length} · cálculos ${R.calculos.filter(c => c.ok).length}/${R.calculos.length} · axe ${ax} · táctiles<44 ${tg} · errores JS ${errs.length} · ${R.peso_kb} KB`);
  await b.close();
})();
