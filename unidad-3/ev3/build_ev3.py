# Informe EV3 (A4 vertical, lenguaje visual de la EV1 y EV2) — Innovación y Emprendimiento III, Unidad 3 Prototipado y testeo.
# Uso:  python3 build_ev3.py   →  Evaluacion3_Informe_Prototipado.html / .pdf
# Contenido: contenido.py (ciclos 1 y 2 desde ../ciclo1 y ../ciclo2), kit de testeo (../testeo/build_kit.py) y plantillas oficiales (anexo_u3.py).
import os
import sys

import pymupdf as fitz
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contenido as C  # noqa: E402
import anexo_u3  # noqa: E402
sys.path.insert(0, os.path.join(HERE, '..', 'testeo'))
import build_kit as K  # noqa: E402

VEC = 'img/vec/'
V1, V2, PAC = '../prototipo/capturas_v1/', '../prototipo/capturas_v2/', '../prototipo/capturas_paciente/'
PEND = '<span class="pend">Pendiente de sesión</span>'
ANEXO_PAGE = '—'


# ---------------------------------------------------------------- utilidades
def sus(*tags):
    return ''.join(f'<span class="sus {t.lower()}">{t}</span>' for t in tags)


def table(headers, rows, cls=''):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


STMT = {
    's-intro': 'Prototipar es <b>hacer tangible la promesa</b> para poder probarla.',
    's-ruta': 'Dos ciclos con focos distintos: <b>primero usarla, después confiar en ella</b>.',
    's-sqa': 'Sabíamos prototipar; teníamos que <b>aprender a medir</b>.',
    's-sb1': 'Un día de Joselyn, <b>de las 11:40 p. m. al domingo</b>.',
    's-mk1': 'Un enlace en el celular: <b>nada que instalar</b>.',
    's-f1': 'El ciclo 1 pregunta: <b>¿se puede usar y se ve bien?</b>',
    's-r1': 'Funciona en lo central y <b>falla en lo que permite corregir</b>.',
    's-cdm1': 'Todo problema de severidad 2 o más <b>entra a la iteración</b>.',
    's-iter': 'Primero <b>visual y funcional</b>; después <b>técnica</b>.',
    's-fun': 'Menos digitación, <b>más datos reales</b>.',
    's-tec': 'Lo que falta no es diseño: <b>es conectar datos reales</b>.',
    's-pac': 'Cada escena del paciente <b>es una hipótesis</b>.',
    's-meta': 'La metáfora pasa <b>del tablero al copiloto</b>.',
    's-sb2': 'El mismo día, <b>con lo que aprendimos</b>.',
    's-mk2': 'Doce cambios, <b>cada uno con su hallazgo</b>.',
    's-f2': 'El ciclo 2 pregunta: <b>¿resuelve con exactitud lo que ella necesita?</b>',
    's-r2': 'Exacto, rápido y <b>sin datos clínicos</b>.',
    's-cdm2': 'Las brechas no son fallas: <b>son el backlog del MVP</b>.',
    's-val': 'Quien usa la app y <b>quien vive sus efectos</b>.',
    's-vp': 'Lo que recibe el paciente <b>cuando su kine usa Copiloto Kine</b>.',
    's-cov': 'Ocho de trece cumplen; <b>lo demás es integración</b>.',
    's-pv': 'De copiloto financiero a <b>copiloto de su día</b>.',
    's-pestal': 'El contexto de la UA1, <b>ahora con evidencia</b>.',
    's-arte': 'Nadie cruza agenda, costos por atención <b>e impuestos chilenos</b>.',
    's-pert': 'Pertinente en lo que demuestra; <b>abierta en lo que falta validar</b>.',
    's-sost': 'Sostenible es que la práctica <b>pueda durar</b>.',
    's-gest': 'Cuatro semanas, <b>cuatro roles, una bitácora</b>.',
    's-concl': 'Probar con evidencia, iterar con criterio y <b>llevarlo a las personas</b>.',
}


def section(sid, label, kicker, title, body, code=None):
    c = f'<span class="code">{code}</span>' if code else ''
    st = f'<div class="stmt">{STMT[sid]}</div>' if sid in STMT else ''
    return (f'<div class="section" id="{sid}"><div class="section-head" data-sec="{label}"><div class="kicker">{kicker}</div>'
            f'<h2>{c}{title}</h2></div>{st}{body}</div>')


def card(cols):
    return '<div class="inst-card">' + ''.join(f'<div class="col"><div class="lbl">{l}</div>{v}</div>' for l, v in cols) + '</div>'


def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def phones(items):
    return '<div class="phones">' + ''.join(f'<figure><img src="{s}"><figcaption>{t}</figcaption></figure>' for s, t in items) + '</div>'


def scenes(sc, it=False):
    out = ''
    for i, (t, img, kind, txt, a, b) in enumerate(sc, 1):
        ca, cb = (('ok', 'Cualidad (testeo)'), ('mj', 'Mejora incorporada')) if it else (('p', 'Componente del producto'), ('v', 'Componente de la propuesta de valor'))
        out += (f'<div class="sc2"><div class="im"><img src="{img}"><span class="n">{i:02d}</span></div><div class="tx"><div class="h">{t}</div><div>{txt}</div>'
                f'<div class="c {ca[0]}"><b>{ca[1]}</b>{a}</div><div class="c {cb[0]}"><b>{cb[1]}</b>{b}</div></div></div>')
    return f'<div class="sb2">{out}</div>'


def cdm(D):
    def cell(k, cls):
        return f'<td class="{cls}">{ul(D[k])}</td>'
    return ('<table class="cdm"><thead><tr><th style="width:20mm"></th><th>Cualidades</th><th>Debilidades</th><th>Mejoras</th></tr></thead><tbody>'
            f'<tr><td class="rh">Producto / servicio</td>{cell("prod_c", "c")}{cell("prod_d", "d")}{cell("prod_m", "m")}</tr>'
            f'<tr><td class="rh">Propuesta de valor</td>{cell("pdv_c", "c")}{cell("pdv_d", "d")}{cell("pdv_m", "m")}</tr></tbody></table>')


def kpis(items):
    return '<div class="kpi2">' + ''.join(f'<div><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in items) + '</div>'


def ficha_tbl(F):
    rows = [[f'<b>{r[0]}</b>', r[1], r[2], r[3], r[4], r[5], r[6], r[7], f'{r[8]}<br>{r[9]}'] for r in F['filas']]
    return table(['Objetivo específico', 'Participantes', 'Prototipo', 'Actividades', 'Roles', 'Indicador', 'Pregunta', 'Procesamiento', 'Lugar · tiempo'], rows, 'tight ficha')


def fix(o):
    o = o.replace(': true', ': sí').replace(': false', ': no').replace(' | ', ' · ')
    return (o[:78] + '…') if len(o) > 78 else o


# ---------------------------------------------------------------- páginas
def portada():
    chips = ''.join(f'<span class="chip">{c}</span>' for c in [
        '3.1.1.1 SQA', '3.1.2.1 Storyboard', '3.1.2.2 Mock-up', '3.1.2.3 Ficha de testeo', '3.1.2.4 Matriz CDM', '3.1.3.1 Metáforas iteradas',
        '3.1.3.2 Storyboard iterado', '3.1.3.3 Mock-up iterado', '3.1.3.4 Testeo de la iteración', '3.1.4.1 PESTAL profundizada'])
    return f'''<div class="cover"><div class="bar"></div>
<img class="hero" src="img/01-portada.jpg">
<div><div class="inst" style="color:var(--accent)">Innovación y Emprendimiento III · INACAP Rancagua</div></div>
<div><h1>EVALUACIÓN<br>N°3</h1>
<div class="sub">PROTOTIPADO Y TESTEO</div><div class="inst" style="margin-top:2mm">Informe sumativo grupal · Unidad de Aprendizaje N°3 · FGIE03</div><div class="div"></div>
<div class="desc">Fase de desarrollo, prototipado y testeo del Ciclo de Innovación INACAP aplicada al caso de Joselyn Toledo, kinesióloga independiente
con atención mixta. Del storyboard al prototipo navegable Copiloto Kine, dos ciclos de testeo, la iteración de la propuesta de valor y su
verificación frente al estado del arte, con trazabilidad a los criterios 3.1.1 a 3.1.5.</div>
<div class="grid">{chips}</div></div>
<div class="meta"><div class="team"><div>Francisco Ahumada · Claudia Cifuentes</div><div>Néstor Rivera · Benjamín Vera Yáñez</div>
<div class="inst" style="margin-top:1mm">Diseño Digital · INACAP Rancagua</div><div class="inst" style="margin-top:1mm">Profesor: Roberto Escobar Donoso</div></div>
<div style="text-align:right"><div class="inst">Rancagua, Chile</div><div class="inst">Noviembre 2026</div></div></div></div>'''


def indice():
    items = [('Marco', [('01', 's-intro', 'Introducción, caso y propuesta de valor de partida'), ('02', 's-ruta', 'Ruta metodológica y trazabilidad de criterios'), ('3.1.1.1', 's-sqa', 'Evaluación diagnóstica: tabla SQA')]),
             ('Prototipado · versión 1', [('3.1.2.1', 's-sb1', 'Storyboard con propuesta de valor'), ('3.1.2.2', 's-mk1', 'Mock-up con propuesta de valor')]),
             ('Testeo · ciclo 1 funcional y estético', [('3.1.2.3', 's-f1', 'Ficha de planificación del testeo'), ('Ciclo 1', 's-r1', 'Resultados: tareas, accesibilidad y heurísticas'), ('3.1.2.4', 's-cdm1', 'Matriz CDM con propuesta de valor')]),
             ('Iteración · versión 2', [('Iteración', 's-iter', 'De la versión actual a la actualizada'), ('3.1.3.1', 's-meta', 'Panel de metáforas y atributos iterado'), ('3.1.3.2', 's-sb2', 'Storyboard iterado'), ('3.1.3.3', 's-mk2', 'Mock-up iterado y ajustes fundamentados')]),
             ('Testeo · ciclo 2 técnico', [('3.1.3.4', 's-f2', 'Ficha de planificación del testeo de la iteración'), ('Ciclo 2', 's-r2', 'Resultados técnicos y cobertura de requerimientos'), ('3.1.2.4', 's-cdm2', 'Brechas y matriz CDM del ciclo 2'), ('Técnica', 's-tec', 'Propuesta técnica v3: integraciones y funcionalidades')]),
             ('Validación y propuesta de valor', [('Usuarios', 's-val', 'Validación con usuarios externos: kit de testeo'), ('Paciente', 's-pac', 'Storyboard del paciente'), ('Paciente', 's-vp', 'Vista paciente'), ('3.1.5', 's-pv', 'Propuesta de valor iterada')]),
             ('Estado del arte y pertinencia', [('3.1.4.1', 's-pestal', 'Matriz PESTAL profundizada'), ('3.1.4', 's-arte', 'Estado del arte y tendencias'), ('3.1.5', 's-pert', 'Pertinencia de la propuesta de valor')]),
             ('Cierre', [('Sost.', 's-sost', 'Enfoque sostenible'), ('Gestión', 's-gest', 'Gestión de la fase y bitácora'), ('Cierre', 's-concl', 'Conclusiones y próximos pasos'), ('Ref.', 's-ref', 'Referencias')])]
    out = ''
    for g, li in items:
        out += f'<div class="grp">{g}</div><ul>' + ''.join(f'<li><span class="c">{c}</span><span class="t"><a href="#{h}">{t}</a></span></li>' for c, h, t in li) + '</ul>'
    out += ('<div class="grp">Anexo</div><ul>'
            f'<li><span class="c">Anexo A</span><span class="t">Plantillas oficiales del toolkit UA3 completas (7 instrumentos)</span><span style="font-family:var(--fm);font-size:8pt">{ANEXO_PAGE}</span></li></ul>')
    return section('s-indice', 'ÍNDICE', 'Contenido', 'Índice', f'<div class="toc">{out}</div>')


def intro():
    b = f'''<p class="lead">La Unidad 3 corresponde a la fase de <strong>desarrollo, prototipado y testeo</strong> del Ciclo de Innovación INACAP. Su aprendizaje esperado
es elaborar el prototipo de la propuesta de valor, testearlo con usuarios en más de un ciclo, ajustarlo según los resultados y verificar su pertinencia frente al estado del arte y las tendencias.</p>
<h3>Caso y punto de partida</h3>
<div class="case"><img src="img/02-caso.jpg"><div class="facts">
<div><b>Usuaria</b>Joselyn Toledo — kinesióloga independiente: Centro Médico InMotion (70/30) y domicilios en Rancagua y Machalí.</div>
<div><b>Problema (UA1)</b>No sabe cuánto gana de verdad; cuadra ingresos y gastos en Excel de noche (~1 h diaria).</div>
<div><b>Solución (UA2)</b>Copiloto Kine: convierte cada atención en ganancia real y anticipa los meses bajos.</div></div></div>
<h3>Desafío</h3><div class="big-q">{C.DESAFIO}</div>
<h3>Propuesta de valor que llegamos a probar (EV2)</h3><p>{C.PDV_EV2}</p>
<div class="note"><b>Nota de transparencia.</b> Los ciclos 1 y 2 los ejecutó el equipo como usuarios internos —alternativa que el toolkit permite— con scripts
reproducibles y resultados guardados en el repositorio (<code>unidad-3/ciclo1</code> y <code>ciclo2</code>). La validación con usuarias, pacientes y una contadora queda preparada
en un kit de testeo y sus resultados se informan como pendientes: no atribuimos opiniones a personas que aún no han participado.</div>'''
    return section('s-intro', '01 · INTRODUCCIÓN', 'Marco', 'Introducción', b)


def ruta():
    cyc = [('S11 · Prototipar', 'SQA, storyboard y mock-up v1'), ('S11–S12 · Ciclo 1', 'Uso y estética: 11 tareas, WCAG AA, heurísticas'), ('S12 · CDM 1', 'Cualidades, debilidades y mejoras'),
           ('S12–S13 · Iterar', 'Metáfora, storyboard y mock-up v2'), ('S13 · Ciclo 2', 'Técnico: 11 pruebas y cobertura R1–R13'), ('S13–S14 · Usuarios', 'Kit para kinesiólogas, pacientes y contadora')]
    ch = '<span class="ar">›</span>'.join(f'<div><b>{t}</b>{d}</div>' for t, d in cyc)
    cr = [('3.1.1', '15', 'Aplica la fase de desarrollo y prototipado del Ciclo de Innovación INACAP', '3.1.1.1 · 3.1.2.1 · 3.1.2.2'),
          ('3.1.2', '20', 'Elabora un prototipo funcional y lo valida con usuarios en más de un ciclo, con enfoque sostenible', 'Ciclos 1 y 2 · kit de testeo · sostenibilidad'),
          ('3.1.3', '15', 'Ajusta el prototipo a partir de los resultados del testeo, fundamentando los cambios', '3.1.2.4 · 3.1.3.1–3.1.3.4'),
          ('3.1.4', '20', 'Analiza el estado del arte y las tendencias en relación con el desafío', '3.1.4.1 · estado del arte · tendencias'),
          ('3.1.5', '30', 'Pertinencia de la propuesta de valor', 'Propuesta iterada · pertinencia')]
    b = f'''<div class="side"><img src="img/03-ciclo.jpg" style="width:62mm;height:34.6mm"><div><p class="lead">El trabajo siguió el calendario S11–S14 del manual. Cada ciclo de testeo tuvo un foco distinto, para no mezclar problemas de uso con problemas de exactitud: primero que se pueda usar y se vea bien; después, que calcule exacto y resuelva las necesidades puntuales de la kinesióloga.</p></div></div>
<div class="cycle">{ch}</div>
<div class="grid2"><div class="box"><div class="t">Ciclo 1 · funcional y estético</div>¿Puede una kinesióloga hacer su día sin ayuda? ¿Se lee, se toca y se entiende? Tareas, auditoría WCAG 2.1 AA, objetivos táctiles, tipografía y heurísticas de Nielsen.</div>
<div class="box"><div class="t">Ciclo 2 · técnico</div>¿Resuelve con exactitud sus necesidades puntuales? Cálculos, cierre del día, persistencia, costos editables, exportación sin datos clínicos, rendimiento y brechas.</div></div>
<h3>Trazabilidad con la rúbrica ES03</h3>
{table(['Criterio', 'Pts.', 'Indicador', 'Dónde se evidencia'], [[f'<b>{a}</b>', b_, c, f'<span class="small muted">{d}</span>'] for a, b_, c, d in cr], 'tight')}'''
    return section('s-ruta', '02 · RUTA', 'Marco', 'Ruta metodológica', b)


def sqa():
    cols = ''.join(f'<div class="box"><div class="t">{t}</div>{ul(items)}</div>' for t, items in C.SQA)
    b = f'''{card([('Instrumento', '3.1.1.1 Tabla SQA'), ('Momento', 'Evaluación diagnóstica · S11'), ('Participantes', 'Los cuatro integrantes'), ('Uso', 'Orientar la planificación del testeo')])}
<div class="grid3">{cols}</div>
<h3>Lectura</h3><p>La tabla mostró que el equipo dominaba la representación visual —es su disciplina—, pero no sabía cómo testear una herramienta financiera
sin datos reales ni con qué indicadores. Esa brecha orientó todo lo que sigue: medir tareas, accesibilidad y exactitud en vez de preguntar solo si el prototipo “gusta”.</p>
<img class="banner" src="img/04-card-sorting.jpg" style="height:36mm">'''
    return section('s-sqa', '3.1.1.1 · SQA', 'Evaluación diagnóstica', 'Tabla SQA', b, '3.1.1.1')


def sb1():
    b = card([('Instrumento', '3.1.2.1 Storyboard con propuesta de valor'), ('Insumo', 'Propuesta de valor y atributos EV2'), ('Formato', 'Escenas con capturas del prototipo v1'), ('Plantilla', 'Anexo A')])
    b += f'<div class="big-q" style="font-size:10.5pt">{C.PDV_EV2}</div>' + scenes(C.SCENES)
    return section('s-sb1', '3.1.2.1 · STORYBOARD', 'Prototipado · versión 1', 'Storyboard con propuesta de valor', b, '3.1.2.1')


def mk1():
    b = f'''<p class="lead">El mock-up se construyó como prototipo navegable en HTML para celular (390 px): se abre desde un enlace, sin instalar nada. Paleta clara del
proyecto con acentos naranjos; la clínica se identifica en morado y el domicilio en naranjo.</p>
{phones([(m[1], m[0]) for m in C.MOCK_V1]).replace('class="phones"', 'class="phones s6"')}
{table(['Pantalla', 'Qué materializa', 'Atributo de la propuesta de valor'], [[f'<b>{m[0]}</b>', m[2], m[3]] for m in C.MOCK_V1], 'tight')}
<p class="small muted">Archivo: <code>unidad-3/prototipo/copiloto-kine-v1.html</code>. Las pantallas usan datos de ejemplo de un día tipo de Joselyn (2 atenciones en clínica y 3 a domicilio).</p>'''
    return section('s-mk1', '3.1.2.2 · MOCK-UP', 'Prototipado · versión 1', 'Mock-up con propuesta de valor', b, '3.1.2.2')


def pagina_cita():
    return '''<div class="full orange"><img src="img/06-nudo.jpg">
<div class="in" style="top:24mm"><div class="kick">La voz de las usuarias · lo que el prototipo debe resolver</div>
<div class="q">“Para poder organizar el Excel sobre los ingresos y egresos que estoy teniendo me toma una hora actualmente diario.”</div>
<div class="src">— Catalina, kinesióloga · entrevista a experta UA1</div>
<div class="q2">La meta del desafío: menos de 30 minutos. El prototipo v2 cierra un día de cinco atenciones en 11 toques.</div></div>
<div class="foot"><span>Testeo del prototipo</span><span>Ciclos 1 y 2</span></div></div>'''


def f1():
    b = card([('Instrumento', '3.1.2.3 Ficha de planificación del testeo'), ('Foco', 'Funcional y estético'), ('Prototipo', 'v1 en celular (390 px)'), ('Plantilla', 'Anexo A')])
    b += f'<div class="side"><img src="{VEC}16-testeo.png" style="width:58mm;height:32.4mm"><div class="big-q" style="font-size:10.5pt;margin:0">{C.FICHA_C1["objetivo"]}</div></div>' + ficha_tbl(C.FICHA_C1)
    b += f'<p class="small"><b>Roles.</b> {C.EQUIPO_ROLES}.</p>'
    b += ('<h3>Herramientas de medición</h3>' + ul([
        '<b>Recorrido de 11 tareas</b> automatizado con Playwright: éxito y número de toques por tarea (<code>ciclo1/evaluar_prototipo.js</code>).',
        '<b>Auditoría WCAG 2.1 A/AA</b> con axe-core 4.10 en las cinco vistas.', '<b>Objetivos táctiles</b> menores a 44 px y <b>tamaños de letra</b> visibles por vista.',
        '<b>Revisión heurística</b> (10 heurísticas de Nielsen) con severidad 0–4, consensuada por el equipo.']))
    return section('s-f1', '3.1.2.3 · FICHA CICLO 1', 'Testeo · ciclo 1', 'Ficha de planificación del testeo', b, '3.1.2.3')


def r1():
    t = C.C1['tasks']; ok = sum(x['ok'] for x in t)
    axe = sum(x['n'] for v in C.C1['axe'].values() for x in v); tg = sum(len(v) for v in C.C1['targets'].values())
    rows = [[f'<b>{x["id"]}</b>', x['name'], f'<span class="{"ok" if x["ok"] else "ko"}">{"✔" if x["ok"] else "✖"}</span>', x['taps'] if x['ok'] else '—', f'<span class="small">{fix(x["obs"])}</span>'] for x in t]
    hr = [[h, d, f'<span class="sev s{s}">{s}</span>'] for h, d, s in C.HEUR]
    b = (kpis([(f'{ok}/{len(t)}', 'tareas completadas sin ayuda (meta ≥ 90 %)'), (axe, 'errores de contraste WCAG AA'), (tg, 'botones o enlaces bajo 44 px'), ('10–11', 'px: letra mínima en etiquetas')])
         + table(['#', 'Tarea', 'Éxito', 'Toques', 'Evidencia'], rows, 'tight xs')
         + '<h3>Revisión heurística</h3>' + table(['Heurística', 'Hallazgo', 'Sev.'], hr, 'tight xs')
         + '<p class="small"><b>Lectura.</b> Lo central funciona: la ganancia del mes se lee sin tocar nada y una atención se registra en dos toques. Las cuatro tareas fallidas comparten causa: '
           'no hay forma de corregir (deshacer, inasistencia, costos, exportación). En lo estético, el tablero compacto funciona; el naranjo del proyecto no alcanza contraste con texto blanco (2,84:1).</p>')
    return section('s-r1', 'CICLO 1 · RESULTADOS', 'Testeo · ciclo 1', 'Resultados del ciclo 1', b)


def cdm1():
    b = card([('Instrumento', '3.1.2.4 Matriz CDM con propuesta de valor'), ('Fuente', 'Tareas, auditoría y heurísticas del ciclo 1'), ('Regla', 'Severidad ≥ 2 → iteración'), ('Plantilla', 'Anexo A')])
    b += cdm(C.CDM_C1)
    b += '<h3>Análisis y conclusiones</h3><p>La promesa “automático” se rompe ante el primer error: sin deshacer ni inasistencia, una equivocación se convierte en un ingreso falso. En la propuesta de valor, “ganancia real” —su centro— no está definida en pantalla. Y la ruta del día, que no era el foco, resultó lo más “copiloto” de la app: esa observación cambia la metáfora en la iteración.</p>'
    return section('s-cdm1', '3.1.2.4 · CDM CICLO 1', 'Testeo · ciclo 1', 'Matriz CDM del ciclo 1', b, '3.1.2.4')


def pagina_cifras():
    return f'''<div class="full dark"><div class="in" style="top:40mm"><div class="kick" style="color:#FF6B35">De la prueba a la iteración</div>
<div class="big">7 DE 11 <em>→ 11 DE 11</em>.</div>
<div class="lead2">Los hallazgos del ciclo 1 se convirtieron en doce cambios concretos. La versión 2 completa todas las tareas, sin errores de accesibilidad.</div>
<div class="ncards"><div><div class="n">12</div><div class="t">Cambios en v2</div><div class="d">Cada uno trazado a un hallazgo medido y a un requerimiento de la EV2.</div></div>
<div><div class="n">11 → 0</div><div class="t">Errores de contraste</div><div class="d">Naranjo accesible #C2410C (5,2:1) en botones y verde oscuro en estados.</div></div>
<div><div class="n">12 px</div><div class="t">Letra mínima</div><div class="d">Y todos los botones de 44 px o más: se usa con una mano, entre domicilios.</div></div></div></div>
<div class="foot"><span>Iteración del prototipo</span><span>3.1.3.1 – 3.1.3.3</span></div></div>'''


def iter_docs():
    rows = [[f'<span class="code">{c}</span><br><b>{n}</b>', f'<span class="vv a">Versión actual</span><br>{a}', f'<span class="vv b">Versión actualizada</span><br>{b_}', f'<span class="small muted">{h}</span>'] for c, n, a, b_, h in C.ITER_DOCS]
    b = (f'<div class="side"><img src="{VEC}18-iteracion.png" style="width:56mm;height:31.3mm;object-fit:contain;background:#F4F2FC"><p class="lead" style="margin:0">Los instrumentos del toolkit no se llenan una sola vez: cada uno se presenta en su <b>versión actual</b> —más visual y funcional, la que llevamos al ciclo 1— y en su <b>versión actualizada</b> según los hallazgos clave del testeo, más técnica y enfocada en resolver las necesidades puntuales de la kinesióloga.</p></div>'
         + table(['Instrumento', 'Versión actual · visual y funcional', 'Versión actualizada · técnica', 'Hallazgo que la motiva'], rows, 'tight')
         + '<p class="small">Las páginas siguientes muestran cada par. Las plantillas oficiales de ambas versiones están en el Anexo A.</p>')
    return section('s-iter', 'ITERACIÓN DE INSTRUMENTOS', 'Iteración · versión 2', 'De la versión actual a la actualizada', b)


def tecnico():
    izq = ''.join(f'<div class="nd"><b>{n}</b>{f}</div>' for n, _, f, _, _ in C.INTEGRACIONES[:3])
    der = ''.join(f'<div class="nd p"><b>{n}</b>{f}</div>' for n, _, f, _, _ in C.INTEGRACIONES[3:])
    arq = f'<div class="arq"><div class="col">{izq}</div><div class="core"><div class="t">COPILOTO KINE · V3</div><div class="d">App web instalable (PWA) · cálculo de ganancia real · ruta · proyección · sin datos clínicos</div></div><div class="col">{der}</div></div>'
    integ = [[f'<b>{n}</b>', fu, f'<span class="small">{u}</span>', sus(*[x.strip() for x in d.split('·')]), et] for n, fu, u, d, et in C.INTEGRACIONES]
    fn = [[f'<span class="fn {a}">{a}</span>', f, f'<span class="small muted">{r}</span>'] for a, f, r in C.FUNCIONES]
    b = (f'<p class="lead">El ciclo 2 dejó claro que lo que falta no es diseño sino integración con datos reales. Esta es la propuesta técnica para la versión 3 (MVP de la Unidad 4): qué se conecta, qué se agrega y qué se quita.</p>{arq}'
         + table(['Integración', 'Fuente / servicio', 'Para qué', 'Sost.', 'Etapa'], integ, 'tight xs')
         )
    b2 = (table(['Acción', 'Funcionalidad', 'Por qué'], fn, 'tight')
         + f'<img class="banner vec" src="{VEC}17-ruta.png" style="height:40mm">'
         + '<div class="note" style="border-color:var(--accent);background:rgba(255,107,53,.05)"><b>Ejemplo · costo por km con precio real.</b> Costo de combustible por km = precio del litro ÷ rendimiento del auto. Con un rendimiento de 14 km/l, cada $50 que baja el litro reduce el costo en ~$3,6 por km; en los ~400 km de domicilios de un mes son ~$1.430 menos, más el ahorro de los 140 km que evita la ruta sugerida. La app usaría el precio de la bencinera elegida en lugar del valor fijo de $180/km del prototipo.</div>')
    return (section('s-tec', 'PROPUESTA TÉCNICA V3', 'Testeo · ciclo 2', 'Propuesta técnica: integraciones', b)
            + section('s-fun', 'PROPUESTA TÉCNICA V3', 'Testeo · ciclo 2', 'Funcionalidades: agregar, mantener y quitar', b2))


def recorrido():
    cards = ''.join(f'<div class="sc2"><div class="im"><img src="{img}"><span class="n">{i:02d}</span></div><div class="tx"><div class="h">{t}</div><div class="c v"><b>Mensaje / prototipo</b>{m}</div><div class="c p"><b>Hipótesis</b>{h}</div></div></div>' for i, (img, t, m, h) in enumerate(C.SB_PACIENTE, 1))
    b = (f'<p class="lead">El storyboard del paciente construido en la EV2 —con don Luis, adulto mayor atendido a domicilio, y Camila, estudiante con dolor de espalda— se convierte en el guion del testeo con pacientes: cada escena tiene un mensaje de la vista paciente y una hipótesis que validar.</p><div class="sb2">{cards}</div>'
         + '<p class="small" style="margin-top:3mm"><b>Lectura.</b> Las escenas 2 a 5 ya están prototipadas (mensajes M1 a M4). La reserva en línea (escena 1) depende de la agenda que Joselyn ya usa, y el seguimiento después del alta (escena 6) queda para la fase 2.</p>')
    return section('s-pac', 'RECORRIDO DEL PACIENTE', 'Validación y propuesta de valor', 'Storyboard del paciente', b)


def meta():
    M = C.METAFORA_ITER
    at = ''.join(f'<div class="attr"><div class="n">{n}</div><div class="s">…{s}</div>{sus(*tags)}<div class="r"><b>Ajuste según el testeo</b>{r}</div></div>' for n, s, r, tags in M['atributos'])
    b = f'''{card([('Instrumento', '3.1.3.1 Panel de metáforas y atributos iterado'), ('Fuente', 'Matriz CDM del ciclo 1'), ('Cambio', 'Metáfora y 2 atributos')])}
<div class="grid2"><div class="met" style="background:#F4F3F8;color:var(--page-text2)"><div class="k" style="color:var(--page-text2)">Antes · EV2</div><div class="m" style="color:var(--page-text2)">{M["antes"]}</div></div>
<div class="met"><div class="k">Después · iteración</div><div class="m">{M["despues"]}</div></div></div>
<p><b>Fundamento.</b> {M["porque"]}</p>
<div class="grid2" style="flex-wrap:wrap">{at}</div>'''
    return section('s-meta', '3.1.3.1 · METÁFORA', 'Iteración · versión 2', 'Panel de metáforas y atributos iterado', b, '3.1.3.1')


def sb2():
    b = card([('Instrumento', '3.1.3.2 Storyboard iterado'), ('Insumo', 'Matriz CDM del ciclo 1'), ('Formato', 'Escenas con capturas del prototipo v2'), ('Plantilla', 'Anexo A')])
    b += f'<div class="big-q" style="font-size:10.5pt">{C.PDV_ITER}</div>' + scenes(C.SCENES_ITER, it=True)
    return section('s-sb2', '3.1.3.2 · STORYBOARD ITERADO', 'Iteración · versión 2', 'Storyboard iterado', b, '3.1.3.2')


def mk2():
    pares = [('01_tablero.png', '01_tablero.png', 'Tablero'), ('06_agenda.png', '06_agenda.png', 'Agenda'), ('08_destinos.png', '08_mi_plata.png', 'Destinos → Mi plata')]
    ba = ''.join(f'<div><div class="ba"><img src="{V1 + a}"><span class="arr">→</span><img src="{V2 + c}"></div><div class="lbl">{t} · v1 → v2</div></div>' for a, c, t in pares)
    rows = [[f'<b>{i}</b>', c, h, r] for i, (c, h, r, _) in enumerate(C.CAMBIOS, 1)]
    b = (f'<div style="display:flex;justify-content:space-between">{ba}</div>'
         + table(['#', 'Cambio en v2', 'Hallazgo del ciclo 1', 'Requerimiento'], rows, 'tight')
         + '<p class="small"><b>Resultado.</b> Con los mismos scripts del ciclo 1, la versión 2 completa 11 de 11 tareas, con 0 errores WCAG AA, 0 objetivos táctiles bajo 44 px y letra mínima de 12 px. Archivo: <code>unidad-3/prototipo/copiloto-kine.html</code>.</p>')
    return section('s-mk2', '3.1.3.3 · MOCK-UP ITERADO', 'Iteración · versión 2', 'Mock-up iterado y ajustes fundamentados', b, '3.1.3.3')


def f2():
    b = card([('Instrumento', '3.1.3.4 Ficha de planificación del testeo de la iteración'), ('Foco', 'Técnico: necesidades puntuales'), ('Prototipo', 'v2'), ('Plantilla', 'Anexo A')])
    b += f'<div class="side"><img src="img/07-oficina-movil.jpg" style="width:58mm;height:32.4mm"><div class="big-q" style="font-size:10.5pt;margin:0">{C.FICHA_C2["objetivo"]}</div></div>' + ficha_tbl(C.FICHA_C2)
    b += ('<p class="small"><b>Referencia independiente.</b> Las pruebas comparan lo que muestra la app con una hoja de cálculo del equipo: clínica = valor × (1 − comisión 30 %) × (1 − retención 15,25 %); '
          'domicilio = valor − km × $180 − materiales − valor × 15,25 %. Script: <code>ciclo2/verificar_tecnico.js</code>.</p>')
    return section('s-f2', '3.1.3.4 · FICHA CICLO 2', 'Testeo · ciclo 2', 'Ficha de planificación del testeo de la iteración', b, '3.1.3.4')


def r2():
    pr = C.C2['pruebas']
    rows = [[f'<b>{p["id"]}</b>', p['req'], p['nombre'], '<span class="ok">✔</span>' if p['ok'] else '<span class="ko">✖</span>', f'<span class="small">{p["evidencia"][:70]}</span>'] for p in pr]
    cl = {'Cumple': 'ok', 'Cumple*': 'ok', 'Parcial': 'pa', 'Simulado': 'ko'}
    cov = [[f'<b>{r}</b>', n, f'<span class="{cl[e]}">{e}</span>', ev, f'<span class="small">{o}</span>'] for r, n, e, ev, o in C.COBERTURA]
    b = (kpis([(f'{sum(p["ok"] for p in pr)}/{len(pr)}', 'pruebas técnicas aprobadas'), ('$0', 'diferencia con la referencia en 5 atenciones'), ('11', 'toques para cerrar el día (antes ~60 min)'), ('39 KB', 'peso total; legible sin fuentes web')])
         + table(['#', 'Req.', 'Prueba', 'OK', 'Evidencia'], rows, 'tight xs')
         + '<p class="small"><b>Lectura.</b> Las once pruebas pasan. El dato clave para la usuaria: cerrar un día de cinco atenciones toma 11 toques y ningún número digitado, frente a la hora diaria de Excel que describió Catalina en la UA1. Cambiar el costo por km o la tasa de retención recalcula todo al instante, lo que hace a la herramienta resistente al alza de la Ley 21.133.</p>')
    b2 = (table(['#', 'Requerimiento (EV2)', 'Estado', 'Prueba', 'Observación'], cov, 'tight')
          + '<div class="kpi2"><div><div class="v">8</div><div class="l">cumplen (R9 con mapa ilustrativo)</div></div><div><div class="v">4</div><div class="l">parciales: R1, R4, R10, R13</div></div><div><div class="v">1</div><div class="l">simulado: R2, integración con la agenda</div></div></div>'
          + '<p class="small">Los parciales y el simulado no son problemas de diseño sino de integración con datos reales; se convierten en las brechas B1 a B7.</p>')
    return (section('s-r2', 'CICLO 2 · RESULTADOS', 'Testeo · ciclo 2', 'Resultados de las pruebas técnicas', b)
            + section('s-cov', 'CICLO 2 · COBERTURA', 'Testeo · ciclo 2', 'Cobertura de requerimientos', b2))


def cdm2():
    br = [[f'<b>{b_}</b>', t, d, f'<span class="code{"" if "MVP" in f or "Inm" in f else " b"}">{f}</span>'] for b_, t, d, f in C.BRECHAS]
    b = (table(['#', 'Brecha técnica', 'Qué hacer', 'Cuándo'], br, 'tight') + '<h3>Matriz CDM del ciclo 2</h3>' + cdm(C.CDM_C2)
         + '<p><b>Análisis y conclusiones.</b> El prototipo v2 cumple 8 de 13 requerimientos, 4 de forma parcial y 1 simulado. Lo que falta no es diseño sino integración: agenda real, respaldo en la nube y proyección desde el historial. B6 (motivo de consulta visible) se resuelve antes de usar datos reales.</p>')
    return section('s-cdm2', '3.1.2.4 · CDM CICLO 2', 'Testeo · ciclo 2', 'Brechas y matriz CDM del ciclo 2', b, '3.1.2.4')


def val():
    hip = [[f'<b>{h}</b>', p, t, c, '<span class="pend">Pendiente</span>'] for h, p, t, _, c, _ in K.HIP]
    pf = ''.join(f'<div class="pfc {p["tipo"]}"><div class="cd">{p["c"]}</div><div><b>{p["n"]}</b> · {p["t"]}<div class="small muted">{p["s"]} · {p["m"]}</div></div></div>' for p in K.PERF)
    b = f'''<p class="lead">Para validar con usuarios externos preparamos un kit de testeo (19 páginas) para tres públicos: las <b>kinesiólogas</b>, que usan la app; los
<b>pacientes</b>, que reciben sus mensajes y de quienes depende la ruta; y una <b>contadora</b>, que recibe el resumen mensual.</p>
<div class="pj"><figure><img src="img/storyboard/personajes/joselyn.jpg"><figcaption><b>Joselyn</b>Usuaria principal · kinesióloga</figcaption></figure>
<figure><img src="img/storyboard/personajes/don-luis.jpg"><figcaption><b>Don Luis</b>Paciente · adulto mayor a domicilio</figcaption></figure>
<figure><img src="img/storyboard/personajes/camila.jpg"><figcaption><b>Camila</b>Paciente · estudiante con dolor de espalda</figcaption></figure>
<figure><img src="{VEC}19-pacientes.png" style="object-position:50% 70%"><figcaption><b>Otros perfiles</b>Cuidadora, oficina, turnos y deportista</figcaption></figure></div>
<div class="pfs2">{pf}</div>
<h3>Hipótesis y criterios de éxito</h3>{table(['#', 'Público', 'Hipótesis', 'Éxito si…', 'Resultado'], hip, 'tight xs')}
'''
    b2 = f'''<p class="lead">Las kinesiólogas usan la app; los pacientes solo reciben sus mensajes. Para testear con ellos construimos una vista que simula los cuatro mensajes que recibirían por WhatsApp.</p>
{phones([(PAC + '01_recordatorio.png', 'M1 · Recordatorio · H5'), (PAC + '02_voy_en_camino.png', 'M2 · Voy en camino · H6'), (PAC + '03_comprobante.png', 'M3 · Comprobante · H7'), (PAC + '04_hora_liberada.png', 'M4 · Hora liberada · H10')]).replace('class="phones"', 'class="phones big"')}
<p class="small">La hipótesis más riesgosa del modelo es H5: si los pacientes no aceptan una ventana de llegada de 30 minutos, la ruta sugerida no se puede aplicar. Por eso los pacientes son parte del testeo aunque no usen la app. Los mensajes no incluyen diagnósticos (Ley 21.719), la vista tiene “Letra grande” para adultos mayores y sus cuatro pantallas pasan la auditoría WCAG AA sin errores. Archivo: <code>prototipo/vista-paciente.html</code>.</p>
<div class="note"><b>Estado y siguientes pasos.</b> Antes de las sesiones se integra la retroalimentación de la emprendedora en la reunión del 12 de noviembre (grabación compartida por el profesor). Los pacientes de Joselyn participan solo si ella los invita; se complementa con personas del entorno del equipo que calcen con cada perfil.</div>
<h3>Contenido del kit de testeo</h3>
{table(['Documento', 'Para qué sirve'], [['Plan e hipótesis', '10 hipótesis con métrica y criterio de éxito definidos antes de testear'], ['Perfiles', '9 perfiles con criterios de reclutamiento y adaptaciones'],
        ['Guiones A, B y C', 'Kinesiólogas (40–60 min), pacientes (15 min) y contadora (20 min)'], ['Consentimiento informado', 'Participación voluntaria, sin datos de salud (Ley 21.719)'],
        ['Pautas y cuestionarios', 'Observación de tareas, encuesta de pacientes y escala SUS'], ['Matriz de consolidación', 'Regla de decisión por hipótesis: mantener, iterar o descartar']], 'tight')}'''
    return (section('s-val', 'VALIDACIÓN CON USUARIOS', 'Validación y propuesta de valor', 'Validación con usuarios externos', b)
            + section('s-vp', 'VISTA PACIENTE', 'Validación y propuesta de valor', 'Nuevo estímulo: vista paciente', b2))


def pagina_pv():
    return f'''<div class="full dark solid"><img class="phone" src="{V2}01_tablero.png" style="width:66mm;right:16mm;bottom:30mm;border-radius:8mm;border:2.5mm solid #1E1A30">
<div class="in" style="top:36mm"><div class="kick" style="color:#FF6B35">Propuesta de valor iterada · 3.1.5</div>
<div class="big">EL COPILOTO<br>DE SU <em>DÍA</em>.</div>
<div class="pv">Ordena su ruta y convierte cada atención en <b>ganancia real</b>, para que entregue sus números <b>sin pasar nada a Excel</b>.</div>
<div class="tags"><span>Anticipador</span><span>Claro</span><span>Automático y corregible</span><span>Sostenible</span></div></div>
<div class="foot"><span>Propuesta de valor iterada</span><span>Semana 13</span></div></div>'''


def pv():
    b = f'''<div class="grid2"><div class="box"><div class="t" style="color:var(--page-text2)">Antes · EV2</div><div style="font-size:10pt;font-weight:600;line-height:1.42">{C.PDV_EV2}</div></div>
<div class="box" style="border-color:var(--accent)"><div class="t">Después · iteración</div><div style="font-size:10pt;font-weight:600;line-height:1.42">{C.PDV_ITER}</div></div></div>
<img class="banner vec" src="{VEC}17-ruta.png">
<h3>Qué cambió y por qué</h3>
{table(['Cambio', 'Evidencia que lo respalda'], [
        ['<b>La ruta pasa al centro</b> (“ordena su ruta de domicilios”)', 'Ciclo 1: la ruta fue la vista con más valor percibido; ciclo 2: 7 km menos por día (P8).'],
        ['<b>Sale “se conecta a la agenda que ya usa”</b>', 'Ciclo 2: la integración es simulada (R2, brecha B1). No prometemos lo que el MVP aún no cumple.'],
        ['<b>Entra “entrega sus números a la contadora sin Excel”</b>', 'Ciclo 2: exportación verificada sin diagnósticos ni nombres (P6) y retención configurable (P11).'],
        ['<b>“Ya descontados”</b> en vez de “descontando”', 'Ciclo 2: cálculo exacto en 5 de 5 atenciones (P1); el usuario no hace la cuenta.']], 'tight')}
<h3>Métricas claves para la Unidad 4</h3>
{table(['Métrica', 'Hoy (prototipo)', 'Meta MVP'], [['Tiempo de cierre del día', '11 toques (~1 min)', '< 30 min/día real (desafío)'], ['Usabilidad (SUS)', 'Por medir con usuarias', '≥ 75'],
        ['Pacientes que aceptan la ventana de llegada', 'Por medir (H5)', '≥ 70 %'], ['Km ahorrados por día con domicilios', '7 km (día de ejemplo)', 'Medido con rutas reales']], 'tight')}'''
    return section('s-pv', '3.1.5 · PROPUESTA DE VALOR', 'Validación y propuesta de valor', 'Propuesta de valor iterada', b, '3.1.5')


def pestal():
    ico = {'Político': 'politico', 'Económico': 'economico', 'Social': 'social', 'Tecnológico': 'tecnologico', 'Ambiental': 'ambiental', 'Legal': 'legal'}
    rows = ''.join(f'''<tr><td><img src="img/pestal-{ico[n]}.png" style="width:7.5mm;height:7.5mm;display:block;margin-bottom:.6mm">{n}<small>Original: {o["f"]}</small></td>
<td>{p["f"]}</td><td>{p["o"]}</td><td>{p["a"]}</td></tr>''' for n, o, p in C.PESTAL)
    b = f'''<p class="small"><b>Instrumento 3.1.4.1</b> · base: PESTAL de la UA1 (1.1.3.1) · profundizado con la evidencia de los ciclos 1 y 2 · plantilla oficial en el Anexo A.<br><b>Desafío:</b> {C.DESAFIO}</p>
<table class="pestal tight xs"><thead><tr><th>Factor</th><th>Factor profundizado</th><th>Oportunidad</th><th>Amenaza</th></tr></thead><tbody>{rows}</tbody></table>'''
    return section('s-pestal', '3.1.4.1 · PESTAL', 'Estado del arte y pertinencia', 'Matriz PESTAL profundizada', b, '3.1.4.1')


def arte():
    dot = {2: '<span class="dot d2">●</span>', 1: '<span class="dot d1">◐</span>', 0: '<span class="dot d0">○</span>'}
    rows = [[('<b>' + n + '</b>') if 'Copiloto' in n else n] + [dot[v] for v in vs] for n, vs in C.ARTE]
    tr = [[f'<b>{t}</b>', d, r] for t, d, r in C.TENDENCIAS]
    b = (f'<div class="side"><img src="{VEC}20-estado-arte.png" style="width:54mm;height:30.2mm"><p class="small" style="margin:0"><b>Relación con el desafío.</b> El mercado ofrece agendas (AgendaPro, Encuadrado, Cal.com) y contabilidad (Nubox), pero nadie conecta la cita con lo que realmente queda después de comisión, traslado y retención. Ese cruce es justamente lo que el desafío pide.</p></div>'
         + table(['Solución'] + C.ARTE_VARS, rows, 'mat tight xs')
         + '<p class="small muted">● cubre · ◐ parcial · ○ no cubre. Antecedentes revisados en la UA1 en sus sitios oficiales. Copiloto Kine se evalúa por lo que hace hoy: agenda y ruta simuladas = ◐.</p>'
         + '<h3>Tendencias de la especialidad</h3>' + table(['Tendencia', 'Qué está pasando', 'Cómo responde Copiloto Kine v2'], tr, 'tight xs')
         )
    return section('s-arte', '3.1.4 · ESTADO DEL ARTE', 'Estado del arte y pertinencia', 'Estado del arte y tendencias', b, '3.1.4')


def pert():
    rows = [[f'<b>{a}</b>', b_, c] for a, b_, c in C.PERTINENCIA]
    b = (table(['Dimensión', 'Lo que sabemos', 'Cómo responde la propuesta iterada'], rows, 'tight')
         + '<div class="big-q" style="font-size:12pt">La propuesta es pertinente en lo que el prototipo demuestra: resuelve el problema de origen, se diferencia del estado del arte y responde a las tendencias. Quedan tres decisiones abiertas para la validación con usuarias: precio, ventana horaria y alcance del MVP.</div>'
         + '<img class="banner" src="img/02-caso.jpg">')
    return section('s-pert', '3.1.5 · PERTINENCIA', 'Estado del arte y pertinencia', 'Pertinencia de la propuesta de valor', b, '3.1.5')


def sost():
    b = f'''<img class="banner vec" src="{VEC}21-sostenible.png">
<div class="grid3"><div class="box"><div class="t">Económico {sus('Ec')}</div><div style="font-family:var(--fd);font-size:22pt;color:var(--accent)">+$570.000</div>
Acciones de la proyección (packs, grupo, colchón) para cubrir enero y febrero. Retención configurable ante el alza de la Ley 21.133 (15,25 % → 16 % → 17 %).</div>
<div class="box"><div class="t">Social {sus('So')}</div><div style="font-family:var(--fd);font-size:22pt;color:var(--accent)">~1 h → 11 toques</div>
Cierre del día sin trabajo nocturno. Accesibilidad WCAG AA, letra grande para adultos mayores y datos de salud fuera del sistema (Ley 21.719).</div>
<div class="box"><div class="t">Ambiental {sus('Am')}</div><div style="font-family:var(--fd);font-size:22pt;color:var(--accent)">−140 km/mes</div>
Ruta sugerida: 20 vs. 27 km en el día de ejemplo (−26 %). Con 20 días de domicilios: ~10 l de bencina y ~23 kg de CO2 menos (estimación del equipo: 14 km/l, 2,3 kg CO2/l).</div></div>
<h3>Sostenibilidad en el prototipo, no solo en el discurso</h3>
{table(['Decisión de diseño', 'Dimensión', 'Evidencia'], [['Registro de un toque y corrección inmediata', sus('So', 'Ec'), 'T2, T4, T10 · P3, P4, P7'], ['Ruta agrupada por sector', sus('Am', 'Ec'), 'P8: −7 km y $1.260 por día'],
        ['Colchón y acciones para meses bajos', sus('Ec'), 'T7: brecha de $770.000 → $530.000 con una acción'], ['Exportación sin datos clínicos', sus('So'), 'P6'], ['Prototipo liviano (39 KB)', sus('Am', 'So'), 'P9: funciona con datos móviles']], 'tight')}'''
    return section('s-sost', 'SOSTENIBILIDAD', 'Cierre', 'Enfoque sostenible', b)


def gest():
    w = C.GANTT_W
    rows = ''.join(f'<tr><td>{t}</td>' + ''.join(f'<td class="{m.get(x, "")}">{"◆" if m.get(x) == "hito" else ""}</td>' for x in w) + '</tr>' for t, m in C.GANTT)
    roles = [['Claudia Cifuentes', 'Moderación de sesiones de testeo'], ['Néstor Rivera', 'Prototipo y ejecución de tareas'], ['Francisco Ahumada', 'Registro de observaciones y matrices CDM'], ['Benjamín Vera Yáñez', 'Secretario técnico: consolidación, auditoría técnica y bitácora']]
    b = (f'<table class="gantt"><thead><tr><th>Actividad</th>{"".join(f"<th>{x}</th>" for x in w)}</tr></thead><tbody>{rows}</tbody></table>'
         + '<h3>Roles</h3>' + table(['Integrante', 'Rol'], roles, 'tight')
         + '<h3>Bitácora y evidencias</h3>' + ul(['Bitácora de avance U3 (versión S13) completa con los seis indicadores: <code>entregas/Bitacora_avance_U3_EV3.xlsx</code>.',
                                                  'Prototipos: <code>prototipo/copiloto-kine-v1.html</code>, <code>copiloto-kine.html</code> y <code>vista-paciente.html</code>, con capturas.',
                                                  'Ciclos: scripts y resultados JSON en <code>ciclo1/</code> y <code>ciclo2/</code>; kit de testeo en <code>testeo/</code>.'])
         + '<p class="small"><b>Aprendizaje de gestión.</b> Las sesiones con usuarias externas deben agendarse desde la primera semana de la unidad; esta vez quedaron para después de la reunión con la emprendedora.</p>')
    return section('s-gest', 'GESTIÓN', 'Cierre', 'Gestión de la fase y bitácora', b)


def concl():
    b = '''<div class="grid3"><div class="box"><div class="t">Aprendimos</div><ul><li>Medir tareas, accesibilidad y exactitud da evidencia más útil que preguntar si “gusta”.</li><li>“Automático” sin “corregible” genera registros falsos.</li><li>La ruta es tan valiosa como el tablero: la metáfora se movió al copiloto.</li><li>El paciente también es usuario: sin su ventana horaria no hay ruta.</li></ul></div>
<div class="box"><div class="t">Logramos</div><ul><li>Prototipo v2 navegable: 11/11 tareas, 0 errores WCAG AA.</li><li>11/11 pruebas técnicas: cálculo exacto y exportación sin datos clínicos.</li><li>8 de 13 requerimientos cumplidos (4 parciales) y 7 brechas priorizadas.</li><li>Kit de testeo con 10 hipótesis y 9 perfiles.</li></ul></div>
<div class="box"><div class="t">Sigue</div><ul><li>Integrar la retroalimentación de la emprendedora (12/11).</li><li>Sesiones con Joselyn, Catalina, pacientes y contadora.</li><li>Consolidar: SUS, CDM con usuarios y decisiones v3.</li><li>UA4: MVP con agenda real, respaldo en la nube y aviso por WhatsApp.</li></ul></div></div>
<h3>Conclusión</h3><p>La Unidad 3 convirtió una propuesta de valor en un prototipo que se puede usar, medir y corregir. Testear en dos ciclos con focos distintos permitió arreglar primero la experiencia y después verificar que la herramienta resuelve con exactitud las necesidades puntuales de la kinesióloga. La propuesta iterada es más honesta —promete solo lo que el prototipo demuestra— y más amplia, porque incorpora la ruta y al paciente. El siguiente paso es llevarla a las personas.</p>
<img class="banner" src="img/05-entrevista.jpg">'''
    return section('s-concl', 'CONCLUSIONES', 'Cierre', 'Conclusiones y próximos pasos', b)


def refs():
    r = ['Brooke, J. (1996). SUS: A “quick and dirty” usability scale. En P. W. Jordan et al. (Eds.), <i>Usability evaluation in industry</i> (pp. 189–194). Taylor &amp; Francis.',
         'Deque Systems. (2024). <i>axe-core</i> (versión 4.10) [Software]. https://github.com/dequelabs/axe-core',
         'INACAP. (2026). <i>Manual del estudiante y toolkit, Unidad 3: Prototipado y testeo</i>. Innovación y Emprendimiento III (FGIE03).',
         'Ley N.° 20.584. (2012). Regula los derechos y deberes de las personas en relación con su atención en salud. Biblioteca del Congreso Nacional de Chile.',
         'Ley N.° 21.133. (2019). Incorporación de los trabajadores independientes a los regímenes de protección social. Biblioteca del Congreso Nacional de Chile.',
         'Ley N.° 21.719. (2024). Regula la protección y el tratamiento de los datos personales. Biblioteca del Congreso Nacional de Chile.',
         'Microsoft. (2026). <i>Playwright</i> [Software]. https://playwright.dev',
         'Nielsen, J. (1994). <i>10 usability heuristics for user interface design</i>. Nielsen Norman Group.',
         'W3C. (2018). <i>Web Content Accessibility Guidelines (WCAG) 2.1</i>. https://www.w3.org/TR/WCAG21/',
         'Equipo del proyecto. (2026). Informes EV1 y EV2 y entrevistas a Joselyn Toledo y Catalina (UA1). INACAP Rancagua.']
    return section('s-ref', 'REFERENCIAS', 'Fuentes', 'Referencias', ''.join(f'<p class="small" style="padding-left:6mm;text-indent:-6mm">{x}</p>' for x in r))


def pagina_anexo(titles):
    li = ''.join(f'<div style="border-bottom:1px solid #2A2640;padding:2mm 0;font-size:9.5pt;color:#E9E6F7">{t}</div>' for t in titles)
    return f'''<div class="full dark"><div class="in" style="top:34mm"><div class="kick" style="color:#FF6B35">Anexo A</div>
<div class="big">TOOLKIT UA3<br><em>COMPLETO</em>.</div>
<div class="lead2">Las plantillas oficiales de Innovación y Emprendimiento III, llenas con el trabajo del equipo. Cada instrumento conserva su código y su formato original.</div>
<div style="margin-top:8mm;max-width:150mm">{li}</div></div>
<div class="foot"><span>Plantillas oficiales del toolkit</span><span>3.1.2.1 – 3.1.4.1</span></div></div>'''


def pagina_cierre():
    return '''<div class="full sunset"><img src="img/15-horizonte.jpg">
<div class="in" style="top:30mm"><div class="kick" style="color:#FFD9C7">Conclusión</div>
<div class="big" style="font-size:38pt">PROBAR CON EVIDENCIA, ITERAR CON CRITERIO Y <em style="color:#FFD9C7">LLEVARLO A LAS PERSONAS</em>.</div>
<div class="lead2" style="color:#F3E6FF">Copiloto Kine está listo para su ciclo con usuarias reales y para convertirse en MVP en la Unidad 4.</div></div>
<div class="foot"><span>Criterios 3.1.1 – 3.1.5</span><span>Gracias</span></div></div>'''


# ---------------------------------------------------------------- anexo: plantillas en A4
def anexo(first):
    from anexo_toolkit import MUTE, INK, ORANGE, F
    out = fitz.open(); n = first; titles = []
    for title, src in anexo_u3.build():
        sp = src[0]; titles.append(title)
        tall = sp.rect.height > sp.rect.width
        W, H = (595.28, 841.89) if tall else (841.89, 595.28)
        page = out.new_page(width=W, height=H)
        page.insert_font(fontname='fmono', fontfile=F['mono'])
        m = 28
        page.show_pdf_page(fitz.Rect(m, 42, W - m, H - 32), src, 0, keep_proportion=True)
        page.insert_text((m, 24), anexo_u3.T.clean('ANEXO A · ' + title).upper(), fontname='fmono', fontsize=6.6, color=ORANGE)
        page.draw_line(fitz.Point(m, 31), fitz.Point(W - m, 31), color=(0.89, 0.88, 0.94), width=0.6)
        page.draw_line(fitz.Point(m, H - 24), fitz.Point(W - m, H - 24), color=(0.89, 0.88, 0.94), width=0.6)
        page.insert_text((m, H - 13), 'INACAP Rancagua · UA3 Prototipado y Testeo · Evaluación N°3 · Anexo', fontname='fmono', fontsize=6.3, color=MUTE)
        page.insert_text((W - m - 52, H - 13), f'Página {n}', fontname='fmono', fontsize=6.6, color=INK)
        n += 1
    return out, titles


# ---------------------------------------------------------------- ensamblado
EXTRA = '''<style>
.pfs2{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;margin:2mm 0 3mm}
.pfc{display:flex;gap:2mm;border:1px solid var(--page-border);border-radius:5px;padding:1.6mm 2mm;font-size:7.3pt;line-height:1.35;break-inside:avoid}
.pfc .cd{width:7.5mm;height:7.5mm;border-radius:4px;background:#12101E;color:var(--accent);font-family:var(--fd);font-size:11pt;display:flex;align-items:center;justify-content:center;flex:none}
.pfc.k .cd{background:var(--accent);color:#fff}.pfc.e .cd{background:var(--h6);color:#fff}
.pfc .small{font-size:6.6pt}
table.ficha{font-size:7pt}table.ficha td{padding:3px 4px}
.attr{width:calc(50% - 2mm);margin-bottom:3mm}
code{font-family:var(--fm);font-size:7pt;background:var(--page-card);padding:0 3px;border-radius:2px}
.cover .grid{max-width:118mm}
.sb2{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2.6mm}
.sc2{border:1px solid var(--page-border);border-radius:6px;overflow:hidden;break-inside:avoid;background:#fff}
.sc2 .im{position:relative;height:31mm;overflow:hidden}.sc2 .im img{width:100%;height:100%;object-fit:cover;display:block}
.sc2 .im .n{position:absolute;left:2mm;top:2mm;background:var(--accent);color:#fff;font-family:var(--fd);font-size:12pt;line-height:1;padding:1mm 1.8mm .6mm;border-radius:3px}
.sc2 .tx{padding:1.8mm 2.2mm 2.2mm;font-size:7.1pt;line-height:1.36}
.sc2 .h{font-weight:700;font-size:8.2pt;margin-bottom:.8mm}
.sc2 .c{margin-top:1.1mm;padding:.9mm 1.4mm;border-radius:3px;font-size:6.7pt;line-height:1.3}
.sc2 .c b{display:block;font-family:var(--fm);font-size:5.5pt;letter-spacing:.08em;text-transform:uppercase;font-weight:400}
.sc2 .c.p{background:#F1EEFA}.sc2 .c.p b{color:#7B3FA0}.sc2 .c.v{background:rgba(255,107,53,.08)}.sc2 .c.v b{color:var(--accent)}
.sc2 .c.ok{background:rgba(31,138,91,.08)}.sc2 .c.ok b{color:var(--ok)}.sc2 .c.mj{background:rgba(255,179,71,.14)}.sc2 .c.mj b{color:#B7701A}
.vv{display:inline-block;font-family:var(--fm);font-size:6pt;letter-spacing:.08em;text-transform:uppercase;border-radius:3px;padding:0 4px;color:#fff}
.vv.a{background:#9B98B8}.vv.b{background:var(--accent)}
.pj{display:flex;gap:3mm;margin:1mm 0 3mm}.pj figure{flex:1;margin:0;border:1px solid var(--page-border);border-radius:6px;overflow:hidden;background:#F4F3FA}
.pj img{width:100%;height:17mm;object-fit:cover;object-position:50% 30%;display:block}.pj figcaption{font-size:6.6pt;padding:.8mm 1.6mm;line-height:1.3}.pj figcaption b{display:block;font-size:7.8pt}
.arq{display:grid;grid-template-columns:1fr 46mm 1fr;gap:3mm;align-items:center;margin:2mm 0 4mm}
.arq .col{display:flex;flex-direction:column;gap:2mm}
.arq .nd{border:1px solid var(--page-border);border-left:3px solid var(--accent);border-radius:6px;padding:1.6mm 2.2mm;font-size:7pt;line-height:1.3;background:#fff}
.arq .nd b{display:block;font-size:7.8pt}.arq .nd.p{border-left-color:var(--h6)}
.arq .core{background:#12101E;color:#F5F2FF;border-radius:10px;padding:4mm 3mm;text-align:center}
.arq .core .t{font-family:var(--fd);font-size:17pt;line-height:1;color:var(--accent)}.arq .core .d{font-size:6.8pt;color:#C9C6DA;margin-top:1.5mm;line-height:1.35}
.fn{display:inline-block;font-family:var(--fm);font-size:6pt;letter-spacing:.08em;text-transform:uppercase;border-radius:3px;padding:0 5px;color:#fff}
.fn.Agregar{background:var(--ok)}.fn.Mantener{background:#7B3FA0}.fn.Quitar{background:#C2283F}
.banner.vec{height:46mm;object-fit:contain;background:#F4F2FC}
.pestal td:first-child small{font-family:var(--fb);font-size:6.6pt;letter-spacing:0;line-height:1.35;margin-top:1mm}.pestal td:first-child{width:24%}.pestal td{font-size:7.4pt;padding:2.6px 5px}.pestal td:first-child{font-size:11pt}
.side img{object-fit:cover}
#s-indice .toc li{padding:.45mm 0;font-size:8pt}#s-indice .toc .grp{margin:1.5mm 0 0}#s-indice h2{margin-bottom:0}#s-indice .stmt{display:none}
.phones.s6 figure{width:25.5mm}.phones.s6 img{width:25.5mm;height:55.2mm}
.phones.big figure{width:38mm}.phones.big img{width:38mm;height:82.2mm}
table.xs{font-size:7.3pt}table.xs td{padding:2.6px 5px}
</style>'''
HEAD = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Evaluación 3 — Prototipado y testeo</title><link rel="stylesheet" href="ev3.css">{EXTRA}</head><body>'


def render(body, name):
    path = os.path.join(HERE, name)
    open(path, 'w', encoding='utf-8').write(HEAD + body + '</body></html>')
    return HTML(path, base_url=HERE).write_pdf()


def main_body():
    return (portada() + indice() + intro() + ruta() + sqa() + sb1() + mk1() + pagina_cita() + f1() + r1() + cdm1() + pagina_cifras()
            + iter_docs() + meta() + sb2() + mk2() + f2() + r2() + cdm2() + tecnico() + val() + recorrido() + pagina_pv() + pv() + pestal() + arte() + pert() + sost() + gest() + concl() + refs())


if __name__ == '__main__':
    n_main = fitz.open(stream=render(main_body(), '_tmp.html'), filetype='pdf').page_count
    ANEXO_PAGE = n_main + 1
    main_pdf = fitz.open(stream=render(main_body(), 'Evaluacion3_Informe_Prototipado.html'), filetype='pdf')
    assert main_pdf.page_count == n_main
    anexo_pdf, titles = anexo(n_main + 2)
    for extra in (fitz.open(stream=render(pagina_anexo(titles), '_anexo.html'), filetype='pdf'), anexo_pdf,
                  fitz.open(stream=render(pagina_cierre(), '_cierre.html'), filetype='pdf')):
        main_pdf.insert_pdf(extra)
    for f in ('_tmp.html', '_anexo.html', '_cierre.html'):
        os.remove(os.path.join(HERE, f))
    main_pdf.save(os.path.join(HERE, 'Evaluacion3_Informe_Prototipado.pdf'), garbage=3, deflate=True)
    print('ok', main_pdf.page_count, 'páginas · anexo desde', ANEXO_PAGE)
