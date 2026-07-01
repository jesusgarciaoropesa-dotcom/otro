# Mi Balcón Verde — web del nicho "huerto urbano en balcón/terraza"

Sitio estático construido con [Astro](https://astro.build) + Tailwind CSS, siguiendo
el plan de negocio de `../plan-nicho-huerto-urbano-balcon.md`. Pensado para SEO y
monetización con Google AdSense + afiliación.

## Estructura del proyecto

```
web/
├── public/
│   ├── robots.txt
│   └── ads.txt              # completar con tu Publisher ID de AdSense
├── src/
│   ├── content/articulos/    # artículos en Markdown (aquí se añade contenido nuevo)
│   ├── content.config.ts     # schema de la colección de artículos
│   ├── data/categorias.ts    # las 9 categorías del sitio
│   ├── components/           # Header, Footer, AdSlot
│   ├── layouts/               # BaseLayout, ArticleLayout
│   └── pages/
│       ├── index.astro                    # home
│       ├── categorias/[categoria].astro   # listado por categoría (ruta dinámica)
│       ├── articulos/[...slug].astro      # artículo individual (ruta dinámica)
│       └── *.astro                        # páginas legales (privacidad, cookies, contacto...)
```

## Cómo añadir un artículo nuevo

Crea un archivo `.md` en `src/content/articulos/` con este frontmatter:

```md
---
title: "Título SEO del artículo"
description: "Meta descripción de 150-160 caracteres"
categoria: "que-plantar" # una de las 9 categorías definidas en src/data/categorias.ts
intencion: "informativa" # informativa | transaccional | comparativa
keywords: ["keyword long-tail 1", "keyword long-tail 2"]
pubDate: 2026-04-01
pilar: false # true solo para el artículo principal de una categoría (se destaca en home)
---

Contenido del artículo en Markdown...
```

El slug de la URL es el nombre del archivo (sin `.md`). La página se genera
automáticamente en `/articulos/<nombre-del-archivo>/` y aparece en el listado de su
categoría y en "Últimos artículos" de la home sin tocar código.

El plan de contenido completo (88 títulos clasificados por categoría, con
intención de búsqueda) está en `../plan-nicho-huerto-urbano-balcon.md`, sección 4.
Ya están escritos 8 artículos de muestra como referencia de formato y tono.

## Monetización (AdSense)

- El componente `src/components/AdSlot.astro` inserta el bloque de anuncio. Está
  colocado en 3 posiciones (siguiendo la sección 6 del plan): home (`home-mid`),
  categoría (`categoria-<slug>-top`) y artículo (`article-top` y `article-bottom`).
- Antes de publicar: sustituye `ADSENSE_CLIENT_ID` en `AdSlot.astro` por tu
  `ca-pub-XXXXXXXXXXXXXXXX` real, añade el script de AdSense en `BaseLayout.astro`
  (`<head>`), y completa `public/ads.txt` con la línea que te da tu cuenta de AdSense.
- Para insertar anuncios *dentro* del cuerpo de un artículo (no solo arriba/abajo),
  puedes añadir un remark/rehype plugin que inyecte `<AdSlot />` tras el segundo o
  tercer párrafo — no incluido en este scaffold inicial para mantenerlo simple.

## Antes de publicar en producción

1. Sustituye el contenido de `politica-de-privacidad.astro` y
   `politica-de-cookies.astro` por texto legal revisado (son plantillas de partida).
2. Añade un banner de consentimiento de cookies (CMP) compatible con Google Consent
   Mode si vas a tener tráfico de la UE.
3. Cambia el dominio en `astro.config.mjs` (`site: '...'`) por el dominio real.
4. Sustituye los enlaces de afiliado de ejemplo por tus enlaces reales (Amazon
   Afiliados, etc.) cuando los añadas al contenido.

## Comandos

| Comando           | Acción                                              |
| :----------------- | :--------------------------------------------------- |
| `npm install`       | Instala dependencias                                 |
| `npm run dev`       | Servidor local en `http://localhost:4321`            |
| `npm run build`     | Build de producción en `./dist/`                     |
| `npm run preview`   | Previsualiza el build antes de desplegar             |

## Despliegue

Al ser un sitio 100% estático, se despliega gratis en **Vercel** o **Netlify**:
conecta el repositorio, indica `web/` como directorio raíz del proyecto, comando de
build `npm run build` y directorio de salida `dist/`. También funciona en
cualquier hosting estático (Cloudflare Pages, GitHub Pages, etc.).

### GitHub Pages (configuración actual del repo)

El repo está configurado para GitHub Pages en modo **"Deploy from a branch"**,
que sirve archivos tal cual sin ejecutar ningún build. Como Astro necesita
`npm run build`, el workflow `.github/workflows/deploy-web.yml` compila el sitio
en cada push a `web/` y publica el contenido de `web/dist/` en una rama `gh-pages`
(usando `peaceiris/actions-gh-pages`).

**Pasos para activarlo:**
1. Haz push de estos cambios (el workflow se ejecuta automáticamente y crea/actualiza
   la rama `gh-pages`).
2. En el repo, ve a **Settings → Pages**.
3. En **Source**, selecciona **Deploy from a branch**.
4. En **Branch**, elige `gh-pages` y la carpeta `/ (root)`. Guarda.
5. El sitio quedará publicado en `https://jesusgarciaoropesa-dotcom.github.io/otro/`.

Como es un *project site* (no `usuario.github.io`), Astro necesita `base: '/otro'`
en `astro.config.mjs` para que todos los enlaces y assets funcionen bajo esa
subruta — ya está configurado. Todos los enlaces internos usan el helper
`src/lib/url.ts` (`withBase()`) precisamente para no depender de rutas absolutas
hardcodeadas, que romperían bajo un `base` distinto de `/`.

Si en el futuro pasas a un dominio propio (ej. `milbalconverde.com`), cambia en
`astro.config.mjs`: `site` al dominio real y `base: '/'` (o elimínalo), añade un
archivo `public/CNAME` con el dominio, y actualiza el DNS según la
[documentación de GitHub Pages](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site).
