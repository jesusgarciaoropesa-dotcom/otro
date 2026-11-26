// llms.txt (formato llmstxt.org): resumen de la web para asistentes de IA (ChatGPT, Perplexity, Claude…).
// Se genera solo en cada build con todos los artículos, agrupados por categoría.
import { getCollection } from 'astro:content';
import { categorias } from '../data/categorias';

export async function GET() {
  const articulos = await getCollection('articulos');
  const lineas: string[] = [
    '# MiHuertoUrbano (mihuertourbano.xyz)',
    '',
    '> Guías prácticas en español de España para cultivar hortalizas, aromáticas y frutales en balcones, terrazas y macetas, con clima de interior peninsular (heladas en invierno y mucho calor en verano): qué plantar cada mes, riego, plagas, sustratos y frutales en maceta.',
    '',
    '- [Qué plantar en tu balcón](https://mihuertourbano.xyz/que-plantar-en-tu-balcon/): calendario de siembra por meses.',
    '- [Qué le pasa a mi planta](https://mihuertourbano.xyz/que-le-pasa-a-mi-planta/): diagnóstico de problemas por síntomas.',
    '',
  ];
  for (const c of categorias) {
    const deCat = articulos
      .filter((a) => a.data.categoria === c.slug)
      .sort((a, b) => a.data.title.localeCompare(b.data.title, 'es'));
    if (!deCat.length) continue;
    lineas.push(`## ${c.nombre}`, '');
    for (const a of deCat) lineas.push(`- [${a.data.title}](https://mihuertourbano.xyz/articulos/${a.id}/): ${a.data.description}`);
    lineas.push('');
  }
  return new Response(lineas.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
