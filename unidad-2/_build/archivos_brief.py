"""Genera los dos archivos del brief U3 como presentaciones independientes, con la
identidad visual del equipo (sin la marca HORIZON), a partir de las láminas de la
presentación principal. Así los tres documentos se mantienen sincronizados.

Salidas (en unidad-2/ev2/):
  EV2_Canvas_Storyboard.html   · portada · Business Model Canvas · storyboards con propuesta de valor
  EV2_Prototipado_Testeo.html  · portada con integrantes · el problema · nuestro prototipo V1, V2 y paciente
Uso: python3 unidad-2/_build/archivos_brief.py && node unidad-2/_build/render_presentacion.js <archivo.html>
"""
import re
from pathlib import Path

EV2 = Path(__file__).resolve().parents[1] / 'ev2'
SRC = (EV2 / 'Evaluacion2_Presentacion.html').read_text(encoding='utf-8')

head = SRC.split('<!-- 01 PORTADA -->', 1)[0]
SECS = {m.group(1): m.group(2) for m in re.finditer(r'<!-- (.*?) -->\n(<section .*?</section>\n)', SRC, flags=re.S)}
GRUPO, SECCION, FECHA = '___', '___', 'Noviembre 2026'
EQUIPO = [('Benjamín Vera Yáñez', 'Secretario técnico · consolida y prototipa'), ('Francisco Ahumada', 'Referentes financieros · factibilidad'),
          ('Claudia Cifuentes', 'Perfil de usuaria · co-creación'), ('Néstor Rivera', 'Ideación · registro y métricas')]
UNIDAD = 'Unidad 3 · Prototipado y testeo'

head = head.replace('</style>', """
</style>""", 1)


def relabel(sec, foot_extra=None):
    for a in ('01 · El problema', '03 · Modelo y storyboard', '04 · Prototipo y testeo'):
        sec = sec.replace(a, UNIDAD)
    sec = sec.replace('02 · Contexto', 'Contexto')
    return sec


def number(html):
    parts = html.split('<section ')
    out = [parts[0]]
    for i, p in enumerate(parts[1:], start=1):
        p = re.sub(r'(<div class="foot"><span>.*?</span><b>)\d+(</b></div>)', lambda x: f'{x.group(1)}{i:02d}{x.group(2)}', p, count=1, flags=re.S)
        out.append(p)
    return '<section '.join(out)


def write(name, title, slides):
    html = head.replace('<title>Evaluación 2 — Presentación Copiloto Kine</title>', f'<title>{title}</title>')
    html = html + ''.join(slides) + '\n</body>\n</html>\n'
    (EV2 / name).write_text(number(html), encoding='utf-8')
    print('listo:', name, html.count('<section '), 'láminas')


# ------------------------------------------------ Archivo 1 · Canvas + storyboard
canvas = relabel(SECS['10 CANVAS'])
canvas = re.sub(r'<div class="foot"><span>Propuesta · Modelo Canvas · .*?</span>',
                f'<div class="foot"><span>Proyecto: Copiloto Kine · Integrantes: F. Ahumada, C. Cifuentes, N. Rivera, B. Vera Yáñez · Sección {SECCION}</span>', canvas, count=1)
canvas = canvas.replace(f'<div class="label">{UNIDAD} · Modelo de negocio</div>',
                        f'<div class="label">Unidad 3 · Modelo de negocio · <span style="color:var(--accent)">+ naranjo</span> = iteración V2</div>')
# Reparto: cada lámina de la presentación general va a uno solo de los dos archivos.
CANVAS_SLIDES = ['09 PROPUESTA DE VALOR', '10 CANVAS', '11 STORYBOARD V1', '14 STORYBOARD V2', 'STORYBOARD PACIENTE']
PROTO_SLIDES = ['PROBLEMA', '03 CASO', '04 UA1', '05 DESAFÍO', '06 REFERENTES', '07 REQUERIMIENTOS', '08 IDEACIÓN',
                '12 MOCKUPS V1', '13 ITERACIÓN', 'PROTO V2', 'MOCKUPS V2 DIA', 'MOCKUPS V2 NUMEROS', 'MOCKUPS V2 PACIENTE',
                'MAPA PANTALLAS', '16 CIERRE']
pick = lambda k: canvas if k == '10 CANVAS' else relabel(SECS[k])
PORTADA = SECS['01 PORTADA']  # misma portada que la presentación principal
write('EV2_Canvas_Storyboard.html', 'Copiloto Kine — Canvas y storyboard', [PORTADA] + [pick(k) for k in CANVAS_SLIDES])

# ------------------------------------------------ Archivo 2 · Prototipado y testeo
cierre_proto = relabel(SECS['16 CIERRE']).replace('<div class="label">Cierre</div>', f'<div class="label">{UNIDAD}</div>')
write('EV2_Prototipado_Testeo.html', 'Copiloto Kine — Prototipado y testeo',
      [PORTADA] + [cierre_proto if k == '16 CIERRE' else relabel(SECS[k]) for k in PROTO_SLIDES])
usadas = set(CANVAS_SLIDES) | set(PROTO_SLIDES) | {'01 PORTADA', '02 ÍNDICE'}
faltan = [k for k in SECS if k not in usadas]
assert not faltan, f'Láminas sin repartir: {faltan}'
