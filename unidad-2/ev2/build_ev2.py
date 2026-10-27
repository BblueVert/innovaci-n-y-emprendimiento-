# Genera el Informe EV2 (A4 vertical) — Innovación y Emprendimiento III, Unidad 2.
# Uso:  python3 build_ev2.py   →  Evaluacion2_Informe_Ideacion.html / .pdf
import os
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- utilidades
def sus(*tags):
    names = {'Ec': 'ec', 'So': 'so', 'Am': 'am'}
    return ''.join(f'<span class="sus {names[t]}">{t}</span>' for t in tags)

def table(headers, rows, cls=''):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

STMT = {}

def section(sid, label, kicker, title, body, code=None):
    c = f'<span class="code">{code}</span>' if code else ''
    st = f'<div class="stmt">{STMT[sid]}</div>' if sid in STMT else ''
    return f'''<div class="section" id="{sid}"><div class="section-head" data-sec="{label}">
<div class="kicker">{kicker}</div><h2>{c}{title}</h2></div>{st}{body}</div>'''

def card(cols):
    return '<div class="inst-card">' + ''.join(f'<div class="col"><div class="lbl">{l}</div>{v}</div>' for l, v in cols) + '</div>'

PEND = '<span class="pend">Pendiente de sesión</span>'
DOT = {2: '<span class="dot d2">●</span>', 1: '<span class="dot d1">◐</span>', 0: '<span class="dot d0">○</span>'}

DESAFIO = ('¿Cómo podríamos aumentar la visibilidad financiera de kinesiólogas independientes con atención mixta, '
           'conectando su agenda con sus ingresos y costos, para reducir a la mitad el tiempo de registro manual '
           '(de ~1 h a menos de 30 min diarios) en Rancagua durante 2027?')
EQUIPO = ['Francisco Ahumada', 'Claudia Cifuentes', 'Néstor Rivera', 'Benjamín Vera Yáñez']
PRODUCTO = 'Copiloto Kine'

# ---------------------------------------------------------------- datos: referentes (2.1.2.1)
REFS = [
    dict(n='Uber Driver', amb='Movilidad · app del conductor', src='uber.com/cl', v=[2, 1, 2, 1, 1], s=['Ec'],
         d='App con la que el conductor recibe viajes, ve sus ganancias por viaje, día y semana, y cobra de forma automática al terminar cada servicio.',
         r='La ganancia aparece en el momento en que termina el servicio, no al final del mes. Tarifa calculada por distancia y tiempo.',
         a='Mostrar la ganancia neta de cada atención apenas termina, con el costo del traslado ya descontado.', t='T1 · T6'),
    dict(n='YNAB', amb='Finanzas personales', src='ynab.com', v=[1, 2, 0, 2, 2], s=['Ec', 'So'],
         d='Método y app de presupuesto basado en asignar a cada peso un propósito antes de gastarlo, incluidos los gastos futuros e irregulares.',
         r='Separa el dinero por propósito y prepara los gastos que todavía no llegan. Incluye educación financiera en la herramienta.',
         a='Reservar en cada cobro la retención de la boleta y un colchón para los meses bajos.', t='T2'),
    dict(n='Fintual', amb='Inversión · fintech chilena', src='fintual.cl', v=[1, 2, 0, 1, 2], s=['Ec'],
         d='Plataforma de inversión que presenta metas con gráficos de proyección y un lenguaje simple, sin jerga financiera.',
         r='Proyección visual de metas en el tiempo y comunicación cercana.',
         a='Explicar la proyección a 3–6 meses en palabras cotidianas: “en marzo vas a necesitar…”.', t='T2'),
    dict(n='Mercado Pago', amb='Fintech · medios de pago', src='mercadopago.cl', v=[2, 1, 2, 0, 1], s=['Ec', 'Am'],
         d='Medio de cobro con link de pago, código QR y lector de tarjetas; cada transacción queda registrada en reportes descargables.',
         r='El cobro genera el dato financiero sin digitarlo. Sin efectivo ni comprobantes en papel.',
         a='Cobrar en el domicilio y que el pago alimente solo el registro de la atención.', t='T1 · T6'),
    dict(n='Smart Fit', amb='Fitness · membresías', src='smartfit.cl', v=[1, 0, 2, 1, 1], s=['Ec'],
         d='Cadena de gimnasios con planes mensuales y cobro recurrente automático.',
         r='Ingreso predecible mes a mes gracias a la recurrencia.',
         a='Packs prepagados y una membresía de mantención post-alta para estabilizar los ingresos.', t='T3'),
    dict(n='Duolingo', amb='Educación · aprendizaje de idiomas', src='duolingo.com', v=[0, 1, 0, 2, 1], s=['So'],
         d='App de idiomas que sostiene un hábito diario con rachas, recordatorios y metas muy cortas.',
         r='Convierte una tarea pesada en un gesto diario de segundos.',
         a='Cierre del día en un gesto y rachas para los ejercicios en casa del paciente.', t='T4'),
    dict(n='Strava', amb='Deporte · comunidad', src='strava.com', v=[2, 2, 0, 2, 1], s=['So'],
         d='Red social deportiva que registra la actividad por GPS, muestra el progreso y agrupa a los usuarios en clubes.',
         r='El registro ocurre solo mientras se hace la actividad; el progreso se ve en una pantalla.',
         a='Registro automático por atención y comunidad para los grupos de adultos mayores.', t='T1 · T4'),
    dict(n='Google Maps', amb='Navegación · rutas', src='google.com/maps', v=[2, 1, 1, 0, 2], s=['Am', 'Ec'],
         d='Mapas con rutas de varias paradas y registro de trayectos; en algunos países sugiere la ruta de menor consumo de combustible.',
         r='Optimiza el recorrido y registra los kilómetros sin intervención del usuario.',
         a='Agrupar los domicilios por sector y calcular el costo real del traslado.', t='T5'),
    dict(n='Too Good To Go', amb='Alimentación · excedentes', src='toogoodtogo.com', v=[0, 0, 2, 1, 2], s=['Am', 'Ec'],
         d='App que vende a precio reducido la comida que los locales no vendieron, evitando que se pierda.',
         r='Convierte una capacidad ociosa en ingreso y en impacto ambiental positivo.',
         a='Ofrecer los cupos libres de último minuto a precio preferente: la hora vacía también genera ingreso.', t='T5'),
    dict(n='SII · Propuesta de F22', amb='Servicio público · tributación', src='sii.cl', v=[2, 1, 1, 0, 1], s=['Ec'],
         d='El Servicio de Impuestos Internos prepara una propuesta de declaración anual de renta con la información de las boletas emitidas.',
         r='El contribuyente parte desde una propuesta ya calculada, no desde una hoja en blanco.',
         a='Mostrar cada mes una “propuesta” de lo que habrá que pagar o recibir en la Operación Renta.', t='T2'),
]
VARS = ['V1 Captura automática del dato', 'V2 Visualización y proyección', 'V3 Cobro, costos y precio', 'V4 Hábito y relación', 'V5 Sostenibilidad']

TEND = [
    ('T1', 'El dato se captura solo', 'Uber · Mercado Pago · Strava · Google Maps', 'Cada atención realizada debe generar su registro sin digitar.', ['Ec', 'So']),
    ('T2', 'Dinero con propósito y proyección legible', 'YNAB · Fintual · SII', 'Separar retención y colchón; proyectar en lenguaje cotidiano.', ['Ec']),
    ('T3', 'Recurrencia que da estabilidad', 'Smart Fit', 'Packs y membresías aplanan la curva estacional.', ['Ec']),
    ('T4', 'Hábitos de segundos y comunidad', 'Duolingo · Strava', 'El cierre diario debe durar segundos; la comunidad sostiene la adherencia.', ['So']),
    ('T5', 'Eficiencia como sostenibilidad', 'Google Maps · Too Good To Go', 'Menos kilómetros y horas vacías aprovechadas: ahorro y menor impacto.', ['Am', 'Ec']),
    ('T6', 'Transparencia en tiempo real', 'Uber · Mercado Pago', 'Ver la ganancia al instante genera confianza en la herramienta.', ['Ec']),
]

# ---------------------------------------------------------------- datos: requerimientos (2.1.3)
EMPATIA = [
    ('¿Qué piensa y qué siente?', 'Siente que tiene “cierto desorden o falta de educación” en lo económico. Está orgullosa de su trato personalizado, pero insegura ante una carrera que describe como “muy inestable”.'),
    ('¿Qué ve?', 'Centros con atención masiva; colegas que usan Cal.com o AgendaPro; una clínica donde la secretaria gestiona la agenda; su propio Excel y el calendario del celular.'),
    ('¿Qué oye?', 'A la contadora hablando de retenciones y Operación Renta; a pacientes que piden hora por WhatsApp; a pares que dicen que llevar el orden “ha sido complejo”.'),
    ('¿Qué dice y qué hace?', 'Atiende de 10 a 32 h semanales, de lunes a sábado, en clínica (70/30) y a domicilio. Coordina por WhatsApp, prepara materiales según patología y registra ingresos y gastos en Excel al cierre del día.'),
    ('¿Qué le duele?', 'No saber cuánto gana realmente; los meses bajos que llegan por sorpresa; el tiempo administrativo fuera del horario de atención; los costos del domicilio que no ve; los impuestos anuales.'),
    ('¿A qué aspira?', 'A una práctica estable que le permita crecer: sumar kinesiólogos por comisión, abrir grupos para adultos mayores e invertir en presoterapia, decidiendo con datos.'),
]
REQS = [
    ('I2', 'La agenda es el origen del dato financiero', [
        ('R1', 'Convertir cada cita confirmada en un ingreso proyectado, sin volver a digitarla.', 'Funcional', ['Ec']),
        ('R2', 'Integrarse con la agenda que ya usa (Google Calendar, Cal.com, WhatsApp) en lugar de reemplazarla.', 'Negocio', ['Ec', 'Am']),
        ('R3', 'Distinguir el ingreso de clínica (comisión 70/30) del ingreso a domicilio.', 'Funcional', ['Ec'])]),
    ('I1', 'Ocupada no es lo mismo que rentable', [
        ('R4', 'Mostrar la ganancia neta por atención, por semana y por mes.', 'Funcional', ['Ec']),
        ('R5', 'Usar lenguaje no contable y una lectura de menos de 1 minuto desde el celular.', 'Experiencia', ['So'])]),
    ('I3', 'El Excel como parche diario', [
        ('R6', 'Cerrar el día en menos de 30 minutos, idealmente con una confirmación de un toque por atención.', 'Experiencia', ['So']),
        ('R7', 'Permitir el registro en el momento de la atención, no al final del día.', 'Experiencia', ['So'])]),
    ('I5', 'Los costos invisibles del domicilio', [
        ('R8', 'Descontar por atención el traslado (km y combustible) y los materiales usados.', 'Funcional', ['Ec']),
        ('R9', 'Sugerir agrupar los domicilios por sector para reducir los kilómetros.', 'Funcional', ['Am', 'Ec'])]),
    ('I6', 'Inestabilidad sin memoria', [
        ('R10', 'Construir un historial y proyectar 3 a 6 meses considerando la estacionalidad.', 'Funcional', ['Ec']),
        ('R11', 'Alertar los meses bajos con anticipación y sugerir acciones (packs, campañas).', 'Funcional', ['Ec', 'So'])]),
    ('I4', 'Impuestos como sorpresa', [
        ('R12', 'Provisionar la retención vigente de la boleta de honorarios y estimar la Operación Renta.', 'Legal', ['Ec']),
        ('R13', 'Guardar solo datos financieros y de agenda, nunca la ficha clínica (Ley 21.719).', 'Legal', ['So'])]),
]
CATS = [
    ('C1', 'Agenda conectada', ['Que la cita genere el dato financiero', 'No cambiar de herramienta de agenda'], ['R1', 'R2', 'R3']),
    ('C2', 'Visibilidad de la ganancia real', ['Saber cuánto gana realmente', 'Entender sin lenguaje contable'], ['R4', 'R5']),
    ('C3', 'Tiempo y bienestar', ['Recuperar el tiempo fuera de horario', 'Bajar la carga mental del cierre del día'], ['R6', 'R7']),
    ('C4', 'Costos y rutas del domicilio', ['Conocer el costo real de cada visita', 'Recorrer menos kilómetros'], ['R8', 'R9']),
    ('C5', 'Anticipación y estabilidad', ['Prever los meses bajos', 'Tener un colchón para decidir con calma'], ['R10', 'R11']),
    ('C6', 'Cumplimiento y confianza', ['Evitar la sorpresa tributaria', 'Proteger sus datos y los de sus pacientes'], ['R12', 'R13']),
]
# posición en el mapa de jerarquías: (impacto en sostenibilidad 0–1, frecuencia del dolor 0–1)
JER = {'C1': (.80, .78), 'C2': (.93, .58), 'C3': (.62, .93), 'C4': (.57, .64), 'C5': (.82, .34), 'C6': (.72, .12)}
PRIO = [('1', 'C1 · C2', 'Núcleo de la solución: sin agenda conectada no hay dato, y sin dato no hay ganancia visible.'),
        ('2', 'C3 · C4', 'Victorias tempranas: liberan tiempo y muestran el costo del domicilio desde la primera semana.'),
        ('3', 'C5', 'Requiere historial: se activa cuando hay 2 a 3 meses de datos.'),
        ('4', 'C6', 'Alto impacto pero dolor anual: se resuelve sobre la base de C1 y C2.')]

# ---------------------------------------------------------------- datos: brainstorming (2.1.4.1)
CATN = {'A': 'Agenda conectada', 'B': 'Visibilidad financiera', 'C': 'Costos y rutas', 'D': 'Anticipación y estabilidad',
        'E': 'Impuestos y datos', 'F': 'Relación y comunidad', 'G': 'Tiempo y bienestar', 'H': 'Exploratorias'}
CATC = {'A': '#DCE3FF', 'B': '#FFE0D3', 'C': '#D3EFEB', 'D': '#FFEBCC', 'E': '#E9DDF2', 'F': '#FBDDE3', 'G': '#D8EFE2', 'H': '#ECEBF2'}
# (texto, categoría, originalidad 1-5, factibilidad 1-5, sostenibilidad, voz de usuaria/experto)
IDEAS = [
    ('Conector con Google Calendar / Cal.com que convierte citas en ingresos proyectados', 'A', 3, 5, ['Ec'], 'Catalina'),
    ('Botón “atención realizada” en la notificación al terminar la cita', 'A', 3, 5, ['So'], ''),
    ('Confirmación de cita por WhatsApp con un toque que actualiza la proyección', 'A', 2, 5, [], ''),
    ('Etiqueta automática clínica / domicilio según el lugar de la cita', 'A', 3, 4, ['Ec'], ''),
    ('Lista de espera que llena las cancelaciones', 'A', 3, 3, ['Ec'], ''),
    ('Bloqueo automático del tiempo de traslado entre domicilios', 'A', 3, 4, ['Am'], ''),
    ('Agendar por voz: “agenda a Juan el jueves a las 10”', 'A', 4, 2, [], ''),
    ('IA que lee los chats de WhatsApp y detecta citas', 'A', 5, 2, [], ''),
    ('Tablero “ganancia real del mes” con semáforo', 'B', 3, 5, ['Ec'], ''),
    ('Ganancia neta de cada atención visible al cerrarla', 'B', 4, 4, ['Ec'], 'Asesor'),
    ('Reporte semanal automático por WhatsApp', 'B', 3, 5, ['So'], ''),
    ('Comparador clínica 70/30 vs. domicilio: ¿dónde gano más por hora?', 'B', 4, 4, ['Ec'], 'Joselyn'),
    ('Meta mensual con anillo de avance', 'B', 3, 5, [], ''),
    ('Calculadora “¿me conviene tomar este paciente?”', 'B', 4, 3, ['Ec'], ''),
    ('Resumen anual de la práctica estilo “Wrapped”', 'B', 5, 3, ['So'], ''),
    ('Exportar el mes a Excel para la contadora', 'B', 1, 5, [], ''),
    ('Costo por km configurable y descuento automático en cada domicilio', 'C', 4, 4, ['Ec', 'Am'], 'Catalina'),
    ('Kit de materiales por patología con su costo asociado', 'C', 4, 4, ['Ec'], 'Joselyn'),
    ('Ruta del día que agrupa los domicilios', 'C', 3, 4, ['Am'], ''),
    ('Tarifa de domicilio por zona de Rancagua', 'C', 2, 5, ['Ec'], ''),
    ('Huella de carbono semanal según los km recorridos', 'C', 5, 3, ['Am'], ''),
    ('Días por sector: “martes = Machalí”', 'C', 4, 4, ['Am', 'Ec'], ''),
    ('Registrar gastos con foto de la boleta', 'C', 2, 4, [], ''),
    ('Compartir auto e insumos con otra kinesióloga', 'C', 4, 2, ['Am'], ''),
    ('Proyección de 3 a 6 meses desde la agenda y el historial', 'D', 4, 4, ['Ec'], ''),
    ('Alerta temprana de meses bajos con acciones sugeridas', 'D', 4, 4, ['Ec', 'So'], 'Asesor'),
    ('Packs prepagados de 4 y 8 sesiones', 'D', 2, 5, ['Ec'], ''),
    ('Membresía de mantención post-alta', 'D', 3, 4, ['Ec', 'So'], ''),
    ('Colchón automático: un % de cada pago para los meses bajos', 'D', 4, 4, ['Ec'], 'Asesor'),
    ('Cupos de último minuto a precio preferente', 'D', 4, 4, ['Ec', 'Am'], ''),
    ('Convenios con clubes deportivos para la temporada de lesiones', 'D', 3, 3, ['Ec'], ''),
    ('Simulador “¿qué pasa si sumo un kinesiólogo por comisión?”', 'D', 4, 3, ['Ec'], 'Joselyn'),
    ('Provisión automática de la retención de cada boleta', 'E', 4, 4, ['Ec'], 'Asesor'),
    ('Termómetro de la Operación Renta en pesos', 'E', 4, 4, ['Ec'], 'Asesor'),
    ('Sobres para separar lo personal de lo profesional', 'E', 3, 3, ['Ec'], 'Asesor'),
    ('Recordatorios tributarios clave (abril)', 'E', 2, 5, [], ''),
    ('Privacidad por diseño: solo datos financieros, nunca ficha clínica', 'E', 3, 5, ['So'], ''),
    ('Emitir la boleta de honorarios desde la app', 'E', 3, 2, [], ''),
    ('Aviso automático “voy en camino” al paciente', 'F', 3, 4, ['So'], ''),
    ('Rachas para los ejercicios en casa del paciente', 'F', 4, 3, ['So'], ''),
    ('Tarjeta de progreso del paciente (dolor y movilidad)', 'F', 4, 3, ['So'], ''),
    ('Grupos de adultos mayores con cupos y cobro grupal', 'F', 3, 3, ['So', 'Ec'], 'Joselyn'),
    ('Seguimiento post-alta automático a los 30 días', 'F', 3, 4, ['So'], 'Catalina'),
    ('Pedir reseña en Google al dar el alta', 'F', 2, 5, [], ''),
    ('Programa de referidos', 'F', 2, 4, ['Ec'], ''),
    ('Comunidad de kinesiólogas independientes de Rancagua con datos comparados', 'F', 4, 3, ['So'], ''),
    ('Cierre del día en 3 preguntas (menos de 5 min)', 'G', 3, 5, ['So'], 'Catalina'),
    ('Modo “no trabajo de noche”: el cierre se hace antes de las 21 h', 'G', 4, 4, ['So'], ''),
    ('Indicador de horas recuperadas al mes', 'G', 4, 5, ['So'], ''),
    ('Asistente IA que responde WhatsApp fuera de horario', 'G', 4, 3, ['So'], ''),
    ('Plantillas de mensajes con su propia voz', 'G', 2, 5, ['So'], 'Joselyn'),
    ('Onboarding de 10 min importando su Excel actual', 'G', 3, 4, [], ''),
    ('Lentes de realidad aumentada que registran la sesión', 'H', 5, 1, [], ''),
    ('Puntos InMotion canjeables por los pacientes', 'H', 5, 2, [], ''),
    ('IA que predice lesiones estacionales según el clima', 'H', 5, 2, [], ''),
    ('Marketplace de kinesiólogas a domicilio administrado por Joselyn', 'H', 4, 2, ['Ec'], 'Joselyn'),
    ('Auto eléctrico compartido entre kinesiólogas', 'H', 5, 1, ['Am'], ''),
    ('Presoterapia en arriendo por horas', 'H', 4, 2, ['Ec'], 'Joselyn'),
    ('Reembolso automático con Fonasa e isapres', 'H', 4, 2, ['Ec'], ''),
    ('Sello “práctica sostenible” para profesionales de salud', 'H', 5, 2, ['So', 'Am'], ''),
]
IDEAS = [dict(id=f'{i + 1:02d}', t=t, c=c, o=o, f=f, s=s, v=v) for i, (t, c, o, f, s, v) in enumerate(IDEAS)]
quad = lambda i: ('+O' if i['o'] >= 4 else '-O') + ('+F' if i['f'] >= 4 else '-F')
BYID = {i['id']: i for i in IDEAS}
GRUPOS = [
    ('Ganancia real por atención', 'B', ['10', '12', '17', '18'], 'Cada atención muestra su ganancia neta, con comisión, traslado y materiales descontados.'),
    ('Anticipación y colchón', 'D', ['25', '26', '29', '30'], 'Proyecta los meses que vienen, avisa los bajos y transforma horas vacías en ingreso.'),
    ('Impuestos sin sorpresa', 'E', ['33', '34'], 'Separa la retención en cada cobro y muestra en pesos la Operación Renta que viene.'),
    ('Tiempo y rutas sostenibles', 'G', ['22', '48', '49'], 'Menos km y cero trabajo nocturno: el tiempo recuperado vuelve a la atención 1:1.'),
]
BASE = ['01', '02', '47']

# ---------------------------------------------------------------- piezas visuales
def jerarquias_svg():
    W, H, P = 620, 400, 46
    x = lambda v: P + v * (W - 2 * P)
    y = lambda v: H - P - v * (H - 2 * P)
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Plus Jakarta Sans">',
         f'<rect x="{P}" y="{P}" width="{W - 2 * P}" height="{H - 2 * P}" fill="#F8F7FF" stroke="#E2E0EF"/>',
         f'<rect x="{x(.5)}" y="{P}" width="{W / 2 - P}" height="{H / 2 - P}" fill="rgba(255,107,53,.08)"/>',
         f'<line x1="{x(.5)}" y1="{P}" x2="{x(.5)}" y2="{H - P}" stroke="#C9C6DA" stroke-dasharray="4 4"/>',
         f'<line x1="{P}" y1="{y(.5)}" x2="{W - P}" y2="{y(.5)}" stroke="#C9C6DA" stroke-dasharray="4 4"/>',
         f'<text x="{W / 2}" y="{H - 14}" text-anchor="middle" font-family="DM Mono" font-size="9" fill="#504D6E" letter-spacing="1.5">EJE 1 · IMPACTO EN LA SOSTENIBILIDAD DE LA PRÁCTICA →</text>',
         f'<text transform="translate(16 {H / 2}) rotate(-90)" text-anchor="middle" font-family="DM Mono" font-size="9" fill="#504D6E" letter-spacing="1.5">EJE 2 · FRECUENCIA DEL DOLOR →</text>',
         f'<text x="{x(.5) + 8}" y="{y(.5) - 8}" font-family="DM Mono" font-size="8.5" fill="#FF6B35" letter-spacing="1.2">PRIORIDAD ALTA</text>',
         f'<text x="{P + 8}" y="{H - P - 8}" font-family="DM Mono" font-size="8.5" fill="#9B98B8" letter-spacing="1.2">PRIORIDAD BAJA</text>',
         f'<text x="{P + 4}" y="{P - 6}" font-family="DM Mono" font-size="8" fill="#9B98B8">diaria</text>',
         f'<text x="{P + 4}" y="{H - P + 12}" font-family="DM Mono" font-size="8" fill="#9B98B8">anual</text>']
    for code, name, nec, reqs in CATS:
        cx, cy = x(JER[code][0]), y(JER[code][1])
        s.append(f'<circle cx="{cx}" cy="{cy}" r="17" fill="#D9D2FF" stroke="#7B3FA0" stroke-width="1"/>')
        s.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="Bebas Neue" font-size="15" fill="#12101E">{code}</text>')
        lx = cx - 24
        s.append(f'<text x="{lx}" y="{cy - 2}" text-anchor="end" font-size="9" font-weight="700" fill="#12101E">{name}</text>')
        w = 24 * len(reqs) + 4
        s.append(f'<rect x="{lx - w}" y="{cy + 3}" width="{w}" height="13" rx="3" fill="#FFD6C2" stroke="#E8637A" stroke-width=".6"/>')
        s.append(f'<text x="{lx - w / 2}" y="{cy + 12.5}" text-anchor="middle" font-family="DM Mono" font-size="7.5" fill="#12101E">{" · ".join(reqs)}</text>')
    s.append('</svg>')
    return ''.join(s)

def collage_svg():
    return '''<svg viewBox="0 0 380 250" xmlns="http://www.w3.org/2000/svg" font-family="DM Mono" width="100%">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF6B35"/><stop offset=".6" stop-color="#E8637A"/><stop offset="1" stop-color="#7B3FA0"/></linearGradient></defs>
<rect width="380" height="250" rx="10" fill="url(#g)"/>
<path d="M-5 225 C70 180 130 230 190 195 S300 150 385 170" stroke="#12101E" stroke-width="18" fill="none"/>
<path d="M-5 225 C70 180 130 230 190 195 S300 150 385 170" stroke="#fff" stroke-width="1.6" stroke-dasharray="9 7" fill="none"/>
<g transform="translate(18,18)"><rect width="215" height="118" rx="10" fill="#12101E"/>
<path d="M18 92 A44 44 0 0 1 106 92" stroke="#3A3F63" stroke-width="9" fill="none"/><path d="M18 92 A44 44 0 0 1 88 58" stroke="#FF6B35" stroke-width="9" fill="none"/>
<line x1="62" y1="92" x2="84" y2="62" stroke="#fff" stroke-width="3" stroke-linecap="round"/><circle cx="62" cy="92" r="5" fill="#fff"/>
<path d="M126 92 A36 36 0 0 1 198 92" stroke="#3A3F63" stroke-width="7" fill="none"/><path d="M126 92 A36 36 0 0 1 168 57" stroke="#8BE3B4" stroke-width="7" fill="none"/>
<line x1="162" y1="92" x2="170" y2="64" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/><circle cx="162" cy="92" r="4" fill="#fff"/>
<text x="14" y="20" fill="#FF6B35" font-size="9" letter-spacing="1">COPILOTO KINE</text>
<text x="62" y="111" fill="#fff" font-size="7" text-anchor="middle">GANANCIA DEL MES</text><text x="162" y="111" fill="#fff" font-size="7" text-anchor="middle">COLCHÓN</text></g>
<g transform="translate(250,18)"><rect width="40" height="104" rx="9" fill="#12101E"/><circle cx="20" cy="22" r="11" fill="#3A3F63"/><circle cx="20" cy="52" r="11" fill="#FFD23F"/><circle cx="20" cy="82" r="11" fill="#3A3F63"/></g>
<g transform="translate(300,22)"><rect width="66" height="62" rx="8" fill="#fff"/><text x="8" y="18" font-size="7.5" fill="#12101E">Alerta</text><text x="8" y="32" font-size="7.5" fill="#12101E">febrero</text><text x="8" y="46" font-size="7.5" fill="#12101E">viene bajo</text></g>
<text x="190" y="243" text-anchor="middle" fill="#fff" font-size="7.5" letter-spacing="1.5">RUTA DEL DÍA · DOMICILIOS AGRUPADOS</text></svg>'''

# ---------------------------------------------------------------- secciones
def portada():
    chips = ''.join(f'<span class="chip">{c}</span>' for c in [
        '2.1.2.1 Referentes', '2.1.3.1 Perfil y requerimientos', '2.1.3.2 Categorías', '2.1.3.3 Jerarquías',
        '2.1.4.1 Brainstorming', '2.1.4.2 Clasificación de ideas', '2.1.4.3 Metáforas y atributos', '2.1.4.4 Propuesta de valor'])
    return f'''<div class="cover"><div class="bar"></div>
<img class="hero" src="img/01-portada.jpg">
<div><div class="inst" style="color:var(--accent)">Innovación y Emprendimiento III · INACAP Rancagua</div></div>
<div><h1>EVALUACIÓN<br>N°2</h1>
<div class="sub">IDEACIÓN DE PROPUESTAS</div><div class="inst" style="margin-top:2mm">Informe sumativo grupal · Unidad de Aprendizaje N°2 · FGIE03</div><div class="div"></div>
<div class="desc">Fase de generación de ideas del Ciclo de Innovación INACAP aplicada al caso de Joselyn Toledo, kinesióloga independiente con
atención mixta (Centro Médico InMotion + domicilio). Desde el estudio de referentes hasta la propuesta de valor y sus métricas claves,
con enfoque sostenible y trazabilidad a los criterios 2.1.1 a 2.1.5.</div>
<div class="grid">{chips}</div></div>
<div class="meta"><div class="team"><div>Francisco Ahumada · Claudia Cifuentes</div><div>Néstor Rivera · Benjamín Vera Yáñez</div>
<div class="inst" style="margin-top:1mm">Diseño Digital · INACAP Rancagua</div><div class="inst" style="margin-top:1mm">Profesor: Roberto Escobar Donoso</div></div>
<div style="text-align:right"><div class="inst">Rancagua, Chile</div><div class="inst">Octubre 2026</div></div></div></div>'''

def indice():
    items = [('Marco', [('01', 's-intro', 'Introducción, desafío y enfoque sostenible'), ('02', 's-ruta', 'Ruta metodológica y trazabilidad de criterios')]),
             ('Técnica · Estudio comparativo de referentes', [('2.1.2.1 A', 's-fichas', 'Fichas de referentes'), ('2.1.2.1 B', 's-matriz', 'Matriz de referentes y tendencias')]),
             ('Técnica · Perfil de usuario y requerimientos', [('2.1.3.1', 's-perfil', 'Tabla con perfil de usuario y requerimientos'), ('2.1.3.2', 's-cat', 'Mapa de categorías'), ('2.1.3.3', 's-jer', 'Mapa de jerarquías')]),
             ('Técnica · Brainstorming', [('2.1.4.1', 's-bs', 'Canvas brainstorming'), ('2.1.4.2', 's-clas', 'Mapa de clasificación de ideas y concepto directriz'), ('Selección', 's-fact', 'Evaluación de factibilidad y selección de la idea')]),
             ('Co-creación y conceptualización', [('Usuarias', 's-cocrea', 'Participación de usuarias y co-creación'), ('2.1.4.3', 's-meta', 'Panel de metáforas y atributos'), ('2.1.4.4', 's-pv', 'Panel de propuesta de valor y métricas claves')]),
             ('Cierre', [('Sost.', 's-sost', 'Enfoque sostenible transversal'), ('2.1.5', 's-tiempo', 'Organización del tiempo'), ('Cierre', 's-concl', 'Conclusiones y próximos pasos'), ('Ref.', 's-ref', 'Referencias')])]
    out = ''
    for g, li in items:
        out += f'<div class="grp">{g}</div><ul>' + ''.join(f'<li><span class="c">{c}</span><span class="t"><a href="#{h}">{t}</a></span></li>' for c, h, t in li) + '</ul>'
    out += ('<div class="grp">Anexo</div><ul>'
            f'<li><span class="c">Anexo A</span><span class="t">Toolkit UA2 completo: los 9 instrumentos oficiales con sus matrices llenas</span><span style="font-family:var(--fm);font-size:8pt">{ANEXO_PAGE}</span></li></ul>')
    return section('s-indice', 'ÍNDICE', 'Contenido', 'Índice', f'<div class="toc">{out}</div>')

def intro():
    b = f'''<p class="lead">La Unidad 2 corresponde a la fase de <strong>generación de ideas</strong> del Ciclo de Innovación INACAP. Su aprendizaje esperado
es proponer una idea innovadora y su propuesta de valor a partir del diagnóstico de necesidades de la usuaria y de las variables del contexto
levantadas en la Unidad 1.</p>
<h3>Caso y punto de partida</h3>
<div class="case"><img src="img/02-caso.jpg"><div class="facts">
<div><b>Usuaria</b>Joselyn Toledo — kinesióloga, Centro Médico InMotion. ~1 año con empresa propia.</div>
<div><b>Modelo</b>Clínica (comisión 70/30) + atención particular a domicilio, 10 a 32 h semanales.</div>
<div><b>Insight raíz (UA1)</b>I2 · La agenda es el origen del dato financiero (triangulado 3/3).</div></div></div>
<h4>Desafío redefinido en la Unidad 1</h4><div class="big-q">{DESAFIO}</div>
<p>El desafío se mantiene sin cambios porque la UA1 lo validó con tres fuentes: la usuaria, una experta par (Catalina) y un asesor financiero.
Sobre él se construyen todos los instrumentos de esta unidad.</p>
<h3>Enfoque sostenible del informe</h3>
<p>La rúbrica ES02 pide integrar un enfoque sostenible en cada criterio. En este caso, sostenibilidad significa que la práctica independiente
pueda <strong>mantenerse en el tiempo</strong> sin desgastar a la profesional ni al entorno:</p>
<div class="grid3">
<div class="box"><div class="t">Económica {sus("Ec")}</div>Ingresos estables y predecibles, ganancia real conocida, impuestos provisionados y un colchón para los meses bajos.</div>
<div class="box"><div class="t">Social {sus("So")}</div>Bienestar de la profesional (menos trabajo nocturno), continuidad de la atención a pacientes —incluidos adultos mayores— y protección de datos.</div>
<div class="box"><div class="t">Ambiental {sus("Am")}</div>Menos kilómetros y combustible al agrupar domicilios, horas ociosas aprovechadas y cero registros en papel.</div></div>
<p class="small muted">Alineación con la Agenda 2030: ODS 3 (salud y bienestar), ODS 8 (trabajo decente y crecimiento económico) y ODS 13 (acción por el clima).
Las etiquetas {sus("Ec")}{sus("So")}{sus("Am")} marcan esta lectura en referentes, requerimientos, ideas, atributos y métricas.</p>
'''
    return section('s-intro', '01 · MARCO', '01 · Marco del proyecto', 'Introducción, desafío y enfoque sostenible', b)

def ruta():
    rows = [
        ('S6', '2.1.1.1 Ra-P-Rp', 'Evaluación diagnóstica: activar lo aprendido en Innovación y Emprendimiento II', 'Diagnóstica'),
        ('S6', '2.1.2.1 A/B Referentes', 'Inspirarse en soluciones de otros ámbitos y detectar tendencias', '2.1.2'),
        ('S7', '2.1.3.1 – 2.1.3.3 Requerimientos', 'Perfil de usuaria, requerimientos, categorías y jerarquías', '2.1.3'),
        ('S7', '2.1.4.1 – 2.1.4.2 Brainstorming', 'Generar 60 ideas y clasificarlas por originalidad y factibilidad', '2.1.1 · 2.1.4'),
        ('S7', '2.1.4.3 Metáforas y atributos', 'Conceptualizar la idea seleccionada', '2.1.1 · 2.1.4'),
        ('S8', '2.1.4.4 Propuesta de valor', 'Redactar la propuesta de valor y sus métricas claves', '2.1.4'),
        ('S6–S9', 'Bitácora de avance', 'Planificar y registrar plazos, responsables y aprendizajes', '2.1.5'),
        ('S10', 'Evaluación sumativa grupal', 'Este informe', '2.1.1 – 2.1.5')]
    b = f'''<div class="side" style="margin-bottom:3mm;align-items:center"><img src="img/03-ciclo.jpg" style="width:58mm;height:32.4mm"><div>
<p style="margin:0">El equipo aplicó los instrumentos del toolkit UA2 en el orden del manual del estudiante (semanas 6 a 10). Cada instrumento usa como insumo
el resultado del anterior; la tabla muestra la secuencia y el criterio de la rúbrica ES02 que respalda.</p></div></div>
{table(['Semana', 'Instrumento', 'Objetivo de aplicación', 'Criterio'], rows, 'tight')}
<h3>Hilo conductor de la unidad</h3>
<div class="chain">
<div><b>Insight (UA1)</b>La agenda y las finanzas viven separadas; cada cita es un ingreso que se pierde.</div>
<div><b>Referentes</b>En otros ámbitos, el dato se captura solo y se lee de un vistazo.</div>
<div><b>Requerimientos</b>13 requerimientos en 6 categorías; núcleo: agenda conectada y ganancia real.</div>
<div><b>Ideas</b>60 ideas → 13 originales y factibles → concepto {PRODUCTO}.</div>
<div><b>Concepto</b>“El tablero y el copiloto de un auto de rally”.</div>
<div><b>Valor</b>Saber cuánto gana, anticipar los meses bajos y recuperar su tiempo.</div></div>
<h3>Ponderación de la evaluación (rúbrica ES02)</h3>
{table(['Criterio', 'Qué se evalúa', '%'], [
        ('2.1.1', 'Aplicar la generación de ideas con oportunidades detectadas, Ciclo INACAP y enfoque sostenible', '20'),
        ('2.1.2', 'Analizar casos existentes como inspiración, con enfoque sostenible', '20'),
        ('2.1.3', 'Definir requerimientos coherentes con el problema y la sostenibilidad', '20'),
        ('2.1.4', 'Sintetizar ideas y propuestas de valor con entorno, sostenibilidad y co-creación', '20'),
        ('2.1.5', 'Organizar el tiempo de forma planificada y realista, considerando múltiples dimensiones', '20')], 'tight')}'''
    return section('s-ruta', '02 · MARCO', '02 · Marco del proyecto', 'Ruta metodológica y trazabilidad', b)

def fichas():
    cards = ''
    for i, r in enumerate(REFS):
        ini = ''.join(w[0] for w in r['n'].replace('·', ' ').split()[:2]).upper()
        cards += f'''<div class="ref"><div class="top"><div class="mono">{ini}</div><div><b>{i + 1:02d} · {r["n"]}</b><span>{r["amb"]}</span></div></div>
<div class="bd"><div class="lbl">Descripción</div>{r["d"]}
<div class="lbl">Aspectos relevantes</div>{r["r"]}
<div class="rel"><b>Para el desafío:</b> {r["a"]}</div>
<div class="src">Variables: V1–V5 · Sostenibilidad {sus(*r["s"])} · Fuente: {r["src"]}</div></div></div>'''
    b = f'''{card([('Técnica', 'Estudio comparativo de referentes (Briede-Westermeyer et al., 2018).'), ('Criterio', '2.1.2'),
               ('Selección', '10 casos de <strong>otros ámbitos</strong> (el toolkit sugiere 8–10). Los casos del mismo rubro ya se analizaron como antecedentes en la UA1.')])}
<p>Se buscaron soluciones que resuelven en otro contexto un problema análogo al de la usuaria: capturar un dato sin esfuerzo, mostrar dinero de forma legible,
cobrar sin fricción, sostener un hábito o aprovechar mejor los recursos. Cada ficha registra nombre, ámbito, descripción, aspectos relevantes, aplicación al desafío,
lectura de sostenibilidad y fuente.</p><div class="refs">{cards}</div>
<p class="small muted">Descripciones basadas en la información pública de cada servicio a octubre de 2026. Agregar capturas de pantalla en el campo “Imagen” del tablero de trabajo.</p>'''
    return section('s-fichas', '2.1.2.1 A', 'Técnica · Estudio comparativo de referentes', 'Instrumento 2.1.2.1 (A) — Fichas de referentes', b)

def matriz():
    head = ['Caso'] + [v.split(' ', 1)[0] for v in VARS] + ['Tendencia']
    rows = [[f'<strong>{r["n"]}</strong>'] + [DOT[x] for x in r['v']] + [r['t']] for r in REFS]
    rows.append(['<strong>Oportunidad: ' + PRODUCTO + '</strong>'] + [DOT[2]] * 5 + ['T1–T6'])
    vleg = ''.join(f'<li><strong>{v.split(" ", 1)[0]}</strong> {v.split(" ", 1)[1]}</li>' for v in VARS)
    tend = ''.join(f'<tr><td><strong>{c}</strong></td><td><strong>{t}</strong><br><span class="small muted">{cs}</span></td><td>{ins} {sus(*s)}</td></tr>' for c, t, cs, ins, s in TEND)
    b = f'''<div class="grid2"><div><h4>Variables de análisis</h4><ul class="small">{vleg}</ul></div>
<div><h4>Escala</h4><p class="small">{DOT[2]} Resuelto · {DOT[1]} Parcial · {DOT[0]} No resuelto — evaluación del equipo.</p>
<p class="small">Las variables V1–V4 se derivan de los insights I1, I2, I3 y I6; V5 incorpora el enfoque sostenible exigido por la rúbrica.</p></div></div>
<table class="mat tight"><thead><tr>{''.join(f'<th>{h}</th>' for h in head)}</tr></thead><tbody>{''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)}</tbody></table>
<h3>Tendencias identificadas</h3><table class="tight"><thead><tr><th>N°</th><th>Tendencia y casos</th><th>Lectura para el desafío</th></tr></thead><tbody>{tend}</tbody></table>
<h3>Análisis y conclusiones</h3>
<div class="grid2"><div class="box"><div class="t">Lo que ningún caso resuelve solo</div>Ninguno de los 10 referentes reúne las cinco variables. Los que capturan el dato
(Uber, Mercado Pago, Strava) no lo proyectan; los que proyectan (Fintual, YNAB) no lo capturan. La oportunidad está en <strong>integrar</strong>: captura automática + lectura simple + anticipación.</div>
<div class="box"><div class="t">Elementos novedosos seleccionados</div>Ganancia visible al terminar el servicio (Uber) · dinero con propósito (YNAB) · proyección en lenguaje cotidiano (Fintual) ·
cobro que crea el dato (Mercado Pago) · recurrencia (Smart Fit) · hábito de segundos (Duolingo) · rutas eficientes (Google Maps) · capacidad ociosa (Too Good To Go) · propuesta precalculada (SII).</div></div>
<div class="verdict"><strong>Conclusión para la ideación.</strong> La tendencia dominante (T1) es que el dato se genere como consecuencia de la operación. Para Joselyn, la solución no debe pedirle
“ordenar mejor su Excel”, sino eliminar la digitación. T2 y T5 aportan la dimensión sostenible: estabilidad económica y menos recursos consumidos por atención.</div>
<p class="small muted">Relación con la UA1: los antecedentes del rubro (AgendaPro, Encuadrado, Cal.com, Nubox, entre otros) resolvían la agenda o la contabilidad por separado. Los referentes muestran <em>cómo</em> unirlas.</p>'''
    return section('s-matriz', '2.1.2.1 B', 'Técnica · Estudio comparativo de referentes', 'Instrumento 2.1.2.1 (B) — Matriz de referentes', b)

def perfil():
    emp = ''.join(f'<div class="box"><div class="t">{q}</div>{a}</div>' for q, a in EMPATIA)
    emp_rows = '<div class="grid3 emp">' + ''.join(f'<div class="box"><div class="t">{q}</div>{a}</div>' for q, a in EMPATIA[:3]) + '</div><div class="grid3 emp">' + ''.join(f'<div class="box"><div class="t">{q}</div>{a}</div>' for q, a in EMPATIA[3:]) + '</div>'
    req_rows = []
    for code, name, reqs in REQS:
        for k, (rc, txt, tipo, s) in enumerate(reqs):
            req_rows.append((f'<strong>{code}</strong> {name}' if k == 0 else '', f'<strong>{rc}</strong> {txt}', tipo, sus(*s)))
    b = f'''{card([('Técnica', 'Perfil de usuario y estudio de requerimientos.'), ('Criterio', '2.1.3'), ('Insumos', 'Entrevista a Joselyn, observación AEIOU, entrevistas a expertos y matriz de categorización de insights (UA1).')])}
<div class="box"><div class="t">Desafío</div>{DESAFIO}</div>
<h3>Perfil de usuaria — Joselyn Toledo</h3>
<div class="side" style="margin-bottom:3mm"><img src="img/07-oficina-movil.jpg" style="width:30mm;height:30mm"><div><p style="margin:0">Joselyn atiende en dos contextos —el box de InMotion y los hogares de sus pacientes— y su oficina es el celular:
WhatsApp para agendar, el calendario para los horarios y un Excel que se llena al final del día. El mapa de empatía ordena lo que piensa, ve, oye, dice, le duele y desea.</p></div></div>
{emp_rows}
<h3>Insights y requerimientos</h3>
<p>Cada insight priorizado en la UA1 se traduce en lo que la solución <strong>debe cumplir</strong>. Se clasifica el tipo de requerimiento y su aporte a la sostenibilidad.</p>
{table(['Insight (UA1)', 'Requerimiento de la solución', 'Tipo', 'Sost.'], req_rows, 'tight')}
<div class="box"><div class="t">Solución — dirección preliminar</div>Una herramienta que se conecte a la agenda existente, registre cada atención en el momento,
descuente costos e impuestos y proyecte los próximos meses, con una lectura simple desde el celular.</div>
<p class="small muted">I7 (fidelización informal) e I8 (crecimiento sin plan) quedan fuera del foco: dependen de resolver primero I1, I2 e I6 (ver mapa de priorización UA1).
La retención vigente de la boleta de honorarios sube gradualmente hasta 17 % en 2028 (Ley 21.133).</p>'''
    return section('s-perfil', '2.1.3.1', 'Técnica · Perfil de usuario y estudio de requerimientos', 'Instrumento 2.1.3.1 — Tabla con perfil de usuario y requerimientos', b)

def categorias():
    rows = [(f'<strong>{c}</strong> {n}', '<br>'.join('· ' + x for x in nec), ' · '.join(r)) for c, n, nec, r in CATS]
    b = f'''{card([('Técnica', 'Categorización y jerarquización.'), ('Criterio', '2.1.3'), ('Cómo se construyó', 'Los 13 requerimientos se agruparon por saturación; cada categoría se cruza con las necesidades de la usuaria detectadas en la UA1.')])}
{table(['Categoría', 'Necesidades de la usuaria (UA1)', 'Requerimientos'], rows)}
<div class="verdict"><strong>Lectura.</strong> Las seis categorías cubren las tres dimensiones de la sostenibilidad: C2 y C5 la económica, C3 y C6 la social,
y C4 la ambiental. C1 es transversal: sin agenda conectada, ninguna de las otras recibe datos.</div>'''
    return section('s-cat', '2.1.3.2', 'Técnica · Categorización y jerarquización', 'Instrumento 2.1.3.2 — Mapa de categorías', b)

def jerarquias():
    b = f'''{card([('Eje 1 (horizontal)', 'Impacto en la sostenibilidad de la práctica: cuánto cambia su estabilidad económica, su bienestar y su consumo de recursos.'),
               ('Eje 2 (vertical)', 'Frecuencia del dolor: de un problema anual (impuestos) a uno diario (registro).'), ('Criterio', '2.1.3')])}
<div class="legend"><span><span class="sw" style="background:#D9D2FF"></span>Necesidad / categoría</span><span><span class="sw" style="background:#FFD6C2"></span>Requerimiento</span></div>
{jerarquias_svg()}
<h3>Jerarquía resultante</h3>{table(['Prioridad', 'Categorías', 'Justificación'], PRIO, 'tight')}
<p class="small muted">Ubicación consensuada a partir de la frecuencia declarada por la usuaria y del impacto descrito por los expertos en la UA1.</p>'''
    return section('s-jer', '2.1.3.3', 'Técnica · Categorización y jerarquización', 'Instrumento 2.1.3.3 — Mapa de jerarquías', b)

def postit(i, compact=False):
    voz = f' · voz: {i["v"]}' if i['v'] else ''
    of = '' if compact else f'<span class="of">O{i["o"]} · F{i["f"]}{voz}</span>'
    return f'<div class="pi c{i["c"]}{" voz" if i["v"] else ""}"><span class="id">{i["id"]} {sus(*i["s"]) if i["s"] else ""}</span>{i["t"]}{of}</div>'

def brainstorming():
    leg = ''.join(f'<span><i style="background:{CATC[k]}"></i>{k} · {v}</span>' for k, v in CATN.items())
    groups = ''
    for k in CATN:
        ids = [i for i in IDEAS if i['c'] == k]
        groups += f'<h4>{k} · {CATN[k]} ({len(ids)})</h4><div class="pis">' + ''.join(postit(i) for i in ids) + '</div>'
    nvoz = sum(1 for i in IDEAS if i['v'])
    nsus = sum(1 for i in IDEAS if i['s'])
    b = f'''{card([('Técnica', 'Brainstorming (Llorenc, 2011; Pomar, 2020).'), ('Criterios', '2.1.1 · 2.1.4'),
               ('Reglas', 'No juzgar · cantidad antes que calidad · una idea por post-it · desafío siempre a la vista.')])}
<div class="side" style="margin-bottom:3mm"><img src="img/04-card-sorting.jpg" style="width:64mm;height:35.7mm"><div class="box" style="margin:0"><div class="t">Desafío al centro del canvas</div>{DESAFIO}</div></div>
<h4>Dinámica</h4><ul class="small">
<li><strong>10 min</strong> · moderador y ajuste del desafío con los requerimientos jerarquizados.</li>
<li><strong>35 min</strong> · generación libre, partiendo de las tendencias T1–T6 como detonantes.</li>
<li><strong>5 min</strong> · plenario y limpieza de ideas repetidas.</li></ul>
<div class="kpi2"><div><span class="v">{len(IDEAS)}</span><span class="l">ideas generadas</span></div>
<div><span class="v">{nsus}</span><span class="l">con aporte sostenible</span></div>
<div><span class="v">{nvoz}</span><span class="l">nacen de la voz de usuarias o expertos</span></div></div>
<div class="catlg">{leg}</div>
<p class="small">Cada post-it indica su número, sus etiquetas de sostenibilidad, la puntuación de originalidad (O) y factibilidad (F) de 1 a 5, y si nace de una cita de la usuaria
o de un experto (borde punteado). Las ideas exploratorias (H) se registran aunque parezcan imposibles: así lo pide la técnica.</p>
{groups}'''
    return section('s-bs', '2.1.4.1', 'Técnica · Brainstorming', 'Instrumento 2.1.4.1 — Canvas brainstorming', b)

def clasificacion():
    def chips(q):
        out = ''
        for i in IDEAS:
            if quad(i) == q:
                t = i['t'] if len(i['t']) <= 22 else i['t'][:21].rstrip() + '…'
                out += f'<span class="ch" style="background:{CATC[i["c"]]}"><b>{i["id"]}</b>{t}</span>'
        return out
    cnt = {q: sum(1 for i in IDEAS if quad(i) == q) for q in ['+O+F', '-O+F', '+O-F', '-O-F']}
    b = f'''{card([('Ejes', '<strong>Originalidad:</strong> distinta a lo que hoy usa la usuaria y su competencia (Excel, Cal.com, AgendaPro).<br><strong>Factibilidad:</strong> posible con herramientas existentes, bajo costo y prototipable en la UA3.'),
               ('Regla', 'Puntaje ≥ 4 de 5 en cada eje. Las ideas se revisaron una a una.'), ('Criterios', '2.1.1 · 2.1.4')])}
<table class="qt"><tr><td class="ax" colspan="2">(+) FACTIBLE ↑</td></tr>
<tr><td><div class="h">(−) Original · (+) Factible — base operativa ({cnt["-O+F"]})</div>{chips("-O+F")}</td>
<td class="hot"><div class="h">★ (+) Original · (+) Factible — foco ({cnt["+O+F"]})</div>{chips("+O+F")}</td></tr>
<tr><td class="cold"><div class="h">(−) Original · (−) Factible — descartadas ({cnt["-O-F"]})</div>{chips("-O-F")}</td>
<td><div class="h">(+) Original · (−) Factible — banco de ideas futuras ({cnt["+O-F"]})</div>{chips("+O-F")}</td></tr>
<tr><td class="ax">(−) FACTIBLE · (−) ORIGINAL</td><td class="ax">(+) ORIGINAL →</td></tr></table>'''
    boxes = [f'<div class="box"><div class="t">{n}</div>' + ''.join(postit(BYID[x], True).replace('class="pi', 'style="width:100%;margin-bottom:1.2mm" class="pi') for x in ids) + f'<p class="small" style="margin:1mm 0 0"><strong>Síntesis:</strong> {s}</p></div>' for n, c, ids, s in GRUPOS]
    b += f'''<h3>Categorías de las ideas con más potencial</h3><div class="grid2"><div>{boxes[0]}{boxes[2]}</div><div>{boxes[1]}{boxes[3]}</div></div>
<p class="small">Habilitan el concepto tres ideas de la base operativa: <strong>01</strong> conector con la agenda, <strong>02</strong> botón “atención realizada” y <strong>47</strong> cierre del día en 3 preguntas.</p>
<div class="met"><div class="k">Concepto directriz</div><div class="m">{PRODUCTO}</div>
<p>Un copiloto financiero que se conecta a la agenda que la kinesióloga ya usa, convierte cada atención en <strong style="color:#fff">ganancia real</strong>
—descontando comisión, traslado, materiales e impuestos—, proyecta los meses que vienen y le devuelve su tiempo con rutas más cortas y sin cierres nocturnos.</p></div>'''
    return section('s-clas', '2.1.4.2', 'Técnica · Brainstorming', 'Instrumento 2.1.4.2 — Mapa de clasificación de ideas', b)

def factibilidad():
    crit = ['Responde al desafío (registro &lt; 30 min)', 'Recursos internos del equipo', 'Recursos externos disponibles', 'Prototipable y testeable en la UA3', 'Aporte sostenible (Ec · So · Am)', 'Diferenciación frente a antecedentes']
    A = [5, 4, 4, 4, 5, 5]; Bv = [2, 5, 5, 5, 3, 1]; Cv = [4, 2, 2, 2, 3, 2]
    rows = [[c, str(a), str(b), str(cc)] for c, a, b, cc in zip(crit, A, Bv, Cv)]
    rows.append(['<strong>Total (máx. 30)</strong>', f'<strong>{sum(A)}</strong>', str(sum(Bv)), str(sum(Cv))])
    tbl = table(['Criterio (1–5)', f'A · {PRODUCTO}', 'B · Planilla inteligente', 'C · Agenda propia nueva'], rows, 'score tight')
    tbl = tbl.replace('<td>27</td>', '<td class="win">27</td>')
    b = f'''<p>Antes de conceptualizar, el equipo comparó tres caminos posibles para responder al desafío con los recursos que realmente tiene.</p>
<div class="grid3">
<div class="box"><div class="t">A · {PRODUCTO}</div>Se conecta a la agenda existente; tablero de ganancia real, costos de domicilio, proyección y provisión de impuestos.</div>
<div class="box"><div class="t">B · Planilla inteligente</div>Plantilla de Google Sheets con fórmulas. Barata y rápida, pero mantiene la digitación diaria.</div>
<div class="box"><div class="t">C · Agenda propia nueva</div>Agenda con módulo financiero. Compite con Cal.com y AgendaPro y obliga a la usuaria a cambiar de herramienta.</div></div>
{tbl}
<h3>Recursos para prototipar y testear</h3>
{table(['Tipo', 'Recurso', 'Disponibilidad'], [
        ('Interno', 'Diseño UX/UI y prototipado en Figma; diseño web en WordPress; uso de IA para contenidos', 'Competencias del equipo (Diseño Digital)'),
        ('Interno', '4 integrantes, ~2 h semanales de trabajo autónomo cada uno + horas de clase', 'Ver organización del tiempo (2.1.5)'),
        ('Externo', 'Google Calendar y Google Sheets como base de datos del prototipo', 'Gratuito'),
        ('Externo', 'Usuarias para testear: Joselyn (caso) y Catalina (experta par)', 'Contactadas en la UA1'),
        ('Externo', 'Validación tributaria con el asesor financiero entrevistado por Francisco', 'Contactado en la UA1')], 'tight')}
<div class="verdict"><strong>Idea seleccionada: A · {PRODUCTO}</strong>, con un alcance mínimo para la UA3: conexión con la agenda, cierre de un toque, ganancia neta por atención
con costos de domicilio, tablero con semáforo y proyección simple a 3 meses. La provisión de impuestos, las rutas y los cupos de último minuto quedan para una segunda iteración.</div>'''
    return section('s-fact', 'SELECCIÓN', 'Técnica · Brainstorming', 'Evaluación de factibilidad y selección de la idea', b)

def cocreacion():
    aportes = [
        ('Joselyn · usuaria', '“Siento que igual tengo como un cierto desorden o falta de educación.”', 'R5 lenguaje no contable; atributo “Legible de un vistazo”.'),
        ('Joselyn · usuaria', '“Yo los trato como a mí me gustase que me tratasen.”', 'Atributo “Sostenible”: la tecnología libera tiempo para el trato 1:1.'),
        ('Joselyn · usuaria', 'Visión de crecimiento: comisionistas, grupos de adultos mayores, presoterapia.', 'Ideas 32, 42, 56 y 58.'),
        ('Catalina · experta par', '“Para organizar el Excel… me toma una hora actualmente diario.”', 'Meta del desafío y métrica de eficiencia (&lt; 30 min).'),
        ('Catalina · experta par', '“Sí pagaría por una herramienta así que juntara eso… 30 a 40 mil pesos.”', 'Concepto integrado (idea 01) y rango de precio.'),
        ('Catalina · experta par', 'Usa Cal.com gratuito con Google Calendar.', 'R2: integrarse con la agenda existente, no reemplazarla.'),
        ('Asesor financiero', '“Estar ocupado y estar ganando dinero no son lo mismo.”', 'Idea 10: ganancia neta por atención.'),
        ('Asesor financiero', 'La Operación Renta llega como sorpresa; no hay colchón para meses bajos.', 'Ideas 26, 29, 33 y 34.')]
    proto = [('5 min', 'Contexto', 'Mostrar el desafío y preguntar si lo representa.', 'Desafío impreso'),
             ('15 min', 'Votación de ideas', '3 votos por usuaria sobre las ideas del cuadrante foco; espacio para agregar ideas propias.', 'Mapa de clasificación'),
             ('10 min', 'Metáfora y atributos', '¿El “tablero y copiloto” describe lo que necesitas? Ordenar los 4 atributos por importancia.', 'Panel 2.1.4.3'),
             ('10 min', 'Test de 5 segundos', 'Leer la propuesta de valor 5 segundos y explicarla con sus palabras.', 'Panel 2.1.4.4'),
             ('5 min', 'Métricas', 'Elegir la métrica que demostraría que la herramienta le sirve.', 'Lista de métricas')]
    res = [('Ideas más votadas', PEND), ('Ideas nuevas aportadas por las usuarias', PEND), ('¿La metáfora hace sentido?', PEND),
           ('Orden de los atributos', PEND), ('Explicación de la propuesta de valor con sus palabras', PEND), ('Ajustes realizados', PEND)]
    b = f'''{card([('Criterio', '2.1.4 — participación de usuarios como parte del proceso de co-creación.'), ('Participantes', 'Joselyn Toledo (usuaria) · Catalina (experta par y usuaria del segmento).'),
               ('Momentos', '1) Su voz como insumo directo de la ideación. 2) Sesión de validación del concepto.')])}
<div class="side"><img src="img/05-entrevista.jpg" style="width:46mm;height:61.6mm"><div>
<h3 style="margin-top:0">1 · La voz de las usuarias en la ideación</h3>
<p>La co-creación no empieza en una sesión: empieza escuchando. Doce de las sesenta ideas nacen directamente de lo que dijeron la usuaria y los expertos
en la UA1 y se marcan con borde punteado en el canvas.</p>
<p>La segunda instancia es una sesión de 45 minutos en la que Joselyn y Catalina votan ideas, validan la metáfora y ponen a prueba la propuesta de valor.</p></div></div>
<p>Trazabilidad de los aportes:</p>
{table(['Fuente', 'Aporte textual o declarado', 'Cómo se incorporó'], aportes, 'tight')}
<h3>2 · Sesión de co-creación y validación (45 min)</h3>
{table(['Tiempo', 'Momento', 'Actividad', 'Material'], proto, 'tight')}
<p class="small">Modalidad: presencial con Joselyn; remota con Catalina (videollamada o notas de voz por WhatsApp, como en la UA1). Moderación: Claudia Cifuentes; registro: Néstor Rivera.</p>
<h4>Resultados de la sesión</h4>{table(['Resultado', 'Registro'], res, 'tight')}
<div class="note"><strong>Pendiente del equipo:</strong> registrar aquí los resultados reales de la sesión y ajustar la metáfora, los atributos o la propuesta de valor si las usuarias lo piden.
Reglas de ajuste acordadas: si la metáfora no hace sentido, se prueba la alternativa “GPS que recalcula”; si la propuesta de valor no se entiende en 5 segundos, se reescribe con las palabras de las usuarias.</div>'''
    return section('s-cocrea', 'CO-CREACIÓN', 'Co-creación con usuarias', 'Participación de usuarias y co-creación', b)

ATR = [('Anticipador', 'en el sentido de que avisa antes de la curva: proyecta los ingresos de los próximos meses y alerta la temporada baja con tiempo para actuar.', 'Ingresos estacionales sin proyección (I6).', 'R10 · R11', ['Ec']),
       ('Legible de un vistazo', 'en el sentido de un tablero: semáforo, números grandes y palabras cotidianas, sin jerga contable.', '“Desorden o falta de educación” económica (I1).', 'R4 · R5', ['So']),
       ('Automático', 'en el sentido de que la cita, el cobro y el traslado se registran solos; la usuaria solo confirma.', 'Excel diario al cierre de la jornada (I2 · I3).', 'R1 · R6 · R7 · R8', ['So', 'Ec']),
       ('Sostenible', 'en el sentido de que rinde más con menos: menos km, menos horas nocturnas y un colchón para los meses bajos; el tiempo vuelve al trato 1:1.', 'Costos invisibles, desgaste e impuestos (I4 · I5).', 'R9 · R12 · R13', ['Ec', 'So', 'Am'])]

def metaforas():
    atr = ATR
    b = f'''{card([('Técnica', 'Generación de metáfora y atributos.'), ('Criterios', '2.1.1 · 2.1.4'), ('Rol del instrumento', 'Mantener la coherencia del prototipado, el testeo y la propuesta de valor en la UA3.')])}
<div class="met"><div class="k">Metáfora seleccionada</div><div class="m">“{PRODUCTO} es como el tablero y el copiloto de un auto de rally.”</div>
<p>Joselyn maneja: atiende a sus pacientes. El tablero le muestra la velocidad y el combustible (ganancia del mes y colchón), y el copiloto le lee la ruta que viene:
las curvas (meses bajos), los tramos (la agenda del día) y cuándo acelerar. Ella nunca suelta el volante.</p></div>
<div class="grid2"><div><h4>¿Por qué esta metáfora?</h4><p class="small">Nace de su rutina real: recorre Rancagua en su auto entre domicilios. Un tablero no exige saber mecánica para usarlo,
igual que la solución no debe exigir saber de finanzas. Además, la imagen del copiloto protege su rol: la herramienta acompaña, no decide por ella.</p>
<h4>Metáforas descartadas</h4><ul class="small"><li>Como un GPS que recalcula la ruta cuando algo cambia (cancelaciones).</li><li>Como una alcancía con compartimentos: cada peso tiene un destino.</li></ul></div>
<div><h4>Collage</h4>{collage_svg()}</div></div>
<div class="collage"><img src="img/02-caso.jpg" style="width:62.7mm;height:35mm"><img src="img/14-dashboard.jpg" style="width:26.1mm;height:35mm"><img src="img/06-nudo.jpg" style="width:35mm;height:35mm"><img src="img/07-oficina-movil.jpg" style="width:35mm;height:35mm"></div>
<p class="small muted">Collage: doble contexto de atención (clínica y domicilio), el celular como oficina móvil, el desorden que se ordena y una referencia visual de tablero. Imágenes generadas con IA por el equipo en la UA1; ilustración del tablero, elaboración propia.</p>
'''
    cards = [f'<div class="attr" style="margin-bottom:3mm"><div class="n">{n} {sus(*s)}</div><div class="s">“{d}”</div><div class="r"><b>Necesidad</b>{nec}</div><div class="r"><b>Requerimientos</b>{r}</div></div>' for n, d, nec, r, s in atr]
    b += f'<h3>Atributos</h3><div class="grid2"><div>{cards[0]}{cards[2]}</div><div>{cards[1]}{cards[3]}</div></div>'
    return section('s-meta', '2.1.4.3', 'Técnica · Generación de metáfora y atributos', 'Instrumento 2.1.4.3 — Panel de metáforas y atributos', b)

def propuesta():
    lean = f'''<table class="lean"><colgroup><col><col><col><col><col></colgroup>
<tr><td rowspan="2"><div class="t">Problema</div><ol><li>No sabe cuánto gana realmente (I1).</li><li>Agenda y finanzas desconectadas; registro manual de ~1 h diaria (I2 · I3).</li><li>Meses bajos e impuestos que llegan por sorpresa (I4 · I6).</li></ol>
<div class="t" style="margin-top:2mm">Alternativas hoy</div>Excel, Cal.com, AgendaPro, contadora externa.</td>
<td><div class="t">Solución</div><ol><li>Conexión con la agenda y cierre de un toque.</li><li>Ganancia neta por atención con comisión y costos del domicilio.</li><li>Proyección a 3–6 meses y provisión de la retención.</li></ol></td>
<td rowspan="2" class="pv"><div class="t">Propuesta de valor</div><strong>El copiloto financiero de la kinesióloga independiente:</strong> convierte cada atención en ganancia real y le avisa qué viene, sin que tenga que digitar.
<div class="t" style="margin-top:2mm">Concepto de alto nivel</div>“Un tablero de auto para tu práctica”.</td>
<td><div class="t">Ventaja especial</div>Único que cruza agenda + costos por atención + retención chilena (vacío de la matriz de antecedentes UA1). Co-creado con kinesiólogas reales.</td>
<td rowspan="2"><div class="t">Segmento de clientes</div>Kinesiólogas y kinesiólogos independientes con atención mixta (clínica + domicilio) en Rancagua y O’Higgins.
<div class="t" style="margin-top:2mm">Early adopters</div>Profesionales con 0 a 2 años de práctica particular, como Joselyn y Catalina.</td></tr>
<tr><td><div class="t">Métricas clave</div>Minutos diarios de registro · % de citas registradas solas · diferencia entre proyección y realidad · horas y km recuperados.</td>
<td><div class="t">Canales</div>Recomendación entre pares, Instagram y contenido educativo, clínicas como InMotion, comunidad gremial de kinesiología.</td></tr>
<tr><td colspan="2"><div class="t">Estructura de costes</div>Diseño y desarrollo low-code; servicios en la nube y APIs (Google Calendar sin costo); soporte; adquisición por contenido digital.</td>
<td colspan="3"><div class="t">Flujo de ingresos</div>Suscripción mensual de referencia: $20.000–$25.000 CLP, bajo la disposición a pagar declarada ($30.000–$40.000) y dentro del rango del mercado ($8.000–$25.000) (UA1). Plan básico gratuito con el tablero mensual.</td></tr></table>'''
    met = [('Eficiencia', 'Minutos diarios dedicados al registro', '~60 min (Catalina, UA1) · Joselyn: medir', '&lt; 30 min', 'Autorreporte semanal + registro de uso', ['So']),
           ('Eficiencia', '% de atenciones registradas sin digitar', '0 % (todo manual)', '≥ 80 %', 'Atenciones confirmadas / atenciones de la agenda', ['So']),
           ('Eficacia', 'Diferencia entre ganancia proyectada y real del mes', 'Sin proyección', '≤ 10 %', 'Comparación mensual', ['Ec']),
           ('Eficacia', 'Meses con la retención provisionada', '0', '100 %', 'Provisión acumulada vs. retención', ['Ec']),
           ('Efectividad', 'La usuaria sabe cuánto ganó el mes (1–5)', 'Por medir en el test', '≥ 4', 'Pregunta de cierre mensual', ['Ec', 'So']),
           ('Efectividad', 'Colchón para meses bajos', 'Sin colchón', '≥ 1 mes de costos fijos', 'Saldo del fondo', ['Ec']),
           ('Sostenibilidad', 'Km mensuales en domicilios', 'Por medir (registro de 2 semanas)', '−10 % al agrupar por sector', 'Km por ruta registrada', ['Am'])]
    b = f'''{card([('Técnica', 'Diseño de propuesta de valor y métricas claves (Carlson y Wilmot, 2006; Maurya, 2012).'), ('Criterio', '2.1.4'), ('Semana', '8 · actividad online')])}
<div class="grid2"><div class="box"><div class="t">Situación actual</div>Atiende de día y cuadra Excel de noche; no sabe si un mes fue bueno hasta que termina; los costos del domicilio y los impuestos no aparecen en sus números.</div>
<div class="box"><div class="t">Situación futura deseada</div>Cierra cada atención con un toque, ve su ganancia real en el celular, sabe con meses de anticipación qué viene y tiene apartado lo de los impuestos.</div></div>
<h4>Fórmula de la propuesta de valor</h4>
<div class="formula"><div><b>¿Qué es?</b>Un copiloto financiero digital.</div><div><b>¿Cómo es?</b>Conectado a su agenda, automático, legible de un vistazo y anticipador.</div>
<div><b>¿Por qué?</b>Porque convierte cada cita en ingreso y descuenta comisión, traslado, materiales y retención.</div><div><b>¿Para qué?</b>Para que sepa cuánto gana, anticipe los meses bajos y recupere su tiempo.</div></div>
<div class="pvq">{PRODUCTO} es el copiloto financiero de la kinesióloga independiente: se conecta a la agenda que ya usa y convierte cada atención en ganancia real
—descontando traslado, materiales, comisión e impuestos— para que sepa cuánto gana, anticipe los meses bajos y deje de cuadrar Excel de noche.</div>
<div class="grid2"><div class="box"><div class="t">Necesidades</div>C1 Agenda conectada · C2 Ganancia real · C3 Tiempo y bienestar · C4 Costos y rutas · C5 Anticipación · C6 Cumplimiento y confianza.</div>
<div class="box"><div class="t">Atributos</div>Anticipador · Legible de un vistazo · Automático · Sostenible.</div></div>
<h3>Panel de propuesta de valor</h3>{lean}
<h3>Métricas claves</h3>{table(['Dimensión', 'Métrica', 'Línea base', 'Meta', 'Cómo se mide', 'Sost.'], [(a, b, c, d, e, sus(*s)) for a, b, c, d, e, s in met], 'tight')}
<p class="small muted">Las líneas base “por medir” se levantan en las dos primeras semanas del testeo de la UA3. El precio es una referencia a validar en la UA4 (factibilidad económica).</p>'''
    return section('s-pv', '2.1.4.4', 'Técnica · Diseño de propuesta de valor y métricas claves', 'Instrumento 2.1.4.4 — Panel de propuesta de valor', b)

def sostenibilidad():
    rows = [('Referentes (2.1.2)', 'V5 Sostenibilidad como variable; tendencias T2 y T5', 'Too Good To Go y Google Maps inspiran ideas de eficiencia', sus('Ec', 'Am')),
            ('Requerimientos (2.1.3)', 'Cada requerimiento etiquetado; R9 y R13 nacen de la mirada sostenible', 'C3, C4 y C6 cubren lo social y lo ambiental', sus('Ec', 'So', 'Am')),
            ('Ideas (2.1.4.1–2)', f'{sum(1 for i in IDEAS if i["s"])} de {len(IDEAS)} ideas con aporte sostenible', 'Ideas 22, 29, 30 y 48 dentro del foco', sus('Ec', 'So', 'Am')),
            ('Concepto (2.1.4.3)', 'Atributo 4: “Sostenible”', 'Protege el bienestar y el trato 1:1', sus('So')),
            ('Propuesta de valor (2.1.4.4)', 'Métricas de horas, colchón y km', 'Impacto medible en las tres dimensiones', sus('Ec', 'So', 'Am'))]
    risks = [('Sobrecarga de notificaciones', 'Resumen semanal y un solo aviso diario configurable'), ('Dependencia de una plataforma externa', 'Exportación de datos en todo momento'),
             ('Datos sensibles de salud', 'Solo datos financieros y de agenda; nunca la ficha clínica (Ley 21.719)'), ('Brecha digital de la usuaria', 'Onboarding de 10 min importando su Excel')]
    b = f'''<p>El enfoque sostenible no se agregó al final: se aplicó como variable, requerimiento, filtro, atributo y métrica a lo largo de toda la unidad.</p>
{table(['Etapa', 'Cómo se integró', 'Resultado', 'Dimensión'], rows, 'tight')}
<div class="grid3"><div class="box"><div class="t">ODS 3 · Salud y bienestar</div>Más tiempo y continuidad de atención para pacientes; menos desgaste de la profesional.</div>
<div class="box"><div class="t">ODS 8 · Trabajo decente</div>Práctica independiente estable, con ingresos conocidos e impuestos al día.</div>
<div class="box"><div class="t">ODS 13 · Acción por el clima</div>Menos kilómetros y combustible al agrupar domicilios; cero papel.</div></div>
<h3>Riesgos para la sostenibilidad de la propia solución</h3>{table(['Riesgo', 'Cómo se aborda en el diseño'], risks, 'tight')}'''
    return section('s-sost', 'SOSTENIBILIDAD', 'Enfoque sostenible', 'Enfoque sostenible transversal', b)

def tiempo():
    W = ['S6', 'S7', 'S8', 'S9', 'S10']
    G = [('Ra-P-Rp diagnóstica (en clase)', {'S6': 'on'}), ('Fichas y matriz de referentes', {'S6': 'on', 'S7': 'mid'}),
         ('Perfil, requerimientos, categorías y jerarquías', {'S7': 'on'}), ('Brainstorming y mapa de clasificación', {'S7': 'on'}),
         ('Metáforas y atributos', {'S7': 'mid', 'S8': 'on'}), ('Propuesta de valor y métricas claves', {'S8': 'on'}),
         ('Sesión de co-creación con usuarias', {'S8': 'mid', 'S9': 'on'}), ('Bitácora de avance (registro semanal)', {'S6': 'mid', 'S7': 'mid', 'S8': 'mid', 'S9': 'hito'}),
         ('Consolidación del informe y revisión cruzada', {'S9': 'on', 'S10': 'mid'}), ('Entrega sumativa grupal', {'S10': 'hito'})]
    lbl = {'on': '', 'mid': '', 'hito': '◆'}
    rows = ''.join('<tr><td>' + t + '</td>' + ''.join(f'<td class="{m.get(w, "")}">{lbl.get(m.get(w, ""), "")}</td>' for w in W) + '</tr>' for t, m in G)
    roles = [('Benjamín Vera Yáñez', 'Secretario técnico: consolida instrumentos, tablero Figma, informe y bitácora', 'Referentes de datos y visualización · metáfora'),
             ('Francisco Ahumada', 'Referentes financieros y vínculo con el asesor financiero', 'Factibilidad · costos e ingresos de la propuesta'),
             ('Claudia Cifuentes', 'Perfil de usuaria y requerimientos', 'Moderación de la sesión de co-creación'),
             ('Néstor Rivera', 'Moderación del brainstorming y mapa de clasificación', 'Registro de la co-creación · métricas claves')]
    dims = [('Académica', 'FGIE03 comparte semanas con evaluaciones de otras asignaturas de Diseño Digital (talleres y seminario).', 'Adelantar la consolidación a S9; cada instrumento cerrado la misma semana en que se aplica.'),
            ('Profesional', 'Integrantes con trabajo o proyectos de diseño en paralelo (por ejemplo, la agencia de diseño de Benjamín).', 'Trabajo asincrónico en el tablero Figma y entregas parciales por instrumento.'),
            ('Personal', 'Tiempos de traslado, familia y descanso; disponibilidad variable de la usuaria.', 'Reuniones sincrónicas de máximo 60 min; fines de semana sin reuniones; holgura de 1 semana.')]
    risks = [('La usuaria no puede asistir a la co-creación', 'Sesión remota o por notas de voz, como se hizo con Catalina en la UA1'),
             ('Límite de uso de herramientas (plan gratuito de Figma)', 'Plantillas exportables (SVG/PNG) y respaldo en el repositorio'),
             ('Coincidencia con otras evaluaciones', 'Hitos internos una semana antes de cada entrega'),
             ('Integrante con baja disponibilidad una semana', 'Roles con respaldo cruzado: cada instrumento tiene responsable y apoyo')]
    b = f'''{card([('Criterio', '2.1.5 — organizar el tiempo de manera planificada y realista.'), ('Carga de la unidad', '20 h según el manual: 15 presenciales + 5 online, más ~2 h semanales de trabajo autónomo por integrante.'),
               ('Herramientas', 'Bitácora de avance (semanal), tablero Figma compartido, Microsoft Teams y repositorio del proyecto.')])}
<h3>Carta Gantt de la unidad</h3>
<table class="gantt tight"><thead><tr><th>Actividad</th>{''.join(f'<th>{w}</th>' for w in W)}</tr></thead><tbody>{rows}</tbody></table>
<p class="small muted"><span class="sq" style="background:var(--accent)"></span>trabajo principal · <span class="sq" style="background:rgba(255,107,53,.35)"></span>apoyo o continuidad · <span class="sq" style="background:#12101E"></span>hito de entrega</p>
<h3>Responsables</h3>{table(['Integrante', 'Responsabilidad principal', 'Apoyo'], roles, 'tight')}
<h3>Dimensiones consideradas</h3>{table(['Dimensión', 'Demanda', 'Estrategia del equipo'], dims, 'tight')}
<h3>Riesgos y holguras</h3>{table(['Riesgo', 'Mitigación'], risks, 'tight')}
<p class="small">La bitácora de avance registra, para cada indicador, el instrumento usado, su objetivo, el plazo, los responsables, si se logró el objetivo y lo aprendido para la siguiente unidad.</p>'''
    return section('s-tiempo', '2.1.5', 'Organización del tiempo', 'Organización del tiempo de acuerdo a la meta', b, )

def conclusiones():
    traz = [('2.1.1', 'Brainstorming de 60 ideas desde las oportunidades de la UA1; clasificación, concepto y metáfora con enfoque sostenible.', 'Secciones 2.1.4.1 · 2.1.4.2 · 2.1.4.3'),
            ('2.1.2', '10 referentes de otros ámbitos, matriz con variable de sostenibilidad y 6 tendencias.', 'Secciones 2.1.2.1 A · B'),
            ('2.1.3', 'Perfil de usuaria, 13 requerimientos etiquetados, 6 categorías y mapa de jerarquías.', 'Secciones 2.1.3.1 · 2.1.3.2 · 2.1.3.3'),
            ('2.1.4', 'Selección por factibilidad, voz de usuarias en la ideación, sesión de co-creación y propuesta de valor con métricas.', 'Secciones de co-creación · 2.1.4.4'),
            ('2.1.5', 'Carta Gantt, responsables, dimensiones académica, profesional y personal, riesgos y bitácora.', 'Sección 2.1.5')]
    b = f'''<h3>Conclusiones</h3>
<p>La Unidad 2 transformó un hallazgo —la agenda y las finanzas viven separadas— en una propuesta concreta: <strong>{PRODUCTO}</strong>. Los referentes de otros ámbitos mostraron que la
mejor forma de ordenar las finanzas de una profesional ocupada no es pedirle más disciplina, sino hacer que el dato se genere solo. Los requerimientos y su jerarquía dejaron claro que el núcleo es la
agenda conectada y la ganancia real; el brainstorming y la clasificación permitieron llegar a un concepto factible con los recursos del equipo.</p>
<p>El enfoque sostenible cambió el resultado: incorporó ideas como agrupar domicilios, aprovechar horas vacías o cerrar el día antes de las 21 h, que no aparecían si solo se miraba lo financiero.
La metáfora del tablero y el copiloto resume la intención: acompañar a la kinesióloga sin quitarle el volante de su práctica.</p>
<h3>Aprendizajes del equipo</h3><ul>
<li>Mirar fuera del rubro abre más ideas que comparar competidores directos.</li>
<li>Definir los ejes de clasificación antes de mover los post-it evita discusiones y acelera el consenso.</li>
<li>La co-creación debe planificarse desde el inicio de la unidad: la disponibilidad de las usuarias es el recurso más escaso.</li></ul>
<h3>Próximos pasos (UA3 · Desarrollo y prototipado)</h3><ul>
<li>Prototipo navegable en Figma del alcance mínimo de {PRODUCTO}.</li>
<li>Dos ciclos de testeo con Joselyn y Catalina, midiendo las métricas claves (exigencia de la rúbrica ES03).</li>
<li>Validación de las reglas tributarias con el asesor financiero.</li></ul>
<h3>Trazabilidad con la rúbrica ES02</h3>{table(['Criterio', 'Evidencia en este informe', 'Dónde'], traz, 'tight')}'''
    return section('s-concl', 'CIERRE', 'Cierre', 'Conclusiones y próximos pasos', b)

def referencias():
    refs = [
        'Briede-Westermeyer, J. C., Leal-Figueroa, I. M., y Pérez-Villalobos, C. E. (2018). Análisis de referentes como estrategia de aprendizaje del diseño conceptual de productos. <em>Formación Universitaria, 11</em>(1), 3–12. https://doi.org/10.4067/S0718-50062018000100003',
        'Carlson, C. R., y Wilmot, W. W. (2006). <em>Innovation: The five disciplines for creating what customers want</em>. Crown Business.',
        'INACAP. (2026). <em>Toolkit Innovación y Emprendimiento III — Unidad 2: Ideación de propuestas</em>. Vicerrectoría Académica, Formación General.',
        'INACAP. (2026). <em>Guía para el estudiante — Innovación y Emprendimiento III, Unidad 2</em>. Vicerrectoría Académica, Formación General.',
        'Ley N° 21.133. (2019). Modifica las normas para la incorporación de los trabajadores independientes a los regímenes de protección social. Biblioteca del Congreso Nacional de Chile.',
        'Ley N° 21.719. (2024). Regula la protección y el tratamiento de los datos personales. Biblioteca del Congreso Nacional de Chile.',
        'Llorenc, G. (2011). <em>Anatomía de la creatividad</em>. Adria Gibernau.',
        'Maurya, A. (2012). <em>Running lean: Iterate from plan A to a plan that works</em> (2.ª ed.). O’Reilly Media.',
        'Naciones Unidas. (2015). <em>Transformar nuestro mundo: la Agenda 2030 para el Desarrollo Sostenible</em> (A/RES/70/1).',
        'Osterwalder, A., y Pigneur, Y. (2010). <em>Business model generation</em>. John Wiley and Sons.',
        'Pomar, P. (2020). <em>Cómo hacer brainstorming y no morir en el invento</em>. Thinkernautas.',
        'Servicio de Impuestos Internos. (2026). <em>Boletas de honorarios electrónicas y propuesta de declaración de renta</em>. https://www.sii.cl',
        'Sitios oficiales de los referentes (consultados en octubre de 2026): uber.com/cl, ynab.com, fintual.cl, mercadopago.cl, smartfit.cl, duolingo.com, strava.com, google.com/maps, toogoodtogo.com.']
    b = '<div class="small">' + ''.join(f'<p style="padding-left:6mm;text-indent:-6mm">{r}</p>' for r in refs) + '</div>'
    b += '''<h3>Anexos entregados por separado</h3><ul class="small"><li>Tableros de trabajo en Figma (instrumentos 18 a 26).</li><li>Bitácora de declaración de avance (Excel).</li>
<li>Registro de la sesión de co-creación <span class="pend">Pendiente de sesión</span></li><li>Fotografías de las entrevistas de la UA1.</li></ul>'''
    return section('s-ref', 'REFERENCIAS', 'Cierre', 'Referencias', b)

STMT.update({
    's-intro': 'Una kinesióloga, dos negocios en paralelo y <b>un dato que nunca llega</b>.',
    's-ruta': 'De un insight a una propuesta de valor, <b>en cinco semanas</b>.',
    's-fichas': 'Mirar fuera del rubro: <b>diez soluciones de otros mundos</b>.',
    's-matriz': 'En otros ámbitos, <b>el dato se captura solo</b>.',
    's-perfil': 'Lo que la usuaria necesita, convertido en <b>lo que la solución debe cumplir</b>.',
    's-cat': 'Trece requerimientos, <b>seis necesidades</b>.',
    's-jer': 'Primero la agenda conectada; <b>después todo lo demás</b>.',
    's-bs': 'Cantidad antes que calidad: <b>sesenta ideas sin juicio</b>.',
    's-clas': 'Más originales y más factibles: <b>trece ideas en el foco</b>.',
    's-fact': 'Tres caminos posibles, <b>uno que responde al desafío</b>.',
    's-cocrea': 'Diseñar <b>con</b> las usuarias, no solo <b>para</b> ellas.',
    's-meta': 'Ella maneja. <b>La herramienta es el copiloto</b>.',
    's-pv': 'Saber cuánto gana, anticipar lo que viene y <b>recuperar su tiempo</b>.',
    's-sost': 'Sostenible es que la práctica <b>pueda durar</b>.',
    's-tiempo': 'La meta, repartida en <b>semanas, personas y holguras</b>.',
    's-concl': 'Una idea que nace del dolor real y <b>se puede prototipar mañana</b>.',
})

# ---------------------------------------------------------------- páginas a sangre (lenguaje EV1)
def pagina_cita():
    return '''<div class="full orange"><img src="img/06-nudo.jpg">
<div class="in" style="top:24mm"><div class="kick">La voz de las usuarias · punto de partida de los requerimientos</div>
<div class="q">“Para poder organizar el Excel sobre los ingresos y egresos que estoy teniendo me toma una hora actualmente diario.”</div>
<div class="src">— Catalina, kinesióloga · entrevista a experta UA1 · P09</div>
<div class="q2">“Siento que igual tengo como un cierto desorden o falta de educación.”<br><span class="src">— Joselyn Toledo, sobre su gestión económica</span></div></div>
<div class="foot"><span>Perfil de usuaria y requerimientos</span><span>2.1.3</span></div></div>'''

def pagina_cifras():
    foco = sum(1 for i in IDEAS if quad(i) == '+O+F')
    return f'''<div class="full dark"><div class="in" style="top:40mm"><div class="kick" style="color:#FF6B35">Ideación · brainstorming y clasificación</div>
<div class="big">MUCHAS IDEAS,<br>UN SOLO <em>CONCEPTO</em>.</div>
<div class="lead2">Del desafío y los requerimientos jerarquizados salieron sesenta ideas sin juicio. Clasificadas por originalidad y factibilidad, trece quedaron en el foco y se sintetizaron en un concepto directriz.</div>
<div class="ncards"><div><div class="n">{len(IDEAS)}</div><div class="t">Ideas generadas</div><div class="d">8 categorías, incluidas las exploratorias que la técnica pide no descartar.</div></div>
<div><div class="n">{foco}</div><div class="t">En el foco</div><div class="d">Más originales y más factibles: la materia prima del concepto.</div></div>
<div><div class="n">1</div><div class="t">{PRODUCTO}</div><div class="d">Un copiloto financiero conectado a la agenda que ya usa.</div></div></div></div>
<div class="foot"><span>Canvas brainstorming · mapa de clasificación</span><span>2.1.4.1 · 2.1.4.2</span></div></div>'''

def pagina_pv():
    return f'''<div class="full dark solid"><img class="phone" src="img/14-dashboard.jpg">
<div class="in" style="top:36mm"><div class="kick" style="color:#FF6B35">Propuesta de valor · 2.1.4.4</div>
<div class="big">UN TABLERO<br>PARA TU <em>PRÁCTICA</em>.</div>
<div class="pv">{PRODUCTO} convierte cada atención en <b>ganancia real</b> y te avisa <b>qué viene</b>, sin que tengas que digitar.</div>
<div class="tags"><span>Anticipador</span><span>Legible de un vistazo</span><span>Automático</span><span>Sostenible</span></div></div>
<div class="foot"><span>Panel de propuesta de valor y métricas claves</span><span>Semana 8</span></div></div>'''

def pagina_cierre():
    return '''<div class="full sunset"><img src="img/15-horizonte.jpg">
<div class="in" style="top:30mm"><div class="kick" style="color:#FFD9C7">Conclusión</div>
<div class="big" style="font-size:38pt">EL VALOR NO ESTÁ EN ORDENAR EL EXCEL, SINO EN QUE <em style="color:#FFD9C7">EL DATO SE GENERE SOLO</em>.</div>
<div class="lead2" style="color:#F3E6FF">Referentes, requerimientos, ideas y usuarias convergen en lo mismo: conectar la agenda con el dinero para que la práctica independiente sea sostenible.</div></div>
<div class="foot"><span>Criterios 2.1.1 – 2.1.5</span><span>Gracias</span></div></div>'''

def pagina_anexo(titles):
    seen = []
    for t in titles:
        k = t.split(' · ', 1)[1].rsplit(' ', 1)[0] if t[-1].isdigit() else t.split(' · ', 1)[1]
        if k not in seen: seen.append(k)
    li = ''.join(f'<div style="border-bottom:1px solid #2A2640;padding:2mm 0;font-size:9.5pt;color:#E9E6F7">{k}</div>' for k in seen)
    return f'''<div class="full dark"><div class="in" style="top:34mm"><div class="kick" style="color:#FF6B35">Anexo A</div>
<div class="big">TOOLKIT UA2<br><em>COMPLETO</em>.</div>
<div class="lead2">Las plantillas oficiales del toolkit de Innovación y Emprendimiento III, llenas con el trabajo del equipo. Cada instrumento conserva su código y su formato original; las fichas de referentes se presentan una por caso.</div>
<div style="margin-top:8mm;max-width:150mm">{li}</div></div>
<div class="foot"><span>Matrices y paneles del toolkit</span><span>2.1.2.1 – 2.1.4.4</span></div></div>'''

# ---------------------------------------------------------------- ensamblado
import pymupdf as fitz
import anexo_toolkit

HEAD = '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Evaluación 2 — Ideación de Propuestas</title><link rel="stylesheet" href="ev2.css"></head><body>'
D = dict(REFS=REFS, VARS=VARS, DESAFIO=DESAFIO, EMPATIA=EMPATIA, REQS=REQS, CATS=CATS, JER=JER, IDEAS=IDEAS, CATC=CATC, CATN=CATN, quad=quad,
         METAFORA=f'“{PRODUCTO} es como el tablero y el copiloto de un auto de rally.” Joselyn maneja: atiende a sus pacientes. El tablero le muestra la ganancia del mes y el colchón; el copiloto le lee la ruta que viene: los meses bajos, la agenda del día y cuándo acelerar. Ella nunca suelta el volante.',
         ATRIBUTOS=ATR, PV=f'{PRODUCTO} es el copiloto financiero de la kinesióloga independiente: se conecta a la agenda que ya usa y convierte cada atención en ganancia real —descontando traslado, materiales, comisión e impuestos— para que sepa cuánto gana, anticipe los meses bajos y deje de cuadrar Excel de noche.')

def render(body, name):
    path = os.path.join(HERE, name)
    open(path, 'w', encoding='utf-8').write(HEAD + body + '</body></html>')
    return HTML(path, base_url=HERE).write_pdf()

def main_body():
    return (portada() + indice() + intro() + ruta() + fichas() + matriz() + pagina_cita() + perfil() + categorias() + jerarquias()
            + pagina_cifras() + brainstorming() + clasificacion() + factibilidad() + cocreacion() + metaforas() + pagina_pv() + propuesta()
            + sostenibilidad() + tiempo() + conclusiones() + referencias())

# 1.ª pasada: largo del cuerpo principal → página donde empieza el anexo
ANEXO_PAGE = '—'
n_main = fitz.open(stream=render(main_body(), '_tmp.html'), filetype='pdf').page_count
ANEXO_PAGE = n_main + 1
main_pdf = fitz.open(stream=render(main_body(), 'Evaluacion2_Informe_Ideacion.html'), filetype='pdf')
assert main_pdf.page_count == n_main
anexo_pdf, titles = anexo_toolkit.build(D, n_main + 2)
div_pdf = fitz.open(stream=render(pagina_anexo(titles), '_anexo.html'), filetype='pdf')
end_pdf = fitz.open(stream=render(pagina_cierre(), '_cierre.html'), filetype='pdf')
for extra in (div_pdf, anexo_pdf, end_pdf):
    main_pdf.insert_pdf(extra)
for f in ('_tmp.html', '_anexo.html', '_cierre.html'):
    os.remove(os.path.join(HERE, f))
main_pdf.save(os.path.join(HERE, 'Evaluacion2_Informe_Ideacion.pdf'), garbage=3, deflate=True)
print('ok', main_pdf.page_count, 'páginas · anexo desde', ANEXO_PAGE)
