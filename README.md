# Rama `redes` — piezas listas para Instagram y Facebook

Esta rama **no forma parte de la web** (no se despliega). Guarda las piezas que
genera `reels/generar_reel.py` para publicarlas desde el Centro de mando
(Supabase, esquema `centro`).

- `carruseles/<slug>/01.jpg … NN.jpg` — láminas 1080×1350 (4:5) en orden.
- `configs/<slug>-carrusel.json` — la configuración con la que se generaron
  (copia también en `reels/config/` de la rama de trabajo cuando se integre).

El publicador de Supabase descarga las láminas desde
`https://raw.githubusercontent.com/jesusgarciaoropesa-dotcom/otro/redes/carruseles/<slug>/NN.jpg`.

Rotación de fotos: el Centro de mando apunta qué foto de `web/public/images/articulos/`
usa cada publicación (`centro.fotos_usos`) para no repetir siempre las mismas, y
lista en `centro.fotos_pendientes` las fotos nuevas que conviene generar con Gemini
(método de `especificaciones-fotos-articulos.md`: editar la foto base del balcón).
