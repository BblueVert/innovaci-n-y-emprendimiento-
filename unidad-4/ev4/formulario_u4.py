# 4.1.3.1 Formulario de postulación a fondo concursable (Datos básicos del proyecto) llenado con el contenido del equipo.
# Uso: python3 formulario_u4.py → entregables/4.1.3.1_Formulario_Postulacion_Copiloto_Kine.docx
# Los datos personales (RUT, correo, teléfono), el líder y la experiencia emprendedora quedan en blanco para cada integrante.
import os
import docx
from docx.shared import Pt, RGBColor
import contenido_u4 as C

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'material', 'plantillas', 'FGIE03_MC_U04S16_Datos_Basicos_del_Proyecto.docx')
OUT = os.path.join(HERE, 'entregables', '4.1.3.1_Formulario_Postulacion_Copiloto_Kine.docx')


def fill(cell, text):
    cell.text = ''
    parts = [x for x in text.split('\n') if x.strip()] or ['']
    p = cell.paragraphs[0]
    for i, line in enumerate(parts):
        if i:
            p = cell.add_paragraph()
        r = p.add_run(line)
        r.font.size = Pt(10)
        r.font.name = 'Arial'


def mark(table, options):
    for row in table.rows:
        if row.cells[1].text.strip() in options:
            fill(row.cells[0], 'X')
            row.cells[0].paragraphs[0].runs[0].bold = True
            row.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xC2, 0x41, 0x0C)


def main():
    d = docx.Document(SRC)
    t = d.tables
    F = C.FORM
    fill(t[0].cell(0, 0), F['titulo'])
    fill(t[1].cell(0, 0), F['resumen'])
    mark(t[2], F['ods'])
    fill(t[4].cell(0, 0), F['desafio'])
    fill(t[5].cell(0, 0), F['problema'])
    fill(t[6].cell(0, 0), F['consecuencias'])
    fill(t[7].cell(0, 0), F['mercado'])
    mark(t[8], [F['tipo']])
    fill(t[9].cell(0, 0), F['solucion'])
    fill(t[10].cell(0, 0), F['novedad'])
    fill(t[11].cell(0, 0), F['canales'])
    fill(t[12].cell(0, 0), F['actividades'])
    fill(t[13].cell(0, 0), F['costos'])
    fill(t[14].cell(0, 0), F['ingresos'])
    # equipo: solo nombre y apellido paterno (RUT, correo y teléfono los completa cada integrante)
    for i, nombre in enumerate(C.EQUIPO, 1):
        partes = nombre.split()
        fill(t[15].cell(i, 1), partes[0])
        fill(t[15].cell(i, 2), partes[1])
        if len(partes) > 2:
            fill(t[15].cell(i, 3), partes[2])
    fill(t[16].cell(0, 0), F['equipo_desc'])
    mark(t[18], [F['programa']])
    fill(t[20].cell(0, 0), F['carrera'])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d.save(OUT)
    print('ok', OUT)


if __name__ == '__main__':
    main()
