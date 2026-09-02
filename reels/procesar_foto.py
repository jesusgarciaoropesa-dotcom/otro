#!/usr/bin/env python3
"""
Procesa una foto para el interior de un artículo de MiHuertoUrbano:

  1. Recorta al formato 1200x670 (centrado, sin deformar).
  2. Superpone el logo (regadera + ciudad) abajo a la derecha.
  3. Guarda el resultado como JPG optimizado en web/public/images/articulos/.

Uso:
    python3 reels/procesar_foto.py <foto_origen> <nombre-destino-sin-extension>

Ejemplo:
    python3 reels/procesar_foto.py /ruta/foto.jpg acolchado-mulching-tomatera
    # -> web/public/images/articulos/acolchado-mulching-tomatera.jpg
"""
import sys
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
DEST_DIR = REPO / "web" / "public" / "images" / "articulos"
LOGO = REPO / "web" / "public" / "images" / "logo-full.png"

W, H = 1200, 670
LOGO_W = 175          # ancho del logo en la imagen final
MARGIN = 18           # margen del logo respecto a los bordes


def recortar(im: Image.Image) -> Image.Image:
    """Recorta al centro para cubrir 1200x670 sin deformar."""
    im = im.convert("RGB")
    src_w, src_h = im.size
    escala = max(W / src_w, H / src_h)
    nueva = (round(src_w * escala), round(src_h * escala))
    im = im.resize(nueva, Image.LANCZOS)
    x = (nueva[0] - W) // 2
    y = (nueva[1] - H) // 2
    return im.crop((x, y, x + W, y + H))


def poner_logo(im: Image.Image) -> Image.Image:
    logo = Image.open(LOGO).convert("RGBA")
    ratio = LOGO_W / logo.width
    logo = logo.resize((LOGO_W, round(logo.height * ratio)), Image.LANCZOS)
    pos = (W - logo.width - MARGIN, H - logo.height - MARGIN)
    im = im.convert("RGBA")
    im.alpha_composite(logo, pos)
    return im.convert("RGB")


def main():
    if len(sys.argv) != 3:
        sys.exit("Uso: python3 reels/procesar_foto.py <foto_origen> <nombre-destino>")
    origen = Path(sys.argv[1])
    nombre = sys.argv[2].removesuffix(".jpg")
    if not origen.exists():
        sys.exit(f"No existe la foto: {origen}")
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    dest = DEST_DIR / f"{nombre}.jpg"
    im = recortar(Image.open(origen))
    im = poner_logo(im)
    im.save(dest, "JPEG", quality=88, optimize=True)
    print(f"OK -> {dest.relative_to(REPO)}  ({im.size[0]}x{im.size[1]})")


if __name__ == "__main__":
    main()
