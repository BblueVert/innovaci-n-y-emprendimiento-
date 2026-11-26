"""Imagen de la portada EV4: los instrumentos reales de la unidad (los que se presentan a continuación)."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TK = os.path.join(HERE, '..', 'tablero_toolkit', 'img')
OUT = os.path.join(HERE, '..', '..', 'unidad-3', 'ev3', 'img', 'ev4-instrumentos.jpg')
FONT = ImageFont.truetype('/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf', 26)

BG, ACC = (30, 26, 48), (255, 107, 53)
W, G = 1240, 44                       # ancho del lienzo y margen/gap
COLW = (W - 3 * G) // 2

# (archivo, etiqueta, columna)
ITEMS = [('u4_form.jpg', '4.1.3.1 · FORMULARIO', 0), ('u4_pitch.jpg', 'MODELO DE NEGOCIO', 0),
         ('u4_lean.jpg', '4.1.2.1 · LEAN CANVAS', 1), ('u4_guion.jpg', '4.1.3.2 · GUION PITCH', 1)]


def card(f):
    im = Image.open(os.path.join(TK, f)).convert('RGB')
    return im.resize((COLW, round(COLW * im.size[1] / im.size[0])), Image.LANCZOS)


cols = {0: [], 1: []}
for f, lab, c in ITEMS:
    cols[c].append((card(f), lab))
heights = [sum(im.size[1] for im, _ in v) + G * (len(v) - 1) for v in cols.values()]
H = max(heights) + 2 * G
canvas = Image.new('RGB', (W, H), BG)

for c, v in cols.items():
    x = G + c * (COLW + G)
    y = G + (H - 2 * G - heights[c]) // 2
    for im, lab in v:
        sh = Image.new('L', (W, H), 0)
        ImageDraw.Draw(sh).rectangle([x + 8, y + 14, x + COLW + 8, y + im.size[1] + 14], fill=150)
        canvas.paste((8, 6, 16), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
        canvas.paste(im, (x, y))
        d = ImageDraw.Draw(canvas)
        tw = d.textlength(lab, font=FONT)
        d.rounded_rectangle([x + 14, y + 14, x + 14 + tw + 28, y + 14 + 46], 23, fill=ACC)
        d.text((x + 28, y + 23), lab, font=FONT, fill='white')
        y += im.size[1] + G

canvas.save(OUT, quality=92)
print(OUT, canvas.size)
