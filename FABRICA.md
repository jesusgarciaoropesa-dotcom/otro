# Fábrica de contenido — MiHuertoUrbano

Cinco agentes de IA preparan cada semana las publicaciones de Instagram y Facebook. Cada uno es una
tarea programada de Claude con **un solo trabajo**; se pasan el trabajo a través de tablas del esquema
`centro` de Supabase (`wtj-barbershop`). Jesús solo decide en dos sitios del panel **Centro de mando**:
las propuestas del Analista (pestaña *Fábrica*) y las publicaciones (pestaña *Revisar*).

## La cadena

```
Analista ──propuestas──▶ Jesús aprueba ──reglas──▶ todos
   │ informe (temas próximos)
   ▼
Estratega ──plan_editorial (planificado)──▶ Fotógrafo ──(fotos_listas)──▶ Productor
                                               │ fotos_pendientes ▶ Jesús (Gemini)
Productor ──publicaciones (para_revisar)──▶ Revisor ──revisión + informe──▶ Jesús aprueba ──▶ Publicador
```

| Agente | Cuándo (Madrid) | Hace | Lee | Escribe |
| --- | --- | --- | --- | --- |
| Analista | jueves 10:17 | Mira la competencia (web y redes) y la temporada; propone mejoras con fuente | propuestas, reglas, publicaciones, informes | `propuestas`, `informes` |
| Estratega | sábado 9:47 | Elige los 3 temas de la semana siguiente con gancho, ángulo, guion y escenarios | reglas, propuestas aprobadas, informe del Analista, artículos | `plan_editorial` → *planificado* |
| Fotógrafo | sábado 12:23 | Elige la foto de cada lámina con variedad de escenarios; pide las que faltan | plan, `fotos`, `fotos_uso`, `escenarios` | `plan_editorial.fotos` → *fotos_listas*, `fotos_pendientes` |
| Productor | domingo 9:31 | Incorpora fotos nuevas, genera los carruseles, los sube aquí y crea las publicaciones | plan, `fotos_pendientes`, reglas | rama `redes`, `publicaciones` → *para_revisar*, plan → *producido* |
| Lector de redes | miércoles 9:07 | Guarda tus números de Instagram (alcance, vistas, guardados) y los de la competencia (función de Supabase, no IA) | `competidores` | `redes_fotos` |
| Revisor | domingo 12:47 | Comprueba datos, láminas, textos, enlaces y reglas; corrige lo pequeño; resumen a Jesús | publicaciones, artículos, reglas | `publicaciones.revision`, `informes` |
| Publicador | cada 15 min | Publica lo aprobado cuando llega su hora: carruseles, reels y, tras cada carrusel, su historia (función de Supabase, no IA) | publicaciones *aprobada* | Meta, `publicaciones` |
| Informe mensual | día 1, 11:23 | Resume el mes: seguidores, alcance por formato, mejores posts y competencia | `redes_fotos`, `publicaciones` | `informes`, `propuestas` |

La ficha de cada agente (misión, horario, a quién entrega) está en `centro.agentes`, y su última
ejecución en la vista `centro.agentes_estado` (cada agente registra lo que hace en `centro.registro`).
Si un agente no pasa, el siguiente cubre su parte (el Productor sabe elegir temas y fotos él solo).

## Formatos

- **Carrusel** (lunes, miércoles y viernes 13:30): láminas 4:5 en `carruseles/<slug>/NN.jpg`.
- **Reel** (el día siguiente a su carrusel, 19:30): el mismo contenido en vídeo vertical 1080×1920 sin música,
  `reels/<slug>.mp4`, con la lámina 01 como portada. Otra primera línea de texto.
  Voz en off con `herramientas/voz_reel.py`: voz **em_alex de Kokoro** (elegida por Jesús el 5-11-2026;
  gratis y de uso comercial libre; el modelo se descarga solo la primera vez). La de Piper queda con `--motor piper`.
- **Historia** (sale sola justo después del carrusel): `carruseles/<slug>/historia.jpg`, hecha con
  `herramientas/generar_historia.py` a partir de la portada.

## Propuestas y reglas

El Analista escribe como mucho 5 propuestas por semana en `centro.propuestas`. Si Jesús aprueba una
que trae `regla_propuesta`, un trigger la copia a `centro.reglas` y desde ese momento la cumplen todos
los agentes. Las que no se pueden automatizar quedan como tareas de Jesús en la pestaña Fábrica.
Las descartadas no se vuelven a proponer.

## Piezas

| Pieza | Dónde |
| --- | --- |
| Artículos y fotos propias | rama de trabajo del repo (`web/src/content/articulos`, `web/public/images/articulos`) |
| Generador de carruseles y reels | `reels/generar_reel.py` (rama de trabajo) |
| Carruseles generados y sus configuraciones | esta rama `redes` (`carruseles/<slug>/`, `configs/`) |
| Fotos nuevas hechas con Gemini | esta rama `redes` (`fotos-nuevas/`); para la web hay que copiarlas a `web/public/images/articulos/` en la rama de despliegue |

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
