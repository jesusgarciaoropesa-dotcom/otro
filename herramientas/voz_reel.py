#!/usr/bin/env python3
"""
Voz en off para los reels de MiHuertoUrbano (gratis y sin internet, con Piper).

Lee el titular y el subtítulo de cada lámina del JSON del reel y los coloca en el
vídeo justo cuando aparece esa lámina. Usa la voz guardada en voces/ de la rama "redes".

Uso:
    # 1) Medir: dice qué duración por lámina hace falta para que quepa la voz
    python3 herramientas/voz_reel.py medir CONFIG_REEL.json
    # 2) Mezclar la voz con un reel ya generado con esa duración
    python3 herramientas/voz_reel.py mezclar CONFIG_REEL.json REEL.mp4 SALIDA.mp4

Opciones: --modelo voces/es_ES-davefx-medium.onnx  --trans-dur 0.5 (igual que el generador)
Requiere: pip install piper-tts imageio-ffmpeg
"""
import argparse, json, re, subprocess, sys, tempfile, wave
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
MODELO = AQUI / "voces" / "es_ES-davefx-medium.onnx"
MARGEN_ANTES = 0.45   # la voz entra cuando el texto ya está en pantalla
MARGEN_DESPUES = 0.7  # respiro antes de la siguiente lámina
MIN_DUR = 5.5

EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍👉🌱]")

def texto_lamina(s: dict) -> str:
    partes = [s.get("titulo", ""), s.get("subtitulo", "")]
    t = ". ".join(p.strip().rstrip(".") for p in partes if p and p.strip())
    t = EMOJI.sub("", t).replace("·", ",").replace("MiHuertoUrbano.xyz", "Mi Huerto Urbano punto xyz")
    return re.sub(r"\s+", " ", t).strip() + "."

def sintetizar(modelo: Path, texto: str, salida: Path, velocidad: float = 1.0) -> float:
    from piper import PiperVoice
    from piper.config import SynthesisConfig
    voz = PiperVoice.load(str(modelo))
    with wave.open(str(salida), "wb") as w:
        voz.synthesize_wav(texto, w, syn_config=SynthesisConfig(length_scale=velocidad))
    with wave.open(str(salida)) as w:
        return w.getnframes() / w.getframerate()

def ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accion", choices=["medir", "mezclar"])
    ap.add_argument("config"); ap.add_argument("reel", nargs="?"); ap.add_argument("salida", nargs="?")
    ap.add_argument("--modelo", default=str(MODELO))
    ap.add_argument("--trans-dur", type=float, default=0.5)
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    slides = cfg.get("slides") or cfg.get("diapositivas")
    dur = float(cfg.get("duracion_slide", 3.4))
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        wavs, largos = [], []
        for i, s in enumerate(slides):
            w = td / f"v{i}.wav"
            largos.append(sintetizar(Path(a.modelo), texto_lamina(s), w))
            wavs.append(w)
        necesaria = round(max(MIN_DUR, max(largos) + MARGEN_ANTES + MARGEN_DESPUES + a.trans_dur), 1)
        if a.accion == "medir":
            print(json.dumps({"duracion_slide": necesaria, "voz_por_lamina": [round(x, 2) for x in largos]}))
            return
        if dur + 1e-6 < necesaria:
            sys.exit(f"ERROR: el reel usa {dur}s por lámina y la voz necesita {necesaria}s. "
                     f"Pon \"duracion_slide\": {necesaria} en {a.config}, regenera el reel y vuelve a mezclar.")
        paso = dur - a.trans_dur
        entradas, filtros = [], []
        for i, w in enumerate(wavs):
            entradas += ["-i", str(w)]
            ms = int((i * paso + MARGEN_ANTES) * 1000)
            filtros.append(f"[{i+1}:a]adelay={ms}|{ms}[a{i}]")
        mezcla = "".join(f"[a{i}]" for i in range(len(wavs)))
        filtros.append(f"{mezcla}amix=inputs={len(wavs)}:normalize=0,loudnorm=I=-16:TP=-1.5,apad[voz]")
        cmd = [ffmpeg(), "-y", "-loglevel", "error", "-i", a.reel, *entradas,
               "-filter_complex", ";".join(filtros), "-map", "0:v", "-map", "[voz]",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-shortest", a.salida]
        subprocess.run(cmd, check=True)
    print("✅ Reel con voz:", a.salida)

if __name__ == "__main__":
    main()
