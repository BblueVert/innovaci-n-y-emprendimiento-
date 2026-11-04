// Arma imágenes de 3 teléfonos (fondo transparente) con las capturas de la app,
// para insertarlas en las plantillas PowerPoint de la entrega.
// Uso: node unidad-2/_build/composiciones_mockup.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const CAP = path.resolve(__dirname, '../app/capturas');
const OUT = path.resolve(__dirname, '../entrega_ev2/img');
fs.mkdirSync(OUT, { recursive: true });

const SETS = {
  'mockup-v1': ['v1-04-atencion', 'v1-05-tablero', 'v1-06-proyeccion'],
  'mockup-v2': ['v2-05-atencion', 'v2-07-tablero', 'v2-08-proyeccion'],
  'mockup-v2-dia': ['v2-03-hoy', 'v2-04-ruta', 'v2-10-cierre-listo'],
  'mockup-paciente': ['p-01-reserva', 'p-03-whatsapp-luis', 'p-04-pago']
};

const page = (files) => `<!doctype html><html><head><style>
  html,body{margin:0;background:transparent}
  .row{display:flex;gap:34px;padding:26px 30px 40px;width:max-content}
  .ph{width:250px;border-radius:38px;background:#0D0B18;padding:9px;box-shadow:0 18px 34px rgba(14,40,65,.28)}
  .ph img{width:100%;display:block;border-radius:30px}
</style></head><body><div class="row">${files.map((f) => `<div class="ph"><img src="file://${CAP}/${f}.png"></div>`).join('')}</div></body></html>`;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 2 });
  for (const [name, files] of Object.entries(SETS)) {
    const tmp = path.join(OUT, '_tmp.html');
    fs.writeFileSync(tmp, page(files));
    await p.goto('file://' + tmp);
    await p.waitForLoadState('networkidle');
    const el = await p.$('.row');
    await el.screenshot({ path: path.join(OUT, name + '.png'), omitBackground: true });
    fs.unlinkSync(tmp);
    console.log(name);
  }
  await b.close();
})();
