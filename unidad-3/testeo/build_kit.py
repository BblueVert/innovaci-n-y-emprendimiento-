# Kit de testeo con usuarios · Copiloto Kine (v2) · EV3 Innovación y Emprendimiento III.
# Documentos listos para aplicar con distintos públicos: kinesiólogas (usuarias principales), pacientes de distintos perfiles
# (usuarios secundarios: reciben los mensajes) y contadora. Los resultados quedan marcados como pendientes hasta aplicar las sesiones.
# Uso: python3 build_kit.py  →  Kit_Testeo_Copiloto_Kine.html / .pdf
import os
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
PEND = '<span class="pend">Pendiente de sesión</span>'
EQUIPO = 'Francisco Ahumada · Claudia Cifuentes · Néstor Rivera · Benjamín Vera Yáñez'


def table(headers, rows, cls=''):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def section(sid, label, kicker, title, body, code=None):
    c = f'<span class="code">{code}</span>' if code else ''
    return (f'<div class="section" id="{sid}"><div class="section-head" data-sec="{label}"><div class="kicker">{kicker}</div>'
            f'<h2>{c}{title}</h2></div>{body}</div>')


def blank(n, cols):
    return ''.join('<tr>' + ''.join('<td>&nbsp;</td>' for _ in range(cols)) + '</tr>' for _ in range(n))


# ---------------------------------------------------------------- hipótesis (cruce EV1 · EV2 · ciclos 1 y 2)
HIP = [
    ('H1', 'Kinesióloga', 'Cierra el día en menos de 30 minutos (meta del desafío).', 'Tiempo y toques para cerrar un día de 5 atenciones', '≤ 5 min sin digitar', 'Desafío UA1 · P4 ciclo 2 (11 toques)'),
    ('H2', 'Kinesióloga', 'Entiende “ganancia real” sin explicación.', 'La explica con sus palabras tras ver el tablero 5 s', '2 de 2 kinesiólogas', 'H2 heurística ciclo 1'),
    ('H3', 'Kinesióloga · contadora', 'Confía en el cálculo de comisión, traslado y retención.', 'Confianza 1–5 y revisión de la contadora', '≥ 4 y sin errores', 'P1 · P11 ciclo 2 · R12'),
    ('H4', 'Kinesióloga', 'Pagaría una suscripción mensual por la herramienta.', 'Precio aceptable (4 preguntas de sensibilidad al precio)', 'Rango que incluya ≤ $25.000', 'Antecedentes UA1 · amenaza económica PESTAL'),
    ('H5', 'Pacientes a domicilio', 'Aceptan una ventana de llegada de 30 min para que la kine ordene su ruta.', 'Respuesta al recordatorio M1', '≥ 70 % confirma la ventana', 'Ruta sugerida (−7 km/día) · amenaza ambiental PESTAL'),
    ('H6', 'Pacientes', 'El aviso “voy en camino” se entiende y da tranquilidad.', 'Comprensión sin ayuda y valoración 1–5', '≥ 80 % entiende · ≥ 4', 'Atributo “Cercano” · CDM ciclo 1'),
    ('H7', 'Pacientes', 'El comprobante sin diagnóstico les sirve (incluido reembolso).', '¿Le falta algo para usarlo?', '≥ 80 % lo considera suficiente', 'B6 · Ley 21.719 · R13'),
    ('H8', 'Adulto mayor', 'Lee y responde el recordatorio solo o con letra grande.', 'Completa M1 sin ayuda del moderador', '≥ 2 de 3 participantes', 'Brecha digital · PESTAL social'),
    ('H9', 'Contadora', 'El resumen exportado alcanza para la declaración mensual y anual.', 'Lista de verificación de la contadora', 'Sin campos faltantes críticos', 'P6 ciclo 2 · R12'),
    ('H10', 'Pacientes', 'Una hora liberada a precio preferente les interesa y no se siente invasiva.', 'Respuesta a M4', '≥ 50 % la tomaría · 0 la percibe como spam', 'Idea EV2 (referente Too Good To Go) · R11'),
]

# ---------------------------------------------------------------- perfiles
PERF = [
    dict(c='K1', n='Joselyn Toledo', t='Kinesióloga independiente · usuaria del caso', tipo='k', real=True,
         d='Atención mixta: Centro Médico InMotion (70/30) y domicilios en Rancagua y Machalí. Hoy cuadra ingresos en Excel de noche.',
         s='Prototipo Kine completo (tareas T1–T11)', h='H1 · H2 · H3 · H4', m='Presencial con su celular · 60 min', a='Moderación sin explicar la interfaz; pedir que piense en voz alta.'),
    dict(c='K2', n='Catalina', t='Kinesióloga · experta par (UA1)', tipo='k', real=True,
         d='Colega independiente entrevistada en la UA1: “organizar el Excel me toma una hora diaria”.',
         s='Prototipo Kine: T1, T2, T5, T7, T9, T11', h='H1 · H2 · H4', m='Remota (videollamada compartiendo pantalla) · 40 min', a='Si no puede conectarse: recorrido grabado + notas de voz con las preguntas.'),
    dict(c='C1', n='Contadora o asesor financiero', t='Experto técnico', tipo='e', real=False,
         d='Lleva la contabilidad de profesionales a honorarios (boletas, retención, Operación Renta).',
         s='Exportación CSV + vista “Mi plata”', h='H3 · H9', m='Remota · 20 min', a='Enviar el CSV de ejemplo con anticipación.'),
    dict(c='P1', n='“Don Hernán”', t='Adulto mayor atendido a domicilio', tipo='p',
         d='70 años o más. Rehabilitación tras una caída o por artrosis. Vive en Machalí con su familia. Usa WhatsApp, con letra grande.',
         s='Vista paciente: M1 y M2 (con “Letra grande”)', h='H5 · H6 · H8', m='Presencial, idealmente en su casa · 15 min', a='Leer en voz alta si lo pide; frases cortas; un mensaje a la vez; permitir acompañante.'),
    dict(c='P2', n='“Marcela”', t='Cuidadora familiar', tipo='p',
         d='40 a 60 años. Coordina las sesiones de su madre o padre mientras trabaja. Paga por transferencia y guarda las boletas.',
         s='Vista paciente: M1, M2 y M3', h='H5 · H6 · H7', m='Presencial o remota · 15 min', a='Preguntar por quién recibe los mensajes: ella o su familiar.'),
    dict(c='P3', n='“Camila”', t='Estudiante con dolor de espalda', tipo='p',
         d='18 a 25 años. Dolor lumbar o cervical por postura y horas de notebook. Presupuesto ajustado. Agenda todo desde el celular.',
         s='Vista paciente: M1, M3 y M4', h='H5 · H7 · H10', m='Presencial en INACAP · 15 min', a='Explorar sensibilidad al precio y packs.'),
    dict(c='P4', n='“Rodrigo”', t='Trabajador de oficina o teletrabajo', tipo='p',
         d='30 a 45 años. Cervicalgia o tendinitis por trabajo en computador. Agenda rígida; pide reembolso a su Isapre o seguro.',
         s='Vista paciente: M1 y M3', h='H5 · H7', m='Remota o presencial · 15 min', a='Explorar si una ventana de 30 min le complica el horario laboral.'),
    dict(c='P5', n='“Luis”', t='Trabajador por turnos (minería o industria)', tipo='p',
         d='35 a 55 años. Lumbalgia no laboral. Sistema de turnos 7×7: solo puede atenderse en sus días libres.',
         s='Vista paciente: M1 y M4', h='H5 · H10', m='Presencial o remota · 15 min', a='Explorar agendamiento en bloques de días libres.'),
    dict(c='P6', n='“Valentina”', t='Deportista amateur', tipo='p',
         d='20 a 35 años. Esguince o tendinopatía por running o fútbol. Quiere volver rápido a entrenar; flexible en horario.',
         s='Vista paciente: M1, M2 y M4', h='H6 · H10', m='Presencial · 15 min', a='Explorar interés en horas liberadas de último minuto.'),
]

TAREAS = [
    ('T1', 'Es lunes temprano. ¿Cómo va tu mes? ¿Vas bien?', 'Dice la ganancia del mes y el estado sin tocar nada'),
    ('T2', 'Terminaste con Rosa en la clínica. Regístralo.', '≤ 2 toques'),
    ('T3', '¿Cuánto te quedó realmente de la atención de Carmen a domicilio?', 'Lee $21.090 y nombra al menos 2 descuentos'),
    ('T4', 'Marcaste a Pedro por error. Corrígelo.', 'Usa “Deshacer”'),
    ('T5', 'Vas a salir a domicilios. Revisa la ruta y avisa a tu primera paciente.', 'Usa “Voy en camino”'),
    ('T6', 'Compara la ruta sugerida con el orden en que lo harías tú.', 'Encuentra la diferencia de km'),
    ('T7', '¿Cuánto te falta para cubrir enero y febrero? Agrega una acción.', 'Lee la brecha y agrega una acción'),
    ('T8', '¿Cuánto tienes separado para impuestos?', 'Lo encuentra en “Mi plata”'),
    ('T9', 'La clínica subió la comisión a 35 %. Actualízalo.', 'Edita el campo de comisión'),
    ('T10', 'Luis no llegó a su hora. Regístralo.', 'Usa “No asistió”'),
    ('T11', 'Es fin de mes. Prepara lo que le envías a tu contadora.', 'Descarga el resumen'),
]

SUS = ['Creo que me gustaría usar esta app con frecuencia.', 'Encontré la app innecesariamente compleja.', 'Pensé que la app era fácil de usar.',
       'Creo que necesitaría ayuda de una persona con conocimientos técnicos para usarla.', 'Las funciones de la app están bien integradas.',
       'Pensé que había demasiada inconsistencia en la app.', 'Imagino que la mayoría de las personas aprendería a usarla muy rápido.',
       'Encontré la app muy engorrosa de usar.', 'Me sentí muy segura usando la app.', 'Necesité aprender muchas cosas antes de poder usarla.']

ENC_PAC = ['Entendí el mensaje sin ayuda.', 'La información de hora y valor es suficiente.', 'El aviso “voy en camino” me da tranquilidad.',
           'El comprobante me sirve para mis trámites o reembolsos.', 'Me parece bien una ventana de llegada de 30 minutos.',
           'Me sentiría cómodo/a de que mi kine use una app para ordenar su día.']

DECISION = [
    ('H1', 'Mantener el registro de un toque como núcleo del MVP.', 'Agregar cierre del día en lote (“marcar todas como realizadas”).'),
    ('H2', 'Mantener la definición bajo el indicador.', 'Cambiar el término por “lo que te queda”.'),
    ('H3', 'Avanzar a integrar la boleta del SII.', 'Mostrar la fórmula en cada desglose y validar con la contadora.'),
    ('H4', 'Precio de lanzamiento dentro del rango aceptado.', 'Plan gratuito con 1 función (ganancia real) y pago por ruta y proyección.'),
    ('H5', 'Ruta sugerida para todos los domicilios.', 'Marcar “hora fija” por paciente: la ruta se ordena solo con los flexibles.'),
    ('H6', 'Pasar el aviso a WhatsApp real (enlace wa.me, B5).', 'Reescribir el mensaje con hora exacta en vez de minutos.'),
    ('H7', 'Comprobante como está.', 'Agregar campos que pidan (RUT, código de prestación) sin datos clínicos.'),
    ('H8', 'Mensajes en texto con letra del sistema.', 'Versión con nota de voz o envío al cuidador.'),
    ('H9', 'Mantener columnas del CSV.', 'Agregar las columnas que pida la contadora (folio de boleta, RUT).'),
    ('H10', 'Incluir horas liberadas en la fase 2.', 'Descartar o dejar solo para pacientes que lo activen.'),
]


# ---------------------------------------------------------------- páginas
def portada():
    chips = ''.join(f'<span class="chip">{c}</span>' for c in ['3.1.2.3 Ficha de planificación', '3.1.3.4 Testeo de la iteración', '10 hipótesis', '9 perfiles', '3 guiones', 'Formularios imprimibles'])
    return f'''<div class="cover"><div class="bar"></div><img class="hero" src="../ev3/img/01-portada.jpg">
<div><div class="inst" style="color:var(--accent)">Innovación y Emprendimiento III · INACAP Rancagua</div></div>
<div><h1>KIT DE<br>TESTEO</h1><div class="sub">COPILOTO KINE · PROTOTIPO V2</div>
<div class="inst" style="margin-top:2mm">Documentos para validar con usuarias, pacientes y expertos · Unidad 3 · FGIE03</div><div class="div"></div>
<div class="desc">Todo lo necesario para llevar el prototipo a personas reales: hipótesis, perfiles de participantes, guiones de sesión,
consentimiento, pautas de observación, cuestionarios y la matriz para consolidar resultados y decidir la siguiente iteración.</div>
<div class="grid">{chips}</div></div>
<div class="meta"><div class="team"><div>Francisco Ahumada · Claudia Cifuentes</div><div>Néstor Rivera · Benjamín Vera Yáñez</div>
<div class="inst" style="margin-top:1mm">Profesor: Roberto Escobar Donoso</div></div>
<div style="text-align:right"><div class="inst">Rancagua, Chile</div><div class="inst">Noviembre 2026</div></div></div></div>'''


def uso():
    pasos = [('1', 'Antes', 'Revisar hipótesis y perfiles · reclutar · enviar invitación · preparar celular con el prototipo y la vista paciente.'),
             ('2', 'Durante', 'Leer el guion que corresponde · firmar consentimiento · registrar en la pauta · aplicar cuestionario.'),
             ('3', 'Después', 'Calcular SUS · pasar datos a la matriz de consolidación · decidir mantener, iterar o descartar por hipótesis.')]
    b = f'''<p class="lead">Este kit convierte el prototipo v2 en una prueba aplicable con personas. Los ciclos 1 y 2 se hicieron dentro del equipo
(uso y estética, luego verificación técnica); este kit prepara el <b>ciclo con usuarios reales</b>, que el toolkit pide para validar el prototipo con usuarios internos y externos.</p>
<div class="chain">{''.join(f'<div><b>{n} · {t}</b>{d}</div>' for n, t, d in pasos)}</div>
<h3>Qué se prueba con cada público</h3>
{table(['Público', 'Rol frente a Copiloto Kine', 'Estímulo', 'Guion'], [
        ['<b>Kinesiólogas</b> (K1, K2)', 'Usuarias principales: registran, ordenan su ruta y controlan su plata.', '<code>prototipo/copiloto-kine.html</code>', 'A · 40–60 min'],
        ['<b>Pacientes</b> (P1–P6)', 'Usuarios secundarios: reciben el recordatorio, el aviso, el comprobante y las horas liberadas.', '<code>prototipo/vista-paciente.html</code>', 'B · 15 min'],
        ['<b>Contadora</b> (C1)', 'Experta técnica: recibe el resumen mensual.', 'CSV exportado + “Mi plata”', 'C · 20 min']])}
<h3>Por qué incluir pacientes</h3>
<p>El paciente no usa la app, pero vive sus consecuencias: la ruta sugerida solo funciona si acepta una <b>ventana de llegada</b>, el aviso
“voy en camino” es su principal contacto con el sistema y el comprobante debe servirle sin exponer datos de salud. Por eso las hipótesis H5 a H8 y H10
solo se pueden validar con ellos. Los perfiles cubren distintas edades, trabajos y dolencias porque la kinesiología atiende a casi cualquier persona.</p>
<div class="note"><b>Insumo pendiente · reunión del jueves 12 de noviembre (8:30).</b> El profesor compartirá la grabación de la retroalimentación
de la emprendedora sobre los trabajos revisados. Su transcripción entra en la matriz de consolidación (página “Consolidar”) como fuente F0, antes de las sesiones,
para ajustar el prototipo o el guion si corresponde.</div>'''
    return section('k-uso', 'CÓMO USAR EL KIT', 'Kit de testeo', 'Cómo usar este kit', b)


def plan():
    b = f'''<div class="pvq">Objetivo: validar con kinesiólogas, pacientes y una contadora que Copiloto Kine v2 resuelve sus necesidades reales
—saber cuánto se gana, cerrar el día sin Excel, coordinar domicilios y entregar números sin datos de salud— y decidir qué cambia en la versión 3.</div>
<h3>Hipótesis a validar</h3>
{table(['#', 'Público', 'Hipótesis', 'Cómo se mide', 'Criterio de éxito', 'Origen'], [[f'<b>{a}</b>', b_, c, d, e, f'<span class="small muted">{f}</span>'] for a, b_, c, d, e, f in HIP], 'tight')}'''
    return section('k-plan', 'PLAN DE TESTEO', '3.1.3.4 · Ficha de planificación del testeo con usuarios', 'Plan e hipótesis', b, '3.1.3.4')


def plan2():
    filas = [
        ['Validar uso y valor con kinesiólogas', 'K1 Joselyn · K2 Catalina', 'Prototipo Kine v2 en su celular', 'Tareas T1–T11, SUS, preguntas CDM, precio', 'Mod.: Claudia · Obs.: Francisco · Téc.: Néstor', 'H1 · H2 · H3 · H4', 'Clínica o remota', '40–60 min'],
        ['Validar mensajes con pacientes', 'P1–P6 · 1 a 2 por perfil', 'Vista paciente (M1–M4)', 'Lectura y reacción a cada mensaje, encuesta breve', 'Mod.: Claudia o Benjamín · Obs.: Néstor', 'H5 · H6 · H7 · H8 · H10', 'Domicilio, INACAP o remota', '15 min'],
        ['Validar exactitud y entrega contable', 'C1 contadora', 'CSV + “Mi plata”', 'Revisión guiada con lista de verificación', 'Benjamín', 'H3 · H9', 'Remota', '20 min'],
    ]
    crono = [('Jue 12 nov · 8:30', 'Reunión con retroalimentación de la emprendedora (grabación del profesor)', 'Insumo F0'),
             ('Vie 13 – lun 16 nov', 'Transcribir y analizar F0 · ajustes menores al prototipo o al guion · reclutar e invitar', 'Equipo'),
             ('Mar 17 – jue 19 nov', 'Sesiones: K1, K2, C1 y pacientes P1–P6', 'Moderación por turnos'),
             ('Vie 20 nov', 'Consolidar: SUS, matriz, CDM y decisiones v3', 'Benjamín consolida'),
             ('Semana siguiente', 'Presentar resultados y backlog del MVP (UA4)', 'Equipo')]
    b = f'''<h3>Actividades, roles y lugar</h3>
{table(['Objetivo específico', 'Participantes', 'Prototipo', 'Actividad', 'Roles', 'Hipótesis', 'Lugar', 'Tiempo'], filas, 'tight')}
<div class="grid2"><div><h3>Muestra</h3>
<ul><li><b>Kinesiólogas:</b> 2 (caso + experta par).</li><li><b>Pacientes:</b> mínimo 6 (uno por perfil), ideal 10–12. Con 5 personas por segmento se detecta la mayoría de los problemas de uso.</li>
<li><b>Contadora:</b> 1.</li></ul>
<h3>Reclutamiento ético</h3>
<ul><li>Pacientes de Joselyn <b>solo si ella los invita</b> y aceptan; nunca se usan sus datos de agenda.</li>
<li>Alternativa: personas del entorno del equipo que calcen con el perfil (familiares, compañeros INACAP, trabajadores por turno).</li>
<li>La dolencia se pregunta solo como categoría general y es voluntaria; no se registran diagnósticos.</li></ul></div>
<div><h3>Cronograma</h3>{table(['Fecha', 'Actividad', 'Responsable'], crono, 'tight')}
<h3>Materiales</h3><ul class="small"><li>Celular con ambos prototipos abiertos y datos limpios (botón “Deshacer” o borrar datos del sitio).</li>
<li>Consentimientos y pautas impresos (págs. siguientes).</li><li>Grabación de audio solo con autorización.</li><li>Cronómetro y lápiz.</li></ul></div></div>'''
    return section('k-plan2', 'PLAN DE TESTEO', '3.1.3.4 · Ficha de planificación del testeo con usuarios', 'Actividades, muestra y calendario', b)


def perfiles():
    cards = ''
    for p in PERF:
        tag = {'k': 'Kinesióloga', 'e': 'Experto', 'p': 'Paciente'}[p['tipo']]
        real = '<span class="code b">Participante real</span>' if p.get('real') else ('<span class="code">Perfil a reclutar</span>')
        cards += f'''<div class="pf {p['tipo']}"><div class="top"><span class="cd">{p['c']}</span><div><b>{p['n']}</b><span>{p['t']}</span></div><em>{tag}</em></div>
<div class="bd"><p>{p['d']}</p><div class="kv"><span>Prueba</span>{p['s']}</div><div class="kv"><span>Hipótesis</span>{p['h']}</div>
<div class="kv"><span>Modalidad</span>{p['m']}</div><div class="kv"><span>Adaptación</span>{p['a']}</div><div style="margin-top:1mm">{real}</div></div></div>'''
    b = f'''<p class="lead">Nueve perfiles: dos kinesiólogas reales (el caso y la experta de la UA1), una contadora y seis perfiles de pacientes que cubren
edades, trabajos y dolencias frecuentes en la consulta particular. Los nombres de pacientes entre comillas son ficticios: describen a quién reclutar.</p>
<div class="pfs">{cards}</div>'''
    return section('k-perf', 'PERFILES', 'Participantes del testeo', 'Perfiles de participantes', b)


def estimulos():
    shots = [('../prototipo/capturas_v2/01_tablero.png', 'Kine · Tablero'), ('../prototipo/capturas_v2/02_ruta_sugerida.png', 'Kine · Ruta'),
             ('../prototipo/capturas_v2/06_agenda.png', 'Kine · Agenda'), ('../prototipo/capturas_paciente/01_recordatorio.png', 'M1 · Recordatorio'),
             ('../prototipo/capturas_paciente/02_voy_en_camino.png', 'M2 · Voy en camino'), ('../prototipo/capturas_paciente/03_comprobante.png', 'M3 · Comprobante'),
             ('../prototipo/capturas_paciente/04_hora_liberada.png', 'M4 · Hora liberada')]
    ph = ''.join(f'<figure><img src="{s}"><figcaption>{t}</figcaption></figure>' for s, t in shots)
    b = f'''<p class="lead">Dos prototipos navegables en el celular. El de la kinesióloga es el v2 iterado tras los ciclos 1 y 2; la <b>vista paciente</b>
es nueva: simula los mensajes que el paciente recibiría por WhatsApp cuando su kine usa Copiloto Kine. No envía nada y no muestra datos clínicos.</p>
<div class="shots">{ph}</div>
{table(['Mensaje', 'Qué valida', 'Hipótesis'], [
        ['M1 · Recordatorio con ventana de llegada', 'Si el paciente acepta 30 min de holgura para que la ruta se ordene.', 'H5 · H8'],
        ['M2 · Voy en camino', 'Comprensión del aviso y tranquilidad en la espera.', 'H6'],
        ['M3 · Comprobante', 'Si sirve para trámites y reembolsos sin diagnóstico.', 'H7'],
        ['M4 · Hora liberada', 'Interés por horas de último minuto a precio preferente.', 'H10']], 'tight')}
<p class="small muted">Antes de cada sesión: abrir la pestaña que corresponde, usar “Cambiar nombre del paciente” con el nombre del participante
y activar “Letra grande” para P1.</p>'''
    return section('k-est', 'ESTÍMULOS', 'Lo que se muestra', 'Prototipos de la sesión', b)


def guion_a():
    pasos = [
        ('0 · Bienvenida', '3 min', '“Gracias por tu tiempo. Estamos probando una app, no a ti: si algo no se entiende, es un problema de la app. Piensa en voz alta mientras la usas. No te vamos a ayudar durante las tareas para ver cómo funciona sola.”'),
        ('1 · Consentimiento', '2 min', 'Leer y firmar el consentimiento. Preguntar si autoriza grabar audio.'),
        ('2 · Contexto', '5 min', '¿Cómo cerraste tu último día de trabajo? ¿Cuánto tiempo te tomó? ¿Sabes cuánto ganaste el mes pasado, ya descontados los costos?'),
        ('3 · Primera impresión', '2 min', 'Mostrar el tablero 5 segundos y ocultarlo. “¿Qué te dijo esa pantalla?” “¿Qué significa ganancia real?”'),
        ('4 · Tareas', '25 min', 'Leer cada tarea tal cual (tabla). Registrar éxito, toques, tiempo y frases en la pauta. Si se bloquea 2 min, pasar a la siguiente.'),
        ('5 · Cuestionario SUS', '5 min', 'Aplicar las 10 afirmaciones (formulario).'),
        ('6 · Propuesta de valor', '7 min', '¿Qué cualidades tiene? ¿Qué debilidades? ¿Qué mejorarías? ¿Te hace sentido que sea “como un copiloto de rally que lee la ruta y lleva las cuentas”?'),
        ('7 · Precio', '3 min', '¿A qué precio mensual te parecería barata? ¿Cara pero la pagarías? ¿Tan cara que no la pagarías? ¿Tan barata que dudarías de su calidad?'),
        ('8 · Cierre', '2 min', '“Si mañana pudieras usar una sola función, ¿cuál sería?” Agradecer.'),
    ]
    b = f'''<div class="inst-card"><div class="col"><div class="lbl">Participantes</div>K1 Joselyn · K2 Catalina</div><div class="col"><div class="lbl">Duración</div>40–60 min</div>
<div class="col"><div class="lbl">Estímulo</div>copiloto-kine.html (v2)</div><div class="col"><div class="lbl">Hipótesis</div>H1 · H2 · H3 · H4</div></div>
{table(['Bloque', 'Tiempo', 'Qué decir o hacer'], pasos, 'tight')}
<h3 style="break-before:page">Tareas (leer tal cual)</h3>
{table(['#', 'Escenario', 'Éxito si…'], [[f'<b>{a}</b>', f'“{b_}”', c] for a, b_, c in TAREAS], 'tight')}
<p class="small muted">Para K2 (remota) aplicar T1, T2, T5, T7, T9 y T11. Si no hay conexión, enviar el enlace y pedir notas de voz por tarea.</p>'''
    return section('k-ga', 'GUION A', 'Guion de sesión · kinesiólogas', 'Guion A · Kinesiólogas', b)


def guion_b():
    pasos = [
        ('0 · Bienvenida', '1 min', '“Te vamos a mostrar unos mensajes que te podría mandar tu kinesióloga. No hay respuestas correctas.”'),
        ('1 · Consentimiento', '1 min', 'Versión breve, leída en voz alta. No se pregunta diagnóstico; si menciona su dolencia, no se anota.'),
        ('2 · Contexto', '2 min', '¿Te has atendido con kinesiólogo? ¿En consulta o en tu casa? ¿Cómo coordinan la hora? ¿Qué te molesta de esperar?'),
        ('3 · M1 Recordatorio', '3 min', '“Te llega este mensaje. ¿Qué entiendes? ¿Qué responderías?” → ¿Te acomoda una ventana de 30 min? ¿Por qué?'),
        ('4 · M2 Voy en camino', '2 min', '“¿Qué te dice este mensaje? ¿Te sirve? ¿Qué le cambiarías?”'),
        ('5 · M3 Comprobante', '2 min', '“¿Para qué usarías este comprobante? ¿Le falta algo?” (reembolso, Isapre, Fonasa, seguro)'),
        ('6 · M4 Hora liberada', '2 min', '“¿La tomarías? ¿Te molestaría recibir este tipo de mensaje?”'),
        ('7 · Privacidad', '1 min', '“¿Te parece bien que tu kine use una app para ordenar su día? ¿Qué datos tuyos no te gustaría que estuvieran ahí?”'),
        ('8 · Encuesta y cierre', '2 min', 'Encuesta breve (formulario) y agradecer.'),
    ]
    adap = [['P1 Adulto mayor', 'Activar “Letra grande”. Leer en voz alta si lo pide. Permitir que responda el acompañante, anotando quién respondió. Medir H8: ¿lo resolvió sin ayuda?'],
            ['P2 Cuidadora', 'Preguntar quién debería recibir cada mensaje: ella, su familiar o ambos. Usar “Enviar boleta a otro correo” en M3.'],
            ['P3 Estudiante', 'Profundizar en M4 y precio: ¿cuánto pagaría por sesión? ¿Packs?'],
            ['P4 Oficina', 'En M1, explorar “Necesito una hora exacta”: ¿le sirve la ventana con su horario laboral?'],
            ['P5 Turnos 7×7', 'En M1 y M4: ¿cómo agenda en sus días libres? ¿Le sirve reservar un bloque de sesiones?'],
            ['P6 Deportista', 'En M4: ¿tomaría horas de último minuto? ¿Le interesa seguir su avance?']]
    b = f'''<div class="inst-card"><div class="col"><div class="lbl">Participantes</div>P1–P6 · 1 a 2 por perfil</div><div class="col"><div class="lbl">Duración</div>15 min</div>
<div class="col"><div class="lbl">Estímulo</div>vista-paciente.html (M1–M4)</div><div class="col"><div class="lbl">Hipótesis</div>H5 · H6 · H7 · H8 · H10</div></div>
{table(['Bloque', 'Tiempo', 'Qué decir o hacer'], pasos, 'tight')}
<h3>Adaptaciones por perfil</h3>{table(['Perfil', 'Ajuste de la sesión'], adap, 'tight')}'''
    return section('k-gb', 'GUION B', 'Guion de sesión · pacientes', 'Guion B · Pacientes', b)


def guion_c():
    check = ['Las columnas permiten calcular ingresos brutos del mes.', 'La retención está calculada con la tasa vigente (15,25 % en 2026; 16 % en 2027).',
             'Se distinguen ingresos de clínica (con comisión) y de domicilio.', 'Los costos de traslado y materiales están separados.',
             'Falta algún dato para cuadrar con las boletas del SII (folio, RUT, fecha de emisión).', 'El formato (CSV con “;”) se abre bien en su planilla.',
             'No hay datos que no debería recibir (diagnósticos, nombres completos).', '¿Cada cuánto le serviría recibirlo? (semanal, mensual, anual).']
    b = f'''<div class="inst-card"><div class="col"><div class="lbl">Participante</div>C1 contadora o asesor</div><div class="col"><div class="lbl">Duración</div>20 min</div>
<div class="col"><div class="lbl">Estímulo</div>CSV exportado + “Mi plata”</div><div class="col"><div class="lbl">Hipótesis</div>H3 · H9</div></div>
<ol><li><b>Contexto (3 min).</b> ¿Cómo le llegan hoy los números de sus clientes a honorarios? ¿Qué es lo que más le cuesta?</li>
<li><b>Revisión del resumen (10 min).</b> Abrir el CSV y recorrer la lista de verificación.</li>
<li><b>Cálculo (5 min).</b> Mostrar el desglose de Carmen ($28.000 → $21.090). “¿Está bien calculado? ¿Qué haría distinto?”</li>
<li><b>Cierre (2 min).</b> “¿Recomendaría esta herramienta a sus clientes?”</li></ol>
{table(['Punto a revisar', 'Sí', 'No', 'Comentario'], [[c, '☐', '☐', ''] for c in check], 'tight form')}'''
    return section('k-gc', 'GUION C', 'Guion de sesión · contadora', 'Guion C · Contadora', b)


def consentimiento():
    b = f'''<div class="consent"><p>Te invitamos a participar en una prueba del prototipo <b>Copiloto Kine</b>, desarrollado por estudiantes de Diseño Digital de INACAP Rancagua
para la asignatura Innovación y Emprendimiento III (profesor Roberto Escobar Donoso). El objetivo es evaluar el prototipo, no a ti.</p>
<ul><li>La sesión dura entre 15 y 60 minutos, según tu perfil.</li>
<li>Tu participación es voluntaria. Puedes no responder una pregunta o retirarte cuando quieras, sin dar explicaciones.</li>
<li>No te pediremos diagnósticos ni información de salud. Si mencionas alguna, no quedará registrada.</li>
<li>Tus respuestas se usarán solo con fines académicos y se presentarán sin tu nombre (con un código, por ejemplo “P3”).</li>
<li>Los datos se guardan en el equipo de trabajo y se eliminan al cerrar la asignatura, de acuerdo con la Ley 19.628 y la Ley 21.719 de protección de datos personales.</li>
<li>Si lo autorizas, grabaremos solo el audio para no perder detalles; la grabación no se comparte.</li></ul>
<table class="form sign"><tbody>
<tr><td>Nombre</td><td></td><td>Código de participante</td><td style="width:22%"></td></tr>
<tr><td>Autorizo grabar audio</td><td>☐ Sí &nbsp;&nbsp; ☐ No</td><td>Fecha</td><td></td></tr>
<tr><td>Firma</td><td></td><td>Moderador/a</td><td></td></tr></tbody></table>
<p class="small muted">Contacto del equipo: {EQUIPO} · INACAP Rancagua.</p></div>'''
    return section('k-cons', 'CONSENTIMIENTO', 'Formulario imprimible', 'Consentimiento informado', b)


def pauta():
    rows = ''.join(f'<tr><td><b>{t}</b></td><td class="sm">{s[:60]}{"…" if len(s) > 60 else ""}</td><td>☐ S ☐ A ☐ N</td><td></td><td></td><td></td><td></td></tr>' for t, s, _ in TAREAS)
    b = f'''<table class="form head"><tbody><tr><td>Código</td><td></td><td>Perfil</td><td></td><td>Fecha</td><td></td></tr>
<tr><td>Moderador/a</td><td></td><td>Observador/a</td><td></td><td>Modalidad</td><td>☐ Presencial ☐ Remota</td></tr></tbody></table>
<table class="form obs"><thead><tr><th>#</th><th>Tarea</th><th>Resultado</th><th>Toques</th><th>Tiempo</th><th>Frase textual / observación</th><th>Sev. 0–4</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small muted"><b>Resultado:</b> S = sin ayuda · A = con ayuda · N = no la completa. <b>Severidad:</b> 0 sin problema · 1 cosmético · 2 menor · 3 mayor · 4 bloqueante.</p>
<h3>Primera impresión (5 segundos)</h3><div class="lines"></div>
<h3>Cualidades · debilidades · mejoras</h3><table class="form"><tbody><tr><td style="width:33%">Cualidades</td><td style="width:33%">Debilidades</td><td>Mejoras</td></tr><tr class="tall"><td></td><td></td><td></td></tr></tbody></table>'''
    return section('k-pauta', 'PAUTA A', 'Formulario imprimible · guion A', 'Pauta de observación · kinesiólogas', b)


def pauta_b():
    msgs = [('M1', 'Recordatorio', '¿Confirma la ventana de 30 min? ☐ Sí ☐ Pide hora exacta ☐ Cambia'), ('M2', 'Voy en camino', '¿Lo entiende sin ayuda? ☐ Sí ☐ No'),
            ('M3', 'Comprobante', '¿Le sirve para sus trámites? ☐ Sí ☐ Le falta algo'), ('M4', 'Hora liberada', '¿La tomaría? ☐ Sí ☐ No ☐ Lo siente invasivo')]
    rows = ''.join(f'<tr><td><b>{a}</b></td><td>{b_}</td><td class="sm">{c}</td><td></td></tr>' for a, b_, c in msgs)
    b = f'''<table class="form head"><tbody><tr><td>Código</td><td></td><td>Perfil</td><td>☐ P1 ☐ P2 ☐ P3 ☐ P4 ☐ P5 ☐ P6</td></tr>
<tr><td>Edad (rango)</td><td>☐ 18–29 ☐ 30–44 ☐ 45–59 ☐ 60–74 ☐ 75+</td><td>¿Atención previa?</td><td>☐ Consulta ☐ Domicilio ☐ Nunca</td></tr></tbody></table>
<table class="form obs"><thead><tr><th>#</th><th>Mensaje</th><th>Registro</th><th>Frase textual / observación</th></tr></thead><tbody>{rows}</tbody></table>
<table class="form"><tbody><tr><td style="width:40%">¿Lo resolvió sin ayuda? (P1)</td><td>☐ Solo ☐ Con letra grande ☐ Con acompañante ☐ No</td></tr>
<tr><td>Privacidad: datos que no querría en la app</td><td></td></tr><tr><td>Quién debería recibir los mensajes</td><td>☐ Paciente ☐ Familiar ☐ Ambos</td></tr></tbody></table>
<h3>Encuesta breve (1 = muy en desacuerdo · 5 = muy de acuerdo)</h3>
<table class="form lik"><thead><tr><th>Afirmación</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr></thead><tbody>
{''.join(f'<tr><td>{s}</td>' + '<td>☐</td>' * 5 + '</tr>' for s in ENC_PAC)}</tbody></table>
<table class="form"><tbody><tr><td style="width:62%">Del 0 al 10, ¿cuánto recomendarías a una kinesióloga que te avise así?</td><td>0 1 2 3 4 5 6 7 8 9 10</td></tr></tbody></table>'''
    return section('k-pautab', 'PAUTA B', 'Formulario imprimible · guion B', 'Pauta y encuesta · pacientes', b)


def sus():
    rows = ''.join(f'<tr><td>{i}</td><td>{s}</td>' + '<td>☐</td>' * 5 + '</tr>' for i, s in enumerate(SUS, 1))
    b = f'''<p class="lead">Escala de usabilidad del sistema (SUS), versión en español. Responder pensando en la app que acabas de usar.</p>
<table class="form lik"><thead><tr><th>#</th><th>Afirmación</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small">1 = muy en desacuerdo · 5 = muy de acuerdo</p>
<div class="box"><div class="t">Cálculo (lo completa el equipo)</div>Ítems impares: respuesta − 1. Ítems pares: 5 − respuesta. Sumar y multiplicar por 2,5 → puntaje de 0 a 100.
Sobre <b>68</b> es usabilidad aceptable; sobre <b>80</b>, buena. Meta del prototipo: <b>≥ 75</b>.
<table class="form" style="margin-top:2mm"><tbody><tr><td>Suma impares</td><td></td><td>Suma pares</td><td></td><td>Puntaje SUS</td><td></td></tr></tbody></table></div>'''
    return section('k-sus', 'SUS', 'Formulario imprimible · guion A', 'Cuestionario de usabilidad (SUS)', b)


def consolidar():
    rows = [[f'<b>{h}</b>', next(x[2] for x in HIP if x[0] == h), '<span class="pend">Pendiente</span>', '', f'<span class="small">✔ {ok}</span><br><span class="small muted">✖ {ko}</span>'] for h, ok, ko in DECISION]
    b = f'''<p class="lead">Al terminar las sesiones, cada hipótesis se resuelve con una regla definida de antemano. Así la iteración v3 no depende de opiniones
sueltas: si se cumple el criterio, se mantiene; si no, ya sabemos qué cambiar.</p>
{table(['#', 'Hipótesis', 'Resultado', 'Evidencia', 'Si se cumple ✔ / si no ✖'], rows, 'tight dec')}
<h3 style="break-before:page">Método de procesamiento</h3>
{table(['Dato', 'Cómo se procesa', 'Dónde queda'], [
        ['Éxito y toques por tarea (pauta A)', 'Tasa de éxito por tarea = S / participantes; promedio de toques y tiempo; frases textuales agrupadas por tema.', 'Tabla de tareas ciclo 3'],
        ['SUS', 'Puntaje 0–100 por participante y promedio (meta ≥ 75).', 'Resultado H1–H3'],
        ['Respuestas a M1–M4 (pauta B)', 'Conteo por opción y por perfil; % que acepta la ventana (H5), entiende (H6), le sirve (H7), la tomaría (H10).', 'Resultado H5–H10'],
        ['Encuesta de pacientes', 'Promedio por afirmación (1–5) y por perfil; recomendación 0–10 (promotores 9–10 menos detractores 0–6).', 'Resultado H6–H8'],
        ['Lista de la contadora', 'Campos faltantes críticos y no críticos.', 'Resultado H9 · backlog'],
        ['Cualidades, debilidades y mejoras', 'Post-its por sesión → agrupación por afinidad → matriz CDM (3.1.2.4) del ciclo con usuarios.', 'CDM ciclo 3'],
        ['Problemas observados', 'Severidad 0–4 (promedio de observadores); ≥ 3 entra a la iteración v3.', 'Backlog priorizado']], 'tight')}
<h3>Fuentes a integrar</h3>
{table(['Fuente', 'Tipo', 'Estado'], [['F0 · Reunión jue 12 nov: retroalimentación de la emprendedora sobre los trabajos revisados (grabación del profesor)', 'Retroalimentación experta general', PEND],
        ['F1 · Sesión K1 Joselyn', 'Usuaria principal', PEND], ['F2 · Sesión K2 Catalina', 'Experta par', PEND],
        ['F3 · Sesiones P1–P6', 'Usuarios secundarios', PEND], ['F4 · Sesión C1 contadora', 'Experto técnico', PEND]], 'tight')}'''
    return section('k-cons2', 'CONSOLIDAR', 'Matriz de consolidación y decisiones', 'Consolidar y decidir', b)


def invitaciones():
    msgs = [('Joselyn (K1)', 'Hola Joselyn 😊 Te cuento que armamos el prototipo de Copiloto Kine con todo lo que conversamos: registra tus atenciones con un toque, te muestra cuánto te queda de verdad y ordena tu ruta de domicilios. ¿Tendrías 45 minutos la próxima semana para probarlo en tu celular? Nos adaptamos a tu horario.'),
            ('Catalina (K2)', 'Hola Cata, ¿cómo estás? Con el equipo convertimos lo que nos contaste del Excel diario en un prototipo. ¿Te animas a probarlo unos 30–40 minutos por videollamada? Nos ayuda mucho tu mirada de kinesióloga.'),
            ('Pacientes (P1–P6)', 'Hola, somos estudiantes de Diseño Digital de INACAP Rancagua. Estamos probando unos mensajes que una kinesióloga le enviaría a sus pacientes (recordatorio, aviso de llegada y comprobante). ¿Nos regalas 15 minutos? No te preguntaremos nada de tu salud.'),
            ('Contadora (C1)', 'Hola, somos estudiantes de INACAP Rancagua. Diseñamos una herramienta para que kinesiólogas a honorarios lleven sus ingresos, costos y retención. ¿Podría revisar 20 minutos el resumen que exporta y decirnos si le sirve para su trabajo?')]
    b = ''.join(f'<div class="wa"><div class="to">{t}</div><div class="bub">{m}</div></div>' for t, m in msgs)
    return section('k-inv', 'INVITACIONES', 'Mensajes listos para copiar', 'Invitaciones', '<p class="lead">Textos breves para WhatsApp. Ajustar el día y la hora antes de enviar.</p>' + b)


CSS = '''<style>
.pfs{display:block}.pfs::after{content:'';display:block;clear:both}
.pf{float:left;width:calc(50% - 1.6mm);margin:0 3.2mm 3mm 0;border:1px solid var(--page-border);border-radius:6px;overflow:hidden;break-inside:avoid;font-size:7.7pt;line-height:1.4}
.pf:nth-child(2n){margin-right:0}
.pf .top{display:flex;align-items:center;gap:2.4mm;background:var(--page-card);border-bottom:1px solid var(--page-border);padding:2mm 2.6mm}
.pf .top b{display:block;font-size:9.2pt;line-height:1.2}.pf .top span{font-size:7pt;color:var(--page-text2)}
.pf .top em{margin-left:auto;font-style:normal;font-family:var(--fm);font-size:6pt;letter-spacing:.08em;text-transform:uppercase;color:var(--page-text2)}
.pf .cd{width:9mm;height:9mm;border-radius:5px;background:#12101E;color:var(--accent);font-family:var(--fd);font-size:13pt;display:flex;align-items:center;justify-content:center;flex:none}
.pf.k .cd{color:#fff;background:var(--accent)}.pf.e .cd{background:var(--h6);color:#fff}
.pf .bd{padding:2mm 2.6mm}.pf .bd p{margin-bottom:1.4mm}
.pf .kv{display:flex;gap:2mm;border-top:.5pt solid var(--page-border);padding:.8mm 0}.pf .kv span{font-family:var(--fm);font-size:5.9pt;letter-spacing:.08em;text-transform:uppercase;color:var(--page-text2);width:16mm;flex:none;padding-top:.3mm}
.shots{display:flex;gap:2mm;margin:3mm 0 4mm}.shots figure{flex:1}.shots img{width:100%;border-radius:4px;border:1px solid var(--page-border);display:block}
.shots figcaption{font-family:var(--fm);font-size:5.8pt;letter-spacing:.06em;text-transform:uppercase;color:var(--page-text2);margin-top:1mm;text-align:center}
table.form td{border:.6pt solid #BDB9D2;height:7.5mm;vertical-align:middle;font-size:7.8pt}
table.form th{border:.6pt solid #BDB9D2}
table.form.head td:nth-child(odd),table.form.sign td:nth-child(odd){font-family:var(--fm);font-size:6.3pt;letter-spacing:.06em;text-transform:uppercase;color:var(--page-text2);background:var(--page-card);width:15%}
table.form.obs td{height:9.5mm;vertical-align:top}table.form.obs td.sm{font-size:7pt;color:var(--page-text2)}
table.form.obs td:nth-child(3){white-space:nowrap}
table.form.obs th:nth-child(6),table.form.obs td:nth-child(6){width:34%}
table.form.lik td:not(:first-child):not(:nth-child(2)),table.form.lik th:not(:first-child):not(:nth-child(2)){text-align:center;width:7%}
table.form.lik td{height:8mm}
table.form tr.tall td{height:20mm}
table.form.sign td{height:12mm}
.lines{border-bottom:.6pt solid #BDB9D2;height:8mm}
.consent{font-size:9pt}.consent li{margin-bottom:1.6mm}
.wa{margin-bottom:4mm;break-inside:avoid}.wa .to{font-family:var(--fm);font-size:6.6pt;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-bottom:1mm}
.wa .bub{background:#E7FFDB;border-radius:0 10px 10px 10px;padding:3mm 4mm;font-size:9pt;max-width:150mm;border:1px solid #CDEFC0}
table.dec td:nth-child(3){width:24mm}table.dec td:nth-child(4){width:18mm}table.dec td:nth-child(5){width:62mm}table.dec td{font-size:7.4pt;padding:2.5px 5px}
code{font-family:var(--fm);font-size:7pt;background:var(--page-card);padding:0 3px;border-radius:2px}
@page{@bottom-left{content:"INACAP Rancagua · UA3 Prototipado y Testeo · Kit de testeo Copiloto Kine"}}
</style>'''

HEAD = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Kit de testeo · Copiloto Kine</title><link rel="stylesheet" href="../ev3/ev3.css">{CSS}</head><body>'

if __name__ == '__main__':
    body = (portada() + uso() + plan() + plan2() + perfiles() + estimulos() + guion_a() + guion_b() + guion_c()
            + consentimiento() + pauta() + pauta_b() + sus() + consolidar() + invitaciones())
    path = os.path.join(HERE, 'Kit_Testeo_Copiloto_Kine.html')
    open(path, 'w', encoding='utf-8').write(HEAD + body + '</body></html>')
    HTML(path, base_url=HERE).write_pdf(os.path.join(HERE, 'Kit_Testeo_Copiloto_Kine.pdf'))
    import pymupdf
    print('ok', pymupdf.open(os.path.join(HERE, 'Kit_Testeo_Copiloto_Kine.pdf')).page_count, 'páginas')
