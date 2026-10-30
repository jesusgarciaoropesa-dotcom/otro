# Fábrica semanal de contenido — MiHuertoUrbano

Cómo se preparan cada semana las publicaciones de Instagram y Facebook. Lo ejecuta
una tarea programada de Claude **cada domingo a las 9:31** (hora de Madrid) y el
resultado se revisa en el panel **Centro de mando** (pestaña Revisar).

## Piezas

| Pieza | Dónde |
| --- | --- |
| Artículos y fotos propias | rama de trabajo del repo (`web/src/content/articulos`, `web/public/images/articulos`) |
| Generador de carruseles y reels | `reels/generar_reel.py` (rama de trabajo) |
| Carruseles generados y sus configuraciones | esta rama `redes` (`carruseles/<slug>/`, `configs/`) |
| Cola de publicación, inventario de fotos, fotos pendientes | Supabase `wtj-barbershop`, esquema `centro` |
| Publicación en Meta | función `publicar` de Supabase, cada 15 minutos, solo lo aprobado |

## Cada domingo

1. Elige **3 temas de temporada** de los artículos de la web (lunes, miércoles y viernes a las 13:30).
2. Para cada tema monta un **carrusel 4:5** con el generador y con **fotos propias**, evitando las
   que se han usado en redes en las últimas 8 semanas (`centro.fotos_uso`).
3. Sube las láminas a esta rama y crea las publicaciones en `centro.publicaciones` como *para revisar*.
4. Si un tema necesita una foto que no existe o las que hay están muy gastadas, añade una petición a
   `centro.fotos_pendientes` con la descripción para Gemini, el escenario y la foto que hay que adjuntar
   (ver *Escenarios*).
5. Las fotos nuevas que Jesús sube desde el panel se guardan aquí en `fotos-nuevas/` y pasan al
   inventario. Para que salgan también en la web hay que copiarlas a `web/public/images/articulos/`
   en la rama de despliegue.

## Escenarios

Las fotos no salen siempre del mismo balcón. Cada foto está clasificada en `centro.fotos.escenario` y
`centro.escenarios` describe cada escenario, su foto base y cómo se pide a Gemini:

| Escenario | Qué es | Gemini |
| --- | --- | --- |
| forja | balcón de barandilla de hierro y edificios antiguos | editar `cuantas-horas-sol-balcon.jpg` |
| mirador | maceta de barro en barandilla con la ciudad al fondo | no pedir más (ya hay demasiadas) |
| ladrillo | balcón de ladrillo con jardín vertical | editar `hero-huerto.jpg` |
| terraza | terraza de pared blanca | editar `cultivo-repollo-col-maceta.jpg` |
| interior | junto a la ventana | editar `semillero-plantulas-ventana.jpg` |
| manos | primer plano de manos trabajando | referencia de estilo |
| bodegon | objetos sobre mesa, vista cenital | referencia de estilo |
| macro | detalle de insecto, hoja o fruto | referencia de estilo |
| exterior | huerto o árbol en suelo | referencia de estilo |

Reglas: cada carrusel mezcla al menos 3 escenarios, como mucho 2 fotos de *mirador*, sin dos láminas
seguidas del mismo escenario si hay alternativa, y las 3 portadas de la semana de escenarios distintos.
Las fotos nuevas se piden en los escenarios con menos fotos.

## Reglas de contenido

- Español de España, tuteando, tono cercano y práctico (ver `CLAUDE.md`).
- Instagram: enlace en la bio. Facebook: enlace directo al artículo.
- Las correcciones de Jesús están en `centro.reglas` y son obligatorias.
- Nada de inventar datos: todo sale de los artículos de la web.
