# Mockup de iPhone a partir de la foto con pantalla verde (img/mockup/iphone_greenscreen.jpg).
# Recorta el teléfono con fondo transparente y coloca cada captura dentro de la pantalla, completa y sin recortes.
# Uso: from mockup import mock; mock('../prototipo/capturas_v3/01_tablero.png') -> ruta del PNG compuesto (en caché).
import hashlib
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'img', 'mockup', 'iphone_greenscreen.jpg')
OUT = os.path.join(HERE, 'img', 'mockup', 'out')
BODY = (541, 75, 837, 691)      # caja del teléfono en la foto original (px)
RADIUS = 50                      # radio de las esquinas del cuerpo (px de la foto)
S = 3                            # factor de trabajo (supermuestreo)
W_OUT = 540                      # ancho final del PNG
STATUS = 40                      # alto de la barra de estado bajo la isla dinámica (px de la foto)
ASPECT = (BODY[2] - BODY[0]) / (BODY[3] - BODY[1])  # ancho / alto del mockup

_frame = None


def _base():
    """Marco del teléfono (RGBA, fondo transparente) + máscara de pantalla, en escala S."""
    global _frame
    if _frame is not None:
        return _frame
    im = Image.open(SRC).convert('RGB').crop(BODY)
    w, h = im.size
    im = im.resize((w * S, h * S), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # máscara de pantalla: cuánto "verde de croma" tiene cada píxel (suave en los bordes)
    green = np.clip((g - np.maximum(r, b) - 50) / 70, 0, 1)
    # quitar el reflejo verde del bisel
    spill = g > np.maximum(r, b)
    a[..., 1] = np.where(spill, np.maximum(r, b), g)
    # silueta del cuerpo: rectángulo redondeado con antialias
    big = Image.new('L', (w * S * 4, h * S * 4), 0)
    ImageDraw.Draw(big).rounded_rectangle((0, 0, w * S * 4 - 1, h * S * 4 - 1), radius=RADIUS * S * 4, fill=255)
    body = np.asarray(big.resize((w * S, h * S), Image.LANCZOS)).astype(float) / 255
    ys, xs = np.where(green > .5)
    _frame = (a, green, body, (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    return _frame


def _screen(path, sw, sh):
    """Captura completa encajada en la pantalla: franja superior para la isla y bordes extendidos."""
    shot = Image.open(path).convert('RGB')
    top = STATUS * S
    avail_h = sh - top
    nw = round(avail_h * shot.width / shot.height)
    if nw > sw:  # captura más ancha: ajustar por ancho
        nw = sw; avail_h = round(sw * shot.height / shot.width); top = sh - avail_h
    shot = shot.resize((nw, avail_h), Image.LANCZOS)
    arr = np.asarray(shot)
    x0 = (sw - nw) // 2
    # extender bordes (fondo y barra inferior quedan continuos)
    left = np.repeat(arr[:, :1], x0, axis=1)
    right = np.repeat(arr[:, -1:], sw - nw - x0, axis=1)
    mid = np.concatenate([left, arr, right], axis=1)
    head = np.repeat(mid[:1], top, axis=0)
    return np.concatenate([head, mid], axis=0)[:sh, :sw]


def mock(path):
    path = os.path.normpath(os.path.join(HERE, path)) if not os.path.isabs(path) else path
    key = hashlib.md5((path + str(os.path.getmtime(path)) + str(os.path.getmtime(SRC)) + 'v1').encode()).hexdigest()[:12]
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, f'{os.path.splitext(os.path.basename(path))[0]}_{key}.png')
    if os.path.exists(dst):
        return os.path.relpath(dst, HERE)
    frame, green, body, (x0, y0, x1, y1) = _base()
    scr = np.zeros_like(frame)
    scr[y0:y1, x0:x1] = _screen(path, x1 - x0, y1 - y0)
    g = green[..., None]
    rgb = frame * (1 - g) + scr * g
    out = np.dstack([rgb, body * 255]).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(out, 'RGBA')
    im = im.resize((W_OUT, round(W_OUT / ASPECT)), Image.LANCZOS)
    im.save(dst, optimize=True)
    return os.path.relpath(dst, HERE)


if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]:
        print(mock(p))
