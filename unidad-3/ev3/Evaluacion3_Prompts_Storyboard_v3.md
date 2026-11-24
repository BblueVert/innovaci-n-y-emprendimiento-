# EV3 — Prompts del storyboard iterado v3 (3.1.3.2) para Google Flow

Un martes de Josselyn con **Copiloto Kine v3**, después de la retroalimentación del 12/11: sus agendas reales (AgendaPro y la clínica), sus cuatro lugares de trabajo (InMotion, domicilio, piscina temperada y gimnasio), la precordillera de Aguas Buenas y la clase grupal en Las Cabras.

| # | Archivo | Escena | Mejora del ciclo 3 | Ingredientes |
|---|---|---|---|---|
| 1 | `v3-01.jpg` | **8:15 · la agenda ya está** | AgendaPro + agenda de la clínica (RF3) | J, escenario box |
| 2 | `v3-02.jpg` | **10:05 · ¿qué me conviene?** | Ganancia por hora por canal (RF5) | J |
| 3 | `v3-03.jpg` | **13:30 · Aguas Buenas** | Tiempo de viaje y tarifa por tramo (RF6) | J, L, auto |
| 4 | `v3-04.jpg` | **16:00 · piscina temperada** | Servicios con su propio costo (RF7) | J |
| 5 | `v3-05.jpg` | **20:10 · día cerrado** | Reemplaza el registro nocturno (RF2) | J |
| 6 | `v3-06.jpg` | **Fin de mes · Las Cabras** | Clase grupal para adultos mayores (RF10) | J, grupo |

## Cómo usarlos

1. En el proyecto de Flow de la EV2 (`Copiloto Kine · Storyboard`), reutiliza los **ingredientes** ya creados: Josselyn (J) y don Luis (L). Así mantienen la misma cara y ropa que en los storyboards anteriores.
2. Usa **"Ingredientes a imagen"**, formato **16:9**, y pega el prompt de la escena con el **bloque de estilo** al final.
3. **Sin texto** en las imágenes. Si aparecen letras en la pantalla del celular, regenera o agrega `blank abstract UI shapes`.
4. Genera 2–4 variantes por viñeta y elige la más clara.
5. Guárdalas con el nombre exacto en `unidad-3/ev3/img/storyboard/` (`v3-01.jpg` … `v3-06.jpg`) y vuelve a generar la presentación:
   ```
   python3 unidad-3/ev3/build_presentacion.py
   ```
   Cada escena usa la ilustración si existe; si no, muestra la captura del prototipo v3 en el mockup de iPhone.

---

## Bloque de estilo (pegar al final de cada prompt)

```
Style: flat vector editorial illustration, clean geometric shapes, soft subtle shadows, no outlines or very thin ones, warm palette of orange #FF6B35, coral #E8637A, deep purple #7B3FA0, amber #FFB347 and off-white #F8F7FF, calm and friendly mood, rural-urban central Chile setting (San Fernando, Colchagua valley, vineyards and poplar trees, the Andes foothills close in the background when outdoors), wide 16:9 composition with the main action centered in the middle horizontal band and empty space above and below, phone screens show only blank abstract UI blocks in orange and purple, absolutely no text, no letters, no numbers, no logos, no brand names.
```

---

## Personajes y escenarios nuevos (ingredientes opcionales)

Josselyn (J) y don Luis (L) son los mismos de la EV2. Para las escenas nuevas sirven estos apoyos, en 1:1:

**Piscina temperada**
```
Interior of a small heated indoor therapy pool in central Chile: warm turquoise water, large windows with soft daylight, foam floating noodles and kickboards in orange and purple on the edge, tiled floor, calm steamy atmosphere, no people. [Bloque de estilo]
```

**Grupo de adultos mayores (Las Cabras)**
```
Group of six cheerful Chilean older adults, aged 65 to 80, mixed men and women, comfortable sportswear in muted purple, coral and beige tones, standing in a circle in a simple community hall with wooden floor and large windows, full body, plain composition. [Bloque de estilo]
```

---

## Prompts por escena

### `v3-01` · 8:15 · la agenda ya está
```
Early morning inside a small physiotherapy box at a medical center, the physiotherapist (character J, orange scrub top) stands next to the treatment table holding her smartphone, floating above the phone two small abstract calendar cards (one purple, one orange) merge with dotted lines into a single list of seven appointment blocks, each block with a tiny colored dot (purple, orange, turquoise, amber), she looks calm and ready, soft daylight from the window, coffee cup on the shelf. [Bloque de estilo]
```

### `v3-02` · 10:05 · ¿qué me conviene?
```
Mid-morning, the physiotherapist (character J) sits in a small break room of the medical center between patients, looking thoughtfully at her phone, floating beside the phone a simple horizontal bar chart of five bars of different lengths in purple, turquoise, orange, green and amber, the longest bar on top glowing softly, a small clock icon and a small car icon next to the shorter orange bar, she has a light "aha" expression, soft warm light. [Bloque de estilo]
```

### `v3-03` · 13:30 · Aguas Buenas
```
Early afternoon in the Andes foothills near San Fernando, a narrow gravel road climbing between dry hills and poplar trees, a small orange hatchback parked in front of a rural adobe house with a tiled roof, the physiotherapist (character J) with her equipment bag says goodbye to an elderly man (character L) at the door while looking at her phone, floating above the phone a small clock icon with a dotted winding road and a small coin with a plus sign, the mountains close and big in the background, bright dry summer light. [Bloque de estilo]
```

### `v3-04` · 16:00 · piscina temperada
```
Afternoon at a small heated indoor therapy pool, the physiotherapist (character J) in a dark purple swim shirt sits at the pool edge with her feet in the warm turquoise water, checking her phone before a session, floating above the phone three stacked abstract cards with tiny icons of a wave, a house and a dumbbell, each with a small coin, foam noodles in orange and purple floating nearby, calm steamy light through large windows. [Bloque de estilo]
```

### `v3-05` · 20:10 · día cerrado
```
Evening at home, the physiotherapist (character J) in comfortable clothes sits relaxed on a sofa holding her phone, the phone shows one tidy abstract summary card with a big green check mark, on the coffee table a closed notebook and a pen pushed aside, in the background her family sets the dinner table with warm light, she smiles relieved, purple night through the window. [Bloque de estilo]
```

### `v3-06` · Fin de mes · Las Cabras
```
Morning in a simple community hall in a small Chilean town surrounded by vineyards, the physiotherapist (character J) leads a gentle balance exercise for a group of six cheerful older adults standing in a circle, arms open, colorful foam balls on the wooden floor, on a side table her phone shows an abstract row of ten small squares, eight of them filled in green, large windows with vineyards and hills outside, warm joyful mood. [Bloque de estilo]
```

---

## Movimiento sugerido para Veo (opcional)

| Escena | Movimiento |
|---|---|
| v3-01 | Las dos tarjetas de calendario se acercan y se funden en la lista. |
| v3-02 | Las barras crecen de izquierda a derecha y la más larga brilla. |
| v3-03 | Paneo lento desde el camino de ripio hasta la puerta de la casa. |
| v3-04 | Ondas suaves en el agua; las tarjetas flotan levemente. |
| v3-05 | El check verde aparece y la luz de la cena se vuelve más cálida. |
| v3-06 | El grupo abre los brazos al mismo tiempo; los cuadrados se llenan de verde. |
