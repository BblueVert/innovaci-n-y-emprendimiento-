# Innovación y Emprendimiento III — Proyecto HORIZON

Repositorio del trabajo de la asignatura **Innovación y Emprendimiento III** (FGIE03), carrera Diseño Digital, INACAP Rancagua.

## Equipo
- Francisco Ahumada
- Claudia Cifuentes
- Néstor Rivera
- Benjamín Vera Yáñez

## Caso de estudio
**Joselyn Toledo**, kinesióloga independiente — Centro Médico InMotion. Atiende en modalidad mixta: clínica (comisión 70/30) y atención particular a domicilio.

Objetivo del proyecto: diagnosticar su situación de negocio, identificar oportunidades y proponer mejoras, aplicando el **Ciclo de Innovación INACAP** (needfinding, entrevistas, matrices, redefinición del desafío).

## Estado actual

- **Semana 1** — Completa: Canvas de Preguntas (33 preguntas / 9 bloques BMC), Card Sorting (9 categorías emergentes), entrevista de usuario Ficha A/B (Joselyn), observación no participante (por autorreporte).
- **Semana 2** — Entrevista a experto/a Ficha A completa; Ficha B pendiente de completar con las respuestas de Catalina. Matriz PESTAL formateada en grid 2×3.
- **Semana 3** — En progreso: matrices de vaciado de hallazgos y estudio comparativo de antecedentes.

### Unidad 2 — Ideación de propuestas
- **Semana 6** — Ficha y Matriz de referentes (2.1.2.1 A/B): 9 casos de otros ámbitos (Calendly, Uber, YNAB, Fintual, Duolingo, Strava, Doctoralia, Smart Fit, Mercado Pago), 6 variables y 6 tendencias.
- **Semana 7** — Canvas brainstorming (36 ideas), Mapa de clasificación originalidad × factibilidad (16 ideas foco en 4 categorías), concepto directriz **Tablero InMotion** y Panel de metáforas y atributos (“tablero y copiloto de un auto de rally”: anticipador, legible, automático, cercano).

### Oportunidades seleccionadas
1. Sistema de agenda personalizado + dashboard financiero en tiempo real, para reemplazar herramientas genéricas de pago.
2. Construcción de presencia en Instagram y sitio web para InMotion, desde cero.

## Contenido de este repositorio

| Archivo | Descripción |
|---|---|
| `Evaluacion1_Informe_Consolidado.html` | Informe A4 consolidado — Evaluación N°1: Diagnóstico y Selección de Oportunidades. Contexto, metodología, guion de sondeo, card sorting, entrevista a Joselyn, mapa de síntesis, hallazgos. |
| `Entrevista_Experta_Cata.html` | Ficha de Entrevista a Experta (Instrumento 1.1.2.3) — guion de 10 preguntas para Catalina, validando el dolor de gestión de agenda/finanzas. Ficha B pendiente de completar con sus respuestas. |

Ambos documentos usan la identidad visual HORIZON (portada degradada, barra de acento, tipografía Arial Narrow/Courier New/Helvetica o Bebas Neue/DM Mono/Plus Jakarta Sans según el entregable) y están pensados para exportarse a PDF vía WeasyPrint, formato A4.

## Material de curso (`/material-curso`)

Toolkit oficial FGIE03 (INACAP), plantillas en blanco de los instrumentos y las infografías de apoyo, más el Canvas de Preguntas ya completado por el equipo:

| Archivo | Descripción |
|---|---|
| `FGIE03_U01S00_MANUAL_ESTUDIANTE_U01.pdf` | Manual del estudiante — Unidad 1 |
| `FGIE03_U01S00_TOOLKIT_U01.pdf` | Toolkit completo de técnicas e instrumentos, unidades 1–4 |
| `FGIE03_U01S02_ActividadS2.pdf` | Guía de actividad Semana 2 — Entrevista a experto/a |
| `FGIE03_AF_U01S01_Bitacora_de_avance.xlsx` | Bitácora de declaración de avance, semanas 1–4 |
| `Rubricas_FGIE03.xlsx` | Escalas de apreciación y rúbricas oficiales (ES01–ES04) |
| `Canvas_Preguntas_Kinesiologia_SPA.pdf` | Canvas de Preguntas completo del equipo (33 preguntas, 9 bloques BMC) |
| `1.1.2.1.A/B_..._entrevista_usuario.pdf` | Plantillas: preparación y pauta de entrevista a usuario |
| `1.1.2.2.A/B_..._observacion.pdf` | Plantillas: preparación y pauta de observación no participante AEIOU |
| `1.1.2.3.A/B_..._entrevista_experto.pdf` | Plantillas: preparación y pauta de entrevista a experto/a |
| `1.1.3.1_Matriz_PESTAL_plantilla.pdf` | Plantilla matriz PESTAL |
| `1.1.5.1.B_Matriz_antecedentes_plantilla.pdf` | Plantilla matriz comparativa de antecedentes |
| `*_infografia.pdf` | Infografías de apoyo con ejemplos aplicados por técnica (entrevista usuario/experto, observación, cuestionario, PESTEL, procesamiento de hallazgos, redefinición del desafío) |

## Unidad 2 (`/unidad-2`)

| Ruta | Descripción |
|---|---|
| `entregas/Act_online_sem6_Gx.docx` | Word institucional Semana 6 (Arial 12, títulos 16, justificado): portada, introducción, contraparte, instrumentos, conclusión individual, anexo |
| `entregas/Act_online_sem7_Gx.docx` | Word institucional Semana 7: brainstorming, clasificación, concepto directriz, panel de metáforas |
| `entregas/Bitacora_avance_U2_S6-S7.xlsx` | Bitácora de avance U2 con indicadores 1–6, 8 y 11 completos |
| `tableros/*.png` / `*.html` | Tableros estilo MIRO de cada instrumento (se insertan en los Word) |
| `_build/` | Fuente de contenido (`data.js`) y generador: `npm i docx playwright && node build.js` |
| `material/` | Toolkit, manual, pautas S6/S7 y bitácora en blanco de la U2 |

## Pendientes
- Completar Ficha B de la entrevista a Catalina con sus respuestas.
- Rellenar las plantillas en blanco (entrevista usuario/experto, observación, PESTAL, antecedentes) con la información real del caso.
- Terminar matrices de Semana 3 (vaciado de hallazgos, comparativo de antecedentes).
- Redefinición del desafío (Semana 4).
- Informe sumativo final cubriendo los seis criterios 1.1.1–1.1.6.
- U2: reemplazar `Gx` por el número de grupo, insertar fotos de entrevistas en el anexo y que cada integrante escriba su conclusión individual.
- U2: tabla de perfil de usuario y requerimientos (2.1.3.1–2.1.3.3), evaluación de factibilidad y cocreación con Joselyn (indicadores 7, 9, 10), panel de propuesta de valor (2.1.4.4).
