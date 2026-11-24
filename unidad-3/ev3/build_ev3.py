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
URL = 'https://copiloto-kine.vercel.app'
URL_PRO, URL_CLI = URL + '/profesional/', URL + '/cliente/'
lnk = lambda u, t=None: f'<a class="lk" href="{u}">{t or u.replace("https://", "")}</a>'
V1, V2, PAC = '../prototipo/capturas_v1/', '../prototipo/capturas_v2/', '../prototipo/capturas_paciente/'
V3 = '../prototipo/capturas_v3/'
PAC1 = '../prototipo/capturas_paciente_v1/'
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
    's-links': 'Dos vistas, <b>un mismo sistema</b>.',
    's-ruta': 'Dos ciclos con focos distintos: <b>primero usarla, después confiar en ella</b>.',
    's-sqa': 'Sabíamos prototipar; teníamos que <b>aprender a medir</b>.',
    's-sb1': 'Un día de Josselyn, <b>de las 11:40 p. m. al domingo</b>.',
    's-mk1': 'Un enlace en el celular: <b>nada que instalar</b>.',
    's-f1': 'El ciclo 1 pregunta: <b>¿se puede usar y se ve bien?</b>',
    's-r1': 'Funciona en lo central y <b>falla en lo que permite corregir</b>.',
    's-cdm1': 'Todo problema de severidad 2 o más <b>entra a la iteración</b>.',
    's-iter': 'Primero <b>visual y funcional</b>; después <b>técnica</b>.',
    's-fun': 'Menos digitación, <b>más datos reales</b>.',
    's-tec': 'Lo que falta no es diseño: <b>es conectar datos reales</b>.',
    's-retro': 'La clienta ya hace lo que la app promete: <b>a mano y de noche</b>.',
    
    's-retro3': 'Todos vieron el mismo problema: <b>la diferencia está en cómo se resuelve</b>.',
    's-aplica': 'De la conversación a <b>cambios medibles</b>.',
    's-vp2': 'Un mensaje, <b>una decisión</b>.',
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
<div class="desc">Fase de desarrollo, prototipado y testeo del Ciclo de Innovación INACAP aplicada al caso de Josselyn Toledo, kinesióloga independiente
con atención en cuatro canales. Del storyboard al prototipo navegable Copiloto Kine: dos ciclos de testeo internos, la
validación con la clienta y Sercotec, la iteración a la versión 3 y su verificación frente al estado del arte, con trazabilidad a los criterios 3.1.1 a 3.1.5.</div>
<div class="grid">{chips}</div><div class="url">PROTOTIPOS · <a href="{URL_PRO}">VISTA PROFESIONAL</a> · <a href="{URL_CLI}">VISTA CLIENTE</a> · copiloto-kine.vercel.app</div></div>
<div class="meta"><div class="team"><div>Francisco Ahumada · Claudia Cifuentes</div><div>Néstor Rivera · Benjamín Vera Yáñez</div>
<div class="inst" style="margin-top:1mm">Diseño Digital · INACAP Rancagua</div><div class="inst" style="margin-top:1mm">Profesor: Roberto Escobar Donoso</div></div>
<div style="text-align:right"><div class="inst">Rancagua, Chile</div><div class="inst">Noviembre 2026</div></div></div></div>'''


def indice():
    items = [('Marco', [('01', 's-intro', 'Introducción, caso y propuesta de valor de partida'), ('Links', 's-links', 'Prototipos navegables: vista profesional y vista cliente'), ('02', 's-ruta', 'Ruta metodológica y trazabilidad de criterios'), ('3.1.1.1', 's-sqa', 'Evaluación diagnóstica: tabla SQA')]),
             ('Prototipado · versión 1', [('3.1.2.1', 's-sb1', 'Storyboard con propuesta de valor'), ('3.1.2.2', 's-mk1', 'Mock-up con propuesta de valor')]),
             ('Testeo · ciclo 1 funcional y estético', [('3.1.2.3', 's-f1', 'Ficha de planificación del testeo'), ('Ciclo 1', 's-r1', 'Resultados: tareas, accesibilidad y heurísticas'), ('3.1.2.4', 's-cdm1', 'Matriz CDM con propuesta de valor')]),
             ('Iteración · versión 2', [('Iteración', 's-iter', 'De la versión actual a la actualizada'), ('3.1.3.1', 's-meta', 'Panel de metáforas y atributos iterado'), ('3.1.3.2', 's-sb2', 'Storyboard iterado'), ('3.1.3.3', 's-mk2', 'Mock-up iterado y ajustes fundamentados')]),
             ('Testeo · ciclo 2 técnico', [('3.1.3.4', 's-f2', 'Ficha de planificación del testeo de la iteración'), ('Ciclo 2', 's-r2', 'Resultados técnicos y cobertura de requerimientos'), ('3.1.2.4', 's-cdm2', 'Brechas y matriz CDM del ciclo 2'), ('Técnica', 's-tec', 'Propuesta técnica del MVP: integraciones y funcionalidades')]),
             ('Testeo · ciclo 3 con la clienta', [('3.1.2.3', 's-f3', 'Ficha del ciclo 3: clienta, Sercotec y docentes'), ('12/11', 's-retro', 'Retroalimentación de la clienta y Sercotec'), ('12/11', 's-retro2', 'Patrones y cambios a la propuesta'), ('12/11', 's-retro3', 'Hallazgos generales y otras propuestas revisadas'), ('12/11', 's-comp', 'Comparativa de las 4 propuestas'), ('3.1.2.4', 's-cdm3', 'Matriz CDM del ciclo 3'), ('12/11', 's-aplica', 'Cómo aplicamos los hallazgos')]),
             ('Iteración · versión 3', [('Iteración', 's-iter3', 'De la versión 2 a la versión 3'), ('3.1.3.1', 's-meta3', 'Panel de metáforas y atributos (v3)'), ('3.1.3.2', 's-sb3', 'Storyboard iterado (v3)'), ('3.1.3.3', 's-mk3', 'Mock-up iterado (v3) y ajustes'), ('Verif.', 's-ver3', 'Verificación del prototipo v3'), ('3.1.3.4', 's-f4', 'Ficha del testeo de la iteración · ciclo 4'), ('Costo', 's-cost', 'Costeo de la solución')]),
             ('Validación y propuesta de valor', [('Usuarios', 's-val', 'Validación con usuarios externos: kit de testeo'), ('Paciente', 's-pac', 'Storyboard del paciente'), ('Paciente', 's-vp', 'Vista paciente · versión actual'), ('Paciente', 's-vp2', 'Vista paciente v2 para personas mayores'), ('3.1.5', 's-pv', 'Propuesta de valor iterada')]),
             ('Estado del arte y pertinencia', [('3.1.4.1', 's-pestal', 'Matriz PESTAL profundizada'), ('3.1.4', 's-arte', 'Estado del arte y tendencias'), ('3.1.5', 's-pert', 'Pertinencia de la propuesta de valor')]),
             ('Cierre', [('Sost.', 's-sost', 'Enfoque sostenible'), ('Gestión', 's-gest', 'Gestión de la fase y bitácora'), ('Cierre', 's-concl', 'Conclusiones y próximos pasos'), ('Ref.', 's-ref', 'Referencias')])]
    out = ''
    for g, li in items:
        out += f'<div class="grp">{g}</div><ul>' + ''.join(f'<li><span class="c">{c}</span><span class="t"><a href="#{h}">{t}</a></span></li>' for c, h, t in li) + '</ul>'
    out += ('<div class="grp">Anexo</div><ul>'
            f'<li><span class="c">Anexo A</span><span class="t">Plantillas oficiales del toolkit UA3 completas (11 plantillas, ciclos 1 a 4)</span><span style="font-family:var(--fm);font-size:8pt">{ANEXO_PAGE}</span></li></ul>')
    return section('s-indice', 'ÍNDICE', 'Contenido', 'Índice', f'<div class="toc">{out}</div>')


def intro():
    b = f'''<p class="lead">La Unidad 3 corresponde a la fase de <strong>desarrollo, prototipado y testeo</strong> del Ciclo de Innovación INACAP. Su aprendizaje esperado
es elaborar el prototipo de la propuesta de valor, testearlo con usuarios en más de un ciclo, ajustarlo según los resultados y verificar su pertinencia frente al estado del arte y las tendencias.</p>
<h3>Caso y punto de partida</h3>
<div class="case"><img src="img/02-caso.jpg"><div class="facts">
<div><b>Usuaria</b>Josselyn Toledo — kinesióloga y psicomotricista acuática: Centro Médico InMotion (factura mensual), domicilios en San Fernando y Agua Buena, piscina temperada y gimnasio.</div>
<div><b>Problema (UA1)</b>No sabe cuánto gana de verdad; cuadra ingresos y gastos en Excel de noche (~1 h diaria).</div>
<div><b>Solución (UA2)</b>Copiloto Kine: convierte cada atención en ganancia real y anticipa los meses bajos.</div></div></div>
<h3>Desafío</h3><div class="big-q">{C.DESAFIO}</div>
<h3>Propuesta de valor que llegamos a probar (EV2)</h3><p>{C.PDV_EV2}</p>
<div class="note"><b>Nota de transparencia.</b> Los ciclos 1 y 2 los ejecutó el equipo como usuarios internos —alternativa que el toolkit permite— con scripts
reproducibles (<code>unidad-3/ciclo1</code> y <code>ciclo2</code>). El ciclo 3 es la validación externa con la clienta, Sercotec y docentes (reunión del 12/11), documentada con una
transcripción con minuto. El ciclo 4, con Josselyn y Catalina usando la v3, está planificado y sus resultados se informan como pendientes: no atribuimos opiniones a personas que aún no han participado.</div>'''
    return section('s-intro', '01 · INTRODUCCIÓN', 'Marco', 'Introducción', b)


def links():
    def card(qr, img, t, d, u, c):
        return (f'<div class="pcard {c}"><img class="ph" src="{img}"><div class="tx"><div class="kk">{t}</div><div class="d">{d}</div>'
                f'<div class="qr"><img src="{qr}"><div>Escanea con el celular o haz clic:<br>{lnk(u)}</div></div></div></div>')
    b = (f'<p class="lead">Los dos prototipos están publicados y se abren desde cualquier celular, sin instalar nada. Son la evidencia funcional del informe: cada pantalla citada en las secciones siguientes se puede recorrer en estos enlaces.</p>'
         + card('img/qr-profesional.png', V3 + '01_tablero.png', 'Vista profesional · Josselyn', 'La app de la kinesióloga (prototipo v3): ganancia real y por hora de sus cinco canales, ruta en San Fernando con el costo del tiempo de viaje, agenda desde AgendaPro y la clínica, clase grupal y resumen exportable.', URL_PRO, '')
         + card('img/qr-cliente.png', PAC + '01_recordatorio_a.png', 'Vista cliente · paciente', 'Los mensajes que recibe el paciente (v2, simplificada para personas mayores): recordatorio, voy en camino, pago, clase grupal y hora liberada.', URL_CLI, 'c')
         + f'<p class="small muted">Portada de ambos: {lnk(URL + "/")}. Las versiones v1 y v2 y el código fuente están en el repositorio del proyecto (<code>unidad-3/prototipo</code>). Los prototipos no envían mensajes ni guardan datos fuera del dispositivo.</p>')
    return section('s-links', 'PROTOTIPOS NAVEGABLES', 'Marco', 'Prototipos navegables: vista profesional y vista cliente', b)


def ruta():
    cyc = [('S11 · Prototipar', 'SQA, storyboard y mock-up v1'), ('S11–S12 · Ciclo 1', 'Uso y estética: 11 tareas, WCAG AA, heurísticas'), ('S12 · CDM 1', 'Cualidades, debilidades y mejoras'),
           ('S12–S13 · Iterar v2', 'Metáfora, storyboard y mock-up v2'), ('S13 · Ciclo 2', 'Técnico: 11 pruebas'), ('S13 · Ciclo 3', 'Clienta, Sercotec y docentes (12/11)'), ('S14 · Iterar v3', '12 cambios del ciclo 3'), ('S15 · Ciclo 4', 'Josselyn y Catalina con la v3')]
    ch = '<span class="ar">›</span>'.join(f'<div><b>{t}</b>{d}</div>' for t, d in cyc)
    cr = [('3.1.1', '15', 'Aplica la fase de desarrollo y prototipado del Ciclo de Innovación INACAP', '3.1.1.1 · 3.1.2.1 · 3.1.2.2'),
          ('3.1.2', '20', 'Elabora un prototipo funcional y lo valida con usuarios en más de un ciclo, con enfoque sostenible', 'Ciclos 1 y 2 · ciclo 3 con la clienta · ciclo 4 · sostenibilidad'),
          ('3.1.3', '15', 'Ajusta el prototipo a partir de los resultados del testeo, fundamentando los cambios', 'Dos iteraciones: v2 y v3 · 3.1.2.4 · 3.1.3.1–3.1.3.4'),
          ('3.1.4', '20', 'Analiza el estado del arte y las tendencias en relación con el desafío', '3.1.4.1 · estado del arte · tendencias'),
          ('3.1.5', '30', 'Pertinencia de la propuesta de valor', 'Propuesta iterada · pertinencia')]
    b = f'''<div class="side"><img src="img/03-ciclo.jpg" style="width:62mm;height:34.6mm"><div><p class="lead">El trabajo siguió el calendario S11–S15. Cada ciclo de testeo tuvo un foco distinto: primero que se pueda usar y se vea bien; después, que calcule exacto; luego, que la clienta reconozca su forma real de trabajar; y por último, que la usuaria lo use en su celular.</p></div></div>
<div class="cycle">{ch}</div>
<div class="grid2"><div class="box"><div class="t">Ciclo 1 · funcional y estético</div>¿Puede una kinesióloga hacer su día sin ayuda? ¿Se lee, se toca y se entiende? Tareas, auditoría WCAG 2.1 AA, objetivos táctiles, tipografía y heurísticas de Nielsen.</div>
<div class="box"><div class="t">Ciclo 2 · técnico</div>¿Resuelve con exactitud sus necesidades puntuales? Cálculos, cierre del día, persistencia, costos editables, exportación sin datos clínicos, rendimiento y brechas.</div>
<div class="box"><div class="t">Ciclo 3 · con la clienta</div>¿Calza con su rutina real? Reunión del 12/11 con Josselyn, Sercotec y docentes: 12 hallazgos que originan la v3.</div>
<div class="box"><div class="t">Ciclo 4 · usuarias (planificado)</div>¿Lo usa en su celular y le ayuda a decidir? Josselyn y Catalina con la v3: tareas N1–N10, SUS y precio.</div></div>
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
<p class="small muted">Archivo: <code>unidad-3/prototipo/copiloto-kine-v1.html</code>. La versión iterada (v2) se prueba en {lnk(URL_PRO)}. Las pantallas usan datos de ejemplo de un día tipo de Josselyn (2 atenciones en clínica y 3 a domicilio).</p>'''
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
    arq = f'<div class="arq"><div class="col">{izq}</div><div class="core"><div class="t">COPILOTO KINE · MVP</div><div class="d">App web instalable (PWA) · cálculo de ganancia real · ruta · proyección · sin datos clínicos</div></div><div class="col">{der}</div></div>'
    integ = [[f'<b>{n}</b>', fu, f'<span class="small">{u}</span>', sus(*[x.strip() for x in d.split('·')]), et] for n, fu, u, d, et in C.INTEGRACIONES]
    fn = [[f'<span class="fn {a}">{a}</span>', f, f'<span class="small muted">{r}</span>'] for a, f, r in C.FUNCIONES]
    b = (f'<p class="lead">El ciclo 2 dejó claro que lo que falta no es diseño sino integración con datos reales. Esta es la propuesta técnica para el MVP de la Unidad 4: qué se conecta, qué se agrega y qué se quita.</p>{arq}'
         + table(['Integración', 'Fuente / servicio', 'Para qué', 'Sost.', 'Etapa'], integ, 'tight xs')
         )
    b2 = (table(['Acción', 'Funcionalidad', 'Por qué'], fn, 'tight')
         + f'<img class="banner vec" src="{VEC}17-ruta.png" style="height:40mm">'
         + '<div class="note" style="border-color:var(--accent);background:rgba(255,107,53,.05)"><b>Ejemplo · costo por km con precio real.</b> Costo de combustible por km = precio del litro ÷ rendimiento del auto. Con un rendimiento de 14 km/l, cada $50 que baja el litro reduce el costo en ~$3,6 por km; en los ~400 km de domicilios de un mes son ~$1.430 menos, más el ahorro de los 140 km que evita la ruta sugerida. La app usaría el precio de la bencinera elegida en lugar del valor fijo de $180/km del prototipo.</div>')
    return (section('s-tec', 'PROPUESTA TÉCNICA MVP', 'Testeo · ciclo 2', 'Propuesta técnica del MVP: integraciones', b)
            + section('s-fun', 'PROPUESTA TÉCNICA MVP', 'Testeo · ciclo 2', 'Funcionalidades: agregar, mantener y quitar', b2))


def retro():
    rows = [[f'<b>{c}</b>', f'<b>{t}</b><div class="small muted" style="margin-top:.6mm">{q}</div>', f'<span class="code b">{m}</span>', i] for c, t, q, m, i in C.RETRO_HALLAZGOS]
    b = (f'<div class="side"><img src="img/05-entrevista.jpg" style="width:40mm;height:22.4mm"><p class="small" style="margin:0">{C.RETRO_CONTEXTO} '
         'La transcripción completa, con cada interlocutor identificado, está en <code>retroalimentacion/</code>. Las citas son textuales con el minuto de la grabación.</p></div>'
         + table(['#', 'Hallazgo y cita de la clienta', 'Min.', 'Implicancia para Copiloto Kine'], rows, 'tight xxs'))
    doc = [[f'<b>{w}</b>', t, f'<span class="code b">{m}</span>'] for w, t, m in C.RETRO_DOCENTES]
    pat = [[f'<b>{p}</b>', f'<span class="small muted">{e}</span>', d] for p, e, d in C.RETRO_PATRONES]
    cam = [[f'<b>{i}</b>', c, f'<span class="small muted">{h}</span>', f'<span class="code">{e}</span>'] for i, (c, h, e) in enumerate(C.RETRO_CAMBIOS, 1)]
    b2 = ('<h3 style="margin-top:1mm">Lo que pidieron Sercotec y los docentes</h3>' + table(['Quién', 'Sugerencia', 'Min.'], doc, 'tight xxs')
          + '<h3>Patrones al hilar los hallazgos</h3>' + table(['Patrón', 'Evidencia', 'Qué significa'], pat, 'tight xxs')
          + '<h3>Cambios a la propuesta (prototipo v3)</h3>' + table(['#', 'Cambio', 'Origen', 'Dónde'], cam, 'tight xxs')
          + '<p class="small"><b>Lectura.</b> La clienta valida el núcleo (no existe algo así; ya lo hace a mano cada noche; le importa qué canal le conviene) y corrige dos supuestos: usa AgendaPro y la clínica le paga con factura mensual.</p>')
    return (section('s-retro', 'CICLO 3 · 12/11', 'Testeo · ciclo 3 con la clienta', 'Retroalimentación de la clienta y Sercotec', b)
            + section('s-retro2', 'CICLO 3 · 12/11', 'Testeo · ciclo 3 con la clienta', 'Patrones y cambios a la propuesta', b2))


def retro3():
    gen = [[f'<b>{t}</b>', f'<span class="muted">{e}</span>', i] for t, e, i in C.RETRO_GENERALES]
    otr = [[f'<b>{n}</b><br><span class="code b">{m}</span>', d, r, i] for n, m, d, r, i in C.RETRO_OTRAS]
    b = ('<h3 style="margin-top:1mm">Hallazgos generales de la conversación</h3>' + table(['Hallazgo', 'Evidencia', 'Qué hacemos con esto'], gen, 'tight xxs')
         + '<h3>Las otras propuestas revisadas</h3>' + table(['Propuesta', 'Cómo lo propone', 'Reacción en la reunión', 'Qué tomamos'], otr, 'tight xxs'))
    return section('s-retro3', 'CICLO 3 · 12/11', 'Testeo · ciclo 3 con la clienta', 'Hallazgos generales y otras propuestas', b)


def aplica():
    g = [[f'<b>{h}</b>', p, pr, f'<span class="muted">{v}</span>'] for h, p, pr, v in C.APLICA_GENERALES]
    o = [[f'<b>{n}</b>', f'<span class="muted">{q}</span>', a] for n, q, a in C.APLICA_OTRAS]
    b = ('<p class="small">Cada hallazgo se traduce en una acción en el producto, en la propuesta que se presenta y en una forma de validarlo. Así la retroalimentación no queda como comentario, sino como cambios medibles para el prototipo v3 y la entrega final.</p>'
         + '<h3 style="margin-top:1mm">Hallazgos generales → acciones</h3>' + table(['Hallazgo', 'En el producto', 'En la propuesta y presentación final', 'Cómo lo validamos'], g, 'tight xxs')
         + '<h3>Lo que tomamos de las otras propuestas</h3>' + table(['Fuente', 'Lo que proponen', 'Cómo lo aplicamos (v3 y MVP)'], o, 'tight xxs'))
    return section('s-aplica', 'CICLO 3 · 12/11', 'Testeo · ciclo 3 con la clienta', 'Cómo aplicamos los hallazgos', b)


def recorrido():
    cards = ''.join(f'<div class="sc2"><div class="im"><img src="{img}"><span class="n">{i:02d}</span></div><div class="tx"><div class="h">{t}</div><div class="c v"><b>Mensaje / prototipo</b>{m}</div><div class="c p"><b>Hipótesis</b>{h}</div></div></div>' for i, (img, t, m, h) in enumerate(C.SB_PACIENTE, 1))
    b = (f'<p class="lead">El storyboard del paciente construido en la EV2 —con don Luis, adulto mayor atendido a domicilio, y Camila, estudiante con dolor de espalda— se convierte en el guion del testeo con pacientes: cada escena tiene un mensaje de la vista paciente y una hipótesis que validar.</p><div class="sb2">{cards}</div>'
         + '<p class="small" style="margin-top:3mm"><b>Lectura.</b> Las escenas 2 a 5 ya están prototipadas (mensajes M1 a M4). La reserva en línea (escena 1) depende de la agenda que Josselyn ya usa, y el seguimiento después del alta (escena 6) queda para la fase 2.</p>')
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
         + '<p class="small"><b>Resultado.</b> Con los mismos scripts del ciclo 1, la versión 2 completa 11 de 11 tareas, con 0 errores WCAG AA, 0 objetivos táctiles bajo 44 px y letra mínima de 12 px. Pruébalo: ' + lnk(URL_PRO) + '.</p>')
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
    b = f'''<p class="lead">Para validar con usuarios externos preparamos un kit de testeo (20 páginas) para tres públicos: las <b>kinesiólogas</b>, que usan la app; los
<b>pacientes</b>, que reciben sus mensajes y de quienes depende la ruta; y una <b>contadora</b>, que recibe el resumen mensual.</p>
<div class="pj"><figure><img src="img/storyboard/personajes/joselyn.jpg"><figcaption><b>Josselyn</b>Usuaria principal · kinesióloga</figcaption></figure>
<figure><img src="img/storyboard/personajes/don-luis.jpg"><figcaption><b>Don Luis</b>Paciente · adulto mayor a domicilio</figcaption></figure>
<figure><img src="img/storyboard/personajes/camila.jpg"><figcaption><b>Camila</b>Paciente · estudiante con dolor de espalda</figcaption></figure>
<figure><img src="{VEC}19-pacientes.png" style="object-position:50% 70%"><figcaption><b>Otros perfiles</b>Cuidadora, oficina, turnos y deportista</figcaption></figure></div>
<div class="pfs2">{pf}</div>
<h3>Hipótesis y criterios de éxito</h3>{table(['#', 'Público', 'Hipótesis', 'Éxito si…', 'Resultado'], hip, 'tight xxs')}
'''
    b2 = f'''<p class="lead">Las kinesiólogas usan la app; los pacientes solo reciben sus mensajes. La <b>versión actual</b> de la vista paciente simula cuatro mensajes de WhatsApp. Tras la reunión del 12/11 se itera a una versión simplificada para personas mayores (página siguiente).</p>
{phones([(PAC1 + '01_recordatorio.png', 'v1 · M1 Recordatorio'), (PAC1 + '02_voy_en_camino.png', 'v1 · M2 Voy en camino'), (PAC1 + '03_comprobante.png', 'v1 · M3 Comprobante'), (PAC1 + '04_hora_liberada.png', 'v1 · M4 Hora liberada')]).replace('class="phones"', 'class="phones big"')}
<p class="small">La hipótesis más riesgosa del modelo es H5: si los pacientes no aceptan una ventana de llegada de 30 minutos, la ruta sugerida no se puede aplicar. Por eso los pacientes son parte del testeo aunque no usen la app. Los mensajes no incluyen diagnósticos (Ley 21.719), la vista tiene “Letra grande” para adultos mayores y sus cuatro pantallas pasan la auditoría WCAG AA sin errores. Versión actualizada en ' + lnk(URL_CLI) + '.</p>
<div class="note"><b>Estado y siguientes pasos.</b> La retroalimentación de la reunión del 12 de noviembre ya está integrada (sección anterior); con ella se ajustan el guion y el prototipo v3 antes de las sesiones. Los pacientes de Josselyn participan solo si ella los invita; se complementa con personas del entorno del equipo que calcen con cada perfil.</div>
<h3>Contenido del kit de testeo</h3>
{table(['Documento', 'Para qué sirve'], [['Plan e hipótesis', '11 hipótesis con métrica y criterio de éxito definidos antes de testear'], ['Perfiles', '9 perfiles con criterios de reclutamiento y adaptaciones'],
        ['Guiones A, B y C', 'Kinesiólogas (40–60 min), pacientes (15 min) y contadora (20 min)'], ['Consentimiento informado', 'Participación voluntaria, sin datos de salud (Ley 21.719)'],
        ['Pautas y cuestionarios', 'Observación de tareas, encuesta de pacientes y escala SUS'], ['Matriz de consolidación', 'Regla de decisión por hipótesis: mantener, iterar o descartar']], 'tight')}'''
    pr = [[f'<b>{a}</b>', f'<span class="muted">{v1}</span>', v2] for a, v1, v2 in C.PAC_PRINCIPIOS]
    hz = [[f'<b>{h}</b>', c] for h, c in C.PAC_HALLAZGOS]
    b3 = (f'''<p class="small">Muchos pacientes de Josselyn son personas mayores atendidas a domicilio, como don Luis. La v2 simplifica el flujo y los componentes: cada mensaje pide una sola decisión, con letra y botones grandes, la hora exacta y ayuda siempre a mano. Además incorpora los hallazgos del 12/11.</p>
{phones([(PAC + '01_recordatorio_a.png', 'M1 · Recordatorio'), (PAC + '02_voy_en_camino_a.png', 'M2 · Voy en camino'), (PAC + '03_pago_comprobante_a.png', 'M3 · Pago y comprobante'), (PAC + '04_clase_grupal_a.png', 'M4 · Clase grupal'), (PAC + '05_hora_liberada_a.png', 'M5 · Hora liberada')]).replace('class="phones"', 'class="phones s6"')}'''
          + table(['Componente', 'Versión actual (v1)', 'Versión simplificada (v2)'], pr, 'tight xxs')
          + '<h3>Hallazgos que se ven en el lado del paciente</h3>' + table(['Hallazgo', 'Cómo se refleja en los mensajes'], hz, 'tight xxs')
          + '<p class="small"><b>Verificación.</b> Las cinco pantallas pasan WCAG 2.1 AA sin errores, todos los botones miden 56 px o más y la letra mínima es de 14 px. Pruébalo: ' + lnk(URL_CLI) + ' (v1 en el repositorio: <code>vista-paciente-v1.html</code>).</p>')
    return (section('s-val', 'VALIDACIÓN CON USUARIOS', 'Validación y propuesta de valor', 'Validación con usuarios externos', b)
            + section('s-vp', 'VISTA PACIENTE', 'Validación y propuesta de valor', 'Vista paciente · versión actual', b2)
            + section('s-vp2', 'VISTA PACIENTE', 'Validación y propuesta de valor', 'Vista paciente v2: simple para personas mayores', b3))


def pagina_pv():
    return f'''<div class="full dark solid"><img class="phone" src="{V3}02_ganancia_por_hora.png" style="width:66mm;right:16mm;bottom:30mm;border-radius:8mm;border:2.5mm solid #1E1A30">
<div class="in" style="top:36mm"><div class="kick" style="color:#FF6B35">Propuesta de valor iterada (v3) · 3.1.5</div>
<div class="big">EL COPILOTO<br>DE SU <em>TERRENO</em>.</div>
<div class="pv">Toma sus agendas, ordena su ruta y convierte cada atención —en clínica, a domicilio, en piscina o en el gimnasio— en <b>ganancia real y por hora</b>, contando también <b>el tiempo de viaje</b>.</div>
<div class="tags"><span>Anticipador</span><span>Claro</span><span>Conectado y corregible</span><span>Justo con su tiempo</span></div></div>
<div class="foot"><span>Propuesta de valor iterada</span><span>Semana 14</span></div></div>'''


def pv():
    b = f'''<div class="grid2"><div class="box"><div class="t" style="color:var(--page-text2)">Antes · EV2</div><div style="font-size:10pt;font-weight:600;line-height:1.42">{C.PDV_EV2}</div></div>
<div class="box"><div class="t" style="color:var(--page-text2)">Iteración v2 · ciclos 1 y 2</div><div style="font-size:10pt;font-weight:600;line-height:1.42">{C.PDV_ITER}</div></div></div>
<div class="box" style="border-color:var(--accent);margin-top:3mm"><div class="t">Versión 3 · ciclo 3 con la clienta</div><div style="font-size:10.5pt;font-weight:600;line-height:1.42">{C.PDV_V3}</div></div>
<h3>Qué cambió de la v2 a la v3 y por qué</h3>
{table(['Cambio', 'Evidencia que lo respalda'], [
        ['<b>“Toma las citas de AgendaPro y de la clínica”</b>', 'RF3: usa AgendaPro y una agenda médica; Google Calendar queda como alternativa.'],
        ['<b>“En clínica, a domicilio, en piscina o en el gimnasio”</b>', 'RF7: es psicomotricista acuática y hace entrenamiento personalizado.'],
        ['<b>“Ganancia por hora… contando el tiempo de viaje”</b>', 'RF5 y RF6: quiere saber qué canal rinde más; Agua Buena le toma 25–30 min (Ariel: la hora hombre es un costo oculto).'],
        ['<b>“Cobre lo justo por cada tramo”</b>', 'RF6 y RF9: caminos de precordillera y un mercado que no valora lo especializado.'],
        ['<b>“Sin anotar nada de noche”</b>', 'RF2: hoy anota todo cada noche en el teléfono.']], 'tight')}
<h3>Qué cambió de la EV2 a la v2</h3>
{table(['Cambio', 'Evidencia que lo respalda'], [
        ['<b>La ruta pasa al centro</b> (“ordena su ruta de domicilios”)', 'Ciclo 1: la ruta fue la vista con más valor percibido; ciclo 2: 7 km menos por día (P8).'],
        ['<b>Sale “se conecta a la agenda que ya usa”</b>', 'Ciclo 2: la integración es simulada (R2, brecha B1). No prometemos lo que el MVP aún no cumple.'],
        ['<b>Entra “entrega sus números a la contadora sin Excel”</b>', 'Ciclo 2: exportación verificada sin diagnósticos ni nombres (P6) y retención configurable (P11).'],
        ['<b>“Ya descontados”</b> en vez de “descontando”', 'Ciclo 2: cálculo exacto en 5 de 5 atenciones (P1); el usuario no hace la cuenta.']], 'tight')}
<h3>Métricas claves para la Unidad 4</h3>
{table(['Métrica', 'Hoy (prototipo)', 'Meta MVP'], [['Tiempo de cierre del día', 'Resumen en 16 toques para 7 atenciones (N10)', '< 30 min/día real (desafío)'], ['Usabilidad (SUS)', 'Por medir en el ciclo 4', '≥ 75'], ['Decisiones tomadas con la ganancia por hora', 'Por medir en el ciclo 4', '≥ 1 decisión concreta por usuaria'],
        ['Pacientes que aceptan la ventana de llegada', 'Por medir (H5)', '≥ 70 %'], ['Km ahorrados por día con domicilios', '7 km (día de ejemplo)', 'Medido con rutas reales']], 'tight')}'''
    return section('s-pv', '3.1.5 · PROPUESTA DE VALOR', 'Validación y propuesta de valor', 'Propuesta de valor iterada: EV2 → v2 → v3', b, '3.1.5')


# ================================================================ ciclo 3 e iteración v3
def f3():
    b = card([('Instrumento', '3.1.2.3 Ficha de planificación del testeo'), ('Foco', 'Validación externa'), ('Prototipo', 'v2 y propuesta (carpeta “Grupo2”)'), ('Plantilla', 'Anexo A')])
    b += f'<div class="side"><img src="img/05-entrevista.jpg" style="width:58mm;height:32.4mm"><div class="big-q" style="font-size:10.5pt;margin:0">{C.FICHA_C3["objetivo"]}</div></div>' + ficha_tbl(C.FICHA_C3)
    b += ('<p class="small"><b>Por qué cuenta como ciclo de testeo.</b> Es la primera vez que la propuesta y el prototipo se enfrentan a la clienta real y a actores del ecosistema '
          '(Sercotec y docentes), con preguntas abiertas y comparación con otras tres propuestas. El procesamiento es reproducible: transcripción con minuto, '
          'codificación de 12 hallazgos (RF1–RF12), patrones y matriz CDM. Sus resultados están en las páginas siguientes.</p>')
    return section('s-f3', '3.1.2.3 · FICHA CICLO 3', 'Testeo · ciclo 3 con la clienta', 'Ficha de planificación del testeo · ciclo 3', b, '3.1.2.3')


def comp():
    dot = {2: '<span class="dot d2">●</span>', 1: '<span class="dot d1">◐</span>', 0: '<span class="dot d0">○</span>'}
    rows = [[('<b>' + n + '</b>') if 'Copiloto' in n else n] + [dot[v] for v in vs] + [f'<span class="small">{c}</span>'] for n, vs, c in C.COMPARA]
    b = ('<p class="lead">Mabel lo dijo al cierre: “las propuestas pueden ser muy similares porque todos identificaron el tema de los ingresos” (38:45). La diferencia está en cómo resuelve cada una. Esta matriz compara las cuatro propuestas revisadas el 12/11 según lo que mostraron en pantalla.</p>'
         + table(['Propuesta'] + C.COMPARA_CRIT + ['Costo para ella'], rows, 'mat tight xs')
         + f'<p class="small muted">{C.COMPARA_NOTA}</p>'
         + '<h3>Lectura</h3><p class="small">Las dos propuestas en Excel cubren bien la exportación y el análisis por tipo de cliente, pero dependen de que Josselyn digite todo. El modelo grupal aporta lo que ninguna app tiene: una nueva fuente de ingreso para los meses bajos. Copiloto Kine es la única que parte de la agenda, cuenta el tiempo de viaje y piensa en el paciente; por eso en la v3 incorporamos la exportación a planilla y la clase grupal, en lugar de competir con ellas.</p>')
    return section('s-comp', 'CICLO 3 · COMPARATIVA', 'Testeo · ciclo 3 con la clienta', 'Las 4 propuestas frente a frente', b, '3.1.4')


def cdm3():
    b = card([('Instrumento', '3.1.2.4 Matriz CDM con propuesta de valor'), ('Fuente', 'Transcripción 12/11 · RF1–RF12'), ('Prototipo', 'v2'), ('Plantilla', 'Anexo A')])
    b += cdm(C.CDM_C3)
    b += ('<h3>Análisis y conclusiones</h3><p>La clienta valida el núcleo —“eso hago yo igual en el teléfono… simplemente no tengo esa aplicación”— y, al mismo tiempo, desarma cuatro supuestos del prototipo: '
          'no usa Google Calendar sino AgendaPro; la clínica no le paga por atención sino con una factura mensual; no trabaja en dos lugares sino en cuatro; y en su territorio el traslado cuesta más en tiempo que en bencina. '
          'La pregunta de fondo cambia de “cuánto gané” a “qué me conviene”. Esa es la base de la versión 3.</p>')
    return section('s-cdm3', '3.1.2.4 · CDM CICLO 3', 'Testeo · ciclo 3 con la clienta', 'Matriz CDM del ciclo 3', b, '3.1.2.4')


def pagina_cifras_v3():
    return f"""<div class="full dark"><div class="in" style="top:40mm"><div class="kick" style="color:#FF6B35">Del ciclo 3 a la versión 3</div>
<div class="big">2 CANALES <em>→ 5 CANALES</em>.</div>
<div class="lead2">La v3 trabaja como ella: clínica con factura mensual, domicilio, piscina, gimnasio y clase grupal, en San Fernando y sus caminos rurales.</div>
<div class="ncards"><div><div class="n">12</div><div class="t">Cambios en v3</div><div class="d">Cada uno trazado a un hallazgo de la clienta (RF1–RF12) o de Sercotec y los docentes.</div></div>
<div><div class="n">{C.V3_OK}/{len(C.V3_TASKS)}</div><div class="t">Tareas completadas</div><div class="d">11 tareas base (regresión) y 10 nuevas, una por cambio.</div></div>
<div><div class="n">{C.V3_AXE}</div><div class="t">Errores WCAG AA</div><div class="d">Cálculos idénticos a la referencia en {C.V3_CALC_OK} de {len(C.R3["calculos"])} casos.</div></div></div></div>
<div class="foot"><span>Iteración del prototipo</span><span>Versión 3</span></div></div>"""


def iter3():
    rows = [[f'<span class="code">{c}</span><br><b>{n}</b>', f'<span class="vv a">Versión 2</span><br>{a}', f'<span class="vv b">Versión 3</span><br>{b_}', f'<span class="small muted">{h}</span>'] for c, n, a, b_, h in C.ITER_DOCS_V3]
    b = (f'<div class="side"><img src="{VEC}18-iteracion.png" style="width:56mm;height:31.3mm;object-fit:contain;background:#F4F2FC"><p class="lead" style="margin:0">El manual pide que en la iteración se ajusten <b>la metáfora, los atributos y los prototipos</b>, dando paso a nuevos testeos. Esta segunda iteración parte de la matriz CDM del ciclo 3 —la primera con la clienta real— y vuelve a pasar por los cuatro instrumentos 3.1.3.</p></div>'
         + table(['Instrumento', 'Versión 2', 'Versión 3', 'Hallazgo que la motiva'], rows, 'tight')
         + '<p class="small">Las plantillas oficiales de la v3 (storyboard iterado y ficha del ciclo 4) y del ciclo 3 (ficha y CDM) están en el Anexo A.</p>')
    return section('s-iter3', 'ITERACIÓN V3', 'Iteración · versión 3', 'De la versión 2 a la versión 3', b)


def meta3():
    M = C.METAFORA_V3
    at = ''.join(f'<div class="attr"><div class="n">{n}</div><div class="s">…{s}</div>{sus(*tags)}<div class="r"><b>Ajuste según el ciclo 3</b>{r}</div></div>' for n, s, r, tags in M['atributos'])
    b = f"""{card([('Instrumento', '3.1.3.1 Panel de metáforas y atributos iterado'), ('Fuente', 'Matriz CDM del ciclo 3'), ('Cambio', 'Metáfora, 2 atributos ajustados y 1 nuevo')])}
<div class="grid2"><div class="met" style="background:#F4F3F8;color:var(--page-text2)"><div class="k" style="color:var(--page-text2)">Antes · v2</div><div class="m" style="color:var(--page-text2)">{M["antes"]}</div></div>
<div class="met"><div class="k">Después · v3</div><div class="m">{M["despues"]}</div></div></div>
<p><b>Fundamento.</b> {M["porque"]}</p>
<div class="grid2" style="flex-wrap:wrap">{at}</div>"""
    return section('s-meta3', '3.1.3.1 · METÁFORA V3', 'Iteración · versión 3', 'Panel de metáforas y atributos (v3)', b, '3.1.3.1')


def sb3():
    b = card([('Instrumento', '3.1.3.2 Storyboard iterado'), ('Insumo', 'Matriz CDM del ciclo 3'), ('Formato', 'Escenas con capturas del prototipo v3'), ('Plantilla', 'Anexo A')])
    b += f'<div class="big-q" style="font-size:10pt">{C.PDV_V3}</div>' + scenes(C.SCENES_V3, it=True).replace('class="sb2"', 'class="sb2 ph"')
    b += '<p class="small" style="margin-top:3mm"><b>Qué cambió en la secuencia.</b> El día ya no transcurre entre Rancagua y Machalí con clínica y domicilio: empieza en InMotion, sube a Agua Buena, pasa por la piscina temperada y termina en el gimnasio. Cada escena muestra la cualidad que se conserva y la mejora que trajo el ciclo 3.</p>'
    return section('s-sb3', '3.1.3.2 · STORYBOARD V3', 'Iteración · versión 3', 'Storyboard iterado (v3)', b, '3.1.3.2')


def mk3():
    ba = ''.join(f'<div><div class="ba"><img src="{a}"><span class="arr">→</span><img src="{c}"></div><div class="lbl">{t} · v2 → v3</div></div>' for a, c, t, _ in C.MOCK_V2V3[:3])
    rows = [[f'<b>{i}</b>', c, h, r, f'<span class="{"ok" if e.startswith("Funcional") else "pa"}">{e}</span>'] for i, (c, h, r, _, e) in enumerate(C.CAMBIOS_V3, 1)]
    b = (f'<div style="display:flex;justify-content:space-between">{ba}</div>'
         + table(['#', 'Cambio en v3', 'Hallazgo', 'Req. / atributo', 'Estado'], rows, 'tight xs')
         + '<p class="small"><b>Fundamento.</b> Ningún cambio sale de una preferencia del equipo: todos responden a una cita de la clienta o a una sugerencia de Sercotec y los docentes (columna “Hallazgo”). La agenda queda simulada porque la conexión real con AgendaPro es parte del MVP. Pruébalo: ' + lnk(URL_PRO) + '.</p>')
    b2 = (phones([(V3 + '04_paradas_tramos.png', 'Ruta · tramos'), (V3 + '09_clinica_factura.png', 'Clínica · factura'), (V3 + '10_servicios.png', 'Servicios'), (V3 + '07_clase_grupal.png', 'Clase grupal'), (V3 + '08_resumen_canal.png', 'Resumen por canal'), (V3 + '11_cierre_dia.png', 'Cierre del día')]).replace('class="phones"', 'class="phones s6"')
          + table(['Pantalla', 'Qué materializa', 'Atributo'], [
              ['<b>Ruta · tramos</b>', 'Cada parada muestra km, minutos, costo en bencina y valor del tiempo; tarifa sugerida por tramo urbano, rural y precordillera.', 'Justo con su tiempo'],
              ['<b>Clínica · factura</b>', 'Elige si la clínica le paga por atención (70/30) o con un monto fijo mensual; la sesión se registra igual para contarla.', 'Conectado y corregible'],
              ['<b>Servicios</b>', 'Valor y costo propio de domicilio, piscina (arriendo), gimnasio (insumos), grupal (sala) y clínica.', 'Claro'],
              ['<b>Clase grupal</b>', 'Inscritos, cobro por persona, ganancia del mes y desde cuántas personas rinde más que un domicilio.', 'Anticipador'],
              ['<b>Resumen por canal</b>', 'Semana y mes: atenciones, ganancia y ganancia por hora; descarga para Excel o Google Sheets.', 'Claro'],
              ['<b>Cierre del día</b>', 'Atenciones, inasistencias, km, tiempo de viaje y pagos pendientes: reemplaza la nota nocturna.', 'Conectado y corregible']], 'tight xs'))
    return (section('s-mk3', '3.1.3.3 · MOCK-UP V3', 'Iteración · versión 3', 'Mock-up iterado (v3) y ajustes fundamentados', b, '3.1.3.3')
            + section('s-mk3b', '3.1.3.3 · MOCK-UP V3', 'Iteración · versión 3', 'Lo nuevo de la v3, pantalla por pantalla', b2, '3.1.3.3'))


def ver3():
    t = C.V3_TASKS
    rows = [[f'<b>{x["id"]}</b>', f'<span class="small muted">{x["origen"]}</span>', x['name'], f'<span class="{"ok" if x["ok"] else "ko"}">{"✔" if x["ok"] else "✖"}</span>', x['taps'], f'<span class="small">{fix(x["obs"])}</span>'] for x in t]
    calc = [[f'<b>{c["id"]}</b>', f'${c["net_app"]:,}'.replace(',', '.'), f'${c["net_ref"]:,}'.replace(',', '.'), (f'${c["perh_app"]:,}/h'.replace(',', '.') if 'perh_app' in c else '—'), (f'${c["viaje_app"]:,}'.replace(',', '.') if 'viaje_app' in c else '—'), '<span class="ok">✔</span>' if c['ok'] else '<span class="ko">✖</span>'] for c in C.R3['calculos']]
    base = sum(x['ok'] for x in t if x['id'].startswith('T')); nuevas = [x for x in t if x['id'].startswith('N')]
    b = (kpis([(f'{base}/11', 'tareas base: lo de v1 y v2 sigue funcionando'), (f'{sum(x["ok"] for x in nuevas)}/{len(nuevas)}', 'tareas nuevas, una por cambio del ciclo 3'), (f'{C.V3_CALC_OK}/{len(C.R3["calculos"])}', 'cálculos idénticos a la referencia'), (f'{C.V3_AXE} · {C.V3_TARGETS}', 'errores WCAG AA · botones bajo 44 px')])
         + f'<p class="small"><b>Regresión (T1–T11).</b> Las 11 tareas de los ciclos 1 y 2 se repiten sobre la v3 y pasan todas: ganancia del mes visible sin tocar nada, registro en 2 toques, deshacer, inasistencia, ruta y aviso, comparación de rutas, proyección, impuestos, costos editables y exportación.</p>'
         + '<h3>Tareas nuevas · una por cambio del ciclo 3</h3>'
         + table(['#', 'Origen', 'Tarea', 'OK', 'Toques', 'Evidencia'], [r for r in rows if r[0].startswith('<b>N')], 'tight xxs')
         + '<h3>Cálculos contra la referencia</h3>' + table(['Atención', 'Ganancia app', 'Referencia', 'Por hora', 'Valor del viaje', 'OK'], calc, 'tight xs')
         + '<p class="small"><b>Referencia.</b> Ganancia = valor − km × $180 − costo del servicio − valor × 15,25 %; por hora = ganancia ÷ (duración + minutos de viaje); valor del viaje = minutos ÷ 60 × $15.000. Script reproducible: <code>iteracion-v3/verificar_v3.js</code>. '
           'Es una verificación interna antes de llevar la v3 a la usuaria: confirma que nada se rompió y que lo nuevo calcula bien, pero no reemplaza el ciclo 4.</p>')
    return section('s-ver3', 'VERIFICACIÓN V3', 'Iteración · versión 3', 'Verificación del prototipo v3', b)


def f4():
    b = card([('Instrumento', '3.1.3.4 Ficha de planificación del testeo de la iteración'), ('Foco', 'Uso real y decisión'), ('Prototipo', 'v3 en el celular de la usuaria'), ('Plantilla', 'Anexo A')])
    b += f'<div class="side"><img src="img/07-oficina-movil.jpg" style="width:58mm;height:32.4mm"><div class="big-q" style="font-size:10pt;margin:0">{C.FICHA_C4["objetivo"]}</div></div>' + ficha_tbl(C.FICHA_C4)
    b += ('<p class="small"><b>Qué cambia respecto del ciclo 2.</b> El ciclo 2 fue técnico e interno; el ciclo 4 es con la usuaria real y una par, en su propio celular, con las tareas nuevas N1–N10, '
          'una pregunta de decisión (¿qué haría distinto con la ganancia por hora?), la escala SUS y la disposición a pagar. Se suma al guion A del kit de testeo. '
          'Resultados <span class="pend">pendientes de sesión</span>.</p>')
    return section('s-f4', '3.1.3.4 · FICHA CICLO 4', 'Iteración · versión 3', 'Ficha del testeo de la iteración · ciclo 4', b, '3.1.3.4')


def cost():
    d = [[f'<b>{a}</b>', b_, c, f'<span class="small muted">{e}</span>'] for a, b_, c, e in C.COSTEO_DESARROLLO]
    o = [[f'<b>{a}</b>', b_, c, f'<b>{e}</b>'] for a, b_, c, e in C.COSTEO_OPERACION]
    k = [[f'<b>{a}</b>', b_, c] for a, b_, c in C.COSTEO_COMPARA]
    b = ('<p class="lead">Mabel pidió que “se pueda identificar más o menos cuánto saldría” (12:30) y el profesor, que fuera “de muy bajo costo… plataformas liberadas” (12:52). Este es el costeo del MVP con valores de referencia de noviembre de 2026.</p>'
         + '<h3>Desarrollo</h3>' + table(['Ítem', 'Qué incluye', 'Costo', 'Nota'], d, 'tight')
         + '<h3>Operación mensual</h3>' + table(['Etapa', 'Servicios', 'Costo', 'Precio a la usuaria'], o, 'tight')
         + '<h3>Frente a sus alternativas</h3>' + table(['Opción', 'Costo directo', 'Costo real'], k, 'tight')
         + '<p class="small"><b>Decisión de precio.</b> La EV2 usaba $20–25 mil al mes como referencia del mercado. El ciclo 3 mostró que la solución debe ser de bajo costo (Ariel) y que en la región lo especializado se valora poco (RF9). Proponemos un piloto gratis de 3 meses y $9.990 al mes después: con 5 usuarias se cubre la operación comercial. Es una hipótesis (H4) que se valida en el ciclo 4. Precios de lista de Vercel, Supabase y NIC Chile a $950 por dólar.</p>')
    return section('s-cost', 'COSTEO', 'Iteración · versión 3', 'Costeo de la solución', b, '3.1.5')


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
         + '<p class="small muted">● cubre · ◐ parcial · ○ no cubre. Antecedentes revisados en la UA1 en sus sitios oficiales. Copiloto Kine se evalúa por lo que hace hoy: agenda y ruta simuladas = ◐. La v3 suma la ganancia por hora por canal (ciclo 3).</p>'
         + '<h3>Tendencias de la especialidad</h3>' + table(['Tendencia', 'Qué está pasando', 'Cómo responde Copiloto Kine'], tr, 'tight xs')
         )
    return section('s-arte', '3.1.4 · ESTADO DEL ARTE', 'Estado del arte y pertinencia', 'Estado del arte y tendencias', b, '3.1.4')


def pert():
    rows = [[f'<b>{a}</b>', b_, c] for a, b_, c in C.PERTINENCIA_V3]
    b = (table(['Dimensión', 'Lo que sabemos', 'Cómo responde la propuesta iterada'], rows, 'tight')
         + '<div class="big-q" style="font-size:12pt">La propuesta es pertinente porque nace de la rutina real de la clienta (ciclo 3), se diferencia del estado del arte y de las otras tres propuestas, y es viable con un piloto casi sin costo. Quedan tres decisiones para el ciclo 4: precio, tarifa por tramo y alcance del módulo grupal.</div>'
         + '<img class="banner" src="img/02-caso.jpg">')
    return section('s-pert', '3.1.5 · PERTINENCIA', 'Estado del arte y pertinencia', 'Pertinencia de la propuesta de valor', b, '3.1.5')


def sost():
    b = f'''<img class="banner vec" src="{VEC}21-sostenible.png">
<div class="grid3"><div class="box"><div class="t">Económico {sus('Ec')}</div><div style="font-family:var(--fd);font-size:22pt;color:var(--accent)">+$570.000</div>
Ganancia por hora por canal, tarifa por tramo y clase grupal con punto de equilibrio para los meses bajos. Retención configurable ante el alza de la Ley 21.133 (15,25 % → 16 % → 17 %).</div>
<div class="box"><div class="t">Social {sus('So')}</div><div style="font-family:var(--fd);font-size:22pt;color:var(--accent)">~1 h → 1 min</div>
Cierre del día con resumen, sin anotar de noche (RF2). Tiempo de viaje valorado: su hora profesional deja de ser invisible. Accesibilidad WCAG AA, letra grande para adultos mayores y datos de salud fuera del sistema (Ley 21.719).</div>
<div class="box"><div class="t">Ambiental {sus('Am')}</div><div style="font-family:var(--fd);font-size:22pt;color:var(--accent)">−140 km/mes</div>
Ruta sugerida: 20 vs. 27 km en el día de ejemplo (−26 %). Con 20 días de domicilios: ~10 l de bencina y ~23 kg de CO2 menos (estimación del equipo: 14 km/l, 2,3 kg CO2/l).</div></div>
<h3>Sostenibilidad en el prototipo, no solo en el discurso</h3>
{table(['Decisión de diseño', 'Dimensión', 'Evidencia'], [['Registro de un toque y corrección inmediata', sus('So', 'Ec'), 'T2, T4, T10 · P3, P4, P7'], ['Ruta agrupada por sector', sus('Am', 'Ec'), 'P8: −7 km y $1.260 por día'],
        ['Colchón y acciones para meses bajos', sus('Ec'), 'T7: brecha de $770.000 → $530.000 con una acción'], ['Exportación sin datos clínicos', sus('So'), 'P6'], ['Prototipo liviano (39 KB)', sus('Am', 'So'), 'P9: funciona con datos móviles']], 'tight')}'''
    return section('s-sost', 'SOSTENIBILIDAD', 'Cierre', 'Enfoque sostenible', b)


def gest():
    w = C.GANTT_W3
    rows = ''.join(f'<tr><td>{t}</td>' + ''.join(f'<td class="{m.get(x, "")}">{"◆" if m.get(x) == "hito" else ""}</td>' for x in w) + '</tr>' for t, m in C.GANTT_V3)
    roles = [['Claudia Cifuentes', 'Moderación de sesiones de testeo'], ['Néstor Rivera', 'Prototipo y ejecución de tareas'], ['Francisco Ahumada', 'Registro de observaciones y matrices CDM'], ['Benjamín Vera Yáñez', 'Secretario técnico: consolidación, auditoría técnica y bitácora']]
    b = (f'<table class="gantt"><thead><tr><th>Actividad</th>{"".join(f"<th>{x}</th>" for x in w)}</tr></thead><tbody>{rows}</tbody></table>'
         + '<h3>Roles</h3>' + table(['Integrante', 'Rol'], roles, 'tight')
         + '<h3>Bitácora y evidencias</h3>' + ul(['Bitácora de avance U3 (versión S13) completa con los seis indicadores: <code>entregas/Bitacora_avance_U3_EV3.xlsx</code>.',
                                                  'Prototipos publicados: vista profesional ' + lnk(URL_PRO) + ' y vista cliente ' + lnk(URL_CLI) + '; código y versiones v1 en <code>prototipo/</code>.',
                                                  'Ciclos: scripts y resultados JSON en <code>ciclo1/</code>, <code>ciclo2/</code> e <code>iteracion-v3/</code>; transcripción del ciclo 3 en <code>retroalimentacion/</code>; kit de testeo en <code>testeo/</code>.'])
         + '<p class="small"><b>Aprendizaje de gestión.</b> Las sesiones con usuarias externas deben agendarse desde la primera semana de la unidad. La reunión del 12/11 mostró que una sola conversación con la clienta cambia más el producto que dos ciclos internos: el ciclo 4 se agenda apenas se publique la v3.</p>')
    return section('s-gest', 'GESTIÓN', 'Cierre', 'Gestión de la fase y bitácora', b)


def concl():
    b = '''<div class="grid3"><div class="box"><div class="t">Aprendimos</div><ul><li>Medir tareas, accesibilidad y exactitud da evidencia más útil que preguntar si “gusta”.</li><li>“Automático” sin “corregible” genera registros falsos.</li><li>La ruta es tan valiosa como el tablero: la metáfora se movió al copiloto.</li><li>La clienta cambió la pregunta: no “cuánto gané” sino “qué me conviene”.</li></ul></div>
<div class="box"><div class="t">Logramos</div><ul><li>Tres versiones del prototipo y tres ciclos aplicados; el tercero con la clienta real.</li><li>v3 navegable: 21/21 tareas, cálculos exactos y 0 errores WCAG AA.</li><li>12 cambios de la v3 trazados a lo que dijo la clienta.</li><li>Costeo: piloto ≈ $900/mes y precio de $9.990 a validar.</li></ul></div>
<div class="box"><div class="t">Sigue</div><ul><li>Ciclo 4: Josselyn y Catalina con la v3 en su celular (N1–N10, SUS y precio).</li><li>Sesiones con pacientes y contadora del kit de testeo.</li><li>CDM del ciclo 4: precio, tramos y módulo grupal.</li><li>UA4: MVP con la exportación de AgendaPro, respaldo en la nube y aviso por WhatsApp.</li></ul></div></div>
<h3>Conclusión</h3><p>La Unidad 3 convirtió una propuesta de valor en un prototipo que se puede usar, medir y corregir. Testear en dos ciclos con focos distintos permitió arreglar primero la experiencia y después verificar que la herramienta resuelve con exactitud las necesidades puntuales de la kinesióloga. La reunión con la clienta, Sercotec y los docentes fue el ciclo que más cambió el producto: la v3 deja de ser una app de una kinesióloga genérica y pasa a trabajar como Josselyn —cuatro lugares, factura mensual, caminos de precordillera— y responde la pregunta que ella hizo: qué le conviene. El siguiente paso es ponerla en sus manos.</p>
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
         'Equipo del proyecto. (2026). Informes EV1 y EV2 y entrevistas a Josselyn Toledo y Catalina (UA1). INACAP Rancagua.',
         'Equipo del proyecto. (2026). <i>Transcripción de la reunión de retroalimentación con Josselyn Toledo, Sercotec y docentes INACAP, 12 de noviembre de 2026</i>.',
         'Vercel, Supabase, NIC Chile y Comisión Nacional de Energía. (2026). Precios de lista y condiciones de uso de sus servicios [Sitios web oficiales].']
    return section('s-ref', 'REFERENCIAS', 'Fuentes', 'Referencias', ''.join(f'<p class="small" style="padding-left:6mm;text-indent:-6mm">{x}</p>' for x in r))


def pagina_anexo(titles):
    li = ''.join(f'<div style="border-bottom:1px solid #2A2640;padding:2mm 0;font-size:9.5pt;color:#E9E6F7">{t}</div>' for t in titles)
    return f'''<div class="full dark"><div class="in" style="top:34mm"><div class="kick" style="color:#FF6B35">Anexo A</div>
<div class="big">TOOLKIT UA3<br><em>COMPLETO</em>.</div>
<div class="lead2">Las plantillas oficiales de Innovación y Emprendimiento III, llenas con el trabajo del equipo. Cada instrumento conserva su código y su formato original.</div>
<div style="margin-top:8mm;max-width:150mm">{li}</div></div>
<div class="foot"><span>Plantillas oficiales del toolkit</span><span>Ciclos 1 a 4</span></div></div>'''


def pagina_cierre():
    return '''<div class="full sunset"><img src="img/15-horizonte.jpg">
<div class="in" style="top:30mm"><div class="kick" style="color:#FFD9C7">Conclusión</div>
<div class="big" style="font-size:38pt">PROBAR CON EVIDENCIA, ITERAR CON CRITERIO Y <em style="color:#FFD9C7">LLEVARLO A LAS PERSONAS</em>.</div>
<div class="lead2" style="color:#F3E6FF">Copiloto Kine v3 ya trabaja como Josselyn; el ciclo 4 lo pone en sus manos y la Unidad 4 lo convierte en MVP.</div></div>
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
.lk{color:#C2410C;font-weight:700;text-decoration:underline;word-break:break-all}
.pcard{display:flex;gap:5mm;border:1px solid var(--page-border);border-left:4px solid var(--accent);border-radius:8px;padding:4mm;margin:3mm 0 4mm;break-inside:avoid;background:#fff}
.pcard.c{border-left-color:var(--h6)}
.pcard .ph{width:33mm;height:70mm;object-fit:cover;object-position:top;border-radius:6px;border:1px solid var(--page-border);flex:none}
.pcard .kk{font-family:var(--fd);font-size:20pt;line-height:1;letter-spacing:.02em}.pcard .d{font-size:9pt;margin:2mm 0 4mm;color:var(--page-text2)}
.pcard .qr{display:flex;gap:4mm;align-items:center;font-size:9pt}.pcard .qr img{width:30mm;height:30mm;border:1px solid var(--page-border);border-radius:4px}
.cover .url{margin-top:4mm;font-family:var(--fm);font-size:7.5pt;letter-spacing:.06em}.cover .url a{color:#FF8A4C;text-decoration:none}
.banner.vec{height:46mm;object-fit:contain;background:#F4F2FC}
.pestal td:first-child small{font-family:var(--fb);font-size:6.6pt;letter-spacing:0;line-height:1.35;margin-top:1mm}.pestal td:first-child{width:24%}.pestal td{font-size:7.4pt;padding:2.6px 5px}.pestal td:first-child{font-size:11pt}
.side img{object-fit:cover}
#s-indice .toc li{padding:.3mm 0;font-size:7.6pt;line-height:1.35}#s-indice .toc .grp{margin:1.1mm 0 0;font-size:6.2pt}#s-indice h2{margin-bottom:0}#s-indice .stmt{display:none}
.phones.s6 figure{width:25.5mm}.phones.s6 img{width:25.5mm;height:55.2mm}
.sb2.ph .sc2 .im{height:46mm}.sb2.ph .sc2 .im img{object-position:top}
.phones.big figure{width:38mm}.phones.big img{width:38mm;height:82.2mm}
table.xs{font-size:7.3pt}table.xs td{padding:2.6px 5px}
table.xxs{font-size:6.9pt;line-height:1.32}table.xxs td{padding:2px 4px}
</style>'''
HEAD = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Evaluación 3 — Prototipado y testeo</title><link rel="stylesheet" href="ev3.css">{EXTRA}</head><body>'


def render(body, name):
    path = os.path.join(HERE, name)
    open(path, 'w', encoding='utf-8').write(HEAD + body + '</body></html>')
    return HTML(path, base_url=HERE).write_pdf()


def main_body():
    return (portada() + indice() + intro() + links() + ruta() + sqa() + sb1() + mk1() + pagina_cita() + f1() + r1() + cdm1() + pagina_cifras()
            + iter_docs() + meta() + sb2() + mk2() + f2() + r2() + cdm2() + tecnico()
            + f3() + retro() + retro3() + comp() + cdm3() + aplica()
            + pagina_cifras_v3() + iter3() + meta3() + sb3() + mk3() + ver3() + f4() + cost()
            + val() + recorrido() + pagina_pv() + pv() + pestal() + arte() + pert() + sost() + gest() + concl() + refs())


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
