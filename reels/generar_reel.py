#!/usr/bin/env python3
"""
Generador de reels de MiHuertoUrbano
====================================

Convierte un artículo del blog en un reel vertical (1080x1920, 9:16) para
Instagram y Facebook, con el estilo de marca del sitio:

  - Foto propia del artículo con zoom lento (efecto Ken Burns)
  - Fondo desenfocado de la misma foto
  - Nombre de marca arriba y el logo (regadera + ciudad) sobre la foto
  - Banda inferior verde con: kicker dorado + titular en Fraunces
    (con una palabra subrayada en dorado) + subtítulo
  - Diapositiva final de llamada a la acción (píldora dorada)

El contenido de cada reel se define en un archivo JSON dentro de reels/config/.
No hay que tocar este script para crear un reel nuevo: solo copiar un JSON.

Uso:
    python3 reels/generar_reel.py reels/config/aguacate-riego.json

Salida:
    reels/salida/<slug>.mp4

Requisitos (ya presentes en el entorno de Claude Code en la web):
    - Chromium (para renderizar el texto con las fuentes reales de la web)
    - ffmpeg (se usa el que trae el paquete de Python imageio-ffmpeg si no
      hay uno en el sistema:  pip install imageio-ffmpeg)
    - Las dependencias de la web instaladas (cd web && npm install), porque
      las fuentes salen de web/node_modules/@fontsource-variable/

Todo el diseño (colores, fuentes, medidas) sale de la propia web, así que
los reels siempre quedan coherentes con la marca.
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

# --------------------------------------------------------------------------
# Rutas del proyecto
# --------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
WEB_PUBLIC = REPO / "web" / "public"
FONTS_DIR = REPO / "web" / "node_modules" / "@fontsource-variable"
SALIDA = REPO / "reels" / "salida"

# --------------------------------------------------------------------------
# Colores de marca (copiados de web/src/styles: variables --color-*)
# --------------------------------------------------------------------------
C = {
    "hoja": "#3f6b3a",
    "hoja_oscuro": "#24401f",
    "tierra": "#a8562f",
    "mostaza": "#d9a441",
    "mostaza_claro": "#e8bf62",
    "crema": "#faf3e6",
}

# --------------------------------------------------------------------------
# Geometría del lienzo 1080x1920 (medida sobre el último reel real)
# --------------------------------------------------------------------------
W, H = 1080, 1920
WIN_TOP = 475       # borde superior de la "ventana" de la foto
WIN_H = 630         # alto de la ventana de la foto
WIN_BOTTOM = WIN_TOP + WIN_H


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def find_chrome() -> str:
    """Localiza el ejecutable de Chromium."""
    env = os.environ.get("CHROME_BIN")
    if env and Path(env).exists():
        return env
    candidates = [
        "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    ]
    # Cualquier chromium-* dentro de PLAYWRIGHT_BROWSERS_PATH
    pw = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    if pw.exists():
        candidates += [str(p) for p in pw.glob("chromium-*/chrome-linux/chrome")]
        candidates += [
            str(p) for p in pw.glob("chromium_headless_shell-*/chrome-linux/headless_shell")
        ]
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        found = shutil.which(name)
        if found:
            candidates.append(found)
    for c in candidates:
        if c and Path(c).exists():
            return c
    sys.exit("ERROR: no se encontró Chromium. Define CHROME_BIN=/ruta/a/chrome")


def find_ffmpeg() -> str:
    """Localiza ffmpeg (sistema o el de imageio-ffmpeg)."""
    sys_ff = shutil.which("ffmpeg")
    if sys_ff:
        return sys_ff
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit(
            "ERROR: no se encontró ffmpeg. Instálalo o ejecuta:\n"
            "  pip install imageio-ffmpeg"
        )


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def font_face(family: str, file: Path) -> str:
    uri = data_uri(file, "font/woff2")
    return (
        f"@font-face{{font-family:'{family}';"
        f"src:url('{uri}') format('woff2');"
        "font-weight:100 900;font-style:normal;font-display:block;}"
    )


def resolve_foto(valor: str) -> Path:
    """Acepta ruta absoluta, relativa al repo, o del estilo /images/... (web/public)."""
    p = Path(valor)
    if p.is_absolute() and p.exists():
        return p
    # /images/... -> web/public/images/...
    cand = WEB_PUBLIC / valor.lstrip("/")
    if cand.exists():
        return cand
    cand2 = (REPO / valor).resolve()
    if cand2.exists():
        return cand2
    sys.exit(f"ERROR: no encuentro la foto '{valor}'")


def subrayar(titulo: str, destacado: str) -> str:
    """Envuelve la palabra 'destacado' del titular en un <span> subrayado."""
    if not destacado:
        return escape(titulo)
    idx = titulo.lower().find(destacado.lower())
    if idx < 0:
        return escape(titulo)
    antes = escape(titulo[:idx])
    palabra = escape(titulo[idx : idx + len(destacado)])
    despues = escape(titulo[idx + len(destacado) :])
    return f"{antes}<span class='hl'>{palabra}</span>{despues}"


def escape(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


# --------------------------------------------------------------------------
# Plantillas HTML (dos capas por diapositiva)
# --------------------------------------------------------------------------
def css_comun(foto_uri: str) -> str:
    fraunces = font_face("Fraunces", FONTS_DIR / "fraunces/files/fraunces-latin-wght-normal.woff2")
    inter = font_face("Inter", FONTS_DIR / "inter/files/inter-latin-wght-normal.woff2")
    return f"""
{fraunces}
{inter}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
.canvas{{position:relative;width:{W}px;height:{H}px}}
"""


def html_fondo(foto_uri: str) -> str:
    """Capa de fondo (opaca): desenfoque + ventana nítida de la foto. Hace zoom."""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{css_comun(foto_uri)}
.blur{{position:absolute;inset:0;background:url('{foto_uri}') center/cover no-repeat;
      filter:blur(34px) brightness(.78) saturate(1.05);transform:scale(1.15)}}
.tinte{{position:absolute;inset:0;background:
      linear-gradient(180deg, rgba(20,30,16,.55) 0%, rgba(20,30,16,.15) 22%,
      rgba(20,30,16,.15) 55%, rgba(15,22,12,.75) 100%)}}
.ventana{{position:absolute;left:0;right:0;top:{WIN_TOP}px;height:{WIN_H}px;
      background:url('{foto_uri}') center/cover no-repeat;
      box-shadow:0 18px 40px rgba(0,0,0,.45)}}
</style></head><body>
<div class="canvas">
  <div class="blur"></div>
  <div class="tinte"></div>
  <div class="ventana"></div>
</div></body></html>"""


def html_texto(slide: dict, marca: str, logo_uri: str) -> str:
    """Capa de texto (transparente y estática): marca, logo, banda y textos."""
    band_top = WIN_BOTTOM - 25
    logo_top = WIN_BOTTOM - 165
    if slide.get("cta"):
        bloque = f"""
      <div class="cta-pill">{escape(slide['pildora'])}</div>
      <p class="sub cta-sub">{escape(slide.get('subtitulo',''))}</p>"""
    else:
        titulo_html = subrayar(slide["titulo"], slide.get("destacado", ""))
        bloque = f"""
      <p class="kicker">{escape(slide.get('kicker',''))}</p>
      <h1 class="titular">{titulo_html}</h1>
      <p class="sub">{escape(slide.get('subtitulo',''))}</p>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{css_comun('')}
.marca{{position:absolute;top:150px;left:0;right:0;text-align:center;
      font-family:'Fraunces',serif;font-weight:800;font-size:52px;color:{C['crema']};
      letter-spacing:.5px;text-shadow:0 2px 10px rgba(0,0,0,.55)}}
.logo{{position:absolute;right:36px;top:{logo_top}px;width:150px;height:auto;
      filter:drop-shadow(0 4px 10px rgba(0,0,0,.45))}}
.banda{{position:absolute;left:0;right:0;top:{band_top}px;bottom:0;
      background:linear-gradient(180deg,
        rgba(63,107,58,0) 0%,
        rgba(36,64,31,.92) 14%,
        rgba(20,32,16,.97) 46%,
        rgba(12,18,10,.98) 100%)}}
.textos{{position:absolute;left:60px;right:60px;top:{band_top+120}px;text-align:center}}
.kicker{{font-family:'Inter',sans-serif;font-weight:800;font-size:36px;
      letter-spacing:5px;text-transform:uppercase;color:{C['mostaza_claro']};
      margin-bottom:26px}}
.titular{{font-family:'Fraunces',serif;font-weight:900;font-size:86px;
      line-height:1.04;color:#fdfaf2;text-shadow:0 3px 14px rgba(0,0,0,.5)}}
.titular .hl{{position:relative;white-space:nowrap}}
.titular .hl::after{{content:'';position:absolute;left:4%;right:4%;bottom:-.10em;
      height:11px;border-radius:6px;background:{C['mostaza']}}}
.sub{{font-family:'Inter',sans-serif;font-weight:700;font-size:48px;color:#f3ede0;
      margin-top:40px;text-shadow:0 2px 10px rgba(0,0,0,.5)}}
.cta-pill{{display:inline-block;font-family:'Inter',sans-serif;font-weight:800;
      font-size:44px;letter-spacing:1px;text-transform:uppercase;
      color:{C['hoja_oscuro']};background:{C['mostaza']};
      padding:26px 54px;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,.4)}}
.cta-sub{{margin-top:44px}}
</style></head><body>
<div class="canvas">
  <div class="banda"></div>
  <div class="marca">{escape(marca)}</div>
  <img class="logo" src="{logo_uri}">
  <div class="textos">{bloque}</div>
</div></body></html>"""


# --------------------------------------------------------------------------
# Render de una capa a PNG con Chromium headless
# --------------------------------------------------------------------------
def render_png(chrome: str, html: str, out_png: Path, tmp: Path, transparente: bool):
    html_file = tmp / (out_png.stem + ".html")
    html_file.write_text(html, encoding="utf-8")
    cmd = [
        chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        f"--window-size={W},{H}", "--virtual-time-budget=4000",
        f"--screenshot={out_png}",
    ]
    if transparente:
        cmd.append("--default-background-color=00000000")
    cmd.append(f"file://{html_file}")
    subprocess.run(cmd, check=True, capture_output=True)
    if not out_png.exists():
        sys.exit(f"ERROR: Chromium no generó {out_png}")


# --------------------------------------------------------------------------
# Montaje de vídeo con ffmpeg
# --------------------------------------------------------------------------
def clip_slide(ffmpeg: str, bg: Path, fg: Path, out: Path, dur: float, fps: int,
               zoom: float, direccion: str):
    """Un clip por diapositiva: Ken Burns (alternando dirección) + texto que
    entra animado (deslizándose hacia arriba + fundido)."""
    frames = int(round(dur * fps))
    denom = max(frames - 1, 1)
    # Zoom basado en 'on' (nº de frame) para que sea suave; alterna acercar/alejar.
    if direccion == "out":
        zexpr = f"{zoom}-{(zoom-1):.6f}*on/{denom}"
    else:
        zexpr = f"1+{(zoom-1):.6f}*on/{denom}"
    anim = 0.55  # duración de la entrada del texto (segundos)
    desl = 80    # píxeles que se desliza el texto al entrar
    # Preescalado x2 para que el zoompan no dé saltos de píxel.
    fc = (
        f"[0:v]scale={W*2}:{H*2},"
        f"zoompan=z='{zexpr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={W}x{H}:fps={fps}[bg];"
        f"[1:v]format=rgba,fade=t=in:st=0:d={anim}:alpha=1[fg];"
        f"[bg][fg]overlay=x=0:y='{desl}*(lt(t\\,{anim}))*(1-t/{anim})':"
        f"format=auto,format=yuv420p[v]"
    )
    cmd = [
        ffmpeg, "-y",
        "-loop", "1", "-framerate", str(fps), "-t", f"{dur}", "-i", str(bg),
        "-loop", "1", "-framerate", str(fps), "-t", f"{dur}", "-i", str(fg),
        "-filter_complex", fc, "-map", "[v]",
        "-t", f"{dur}", "-r", str(fps),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", str(out),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def combinar(ffmpeg: str, clips: list, out: Path, dur: float, fps: int,
             transicion: str, tdur: float):
    """Une los clips con transiciones xfade (deslizado/fundido) en vez de cortes."""
    if len(clips) == 1:
        shutil.copy(clips[0], out)
        return
    inputs = []
    for c in clips:
        inputs += ["-i", str(c)]
    filt = ""
    prev = "[0:v]"
    off = dur - tdur
    for i in range(1, len(clips)):
        etq = "[v]" if i == len(clips) - 1 else f"[x{i}]"
        filt += (
            f"{prev}[{i}:v]xfade=transition={transicion}:duration={tdur}:"
            f"offset={off:.3f}{etq};"
        )
        prev = etq
        off += dur - tdur
    filt = filt.rstrip(";")
    cmd = [
        ffmpeg, "-y", *inputs, "-filter_complex", filt, "-map", "[v]",
        "-r", str(fps), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


# --------------------------------------------------------------------------
# Principal
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Genera un reel de MiHuertoUrbano desde un JSON.")
    ap.add_argument("config", help="Ruta al JSON de configuración del reel")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--zoom", type=float, default=1.14, help="Zoom del efecto Ken Burns (1.14 = +14%)")
    ap.add_argument("--transicion", default="slideup",
                    help="Transición entre diapositivas (slideup, slideleft, smoothup, fade, wipeup...)")
    ap.add_argument("--trans-dur", type=float, default=0.5, help="Duración de la transición (s)")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    slug = cfg.get("slug") or Path(args.config).stem
    marca = cfg.get("marca", "MiHuertoUrbano")
    dur = float(cfg.get("duracion_slide", 3.4))
    slides = cfg["slides"]

    chrome = find_chrome()
    ffmpeg = find_ffmpeg()

    logo_uri = data_uri(WEB_PUBLIC / "images" / "logo-full.png", "image/png")
    foto_defecto = cfg.get("foto")

    # Caché de fotos ya convertidas a data-URI (por si varias diapositivas
    # comparten la misma foto).
    cache_uri: dict = {}

    def uri_de(rel: str) -> str:
        if rel not in cache_uri:
            p = resolve_foto(rel)
            mime = "image/jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "image/png"
            cache_uri[rel] = data_uri(p, mime)
        return cache_uri[rel]

    SALIDA.mkdir(parents=True, exist_ok=True)
    final = SALIDA / f"{slug}.mp4"

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        clips = []
        cache_bg: dict = {}  # ruta-foto -> bg_png ya renderizado

        for i, slide in enumerate(slides):
            # Cada diapositiva usa su propia foto, o la foto por defecto del reel.
            rel = slide.get("foto") or foto_defecto
            if not rel:
                sys.exit("ERROR: falta 'foto' (ni en la diapositiva ni en el reel)")
            if rel not in cache_bg:
                bg_png = tmp / f"bg_{len(cache_bg):02d}.png"
                render_png(chrome, html_fondo(uri_de(rel)), bg_png, tmp, transparente=False)
                cache_bg[rel] = bg_png
            bg_png = cache_bg[rel]

            fg_png = tmp / f"fg_{i:02d}.png"
            render_png(chrome, html_texto(slide, marca, logo_uri), fg_png, tmp, transparente=True)
            clip = tmp / f"slide_{i:02d}.mp4"
            direccion = "in" if i % 2 == 0 else "out"
            clip_slide(ffmpeg, bg_png, fg_png, clip, dur, args.fps, args.zoom, direccion)
            clips.append(clip)
            print(f"  ✓ diapositiva {i+1}/{len(slides)}")

        combinar(ffmpeg, clips, final, dur, args.fps, args.transicion, args.trans_dur)

    dur_total = dur * len(slides) - args.trans_dur * (len(slides) - 1)
    print(f"\n✅ Reel generado: {final}")
    print(f"   {W}x{H} · {dur_total:.1f}s · {len(slides)} diapositivas · {args.fps} fps")


if __name__ == "__main__":
    main()
