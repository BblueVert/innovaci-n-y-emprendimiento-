# Anexo: las plantillas oficiales del toolkit UA2 (INACAP) completadas con el contenido del informe.
# Escribe sobre los PDF originales de material/plantillas y los monta en páginas A4.
import html
import os
import re
import pymupdf as fitz

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, '..', 'material', 'plantillas')
FT = os.path.join(HERE, 'fonts', 'ttf')
F = {
    'r': os.path.join(FT, 'plus-jakarta-sans-latin-400-normal.ttf'),
    'm': os.path.join(FT, 'plus-jakarta-sans-latin-500-normal.ttf'),
    'b': os.path.join(FT, 'plus-jakarta-sans-latin-700-normal.ttf'),
    'i': os.path.join(FT, 'plus-jakarta-sans-latin-400-italic.ttf'),
    'mono': os.path.join(FT, 'dm-mono-latin-400-normal.ttf'),
    'bebas': os.path.join(FT, 'bebas-neue-latin-400-normal.ttf'),
    'serif': os.path.join(FT, 'instrument-serif-latin-400-italic.ttf'),
}
INK = (0.07, 0.06, 0.12)
MUTE = (0.31, 0.30, 0.43)
ORANGE = (1, 0.42, 0.21)
GREEN = (0.12, 0.54, 0.36)
AMBER = (1, 0.70, 0.28)
GREY = (0.79, 0.78, 0.85)
hexc = lambda h: tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))

LOGO = {'Uber Driver': 'uber', 'YNAB': 'ynab', 'Fintual': 'fintual', 'Mercado Pago': 'mercadopago', 'Smart Fit': 'smartfit', 'Duolingo': 'duolingo', 'Strava': 'strava', 'Google Maps': 'googlemaps', 'Too Good To Go': 'toogoodtogo', 'SII · Propuesta de F22': 'sii'}

EQUIPO = 'Francisco Ahumada · Claudia Cifuentes · Néstor Rivera · Benjamín Vera Yáñez'
CURSO = 'Innovación y Emprendimiento III (FGIE03)'


def clean(s):
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    return s.replace('→', '>').replace('≥', '>=').replace('≤', '<=').replace('★', '*')


def fonts(page):
    for k, path in F.items():
        page.insert_font(fontname='f' + k, fontfile=path)


def box(page, rect, text, size=10, font='r', color=INK, align=0, min_size=4.5, lh=1.25):
    """Escribe texto en un rectángulo reduciendo el tamaño hasta que quepa."""
    rect = fitz.Rect(rect)
    text = clean(text)
    s = size
    while s >= min_size:
        # medición en una página temporal para no ensuciar la real
        tmp = fitz.open(); tp = tmp.new_page(width=page.rect.width, height=page.rect.height)
        tp.insert_font(fontname='f' + font, fontfile=F[font])
        rc = tp.insert_textbox(rect, text, fontname='f' + font, fontsize=s, align=align, lineheight=lh)
        tmp.close()
        if rc >= 0:
            break
        s -= 0.25
    page.insert_textbox(rect, text, fontname='f' + font, fontsize=s, color=color, align=align, lineheight=lh)
    return s


def dot(page, x, y, level, r=3.2):
    """Escala ● ◐ ○ dibujada (las tipografías no traen esos glifos)."""
    c = fitz.Point(x, y)
    if level == 2:
        page.draw_circle(c, r, color=GREEN, fill=GREEN, width=0.6)
    elif level == 1:
        page.draw_circle(c, r, color=AMBER, width=0.8)
        page.draw_sector(c, fitz.Point(x, y - r), 180, color=AMBER, fill=AMBER, width=0.1, fullSector=True)
    else:
        page.draw_circle(c, r, color=GREY, width=0.8)


def footer(page, y, x_int=100, x_cur=694, x_prof=928, size=9):
    y += 5
    page.insert_text((x_int, y), clean(EQUIPO), fontname='fr', fontsize=size, color=INK)
    page.insert_text((x_cur, y), clean(CURSO), fontname='fr', fontsize=size, color=INK)
    page.insert_text((x_prof, y), 'Roberto Escobar Donoso', fontname='fr', fontsize=size, color=INK)


def tpl(name):
    d = fitz.open(os.path.join(TPL, name))
    fonts(d[0])
    return d


# ---------------------------------------------------------------- instrumentos
MAT = {
    'Uber Driver': ['El viaje y el pago se registran solos al terminar.', 'Ganancias por día y semana; sin proyección.', 'Tarifa por distancia y tiempo; pago automático.', 'Metas de ganancia y calificaciones.', 'Ec: ingreso visible al instante.'],
    'YNAB': ['Importa movimientos bancarios (según país); asignación manual.', 'Metas y dinero asignado por propósito.', 'No gestiona cobros.', 'El método y la educación financiera sostienen el hábito.', 'Ec: colchón para gastos irregulares.'],
    'Fintual': ['Aportes automáticos programados.', 'Proyección visual de metas en el tiempo.', 'No aplica a cobros.', 'Comunicación cercana y simple.', 'Ec: ahorro de largo plazo.'],
    'Mercado Pago': ['Cada cobro queda registrado automáticamente.', 'Reportes de ventas descargables.', 'Link, QR y tarjeta, sin efectivo.', 'Sin mecanismos de hábito.', 'Ec · Am: sin efectivo ni papel.'],
    'Smart Fit': ['El cobro recurrente queda registrado.', 'No muestra proyecciones al socio.', 'Débito automático mensual por plan.', 'App y planes escalonados.', 'Ec: ingreso predecible.'],
    'Duolingo': ['No captura datos externos.', 'Progreso y rachas visibles.', 'Freemium; no aplica.', 'Rachas y recordatorios diarios.', 'So: hábito sostenido sin esfuerzo.'],
    'Strava': ['Registro automático por GPS.', 'Progreso y estadísticas claras.', 'Suscripción; no aplica.', 'Clubes e hitos generan comunidad.', 'So: salud y comunidad.'],
    'Google Maps': ['Registro automático de trayectos.', 'Tiempos y distancias del recorrido.', 'No calcula el costo del traslado.', 'No aplica.', 'Am: rutas eficientes, menos km.'],
    'Too Good To Go': ['Publicación manual del excedente.', 'No aplica.', 'Precio reducido para capacidad ociosa.', 'Avisos de locales favoritos.', 'Am · Ec: evita desperdicio y genera ingreso.'],
    'SII · Propuesta de F22': ['Precarga los datos de las boletas emitidas.', 'Propuesta anual, no mensual.', 'Calcula impuesto o devolución.', 'Interacción una vez al año.', 'Ec: evita la sorpresa tributaria.'],
}


def fichas(D):
    out = []
    for i, r in enumerate(D['REFS']):
        d = tpl('2.1.2.1_A_Ficha_refentes.pdf'); p = d[0]
        p.insert_text((100, 110), clean(f'{i + 1:02d} · {r["n"]}'), fontname='fb', fontsize=15, color=INK)
        # imagen: tarjeta con monograma
        ini = ''.join(w[0] for w in r['n'].replace('·', ' ').split()[:2]).upper()
        p.insert_image(fitz.Rect(130, 128, 290, 288), filename=os.path.join(HERE, 'img', 'logos', LOGO[r['n']] + '.png'))
        p.draw_rect(fitz.Rect(130, 128, 290, 288), color=(0.89, 0.88, 0.94), width=0.8)
        box(p, (310, 160, 610, 200), r['n'], 20, 'b')
        box(p, (310, 205, 610, 260), r['amb'].upper(), 10, 'mono', MUTE)
        # variables
        y = 122
        for k, v in enumerate(D['VARS']):
            dot(p, 650, y + 4, r['v'][k])
            p.insert_text((662, y + 8), clean(v), fontname='fr', fontsize=10.5, color=INK)
            y += 24
        p.insert_text((645, y + 14), 'Sostenibilidad: ' + ' · '.join({'Ec': 'Económica', 'So': 'Social', 'Am': 'Ambiental'}[s] for s in r['s']), fontname='fm', fontsize=10, color=MUTE)
        box(p, (645, y + 22, 1170, 296), 'Tendencia: ' + r['t'], 10, 'r', MUTE)
        box(p, (46, 330, 1170, 448), r['d'], 17, lh=1.35)
        box(p, (46, 480, 1170, 562), r['r'], 17, lh=1.35)
        p.draw_rect(fitz.Rect(46, 570, 1170, 674), color=None, fill=hexc('#FFF1EA'))
        p.draw_rect(fitz.Rect(46, 570, 50, 674), color=None, fill=ORANGE)
        box(p, (60, 580, 1160, 670), 'Para el desafío: ' + r['a'], 17, 'm', lh=1.35)
        p.insert_text((92, 708), clean(r['src'] + ' (consultado en octubre de 2026)'), fontname='fr', fontsize=11, color=INK)
        footer(p, 758)
        out.append((d, f'Anexo A · 2.1.2.1 (A) Ficha de referentes {i + 1:02d}/10'))
    return out


def matriz(D):
    out = []
    refs = D['REFS']
    for part in range(2):
        d = tpl('2.1.2.1_B_Matriz_referentes.pdf'); p = d[0]
        cols = [(163, 362), (368, 566), (572, 770), (776, 974), (980, 1178)]
        for k, (x0, x1) in enumerate(cols):
            box(p, (x0 + 6, 112, x1 - 6, 172), D['VARS'][k].split(' ', 1)[1], 10, 'b')
        rows = [(174, 277), (282, 385), (389, 493), (497, 600), (605, 708)]
        for j, (y0, y1) in enumerate(rows):
            r = refs[part * 5 + j]
            p.insert_image(fitz.Rect(46, y0 + 30, 96, y0 + 80), filename=os.path.join(HERE, 'img', 'logos', LOGO[r['n']] + '.png'))
            box(p, (98, y0 + 30, 160, y1 - 4), r['n'], 9.5, 'b')
            for k, (x0, x1) in enumerate(cols):
                dot(p, x0 + 11, y0 + 12, r['v'][k], 3.6)
                box(p, (x0 + 20, y0 + 6, x1 - 6, y1 - 6), MAT[r['n']][k], 9.5)
        # leyenda
        for k, (lv, t) in enumerate([(2, 'Resuelto'), (1, 'Parcial'), (0, 'No resuelto')]):
            dot(p, 600 + k * 85, 64, lv, 3.6); p.insert_text((608 + k * 85, 67), t, fontname='fr', fontsize=9, color=MUTE)
        footer(p, 758)
        out.append((d, f'Anexo A · 2.1.2.1 (B) Matriz de referentes {part + 1}/2'))
    return out


def tabla(D):
    d = tpl('2.1.3.1_Tabla_con_requerimientos_y_perfil_de_usuario.pdf'); p = d[0]
    box(p, (46, 112, 1170, 157), D['DESAFIO'], 10.5)
    emp = [(40, 213, 285, 405), (293, 213, 574, 405), (40, 413, 285, 612), (293, 413, 574, 612), (40, 622, 285, 741), (293, 622, 574, 741)]
    for (q, a), (x0, y0, x1, y1) in zip(D['EMPATIA'], emp):
        box(p, (x0 + 8, y0 + 26, x1 - 8, y1 - 6), a, 9.5)
    p.insert_text((380, 194), 'Joselyn Toledo, kinesióloga independiente', fontname='fi', fontsize=8, color=MUTE)
    rows = [(213, 296), (302, 385), (392, 475), (482, 564), (572, 653), (660, 741)]
    for (code, name, reqs), (y0, y1) in zip(D['REQS'], rows):
        box(p, (590, y0 + 16, 806, y1 - 4), f'{code} · {name}', 9.5, 'm')
        box(p, (822, y0 + 16, 1170, y1 - 4), '\n'.join(f'{rc} {t}' for rc, t, _, _ in reqs), 9)
    box(p, (950, 186, 1170, 204), 'Copiloto Kine: agenda conectada + ganancia real + proyección', 8, 'i', MUTE)
    footer(p, 758)
    return [(d, 'Anexo A · 2.1.3.1 Tabla con perfil de usuario y requerimientos')]


def categorias(D):
    d = tpl('2.1.3.2_Mapa_de_categorias.pdf'); p = d[0]
    slots = [((40, 94, 241, 257), (331, 94, 579, 257)), ((640, 94, 841, 257), (931, 94, 1178, 257)),
             ((40, 289, 241, 453), (331, 289, 579, 453)), ((640, 289, 841, 453), (931, 289, 1178, 453)),
             ((40, 491, 241, 654), (331, 491, 579, 654)), ((640, 491, 841, 654), (931, 491, 1178, 654))]
    for (code, name, nec, reqs), (c, n) in zip(D['CATS'], slots):
        box(p, (c[0] + 8, c[1] + 22, c[2] - 8, c[3] - 30), f'{code}\n{name}', 15, 'b')
        box(p, (c[0] + 8, c[3] - 28, c[2] - 8, c[3] - 6), 'Requerimientos: ' + ' · '.join(reqs), 9, 'mono', MUTE)
        box(p, (n[0] + 8, n[1] + 22, n[2] - 8, n[3] - 8), '\n'.join('· ' + x for x in nec), 12)
    footer(p, 758)
    return [(d, 'Anexo A · 2.1.3.2 Mapa de categorías')]


def jerarquias(D):
    d = tpl('2.1.3.3_Mapa_de_jerarquias.pdf'); p = d[0]
    p.insert_text((125, 130), 'Frecuencia del dolor (anual > diaria)', fontname='fm', fontsize=11, color=MUTE)
    box(p, (760, 692, 1080, 740), 'Impacto en la sostenibilidad de la práctica (bajo > alto)', 11, 'm', MUTE, align=2)
    X = lambda v: 130 + v * (1020 - 130)
    Y = lambda v: 670 - v * (670 - 170)
    p.draw_rect(fitz.Rect(X(.5), Y(1), X(1), Y(.5)), color=None, fill=hexc('#FFF1EA'))
    p.insert_text((X(.5) + 8, Y(.5) - 8), 'PRIORIDAD ALTA', fontname='fmono', fontsize=10, color=ORANGE)
    p.insert_text((X(0) + 8, Y(0) - 8), 'PRIORIDAD BAJA', fontname='fmono', fontsize=10, color=MUTE)
    for code, name, nec, reqs in D['CATS']:
        vx, vy = D['JER'][code]
        cx, cy = X(vx), Y(vy)
        p.draw_circle(fitz.Point(cx, cy), 17, color=hexc('#7B3FA0'), fill=hexc('#D9D2FF'), width=0.8)
        cw_ = fitz.Font(fontfile=F['bebas']).text_length(code, fontsize=17)
        p.insert_text((cx - cw_ / 2, cy + 6), code, fontname='fbebas', fontsize=17, color=INK)
        p.insert_textbox(fitz.Rect(cx - 250, cy - 16, cx - 24, cy + 2), name, fontname='fb', fontsize=11, color=INK, align=2)
        lbl = ' · '.join(reqs); w = fitz.Font(fontfile=F['mono']).text_length(lbl, fontsize=8) + 12
        p.draw_rect(fitz.Rect(cx - 24 - w, cy + 3, cx - 24, cy + 17), color=hexc('#E8637A'), fill=hexc('#FFD6C2'), width=0.5)
        lw = fitz.Font(fontfile=F['mono']).text_length(lbl, fontsize=8)
        p.insert_text((cx - 24 - w / 2 - lw / 2, cy + 13.5), lbl, fontname='fmono', fontsize=8, color=INK)
    p.draw_circle(fitz.Point(870, 112), 6, color=hexc('#7B3FA0'), fill=hexc('#D9D2FF')); p.insert_text((880, 116), 'Necesidad / categoría', fontname='fr', fontsize=9, color=MUTE)
    p.draw_rect(fitz.Rect(864, 124, 876, 134), color=hexc('#E8637A'), fill=hexc('#FFD6C2')); p.insert_text((880, 133), 'Requerimiento', fontname='fr', fontsize=9, color=MUTE)
    footer(p, 758)
    return [(d, 'Anexo A · 2.1.3.3 Mapa de jerarquías')]


def postit(p, rect, i, catc, compact=False):
    p.draw_rect(rect, color=None, fill=hexc(catc[i['c']]))
    if i['v']:
        p.draw_rect(rect, color=INK, width=1.2, dashes='[4 3] 0')
    if compact:
        box(p, (rect.x0 + 6, rect.y0 + 5, rect.x1 - 6, rect.y1 - 3), f'{i["id"]} {i["t"]}', 13, 'm')
        return
    p.insert_text((rect.x0 + 7, rect.y0 + 14), f'{i["id"]}  ' + (' '.join(i['s'])), fontname='fmono', fontsize=8.5, color=MUTE)
    box(p, (rect.x0 + 7, rect.y0 + 20, rect.x1 - 7, rect.y1 - 18), i['t'], 11.5, 'm')
    p.insert_text((rect.x0 + 7, rect.y1 - 7), f'O{i["o"]} · F{i["f"]}' + (f' · voz: {i["v"]}' if i['v'] else ''), fontname='fmono', fontsize=8, color=MUTE)


def canvas(D):
    d = tpl('2.1.4.1_Canvas_Brainstorming.pdf'); p = d[0]
    box(p, (620, 790, 1080, 905), D['DESAFIO'], 13, 'm', align=1)
    x0, y0, x1, y1 = 103, 167, 1598, 1593
    cols, rows = 10, 9
    cw, rh = (x1 - x0) / cols, (y1 - y0) / rows
    cells = [(c, r) for r in range(rows) for c in range(cols) if not (3 <= c <= 6 and 3 <= r <= 5)]
    for i, (c, r) in zip(D['IDEAS'], cells):
        rect = fitz.Rect(x0 + c * cw + 4, y0 + r * rh + 4, x0 + (c + 1) * cw - 4, y0 + (r + 1) * rh - 4)
        postit(p, rect, i, D['CATC'])
    # leyenda dentro del canvas, bajo el desafío
    lx, ly = 640, 930
    for k, (key, name) in enumerate(D['CATN'].items()):
        xx, yy = lx + (k % 2) * 215, ly + (k // 2) * 22
        p.draw_rect(fitz.Rect(xx, yy - 9, xx + 11, yy + 2), color=None, fill=hexc(D['CATC'][key]))
        p.insert_text((xx + 16, yy), f'{key} · {name}', fontname='fr', fontsize=10, color=MUTE)
    p.insert_text((640, ly + 96), 'Borde punteado: idea nacida de la voz de la usuaria o de un experto (UA1).', fontname='fi', fontsize=9.5, color=MUTE)
    footer(p, 1659, 128, 930, 1235, 12)
    return [(d, 'Anexo A · 2.1.4.1 Canvas brainstorming')]


def clasificacion(D):
    d = tpl('2.1.4.2_Mapa_de_clasificacion_de_ideas.pdf'); p = d[0]
    quads = {'-O+F': (120, 290, 820, 825), '+O+F': (852, 290, 1560, 825), '-O-F': (120, 905, 820, 1435), '+O-F': (852, 905, 1560, 1435)}
    titles = {'-O+F': 'Base operativa', '+O+F': 'Foco de la solución', '-O-F': 'Descartadas', '+O-F': 'Banco de ideas futuras'}
    p.draw_rect(fitz.Rect(*quads['+O+F']), color=ORANGE, fill=hexc('#FFF1EA'), width=2)
    for q, (qx0, qy0, qx1, qy1) in quads.items():
        ideas = [i for i in D['IDEAS'] if D['quad'](i) == q]
        p.insert_text((qx0 + 10, qy0 + 22), f'{titles[q]} ({len(ideas)})', fontname='fb', fontsize=14, color=ORANGE if q == '+O+F' else INK)
        cols = 2
        cw = (qx1 - qx0 - 20) / cols
        rh = min(60, (qy1 - qy0 - 40) / max(1, -(-len(ideas) // cols)))
        for n, i in enumerate(ideas):
            c, r = n % cols, n // cols
            rect = fitz.Rect(qx0 + 10 + c * cw + 3, qy0 + 34 + r * rh + 3, qx0 + 10 + (c + 1) * cw - 3, qy0 + 34 + (r + 1) * rh - 3)
            postit(p, rect, i, D['CATC'], compact=True)
    footer(p, 1659, 128, 930, 1235, 12)
    return [(d, 'Anexo A · 2.1.4.2 Mapa de clasificación de ideas')]


def metaforas(D):
    d = tpl('2.1.4.3_Panel_de_metaforas_y_atributos.pdf'); p = d[0]
    imgs = [('02-caso.jpg', 1376, 768), ('07-oficina-movil.jpg', 1024, 1024), ('14-dashboard.jpg', 896, 1200), ('06-nudo.jpg', 1024, 1024)]
    x, y0, h = 122, 112, (1170 - 122 - 30) / (1376 / 768 + 1 + 896 / 1200 + 1)
    for f, w0, h0 in imgs:
        w = h * w0 / h0
        p.insert_image(fitz.Rect(x, y0, x + w, y0 + h), filename=os.path.join(HERE, 'img', f), keep_proportion=True)
        x += w + 10
    box(p, (130, 368, 1170, 452), D['METAFORA'], 13, 'serif')
    slots = [(38, 479, 276, 716), (339, 479, 577, 716), (640, 479, 878, 716), (941, 479, 1179, 716)]
    for (n, desc, nec, req, s), (x0, y0, x1, y1) in zip(D['ATRIBUTOS'], slots):
        box(p, (x0 + 8, y0 + 30, x1 - 8, y0 + 52), n + '  ' + ' '.join(s), 14, 'b', align=1)
        box(p, (x0 + 10, y0 + 56, x1 - 10, y0 + 156), '“' + desc + '”', 11, 'i')
        box(p, (x0 + 10, y0 + 160, x1 - 10, y1 - 6), f'Necesidad: {nec}\nRequerimientos: {req}', 9, 'r', MUTE)
    footer(p, 758)
    return [(d, 'Anexo A · 2.1.4.3 Panel de metáforas y atributos')]


def propuesta(D):
    d = tpl('2.1.4.4_Panel_de_propuesta_de_valor.pdf'); p = d[0]
    W = INK
    box(p, (45, 140, 111, 655), '1. No sabe cuánto gana realmente (I1).\n\n2. Agenda y finanzas desconectadas; registro manual de ~1 h diaria (I2 · I3).\n\n3. Meses bajos e impuestos por sorpresa (I4 · I6).\n\nAlternativas hoy: Excel, Cal.com, AgendaPro, contadora.', 8.5, 'r', W)
    box(p, (118, 145, 190, 655), '1. Conexión con la agenda y cierre de un toque.\n\n2. Ganancia neta por atención con comisión y costos del domicilio.\n\n3. Proyección a 3–6 meses y provisión de la retención.', 8.5, 'r', W)
    box(p, (208, 132, 570, 228), 'C1 Agenda conectada · C2 Ganancia real · C3 Tiempo y bienestar · C4 Costos y rutas · C5 Anticipación · C6 Cumplimiento y confianza', 11)
    box(p, (630, 132, 1008, 228), 'Anticipador · Legible de un vistazo · Automático · Sostenible', 12)
    box(p, (470, 250, 1015, 482), D['PV'], 13.5, 'serif')
    box(p, (430, 496, 1015, 655), 'Eficiencia: minutos diarios de registro (de ~60 a menos de 30) · atenciones registradas sin digitar (80 % o más).\n'
        'Eficacia: diferencia entre ganancia proyectada y real (10 % o menos) · meses con retención provisionada (100 %).\n'
        'Efectividad: la usuaria sabe cuánto ganó (4 de 5 o más) · colchón de al menos 1 mes.\nSostenibilidad: km mensuales (-10 %) · horas recuperadas.', 9.5)
    box(p, (1029, 152, 1100, 378), 'Único que cruza agenda + costos por atención + retención chilena. Co-creado con kinesiólogas reales.', 8.5, 'r', W)
    box(p, (1029, 420, 1100, 655), 'Recomendación entre pares, Instagram y contenido educativo, clínicas como InMotion, gremio.', 8.5, 'r', W)
    box(p, (1106, 145, 1175, 655), 'Kinesiólogas independientes con atención mixta en Rancagua y O’Higgins.\n\nEarly adopters: 0 a 2 años de práctica particular (Joselyn, Catalina).', 8.5, 'r', W)
    box(p, (230, 664, 555, 710), 'Diseño y desarrollo low-code; nube y APIs (Google Calendar sin costo); soporte; adquisición por contenido digital.', 8.5, 'r', W)
    box(p, (740, 664, 1175, 710), 'Suscripción de referencia $20.000–$25.000 CLP/mes (disposición a pagar $30–40 mil; mercado $8–25 mil). Plan básico gratuito.', 8.5, 'r', W)
    footer(p, 758)
    return [(d, 'Anexo A · 2.1.4.4 Panel de propuesta de valor y métricas claves')]


NOTES = {
    '2.1.4.1': 'Lectura: 60 ideas alrededor del desafío. El color indica la categoría; las etiquetas Ec, So y Am, el aporte a la sostenibilidad económica, social o ambiental; O y F, el puntaje de originalidad y factibilidad (1 a 5). El borde punteado marca ideas nacidas de citas de la usuaria o de los expertos de la UA1. Para leer el detalle, ampliar el PDF o consultar la sección 2.1.4.1 del informe.',
    '2.1.4.2': 'Lectura: cada idea se ubicó según su originalidad (eje horizontal) y su factibilidad (eje vertical), con un umbral de 4 sobre 5 en cada eje. El cuadrante destacado concentra las 13 ideas del foco, agrupadas luego en 4 categorías y sintetizadas en el concepto directriz Copiloto Kine.',
}

# ---------------------------------------------------------------- montaje en A4
def build(D, first_page_number):
    items = fichas(D) + matriz(D) + tabla(D) + categorias(D) + jerarquias(D) + canvas(D) + clasificacion(D) + metaforas(D) + propuesta(D)
    out = fitz.open()
    n = first_page_number
    for src, title in items:
        sp = src[0]
        square = abs(sp.rect.width - sp.rect.height) < 5
        W, H = (595.28, 841.89) if square else (841.89, 595.28)
        page = out.new_page(width=W, height=H)
        page.insert_font(fontname='fmono', fontfile=F['mono'])
        m, top = 28, 46
        if square:
            avail = fitz.Rect(m, top, W - m, top + (W - 2 * m))
        else:
            avail = fitz.Rect(m, top, W - m, H - 34)
        page.show_pdf_page(avail, src, 0, keep_proportion=True)
        if square:
            page.insert_font(fontname='fnote', fontfile=F['r'])
            note = NOTES.get(title.split(' · ')[1].split(' ', 1)[0], '')
            page.insert_textbox(fitz.Rect(m + 6, avail.y1 + 14, W - m - 6, H - 40), note, fontname='fnote', fontsize=8.5, color=MUTE, lineheight=1.4)
        page.insert_text((m, 26), clean(title).upper(), fontname='fmono', fontsize=6.6, color=ORANGE)
        page.draw_line(fitz.Point(m, 32), fitz.Point(W - m, 32), color=(0.89, 0.88, 0.94), width=0.6)
        page.draw_line(fitz.Point(m, H - 24), fitz.Point(W - m, H - 24), color=(0.89, 0.88, 0.94), width=0.6)
        page.insert_text((m, H - 13), 'INACAP Rancagua · UA2 Ideación de Propuestas · Evaluación N°2 · Anexo', fontname='fmono', fontsize=6.3, color=MUTE)
        page.insert_text((W - m - 52, H - 13), f'Página {n}', fontname='fmono', fontsize=6.6, color=INK)
        n += 1
    return out, [t for _, t in items]
