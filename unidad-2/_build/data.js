// Contenido fuente de la Unidad 2 (Semanas 6 y 7).
// Editar aquí y volver a correr `node build.js` para regenerar tableros y Word.

const equipo = [
  { key: 'F', nombre: 'Francisco Ahumada', color: '#FFE66D' },
  { key: 'C', nombre: 'Claudia Cifuentes', color: '#FFB3C7' },
  { key: 'N', nombre: 'Néstor Rivera', color: '#A8D8FF' },
  { key: 'B', nombre: 'Benjamín Vera Yáñez', color: '#B8F2B0', secretario: true },
];

const contraparte = {
  nombre: 'Joselyn Toledo',
  negocio: 'Centro Médico InMotion + atención particular a domicilio',
  ubicacion: 'Rancagua, Región de O’Higgins, Chile',
  encargado: 'Joselyn Toledo, kinesióloga (dueña y profesional tratante)',
  actividad: 'Servicios de kinesiología: rehabilitación músculoesquelética, kinesioterapia respiratoria y neurológica, masoterapia, psicomotricidad acuática, piso pélvico y fisiología del ejercicio.',
  modelo: 'Modelo mixto: atención en clínica InMotion (comisión 70/30, agenda vía secretaria) y atención a domicilio particular (agenda por WhatsApp, vehículo y materiales propios).',
  antiguedad: 'Empresa propia desde hace aproximadamente 1 año; carga variable de 10 a 32 horas semanales, lunes a sábado.',
  dolor: 'Gestión financiera y de agenda manual (Excel + calendario del celular), ingresos estacionales sin proyección a 6–12 meses.',
};

const desafio = '¿Cómo podríamos ordenar la agenda y las finanzas de Joselyn Toledo, kinesióloga independiente de InMotion, para que proyecte sus ingresos a 6 meses y libere horas administrativas cada semana, sin perder su atención personalizada 1:1?';

// ---------- SEMANA 6 · Referentes ----------
const variables = [
  { k: 'agenda', t: 'Agenda y reserva' },
  { k: 'finanzas', t: 'Control financiero' },
  { k: 'cobro', t: 'Cobro y pago' },
  { k: 'relacion', t: 'Relación y fidelización' },
  { k: 'novedad', t: 'Elemento novedoso para el desafío' },
  { k: 'tendencia', t: 'Tendencia' },
];

const referentes = [
  {
    n: 1, nombre: 'Calendly', ambito: 'Productividad · agendamiento B2B', fuente: 'calendly.com',
    desc: 'Agenda online donde el cliente elige un horario libre desde un link; se sincroniza con el calendario del profesional y envía confirmaciones.',
    agenda: 'Autoservicio 24/7 con reglas de disponibilidad y “buffers” entre citas.',
    finanzas: 'No aplica de forma nativa.',
    cobro: 'Permite cobrar al reservar (integración Stripe/PayPal).',
    relacion: 'Recordatorios automáticos y reprogramación sin intermediario.',
    novedad: 'Tiempos “buffer” configurables → bloquear el traslado entre domicilios.',
    tendencia: 'Autoservicio',
  },
  {
    n: 2, nombre: 'Uber', ambito: 'Movilidad · servicio on-demand', fuente: 'uber.com',
    desc: 'App de transporte que conecta pasajero y conductor, con seguimiento en tiempo real, tarifa calculada y pago automático al terminar.',
    agenda: 'Solicitud inmediata o programada; el usuario ve cuándo llega el servicio.',
    finanzas: 'El conductor ve sus ganancias diarias y semanales en la app.',
    cobro: 'Pago automático e invisible al finalizar el viaje.',
    relacion: 'Calificación bidireccional y aviso “tu conductor va en camino”.',
    novedad: 'Aviso “voy en camino” + tarifa según distancia/zona para domicilios.',
    tendencia: 'Transparencia en tiempo real',
  },
  {
    n: 3, nombre: 'YNAB — You Need A Budget', ambito: 'Finanzas personales', fuente: 'ynab.com',
    desc: 'App de presupuesto basada en asignar a cada peso un “trabajo” antes de gastarlo, con foco en educación financiera.',
    agenda: 'No aplica.',
    finanzas: 'Categorías tipo “sobres”, metas y métrica “edad del dinero”.',
    cobro: 'No aplica.',
    relacion: 'Contenido educativo y talleres gratuitos dentro de la herramienta.',
    novedad: 'Separar cada ingreso por propósito: impuestos, bencina, fondo de temporada baja.',
    tendencia: 'Educación financiera integrada',
  },
  {
    n: 4, nombre: 'Fintual', ambito: 'Inversión · fintech chilena', fuente: 'fintual.cl',
    desc: 'Plataforma de inversión que muestra metas con gráficos de proyección y lenguaje simple, sin jerga financiera.',
    agenda: 'No aplica.',
    finanzas: 'Proyección visual de metas en el tiempo; aportes automáticos.',
    cobro: 'Transferencias y aportes programados.',
    relacion: 'Comunicación cercana, con humor y “sin letra chica”.',
    novedad: 'Mostrar la meta mensual y la proyección a 6 meses en lenguaje cotidiano.',
    tendencia: 'Datos simples y proyección visual',
  },
  {
    n: 5, nombre: 'Duolingo', ambito: 'Educación · aprendizaje de idiomas', fuente: 'duolingo.com',
    desc: 'App de idiomas que sostiene el hábito diario con rachas, recordatorios y metas cortas.',
    agenda: 'Recordatorios a la hora que el usuario suele practicar.',
    finanzas: 'No aplica.',
    cobro: 'Modelo freemium con suscripción.',
    relacion: 'Rachas, logros y notificaciones con personalidad propia.',
    novedad: 'Rachas para los ejercicios en casa → más adherencia y retorno del paciente.',
    tendencia: 'Gamificación de hábitos',
  },
  {
    n: 6, nombre: 'Strava', ambito: 'Deporte · comunidad', fuente: 'strava.com',
    desc: 'Red social deportiva que registra actividad, muestra progreso y conecta a los usuarios en clubes.',
    agenda: 'No aplica.',
    finanzas: 'No aplica.',
    cobro: 'Freemium con suscripción.',
    relacion: 'Progreso visual, hitos y clubes que generan pertenencia.',
    novedad: 'Tarjeta de progreso del tratamiento + comunidad para grupos de adultos mayores.',
    tendencia: 'Cuantificación personal y comunidad',
  },
  {
    n: 7, nombre: 'Doctoralia', ambito: 'Salud · marketplace de agenda', fuente: 'doctoralia.cl',
    desc: 'Plataforma donde pacientes buscan profesionales de salud, leen opiniones verificadas y reservan hora online.',
    agenda: 'Reserva online con disponibilidad en tiempo real.',
    finanzas: 'Panel para el profesional con reservas y estadísticas.',
    cobro: 'Depende del profesional.',
    relacion: 'Opiniones verificadas y recordatorios de cita.',
    novedad: 'Reputación digital con reseñas verificadas como canal de captación.',
    tendencia: 'Reputación digital',
  },
  {
    n: 8, nombre: 'Smart Fit', ambito: 'Fitness · cadena de gimnasios', fuente: 'smartfit.cl',
    desc: 'Gimnasio de bajo costo con planes mensuales escalonados y cobro recurrente automático a tarjeta.',
    agenda: 'Reserva de clases grupales desde la app.',
    finanzas: 'Ingresos predecibles por membresía.',
    cobro: 'Débito automático mensual.',
    relacion: 'Planes con beneficios crecientes; app como punto de contacto.',
    novedad: 'Packs y membresía de mantención post-alta → ingreso recurrente.',
    tendencia: 'Economía de suscripción',
  },
  {
    n: 9, nombre: 'Mercado Pago', ambito: 'Fintech · pagos', fuente: 'mercadopago.cl',
    desc: 'Billetera y medio de cobro con link de pago, QR y lector de tarjetas; registra cada transacción automáticamente.',
    agenda: 'No aplica.',
    finanzas: 'Historial y reportes de ventas descargables.',
    cobro: 'Link por WhatsApp, QR o tarjeta, sin efectivo.',
    relacion: 'Comprobante inmediato al cliente.',
    novedad: 'Cobrar en el domicilio y que el pago alimente solo el registro financiero.',
    tendencia: 'Pagos sin fricción',
  },
];

const tendencias = [
  { t: 'Autoservicio 24/7', casos: 'Calendly · Doctoralia · Uber', ins: 'El paciente reserva y reprograma solo; Joselyn deja de coordinar hora por hora en WhatsApp.' },
  { t: 'Ingreso predecible por recurrencia', casos: 'Smart Fit · YNAB', ins: 'Packs y membresías suavizan la estacionalidad que Joselyn describe como “muy inestable”.' },
  { t: 'Datos simples y proyección visual', casos: 'Fintual · YNAB · Strava', ins: 'La información financiera debe leerse de un vistazo, sin saber de finanzas.' },
  { t: 'Pagos sin fricción con registro automático', casos: 'Mercado Pago · Uber · Calendly', ins: 'Cada cobro se convierte en dato sin digitarlo en Excel.' },
  { t: 'Adherencia y comunidad', casos: 'Duolingo · Strava', ins: 'Mantener al paciente activo entre sesiones sostiene resultados y retorno.' },
  { t: 'Reputación digital', casos: 'Doctoralia · Uber', ins: 'Las reseñas verificadas escalan el boca a boca, hoy su principal canal.' },
];

// ---------- SEMANA 7 · Brainstorming ----------
// cat: A Agenda · B Finanzas · C Cobro · D Relación/adherencia · E Captación · F Modelo de servicio
// o = originalidad (1–10), f = factibilidad (1–10). Umbral de cuadrante: 6.
const categorias = {
  A: { t: 'Agenda inteligente', c: '#4C6FFF' },
  B: { t: 'Tablero financiero', c: '#FF6B35' },
  C: { t: 'Cobro sin fricción', c: '#12A37F' },
  D: { t: 'Relación y adherencia', c: '#C2409A' },
  E: { t: 'Captación y visibilidad', c: '#8A6D00' },
  F: { t: 'Modelo de servicio', c: '#5A5A5A' },
};

const ideas = [
  { id: 'F1', a: 'F', t: 'Link de agenda online en la bio de IG y en WhatsApp', cat: 'A', o: 3, f: 9 },
  { id: 'F2', a: 'F', t: 'Bloqueo automático del tiempo de traslado entre domicilios según comuna', cat: 'A', o: 6, f: 7 },
  { id: 'F3', a: 'F', t: 'Tabla de precios de domicilio por sector de Rancagua', cat: 'C', o: 4, f: 9 },
  { id: 'F4', a: 'F', t: 'Ruta del día que agrupa pacientes por sector', cat: 'A', o: 6, f: 6 },
  { id: 'F5', a: 'F', t: 'Mensaje automático “voy en camino” por WhatsApp', cat: 'D', o: 6, f: 7 },
  { id: 'F6', a: 'F', t: 'App propia con realidad aumentada para corregir ejercicios', cat: 'D', o: 9, f: 2 },
  { id: 'F7', a: 'F', t: 'Reservar hora por asistente de voz (Alexa / Google)', cat: 'A', o: 8, f: 2 },
  { id: 'F8', a: 'F', t: 'Chatbot de WhatsApp que agenda y confirma solo', cat: 'A', o: 6, f: 6 },
  { id: 'F9', a: 'F', t: 'Kinesiología por suscripción para empresas de Rancagua', cat: 'F', o: 8, f: 4 },

  { id: 'C1', a: 'C', t: 'Recordatorio 24 h antes con botón de confirmar', cat: 'A', o: 2, f: 10 },
  { id: 'C2', a: 'C', t: 'Plan de ejercicios en casa con rachas tipo Duolingo', cat: 'D', o: 8, f: 5 },
  { id: 'C3', a: 'C', t: 'Encuesta de 1 pregunta al dar el alta', cat: 'D', o: 3, f: 9 },
  { id: 'C4', a: 'C', t: 'Programa de referidos: descuento por traer a alguien', cat: 'E', o: 4, f: 8 },
  { id: 'C5', a: 'C', t: 'Carrusel semanal en IG “mitos de la kine”', cat: 'E', o: 3, f: 8 },
  { id: 'C6', a: 'C', t: 'Grupo de adultos mayores con clases y comunidad en WhatsApp', cat: 'F', o: 6, f: 6 },
  { id: 'C7', a: 'C', t: 'Tarjeta de progreso visual del paciente (dolor, movilidad)', cat: 'D', o: 7, f: 7 },
  { id: 'C8', a: 'C', t: 'Pedir reseña en Google al terminar el tratamiento', cat: 'E', o: 3, f: 9 },
  { id: 'C9', a: 'C', t: 'Cápsulas de video con un referente local de salud', cat: 'E', o: 5, f: 4 },

  { id: 'N1', a: 'N', t: 'Dashboard de ingresos clínica vs. domicilio en tiempo real', cat: 'B', o: 6, f: 7 },
  { id: 'N2', a: 'N', t: 'Semáforo de meta mensual en el celular', cat: 'B', o: 7, f: 8 },
  { id: 'N3', a: 'N', t: 'Proyección de ingresos a 6 meses según historial y temporada', cat: 'B', o: 8, f: 6 },
  { id: 'N4', a: 'N', t: '“Sobres” automáticos: % de cada pago a impuestos, bencina y fondo de temporada baja', cat: 'B', o: 8, f: 7 },
  { id: 'N5', a: 'N', t: 'Registrar gastos sacando foto a la boleta', cat: 'B', o: 5, f: 6 },
  { id: 'N6', a: 'N', t: 'Emisión automática de boleta de honorarios al cobrar', cat: 'C', o: 5, f: 4 },
  { id: 'N7', a: 'N', t: 'IA que predice cancelaciones y llama a lista de espera', cat: 'A', o: 9, f: 3 },
  { id: 'N8', a: 'N', t: 'Moneda propia InMotion para pagar sesiones', cat: 'C', o: 10, f: 1 },
  { id: 'N9', a: 'N', t: 'Reporte semanal al WhatsApp: “esta semana generaste $X”', cat: 'B', o: 7, f: 8 },

  { id: 'B1', a: 'B', t: 'Cobro con link o QR en el domicilio', cat: 'C', o: 3, f: 10 },
  { id: 'B2', a: 'B', t: 'Packs prepagados de 4 y 8 sesiones', cat: 'C', o: 4, f: 9 },
  { id: 'B3', a: 'B', t: 'Membresía mensual de mantención post-alta', cat: 'F', o: 6, f: 7 },
  { id: 'B4', a: 'B', t: 'Sistema integrado: agenda + cobro + dashboard en un solo lugar', cat: 'B', o: 8, f: 6 },
  { id: 'B5', a: 'B', t: 'Landing web InMotion con perfil profesional y reserva', cat: 'E', o: 4, f: 8 },
  { id: 'B6', a: 'B', t: 'Calendario de campañas preventivas para meses bajos', cat: 'E', o: 7, f: 7 },
  { id: 'B7', a: 'B', t: 'Precio preferente en horarios valle', cat: 'C', o: 7, f: 6 },
  { id: 'B8', a: 'B', t: 'Red de kinesiólogos por comisión administrada por Joselyn', cat: 'F', o: 8, f: 3 },
  { id: 'B9', a: 'B', t: 'Asistente IA que responde WhatsApp fuera de horario', cat: 'A', o: 7, f: 6 },
];

const umbral = 6;
const cuadrante = (i) => (i.o >= umbral ? '+O' : '-O') + (i.f >= umbral ? '+F' : '-F');

// Agrupación de las ideas con más potencial (cuadrante +O+F) en categorías
const grupos = [
  { t: 'Tablero financiero', cat: 'B', ideas: ['N1', 'N2', 'N3', 'N4', 'N9', 'B4'], sintesis: 'Un panel en el celular que muestra ingresos por canal, avance de la meta del mes, reservas por propósito y la proyección a 6 meses.' },
  { t: 'Agenda inteligente', cat: 'A', ideas: ['F2', 'F4', 'F8', 'B9'], sintesis: 'Reserva autónoma que respeta los tiempos de traslado, agrupa domicilios por sector y responde fuera de horario.' },
  { t: 'Relación y adherencia', cat: 'D', ideas: ['F5', 'C7', 'C6'], sintesis: 'Contacto cálido y automático: aviso de llegada, progreso visible y comunidad para pacientes grupales.' },
  { t: 'Ingreso estable', cat: 'C', ideas: ['B3', 'B6', 'B7'], sintesis: 'Recurrencia y campañas que aplanan la curva estacional de ingresos.' },
];

const conceptoNombre = 'Tablero InMotion';
const concepto = 'Un sistema de gestión para Joselyn que agenda y ordena sus sesiones por sí solo, registra cada cobro al terminar la atención y le muestra en el celular, de un vistazo, cuánto lleva, cuánto le falta para su meta y qué viene en los próximos 6 meses — para que su tiempo vuelva al trato 1:1 con sus pacientes.';

// ---------- SEMANA 7 · Metáfora y atributos ----------
const metafora = {
  titulo: 'Como el tablero y el copiloto de un auto de rally',
  bajada: 'Joselyn maneja (atiende a sus pacientes); el tablero le muestra velocidad y combustible (ingresos y meta), y el copiloto le lee la ruta que viene: las curvas (temporada baja), los tramos (agenda del día) y cuándo acelerar. Ella nunca suelta el volante.',
  porque: 'La metáfora nace de su propia rutina: recorre Rancagua en su vehículo entre domicilios. Un tablero no exige saber de mecánica para usarlo, igual que la solución no debe exigir saber de finanzas.',
  otras: [
    'Como un GPS: recalcula la ruta cuando algo cambia (cancelaciones).',
    'Como una alcancía con compartimentos: cada peso tiene un destino.',
  ],
};

const atributos = [
  { t: 'Anticipador', en: 'en el sentido de que avisa antes de la curva: proyecta los ingresos a 6 meses y alerta la temporada baja con tiempo para actuar.', nec: 'Ingresos estacionales sin proyección.', req: 'Proyección basada en historial y alertas tempranas.' },
  { t: 'Legible de un vistazo', en: 'en el sentido de un tablero: semáforo, números grandes y lenguaje cotidiano, sin jerga financiera.', nec: '“Siento que tengo cierto desorden o falta de educación” en lo económico.', req: 'Visualización simple, pensada para el celular.' },
  { t: 'Automático', en: 'en el sentido de que registra cobros, recordatorios y traslados sin que Joselyn tenga que digitar nada.', nec: 'Control manual en Excel y coordinación uno a uno por WhatsApp.', req: 'Integración agenda → cobro → registro.' },
  { t: 'Cercano', en: 'en el sentido de que la tecnología trabaja atrás para que ella tenga más tiempo y cercanía con cada paciente.', nec: '“Los trato como a mí me gustaría que me trataran.”', req: 'Mensajes con su voz y trato 1:1 intacto.' },
];

const promptsCollage = [
  'Close-up of a rally car dashboard at golden hour, analog speedometer and fuel gauge glowing orange, co-pilot hand holding a route notebook in soft focus, cinematic, warm light, 35mm photo --ar 4:3',
  'Female physiotherapist in navy scrubs checking a minimal finance dashboard on her smartphone inside her car before a home visit, traffic-light indicators on screen, natural daylight, editorial photo --ar 4:3',
  'Flat vector illustration of a winding road map of a Chilean city with pin markers grouped by neighborhood, a small car icon and a timeline of appointments, orange and navy palette, clean UI style --ar 4:3',
  'Minimal 3D icon set: traffic light, calendar with checkmark, coin split into three jars, WhatsApp-style chat bubble, soft clay render, orange #FF6B35 and navy #1B1F3B accents on off-white --ar 1:1',
];

module.exports = {
  equipo, contraparte, desafio, variables, referentes, tendencias,
  categorias, ideas, umbral, cuadrante, grupos, conceptoNombre, concepto,
  metafora, atributos, promptsCollage,
};
