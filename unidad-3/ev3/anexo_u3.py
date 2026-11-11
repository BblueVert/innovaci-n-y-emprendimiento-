# Anexo EV3: plantillas oficiales del toolkit UA3 (INACAP) completadas con el trabajo del equipo.
# Reutiliza las utilidades de texto del anexo de la EV2 (unidad-2/ev2/anexo_toolkit.py).
import os
import sys
import pymupdf as fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'unidad-2', 'ev2'))
import anexo_toolkit as T  # noqa: E402
from anexo_toolkit import box, fonts, INK, MUTE, ORANGE  # noqa: E402
import contenido as C  # noqa: E402

TPL = os.path.join(HERE, '..', 'material', 'plantillas')
T.CURSO = 'Innovación y Emprendimiento III (FGIE03)'


def tpl(name):
    d = fitz.open(os.path.join(TPL, name))
    fonts(d[0])
    return d


def foot(page, y=759):
    T.footer(page, y, x_int=100, x_cur=692, x_prof=924, size=8)


def img_fit(page, rect, path, crop_top=True):
    """Inserta una imagen cubriendo el rectángulo (recorte superior para capturas verticales)."""
    import io
    from PIL import Image
    rect = fitz.Rect(rect)
    im = Image.open(path).convert('RGB')
    w, h = im.size
    rr = rect.width / rect.height
    if w / h > rr:
        cw = int(h * rr); im = im.crop(((w - cw) // 2, 0, (w + cw) // 2, h))
    else:
        ch = int(w / rr); im = im.crop((0, 0, w, ch) if crop_top else (0, (h - ch) // 2, w, (h + ch) // 2))
    im.thumbnail((900, 900))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=85)
    page.insert_image(rect, stream=buf.getvalue())


SC_RECTS = [(40, 243, 404, 409), (428, 243, 792, 409), (815, 243, 1178, 409), (40, 496, 404, 662), (428, 496, 792, 662), (815, 496, 1178, 662)]


def storyboard(scenes, pdv, title_note):
    d = tpl('3.1.2.1_Storyboard_PdV.pdf'); p = d[0]
    box(p, (142, 104, 1170, 220), pdv, size=13, font='serif', lh=1.3)
    box(p, (50, 196, 1170, 222), title_note, size=8, font='mono', color=MUTE)
    for i, (tit, img, kind, txt, prod, pv) in enumerate(scenes):
        x0, y0, x1, y1 = SC_RECTS[i]
        path = os.path.join(HERE, img)
        if kind == 'wide':
            img_fit(p, (x0 + 1, y0 + 1, x0 + 200, y1 - 1), path, crop_top=False)
        else:
            img_fit(p, (x0 + 1, y0 + 1, x0 + 100, y1 - 1), path)
        tx = x0 + (206 if kind == 'wide' else 108)
        p.draw_rect(fitz.Rect(tx - 3, y0 + 8, tx - 1, y0 + 26), color=ORANGE, fill=ORANGE)
        box(p, (tx + 2, y0 + 6, x1 - 8, y0 + 40), f'{i + 1} · {tit}', size=10.5, font='b')
        box(p, (tx + 2, y0 + 42, x1 - 8, y1 - 6), txt, size=9.5, font='r', lh=1.3)
        top = 444 if y0 < 400 else 698
        bx = x0 if i % 3 == 0 else (x0 + 2)
        box(p, (bx + 1, top, bx + 170, top + 44), prod, size=8.5, lh=1.15)
        box(p, (bx + 193, top, bx + 362, top + 44), pv, size=8.5, lh=1.15, color=(0.48, 0.25, 0.63))
    foot(p)
    return d


COLS = [43, 211, 335, 458, 540, 642, 776, 912, 1058, 1116, 1181]
ROWS = [274, 362, 451, 540, 623, 713]


def ficha(F, note):
    d = tpl('3.1.2.3_Ficha_Planificacion_Testeo.pdf'); p = d[0]
    box(p, (50, 124, 1172, 214), F['objetivo'], size=13, font='m', lh=1.3)
    box(p, (50, 214, 1172, 226), note, size=7.5, font='mono', color=MUTE)
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # objetivo, participantes, prototipo, actividades, roles, indicador, pregunta, modelo, lugar, tiempo
    filas = F['filas']
    # en la plantilla: Obj · Participantes · Prototipo · Actividades · Roles · Indicador · Pregunta · Modelo · Lugar · Tiempo
    for r, fila in enumerate(filas[:5]):
        obj, part, proto, act, roles, ind, preg, modelo, lugar, tiempo = fila
        vals = [obj, part, proto, act, roles, ind, preg, modelo, lugar, tiempo]
        y0, y1 = ROWS[r], ROWS[r + 1]
        for c in order:
            box(p, (COLS[c] + 4, y0 + 4, COLS[c + 1] - 4, y1 - 3), vals[c], size=8.5, font='b' if c == 0 else 'r', lh=1.2)
    foot(p)
    return d


def cdm(D, note):
    d = tpl('3.1.2.4_Matriz_CDM_PdV.pdf'); p = d[0]
    cols = [(150, 478), (497, 825), (845, 1172)]
    for row, (y0, y1) in (('prod', (142, 405)), ('pdv', (414, 708))):
        for (x0, x1), k in zip(cols, ('c', 'd', 'm')):
            items = D[f'{row}_{k}']
            box(p, (x0, y0, x1, y1), '\n'.join('• ' + t for t in items), size=10, lh=1.3)
    box(p, (48, 600, 140, 708), note, size=7, font='mono', color=MUTE)
    foot(p)
    return d


PEST_ROWS = [(213, 435), (447, 669), (680, 903), (914, 1137), (1148, 1371), (1382, 1605)]


def pestal():
    d = tpl('3.1.4.1_Matriz_PESTAL_profundizada.pdf'); p = d[0]
    box(p, (90, 100, 1168, 156), C.DESAFIO, size=12, font='m', lh=1.3)
    for (name, o, pr), (y0, y1) in zip(C.PESTAL, PEST_ROWS):
        mid = (y0 + y1) / 2
        for (x0, x1), k in zip(((180, 498), (516, 834), (852, 1170)), ('f', 'o', 'a')):
            box(p, (x0, y0 + 6, x1, mid - 4), o[k], size=11, lh=1.25, color=MUTE)
            box(p, (x0, mid + 6, x1, y1 - 4), pr[k], size=11, lh=1.25, font='m')
    T.footer(p, 1631, x_int=100, x_cur=692, x_prof=924, size=8)
    return d


def build():
    """Devuelve una lista de (título, documento de 1 página)."""
    out = [
        ('3.1.2.1 · Storyboard con propuesta de valor (prototipo v1)', storyboard(C.SCENES, C.PDV_EV2, 'Propuesta de valor EV2 · escenas con capturas del prototipo v1')),
        ('3.1.2.3 · Ficha de planificación del testeo · ciclo 1 (funcional y estético)', ficha(C.FICHA_C1, 'Ciclo 1 · prueba interna del equipo con perfil de usuaria · ' + C.EQUIPO_ROLES)),
        ('3.1.2.4 · Matriz CDM con propuesta de valor · ciclo 1', cdm(C.CDM_C1, 'Ciclo 1 · prototipo v1 · uso y estética')),
        ('3.1.3.2 · Storyboard iterado con propuesta de valor (prototipo v2)', storyboard(C.SCENES_ITER, C.PDV_ITER, 'Propuesta de valor iterada · cualidades (izq.) y mejoras incorporadas (der.) por escena')),
        ('3.1.3.4 · Ficha de planificación del testeo de la iteración · ciclo 2 (técnico)', ficha(C.FICHA_C2, 'Ciclo 2 · verificación técnica del prototipo v2 contra las necesidades de la kinesióloga')),
        ('3.1.2.4 · Matriz CDM con propuesta de valor · ciclo 2', cdm(C.CDM_C2, 'Ciclo 2 · prototipo v2 · técnico')),
        ('3.1.4.1 · Matriz PESTAL profundizada', pestal()),
    ]
    return out


if __name__ == '__main__':
    doc = fitz.open()
    for t, d in build():
        doc.insert_pdf(d)
    doc.save(os.path.join(HERE, '_anexo_prueba.pdf'))
    print('ok', doc.page_count)
