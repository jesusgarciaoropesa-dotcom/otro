import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { getCategoria } from '../data/categorias';

export async function GET(context) {
  const articulos = await getCollection('articulos');
  const ordenados = [...articulos].sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );

  return rss({
    title: 'MiHuertoUrbano',
    description:
      'Guías prácticas para cultivar hortalizas, aromáticas y frutales en balcones y terrazas pequeñas, sin necesidad de jardín.',
    site: context.site,
    items: ordenados.map((a) => ({
      title: a.data.title,
      description: a.data.description,
      pubDate: a.data.pubDate,
      link: `/articulos/${a.id}/`,
      categories: [getCategoria(a.data.categoria)?.nombre ?? a.data.categoria],
    })),
    customData: '<language>es-es</language>',
  });
}
