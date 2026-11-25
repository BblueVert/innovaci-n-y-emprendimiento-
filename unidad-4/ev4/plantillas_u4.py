# Plantillas oficiales de la UA4 llenas con el contenido del equipo: 4.1.2.1 Lean Canvas y 4.1.3.2 Guion pitch.
# Uso: python3 plantillas_u4.py  → 4.1.2.1_Lean_Canvas_Copiloto_Kine.pdf/.png y 4.1.3.2_Guion_Pitch_Copiloto_Kine.pdf/.png
import os
import sys
import pymupdf as fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'unidad-2', 'ev2'))
import anexo_toolkit as T  # noqa: E402
from anexo_toolkit import box, fonts, INK, MUTE  # noqa: E402
import contenido_u4 as C  # noqa: E402

TPL = os.path.join(HERE, '..', 'material', 'plantillas')
OUT = os.path.join(HERE, 'entregables')
PURPLE = (0.48, 0.25, 0.63)
ORANGE = (0.76, 0.25, 0.05)
T.CURSO = C.ASIGNATURA
T.EQUIPO = ' · '.join(C.EQUIPO)


def bullets(items):
    return '\n'.join(i if i[:2] in ('1.', '2.', '3.') else '• ' + i for i in items)


def lean_canvas():
    d = fitz.open(os.path.join(TPL, '4.1.2.1_Lean_Canvas.pdf')); p = d[0]; fonts(p)
    X = [52, 537, 1022, 1508, 1993, 2478]
    m = 20
    L = C.LC
    # columna 1 · problema (alto completo)
    s = box(p, (X[0] + m, 262, X[1] - m, 900), bullets(L['problema']), size=25, lh=1.28)
    box(p, (X[0] + m, 915, X[1] - m, 1120), 'Alternativas existentes\n' + L['alternativas'].replace('Hoy: ', ''), size=min(s, 22), color=MUTE, lh=1.25)
    # columna 2 · solución / métricas
    box(p, (X[1] + m, 262, X[2] - m, 635), bullets(L['solucion']), size=25, lh=1.28)
    box(p, (X[1] + m, 752, X[2] - m, 1120), bullets(L['metricas']), size=22, lh=1.25)
    # columna 3 · propuesta de valor (alto completo)
    box(p, (X[2] + m, 352, X[3] - m, 560), L['pdv'], size=40, font='b', color=ORANGE, lh=1.15)
    box(p, (X[2] + m, 575, X[3] - m, 900), L['pdv_detalle'], size=25, font='m', lh=1.3)
    box(p, (X[2] + m, 915, X[3] - m, 1120), L['concepto'], size=23, color=PURPLE, lh=1.25)
    # columna 4 · ventaja especial / canales
    box(p, (X[3] + m, 262, X[4] - m, 635), bullets(L['ventaja']), size=24, lh=1.26)
    box(p, (X[3] + m, 752, X[4] - m, 1120), bullets(L['canales']), size=22, lh=1.25)
    # columna 5 · segmento (alto completo)
    box(p, (X[4] + m, 262, X[5] - m, 1120), bullets(L['segmento']), size=24, lh=1.28)
    # fila inferior · costos / ingresos
    box(p, (X[0] + m, 1278, 1265 - m, 1570), bullets(L['costos']), size=24, lh=1.28)
    box(p, (1265 + m, 1278, X[5] - m, 1570), bullets(L['ingresos']), size=24, lh=1.28)
    # pie: integrantes, curso, profesor
    p.draw_rect(fitz.Rect(30, 1650, 1300, 1685), color=None, fill=(1, 1, 1))  # etiquetas de la plantilla con fuente rota
    for x, lab, t in ((40, 'Integrantes:', T.EQUIPO), (980, 'Curso:', 'Innovación y Emprendimiento III'), (1440, 'Profesor:', C.PROFESOR)):
        p.insert_text((x, 1673), lab, fontname='fb', fontsize=15, color=INK)
        p.insert_text((x + (125 if lab == 'Integrantes:' else 70 if lab == 'Curso:' else 92), 1673), T.clean(t), fontname='fr', fontsize=15, color=INK)
    return d


def guion():
    d = fitz.open(os.path.join(TPL, '4.1.3.2_Guion_Pitch.pdf')); p = d[0]; fonts(p)
    box(p, (48, 112, 1180, 136), C.PITCH_FRASE, size=12, font='b', color=ORANGE)
    tops = [(151, 275), (287, 412), (424, 548), (560, 685)]
    for (t, txt), (y0, y1) in zip(C.PITCH, tops):
        box(p, (50, y0 + 22, 1166, y1 - 6), txt, size=12, lh=1.4)
    T.footer(p, 754, x_int=100, x_cur=694, x_prof=928, size=8)
    return d


def save(d, name):
    os.makedirs(OUT, exist_ok=True)
    d.save(os.path.join(OUT, name + '.pdf'), garbage=3, deflate=True)
    d[0].get_pixmap(dpi=110 if d[0].rect.width < 1500 else 60).save(os.path.join(OUT, name + '.png'))


if __name__ == '__main__':
    save(lean_canvas(), '4.1.2.1_Lean_Canvas_Copiloto_Kine')
    save(guion(), '4.1.3.2_Guion_Pitch_Copiloto_Kine')
    print('ok')
