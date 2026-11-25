# Speech del pitch en PDF (A4) con la identidad del proyecto. Uso: python3 speech_pdf.py
import os
from weasyprint import HTML
import contenido_u4 as C

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '..', 'unidad-3', 'ev3', 'fonts')
OUT = os.path.join(HERE, 'entregables', 'Pitch_Speech_Copiloto_Kine.pdf')
PARTES = [('Pitch', 'Claudia', '0:00 – 0:05', '1', C.PITCH_FRASE)] + [
    (t, C.PITCH_QUIEN[t], r, d, x) for (t, x), r, d in zip(C.PITCH, ['0:05 – 0:50', '0:50 – 1:40', '1:40 – 2:35', '2:35 – 3:20'], ['3 → 46', '48 → 49', '50 → 52', '56 → 58 → 59'])]
COL = {'Claudia': '#7B3FA0', 'Néstor': '#FF6B35', 'Francisco': '#1F9D6B', 'Benjamín': '#1C8AD1'}

secs = ''.join(f'''<section style="border-left:2.2mm solid {COL[q]}">
<div class="meta"><span class="q" style="color:{COL[q]}">{q}</span><span>{t}</span><span class="r">{r} · diapositiva{'s' if '→' in d else ''} {d}</span></div>
<p class="{'frase' if t == 'Pitch' else ''}">{x}</p></section>''' for t, q, r, d, x in PARTES)
total = sum(len(x.split()) for _, x in C.PITCH) + len(C.PITCH_FRASE.split())
html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{{font-family:Bebas;src:url(file://{FONTS}/bebas-neue-latin-400-normal.woff2)}}
@font-face{{font-family:Jakarta;src:url(file://{FONTS}/plus-jakarta-sans-latin-400-normal.woff2)}}
@font-face{{font-family:Jakarta;font-weight:700;src:url(file://{FONTS}/plus-jakarta-sans-latin-700-normal.woff2)}}
@font-face{{font-family:Mono;src:url(file://{FONTS}/dm-mono-latin-400-normal.woff2)}}
@page{{size:A4;margin:16mm 17mm 16mm 17mm;@bottom-left{{content:"Copiloto Kine · Pitch · Innovación y Emprendimiento III · INACAP Rancagua";font-family:Mono;font-size:7pt;color:#8A86A6}}@bottom-right{{content:counter(page) " / " counter(pages);font-family:Mono;font-size:7pt;color:#8A86A6}}}}
body{{font-family:Jakarta,sans-serif;color:#17142A;margin:0}}
.k{{font-family:Mono;font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:#C2410C}}
h1{{font-family:Bebas;font-weight:400;font-size:40pt;line-height:.95;margin:2mm 0 2mm}}
h1 em{{font-style:normal;color:#FF6B35}}
.sub{{font-size:10pt;color:#5E5878;margin-bottom:6mm}}
.order{{display:flex;gap:2mm;margin-bottom:7mm}}.order div{{flex:1;border:1px solid #E3DEF2;border-radius:2mm;padding:2mm 2.5mm;font-size:8pt}}.order b{{display:block;font-size:9pt}}
section{{padding:1mm 0 1mm 6mm;margin:0 0 5.5mm;break-inside:avoid}}
.meta{{display:flex;gap:4mm;align-items:baseline;font-family:Mono;font-size:8.5pt;letter-spacing:.08em;text-transform:uppercase;color:#5E5878;margin-bottom:2mm}}
.meta .q{{font-family:Bebas;font-size:22pt;letter-spacing:.02em;text-transform:none}}.meta .r{{margin-left:auto}}
p{{font-size:13.6pt;line-height:1.5;margin:0}}
p.frase{{font-family:Bebas;font-size:26pt;line-height:1.05;color:#C2410C}}
.tips{{background:#F6F4FC;border-radius:3mm;padding:4mm 5mm;font-size:9.5pt;line-height:1.5;break-inside:avoid}}.tips b{{font-family:Bebas;font-size:16pt;font-weight:400;display:block}}
</style></head><body>
<div class="k">Guion del pitch · instrumento 4.1.3.2</div>
<h1>COPILOTO KINE · <em>PITCH DE 3:15</em></h1>
<div class="sub">4 integrantes · {total} palabras · ~130 palabras por minuto · límite 3:30</div>
<div class="order"><div><b>1 · Quién eres</b>Claudia</div><div><b>2 · Qué haces</b>Néstor</div><div><b>3 · Por qué es único</b>Francisco</div><div><b>4 · Objetivo</b>Benjamín</div></div>
{secs}
<div class="tips"><b>Para grabar</b>
Cada parte dura 50 segundos como máximo; si alguien se pasa, acorta su frase más larga, nunca el cierre. Los cambios de persona no deberían tomar más de 2 segundos: quien termina mira al siguiente. Mientras habla Néstor, si pueden, muestren la app en un celular real (diapositiva 49 o el QR de la 58).</div>
</body></html>'''
HTML(string=html).write_pdf(OUT)
print('ok', OUT)
