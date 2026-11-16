"""Guía-calendario de siembra en maceta (interior peninsular) de MiHuertoUrbano, en PDF.

HTML + CSS con las fuentes y colores de la web, convertido a PDF con Chromium (Playwright).
Datos de cultivos: web/src/data/calculadora-cultivos.ts (los mismos de la calculadora de la web).
Datos de heladas: AEMET, valores climatológicos normales de Toledo (estación 3260B, 1981-2010).

Uso:  python3 descargables/calendario/generar.py
Sale: descargables/calendario-siembra-balcon-interior.pdf (y copia en web/public/descargables/)
"""
import base64, io, pathlib, re, shutil
from PIL import Image
import qrcode, qrcode.image.svg

RAIZ = pathlib.Path(__file__).resolve().parents[2]
WEB = RAIZ / "web"
SALIDA = RAIZ / "descargables" / "calendario-siembra-balcon-interior.pdf"
PUBLICO = WEB / "public" / "descargables" / SALIDA.name
FUENTES = WEB / "node_modules" / "@fontsource-variable"

# ---------------------------------------------------------------- datos
ts = (WEB / "src/data/calculadora-cultivos.ts").read_text(encoding="utf-8")
cultivos = []
for linea in ts.splitlines():
    if "nombre: '" not in linea:
        continue
    g = lambda k, pat=r"'([^']*)'": (re.search(rf"\b{k}: {pat}", linea) or [None, None])[1]
    cultivos.append({
        "nombre": g("nombre"), "slug": g("slug"), "luz": g("luz"), "tipo": g("tipo"),
        "meses": [int(x) for x in g("meses", r"\[([\d, ]+)\]").split(",")],
        "familia": g("familia"), "facil": g("facil", r"(true|false)") == "true",
        "dias": int(g("dias", r"(\d+)")) if g("dias", r"(\d+)") else None,
        "buenas": re.findall(r"'([^']+)'", g("buenas", r"\[([^\]]*)\]") or ""),
        "nota": g("nota"),
    })
assert len(cultivos) > 30, "No se han leído bien los cultivos"

GRUPOS = [("hortaliza", "Hortalizas de fruto y legumbres"), ("hoja", "Hojas"),
          ("raiz", "Raíces y bulbos"), ("aromatica", "Aromáticas"), ("fruta", "Frutales y frutos rojos")]
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
         "Septiembre", "Octubre", "Noviembre", "Diciembre"]
LUZ = {"pleno": ("Pleno sol", "6 h o más de sol directo"),
       "media": ("Semisombra", "3-5 h de sol o sol de media jornada"),
       "sombra": ("Poca luz", "tolera balcones con poco sol")}
# AEMET Toledo 3260B: temperatura mínima media (°C) y días de helada por mes
TM = [1.3, 2.6, 5.0, 7.2, 11.0, 15.9, 18.9, 18.6, 14.9, 10.2, 5.3, 2.5]
DH = [12.7, 6.9, 2.3, 0.3, 0, 0, 0, 0, 0, 0, 3.3, 9.8]
NOTA_MES = {  # lo que dicen los datos de AEMET de cada mes, en palabras
    0: "El mes más frío: casi 13 días de helada de media. Nada delicado fuera sin protección.",
    1: "Aún hiela unos 7 días. Buen momento para empezar el semillero dentro de casa.",
    2: "Las heladas se vuelven raras (unos 2 días). Siembra en semillero lo de calor.",
    3: "Hiela muy poco y la mínima ronda los 7 °C. Las plantas de calor, mejor a finales.",
    4: "Sin heladas y con mínimas de 11 °C: ya puede salir todo al balcón.",
    5: "Mínimas de casi 16 °C. Riega a primera hora o al atardecer.",
    6: "El mes más caluroso. Riego diario en maceta y sombreo en las horas fuertes.",
    7: "Sigue el calor (mínimas de 18,6 °C). Prepara semilleros de otoño a la sombra.",
    8: "Las noches refrescan: buen mes para sembrar lo de hoja.",
    9: "Mínimas de 10 °C. Último gran mes de siembra de hojas y raíces.",
    10: "Vuelven las heladas (unos 3 días). Ajos y habas aún se plantan.",
    11: "Unos 10 días de helada. Protege con velo y riega muy poco.",
}

# ---------------------------------------------------------------- recursos
def fuente(familia, archivo):
    return base64.b64encode((FUENTES / familia / "files" / archivo).read_bytes()).decode()

def foto(ruta, ancho=1600, recorte=None, calidad=78):
    im = Image.open(WEB / "public" / ruta).convert("RGB")
    if recorte:  # (izq, arriba, der, abajo) en fracciones, p. ej. para quitar la marca de agua
        w, h = im.size
        im = im.crop((int(recorte[0] * w), int(recorte[1] * h), int(recorte[2] * w), int(recorte[3] * h)))
    if im.width > ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=calidad, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def qr(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=0)
    s = img.to_string(encoding="unicode")
    return re.sub(r'<\?xml[^>]*>', "", s).replace('fill="#000000"', 'fill="#24401f"')

LOGO = "data:image/png;base64," + base64.b64encode((WEB / "public/images/logo-full.png").read_bytes()).decode()
PORTADA = foto("images/hero-huerto.jpg", 1800, calidad=80)
FOTO_CLIMA = foto("images/articulos/balcon-otono-amanecer.jpg", 1400, recorte=(0, 0, 0.86, 0.86))
FOTO_LUZ = foto("images/articulos/cuantas-horas-sol-balcon.jpg", 1200, recorte=(0, 0, 0.86, 0.86))
FOTO_FACIL = foto("images/articulos/balcon-cosecha-atardecer.jpg", 1400, recorte=(0, 0, 0.86, 0.86))
FOTO_INVERNADERO = foto("images/articulos/mini-invernadero-estanteria-balcon.jpg", 1400, recorte=(0, 0.05, 0.86, 0.86))
FOTO_SEMILLERO = foto("images/articulos/semillero-bandeja-alveolos-tomate.jpg", 1200, recorte=(0, 0, 0.86, 0.86))

# ---------------------------------------------------------------- piezas
ICONO_LUZ = {
    "pleno": '<svg viewBox="0 0 16 16" class="ico"><circle cx="8" cy="8" r="3.4" fill="#d9a441"/><g stroke="#d9a441" stroke-width="1.4" stroke-linecap="round"><path d="M8 1.2v2M8 12.8v2M1.2 8h2M12.8 8h2M3.2 3.2l1.4 1.4M11.4 11.4l1.4 1.4M3.2 12.8l1.4-1.4M11.4 4.6l1.4-1.4"/></g></svg>',
    "media": '<svg viewBox="0 0 16 16" class="ico"><circle cx="6.5" cy="6.5" r="3" fill="#d9a441"/><path d="M5 13.5h7.2a2.6 2.6 0 0 0 .3-5.2 3.5 3.5 0 0 0-6.6 1A2.1 2.1 0 0 0 5 13.5z" fill="#9db59a"/></svg>',
    "sombra": '<svg viewBox="0 0 16 16" class="ico"><path d="M3.5 13h8.7a3 3 0 0 0 .3-6 4 4 0 0 0-7.6 1.1A2.5 2.5 0 0 0 3.5 13z" fill="#7d9579"/></svg>',
}
ESTRELLA = '<span class="estrella" title="Fácil para empezar">★</span>'

def barras(meses):
    """12 celdas; los meses de siembra seguidos se pintan como una barra continua."""
    celdas = []
    for m in range(1, 13):
        if m in meses:
            ini = (m - 1) not in meses or m == 1
            fin = (m + 1) not in meses or m == 12
            celdas.append(f'<td class="m on{" ini" if ini else ""}{" fin" if fin else ""}"><i></i></td>')
        else:
            celdas.append('<td class="m"></td>')
    return "".join(celdas)

def tabla(grupos):
    filas = []
    for clave, titulo in grupos:
        lista = [c for c in cultivos if c["tipo"] == clave]
        filas.append(f'<tr class="grupo"><th colspan="15">{titulo}</th></tr>')
        for c in lista:
            dias = f'{c["dias"]} d' if c["dias"] else "—"
            filas.append(
                f'<tr><td class="nombre">{c["nombre"]}{ESTRELLA if c["facil"] else ""}</td>'
                f'<td class="luz">{ICONO_LUZ[c["luz"]]}</td>{barras(c["meses"])}'
                f'<td class="dias">{dias}</td></tr>')
    cab = "".join(f'<th class="m">{m[:3]}</th>' for m in MESES)
    return (f'<table class="cal"><thead><tr><th class="nombre">Cultivo</th><th class="luz">Luz</th>{cab}'
            f'<th class="dias">Cosecha</th></tr></thead><tbody>{"".join(filas)}</tbody></table>')

def grafica_heladas():
    w, h, pad = 520, 170, 28
    bw = (w - pad) / 12
    maxd = 14
    partes = []
    for i, d in enumerate(DH):
        x = pad + i * bw + bw * 0.18
        bh = (h - 40) * d / maxd
        y = h - 22 - bh
        color = "#24401f" if d >= 5 else ("#3f6b3a" if d > 0 else "#e2d8c3")
        partes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw * 0.64:.1f}" height="{max(bh, 2):.1f}" rx="3" fill="{color}"/>')
        if d:
            partes.append(f'<text x="{x + bw * 0.32:.1f}" y="{y - 5:.1f}" class="v">{str(d).replace(".", ",")}</text>')
        partes.append(f'<text x="{x + bw * 0.32:.1f}" y="{h - 8}" class="mes">{MESES[i][:3]}</text>')
    # línea de mínimas
    pts = " ".join(f'{pad + i * bw + bw / 2:.1f},{h - 22 - (h - 40) * (t / 20):.1f}' for i, t in enumerate(TM))
    partes.append(f'<polyline points="{pts}" fill="none" stroke="#d9a441" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, t in enumerate(TM):
        cx, cy = pad + i * bw + bw / 2, h - 22 - (h - 40) * (t / 20)
        partes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="#fff" stroke="#d9a441" stroke-width="2"/>')
    return f'<svg viewBox="0 0 {w} {h}" class="grafica">{"".join(partes)}</svg>'

def tarjetas_mes(desde, hasta):
    out = []
    for i in range(desde, hasta):
        lista = [c for c in cultivos if (i + 1) in c["meses"]]
        lista.sort(key=lambda c: (not c["facil"], c["nombre"]))
        chips = "".join(f'<span class="chip{" facil" if c["facil"] else ""}">{c["nombre"]}</span>' for c in lista) \
            or '<span class="vacio">Mes de cuidados y cosecha: poca siembra.</span>'
        helada = f'{str(DH[i]).replace(".", ",")} días de helada' if DH[i] else "Sin heladas"
        out.append(f'''
        <article class="mes-card">
          <header><span class="num">{i + 1:02d}</span><h3>{MESES[i]}</h3>
            <span class="clima">{helada} · mín. {str(TM[i]).replace(".", ",")} °C · {len(lista)} cultivos</span></header>
          <p class="nota-mes">{NOTA_MES[i]}</p>
          <div class="chips">{chips}</div>
        </article>''')
    return "".join(out)

faciles = sorted([c for c in cultivos if c["facil"] and c["dias"]], key=lambda c: c["dias"])[:10]
def ficha(c):
    meses = ", ".join(MESES[m - 1].lower() for m in c["meses"])
    vecinos = ", ".join(c["buenas"][:3]) if c["buenas"] else "—"
    return f'''<div class="ficha"><div class="ficha-top"><h4>{c["nombre"]}</h4><span class="dias-big">{c["dias"]}<small> días</small></span></div>
      <p>{c["nota"]}</p>
      <dl><dt>Siembra</dt><dd>{meses}</dd><dt>Luz</dt><dd>{ICONO_LUZ[c["luz"]]} {LUZ[c["luz"]][0]}</dd><dt>Buenos vecinos</dt><dd>{vecinos}</dd></dl></div>'''

def pie(n, claro=False):
    return f'<div class="pie{" claro" if claro else ""}"><span>MiHuertoUrbano · Calendario de siembra en maceta</span><span>mihuertourbano.xyz · {n}</span></div>'

QR_WEB = qr("https://mihuertourbano.xyz/que-plantar-en-tu-balcon/")
QR_MES = qr("https://mihuertourbano.xyz/articulos/calendario-siembra-completo-mes-a-mes/")
N = len(cultivos); NF = sum(c["facil"] for c in cultivos)

# ---------------------------------------------------------------- HTML
html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Calendario de siembra en maceta · MiHuertoUrbano</title>
<style>
@font-face {{ font-family: Fraunces; src: url(data:font/woff2;base64,{fuente("fraunces", "fraunces-latin-wght-normal.woff2")}) format("woff2"); font-weight: 100 900; }}
@font-face {{ font-family: Inter; src: url(data:font/woff2;base64,{fuente("inter", "inter-latin-wght-normal.woff2")}) format("woff2"); font-weight: 100 900; }}
@page {{ size: A4; margin: 0; }}
:root {{ --hoja:#3f6b3a; --hoja-osc:#24401f; --tierra:#a8562f; --mostaza:#d9a441; --crema:#faf3e6; --linea:#e7dcc6; --texto:#2b2b26; --suave:#6f6a5e; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: Inter, sans-serif; color: var(--texto); font-size: 9.6pt; line-height: 1.45; }}
.pagina {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; background: #fffdf8; padding: 18mm 16mm 20mm; }}
.pagina:last-child {{ page-break-after: auto; }}
h1, h2, h3, h4 {{ font-family: Fraunces, serif; color: var(--hoja-osc); font-weight: 650; line-height: 1.08; }}
h2 {{ font-size: 25pt; letter-spacing: -.01em; }}
.antetitulo {{ font-size: 7.6pt; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; color: var(--tierra); margin-bottom: 2.5mm; }}
.entradilla {{ font-size: 10.5pt; color: var(--suave); max-width: 150mm; margin-top: 3mm; }}
.pie {{ position: absolute; left: 16mm; right: 16mm; bottom: 9mm; display: flex; justify-content: space-between; font-size: 7pt; color: var(--suave); border-top: .6pt solid var(--linea); padding-top: 2.5mm; }}
.pie.claro {{ color: rgba(255,255,255,.8); border-color: rgba(255,255,255,.3); }}
.ico {{ width: 11pt; height: 11pt; vertical-align: -2pt; }}
.estrella {{ color: var(--mostaza); margin-left: 3pt; font-size: 8pt; }}

/* portada */
.portada {{ padding: 0; background: var(--hoja-osc); }}
.portada .img {{ position: absolute; inset: 0; background: url({PORTADA}) 64% center / cover; }}
.portada .velo {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(20,34,17,.55) 0%, rgba(20,34,17,0) 26%, rgba(20,34,17,0) 42%, rgba(20,34,17,.88) 70%, rgba(20,34,17,.97) 100%); }}
.portada .marca {{ position: absolute; top: 14mm; left: 16mm; right: 16mm; display: flex; justify-content: space-between; align-items: center; color: #fff; }}
.portada .marca img {{ height: 15mm; background: rgba(255,253,248,.92); border-radius: 3mm; padding: 1.6mm 3mm; }}
.portada .marca span {{ font-size: 7.5pt; letter-spacing: .2em; text-transform: uppercase; font-weight: 600; }}
.portada .titulo {{ position: absolute; left: 16mm; right: 16mm; bottom: 30mm; color: #fff; }}
.portada .titulo .antetitulo {{ color: var(--mostaza); }}
.portada h1 {{ color: #fff; font-size: 46pt; letter-spacing: -.02em; }}
.portada h1 em {{ font-style: normal; color: var(--mostaza); }}
.portada .sub {{ font-size: 12.5pt; margin-top: 5mm; max-width: 140mm; color: rgba(255,255,255,.88); }}
.portada .datos {{ display: flex; gap: 9mm; margin-top: 9mm; }}
.portada .datos div {{ border-left: 1.4pt solid var(--mostaza); padding-left: 3mm; }}
.portada .datos b {{ display: block; font-family: Fraunces; font-size: 20pt; color: #fff; font-weight: 600; line-height: 1; }}
.portada .datos small {{ font-size: 7.6pt; color: rgba(255,255,255,.75); text-transform: uppercase; letter-spacing: .1em; }}

/* cómo usar */
.indice {{ display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 8mm; margin-top: 8mm; }}
.indice div {{ display: flex; gap: 3mm; align-items: baseline; border-bottom: .6pt solid var(--linea); padding-bottom: 2mm; }}
.indice b {{ font-family: Fraunces; color: var(--mostaza); font-size: 14pt; width: 8mm; }}
.indice span {{ font-weight: 600; color: var(--hoja-osc); }}
.indice small {{ display: block; color: var(--suave); font-weight: 400; font-size: 8pt; }}
.bloque-foto {{ height: 62mm; border-radius: 4mm; background-size: cover; background-position: center; margin: 9mm 0 7mm; }}
.luces {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; margin-top: 4mm; }}
.luz-card {{ background: var(--crema); border-radius: 3mm; padding: 4mm; }}
.luz-card .ico {{ width: 20pt; height: 20pt; }}
.luz-card h4 {{ font-size: 12pt; margin: 2mm 0 1mm; }}
.luz-card p {{ font-size: 8.4pt; color: var(--suave); }}
.leyenda {{ display: flex; gap: 6mm; flex-wrap: wrap; margin-top: 7mm; font-size: 8.4pt; align-items: center; }}
.leyenda .barra {{ display: inline-block; width: 13mm; height: 3.2mm; border-radius: 2mm; background: var(--hoja); vertical-align: -1pt; margin-right: 1.5mm; }}
.consejo-arriba {{ margin-top: 7mm; background: var(--hoja-osc); color: #fff; border-radius: 3mm; padding: 4.5mm 5mm; font-size: 9pt; }}
.consejo-arriba b {{ color: var(--mostaza); }}

/* clima */
.clima-top {{ display: grid; grid-template-columns: 1.35fr 1fr; gap: 7mm; margin-top: 7mm; align-items: stretch; }}
.caja {{ background: var(--crema); border-radius: 4mm; padding: 5mm; }}
.caja h4 {{ font-size: 11.5pt; margin-bottom: 1mm; }}
.caja .aclara {{ font-size: 7.6pt; color: var(--suave); }}
.grafica {{ width: 100%; margin-top: 3mm; }}
.grafica text {{ font-family: Inter; font-size: 9px; fill: var(--suave); text-anchor: middle; }}
.grafica text.v {{ font-weight: 700; fill: var(--hoja-osc); }}
.leyenda-graf {{ display: flex; gap: 5mm; font-size: 7.4pt; color: var(--suave); margin-top: 1mm; }}
.leyenda-graf i {{ display: inline-block; width: 7mm; height: 2.6mm; border-radius: 1mm; vertical-align: -.5pt; margin-right: 1mm; }}
.dato-grande {{ display: flex; flex-direction: column; justify-content: space-between; background-size: cover; background-position: center; border-radius: 4mm; padding: 5mm; color: #fff; position: relative; overflow: hidden; }}
.dato-grande::before {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(20,34,17,.15), rgba(20,34,17,.85)); }}
.dato-grande > * {{ position: relative; }}
.dato-grande b {{ font-family: Fraunces; font-size: 38pt; line-height: 1; color: var(--mostaza); font-weight: 600; }}
.dato-grande p {{ font-size: 9pt; }}
.consejos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5mm 7mm; margin-top: 8mm; }}
.consejo {{ border-top: 2pt solid var(--mostaza); padding-top: 3mm; }}
.consejo .etq {{ font-size: 7pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--tierra); }}
.consejo h4 {{ font-size: 12.5pt; margin: 1mm 0 1.5mm; }}
.consejo p {{ font-size: 8.8pt; }}
.fuente {{ font-size: 7pt; color: var(--suave); margin-top: 7mm; }}

/* tabla */
.cal {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 6mm; font-size: 8.6pt; }}
.cal thead th {{ font-size: 6.8pt; text-transform: uppercase; letter-spacing: .06em; color: var(--suave); font-weight: 600; padding-bottom: 2mm; border-bottom: 1pt solid var(--hoja-osc); }}
.cal th.nombre, .cal td.nombre {{ text-align: left; width: 44mm; }}
.cal td.nombre {{ font-weight: 550; color: var(--texto); padding: 1.15mm 0; }}
.cal .luz {{ width: 8mm; text-align: center; }}
.cal .dias {{ width: 14mm; text-align: right; color: var(--suave); font-size: 7.8pt; font-variant-numeric: tabular-nums; }}
.cal td {{ border-bottom: .5pt solid var(--linea); }}
.cal tr.grupo th {{ text-align: left; font-family: Fraunces; font-size: 11pt; color: var(--tierra); font-weight: 600; padding: 4mm 0 1.2mm; border-bottom: .8pt solid var(--tierra); }}
.cal td.m {{ padding: 0; }}
.cal td.m:nth-child(3), .cal td.m:nth-child(4), .cal td.m:nth-child(14) {{ background-color: #eeeee4 !important; }}
.cal td.m.on i {{ display: block; height: 3.3mm; background: var(--hoja); margin: 0; }}
.cal td.m.on.ini i {{ border-radius: 2mm 0 0 2mm; margin-left: .6mm; }}
.cal td.m.on.fin i {{ border-radius: 0 2mm 2mm 0; margin-right: .6mm; }}
.cal td.m.on.ini.fin i {{ border-radius: 2mm; }}
.cal tbody tr:not(.grupo):nth-child(even) td {{ background-color: #fcf7ee; }}
.nota-tabla {{ font-size: 7.6pt; color: var(--suave); margin-top: 4mm; }}

/* mes a mes */
.meses {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 5mm; align-items: stretch; }}
.mes-card {{ background: #fff; border: .7pt solid var(--linea); border-radius: 3.5mm; padding: 3.2mm 4mm; display: flex; flex-direction: column; }}
.mes-card header {{ display: grid; grid-template-columns: auto 1fr; column-gap: 3mm; align-items: baseline; border-bottom: .7pt solid var(--linea); padding-bottom: 2mm; }}
.mes-card .num {{ font-family: Fraunces; font-size: 20pt; color: var(--mostaza); font-weight: 600; grid-row: span 2; }}
.mes-card h3 {{ font-size: 15pt; }}
.mes-card .clima {{ font-size: 7.2pt; color: var(--tierra); font-weight: 600; text-transform: uppercase; letter-spacing: .06em; }}
.nota-mes {{ font-size: 7.9pt; color: var(--suave); margin: 2mm 0; line-height: 1.35; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 1mm; }}
.chip {{ font-size: 6.9pt; background: var(--crema); color: var(--hoja-osc); border-radius: 10mm; padding: .45mm 2mm; font-weight: 550; }}
.chip.facil {{ background: var(--hoja); color: #fff; }}
.vacio {{ font-size: 8pt; color: var(--suave); font-style: italic; }}
.meses.amplio .chip {{ font-size: 7.8pt; padding: .8mm 2.6mm; }}
.meses.amplio .chips {{ gap: 1.6mm; }}
.meses.amplio .nota-mes {{ font-size: 8.6pt; margin: 2.5mm 0 3mm; }}
.meses.amplio .mes-card {{ padding: 4.5mm 5mm; min-height: 70mm; }}
.mes-card footer {{ margin-top: auto; padding-top: 2.5mm; font-size: 7pt; color: var(--suave); }}

/* fáciles */
.fichas {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 5mm; margin-top: 6mm; }}
.ficha {{ border: .7pt solid var(--linea); border-radius: 3mm; padding: 3.5mm 4mm; background: #fff; }}
.ficha-top {{ display: flex; justify-content: space-between; align-items: baseline; }}
.ficha h4 {{ font-size: 12.5pt; }}
.dias-big {{ font-family: Fraunces; font-size: 15pt; color: var(--hoja); font-weight: 600; }}
.dias-big small {{ font-size: 7.5pt; font-family: Inter; color: var(--suave); font-weight: 500; }}
.ficha p {{ font-size: 8.4pt; margin: 1.2mm 0 2mm; }}
.ficha dl {{ display: grid; grid-template-columns: auto 1fr; gap: .6mm 3mm; font-size: 7.6pt; }}
.ficha dt {{ color: var(--tierra); font-weight: 600; }}
.foto-banda {{ height: 52mm; border-radius: 4mm; background-size: cover; background-position: center 40%; margin-top: 6mm; }}

/* diario */
.diario {{ width: 100%; border-collapse: collapse; margin-top: 6mm; font-size: 8pt; }}
.diario th {{ text-align: left; font-size: 6.8pt; text-transform: uppercase; letter-spacing: .08em; color: var(--suave); border-bottom: 1pt solid var(--hoja-osc); padding: 0 2mm 2mm 0; }}
.diario td {{ height: 9.4mm; border-bottom: .6pt solid var(--linea); }}

/* contraportada */
.final {{ background: var(--hoja-osc); color: #fff; }}
.final h2 {{ color: #fff; }}
.final .entradilla {{ color: rgba(255,255,255,.82); }}
.qrs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7mm; margin-top: 11mm; }}
.qr-card {{ background: #fffdf8; color: var(--texto); border-radius: 4mm; padding: 6mm; display: grid; grid-template-columns: 30mm 1fr; gap: 5mm; align-items: center; }}
.qr-card svg {{ width: 30mm; height: 30mm; }}
.qr-card h4 {{ font-size: 13pt; margin-bottom: 1.5mm; }}
.qr-card p {{ font-size: 8.4pt; color: var(--suave); }}
.qr-card a {{ color: var(--tierra); font-size: 7.6pt; font-weight: 600; text-decoration: none; word-break: break-all; }}
.final .lista {{ margin-top: 11mm; display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 8mm; }}
.final .lista div {{ border-top: 1pt solid rgba(255,255,255,.25); padding-top: 3mm; font-size: 9pt; color: rgba(255,255,255,.88); }}
.final .lista b {{ display: block; font-family: Fraunces; font-size: 12pt; color: var(--mostaza); font-weight: 600; margin-bottom: 1mm; }}
.final .fuentes {{ position: absolute; left: 16mm; right: 16mm; bottom: 22mm; font-size: 7pt; color: rgba(255,255,255,.65); }}
.final .logo-final {{ position: absolute; right: 16mm; top: 18mm; height: 13mm; background: #fffdf8; border-radius: 3mm; padding: 1.6mm 3mm; }}
</style></head><body>

<section class="pagina portada">
  <div class="img"></div><div class="velo"></div>
  <div class="marca"><img src="{LOGO}" alt="MiHuertoUrbano"><span>Guía descargable</span></div>
  <div class="titulo">
    <div class="antetitulo">Balcón y terraza · Interior peninsular</div>
    <h1>Calendario<br>de siembra<br><em>en maceta</em></h1>
    <p class="sub">Qué sembrar cada mes, cuánto sol necesita cada cultivo y cómo adaptarlo a los inviernos fríos del interior.</p>
    <div class="datos"><div><b>{N}</b><small>cultivos</small></div><div><b>12</b><small>meses</small></div><div><b>{NF}</b><small>fáciles para empezar</small></div></div>
  </div>
</section>

<section class="pagina">
  <div class="antetitulo">Antes de empezar</div>
  <h2>Cómo usar esta guía</h2>
  <p class="entradilla">Está pensada para imprimirla y tenerla a mano junto a las macetas. Las fechas son las de un clima mediterráneo; en la página 3 tienes cómo ajustarlas si vives en el interior, donde los inviernos son más fríos.</p>
  <div class="indice">
    <div><b>3</b><span>El clima del interior<small>Heladas mes a mes y cómo ajustar las fechas</small></span></div>
    <div><b>4</b><span>Calendario anual<small>Los {N} cultivos en una tabla</small></span></div>
    <div><b>6</b><span>Mes a mes<small>Qué sembrar cada mes, de un vistazo</small></span></div>
    <div><b>8</b><span>Los 10 más fáciles<small>Para estrenarte con buen pie</small></span></div>
    <div><b>9</b><span>Mi diario de siembra<small>Para apuntar lo que siembras</small></span></div>
    <div><b>10</b><span>Más ayuda en la web<small>Calculadora y guía de cada mes</small></span></div>
  </div>
  <div class="bloque-foto" style="background-image:url({FOTO_LUZ})"></div>
  <div class="antetitulo">Lo primero: mira cuánto sol le da a tu balcón</div>
  <div class="luces">
    <div class="luz-card">{ICONO_LUZ["pleno"]}<h4>Pleno sol</h4><p>6 horas o más de sol directo. Puedes con todo, también tomates, pimientos y calabacines.</p></div>
    <div class="luz-card">{ICONO_LUZ["media"]}<h4>Semisombra</h4><p>Entre 3 y 5 horas de sol, o solo de media jornada. Hojas, raíces y muchas aromáticas.</p></div>
    <div class="luz-card">{ICONO_LUZ["sombra"]}<h4>Poca luz</h4><p>Menos de 3 horas. Elige los cultivos marcados con este icono.</p></div>
  </div>
  <div class="leyenda"><span><span class="barra"></span>Meses para sembrar o plantar</span><span>{ESTRELLA} Fácil para empezar</span><span><b>Cosecha:</b> días orientativos desde la siembra</span></div>
  {pie(2)}
</section>

<section class="pagina">
  <div class="antetitulo">Ajusta las fechas a tu zona</div>
  <h2>El clima del interior</h2>
  <p class="entradilla">En el interior peninsular hiela unos 35 días al año, casi todos de diciembre a febrero. Por eso aquí las siembras de primavera se retrasan y las de otoño conviene adelantarlas.</p>
  <div class="clima-top">
    <div class="caja"><h4>Días de helada y temperatura mínima</h4>
      <p class="aclara">Media de cada mes en Toledo (AEMET)</p>{grafica_heladas()}
      <div class="leyenda-graf"><span><i style="background:#24401f"></i>Días de helada</span><span><i style="background:#d9a441;height:1.2mm"></i>Mínima media (0-20 °C)</span></div></div>
    <div class="dato-grande" style="background-image:url({FOTO_CLIMA})"><span class="antetitulo" style="color:#fff">La regla de oro</span>
      <div><b>+15-30</b><p>días de retraso en las siembras de primavera respecto a lo que verás en calendarios generales.</p></div></div>
  </div>
  <div class="consejos">
    <div class="consejo"><div class="etq">Primavera</div><h4>Espera a que pase el frío</h4><p>Aún hiela algún día en marzo y, de forma rara, en abril. Lo de calor (tomate, pimiento, berenjena, calabacín, albahaca) se empieza en semillero dentro de casa y sale al balcón cuando las noches ya no bajan de unos grados.</p></div>
    <div class="consejo"><div class="etq">La regla</div><h4>Retrasa de 15 días a un mes</h4><p>Es el ajuste que recomiendan los huertos escolares del Ayuntamiento de Madrid para las zonas más frías. Si la tabla dice marzo, piensa en finales de marzo o en abril.</p></div>
    <div class="consejo"><div class="etq">Otoño</div><h4>Siembra pronto</h4><p>De septiembre a noviembre la mínima media baja de 14,9 °C a 5,3 °C. Lo de hoja, mejor en septiembre y octubre; en noviembre ya hay unos 3 días de helada, aunque ajos y habas aún se plantan.</p></div>
    <div class="consejo"><div class="etq">Invierno</div><h4>Protege, no siembres fuera</h4><p>Ajos, habas y hojas aguantan. Lo delicado, con velo antiheladas, junto a la pared y con la maceta separada del suelo. Riega poco: el sustrato tarda en secarse.</p></div>
  </div>
  <div class="foto-banda" style="background-image:url({FOTO_INVERNADERO}); height:44mm; margin-top:8mm"></div>
  <p class="fuente" style="margin-top:3mm">En un balcón de ciudad suele helar algo menos que en la estación meteorológica: fíjate también en lo que ves en tu zona.</p>
  {pie(3)}
</section>

<section class="pagina">
  <div class="antetitulo">Calendario anual · 1 de 2</div>
  <h2>Hortalizas, hojas y raíces</h2>
  {tabla(GRUPOS[:3])}
  <p class="nota-tabla">Las columnas sombreadas son los meses con más heladas (diciembre a febrero): en esos meses, siembra en semillero dentro de casa o protege con velo.</p>
  {pie(4)}
</section>

<section class="pagina">
  <div class="antetitulo">Calendario anual · 2 de 2</div>
  <h2>Aromáticas y frutales</h2>
  {tabla(GRUPOS[3:])}
  <div class="foto-banda" style="background-image:url({FOTO_SEMILLERO})"></div>
  <p class="nota-tabla">Los frutales y las aromáticas perennes no tienen días de cosecha: tardan meses o años y luego producen temporada tras temporada.</p>
  {pie(5)}
</section>

<section class="pagina">
  <div class="antetitulo">Mes a mes · enero a junio</div>
  <h2>Qué sembrar cada mes</h2>
  <div class="meses">{tarjetas_mes(0, 6)}</div>
  {pie(6)}
</section>

<section class="pagina">
  <div class="antetitulo">Mes a mes · julio a diciembre</div>
  <h2>Qué sembrar cada mes</h2>
  <div class="meses amplio">{tarjetas_mes(6, 12)}</div>
  {pie(7)}
</section>

<section class="pagina">
  <div class="antetitulo">Para estrenarte</div>
  <h2>Los 10 más fáciles</h2>
  <p class="entradilla">Rápidos, resistentes y poco exigentes. Ordenados de menos a más días hasta la cosecha.</p>
  <div class="fichas">{"".join(ficha(c) for c in faciles)}</div>
  {pie(8)}
</section>

<section class="pagina">
  <div class="antetitulo">Para imprimir y rellenar</div>
  <h2>Mi diario de siembra</h2>
  <p class="entradilla">Apunta lo que siembras: el año que viene sabrás qué funcionó en tu balcón y cuándo.</p>
  <table class="diario"><thead><tr><th style="width:24mm">Fecha</th><th>Cultivo</th><th style="width:30mm">Maceta / lugar</th><th style="width:26mm">Germinó</th><th style="width:26mm">Cosecha</th><th style="width:38mm">Notas</th></tr></thead>
  <tbody>{"<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>" * 21}</tbody></table>
  {pie(9)}
</section>

<section class="pagina final">
  <img class="logo-final" src="{LOGO}" alt="MiHuertoUrbano">
  <div class="antetitulo" style="color:var(--mostaza)">Sigue aprendiendo</div>
  <h2>Más ayuda en la web</h2>
  <p class="entradilla">Escanea con la cámara del móvil o pulsa en los enlaces.</p>
  <div class="qrs">
    <div class="qr-card">{QR_WEB}<div><h4>¿Qué planto en mi balcón?</h4><p>La calculadora te dice qué sembrar según la luz de tu balcón y el mes.</p><a href="https://mihuertourbano.xyz/que-plantar-en-tu-balcon/">mihuertourbano.xyz/que-plantar-en-tu-balcon</a></div></div>
    <div class="qr-card">{QR_MES}<div><h4>La guía de cada mes</h4><p>Siembras, cuidados y cosechas, mes a mes, con todo el detalle.</p><a href="https://mihuertourbano.xyz/articulos/calendario-siembra-completo-mes-a-mes/">mihuertourbano.xyz/…/calendario-siembra-completo-mes-a-mes</a></div></div>
  </div>
  <div class="lista">
    <div><b>Una ficha por cultivo</b>Cómo sembrar, regar y cosechar cada uno en maceta.</div>
    <div><b>¿Qué le pasa a mi planta?</b>Hojas amarillas, plagas, hongos… y cómo arreglarlo.</div>
    <div><b>Riego automático</b>Para que el balcón no dependa de ti en verano.</div>
    <div><b>Instagram y Facebook</b>@mihuertourbano.xyz · consejos de temporada cada semana.</div>
  </div>
  <div class="fuentes">Fuentes: AEMET, valores climatológicos normales de Toledo, estación 3260B (serie 1981-2010). Ayuntamiento de Madrid, Huertos escolares sostenibles, «Calendario de cultivo» (2018). Fechas orientativas: ajústalas siempre a tu zona y a tu balcón.</div>
  {pie(10, claro=True)}
</section>
</body></html>'''

tmp = RAIZ / "descargables" / "calendario" / "_calendario.html"
tmp.write_text(html, encoding="utf-8")

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(tmp.as_uri(), wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    pg.pdf(path=str(SALIDA), format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
tmp.unlink()
import subprocess
if shutil.which("qpdf"):  # PDF "linealizado": el móvil lo enseña mientras se descarga
    lin = SALIDA.with_suffix(".lin.pdf")
    subprocess.run(["qpdf", "--linearize", str(SALIDA), str(lin)], check=True)
    lin.replace(SALIDA)
PUBLICO.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(SALIDA, PUBLICO)
print(SALIDA, f"{SALIDA.stat().st_size / 1e6:.1f} MB", N, "cultivos")
