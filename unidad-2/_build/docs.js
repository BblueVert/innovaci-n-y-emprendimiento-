// Genera los Word de entrega S6 y S7 con el formato institucional de la pauta:
// Arial 12, títulos 16, texto justificado; portada, introducción, contraparte,
// instrumentos (imágenes + comentarios), conclusión individual y anexo.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, HeadingLevel, PageBreak, PageOrientation,
  LevelFormat, BorderStyle, Footer, PageNumber,
} = require('docx');
const D = require('./data');

const FONT = 'Arial';
const NAVY = '1B1F3B';
const ORANGE = 'FF6B35';
const A4 = { width: 11906, height: 16838 };
const MARGIN = 1134; // 2 cm
const PORTRAIT_W = A4.width - 2 * MARGIN; // 9638 DXA
const LANDSCAPE_W = A4.height - 2 * MARGIN; // 14570 DXA

const P = (text, opts = {}) => new Paragraph({
  alignment: opts.align ?? AlignmentType.JUSTIFIED,
  spacing: { after: opts.after ?? 160, line: 300 },
  ...(opts.bullet ? { numbering: { reference: 'bullets', level: 0 } } : {}),
  children: (Array.isArray(text) ? text : [text]).map((t) => (typeof t === 'string' ? new TextRun(t) : t)),
});
const B = (t) => new TextRun({ text: t, bold: true });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

function image(file, widthDxa) {
  const buf = fs.readFileSync(file);
  const w = buf.readUInt32BE(16);
  const h = buf.readUInt32BE(20);
  const px = Math.round((widthDxa / 1440) * 96);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new ImageRun({ type: 'png', data: buf, transformation: { width: px, height: Math.round((px * h) / w) } })],
  });
}
const caption = (t) => new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 200 },
  children: [new TextRun({ text: t, italics: true, size: 20, color: '555555' })],
});

function table(rows, widths, { header = true } = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF' };
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: header && ri === 0,
      children: r.map((c, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        borders: { top: border, bottom: border, left: border, right: border },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        shading: header && ri === 0 ? { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' }
          : (!header && ci === 0 ? { type: ShadingType.CLEAR, fill: 'F2F2F2', color: 'auto' } : undefined),
        children: [new Paragraph({
          alignment: AlignmentType.LEFT,
          children: [new TextRun({ text: c, size: 20, bold: (header && ri === 0) || (!header && ci === 0), color: header && ri === 0 ? 'FFFFFF' : undefined })],
        })],
      })),
    })),
  });
}

function portada({ codigo, semana, instrumentos }) {
  const line = (t, o = {}) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: o.after ?? 120 }, children: [new TextRun({ text: t, ...o })] });
  return [
    line('INACAP Sede Rancagua · Formación General', { size: 22, color: '555555', after: 60 }),
    line('Innovación y Emprendimiento III (FGIE03)', { size: 22, color: '555555', after: 1600 }),
    line('Actividad Online', { size: 28, color: ORANGE, bold: true }),
    line('Ideación de Propuestas', { size: 44, bold: true, color: NAVY }),
    line(`${semana} · Unidad 2`, { size: 28, bold: true, after: 240 }),
    ...instrumentos.map((i) => line(i, { size: 24, after: 60 })),
    line(`Archivo: ${codigo}`, { size: 20, color: '777777', after: 1400 }),
    line('Integrantes', { bold: true, size: 24 }),
    ...D.equipo.map((m) => line(m.nombre + (m.secretario ? ' — Secretario técnico' : ''), { size: 24, after: 40, color: m.secretario ? 'C00000' : undefined, bold: !!m.secretario })),
    line('', { after: 600 }),
    line('Caso: Joselyn Toledo — Centro Médico InMotion', { size: 22 }),
    line('Rancagua, septiembre de 2026', { size: 22 }),
    pageBreak(),
  ];
}

function contraparte() {
  const c = D.contraparte;
  return [
    H1('2. Datos básicos de la contraparte'),
    table([
      ['Contraparte', `${c.nombre} — ${c.negocio}`],
      ['Ubicación', c.ubicacion],
      ['Encargada', c.encargado],
      ['Actividad económica', c.actividad],
      ['Modelo de atención', c.modelo],
      ['Antigüedad y carga', c.antiguedad],
      ['Dolor principal (UA1)', c.dolor],
    ], [2600, PORTRAIT_W - 2600], { header: false }),
    P(''),
    P([B('Desafío de trabajo (redefinido en UA1): '), D.desafio]),
  ];
}

function conclusionIndividual(texto) {
  return [
    H1('4. Conclusión individual'),
    P([B('Benjamín Vera Yáñez. '), new TextRun({ text: '(Cada integrante reemplaza esta sección por su propia conclusión antes de subir su archivo a AAI.)', italics: true, color: '777777' })]),
    ...texto.map((t) => P(t)),
  ];
}

function anexo(extra = []) {
  return [
    H1('5. Anexo'),
    H2('5.1 Registro de entrevistas'),
    P('Fotografías de la entrevista en profundidad a Joselyn Toledo (Clase 3) y de la entrevista a la experta Catalina, realizadas en la Unidad 1 y utilizadas como base para esta actividad.'),
    P([new TextRun({ text: '[Insertar aquí las fotografías de las entrevistas]', italics: true, color: 'C00000' })], { align: AlignmentType.CENTER }),
    ...extra,
  ];
}

const baseStyles = {
  default: { document: { run: { font: FONT, size: 24 } } },
  paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 32, bold: true, font: FONT, color: NAVY }, paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 28, bold: true, font: FONT, color: ORANGE }, paragraph: { spacing: { before: 200, after: 140 }, outlineLevel: 1 } },
  ],
};
const numbering = { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] };

const footer = (codigo) => ({
  default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
    new TextRun({ text: `${codigo} · Equipo HORIZON · pág. `, size: 18, color: '777777' }),
    new TextRun({ children: [PageNumber.CURRENT], size: 18, color: '777777' }),
  ] })] }),
});
const portrait = (codigo, children) => ({ properties: { page: { size: A4, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } }, footers: footer(codigo), children });
const landscape = (codigo, children) => ({ properties: { page: { size: { ...A4, orientation: PageOrientation.LANDSCAPE }, margin: { top: 900, bottom: 900, left: MARGIN, right: MARGIN } } }, footers: footer(codigo), children });

// ======================= SEMANA 6 =======================
function semana6(tab) {
  const code = 'Act_online_sem6_Gx';
  const img = (f) => image(path.join(tab, f + '.png'), LANDSCAPE_W);
  return new Document({
    creator: 'Equipo HORIZON', title: 'Semana 6 — Matriz de referentes', styles: baseStyles, numbering,
    sections: [
      portrait(code, [
        ...portada({ codigo: code, semana: 'Semana 6', instrumentos: ['Instrumento 2.1.2.1.A — Ficha de referentes', 'Instrumento 2.1.2.1.B — Matriz de referentes'] }),
        H1('1. Introducción'),
        P('La Unidad 2 del Ciclo de Innovación INACAP inicia la fase de ideación. Antes de generar ideas, el equipo buscó inspiración fuera del rubro de la kinesiología: el estudio comparativo de referentes analiza proyectos de otras categorías para identificar elementos innovadores que puedan trasladarse al desafío de nuestra contraparte.'),
        P('Esta actividad corresponde al criterio 2.1.2 (“Analiza casos existentes que sirvan de inspiración para la propuesta de solución a la problemática definida”). Se seleccionaron 9 casos, dentro del rango de 8 a 10 que recomienda el toolkit, a partir de los hallazgos de la Unidad 1: la entrevista en profundidad a Joselyn, la entrevista a la experta Catalina, la matriz PESTAL y el estudio de antecedentes.'),
        P('Objetivo de la actividad: identificar tendencias y elementos novedosos en soluciones de otros ámbitos (movilidad, finanzas, educación, deporte, fitness y pagos) que inspiren una propuesta para ordenar la agenda y las finanzas de Joselyn.'),
        ...contraparte(),
        pageBreak(),
        H1('3. Instrumentos'),
        H2('3.1 Criterios de selección y variables de análisis'),
        P('Los casos se eligieron con tres filtros: (1) resolver en otro rubro un problema análogo al de Joselyn (agenda, control del dinero, cobro o fidelización); (2) tener presencia o uso en Chile, o ser una referencia global reconocida; (3) aportar diversidad: servicios, productos digitales y modelos de negocio distintos.'),
        P('Las variables de la matriz se derivan directamente del dolor detectado en la UA1:'),
        ...D.variables.map((v) => P([B(v.t + ': '), {
          agenda: 'cómo el caso resuelve la reserva, disponibilidad y coordinación de horarios.',
          finanzas: 'qué visibilidad entrega sobre el dinero (registro, reportes, proyección).',
          cobro: 'cómo se cobra y qué fricción elimina.',
          relacion: 'qué mecanismos usa para mantener y fidelizar al usuario.',
          novedad: 'el elemento concreto que podría trasladarse al caso InMotion.',
          tendencia: 'la tendencia social, tecnológica o económica que representa.',
        }[v.k]], { bullet: true, after: 60 })),
      ]),
      landscape(code, [
        H2('3.2 Instrumento 2.1.2.1.A — Fichas de referentes'),
        img('S6_01_fichas_referentes'),
        caption('Figura 1. Fichas de los 9 referentes: nombre, ámbito, descripción, aspecto relevante, fuente y tendencia. Elaboración propia en MIRO.'),
      ]),
      portrait(code, [
        P([B('Llenado: '), 'cada integrante investigó y fichó casos en MIRO con la estructura del toolkit (nombre, imagen, fuente, descripción y aspectos relevantes). En plenario se validó que ningún caso fuera del mismo rubro de la contraparte, salvo Doctoralia, que se mantuvo por su modelo de reputación digital y no por ser un servicio de kinesiología.']),
        P([B('Resultado: '), '9 fichas completas que cubren 7 ámbitos distintos. Se descartaron Booksy y Fresha por ser software de agenda del mismo rubro (bienestar), lo que habría limitado la mirada.']),
      ]),
      landscape(code, [
        H2('3.3 Instrumento 2.1.2.1.B — Matriz de referentes'),
        img('S6_02_matriz_referentes'),
        caption('Figura 2. Matriz comparativa de los 9 referentes según las 6 variables de análisis. La columna naranja destaca el elemento novedoso trasladable al desafío.'),
      ]),
      portrait(code, [
        P([B('Llenado: '), 'se vació la información de las fichas en la matriz, caso por caso y variable por variable. Las celdas con “—” indican que el caso no resuelve esa variable, lo que también es información: ningún referente resuelve por sí solo las cuatro dimensiones del problema de Joselyn.']),
        P([B('Análisis: '), 'los casos más completos para el desafío son Uber y Calendly (agenda + cobro + relación). Los casos financieros (YNAB, Fintual) aportan la lógica de visualización y separación del dinero, pero no la operación. Duolingo y Strava no tocan la gestión, pero aportan cómo sostener la relación con el paciente entre sesiones.']),
      ]),
      landscape(code, [
        H2('3.4 Tendencias identificadas'),
        img('S6_03_tendencias'),
        caption('Figura 3. Seis tendencias transversales detectadas en los referentes y su lectura para el caso InMotion.'),
      ]),
      portrait(code, [
        H2('3.5 Resultado y conclusiones del instrumento'),
        P('Elementos novedosos seleccionados para llevar a la ideación:'),
        P([B('Del traslado: '), 'bloques de tiempo automáticos entre domicilios (Calendly) y aviso “voy en camino” (Uber).'], { bullet: true, after: 60 }),
        P([B('Del dinero: '), 'separar cada ingreso por propósito (YNAB) y mostrar la meta y su proyección en lenguaje cotidiano (Fintual).'], { bullet: true, after: 60 }),
        P([B('Del cobro: '), 'pago con link o QR que alimenta automáticamente el registro (Mercado Pago).'], { bullet: true, after: 60 }),
        P([B('De la estabilidad: '), 'packs y membresías que generan ingreso recurrente (Smart Fit).'], { bullet: true, after: 60 }),
        P([B('De la relación: '), 'progreso visible y rachas para los ejercicios en casa (Strava, Duolingo) y reseñas verificadas como canal de captación (Doctoralia).'], { bullet: true }),
        P('Conclusión: la tendencia dominante es que el dato se genera solo, como consecuencia de la operación (reservar, cobrar), y se presenta de forma visual y simple. Para Joselyn esto significa que la solución no debe pedirle “ordenar mejor su Excel”, sino eliminar la digitación. Esta conclusión orienta directamente el brainstorming de la Semana 7.'),
        ...conclusionIndividual([
          'Hacer el estudio de referentes me cambió la forma de mirar el problema. Al principio buscábamos “apps para kinesiólogos” y todas se parecían. Cuando nos obligamos a mirar movilidad, finanzas personales o deporte, aparecieron ideas que ningún software del rubro ofrece, como separar el dinero por propósito o avisar la llegada al domicilio.',
          'Lo más valioso fue definir las variables antes de fichar los casos: nos obligó a analizar cada referente contra el dolor real de Joselyn y no solo a describirlo. También aprendí que las celdas vacías de la matriz dicen mucho, porque muestran que la oportunidad está en integrar lo que hoy existe por separado.',
          'Como mejora de gestión para las siguientes semanas, repartir los casos por integrante con un formato de ficha común desde el inicio nos habría ahorrado tiempo de consolidación como secretario técnico.',
        ]),
        ...anexo(),
      ]),
    ],
  });
}

// ======================= SEMANA 7 =======================
function semana7(tab) {
  const code = 'Act_online_sem7_Gx';
  const img = (f) => image(path.join(tab, f + '.png'), LANDSCAPE_W);
  const cnt = (q) => D.ideas.filter((i) => D.cuadrante(i) === q).length;
  const ideasPor = D.equipo.map((m) => `${m.nombre.split(' ')[0]}: ${D.ideas.filter((i) => i.a === m.key).length}`).join(' · ');
  return new Document({
    creator: 'Equipo HORIZON', title: 'Semana 7 — Brainstorming, clasificación y metáforas', styles: baseStyles, numbering,
    sections: [
      portrait(code, [
        ...portada({ codigo: code, semana: 'Semana 7', instrumentos: ['Instrumento 2.1.4.1 — Canvas brainstorming', 'Instrumento 2.1.4.2 — Mapa de clasificación de ideas', 'Instrumento 2.1.4.3 — Panel de metáforas y atributos'] }),
        H1('1. Introducción'),
        P('Con las tendencias y elementos novedosos obtenidos del estudio de referentes (Semana 6), el equipo entró en la generación de ideas del Ciclo de Innovación INACAP. Esta semana se aplicaron tres instrumentos encadenados: un brainstorming para producir la mayor cantidad de ideas posible, un mapa de clasificación para filtrarlas por originalidad y factibilidad, y un panel de metáforas y atributos para conceptualizar la idea seleccionada.'),
        P('La actividad responde a los criterios 2.1.1 (aplica la fase de generación de ideas) y 2.1.4 (sintetiza ideas que respondan a los requerimientos del problema y a las variables del entorno).'),
        ...contraparte(),
        pageBreak(),
        H1('3. Instrumentos'),
        H2('3.1 Instrumento 2.1.4.1 — Canvas brainstorming'),
        P([B('Objetivo: '), 'generar el mayor número de ideas de solución para el desafío, privilegiando la cantidad por sobre la calidad y sin juzgar.']),
        P([B('Llenado: '), 'se destinaron los primeros minutos a revisar y ajustar el desafío con los hallazgos de la UA1 y las tendencias de la Semana 6. Luego se realizó una sesión de 45 minutos en MIRO, con el desafío escrito al centro del canvas. Cada integrante usó un color de post-it propio (una idea por post-it) para registrar su autoría. El secretario técnico cronometró la sesión y cuidó la regla de no juzgar.']),
      ]),
      landscape(code, [
        img('S7_01_canvas_brainstorming'),
        caption(`Figura 1. Canvas brainstorming con ${D.ideas.length} ideas (${ideasPor}). Elaboración propia en MIRO.`),
      ]),
      portrait(code, [
        P([B('Resultado: '), `${D.ideas.length} ideas; cada integrante aportó 9, por sobre el mínimo de 3 que exige la pauta. Surgieron desde ideas simples (recordatorio 24 h antes) hasta ideas “locas” que se registraron igual (moneda propia InMotion, reserva por asistente de voz), coherente con la lógica de la técnica.`]),
        H2('3.2 Instrumento 2.1.4.2 — Mapa de clasificación de ideas'),
        P([B('Objetivo: '), 'ordenar todas las ideas del brainstorming según los ejes de originalidad y factibilidad, para identificar las que tienen más potencial.']),
        P([B('Llenado: '), 'antes de mover los post-it se acordaron los criterios de cada eje. Originalidad: qué tan distinta es la idea frente a lo que hoy usa Joselyn (Excel, calendario, WhatsApp) y su competencia. Factibilidad: si puede implementarse con herramientas existentes, bajo presupuesto y en aproximadamente un mes. Cada idea se puntuó de 1 a 10 en ambos ejes por consenso y se ubicó en su cuadrante (umbral: 6 puntos).']),
      ]),
      landscape(code, [
        img('S7_02_mapa_clasificacion'),
        caption('Figura 2. Mapa de clasificación de ideas en los cuadrantes originalidad × factibilidad. El cuadrante destacado concentra las ideas con más potencial.'),
      ]),
      portrait(code, [
        P([B('Resultado de la clasificación:')]),
        table([
          ['Cuadrante', 'N° ideas', 'Decisión'],
          ['+ Original / + Factible', String(cnt('+O+F')), 'Foco de la solución: se agrupan en categorías.'],
          ['− Original / + Factible', String(cnt('-O+F')), 'Base operativa: se incorporan como funciones mínimas (link de agenda, cobro por QR, packs).'],
          ['+ Original / − Factible', String(cnt('+O-F')), 'Banco de ideas futuras (por ejemplo, red de kinesiólogos por comisión, cuando el negocio escale).'],
          ['− Original / − Factible', String(cnt('-O-F')), 'Descartadas.'],
        ], [3000, 1300, PORTRAIT_W - 4300]),
        P(''),
        P('Las ideas del cuadrante “+ original / + factible” se agruparon en cuatro categorías y se sintetizaron en un concepto directriz:'),
      ]),
      landscape(code, [
        img('S7_03_categorias_concepto'),
        caption('Figura 3. Categorías de las ideas con más potencial y concepto directriz resultante.'),
      ]),
      portrait(code, [
        P([B(`Concepto directriz — ${D.conceptoNombre}: `), D.concepto]),
        P('El concepto integra la mayoría de las tendencias de la Semana 6: autoservicio (agenda inteligente), datos simples y proyección visual (tablero financiero), pagos con registro automático (cobro integrado), recurrencia (ingreso estable) y adherencia (relación). Así responde al dolor financiero sin sacrificar el diferenciador de Joselyn: la atención personalizada 1:1.'),
        pageBreak(),
        H2('3.3 Instrumento 2.1.4.3 — Panel de metáforas y atributos'),
        P([B('Objetivo: '), 'conceptualizar la idea seleccionada mediante una analogía reconocible y definir los atributos que deberá tener la solución, para mantener la coherencia durante el prototipado, testeo e iteración.']),
        P([B('Llenado: '), 'se propusieron tres metáforas y se eligió por consenso la que mejor conectaba con la rutina real de la usuaria. Luego se definieron cuatro atributos con su bajada (“… en el sentido de …”), vinculando cada uno con una necesidad de la UA1 y un requerimiento de la solución. Finalmente se construyó el collage que representa visualmente la metáfora.']),
      ]),
      landscape(code, [
        img('S7_04_panel_metaforas'),
        caption('Figura 4. Panel de metáforas y atributos: metáfora seleccionada, collage y cuatro atributos con su bajada a necesidades y requerimientos.'),
      ]),
      portrait(code, [
        P([B(`Metáfora: “${D.metafora.titulo}”. `), D.metafora.bajada]),
        P(D.metafora.porque),
        table([
          ['Atributo', 'Bajada (“en el sentido de…”)', 'Necesidad (UA1)', 'Requerimiento'],
          ...D.atributos.map((a) => [a.t, a.en.replace(/^en el sentido de /, ''), a.nec, a.req]),
        ], [1700, 3538, 2200, 2200]),
        P(''),
        H2('3.4 Resultado y conclusiones de los instrumentos'),
        P(`El proceso convirtió ${D.ideas.length} ideas dispersas en un concepto único y en cuatro atributos que servirán como criterios de diseño en la Unidad 3: cualquier prototipo del ${D.conceptoNombre} deberá ser anticipador, legible de un vistazo, automático y cercano. Si una función no cumple alguno de estos atributos, no entra en el prototipo.`),
        P('Próximo paso: evaluar la factibilidad técnica y de recursos de la idea seleccionada, validar la metáfora y los atributos con Joselyn (cocreación) y construir el panel de propuesta de valor y métricas claves (2.1.4.4).'),
        ...conclusionIndividual([
          'El brainstorming me enseñó a separar el momento de generar ideas del momento de evaluarlas. Cuando dejamos de discutir cada post-it, las ideas empezaron a salir más rápido y varias de las que parecían absurdas terminaron inspirando otras más aterrizadas, como la moneda propia, que derivó en la idea de los packs prepagados.',
          'El mapa de clasificación fue el paso más difícil, porque obligó al equipo a acordar qué significaba “factible” antes de mover los post-it. Definir ese criterio en conjunto (herramientas existentes, bajo costo y un mes) evitó discusiones posteriores y dejó un filtro claro.',
          'La metáfora del tablero y el copiloto fue la mejor forma de explicar la idea a alguien que no es del área: cualquiera entiende que un tablero muestra lo importante sin saber de mecánica. Para las próximas unidades, validar la metáfora directamente con Joselyn nos permitirá confirmar que habla su idioma.',
        ]),
        ...anexo([
          H2('5.2 Prompts de IA para el collage (opcional)'),
          P('Si se desea reemplazar el collage ilustrado por imágenes fotográficas, estos son los prompts usados como referencia visual (Midjourney / Firefly / DALL·E):'),
          ...D.promptsCollage.map((p) => P(p, { bullet: true, after: 80, align: AlignmentType.LEFT })),
        ]),
      ]),
    ],
  });
}

async function build(tab, outDir) {
  fs.mkdirSync(outDir, { recursive: true });
  const out = [
    ['Act_online_sem6_Gx.docx', semana6(tab)],
    ['Act_online_sem7_Gx.docx', semana7(tab)],
  ];
  for (const [f, doc] of out) fs.writeFileSync(path.join(outDir, f), await Packer.toBuffer(doc));
  return out.map(([f]) => path.join(outDir, f));
}

module.exports = { build };
