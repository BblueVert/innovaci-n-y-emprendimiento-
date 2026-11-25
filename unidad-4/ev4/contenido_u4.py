# Contenido de la EV4 (Unidad 4 · Difusión de la innovación) · caso Josselyn Toledo / Copiloto Kine.
# Fuente única para el Lean Canvas (4.1.2.1), el formulario de postulación (4.1.3.1), el informe final y el pitch (4.1.3.2).
# Las cifras de mercado marcadas como "estimación" son supuestos del equipo, no datos oficiales.

PRODUCTO = 'Copiloto Kine'
EQUIPO = ['Francisco Ahumada', 'Claudia Cifuentes', 'Néstor Rivera', 'Benjamín Vera Yáñez']
PROFESOR = 'Roberto Escobar Donoso'
CARRERA = 'Diseño Digital'
ASIGNATURA = 'Innovación y Emprendimiento III (FGIE03)'
SEDE = 'INACAP Rancagua'
URL_PRO = 'https://copiloto-kine.vercel.app/profesional/'
URL_CLI = 'https://copiloto-kine.vercel.app/cliente/'

TITULO = 'Copiloto Kine: ganancia real y por hora para kinesiólogas independientes de O’Higgins'  # ≤ 15 palabras

DESAFIO = ('¿Cómo podríamos aumentar la visibilidad financiera de kinesiólogas independientes con atención mixta, conectando su agenda '
           'con sus ingresos y costos, para reducir a la mitad el tiempo de registro manual (de ~1 h a menos de 30 min diarios) en Rancagua '
           'durante 2027?')

# ---------------------------------------------------------------- Lean Canvas (4.1.2.1)
LC = {
    'problema': [
        '1. No sabe cuánto gana de verdad ni qué le conviene: atiende en clínica (factura mensual), a domicilio, en piscina y en su gimnasio, y lo anota todo cada noche en el teléfono (~1 h).',
        '2. El traslado no se mide ni se cobra: en caminos rurales como Aguas Buenas pierde 25–30 min por visita, más bencina.',
        '3. Ingresos estacionales: enero y febrero bajan cerca de 35 % y no tiene un plan para cubrirlos.',
    ],
    'alternativas': 'Hoy: AgendaPro y agenda médica (solo agendan), notas del celular, planillas Excel y la contadora a fin de año.',
    'solucion': [
        '1. Cada cita de AgendaPro y de la clínica se convierte sola en ganancia real (comisión o factura, traslado, materiales y retención).',
        '2. Ganancia por hora de cada canal, con el tiempo de viaje valorado y una tarifa sugerida por tramo.',
        '3. Proyección de meses bajos con acciones (clase grupal, packs, colchón) y resumen exportable para la contadora.',
    ],
    'metricas': [
        'Adquisición: kinesiólogas que abren la demo (meta: 100 en 3 meses).',
        'Activación: conecta su agenda y registra su 1.ª atención el primer día (≥ 60 %).',
        'Retención: cierra el día ≥ 4 de 5 días hábiles; uso a los 90 días ≥ 50 %.',
        'Ingresos: conversión del piloto gratis a pago ≥ 30 %.',
        'Referencia: cada usuaria refiere a 1 colega en 6 meses.',
        'Producto: cierre del día < 2 min; ≥ 80 % de atenciones registradas solas.',
    ],
    'pdv': 'Sabe cuánto ganas y qué te conviene, sin anotar nada de noche.',
    'pdv_detalle': ('El copiloto de la kinesióloga que trabaja en varios lugares: toma sus citas, ordena su ruta y convierte cada atención en '
                    'ganancia real y por hora, contando también el tiempo de viaje.'),
    'concepto': 'Concepto en alto nivel: “un copiloto de rally para su consulta itinerante”.',
    'ventaja': [
        'Nace del trabajo real con una kinesióloga de la región: 4 ciclos de testeo, uno con la clienta, Sercotec y docentes.',
        'Única que cruza agenda + costo de traslado rural + retención de boletas (Ley 21.133) + vista para el paciente.',
        'Conocimiento del territorio (caminos rurales, estacionalidad) y privacidad por diseño (Ley 21.719): difícil de copiar por apps genéricas.',
    ],
    'canales': [
        'Directo: piloto gratis de 3 meses con Josselyn y su red (boca a boca entre kinesiólogas).',
        'Comunidades: Colegio de Kinesiólogos, grupos de WhatsApp y Facebook de la región, ex compañeros de universidad.',
        'Contenido: Instagram y TikTok con casos (“¿cuánto te cuesta un domicilio en precordillera?”).',
        'Aliados: Sercotec, centros de negocios y clínicas que trabajan con kines independientes.',
        'App web: se abre desde un enlace, sin instalar nada.',
    ],
    'segmento': [
        'Kinesiólogas y kinesiólogos independientes con atención mixta (clínica + particulares) en la Región de O’Higgins.',
        'Early adopters: profesionales que ya registran sus ingresos a mano y atienden a domicilio en zonas rurales (Josselyn y Catalina).',
        'Otros roles: pacientes (reciben avisos y comprobantes) y contadora (recibe el resumen mensual).',
        'Mercado: 30.050 kinesiólogos en el Registro Nacional de Prestadores (Superintendencia de Salud); en O’Higgins, ~1.500 (estimación del equipo, ~5 % de la población del país).',
    ],
    'costos': [
        'Desarrollo del MVP: 4 integrantes × 60 h (aporte del equipo; referencia $1.920.000).',
        'Operación piloto: ~$900/mes (dominio; hosting, base de datos, mapas y precios de bencina en planes gratuitos).',
        'Operación comercial: ~$48.000/mes (Vercel Pro, Supabase Pro y WhatsApp Business API).',
        'Adquisición de clientes (CAC): ~$15.000 por usuaria (contenido, charlas y referidos).',
        'Soporte y mantención: 8 h/mes del equipo.',
    ],
    'ingresos': [
        'Suscripción mensual: $9.990 (piloto gratis 3 meses; precio a validar en el ciclo 4).',
        'Plan anual: $99.900 (2 meses de regalo).',
        'Valor del tiempo de vida (LTV): 24 meses × $9.990 ~$240.000.',
        'Margen bruto con 30 usuarias: ingresos $299.700 − operación $48.000 ~84 %.',
        'Punto de equilibrio de la operación: 5 usuarias pagando.',
    ],
}

# ---------------------------------------------------------------- Factibilidad económica (4.1.2)
SUPUESTOS = [
    ('Precio', '$9.990 al mes por usuaria', 'Bajo la referencia del mercado ($20–25 mil) por lo dicho en el ciclo 3: bajo costo y región que valora poco lo especializado.'),
    ('Costo operativo comercial', '$48.000 al mes', 'Vercel Pro (US$20), Supabase Pro (US$25) y WhatsApp Business API, a $950/US$.'),
    ('CAC', '$15.000 por usuaria', 'Contenido en redes, charlas en el Colegio de Kinesiólogos y referidos.'),
    ('Permanencia', '24 meses promedio', 'Abandono mensual supuesto de ~4 %.'),
    ('Mercado regional', '~1.500 kinesiólogos', 'Estimación: 5 % de los 30.050 registrados en Chile.'),
]
ESCENARIOS = [  # usuarias pagando a fin del año 1
    ('Conservador', 15, 'Josselyn, Catalina y su red directa.'),
    ('Base', 30, '2 % del mercado regional estimado.'),
    ('Optimista', 75, '5 % del mercado regional con apoyo de Sercotec.'),
]
PRECIO, OPEX = 9990, 48000


def escenario(n):
    ing = n * PRECIO
    return dict(n=n, ingresos_mes=ing, margen_mes=ing - OPEX, margen_pct=round((ing - OPEX) / ing * 100) if ing else 0, ingresos_anio=ing * 12)


IMPACTOS = [
    ('Económico', 'La usuaria ve su ganancia por hora y cobra el traslado: un recargo de $3.000–6.000 en 8 domicilios rurales al mes suma $24.000–48.000, más que el costo de la app. La clase grupal agrega ~$213.000 al mes en los meses bajos.'),
    ('Tecnológico', 'App web liviana (64 KB) que funciona en teléfono, tablet y computador; se integra con lo que ya usa (AgendaPro, WhatsApp, Excel) en vez de reemplazarlo.'),
    ('Sociocultural', 'Libera ~1 h diaria de trabajo nocturno (tiempo con su familia); acerca atención preventiva grupal a adultos mayores de Las Cabras; vista paciente accesible para personas mayores.'),
    ('Medioambiental', 'La ruta sugerida reduce 12 km en un día tipo (41 vs. 53 km): ~240 km y ~40 kg de CO2 menos al mes con 20 días de domicilios (estimación con 14 km/l y 2,3 kg CO2/l).'),
]

# ---------------------------------------------------------------- Sostenibilidad y acciones futuras (4.1.5)
ACCIONES = [
    ('Dic 2026', 'Ciclo 4: sesión con Josselyn y Catalina con la v3 (SUS, precio, tramos).', 'Equipo'),
    ('Ene 2027', 'MVP: importación de la agenda de AgendaPro, respaldo en la nube y aviso por WhatsApp (wa.me).', 'Equipo'),
    ('Feb–Mar 2027', 'Piloto gratis con 5 kinesiólogas de O’Higgins; medir activación y retención.', 'Equipo + Josselyn'),
    ('Mar 2027', 'Clase grupal piloto en Las Cabras con una agrupación de adultos mayores.', 'Josselyn'),
    ('Abr 2027', 'Postulación a fondos (Sercotec Capital Semilla Emprende o similar) con los resultados del piloto.', 'Equipo'),
    ('2.º sem. 2027', 'Plan pagado a $9.990 y expansión a otras regiones y profesiones de salud independientes.', 'Equipo'),
]
RIESGOS = [
    ('Baja disposición a pagar', 'Piloto gratis y precio bajo; medir conversión antes de escalar.'),
    ('AgendaPro no permite integrar', 'Importar su exportación en Excel; Google Calendar como alternativa.'),
    ('Datos de salud', 'Solo montos e iniciales, nunca diagnósticos (Ley 21.719).'),
    ('Pocas usuarias en la región', 'Abrir a fonoaudiólogas, terapeutas ocupacionales y nutricionistas independientes.'),
]

# ---------------------------------------------------------------- Guion del pitch (4.1.3.2) · 3,5 min
PITCH_FRASE = 'Copiloto Kine: sabe cuánto ganas y qué te conviene, sin anotar nada de noche.'
PITCH = [
    ('Quién eres', 'Somos Francisco, Claudia, Néstor y Benjamín, estudiantes de Diseño Digital de INACAP Rancagua. Este año trabajamos con Josselyn Toledo, kinesióloga y psicomotricista acuática de San Fernando. Josselyn atiende en cuatro lugares: en una clínica, a domicilio, en una piscina temperada y en su propio gimnasio. Y cada noche, después de atender, anota en el teléfono cuánto ganó, cuánto gastó en bencina y cuántas sesiones hizo. Aun así, no sabe qué le conviene. Como ella, hay cerca de mil quinientos kinesiólogos en la Región de O’Higgins, y muchos trabajan de forma independiente, entre la clínica y los domicilios, con caminos rurales y meses en que los ingresos caen.'),
    ('Qué haces', 'Creamos Copiloto Kine, una app web que funciona en el celular, sin instalar nada. Toma las citas que Josselyn ya tiene en AgendaPro y en la agenda de la clínica, y convierte cada atención en ganancia real: descuenta la comisión o la factura de la clínica, el traslado, los materiales y la retención de la boleta. Le muestra cuánto gana por hora en cada lugar, cuánto le cuesta en tiempo y en bencina el viaje a Aguas Buenas, y cuánto debería cobrar por ese tramo. Además, le avisa con semanas de anticipación que enero y febrero vienen bajos y le propone acciones con su monto, como una clase grupal para adultos mayores en Las Cabras. Al final del día, cierra todo en un minuto.'),
    ('Por qué es único', 'Las apps que usa Josselyn solo agendan, y las planillas en Excel hay que alimentarlas a mano. Copiloto Kine es la única que cruza la agenda con el costo del traslado rural, la retención de boletas y la experiencia del paciente, que recibe avisos claros pensados para personas mayores. No lo inventamos en una sala: lo probamos en cuatro ciclos, uno de ellos con la propia Josselyn, Sercotec y docentes, y lo ajustamos a cómo trabaja de verdad. El prototipo completa 21 de 21 tareas, calcula exacto y no tiene errores de accesibilidad. Y cuesta $9.990 al mes: menos de lo que Josselyn recupera cobrando un solo tramo rural.'),
    ('Objetivo', 'Queremos que las kinesiólogas independientes de O’Higgins dejen de trabajar de noche en sus cuentas y decidan con datos dónde atender, cuánto cobrar y cómo preparar los meses bajos. En marzo partimos con un piloto gratis para cinco profesionales de la región, medimos cuántas siguen usándolo, y con esos resultados postularemos a fondos de Sercotec para escalar a otras regiones y a otras profesiones de salud independientes. Copiloto Kine: sabe cuánto ganas y qué te conviene, sin anotar nada de noche.'),
]

# ---------------------------------------------------------------- Formulario de postulación (4.1.3.1)
FORM = {
    'titulo': TITULO,
    'resumen': ('Las kinesiólogas independientes de O’Higgins trabajan en varios lugares a la vez —clínica, domicilio, piscina, gimnasio— y no saben '
                'cuánto ganan realmente ni qué les conviene. Josselyn Toledo, kinesióloga de San Fernando, anota cada noche en su teléfono lo que ganó y '
                'gastó en bencina: casi una hora diaria, sin saber si un domicilio rural le rinde. Copiloto Kine es una app web que toma las citas de la '
                'agenda que ya usa (AgendaPro y la de la clínica) y convierte cada atención en ganancia real y ganancia por hora, descontando comisión o '
                'factura, traslado, materiales y retención de boletas. Valora el tiempo de viaje, sugiere cuánto cobrar por tramo rural, anticipa los meses '
                'bajos con acciones concretas (como clases grupales para adultos mayores) y entrega un resumen para la contadora. El prototipo se validó en '
                'cuatro ciclos, uno con la clienta, Sercotec y docentes. Impacto: cerca de una hora diaria de trabajo nocturno liberada, mejores ingresos '
                'por cobrar el traslado y menos kilómetros recorridos.'),
    'ods': ['Salud y Bienestar', 'Trabajo Decente y Crecimiento Económico', 'Industria, Innovación e Infraestructura'],
    'otro': '',
    'desafio': DESAFIO,
    'problema': ('Las y los kinesiólogos independientes con atención mixta combinan una clínica (por comisión o con una factura mensual) con pacientes '
                 'particulares a domicilio y otros servicios. En Chile hay 30.050 kinesiólogos en el Registro Nacional de Prestadores Individuales '
                 '(Superintendencia de Salud); en O’Higgins estimamos cerca de 1.500. Las herramientas que usan solo agendan (AgendaPro, agendas médicas) '
                 'y la parte financiera queda en notas del celular o en Excel.\n\n'
                 'En la investigación (UA1) y en la reunión con la clienta del 12/11 encontramos tres problemas: (1) no saben cuánto ganan de verdad ni qué '
                 'canal les conviene: Josselyn atiende en clínica, a domicilio, en piscina y en su gimnasio, y registra todo cada noche (“cada noche anoto '
                 'todo… lo que gasto en bencina… cuánto gané en cada sesión”); una experta par, Catalina, declara “me toma una hora diaria”; (2) el traslado '
                 'no se mide ni se cobra: un domicilio en Aguas Buenas, en la precordillera, le toma 25–30 minutos por camino de ripio; (3) los ingresos son '
                 'estacionales: enero y febrero bajan cerca de 35 % sin un plan para cubrirlos.\n\n'
                 'Afecta directamente a la profesional, e indirectamente a sus pacientes (muchos adultos mayores en zonas rurales) y a su contadora.'),
    'consecuencias': ('Para la profesional: cerca de 1 hora diaria de trabajo administrativo nocturno (unas 22 horas al mes, que a $15.000 la hora '
                      'equivalen a ~$330.000 de su tiempo) y desgaste personal. Decide a ciegas: puede estar atendiendo a pérdida un domicilio rural, '
                      'porque el viaje de ida y vuelta (56 minutos y 28 km a Aguas Buenas) no se cobra. Sin proyección, enero y febrero la toman por '
                      'sorpresa y recurre a sus ahorros.\n\n'
                      'Para el territorio: en comunas rurales como Las Cabras o Aguas Buenas, los adultos mayores dependen de la atención a domicilio; '
                      'si a la profesional no le rinde, la oferta se reduce. La región “valora poco lo especializado” (clienta, 12/11), por lo que '
                      'subir precios sin argumentos es difícil.\n\n'
                      'Para el sector: el trabajo independiente en salud crece y la Ley 21.133 aumenta gradualmente la retención de boletas (15,25 % en '
                      '2026, 16 % en 2027, 17 % en 2028), lo que hace más necesario provisionar impuestos. Las soluciones del mercado (AgendaPro, '
                      'Encuadrado, Reservo, Medilink, Nubox) agendan o llevan contabilidad, pero ninguna cruza la cita con el traslado, la comisión y la '
                      'retención chilena.'),
    'mercado': ('Ubicación: Región de O’Higgins (San Fernando, Rancagua, Colchagua y comunas rurales), con proyección nacional.\n'
                'Mercado potencial: 30.050 kinesiólogos registrados en Chile; ~1.500 en O’Higgins (estimación del equipo, ≈ 5 % de la población). '
                'Mercado objetivo inicial: los independientes con atención mixta; meta del año 1: 30 usuarias pagando (2 % del mercado regional).\n'
                'Clientes y usuarios: la kinesióloga independiente paga y usa la app. Usuarios secundarios: sus pacientes, que reciben recordatorios, '
                'avisos de llegada y comprobantes; y su contadora, que recibe el resumen.\n'
                'Segmento más importante (early adopters): profesionales que ya registran ingresos a mano y atienden a domicilio en zonas rurales, como '
                'Josselyn y Catalina. Otros segmentos futuros: fonoaudiólogas, terapeutas ocupacionales y nutricionistas independientes.\n'
                'Relación: cercana y de autoservicio; piloto acompañado, comunidad de usuarias y soporte por WhatsApp.\n'
                'Competidores y sustitutos: agendas (AgendaPro, Encuadrado, Reservo, Cal.com), software clínico (Medilink, Cliniko), contabilidad '
                '(Nubox) y planillas Excel. Proveedores: servicios en la nube (Vercel, Supabase), mapas (OpenRouteService), precios de combustible '
                '(API Bencina en Línea, CNE) y WhatsApp.'),
    'tipo': 'Un nuevo producto (bien o servicio)',
    'solucion': ('Copiloto Kine es una app web para el celular (sin instalación) que funciona como copiloto financiero de la kinesióloga '
                 'independiente:\n'
                 '1. La agenda entra sola: toma las citas de AgendaPro y de la agenda de la clínica.\n'
                 '2. Cada atención se vuelve ganancia real con un toque: descuenta comisión o factura mensual, traslado, materiales o arriendos, y '
                 'retención de la boleta.\n'
                 '3. Ganancia por hora de cada canal (clínica, domicilio, piscina, gimnasio, clase grupal), contando el tiempo de viaje.\n'
                 '4. Ruta del día con el costo del traslado y una tarifa sugerida por tramo (urbano, rural, precordillera).\n'
                 '5. Proyección de meses bajos con acciones, entre ellas una clase grupal con su punto de equilibrio.\n'
                 '6. Resumen semanal y mensual exportable a Excel para la contadora, sin datos clínicos.\n'
                 '7. Vista paciente: mensajes simples para personas mayores (recordatorio, “voy en camino”, comprobante).\n\n'
                 f'Nivel de avance: prototipo navegable v3 publicado ({URL_PRO}), validado en cuatro ciclos (dos internos, uno con la clienta, '
                 'Sercotec y docentes, y uno planificado con usuarias). Completa 21 de 21 tareas, calcula igual que la hoja de referencia y no tiene '
                 'errores de accesibilidad WCAG AA. Siguiente paso: MVP con la agenda real, respaldo en la nube y aviso por WhatsApp.'),
    'novedad': ('Novedad: es la única solución que cruza la agenda con lo que realmente queda de cada atención en un trabajo itinerante y rural: '
                'comisión o factura, traslado en bencina y en tiempo, y retención chilena. Las alternativas cubren una parte: AgendaPro, Encuadrado '
                'o Reservo agendan; Nubox lleva contabilidad; las planillas en Excel hay que alimentarlas a mano.\n'
                'Por qué pagarían: porque recuperan dinero (cobrar un solo tramo rural de $3.000–6.000 ya cubre los $9.990 del mes), tiempo (≈ 1 hora '
                'diaria) y tranquilidad (impuestos provisionados y meses bajos anticipados). Hoy pagan por agendas que no les dicen cuánto ganan.\n'
                'Por qué elegirnos: la diseñamos con una kinesióloga real de la región y la ajustamos a cómo trabaja (cuatro lugares, factura '
                'mensual, caminos rurales). No reemplaza lo que usa: se conecta a su agenda y exporta a la misma planilla de su contadora. Cuesta '
                'menos que una sesión y se prueba gratis.\n'
                'Problemas que resuelve: no saber cuánto gana ni qué le conviene, no cobrar el traslado, la estacionalidad y el trabajo nocturno.\n'
                'Necesidades que satisface: control financiero simple, decidir dónde atender y cuánto cobrar, y tiempo personal.'),
    'canales': ('Fase 1 (piloto): canal directo y personal. Josselyn y Catalina invitan a colegas; demo en vivo desde un enlace; acompañamiento por '
                'WhatsApp.\n'
                'Fase 2 (crecimiento): comunidades profesionales (Colegio de Kinesiólogos, grupos regionales de WhatsApp y Facebook, ex alumnos), '
                'contenido en Instagram y TikTok con casos reales (“¿cuánto te cuesta un domicilio en precordillera?”) y charlas en centros de '
                'negocios Sercotec.\n'
                'Fase 3 (escala): alianzas con clínicas que trabajan con kinesiólogos independientes y con agendas existentes.\n'
                'Los canales más rentables para este segmento son el boca a boca entre colegas y las comunidades profesionales: bajo costo y alta '
                'confianza. La app web se abre desde un enlace, sin tiendas de aplicaciones, lo que reduce la fricción y el costo de distribución.'),
    'actividades': ('Actividades clave: desarrollo y mantención de la app (integración de agenda, cálculo, respaldo); acompañamiento del piloto; '
                    'creación de contenido; gestión de comunidad y soporte.\n'
                    'Cómo se medirán (métricas pirata):\n'
                    '• Adquisición: kinesiólogas que abren la demo (meta 100 en 3 meses).\n'
                    '• Activación: conectan la agenda y registran la primera atención el primer día (≥ 60 %).\n'
                    '• Retención: cierran el día al menos 4 de 5 días hábiles; siguen usando la app a los 90 días (≥ 50 %).\n'
                    '• Ingresos: pasan del piloto gratis al plan pagado (≥ 30 %).\n'
                    '• Referencia: cada usuaria recomienda a una colega en 6 meses.\n'
                    '• Producto: cierre del día en menos de 2 minutos; ≥ 80 % de las atenciones registradas solas; SUS ≥ 75.'),
    'costos': ('Costos fijos: operación comercial ≈ $48.000 al mes (hosting Vercel Pro, base de datos Supabase Pro, WhatsApp Business API, a $950 por '
               'dólar); dominio ≈ $10.900 al año; soporte y mantención 8 horas al mes del equipo.\n'
               'Costos del piloto: ≈ $900 al mes, usando planes gratuitos.\n'
               'Desarrollo del MVP: 4 integrantes × 60 horas, aporte del equipo (valor de referencia $1.920.000).\n'
               'Costos variables: mensajes de WhatsApp por conversación y almacenamiento, bajos por usuaria.\n'
               'Costo de adquisición (CAC): ≈ $15.000 por usuaria (contenido, charlas y referidos); se recupera en el segundo mes de pago.\n'
               'No hay costos de distribución ni almacenaje: es un producto digital que se entrega por un enlace.'),
    'ingresos': ('Modelo: suscripción. Piloto gratis por 3 meses; luego $9.990 al mes o $99.900 al año (2 meses de regalo).\n'
                 'Valor del tiempo de vida (LTV): con 24 meses de permanencia promedio, ≈ $240.000 por usuaria, 16 veces el CAC.\n'
                 'Proyección del año 1: escenario conservador 15 usuarias ($149.850 al mes); base 30 ($299.700 al mes, margen bruto ≈ 84 %); '
                 'optimista 75 ($749.250 al mes). Punto de equilibrio de la operación: 5 usuarias pagando.\n'
                 'Medio de pago preferido: transferencia o débito automático mensual (Mercado Pago o Flow), que es como las profesionales '
                 'independientes pagan hoy otros servicios; plan anual por transferencia.'),
    'equipo_desc': ('Equipo de 4 estudiantes de Diseño Digital de INACAP Rancagua, con competencias en investigación con usuarios, UX/UI, '
                    'prototipado en Figma y HTML, identidad visual y desarrollo web. Roles: Claudia Cifuentes, moderación de sesiones de testeo y '
                    'relación con usuarias; Néstor Rivera, prototipo y ejecución de tareas; Francisco Ahumada, registro, matrices y contenido; '
                    'Benjamín Vera Yáñez, secretario técnico: consolidación, auditoría técnica y desarrollo. Durante 2026 desarrollamos el caso '
                    'completo con la clienta Josselyn Toledo: diagnóstico, ideación, prototipo navegable y cuatro ciclos de testeo. Para el MVP '
                    'buscaremos apoyo de un asesor contable para validar las reglas tributarias.'),
    'programa': 'Instituto Profesional',
    'carrera': 'Diseño Digital',
}
