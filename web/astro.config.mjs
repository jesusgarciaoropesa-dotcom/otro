// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
// Configurado para GitHub Pages (proyecto, no dominio propio):
// https://jesusgarciaoropesa-dotcom.github.io/otro/
// Cuando se pase a un dominio propio, cambia `site` por el dominio y
// elimina `base` (o ponlo a '/').
export default defineConfig({
  site: 'https://jesusgarciaoropesa-dotcom.github.io',
  base: '/otro',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
