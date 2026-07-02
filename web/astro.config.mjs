// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
// Dominio propio servido vía GitHub Pages con public/CNAME.
export default defineConfig({
  site: 'https://mihuertourbano.xyz',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
