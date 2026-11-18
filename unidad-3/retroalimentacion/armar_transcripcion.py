# Transcripción de la reunión de retroalimentación (12/11/2026, 08:33) con interlocutores identificados.
# Fuente: Whisper (small, español) sobre el audio de la grabación de Meet + agrupación de voces (ECAPA, 4 grupos).
# Los nombres se asignaron cruzando cada grupo de voz con el video (Meet muestra en grande a quien habla)
# y se corrigieron a mano por contenido los bloques ambiguos (ver OVERRIDE y SPLIT).
# Uso: python3 armar_transcripcion.py → Transcripcion_reunion_2026-11-12.md
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CLUSTER = {'ARIEL': 'ARIEL', 'MABEL': 'MABEL', 'JOSELYN': 'JOSSELYN', '?': None}
NOMBRE = {'ARIEL': 'Ariel O\'Nell (profesor a cargo, INACAP)', 'MABEL': 'Mabel Aceituno Romero (encargada Sercotec)',
          'JOSSELYN': 'Klga. Josselyn Toledo (clienta)', 'ANA': 'Ana Luisa Aguilera (docente INACAP, otra sección)', 'SIS': '[Sistema de Meet]'}

# Bloques sin voz asignada o mal asignados, corregidos por contexto (índice de bloque → hablante)
OVERRIDE = {9: 'MABEL', 11: 'MABEL', 14: 'MABEL', 17: 'MABEL', 22: 'MABEL', 24: 'MABEL', 27: 'MABEL', 29: 'ARIEL',
            36: 'JOSSELYN', 38: 'JOSSELYN', 40: 'JOSSELYN', 42: 'ARIEL', 44: 'MABEL', 48: 'ARIEL', 52: 'JOSSELYN',
            56: 'ANA', 57: 'ANA', 58: 'MABEL', 60: 'SIS', 67: 'JOSSELYN', 69: 'MABEL', 73: 'JOSSELYN', 75: 'MABEL',
            78: 'MABEL', 80: 'MABEL', 82: 'MABEL', 85: 'MABEL', 87: 'MABEL', 89: 'MABEL', 92: 'MABEL', 100: 'MABEL',
            107: 'JOSSELYN', 109: 'JOSSELYN', 112: 'ARIEL', 113: 'JOSSELYN', 115: 'MABEL', 117: 'JOSSELYN', 119: 'MABEL',
            121: 'MABEL', 123: 'MABEL', 130: 'MABEL', 141: 'MABEL', 145: 'MABEL', 147: 'MABEL', 154: 'MABEL',
            156: 'MABEL', 160: 'ARIEL', 165: 'ARIEL', 168: 'MABEL', 177: 'ARIEL', 178: 'ANA', 184: 'MABEL'}
# Bloques donde hablan dos personas: (índice, texto donde empieza el segundo, segundo hablante)
SPLIT = [(126, 'No, solamente individual todavía.', 'JOSSELYN'), (128, 'Individual.', 'JOSSELYN'),
         (132, 'quizás ahí podrías tener', 'MABEL'), (180, 'ya, de nada profesor', 'MABEL')]

# Correcciones de palabras mal reconocidas por el ASR (nombres propios, lugares y términos del caso)
FIX = [(r'\bJoselyn\b', 'Josselyn'), (r'\ba Selin\b', 'Josselyn'), (r'\bSelin\b', 'Josselyn'), (r'\bYosely\b', 'Josselyn'), (r'Inacá\b', 'INACAP'),
       (r'\bvencina\b', 'bencina'), (r'menstrual(mente)?', r'mensual\1'), (r'equineciología', 'kinesiología'),
       (r'[Qq]uinesi', 'kinesi'), (r'kinesiolo independiente', 'kinesióloga independiente'), (r'\bRengu\b', 'Rengo'),
       (r'\bReguino\b', 'Requínoa'), (r'psicomotrizía', 'psicomotricidad'), (r'\bagenda pro\b', 'AgendaPro'),
       (r'dovisibio', 'domicilio'), (r'homicidios', 'domicilios'), (r'emplendimiento', 'emprendimiento'),
       (r'costos picos', 'costos fijos'), (r'topuercas', 'propuestas'), (r'\bcampas\b|\bcambas\b|\bcambe\b', 'Canvas'),
       (r'hora es hombre', 'hora hombre'), (r'atestiar', 'a testear'), (r'lexel', 'el Excel'), (r'Planía', 'Planilla'),
       (r'otro lado material', 'traslado, materiales'), (r'satención', 'sus atenciones'), (r'\btensión\b', 'atención'),
       (r'piscina temporal', 'piscina temperada'), (r'en mis cuidos', 'enfocados'), (r'Disculpe, mami', 'Disculpe, Mabel'),
       (r'actividad mica', 'actividad mixta'), (r'atención mixed', 'atención mixta'), (r'su agente y su finanza', 'su agenda y sus finanzas'),
       (r'Te estoy viendo todo y', 'Le estoy enviando todo a'), (r'propio AM', 'propio gimnasio'), (r'ponelitos', '[talleres]'),
       (r'otra peuta', 'terapeuta'), (r'estimulación sí como triste', 'estimulación psicomotriz'), (r'Maneches', 'Maneje'),
       (r'un bebao con link', 'una app web con link'), (r'anseviario', '[resumen diario]'), (r'médico digital', '[agenda médica digital]')]


def fix(t):
    for a, b in FIX:
        t = re.sub(a, b, t)
    return t.strip()


def main():
    bloques = []
    for l in open(os.path.join(HERE, '_bloques_asr.txt'), encoding='utf-8'):
        m = re.match(r'(\d{3}) \[(\d\d:\d\d)\] ([^:]+): (.*)', l.rstrip('\n'))
        i, t, s, txt = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        bloques.append([i, t, OVERRIDE.get(i, CLUSTER[s]) or 'MABEL', txt])
    out = []
    for i, t, s, txt in bloques:
        sp = next((x for x in SPLIT if x[0] == i), None)
        if sp and sp[1] in txt:
            a, b = txt.split(sp[1], 1)
            out += [[t, s, a], [t, sp[2], sp[1] + b]]
        else:
            out.append([t, s, txt])
    # unir turnos consecutivos del mismo hablante
    turnos = []
    for t, s, txt in out:
        if turnos and turnos[-1][1] == s:
            turnos[-1][2] += ' ' + txt
        else:
            turnos.append([t, s, txt])
    md = ['# Transcripción · Retroalimentación INACAP I+E con Sercotec y la clienta',
          '', '**Reunión:** “Retroalimentación Inacap I+E – Servicio de atención kinesiológica” · Google Meet · 12 de noviembre de 2026, 08:33 · duración 40:40',
          '', '## Participantes', '',
          '| Interlocutor | Rol en la reunión | Cómo se identificó |', '|---|---|---|',
          '| **Mabel Aceituno Romero** | Encargada de Sercotec del caso: coordina la reunión, comparte pantalla y lee los trabajos | Nombre en Meet y polera con logo de Sercotec; Ariel le agradece “la gestión de conectarnos y el apoyo… este semestre” [40:05] |',
          '| **Ariel O\'Nell** | Profesor a cargo de la actividad (INACAP, Innovación y Emprendimiento) | Nombre en Meet; “yo estoy 100 % en INACAP” [05:13]; presenta los trabajos y su sentido |',
          '| **Klga. Josselyn Toledo** | Clienta del caso: kinesióloga y psicomotricista acuática | Nombre en Meet (“Klga Josselyn Toledo”) |',
          '| **Ana Luisa Aguilera** | Docente INACAP de otra sección que también trabajó el caso; se conecta en tránsito | Mabel la saluda como “profesora” y ella responde que va “camino a la sede” [08:28–08:33]; al cierre dice “tengo clases ahora precisamente con la sección que estuvo trabajando con Josselyn” [39:29] |',
          '', '> Roberto Escobar Donoso, profesor de nuestra sección, no participó en la reunión.',
          '', '> **Nota de método.** Transcripción automática (Whisper, español) con identificación de voces (ECAPA) y verificación visual en el video. '
          'Se corrigieron nombres propios, lugares y términos del caso. Los fragmentos entre corchetes son palabras dudosas. '
          'Puede haber errores menores de reconocimiento; ante una cita textual importante, verificar en la grabación con el minuto indicado.', '',
          '## Transcripción', '']
    for t, s, txt in turnos:
        md.append(f'**[{t}] {NOMBRE[s]}:** {fix(txt)}')
        md.append('')
    open(os.path.join(HERE, 'Transcripcion_reunion_2026-11-12.md'), 'w', encoding='utf-8').write('\n'.join(md))
    print('ok', len(turnos), 'turnos')


if __name__ == '__main__':
    main()
