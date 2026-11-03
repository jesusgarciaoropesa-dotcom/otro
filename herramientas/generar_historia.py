#!/usr/bin/env python3
"""
Historia de Instagram (1080x1920) a partir de la portada de un carrusel.

Fondo: la portada ampliada y desenfocada. Encima: la portada entera, una
etiqueta "NUEVO POST" y una línea de texto. Usa las fuentes de la web
(web/node_modules/@fontsource-variable) y Chromium, igual que el generador de reels.

Uso:
    python3 herramientas/generar_historia.py PORTADA.jpg SALIDA.jpg \
        --fuentes RUTA/web/node_modules/@fontsource-variable \
        [--etiqueta "NUEVO POST"] [--texto "Míralo en el perfil"]
Requiere: CHROME_BIN con la ruta de Chromium y el paquete playwright de Python o Node.
"""
import argparse, base64, os, subprocess, sys, tempfile
from pathlib import Path

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Fraunces; src: url('{fraunces}') format('woff2'); font-weight: 100 900; }}
@font-face {{ font-family: Inter; src: url('{inter}') format('woff2'); font-weight: 100 900; }}
html,body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#24401f; }}
.bg {{ position:absolute; inset:-60px; background:url('{img}') center/cover; filter: blur(40px) brightness(.55); }}
.wrap {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:44px; }}
.tag {{ font: 700 38px Inter; letter-spacing:.18em; color:#24401f; background:#d9b44a; padding:18px 40px; border-radius:999px; }}
.card {{ width:900px; border-radius:28px; overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,.45); }}
.card img {{ display:block; width:100%; }}
.txt {{ font: 600 50px Fraunces; color:#fff; text-align:center; max-width:880px; line-height:1.15; }}
.marca {{ position:absolute; top:96px; width:100%; text-align:center; font: 700 40px Fraunces; color:#fff; }}
</style></head><body><div class="bg"></div>
<div class="wrap"><div class="tag">{etiqueta}</div><div class="card"><img src="{img}"></div><div class="txt">{texto}</div></div>
</body></html>"""

def data_uri(p: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("portada"); ap.add_argument("salida")
    ap.add_argument("--fuentes", required=True)
    ap.add_argument("--etiqueta", default="NUEVO POST")
    ap.add_argument("--texto", default="Míralo en el perfil")
    a = ap.parse_args()
    f = Path(a.fuentes)
    html = HTML.format(
        fraunces=data_uri(f / "fraunces/files/fraunces-latin-wght-normal.woff2", "font/woff2"),
        inter=data_uri(f / "inter/files/inter-latin-wght-normal.woff2", "font/woff2"),
        img=data_uri(Path(a.portada), "image/jpeg"),
        etiqueta=a.etiqueta, texto=a.texto)
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "h.html"; h.write_text(html, encoding="utf-8")
        png = Path(td) / "h.png"
        js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch({{executablePath:process.env.CHROME_BIN||undefined}});
const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});await p.goto('file://{h}');await p.waitForTimeout(400);
await p.screenshot({{path:'{png}'}});await b.close();}})();"""
        subprocess.run(["node", "-e", js], check=True)
        from PIL import Image
        Image.open(png).convert("RGB").save(a.salida, "JPEG", quality=88)
    print("✅ Historia:", a.salida)

if __name__ == "__main__":
    main()
