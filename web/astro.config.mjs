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
  integrations: [
    sitemap({
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
