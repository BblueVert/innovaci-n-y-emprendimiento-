"""Rellena las plantillas oficiales de la entrega con el contenido de Copiloto Kine.

Entradas : unidad-2/material/plantillas_u3/{Canvas.pptx, Unidad3_Prototipado_y_testeo_P2026.pptx}
Salidas  : unidad-2/entrega_ev2/{EV2_Canvas_Storyboard_CopilotoKine.pptx, EV2_Prototipado_CopilotoKine.pptx}
Uso      : python3 unidad-2/_build/llenar_plantillas.py
Requiere : python-pptx y el script add_slide.py de la skill pptx (para duplicar diapositivas).
"""
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / 'material' / 'plantillas_u3'
OUT = ROOT / 'entrega_ev2'
IMG = OUT / 'img'
SB = ROOT / 'ev2' / 'img' / 'storyboard'
ADD_SLIDE = os.environ.get('PPTX_ADD_SLIDE') or str(next(Path('/root/.claude/skills').rglob('pptx/scripts/add_slide.py')))

GRUPO, SECCION, FECHA = '___', '___', 'Noviembre 2026'   # completar con los datos del curso
EQUIPO = [
    ('Benjamín Vera Yáñez', 'Secretario técnico · consolida y prototipa'),
    ('Francisco Ahumada', 'Referentes financieros · factibilidad'),
    ('Claudia Cifuentes', 'Perfil de usuaria · co-creación'),
    ('Néstor Rivera', 'Ideación · registro y métricas'),
]
CARRERA = 'Diseño Digital'


# ---------------------------------------------------------------- utilidades
def duplicate(src, dst, plan):
    """plan: lista de (slide a copiar, después de cuál). Usa add_slide.py (registra rels y content types)."""
    tmp = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    for slide, after in plan:
        subprocess.run([sys.executable, ADD_SLIDE, str(tmp), slide, '--after', after], check=True, stdout=subprocess.DEVNULL)
    if dst.exists():
        dst.unlink()
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(tmp.rglob('*')):
            if f.is_file():
                z.write(f, f.relative_to(tmp).as_posix())
    shutil.rmtree(tmp)


def shape(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise KeyError(name)


def drop(slide, *names):
    for sh in list(slide.shapes):
        if sh.name in names:
            sh._element.getparent().remove(sh._element)


def set_runs(tf, paras, size=None, color=None, align=None, space_after=None):
    """paras: lista de párrafos; cada párrafo es str o lista de (texto, {bold, color, size, italic})."""
    tf.clear()
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if align is not None:
            p.alignment = align
        if space_after is not None:
            p.space_after = Pt(space_after)
        runs = [(para, {})] if isinstance(para, str) else para
        for text, o in runs:
            r = p.add_run()
            r.text = text
            f = r.font
            sz = o.get('size', size)
            if sz:
                f.size = Pt(sz)
            if o.get('bold'):
                f.bold = True
            if o.get('italic'):
                f.italic = True
            c = o.get('color', color)
            if isinstance(c, RGBColor):
                f.color.rgb = c
            elif c is not None:
                f.color.theme_color = c


def textbox(slide, x, y, w, h, paras, name, size=12, color=MSO_THEME_COLOR.TEXT_1, anchor=MSO_ANCHOR.TOP, align=None, space_after=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    set_runs(tf, paras, size=size, color=color, align=align, space_after=space_after)
    return tb


def box(slide, x, y, w, h, name, fill=MSO_THEME_COLOR.BACKGROUND_2, kind=MSO_SHAPE.ROUNDED_RECTANGLE, line=None):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.name = name
    if isinstance(fill, RGBColor):
        s.fill.solid(); s.fill.fore_color.rgb = fill
    else:
        s.fill.solid(); s.fill.fore_color.theme_color = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
    s.shadow.inherit = False
    if kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.08
    return s


def picture_fit(slide, path, x, y, w, h, name):
    from PIL import Image
    iw, ih = Image.open(path).size
    r = min(w / iw, h / ih)
    pw, ph = iw * r, ih * r
    pic = slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))
    pic.name = name
    return pic


ACC = {'color': MSO_THEME_COLOR.ACCENT_1, 'bold': True}

# ================================================================ PROTOTIPADO
def build_prototipado():
    src = TPL / 'Unidad3_Prototipado_y_testeo_P2026.pptx'
    dst = OUT / 'EV2_Prototipado_CopilotoKine.pptx'
    duplicate(src, dst, [('slide3.xml', 'slide3.xml'), ('slide3.xml', 'slide4.xml')])
    prs = Presentation(dst)
    s1, s2, s3, s4, s5 = prs.slides

    # ---- 1 · Portada
    set_runs(shape(s1, 'Text 1').text_frame, ['Copiloto Kine'])
    set_runs(shape(s1, 'Tagline').text_frame, [[('El copiloto financiero de la kinesióloga independiente: convierte cada atención en ganancia real y le avisa qué viene, sin que tenga que digitar.', {'italic': True})]], size=14, color=MSO_THEME_COLOR.BACKGROUND_2)
    set_runs(shape(s1, 'Datos del grupo').text_frame, [f'Grupo N° {GRUPO}   ·   Sección {SECCION}   ·   {FECHA}'], size=12, color=MSO_THEME_COLOR.BACKGROUND_1)
    for i, (n, rol) in enumerate(EQUIPO, start=1):
        set_runs(shape(s1, f'Integrante {i}').text_frame,
                 [[(f'{i}. {n}', {'bold': True, 'size': 13})], [(f'{CARRERA} · {rol}', {'size': 10, 'color': MSO_THEME_COLOR.TEXT_2})]])

    # ---- 2 · El problema que resolvemos
    banda = shape(s2, 'Banda problema'); banda.height = Inches(1.55)
    frase = shape(s2, 'Frase del problema'); frase.height = Inches(1.05)
    set_runs(frase.text_frame, [[
        ('Las kinesiólogas independientes con atención mixta', ACC), (' necesitan ', {}),
        ('saber cuánto ganan realmente y anticipar sus meses bajos', ACC), (' porque ', {}),
        ('su agenda y sus finanzas viven separadas', ACC), (', lo que genera ', {}),
        ('cerca de 1 hora diaria de registro manual y meses bajos e impuestos que llegan por sorpresa', ACC), ('.', {})]], size=16)
    cards = [
        ('USUARIO', 'Joselyn Toledo, kinesióloga con ~1 año de práctica propia. Atiende en el Centro Médico InMotion (70/30) y a domicilio, de 10 a 32 h semanales.'),
        ('NECESIDAD', 'Ver su ganancia real por atención (con comisión, traslado, materiales e impuestos) y saber con tiempo qué viene, sin digitar en un Excel de noche.'),
        ('EVIDENCIA', '8 insights de la UA1, 7 triangulados 3/3 (usuaria, expertos y observación). Catalina: “me toma una hora diaria”. Asesor: “estar ocupado no es lo mismo que ganar”.'),
    ]
    for i, (lab, txt) in enumerate(cards):
        x = 0.5 + i * (2.88 + 0.18)
        box(s2, x, 3.15, 2.88, 1.9, f'Tarjeta {lab.lower()}')
        c = box(s2, x + 0.18, 3.32, 0.34, 0.34, f'Círculo {lab.lower()}', fill=MSO_THEME_COLOR.ACCENT_1, kind=MSO_SHAPE.OVAL)
        set_runs(c.text_frame, [[(str(i + 1), {'bold': True, 'color': MSO_THEME_COLOR.BACKGROUND_1})]], size=12, align=PP_ALIGN.CENTER)
        c.text_frame.margin_left = c.text_frame.margin_right = 0
        textbox(s2, x + 0.62, 3.32, 2.1, 0.34, [[(lab, {'bold': True})]], f'Etiqueta {lab.lower()}', size=12, color=MSO_THEME_COLOR.TEXT_2, anchor=MSO_ANCHOR.MIDDLE)
        textbox(s2, x + 0.18, 3.8, 2.55, 1.15, [txt], f'Texto {lab.lower()}', size=11)

    # ---- 3, 4, 5 · Nuestro prototipo
    protos = [
        (s3, 'Nuestro prototipo · V1', 'mockup-v1.png', 'Versión 1 · alcance mínimo: atención realizada, tablero y proyección', [
            ('Beneficios', 'Cada cita de su agenda se vuelve ingreso. Al cerrar una atención ve su ganancia neta y un tablero con semáforo.'),
            ('Principales costos', 'Diseño y desarrollo low-code del equipo, conexión con Google Calendar (API sin costo) y Google Sheets como base del prototipo.'),
            ('Hipótesis a testear', 'Con el cierre de un toque, Joselyn baja su registro diario de ~60 a menos de 30 min y ≥ 80 % de sus atenciones se registran solas.')]),
        (s4, 'Nuestro prototipo · V2', 'mockup-v2.png', 'Versión 2 · iterada: el pago se reparte solo, tablero con impuestos y alertas con acciones', [
            ('Beneficios', 'Aparta sola la retención y un colchón, agrupa domicilios por sector (−9 km al día), ofrece las horas libres y cierra el día antes de las 21 h.'),
            ('Principales costos', 'Lo de la V1 más mapas, un medio de pago con link (comisión por cobro) y soporte. Para Joselyn: $20.000–25.000 al mes de referencia.'),
            ('Hipótesis a testear', 'Si el copiloto avisa un mes bajo con una acción concreta, Joselyn la activa; y la proyección se equivoca en ≤ 10 % frente a lo real.')]),
        (s5, 'Nuestro prototipo · paciente', 'mockup-paciente.png', 'Versión 2 · lo que vive el paciente: reserva, recordatorio y pago con link', [
            ('Beneficios', 'Reserva en un minuto en la agenda de siempre, recibe recordatorio y aviso de llegada por WhatsApp y paga sin efectivo.'),
            ('Principales costos', 'Mensajes con plantillas en la voz de Joselyn y la comisión del medio de pago en cada cobro.'),
            ('Hipótesis a testear', 'Los pacientes, incluidos adultos mayores, confirman y pagan con link sin ayuda: meta a validar ≥ 70 % de los domicilios.')]),
    ]
    for s, title, img, cap, points in protos:
        set_runs(shape(s, 'Text 1').text_frame, [[(title, {'bold': True, 'color': MSO_THEME_COLOR.TEXT_1})]], size=32)
        marco = shape(s, 'Marco mock up')
        marco.line.fill.background()
        drop(s, 'Icono imagen', 'Texto marco', 'Círculo número 1', 'Número 1', 'Encabezado 1', 'Guía 1', 'Encabezado 2', 'Círculo número 3', 'Número 3', 'Encabezado 3')
        picture_fit(s, IMG / img, 0.6, 1.45, 5.2, 3.2, 'Mock up')
        textbox(s, 0.7, 4.68, 5.0, 0.3, [cap], 'Pie mock up', size=10, color=MSO_THEME_COLOR.TEXT_2, align=PP_ALIGN.CENTER)
        for i, (h, t) in enumerate(points):
            y = 1.35 + i * 1.25
            c = box(s, 6.2, y, 0.42, 0.42, f'Círculo número {i + 1}', fill=MSO_THEME_COLOR.ACCENT_1, kind=MSO_SHAPE.OVAL)
            set_runs(c.text_frame, [[(str(i + 1), {'bold': True, 'color': MSO_THEME_COLOR.BACKGROUND_1})]], size=14, align=PP_ALIGN.CENTER)
            c.text_frame.margin_left = c.text_frame.margin_right = 0
            textbox(s, 6.78, y, 2.75, 0.42, [[(h, {'bold': True})]], f'Encabezado {i + 1}', size=15, anchor=MSO_ANCHOR.MIDDLE)
            textbox(s, 6.78, y + 0.45, 2.75, 0.78, [t], f'Guía {i + 1}', size=10.5, color=MSO_THEME_COLOR.TEXT_1)
    # notas para quien presente
    def note(sl, t):
        tf = sl.notes_slide.notes_text_frame
        if tf is not None:
            tf.text = t
    note(s3, 'V1: alcance mínimo definido en el informe EV2. Hipótesis: el cierre de un toque reduce el registro a menos de 30 min. Se mide con autorreporte y registro de uso.')
    note(s4, 'V2: suma lo que la V1 dejó abierto (impuestos, rutas, meses bajos, bienestar). Hipótesis: la alerta con acción se activa y la proyección falla ≤ 10 %.')
    note(s5, 'Paciente: casi no ve la app; reserva en la agenda de siempre y recibe mensajes con la voz de Joselyn. Hipótesis: confirma y paga con link sin ayuda.')
    prs.save(dst)
    return dst


# ================================================================ CANVAS + STORYBOARD
STORY = {
    'v1': ('Storyboard con propuesta de valor · V1',
           'Propuesta de valor V1: un tablero conectado a la agenda que ya usa. Cada atención se vuelve ganancia real, sin digitar.',
           ['Hoy: el Excel de noche', 'Conecta la agenda que ya usa', 'Cada cita es un ingreso', '“Atención realizada” en un toque', 'Tablero con semáforo', 'Lo que falta: febrero, rutas e impuestos'],
           ['Cuadra ingresos ~1 h después de atender.', 'En 10 min define 70/30, km y materiales.', 'Las citas del día ya muestran su ganancia.', 'Ve su ganancia neta al despedirse.', 'Mira su mes de un vistazo, entre pacientes.', 'Ve el mes bajo, pero no sabe qué hacer.']),
    'v2': ('Storyboard con propuesta de valor · V2',
           'Propuesta de valor V2: el copiloto financiero que convierte cada atención en ganancia real y le avisa qué viene, sin que tenga que digitar.',
           ['Martes = Machalí', 'Un toque reparte el pago', 'La hora vacía genera ingreso', 'Cierre antes de las 21 h', 'Lunes: el resumen llega solo', 'Avisa antes de la curva'],
           ['Domicilios agrupados: −9 km en el día.', 'Retención y colchón se apartan solos.', 'Ofrece el cupo libre y alguien lo toma.', 'Tres preguntas y a cenar con su familia.', 'Ganancia, colchón y renta por WhatsApp.', 'Febrero viene bajo: activa un pack.']),
    'p': ('Storyboard con propuesta de valor · paciente',
          'Para el paciente: reservar, confirmar y pagar en un minuto, con la voz de Joselyn, sin cambiar de agenda ni usar efectivo.',
          ['Reserva en un minuto', 'Recordatorio y confirmación', '“Voy en camino”', 'Paga con un link', 'Un cupo de último minuto', 'Seguimiento después del alta'],
          ['Camila reserva desde el Instagram de InMotion.', 'Don Luis confirma con un toque el día antes.', 'Sabe a qué hora llega Joselyn.', 'Sin efectivo; la boleta llega al correo.', 'Toma una hora libre con descuento.', 'Un mes después, reserva su mantención.']),
}


def build_canvas():
    src = TPL / 'Canvas.pptx'
    dst = OUT / 'EV2_Canvas_Storyboard_CopilotoKine.pptx'
    duplicate(src, dst, [('slide3.xml', 'slide3.xml'), ('slide3.xml', 'slide4.xml')])
    prs = Presentation(dst)
    s1, s2 = prs.slides[0], prs.slides[1]
    DARK = RGBColor(0x12, 0x10, 0x1E)
    GRAY = RGBColor(0x50, 0x4D, 0x6E)
    ORANGE = RGBColor(0xE8, 0x59, 0x0C)

    # ---- 1 · Portada
    sub = shape(s1, 'Subtítulo 2').text_frame
    set_runs(sub, ['Testeo propuesta de solución · Copiloto Kine', [('Integrantes: ', {'bold': True}), ('Francisco Ahumada, Claudia Cifuentes, Néstor Rivera y Benjamín Vera Yáñez', {})]], size=13)
    datos = shape(s1, 'CuadroTexto 4').text_frame
    items = [('Empresa: ', 'Copiloto Kine · caso Joselyn Toledo, kinesióloga (Centro Médico InMotion)'), ('Sección: ', SECCION),
             ('Asignatura: ', 'Innovación y Emprendimiento III (FGIE03)'), ('Docente: ', 'Roberto Escobar Donoso')]
    paras = []
    for k, v in items:
        paras += [[(k, {'bold': True, 'color': DARK}), (v, {'color': ORANGE if v == '___' else DARK})], '']
    set_runs(datos, paras[:-1], size=14)

    # ---- 2 · Business Model Canvas
    set_runs(shape(s2, 'Rectángulo 28').text_frame, [[('PROYECTO: ', {'bold': True}), ('Copiloto Kine', {})]], size=12, color=DARK)
    integ = shape(s2, 'Rectángulo 29'); integ.width = Inches(3.2); integ.height = Inches(0.62)
    set_runs(integ.text_frame, [[('Integrantes: ', {'bold': True}), ('F. Ahumada · C. Cifuentes · N. Rivera · B. Vera Yáñez', {})]], size=9, color=DARK)
    integ.text_frame.word_wrap = True
    for sh in s2.shapes:
        if sh.name == 'CuadroTexto 4' and sh.has_text_frame:
            set_runs(sh.text_frame, [[('Sección: ', {'bold': True}), (SECCION, {'color': ORANGE})]], size=11, color=DARK)
    posts = {'Poblema': ('Problema', 'No sabe cuánto gana: agenda y finanzas separadas y ~1 h de Excel al día.'),
             'Solución propuesta': ('Solución propuesta', 'Copiloto conectado a su agenda: ganancia real por atención y aviso de lo que viene.')}
    for g in [sh for sh in s2.shapes if sh.shape_type == 6]:
        for c in g.shapes:
            if c.has_text_frame and c.text_frame.text.strip() in posts:
                h, t = posts[c.text_frame.text.strip()]
                set_runs(c.text_frame, [[(h, {'bold': True, 'size': 8})], [(t, {'size': 6.5})]], color=DARK)
                c.text_frame.word_wrap = True
    blocks = {
        'socios': (0.45, 1.8, 1.92, 3.15, ['Google Calendar / Cal.com (API sin costo)', 'Clínicas como InMotion', 'Asesor financiero y contadoras: validación tributaria', 'Comunidad gremial de kinesiología', 'Servicios de mapas (rutas)', 'Medio de pago con link']),
        'actividades': (2.5, 1.5, 1.85, 1.35, ['Diseño y desarrollo low-code', 'Integración con la agenda', 'Onboarding y soporte', 'Reglas de retención vigentes']),
        'recursos': (2.5, 3.72, 1.85, 1.28, ['Equipo de Diseño Digital (UX/UI, Figma)', 'Prototipo funcional y datos', 'Co-creación con kinesiólogas']),
        'valor': (4.45, 1.5, 1.85, 3.5, ['Convierte cada atención en ganancia real y avisa qué viene, sin digitar', 'Se conecta a la agenda que ya usa', 'Ganancia neta con comisión, traslado y materiales', 'Retención y colchón apartados solos', 'Menos km y cero cierres nocturnos']),
        'relacion': (6.4, 1.78, 1.85, 1.08, ['Onboarding de 10 min con su Excel', 'Resumen semanal por WhatsApp', 'Co-creación continua']),
        'canales': (6.4, 3.45, 1.85, 1.55, ['Recomendación entre pares', 'Instagram y contenido educativo', 'Clínicas como InMotion', 'Comunidad gremial']),
        'segmentos': (8.35, 1.5, 1.85, 3.5, ['Kinesiólogas/os independientes con atención mixta, Rancagua y O’Higgins', 'Early adopters: 0–2 años de práctica particular (Joselyn, Catalina)', 'Usuarios indirectos: sus pacientes']),
        'costos': (0.45, 5.62, 4.85, 1.1, ['Diseño y desarrollo low-code · nube y APIs · soporte', 'Comisión del medio de pago · adquisición por contenido digital']),
        'ingresos': (5.42, 5.62, 4.75, 1.1, ['Suscripción de referencia $20.000–25.000/mes (disposición a pagar: $30.000–40.000)', 'Plan básico gratuito con el tablero mensual · precio a validar en la UA4']),
    }
    for k, (x, y, w, h, lines) in blocks.items():
        tb = textbox(s2, x, y, w, h, [[('• ' + l, {})] for l in lines], f'Contenido {k}', size=9, color=DARK, space_after=2)
    textbox(s2, 10.34, 4.75, 2.9, 1.9, [[('Espacio para la retroalimentación del asesor.', {'italic': True})]], 'Nota asesor', size=9, color=GRAY)

    # ---- 3, 4, 5 · Storyboard con propuesta de valor
    for s, key in zip(list(prs.slides)[2:5], ['v1', 'v2', 'p']):
        title, vp, heads, texts = STORY[key]
        t = s.shapes.title
        t.left, t.top, t.width, t.height = Inches(0.92), Inches(0.25), Inches(11.5), Inches(0.75)
        set_runs(t.text_frame, [title], size=30)
        band = box(s, 0.92, 1.08, 11.5, 0.62, 'Banda propuesta de valor', fill=RGBColor(0xFF, 0xF1, 0xE9))
        textbox(s, 1.12, 1.08, 11.1, 0.62, [[(vp, {'bold': True})]], 'Propuesta de valor', size=14, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
        W, H, GAP = 3.7, 2.0, 0.2
        for i in range(6):
            col, row = i % 3, i // 3
            x = 0.92 + col * (W + GAP)
            y = 1.88 + row * (H + 0.78)
            pic = s.shapes.add_picture(str(SB / f'{key}-0{i + 1}.jpg'), Inches(x), Inches(y), Inches(W))
            pic.name = f'Viñeta {i + 1}'
            ratio = W / H
            iw, ih = pic.image.size
            if iw / ih > ratio:   # recorte centrado a W×H
                crop = (1 - ratio * ih / iw) / 2
                pic.crop_left = pic.crop_right = crop
            else:
                crop = (1 - (iw / ratio) / ih) / 2
                pic.crop_top = pic.crop_bottom = crop
            pic.height = Inches(H); pic.width = Inches(W)
            num = box(s, x + 0.1, y + 0.1, 0.36, 0.36, f'Número {i + 1}', fill=ORANGE, kind=MSO_SHAPE.OVAL)
            set_runs(num.text_frame, [[(str(i + 1), {'bold': True, 'color': RGBColor(0xFF, 0xFF, 0xFF)})]], size=12, align=PP_ALIGN.CENTER)
            num.text_frame.margin_left = num.text_frame.margin_right = 0
            textbox(s, x, y + H + 0.06, W, 0.62, [[(heads[i], {'bold': True})], [(texts[i], {'color': GRAY})]], f'Texto viñeta {i + 1}', size=11, color=DARK)
    prs.save(dst)
    return dst


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for f in (build_prototipado(), build_canvas()):
        print('listo:', f.relative_to(ROOT.parent))
