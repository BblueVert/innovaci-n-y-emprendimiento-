// Genera las capturas de la app Copiloto Kine (390×844 @2x) para la presentación EV2.
// Uso: node unidad-2/_build/capturas_app.js   (requiere Playwright con Chromium)
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const APP = 'file://' + path.resolve(__dirname, '../app/index.html');
const OUT = path.resolve(__dirname, '../app/capturas');
fs.mkdirSync(OUT, { recursive: true });

// [archivo, versión, ruta, pasos previos (clics dentro de la pantalla)]
const SHOTS = [
  ['v1-01-conectar', 1, 'conectar'],
  ['v1-02-reglas', 1, 'reglas'],
  ['v1-03-hoy', 1, 'hoy'],
  ['v1-04-atencion', 1, 'atencion/a3'],
  ['v1-05-tablero', 1, 'tablero'],
  ['v1-06-proyeccion', 1, 'proyeccion'],
  ['v1-07-cierre', 1, 'cierre'],
  ['v2-00-inicio', 2, 'inicio'],
  ['v2-01-conectar', 2, 'conectar'],
  ['v2-02-reglas', 2, 'reglas'],
  ['v2-03-hoy', 2, 'hoy'],
  ['v2-04-ruta', 2, 'ruta'],
  ['v2-05-atencion', 2, 'atencion/a3'],
  ['v2-06-cupo', 2, 'cupo', ['[data-act="cupo-offer"]']],
  ['v2-07-tablero', 2, 'tablero'],
  ['v2-08-proyeccion', 2, 'proyeccion'],
  ['v2-09-cierre', 2, 'cierre', ['[data-act="q1"]', '[data-act="q2"][data-v="0"]', '[data-act="q3"][data-v="0"]']],
  ['v2-10-cierre-listo', 2, 'cierre', ['[data-act="cerrar"]']],
  ['v2-11-resumen', 2, 'resumen'],
  ['v2-12-ajustes', 2, 'ajustes'],
  ['p-01-reserva', 2, 'p-reserva'],
  ['p-02-reserva-ok', 2, 'p-reserva', ['[data-act="reservar"]']],
  ['p-03-whatsapp-luis', 2, 'p-luis'],
  ['p-04-pago', 2, 'p-pago'],
  ['p-05-pago-ok', 2, 'p-pago', ['[data-act="pagar"]']],
  ['p-06-whatsapp-camila', 2, 'p-camila'],
  ['p-07-whatsapp-camila-ok', 2, 'p-camila', ['[data-act="cupo-take"]']],
  ['v2-13-hoy-cupo-tomado', 2, 'hoy']
];

(async () => {
  const browser = await chromium.launch();
  const errors = [];
  for (const v of [1, 2]) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => errors.push(`v${v}: ${e.message}`));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(`v${v} console: ${m.text()}`); });
    await page.goto(`${APP}?v=${v}&shot=1#/hoy`);
    await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
    await page.goto(`${APP}?v=${v}&shot=1#/hoy`);
    for (const [file, ver, route, steps] of SHOTS) {
      if (ver !== v) continue;
      await page.evaluate((r) => { location.hash = '#/' + r; }, route);
      await page.waitForTimeout(120);
      for (const sel of steps || []) { await page.click(sel); await page.waitForTimeout(80); }
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(2400); // deja pasar los avisos (toast)
      await page.screenshot({ path: path.join(OUT, file + '.png') });
      process.stdout.write('.');
    }
    await ctx.close();
  }
  // Vista de escritorio del prototipo (navegador de pantallas)
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 920 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(`${APP}?v=2#/hoy`);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(OUT, 'escritorio-prototipo.png') });
  await browser.close();
  console.log('\n' + (errors.length ? 'ERRORES:\n' + errors.join('\n') : 'Sin errores de JavaScript.'));
})();
