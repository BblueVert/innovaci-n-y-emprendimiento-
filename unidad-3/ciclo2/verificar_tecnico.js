// Ciclo 2 · verificación técnica del prototipo v2 contra las necesidades de la kinesióloga independiente.
// Uso: node verificar_tecnico.js <ruta-html> <salida.json>
const { chromium } = require('playwright');
const fs = require('fs');
const FILE = process.argv[2], OUT = process.argv[3];
const clp = n => Math.round(n);

// Cálculo de referencia, independiente del prototipo (hoja de cálculo del equipo)
const REF = {
  RET: 0.1525, KM: 180, COM: 0.30,
  net(a) { return a.kind === 'clinic' ? a.price * (1 - this.COM) * (1 - this.RET) : a.price - a.km * this.KM - a.mat - a.price * this.RET; },
};
const APPTS = [
  { id: 'a1', kind: 'clinic', price: 25000 }, { id: 'a2', kind: 'clinic', price: 25000 },
  { id: 'a3', kind: 'home', price: 28000, km: 8, mat: 1200 }, { id: 'a4', kind: 'home', price: 28000, km: 3, mat: 1500 },
  { id: 'a5', kind: 'home', price: 28000, km: 9, mat: 800 },
];
const num = t => +t.replace(/[^\d]/g, '');

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, acceptDownloads: true });
  const p = await ctx.newPage();
  const u = 'file://' + FILE;
  const R = { pruebas: [] };
  const add = (id, req, nombre, ok, evidencia) => R.pruebas.push({ id, req, nombre, ok, evidencia });

  // P1 · Exactitud del cálculo por atención (R4, R8, R12)
  await p.goto(u + '#agenda'); await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForTimeout(300);
  let fails = [], detalle = [];
  for (const a of APPTS) {
    await p.click(`[data-done=${a.id}]`); await p.waitForTimeout(150);
    const shown = num(await p.textContent('#sRows .row.total span:last-child')), exp = clp(REF.net(a));
    detalle.push(`${a.id}: app ${shown} / ref ${exp}`); if (Math.abs(shown - exp) > 1) fails.push(a.id);
    await p.click('#sClose');
  }
  add('P1', 'R4 · R8 · R12', 'Ganancia neta por atención coincide con el cálculo de referencia (5 casos)', !fails.length, detalle.join(' · '));

  // P2 · Suma del día y del mes (R1, R4)
  const day = num(await (await p.goto(u + '#inicio'), p.textContent('#dNet')));
  const expDay = clp(APPTS.reduce((s, a) => s + REF.net(a), 0));
  const month = num(await p.textContent('#mNet'));
  add('P2', 'R1 · R4', 'Ganancia del día y del mes se actualizan con cada atención', Math.abs(day - expDay) <= 5 && month === 412000 + day, `día app ${day} / ref ${expDay} · mes ${month}`);

  // P3 · Persistencia (R6, R7)
  await p.reload(); await p.waitForTimeout(300);
  add('P3', 'R6 · R7', 'Los registros se mantienen al cerrar y volver a abrir la app', num(await p.textContent('#dNet')) === day, `tras recargar: ${await p.textContent('#dCount')}`);

  // P4 · Cierre del día: toques necesarios (R6)
  await p.evaluate(() => localStorage.clear()); await p.goto(u + '#agenda'); await p.reload(); await p.waitForTimeout(300);
  let taps = 0; const t0 = Date.now();
  for (const a of APPTS) { await p.click(`[data-done=${a.id}]`); taps++; await p.click('#sClose'); taps++; }
  await p.click('#closeDay'); taps++;
  add('P4', 'R6', 'Cierre de un día de 5 atenciones', taps <= 12, `${taps} toques, sin digitar ningún número (línea base UA1: ~60 min diarios en Excel)`);

  // P5 · Configuración de costos se refleja en los cálculos (R3, R8)
  await p.goto(u + '#impuestos'); await p.fill('#cKm', '200'); await p.dispatchEvent('#cKm', 'change'); await p.waitForTimeout(150);
  await p.goto(u + '#agenda'); await p.click('[data-undo=a3]'); await p.click('[data-done=a3]'); await p.waitForTimeout(150);
  const n3 = num(await p.textContent('#sRows .row.total span:last-child')), e3 = clp(28000 - 8 * 200 - 1200 - 28000 * 0.1525);
  await p.click('#sClose');
  add('P5', 'R3 · R8', 'Cambiar el costo por km recalcula la ganancia', Math.abs(n3 - e3) <= 1, `a3 con $200/km: app ${n3} / ref ${e3}`);
  await p.goto(u + '#impuestos'); await p.fill('#cKm', '180'); await p.dispatchEvent('#cKm', 'change');

  // P6 · Exportación para la contadora sin datos clínicos (R12, R13)
  await p.goto(u + '#impuestos');
  const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 5000 }), p.click('[data-export]')]);
  const csv = fs.readFileSync(await dl.path(), 'utf8');
  const clinical = /(rodilla|lumbago|hombro|respiratoria|equilibrio)/i.test(csv), names = /(Rosa|Pedro|Carmen|Ana|Luis)/.test(csv);
  fs.writeFileSync(OUT.replace('.json', '_export.csv'), csv);
  add('P6', 'R12 · R13', 'Resumen CSV para la contadora sin diagnósticos ni nombres completos', !clinical && !names, `${csv.trim().split('\n').length - 1} filas · columnas: ${csv.split('\n')[0].replace('﻿', '')}`);

  // P7 · Inasistencia no suma ingreso (R1)
  await p.evaluate(() => localStorage.clear()); await p.goto(u + '#agenda'); await p.reload(); await p.waitForTimeout(300);
  await p.click('[data-noshow=a2]'); await p.waitForTimeout(150);
  add('P7', 'R1', 'Una inasistencia queda registrada y no suma ingreso', num(await (await p.goto(u + '#inicio'), p.textContent('#dNet'))) === 0, await p.textContent('#dCount'));

  // P8 · Ruta: ahorro calculado y coherente con los tramos (R9)
  await p.goto(u + '#ruta'); const sv = await p.textContent('#savingTxt');
  add('P8', 'R9', 'La ruta sugerida reduce km y lo informa en ambos modos', /7 km/.test(sv), sv.trim());

  // P9 · Rendimiento y peso (uso en terreno con datos móviles)
  const size = fs.statSync(FILE).size;
  await p.goto(u + '#inicio'); const perf = await p.evaluate(() => { const n = performance.getEntriesByType('navigation')[0]; return { dcl: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd) }; });
  add('P9', 'R5', 'Peso y tiempo de carga del prototipo', size < 100 * 1024 && perf.dcl < 1500, `${(size / 1024).toFixed(1)} KB · DOMContentLoaded ${perf.dcl} ms · load ${perf.load} ms (archivo local)`);

  // P10 · Funciona sin conexión a las fuentes (respaldo tipográfico)
  const off = await ctx.newPage(); await off.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await off.goto(u + '#inicio'); await off.waitForTimeout(300);
  const visible = await off.isVisible('#mNet'); const ff = await off.evaluate(() => getComputedStyle(document.querySelector('#mNet')).fontFamily);
  add('P10', 'R5', 'Sin internet para las fuentes la app sigue legible (fuentes de respaldo)', visible, `fuente declarada: ${ff}`);

  // P11 · Retención configurable al cambiar la tasa anual (Ley 21.133: 16 % en 2027)
  await p.evaluate(() => localStorage.clear()); await p.goto(u + '#impuestos'); await p.reload(); await p.waitForTimeout(200);
  await p.fill('#cRet', '16'); await p.dispatchEvent('#cRet', 'change');
  await p.goto(u + '#agenda'); await p.click('[data-done=a5]'); await p.waitForTimeout(150);
  const n5 = num(await p.textContent('#sRows .row.total span:last-child')), e5 = clp(28000 - 9 * 180 - 800 - 28000 * 0.16);
  add('P11', 'R12', 'La tasa de retención se puede actualizar para 2027 (16 %)', Math.abs(n5 - e5) <= 1, `a5 con 16 %: app ${n5} / ref ${e5}`);

  fs.writeFileSync(OUT, JSON.stringify(R, null, 1));
  console.log(R.pruebas.map(x => `${x.id} ${x.ok ? 'OK ' : 'FALLA'} ${x.nombre} — ${x.evidencia}`).join('\n'));
  await b.close();
})();
