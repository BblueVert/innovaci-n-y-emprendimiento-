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
FOOT = 'Copiloto Kine · EV4 Difusión de la innovación · INACAP Rancagua'
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
<div class="big" style="margin-top:6mm">EVALUACIÓN N°4<br><em>DIFUSIÓN</em><br>DE LA INNOVACIÓN</div>
<div style="font-family:var(--fd);font-size:22pt;color:#FF8A4C;margin-top:4mm;letter-spacing:.03em">COPILOTO KINE · CASO JOSSELYN TOLEDO</div>
<p class="lead" style="max-width:155mm;margin-top:3mm">{C.LC['pdv']} Propuesta de valor, modelo de negocio, factibilidad y pitch para el ecosistema de O’Higgins.</p>
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


HEAD = '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Evaluación 4 — Difusión de la innovación</title><link rel="stylesheet" href="pres.css"></head><body>'

if __name__ == '__main__':
    body = (portada() + criterios() + caso() + problema() + recorrido() + solucion() + prototipo() + storyboard() + diferenciacion()
            + lean() + factibilidad() + impacto() + formulario() + guion() + sostenibilidad() + links() + pdv_final() + cierre())
    path = os.path.join(EV3, '_ev4.html')
    open(path, 'w', encoding='utf-8').write(HEAD + body + '</body></html>')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    HTML(path, base_url=EV3).write_pdf(OUT)
    os.replace(path, os.path.join(HERE, 'entregables', 'EV4_Presentacion_Copiloto_Kine.html'))
    import pymupdf
    print('ok', pymupdf.open(OUT).page_count, 'diapositivas')
