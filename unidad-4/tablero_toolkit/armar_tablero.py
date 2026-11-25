# Arma el tablero (tipo Whiteboard) con el recuento del toolkit FGIE03 U1–U4 alrededor del proyecto Copiloto Kine.
# Genera un JSON por elemento en ./elementos/ y la lista de lotes (≤ 50 escrituras) en ./lotes.json.
# Uso: python3 armar_tablero.py
import json
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'img')
OUT = os.path.join(HERE, 'elementos')
BLOB = {  # imagen local → id del asset subido al tablero
    'u1_01': '28d6084d8afb0a090cd350008c77c19f', 'u1_02': '7ad9ff8a249bcd172d4f96b0fff47886', 'u1_03': 'd6bc11e64eaf666d12b9aaf76ac56dbf',
    'u1_04': '50adb3531e2eea1f7f6b7ea891a37361', 'u1_05': '38c2fcb6c81458f307ce30ea97c4fee0', 'u1_06': '008cda733583654c137cf995ea8cc3cf',
    'u1_07': 'bd1a3441e007d278cf6a36bd0aa9885f', 'u1_08': '5840732dac0d1c3163cf0ba718432bfc', 'u1_09': '5d91675992a722d19d97e5900c98eca7',
    'u1_10': 'c722ef50d429b484f3eeda928b3bb31b', 'u1_11': '276205fe5e85d2411103de687d53c680', 'u1_12': 'ce8ab28d3263333709d05e8a28d81a90',
    'u1_13': '833715b363b1e0cf16b9f7b078970215', 'u1_14': 'fceb612ef5d3b667acca0c239012ec67', 'u1_15': '28a69ee309e045157a69645610283051',
    'u1_16': '5771909f53371f20e1346558b665d87d', 'u1_17': 'd33c242fb8b84c984e4ddcd9997b0714',
    'u2_43': '8acf707c828e15fb1b870e635387d658', 'u2_44': 'abb6d3661efe1b5446428de589cd47aa', 'u2_45': '0d929756ad3534d02e9b71bf03e751b3',
    'u2_46': 'a14fca2b95aefb08eedb20f1619d0dcc', 'u2_47': '665c3f82a8215d344dec3e1e8dde71cc', 'u2_48': '5ca7df4b57f9ec1d389a95a436a29042',
    'u2_49': '7bd3b9239fc1cc5d003cd2ca27eee26e', 'u2_50': 'ecd5a0b50dd51fe16ac55c6a0364cb31', 'u2_51': 'bafab70180dbaac33e52b89ce645bd4f',
    'u2_fichas': 'fb85dc1bedd38df8e38db23f3ddc8adc',
    'u3_00': '8c8842ce98656fa3e1303af47d4ec905', 'u3_01': 'c3b491032aa3c33af1d7da5f6c067e90', 'u3_02': '69d1d7653e374d534048ae15d42d1c6b',
    'u3_03': '7fa3af29692d5c459661e017ae872842', 'u3_04': '544e19d0df04ceb74c39b3a3090eb9ff', 'u3_05': '3e38cfcbb239a77eea3aa9d3dc609705',
    'u3_06': 'b5f30c2519659fc347640ddfce9cf104', 'u3_07': '3eeb108821faa705322bb115cc41451f', 'u3_08': 'b9eac95324c2f54739372ad82c78f41e',
    'u3_09': 'b813e846e376a972db50c64466373052', 'u3_10': 'ffcbef549d056cd062e12658c8df8939',
    'u4_form': 'afc442d82734777337ad430b0c85cc45', 'u4_guion': '34e87e13916139ec3e907e4c955ddc1a', 'u4_lean': '5c1f92f1be72aee76019a21ff3953693',
    'u4_pitch': '6936eff33fba0e4c08a44adba73ad69e', 'hub_app': 'd00a66ae8de6924bf48ca3c9234fbc27',
}
URL_PRO = 'https://copiloto-kine.vercel.app/profesional/'
URL_CLI = 'https://copiloto-kine.vercel.app/cliente/'

U1 = [('u1_01', '1.1.1.1 · Pregunta exploratoria (diagnóstica)'), ('u1_02', 'Guion de sondeo y card sorting'),
      ('u1_03', '1.1.2.1 A · Preparación entrevista a usuaria'), ('u1_04', '1.1.2.1 B · Pauta entrevista a Josselyn'),
      ('u1_05', '1.1.2.2 A · Preparación de la observación'), ('u1_06', '1.1.2.2 B · Pauta AEIOU'),
      ('u1_07', '1.1.2.3 A · Preparación entrevista a expertos'), ('u1_08', '1.1.2.3 B · Experta par: Catalina'),
      ('u1_09', '1.1.2.3 B · Experto financiero'), ('u1_10', '1.1.3.1 · Matriz PESTAL'),
      ('u1_11', '1.1.4.1 · Vaciado de hallazgos'), ('u1_12', '1.1.4.2 · Categorización de insights'),
      ('u1_13', '1.1.4.3 · Mapa de priorización'), ('u1_14', '1.1.5.1 A · Fichas de antecedentes'),
      ('u1_15', '1.1.5.1 B · Matriz de antecedentes'), ('u1_16', 'Redefinición del desafío'),
      ('u1_17', '1.1.6 · Oportunidades y trabajo futuro')]
U2 = [('u2_fichas', '2.1.2.1 A · Fichas de 10 referentes', 2), ('u2_43', '2.1.2.1 B · Matriz de referentes (1/2)'), ('u2_44', '2.1.2.1 B · Matriz de referentes (2/2)'),
      ('u2_45', '2.1.3.1 · Perfil de usuaria y requerimientos'), ('u2_46', '2.1.3.2 · Mapa de categorías'), ('u2_47', '2.1.3.3 · Mapa de jerarquías'),
      ('u2_48', '2.1.4.1 · Canvas brainstorming (60 ideas)'), ('u2_49', '2.1.4.2 · Mapa de clasificación de ideas'),
      ('u2_50', '2.1.4.3 · Panel de metáforas y atributos'), ('u2_51', '2.1.4.4 · Propuesta de valor y métricas claves')]
U3 = [('sqa', '3.1.1.1 · Tabla SQA (diagnóstica)'), ('u3_00', '3.1.2.1 · Storyboard con propuesta de valor (v1)'), ('u3_01', '3.1.2.3 · Ficha de testeo · ciclo 1 (uso y estética)'),
      ('u3_02', '3.1.2.4 · Matriz CDM · ciclo 1'), ('u3_03', '3.1.3.2 · Storyboard iterado (v2)'), ('u3_04', '3.1.3.4 · Ficha de testeo · ciclo 2 (técnico)'),
      ('u3_05', '3.1.2.4 · Matriz CDM · ciclo 2'), ('u3_06', '3.1.2.3 · Ficha de testeo · ciclo 3 (clienta y Sercotec)'), ('u3_07', '3.1.2.4 · Matriz CDM · ciclo 3'),
      ('u3_08', '3.1.3.2 · Storyboard iterado (v3)'), ('u3_09', '3.1.3.4 · Ficha de testeo · ciclo 4 (usuarias)'), ('u3_10', '3.1.4.1 · Matriz PESTAL profundizada')]
QQQ = [('Qué veo', ['Un prototipo v3 validado en 4 ciclos', 'Costos, precio y canales definidos', 'Interés de la clienta y de Sercotec']),
       ('Qué no veo', ['Cuántas kinesiólogas pagarían de verdad', 'La integración real con AgendaPro', 'Quién mantiene la app después del curso']),
       ('Qué infiero', ['Un piloto gratis es la mejor prueba de precio', 'El pitch debe partir por el dolor de Josselyn', 'Sercotec es canal de difusión y financiamiento'])]

E = {}   # id → elemento
N = [0]


def nid():
    N[0] += 1
    return f'e{N[0]}'


def add(el):
    i = nid(); E[i] = el
    return i


def size(name, w):
    im = Image.open(os.path.join(IMG, name + ('.png' if name == 'hub_app' else '.jpg')))
    return w, round(w * im.height / im.width)


def flow(items, x0, y0, maxw, gap=24, cap=46):
    """items: (w, h, draw(x, y)) → coloca en filas; devuelve (ancho, alto) usados."""
    x, y, rowh, used = x0, y0, 0, 0
    for w, h, draw in items:
        if x > x0 and x + w > x0 + maxw:
            x = x0; y += rowh + gap; rowh = 0
        draw(x, y)
        x += w + gap; rowh = max(rowh, h + cap); used = max(used, x - gap - x0)
    return used, y + rowh - y0


def img_item(name, caption, w):
    w, h = size(name, w)

    def draw(x, y):
        add({'type': 'image', 'x': x, 'y': y, 'w': w, 'h': h, 'src': f'/_blob/{BLOB[name]}'})
        add({'type': 'text', 'x': x, 'y': y + h + 8, 'text': caption, 'size': 'small', 'wrap': w})
    return (w, h, draw)


def section_items(unit):
    if unit == 1:
        return [img_item(n, c, 210) for n, c in U1]
    if unit == 2:
        return [img_item(t[0], t[1], 684 if len(t) > 2 else 330) for t in U2]
    if unit == 3:
        out = []
        for n, c in U3:
            if n == 'sqa':
                def draw(x, y, c=c):
                    add({'type': 'table', 'x': x, 'y': y, 'size': 'small',
                         'cols': {'c1': {'at': 1, 'w': 70}, 'c2': {'at': 2, 'w': 260}},
                         'rows': {'r1': {'at': 1, 'c1': 'SQA', 'c2': 'Diagnóstico de la UA3'},
                                  'r2': {'at': 2, 'c1': 'Sé', 'c2': 'Prototipar en Figma y HTML'},
                                  'r3': {'at': 3, 'c1': 'Quiero', 'c2': 'Testear sin datos reales'},
                                  'r4': {'at': 4, 'c1': 'Aprendí', 'c2': 'Medir tareas, no opiniones'}}})
                    add({'type': 'text', 'x': x, 'y': y + 186, 'text': c, 'size': 'small', 'wrap': 330})
                out.append((330, 178, draw))
            else:
                out.append(img_item(n, c, 330 if n != 'u3_10' else 160))
        return out
    # unidad 4
    out = []

    def qqq(x, y):
        add({'type': 'text', 'x': x, 'y': y, 'text': '4.1.1.1 · Qué veo, qué no veo, qué infiero (diagnóstica)', 'size': 'body'})
        for k, (t, items) in enumerate(QQQ):
            cx = x + k * 228
            add({'type': 'text', 'x': cx, 'y': y + 36, 'text': f'**{t}**', 'size': 'body'})
            for j, it in enumerate(items):
                add({'type': 'shape', 'kind': 'rounded', 'x': cx, 'y': y + 70 + j * 104, 'w': 212, 'h': 92, 'color': 'white', 'stroke': 'ink', 'size': 'small', 'text': it})
    out.append((680, 380, qqq))
    out.append(img_item('u4_lean', '4.1.2.1 · Lean Canvas', 680))
    out.append(img_item('u4_guion', '4.1.3.2 · Guion del pitch', 520))
    out.append(img_item('u4_form', '4.1.3.1 · Formulario de postulación a fondo', 240))
    out.append(img_item('u4_pitch', 'Presentación del pitch (entregable final)', 560))
    return out


TITLES = {1: 'U1 · Diagnóstico y selección de oportunidades', 2: 'U2 · Ideación de propuestas',
          3: 'U3 · Prototipado y testeo', 4: 'U4 · Propuesta de valor y difusión'}
COLORS = {1: 'blue', 2: 'purple', 3: 'green', 4: 'peach'}
PAD, MAXW = 24, 1400


def build():
    # medir cada sección en un origen de prueba para conocer su alto
    dims = {}
    for u in (1, 2, 3, 4):
        saved = dict(E); n0 = N[0]
        dims[u] = flow(section_items(u), 0, 0, MAXW)
        E.clear(); E.update(saved); N[0] = n0
    W = MAXW + 2 * PAD
    top_h = max(dims[1][1], dims[2][1]) + 2 * PAD
    bot_h = max(dims[3][1], dims[4][1]) + 2 * PAD
    gap_x, band = 60, 260
    pos = {1: (-W - gap_x, -band - top_h, top_h), 2: (gap_x, -band - top_h, top_h), 3: (gap_x, band, bot_h), 4: (-W - gap_x, band, bot_h)}
    # título
    add({'type': 'text', 'x': -W - gap_x, 'y': -band - top_h - 210, 'text': 'Toolkit Copiloto Kine', 'size': 'title'})
    add({'type': 'text', 'x': -W - gap_x, 'y': -band - top_h - 140, 'text': 'Cuatro unidades del Ciclo de Innovación INACAP, un mismo proyecto', 'size': 'large'})
    sec = {}
    for u in (1, 2, 3, 4):
        x, y, h = pos[u]
        sec[u] = add({'type': 'container', 'x': x, 'y': y, 'w': W, 'h': h, 'text': TITLES[u], 'color': COLORS[u]})
        flow(section_items(u), x + PAD, y + PAD, MAXW)
    # centro: el proyecto
    hub_w, hub_h = 1100, 400
    hx, hy = -hub_w // 2, -hub_h // 2
    hub = add({'type': 'shape', 'kind': 'rounded', 'x': hx, 'y': hy, 'w': hub_w, 'h': hub_h, 'color': 'white', 'stroke': 'terracotta', 'text': ''})
    pw, ph = size('hub_app', 170)
    add({'type': 'image', 'x': hx + 30, 'y': hy + (hub_h - ph) // 2, 'w': pw, 'h': ph, 'src': f'/_blob/{BLOB["hub_app"]}'})
    tx = hx + 30 + pw + 36
    add({'type': 'text', 'x': tx, 'y': hy + 28, 'text': 'Copiloto Kine', 'size': 'large', 'color': 'terracotta'})
    add({'type': 'text', 'x': tx, 'y': hy + 76, 'wrap': hub_w - (tx - hx) - 30, 'size': 'body',
         'text': ('**Sabe cuánto ganas y qué te conviene, sin anotar nada de noche.**\n'
                  'App web que convierte cada atención de una kinesióloga independiente en ganancia real y por hora, contando el tiempo de viaje.\n'
                  'Caso: Josselyn Toledo, kinesióloga de San Fernando (InMotion, domicilios, piscina y gimnasio).\n'
                  'Equipo: Francisco Ahumada, Claudia Cifuentes, Néstor Rivera y Benjamín Vera Yáñez · Diseño Digital, INACAP Rancagua · Prof. Roberto Escobar Donoso.\n\n'
                  f'- [Prototipo · vista profesional]({URL_PRO})\n- [Prototipo · vista cliente (paciente)]({URL_CLI})')})
    # flechas del ciclo
    add({'type': 'arrow', 'from': sec[1], 'to': sec[2], 'fromSide': 'right', 'toSide': 'left'})
    add({'type': 'arrow', 'from': sec[2], 'to': sec[3], 'fromSide': 'bottom', 'toSide': 'top'})
    add({'type': 'arrow', 'from': sec[3], 'to': sec[4], 'fromSide': 'left', 'toSide': 'right'})
    add({'type': 'arrow', 'from': sec[4], 'to': sec[1], 'fromSide': 'top', 'toSide': 'bottom'})
    return hub


def main():
    build()
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    # orden: secciones atrás, luego el bloque central, luego el resto
    ids = list(E)
    order = [i for i in ids if E[i]['type'] == 'container'] + [i for i in ids if E[i]['type'] == 'shape' and E[i].get('stroke') == 'terracotta'] \
        + [i for i in ids if E[i]['type'] != 'container' and not (E[i]['type'] == 'shape' and E[i].get('stroke') == 'terracotta')]
    writes = []
    meta = {'v': 1, 'title': 'Toolkit Copiloto Kine', 'order': order}
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w'), ensure_ascii=False)
    for i in order:
        p = os.path.join(OUT, f'{i}.json')
        json.dump(E[i], open(p, 'w'), ensure_ascii=False)
        writes.append({'op': 'set', 'collection': 'elements', 'doc_id': i, 'file_path': p})
    writes = [{'op': 'set', 'collection': 'board', 'doc_id': 'meta', 'file_path': os.path.join(OUT, 'meta.json')}] + writes
    lotes = [writes[k:k + 50] for k in range(0, len(writes), 50)]
    json.dump(lotes, open(os.path.join(HERE, 'lotes.json'), 'w'), ensure_ascii=False, indent=0)
    xs = [e.get('x', 0) for e in E.values() if 'x' in e]; ys = [e.get('y', 0) for e in E.values() if 'y' in e]
    print(len(E), 'elementos ·', len(lotes), 'lotes · x', min(xs), max(xs), '· y', min(ys), max(ys))


if __name__ == '__main__':
    main()
