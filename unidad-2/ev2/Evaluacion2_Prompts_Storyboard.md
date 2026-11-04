# EV2 — Prompts de storyboard para Google Flow

Secuencias de situaciones para ilustrar cómo **Joselyn** (nuestra usuaria) y **sus pacientes** interactúan con **Copiloto Kine**. Son 3 storyboards de 6 viñetas cada uno, más un banco de 6 situaciones extra:

| Storyboard | Lámina | Archivos |
|---|---|---|
| V1 · Joselyn con el alcance mínimo | 11 | `v1-01.png` … `v1-06.png` |
| V2 · Joselyn con la versión iterada | 14 | `v2-01.png` … `v2-06.png` |
| V2 · El paciente | 15 | `p-01.png` … `p-06.png` |
| Banco de situaciones extra | — | `x-01.png` … `x-06.png` |

Las pantallas de la app que aparecen en cada escena existen de verdad en el prototipo (`unidad-2/app`). La columna **Pantalla** indica cuál es, por si quieren usar la captura como referencia.

---

## 1. Cómo trabajarlo en Google Flow

1. **Crear un proyecto** en Flow llamado `Copiloto Kine · Storyboard EV2`.
2. **Generar primero los personajes** (sección 3), en formato 1:1, y guardarlos como **ingredientes**. Así Joselyn, don Luis y Camila mantienen la misma cara, ropa y colores en todas las viñetas.
3. Para cada viñeta, usar **"Ingredientes a imagen"** (o *Frames/Ingredients*). Se adjuntan los personajes que aparecen y se pega el prompt de la escena.
4. **Formato 16:9 horizontal.** La lámina recorta la imagen a una franja más ancha (≈ 2,5:1), así que la acción debe quedar en la **franja central** y con aire arriba y abajo. Cada prompt ya lo pide.
5. **Sin texto en las imágenes.** Los títulos y textos van en la lámina. Si la IA dibuja letras en la pantalla del celular, regenerar o pedir "blank abstract UI shapes".
6. Generar 2–4 variantes por viñeta y elegir la más clara. Mantener la misma **seed** o el mismo hilo de generación entre viñetas del mismo storyboard.
7. **Guardar** con el nombre exacto en `unidad-2/ev2/img/storyboard/` (por ejemplo `v2-03.png`) y volver a exportar la presentación:
   ```
   node unidad-2/_build/render_presentacion.js
   ```
   La lámina usa la imagen si existe. Si no, muestra la ilustración vectorial actual.
8. **Opcional:** cada escena sirve también como *frame* inicial para un clip corto de Veo. En la sección 6 hay una línea de movimiento sugerida para animarlas.

---

## 2. Bloque de estilo (pegar al final de cada prompt)

Es el mismo lenguaje de las ilustraciones de la EV1 y del informe EV2 (`img/02-caso.jpg`, `img/07-oficina-movil.jpg`):

```
Style: flat vector editorial illustration, clean geometric shapes, soft subtle shadows, no outlines or very thin ones, warm palette of orange #FF6B35, coral #E8637A, deep purple #7B3FA0, amber #FFB347 and off-white #F8F7FF, calm and friendly mood, Chilean urban setting (Rancagua / Machalí, low houses, the Andes softly in the background when outdoors), wide 16:9 composition with the main action centered in the middle horizontal band and empty space above and below, phone screens show only blank abstract UI blocks in orange and purple, absolutely no text, no letters, no numbers, no logos, no brand names.
```

---

## 3. Personajes (ingredientes)

Generarlos primero, en 1:1, fondo liso `#F8F7FF`, cuerpo entero, de frente y 3/4.

### J · Joselyn Toledo — kinesióloga (usuaria)
```
Character sheet of a Chilean female physiotherapist, around 30 years old, warm light-brown skin, dark brown hair tied in a low bun, friendly confident expression, wearing an orange #FF6B35 scrub top with a small white name tag, dark purple #4A3580 scrub pants and white sneakers, carrying a purple and orange equipment bag with a foam roller, smartphone in one hand, full body front view and three-quarter view side by side, plain off-white background #F8F7FF. [Bloque de estilo]
```

### L · Don Luis Muñoz — paciente adulto mayor (domicilio)
```
Character sheet of a 72-year-old Chilean man, short grey hair, kind face, slightly hunched posture from lower back pain, wearing a beige cardigan over a light blue shirt, grey trousers and house slippers, holding a basic smartphone with large text, full body front view and three-quarter view, plain off-white background #F8F7FF. [Bloque de estilo]
```

### C · Camila Fuentes — paciente joven (ex lesión de tobillo)
```
Character sheet of a 28-year-old Chilean woman, long dark hair in a high ponytail, athletic build, wearing a coral #E8637A sports jacket, black leggings and running shoes, smartphone in hand, energetic friendly expression, full body front view and three-quarter view, plain off-white background #F8F7FF. [Bloque de estilo]
```

### Escenarios de apoyo (opcionales, también como ingredientes)
```
Interior of a small clean physiotherapy box at a medical center: treatment table with purple cushion, shelves with rehab equipment, window with soft daylight, orange accents. [Bloque de estilo]
```
```
Exterior of a modest single-story Chilean house in Machalí with a small front garden, a small orange hatchback parked in front, the Andes mountains softly in the background, late morning light. [Bloque de estilo]
```

---

## 4. Storyboards

### 4.1 Storyboard V1 — Joselyn con el alcance mínimo (lámina 11)
Hilo: el tablero ya conecta agenda y ganancia, pero todavía quedan dolores sin resolver (impuestos, rutas, qué hacer en meses bajos).

| # | Archivo | Situación | Pantalla del prototipo | Ingredientes |
|---|---|---|---|---|
| 1 | `v1-01.png` | **Hoy, el Excel de noche.** 23:10. Joselyn, cansada en la mesa de su casa, cuadra ingresos en un notebook con una planilla y el celular lleno de chats. | — (situación actual) | J |
| 2 | `v1-02.png` | **Conecta su agenda.** En una pausa en la clínica, sentada en el box, conecta su calendario y define sus reglas en 10 minutos. | Conectar agenda · Tus reglas | J |
| 3 | `v1-03.png` | **La cita se vuelve ingreso.** Por la mañana, con café, mira su celular: las citas del día ya aparecen con su ganancia estimada. | Hoy | J |
| 4 | `v1-04.png` | **"Atención realizada" en un toque.** En la puerta de la casa de don Luis, al despedirse, toca un botón en el celular. | Atención realizada | J, L |
| 5 | `v1-05.png` | **Tablero con semáforo.** Entre pacientes, en el auto estacionado, mira su tablero del mes y sonríe aliviada. | Tablero | J |
| 6 | `v1-06.png` | **Lo que falta.** De noche ve que febrero viene bajo, pero la app no le dice qué hacer; sobre la mesa, un mapa con domicilios dispersos y un sobre de impuestos. | Proyección (3 meses) | J |

**Prompts**

`v1-01`
```
Night scene, 11 pm, a tired female physiotherapist (use character J, still in her orange scrub top) sitting at a small kitchen table at home, laptop open showing an abstract spreadsheet grid, a smartphone beside it buzzing with many chat bubbles, a cold cup of tea, a warm desk lamp as the only light, dark purple night through the window with a crescent moon, she rubs her forehead, feeling overwhelmed. [Bloque de estilo]
```
`v1-02`
```
Daytime, inside a small physiotherapy box at a medical center, the physiotherapist (character J) sits on the edge of the treatment table during a break, holding her smartphone, the screen shows abstract blocks of a calendar connecting to a dashboard with a dotted line and a small coin icon, she looks focused and curious, soft daylight from the window. [Bloque de estilo]
```
`v1-03`
```
Early morning at home, the physiotherapist (character J) in her orange scrubs stands by the kitchen counter holding a coffee mug and looking at her phone, floating above the phone a simple list of appointment cards in purple and orange, each with a small coin icon, calm and organized mood, morning light. [Bloque de estilo]
```
`v1-04`
```
At the front door of a modest Chilean house, the physiotherapist (character J) with her equipment bag says goodbye to an elderly man (character L) standing at the doorway with a cardigan, while she taps a single large green check button on her phone with her thumb, a small green check mark floating above the phone, warm late-morning light, small orange car parked behind. [Bloque de estilo]
```
`v1-05`
```
Inside a parked small orange car, the physiotherapist (character J) in the driver seat holds her phone, the screen shows an abstract dashboard with a big number block, a progress bar and a small yellow traffic-light dot, she smiles relieved, view through the side window, residential street and mountains in the background. [Bloque de estilo]
```
`v1-06`
```
Evening at home, the physiotherapist (character J) looks at her phone with a worried expression, the phone shows a simple bar chart with one short red bar, on the table a paper map with scattered pins far apart from each other and a closed envelope with a small warning triangle, unresolved tension, warm lamp light, dark window. [Bloque de estilo]
```

---

### 4.2 Storyboard V2 — Joselyn con la versión iterada (lámina 14)
Hilo: el copiloto lee la ruta. Rutas por sector, impuestos y colchón automáticos, horas vacías recuperadas, cierre antes de las 21 h y alertas con acciones.

| # | Archivo | Situación | Pantalla del prototipo | Ingredientes |
|---|---|---|---|---|
| 1 | `v2-01.png` | **Martes = Machalí.** 8:05, antes de salir, Joselyn ve su ruta del día: 3 domicilios agrupados en un mismo sector. | Hoy · Ruta del día | J |
| 2 | `v2-02.png` | **Un toque reparte el pago.** Tras atender a don Luis, confirma la atención y el pago se separa solo: lo suyo, la retención y el colchón. | Atención realizada (V2) | J, L |
| 3 | `v2-03.png` | **La hora vacía también genera ingreso.** 13:04, un paciente cancela. En el auto, ofrece el cupo de último minuto con un toque. | Cupo de último minuto | J |
| 4 | `v2-04.png` | **Cierre antes de las 21 h.** 20:40, responde tres preguntas en el sofá y deja el celular: cena con su familia. | Cierre del día | J |
| 5 | `v2-05.png` | **Lunes: el tablero llega solo.** Con un café, recibe por WhatsApp el resumen de su semana. | Resumen semanal (WhatsApp) | J |
| 6 | `v2-06.png` | **Avisa antes de la curva.** El copiloto advierte que febrero viene bajo y propone un pack; ella activa la acción tranquila. | Proyección (6 meses + acciones) | J |

**Prompts**

`v2-01`
```
Morning, the physiotherapist (character J) standing next to her small orange hatchback with her equipment bag, looking at her phone, above the phone floats a simplified map with three orange pins close together inside one neighborhood circle connected by a short smooth route line, a longer grey dashed line fading away to show the old longer route, Andes mountains in the background, fresh optimistic light. [Bloque de estilo]
```
`v2-02`
```
Living room of a modest Chilean home, after a physiotherapy session, the elderly man (character L) sits comfortably on a sofa smiling, the physiotherapist (character J) stands beside him tapping her phone, from the phone three small floating jars or coin stacks separate in orange, purple and amber, symbolizing money being split automatically, sense of order and relief. [Bloque de estilo]
```
`v2-03`
```
Midday inside the parked orange car, the physiotherapist (character J) eats a sandwich and taps her phone, above the phone a calendar block with an empty slot transforms into a filled slot with a small green check, a chat bubble flies out of the phone toward the edge of the frame, light and efficient mood. [Bloque de estilo]
```
`v2-04`
```
Evening at home, 8:40 pm, the physiotherapist (character J) in comfortable clothes sits on a sofa and puts her phone face down on a side table, a small wall clock shows the hands before nine, in the background a warmly lit dining table with family members setting dinner, peaceful work-life balance mood, warm amber light. [Bloque de estilo]
```
`v2-05`
```
Monday morning at a small café table near a window, the physiotherapist (character J) in her orange scrubs holds a coffee and reads a chat message on her phone, a floating message card with a green dot and a few abstract summary lines next to the phone, sunny calm atmosphere, a few plants. [Bloque de estilo]
```
`v2-06`
```
The physiotherapist (character J) at the clinic box, looking at her phone with a calm confident expression, floating above the phone a line chart with a dip in the middle marked by a small coral warning triangle and an orange dashed line that lifts the dip upward, a small bell and a package icon representing a session pack offer, sense of control. [Bloque de estilo]
```

---

### 4.3 Storyboard V2 — El paciente (lámina 15)
Hilo: el paciente casi no ve la app. Reserva en la agenda de siempre y recibe mensajes de Joselyn, con su voz, en los momentos justos.

| # | Archivo | Situación | Pantalla del prototipo | Ingredientes |
|---|---|---|---|---|
| 1 | `p-01.png` | **Reserva en un minuto.** Camila ve el link en el Instagram de InMotion y reserva su hora desde el sofá, de noche. | Reserva en línea | C |
| 2 | `p-02.png` | **Recordatorio y confirmación.** El día antes, don Luis recibe el recordatorio por WhatsApp y toca "Confirmo". | WhatsApp de don Luis | L |
| 3 | `p-03.png` | **"Voy en camino".** Don Luis mira por la ventana: le avisan que Joselyn llega a las 11:30, y el auto naranjo dobla la esquina. | WhatsApp de don Luis | L, J |
| 4 | `p-04.png` | **Paga con un link.** Al terminar la sesión, don Luis paga desde su celular, sin efectivo, y la boleta le llega al correo. | Pago con link · Pago recibido | L, J |
| 5 | `p-05.png` | **Un cupo de último minuto.** A la hora de almuerzo, Camila recibe la oferta de una hora libre con descuento y la toma. | WhatsApp de Camila | C |
| 6 | `p-06.png` | **Seguimiento después del alta.** Un mes después, Camila entrena de nuevo; recibe el mensaje de seguimiento y reserva un pack de mantención. | WhatsApp de Camila | C |

**Prompts**

`p-01`
```
Night, cozy living room, a young athletic woman (character C) lying on a sofa with a blanket, scrolling her phone, above the phone a simple social media post card with an orange and purple image transitions into a calendar with one highlighted slot and a small green check, relaxed and effortless mood, warm lamp light. [Bloque de estilo]
```
`p-02`
```
Afternoon in a modest Chilean kitchen, the elderly man (character L) sitting at a table with a cup of tea, holding his phone close and smiling as he taps a large button, a big friendly chat bubble with a green check floats next to the phone, reading glasses on his forehead, warm homely atmosphere. [Bloque de estilo]
```
`p-03`
```
Inside a modest house, the elderly man (character L) looks out of a front window holding his phone, a chat bubble with a small car icon floats next to the phone, outside through the window a small orange hatchback turns the corner of the street with the physiotherapist (character J) driving, Andes in the distance, late morning light. [Bloque de estilo]
```
`p-04`
```
Living room after a session, the elderly man (character L) seated in an armchair pays with his phone, a floating card with a green check and a small envelope flying away symbolizing the receipt sent by email, the physiotherapist (character J) packs her equipment bag in the background smiling, no cash, tidy and calm. [Bloque de estilo]
```
`p-05`
```
Lunch break at a simple office desk or park bench, the young woman (character C) holding a salad bowl and her phone, a chat bubble with a clock icon and a small orange discount tag floats beside the phone, she taps a button with an excited expression, bright midday light. [Bloque de estilo]
```
`p-06`
```
Morning outdoors in a park with the Andes behind, the young woman (character C) in running clothes stretches her ankle on a bench, she reads a friendly chat bubble with a heart and a small calendar icon on her phone, a sense of continuity of care and wellbeing, fresh light. [Bloque de estilo]
```

---

## 5. Banco de situaciones extra (para variantes o láminas de apoyo)

| # | Archivo | Situación | Por qué sirve |
|---|---|---|---|
| X1 | `x-01.png` | **Día de lluvia, dos cancelaciones.** Joselyn en el auto con lluvia; el copiloto reacomoda la ruta y ofrece las horas libres. | Muestra la ruta y los cupos en un día difícil. |
| X2 | `x-02.png` | **Abril sin sorpresa.** Joselyn con su contadora revisa la Operación Renta: el monto ya estaba apartado. | Dimensión económica e impuestos (I4). |
| X3 | `x-03.png` | **El paciente sin smartphone.** La hija de don Luis recibe los recordatorios y paga por él. | Inclusión de adultos mayores (dimensión social). |
| X4 | `x-04.png` | **La clínica y el domicilio en un mismo tablero.** En el box de InMotion, la secretaria agenda y Joselyn ve la cita aparecer en su copiloto. | Integración con la agenda existente (R2). |
| X5 | `x-05.png` | **Sesión de co-creación.** El equipo HORIZON muestra el prototipo a Joselyn y Catalina, que votan con post-it. | Evidencia de co-creación (criterio 2.1.4). |
| X6 | `x-06.png` | **Crecer con datos.** Joselyn, con su tablero, evalúa sumar un grupo de adultos mayores o un kinesiólogo por comisión. | Visión de crecimiento (I8). |

`x-01`
```
Rainy afternoon, the physiotherapist (character J) inside her parked orange car with rain drops on the windshield, looking at her phone, above the phone a simplified map where a route line reorganizes itself and two empty calendar slots light up, calm problem-solving mood, cool blue-grey light with warm orange accents. [Bloque de estilo]
```
`x-02`
```
Small accounting office, the physiotherapist (character J) sits across a desk from a friendly female accountant in her fifties, both look at a phone and a document, a floating gauge icon almost full in orange, relaxed smiles, April autumn light through the window. [Bloque de estilo]
```
`x-03`
```
Kitchen of a family home, a woman in her forties (daughter of character L) holds her phone showing a chat bubble with a green check, while the elderly man (character L) sits next to her with a flip phone, caring family moment. [Bloque de estilo]
```
`x-04`
```
Reception of a small medical center, a receptionist at a desk enters an appointment on a computer, a dotted line flies from the computer to the phone of the physiotherapist (character J) standing at the doorway of the treatment box, the phone shows a new purple appointment block. [Bloque de estilo]
```
`x-05`
```
Co-creation workshop around a table, four young design students show a smartphone prototype to two female physiotherapists (one is character J), colorful sticky notes in orange, purple and amber on the table and wall, people voting with small round stickers, collaborative and warm mood. [Bloque de estilo]
```
`x-06`
```
The physiotherapist (character J) in a bright community room imagining the future: on one side a small group of elderly people doing gentle exercises with resistance bands, on the other side a second physiotherapist joining the team, her phone shows an upward line chart, hopeful and ambitious mood. [Bloque de estilo]
```

---

## 6. Animación opcional en Flow (Veo)

Si quieren convertir una viñeta en un clip de 4–8 s, usarla como *frame* inicial y agregar una línea de movimiento:

| Viñeta | Movimiento sugerido |
|---|---|
| v1-01 | `slow push-in on her tired face, the phone keeps lighting up with new chat bubbles` |
| v2-01 | `the route line draws itself from pin to pin, then she gets into the car` |
| v2-02 | `the three coin stacks separate smoothly and float into place` |
| v2-04 | `she places the phone face down and walks toward the dinner table` |
| p-03 | `the orange car turns the corner and parks in front of the house` |
| p-05 | `she taps the button and a green check pops up` |

Mantener `no text` en todas las animaciones.
