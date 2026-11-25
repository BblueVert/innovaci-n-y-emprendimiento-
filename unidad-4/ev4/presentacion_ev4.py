# Presentación EV4 (16:9, PDF) con el lenguaje visual del proyecto (el mismo de la EV3: pres.css, mockups de iPhone, láminas oscuras).
# Entregable final ES4: incluye links y QR a la vista profesional, la vista cliente y el tablero del toolkit U1–U4.
# Uso: python3 presentacion_ev4.py → entregables/EV4_Presentacion_Copiloto_Kine.pdf
import os
import sys
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
EV3 = os.path.join(HERE, '..', '..', 'unidad-3', 'ev3')
sys.path.insert(0, EV3)
import build_presentacion as B  # noqa: E402  (componentes de la EV3)
import contenido as C3  # noqa: E402
import contenido_u4 as C  # noqa: E402

REL = '../../unidad-4/ev4/'  # rutas de esta carpeta vistas desde ev3 (base_url)
OUT = os.path.join(HERE, 'entregables', 'EV4_Presentacion_Copiloto_Kine.pdf')
TABLERO = 'https://claude.ai/artifact/6kjUvwa7Y9JhZNj7LzP1jv'
FOOT = 'Copiloto Kine · Presentación final EV1–EV4 · INACAP Rancagua'
N = [0]
head, table, ul, phones, dev = B.head, B.table, B.ul, B.phones, B.dev
clp = lambda n: '$' + f'{round(n):,}'.replace(',', '.')  # noqa: E731


def slide(body, crit='', cls=''):
    N[0] += 1
    return (f'<section class="s {cls}">{body}<div class="ft"><span>{FOOT}</span>'
            f'<span><b>{crit}</b>{" · " if crit else ""}{N[0]:02d}</span></div></section>')


def portada():
    return slide(f'''<img class="hero" src="img/01-portada.jpg"><div class="z" style="margin-top:6mm">
<div class="k">Innovación y Emprendimiento III · FGIE03 · INACAP Rancagua</div>
<div class="big" style="margin-top:6mm">PRESENTACIÓN<br><em>FINAL</em><br>EV1 A EV4</div>
<div style="font-family:var(--fd);font-size:22pt;color:#FF8A4C;margin-top:4mm;letter-spacing:.03em">COPILOTO KINE · CASO JOSSELYN TOLEDO</div>
<p class="lead" style="max-width:155mm;margin-top:3mm">{C.LC['pdv']} Diagnóstico, ideación, prototipado y difusión de una solución para kinesiólogas independientes de O’Higgins.</p>
<div style="margin-top:9mm;font-size:10pt"><b>Francisco Ahumada · Claudia Cifuentes · Néstor Rivera · Benjamín Vera Yáñez</b><br>
<span style="font-family:var(--fm);font-size:8pt;letter-spacing:.1em;color:#9B98B8">PROFESOR: ROBERTO ESCOBAR DONOSO · DISEÑO DIGITAL · DICIEMBRE 2026</span></div></div>''', cls='dark solid')


def criterios():
    cr = [('4.1.1', 'Fase de propuesta de valor', 'Recorrido U1–U4 · QQQ · tablero del toolkit'),
          ('4.1.2', 'Factibilidad económica e impacto', 'Lean Canvas · escenarios · impacto en 4 dimensiones'),
          ('4.1.3', 'Propuesta de valor persuasiva', 'Formulario de postulación a fondo concursable'),
          ('4.1.4', 'Comunica la diferenciación', 'Comparativa · guion del pitch de 3½ min'),
          ('4.1.5', 'Sostenibilidad y acciones', 'Evaluación frente al desafío · hoja de ruta · riesgos')]
    cards = ''.join(f'<div><div class="c">CRITERIO {c}</div><div style="margin-top:1.5mm;font-size:11pt"><b>{t}</b></div><div class="w">{w}</div></div>' for c, t, w in cr)
    ag = ['El caso y el problema', 'De la U1 a la U3: cómo llegamos aquí', 'La solución y el prototipo', 'Diferenciación', 'Lean Canvas y factibilidad',
          'Impacto', 'Formulario y guion del pitch', 'Sostenibilidad y acciones futuras', 'Links: prototipo y tablero del toolkit']
    return slide(head('Qué presentamos', 'Agenda y criterios de evaluación') + f'<div class="cri">{cards}</div>'
                 + '<div style="margin-top:6mm;columns:3;font-size:10pt">' + ''.join(f'<div style="margin-bottom:1.8mm"><span style="font-family:var(--fm);color:var(--acc2);font-size:8pt">{i:02d}</span> &nbsp;{a}</div>' for i, a in enumerate(ag, 1)) + '</div>', 'Rúbrica ES04')


def caso():
    return slide(head('Antecedentes de la empresa', 'Una kinesióloga, cuatro lugares de trabajo y ninguna herramienta que los cruce') + f'''
<div class="col2"><div class="a"><div class="row">
<div class="card"><div class="t">Empresa</div>Josselyn Toledo, kinesióloga y psicomotricista acuática independiente.</div>
<div class="card"><div class="t">Ubicación</div>San Fernando y alrededores, Región de O’Higgins: Aguas Buenas, Las Cabras, camino a Roma.</div></div>
<div class="card" style="margin-top:3mm"><div class="t">Actividad</div>Atiende en el Centro Médico InMotion (factura mensual), a domicilio, en una piscina temperada y en su gimnasio.
Su sello es la atención uno a uno: “Yo los trato como a mí me gustase que me tratasen”.</div>
<h3 style="margin-top:4mm">Problemas detectados en el diagnóstico</h3>{ul(["No sabe cuánto gana de verdad ni qué lugar le conviene.", "Registra todo a mano cada noche: cerca de 1 hora.", "El traslado rural no se mide ni se cobra (25–30 min a Aguas Buenas).", "Enero y febrero bajan cerca de 35 % sin un plan."])}</div>
<div class="b"><img src="img/02-caso.jpg" style="width:100%;border-radius:8px;border:1px solid var(--line)"></div></div>''', 'Contexto')


def problema():
    q = [('Cada noche anoto todo… lo que gasto en bencina… cuánto gané en cada sesión.', 'Josselyn, 12/11'),
         ('Me toma una hora actualmente diario.', 'Catalina, kinesióloga'),
         ('Estar ocupado y estar ganando dinero no son lo mismo.', 'asesor financiero')]
    qs = ''.join(f'<div class="quote" style="font-size:12pt;margin-bottom:3mm">“{t}”<div style="font-family:var(--fm);font-size:7.5pt;color:var(--ink2);margin-top:1mm;font-weight:400">— {s}</div></div>' for t, s in q)
    return slide(head('Problema priorizado', 'La agenda y las finanzas viven separadas')
                 + '<div class="kpis"><div><div class="v">~1 h</div><div class="l">diaria de registro manual</div></div><div><div class="v">25–30 min</div><div class="l">por domicilio en precordillera</div></div>'
                 + '<div><div class="v">−35 %</div><div class="l">ingresos en enero y febrero</div></div><div><div class="v">30.050</div><div class="l">kinesiólogos en Chile (Superintendencia de Salud)</div></div></div>'
                 + f'<div class="col2"><div class="a">{qs}</div><div class="b"><div class="card"><div class="t">Insight raíz (UA1)</div>Cada cita agendada es un ingreso que se pierde: hay que reescribirlo a mano, sin descontar comisión, traslado ni impuestos. Sin agenda confiable no hay dato financiero confiable.</div>'
                 + '<div class="card" style="margin-top:3mm"><div class="t">Desafío</div>' + C.DESAFIO + '</div></div></div>', '4.1.1')


def recorrido():
    st = [('on', 'U1 · Diagnóstico', '17 instrumentos: entrevistas, AEIOU, expertos, PESTAL, 8 insights y desafío.'),
          ('on', 'U2 · Ideación', '10 referentes, 13 requerimientos, 60 ideas, metáfora y propuesta de valor.'),
          ('on', 'U3 · Prototipado', 'Prototipo v1 → v2 → v3 y 4 ciclos de testeo, uno con la clienta y Sercotec.'),
          ('on', 'U4 · Difusión', 'Lean Canvas, factibilidad, formulario de postulación y pitch.')]
    ch = ''.join(f'<div class="{c}"><b>{t}</b>{d}</div>' for c, t, d in st)
    qqq = [('Qué veo', ['Un prototipo validado en 4 ciclos', 'Costos, precio y canales definidos', 'Interés de la clienta y de Sercotec']),
           ('Qué no veo', ['Cuántas kinesiólogas pagarían de verdad', 'La integración real con AgendaPro', 'Quién mantiene la app después del curso']),
           ('Qué infiero', ['Un piloto gratis es la mejor prueba de precio', 'El pitch debe partir por el dolor de Josselyn', 'Sercotec es canal de difusión y financiamiento'])]
    cols = ''.join(f'<div class="card"><div class="t">{t}</div>{ul(i)}</div>' for t, i in qqq)
    return slide(head('Ciclo de Innovación INACAP', 'Cuatro unidades, un mismo proyecto') + f'<div class="chain">{ch}</div>'
                 + f'<h3 style="margin-top:5mm">4.1.1.1 · Qué veo, qué no veo, qué infiero (diagnóstica U4)</h3><div class="row">{cols}</div>'
                 + f'<p class="note" style="margin-top:3mm">Todas las plantillas del toolkit, de la U1 a la U4, están en el tablero del proyecto: <b>{TABLERO}</b></p>', '4.1.1')


def solucion():
    M = C3.METAFORA_V3
    at = ''.join(f'<div class="attr"><div class="n">{n}</div><div class="s2">…{s}</div></div>' for n, s, r, tags in M['atributos'])
    return slide(head('La solución', 'Copiloto Kine, el copiloto de la kinesióloga que trabaja en varios lugares') + f'''
<div class="col2"><div class="a"><div class="quote" style="font-size:13pt">{C3.PDV_V3}</div>
<div class="row" style="gap:3mm;flex-wrap:wrap">{at}</div></div>
<div class="b" style="flex:.42;text-align:center">{dev("../prototipo/capturas_v3/02_ganancia_por_hora.png", 120)}</div></div>''', '4.1.3')


def prototipo():
    V3 = C3.V3
    return slide(head('Prototipo v3 navegable', 'Lo que hace, pantalla por pantalla')
                 + phones([(V3 + '05_agenda.png', 'Agenda conectada', 'AgendaPro y clínica'), (V3 + '02_ganancia_por_hora.png', '¿Qué me conviene?', 'Ganancia por hora por canal'),
                           (V3 + '04_paradas_tramos.png', 'Ruta y tramos', 'Tiempo de viaje con valor'), (V3 + '07_clase_grupal.png', 'Clase grupal', 'Punto de equilibrio'),
                           (V3 + '11_cierre_dia.png', 'Cierre del día', 'Reemplaza la nota nocturna')], h=96)
                 + f'<p class="note" style="margin-top:3mm">Validado en 4 ciclos: {C3.V3_OK}/{len(C3.V3_TASKS)} tareas, {C3.V3_CALC_OK}/{len(C3.R3["calculos"])} cálculos exactos y {C3.V3_AXE} errores de accesibilidad WCAG AA. Pruébalo: <b>{C.URL_PRO}</b></p>', '4.1.3 · 4.1.4')


def storyboard():
    return slide(head('Un día con Copiloto Kine', 'Un martes de Josselyn en San Fernando, Aguas Buenas y la piscina') + B.scenes(C3.SCENES_V3, 'it'), '4.1.4')


def diferenciacion():
    dot = {2: '<span class="d2">●</span>', 1: '<span class="d1">◐</span>', 0: '<span class="d0">○</span>'}
    rows = ''.join(f'<tr class="{"me" if "Copiloto" in n else ""}"><td>{n}</td>' + ''.join(f'<td>{dot[v]}</td>' for v in vs) + f'<td style="font-size:7.6pt">{c}</td></tr>' for n, vs, c in C3.COMPARA)
    return slide(head('Diferenciación', 'Las otras propuestas ordenan; Copiloto Kine parte de la agenda y del territorio')
                 + f'<table class="mat big"><thead><tr><th>Propuesta</th>{"".join(f"<th>{v}</th>" for v in C3.COMPARA_CRIT)}<th>Costo para ella</th></tr></thead><tbody>{rows}</tbody></table>'
                 + '<div class="row" style="margin-top:4mm"><div class="card"><div class="t">Frente a las apps</div>AgendaPro, Reservo o Encuadrado agendan; Nubox lleva contabilidad. Ninguna cruza la cita con comisión, traslado y retención chilena.</div>'
                 + '<div class="card"><div class="t">Frente a las planillas</div>Hay que alimentarlas a mano. Copiloto Kine exporta a la misma planilla de la contadora, así que puede convivir con ellas.</div>'
                 + '<div class="card"><div class="t">Ventaja especial</div>Nace del trabajo con una clienta real y su territorio: caminos rurales, cuatro lugares de trabajo y meses bajos.</div></div>', '4.1.4')


def lean():
    return slide(head('4.1.2.1 · Lean Canvas', 'El modelo de negocio en una hoja', '4.1.2.1')
                 + f'<img src="{REL}entregables/4.1.2.1_Lean_Canvas_Copiloto_Kine.png" style="height:124mm;width:auto;display:block;margin:0 auto;border:1px solid var(--line);border-radius:6px">', '4.1.2')


def factibilidad():
    esc = [C.escenario(n) for _, n, _ in C.ESCENARIOS]
    rows = [[f'<b>{n}</b>', e['n'], clp(e['ingresos_mes']), clp(e['margen_mes']), f"{e['margen_pct']} %", clp(e['ingresos_anio'])] for (n, _, _), e in zip(C.ESCENARIOS, esc)]
    sup = [[f'<b>{a}</b>', b, f'<span style="color:var(--ink2)">{c}</span>'] for a, b, c in C.SUPUESTOS]
    return slide(head('Factibilidad económica', 'Se sostiene con pocas usuarias y se paga solo')
                 + '<div class="kpis"><div><div class="v">$9.990</div><div class="l">al mes · piloto gratis 3 meses</div></div><div><div class="v">5</div><div class="l">usuarias cubren la operación (~$48.000/mes)</div></div>'
                 + '<div><div class="v">84 %</div><div class="l">margen bruto con 30 usuarias</div></div><div><div class="v">16×</div><div class="l">valor de vida ($240.000) sobre costo de adquisición ($15.000)</div></div></div>'
                 + '<div class="col2"><div class="a">' + table(['Escenario año 1', 'Usuarias', 'Ingresos/mes', 'Margen/mes', 'Margen', 'Ingresos/año'], rows, 'sm')
                 + '<p class="note" style="margin-top:3mm">Para la usuaria, cobrar el recargo de un solo tramo rural ($3.000–6.000) cubre casi todo el mes de suscripción.</p></div>'
                 + '<div class="b">' + table(['Supuesto', 'Valor', 'Fundamento'], sup, 'sm xs') + '</div></div>', '4.1.2')


def impacto():
    big = {'Económico': '+$24–48 mil', 'Tecnológico': '64 KB', 'Sociocultural': '~1 h/día', 'Medioambiental': '−240 km/mes'}
    cards = ''.join(f'<div class="card"><div class="t">{d}</div><div style="font-family:var(--fd);font-size:26pt;color:var(--acc2);line-height:1;margin:1mm 0 2mm">{big[d]}</div><div style="font-size:9pt">{t}</div></div>' for d, t in C.IMPACTOS)
    return slide(head('Impacto', 'Tecnológico, económico, sociocultural y medioambiental') + f'<div class="row">{cards}</div>'
                 + '<p class="note" style="margin-top:4mm">Estimaciones del equipo con el día de ejemplo del prototipo: recargo por tramo en 8 domicilios rurales al mes; ruta sugerida de 41 vs. 53 km con 20 días de domicilios, 14 km/l y 2,3 kg de CO2 por litro.</p>', '4.1.2 · 4.1.5')


def formulario():
    F = C.FORM
    return slide(head('4.1.3.1 · Formulario de postulación a fondo concursable', 'La propuesta, lista para postular', '4.1.3.1') + f'''
<div class="col2"><div class="a"><div class="card"><div class="t">Título</div><b>{F['titulo']}</b></div>
<div class="card" style="margin-top:3mm"><div class="t">Resumen (165 de 200 palabras)</div><div style="font-size:8.6pt">{F['resumen']}</div></div>
<div class="row" style="margin-top:3mm"><div class="card"><div class="t">ODS</div>{ul(F['ods'])}</div><div class="card"><div class="t">Tipo de solución</div>{F['tipo']}<br><span style="color:var(--ink2);font-size:8.5pt">Nivel de avance: prototipo validado; siguiente paso, MVP.</span></div></div></div>
<div class="b" style="flex:.42"><img src="../../unidad-4/tablero_toolkit/img/u4_form.jpg" style="width:100%;border:1px solid var(--line);border-radius:6px"></div></div>''', '4.1.3')


def guion():
    cards = ''.join(f'<div class="card"><div class="t">{t}</div><div style="font-size:8.6pt;line-height:1.38">{x}</div></div>' for t, x in C.PITCH)
    return slide(head('4.1.3.2 · Guion del pitch (3½ min)', C.PITCH_FRASE, '4.1.3.2') + f'<div class="row" style="align-items:stretch">{cards}</div>', '4.1.4')


def sostenibilidad():
    acc = [[f'<b>{a}</b>', b, f'<span style="color:var(--ink2)">{c}</span>'] for a, b, c in C.ACCIONES]
    rie = [[f'<b>{a}</b>', b] for a, b in C.RIESGOS]
    return slide(head('Sostenibilidad y acciones futuras', 'Del prototipo al piloto y a la postulación a fondos') + f'''
<div class="col2"><div class="a"><div class="card"><div class="t">Frente al desafío</div>El desafío pedía bajar el registro de ~1 h a menos de 30 min diarios. El prototipo cierra un día de 7 atenciones en menos de un minuto; falta verificarlo con la agenda real en el MVP.</div>
<h3 style="margin-top:3mm">Hoja de ruta</h3>{table(["Cuándo", "Acción", "Quién"], acc, "sm")}</div>
<div class="b" style="flex:.8"><h3>Riesgos y cómo los enfrentamos</h3>{table(["Riesgo", "Mitigación"], rie, "sm")}</div></div>''', '4.1.5')


def links():
    cards = [('qr_profesional', 'Prototipo · vista profesional', 'La app de Josselyn: ganancia real y por hora, ruta, agenda y Mi plata.', C.URL_PRO),
             ('qr_cliente', 'Prototipo · vista cliente', 'Los mensajes que recibe el paciente, pensados para personas mayores.', C.URL_CLI),
             ('qr_tablero', 'Tablero del toolkit U1–U4', 'Todas las plantillas del proyecto alrededor de Copiloto Kine (reemplaza el Miro).', TABLERO)]
    out = ''.join(f'<div class="card" style="text-align:center"><img src="{REL}img/{q}.png" style="width:44mm;height:44mm;margin:2mm auto 3mm;display:block">'
                  f'<div class="t">{t}</div><div style="font-size:9pt;margin:1mm 0 2mm">{d}</div><a href="{u}" style="font-family:var(--fm);font-size:7.6pt;color:var(--acc2);word-break:break-all">{u}</a></div>' for q, t, d, u in cards)
    return slide(head('Links del proyecto', 'Escanea o haz clic: el prototipo y todo el toolkit') + f'<div class="row" style="margin-top:4mm">{out}</div>', 'Links')


def pdv_final():
    return slide(f'''<img class="pvphone" src="{B.mock('../prototipo/capturas_v3/01_tablero.png')}"><div class="z" style="max-width:200mm;margin-top:4mm">
<div class="k">Conclusión · propuesta de valor</div>
<div class="big" style="font-size:48pt;margin:4mm 0 5mm">SABE CUÁNTO GANAS Y <em>QUÉ TE CONVIENE</em>, SIN ANOTAR NADA DE NOCHE.</div>
<div class="pvq" style="font-size:13pt">Una solución de bajo costo, diseñada en O’Higgins con una usuaria real, que deja de convertir la noche en contabilidad y ayuda a decidir dónde atender, cuánto cobrar y cómo preparar los meses bajos.</div>
<div class="tags" style="margin-top:5mm"><span>Anticipador</span><span>Claro</span><span>Conectado y corregible</span><span>Justo con su tiempo</span></div></div>''', '4.1.3 · 4.1.4', 'dark')


def cierre():
    return slide('''<div class="k" style="margin-top:14mm">Gracias</div>
<div class="big" style="font-size:52pt;margin-top:5mm;max-width:270mm">DEL DIAGNÓSTICO AL PITCH: <em>UN COPILOTO PARA LA KINESIÓLOGA INDEPENDIENTE</em>.</div>
<p style="font-size:14pt;max-width:220mm;margin-top:6mm">Gracias a Josselyn Toledo, a Catalina, a Sercotec y a los docentes de INACAP Rancagua.</p>''', 'Cierre', 'orange')


# ================================================================ presentación completa: recuento EV1, EV2 y EV3
TK = '../../unidad-4/tablero_toolkit/img/'
B.slide = slide  # las láminas de la EV3 usan el pie y la numeración de esta presentación


def divisor(n, titulo, sub, img, puntos):
    li = ''.join(f'<div style="border-bottom:1px solid #2A2640;padding:1.6mm 0;font-size:10.5pt">{p}</div>' for p in puntos)
    return slide(f'''<img class="hero" src="{img}" style="opacity:.9"><div class="z" style="margin-top:8mm;max-width:165mm">
<div class="k">Evaluación N°{n}</div><div class="big" style="font-size:54pt;margin:4mm 0 4mm">{titulo}</div>
<p class="lead" style="max-width:150mm">{sub}</p><div style="margin-top:5mm;max-width:150mm">{li}</div></div>''', f'EV{n}', 'dark solid')


def galeria(titulo, items, crit, cols=5, h=48):
    figs = ''.join(f'<figure style="margin:0"><div style="height:{h}mm;display:flex;align-items:center;justify-content:center;background:var(--card);border:1px solid var(--line);border-radius:5px;overflow:hidden">'
                   f'<img src="{TK}{f}" style="max-width:100%;max-height:{h}mm;display:block"></div>'
                   f'<figcaption style="font-size:7.4pt;line-height:1.25;margin-top:1.2mm"><b>{c}</b></figcaption></figure>' for f, c in items)
    return slide(head('Recuento del toolkit', titulo) + f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:3.5mm 4mm">{figs}</div>'
                 + f'<p class="note" style="margin-top:3mm">Plantillas completas y en alta resolución en el tablero del toolkit: <b>{TABLERO}</b></p>', crit)


# ---------------------------------------------------------------- EV1 · Diagnóstico y selección de oportunidades
def ev1_metodo():
    sem = [('S1 · Usuaria', 'Canvas de 33 preguntas sobre los 9 bloques del modelo de negocio, card sorting en 9 categorías y entrevista en profundidad a Josselyn.'),
           ('S2 · Expertos y entorno', 'Observación AEIOU por autorreporte, entrevista a una kinesióloga par (Catalina) y a un asesor financiero; matriz PESTAL.'),
           ('S3 · Síntesis', 'Vaciado de hallazgos, categorización de 8 insights, mapa de priorización y estudio de 8 antecedentes.'),
           ('S4 · Desafío', 'Redefinición con “¿Cómo podríamos…?” y selección de oportunidades de trabajo futuro.')]
    ch = ''.join(f'<div class="on"><b>{t}</b>{d}</div>' for t, d in sem)
    return slide(head('EV1 · Metodología', 'Needfinding en cuatro semanas, con tres fuentes que se triangulan') + f'<div class="chain">{ch}</div>'
                 + '''<div class="row" style="margin-top:4mm"><div class="card"><div class="t">Usuaria · Josselyn</div>~1 año con empresa propia; clínica (comisión 70/30) + domicilios; 10 a 32 h semanales. Dolor principal: la gestión financiera.
“Siento que igual tengo como un cierto desorden o falta de educación.”</div>
<div class="card"><div class="t">Experta par · Catalina</div>Usa Cal.com con Google Calendar y un Excel mensual que le toma ~1 h diaria. Pagaría $30–40 mil al mes por juntar agenda y finanzas.</div>
<div class="card"><div class="t">Asesor financiero</div>Los independientes usan el saldo bancario como termómetro, no provisionan la Operación Renta y no tienen colchón para enero y febrero. Precio de referencia: $8–25 mil.</div></div>''', '1.1.1 · 1.1.2')


def ev1_insights():
    ins = [('I1', 'Ocupada no es lo mismo que rentable', '3/3'), ('I2', 'La agenda es el origen del dato financiero (raíz)', '3/3'), ('I3', 'El Excel como parche diario (~1 h)', '3/3'),
           ('I4', 'Impuestos como sorpresa', '3/3'), ('I5', 'Los costos invisibles del domicilio', '3/3'), ('I6', 'Inestabilidad sin memoria', '3/3'),
           ('I7', 'Fidelización informal por WhatsApp', '3/3'), ('I8', 'Crecimiento sin plan', '2/3')]
    rows = [[f'<b>{a}</b>', b, c] for a, b, c in ins]
    quad = [('Victorias tempranas · (−) complejidad (+) impacto', 'I3 · I5 · I1'), ('Prioridad · (+) complejidad (+) impacto', 'I2 · I6 · I4'),
            ('(−) complejidad (−) impacto', 'I7'), ('(+) complejidad (−) impacto', 'I8')]
    q = ''.join(f'<div class="card" style="{"border-color:var(--acc)" if "Prioridad" in t else ""}"><div class="t">{t}</div><div style="font-family:var(--fd);font-size:22pt">{v}</div></div>' for t, v in quad)
    return slide(head('EV1 · Procesamiento de hallazgos', 'Ocho insights; el raíz: la agenda y las finanzas viven separadas')
                 + '<div class="col2"><div class="a">' + table(['#', 'Insight', 'Fuentes'], rows, 'sm') + '</div>'
                 + f'<div class="b"><h3>Mapa de priorización</h3><div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm">{q}</div>'
                 + '<div class="quote" style="font-size:11pt;margin-top:3mm">“Sin agenda confiable no hay dato de ingresos confiable, y sin dato de ingresos confiable no hay control financiero posible.” — asesor financiero</div></div></div>', '1.1.4')


def ev1_entorno():
    rows = [[f'<b>{n}</b>', o['f'], o['o'], o['a']] for n, o, _ in C3.PESTAL]
    ant = [n for n, _ in C3.ARTE[:8]]
    return slide(head('EV1 · Entorno y antecedentes', 'PESTAL y 8 soluciones existentes')
                 + table(['Factor', 'Cambio', 'Oportunidad', 'Amenaza'], rows, 'sm xs')
                 + f'<div class="card" style="margin-top:3mm"><div class="t">Estudio comparativo de antecedentes</div>{" · ".join(ant)}: todos agendan o llevan contabilidad, pero ninguno conecta la cita con lo que realmente queda después de comisión, traslado y retención. Esa es la oportunidad.</div>', '1.1.3 · 1.1.5')


def ev1_desafio():
    return slide(head('EV1 · Problemática y desafío', 'Del insight raíz al desafío redefinido') + f'''
<div class="quote" style="font-size:15pt">{C.DESAFIO}</div>
<div class="row" style="margin-top:4mm"><div class="card"><div class="t">Oportunidad 1 (seleccionada)</div>Sistema que conecte la agenda con un tablero financiero en tiempo real: ganancia real, costos de domicilio, impuestos y proyección.</div>
<div class="card"><div class="t">Oportunidad 2</div>Presencia digital para captar pacientes: Instagram y sitio web para su práctica.</div>
<div class="card"><div class="t">Por qué la primera</div>Responde al insight raíz (I2), habilita I1, I4 e I6 y la validan las tres fuentes. Meta medible: bajar el registro de ~1 h a menos de 30 min diarios.</div></div>''', '1.1.6')


# ---------------------------------------------------------------- EV2 · Ideación de propuestas
REF = [('Uber Driver', [2, 1, 2, 1, 1]), ('YNAB', [1, 2, 0, 2, 2]), ('Fintual', [1, 2, 0, 1, 2]), ('Mercado Pago', [2, 1, 2, 0, 1]), ('Smart Fit', [1, 0, 2, 1, 1]),
       ('Duolingo', [0, 1, 0, 2, 1]), ('Strava', [2, 2, 0, 2, 1]), ('Google Maps', [2, 1, 1, 0, 2]), ('Too Good To Go', [0, 0, 2, 1, 2]), ('SII · propuesta F22', [2, 1, 1, 0, 1]),
       ('Oportunidad: Copiloto Kine', [2, 2, 2, 2, 2])]


def ev2_referentes():
    dot = {2: '<span class="d2">●</span>', 1: '<span class="d1">◐</span>', 0: '<span class="d0">○</span>'}
    rows = ''.join(f'<tr class="{"me" if "Copiloto" in n else ""}"><td>{n}</td>' + ''.join(f'<td>{dot[v]}</td>' for v in vs) + '</tr>' for n, vs in REF)
    tend = ['El dato se captura solo (Uber, Mercado Pago, Strava)', 'Dinero con propósito y proyección legible (YNAB, Fintual, SII)', 'Recurrencia que da estabilidad (Smart Fit)',
            'Hábitos de segundos y comunidad (Duolingo, Strava)', 'Eficiencia como sostenibilidad (Google Maps, Too Good To Go)', 'Transparencia en tiempo real (Uber, Mercado Pago)']
    return slide(head('EV2 · Estudio de referentes', 'En otros rubros, el dato se captura solo')
                 + '<div class="col2"><div class="a"><table class="mat big"><thead><tr><th>Referente</th><th>Captura automática</th><th>Visualización y proyección</th><th>Cobro y costos</th><th>Hábito</th><th>Sostenibilidad</th></tr></thead>'
                 + f'<tbody>{rows}</tbody></table></div><div class="b" style="flex:.7"><h3>Seis tendencias</h3>{ul(tend)}'
                 + '<div class="card" style="margin-top:3mm"><div class="t">Conclusión</div>Ninguno reúne las cinco variables: los que capturan el dato no lo proyectan y los que proyectan no lo capturan.</div></div></div>', '2.1.2')


def ev2_requerimientos():
    rows = [[f'<b>{r}</b>', n] for r, n, *_ in C3.COBERTURA]
    return slide(head('EV2 · Perfil de usuaria y requerimientos', '13 requerimientos en 6 categorías') + f'''
<div class="col2"><div class="a" style="flex:.8"><div class="card"><div class="t">Perfil · mapa de empatía</div>
<b>Piensa y siente:</b> “cierto desorden” en lo económico; orgullosa de su trato 1:1; insegura ante una carrera “muy inestable”.<br>
<b>Le duele:</b> no saber cuánto gana, los meses bajos por sorpresa, el trabajo administrativo de noche, los costos del domicilio que no ve y los impuestos anuales.<br>
<b>Aspira:</b> una práctica estable: sumar kinesiólogos, abrir grupos para adultos mayores e invertir en presoterapia, decidiendo con datos.</div>
<div class="card" style="margin-top:3mm"><div class="t">Núcleo de la jerarquía</div>R1 y R2 (la cita entra sola desde la agenda que ya usa) + R4 (ganancia real). Sin ellos, el resto no funciona.</div></div>
<div class="b">{table(["#", "Requerimiento"], rows, "sm xs")}</div></div>''', '2.1.3')


def ev2_ideas():
    fac = [('Responde al desafío', 5, 2, 4), ('Recursos internos', 4, 5, 2), ('Recursos externos', 4, 5, 2), ('Prototipable en la UA3', 4, 5, 2),
           ('Aporte sostenible', 5, 3, 3), ('Diferenciación', 5, 1, 2), ('<b>Total (máx. 30)</b>', '<b>27</b>', '<b>21</b>', '<b>15</b>')]
    return slide(head('EV2 · Brainstorming, selección y co-creación', '60 ideas, 13 originales y factibles, un concepto')
                 + '<div class="kpis"><div><div class="v">60</div><div class="l">ideas en el canvas de brainstorming</div></div><div><div class="v">13</div><div class="l">originales y factibles</div></div>'
                 + '<div><div class="v">12</div><div class="l">nacidas de lo que dijeron las usuarias y expertos</div></div><div><div class="v">27/30</div><div class="l">puntaje de factibilidad de Copiloto Kine</div></div></div>'
                 + '<div class="col2"><div class="a">' + table(['Criterio (1–5)', 'A · Copiloto Kine', 'B · Planilla inteligente', 'C · Agenda propia'], fac, 'sm') + '</div>'
                 + '<div class="b"><div class="card"><div class="t">Co-creación</div>Josselyn y Catalina como fuente directa de ideas y una sesión de 45 min para votar ideas, validar la metáfora y probar la propuesta de valor.</div>'
                 + '<div class="card" style="margin-top:3mm"><div class="t">Por qué A</div>Se conecta a la agenda que ya usa en vez de reemplazarla (Catalina usa Cal.com gratis) y es la única que responde al desafío sin digitar.</div></div></div>', '2.1.1 · 2.1.4')


def ev2_propuesta():
    return slide(head('EV2 · Metáfora, atributos y propuesta de valor', '“El tablero y el copiloto de un auto de rally”') + f'''
<div class="row"><div class="attr"><div class="n">Anticipador</div><div class="s2">…avisa los meses bajos antes de que lleguen.</div></div>
<div class="attr"><div class="n">Legible de un vistazo</div><div class="s2">…se entiende sin saber contabilidad.</div></div>
<div class="attr"><div class="n">Automático</div><div class="s2">…la cita se convierte en ingreso sin digitar.</div></div>
<div class="attr"><div class="n">Sostenible</div><div class="s2">…menos km, menos trabajo nocturno, datos protegidos.</div></div></div>
<div class="quote" style="font-size:13pt;margin-top:4mm">{C3.PDV_EV2}</div>
<div class="kpis" style="margin-top:3mm"><div><div class="v">&lt; 30 min</div><div class="l">registro diario (meta del desafío)</div></div><div><div class="v">≥ 80 %</div><div class="l">atenciones registradas solas</div></div>
<div><div class="v">$20–25 mil</div><div class="l">precio de referencia (EV2)</div></div><div><div class="v">ODS 3 · 8 · 13</div><div class="l">enfoque sostenible</div></div></div>''', '2.1.4')


G1 = [('u1_01.jpg', '1.1.1.1 Pregunta exploratoria'), ('u1_02.jpg', 'Guion y card sorting'), ('u1_03.jpg', '1.1.2.1 A Preparación entrevista'), ('u1_04.jpg', '1.1.2.1 B Pauta Josselyn'),
      ('u1_05.jpg', '1.1.2.2 A Preparación observación'), ('u1_06.jpg', '1.1.2.2 B Pauta AEIOU'), ('u1_07.jpg', '1.1.2.3 A Preparación expertos'), ('u1_08.jpg', '1.1.2.3 B Catalina'),
      ('u1_09.jpg', '1.1.2.3 B Asesor financiero'), ('u1_10.jpg', '1.1.3.1 PESTAL'), ('u1_11.jpg', '1.1.4.1 Vaciado de hallazgos'), ('u1_12.jpg', '1.1.4.2 Categorización'),
      ('u1_13.jpg', '1.1.4.3 Priorización'), ('u1_14.jpg', '1.1.5.1 A Fichas de antecedentes'), ('u1_15.jpg', '1.1.5.1 B Matriz de antecedentes'), ('u1_16.jpg', 'Redefinición del desafío'),
      ('u1_17.jpg', '1.1.6 Oportunidades')]
G2 = [('u2_fichas.jpg', '2.1.2.1 A Fichas de 10 referentes'), ('u2_43.jpg', '2.1.2.1 B Matriz de referentes 1/2'), ('u2_44.jpg', '2.1.2.1 B Matriz de referentes 2/2'),
      ('u2_45.jpg', '2.1.3.1 Perfil y requerimientos'), ('u2_46.jpg', '2.1.3.2 Mapa de categorías'), ('u2_47.jpg', '2.1.3.3 Mapa de jerarquías'), ('u2_48.jpg', '2.1.4.1 Canvas brainstorming'),
      ('u2_49.jpg', '2.1.4.2 Clasificación de ideas'), ('u2_50.jpg', '2.1.4.3 Metáforas y atributos'), ('u2_51.jpg', '2.1.4.4 Propuesta de valor y métricas')]
G3 = [('u3_00.jpg', '3.1.2.1 Storyboard v1'), ('u3_01.jpg', '3.1.2.3 Ficha ciclo 1'), ('u3_02.jpg', '3.1.2.4 CDM ciclo 1'), ('u3_03.jpg', '3.1.3.2 Storyboard v2'),
      ('u3_04.jpg', '3.1.3.4 Ficha ciclo 2'), ('u3_05.jpg', '3.1.2.4 CDM ciclo 2'), ('u3_06.jpg', '3.1.2.3 Ficha ciclo 3'), ('u3_07.jpg', '3.1.2.4 CDM ciclo 3'),
      ('u3_08.jpg', '3.1.3.2 Storyboard v3'), ('u3_09.jpg', '3.1.3.4 Ficha ciclo 4'), ('u3_10.jpg', '3.1.4.1 PESTAL profundizada')]
G4 = [('u4_lean.jpg', '4.1.2.1 Lean Canvas'), ('u4_form.jpg', '4.1.3.1 Formulario de postulación'), ('u4_guion.jpg', '4.1.3.2 Guion del pitch'), ('u4_pitch.jpg', 'Presentación del pitch')]


def bloque_ev1():
    return (divisor(1, 'DIAGNÓSTICO Y <em>SELECCIÓN DE OPORTUNIDADES</em>', 'Semanas 1 a 4 · criterios 1.1.1 a 1.1.6 · needfinding con la usuaria, expertos y el entorno.', 'img/05-entrevista.jpg',
                    ['Entrevista a Josselyn, observación AEIOU y dos expertos', '8 insights; raíz: la agenda y las finanzas viven separadas', 'PESTAL y 8 antecedentes', 'Desafío redefinido y oportunidad seleccionada'])
            + ev1_metodo() + ev1_insights() + ev1_entorno() + ev1_desafio()
            + galeria('EV1 · instrumentos de la Unidad 1 (1/2)', G1[:10], 'EV1') + galeria('EV1 · instrumentos de la Unidad 1 (2/2)', G1[10:], 'EV1'))


def bloque_ev2():
    return (divisor(2, 'IDEACIÓN <em>DE PROPUESTAS</em>', 'Semanas 6 a 10 · criterios 2.1.1 a 2.1.5 · de un insight a una propuesta de valor.', 'img/04-card-sorting.jpg',
                    ['10 referentes de otros rubros y 6 tendencias', 'Perfil de usuaria y 13 requerimientos', '60 ideas, selección por factibilidad y co-creación', 'Metáfora, atributos y propuesta de valor'])
            + ev2_referentes() + ev2_requerimientos() + ev2_ideas() + ev2_propuesta()
            + galeria('EV2 · instrumentos de la Unidad 2', G2, 'EV2', cols=5, h=46))


def bloque_ev3():
    return (divisor(3, 'PROTOTIPADO <em>Y TESTEO</em>', 'Semanas 11 a 14 · criterios 3.1.1 a 3.1.5 · tres versiones del prototipo y cuatro ciclos de testeo.', 'img/07-oficina-movil.jpg',
                    ['Prototipo v1 → v2 → v3 navegable en el celular', 'Ciclos 1 y 2 internos; ciclo 3 con la clienta, Sercotec y docentes', '24 cambios fundamentados en el testeo', 'Estado del arte, PESTAL profundizada y pertinencia'])
            + B.ruta_c() + B.sqa() + B.storyboard_v1() + B.mock_v1() + B.ciclo1_c() + B.iter_v2_c() + B.mock_it() + B.ciclo2_c() + B.cdm12_c()
            + B.ficha3() + B.retro_rf() + B.retro_sug() + B.cdm_slide(C3.CDM_C3, 'Ciclo 3 · clienta, Sercotec y docentes (prototipo v2)', '3.1.2.4', '3.1.2 · 3.1.3')
            + B.salto_v3() + B.metafora_v3() + B.storyboard_v3() + B.mock_v3_c() + B.mock_v3_b() + B.cambios_verif_c() + B.ficha4() + B.usuarios_c()
            + B.pestal_c() + B.arte_c() + B.pertinencia() + B.sost_gest_c()
            + galeria('EV3 · instrumentos de la Unidad 3', G3, 'EV3', cols=6, h=50))


def bloque_ev4():
    return (divisor(4, 'DIFUSIÓN <em>DE LA INNOVACIÓN</em>', 'Semanas 15 a 18 · criterios 4.1.1 a 4.1.5 · comunicar el potencial de la solución al ecosistema.', 'img/15-horizonte.jpg',
                    ['Qué veo, qué no veo, qué infiero', 'Lean Canvas, factibilidad e impacto', 'Formulario de postulación a fondo concursable', 'Guion del pitch, sostenibilidad y acciones futuras'])
            + problema() + recorrido() + solucion() + prototipo() + diferenciacion() + lean() + factibilidad() + impacto() + formulario() + guion() + sostenibilidad()
            + galeria('EV4 · instrumentos de la Unidad 4', G4, 'EV4', cols=4, h=60))


def agenda():
    bl = [('EV1', 'Diagnóstico y selección de oportunidades', 'Needfinding, 8 insights, PESTAL, antecedentes y desafío'),
          ('EV2', 'Ideación de propuestas', 'Referentes, requerimientos, 60 ideas, metáfora y propuesta de valor'),
          ('EV3', 'Prototipado y testeo', 'Prototipo v1 → v3, 4 ciclos de testeo, estado del arte y pertinencia'),
          ('EV4', 'Difusión de la innovación', 'Lean Canvas, factibilidad, impacto, formulario, pitch y acciones futuras')]
    cards = ''.join(f'<div><div class="c">{a}</div><div style="margin-top:1.5mm;font-size:11pt"><b>{t}</b></div><div class="w">{w}</div></div>' for a, t, w in bl)
    return slide(head('Qué presentamos', 'El proyecto completo, de la EV1 a la EV4') + f'<div class="cri" style="grid-template-columns:repeat(4,1fr)">{cards}</div>'
                 + '<div class="row" style="margin-top:5mm"><div class="card"><div class="t">Recuento del toolkit</div>Cada evaluación cierra con la galería de sus plantillas; todas están también en el tablero del toolkit (link al final).</div>'
                 + f'<div class="card"><div class="t">Prototipo navegable</div>Vista profesional y vista cliente, publicadas y con código QR al final.</div>'
                 + '<div class="card"><div class="t">Criterios ES04</div>4.1.1 propuesta de valor · 4.1.2 factibilidad e impacto · 4.1.3 persuasión · 4.1.4 diferenciación · 4.1.5 sostenibilidad.</div></div>', 'Agenda')


HEAD = '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Copiloto Kine — Presentación final</title><link rel="stylesheet" href="pres.css"></head><body>'

if __name__ == '__main__':
    body = (portada() + agenda() + caso() + bloque_ev1() + bloque_ev2() + bloque_ev3() + bloque_ev4() + links() + pdv_final() + cierre())
    path = os.path.join(EV3, '_ev4.html')
    open(path, 'w', encoding='utf-8').write(HEAD + body + '</body></html>')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    HTML(path, base_url=EV3).write_pdf(OUT)
    os.replace(path, os.path.join(HERE, 'entregables', 'EV4_Presentacion_Copiloto_Kine.html'))
    import pymupdf
    print('ok', pymupdf.open(OUT).page_count, 'diapositivas')
