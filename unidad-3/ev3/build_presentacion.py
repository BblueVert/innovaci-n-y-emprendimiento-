# Entrega EV3 en formato presentación (16:9) · Innovación y Emprendimiento III · Unidad 3 Prototipado y testeo.
# Reúne: herramientas del toolkit UA3, prototipo v1 → ciclo 1 → v2 → ciclo 2, kit de testeo con usuarios,
# PESTAL profundizada, estado del arte, pertinencia de la propuesta de valor y anexo con plantillas oficiales.
# Uso: python3 build_presentacion.py → Evaluacion3_Presentacion_Prototipado.html / .pdf
import os
import sys
import pymupdf as fitz
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contenido as C  # noqa: E402
import anexo_u3  # noqa: E402
from mockup import mock, ASPECT  # noqa: E402
sys.path.insert(0, os.path.join(HERE, '..', 'testeo'))
import build_kit as K  # noqa: E402

N = [0]
H_PH = 92  # alto estándar de las pantallas en las láminas (mm)
PAC = '../prototipo/capturas_paciente/'


def table(headers, rows, cls=''):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def slide(body, crit='', cls=''):
    N[0] += 1
    return (f'<section class="s {cls}">{body}<div class="ft"><span>Copiloto Kine · EV3 Prototipado y testeo · INACAP Rancagua</span>'
            f'<span><b>{crit}</b>{" · " if crit else ""}{N[0]:02d}</span></div></section>')


def head(kicker, title, code=None):
    c = f'<span class="c">{code}</span>' if code else ''
    return f'<div class="k">{kicker}</div><h1>{c}{title}</h1>'


def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


R = 1 / ASPECT  # alto / ancho del mockup de iPhone


def dev(src, h, hl=False):
    """Captura completa dentro del mockup de iPhone (foto recortada, fondo transparente), alto h en mm."""
    return f'<img class="iph" src="{mock(src)}" style="width:{h / R:.1f}mm;height:{h:.1f}mm">'


def phones(items, h=92, crop=None):
    out = ''
    for it in items:
        src, t = it[0], it[1]
        sub = f'<span>{it[2]}</span>' if len(it) > 2 else ''
        out += f'<figure style="width:{h / R + 4:.1f}mm">{dev(src, h)}<figcaption><b>{t}</b>{sub}</figcaption></figure>'
    return f'<div class="phones">{out}</div>'


# ---------------------------------------------------------------- diapositivas
def portada():
    return slide(f'''<img class="hero" src="img/01-portada.jpg"><div class="z" style="margin-top:6mm">
<div class="k">Innovación y Emprendimiento III · FGIE03 · INACAP Rancagua</div>
<div class="big" style="margin-top:6mm">EVALUACIÓN N°3<br><em>PROTOTIPADO</em><br>Y TESTEO</div>
<div style="font-family:var(--fd);font-size:22pt;color:#FF8A4C;margin-top:4mm;letter-spacing:.03em">COPILOTO KINE · CASO JOSELYN TOLEDO</div>
<p class="lead" style="max-width:150mm;margin-top:3mm">Del storyboard al prototipo v3: dos ciclos internos, la validación con la clienta y Sercotec, y la iteración que trabaja como ella trabaja.</p>
<div style="margin-top:9mm;font-size:10pt"><b>Francisco Ahumada · Claudia Cifuentes · Néstor Rivera · Benjamín Vera Yáñez</b><br>
<span style="font-family:var(--fm);font-size:8pt;letter-spacing:.1em;color:#9B98B8">PROFESOR: ROBERTO ESCOBAR DONOSO · DISEÑO DIGITAL · NOVIEMBRE 2026</span></div></div>''', cls='dark solid')


def criterios():
    cr = [('3.1.1', 15, 'Uso de herramientas metodológicas para prototipar y testear', 'SQA · storyboard · mock-up · fichas · CDM'),
          ('3.1.2', 20, 'Prototipo validado en más de un ciclo, con enfoque sostenible', 'Ciclo 1 funcional · ciclo 2 técnico · ciclo 3 con la clienta · ciclo 4 planificado'),
          ('3.1.3', 15, 'Ajusta el prototipo de forma fundamentada', 'Dos iteraciones: v2 (12 cambios del ciclo 1) y v3 (12 cambios del ciclo 3)'),
          ('3.1.4', 20, 'Estado del arte y tendencias', 'PESTAL profundizada · matriz de antecedentes · 6 tendencias'),
          ('3.1.5', 30, 'Pertinencia de la propuesta de valor', 'Propuesta iterada contrastada con problema, mercado y evidencia')]
    cards = ''.join(f'<div><div class="c">CRITERIO {c}</div><div class="p">{p}<small> pts</small></div><div style="margin-top:1.5mm"><b>{t}</b></div><div class="w">{w}</div></div>' for c, p, t, w in cr)
    ag = ['Punto de partida y ruta', 'Herramientas U3: SQA, storyboard y mock-up', 'Ciclo 1 · uso y estética', 'Iteración v2', 'Ciclo 2 · técnico',
          'Ciclo 3 · clienta, Sercotec y docentes', 'Iteración v3: metáfora, storyboard y mock-up', 'Ciclo 4 · ficha con usuarias', 'Costo y propuesta de valor v3',
          'PESTAL, estado del arte y tendencias', 'Pertinencia, sostenibilidad y gestión', 'Anexo: plantillas oficiales']
    return slide(head('Qué presentamos', 'Agenda y criterios de evaluación') + f'<div class="cri">{cards}</div>'
                 + f'<div style="margin-top:6mm;columns:2;font-size:10pt">' + ''.join(f'<div style="margin-bottom:1.6mm"><span style="font-family:var(--fm);color:var(--acc2);font-size:8pt">{i:02d}</span> &nbsp;{a}</div>' for i, a in enumerate(ag, 1)) + '</div>', 'Rúbrica ES03')


def partida():
    return slide(head('Punto de partida · UA1 y UA2', 'El problema y la propuesta que llegamos a probar') + f'''
<div class="col2"><div class="a"><h3>Desafío (UA1)</h3><div class="quote" style="font-size:14pt">{C.DESAFIO}</div>
<h3>Propuesta de valor (EV2)</h3><p style="font-size:10pt">{C.PDV_EV2}</p>
<div><span class="chip o">Anticipador</span><span class="chip o">Legible de un vistazo</span><span class="chip o">Automático</span><span class="chip o">Sostenible</span><span class="chip">Requerimientos R1–R13</span></div></div>
<div class="b"><img src="img/02-caso.jpg" style="width:100%;border-radius:8px;border:1px solid var(--line)">
<div class="card" style="margin-top:3mm;font-size:9pt"><div class="t">Usuaria</div>Josselyn Toledo, kinesióloga y psicomotricista acuática: Centro Médico InMotion (factura mensual), domicilios en San Fernando y la precordillera, piscina temperada y gimnasio.
Anota todo cada noche en el teléfono y no sabe qué canal le conviene.</div></div></div>''', 'Contexto')


def ruta():
    st = [('on', 'S11 · Prototipar', 'SQA, storyboard y mock-up v1 con la propuesta de valor.'),
          ('on', 'S11–S12 · Ciclo 1', 'Testeo funcional y estético: 11 tareas, WCAG AA, heurísticas.'),
          ('on', 'S12 · CDM 1', 'Cualidades, debilidades y mejoras → backlog v2.'),
          ('on', 'S12–S13 · Iterar', 'Metáfora, storyboard y mock-up v2: 12 cambios.'),
          ('on', 'S13 · Ciclo 2', 'Verificación técnica: 11 pruebas + cobertura R1–R13.'),
          ('on', 'S13 · Ciclo 3', 'Clienta, Sercotec y docentes (12/11): 12 hallazgos.'),
          ('on', 'S14 · Iterar v3', 'Metáfora, storyboard y mock-up v3: 12 cambios.'),
          ('pe', 'S15 · Ciclo 4', 'Josselyn y Catalina con la v3 en su celular.')]
    ch = ''.join(f'<div class="{c}"><b>{t}</b>{d}</div>' for c, t, d in st)
    return slide(head('Ruta metodológica', 'Cuatro ciclos con focos distintos: dos internos, uno con la clienta y uno con usuarias') + f'<div class="chain">{ch}</div>' + f'''
<div class="row" style="margin-top:4mm"><div class="card"><div class="t">Ciclo 1 · funcional y estético</div>¿Puede una kinesióloga hacer su día sin ayuda? ¿Se lee, se toca y se entiende? Medido con tareas, auditoría WCAG 2.1 AA, objetivos táctiles, tamaño de letra y heurísticas de Nielsen.</div>
<div class="card"><div class="t">Ciclo 2 · técnico</div>¿Resuelve con exactitud sus necesidades puntuales? Cálculo por atención, cierre del día, persistencia, costos editables, exportación sin datos clínicos, rendimiento y brechas.</div>
<div class="card"><div class="t">Ciclo 3 · con la clienta</div>Reunión del 12/11 con Josselyn, Sercotec y docentes: valida el problema y cambia el producto (AgendaPro, factura mensual, 4 canales, tiempo de viaje). Origina la v3.</div>
<div class="card"><div class="t">Ciclo 4 · usuarias · planificado</div>Josselyn y Catalina usan la v3 en su celular: tareas nuevas, decisión con la ganancia por hora, SUS y precio.</div></div>
<p class="note" style="margin-top:4mm"><b>Transparencia.</b> Los ciclos 1 y 2 los ejecutó el equipo como usuarios internos (lo permite el toolkit) con scripts reproducibles en <code>unidad-3/ciclo1</code> y <code>ciclo2</code>. El ciclo 3 usa la transcripción de la reunión real; los resultados del ciclo 4 se marcan como pendientes: no inventamos respuestas de personas reales.</p>''', '3.1.1 · 3.1.2')


def sqa():
    cols = ''.join(f'<div class="card"><div class="t">{t}</div>{ul(items)}</div>' for t, items in C.SQA)
    return slide(head('3.1.1.1 · Evaluación diagnóstica', 'Tabla SQA', '3.1.1.1') + f'<div class="row">{cols}</div>', '3.1.1')


def scenes(sc, mode):
    out = ''
    for i, (t, img, kind, txt, a, b) in enumerate(sc, 1):
        la, lb = ('Producto', 'Propuesta de valor') if mode == 'v1' else ('Cualidad', 'Mejora incorporada')
        boxes = f'<div class="cc"><div class="c p"><b>{la}</b>{a}</div><div class="c v"><b>{lb}</b>{b}</div></div>'
        head_ = f'<div class="n">Escena {i}</div><div class="h">{t}</div><div class="d">{txt}</div>'
        if kind == 'wide':
            out += f'<div class="sc w"><div class="top"><img class="il" src="{img}"><div class="tx">{head_}</div></div>{boxes}</div>'
        else:
            out += f'<div class="sc ph">{dev(img, 54)}<div class="tx">{head_}{boxes}</div></div>'
    return f'<div class="sb">{out}</div>'


def storyboard_v1():
    return slide(head('3.1.2.1 · Storyboard con propuesta de valor', 'Un día de Josselyn con Copiloto Kine', '3.1.2.1') + scenes(C.SCENES, 'v1'), '3.1.1 · 3.1.5')


def mock_v1():
    return slide(head('3.1.2.2 · Mock-up con propuesta de valor', 'Prototipo v1 navegable en el celular', '3.1.2.2')
                 + phones([(f, t, f'{d}<br><i style="color:var(--acc2)">{a}</i>') for t, f, d, a in C.MOCK_V1], h=H_PH)
                 + '<p style="margin-top:3mm;font-size:8.6pt;color:var(--ink2)">HTML autocontenido (390 px), sin instalación: se abre desde un enlace en el celular. Paleta clara del proyecto con acentos naranjos; clínica en morado y domicilio en naranjo.</p>', '3.1.2')


def ficha_tbl(F):
    rows = [[f'<b>{r[0]}</b>', r[1], r[3], r[4], r[5], r[6], r[7], f'{r[8]} · {r[9]}'] for r in F['filas']]
    return table(['Objetivo específico', 'Participantes', 'Actividad', 'Roles', 'Indicador', 'Pregunta', 'Procesamiento', 'Lugar · tiempo'], rows, 'sm')


def ficha1():
    return slide(head('3.1.2.3 · Ficha de planificación del testeo', 'Ciclo 1 · funcional y estético', '3.1.2.3')
                 + f'<div class="quote" style="font-size:13pt">{C.FICHA_C1["objetivo"]}</div>' + ficha_tbl(C.FICHA_C1)
                 + f'<p style="font-size:8.4pt;color:var(--ink2);margin-top:2mm">{C.EQUIPO_ROLES}</p>', '3.1.2')


def fix(o):
    o = o.replace(': true', ': sí').replace(': false', ': no').replace(' | ', ' · ')
    return (o[:95] + '…') if len(o) > 95 else o


def res1():
    t = C.C1['tasks']; ok = sum(x['ok'] for x in t)
    axe = sum(x['n'] for v in C.C1['axe'].values() for x in v); tg = sum(len(v) for v in C.C1['targets'].values())
    rows = [[f'<b>{x["id"]}</b>', x['name'], f'<span class="{"ok" if x["ok"] else "ko"}">{"✔" if x["ok"] else "✖"}</span>', x['taps'] if x['ok'] else '—',
             fix(x['obs'])] for x in t]
    return slide(head('Ciclo 1 · resultados', 'Funciona en lo central; falla en corregir y en accesibilidad')
                 + f'''<div class="kpis"><div><div class="v">{ok}/{len(t)}</div><div class="l">tareas completadas sin ayuda (meta ≥ 90 %)</div></div>
<div><div class="v">{axe}</div><div class="l">errores de contraste WCAG AA (blanco sobre naranjo 2,84:1)</div></div>
<div><div class="v">{tg}</div><div class="l">botones o enlaces bajo 44 px (enlaces de 19 px)</div></div>
<div><div class="v">10–11 px</div><div class="l">textos en etiquetas, leyendas y navegación</div></div></div>'''
                 + table(['#', 'Tarea', 'Éxito', 'Toques', 'Evidencia'], rows, 'sm'), '3.1.2')


def heur():
    rows = [[h, d, f'<span class="bar s{min(s, 3)}" style="width:{4 + s * 9}mm"></span> &nbsp;<b>{s}</b>'] for h, d, s in C.HEUR]
    return slide(head('Ciclo 1 · revisión heurística', 'Tres problemas mayores, todos de control del usuario')
                 + '<div class="col2"><div class="a">' + table(['Heurística', 'Hallazgo', 'Severidad 0–4'], rows, 'sm') + '</div>'
                 + '''<div class="b"><div class="card"><div class="t">Lectura</div><ul><li>Severidad 3 en <b>H3, H5 y H7</b>: no se puede deshacer, no existe “no asistió” y los costos no se ajustan. La promesa “automático” se rompe ante el primer error.</li>
<li>Severidad 2 en <b>H2 y H9</b>: “Destinos” y “ganancia real” no se entienden sin explicación.</li><li>Lo estético funciona: tablero compacto, paleta clara y jerarquía legible (H8 = 1).</li></ul></div>
<div class="card" style="margin-top:3mm"><div class="t">Regla de decisión</div>Todo problema de severidad ≥ 2 entra a la iteración v2.</div></div></div>''', '3.1.2')


def cdm_slide(D, title, code, crit):
    def cell(items):
        return '<div class="cell">' + ul(items) + '</div>'
    g = ('<div class="cdm"><div></div><div class="hd c">Cualidades</div><div class="hd d">Debilidades</div><div class="hd m">Mejoras</div>'
         f'<div class="rh">PRODUCTO / SERVICIO</div>{cell(D["prod_c"])}{cell(D["prod_d"])}{cell(D["prod_m"])}'
         f'<div class="rh">PROPUESTA DE VALOR</div>{cell(D["pdv_c"])}{cell(D["pdv_d"])}{cell(D["pdv_m"])}</div>')
    return slide(head(f'{code} · Matriz CDM con propuesta de valor', title, code) + g, crit)


def antes_despues():
    v2 = C.C1V2['tasks']; ok2 = sum(x['ok'] for x in v2)
    return slide(f'''<div class="k" style="margin-top:10mm">De la prueba a la iteración</div>
<div class="big" style="font-size:88pt;margin-top:6mm">7 DE 11 <em>→ {ok2} DE 11</em></div>
<p style="font-size:15pt;max-width:220mm;margin-top:5mm">Tareas completadas sin ayuda, de la versión 1 a la versión 2. Los errores de contraste bajaron de 11 a 0, los botones chicos de 7 a 0 y la letra mínima subió a 12 px.</p>''', '3.1.3', 'orange')


def metafora():
    M = C.METAFORA_ITER
    at = ''.join(f'<div class="attr"><div class="n">{n}</div><div class="s2">…{s}</div><div class="r">{r}</div><div style="margin-top:1.5mm">{"".join(f"<span class=chip>{x}</span>" for x in tags)}</div></div>' for n, s, r, tags in M['atributos'])
    return slide(head('3.1.3.1 · Panel de metáforas y atributos iterado', 'La metáfora pasa del tablero al copiloto', '3.1.3.1') + f'''
<div class="row"><div><div class="k" style="color:var(--ink2)">Antes (EV2)</div><div class="quote" style="font-size:13pt;border-color:#C9C6DA;color:var(--ink2)">{M["antes"]}</div></div>
<div><div class="k">Después (iteración)</div><div class="quote" style="font-size:13pt">{M["despues"]}</div></div></div>
<p style="font-size:9pt;margin-bottom:3mm"><b>Por qué:</b> {M["porque"]}</p><div class="row" style="gap:3mm">{at}</div>''', '3.1.3')


def storyboard_it():
    return slide(head('3.1.3.2 · Storyboard iterado', 'El mismo día, con lo que aprendimos del ciclo 1', '3.1.3.2') + scenes(C.SCENES_ITER, 'it'), '3.1.3')


def mock_it():
    V1, V2 = '../prototipo/capturas_v1/', '../prototipo/capturas_v2/'
    pares = [('01_tablero.png', '01_tablero.png', 'Tablero', '“Ganancia real” definida; letra ≥ 12 px'),
             ('06_agenda.png', '06_agenda.png', 'Agenda', 'Deshacer y “No asistió”; botones accesibles'),
             ('08_destinos.png', '08_mi_plata.png', '“Destinos” → “Mi plata”', 'Costos editables y exportación')]
    blk = ''.join(pair(V1 + a, V2 + b, t, d, 80, 'v1', 'v2') for a, b, t, d in pares)
    return slide(head('3.1.3.3 · Mock-up iterado', 'Versión 1 → versión 2', '3.1.3.3') + f'<div class="pairs">{blk}</div>', '3.1.3')


def pair(a, b, t, d, h, va, vb):
    return (f'<div class="pair"><div class="ba2"><div><div class="vt">{va}</div>{dev(a, h)}</div><div class="ar">→</div>'
            f'<div><div class="vt on">{vb}</div>{dev(b, h, True)}</div></div><div class="pc"><b>{t}</b><span>{d}</span></div></div>')


def cambios():
    rows = [[f'<b>{i}</b>', c, h, r] for i, (c, h, r, _) in enumerate(C.CAMBIOS, 1)]
    return slide(head('3.1.3.3 · Ajustes fundamentados', 'Cada cambio responde a un hallazgo medido', '3.1.3.3')
                 + table(['#', 'Cambio en v2', 'Hallazgo del ciclo 1', 'Requerimiento / atributo'], rows, 'sm'), '3.1.3')


def ficha2():
    return slide(head('3.1.3.4 · Ficha de planificación del testeo de la iteración', 'Ciclo 2 · técnico: ¿resuelve sus necesidades puntuales?', '3.1.3.4')
                 + f'<div class="quote" style="font-size:12pt">{C.FICHA_C2["objetivo"]}</div>' + ficha_tbl(C.FICHA_C2), '3.1.2 · 3.1.3')


def res2():
    pr = C.C2['pruebas']
    rows = [[f'<b>{p["id"]}</b>', p['req'], p['nombre'], f'<span class="ok">✔</span>' if p['ok'] else '<span class="ko">✖</span>',
             (p['evidencia'][:88] + '…') if len(p['evidencia']) > 88 else p['evidencia']] for p in pr]
    return slide(head('Ciclo 2 · resultados', 'Exacto, rápido y sin datos clínicos')
                 + f'''<div class="kpis"><div><div class="v ok">{sum(p["ok"] for p in pr)}/{len(pr)}</div><div class="l">pruebas técnicas aprobadas</div></div>
<div><div class="v ok">$0</div><div class="l">diferencia con la hoja de referencia en 5 atenciones</div></div>
<div><div class="v ok">11</div><div class="l">toques para cerrar un día de 5 atenciones (antes ~60 min en Excel)</div></div>
<div><div class="v ok">39 KB</div><div class="l">peso total; legible sin fuentes web</div></div></div>''' + table(['#', 'Req.', 'Prueba', 'OK', 'Evidencia'], rows, 'sm'), '3.1.2')


def cobertura():
    cl = {'Cumple': 'ok', 'Cumple*': 'ok', 'Parcial': 'pa', 'Simulado': 'ko'}
    rows = [[f'<b>{r}</b>', n, f'<span class="{cl[e]}">{e}</span>', ev, o] for r, n, e, ev, o in C.COBERTURA]
    cnt = {k: sum(1 for x in C.COBERTURA if x[2].startswith(k)) for k in ('Cumple', 'Parcial', 'Simulado')}
    return slide(head('Ciclo 2 · trazabilidad', f'Requerimientos: {cnt["Cumple"]} cumplen, {cnt["Parcial"]} parciales, {cnt["Simulado"]} simulado')
                 + table(['#', 'Requerimiento (EV2)', 'Estado', 'Prueba', 'Observación'], rows, 'sm'), '3.1.2 · 3.1.5')


def brechas():
    rows = [[f'<b>{b}</b>', t, d, f'<span class="chip {"o" if "MVP" in f or "Inm" in f else ""}">{f}</span>'] for b, t, d, f in C.BRECHAS]
    return slide(head('Ciclo 2 · brechas técnicas', 'Lo que el prototipo todavía no resuelve') + table(['#', 'Brecha', 'Qué hacer', 'Cuándo'], rows)
                 + '<p class="note" style="margin-top:3mm">Las brechas no son fallas del prototipo sino el <b>backlog del MVP</b> (UA4): integraciones reales, respaldo en la nube y privacidad reforzada. B6 se resuelve antes de usar datos reales.</p>', '3.1.3')


def validacion():
    hip = ''.join(f'<tr><td><b>{h}</b></td><td>{p}</td><td>{t}</td><td>{c}</td></tr>' for h, p, t, _, c, _ in K.HIP)
    return slide(head('Validación con usuarios · kit de testeo', 'Preparado para kinesiólogas, pacientes y contadora') + f'''
<div class="col2"><div class="a"><table class="sm"><thead><tr><th>#</th><th>Público</th><th>Hipótesis</th><th>Éxito si…</th></tr></thead><tbody>{hip}</tbody></table></div>
<div class="b"><div class="card"><div class="t">Qué incluye el kit (20 págs.)</div><ul><li>Plan, hipótesis, muestra y calendario</li><li>9 perfiles de participantes</li><li>Guiones A (kines), B (pacientes) y C (contadora)</li>
<li>Consentimiento informado (Ley 21.719)</li><li>Pautas de observación, SUS y encuesta de pacientes</li><li>Matriz de consolidación con reglas de decisión</li><li>Invitaciones listas para WhatsApp</li></ul></div>
<div class="card" style="margin-top:3mm"><div class="t">Estado</div>Ciclo 3 (12/11) aplicado con la clienta. Sesiones del ciclo 4 con la v3 <span class="pend">pendientes</span>; el guion A suma las tareas N1–N10.</div></div></div>''', '3.1.2 · 3.1.5')


def perfiles():
    cards = ''.join(f'<div class="pf t{p["tipo"]}"><div class="top"><div class="cd">{p["c"]}</div><div><b>{p["n"]}</b><br><span style="color:var(--ink2)">{p["t"]}</span></div></div>{p["d"]}<div class="h">{p["h"]} · {p["m"]}</div></div>' for p in K.PERF)
    return slide(head('Validación con usuarios · públicos', 'Nueve perfiles: quien usa la app y quien vive sus efectos')
                 + f'<div class="pfs">{cards}</div><p style="font-size:8.2pt;color:var(--ink2);margin-top:2.5mm">K1 y K2 son participantes reales del proyecto (UA1). Los pacientes entre comillas son perfiles a reclutar: se invita a pacientes de Josselyn solo si ella lo propone, o a personas del entorno del equipo que calcen con el perfil. No se registran diagnósticos.</p>', '3.1.2')


def paciente():
    return slide(head('Nuevo estímulo · vista paciente', 'Lo que recibe el paciente cuando su kine usa Copiloto Kine') + '<div class="col2"><div class="a">'
                 + phones([(PAC + '01_recordatorio_a.png', 'M1 · Recordatorio', 'Llego cerca de las 12:30 (H5)'), (PAC + '02_voy_en_camino_a.png', 'M2 · Voy en camino', 'Hora exacta (H6)'),
                           (PAC + '03_pago_comprobante_a.png', 'M3 · Pago', 'Copia al familiar (H7)'), (PAC + '04_clase_grupal_a.png', 'M4 · Clase grupal', 'Personas mayores (H11)')], h=H_PH)
                 + '''</div><div class="b" style="flex:.55"><div class="card"><div class="t">Por qué</div>La ruta sugerida (−7 km/día) solo funciona si el paciente acepta una
ventana de llegada. Es la hipótesis más riesgosa del modelo y no se puede probar con kinesiólogas.</div>
<div class="card" style="margin-top:3mm"><div class="t">Accesibilidad</div>Botón “Letra grande” para adultos mayores, botones de 44 px y 0 errores WCAG AA en los 4 mensajes.</div>
<div class="card" style="margin-top:3mm"><div class="t">Archivo</div><code style="font-size:7.5pt">prototipo/vista-paciente.html</code></div></div></div>''', '3.1.2')


def pdv():
    return slide(f'''<img class="pvphone" src="{mock('../prototipo/capturas_v3/02_ganancia_por_hora.png')}"><div class="z" style="max-width:200mm;margin-top:2mm">
<div class="k">Propuesta de valor iterada (v3) · 3.1.5</div>
<div class="big" style="font-size:40pt;margin:3mm 0 4mm">DEL COPILOTO DE SU DÍA<br>AL <em>COPILOTO DE SU TERRENO</em>.</div>
<div class="pvq" style="font-size:13pt">{C.PDV_V3}</div>
<div style="margin-top:4mm;font-size:9pt;color:#C9C6DA"><b style="color:#fff">EV2 → v2:</b> la ruta al centro y la promesa ajustada a lo verificado. <b style="color:#fff">v2 → v3 (ciclo 3):</b> sus agendas reales, sus cuatro lugares de trabajo, la ganancia por hora y el tiempo de viaje como costo.</div>
<div class="tags" style="margin-top:4mm"><span>Anticipador</span><span>Claro</span><span>Conectado y corregible</span><span>Justo con su tiempo</span></div></div>''', '3.1.5', 'dark')


def pestal(rows, part):
    tr = ''.join(f'<tr><td><b style="font-family:var(--fd);font-size:15pt;font-weight:400">{n.upper()}</b><br><span style="font-size:7.4pt;color:var(--ink2)">{o["f"]}</span></td>'
                 f'<td>{p["f"]}</td><td>{p["o"]}</td><td>{p["a"]}</td></tr>' for n, o, p in rows)
    return slide(head('3.1.4.1 · Matriz PESTAL profundizada', f'Del contexto de la UA1 a la evidencia del prototipo ({part})', '3.1.4.1')
                 + f'<table class="sm" style="font-size:8.3pt"><thead><tr><th style="width:24%">Factor · original (UA1)</th><th>Factor profundizado</th><th>Oportunidad</th><th>Amenaza</th></tr></thead><tbody>{tr}</tbody></table>', '3.1.4')


def arte():
    dot = {2: '<span class="d2">●</span>', 1: '<span class="d1">◐</span>', 0: '<span class="d0">○</span>'}
    rows = ''.join(f'<tr class="{"me" if "Copiloto" in n else ""}"><td>{n}</td>' + ''.join(f'<td>{dot[v]}</td>' for v in vs) + '</tr>' for n, vs in C.ARTE)
    return slide(head('3.1.4 · Estado del arte', 'Nadie cruza agenda, costos por atención e impuestos chilenos')
                 + f'<table class="mat"><thead><tr><th>Solución</th>{"".join(f"<th>{v}</th>" for v in C.ARTE_VARS)}</tr></thead><tbody>{rows}</tbody></table>'
                 + '<p style="font-size:8.6pt;color:var(--ink2)">● cubre · ◐ parcial · ○ no cubre. Antecedentes de la UA1 (AgendaPro, Encuadrado, Reservo, Medilink, Cal.com, Cliniko, Jane App, Nubox) revisados en sus sitios oficiales; v2 y v3 se evalúan con lo que efectivamente hacen hoy (agenda e itinerario simulados = ◐). La v3 suma la ganancia por hora por canal.</p>', '3.1.4')


def tendencias():
    rows = [[f'<b>{t}</b>', d, r] for t, d, r in C.TENDENCIAS]
    return slide(head('3.1.4 · Tendencias', 'Siete tendencias que el prototipo ya incorpora') + table(['Tendencia', 'Qué está pasando', 'Cómo responde Copiloto Kine'], rows), '3.1.4')


def pertinencia():
    rows = [[f'<b>{a}</b>', b, c] for a, b, c in C.PERTINENCIA_V3]
    return slide(head('3.1.5 · Pertinencia de la propuesta de valor', 'La propuesta responde al problema, al mercado y a la evidencia')
                 + table(['Dimensión', 'Lo que sabemos', 'Cómo responde la propuesta iterada'], rows)
                 + '<div class="quote" style="font-size:13pt;margin-top:3mm">Pertinente porque nace de su rutina real (ciclo 3) y se diferencia en lo que las otras propuestas no hacen; el ciclo 4 decidirá precio y alcance del MVP.</div>', '3.1.5')


def sostenibilidad():
    return slide(head('Enfoque sostenible', 'Económico, social y ambiental, con números') + '''<div class="row">
<div class="card"><div class="t">Económico</div><div class="kpis" style="margin:1mm 0 2mm"><div style="border:none;padding:0"><div class="v">+$570.000</div><div class="l">acciones que cubren enero y febrero</div></div></div>
Ganancia por hora por canal, tarifa por tramo para la precordillera y clase grupal para los meses bajos; retención configurable (Ley 21.133).</div>
<div class="card"><div class="t">Social</div><div class="kpis" style="margin:1mm 0 2mm"><div style="border:none;padding:0"><div class="v">~1 h → 1 min</div><div class="l">cierre del día sin anotar de noche (RF2)</div></div></div>
Accesibilidad WCAG AA, letra grande para adultos mayores y datos de salud fuera del sistema (Ley 21.719).</div>
<div class="card"><div class="t">Ambiental</div><div class="kpis" style="margin:1mm 0 2mm"><div style="border:none;padding:0"><div class="v">−140 km/mes</div><div class="l">≈ 10 l de bencina · ≈ 23 kg CO2</div></div></div>
Ruta sugerida: 20 vs. 27 km en el día de ejemplo (−26 %). Estimación del equipo con 20 días de domicilios, 14 km/l y 2,3 kg CO2/l.</div></div>''', '3.1.2')


def gestion():
    w = C.GANTT_W3
    rows = ''.join(f'<tr><td>{t}</td>' + ''.join(f'<td class="{m.get(x, "")}"></td>' for x in w) + '</tr>' for t, m in C.GANTT_V3)
    roles = [('Claudia Cifuentes', 'Moderación de sesiones'), ('Néstor Rivera', 'Ejecución de tareas y prototipo'), ('Francisco Ahumada', 'Registro y CDM'), ('Benjamín Vera Yáñez', 'Secretario técnico: consolidación y auditoría técnica')]
    return slide(head('Gestión de la fase · bitácora', 'Organización del tiempo y roles') + f'''<div class="col2"><div class="a">
<table class="gantt"><thead><tr><th>Actividad</th>{"".join(f"<th>{x}</th>" for x in w)}</tr></thead><tbody>{rows}</tbody></table></div>
<div class="b"><h3>Roles</h3>{table(["Integrante", "Rol"], roles, "sm")}<h3 style="margin-top:3mm">Evidencias en el repositorio</h3>
<p style="font-size:8.6pt"><code>unidad-3/prototipo</code> (v1, v2, v3, vista paciente, capturas) · <code>ciclo1</code>, <code>ciclo2</code> e <code>iteracion-v3</code> (scripts y resultados JSON) · <code>retroalimentacion</code> (transcripción 12/11) · <code>testeo</code> (kit) · bitácora U3.</p></div></div>''', 'Bitácora')


def conclusiones():
    return slide(head('Cierre', 'Conclusiones y próximos pasos') + '''<div class="row">
<div class="card"><div class="t">Aprendimos</div><ul><li>Medir tareas y accesibilidad da evidencia más útil que preguntar si “gusta”.</li><li>“Automático” sin “corregible” genera registros falsos.</li><li>La ruta es tan valiosa como el tablero: la metáfora se movió hacia el copiloto.</li><li>La clienta cambió la pregunta: no “cuánto gané” sino “qué me conviene”.</li></ul></div>
<div class="card"><div class="t">Logramos</div><ul><li>Tres versiones y tres ciclos aplicados; el tercero con la clienta real.</li><li>v3 navegable: 21/21 tareas, cálculos exactos, 0 errores WCAG AA.</li><li>12 cambios de la v3 trazados a lo que dijo la clienta.</li><li>Costeo: piloto ≈ $900/mes; comercial desde $9.990.</li></ul></div>
<div class="card"><div class="t">Sigue</div><ul><li><b>Ciclo 4:</b> Josselyn y Catalina con la v3 en su celular (tareas N1–N10, SUS y precio).</li><li><b>CDM 4:</b> decidir precio, tramos y alcance del módulo grupal.</li><li><b>UA4:</b> MVP con la exportación de AgendaPro, respaldo en la nube y enlace wa.me.</li></ul></div></div>''', 'Cierre')


def referencias():
    refs = ['INACAP (2026). Toolkit y manual del estudiante, Unidad 3 · Innovación y Emprendimiento III (FGIE03).',
            'Nielsen, J. (1994). 10 Usability Heuristics for User Interface Design. Nielsen Norman Group.',
            'W3C (2018). Web Content Accessibility Guidelines (WCAG) 2.1. Deque Systems, axe-core 4.10.',
            'Brooke, J. (1996). SUS: A “quick and dirty” usability scale. Usability Evaluation in Industry.',
            'Ley 21.133 (2019). Incorpora a trabajadores independientes a la seguridad social. Biblioteca del Congreso Nacional.',
            'Ley 21.719 (2024). Regula la protección y el tratamiento de los datos personales. Biblioteca del Congreso Nacional.',
            'Ley 20.584 (2012). Derechos y deberes de los pacientes. Biblioteca del Congreso Nacional.',
            'Sitios oficiales de AgendaPro, Encuadrado, Reservo, Medilink, Cal.com, Cliniko, Jane App y Nubox (consulta UA1).',
            'Equipo (2026). Informes EV1 y EV2, entrevistas a Josselyn Toledo y Catalina (UA1).',
            'Reunión de retroalimentación con Josselyn Toledo, Sercotec y docentes INACAP (12 de noviembre de 2026). Transcripción del equipo.',
            'Vercel, Supabase, Comisión Nacional de Energía (Bencina en Línea) y NIC Chile: precios de lista, noviembre 2026.']
    return slide(head('Fuentes', 'Referencias') + '<div style="font-size:9.6pt;columns:2;column-gap:10mm">' + ''.join(f'<p>{r}</p>' for r in refs) + '</div>', 'Ref.')


def div_anexo(titles):
    li = ''.join(f'<div style="border-bottom:1px solid #2A2640;padding:1.8mm 0;font-size:10pt">{t}</div>' for t in titles)
    return slide(f'''<div class="k" style="margin-top:6mm">Anexo</div><div class="big" style="font-size:54pt;margin:4mm 0 6mm">PLANTILLAS OFICIALES<br><em>TOOLKIT UA3</em></div>
<div style="max-width:220mm">{li}</div>''', 'Anexo', 'dark')


def cierre():
    return slide('''<div class="k" style="margin-top:14mm">Conclusión</div>
<div class="big" style="font-size:52pt;margin-top:5mm;max-width:270mm">PROBAR CON EVIDENCIA, ITERAR CON CRITERIO Y <em>LLEVARLO A LAS PERSONAS</em>.</div>
<p style="font-size:14pt;max-width:220mm;margin-top:6mm">Copiloto Kine v3 ya habla el idioma de Josselyn; el ciclo 4 lo pone en sus manos. Gracias.</p>''', 'Gracias', 'orange')


# ================================================================ ciclo 3 (clienta) e iteración v3
def divisor(k, t, sub):
    return slide(f'<div class="k" style="margin-top:12mm">{k}</div><div class="big" style="font-size:60pt;margin-top:5mm;max-width:270mm">{t}</div>'
                 f'<p style="font-size:14pt;max-width:220mm;margin-top:6mm">{sub}</p>', '3.1.2 · 3.1.3', 'dark')


def ficha3():
    return slide(head('3.1.2.3 · Ficha de planificación del testeo', 'Ciclo 3 · validación con la clienta, Sercotec y docentes', '3.1.2.3')
                 + f'<div class="quote" style="font-size:12pt">{C.FICHA_C3["objetivo"]}</div>' + ficha_tbl(C.FICHA_C3)
                 + f'<p class="note" style="margin-top:3mm">{C.RETRO_CONTEXTO} Fuente: <code>unidad-3/retroalimentacion/Transcripcion_reunion_2026-11-12.md</code>.</p>', '3.1.2')


def retro_rf():
    rows = [[f'<b>{c}</b>', f'<b>{t}</b><br><span style="color:var(--ink2)">{q}</span>', m, i] for c, t, q, m, i in C.RETRO_HALLAZGOS]
    return slide(head('Ciclo 3 · resultados', 'Lo que dijo la clienta: 12 hallazgos con su minuto')
                 + table(['#', 'Hallazgo y cita', 'Min.', 'Implicancia'], rows, 'sm xs'), '3.1.2')


def retro_sug():
    doc = [[f'<b>{w}</b>', t, m] for w, t, m in C.RETRO_DOCENTES]
    pat = [[f'<b>{p}</b>', d] for p, e, d in C.RETRO_PATRONES]
    return slide(head('Ciclo 3 · Sercotec y docentes', 'Barato, multi-dispositivo, con costo estimado y combinable')
                 + '<div class="col2"><div class="a">' + table(['Quién', 'Sugerencia', 'Min.'], doc, 'sm') + '</div><div class="b">'
                 + '<h3>Patrones</h3>' + table(['Patrón', 'Qué significa'], pat, 'sm') + '</div></div>', '3.1.2')


def compara():
    dot = {2: '<span class="d2">●</span>', 1: '<span class="d1">◐</span>', 0: '<span class="d0">○</span>'}
    rows = ''.join(f'<tr class="{"me" if "Copiloto" in n else ""}"><td>{n}</td>' + ''.join(f'<td>{dot[v]}</td>' for v in vs) + f'<td style="font-size:7.6pt">{c}</td></tr>' for n, vs, c in C.COMPARA)
    return slide(head('Ciclo 3 · las 4 propuestas que vio la clienta', 'Mismo problema, distintas soluciones: qué hace cada una')
                 + f'<table class="mat big"><thead><tr><th>Propuesta</th>{"".join(f"<th>{v}</th>" for v in C.COMPARA_CRIT)}<th>Costo para ella</th></tr></thead><tbody>{rows}</tbody></table>'
                 + f'<p style="font-size:8.2pt;color:var(--ink2)">{C.COMPARA_NOTA}</p>'
                 + '<h3 style="margin-top:3mm">Lo que tomamos de las otras propuestas</h3>' + table(['Fuente', 'Lo que proponen', 'Cómo lo aplicamos (v3 y MVP)'], [[f'<b>{n}</b>', q, a] for n, q, a in C.APLICA_OTRAS], 'sm xs'), '3.1.4 · 3.1.5')


def salto_v3():
    return slide(f"""<div class="k" style="margin-top:10mm">Del ciclo 3 a la versión 3</div>
<div class="big" style="font-size:78pt;margin-top:6mm">2 CANALES <em>→ 5 CANALES</em></div>
<p style="font-size:15pt;max-width:230mm;margin-top:5mm">La v3 trabaja como ella: clínica con factura mensual, domicilio, piscina, gimnasio y clase grupal, en San Fernando y sus caminos rurales.
{C.V3_OK} de {len(C.V3_TASKS)} tareas completadas, cálculos exactos y {C.V3_AXE} errores de accesibilidad AA.</p>""", '3.1.3', 'orange')


def metafora_v3():
    M = C.METAFORA_V3
    at = ''.join(f'<div class="attr"><div class="n">{n}</div><div class="s2">…{s}</div><div class="r">{r}</div><div style="margin-top:1.5mm">{"".join(f"<span class=chip>{x}</span>" for x in tags)}</div></div>' for n, s, r, tags in M['atributos'])
    return slide(head('3.1.3.1 · Panel de metáforas y atributos iterado (v3)', 'El copiloto ahora conoce el terreno', '3.1.3.1') + f"""
<div class="row"><div><div class="k" style="color:var(--ink2)">Antes (v2)</div><div class="quote" style="font-size:12pt;border-color:#C9C6DA;color:var(--ink2)">{M["antes"]}</div></div>
<div><div class="k">Después (v3)</div><div class="quote" style="font-size:12pt">{M["despues"]}</div></div></div>
<p style="font-size:8.8pt;margin-bottom:3mm"><b>Por qué:</b> {M["porque"]}</p><div class="row" style="gap:3mm">{at}</div>""", '3.1.3')


def storyboard_v3():
    return slide(head('3.1.3.2 · Storyboard iterado (v3)', 'Un martes de Josselyn en San Fernando, Agua Buena y la piscina', '3.1.3.2') + scenes(C.SCENES_V3, 'it'), '3.1.3')


def mock_v3():
    out = ''
    for k, grupo in enumerate((C.MOCK_V2V3[:2], C.MOCK_V2V3[2:]), 1):
        blk = ''.join(pair(a, b, t, d, 104, 'v2', 'v3') for a, b, t, d in grupo)
        out += slide(head('3.1.3.3 · Mock-up iterado', f'Versión 2 → versión 3 ({k}/2)', '3.1.3.3') + f'<div class="pairs">{blk}</div>', '3.1.3')
    return out


def mock_v3_b():
    V3 = C.V3
    return slide(head('3.1.3.3 · Mock-up v3', 'Lo nuevo, pantalla por pantalla', '3.1.3.3')
                 + phones([(V3 + '04_paradas_tramos.png', 'Tramos', 'Tiempo de viaje con valor y recargo por tramo'), (V3 + '09_clinica_factura.png', 'Clínica', 'Factura mensual o 70/30'),
                           (V3 + '10_servicios.png', 'Servicios', 'Piscina, gimnasio y grupal con su costo'), (V3 + '07_clase_grupal.png', 'Clase grupal', 'Cupos y punto de equilibrio'),
                           (V3 + '11_cierre_dia.png', 'Cierre del día', 'Resumen que reemplaza la nota nocturna')], h=H_PH), '3.1.3')


def cambios_v3():
    rows = [[f'<b>{i}</b>', c, h, r, f'<span class="{"ok" if e.startswith("Funcional") else "pa"}">{e}</span>'] for i, (c, h, r, _, e) in enumerate(C.CAMBIOS_V3, 1)]
    return slide(head('3.1.3.3 · Ajustes fundamentados (v3)', 'Cada cambio responde a lo que dijo la clienta', '3.1.3.3')
                 + table(['#', 'Cambio en v3', 'Hallazgo', 'Req. / atributo', 'Estado'], rows, 'sm'), '3.1.3')


def verif_v3():
    nt = [t for t in C.V3_TASKS if t['id'].startswith('N')]
    rows = [[f'<b>{t["id"]}</b>', t['origen'], t['name'], f'<span class="{"ok" if t["ok"] else "ko"}">{"✔" if t["ok"] else "✖"}</span>', t['taps'], (t['obs'][:78] + '…') if len(t['obs']) > 78 else t['obs']] for t in nt]
    base = sum(t['ok'] for t in C.V3_TASKS if t['id'].startswith('T'))
    return slide(head('Verificación del prototipo v3', 'Las tareas nuevas funcionan y lo anterior no se rompió')
                 + f"""<div class="kpis"><div><div class="v ok">{base}/11</div><div class="l">tareas base (regresión de v1 y v2)</div></div>
<div><div class="v ok">{len(nt) and sum(t['ok'] for t in nt)}/{len(nt)}</div><div class="l">tareas nuevas, una por cambio del 12/11</div></div>
<div><div class="v ok">{C.V3_CALC_OK}/{len(C.R3['calculos'])}</div><div class="l">cálculos idénticos a la referencia (ganancia, por hora y viaje)</div></div>
<div><div class="v ok">{C.V3_AXE} · {C.V3_TARGETS}</div><div class="l">errores WCAG AA · botones bajo 44 px</div></div></div>"""
                 + table(['#', 'Origen', 'Tarea', 'OK', 'Toques', 'Evidencia'], rows, 'sm xs')
                 + '<p class="note" style="margin-top:2mm">Script reproducible: <code>unidad-3/iteracion-v3/verificar_v3.js</code> · resultados en <code>resultados_v3.json</code>. Es verificación interna: la validación de uso es el ciclo 4 con Josselyn.</p>', '3.1.2 · 3.1.3')


def ficha4():
    return slide(head('3.1.3.4 · Ficha de planificación del testeo de la iteración', 'Ciclo 4 · Josselyn y Catalina con el prototipo v3', '3.1.3.4')
                 + f'<div class="quote" style="font-size:11.5pt">{C.FICHA_C4["objetivo"]}</div>' + ficha_tbl(C.FICHA_C4), '3.1.2 · 3.1.3')


def iter_docs_v3():
    rows = [[f'<b>{a}</b>', b, c, d, f'<span style="color:var(--ink2)">{e}</span>'] for a, b, c, d, e in C.ITER_DOCS_V3]
    return slide(head('Iteración de los instrumentos', 'Qué cambió en cada herramienta de la v2 a la v3')
                 + table(['Instrumento', 'Herramienta', 'Versión 2', 'Versión 3', 'Por qué'], rows, 'sm'), '3.1.1 · 3.1.3')


def costeo():
    d = [[f'<b>{a}</b>', b, c, f'<span style="color:var(--ink2)">{e}</span>'] for a, b, c, e in C.COSTEO_DESARROLLO]
    o = [[f'<b>{a}</b>', b, c, f'<b>{e}</b>'] for a, b, c, e in C.COSTEO_OPERACION]
    k = [[f'<b>{a}</b>', b, c] for a, b, c in C.COSTEO_COMPARA]
    return slide(head('Cuánto cuesta · pedido de Sercotec (12:30)', 'Piloto casi sin costo; comercial desde $9.990 al mes')
                 + '<div class="col2"><div class="a"><h3>Desarrollo</h3>' + table(['Ítem', 'Qué incluye', 'Costo', 'Nota'], d, 'sm')
                 + '<h3 style="margin-top:3mm">Operación mensual</h3>' + table(['Etapa', 'Servicios', 'Costo', 'Precio a la usuaria'], o, 'sm') + '</div>'
                 + '<div class="b"><h3>Frente a sus alternativas</h3>' + table(['Opción', 'Costo directo', 'Costo real'], k, 'sm')
                 + '<p class="note" style="margin-top:3mm">Precios de lista de noviembre 2026 a $950/US$. El precio de $9.990 baja la referencia de la EV2 ($20–25 mil) por lo dicho en el ciclo 3: bajo costo (Ariel) y un mercado regional que valora poco lo especializado (RF9). Se valida en el ciclo 4 (H4).</p></div></div>', '3.1.5')


# ================================================================ versión condensada (informe + presentación en un solo archivo)
URL = 'https://copiloto-kine.vercel.app'


def criterios_c():
    cr = [('3.1.1', 15, 'Fase de desarrollo y prototipado', 'SQA · storyboard · mock-up · fichas · CDM'),
          ('3.1.2', 20, 'Prototipo validado en más de un ciclo, sostenible', '4 ciclos: 2 internos, 1 con la clienta, 1 con usuarias'),
          ('3.1.3', 15, 'Ajusta el prototipo con fundamento', 'v1 → v2 → v3 · 24 cambios trazados'),
          ('3.1.4', 20, 'Estado del arte y tendencias', 'PESTAL profundizada · antecedentes · 4 propuestas'),
          ('3.1.5', 30, 'Pertinencia de la propuesta de valor', 'Propuesta v3 · costo · pertinencia')]
    cards = ''.join(f'<div><div class="c">CRITERIO {c}</div><div class="p">{p}<small> pts</small></div><div style="margin-top:1.5mm"><b>{t}</b></div><div class="w">{w}</div></div>' for c, p, t, w in cr)
    ag = ['Caso, prototipos y ruta', 'Prototipo v1 y ciclo 1', 'Iteración v2 y ciclo 2', 'Ciclo 3 · la clienta prueba la propuesta',
          'Iteración v3', 'Ciclo 4 · usuarias y pacientes', 'Costo y propuesta de valor v3', 'Estado del arte, pertinencia y sostenibilidad']
    return slide(head('Qué presentamos', 'Agenda y criterios de evaluación') + f'<div class="cri">{cards}</div>'
                 + '<div style="margin-top:6mm;columns:2;font-size:10.5pt">' + ''.join(f'<div style="margin-bottom:1.8mm"><span style="font-family:var(--fm);color:var(--acc2);font-size:8pt">{i:02d}</span> &nbsp;{a}</div>' for i, a in enumerate(ag, 1)) + '</div>', 'Rúbrica ES03')


def caso_c():
    def qr(img, t, d, u):
        return (f'<div class="card" style="display:flex;gap:4mm;align-items:center"><img src="{img}" style="width:30mm;height:30mm;border:1px solid var(--line);border-radius:4px">'
                f'<div><div class="t">{t}</div><div style="font-size:9pt">{d}</div><code style="font-size:7.4pt">{u}</code></div></div>')
    izq = ('<div class="a"><div class="card" style="font-size:9.6pt"><div class="t">Usuaria</div>Josselyn Toledo, kinesióloga y psicomotricista acuática. '
           'Atiende en el Centro Médico InMotion (factura mensual), a domicilio en San Fernando y la precordillera, en piscina temperada y en su gimnasio. '
           'Anota todo cada noche en el teléfono.</div>'
           f'<h3 style="margin-top:3mm">Desafío (UA1)</h3><div class="quote" style="font-size:12pt">{C.DESAFIO}</div>'
           f'<h3>Propuesta de valor de partida (EV2)</h3><p style="font-size:9.4pt">{C.PDV_EV2}</p></div>')
    der = ('<div class="b"><h3>Prototipos navegables · ábrelos en el celular</h3>'
           + qr('img/qr-profesional.png', 'Vista profesional (v3)', 'La app de Josselyn: ganancia real y por hora, ruta, agenda, proyección y Mi plata.', URL + '/profesional/')
           + '<div style="height:3mm"></div>'
           + qr('img/qr-cliente.png', 'Vista cliente (paciente)', 'Los mensajes que recibe el paciente, simples para personas mayores.', URL + '/cliente/')
           + '<p class="note" style="margin-top:3mm">Datos de ejemplo. Los prototipos no envían mensajes ni guardan datos fuera del dispositivo.</p></div>')
    return slide(head('Caso y punto de partida', 'Josselyn, cuatro lugares de trabajo y ninguna herramienta que los cruce')
                 + f'<div class="col2">{izq}{der}</div>', 'Contexto')


def ruta_c():
    st = [('on', 'S11 · Prototipar', 'SQA, storyboard y mock-up v1.'), ('on', 'S11–S12 · Ciclo 1', 'Uso y estética: 11 tareas, WCAG AA, heurísticas.'),
          ('on', 'S12–S13 · Iterar v2', '12 cambios.'), ('on', 'S13 · Ciclo 2', 'Técnico: 11 pruebas y cobertura.'),
          ('on', 'S13 · Ciclo 3', 'Clienta, Sercotec y docentes (12/11).'), ('on', 'S14 · Iterar v3', '12 cambios del ciclo 3.'), ('pe', 'S15 · Ciclo 4', 'Josselyn y Catalina con la v3.')]
    ch = ''.join(f'<div class="{c}"><b>{t}</b>{d}</div>' for c, t, d in st)
    cards = ('<div class="row" style="margin-top:4mm">'
             '<div class="card"><div class="t">Ciclo 1 · funcional y estético</div>¿Lo usa sin ayuda? ¿Se lee y se toca bien? Tareas, WCAG 2.1 AA, objetivos táctiles y heurísticas de Nielsen.</div>'
             '<div class="card"><div class="t">Ciclo 2 · técnico</div>¿Calcula exacto y resuelve sus necesidades puntuales? Pruebas contra una hoja de referencia, persistencia, privacidad y brechas.</div>'
             '<div class="card"><div class="t">Ciclo 3 · con la clienta</div>¿Calza con su rutina real? Reunión del 12/11: 12 hallazgos que originan la v3.</div>'
             '<div class="card"><div class="t">Ciclo 4 · usuarias</div>¿Lo usa en su celular y le ayuda a decidir? Tareas N1–N10, SUS y precio. <span class="pend">Pendiente</span></div></div>'
             '<p class="note" style="margin-top:4mm"><b>Transparencia.</b> Los ciclos 1 y 2 los ejecutó el equipo como usuarios internos, con scripts reproducibles. '
             'El ciclo 3 usa la transcripción de la reunión real. No inventamos respuestas de personas que aún no participan.</p>')
    return slide(head('Ruta metodológica', 'Cuatro ciclos, cada uno con un foco distinto') + f'<div class="chain">{ch}</div>' + cards, '3.1.1 · 3.1.2')


def ciclo1_c():
    t = C.C1['tasks']; ok = sum(x['ok'] for x in t)
    axe = sum(x['n'] for v in C.C1['axe'].values() for x in v); tg = sum(len(v) for v in C.C1['targets'].values())
    fail = [[f'<b>{x["id"]}</b>', x['name'], f'<span class="ko">{fix(x["obs"])}</span>'] for x in t if not x['ok']]
    hz = [[h, d, f'<b>{sv}</b>'] for h, d, sv in C.HEUR if sv >= 2]
    k = (f'<div class="kpis"><div><div class="v">{ok}/{len(t)}</div><div class="l">tareas sin ayuda (meta ≥ 90 %)</div></div>'
         f'<div><div class="v">{axe}</div><div class="l">errores de contraste WCAG AA</div></div><div><div class="v">{tg}</div><div class="l">botones bajo 44 px</div></div>'
         '<div><div class="v">10–11 px</div><div class="l">letra mínima en etiquetas</div></div></div>')
    return slide(head('3.1.2.3 · Ciclo 1 · ficha y resultados', 'Funciona en lo central; falla en corregir y en accesibilidad', '3.1.2.3')
                 + f'<div class="quote" style="font-size:11pt">{C.FICHA_C1["objetivo"]}</div>' + k
                 + '<div class="col2"><div class="a"><h3>Tareas que fallaron</h3>' + table(['#', 'Tarea', 'Evidencia'], fail, 'sm') + '</div>'
                 + '<div class="b"><h3>Heurísticas con severidad ≥ 2</h3>' + table(['Heurística', 'Hallazgo', 'Sev.'], hz, 'sm') + '</div></div>', '3.1.2')


def iter_v2_c():
    M = C.METAFORA_ITER
    rows = [[f'<b>{i}</b>', c, h] for i, (c, h, r, _) in enumerate(C.CAMBIOS, 1)]
    at = ''.join(f'<span class="chip o">{n}</span>' for n, *_ in M['atributos'])
    izq = (f'<div class="a" style="flex:.8"><div class="k" style="color:var(--ink2)">Antes (EV2)</div><div class="quote" style="font-size:11pt;border-color:#C9C6DA;color:var(--ink2)">{M["antes"]}</div>'
           f'<div class="k">Después (v2)</div><div class="quote" style="font-size:11pt">{M["despues"]}</div><p style="font-size:8.6pt">{M["porque"]}</p><div>{at}</div>'
           '<div class="kpis" style="margin-top:4mm"><div><div class="v ok">11/11</div><div class="l">tareas en v2</div></div><div><div class="v ok">0</div><div class="l">errores AA</div></div></div></div>')
    return slide(head('3.1.3.1 · Iteración v2 · metáfora y ajustes', 'Del tablero al copiloto, y 12 cambios medidos', '3.1.3.1')
                 + f'<div class="col2">{izq}<div class="b">{table(["#", "Cambio en v2", "Hallazgo del ciclo 1"], rows, "sm xs")}</div></div>', '3.1.3')


def ciclo2_c():
    pr = C.C2['pruebas']
    br = [[f'<b>{b}</b>', t, f'<span class="chip {"o" if "MVP" in f or "Inm" in f else ""}">{f}</span>'] for b, t, d, f in C.BRECHAS]
    cnt = {k: sum(1 for x in C.COBERTURA if x[2].startswith(k)) for k in ('Cumple', 'Parcial', 'Simulado')}
    k = (f'<div class="kpis"><div><div class="v ok">{sum(p["ok"] for p in pr)}/{len(pr)}</div><div class="l">pruebas técnicas aprobadas</div></div>'
         '<div><div class="v ok">$0</div><div class="l">diferencia con la hoja de referencia</div></div><div><div class="v ok">11</div><div class="l">toques para cerrar el día (antes ~60 min)</div></div>'
         f'<div><div class="v">{cnt["Cumple"]} · {cnt["Parcial"]} · {cnt["Simulado"]}</div><div class="l">requerimientos que cumplen · parciales · simulado</div></div></div>')
    return slide(head('3.1.3.4 · Ciclo 2 · técnico', 'Exacto, rápido y sin datos clínicos; lo que falta es integración', '3.1.3.4')
                 + f'<div class="quote" style="font-size:11pt">{C.FICHA_C2["objetivo"]}</div>' + k
                 + '<h3>Brechas técnicas → backlog del MVP</h3>' + table(['#', 'Brecha', 'Cuándo'], br, 'sm'), '3.1.2 · 3.1.3')


def cdm12_c():
    def mini(D, t):
        return (f'<div><h3>{t}</h3><table class="sm xs"><thead><tr><th></th><th>Cualidades</th><th>Debilidades</th><th>Mejoras</th></tr></thead><tbody>'
                f'<tr><td><b>Producto</b></td><td>{ul(D["prod_c"][:3])}</td><td>{ul(D["prod_d"][:3])}</td><td>{ul(D["prod_m"][:3])}</td></tr>'
                f'<tr><td><b>Propuesta de valor</b></td><td>{ul(D["pdv_c"])}</td><td>{ul(D["pdv_d"])}</td><td>{ul(D["pdv_m"])}</td></tr></tbody></table></div>')
    return slide(head('3.1.2.4 · Matrices CDM de los ciclos internos', 'De problemas de uso a problemas de integración', '3.1.2.4')
                 + f'<div class="row" style="gap:5mm">{mini(C.CDM_C1, "Ciclo 1 · prototipo v1")}{mini(C.CDM_C2, "Ciclo 2 · prototipo v2")}</div>', '3.1.2 · 3.1.3')


def mock_v3_c():
    blk = ''.join(pair(a, b, t, d, 96, 'v2', 'v3') for a, b, t, d in (C.MOCK_V2V3[0], C.MOCK_V2V3[2]))
    return slide(head('3.1.3.3 · Mock-up iterado', 'Versión 2 → versión 3', '3.1.3.3') + f'<div class="pairs">{blk}</div>', '3.1.3')


def cambios_verif_c():
    rows = [[f'<b>{i}</b>', c, h, f'<span class="{"ok" if e.startswith("Funcional") else "pa"}">{e}</span>'] for i, (c, h, r, _, e) in enumerate(C.CAMBIOS_V3, 1)]
    nt = [x for x in C.V3_TASKS if x['id'].startswith('N')]
    k = ('<div class="kpis"><div><div class="v ok">11/11</div><div class="l">tareas base (regresión)</div></div>'
         f'<div><div class="v ok">{sum(x["ok"] for x in nt)}/{len(nt)}</div><div class="l">tareas nuevas, una por cambio</div></div>'
         f'<div><div class="v ok">{C.V3_CALC_OK}/{len(C.R3["calculos"])}</div><div class="l">cálculos idénticos a la referencia</div></div>'
         f'<div><div class="v ok">{C.V3_AXE} · {C.V3_TARGETS}</div><div class="l">errores WCAG AA · botones bajo 44 px</div></div></div>')
    return slide(head('3.1.3.3 · Ajustes fundamentados y verificación v3', 'Cada cambio responde a la clienta, y funciona', '3.1.3.3')
                 + k + table(['#', 'Cambio en v3', 'Hallazgo', 'Estado'], rows, 'sm xs')
                 + '<p class="note" style="margin-top:2mm">Verificación interna reproducible (<code>iteracion-v3/verificar_v3.js</code>): confirma que nada se rompió y que lo nuevo calcula bien. La validación de uso es el ciclo 4.</p>', '3.1.2 · 3.1.3')


def usuarios_c():
    hip = ''.join(f'<tr><td><b>{h}</b></td><td>{p}</td><td>{t}</td></tr>' for h, p, t, _, c, _ in K.HIP)
    ph = phones([(PAC + '01_recordatorio_a.png', 'M1 · Recordatorio', 'Llego cerca de las 12:30'), (PAC + '02_voy_en_camino_a.png', 'M2 · Voy en camino', 'Hora exacta'),
                 (PAC + '03_pago_comprobante_a.png', 'M3 · Pago', 'Copia al familiar'), (PAC + '04_clase_grupal_a.png', 'M4 · Clase grupal', 'Las Cabras')], h=86)
    izq = (f'<div class="a">{ph}<p class="note" style="margin-top:2mm">Vista paciente v2 para personas mayores: un mensaje = una decisión, letra de 20 px, '
           'botones de 56 px, trato de “usted” y 0 errores WCAG AA.</p></div>')
    der = (f'<div class="b" style="flex:.8"><table class="sm xs"><thead><tr><th>#</th><th>Público</th><th>Hipótesis</th></tr></thead><tbody>{hip}</tbody></table>'
           '<div class="card" style="margin-top:2mm;font-size:8.6pt"><div class="t">Kit (20 págs.)</div>9 perfiles · guiones A (kines), B (pacientes) y C (contadora) · '
           'consentimiento (Ley 21.719) · SUS · matriz de decisión. Resultados <span class="pend">pendientes</span>.</div></div>')
    return slide(head('Ciclo 4 · usuarias y pacientes', 'Kit de testeo y vista paciente: quien usa la app y quien vive sus efectos')
                 + f'<div class="col2">{izq}{der}</div>', '3.1.2 · 3.1.5')


def pestal_c():
    tr = ''.join(f'<tr><td><b style="font-family:var(--fd);font-size:13pt;font-weight:400">{n.upper()}</b></td><td>{p["f"]}</td><td>{p["o"]}</td><td>{p["a"]}</td></tr>' for n, o, p in C.PESTAL)
    return slide(head('3.1.4.1 · Matriz PESTAL profundizada', 'Del contexto de la UA1 a la evidencia del prototipo', '3.1.4.1')
                 + f'<table class="sm xs" style="font-size:7.4pt"><thead><tr><th style="width:11%">Factor</th><th>Factor profundizado</th><th>Oportunidad</th><th>Amenaza</th></tr></thead><tbody>{tr}</tbody></table>', '3.1.4')


def arte_c():
    dot = {2: '<span class="d2">●</span>', 1: '<span class="d1">◐</span>', 0: '<span class="d0">○</span>'}
    rows = ''.join(f'<tr class="{"me" if "Copiloto" in n else ""}"><td>{n}</td>' + ''.join(f'<td>{dot[v]}</td>' for v in vs) + '</tr>' for n, vs in C.ARTE)
    tr = ''.join(f'<li><b>{t}.</b> {r}</li>' for t, d, r in C.TENDENCIAS)
    izq = (f'<div class="a"><table class="mat sm xs"><thead><tr><th>Solución</th>{"".join(f"<th>{v}</th>" for v in C.ARTE_VARS)}</tr></thead><tbody>{rows}</tbody></table>'
           '<p class="note" style="margin-top:2mm">● cubre · ◐ parcial · ○ no cubre. Antecedentes revisados en sus sitios oficiales (UA1). Copiloto Kine se evalúa por lo que hace hoy.</p></div>')
    der = f'<div class="b" style="flex:.75"><h3>Tendencias y cómo responde</h3><ul style="font-size:8.3pt">{tr}</ul></div>'
    return slide(head('3.1.4 · Estado del arte y tendencias', 'Nadie cruza agenda, costos por atención, tiempo de viaje e impuestos')
                 + f'<div class="col2">{izq}{der}</div>', '3.1.4')


def sost_gest_c():
    w = C.GANTT_W3
    rows = ''.join(f'<tr><td>{t}</td>' + ''.join(f'<td class="{m.get(x, "")}"></td>' for x in w) + '</tr>' for t, m in C.GANTT_V3)
    big = 'font-family:var(--fd);font-size:24pt;color:var(--acc2);line-height:1.05'
    cards = ('<div class="row">'
             f'<div class="card"><div class="t">Económico</div><div style="{big}">Ganancia por hora</div>Por canal, tarifa por tramo y clase grupal para los meses bajos; retención configurable (Ley 21.133).</div>'
             f'<div class="card"><div class="t">Social</div><div style="{big}">~1 h → 1 min</div>Cierre del día sin anotar de noche; accesibilidad AA y vista para personas mayores; sin datos de salud (Ley 21.719).</div>'
             f'<div class="card"><div class="t">Ambiental</div><div style="{big}">−12 km / día</div>Ruta sugerida en el día de ejemplo de San Fernando (41 vs. 53 km) y tiempo de viaje visible.</div></div>')
    roles = table(['Integrante', 'Rol'], [('Claudia Cifuentes', 'Moderación'), ('Néstor Rivera', 'Prototipo y tareas'), ('Francisco Ahumada', 'Registro y CDM'), ('Benjamín Vera Yáñez', 'Secretario técnico')], 'sm')
    gantt = f'<table class="gantt"><thead><tr><th>Actividad</th>{"".join(f"<th>{x}</th>" for x in w)}</tr></thead><tbody>{rows}</tbody></table>'
    return slide(head('Enfoque sostenible y gestión de la fase', 'Económico, social y ambiental, con números') + cards
                 + f'<div class="col2" style="margin-top:4mm"><div class="a">{gantt}</div><div class="b" style="flex:.6">{roles}</div></div>', '3.1.2 · Bitácora')


# ---------------------------------------------------------------- ensamblado
HEAD = '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Evaluación 3 — Prototipado y testeo</title><link rel="stylesheet" href="pres.css"></head><body>'
W, H = 960, 540


def render(body, name):
    path = os.path.join(HERE, name)
    open(path, 'w', encoding='utf-8').write(HEAD + body + '</body></html>')
    return HTML(path, base_url=HERE).write_pdf()


def anexo_slide(doc, title, src, clip=None, idx=0, total=1):
    """Monta una plantilla oficial sobre una diapositiva 16:9 con encabezado."""
    p = doc.new_page(width=W, height=H)
    p.draw_rect(fitz.Rect(0, 0, W, H), color=None, fill=(1, 1, 1))
    p.draw_rect(fitz.Rect(0, 0, 6, H), color=None, fill=(1, 0.42, 0.21))
    anexo_u3.fonts(p)
    p.insert_text((30, 28), 'ANEXO · PLANTILLA OFICIAL', fontname='fmono', fontsize=7.5, color=(0.76, 0.25, 0.05))
    p.insert_text((30, 46), anexo_u3.T.clean(title) + (f'  ({idx}/{total})' if total > 1 else ''), fontname='fb', fontsize=13, color=(0.07, 0.06, 0.12))
    r = src[0].rect if clip is None else clip
    avail = fitz.Rect(30, 58, W - 24, H - 14)
    sc = min(avail.width / r.width, avail.height / r.height)
    w, h = r.width * sc, r.height * sc
    tgt = fitz.Rect(avail.x0 + (avail.width - w) / 2, avail.y0, avail.x0 + (avail.width - w) / 2 + w, avail.y0 + h)
    p.show_pdf_page(tgt, src, 0, clip=clip)
    p.draw_rect(tgt, color=(0.89, 0.88, 0.94), width=0.6)


if __name__ == '__main__':
    body = (portada() + criterios_c() + caso_c() + ruta_c() + sqa()
            + storyboard_v1() + mock_v1() + ciclo1_c() + iter_v2_c() + mock_it() + ciclo2_c() + cdm12_c()
            + ficha3() + retro_rf() + retro_sug() + compara() + cdm_slide(C.CDM_C3, 'Ciclo 3 · clienta, Sercotec y docentes (prototipo v2)', '3.1.2.4', '3.1.2 · 3.1.3')
            + salto_v3() + metafora_v3() + storyboard_v3() + mock_v3_c() + mock_v3_b() + cambios_verif_c() + ficha4() + usuarios_c()
            + costeo() + pdv() + pestal_c() + arte_c() + pertinencia() + sost_gest_c() + conclusiones() + referencias())
    main = fitz.open(stream=render(body, 'Evaluacion3_Presentacion_Prototipado.html'), filetype='pdf')
    anx = [x for x in anexo_u3.build() if any(k in x[0] for k in ('ciclo 3', 'prototipo v3', 'ciclo 4', 'PESTAL'))]
    titles = [t for t, _ in anx]
    main.insert_pdf(fitz.open(stream=render(div_anexo(titles), '_div.html'), filetype='pdf'))
    for t, d in anx:
        if d[0].rect.height > 1000:  # PESTAL vertical: en dos mitades legibles
            r = d[0].rect
            anexo_slide(main, t, d, fitz.Rect(0, 0, r.width, 908), 1, 2)
            anexo_slide(main, t, d, fitz.Rect(0, 908, r.width, r.height), 2, 2)
        else:
            anexo_slide(main, t, d)
    N[0] = main.page_count
    main.insert_pdf(fitz.open(stream=render(cierre(), '_cierre.html'), filetype='pdf'))
    for f in ('_div.html', '_cierre.html'):
        os.remove(os.path.join(HERE, f))
    main.save(os.path.join(HERE, 'Evaluacion3_Presentacion_Prototipado.pdf'), garbage=3, deflate=True)
    print('ok', main.page_count, 'diapositivas')
