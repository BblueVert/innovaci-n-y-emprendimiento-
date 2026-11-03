// Regenera tableros (PNG) y documentos Word de la Unidad 2.
// Uso: npm i docx playwright  →  node build.js
const path = require('path');
const { render } = require('./boards');
const { build } = require('./docs');

(async () => {
  const tab = path.join(__dirname, '..', 'tableros');
  await render(tab);
  const files = await build(tab, path.join(__dirname, '..', 'entregas'));
  console.log('Generado:\n' + files.join('\n'));
})();
