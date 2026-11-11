// Ciclo 1 · recorrido de tareas + accesibilidad (WCAG 2 A/AA con axe-core) + objetivos táctiles + tipografía.
// Uso: node evaluar_prototipo.js <ruta-html> <salida.json>
const { chromium } = require('playwright');
const fs = require('fs');
const FILE = process.argv[2], OUT = process.argv[3];

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 390, height: 844 } });
  const u = 'file://' + FILE;
  const R = { archivo: FILE.split('/').pop(), tasks: [], axe: {}, targets: {}, fonts: {} };
  let taps = 0;
  const tap = async s => { taps++; await p.click(s, { timeout: 3000 }); await p.waitForTimeout(150); };
  const task = async (id, name, fn) => {
    await p.goto(u + '#inicio'); await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForTimeout(300);
    taps = 0; let ok = true, obs = '';
    try { obs = (await fn()) || ''; } catch (e) { ok = false; obs = e.message.split('\n')[0]; }
    R.tasks.push({ id, name, taps, ok, obs });
  };

  await task('T1', 'Saber cuánto ganó en el mes y si va bien', async () => `Visible sin tocar nada: ${await p.textContent('#mNet')} · ${(await p.textContent('#mLight')).trim()}`);
  await task('T2', 'Registrar una atención como realizada', async () => { await tap('a[data-nav=agenda]'); await tap('[data-done=a1]'); return 'Hoja de ganancia visible: ' + await p.isVisible('#scrim'); });
  await task('T3', 'Entender de qué se compone la ganancia de una atención', async () => { await tap('a[data-nav=agenda]'); await tap('[data-done=a3]'); return (await p.$$eval('#sRows .row', r => r.map(x => x.innerText.replace(/\n/g, ' ')))).join(' | '); });
  await task('T4', 'Corregir una atención marcada por error', async () => { await tap('a[data-nav=agenda]'); await tap('[data-done=a2]'); await tap('#sClose'); if (!(await p.$$('[data-undo]')).length) throw new Error('No existe opción para deshacer o editar la atención'); await tap('[data-undo]'); return 'Se puede deshacer'; });
  await task('T5', 'Ver la ruta del día y avisar al primer paciente', async () => { await tap('a[data-nav=ruta]'); await tap('[data-notify=a3]'); return 'Feedback: ' + (await p.textContent('#toast')); });
  await task('T6', 'Comparar la ruta sugerida con el orden original', async () => { await tap('a[data-nav=ruta]'); await tap('#rOrig'); return 'Ahorro visible en orden original: ' + await p.isVisible('#saving'); });
  await task('T7', 'Saber cuánto falta para cubrir enero y febrero y agregar una acción', async () => { await tap('a[data-nav=proyeccion]'); const a = await p.textContent('#gapNote'); await tap('[data-k=packs]'); return a.trim() + ' → ' + (await p.textContent('#gapNote')).trim(); });
  await task('T8', 'Saber cuánto tiene separado para impuestos', async () => { await tap('a[data-nav=impuestos]'); return 'Impuestos: ' + await p.textContent('#j2'); });
  await task('T9', 'Cambiar el costo por km o la comisión de la clínica', async () => { await tap('a[data-nav=impuestos]'); if (!(await p.$$('#v-impuestos input')).length) throw new Error('Los costos se muestran pero no se pueden editar'); return 'Costos editables'; });
  await task('T10', 'Marcar que un paciente no asistió', async () => { await tap('a[data-nav=agenda]'); if (!(await p.$$('[data-noshow]')).length) throw new Error('No existe estado de inasistencia o cancelación'); await tap('[data-noshow]'); return 'Inasistencia registrada'; });
  await task('T11', 'Preparar la información del mes para la contadora', async () => { if (!(await p.$$('[data-export]')).length) throw new Error('No existe exportación para la contadora'); return 'Exportación disponible'; });

  const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
  for (const v of ['inicio', 'ruta', 'agenda', 'proyeccion', 'impuestos']) {
    await p.goto(u + '#' + v); await p.waitForTimeout(400); await p.addScriptTag({ content: axeSrc });
    R.axe[v] = await p.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa'] })).violations.map(x => ({ id: x.id, impact: x.impact, n: x.nodes.length, help: x.help, ej: x.nodes.slice(0, 3).map(n => n.target.join(' ')) })));
    R.targets[v] = await p.evaluate(() => [...document.querySelectorAll('button,a,input,select')].filter(e => e.offsetParent && !e.closest('[hidden]')).map(e => { const r = e.getBoundingClientRect(); return { t: (e.innerText || e.getAttribute('aria-label') || e.id || '').trim().replace(/\s+/g, ' ').slice(0, 32), w: Math.round(r.width), h: Math.round(r.height) }; }).filter(x => x.h < 44 || x.w < 44));
    R.fonts[v] = await p.evaluate(() => { const s = {}; [...document.querySelectorAll('body *')].filter(e => e.offsetParent && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())).forEach(e => { const f = parseFloat(getComputedStyle(e).fontSize); s[f] = (s[f] || 0) + 1; }); return s; });
  }
  fs.writeFileSync(OUT, JSON.stringify(R, null, 1));
  console.log('ok');
  await b.close();
})();
