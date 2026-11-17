# Ilustraciones vectoriales EV3, en el estilo de las ilustraciones del proyecto (EV1/EV2):
# planas, fondo lavanda, naranja #FF6B35 → coral → morado #7B3FA0, trazos redondeados.
# Uso: python3 gen_vectores.py → img/vec/*.svg
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'vec')
O, O2, CO, P, P2, AM, INK, SK, SK2, W, LAV = '#FF6B35', '#E8552A', '#E8637A', '#7B3FA0', '#4A3580', '#FFB347', '#2A2340', '#F2B48C', '#C98B65', '#FFFFFF', '#E2DDF3'

DEFS = f'''<defs>
<linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{O}"/><stop offset=".55" stop-color="{CO}"/><stop offset="1" stop-color="{P}"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF8A4C"/><stop offset="1" stop-color="{O}"/></linearGradient>
<linearGradient id="g3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E4DB5"/><stop offset="1" stop-color="#5B2D86"/></linearGradient>
<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="{P2}" flood-opacity=".16"/></filter>
</defs>
<rect width="1376" height="768" fill="#F4F2FC"/>
<g fill="none" stroke="{LAV}" stroke-width="2"><circle cx="1220" cy="120" r="70"/><circle cx="160" cy="650" r="95"/></g>
<g fill="{LAV}">''' + ''.join(f'<circle cx="{x}" cy="{y}" r="5"/>' for x in (100, 125, 150) for y in (110, 135)) + ''.join(f'<circle cx="{x}" cy="{y}" r="5"/>' for x in (1230, 1255, 1280) for y in (640, 665)) + '</g>'


def svg(name, body):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1376 768" width="1376" height="768">{DEFS}{body}</svg>')


def phone(x, y, w=230, h=460, screen='', glow=False):
    g = f'<circle cx="{x + w / 2}" cy="{y + h / 2}" r="{w * .95}" fill="url(#g1)" opacity=".12"/>' if glow else ''
    return (g + f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{INK}"/>'
            f'<rect x="{x + 12}" y="{y + 14}" width="{w - 24}" height="{h - 28}" rx="24" fill="{W}"/>'
            f'<rect x="{x + w / 2 - 30}" y="{y + 22}" width="60" height="9" rx="4.5" fill="{INK}"/></g>{screen}')


def ui(x, y, w, v2=True):
    """Pantalla tipo Copiloto Kine: encabezado, cifra, medidor y lista."""
    a = O if v2 else '#F3B79F'
    b = P if v2 else '#C9B3DA'
    return (f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="10" fill="{a}" opacity="{1 if v2 else .7}"/>'
            f'<rect x="{x + 14}" y="{y + 16}" width="{w * .45}" height="12" rx="6" fill="{W}"/>'
            f'<rect x="{x}" y="{y + 62}" width="{w}" height="96" rx="12" fill="#F6F4FC"/>'
            f'<path d="M{x + 22} {y + 136} a34 34 0 0 1 68 0" fill="none" stroke="{LAV}" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M{x + 22} {y + 136} a34 34 0 0 1 52 -26" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round"/>'
            f'<rect x="{x + 104}" y="{y + 86}" width="{w - 124}" height="20" rx="6" fill="{INK}" opacity=".85"/>'
            f'<rect x="{x + 104}" y="{y + 116}" width="{(w - 124) * .7}" height="10" rx="5" fill="{LAV}"/>'
            + ''.join(f'<rect x="{x}" y="{y + 176 + i * 52}" width="{w}" height="42" rx="10" fill="#F6F4FC"/>'
                      f'<rect x="{x + 10}" y="{y + 186 + i * 52}" width="6" height="22" rx="3" fill="{b if i % 2 else a}"/>'
                      f'<rect x="{x + 26}" y="{y + 188 + i * 52}" width="{w * .5}" height="9" rx="4.5" fill="{INK}" opacity=".7"/>'
                      f'<rect x="{x + 26}" y="{y + 203 + i * 52}" width="{w * .32}" height="7" rx="3.5" fill="{LAV}"/>' for i in range(3)))


def check(x, y, c=O, r=17):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/><path d="M{x - 7} {y} l5 6 l10 -12" fill="none" stroke="{W}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'


def hand(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 C-6 -40 -2 -88 10 -96 C22 -100 30 -90 30 -76 L30 -26 C40 -36 62 -34 66 -18 C78 -24 96 -18 96 -2 C110 -6 124 4 122 22 '
            f'L116 96 C112 140 90 170 50 176 L-6 180 C-40 150 -40 60 0 0 Z" fill="{SK}"/>'
            f'<path d="M30 -26 L30 18 M66 -18 L64 22 M96 -2 L94 26" stroke="{SK2}" stroke-width="3" stroke-linecap="round" fill="none"/>'
            f'<rect x="-18" y="168" width="150" height="80" rx="18" fill="{P}"/></g>')


# ---------------------------------------------------------------- 16 · testeo de usabilidad
def testeo():
    b = phone(573, 120, 230, 470, ui(600, 168, 176), glow=True)
    b += f'<circle cx="704" cy="420" r="30" fill="none" stroke="{O}" stroke-width="4" opacity=".6"/><circle cx="704" cy="420" r="52" fill="none" stroke="{O}" stroke-width="3" opacity=".3"/>'
    b += hand(690, 432, 1)
    # portapapeles con tareas
    b += f'<g filter="url(#sh)" transform="rotate(-6 330 400)"><rect x="210" y="220" width="250" height="330" rx="20" fill="{W}"/><rect x="285" y="200" width="100" height="40" rx="12" fill="{P}"/></g>'
    for i, ok in enumerate((1, 1, 0, 1, 1)):
        yy = 290 + i * 50
        b += f'<g transform="rotate(-6 330 400)">' + (check(250, yy) if ok else f'<circle cx="250" cy="{yy}" r="17" fill="none" stroke="{CO}" stroke-width="4"/><path d="M243 {yy - 7} l14 14 M257 {yy - 7} l-14 14" stroke="{CO}" stroke-width="4" stroke-linecap="round"/>')
        b += f'<rect x="280" y="{yy - 8}" width="{140 - (i % 2) * 40}" height="14" rx="7" fill="{LAV}"/></g>'
    # cronómetro
    b += f'<g filter="url(#sh)"><circle cx="1010" cy="300" r="92" fill="{W}"/></g><circle cx="1010" cy="300" r="74" fill="none" stroke="{LAV}" stroke-width="12"/>'
    b += f'<path d="M1010 226 A74 74 0 0 1 1080 322" fill="none" stroke="url(#g2)" stroke-width="12" stroke-linecap="round"/><rect x="996" y="188" width="28" height="22" rx="6" fill="{P}"/>'
    b += f'<path d="M1010 300 L1010 254 M1010 300 L1040 316" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><circle cx="1010" cy="300" r="9" fill="{O}"/>'
    # insignia de accesibilidad AA
    b += f'<g filter="url(#sh)"><rect x="930" y="450" width="190" height="110" rx="22" fill="url(#g3)"/></g>'
    b += f'<text x="1025" y="522" text-anchor="middle" font-family="Bebas Neue, Arial Black, sans-serif" font-size="64" fill="{W}" letter-spacing="4">AA</text>'
    b += check(1110, 458, '#1F9D6B', 22)
    svg('16-testeo.svg', b)


# ---------------------------------------------------------------- 17 · ruta del día
def ruta():
    b = f'<g filter="url(#sh)"><rect x="300" y="110" width="776" height="520" rx="36" fill="#F1EEE6"/></g>'
    b += f'<g stroke="{W}" stroke-width="26" stroke-linecap="round"><path d="M300 290 H1076 M300 470 H1076 M520 110 V630 M820 110 V630"/></g>'
    b += f'<path d="M300 380 C480 360 600 420 760 380 S980 300 1076 330" stroke="#FBE3B6" stroke-width="34" fill="none"/>'
    b += f'<ellipse cx="960" cy="560" rx="90" ry="44" fill="#D8EFD9"/><ellipse cx="410" cy="180" rx="70" ry="38" fill="#CFE3F5"/>'
    pts = [(420, 520), (600, 470), (700, 300), (930, 240)]
    b += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in pts) + f'" fill="none" stroke="{O}" stroke-width="9" stroke-dasharray="20 14" stroke-linecap="round"/>'
    # clínica (inicio)
    b += f'<g filter="url(#sh)"><rect x="372" y="456" width="96" height="74" rx="10" fill="url(#g3)"/></g><path d="M366 462 L420 420 L474 462 Z" fill="{P2}"/><rect x="408" y="480" width="24" height="12" fill="{W}"/><rect x="414" y="474" width="12" height="24" fill="{W}"/>'
    for i, (x, y) in enumerate(pts[1:], 1):
        b += (f'<g filter="url(#sh)"><path d="M{x} {y + 6} c-34 -40 -40 -58 -40 -74 a40 40 0 0 1 80 0 c0 16 -6 34 -40 74 z" fill="{O if i < 3 else O2}"/></g>'
              f'<circle cx="{x}" cy="{y - 68}" r="22" fill="{W}"/><text x="{x}" y="{y - 59}" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="26" fill="{O2}">{i}</text>')
    # auto
    b += (f'<g transform="translate(815 270) rotate(-16)"><g filter="url(#sh)"><rect x="-46" y="-22" width="92" height="44" rx="14" fill="{O}"/></g><rect x="-16" y="-16" width="34" height="32" rx="6" fill="#FFD9C7"/>'
          f'<circle cx="-26" cy="-24" r="8" fill="{INK}"/><circle cx="26" cy="-24" r="8" fill="{INK}"/><circle cx="-26" cy="24" r="8" fill="{INK}"/><circle cx="26" cy="24" r="8" fill="{INK}"/></g>')
    # tarjeta de ahorro
    b += f'<g filter="url(#sh)"><rect x="990" y="380" width="290" height="150" rx="24" fill="{W}"/></g>'
    b += f'<text x="1030" y="455" font-family="Bebas Neue, Arial Black, sans-serif" font-size="72" fill="{O}">−7 KM</text>'
    b += f'<rect x="1032" y="476" width="150" height="12" rx="6" fill="{LAV}"/><rect x="1032" y="498" width="100" height="12" rx="6" fill="#D8EFD9"/>'
    b += f'<g filter="url(#sh)"><circle cx="190" cy="300" r="70" fill="{W}"/></g><path d="M162 300 a28 28 0 1 1 56 0 c0 14 -10 26 -28 46 c-18 -20 -28 -32 -28 -46z" fill="{P}"/><circle cx="190" cy="298" r="10" fill="{W}"/>'
    svg('17-ruta.svg', b)


# ---------------------------------------------------------------- 18 · iteración v1 → v2
def iteracion():
    b = f'<path d="M500 150 A300 300 0 0 1 980 260" fill="none" stroke="url(#g2)" stroke-width="16" stroke-linecap="round"/><path d="M962 222 L990 270 L940 276" fill="none" stroke="{O}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
    b += f'<path d="M880 640 A300 300 0 0 1 400 520" fill="none" stroke="{P}" stroke-width="16" stroke-linecap="round"/><path d="M420 562 L394 512 L444 508" fill="none" stroke="{P}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
    b += f'<g opacity=".6">{phone(380, 190, 200, 400, ui(404, 236, 152, v2=False))}</g>'
    b += phone(790, 170, 220, 440, ui(816, 218, 168), glow=True)
    for x, y, t, c in ((480, 640, 'V1', '#B9B0D6'), (900, 650, 'V2', O)):
        b += f'<rect x="{x - 46}" y="{y - 30}" width="92" height="48" rx="24" fill="{c}"/><text x="{x}" y="{y + 6}" text-anchor="middle" font-family="Bebas Neue, Arial Black, sans-serif" font-size="38" fill="{W}" letter-spacing="2">{t}</text>'
    # tarjetas de hallazgos
    b += f'<g filter="url(#sh)"><rect x="140" y="250" width="190" height="80" rx="16" fill="{W}"/><rect x="150" y="360" width="190" height="80" rx="16" fill="{W}"/></g>'
    b += f'<circle cx="182" cy="290" r="20" fill="{CO}"/><path d="M175 283 l14 14 M189 283 l-14 14" stroke="{W}" stroke-width="4" stroke-linecap="round"/><rect x="214" y="282" width="96" height="14" rx="7" fill="{LAV}"/>'
    b += f'<circle cx="192" cy="400" r="20" fill="{AM}"/><text x="192" y="411" text-anchor="middle" font-family="Arial" font-weight="700" font-size="28" fill="{W}">!</text><rect x="224" y="392" width="96" height="14" rx="7" fill="{LAV}"/>'
    b += f'<g filter="url(#sh)"><rect x="1060" y="300" width="190" height="200" rx="18" fill="{W}"/></g>'
    for i in range(4):
        b += check(1096, 338 + i * 42, '#1F9D6B', 14) + f'<rect x="1122" y="{331 + i * 42}" width="{100 - i * 12}" height="13" rx="6.5" fill="{LAV}"/>'
    svg('18-iteracion.svg', b)


# ---------------------------------------------------------------- 19 · públicos del testeo
def persona(cx, base, hair, shirt, extra='', skin=SK, hair_shape='short'):
    hs = {'short': f'<path d="M{cx - 46} {base - 300} a46 46 0 0 1 92 0 v-6 a46 40 0 0 0 -92 0 z" fill="{hair}"/>',
          'long': f'<path d="M{cx - 52} {base - 296} a52 54 0 0 1 104 0 v70 h-20 v-62 h-64 v62 h-20 z" fill="{hair}"/>',
          'bun': f'<path d="M{cx - 47} {base - 298} a47 47 0 0 1 94 0 z" fill="{hair}"/><circle cx="{cx + 20}" cy="{base - 356}" r="20" fill="{hair}"/>',
          'bald': f'<path d="M{cx - 47} {base - 292} a47 30 0 0 1 14 -28 M{cx + 47} {base - 292} a47 30 0 0 0 -14 -28" stroke="{hair}" stroke-width="12" fill="none" stroke-linecap="round"/>'}
    return (f'<path d="M{cx - 92} {base} v-110 a92 92 0 0 1 184 0 v110 z" fill="{shirt}"/>'
            f'<rect x="{cx - 16}" y="{base - 232}" width="32" height="34" fill="{SK2}"/>'
            f'<circle cx="{cx}" cy="{base - 290}" r="46" fill="{skin}"/>' + hs[hair_shape]
            + f'<circle cx="{cx - 15}" cy="{base - 286}" r="4.5" fill="{INK}"/><circle cx="{cx + 15}" cy="{base - 286}" r="4.5" fill="{INK}"/>'
            f'<path d="M{cx - 12} {base - 266} q12 10 24 0" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>' + extra)


def pacientes():
    base = 640
    b = f'<rect x="80" y="{base}" width="1216" height="10" rx="5" fill="{LAV}"/>'
    # adulto mayor con bastón y gorro
    b += persona(260, base, '#D9D4E8', P, f'<rect x="200" y="{base - 352}" width="120" height="22" rx="8" fill="{P2}"/><rect x="214" y="{base - 380}" width="92" height="36" rx="16" fill="{P2}"/>'
                 f'<path d="M352 {base - 120} v120" stroke="#8A6A4E" stroke-width="10" stroke-linecap="round"/><path d="M352 {base - 120} q0 -22 -20 -22" stroke="#8A6A4E" stroke-width="10" fill="none" stroke-linecap="round"/>', hair_shape='bald')
    # cuidadora / trabajadora de oficina con notebook
    b += persona(560, base, '#3B2A2A', O, f'<rect x="500" y="{base - 98}" width="120" height="76" rx="8" fill="{INK}"/><circle cx="560" cy="{base - 60}" r="7" fill="{W}"/>', hair_shape='long')
    # trabajador de faena con casco
    b += persona(850, base, '#2A2340', '#5B6B8C', f'<path d="M800 {base - 312} a50 46 0 0 1 100 0 z" fill="{AM}"/><rect x="790" y="{base - 316}" width="120" height="14" rx="7" fill="{O}"/>'
                 f'<path d="M790 {base - 150} l40 150 M910 {base - 150} l-40 150" stroke="{AM}" stroke-width="14"/>', skin=SK2, hair_shape='short')
    # deportista con cintillo
    b += persona(1130, base, '#5A3A2A', CO, f'<rect x="1084" y="{base - 312}" width="92" height="14" rx="7" fill="{P}"/><path d="M1060 {base - 60} h140" stroke="{W}" stroke-width="10" opacity=".7"/>', hair_shape='bun')
    # globos con los mensajes que recibe cada perfil
    icons = [  # reloj, pin, recibo, rayo
        lambda x, y: f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="{W}" stroke-width="6"/><path d="M{x} {y} v-12 M{x} {y} l9 6" stroke="{W}" stroke-width="6" stroke-linecap="round"/>',
        lambda x, y: f'<path d="M{x} {y + 26} c-18 -22 -24 -32 -24 -42 a24 24 0 0 1 48 0 c0 10 -6 20 -24 42 z" fill="{W}"/><circle cx="{x}" cy="{y - 16}" r="8" fill="{O}"/>',
        lambda x, y: f'<path d="M{x - 18} {y - 26} h36 v52 l-9 -7 l-9 7 l-9 -7 l-9 7 z" fill="{W}"/><path d="M{x - 9} {y - 12} h18 M{x - 9} {y} h18" stroke="{P}" stroke-width="5" stroke-linecap="round"/>',
        lambda x, y: f'<path d="M{x + 6} {y - 28} L{x - 16} {y + 4} h16 l-6 26 l24 -34 h-16 z" fill="{W}"/>',
    ]
    for (cx, fill), ic in zip(((260, P), (560, O), (850, P2), (1130, CO)), icons):
        y = 150
        b += f'<g filter="url(#sh)"><rect x="{cx - 62}" y="{y - 52}" width="124" height="104" rx="26" fill="{fill}"/><path d="M{cx - 14} {y + 50} l14 22 l14 -22 z" fill="{fill}"/></g>' + ic(cx, y)
    svg('19-pacientes.svg', b)


# ---------------------------------------------------------------- 20 · estado del arte
def arte():
    b = f'<path d="M180 600 C360 560 420 470 560 470 S800 360 1000 260 L1180 170" fill="none" stroke="{LAV}" stroke-width="14" stroke-linecap="round"/><path d="M1140 160 L1186 166 L1172 210" fill="none" stroke="{LAV}" stroke-width="14" stroke-linecap="round"/>'
    tiles = [(300, 230), (470, 230), (640, 230), (300, 400), (470, 400), (640, 400)]
    for i, (x, y) in enumerate(tiles):
        hl = i == 4
        b += f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="140" height="140" rx="26" fill="{"url(#g1)" if hl else W}"/></g>'
        c = W if hl else (P if i % 2 else O)
        b += f'<rect x="{x + 26}" y="{y + 30}" width="40" height="40" rx="10" fill="{c}" opacity="{1 if hl else .85}"/><rect x="{x + 26}" y="{y + 86}" width="88" height="11" rx="5.5" fill="{W if hl else LAV}"/><rect x="{x + 26}" y="{y + 106}" width="56" height="11" rx="5.5" fill="{W if hl else LAV}" opacity=".7"/>'
        if hl:
            b += f'<path d="M{x + 104} {y + 26} l7 15 l16 2 l-12 11 l3 16 l-14 -8 l-14 8 l3 -16 l-12 -11 l16 -2 z" fill="{W}"/>'
    # lupa
    b += f'<circle cx="930" cy="400" r="150" fill="{W}" opacity=".55"/><circle cx="930" cy="400" r="150" fill="none" stroke="url(#g1)" stroke-width="26"/>'
    b += f'<path d="M1036 506 L1170 640" stroke="{P2}" stroke-width="42" stroke-linecap="round"/>'
    b += f'<rect x="850" y="340" width="40" height="110" rx="8" fill="{LAV}"/><rect x="905" y="300" width="40" height="150" rx="8" fill="{O}"/><rect x="960" y="370" width="40" height="80" rx="8" fill="{P}" opacity=".7"/>'
    svg('20-estado-arte.svg', b)


# ---------------------------------------------------------------- 21 · sostenibilidad
def sostenible():
    b = f'<ellipse cx="688" cy="400" rx="440" ry="250" fill="none" stroke="#D5CEEB" stroke-width="3" stroke-dasharray="10 12"/>'
    b += phone(603, 150, 170, 340, ui(622, 190, 132), glow=True)
    nodes = [(300, 260, O, 'coin'), (1080, 260, P, 'heart'), (688, 640, '#1F9D6B', 'leaf')]
    for x, y, c, k in nodes:
        b += f'<g filter="url(#sh)"><circle cx="{x}" cy="{y}" r="92" fill="{W}"/></g><circle cx="{x}" cy="{y}" r="70" fill="{c}"/>'
        if k == 'coin':
            b += ''.join(f'<ellipse cx="{x}" cy="{y + 22 - i * 16}" rx="34" ry="11" fill="{AM}" stroke="{O2}" stroke-width="3"/>' for i in range(4))
        elif k == 'heart':
            b += f'<path d="M{x} {y + 30} C{x - 50} {y - 6} {x - 40} {y - 46} {x - 14} {y - 40} C{x - 4} {y - 38} {x} {y - 28} {x} {y - 22} C{x} {y - 28} {x + 4} {y - 38} {x + 14} {y - 40} C{x + 40} {y - 46} {x + 50} {y - 6} {x} {y + 30} Z" fill="{W}"/>'
        else:
            b += f'<path d="M{x - 30} {y + 30} C{x - 40} {y - 30} {x + 10} {y - 50} {x + 38} {y - 38} C{x + 40} {y + 10} {x + 4} {y + 40} {x - 30} {y + 30} Z" fill="{W}"/><path d="M{x - 30} {y + 30} L{x + 22} {y - 20}" stroke="#1F9D6B" stroke-width="5" stroke-linecap="round"/>'
    for (x, y, c, _), lx in zip(nodes, ('EC', 'SO', 'AM')):
        b += f'<rect x="{x + 56}" y="{y - 92}" width="62" height="36" rx="18" fill="{INK}"/><text x="{x + 87}" y="{y - 66}" text-anchor="middle" font-family="Arial" font-weight="700" font-size="20" fill="{W}">{lx}</text>'
    svg('21-sostenible.svg', b)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for f in (testeo, ruta, iteracion, pacientes, arte, sostenible):
        f()
    # PNG 2x para el PDF (WeasyPrint no aplica sombras ni fuentes dentro de SVG)
    import subprocess
    js = os.path.join(OUT, '_shot.js')
    open(js, 'w').write("""const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1376, height: 768 }, deviceScaleFactor: 1.5 }); const dir = process.argv[2];
for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.svg'))) { await p.goto('file://' + path.join(dir, f)); await p.screenshot({ path: path.join(dir, f.replace('.svg', '.png')) }); }
await b.close(); })();""")
    subprocess.run(['node', js, OUT], check=True, env={**os.environ, 'NODE_PATH': os.environ.get('NODE_PATH', '')})
    os.remove(js)
    print('ok', sorted(os.listdir(OUT)))
