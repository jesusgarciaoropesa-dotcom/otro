#!/usr/bin/env python3
"""
Voz en off para los reels de MiHuertoUrbano. Por defecto, voz natural de Gemini ("Achird", elegida por
Jesús el 12-11-2026; ver voz_gemini.py). Si faltan los audios de Gemini usa Kokoro ("em_alex").
También: --motor kokoro o --motor piper (la antigua).

Lee el titular y el subtítulo de cada lámina del JSON del reel y los coloca en el
vídeo justo cuando aparece esa lámina. Usa la voz guardada en voces/ de la rama "redes".

Uso:
    # 0) Pedir la voz de Gemini: imprime el SQL que hay que ejecutar en Supabase (execute_sql)
    python3 herramientas/voz_reel.py pedido CONFIG_REEL.json
    # 1) Medir: dice qué duración por lámina hace falta para que quepa la voz
    python3 herramientas/voz_reel.py medir CONFIG_REEL.json
    # 2) Mezclar la voz con un reel ya generado con esa duración
    python3 herramientas/voz_reel.py mezclar CONFIG_REEL.json REEL.mp4 SALIDA.mp4

Opciones: --modelo voces/es_ES-davefx-medium.onnx  --trans-dur 0.5 (igual que el generador)
Requiere: imageio-ffmpeg (kokoro-onnx y el modelo se instalan y descargan solos la primera vez)
"""
import argparse, json, re, subprocess, sys, tempfile, wave
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
MODELO = AQUI / "voces" / "es_ES-davefx-medium.onnx"
MARGEN_ANTES = 0.45   # la voz entra cuando el texto ya está en pantalla
MARGEN_DESPUES = 0.5  # respiro antes de la siguiente lámina
MIN_DUR = 5.5

EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍👉🌱]")

PAUSA_TITULO = 0.55   # silencio entre titular y frase
PAUSA_COMA = 0.28     # silencio en comas
PAUSA_PUNTO = 0.40    # silencio en dos puntos, punto y coma y puntos intermedios
VELOCIDAD = 1.08      # >1 = más despacio
ENTONACION = 0.55     # menos variación = voz más estable

def limpiar(t: str) -> str:
    t = EMOJI.sub("", t or "").replace("·", ",").replace("MiHuertoUrbano.xyz", "Mi Huerto Urbano").replace("mihuertourbano.xyz", "Mi Huerto Urbano")
    return re.sub(r"\s+", " ", t).strip()

def trozos_lamina(s: dict):
    """Lista de (texto, silencio_despues). Titular y frase van separados y cada coma lleva su pausa."""
    out = []
    tit, sub = limpiar(s.get("titulo", "")), limpiar(s.get("subtitulo", ""))
    if tit:
        out.append((tit.rstrip(".") + ".", PAUSA_TITULO if sub else 0))
    if sub:
        partes = re.split(r"([,;:.])\s+", sub)
        for i in range(0, len(partes), 2):
            txt = partes[i].strip()
            sep = partes[i + 1] if i + 1 < len(partes) else ""
            if not txt:
                continue
            pausa = PAUSA_COMA if sep == "," else (PAUSA_PUNTO if sep else 0)
            # La coma se mantiene al final del trozo para que la entonación quede "abierta"
            out.append((txt.rstrip(".") + (sep if sep and sep in ",;:" else "."), pausa))
    return out

_VOZ = {}
MOTOR = "gemini"   # "gemini" (voz Achird, elegida por Jesús), "kokoro" (em_alex) o "piper" (la antigua)

def texto_gemini(trozos) -> str:
    return " ".join(t for t, _ in trozos)

_GEM = {}   # audios de Gemini preparados para este reel

def preparar_gemini(slides):
    """Busca los audios de Gemini del reel: uno por lámina (si ya están todos) o uno para el guion entero
    troceado en frases. Devuelve True si hay voz de Gemini para todas las láminas."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import voz_gemini as G
    _GEM.clear()
    con_texto = {i: trozos_lamina(s) for i, s in enumerate(slides) if trozos_lamina(s)}
    por_lamina = {i: G.descargar(texto_gemini(t), estilo=G.ESTILO_LIBRE) for i, t in con_texto.items()}
    if por_lamina and all(por_lamina.values()):
        _GEM.update(modo="lamina", audios=por_lamina)
        return True
    trozos, sr = G.repartir_entero({i: [x for x, _ in t] for i, t in con_texto.items()})
    if trozos:
        _GEM.update(modo="entero", trozos=trozos, sr=sr, pausas={i: [p for _, p in t] for i, t in con_texto.items()})
        return True
    _GEM.update(modo=None, entero_existe=sr is not None, con_texto=con_texto)
    return False

def sintetizar_gemini(trozos, salida: Path, i: int):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import voz_gemini as G
    if _GEM.get("modo") == "lamina":
        pcm, sr = _GEM["audios"][i]
        pcm = G.recortar(pcm, sr)
    elif _GEM.get("modo") == "entero":
        sr = _GEM["sr"]
        pcm = b"".join(t + b"\x00\x00" * int(sr * p) for t, p in zip(_GEM["trozos"][i], _GEM["pausas"][i]))
    else:
        return None
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm)
    return len(pcm) / 2 / sr

def sintetizar(modelo: Path, trozos, salida: Path, i: int = 0) -> float:
    if MOTOR == "gemini":
        return sintetizar_gemini(trozos, salida, i)
    if MOTOR == "kokoro":
        return sintetizar_kokoro(trozos, salida)
    return sintetizar_piper(modelo, trozos, salida)

def sintetizar_kokoro(trozos, salida: Path) -> float:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from voz_kokoro import Kokoro24
    k = _VOZ.get("kokoro") or _VOZ.setdefault("kokoro", Kokoro24(velocidad=1.05))
    audio = bytearray()
    for texto, pausa in trozos:
        pcm, _ = k.decir(texto)
        audio += pcm + b"\x00\x00" * int(k.sr * pausa)
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(k.sr); w.writeframes(bytes(audio))
    return len(audio) / 2 / k.sr

def sintetizar_piper(modelo: Path, trozos, salida: Path) -> float:
    from piper import PiperVoice
    from piper.config import SynthesisConfig
    voz = _VOZ.get(str(modelo)) or _VOZ.setdefault(str(modelo), PiperVoice.load(str(modelo)))
    cfg = SynthesisConfig(length_scale=VELOCIDAD, noise_scale=ENTONACION)
    sr = voz.config.sample_rate
    audio = bytearray()
    for texto, pausa in trozos:
        for chunk in voz.synthesize(texto, syn_config=cfg):
            audio += chunk.audio_int16_bytes
        audio += b"\x00\x00" * int(sr * pausa)
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(bytes(audio))
    return len(audio) / 2 / sr

def ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accion", choices=["pedido", "medir", "mezclar"])
    ap.add_argument("config"); ap.add_argument("reel", nargs="?"); ap.add_argument("salida", nargs="?")
    ap.add_argument("--modelo", default=str(MODELO))
    ap.add_argument("--motor", choices=["gemini", "kokoro", "piper"], default="gemini")
    ap.add_argument("--trans-dur", type=float, default=0.5)
    a = ap.parse_args()
    global MOTOR
    MOTOR = a.motor
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    slides = cfg.get("slides") or cfg.get("diapositivas")
    dur = float(cfg.get("duracion_slide", 3.4))
    if a.accion == "pedido":
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import voz_gemini as G
        if preparar_gemini(slides):
            print("-- Ya están todos los audios de Gemini.")
        elif not _GEM["entero_existe"]:   # un solo audio para todo el reel (cupo diario pequeño)
            frases = {i: [x for x, _ in t] for i, t in _GEM["con_texto"].items()}
            print("\n".join(G.sql_pedido(G.pedido([G.guion_entero(frases)]))))
        else:                              # el entero no se troceó bien: uno por lámina
            textos = [texto_gemini(t) for t in _GEM["con_texto"].values()]
            print("\n".join(G.sql_pedido(G.pedido(textos, estilo=G.ESTILO_LIBRE))))
        return
    if MOTOR == "gemini" and not preparar_gemini(slides):
        print("AVISO: faltan audios de Gemini (lanza 'pedido' y ejecuta su SQL). Uso la voz de Kokoro.", file=sys.stderr)
        MOTOR = "kokoro"
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        wavs, largos = [], []
        for i, s in enumerate(slides):
            w = td / f"v{i}.wav"
            largos.append(sintetizar(Path(a.modelo), trozos_lamina(s), w, i) if trozos_lamina(s) else 0.0)
            wavs.append(w)
        # láminas sin texto: un silencio corto para que el montaje no falle
        for x, w in zip(largos, wavs):
            if not w.exists():
                with wave.open(str(w), "wb") as f:
                    f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000); f.writeframes(b"\x00\x00" * 2400)
        necesaria = round(max(MIN_DUR, max(largos) + MARGEN_ANTES + MARGEN_DESPUES + a.trans_dur), 1)
        if a.accion == "medir":
            print(json.dumps({"duracion_slide": necesaria, "voz_por_lamina": [round(x, 2) for x in largos], "motor": MOTOR}))
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
    print(f"✅ Reel con voz ({MOTOR}):", a.salida)

if __name__ == "__main__":
    main()
