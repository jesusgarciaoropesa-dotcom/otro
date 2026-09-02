# Cómo hacer pines de Pinterest — MiHuertoUrbano

Pinterest es, para un blog de jardinería, la **vía más rápida a tráfico web**:
funciona como buscador visual, indexa en días (no meses como Google) y cada pin
enlaza directo a un artículo. Es la palanca principal mientras el SEO de Google
madura.

## Qué genera

Por cada pin, dos archivos en `pinterest/salida/`:
- `<slug>.png` — imagen vertical **1000×1500** con el estilo de marca (foto del
  artículo, titular en Fraunces con palabra subrayada, logo, CTA y dominio).
- `<slug>.txt` — el texto listo para pegar en Pinterest: **título**,
  **descripción** (con palabras clave), **enlace de destino** y **hashtags**.

## Crear una tanda de pines

1. Copia y edita un JSON en `pinterest/config/`:

   ```json
   {
     "pines": [
       {
         "slug": "hojas-aguacate-marrones-secas-que-hacer",
         "kicker": "AGUACATE EN MACETA",
         "gancho": "Hojas del aguacate marrones",
         "destacado": "marrones",
         "subtitulo": "por qué pasa y cómo salvarlo",
         "hashtags": ["aguacate", "aguacateenmaceta"]
       }
     ]
   }
   ```

   - `slug`: el artículo. De él se sacan **la foto, las palabras clave y la URL**
     automáticamente.
   - `gancho` + `destacado` + `subtitulo`: el texto del pin (la palabra `destacado`
     se subraya en dorado).
   - `foto` (opcional): ruta de imagen si quieres una distinta a la del artículo.
   - `hashtags` (opcional): etiquetas específicas del tema; se suman a las de marca.

2. Genera:

   ```bash
   python3 pinterest/generar_pin.py pinterest/config/tanda-1.json
   ```

## Cómo publicar en Pinterest (rutina recomendada)

- Sube **1-3 pines al día** (constancia > cantidad). Pinterest premia publicar seguido.
- Crea **tableros por tema**: "Aguacate en maceta", "Riego automático balcón",
  "Qué plantar cada mes", "Plagas del huerto urbano", "Tomates en maceta"…
- Al subir cada pin: pega el **título** y la **descripción** del `.txt`, y pon el
  **enlace de destino** al artículo (¡clave para que traiga tráfico!).
- Puedes hacer **varios pines distintos del mismo artículo** (distinto gancho/foto)
  para multiplicar alcance sin escribir más contenido.

## Idea a futuro

Pinterest permite **pines de vídeo**: los reels que ya generas (`reels/`) sirven
también como pines de vídeo, que suelen tener aún más alcance.
