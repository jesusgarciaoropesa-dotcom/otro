# Cómo hacer reels de MiHuertoUrbano

Este es el método (recuperado y reconstruido) para crear reels verticales para
**Instagram y Facebook** a partir de los artículos del blog. Antes vivía solo
en un chat; ahora está guardado aquí en el repo para que **no se pierda nunca
más**, aunque se cierre una conversación.

---

## Qué genera

Un vídeo vertical **1080×1920 (9:16)**, sin audio, de ~17 segundos, con **5
diapositivas** que van cambiando por corte. El estilo es el de la web:

- Foto propia del artículo con **zoom lento** (efecto Ken Burns).
- Fondo desenfocado de la misma foto.
- Nombre **MiHuertoUrbano** arriba y el **logo** (regadera + ciudad) sobre la foto.
- Banda inferior verde con: **kicker** en dorado + **titular** en tipografía
  Fraunces (con una palabra **subrayada en dorado**) + **subtítulo**.
- Diapositiva final de **llamada a la acción** (píldora dorada "GUÁRDALO · GUÍA
  EN LA BIO").

Todo usa los colores y las fuentes reales del sitio (`--color-mostaza #d9a441`,
`--color-hoja-oscuro #24401f`, Fraunces + Inter), así que siempre queda
coherente con la marca.

---

## La fórmula de las 5 diapositivas

Es la estructura que mejor funciona y la que ya usábamos:

| # | Diapositiva | Kicker (dorado) | Titular | Subtítulo |
|---|-------------|-----------------|---------|-----------|
| 1 | **Gancho** | tema / categoría | Afirmación que rompe el mito | matiz o giro |
| 2 | **Motivo** | `EL MOTIVO` | la causa real | qué provoca |
| 3 | **Solución 1** | `SOLUCIÓN 1` | acción concreta | detalle práctico |
| 4 | **Tranquiliza / Solución 2** | `TRANQUILA` o `SOLUCIÓN 2` | dato que calma o 2º consejo | aclaración |
| 5 | **CTA** | *(píldora)* `GUÁRDALO · GUÍA EN LA BIO` | — | beneficio ("Salva tu X en 2 pasos") |

Consejos de copy:
- El **titular** debe caber en 2 líneas. Frases cortas.
- La palabra **`destacado`** (la que se subraya en dorado) es la clave emocional
  o la sorpresa: *muriendo, seco, lluvia, marrones*…
- Habla de tú, tono cercano, como en el blog.

---

## Cómo crear un reel nuevo (paso a paso)

1. **Copia un JSON** de ejemplo de `reels/config/` y renómbralo:

   ```bash
   cp reels/config/aguacate-riego.json reels/config/mi-nuevo-reel.json
   ```

2. **Edítalo.** Cambia la foto y los textos de las diapositivas:

   ```json
   {
     "slug": "mi-nuevo-reel",
     "foto": "/images/articulos/NOMBRE-DE-LA-FOTO.jpg",
     "articulo": "/articulos/SLUG-DEL-ARTICULO/",
     "duracion_slide": 3.4,
     "slides": [
       { "kicker": "...", "titulo": "...", "destacado": "palabra", "subtitulo": "..." },
       { "kicker": "EL MOTIVO", "titulo": "...", "destacado": "...", "subtitulo": "..." },
       { "kicker": "SOLUCIÓN 1", "titulo": "...", "destacado": "...", "subtitulo": "..." },
       { "kicker": "TRANQUILA", "titulo": "...", "destacado": "...", "subtitulo": "..." },
       { "cta": true, "pildora": "GUÁRDALO · GUÍA EN LA BIO", "subtitulo": "..." }
     ]
   }
   ```

   - `foto`: ruta como en la web (`/images/articulos/...`), o una ruta absoluta.
   - `destacado`: la palabra del `titulo` que se subraya (debe aparecer tal cual
     en el titular).
   - Puedes poner más o menos de 5 diapositivas; la última con `"cta": true`.

3. **Genera el vídeo:**

   ```bash
   python3 reels/generar_reel.py reels/config/mi-nuevo-reel.json
   ```

   El reel queda en `reels/salida/mi-nuevo-reel.mp4`.

4. **Súbelo** a Instagram/Facebook. En el pie pon un resumen + enlace al
   artículo + hashtags (ver plantilla abajo).

---

## Opciones del generador

```bash
python3 reels/generar_reel.py <config.json> [--fps 30] [--zoom 1.08]
```

- `--fps`: fotogramas por segundo (por defecto 30).
- `--zoom`: cuánto acerca el Ken Burns (1.08 = +8 %). Sube a 1.12 para más
  movimiento, o 1.0 para desactivarlo.
- `duracion_slide` (en el JSON): segundos por diapositiva (por defecto 3.4).

---

## Plantilla de pie de foto (caption)

```
🥑 Tu aguacate en maceta con las hojas marrones no se está muriendo:
casi siempre es el riego.

Te dejo la guía completa en el blog (link en la bio) 👉
mihuertourbano.xyz/articulos/hojas-aguacate-marrones-secas-que-hacer/

Guarda el reel para cuando te pase 🌱

#huertourbano #aguacate #plantasenmaceta #jardineriaurbana #balcón
#huertoencasa #cuidadodeplantas
```

---

## Cómo funciona por dentro (para mantenerlo)

1. `generar_reel.py` lee el JSON.
2. Renderiza cada diapositiva en **dos capas** con **Chromium headless**
   (así el texto usa las fuentes reales de la web):
   - *fondo* (foto desenfocada + ventana nítida de la foto) → hace zoom.
   - *texto* (marca, logo, banda y textos) → estático y nítido encima.
3. Con **ffmpeg** aplica el zoom lento al fondo, superpone el texto y une las
   diapositivas en el `.mp4` final.

No hace falta tocar el `.py` para un reel nuevo: solo el JSON.
