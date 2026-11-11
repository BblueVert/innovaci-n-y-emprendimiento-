# Contenido del informe EV3 · Unidad 3 Prototipado y testeo · caso Joselyn Toledo / Copiloto Kine.
# Todo hallazgo de los ciclos 1 y 2 proviene de ../ciclo1 y ../ciclo2 (scripts y JSON reproducibles).
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
C1 = json.load(open(os.path.join(HERE, '..', 'ciclo1', 'resultados_ciclo1.json')))
C1V2 = json.load(open(os.path.join(HERE, '..', 'ciclo2', 'resultados_v2_usabilidad.json')))
C2 = json.load(open(os.path.join(HERE, '..', 'ciclo2', 'resultados_ciclo2.json')))

PRODUCTO = 'Copiloto Kine'
DESAFIO = ('¿Cómo podríamos aumentar la visibilidad financiera de kinesiólogas independientes con atención mixta, '
           'conectando su agenda con sus ingresos y costos, para reducir a la mitad el tiempo de registro manual '
           '(de ~1 h a menos de 30 min diarios) en Rancagua durante 2027?')
PDV_EV2 = (f'{PRODUCTO} es el copiloto financiero de la kinesióloga independiente: se conecta a la agenda que ya usa y convierte '
           'cada atención en ganancia real —descontando traslado, materiales, comisión e impuestos— para que sepa cuánto gana, '
           'anticipe los meses bajos y deje de cuadrar Excel de noche.')
PDV_ITER = (f'{PRODUCTO} es el copiloto de la kinesióloga independiente: ordena su ruta de domicilios y convierte cada atención en '
            'ganancia real —con comisión, traslado, materiales e impuestos ya descontados— para que sepa cuánto gana, anticipe los '
            'meses bajos y entregue sus números a la contadora sin pasar nada a Excel.')

V1 = '../prototipo/capturas_v1/'
V2 = '../prototipo/capturas_v2/'

# ---------------------------------------------------------------- SQA (3.1.1.1)
SQA = [
    ('S · Lo que sabemos', [
        'Prototipar es materializar la idea para probarla antes de invertir (UA3 de Innovación y Emprendimiento II).',
        'Un storyboard muestra la experiencia en el tiempo; un mock-up la materializa en forma.',
        'Nuestra propuesta de valor, atributos y requerimientos ya están definidos (EV2).',
        'Como estudiantes de Diseño Digital, prototipamos en Figma y en HTML.']),
    ('Q · Lo que queremos saber', [
        '¿Cómo testear una herramienta financiera sin datos reales de la usuaria?',
        '¿Qué indicadores muestran que el prototipo funciona y no solo que “gusta”?',
        '¿Cómo pasar de un testeo funcional a uno técnico en la iteración?',
        '¿Qué tan distinta es la propuesta frente a lo que ya existe en 2026?']),
    ('A · Lo que aprendimos', [
        'Un recorrido de tareas con indicadores medibles (éxito, toques, contraste) da evidencia más sólida que la opinión.',
        'Testear al interior del equipo es válido para depurar; la validación final necesita a la usuaria.',
        'Cada ciclo debe tener un foco distinto: primero uso y estética; luego exactitud, privacidad y brechas técnicas.',
        'La ruta del día, que no estaba en el foco original, aporta tanto valor como el tablero financiero.']),
]

# ---------------------------------------------------------------- Storyboard v1 (3.1.2.1)
SCENES = [
    ('11:40 p. m. · el Excel de siempre', 'img/06-nudo.jpg', 'wide',
     'Joselyn termina de atender y cuadra ingresos y gastos en Excel. No sabe si el mes va bien.',
     'Situación actual: registro manual, sin proyección (I1, I3).',
     'Necesidad que la propuesta debe resolver: saber cuánto gana sin trabajo nocturno.'),
    ('8:00 a. m. · abre el tablero', V1 + '01_tablero.png', '',
     'Ve su ganancia real del mes, el % de la meta y un semáforo; abajo, la ruta del día.',
     'Tablero con ganancia real y semáforo de meta.', 'Atributo “Legible de un vistazo”.'),
    ('9:45 · termina en la clínica', V1 + '05_ganancia_atencion.png', '',
     'Toca “Atención realizada” y la app muestra cuánto le quedó tras comisión y retención.',
     'Registro de un toque con desglose de la ganancia.', 'Atributo “Automático”: la cita se vuelve ingreso sin digitar.'),
    ('11:30 · sale a domicilios', V1 + '02_ruta_sugerida.png', '',
     'La ruta agrupa Machalí y el centro y le muestra kilómetros, minutos y costo de bencina.',
     'Ruta del día con paradas y ahorro de km.', 'Atributo “Sostenible”: menos km, menos costo y emisiones.'),
    ('12:10 · “voy en camino”', V1 + '03_ruta_aviso.png', '',
     'Con un toque avisa a Carmen que va llegando, sin escribir mientras maneja.',
     'Aviso automático al paciente.', 'Trato 1:1 que Joselyn define como su diferenciador.'),
    ('Domingo · mira lo que viene', V1 + '07_proyeccion.png', '',
     'Ve que enero y febrero vienen bajos y agrega acciones (packs, colchón) a su plan.',
     'Proyección a 3 meses con acciones sugeridas.', 'Atributo “Anticipador”: avisa antes de la curva.'),
]

# ---------------------------------------------------------------- Mock-up v1 (3.1.2.2)
MOCK_V1 = [
    ('Tablero', V1 + '01_tablero.png', 'Ganancia real del mes, meta, semáforo, colchón, ruta en miniatura y alerta de meses bajos.', 'Legible de un vistazo · Anticipador'),
    ('Ruta', V1 + '02_ruta_sugerida.png', 'Mapa con paradas numeradas, km, minutos, costo y botón “Voy en camino”.', 'Sostenible · Cercano'),
    ('Agenda', V1 + '06_agenda.png', 'Citas de clínica y domicilio; un toque registra la atención.', 'Automático'),
    ('Ganancia', V1 + '05_ganancia_atencion.png', 'Desglose: valor, comisión, traslado, materiales y retención.', 'Legible · Automático'),
    ('Proyección', V1 + '07_proyeccion.png', 'Ganancia proyectada a 3 meses y acciones que cierran la brecha.', 'Anticipador'),
    ('Destinos', V1 + '08_destinos.png', 'Separación en ganancia, impuestos y colchón; costos configurados.', 'Sostenible'),
]

# ---------------------------------------------------------------- Ficha ciclo 1 (3.1.2.3)
EQUIPO_ROLES = 'Moderación: Claudia Cifuentes · Ejecución de tareas: Néstor Rivera · Registro: Francisco Ahumada · Consolidación y auditoría técnica: Benjamín Vera Yáñez'
FICHA_C1 = dict(
    objetivo='Evaluar si el prototipo v1 permite a una kinesióloga independiente completar sus tareas diarias de registro, ruta y control financiero sin ayuda, y si su estética es clara, accesible y coherente con la metáfora.',
    filas=[
        ('Verificar que las tareas principales se completan sin ayuda', 'Equipo en rol de usuaria (perfil de Joselyn, UA2)', 'Prototipo v1 en celular (390 px)', 'Recorrido guiado de 11 tareas', 'Mod.: Claudia · Ejec.: Néstor · Reg.: Francisco', '≥ 90 % de tareas completadas; ≤ 3 toques por tarea', '¿Se pudo completar sin ayuda? ¿Cuántos toques?', 'Planilla de tareas (éxito y toques) automatizada', 'Sala INACAP', '30 min'),
        ('Evaluar legibilidad y accesibilidad', 'Auditoría del equipo', 'Prototipo v1, 5 vistas', 'Auditoría WCAG 2.1 AA (axe-core) y medición de botones y letra', 'Benjamín', '0 errores de contraste; botones ≥ 44 px; texto ≥ 12 px', '¿Se lee y se toca bien en el celular?', 'Reporte automático por vista', 'Remoto', '15 min'),
        ('Revisar coherencia estética y de uso con la metáfora', '3 integrantes', 'Prototipo v1', 'Revisión heurística (10 heurísticas de Nielsen)', 'Todo el equipo', 'Sin problemas de severidad ≥ 3', '¿Transmite “tablero y copiloto” sin recargar?', 'Severidad 0–4 y matriz CDM', 'Sala INACAP', '20 min'),
    ])

HEUR = [
    ('H1 Visibilidad del estado', 'Hoja de confirmación y avisos después de cada acción.', 0),
    ('H2 Relación con el mundo real', '“Destinos” no se entiende; “ganancia real” no está definida.', 2),
    ('H3 Control y libertad', 'No se puede deshacer una atención marcada por error.', 3),
    ('H4 Consistencia', 'Dos naranjas distintos en botones y enlaces.', 1),
    ('H5 Prevención de errores', 'Sin opción “no asistió”: una inasistencia sumaría un ingreso falso.', 3),
    ('H6 Reconocer antes que recordar', 'El desglose muestra todos los descuentos al registrar.', 0),
    ('H7 Flexibilidad', 'Los costos (km, comisión, retención) no se pueden ajustar.', 3),
    ('H8 Estética minimalista', 'Tablero equilibrado; la tarjeta del mapa en miniatura tapaba parte del recorrido.', 1),
    ('H9 Recuperarse de errores', 'Sin camino para corregir una cifra mal registrada.', 2),
    ('H10 Ayuda', 'La proyección no explica de dónde salen los números.', 1),
]

CDM_C1 = dict(
    prod_c=['T1 sin tocar nada: la ganancia del mes es visible al abrir.', 'Registrar una atención: 2 toques con confirmación.', 'Desglose completo de la ganancia por atención.', 'Ruta y aviso al paciente con respuesta inmediata.', 'Proyección que reacciona al agregar acciones.'],
    prod_d=['4 de 11 tareas no se pueden completar: deshacer, inasistencia, editar costos y exportar.', '11 textos con contraste insuficiente (blanco sobre naranja: 2,84:1).', '7 botones o enlaces bajo 44 px (enlaces de 19 px).', 'Textos de 10 y 11 px en etiquetas, leyendas y navegación.', 'En “orden original” desaparece el dato de ahorro.'],
    prod_m=['Agregar “Deshacer” y “No asistió”.', 'Costos editables y exportación para la contadora.', 'Naranja accesible #C2410C (5,2:1) para botones.', 'Botones de 44 px y letra mínima de 12 px.', 'Mostrar la diferencia de km en ambos modos y valores en el gráfico.'],
    pdv_c=['“Legible de un vistazo”: meta en % y semáforo sin leer números.', '“Automático”: la cita se convierte en ingreso sin digitar.', '“Anticipador”: la alerta de enero y febrero aparece en el inicio.'],
    pdv_d=['“Automático” se rompe ante un error: no hay forma de corregir.', '“Ganancia real”, el centro de la propuesta, no se explica.', '“Cercano”: el aviso no muestra qué se le envía al paciente.'],
    pdv_m=['Definir “ganancia real” bajo el indicador.', 'Mostrar el texto del mensaje “voy en camino”.', 'Llevar la ruta al centro de la metáfora: es lo más “copiloto” de la app.'],
)

# ---------------------------------------------------------------- Iteración (3.1.3.x)
CAMBIOS = [
    ('Deshacer una atención', 'T4 fallida · H3 severidad 3', 'R6 · R7', '06_agenda.png'),
    ('Estado “No asistió” sin ingreso', 'T10 fallida · H5 severidad 3', 'R1', '06_agenda.png'),
    ('Costos editables (comisión, km, retención)', 'T9 fallida · H7 severidad 3', 'R3 · R8 · R12', '08_mi_plata.png'),
    ('Exportación CSV para la contadora, sin datos clínicos', 'T11 fallida', 'R12 · R13', '08_mi_plata.png'),
    ('Naranja accesible en botones (#C2410C) y verde oscuro en estados', '11 errores de contraste', 'R5', '05_ganancia_atencion.png'),
    ('Botones y enlaces de 44 px o más', '7 objetivos táctiles chicos', 'R5', '02_ruta_sugerida.png'),
    ('Letra mínima de 12 px', 'Textos de 10–11 px', 'R5', '01_tablero.png'),
    ('Definición de “ganancia real” en el tablero', 'H2 severidad 2', 'R5', '01_tablero.png'),
    ('Diferencia de km visible en ambos modos de ruta', 'T6: ahorro oculto', 'R9', '04_ruta_original.png'),
    ('Valores en las barras de la proyección', 'H10 severidad 1', 'R10', '07_proyeccion.png'),
    ('Texto del mensaje “voy en camino” visible', 'Debilidad de propuesta de valor', 'Cercano', '03_ruta_aviso.png'),
    ('“Destinos” pasa a llamarse “Mi plata”', 'H2 severidad 2', 'R5', '08_mi_plata.png'),
]

METAFORA_ITER = dict(
    antes='“Copiloto Kine es como el tablero y el copiloto de un auto de rally.”',
    despues='“Copiloto Kine es como el copiloto de un rally: lee la ruta, canta los tiempos y lleva las cuentas mientras ella maneja.”',
    porque='En el ciclo 1 la ruta del día fue la vista con más valor percibido y la que mejor encarna la idea de “copiloto”, mientras el tablero funcionó mejor en tamaño reducido. La metáfora deja de centrarse en el instrumento (el tablero) y pasa a centrarse en el acompañante que lee la ruta y lleva la libreta.',
    atributos=[
        ('Anticipador', 'en el sentido de que canta la curva antes de llegar: alerta enero y febrero con 7 semanas y propone acciones con su monto.', 'Se mantiene. Ciclo 1: la alerta se entiende; faltaban valores en el gráfico.', ['Ec']),
        ('Claro', 'en el sentido de que se lee al sol y de un vistazo: letra mínima de 12 px, contraste AA y “ganancia real” explicada en una línea.', 'Reemplaza “Legible de un vistazo” e incorpora la accesibilidad medida.', ['So']),
        ('Automático y corregible', 'en el sentido de que la cita se vuelve ingreso con un toque y, si hubo un error o una inasistencia, se corrige con otro.', 'Se amplía. Ciclo 1: “automático” sin corrección generaba registros falsos.', ['So', 'Ec']),
        ('Sostenible', 'en el sentido de que rinde más con menos: 7 km menos por día, colchón para los meses bajos y datos de salud fuera del sistema.', 'Se refuerza con la ruta y la privacidad por diseño.', ['Ec', 'So', 'Am']),
    ])

SCENES_ITER = [
    ('11:40 p. m. · el Excel de siempre', 'img/06-nudo.jpg', 'wide', 'La escena de partida se mantiene: es la situación que el sistema reemplaza.',
     'Se entiende el problema sin explicación.', 'Mostrar el tiempo perdido: ~1 h diaria (Catalina, UA1).'),
    ('8:00 a. m. · abre el tablero', V2 + '01_tablero.png', '', 'Tablero compacto con la definición de “ganancia real” y la ruta en miniatura.',
     'Respuesta a T1 sin tocar nada.', 'Se agregó la definición; letra mínima de 12 px.'),
    ('9:45 · registra o corrige', V2 + '06_agenda.png', '', 'Puede marcar “Atención realizada”, “No asistió” o deshacer.',
     'El registro sigue siendo de un toque.', 'Se agregaron deshacer e inasistencia (T4, T10).'),
    ('11:30 · ruta del día', V2 + '04_ruta_original.png', '', 'Compara la ruta sugerida con su orden habitual y ve los km y la bencina de diferencia.',
     'La ruta es la vista más valorada.', 'La diferencia se muestra en ambos modos (T6).'),
    ('12:10 · “voy en camino”', V2 + '03_ruta_aviso.png', '', 'El aviso muestra el mensaje exacto que recibe el paciente.',
     'Mantiene el trato cercano.', 'Texto del mensaje visible antes de enviar.'),
    ('Fin de mes · “Mi plata”', V2 + '08_mi_plata.png', '', 'Ajusta sus costos y descarga el resumen para la contadora, sin datos clínicos.',
     'Separa ganancia, impuestos y colchón.', 'Costos editables y exportación (T9, T11).'),
]

# ---------------------------------------------------------------- Ficha ciclo 2 (3.1.3.4)
FICHA_C2 = dict(
    objetivo='Verificar técnicamente que el prototipo v2 resuelve con exactitud y confiabilidad las necesidades puntuales de la kinesióloga independiente (ganancia por atención, costos, impuestos, cierre del día, privacidad y uso en terreno) e identificar las brechas técnicas para la implementación.',
    filas=[
        ('Exactitud de los cálculos', 'Equipo técnico', 'Prototipo v2', 'Pruebas automáticas contra una hoja de cálculo de referencia (P1, P2, P5, P11)', 'Benjamín · Néstor', 'Diferencia ≤ $1 en todos los casos', '¿La ganancia mostrada es la correcta?', 'Script de pruebas con resultado por caso', 'Remoto', '20 min'),
        ('Cierre del día y continuidad de los datos', 'Equipo técnico', 'Prototipo v2', 'Simular un día de 5 atenciones, inasistencia y recarga (P3, P4, P7)', 'Néstor', '≤ 12 toques; 0 datos perdidos', '¿Cerrar el día toma segundos y no pierde nada?', 'Conteo de toques y comparación antes/después', 'Remoto', '15 min'),
        ('Privacidad y entrega a la contadora', 'Equipo + asesor financiero (revisión pendiente)', 'Exportación CSV', 'Descargar el resumen y revisar su contenido (P6)', 'Francisco', '0 diagnósticos y 0 nombres completos', '¿La contadora recibe lo que necesita y nada más?', 'Revisión del archivo exportado', 'Remoto', '10 min'),
        ('Uso en terreno', 'Equipo técnico', 'Prototipo v2 en celular', 'Medir peso, carga, ruta y fuentes sin conexión (P8, P9, P10)', 'Benjamín', '< 100 KB; carga < 1,5 s; legible sin fuentes web', '¿Funciona entre domicilios con datos móviles?', 'Métricas del navegador', 'Remoto', '10 min'),
        ('Cobertura de requerimientos', 'Todo el equipo', 'Prototipo v2 + EV2', 'Trazar R1–R13 contra pruebas y tareas', 'Claudia', '≥ 75 % cumplidos', '¿Qué necesidad queda sin resolver?', 'Matriz de trazabilidad', 'Sala INACAP', '20 min'),
    ])

COBERTURA = [
    ('R1', 'Cita confirmada → ingreso proyectado sin digitar', 'Parcial', 'P2 · P7', 'Funciona con la agenda de ejemplo; falta leer la agenda real.'),
    ('R2', 'Integrarse con la agenda que ya usa', 'Simulado', '—', 'Se muestra “Conectado a Google Calendar”; la conexión real es brecha B1.'),
    ('R3', 'Distinguir clínica (70/30) de domicilio', 'Cumple', 'P1 · P5', 'Comisión editable.'),
    ('R4', 'Ganancia neta por atención, semana y mes', 'Parcial', 'P1 · P2', 'Atención, día y mes; la vista semanal no existe.'),
    ('R5', 'Lenguaje no contable y lectura de menos de 1 minuto', 'Cumple', 'T1 · axe', 'Lectura sin tocar nada; 0 errores WCAG AA.'),
    ('R6', 'Cerrar el día en menos de 30 minutos', 'Cumple', 'P4', '11 toques para 5 atenciones.'),
    ('R7', 'Registrar en el momento de la atención', 'Cumple', 'T2 · P3', '2 toques; persiste al reabrir.'),
    ('R8', 'Descontar traslado y materiales por atención', 'Cumple', 'P1 · P5', 'Costo por km editable.'),
    ('R9', 'Agrupar domicilios por sector', 'Cumple*', 'P8', '*Mapa ilustrativo; la optimización real es brecha B4.'),
    ('R10', 'Historial y proyección de 3 a 6 meses', 'Parcial', 'T7', 'Proyección de ejemplo, no calculada desde historial (B3).'),
    ('R11', 'Alertar meses bajos y sugerir acciones', 'Cumple', 'T7', 'Acciones con monto que cierran la brecha.'),
    ('R12', 'Provisionar retención y estimar Operación Renta', 'Cumple', 'P11 · P6', 'Tasa editable (16 % en 2027); la estimación final queda con la contadora.'),
    ('R13', 'Solo datos financieros, nunca ficha clínica', 'Parcial', 'P6', 'La exportación cumple, pero la agenda muestra el motivo de consulta (B6).'),
]

BRECHAS = [
    ('B1', 'Integración real con la agenda', 'Leer citas de Google Calendar o Cal.com con permiso de la usuaria.', 'MVP (UA4)'),
    ('B2', 'Datos solo en el celular', 'Hoy se guardan en el navegador: si cambia de teléfono, pierde el historial. Respaldo cifrado en la nube.', 'MVP (UA4)'),
    ('B3', 'Proyección de ejemplo', 'Calcularla con el historial propio (promedio por mes del año anterior) desde el tercer mes de uso.', 'Fase 2'),
    ('B4', 'Mapa ilustrativo', 'Usar un servicio de mapas para ordenar paradas reales y estimar tiempos.', 'Fase 2'),
    ('B5', 'Aviso simulado', 'Abrir WhatsApp con el mensaje ya escrito (enlace wa.me) sin costo de API.', 'MVP (UA4)'),
    ('B6', 'Motivo de consulta visible', 'Es un dato de salud: ocultarlo por defecto y dejarlo solo en la agenda original.', 'Inmediato'),
    ('B7', 'Sin costos fijos del mes', 'La ganancia mensual no descuenta celular, seguros ni capacitaciones; agregar costos fijos.', 'MVP (UA4)'),
]

CDM_C2 = dict(
    prod_c=['11 de 11 pruebas técnicas aprobadas.', 'Cálculo exacto: diferencia de $0 frente a la referencia en los 5 casos.', 'Cierre de un día de 5 atenciones en 11 toques, sin digitar.', 'Registros persisten al cerrar y reabrir.', '39,3 KB y carga en 24 ms (archivo local); legible sin fuentes web.'],
    prod_d=['La agenda es de ejemplo: no hay integración real (B1).', 'Los datos viven solo en el celular (B2).', 'La proyección no sale del historial (B3).', 'La agenda muestra el motivo de consulta, un dato de salud (B6).'],
    prod_m=['Ocultar el motivo de consulta (inmediato).', 'Integración con Google Calendar y respaldo en la nube para el MVP.', 'Enlace wa.me para el aviso real.', 'Costos fijos mensuales.'],
    pdv_c=['“Automático y corregible” queda verificado (P3, P4, P7).', 'Retención configurable: resiste el alza de la Ley 21.133 (P11).', 'Privacidad por diseño en la exportación (P6).'],
    pdv_d=['“Anticipador” no es creíble sin historial real.', '“Se conecta a la agenda que ya usa” todavía no es cierto en el prototipo.', 'La ganancia del mes omite costos fijos: puede sobrestimar.'],
    pdv_m=['Ajustar la redacción de la propuesta a lo que el MVP cumple.', 'Prometer la proyección “desde tu tercer mes de uso”.', 'Validar las reglas tributarias con el asesor financiero.'],
)

# ---------------------------------------------------------------- Validación con usuarias
VALIDACION = [
    ('Joselyn Toledo', 'Usuaria del caso', 'Presencial, con su celular', 'Tareas T1–T11 + preguntas CDM + metáfora', 'Pendiente'),
    ('Catalina', 'Experta par (kinesióloga)', 'Remota, videollamada o notas de voz', 'Tareas T1, T2, T5, T7, T11 + disposición a pagar', 'Pendiente'),
    ('Asesor financiero', 'Experto técnico', 'Remota', 'Revisión de cálculos, retención y exportación (P1, P6, P11)', 'Pendiente'),
]

# ---------------------------------------------------------------- PESTAL profundizada (3.1.4.1)
PESTAL = [
    ('Político',
     dict(f='Agenda pública de formalización de trabajadores independientes y transformación digital del Estado.', o='Más profesionales formalizados que necesitan ordenar ingresos y tributación.', a='Cambios de política que alteren reglas de cotización o retención.'),
     dict(f='La formalización avanza con el calendario de la Ley 21.133 y con programas públicos de digitalización de pymes (Ministerio de Economía, Sercotec).', o='Postular el proyecto a fondos de digitalización y emprendimiento en la UA4; el testeo muestra un producto concreto y medible.', a='Dependencia de fondos concursables para el desarrollo inicial; plazos de postulación acotados.')),
    ('Económico',
     dict(f='Ingresos variables por estacionalidad; costos de traslado y combustible en atención a domicilio.', o='Valor claro de una herramienta que muestre la ganancia real y proyecte meses bajos.', a='Baja disposición a pagar por software en profesionales con ingresos ajustados.'),
     dict(f='El ciclo 1 mostró que el costo de traslado es visible y configurable ($180/km); el ciclo 2, que cambia la ganancia de cada domicilio en $160 por cada $20 de alza por km.', o='Las acciones de la proyección (packs, grupo, colchón) suman $570.000 para cubrir enero y febrero: la herramienta genera ingreso, no solo lo registra.', a='Alzas de combustible reducen la ganancia por domicilio; el precio de la suscripción debe mantenerse bajo $25.000 (rango del mercado, UA1).')),
    ('Social',
     dict(f='Envejecimiento de la población y mayor demanda de rehabilitación y atención domiciliaria.', o='Crecimiento del segmento de kinesiología particular y servicios para adultos mayores.', a='Formación universitaria sin contenidos de gestión financiera.'),
     dict(f='La atención a domicilio de adultos mayores es parte de la agenda tipo del prototipo; el aviso “voy en camino” responde a un paciente que espera en casa.', o='El trato 1:1 se protege: la app libera tiempo administrativo y comunica la llegada sin que Joselyn escriba mientras maneja.', a='Brecha digital: usuarias poco habituadas a apps; el ciclo 1 exigió letra mínima de 12 px y contraste AA.')),
    ('Tecnológico',
     dict(f='Adopción masiva de WhatsApp, agendas online (Cal.com, AgendaPro) y boleta de honorarios electrónica del SII.', o='Integrar herramientas que el profesional ya usa en vez de reemplazarlas.', a='Mercado con muchas soluciones genéricas; riesgo de ser “una app más”.'),
     dict(f='El prototipo funciona en el navegador del celular (39 KB) y sin fuentes web; las integraciones reales (agenda, mapas, WhatsApp) son brechas B1, B4 y B5.', o='Enlaces wa.me y APIs de calendario permiten integrar sin costo de licencia en el MVP.', a='Datos guardados solo en el dispositivo (B2): riesgo de pérdida al cambiar de celular.')),
    ('Ambiental',
     dict(f='Traslados en vehículo propio entre domicilios; registros en papel.', o='Optimizar rutas y agrupar atenciones reduce kilómetros y emisiones.', a='Aumento de costos de combustible.'),
     dict(f='La ruta sugerida recorre 7 km menos que el orden original en el día de ejemplo (20 vs. 27 km, −26 %).', o='Con 20 días de domicilios al mes son ~140 km menos: cerca de 10 litros de bencina y unos 23 kg de CO2 (estimación del equipo con 14 km/l y 2,3 kg CO2/l).', a='El ahorro depende de que la usuaria pueda reordenar citas; algunos pacientes tienen horario fijo.')),
    ('Legal',
     dict(f='Ley 21.133 (retención gradual hasta 17 % en 2028), Ley 20.584 sobre ficha clínica y Ley 21.719 de protección de datos (vigencia desde diciembre de 2026).', o='Calcular y provisionar automáticamente la retención y la Operación Renta.', a='Exigencias de resguardo de datos de salud para cualquier sistema que los almacene.'),
     dict(f='La retención 2026 es 15,25 % y sube a 16 % en 2027; la Ley 21.719 rige desde el 1 de diciembre de 2026, con los datos de salud como datos sensibles.', o='Tasa de retención configurable (P11) y exportación sin datos clínicos (P6) como ventaja de cumplimiento.', a='La agenda muestra el motivo de consulta (B6): debe ocultarse antes de usar datos reales.')),
]

# ---------------------------------------------------------------- Estado del arte (3.1.4)
ARTE_VARS = ['Agenda online', 'Ganancia neta por atención', 'Costos de domicilio', 'Retención / impuestos', 'Ruta de domicilios', 'Proyección', 'Foco independiente']
ARTE = [
    ('AgendaPro', [2, 1, 0, 0, 0, 0, 1]), ('Encuadrado', [2, 1, 0, 1, 0, 0, 2]), ('Reservo', [2, 1, 0, 0, 0, 0, 1]),
    ('Medilink', [2, 1, 0, 1, 0, 0, 0]), ('Cal.com', [2, 0, 0, 0, 0, 0, 2]), ('Cliniko', [2, 1, 0, 0, 0, 0, 1]),
    ('Jane App', [2, 1, 0, 0, 0, 0, 1]), ('Nubox', [0, 1, 1, 2, 0, 0, 0]),
    (f'{PRODUCTO} (v2)', [1, 2, 2, 2, 1, 1, 2]),
]
TENDENCIAS = [
    ('Finanzas embebidas en software vertical', 'Las herramientas de gestión incorporan cobros, impuestos y reportes dentro del mismo flujo de trabajo.', 'La ganancia, la retención y el colchón se calculan al registrar la atención, no en otra app.'),
    ('Herramientas para profesionales independientes', 'Crece el software pensado para una persona que trabaja sola, no para centros.', 'Diseñado para una kinesióloga con atención mixta; Cal.com y Encuadrado confirman la tendencia.'),
    ('Atención domiciliaria y envejecimiento', 'La demanda de rehabilitación en casa aumenta con la población mayor.', 'La ruta del día y el aviso “voy en camino” se volvieron centrales tras el ciclo 1.'),
    ('Automatización y asistencia con IA', 'Las apps reducen la digitación: el dato se captura en el momento en que ocurre.', 'Registro de un toque; la siguiente etapa es leer la agenda real y proyectar desde el historial.'),
    ('Privacidad por diseño en salud', 'Normas como la Ley 21.719 exigen minimizar y proteger los datos sensibles.', 'Exportación sin diagnósticos (P6); el motivo de consulta se ocultará (B6).'),
    ('Accesibilidad e inclusión', 'Las pautas WCAG 2.1/2.2 son hoy el estándar mínimo de calidad en productos digitales.', 'v2 sin errores WCAG AA, botones de 44 px y letra mínima de 12 px.'),
]
PERTINENCIA = [
    ('Problema de origen', 'Joselyn no sabe cuánto gana y cuadra Excel de noche (~1 h diaria, I1–I3).', 'Ganancia real al instante y cierre del día en 11 toques (P4).'),
    ('Estado del arte', 'Ningún antecedente cruza agenda, costos por atención y retención chilena.', f'{PRODUCTO} cubre esas tres variables y agrega la ruta (matriz de estado del arte).'),
    ('Tendencias', 'Finanzas embebidas, herramientas para independientes, privacidad y accesibilidad.', 'La v2 responde a las seis tendencias identificadas.'),
    ('Evidencia de testeo', 'Ciclo 1: 7/11 tareas, 11 errores de contraste. Ciclo 2: brechas técnicas acotadas.', 'v2: 11/11 tareas, 0 errores WCAG AA, 11/11 pruebas técnicas.'),
    ('Sostenibilidad', 'Ingresos estacionales, desgaste nocturno y kilómetros innecesarios.', 'Colchón y acciones (+$570.000), cero trabajo nocturno, −7 km por día.'),
]

# ---------------------------------------------------------------- Gestión (bitácora)
GANTT_W = ['S11', 'S12', 'S13', 'S14']
GANTT = [
    ('SQA diagnóstica (en clase)', {'S11': 'on'}), ('Storyboard y mock-up v1 con propuesta de valor', {'S11': 'on'}),
    ('Ficha de testeo y ciclo 1 (funcional y estético)', {'S11': 'mid', 'S12': 'on'}), ('Matriz CDM del ciclo 1', {'S12': 'on'}),
    ('Iteración: metáfora, storyboard y mock-up v2', {'S12': 'on', 'S13': 'mid'}), ('Ficha de testeo de la iteración y ciclo 2 (técnico)', {'S13': 'on'}),
    ('PESTAL profundizada y estado del arte', {'S13': 'on'}), ('Validación con Joselyn, Catalina y asesor', {'S13': 'mid', 'S14': 'on'}),
    ('Bitácora (registro semanal)', {'S11': 'mid', 'S12': 'mid', 'S13': 'hito'}), ('Informe EV3 y entrega', {'S14': 'hito'}),
]
