# Hallazgos · Retroalimentación del 12/11/2026 (Sercotec, clienta y docentes)

Reunión de Meet del 12 de noviembre (08:33, 40 min) con Mabel Aceituno Romero (Sercotec), la clienta Josselyn Toledo, el docente Ariel O’Nell y la docente Ana Luisa Aguilera. Se revisaron cuatro propuestas de distintas secciones: una app de gestión, una planilla Excel, un modelo de programas grupales y la propuesta “Copiloto” (nuestra línea de trabajo, prototipos v1 y v2), leída entre el minuto 30:49 y el 35:29.

Fuente: `Transcripcion_reunion_2026-11-12.md` (citas textuales con minuto de la grabación).

## Hallazgos de la clienta

| # | Hallazgo | Cita | Min. | Implicancia |
|---|---|---|---|---|
| RF1 | No conoce una herramienta que haga esto | “No. Así como solamente por pauta, por agenda, por horario, pero nada más que eso.” | 12:22 | Diferenciación confirmada: las apps que usa solo agendan. |
| RF2 | Ya registra todo cada noche en el teléfono | “Cada noche anoto todo… la ganancia, lo que gasto en bencina durante el día… cuántas sesiones hice y cuánto gané en cada sesión.” | 36:25 | La app debe reemplazar ese hábito nocturno, no crear uno nuevo. |
| RF3 | Usa dos agendas: AgendaPro y una agenda médica | “Tengo dos tipos de agenda, la AgendaPro y la [agenda médica digital], tanto para personal y en clínica.” | 36:25 | Integrar AgendaPro antes que Google Calendar. |
| RF4 | En la clínica factura un monto mensual | “En clínica ya dejo como un monto fijo porque al final yo hago la factura y veo el monto total del mes.” | 36:25 | Modo clínica por factura mensual, además del cálculo por atención. |
| RF5 | Quiere saber qué canal es más rentable | “Si sale más rentable en clínica o en domicilio… en clínica puedo atender dos, tres pacientes por hora… a domicilio atiendo solo una persona, con el viaje incluido.” | 19:21 | Ganancia por hora por canal como métrica central. |
| RF6 | El traslado le cuesta tiempo, no solo bencina | “Agua Buena… queda para la precordillera… es muy malo el camino… me demoro como 25, 30 minutos.” | 20:47 | Incluir el tiempo de viaje como costo (hora profesional) y una tarifa por tramo. |
| RF7 | Hace más que kinesiología | “Trabajo tanto en piscina. Yo soy psicomotricista acuática… los entrenamientos personalizados que hago en mi propio [gimnasio].” | 05:56 · 23:27 | Varios servicios y lugares con costos distintos: clínica, domicilio, piscina, gimnasio. |
| RF8 | Su territorio es San Fernando y alrededores | San Fernando, Agua Buena, Las Cabras (tres pacientes en clínica) y la piscina temperada camino a Roma. | 07:59 · 20:47 · 28:17 | Ajustar rutas y ejemplos a su territorio real (no solo Rancagua–Machalí). |
| RF9 | En la región se valora poco lo especializado | “La gente no sabe lo que es, ni sabe lo que vale realmente… encuentra que es caro.” | 06:42 | Comunicar el valor del servicio (comprobante, explicación) y cuidar el precio de la app. |
| RF10 | Grupal sí, pero preventivo | Lo terapéutico es individual; ve “fantástico” hacer clases grupales para adultos mayores en Las Cabras, que “andan buscando cositas para hacer en grupo”. | 23:27 · 28:17 | Módulo de clases grupales (cupos, asistencia, cobro por persona) como acción de la proyección. |
| RF11 | Sus clientes manejan sus tiempos | “La mayoría son empresarios, independientes, manejan sus tiempos.” | 05:56 | Indicio favorable para la ventana de llegada de 30 min (H5); se valida igual con pacientes. |
| RF12 | Interés directo en la app | “Me encantaría conocerla.” · “Felicitaciones a sus alumnos.” | 13:31 · 38:35 | Disposición a probar: base para la sesión con la usuaria. |

## Sugerencias de Sercotec y docentes

| Quién | Sugerencia | Min. |
|---|---|---|
| Ariel O’Nell | Bajo o cero costo, usable en teléfono, tablet y computador; todo parametrizado: ella ingresa datos y la app entrega el cálculo, con resúmenes semanales y mensuales que sirvan a la parte contable. | 10:47 |
| Ariel O’Nell | Costo oculto: la hora hombre del traslado. Permite definir el valor exacto de su hora profesional. | 19:45 |
| Ariel O’Nell | Las propuestas no son excluyentes: puede combinar una app, una planilla y un modelo grupal. | 17:33 |
| Mabel Aceituno (Sercotec) | Que los estudiantes estimen cuánto costaría la solución. | 12:30 |
| Mabel Aceituno (Sercotec) | Analizar por tipo de cliente y lugar (particular vs. clínica, por semana y mes) para decidir dónde enfocarse. | 18:23 |
| Mabel Aceituno (Sercotec) | No toda cita agendada se concreta; la bencina sube: conviene partir con valores fijos estimados. | 15:12 · 33:31 |

## Patrones

| Patrón | Evidencia | Qué significa |
|---|---|---|
| Rentabilidad por canal y por hora | RF5 · RF6 · RF7 · Ariel 19:45 | La pregunta de fondo no es “cuánto gané” sino “qué me conviene”: clínica, domicilio, piscina o grupo. |
| El hábito ya existe | RF2 · RF3 · RF4 | Josselyn ya registra cada noche y usa AgendaPro: la app gana si se monta sobre eso y lo hace en segundos. |
| El territorio define el costo | RF6 · RF8 · Mabel 33:31 | Caminos rurales y de precordillera: el traslado pesa más en tiempo que en bencina. |
| Diversificar ingresos | RF7 · RF10 · Ariel 26:57 | Clases grupales preventivas para adultos mayores son la acción más concreta para los meses bajos. |
| Bajo costo y complementariedad | Ariel 10:47 · 17:33 · Mabel 12:30 | La solución debe ser barata, multi-dispositivo y exportable a Excel para convivir con otras propuestas. |

## Cambios a la propuesta (prototipo v3)

| # | Cambio | Origen | Dónde |
|---|---|---|---|
| 1 | Integración con AgendaPro (o su exportación) y la agenda de la clínica; Google Calendar queda como alternativa | RF3 | Integración · MVP |
| 2 | “Ganancia por hora” por canal: clínica, domicilio, piscina, gimnasio y grupal | RF5 · RF7 | Tablero · MVP |
| 3 | Tiempo de traslado como costo (valor de la hora profesional) y tarifa sugerida por tramo | RF6 · Ariel | Ruta · MVP |
| 4 | Modo clínica por factura mensual (monto fijo del mes) además del cálculo por atención | RF4 | Registro · MVP |
| 5 | Servicios configurables con su propio costo (piscina, gimnasio, domicilio, clínica) | RF7 | Ajustes · MVP |
| 6 | Módulo de clases grupales: cupos, asistencia y cobro por persona; aparece como acción en la proyección | RF10 | Proyección · fase 2 |
| 7 | Reportes semanales y mensuales por tipo de cliente y lugar, exportables a Excel o Google Sheets | Mabel · Ariel | Reportes · MVP |
| 8 | Ejemplos y rutas en su territorio: San Fernando, Agua Buena, Las Cabras | RF8 | Prototipo v3 |
| 9 | Costo estimado de la solución visible en la propuesta (MVP con herramientas de bajo costo) | Mabel 12:30 | Propuesta |

## Otras propuestas revisadas en la reunión (de otras secciones)

- **App de gestión integral** (09:00–13:37): organizar pacientes y atenciones, centralizar finanzas; Mabel pidió estimar su costo.
- **Planilla Excel de gestión kinesiológica** (14:07–17:33): listas desplegables, ingresos dependientes/independientes; requiere alimentarla a mano. Ariel: complementaria a una app.
- **Programas grupales de movimiento y bienestar** (21:41–29:43): convenios con municipios y empresas. Josselyn: lo terapéutico es individual; lo grupal preventivo para adultos mayores sí le interesa.
- **Copiloto (nuestra línea)** (30:49–35:29): problema, prototipos v1/v2, costo referencial $20.000–25.000/mes e hipótesis; Josselyn: “eso hago yo igual en el teléfono… simplemente no tengo esa aplicación”.
