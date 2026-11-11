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
sys.path.insert(0, os.path.join(HERE, '..', 'testeo'))
import build_kit as K  # noqa: E402

N = [0]
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


def phones(items, crop=False):
    out = ''
    for it in items:
        src, t = it[0], it[1]
        sub = f'<span>{it[2]}</span>' if len(it) > 2 else ''
        img = f'<div class="crop"><img src="{src}"></div>' if crop else f'<img src="{src}">'
        out += f'<figure>{img}<figcaption><b>{t}</b>{sub}</figcaption></figure>'
    return f'<div class="phones">{out}</div>'


# ---------------------------------------------------------------- diapositivas
def portada():
    return slide(f'''<img class="hero" src="img/01-portada.jpg"><div class="z" style="margin-top:6mm">
<div class="k">Innovación y Emprendimiento III · FGIE03 · INACAP Rancagua</div>
<div class="big" style="margin-top:6mm">EVALUACIÓN N°3<br><em>PROTOTIPADO</em><br>Y TESTEO</div>
<div style="font-family:var(--fd);font-size:22pt;color:#FF8A4C;margin-top:4mm;letter-spacing:.03em">COPILOTO KINE · CASO JOSELYN TOLEDO</div>
<p class="lead" style="max-width:150mm;margin-top:3mm">Del storyboard al prototipo navegable, dos ciclos de testeo y un kit para validar con usuarias, pacientes y expertos.</p>
<div style="margin-top:9mm;font-size:10pt"><b>Francisco Ahumada · Claudia Cifuentes · Néstor Rivera · Benjamín Vera Yáñez</b><br>
<span style="font-family:var(--fm);font-size:8pt;letter-spacing:.1em;color:#9B98B8">PROFESOR: ROBERTO ESCOBAR DONOSO · DISEÑO DIGITAL · NOVIEMBRE 2026</span></div></div>''', cls='dark solid')


def criterios():
    cr = [('3.1.1', 15, 'Uso de herramientas metodológicas para prototipar y testear', 'SQA · storyboard · mock-up · fichas · CDM'),
          ('3.1.2', 20, 'Prototipo validado en más de un ciclo, con enfoque sostenible', 'Ciclo 1 funcional/estético · ciclo 2 técnico · kit con usuarios'),
          ('3.1.3', 15, 'Ajusta el prototipo de forma fundamentada', '12 cambios trazados a hallazgos y requerimientos'),
          ('3.1.4', 20, 'Estado del arte y tendencias', 'PESTAL profundizada · matriz de antecedentes · 6 tendencias'),
          ('3.1.5', 30, 'Pertinencia de la propuesta de valor', 'Propuesta iterada contrastada con problema, mercado y evidencia')]
    cards = ''.join(f'<div><div class="c">CRITERIO {c}</div><div class="p">{p}<small> pts</small></div><div style="margin-top:1.5mm"><b>{t}</b></div><div class="w">{w}</div></div>' for c, p, t, w in cr)
    ag = ['Punto de partida y ruta', 'Herramientas U3: SQA, storyboard y mock-up', 'Ciclo 1 · uso y estética', 'Iteración v2', 'Ciclo 2 · técnico',
          'Validación con usuarios: kit de testeo', 'Propuesta de valor iterada', 'PESTAL, estado del arte y tendencias', 'Pertinencia, sostenibilidad y gestión', 'Anexo: plantillas oficiales']
    return slide(head('Qué presentamos', 'Agenda y criterios de evaluación') + f'<div class="cri">{cards}</div>'
                 + f'<div style="margin-top:6mm;columns:2;font-size:10pt">' + ''.join(f'<div style="margin-bottom:1.6mm"><span style="font-family:var(--fm);color:var(--acc2);font-size:8pt">{i:02d}</span> &nbsp;{a}</div>' for i, a in enumerate(ag, 1)) + '</div>', 'Rúbrica ES03')


def partida():
    return slide(head('Punto de partida · UA1 y UA2', 'El problema y la propuesta que llegamos a probar') + f'''
<div class="col2"><div class="a"><h3>Desafío (UA1)</h3><div class="quote" style="font-size:14pt">{C.DESAFIO}</div>
<h3>Propuesta de valor (EV2)</h3><p style="font-size:10pt">{C.PDV_EV2}</p>
<div><span class="chip o">Anticipador</span><span class="chip o">Legible de un vistazo</span><span class="chip o">Automático</span><span class="chip o">Sostenible</span><span class="chip">Requerimientos R1–R13</span></div></div>
<div class="b"><img src="img/02-caso.jpg" style="width:100%;border-radius:8px;border:1px solid var(--line)">
<div class="card" style="margin-top:3mm;font-size:9pt"><div class="t">Usuaria</div>Joselyn Toledo, kinesióloga independiente: Centro Médico InMotion (70/30) + domicilios en Rancagua y Machalí.
Cuadra ingresos en Excel de noche y no sabe cuánto gana de verdad.</div></div></div>''', 'Contexto')


def ruta():
    st = [('on', 'S11 · Prototipar', 'SQA, storyboard y mock-up v1 con la propuesta de valor.'),
          ('on', 'S11–S12 · Ciclo 1', 'Testeo funcional y estético: 11 tareas, WCAG AA, heurísticas.'),
          ('on', 'S12 · CDM 1', 'Cualidades, debilidades y mejoras → backlog v2.'),
          ('on', 'S12–S13 · Iterar', 'Metáfora, storyboard y mock-up v2: 12 cambios.'),
          ('on', 'S13 · Ciclo 2', 'Verificación técnica: 11 pruebas + cobertura R1–R13.'),
          ('pe', 'S13–S14 · Usuarios', 'Kit de testeo: kinesiólogas, 6 perfiles de pacientes y contadora.')]
    ch = ''.join(f'<div class="{c}"><b>{t}</b>{d}</div>' for c, t, d in st)
    return slide(head('Ruta metodológica', 'Dos ciclos con focos distintos y uno preparado con usuarios') + f'<div class="chain">{ch}</div>' + f'''
<div class="row" style="margin-top:4mm"><div class="card"><div class="t">Ciclo 1 · funcional y estético</div>¿Puede una kinesióloga hacer su día sin ayuda? ¿Se lee, se toca y se entiende? Medido con tareas, auditoría WCAG 2.1 AA, objetivos táctiles, tamaño de letra y heurísticas de Nielsen.</div>
<div class="card"><div class="t">Ciclo 2 · técnico</div>¿Resuelve con exactitud sus necesidades puntuales? Cálculo por atención, cierre del día, persistencia, costos editables, exportación sin datos clínicos, rendimiento y brechas.</div>
<div class="card"><div class="t">Ciclo con usuarios · preparado</div>Kit completo con 10 hipótesis y 9 perfiles. Se suma la retroalimentación de la emprendedora (reunión del jueves 12/11) antes de aplicar las sesiones.</div></div>
<p class="note" style="margin-top:4mm"><b>Transparencia.</b> Los ciclos 1 y 2 los ejecutó el equipo como usuarios internos (lo permite el toolkit) con scripts reproducibles en <code>unidad-3/ciclo1</code> y <code>ciclo2</code>. Los resultados con usuarias y pacientes reales se marcan como pendientes: no inventamos respuestas de personas reales.</p>''', '3.1.1 · 3.1.2')


def sqa():
    cols = ''.join(f'<div class="card"><div class="t">{t}</div>{ul(items)}</div>' for t, items in C.SQA)
    return slide(head('3.1.1.1 · Evaluación diagnóstica', 'Tabla SQA', '3.1.1.1') + f'<div class="row">{cols}</div>', '3.1.1')


def scenes(sc, mode):
    out = ''
    for i, (t, img, kind, txt, a, b) in enumerate(sc, 1):
        la, lb = ('Producto', 'Propuesta de valor') if mode == 'v1' else ('Cualidad', 'Mejora incorporada')
        out += (f'<div class="sc"><div class="im {"w" if kind == "wide" else ""}"><img src="{img}"></div><div class="tx"><div class="n">Escena {i}</div>'
                f'<div class="h">{t}</div><div>{txt}</div><div class="c p"><b>{la}</b>{a}</div><div class="c v"><b>{lb}</b>{b}</div></div></div>')
    return f'<div class="sb">{out}</div>'


def storyboard_v1():
    return slide(head('3.1.2.1 · Storyboard con propuesta de valor', 'Un día de Joselyn con Copiloto Kine', '3.1.2.1') + scenes(C.SCENES, 'v1'), '3.1.1 · 3.1.5')


def mock_v1():
    return slide(head('3.1.2.2 · Mock-up con propuesta de valor', 'Prototipo v1 navegable en el celular', '3.1.2.2')
                 + phones([(f, t, f'{d}<br><i style="color:var(--acc2)">{a}</i>') for t, f, d, a in C.MOCK_V1], crop=True)
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
    blk = ''
    for a, b, t, d in pares:
        blk += f'''<div style="flex:1"><div class="ba"><figure style="flex:1"><div class="crop" style="height:96mm"><img src="{V1 + a}" style="width:100%"></div></figure>
<div class="ar">→</div><figure style="flex:1"><div class="crop" style="height:96mm;border-color:var(--acc)"><img src="{V2 + b}" style="width:100%"></div></figure></div>
<div style="text-align:center;margin-top:2mm"><b>{t}</b><br><span style="font-size:8.4pt;color:var(--ink2)">{d}</span></div></div>'''
    return slide(head('3.1.3.3 · Mock-up iterado', 'Versión 1 → versión 2', '3.1.3.3') + f'<div style="display:flex;gap:7mm">{blk}</div>', '3.1.3')


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
<div class="b"><div class="card"><div class="t">Qué incluye el kit (19 págs.)</div><ul><li>Plan, hipótesis, muestra y calendario</li><li>9 perfiles de participantes</li><li>Guiones A (kines), B (pacientes) y C (contadora)</li>
<li>Consentimiento informado (Ley 21.719)</li><li>Pautas de observación, SUS y encuesta de pacientes</li><li>Matriz de consolidación con reglas de decisión</li><li>Invitaciones listas para WhatsApp</li></ul></div>
<div class="card" style="margin-top:3mm"><div class="t">Estado</div>Resultados <span class="pend">Pendientes de sesión</span>. Entrada previa: retroalimentación de la emprendedora en la reunión del jueves 12/11 (grabación del profesor).</div></div></div>''', '3.1.2 · 3.1.5')


def perfiles():
    cards = ''.join(f'<div class="pf t{p["tipo"]}"><div class="top"><div class="cd">{p["c"]}</div><div><b>{p["n"]}</b><br><span style="color:var(--ink2)">{p["t"]}</span></div></div>{p["d"]}<div class="h">{p["h"]} · {p["m"]}</div></div>' for p in K.PERF)
    return slide(head('Validación con usuarios · públicos', 'Nueve perfiles: quien usa la app y quien vive sus efectos')
                 + f'<div class="pfs">{cards}</div><p style="font-size:8.2pt;color:var(--ink2);margin-top:2.5mm">K1 y K2 son participantes reales del proyecto (UA1). Los pacientes entre comillas son perfiles a reclutar: se invita a pacientes de Joselyn solo si ella lo propone, o a personas del entorno del equipo que calcen con el perfil. No se registran diagnósticos.</p>', '3.1.2')


def paciente():
    return slide(head('Nuevo estímulo · vista paciente', 'Lo que recibe el paciente cuando su kine usa Copiloto Kine') + '<div class="col2"><div class="a">'
                 + phones([(PAC + '01_recordatorio.png', 'M1 · Recordatorio', 'Ventana de 30 min (H5)'), (PAC + '02_voy_en_camino.png', 'M2 · Voy en camino', 'Tranquilidad (H6)'),
                           (PAC + '03_comprobante.png', 'M3 · Comprobante', 'Sin diagnóstico (H7)'), (PAC + '04_hora_liberada.png', 'M4 · Hora liberada', 'Precio preferente (H10)')], crop=True)
                 + '''</div><div class="b" style="flex:.55"><div class="card"><div class="t">Por qué</div>La ruta sugerida (−7 km/día) solo funciona si el paciente acepta una
ventana de llegada. Es la hipótesis más riesgosa del modelo y no se puede probar con kinesiólogas.</div>
<div class="card" style="margin-top:3mm"><div class="t">Accesibilidad</div>Botón “Letra grande” para adultos mayores, botones de 44 px y 0 errores WCAG AA en los 4 mensajes.</div>
<div class="card" style="margin-top:3mm"><div class="t">Archivo</div><code style="font-size:7.5pt">prototipo/vista-paciente.html</code></div></div></div>''', '3.1.2')


def pdv():
    return slide(f'''<img class="pvphone" src="../prototipo/capturas_v2/01_tablero.png"><div class="z" style="max-width:200mm;margin-top:4mm">
<div class="k">Propuesta de valor iterada · 3.1.5</div>
<div class="big" style="font-size:46pt;margin:4mm 0 5mm">DE COPILOTO FINANCIERO<br>A <em>COPILOTO DE SU DÍA</em>.</div>
<div class="pvq">{C.PDV_ITER}</div>
<div style="margin-top:6mm;font-size:9.5pt;color:#C9C6DA"><b style="color:#fff">Qué cambió:</b> la ruta pasa al centro (ciclo 1), la promesa “se conecta a la agenda” sale hasta que la integración exista (B1) y se agrega un resultado verificable: entregar los números a la contadora sin Excel (P6).</div>
<div class="tags" style="margin-top:5mm"><span>Anticipador</span><span>Claro</span><span>Automático y corregible</span><span>Sostenible</span></div></div>''', '3.1.5', 'dark')


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
                 + '<p style="font-size:8.6pt;color:var(--ink2)">● cubre · ◐ parcial · ○ no cubre. Antecedentes de la UA1 (AgendaPro, Encuadrado, Reservo, Medilink, Cal.com, Cliniko, Jane App, Nubox) revisados en sus sitios oficiales; el prototipo v2 se evalúa con lo que efectivamente hace hoy (agenda e itinerario simulados = ◐).</p>', '3.1.4')


def tendencias():
    rows = [[f'<b>{t}</b>', d, r] for t, d, r in C.TENDENCIAS]
    return slide(head('3.1.4 · Tendencias', 'Seis tendencias que el prototipo ya incorpora') + table(['Tendencia', 'Qué está pasando', 'Cómo responde Copiloto Kine v2'], rows), '3.1.4')


def pertinencia():
    rows = [[f'<b>{a}</b>', b, c] for a, b, c in C.PERTINENCIA]
    return slide(head('3.1.5 · Pertinencia de la propuesta de valor', 'La propuesta responde al problema, al mercado y a la evidencia')
                 + table(['Dimensión', 'Lo que sabemos', 'Cómo responde la propuesta iterada'], rows)
                 + '<div class="quote" style="font-size:14pt;margin-top:4mm">Pertinente hoy en lo que el prototipo demuestra; la validación con Joselyn, Catalina y pacientes decidirá precio, ventana horaria y alcance del MVP.</div>', '3.1.5')


def sostenibilidad():
    return slide(head('Enfoque sostenible', 'Económico, social y ambiental, con números') + '''<div class="row">
<div class="card"><div class="t">Económico</div><div class="kpis" style="margin:1mm 0 2mm"><div style="border:none;padding:0"><div class="v">+$570.000</div><div class="l">acciones que cubren enero y febrero</div></div></div>
Ganancia real por atención visible; retención configurable ante el alza de la Ley 21.133 (15,25 % → 16 % → 17 %).</div>
<div class="card"><div class="t">Social</div><div class="kpis" style="margin:1mm 0 2mm"><div style="border:none;padding:0"><div class="v">~1 h → 11 toques</div><div class="l">cierre del día sin trabajo nocturno</div></div></div>
Accesibilidad WCAG AA, letra grande para adultos mayores y datos de salud fuera del sistema (Ley 21.719).</div>
<div class="card"><div class="t">Ambiental</div><div class="kpis" style="margin:1mm 0 2mm"><div style="border:none;padding:0"><div class="v">−140 km/mes</div><div class="l">≈ 10 l de bencina · ≈ 23 kg CO2</div></div></div>
Ruta sugerida: 20 vs. 27 km en el día de ejemplo (−26 %). Estimación del equipo con 20 días de domicilios, 14 km/l y 2,3 kg CO2/l.</div></div>''', '3.1.2')


def gestion():
    w = C.GANTT_W
    rows = ''.join(f'<tr><td>{t}</td>' + ''.join(f'<td class="{m.get(x, "")}"></td>' for x in w) + '</tr>' for t, m in C.GANTT)
    roles = [('Claudia Cifuentes', 'Moderación de sesiones'), ('Néstor Rivera', 'Ejecución de tareas y prototipo'), ('Francisco Ahumada', 'Registro y CDM'), ('Benjamín Vera Yáñez', 'Secretario técnico: consolidación y auditoría técnica')]
    return slide(head('Gestión de la fase · bitácora', 'Organización del tiempo y roles') + f'''<div class="col2"><div class="a">
<table class="gantt"><thead><tr><th>Actividad</th>{"".join(f"<th>{x}</th>" for x in w)}</tr></thead><tbody>{rows}</tbody></table></div>
<div class="b"><h3>Roles</h3>{table(["Integrante", "Rol"], roles, "sm")}<h3 style="margin-top:3mm">Evidencias en el repositorio</h3>
<p style="font-size:8.6pt"><code>unidad-3/prototipo</code> (v1, v2, vista paciente, capturas) · <code>ciclo1</code> y <code>ciclo2</code> (scripts y resultados JSON) · <code>testeo</code> (kit) · bitácora U3.</p></div></div>''', 'Bitácora')


def conclusiones():
    return slide(head('Cierre', 'Conclusiones y próximos pasos') + '''<div class="row">
<div class="card"><div class="t">Aprendimos</div><ul><li>Medir tareas y accesibilidad da evidencia más útil que preguntar si “gusta”.</li><li>“Automático” sin “corregible” genera registros falsos.</li><li>La ruta es tan valiosa como el tablero: la metáfora se movió hacia el copiloto.</li><li>El paciente también es usuario: sin su ventana horaria no hay ruta optimizada.</li></ul></div>
<div class="card"><div class="t">Logramos</div><ul><li>Prototipo v2 navegable: 11/11 tareas, 0 errores WCAG AA.</li><li>11/11 pruebas técnicas; cálculo exacto y exportación sin datos clínicos.</li><li>9 de 13 requerimientos cumplidos y 7 brechas priorizadas.</li><li>Kit de testeo con 10 hipótesis y 9 perfiles.</li></ul></div>
<div class="card"><div class="t">Sigue</div><ul><li><b>Jue 12/11:</b> integrar la retroalimentación de la emprendedora.</li><li><b>17–19/11:</b> sesiones con Joselyn, Catalina, pacientes y contadora.</li><li><b>20/11:</b> consolidar, CDM con usuarios y decisiones v3.</li><li><b>UA4:</b> MVP con agenda real, respaldo en la nube y enlace wa.me.</li></ul></div></div>''', 'Cierre')


def referencias():
    refs = ['INACAP (2026). Toolkit y manual del estudiante, Unidad 3 · Innovación y Emprendimiento III (FGIE03).',
            'Nielsen, J. (1994). 10 Usability Heuristics for User Interface Design. Nielsen Norman Group.',
            'W3C (2018). Web Content Accessibility Guidelines (WCAG) 2.1. Deque Systems, axe-core 4.10.',
            'Brooke, J. (1996). SUS: A “quick and dirty” usability scale. Usability Evaluation in Industry.',
            'Ley 21.133 (2019). Incorpora a trabajadores independientes a la seguridad social. Biblioteca del Congreso Nacional.',
            'Ley 21.719 (2024). Regula la protección y el tratamiento de los datos personales. Biblioteca del Congreso Nacional.',
            'Ley 20.584 (2012). Derechos y deberes de los pacientes. Biblioteca del Congreso Nacional.',
            'Sitios oficiales de AgendaPro, Encuadrado, Reservo, Medilink, Cal.com, Cliniko, Jane App y Nubox (consulta UA1).',
            'Equipo (2026). Informes EV1 y EV2, entrevistas a Joselyn Toledo y Catalina (UA1).']
    return slide(head('Fuentes', 'Referencias') + '<div style="font-size:9.6pt;columns:2;column-gap:10mm">' + ''.join(f'<p>{r}</p>' for r in refs) + '</div>', 'Ref.')


def div_anexo(titles):
    li = ''.join(f'<div style="border-bottom:1px solid #2A2640;padding:1.8mm 0;font-size:10pt">{t}</div>' for t in titles)
    return slide(f'''<div class="k" style="margin-top:6mm">Anexo</div><div class="big" style="font-size:54pt;margin:4mm 0 6mm">PLANTILLAS OFICIALES<br><em>TOOLKIT UA3</em></div>
<div style="max-width:220mm">{li}</div>''', 'Anexo', 'dark')


def cierre():
    return slide('''<div class="k" style="margin-top:14mm">Conclusión</div>
<div class="big" style="font-size:52pt;margin-top:5mm;max-width:270mm">PROBAR CON EVIDENCIA, ITERAR CON CRITERIO Y <em>LLEVARLO A LAS PERSONAS</em>.</div>
<p style="font-size:14pt;max-width:220mm;margin-top:6mm">Copiloto Kine está listo para su ciclo con usuarias reales. Gracias.</p>''', 'Gracias', 'orange')


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
    pe = C.PESTAL
    body = (portada() + criterios() + partida() + ruta() + sqa() + storyboard_v1() + mock_v1() + ficha1() + res1() + heur()
            + cdm_slide(C.CDM_C1, 'Ciclo 1 · prototipo v1', '3.1.2.4', '3.1.2') + antes_despues() + metafora() + storyboard_it() + mock_it() + cambios()
            + ficha2() + res2() + cobertura() + brechas() + cdm_slide(C.CDM_C2, 'Ciclo 2 · prototipo v2', '3.1.2.4', '3.1.3')
            + validacion() + perfiles() + paciente() + pdv() + pestal(pe[:3], '1/2') + pestal(pe[3:], '2/2') + arte() + tendencias()
            + pertinencia() + sostenibilidad() + gestion() + conclusiones() + referencias())
    main = fitz.open(stream=render(body, 'Evaluacion3_Presentacion_Prototipado.html'), filetype='pdf')
    anx = anexo_u3.build()
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
