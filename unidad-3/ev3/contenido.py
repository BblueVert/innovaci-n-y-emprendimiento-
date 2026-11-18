# Contenido del informe EV3 · Unidad 3 Prototipado y testeo · caso Josselyn Toledo / Copiloto Kine.
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
SB = 'img/storyboard/'
SCENES = [  # versión actual · visual y funcional (prototipo v1)
    ('23:10 · el Excel de noche', SB + 'v1-01.jpg', 'wide',
     'Después de atender, Josselyn cuadra ingresos y gastos. Le toma cerca de una hora y no sabe si el mes va bien.',
     'Situación actual: registro manual, sin proyección (UA1).', 'Necesidad: saber cuánto gana sin trabajo nocturno.'),
    ('9:45 · entre pacientes, en la clínica', SB + 'v1-02.jpg', 'wide',
     'Abre el tablero: ganancia real del mes, porcentaje de la meta y semáforo, sin tocar nada.',
     'Tablero con ganancia real y semáforo.', 'Atributo “Legible de un vistazo”.'),
    ('8:00 · la agenda llega sola', SB + 'v1-03.jpg', 'wide',
     'Cada cita del día aparece como ingreso proyectado, etiquetada como clínica o domicilio.',
     'Agenda conectada (simulada en v1).', 'Atributo “Automático”: no se vuelve a digitar.'),
    ('12:30 · “atención realizada”', SB + 'v1-04.jpg', 'wide',
     'Al despedirse de don Luis confirma la atención con un toque y ve su ganancia neta.',
     'Registro de un toque con desglose.', 'Ganancia real: traslado, materiales y retención ya descontados.'),
    ('13:10 · ruta y “voy en camino”', SB + 'v1-05.jpg', 'wide',
     'La ruta ordena los domicilios y con un toque avisa al siguiente paciente que va llegando.',
     'Ruta del día y aviso al paciente.', 'Atributos “Sostenible” y “Cercano”.'),
    ('Domingo · lo que viene', SB + 'v1-06.jpg', 'wide',
     'Ve que febrero viene bajo, pero todavía arma a mano lo que le entrega a la contadora.',
     'Proyección a 3 meses.', '“Anticipador”; queda abierto el cierre con la contadora.'),
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
        ('Verificar que las tareas principales se completan sin ayuda', 'Equipo en rol de usuaria (perfil de Josselyn, UA2)', 'Prototipo v1 en celular (390 px)', 'Recorrido guiado de 11 tareas', 'Mod.: Claudia · Ejec.: Néstor · Reg.: Francisco', '≥ 90 % de tareas completadas; ≤ 3 toques por tarea', '¿Se pudo completar sin ayuda? ¿Cuántos toques?', 'Planilla de tareas (éxito y toques) automatizada', 'Sala INACAP', '30 min'),
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

SCENES_ITER = [  # versión actualizada · técnica (prototipo v2 + propuesta v3)
    ('8:30 · martes = Machalí', SB + 'v2-01.jpg', 'wide', 'El copiloto agrupa los domicilios por sector, ordena la ruta y muestra km, minutos y la bencinera más barata del camino.',
     'La ruta fue la vista más valorada (ciclo 1).', 'Diferencia de km en ambos modos; v3: precios de bencina en línea.'),
    ('10:15 · registra o corrige', SB + 'v2-02.jpg', 'wide', 'Cierra la atención con don Luis en un toque. Si se equivocó o el paciente no estuvo, lo corrige con otro.',
     'Registro de un toque y cálculo exacto (P1).', 'Deshacer y “No asistió” (T4, T10).'),
    ('12:40 · “voy en camino”', SB + 'v2-03.jpg', 'wide', 'El aviso muestra el mensaje exacto que recibe el paciente; si alguien cancela, el cupo se ofrece a la lista.',
     'Trato cercano sin escribir mientras maneja.', 'Mensaje visible (v2) y hora liberada (vista paciente).'),
    ('20:40 · día cerrado', SB + 'v2-04.jpg', 'wide', 'Cierra un día de cinco atenciones en 11 toques y llega a tiempo a cenar con su familia.',
     'Sin trabajo nocturno (P4).', 'Persistencia de datos (P3); v3: respaldo en la nube.'),
    ('Fin de mes · “Mi plata”', SB + 'v2-05.jpg', 'wide', 'Ajusta comisión, costo por km y retención, y envía a la contadora el resumen sin datos clínicos.',
     'Separa ganancia, impuestos y colchón.', 'Costos editables y exportación (T9, T11, P5, P6).'),
    ('Seis semanas antes · febrero', SB + 'v2-06.jpg', 'wide', 'El tablero avisa que febrero viene bajo y propone packs y colchón con su monto; la curva se aplana.',
     'Acciones con monto (T7).', 'Valores en el gráfico; v3: proyección desde su historial.'),
]

# Recorrido del paciente (storyboard EV2) ↔ mensajes de la vista paciente
SB_PACIENTE = [
    (SB + 'p-01.jpg', 'Camila reserva en un minuto', 'Agenda en línea que Josselyn ya usa', '—'),
    (SB + 'p-02.jpg', 'Don Luis confirma el recordatorio', 'M1 · ventana de llegada de 30 min', 'H5 · H8'),
    (SB + 'p-03.jpg', '“Voy en camino”', 'M2 · aviso con tiempo estimado', 'H6'),
    (SB + 'p-04.jpg', 'Paga y recibe el comprobante', 'M3 · comprobante sin diagnóstico', 'H7'),
    (SB + 'p-05.jpg', 'Camila toma un cupo liberado', 'M5 · hora liberada a precio preferente', 'H10'),
    (SB + 'p-06.jpg', 'Seguimiento después del alta', 'Fase 2 · pack de mantención o clase grupal (M4)', 'H11'),
]

# Iteración de los instrumentos: versión actual (visual-funcional) → versión actualizada (técnica)
ITER_DOCS = [
    ('3.1.2.1 → 3.1.3.2', 'Storyboard', 'Un día de Josselyn con la promesa de la EV2: tablero, registro, ruta y proyección.', 'Mismo día con lo corregido y lo técnico: ruta por sector con bencina, corrección, cierre a las 20:40 y proyección con acciones.', 'Ruta como vista más valorada; “automático” sin corrección'),
    ('3.1.2.2 → 3.1.3.3', 'Mock-up', 'Prototipo v1: 5 vistas, foco en que se vea y se use bien.', 'Prototipo v2: 12 cambios (accesibilidad, deshacer, inasistencia, costos editables, exportación) + vista paciente.', '7/11 tareas; 11 errores de contraste'),
    ('3.1.2.3 → 3.1.3.4', 'Ficha de testeo', 'Ciclo 1 visual y funcional: tareas, WCAG AA, heurísticas.', 'Ciclo 2 técnico: exactitud de cálculos, persistencia, privacidad, rendimiento y cobertura R1–R13.', 'Lo funcional quedó resuelto en v2'),
    ('3.1.2.4 (×2)', 'Matriz CDM', 'Ciclo 1: uso, estética y promesa de valor.', 'Ciclo 2: brechas técnicas e integraciones para el MVP.', 'Cambia el tipo de debilidad: de uso a integración'),
    ('2.1.4.3 → 3.1.3.1', 'Metáfora y atributos', 'Tablero y copiloto de rally; “Legible de un vistazo”, “Automático”.', 'Copiloto que lee la ruta y lleva las cuentas; “Claro”, “Automático y corregible”.', 'Ruta más valorada; accesibilidad medida'),
    ('2.1.4.4 → 3.1.5', 'Propuesta de valor', '“Se conecta a la agenda que ya usa… deja de cuadrar Excel de noche”.', '“Ordena su ruta… entrega sus números a la contadora sin pasar nada a Excel”.', 'Promesa ajustada a lo verificado (P6, B1)'),
    ('1.1.3.1 → 3.1.4.1', 'Matriz PESTAL', 'Contexto general de la UA1.', 'Cada factor con evidencia del prototipo y oportunidades técnicas (APIs públicas de combustible y mapas).', 'Testeo técnico y brechas B1–B7'),
]

# ---------------------------------------------------------------- Propuesta técnica (versión 3 · MVP)
INTEGRACIONES = [
    ('Precios de combustible', 'API pública “Bencina en Línea” de la Comisión Nacional de Energía (registro gratuito)', 'Costo por km calculado con el precio real de la bencinera más cercana y aviso de la más barata en la ruta del día.', 'Ec · Am', 'MVP'),
    ('Optimización de ruta', 'Servicio de rutas (Google Routes u OpenRouteService) con optimización de paradas y ventanas horarias', 'Orden de domicilios según tráfico real, respetando la ventana de 30 min que acepta cada paciente (H5).', 'Am · Ec', 'MVP'),
    ('Agenda', 'AgendaPro (la que usa Josselyn, retroalimentación 12/11) y, como alternativa, Google Calendar o Cal.com', 'Cada cita se convierte sola en ingreso proyectado (resuelve R1, R2 y B1).', 'So', 'MVP'),
    ('Mensajería', 'Enlace wa.me (sin costo) y luego WhatsApp Business API', 'Recordatorio, “voy en camino”, comprobante y hora liberada (M1–M4).', 'So', 'MVP → fase 2'),
    ('Base de datos', 'Base de datos en la nube con cifrado y respaldo (p. ej. Supabase/PostgreSQL) + modo sin conexión', 'Historial seguro entre dispositivos (B2) y proyección desde el historial propio (B3).', 'So', 'MVP'),
    ('Pagos y boleta', 'Link de pago (Mercado Pago) y registro del folio de la boleta de honorarios del SII', 'El pago registra el ingreso solo; el folio cuadra con lo que ve la contadora.', 'Ec', 'Fase 2'),
]

FUNCIONES = [
    ('Agregar', 'Ganancia por hora por canal (clínica, domicilio, piscina, grupal) y modo clínica por factura mensual', 'Pedido directo de la clienta el 12/11 (RF4, RF5).'),
    ('Agregar', 'Clases grupales para adultos mayores (cupos y cobro por persona)', 'Acción concreta para meses bajos (RF10).'),
    ('Agregar', 'Bencinera más barata en la ruta y costo por km automático', 'Hoy el costo por km es fijo ($180) y lo ajusta la usuaria (T9).'),
    ('Agregar', 'Ventana horaria por paciente y marca “hora fija”', 'La ruta solo es real si el paciente la acepta (H5); los de hora fija no se mueven.'),
    ('Agregar', 'Llegada detectada por ubicación (geocerca) para sugerir “atención realizada”', 'Reduce aún más el registro manual, siempre con confirmación de la usuaria.'),
    ('Agregar', 'Costos fijos del mes (celular, seguros, cursos)', 'La ganancia mensual hoy los omite (B7).'),
    ('Agregar', 'Respaldo en la nube y modo sin conexión', 'Datos solo en el celular (B2); señal irregular entre domicilios.'),
    ('Mantener', 'Registro de un toque, deshacer e inasistencia', 'Validado en ciclos 1 y 2 (T2, T4, T10, P4).'),
    ('Mantener', 'Exportación para la contadora sin datos clínicos', 'Verificado (P6) y alineado con la Ley 21.719.'),
    ('Quitar', 'Motivo de consulta visible en la agenda', 'Es un dato de salud (B6): queda solo en la agenda original.'),
    ('Quitar', 'Mapa ilustrativo y proyección de ejemplo', 'Se reemplazan por la ruta real y la proyección desde el historial (B3, B4).'),
    ('Quitar', 'Nombres completos de pacientes en pantallas compartidas', 'Iniciales por defecto; privacidad por diseño.'),
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
    ('Josselyn Toledo', 'Usuaria del caso', 'Presencial, con su celular', 'Tareas T1–T11 + preguntas CDM + metáfora', 'Pendiente'),
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
     dict(f='La atención a domicilio de adultos mayores es parte de la agenda tipo del prototipo; el aviso “voy en camino” responde a un paciente que espera en casa.', o='El trato 1:1 se protege: la app libera tiempo administrativo y comunica la llegada sin que Josselyn escriba mientras maneja.', a='Brecha digital: usuarias poco habituadas a apps; el ciclo 1 exigió letra mínima de 12 px y contraste AA.')),
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
    ('Problema de origen', 'Josselyn no sabe cuánto gana y cuadra Excel de noche (~1 h diaria, I1–I3).', 'Ganancia real al instante y cierre del día en 11 toques (P4).'),
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
    ('PESTAL profundizada y estado del arte', {'S13': 'on'}), ('Validación con Josselyn, Catalina y asesor', {'S13': 'mid', 'S14': 'on'}),
    ('Bitácora (registro semanal)', {'S11': 'mid', 'S12': 'mid', 'S13': 'hito'}), ('Informe EV3 y entrega', {'S14': 'hito'}),
]

# ---------------------------------------------------------------- Retroalimentación 12/11 (Sercotec + clienta + docentes)
# Fuente: ../retroalimentacion/Transcripcion_reunion_2026-11-12.md (minutos entre corchetes)
RETRO_CONTEXTO = ('Reunión de Meet del 12 de noviembre (08:33, 40 min) con Mabel Aceituno Romero (encargada de Sercotec), la clienta Josselyn Toledo, '
                  'el profesor a cargo Ariel O’Nell (INACAP) y Ana Luisa Aguilera, docente INACAP de otra sección que también trabajó el caso. Se revisaron cuatro propuestas: una herramienta de gestión integral materializada en Excel, '
                  'una planilla Excel de gestión, un modelo de programas grupales y Copiloto Kine (nuestro equipo, carpeta “Grupo2”), leída entre el minuto 30:49 y el 35:29.')
RETRO_HALLAZGOS = [
    ('RF1', 'No conoce una herramienta que haga esto', '“No. Así como solamente por pauta, por agenda, por horario, pero nada más que eso.”', '12:22', 'Diferenciación confirmada: las apps que usa solo agendan.'),
    ('RF2', 'Ya registra todo cada noche en el teléfono', '“Cada noche anoto todo… la ganancia, lo que gasto en bencina durante el día… cuántas sesiones hice y cuánto gané en cada sesión.”', '36:25', 'La app debe reemplazar ese hábito nocturno, no crear uno nuevo.'),
    ('RF3', 'Usa dos agendas: AgendaPro y una agenda médica', '“Tengo dos tipos de agenda, la AgendaPro y la [agenda médica digital], tanto para personal y en clínica.”', '36:25', 'Integrar AgendaPro antes que Google Calendar.'),
    ('RF4', 'En la clínica factura un monto mensual', '“En clínica ya dejo como un monto fijo porque al final yo hago la factura y veo el monto total del mes.”', '36:25', 'Modo clínica por factura mensual, además del cálculo por atención.'),
    ('RF5', 'Quiere saber qué canal es más rentable', '“Si sale más rentable en clínica o en domicilio… en clínica puedo atender dos, tres pacientes por hora… a domicilio atiendo solo una persona, con el viaje incluido.”', '19:21', 'Ganancia por hora por canal como métrica central.'),
    ('RF6', 'El traslado le cuesta tiempo, no solo bencina', '“Agua Buena… queda para la precordillera… es muy malo el camino… me demoro como 25, 30 minutos.”', '20:47', 'Incluir el tiempo de viaje como costo (hora profesional) y una tarifa por tramo.'),
    ('RF7', 'Hace más que kinesiología', '“Trabajo tanto en piscina. Yo soy psicomotricista acuática… los entrenamientos personalizados que hago en mi propio [gimnasio].”', '05:56 · 23:27', 'Varios servicios y lugares con costos distintos: clínica, domicilio, piscina, gimnasio.'),
    ('RF8', 'Su territorio es San Fernando y alrededores', 'San Fernando, Agua Buena, Las Cabras (tres pacientes en clínica) y la piscina temperada camino a Roma.', '07:59 · 20:47 · 28:17', 'Ajustar rutas y ejemplos a su territorio real (no solo Rancagua–Machalí).'),
    ('RF9', 'En la región se valora poco lo especializado', '“La gente no sabe lo que es, ni sabe lo que vale realmente… encuentra que es caro.”', '06:42', 'Comunicar el valor del servicio (comprobante, explicación) y cuidar el precio de la app.'),
    ('RF10', 'Grupal sí, pero preventivo', 'Lo terapéutico es individual; ve “fantástico” hacer clases grupales para adultos mayores en Las Cabras, que “andan buscando cositas para hacer en grupo”.', '23:27 · 28:17', 'Módulo de clases grupales (cupos, asistencia, cobro por persona) como acción de la proyección.'),
    ('RF11', 'Sus clientes manejan sus tiempos', '“La mayoría son empresarios, independientes, manejan sus tiempos.”', '05:56', 'Indicio favorable para la ventana de llegada de 30 min (H5); se valida igual con pacientes.'),
    ('RF12', 'Interés directo en la app', '“Me encantaría conocerla.” · “Felicitaciones a sus alumnos.”', '13:31 · 38:35', 'Disposición a probar: base para la sesión con la usuaria.'),
]
RETRO_DOCENTES = [
    ('Ariel O’Nell (profesor a cargo)', 'Bajo o cero costo, usable en teléfono, tablet y computador; todo parametrizado: ella ingresa datos y la app entrega el cálculo, con resúmenes semanales y mensuales que sirvan a la parte contable.', '10:47'),
    ('Ariel O’Nell (profesor a cargo)', 'Costo oculto: la hora hombre del traslado. Permite definir el valor exacto de su hora profesional.', '19:45'),
    ('Ariel O’Nell (profesor a cargo)', 'Las propuestas no son excluyentes: puede combinar una app, una planilla y un modelo grupal.', '17:33'),
    ('Mabel Aceituno (encargada Sercotec)', 'Que los estudiantes estimen cuánto costaría la solución.', '12:30'),
    ('Mabel Aceituno (encargada Sercotec)', 'Analizar por tipo de cliente y lugar (particular vs. clínica, por semana y mes) para decidir dónde enfocarse.', '18:23'),
    ('Mabel Aceituno (encargada Sercotec)', 'No toda cita agendada se concreta; la bencina sube: conviene partir con valores fijos estimados.', '15:12 · 33:31'),
]
RETRO_PATRONES = [
    ('Rentabilidad por canal y por hora', 'RF5 · RF6 · RF7 · Ariel 19:45', 'La pregunta de fondo no es “cuánto gané” sino “qué me conviene”: clínica, domicilio, piscina o grupo.'),
    ('El hábito ya existe', 'RF2 · RF3 · RF4', 'Josselyn ya registra cada noche y usa AgendaPro: la app gana si se monta sobre eso y lo hace en segundos.'),
    ('El territorio define el costo', 'RF6 · RF8 · Mabel 33:31', 'Caminos rurales y de precordillera: el traslado pesa más en tiempo que en bencina.'),
    ('Diversificar ingresos', 'RF7 · RF10 · Ariel 26:57', 'Clases grupales preventivas para adultos mayores son la acción más concreta para los meses bajos.'),
    ('Bajo costo y complementariedad', 'Ariel 10:47 · 17:33 · Mabel 12:30', 'La solución debe ser barata, multi-dispositivo y exportable a Excel para convivir con otras propuestas.'),
]
RETRO_CAMBIOS = [
    ('Integración con AgendaPro (o su exportación) y la agenda de la clínica; Google Calendar queda como alternativa', 'RF3', 'Integración · MVP'),
    ('“Ganancia por hora” por canal: clínica, domicilio, piscina, gimnasio y grupal', 'RF5 · RF7', 'Tablero · MVP'),
    ('Tiempo de traslado como costo (valor de la hora profesional) y tarifa sugerida por tramo', 'RF6 · Ariel', 'Ruta · MVP'),
    ('Modo clínica por factura mensual (monto fijo del mes) además del cálculo por atención', 'RF4', 'Registro · MVP'),
    ('Servicios configurables con su propio costo (piscina, gimnasio, domicilio, clínica)', 'RF7', 'Ajustes · MVP'),
    ('Módulo de clases grupales: cupos, asistencia y cobro por persona; aparece como acción en la proyección', 'RF10', 'Proyección · fase 2'),
    ('Reportes semanales y mensuales por tipo de cliente y lugar, exportables a Excel o Google Sheets', 'Mabel · Ariel', 'Reportes · MVP'),
    ('Ejemplos y rutas en su territorio: San Fernando, Agua Buena, Las Cabras', 'RF8', 'Prototipo v3'),
    ('Costo estimado de la solución visible en la propuesta (MVP con herramientas de bajo costo)', 'Mabel 12:30', 'Propuesta'),
]
RETRO_DOCENTES.append(('Ana Luisa Aguilera (docente INACAP)', 'Las propuestas de su sección también apuntan al agendamiento y la organización interna; la retroalimentación servirá para mejorarlas.', '39:29'))

# Hallazgos generales de toda la conversación y de las otras propuestas revisadas
RETRO_GENERALES = [
    ('Todas las secciones vieron el mismo problema', '“Las propuestas pueden ser muy similares porque todos identificaron el tema de los ingresos.” (Mabel, 38:45) · “Es el tema del agendamiento y la organización interna.” (Ana, 39:29)', 'La diferenciación no está en el problema sino en cómo se resuelve: ruta, tiempo de traslado, retención, proyección y vista paciente.'),
    ('La clienta elegirá comparando o combinando', '“Presentaciones estandarizadas… para comparar las propuestas.” (Ariel, 37:45) · “No son excluyentes… una batería de apoyo.” (Ariel, 17:33)', 'Mostrar con claridad qué hace nuestra propuesta que las otras no, y que puede convivir con ellas (exportar a Excel).'),
    ('Hay tres modelos de apoyo en juego', 'App de gestión, planilla Excel dinámica y modelo de negocio grupal (Ariel, 29:43); en los documentos, dos de las cuatro propuestas se resuelven en Excel.', 'Copiloto Kine puede integrar los tres: app + exportación a Excel + módulo grupal.'),
    ('El costo es una pregunta obligada', '“Que se pueda identificar más o menos cuánto saldría.” (Mabel, 12:30) · “De muy bajo costo… plataformas liberadas.” (Ariel, 12:52)', 'Incluir un costeo del MVP y del uso mensual en la entrega final.'),
    ('Lo manual no escala', '“Al ser una planilla Excel hay que alimentarla… no va a tener la información sola.” (Mabel, 15:12)', 'La automatización (agenda, ruta, cálculo) es la ventaja frente al Excel.'),
    ('Cada propuesta refleja la formación de su equipo', 'Alumnos contables proponen desde lo contable; administración, desde la gestión. (Ariel, 02:20)', 'Nuestro aporte como Diseño Digital es la experiencia: claridad, accesibilidad, prototipo navegable y la mirada del paciente.'),
    ('La clienta está abierta y comprometida', '“Me encantaría conocerla.” (13:31) · “Muy buenas las propuestas… hay que dar una muy buena resolución.” (39:07)', 'Hay disposición para la sesión de testeo con ella.'),
]
RETRO_OTRAS = [  # descripción tomada de los documentos compartidos en pantalla y de la lectura de Mabel
    ('Herramienta digital de gestión integral (Excel)', '09:00–13:37',
     'Storyboard iterado con la persona “Priscilla”: organizar pacientes y atenciones, centralizar finanzas, ver resultados y planificar captación. Se materializa en una plantilla Excel reutilizable (hojas de pacientes, agenda, ingresos y gastos; cálculos automáticos; tablero con indicadores y gráficos). Mejoras previstas: guía de uso, respaldo, alertas, resúmenes mensuales y metas.',
     'Ariel la presenta como una app simple, de bajo o cero costo, en teléfono, tablet o computador, que considere el traslado según la distancia del paciente. Mabel pide estimar su costo. Josselyn: no conoce algo así; “me encantaría conocerla”.',
     'Es la más cercana a la nuestra, pero depende de que ella digite todo. Nos diferencian la agenda conectada, la ruta, el tiempo de traslado, la retención y la proyección.'),
    ('Planilla Excel de gestión kinesiológica', '14:07–17:33',
     'Problema: organizar atenciones y controlar ingresos y gastos sin una herramienta centralizada. Prototipo: hojas de atenciones y movimientos, listas desplegables (tipo, modalidad, estado, medio de pago), panel mensual y anual; separa ingresos dependientes e independientes. Costos: elaborarla, aprender a usarla, tener computador y Excel, mantenerla al día.',
     'Mabel: hay que alimentarla a mano, pero permite analizar por tipo de cliente. Josselyn: “más similar, pero más detallado” que lo que ya hace. Ariel: complementaria a una app.',
     'Tomamos el panel mensual y anual, el estado de la atención y la exportación a Excel; superamos la carga manual.'),
    ('Programas grupales “Movimiento y bienestar todo el año”', '21:41–29:43',
     'Modelo de negocio en 6 escenas: la estacionalidad corta la continuidad e ingresos; escuchar a niños, adultos, mayores y trabajadores; programa anual adaptado por edad; convenios con empresas y municipalidades; talleres de movimiento, recreación y pausas activas; evaluar asistencia, costos y permanencia.',
     'Josselyn: lo terapéutico (y la psicomotricidad acuática) es individual; lo grupal preventivo para adultos mayores en Las Cabras sí le interesa. Ariel: ejemplo de gimnasia acuática grupal muy rentable en Rancagua.',
     'Incorporamos clases grupales como acción de la proyección y un módulo de cupos y cobro por persona.'),
    ('Copiloto Kine (nuestro equipo, carpeta “Grupo2”)', '30:49–35:29',
     'App web: cada cita de la agenda se vuelve ingreso; ganancia neta con comisión, traslado y materiales; tablero con semáforo; v1 (atención, tablero, proyección) y v2 (retención y colchón, domicilios por sector, horas libres, cierre antes de las 21 h); $20–25 mil/mes de referencia.',
     'Mabel lo explica con un domicilio en Rengo y valores estimados de bencina. Josselyn: “eso hago yo igual en el teléfono… simplemente no tengo esa aplicación”.',
     'Valida el núcleo; corregimos AgendaPro, factura mensual de clínica y ganancia por hora por canal.'),
]

# Cómo aplicamos los hallazgos generales y de las otras propuestas
APLICA_GENERALES = [
    ('Todos vieron el mismo problema', 'Destacar lo que solo hace Copiloto Kine: la cita entra sola, ruta con tiempo de traslado, retención apartada, proyección y vista paciente.', 'Lámina comparativa de las 4 propuestas en la presentación final.', 'Preguntar a Josselyn qué la haría elegir una u otra.'),
    ('Comparará o combinará propuestas', 'Exportar a Excel o Google Sheets con el formato de panel mensual y anual, para convivir con una planilla.', 'Mensaje: “funciona con lo que ya usas: AgendaPro y Excel”.', 'Prueba: abrir el resumen exportado en una planilla.'),
    ('Tres modelos en juego (app, Excel, grupal)', 'Integrarlos en una hoja de ruta: núcleo app → exportación Excel → módulo de clases grupales.', 'Presentarlo como una “batería de apoyo” en un solo lugar.', 'Validar con ella el orden de prioridad.'),
    ('El costo es pregunta obligada', 'Costeo del MVP: horas del equipo, servicios en planes gratuitos o de bajo costo, enlace wa.me y API de combustible sin costo.', 'Tabla de costos de desarrollo, de operación mensual y precio para la usuaria (referencia EV2: $20–25 mil/mes, a validar).', 'Pregunta de precio del guion A (H4).'),
    ('Lo manual no escala', 'Medir automatización: % de atenciones que entran solas desde la agenda y minutos de cierre del día.', 'Mostrar el contraste con las planillas: “no hay que alimentarla”.', 'Meta EV2: ≥ 80 % de atenciones registradas solas; cierre < 30 min.'),
    ('Cada equipo propone desde su formación', 'Reforzar lo de Diseño Digital: experiencia de uso, accesibilidad AA, mirada del paciente.', 'Demo en vivo del prototipo en el celular durante la presentación.', 'Cuestionario SUS ≥ 75 con Josselyn.'),
    ('La clienta está abierta', 'Agendar la sesión de testeo con el prototipo v3 a la brevedad.', '—', 'Kit de testeo, guion A, con preguntas sobre las otras propuestas.'),
]
APLICA_OTRAS = [
    ('Herramienta integral en Excel', 'Guía de uso, respaldo, alertas, resúmenes mensuales y metas de crecimiento.', 'Guía de inicio en 3 pasos; respaldo en la nube (B2); resumen mensual automático; meta de pacientes nuevos además de la meta de ganancia.'),
    ('Planilla Excel de gestión', 'Listas desplegables de tipo, modalidad, estado y medio de pago; panel mensual y anual; ingresos dependientes e independientes.', 'Campos de estado y medio de pago en cada atención; vista anual; separación clínica (factura mensual) / particulares.'),
    ('Programas grupales', 'Estacionalidad, convenios con empresas y municipalidades, pausas activas, seguimiento de asistencia y permanencia.', 'Clases grupales en la proyección de meses bajos; convenios como tipo de cliente (cobro a una institución); pausas activas para las empresas de sus propios clientes; asistencia y permanencia por grupo.'),
    ('Comentarios del profesor y Sercotec', 'Usable en teléfono, tablet o computador; todo parametrizado; resúmenes semanales y mensuales; costo de la hora hombre.', 'App web instalable en cualquier dispositivo; resumen semanal; valor de su hora profesional calculado con el tiempo de traslado.'),
]

# Vista paciente v1 → v2 (personas mayores)
PAC_PRINCIPIOS = [
    ('Mensajes', 'Hasta 3 opciones y un mapa', 'Un mensaje = una acción; máximo 2 botones; al responder, las opciones desaparecen'),
    ('Letra y botones', '16 px; botones de 44 px', 'Letra de 20 px (mínimo 14 px); botones de 56–60 px a todo el ancho'),
    ('Hora', '“Entre 12:15 y 12:45” · “≈ 15 min”', '“Llego cerca de las 12:30” · “Llego a las 12:30”: sin rangos ni cuentas'),
    ('Lenguaje', 'Tuteo y frases largas', 'Trato de “usted”, frases cortas, saludo con su nombre'),
    ('Ayuda', 'Botón “Letra grande” opcional', '“Llamar a Josselyn” siempre visible y “Escuchar mensaje” en voz alta'),
    ('Reagendar', 'Botón “Quiero cambiar la hora”', '“Necesito otra hora” → Josselyn lo llama (sin formularios)'),
    ('Pago', 'Solo comprobante', 'Elegir transferencia o efectivo en un toque; comprobante a la persona y a su familiar'),
    ('Oferta', 'Hora liberada con descuento para todos', 'Personas mayores: invitación a clase grupal; pacientes activos: hora liberada'),
]
PAC_HALLAZGOS = [
    ('RF10 · grupal preventivo para adultos mayores (Las Cabras)', 'M4: invitación a clase de movimiento, con lugar, día, valor y “puede ir con un acompañante”.'),
    ('Planilla de otro equipo · medio de pago y estado', 'M3: el paciente elige transferencia o efectivo; el registro de Josselyn queda con el medio de pago.'),
    ('Clientes con familia que coordina (perfil cuidadora)', 'M3: comprobante en copia a la hija o cuidadora; el familiar también puede confirmar.'),
    ('RF6 · caminos rurales y tiempo de traslado', 'M2: hora de llegada exacta calculada con la ruta, en vez de minutos aproximados.'),
    ('RF9 · el servicio especializado se valora poco', 'M3: el monto se muestra junto a “sesión en su casa”, para dar cuenta del servicio a domicilio.'),
    ('RF11 · pacientes que manejan sus tiempos', 'M5: la hora liberada se ofrece solo a pacientes activos (estudiantes, trabajadores, deportistas).'),
    ('Ariel / Mabel · simple y de bajo costo', 'Todo ocurre en WhatsApp: el paciente no instala nada ni crea cuentas.'),
]
