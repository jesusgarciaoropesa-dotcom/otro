// @ts-check
import { defineConfig } from 'astro/config';
import fs from 'node:fs';
import path from 'node:path';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// Mapa ruta -> fecha (updatedDate si existe, si no pubDate) leído de las
// portadas de los artículos, para poblar <lastmod> en el sitemap y ayudar a
// Google a saber cuándo recrawlear cada página.
const dirArticulos = path.resolve('./src/content/articulos');
const lastmodPorRuta = {};
for (const archivo of fs.readdirSync(dirArticulos)) {
  if (!archivo.endsWith('.md')) continue;
  const txt = fs.readFileSync(path.join(dirArticulos, archivo), 'utf-8');
  const upd = txt.match(/^updatedDate:\s*(\d{4}-\d{2}-\d{2})/m);
  const pub = txt.match(/^pubDate:\s*(\d{4}-\d{2}-\d{2})/m);
  const fecha = upd?.[1] ?? pub?.[1];
  if (fecha) lastmodPorRuta[`/articulos/${archivo.replace(/\.md$/, '')}/`] = fecha;
}

// https://astro.build/config
// Dominio propio servido vía GitHub Pages con public/CNAME.
export default defineConfig({
  site: 'https://mihuertourbano.xyz',
  // Redirecciones 301 de artículos fusionados hacia su versión canónica, para
  // concentrar la autoridad SEO en una sola página y no competir consigo mismos.
  redirects: {
    // URL rota con un espacio (%20) que aparece en Search Console
    '/articulos/culo-negro- tomate-podredumbre-apical/':
      '/articulos/culo-negro-tomate-podredumbre-apical/',
    '/articulos/que-sembrar-otono-huerto-terraza/':
      '/articulos/que-plantar-huerto-urbano-noviembre/',
    '/articulos/que-plantar-huerto-urbano-verano/':
      '/articulos/que-plantar-huerto-urbano-julio/',
    '/articulos/jardin-hierbas-aromaticas-en-cocina/':
      '/articulos/huerto-aromaticas-interior-poca-luz/',
    '/articulos/mejores-kits-riego-automatico-terraza/':
      '/articulos/mejor-sistema-riego-automatico-macetas-balcon/',
    '/articulos/huerto-urbano-principiantes-guia-completa/':
      '/articulos/como-empezar-huerto-urbano-balcon/',
    '/articulos/guia-frutales-en-maceta-balcon/':
      '/articulos/frutales-enanos-maceta-terraza/',
    '/articulos/mejor-tierra-macetas-hortalizas-guia-compra/':
      '/articulos/mejor-sustrato-huerto-urbano-maceta/',
    '/articulos/culo-negro-pimiento/':
      '/articulos/culo-negro-tomate-podredumbre-apical/',
    '/articulos/riego-automatico-app-movil-mejores-dispositivos/':
      '/articulos/mejor-sistema-riego-automatico-macetas-balcon/',
    '/articulos/remedios-caseros-contra-plagas-huerto-urbano/':
      '/articulos/remedios-caseros-plagas-que-no-funcionan/',
  },
  integrations: [
    sitemap({
      // Fuera del sitemap: el buscador interno y la página de enlaces (noindex),
      // que no son contenido para mostrar en Google.
      filter: (pagina) => !/\/(buscar|enlaces)\/$/.test(new URL(pagina).pathname),
      serialize(item) {
        const { pathname } = new URL(item.url);
        if (lastmodPorRuta[pathname]) item.lastmod = lastmodPorRuta[pathname];
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
