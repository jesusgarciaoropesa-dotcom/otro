#!/usr/bin/env python3
"""
Generador de pines de Pinterest para MiHuertoUrbano
===================================================

Convierte artículos del blog en pines verticales 1000x1500 (formato ideal de
Pinterest) con el estilo de marca del sitio, y genera además el texto listo
para pegar en Pinterest (título + descripción con palabras clave + enlace).

Pinterest es, para un blog de jardinería, la vía más rápida a tráfico web:
funciona como buscador visual, indexa en días (no meses como Google) y cada
pin enlaza directo al artículo.

Uso:
    python3 pinterest/generar_pin.py pinterest/config/tanda-1.json

El JSON lista los pines. Cada pin indica el `slug` del artículo (de ahí se
sacan la foto, las palabras clave y la URL automáticamente) y un `gancho`
(titular llamativo para el pin). Ejemplo de entrada:

    {
      "pines": [
        {
          "slug": "hojas-aguacate-marrones-secas-que-hacer",
          "kicker": "AGUACATE EN MACETA",
          "gancho": "Hojas del aguacate marrones",
          "destacado": "marrones",
          "subtitulo": "por qué pasa y cómo salvarlo"
        }
      ]
    }

Salida por cada pin:
    pinterest/salida/<slug>.png      (la imagen del pin)
    pinterest/salida/<slug>.txt      (título + descripción para pegar)

Requisitos: Chromium (para las fuentes reales) y las dependencias de la web
instaladas (cd web && npm install), de donde salen las tipografías.
"""
import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WEB_PUBLIC = REPO / "web" / "public"
ARTICULOS = REPO / "web" / "src" / "content" / "articulos"
FONTS_DIR = REPO / "web" / "node_modules" / "@fontsource-variable"
SALIDA = REPO / "pinterest" / "salida"
SITE = "https://mihuertourbano.xyz"

C = {
    "hoja": "#3f6b3a",
    "hoja_oscuro": "#24401f",
    "tierra": "#a8562f",
    "mostaza": "#d9a441",
    "mostaza_claro": "#e8bf62",
    "crema": "#faf3e6",
}
W, H = 1000, 1500


def find_chrome() -> str:
    env = os.environ.get("CHROME_BIN")
    if env and Path(env).exists():
        return env
    pw = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    cand = list(pw.glob("chromium-*/chrome-linux/chrome")) if pw.exists() else []
    cand += list(pw.glob("chromium_headless_shell-*/chrome-linux/headless_shell")) if pw.exists() else []
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        f = shutil.which(name)
        if f:
            cand.append(Path(f))
    for c in cand:
        if Path(c).exists():
            return str(c)
    sys.exit("ERROR: no se encontró Chromium. Define CHROME_BIN=/ruta/a/chrome")


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def font_face(family: str, file: Path) -> str:
    uri = data_uri(file, "font/woff2")
    return (
        f"@font-face{{font-family:'{family}';src:url('{uri}') format('woff2');"
        "font-weight:100 900;font-style:normal;font-display:block;}"
    )


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def subrayar(titulo: str, destacado: str) -> str:
    if not destacado:
        return escape(titulo)
    i = titulo.lower().find(destacado.lower())
    if i < 0:
        return escape(titulo)
    return (
        escape(titulo[:i])
        + f"<span class='hl'>{escape(titulo[i:i+len(destacado)])}</span>"
        + escape(titulo[i + len(destacado):])
    )


def leer_articulo(slug: str) -> dict:
    """Extrae título, keywords y primera imagen del .md del artículo."""
    f = ARTICULOS / f"{slug}.md"
    if not f.exists():
        sys.exit(f"ERROR: no existe el artículo {slug}.md")
    txt = f.read_text(encoding="utf-8")
    title = re.search(r'^title:\s*"?(.*?)"?\s*$', txt, re.M)
    kw = re.search(r'^keywords:\s*\[(.*?)\]', txt, re.M)
    img = re.search(r'<img[^>]*src="([^"]+)"', txt)
    keywords = []
    if kw:
        keywords = [k.strip().strip('"').strip("'") for k in kw.group(1).split(",")]
    return {
        "title": title.group(1) if title else slug,
        "keywords": keywords,
        "img": img.group(1) if img else None,
        "url": f"{SITE}/articulos/{slug}/",
    }


def html_pin(foto_uri: str, logo_uri: str, pin: dict) -> str:
    fraunces = font_face("Fraunces", FONTS_DIR / "fraunces/files/fraunces-latin-wght-normal.woff2")
    inter = font_face("Inter", FONTS_DIR / "inter/files/inter-latin-wght-normal.woff2")
    titulo_html = subrayar(pin["gancho"], pin.get("destacado", ""))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fraunces}
{inter}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
.pin{{position:relative;width:{W}px;height:{H}px;background:{C['crema']};
     font-family:'Inter',sans-serif}}
.marca{{position:absolute;top:44px;left:0;right:0;text-align:center;z-index:3;
     font-family:'Fraunces',serif;font-weight:800;font-size:40px;color:{C['hoja_oscuro']};
     letter-spacing:.5px}}
.marca span{{color:{C['tierra']}}}
.foto{{position:absolute;top:120px;left:0;width:{W}px;height:760px;
     background:url('{foto_uri}') center/cover no-repeat}}
.logo{{position:absolute;top:{120+760-140}px;right:26px;width:150px;z-index:3;
     filter:drop-shadow(0 4px 10px rgba(0,0,0,.4))}}
.panel{{position:absolute;left:0;right:0;top:860px;bottom:0;
     background:{C['crema']};padding:54px 60px 0;text-align:center}}
.kicker{{font-weight:800;font-size:30px;letter-spacing:4px;text-transform:uppercase;
     color:{C['tierra']};margin-bottom:22px}}
.titular{{font-family:'Fraunces',serif;font-weight:900;font-size:74px;line-height:1.05;
     color:{C['hoja_oscuro']}}}
.titular .hl{{position:relative;white-space:nowrap}}
.titular .hl::after{{content:'';position:absolute;left:2%;right:2%;bottom:-.08em;
     height:12px;border-radius:6px;background:{C['mostaza']}}}
.sub{{font-weight:600;font-size:38px;color:#5c5344;margin-top:26px;line-height:1.25}}
.cta{{position:absolute;left:0;right:0;bottom:104px;text-align:center}}
.pill{{display:inline-block;font-weight:800;font-size:34px;letter-spacing:.5px;
     color:#fff;background:{C['hoja']};padding:22px 46px;border-radius:999px}}
.dominio{{margin-top:24px;font-weight:700;font-size:30px;color:{C['tierra']};letter-spacing:.5px}}
</style></head><body>
<div class="pin">
  <div class="marca">MiHuerto<span>Urbano</span></div>
  <div class="foto"></div>
  <img class="logo" src="{logo_uri}">
  <div class="panel">
    <div class="kicker">{escape(pin.get('kicker',''))}</div>
    <div class="titular">{titulo_html}</div>
    <div class="sub">{escape(pin.get('subtitulo',''))}</div>
  </div>
  <div class="cta">
    <div class="pill">LEER LA GUÍA &#128073;</div>
    <div class="dominio">mihuertourbano.xyz</div>
  </div>
</div></body></html>"""


def render(chrome: str, html: str, out_png: Path, tmp: Path):
    hf = tmp / (out_png.stem + ".html")
    hf.write_text(html, encoding="utf-8")
    cmd = [
        chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", f"--window-size={W},{H}",
        "--virtual-time-budget=4000", f"--screenshot={out_png}", f"file://{hf}",
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if not out_png.exists():
        sys.exit(f"ERROR: Chromium no generó {out_png}")


def caption(art: dict, pin: dict) -> str:
    """Texto listo para pegar en Pinterest: título + descripción + enlace + hashtags."""
    titulo = f"{pin['gancho']}: {pin.get('subtitulo','')}".strip(": ").strip()
    kws = art["keywords"]
    desc_kw = ", ".join(kws[:3]) if kws else ""
    # Hashtags: un set fijo de marca/nicho + los extra del pin (si se indican).
    base = [
        "#huertourbano", "#huertoencasa", "#huertoenbalcon", "#jardineriaurbana",
        "#cultivarencasa", "#plantasenmaceta", "#balconverde", "#terraza",
    ]
    extra = ["#" + re.sub(r"[^a-z0-9]", "", t.lower()) for t in pin.get("hashtags", [])]
    hashtags = " ".join(extra + base)
    return (
        f"TÍTULO DEL PIN:\n{titulo}\n\n"
        f"DESCRIPCIÓN:\n{art['title']}. Guía práctica paso a paso para tu huerto en "
        f"balcón o terraza ({desc_kw}). Consejos fáciles para principiantes. "
        f"Guarda este pin y lee la guía completa en el enlace.\n\n"
        f"ENLACE (destino del pin):\n{art['url']}\n\n"
        f"HASHTAGS:\n{hashtags}\n"
    )


def main():
    ap = argparse.ArgumentParser(description="Genera pines de Pinterest desde un JSON.")
    ap.add_argument("config", help="Ruta al JSON con la lista de pines")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    pines = cfg["pines"]
    chrome = find_chrome()
    logo_uri = data_uri(WEB_PUBLIC / "images" / "logo-full.png", "image/png")
    SALIDA.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for pin in pines:
            art = leer_articulo(pin["slug"])
            foto_rel = pin.get("foto") or art["img"]
            if not foto_rel:
                sys.exit(f"ERROR: el artículo {pin['slug']} no tiene foto; indica 'foto' en el JSON")
            foto = WEB_PUBLIC / foto_rel.lstrip("/")
            if not foto.exists():
                sys.exit(f"ERROR: no encuentro la foto {foto}")
            mime = "image/jpeg" if foto.suffix.lower() in (".jpg", ".jpeg") else "image/png"
            foto_uri = data_uri(foto, mime)

            out_png = SALIDA / f"{pin['slug']}.png"
            render(chrome, html_pin(foto_uri, logo_uri, pin), out_png, tmp)
            (SALIDA / f"{pin['slug']}.txt").write_text(caption(art, pin), encoding="utf-8")
            print(f"  ✓ {pin['slug']}  ->  {out_png.name} + .txt")

    print(f"\n✅ {len(pines)} pines en {SALIDA.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
