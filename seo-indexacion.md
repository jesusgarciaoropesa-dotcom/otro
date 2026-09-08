# Indexación y tráfico — diagnóstico y plan

> Documento vivo. Nace de la pregunta recurrente **"¿cómo aumento el tráfico?"**
> y del informe de Search Console **"Descubierta: actualmente sin indexar"**
> (73 páginas, sept. 2026). Aquí queda el diagnóstico para no repetirlo cada vez.

## Resumen en una frase

La web está **bien construida** (SEO técnico, enlazado interno y rastreo son
correctos). El cuello de botella es la **edad y autoridad del dominio**: un
sitio de ~7 semanas en `.xyz` y casi sin enlaces externos tarda en que Google
priorice indexar todo. Eso **se acelera con acciones**, no solo esperando.

## Lo que YA está bien (comprobado en el código, no tocar)

- **Sitemap** + sitemap de imágenes + `robots.txt` correctos y enlazados.
- **Enlazado interno fuerte**: cada artículo enlaza a 3 relacionados + su serie
  + su categoría. Solo 2 huérfanos reales (`repollo-col`, `rucula`).
- **Rastreo poco profundo**: `/articulos/` lista TODOS los artículos por
  categoría y está en el pie de todas las páginas → cualquier artículo está a
  2 clics de la home. Perfecto para el robot de Google.

Conclusión: **no hace falta reformar la estructura**. El trabajo es de
prioridad de indexación, contenido duplicado y autoridad.

## Acción nº 1 (la que más manda hoy): pedir indexación a mano

Es lo más potente que puedes hacer tú mismo, gratis, en Search Console:

1. Entra en Search Console → barra de arriba **"Inspeccionar URL"**.
2. Pega la URL completa del artículo (p. ej.
   `https://mihuertourbano.xyz/articulos/culo-negro-tomate-podredumbre-apical/`).
3. Pulsa **"Solicitar indexación"**. Espera a que valide (~1 min).
4. Repite con las páginas prioritarias. Hay un límite diario (~10-15), así que
   ve por tandas, empezando por las de abajo.

**Prioridad para pedir indexación** (más valor comercial / más búsquedas):

Páginas dinero (afiliados, comparativas):
- `mejor-sistema-riego-automatico-macetas-balcon`
- `mejores-productos-ecologicos-contra-plagas-huerto`
- `mejor-maceta-frutales-balcon-guia-compra`
- `mejores-macetas-autorregantes-balcon-comparativa`
- `mejores-tutores-estacas-tomateras-pimientos`
- `mejores-kits-huerto-urbano-principiantes`

Problemas que la gente busca mucho (tráfico + enlazan a las de arriba):
- `culo-negro-tomate-podredumbre-apical`
- `por-que-tomateras-se-ponen-amarillas`
- `flores-tomate-caen-sin-cuajar`
- `mildiu-tomatera-como-tratarlo`
- `gomosis-frutales-hueso-durazno-ciruelo` (nuevo)
- `manchas-marrones-hojas-acelga-cercospora` (nuevo)

De temporada (pedir indexación cuando toque el mes):
- `que-plantar-huerto-urbano-octubre` y los meses siguientes.

## Acción nº 2: arreglar contenido DUPLICADO (canibalización)

Hay **pares de artículos que compiten por la misma búsqueda**. Google no sabe
cuál mostrar, reparte la fuerza entre los dos y a veces deja el más débil
**sin indexar**. Detectados (formato: ganador ↔ gemelo débil por enlaces
internos entrantes):

1. **Riego automático (comparativa):**
   - Gana `mejor-sistema-riego-automatico-macetas-balcon` (44 enlaces).
   - Débil `mejores-kits-riego-automatico-terraza` (1 enlace) — casi el mismo tema.
2. **Empezar / principiantes:**
   - Gana `como-empezar-huerto-urbano-balcon` (4).
   - Débil `huerto-urbano-principiantes-guia-completa` (1).
3. **Frutales en maceta (guía general):**
   - Gana `frutales-enanos-maceta-terraza` (8).
   - Débil `guia-frutales-en-maceta-balcon` (1).

**Qué hacer con cada par (decisión del dueño):**
- **Opción A (recomendada) — fusionar:** llevar lo bueno del débil al ganador y
  luego **redirigir** el débil al ganador (301). Concentra toda la fuerza en una
  sola página. En este sitio (Astro + GitHub Pages) la redirección se hace con
  una etiqueta de redirección o con la config de redirects de Astro.
- **Opción B — diferenciar:** reescribir el débil para que apunte a OTRA
  intención de búsqueda distinta (que no se solapen las keywords). Más trabajo,
  solo si de verdad son dos temas distintos.

> Los clústeres de tomate, plagas, compost y vertical **NO son duplicados**: son
> subtemas distintos (autoridad temática buena). No tocarlos.

## Acción nº 3: autoridad externa (el volante de inercia)

Google indexa antes lo que "existe" fuera de tu web:
- **Grupos de Facebook**: responder dudas útil primero → cuando encaje, enlace
  al artículo (ver regla de estilo en `CLAUDE.md`). Aquí el enlace sí funciona
  (a diferencia de Pinterest, que bloqueó la cuenta como spam).
- **Reels** constantes (IG/FB) con "enlace en la bio" / enlace directo en FB.
- Cualquier mención en foros, otros blogs o directorios de nicho ayuda.

## Acción nº 4: frescura, con cabeza

Actualizar un artículo **de verdad** (añadir una sección, una foto, una FAQ) y
poner `updatedDate` invita a Google a re-rastrear. No hacer cambios de fecha
"en falso" en lote: no aporta y puede parecer manipulación.

## Qué NO es el problema (para no perder tiempo)

- No es el sitemap, ni el robots.txt, ni el enlazado interno general.
- No es falta de una página índice: `/articulos/` ya existe y está en el pie.
- No es penalización: "Descubierta: sin indexar" = pendiente de prioridad, no castigo.

## Realidad temporal

En un sitio joven, pasar de "descubierta" a "indexada" para 200+ páginas lleva
**semanas**, incluso haciéndolo todo bien. Lo que acelera de verdad: pedir
indexación a mano de las prioritarias + autoridad externa + resolver duplicados.
