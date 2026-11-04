# Copiloto Kine — prototipo funcional

App web móvil (HTML + CSS + JS, sin dependencias) del concepto seleccionado en la UA2.
Datos ficticios de ejemplo; día de demostración: martes 24 de noviembre de 2026.

- **Abrir:** `index.html` en el navegador. En el computador se ve el teléfono junto a la lista de pantallas; en el celular, a pantalla completa.
- **Versiones:** `index.html?v=1` (alcance mínimo) · `index.html?v=2` (iterada). También desde Ajustes.
- **Capturas:** `?shot=1` muestra solo la pantalla. `node unidad-2/_build/capturas_app.js` regenera `capturas/` (28 PNG a 390×844 @2x).
- **Reiniciar:** botón "Reiniciar datos de ejemplo" (el estado se guarda en el navegador).

| Grupo | Pantallas (ruta) |
|---|---|
| Joselyn · configurar | `#/inicio` · `#/conectar` · `#/reglas` · `#/ajustes` · `#/exportar` |
| Joselyn · su día | `#/hoy` · `#/ruta`* · `#/atencion/a3` · `#/cupo`* · `#/cierre` |
| Joselyn · sus números | `#/tablero` · `#/proyeccion` · `#/resumen`* |
| Paciente | `#/p-reserva` · `#/p-luis`* · `#/p-pago`* · `#/p-camila`* |

\* Solo en la V2.
