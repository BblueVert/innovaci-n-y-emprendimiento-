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
/* Portadas de los archivos del brief */
.cv-sky{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cv-datos{display:grid;grid-template-columns:auto 1fr;gap:10px 18px;font-size:15px;color:#E9E6F7}
.cv-datos b{font-family:var(--fm);font-weight:500;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:#FFB347;padding-top:3px}
.int-card{position:absolute;right:64px;top:64px;width:430px;background:rgba(26,24,40,.92);border:1px solid #302D45;border-radius:16px;padding:20px 22px;backdrop-filter:blur(4px)}
.int-card h3{font-weight:700;font-size:17px;margin-bottom:12px;display:flex;align-items:center;gap:10px}
.int-card h3 i{width:30px;height:30px;border-radius:50%;background:var(--accent);display:grid;place-items:center;font-style:normal;font-size:14px}
.int-card .m{background:#13111F;border:1px solid #252235;border-radius:10px;padding:10px 14px;margin-bottom:9px}
.int-card .m b{display:block;font-size:15px}
.int-card .m span{font-size:12.5px;color:#9B98B8}
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
portada_canvas = f"""<section class="slide dark" style="background:#07060E">
  <img class="cv-sky" src="img/15-horizonte.jpg" alt="">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,6,14,.15) 0%,rgba(7,6,14,.05) 45%,rgba(7,6,14,.75) 75%,rgba(7,6,14,.95) 100%)"></div>
  <div class="abar"></div>
  <div class="row" style="position:relative;align-items:flex-start">
    <div class="label" style="color:#fff">{UNIDAD}</div>
    <div class="label" style="text-align:right;color:#fff">Innovación y Emprendimiento III · FGIE03<br>INACAP Rancagua</div>
  </div>
  <div style="position:absolute;left:72px;top:150px;width:760px">
    <div class="label" style="color:#fff;margin-bottom:10px">Testeo de la propuesta de solución</div>
    <div class="disp" style="font-size:104px;color:#fff;text-shadow:0 4px 30px rgba(7,6,14,.35)">Copiloto Kine</div>
    <div class="disp" style="font-size:36px;color:#fff;margin-top:4px">Business Model Canvas y storyboard con propuesta de valor</div>
  </div>
  <div style="position:absolute;left:72px;right:64px;bottom:46px;display:flex;justify-content:space-between;align-items:flex-end">
    <div class="cv-datos">
      <b>Empresa</b><span>Copiloto Kine · caso Joselyn Toledo, kinesióloga (Centro Médico InMotion)</span>
      <b>Integrantes</b><span>Francisco Ahumada · Claudia Cifuentes · Néstor Rivera · Benjamín Vera Yáñez</span>
      <b>Asignatura</b><span>Innovación y Emprendimiento III (FGIE03)</span>
      <b>Docente</b><span>Roberto Escobar Donoso</span>
    </div>
    <div class="label" style="text-align:right;white-space:nowrap">Sección {SECCION}<br>Rancagua · {FECHA}</div>
  </div>
</section>
"""
canvas = relabel(SECS['10 CANVAS'])
canvas = re.sub(r'<div class="foot"><span>Propuesta · Modelo Canvas · .*?</span>',
                f'<div class="foot"><span>Proyecto: Copiloto Kine · Integrantes: F. Ahumada, C. Cifuentes, N. Rivera, B. Vera Yáñez · Sección {SECCION}</span>', canvas, count=1)
canvas = canvas.replace(f'<div class="label">{UNIDAD} · Modelo de negocio</div>',
                        f'<div class="label">Unidad 3 · Modelo de negocio · <span style="color:var(--accent)">+ naranjo</span> = iteración V2</div>')
cierre_canvas = f"""<section class="slide dark">
  <div class="abar"></div>
  <div class="label">{UNIDAD}</div>
  <h1 style="color:var(--text)">Propuesta de valor</h1>
  <div style="height:3px;width:120px;background:linear-gradient(90deg,var(--accent),var(--h4),transparent);margin:12px 0 26px"></div>
  <div class="dcard" style="border-color:rgba(255,107,53,.45);padding:26px 30px">
    <div style="font-size:26px;line-height:1.42">Copiloto Kine es el copiloto financiero de la kinesióloga independiente: <span class="acc">se conecta a la agenda que ya usa</span> y convierte cada atención en ganancia real (descontando traslado, materiales, comisión e impuestos) para que <span style="color:var(--h3)">sepa cuánto gana, anticipe los meses bajos y deje de cuadrar Excel de noche</span>.</div>
  </div>
  <div class="grid g4" style="margin-top:22px">
    <div class="dcard"><b class="acc">Anticipador</b><div style="color:var(--text2);font-size:14px;margin-top:4px">Avisa antes de la curva.</div></div>
    <div class="dcard"><b class="acc">Automático</b><div style="color:var(--text2);font-size:14px;margin-top:4px">La usuaria solo confirma.</div></div>
    <div class="dcard"><b class="acc">Legible de un vistazo</b><div style="color:var(--text2);font-size:14px;margin-top:4px">Semáforo y palabras simples.</div></div>
    <div class="dcard"><b class="acc">Sostenible</b><div style="color:var(--text2);font-size:14px;margin-top:4px">Menos km, cero cierres nocturnos.</div></div>
  </div>
  <div class="foot"><span>Copiloto Kine · Innovación y Emprendimiento III · INACAP Rancagua · 2026</span><b>00</b></div>
</section>
"""
# Reparto: cada lámina de la presentación general va a uno solo de los dos archivos.
CANVAS_SLIDES = ['09 PROPUESTA DE VALOR', '10 CANVAS', '11 STORYBOARD V1', '14 STORYBOARD V2', 'STORYBOARD PACIENTE']
PROTO_SLIDES = ['PROBLEMA', '03 CASO', '04 UA1', '05 DESAFÍO', '06 REFERENTES', '07 REQUERIMIENTOS', '08 IDEACIÓN',
                '12 MOCKUPS V1', '13 ITERACIÓN', 'PROTO V2', 'MOCKUPS V2 DIA', 'MOCKUPS V2 NUMEROS', 'MOCKUPS V2 PACIENTE',
                'MAPA PANTALLAS', '16 CIERRE']
pick = lambda k: canvas if k == '10 CANVAS' else relabel(SECS[k])
write('EV2_Canvas_Storyboard.html', 'Copiloto Kine — Canvas y storyboard', [portada_canvas] + [pick(k) for k in CANVAS_SLIDES])

# ------------------------------------------------ Archivo 2 · Prototipado y testeo
miembros = ''.join(f'<div class="m"><b>{i}. {n}</b><span>Diseño Digital · {r}</span></div>' for i, (n, r) in enumerate(EQUIPO, start=1))
portada_proto = f"""<section class="slide dark">
  <div class="abar"></div>
  <div style="position:absolute;left:72px;top:60px;width:620px">
    <div class="label acc">{UNIDAD}</div>
    <div class="label" style="margin-top:6px">Innovación y Emprendimiento III · INACAP Rancagua</div>
  </div>
  <div style="position:absolute;left:72px;top:190px;width:620px">
    <div class="disp" style="font-size:104px">Copiloto Kine</div>
    <div style="height:3px;width:200px;background:linear-gradient(90deg,var(--accent),var(--h4),transparent);margin:20px 0"></div>
    <div class="serif" style="font-size:24px;line-height:1.3;color:#E9E6F7">El copiloto financiero de la kinesióloga independiente: convierte cada atención en ganancia real y le avisa qué viene, sin que tenga que digitar.</div>
  </div>
  <div style="position:absolute;left:72px;bottom:46px" class="label">Grupo N° {GRUPO} · Sección {SECCION} · {FECHA}</div>
  <div class="int-card"><h3><i>👥</i>Integrantes del grupo</h3>{miembros}<div class="xs" style="color:#9B98B8;margin-top:4px">Docente: Roberto Escobar Donoso</div></div>
</section>
"""
cierre_proto = relabel(SECS['16 CIERRE']).replace('<div class="label">Cierre</div>', f'<div class="label">{UNIDAD}</div>')
write('EV2_Prototipado_Testeo.html', 'Copiloto Kine — Prototipado y testeo',
      [portada_proto] + [cierre_proto if k == '16 CIERRE' else relabel(SECS[k]) for k in PROTO_SLIDES])
usadas = set(CANVAS_SLIDES) | set(PROTO_SLIDES) | {'01 PORTADA', '02 ÍNDICE'}
faltan = [k for k in SECS if k not in usadas]
assert not faltan, f'Láminas sin repartir: {faltan}'
