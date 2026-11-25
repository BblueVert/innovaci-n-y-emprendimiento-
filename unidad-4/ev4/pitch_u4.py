# PPT del pitch (ES4) sobre la plantilla oficial "PITCH actualizado" de la carpeta Sercotec.
# Llena cada diapositiva de la plantilla, agrega una de modelo de negocio (Lean Canvas) y deja el guion hablado en las notas.
# Uso: python3 pitch_u4.py → entregables/Pitch_Copiloto_Kine.pptx
import copy
import os
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn
import sys
import contenido_u4 as C
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'unidad-3', 'ev3'))
from mockup import mock  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'material', 'sercotec_es4', 'PITCH_actualizado.pptx')
OUT = os.path.join(HERE, 'entregables', 'Pitch_Copiloto_Kine.pptx')
EV3 = os.path.join(HERE, '..', '..', 'unidad-3', 'ev3', 'img')
IMG = os.path.join(HERE, 'img')
RED = RGBColor(0xE3, 0x06, 0x13)
INK = RGBColor(0x26, 0x26, 0x26)
GREY = RGBColor(0x59, 0x59, 0x59)
LINK_PITCH = '[pegar link del video]'
LINK_MIRO = '[pegar link del Miro]'
NOTES = {k: v for k, v in C.PITCH}


def write(tf, paras, size=40, color=INK, space=10):
    """paras: lista de str o (negrita, texto) o ('#', título rojo)."""
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    bp = tf._txBody.find(qn('a:bodyPr'))
    for tag in ('a:normAutofit', 'a:spAutoFit'):
        for e in bp.findall(qn(tag)):
            bp.remove(e)
    first = True
    for item in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(space)
        p.level = 0
        if isinstance(item, tuple) and item[0] == '#':
            r = p.add_run(); r.text = item[1]; r.font.size = Pt(size + 6); r.font.bold = True; r.font.color.rgb = RED
            p._p.get_or_add_pPr().insert(0, p._p.makeelement(qn('a:buNone'), {}))
            continue
        if isinstance(item, tuple):
            r = p.add_run(); r.text = item[0]; r.font.bold = True; r.font.size = Pt(size); r.font.color.rgb = INK
            r2 = p.add_run(); r2.text = ' ' + item[1]; r2.font.size = Pt(size); r2.font.color.rgb = color
        else:
            r = p.add_run(); r.text = item; r.font.size = Pt(size); r.font.color.rgb = color
        for r in p.runs:
            r.font.italic = False


def body(slide):
    for sh in slide.shapes:
        if sh.is_placeholder and sh.placeholder_format.idx != 0 and sh.has_text_frame and sh.name != 'Título Diapositiva 2':
            if 'Título' not in sh.name:
                return sh
    return None


def clean_numbers(slide):
    for sh in list(slide.shapes):
        if sh.shape_type == 17 and sh.has_text_frame and sh.text_frame.text.strip() in ('1', '2'):
            sh._element.getparent().remove(sh._element)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def box(slide, x, y, w, h, paras, size=36, fill=None, color=INK):
    tb = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    if fill:
        tb.fill.solid(); tb.fill.fore_color.rgb = fill
    tf = tb.text_frame; tf.margin_left = tf.margin_right = Cm(0.6); tf.margin_top = tf.margin_bottom = Cm(0.4)
    write(tf, paras, size=size, color=color, space=2)
    return tb


def kpi(slide, x, y, w, value, label):
    box(slide, x, y, w, 4.2, [('#', value), label], size=30, fill=RGBColor(0xF6, 0xF2, 0xF2))


def content_slide(prs, slide, title, left, left_w=31, size=41):
    clean_numbers(slide)
    for sh in slide.shapes:
        if sh.has_text_frame and sh.name == 'Título Diapositiva 2':
            sh.text_frame.text = title
    b = body(slide)
    b.left, b.top, b.width, b.height = Cm(3.4), Cm(11.0), Cm(left_w), Cm(24.5)
    write(b.text_frame, left, size=size)
    b.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    return b


def duplicate(prs, src_slide):
    """Nueva diapositiva con el mismo layout y las mismas imágenes de fondo que src_slide."""
    s = prs.slides.add_slide(src_slide.slide_layout)
    for sh in list(s.shapes):
        sh._element.getparent().remove(sh._element)
    for sh in src_slide.shapes:
        el = copy.deepcopy(sh._element)
        s.shapes._spTree.insert_element_before(el, 'p:extLst')
    for rel in src_slide.part.rels.values():
        if 'image' in rel.reltype:
            s.part.rels.get_or_add(rel.reltype, rel._target)
    # las imágenes copiadas apuntan a los mismos rId; se reasignan por nombre de destino
    rid_map = {r.rId: s.part.relate_to(r._target, r.reltype) for r in src_slide.part.rels.values() if 'image' in r.reltype}
    for blip in s.shapes._spTree.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'):
        old = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if old in rid_map:
            blip.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed', rid_map[old])
    return s


def move(prs, slide, index):
    lst = prs.slides._sldIdLst
    el = [x for x in lst if x.get('id') == str(slide.slide_id)][0]
    lst.remove(el); lst.insert(index, el)


def build():
    prs = Presentation(SRC)
    S = list(prs.slides)

    # 2 · portada con datos
    for sh in S[1].shapes:
        if not sh.has_text_frame:
            continue
        if sh.text_frame.text.startswith('Título'):
            sh.text_frame.paragraphs[0].runs[0].text = 'Copiloto Kine'
            for r in sh.text_frame.paragraphs[0].runs[1:]:
                r.text = ''
        elif sh.text_frame.text.startswith('Subtítulo'):
            sh.text_frame.paragraphs[0].runs[0].text = C.LC['pdv']
            for r in sh.text_frame.paragraphs[0].runs[1:]:
                r.text = ''
        elif sh.text_frame.text.startswith('NOMBRE'):
            lines = [('NOMBRE:', ', '.join(C.EQUIPO)), ('CARRERA:', C.CARRERA), ('ASIGNATURA:', C.ASIGNATURA), ('PROFESOR:', C.PROFESOR),
                     ('FECHA:', '15-12-2026'), ('LINK PITCH:', LINK_PITCH), ('LINK MIRO:', LINK_MIRO)]
            write(sh.text_frame, lines, size=22, space=0)
            sh.top = Cm(25.0); sh.height = Cm(10.5)
    notes(S[1], NOTES['Quién eres'].split('. Josselyn atiende')[0] + '.')

    # 3 · temas a tratar
    temas = [('Punto', 'El problema de Josselyn', ['Antecedentes de la empresa', 'Problema priorizado']),
             ('Punto', 'Copiloto Kine', ['Solución y diferenciación', 'Prototipo validado']),
             ('Punto', 'Cómo crece', ['Modelo de negocio', 'Acciones futuras y conclusiones'])]
    pts = [sh for sh in S[2].shapes if sh.has_text_frame and sh.text_frame.text.strip() == 'Punto Ejemplo']
    subs = [sh for sh in S[2].shapes if sh.has_text_frame and sh.text_frame.text.startswith('> Subtema')]
    pts.sort(key=lambda s: s.top); subs.sort(key=lambda s: s.top)
    for (_, t, items), p, s in zip(temas, pts, subs):
        p.text_frame.paragraphs[0].runs[0].text = t
        for r in p.text_frame.paragraphs[0].runs[1:]:
            r.text = ''
        for para, it in zip(s.text_frame.paragraphs, items + ['']):
            if para.runs:
                para.runs[0].text = ('> ' + it) if it else ''
                for r in para.runs[1:]:
                    r.text = ''

    # 4 · antecedentes
    content_slide(prs, S[3], 'Antecedentes de la Empresa', [
        ('Empresa:', 'Josselyn Toledo, kinesióloga y psicomotricista acuática independiente.'),
        ('Ubicación:', 'San Fernando y alrededores, Región de O’Higgins (Aguas Buenas, Las Cabras, camino a Roma).'),
        ('Actividad:', 'atiende en el Centro Médico InMotion (factura mensual), a domicilio, en una piscina temperada y en su gimnasio.'),
        ('#', 'Problemas detectados en el diagnóstico'),
        'No sabe cuánto gana de verdad ni qué le conviene.',
        'Registra todo a mano cada noche (~1 h).',
        'El traslado rural no se mide ni se cobra.',
        'Enero y febrero bajan ~35 % sin plan.'], left_w=32, size=25)
    S[3].shapes.add_picture(os.path.join(EV3, '02-caso.jpg'), Cm(36.5), Cm(11.5), width=Cm(28))
    notes(S[3], NOTES['Quién eres'])

    # 5 · problema
    content_slide(prs, S[4], 'Problema a abordar seleccionado', [
        ('#', 'Insight priorizado: la agenda y las finanzas viven separadas'),
        'Cada cita es un ingreso que se pierde: hay que reescribirlo a mano, sin descontar comisión, traslado ni impuestos.',
        ('#', 'En sus palabras'),
        '“Cada noche anoto todo… lo que gasto en bencina… cuánto gané en cada sesión.” — Josselyn',
        '“Me toma una hora actualmente diario.” — Catalina, kinesióloga',
        '“Estar ocupado y estar ganando dinero no son lo mismo.” — asesor financiero'], left_w=36, size=29)
    for i, (v, l) in enumerate([('~1 h', 'diaria de registro manual'), ('25–30 min', 'por domicilio en precordillera'), ('−35 %', 'ingresos en enero y febrero'), ('30.050', 'kinesiólogos en Chile (Superintendencia de Salud)')]):
        kpi(S[4], 42, 11.0 + i * 6.0, 22, v, l)
    notes(S[4], 'El problema que priorizamos es que la agenda y las finanzas viven separadas: cada cita es un ingreso que Josselyn tiene que '
                'reescribir a mano cada noche, sin saber cuánto le costó llegar. Una kinesióloga par nos dijo que eso le toma una hora diaria, y un '
                'asesor financiero lo resumió así: estar ocupado y estar ganando dinero no son lo mismo.')

    # 6 · solución
    content_slide(prs, S[5], 'Descripción de la solución', [
        ('#', 'Copiloto Kine: el copiloto de la kinesióloga que trabaja en varios lugares'),
        ('Conectado:', 'toma las citas de AgendaPro y de la clínica; nada se digita dos veces.'),
        ('Claro:', 'ganancia real y ganancia por hora de cada canal, de un vistazo.'),
        ('Justo con su tiempo:', 'valora el viaje y sugiere cuánto cobrar por tramo rural.'),
        ('Anticipador:', 'avisa los meses bajos y propone acciones, como una clase grupal.'),
        ('#', 'Frente a la competencia'),
        'Las agendas solo agendan y las planillas hay que llenarlas a mano: Copiloto Kine cruza agenda, traslado rural, impuestos y paciente.'], left_w=38, size=25)
    S[5].shapes.add_picture(os.path.join(EV3, '..', mock('../prototipo/capturas_v3/02_ganancia_por_hora.png')), Cm(47), Cm(9.8), height=Cm(26))
    notes(S[5], NOTES['Qué haces'])

    # 7 · prototipo
    content_slide(prs, S[6], 'Prototipo', [
        ('#', 'Paso a paso para aplicarlo'),
        '1. Abre el enlace en el celular y conecta su agenda.',
        '2. Al terminar cada atención, la marca con un toque: ve su ganancia real.',
        '3. Revisa la ruta del día y cuánto le cuesta cada tramo.',
        '4. Cierra el día en un minuto y descarga el resumen para su contadora.',
        ('#', 'Validado en 4 ciclos'),
        '21/21 tareas · cálculos exactos · 0 errores de accesibilidad · ciclo con la clienta y Sercotec.',
        ('Pruébalo:', C.URL_PRO)], left_w=27, size=27)
    S[6].shapes.add_picture(os.path.join(IMG, 'prototipo_v3.jpg'), Cm(31.5), Cm(10.5), width=Cm(33.5))
    S[6].shapes.add_picture(os.path.join(EV3, 'qr-profesional.png'), Cm(58.5), Cm(29.2), width=Cm(6.2))
    notes(S[6], NOTES['Por qué es único'])

    # nueva · modelo de negocio (Lean Canvas)
    mn = duplicate(prs, S[6])
    for sh in list(mn.shapes):
        if sh.shape_type == 13 and sh.name not in ('ppt-back-slide.png', 'ppt-footer.jpg', 'logo-inacap.png') or (sh.has_text_frame and sh.name != 'Título Diapositiva 2' and not sh.is_placeholder):
            sh._element.getparent().remove(sh._element)
    for sh in mn.shapes:
        if sh.has_text_frame and sh.name == 'Título Diapositiva 2':
            sh.text_frame.text = 'Modelo de negocio y factibilidad'
        elif sh.is_placeholder and sh.has_text_frame:
            sh._element.getparent().remove(sh._element)
    mn.shapes.add_picture(os.path.join(HERE, 'entregables', '4.1.2.1_Lean_Canvas_Copiloto_Kine.png'), Cm(3.2), Cm(10.2), width=Cm(39))
    e = C.escenario(30)
    ing = '$' + f"{e['ingresos_mes']:,}".replace(',', '.')
    for i, (v, l) in enumerate([('$9.990', 'al mes · piloto gratis 3 meses'), ('5 usuarias', 'cubren la operación (~$48.000/mes)'),
                                (f"{e['margen_pct']} %", f'margen bruto con 30 usuarias ({ing}/mes)'),
                                ('LTV 16×', 'CAC: $240.000 vs. $15.000 por usuaria')]):
        kpi(mn, 43.5, 10.2 + i * 6.3, 21.5, v, l)
    notes(mn, 'Nuestro modelo es una suscripción de $9.990 al mes, con un piloto gratis de tres meses. Con cinco usuarias cubrimos la operación '
              'y con treinta llegamos a un margen bruto cercano al 84 %. Para la kinesióloga, la app se paga sola: cobrar un solo tramo rural ya la cubre.')
    move(prs, mn, 7)

    # 8 · acciones futuras
    S = list(prs.slides)
    af = S[8]
    content_slide(prs, af, 'Acciones Futuras', [('#', 'Hoja de ruta para la sustentabilidad')]
                  + [(f'{c}:', a) for c, a, _ in C.ACCIONES], left_w=36, size=25)
    for i, (d, t) in enumerate([('Económico', 'cobrar el traslado; clase grupal +$213.000/mes en meses bajos'), ('Social', '~1 h diaria de vida personal recuperada; adultos mayores atendidos'),
                                ('Ambiental', '−12 km en un día tipo con la ruta sugerida'), ('Tecnológico', 'app web liviana que se integra con AgendaPro, WhatsApp y Excel')]):
        box(af, 42, 11.0 + i * 6.0, 22.5, 5.4, [('#', d), t], size=28, fill=RGBColor(0xF6, 0xF2, 0xF2))
    notes(af, NOTES['Objetivo'].rsplit(' Copiloto Kine:', 1)[0])

    # 9 · conclusiones
    cc = S[9]
    content_slide(prs, cc, 'Conclusiones', [
        ('#', 'Cómo beneficia a Josselyn frente al problema'),
        'Sabe cuánto gana de verdad y qué canal le conviene.',
        'Deja de anotar de noche: cierra el día en un minuto.',
        'Cobra lo justo por los traslados rurales.',
        'Prepara enero y febrero con acciones concretas.',
        ('#', 'Para el ecosistema'),
        'Una solución de bajo costo, diseñada en O’Higgins con una usuaria real, que puede escalar a otras profesiones de salud independientes.'], left_w=36, size=32)
    box(cc, 41.5, 13.0, 23, 14, [('#', 'Sabe cuánto ganas y qué te conviene, sin anotar nada de noche.')], size=52, fill=RGBColor(0xFF, 0xF1, 0xEE))
    notes(cc, 'Copiloto Kine: sabe cuánto ganas y qué te conviene, sin anotar nada de noche. Muchas gracias.')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    prs.save(OUT)
    print('ok', OUT, len(prs.slides), 'diapositivas')


if __name__ == '__main__':
    build()
