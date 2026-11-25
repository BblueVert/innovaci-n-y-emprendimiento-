# Informe final ES4 (Unidades 1 a 4) sobre el formato Word oficial de la carpeta Sercotec.
# Clona los párrafos de muestra de la plantilla (título, subtítulo, texto) para conservar su formato exacto.
# Uso: python3 informe_u4.py → entregables/Informe_Final_Copiloto_Kine.docx
import copy
import os
import sys
from PIL import Image
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, Cm, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'unidad-3', 'ev3'))
import contenido as C3  # noqa: E402  (EV3: ciclos, cambios v3, comparativa)
from mockup import mock  # noqa: E402
import contenido_u4 as C  # noqa: E402

SRC = os.path.join(HERE, '..', 'material', 'sercotec_es4', 'formato_informe.docx')
OUT = os.path.join(HERE, 'entregables', 'Informe_Final_Copiloto_Kine.docx')
IMG = os.path.join(HERE, 'img')
EV3 = os.path.join(HERE, '..', '..', 'unidad-3', 'ev3')
RED = RGBColor(0xE3, 0x06, 0x13)
LINK_PITCH = '[pegar link del video del pitch]'
LINK_MIRO = '[pegar link del tablero Miro]'


# ---------------------------------------------------------------- imágenes compuestas
def strip(paths, out, h=900, gap=40, bg=(255, 255, 255)):
    ims = [Image.open(p).convert('RGBA') for p in paths]
    ims = [im.resize((round(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
    W = sum(i.width for i in ims) + gap * (len(ims) - 1)
    canvas = Image.new('RGBA', (W, h), bg + (255,))
    x = 0
    for im in ims:
        canvas.alpha_composite(im, (x, 0)); x += im.width + gap
    canvas.convert('RGB').save(out, quality=88)
    return out


def grid(paths, out, cols=3, w=700, gap=24):
    ims = [Image.open(p).convert('RGB') for p in paths]
    ims = [im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) for im in ims]
    h = max(i.height for i in ims); rows = (len(ims) + cols - 1) // cols
    canvas = Image.new('RGB', (cols * w + gap * (cols - 1), rows * h + gap * (rows - 1)), (255, 255, 255))
    for k, im in enumerate(ims):
        canvas.paste(im, ((k % cols) * (w + gap), (k // cols) * (h + gap)))
    canvas.save(out, quality=88)
    return out


def imagenes():
    os.makedirs(IMG, exist_ok=True)
    m = lambda p: os.path.join(EV3, mock(p))  # noqa: E731
    V1, V3 = '../prototipo/capturas_v1/', '../prototipo/capturas_v3/'
    return {
        'caso': os.path.join(EV3, 'img', '02-caso.jpg'),
        'v1': strip([m(V1 + '01_tablero.png'), m(V1 + '02_ruta_sugerida.png'), m(V1 + '05_ganancia_atencion.png'), m(V1 + '07_proyeccion.png')], os.path.join(IMG, 'prototipo_v1.jpg')),
        'v3': strip([m(V3 + '02_ganancia_por_hora.png'), m(V3 + '03_ruta.png'), m(V3 + '06_atencion_agua_buena.png'), m(V3 + '07_clase_grupal.png'), m(V3 + '08_resumen_canal.png')], os.path.join(IMG, 'prototipo_v3.jpg')),
        'paciente': strip([m('../prototipo/capturas_paciente/0%d' % i + s) for i, s in ((1, '_recordatorio_a.png'), (2, '_voy_en_camino_a.png'), (3, '_pago_comprobante_a.png'), (4, '_clase_grupal_a.png'))], os.path.join(IMG, 'vista_paciente.jpg')),
        'sb_v1': grid([os.path.join(EV3, 'img', 'storyboard', f'v1-0{i}.jpg') for i in range(1, 7)], os.path.join(IMG, 'storyboard_v1.jpg')),
        'sb_v3': grid([os.path.join(EV3, 'img', 'storyboard', f'v3-0{i}.jpg') for i in range(1, 7)], os.path.join(IMG, 'storyboard_v3.jpg')),
        'lean': os.path.join(HERE, 'entregables', '4.1.2.1_Lean_Canvas_Copiloto_Kine.png'),
    }


# ---------------------------------------------------------------- documento
class Informe:
    def __init__(self):
        self.d = docx.Document(SRC)
        ps = self.d.paragraphs
        self.tpl = {'h1': copy.deepcopy(ps[24]._p), 'h2': copy.deepcopy(ps[27]._p), 'p': copy.deepcopy(ps[25]._p)}
        body = self.d.element.body
        # quitar el contenido de ejemplo (desde "1 Introducción"), conservando la portada y la sección
        start = ps[24]._p
        el = start
        while el is not None:
            nxt = el.getnext()
            if el.tag != qn('w:sectPr'):
                body.remove(el)
            el = nxt
        self.body = body
        self.sect = body.find(qn('w:sectPr'))
        self.n1 = 0; self.n2 = 0

    def _clone(self, key, text, bold_prefix=None):
        p = copy.deepcopy(self.tpl[key])
        runs = p.findall(qn('w:r'))
        r0 = runs[0]
        for r in runs[1:]:
            p.remove(r)
        for t in r0.findall(qn('w:t')) + r0.findall(qn('w:br')):
            r0.remove(t)
        self.sect.addprevious(p)
        para = docx.text.paragraph.Paragraph(p, self.d._body)
        if bold_prefix:
            rb = copy.deepcopy(r0); r0.addprevious(rb)
            run_b = docx.text.run.Run(rb, para); run_b.text = bold_prefix; run_b.bold = True
        run = docx.text.run.Run(r0, para); run.text = text
        return para

    def cover(self):
        ps = self.d.paragraphs
        ps[2].runs[0].text = 'INFORME FINAL · COPILOTO KINE'
        for r in ps[2].runs[1:]:
            r.text = ''
        ps[3].runs[0].text = 'Innovación y Emprendimiento III · Unidades 1 a 4'
        for r in ps[3].runs[1:]:
            r.text = ''
        p = ps[8]
        base = copy.deepcopy(p.runs[0]._r)
        for r in list(p.runs):
            p._p.remove(r._r)
        lines = [('NOMBRE: ', ', '.join(C.EQUIPO)), ('CARRERA: ', C.CARRERA), ('ASIGNATURA: ', C.ASIGNATURA), ('PROFESOR: ', C.PROFESOR),
                 ('FECHA: ', '15-12-2026'), ('CASO: ', 'Josselyn Toledo, kinesióloga independiente · Centro Médico InMotion · San Fernando'),
                 ('LINK PITCH: ', LINK_PITCH), ('LINK MIRO: ', LINK_MIRO), ('PROTOTIPO: ', C.URL_PRO)]
        for i, (k, v) in enumerate(lines):
            for txt, bold in ((k, True), (v, False)):
                r = copy.deepcopy(base); p._p.append(r)
                run = docx.text.run.Run(r, p)
                for t in r.findall(qn('w:t')) + r.findall(qn('w:br')):
                    r.remove(t)
                run.text = txt; run.bold = bold
            if i < len(lines) - 1:
                p.runs[-1].add_break()

    def pagebreak(self):
        p = self._clone('p', '')
        p.runs[0].add_break(WD_BREAK.PAGE)

    def h1(self, text, new_page=True):
        if new_page and self.n1:
            self.pagebreak()
        self.n1 += 1; self.n2 = 0
        return self._clone('h1', f'{self.n1} {text}')

    def h2(self, text):
        self.n2 += 1
        return self._clone('h2', f'{self.n1}.{self.n2} {text}')

    def p(self, text, bold=None):
        para = self._clone('p', text, bold)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        return para

    def ul(self, items):
        for it in items:
            if isinstance(it, tuple):
                para = self._clone('p', it[1], '– ' + it[0] + ': ')
            else:
                para = self._clone('p', '– ' + it)
            para.paragraph_format.space_after = Pt(2)
            para.paragraph_format.left_indent = Cm(0.5)
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def quote(self, text, src):
        para = self._clone('p', f'“{text}”')
        para.runs[0].italic = True
        para.paragraph_format.left_indent = Cm(1); para.paragraph_format.right_indent = Cm(1)
        r = para.add_run(f' — {src}'); r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    def img(self, path, width_cm, caption):
        para = self._clone('p', '')
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.runs[0].add_picture(path, width=Cm(width_cm))
        cap = self._clone('p', caption)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in cap.runs:
            r.italic = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    def table(self, headers, rows, widths=None, size=8.5):
        t = self.d.add_table(rows=1, cols=len(headers))
        tblPr = t._tbl.tblPr
        borders = OxmlElement('w:tblBorders')
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:space'), '0'); e.set(qn('w:color'), 'BFBFBF')
            borders.append(e)
        tblPr.append(borders)
        w = OxmlElement('w:tblW'); w.set(qn('w:w'), '5000'); w.set(qn('w:type'), 'pct'); tblPr.append(w)
        self.sect.addprevious(t._tbl)
        for i, h in enumerate(headers):
            c = t.rows[0].cells[i]; c.text = ''
            r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(size); r.font.name = 'Tahoma'; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), 'E30613')
            c._tc.get_or_add_tcPr().append(sh)
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                cells[i].text = ''
                r = cells[i].paragraphs[0].add_run(str(v)); r.font.size = Pt(size); r.font.name = 'Tahoma'
                if i == 0:
                    r.bold = True
        if widths:
            for row in t.rows:
                for i, w in enumerate(widths):
                    row.cells[i].width = Cm(w)
        self._clone('p', '')
        return t

    def save(self):
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        self.d.save(OUT)


# ---------------------------------------------------------------- contenido del informe
def build():
    I = imagenes()
    R = Informe()
    R.cover()
    ESC = {e[0]: e for e in C.ESCENARIOS}
    esc = [C.escenario(n) for _, n, _ in C.ESCENARIOS]
    clp = lambda n: '$' + f'{round(n):,}'.replace(',', '.')  # noqa: E731

    # 1 · Introducción
    R.h1('Introducción', new_page=True)
    R.p('Este informe reúne el trabajo de las cuatro unidades de Innovación y Emprendimiento III aplicadas a un caso real: Josselyn Toledo, '
        'kinesióloga independiente de San Fernando que atiende en el Centro Médico InMotion, a domicilio, en una piscina temperada y en su propio '
        'gimnasio. Siguiendo el Ciclo de Innovación INACAP, el equipo diagnosticó su situación (Unidad 1), ideó una solución (Unidad 2), la '
        'prototipó y testeó en cuatro ciclos (Unidad 3) y, en esta última unidad, la convirtió en una propuesta de valor con modelo de negocio, '
        'factibilidad económica y un pitch para comunicarla al ecosistema territorial (Unidad 4).')
    R.p('El resultado es Copiloto Kine, una app web que conecta la agenda de la kinesióloga con sus ingresos y costos: convierte cada atención en '
        'ganancia real y ganancia por hora, valora el tiempo de viaje, sugiere cuánto cobrar por tramo rural y anticipa los meses bajos. El '
        'prototipo está publicado y se puede usar desde cualquier celular.')
    R.p('comunicar el potencial de Copiloto Kine como solución innovadora para kinesiólogas independientes de la Región de O’Higgins, '
        'demostrando su pertinencia, su factibilidad económica y su sostenibilidad.', 'Objetivo general: ')
    R.p('Objetivos específicos:', None)
    R.ul(['Sintetizar el diagnóstico, la ideación y el prototipado realizados en las unidades 1 a 3.',
          'Modelar el negocio con el Lean Canvas y estimar su factibilidad económica.',
          'Evaluar el impacto tecnológico, económico, sociocultural y medioambiental de la solución.',
          'Comunicar la propuesta de valor mediante un pitch de 3½ minutos y proyectar acciones de trabajo.'])

    # 2 · Antecedentes
    R.h1('Antecedentes de la empresa')
    R.h2('El caso: Josselyn Toledo')
    R.img(I['caso'], 12, 'Figura 1. Josselyn atiende en varios lugares y su oficina es el celular (ilustración del proyecto).')
    R.p('Josselyn Toledo es kinesióloga y psicomotricista acuática, con diplomados en fisiología del ejercicio y piso pélvico, y cerca de un año '
        'con empresa propia. Trabaja en un modelo mixto: en el Centro Médico InMotion, donde factura un monto mensual, y con pacientes particulares '
        'a domicilio en San Fernando y la precordillera (por ejemplo, Aguas Buenas), además de sesiones en una piscina temperada y entrenamientos '
        'en su gimnasio. Su propuesta de valor es la atención personalizada uno a uno: “Yo los trato como a mí me gustase que me tratasen”.')
    R.table(['Dato', 'Detalle'], [
        ('Nombre', 'Josselyn Toledo · kinesióloga independiente'),
        ('Ubicación', 'San Fernando y alrededores, Región de O’Higgins (Aguas Buenas, Las Cabras, camino a Roma)'),
        ('Actividad', 'Kinesiología, psicomotricidad acuática y entrenamiento personalizado'),
        ('Lugares de atención', 'Clínica InMotion (factura mensual), domicilios, piscina temperada y gimnasio propio'),
        ('Herramientas actuales', 'AgendaPro, agenda médica de la clínica, WhatsApp, notas del celular y contadora externa'),
        ('Vínculo con el ecosistema', 'Emprendedora apoyada por Sercotec; caso de estudio de la asignatura en INACAP Rancagua')], [4.5, 12.5])
    R.h2('Problemática principal')
    R.p('Josselyn no sabe cuánto gana realmente ni qué le conviene. Cada noche anota en el teléfono lo que ganó, lo que gastó en bencina y cuántas '
        'sesiones hizo; aun así, no puede comparar si le rinde más la clínica o un domicilio rural. El traslado —que en caminos de precordillera le '
        'toma 25 a 30 minutos por visita— no se mide ni se cobra, y los meses de enero y febrero llegan cada año como una sorpresa.')
    R.quote('Cada noche anoto todo… la ganancia, lo que gasto en bencina durante el día… cuántas sesiones hice y cuánto gané en cada sesión', 'Josselyn Toledo, reunión del 12/11')
    R.quote('Para poder organizar el Excel sobre los ingresos y egresos que estoy teniendo me toma una hora actualmente diario', 'Catalina, kinesióloga, entrevista UA1')

    # 3 · Unidad 1
    R.h1('Unidad 1 · Diagnóstico y selección de oportunidades')
    R.h2('Metodología')
    R.p('En la fase de diagnóstico aplicamos el toolkit de needfinding del Ciclo de Innovación INACAP durante las semanas 1 a 4:')
    R.ul([('Usuaria', 'canvas de 33 preguntas sobre los 9 bloques del modelo de negocio, card sorting en 9 categorías y entrevista en profundidad a Josselyn.'),
          ('Observación', 'pauta AEIOU por autorreporte guiado, ya que la atención ocurre en espacios privados.'),
          ('Expertos', 'una kinesióloga par (Catalina) y un asesor financiero de profesionales independientes.'),
          ('Entorno', 'matriz PESTAL y estudio comparativo de 8 antecedentes (AgendaPro, Encuadrado, Reservo, Medilink, Cal.com, Cliniko, Jane App y Nubox).'),
          ('Síntesis', 'vaciado de hallazgos, categorización de insights, mapa de priorización y redefinición del desafío.')])
    R.h2('Hallazgos e insights')
    R.p('Los hallazgos de la usuaria, los expertos y la observación se tradujeron en ocho insights. Siete se sostienen en las tres fuentes:')
    R.table(['#', 'Insight', 'Qué significa'], [
        ('I1', 'Ocupada no es lo mismo que rentable', 'No sabe cuánto gana en un mes promedio; decide sin datos.'),
        ('I2', 'La agenda es el origen del dato financiero', 'Cada cita es un ingreso proyectado que hoy se pierde (insight raíz).'),
        ('I3', 'El Excel como parche diario', '~1 h diaria de registro manual al cierre del día.'),
        ('I4', 'Impuestos como sorpresa', 'No se provisiona la retención ni la Operación Renta.'),
        ('I5', 'Los costos invisibles del domicilio', 'Traslado, combustible y tiempo no se descuentan por atención.'),
        ('I6', 'Inestabilidad sin memoria', 'Enero y febrero bajan y no hay historial para anticiparlo.'),
        ('I7', 'Fidelización informal por WhatsApp', 'El vínculo depende de que el paciente escriba.'),
        ('I8', 'Crecimiento sin plan', 'Quiere sumar servicios grupales e invertir, sin datos que lo respalden.')], [1.2, 5.5, 10.3])
    R.quote('«Estar ocupado» y «estar ganando dinero» no son lo mismo', 'asesor financiero, entrevista UA1')
    R.h2('Análisis del entorno')
    R.table(['Factor', 'Cambio', 'Oportunidad'], [(n, o['f'], o['o']) for n, o, _ in C3.PESTAL], [2.6, 7.2, 7.2])
    R.h2('Problemática seleccionada y desafío')
    R.p('El insight raíz es I2: la agenda y las finanzas viven separadas. Conectarlas habilita I1, I4 e I6, mientras I3 e I5 son victorias tempranas. '
        'Con la técnica “¿Cómo podríamos…?” el equipo redefinió el desafío:')
    R.quote(C.DESAFIO, 'desafío redefinido, UA1')
    R.p('Ese desafío se planteó para Rancagua; en la Unidad 3 la clienta mostró que su territorio real es San Fernando y sus alrededores, por lo que '
        'la solución se proyecta a toda la Región de O’Higgins.')

    # 4 · Unidad 2
    R.h1('Unidad 2 · Ideación de propuestas')
    R.h2('Referentes y tendencias')
    R.p('Estudiamos 10 referentes de otros ámbitos con cinco variables (captura automática del dato, visualización y proyección, cobro y costos, '
        'hábito y sostenibilidad): Uber Driver, YNAB, Fintual, Mercado Pago, Smart Fit, Duolingo, Strava, Google Maps, Too Good To Go y la propuesta '
        'de F22 del SII. Ninguno reúne las cinco: los que capturan el dato no lo proyectan y los que proyectan no lo capturan. De ahí salieron seis '
        'tendencias: el dato se captura solo, dinero con propósito, recurrencia que da estabilidad, hábitos de segundos, eficiencia como '
        'sostenibilidad y transparencia en tiempo real.')
    R.h2('Perfil de usuaria y requerimientos')
    R.p('Con el mapa de empatía de Josselyn definimos 13 requerimientos en 6 categorías. El núcleo: que la cita confirmada se convierta en ingreso sin '
        'digitar (R1), integrarse con la agenda que ya usa (R2), distinguir clínica y domicilio (R3), mostrar la ganancia neta (R4), usar lenguaje no '
        'contable (R5), cerrar el día en menos de 30 minutos (R6), descontar traslado y materiales (R8), proyectar meses bajos (R10–R11), provisionar '
        'la retención (R12) y no guardar datos clínicos (R13).')
    R.h2('Ideas, selección y co-creación')
    R.p('El brainstorming produjo 60 ideas; 13 quedaron en el cuadrante de originales y factibles. Comparamos tres caminos con seis criterios (1 a 5):')
    R.table(['Criterio', 'A · Copiloto Kine', 'B · Planilla inteligente', 'C · Agenda propia nueva'], [
        ('Responde al desafío', 5, 2, 4), ('Recursos internos', 4, 5, 2), ('Recursos externos', 4, 5, 2), ('Prototipable en la UA3', 4, 5, 2),
        ('Aporte sostenible', 5, 3, 3), ('Diferenciación', 5, 1, 2), ('Total (máx. 30)', 27, 21, 15)], [5.5, 3.8, 3.8, 3.9])
    R.p('Doce de las sesenta ideas nacieron directamente de lo que dijeron Josselyn, Catalina y el asesor. Catalina, además, declaró que pagaría entre '
        '$30.000 y $40.000 al mes por una herramienta que juntara agenda y finanzas; el asesor sugirió entre $8.000 y $25.000.')
    R.h2('Metáfora, atributos y propuesta de valor')
    R.p('La idea se conceptualizó con la metáfora del tablero y el copiloto de un auto de rally, con los atributos Anticipador, Legible de un vistazo, '
        'Automático y Sostenible. La propuesta de valor de la Unidad 2 fue:')
    R.quote(C3.PDV_EV2, 'propuesta de valor EV2')

    # 5 · Unidad 3
    R.h1('Unidad 3 · Prototipado y testeo')
    R.h2('Prototipo y versiones')
    R.p('Construimos Copiloto Kine como prototipo navegable en HTML para el celular, sin instalación, y lo iteramos tres veces. Cada versión se '
        'probó en un ciclo con un foco distinto, para no mezclar problemas de uso con problemas de exactitud o de ajuste a la realidad de la clienta.')
    R.img(I['sb_v1'], 15, 'Figura 2. Storyboard v1 con la propuesta de valor: un día de Josselyn con Copiloto Kine.')
    R.img(I['v1'], 14, 'Figura 3. Prototipo v1: tablero, ruta, ganancia por atención y proyección.')
    R.h2('Ciclos de testeo')
    R.table(['Ciclo', 'Foco y participantes', 'Resultado clave'], [
        ('1 · Funcional y estético', 'Equipo con perfil de usuaria · 11 tareas, auditoría WCAG AA, heurísticas', '7/11 tareas; 11 errores de contraste. No se podía corregir un error.'),
        ('2 · Técnico', 'Equipo técnico · 11 pruebas contra una hoja de referencia', '11/11 pruebas; cálculo exacto; brechas de integración (agenda real, respaldo).'),
        ('3 · Clienta y ecosistema', 'Josselyn, Sercotec y docentes INACAP (reunión del 12/11)', '12 hallazgos: usa AgendaPro, factura mensual, 4 lugares de trabajo, traslado rural.'),
        ('4 · Usuarias (planificado)', 'Josselyn y Catalina con la v3 en su celular', 'Tareas N1–N10, SUS y precio. Resultados pendientes.')], [3.6, 6.6, 6.8])
    R.h2('Lo que cambió con la clienta')
    R.p('La reunión del 12 de noviembre fue el ciclo que más cambió el producto. Josselyn validó el núcleo —“eso hago yo igual en el teléfono… '
        'simplemente no tengo esa aplicación”— y corrigió cuatro supuestos: no usa Google Calendar sino AgendaPro; la clínica le paga con una factura '
        'mensual; trabaja en cuatro lugares y no en dos; y en su territorio el traslado cuesta más en tiempo que en bencina. La pregunta de fondo pasó '
        'de “cuánto gané” a “qué me conviene”.')
    R.table(['Cambio en la v3', 'Origen'], [(c, h) for c, h, *_ in C3.CAMBIOS_V3], [12, 5])
    R.img(I['v3'], 15.5, 'Figura 4. Prototipo v3: ganancia por hora por canal, ruta en San Fernando, atención en Aguas Buenas, clase grupal y resumen por canal.')
    R.p(f'Verificación de la v3: {C3.V3_OK} de {len(C3.V3_TASKS)} tareas completadas, {C3.V3_CALC_OK} de {len(C3.R3["calculos"])} cálculos idénticos a la '
        f'referencia, {C3.V3_AXE} errores de accesibilidad WCAG AA y ningún botón bajo 44 px. Prototipo: {C.URL_PRO}')
    R.img(I['sb_v3'], 15, 'Figura 5. Storyboard iterado v3: un martes de Josselyn en InMotion, Aguas Buenas, la piscina, su casa y Las Cabras.')
    R.img(I['paciente'], 12, f'Figura 6. Vista paciente para personas mayores: recordatorio, “voy en camino”, pago y clase grupal ({C.URL_CLI}).')
    R.h2('Comparación con las otras propuestas')
    R.p('En la reunión se revisaron cuatro propuestas para el mismo caso. Dos se resuelven en Excel y una es un modelo de programas grupales. '
        'Copiloto Kine es la única que parte de la agenda, cuenta el tiempo de viaje y considera al paciente; por eso incorporamos la exportación a '
        'Excel y la clase grupal en vez de competir con ellas.')
    sym = {2: 'Sí', 1: 'Parcial', 0: 'No'}
    R.table(['Propuesta', 'Cita entra sola', 'Ganancia real', 'Traslado y tiempo', 'Ganancia por canal', 'Meses bajos', 'Exporta a Excel'],
            [(n, *[sym[v[i]] for i in (0, 1, 2, 3, 4, 6)]) for n, v, _ in C3.COMPARA], size=8)

    # 6 · Unidad 4
    R.h1('Unidad 4 · Propuesta de valor y modelo de negocio')
    R.h2('Propuesta de valor final')
    R.quote(C.LC['pdv'], 'propuesta de valor única')
    R.p(C3.PDV_V3)
    R.h2('Lean Canvas')
    R.img(I['lean'], 17, 'Figura 7. Lean Canvas de Copiloto Kine (instrumento 4.1.2.1).')
    R.p('Lectura del canvas:', None)
    R.ul([('Problema', 'no saber cuánto gana ni qué le conviene; traslado rural que no se cobra; meses bajos sin plan.'),
          ('Segmento', 'kinesiólogas independientes con atención mixta en O’Higgins; early adopters que ya registran a mano y atienden en zonas rurales.'),
          ('Solución', 'agenda que se convierte en ganancia real; ganancia por hora con tiempo de viaje; proyección con acciones y resumen para la contadora.'),
          ('Ventaja especial', 'nace del trabajo con una clienta real y su territorio; cruza agenda, traslado rural, retención chilena y paciente.'),
          ('Canales', 'piloto con la red de Josselyn, comunidades profesionales, contenido en redes y aliados como Sercotec.'),
          ('Métricas', 'adquisición, activación, retención, ingresos y referencia (métricas pirata).')])
    R.h2('Factibilidad económica')
    R.table(['Supuesto', 'Valor', 'Fundamento'], C.SUPUESTOS, [3.6, 3.8, 9.6])
    R.table(['Escenario año 1', 'Usuarias', 'Ingresos al mes', 'Margen al mes', 'Margen %', 'Ingresos al año'],
            [(n, e['n'], clp(e['ingresos_mes']), clp(e['margen_mes']), f"{e['margen_pct']} %", clp(e['ingresos_anio'])) for (n, _, _), e in zip(C.ESCENARIOS, esc)])
    R.p(f'Con 5 usuarias pagando se cubre la operación comercial (≈ {clp(C.OPEX)} al mes). El valor del tiempo de vida de una usuaria (≈ $240.000) es '
        'unas 16 veces su costo de adquisición (≈ $15.000), y el piloto opera con planes gratuitos por cerca de $900 al mes. Para la usuaria, la app '
        'se paga sola: cobrar el recargo de un solo tramo rural ($3.000 a $6.000) cubre casi el costo de todo el mes.')
    R.h2('Impacto')
    R.table(['Dimensión', 'Impacto esperado'], C.IMPACTOS, [3.4, 13.6])
    R.h2('Comunicación de la propuesta: pitch')
    R.p('El pitch de 3½ minutos sigue el guion 4.1.3.2 y la estructura de la presentación entregada: antecedentes, problema, solución, prototipo, '
        'acciones futuras y conclusiones.')
    R.ul([(t, x.split('. ')[0] + '.') for t, x in C.PITCH])
    R.p(f'Link del pitch: {LINK_PITCH}')

    # 7 · Sostenibilidad
    R.h1('Sostenibilidad y acciones futuras')
    R.h2('Evaluación de la sostenibilidad frente al desafío')
    R.p('El desafío pedía reducir a la mitad el tiempo de registro (de ~1 hora a menos de 30 minutos diarios). El prototipo cierra un día de siete '
        'atenciones en menos de un minuto y sin digitar montos; falta verificarlo con la agenda real en el MVP. La solución es sostenible en lo '
        'económico (precio bajo, costos operativos cubiertos con pocas usuarias), en lo social (tiempo personal recuperado, atención a adultos '
        'mayores, datos de salud protegidos) y en lo ambiental (menos kilómetros con la ruta sugerida).')
    R.h2('Hoja de ruta')
    R.table(['Cuándo', 'Acción', 'Responsable'], C.ACCIONES, [3, 11, 3])
    R.h2('Riesgos y mitigación')
    R.table(['Riesgo', 'Cómo lo enfrentamos'], C.RIESGOS, [5, 12])

    # 8 · Conclusión
    R.h1('Conclusión')
    R.p('Copiloto Kine nació de un hallazgo simple —la agenda y las finanzas de una kinesióloga independiente viven separadas— y se convirtió en una '
        'propuesta concreta, probada y con modelo de negocio. Cada unidad aportó una pieza: el diagnóstico mostró que estar ocupada no es lo mismo '
        'que ganar; la ideación encontró en otros rubros la forma de que el dato se genere solo; el prototipado nos enseñó que una conversación con la '
        'clienta cambia más el producto que varios ciclos internos; y el modelo de negocio confirmó que la solución puede sostenerse con un precio '
        'bajo y pocas usuarias.')
    R.p('Frente a las alternativas —agendas que solo agendan y planillas que hay que alimentar a mano— la propuesta se diferencia por partir de la '
        'agenda real, contar el tiempo de viaje en un territorio rural y pensar también en el paciente. El siguiente paso es ponerla en manos de '
        'Josselyn y de otras cinco kinesiólogas de la región en un piloto, y con esos resultados postular a fondos para escalar.')
    R.p('Como estudiantes de Diseño Digital, nuestro aporte fue la experiencia: escuchar a la usuaria, convertir sus palabras en pantallas claras y '
        'accesibles, y medir con evidencia antes de afirmar. Agradecemos a Josselyn Toledo, a Catalina, a Sercotec y a los docentes de INACAP '
        'por su tiempo y retroalimentación.')

    # 9 · Referencias
    R.h1('Referencias')
    for ref in ['INACAP (2026). Manual del estudiante y toolkit, Unidades 1 a 4 · Innovación y Emprendimiento III (FGIE03).',
                'Maurya, A. (2012). Running Lean: Iterate from Plan A to a Plan That Works. O’Reilly Media.',
                'McClure, D. (2007). Startup Metrics for Pirates: AARRR! 500 Startups.',
                'Superintendencia de Salud (2020). Registro Nacional de Prestadores Individuales de Salud: evolución 2010–2019.',
                'Ley N.° 21.133 (2019). Incorpora a los trabajadores independientes a los regímenes de protección social. BCN.',
                'Ley N.° 21.719 (2024). Regula la protección y el tratamiento de los datos personales. BCN.',
                'W3C (2018). Web Content Accessibility Guidelines (WCAG) 2.1.',
                'Equipo del proyecto (2026). Informes EV1, EV2 y EV3; entrevistas a Josselyn Toledo, Catalina y un asesor financiero; transcripción de la '
                'reunión de retroalimentación del 12 de noviembre de 2026.']:
        R.p(ref)
    R.save()
    print('ok', OUT)


if __name__ == '__main__':
    build()
