// Exporta una presentación HTML (por defecto la EV2) a PDF (1280×720 por lámina) y deja vistas previas PNG.
// Uso: node unidad-2/_build/render_presentacion.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

// Uso: node render_presentacion.js [archivo.html] [carpeta_vistas_previas]
const args = process.argv.slice(2);
const HTML = args[0] && args[0].endsWith('.html') ? path.resolve(args.shift()) : path.resolve(__dirname, '../ev2/Evaluacion2_Presentacion.html');
const PDF = HTML.replace(/\.html$/, '.pdf');
const PREV = args[0]; // carpeta opcional para vistas previas PNG

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + HTML, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const missing = await page.evaluate(() => [...document.images].filter((i) => !i.complete || !i.naturalWidth).map((i) => i.getAttribute('src')));
  if (missing.length) console.log('Imágenes sin cargar:', missing.join(', '));
  if (PREV) {
    fs.mkdirSync(PREV, { recursive: true });
    const slides = await page.$$('section.slide');
    for (let i = 0; i < slides.length; i++) await slides[i].screenshot({ path: path.join(PREV, 's' + String(i + 1).padStart(2, '0') + '.png') });
  }
  await page.pdf({ path: PDF, width: '1280px', height: '720px', printBackground: true });
  await browser.close();
  console.log('PDF listo:', PDF);
})();
