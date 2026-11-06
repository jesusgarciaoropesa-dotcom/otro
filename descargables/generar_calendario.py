"""Genera el calendario de siembra en maceta (interior peninsular) en PDF.

Datos de siembra: web/src/data/calculadora-cultivos.ts (los mismos de la calculadora de la web).
Datos de heladas: AEMET, valores climatológicos normales de Toledo (estación 3260B).
Uso: python3 descargables/generar_calendario.py
"""
import re, pathlib
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "descargables" / "calendario-siembra-balcon-interior.pdf"
F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Serif-B", F + "DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", F + "DejaVuSans-Bold.ttf"))

HOJA, HOJA_OSC, TIERRA, MOSTAZA, CREMA = map(HexColor, ["#3f6b3a", "#24401f", "#a8562f", "#d9a441", "#faf3e6"])
GRIS = HexColor("#6b6b6b"); LINEA = HexColor("#e2d8c3")

ts = (RAIZ / "web/src/data/calculadora-cultivos.ts").read_text(encoding="utf-8")
cultivos = []
for m in re.finditer(r"\{ nombre: '([^']+)'.*?tipo: '(\w+)', meses: \[([\d, ]+)\].*?facil: (true|false)", ts):
    cultivos.append((m.group(1), m.group(2), [int(x) for x in m.group(3).split(",")], m.group(4) == "true"))
GRUPOS = [("hortaliza", "Hortalizas de fruto y legumbres"), ("hoja", "Hojas"), ("raiz", "Raíces y bulbos"),
          ("aromatica", "Aromáticas"), ("fruta", "Frutales y frutos rojos")]
MESES = ["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

# AEMET Toledo 3260B: mínima media (°C) y días de helada por mes
TM = [1.3, 2.6, 5.0, 7.2, 11.0, 15.9, 18.9, 18.6, 14.9, 10.2, 5.3, 2.5]
DH = [12.7, 6.9, 2.3, 0.3, 0, 0, 0, 0, 0, 0, 3.3, 9.8]

W, H = landscape(A4)
c = canvas.Canvas(str(SALIDA), pagesize=(W, H))
c.setTitle("Calendario de siembra en maceta · interior peninsular · MiHuertoUrbano")
c.setAuthor("MiHuertoUrbano")

def fondo():
    c.setFillColor(CREMA); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HOJA_OSC); c.rect(0, H - 62, W, 62, fill=1, stroke=0)
    c.setFillColor(GRIS); c.setFont("Sans", 7.5)
    c.drawRightString(W - 30, 16, "mihuertourbano.xyz")

# ---------- Página 1: tabla ----------
fondo()
c.setFillColor(white); c.setFont("Serif-B", 20)
c.drawString(30, H - 36, "Calendario de siembra en maceta")
c.setFont("Sans", 10); c.setFillColor(MOSTAZA)
c.drawString(30, H - 52, "Para balcón y terraza en el interior peninsular · MiHuertoUrbano")

ordenados = [(g, t, [x for x in cultivos if x[1] == g]) for g, t in GRUPOS]
filas = sum(len(x[2]) + 1 for x in ordenados)
x0, ancho_nombre = 30, 170
ancho_mes = (W - 60 - ancho_nombre) / 12
y_top = H - 92
alto = min(13.2, (y_top - 70) / (filas + 1))

c.setFont("Sans-B", 8.5); c.setFillColor(HOJA_OSC)
for i, m in enumerate(MESES):
    c.drawCentredString(x0 + ancho_nombre + ancho_mes * (i + .5), y_top + 4, m)
y = y_top
for g, titulo, lista in ordenados:
    y -= alto
    c.setFont("Sans-B", 8.2); c.setFillColor(TIERRA); c.drawString(x0, y + 3, titulo.upper())
    for nombre, _, meses, facil in lista:
        y -= alto
        c.setStrokeColor(LINEA); c.setLineWidth(.4); c.line(x0, y, W - 30, y)
        c.setFont("Sans", 8.2); c.setFillColor(HexColor("#222222"))
        c.drawString(x0 + 6, y + 3, nombre + ("  ★" if facil else ""))
        for mth in meses:
            c.setFillColor(HOJA)
            c.roundRect(x0 + ancho_nombre + ancho_mes * (mth - 1) + 1.5, y + 1.8, ancho_mes - 3, alto - 3.6, 2.5, fill=1, stroke=0)
# leyenda
c.setFillColor(HOJA); c.roundRect(30, 38, 22, 9, 2.5, fill=1, stroke=0)
c.setFillColor(HexColor("#222222")); c.setFont("Sans", 8)
c.drawString(57, 40, "Mes recomendado para sembrar o plantar.   ★ Fácil para empezar.")
c.setFillColor(GRIS); c.setFont("Sans", 7.2)
c.drawString(30, 26, "Fechas orientativas de clima mediterráneo. En el interior, con inviernos más fríos, las siembras de primavera se retrasan de 15 días a un mes: mira la página 2.")

# ---------- Página 2: ajustes para el interior ----------
c.showPage(); fondo()
c.setFillColor(white); c.setFont("Serif-B", 20)
c.drawString(30, H - 36, "Cómo ajustarlo si vives en el interior")
c.setFont("Sans", 10); c.setFillColor(MOSTAZA)
c.drawString(30, H - 52, "Heladas de media en Toledo (AEMET) y qué significan para tu balcón")

# gráfico de días de helada
gx, gy, gw, gh = 30, H - 300, 400, 190
c.setFillColor(HOJA_OSC); c.setFont("Sans-B", 10); c.drawString(gx, gy + gh + 22, "Días de helada al mes (media)")
bw = gw / 12; maxdh = 14
for i, d in enumerate(DH):
    h = gh * d / maxdh
    c.setFillColor(TIERRA if d >= 1 else LINEA)
    c.rect(gx + bw * i + 4, gy, bw - 8, max(h, 1.2), fill=1, stroke=0)
    c.setFillColor(HexColor("#222222")); c.setFont("Sans", 7.5)
    if d: c.drawCentredString(gx + bw * (i + .5), gy + h + 3, f"{d:.1f}".replace(".", ","))
    c.setFont("Sans-B", 8); c.drawCentredString(gx + bw * (i + .5), gy - 12, MESES[i])
    c.setFont("Sans", 6.8); c.setFillColor(GRIS)
    c.drawCentredString(gx + bw * (i + .5), gy - 23, f"{TM[i]:.1f}°".replace(".", ","))
c.setFont("Sans", 7); c.drawString(gx, gy - 35, "Debajo de cada mes: temperatura mínima media. Unos 35 días de helada al año, casi todos de diciembre a febrero.")

# consejos
tx, ty = 470, H - 100
consejos = [
    ("Primavera: espera a que pase el frío", "En Toledo aún hiela algún día en marzo y, de forma rara, en abril. Los de calor (tomate, pimiento, berenjena, calabacín, albahaca) se siembran en semillero dentro de casa y se sacan al balcón cuando las noches ya no bajan de unos grados."),
    ("Retrasa las siembras de 15 días a un mes", "Es el ajuste que recomiendan los huertos escolares del Ayuntamiento de Madrid para las zonas más frías. Si en la tabla pone marzo, piensa en finales de marzo o abril."),
    ("Otoño: siembra pronto", "De septiembre a noviembre la mínima media baja de 14,9 °C a 5,3 °C. Lo de hoja, mejor en septiembre y octubre; en noviembre ya hay unos 3 días de helada, aunque ajos y habas aún se plantan."),
    ("Invierno: protege, no siembres fuera", "Ajos, habas y hojas aguantan. Lo delicado, con velo antiheladas, junto a la pared y con la maceta separada del suelo. Riega poco: el sustrato tarda en secarse."),
]
for tit, txt in consejos:
    c.setFillColor(HOJA_OSC); c.setFont("Sans-B", 10); c.drawString(tx, ty, tit)
    ty -= 14
    from reportlab.lib.utils import simpleSplit
    c.setFillColor(HexColor("#222222")); c.setFont("Sans", 8.6)
    for ln in simpleSplit(txt, "Sans", 8.6, W - tx - 30):
        c.drawString(tx, ty, ln); ty -= 11.5
    ty -= 12

# guías + fuentes
c.setFillColor(HOJA_OSC); c.setFont("Sans-B", 10); c.drawString(30, 150, "Para cada mes, la guía completa en la web:")
c.setFillColor(TIERRA); c.setFont("Sans", 9)
c.drawString(30, 135, "mihuertourbano.xyz/articulos/calendario-siembra-completo-mes-a-mes/")
c.drawString(30, 121, "mihuertourbano.xyz/que-plantar-en-tu-balcon/  (calculadora según tu luz y tu mes)")
c.linkURL("https://mihuertourbano.xyz/articulos/calendario-siembra-completo-mes-a-mes/", (30, 132, 380, 145))
c.linkURL("https://mihuertourbano.xyz/que-plantar-en-tu-balcon/", (30, 118, 300, 131))
c.setFillColor(GRIS); c.setFont("Sans", 7)
fuentes = [
    "Fuentes: AEMET, valores climatológicos normales de Toledo, estación 3260B (aemet.es, serie 1981-2010).",
    "Ayuntamiento de Madrid, Huertos escolares sostenibles, «Calendario de cultivo» (2018): en zonas más frías las fechas se retrasan de 15 días a un mes.",
    "En un balcón de ciudad suele helar algo menos que en la estación meteorológica. Ajusta siempre a lo que veas en tu zona.",
]
yy = 70
for f_ in fuentes:
    c.drawString(30, yy, f_); yy -= 10
c.save()
print(SALIDA, len(cultivos), "cultivos")
