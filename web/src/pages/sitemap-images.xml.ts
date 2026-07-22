import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { primeraImagen } from '../lib/articuloImagen';

/**
 * Sitemap de imágenes: ayuda a posicionar las fotos de las guías en Google
 * Imágenes (una fuente de tráfico relevante en jardinería). Lista cada
 * artículo con la imagen que abre la guía y su título como caption.
 *
 * Se referencia desde robots.txt junto al sitemap principal.
 */
export const GET: APIRoute = async ({ site }) => {
  const base = (site ?? new URL('https://mihuertourbano.xyz')).toString().replace(/\/$/, '');
  const articulos = await getCollection('articulos');

  const escapar = (s: string) =>
    s
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');

  const urls = articulos
    .map((a) => {
      const img = primeraImagen(a.body);
      if (!img) return null;
      const loc = `${base}/articulos/${a.id}/`;
      const imgLoc = `${base}${img}`;
      return `  <url>
    <loc>${escapar(loc)}</loc>
    <image:image>
      <image:loc>${escapar(imgLoc)}</image:loc>
      <image:title>${escapar(a.data.title)}</image:title>
      <image:caption>${escapar(a.data.description)}</image:caption>
    </image:image>
  </url>`;
    })
    .filter(Boolean)
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
${urls}
</urlset>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
};
