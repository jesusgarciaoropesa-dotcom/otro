import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articulos = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articulos' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    categoria: z.enum([
      'primeros-pasos',
      'riego-automatico',
      'cultivo-vertical',
      'que-plantar',
      'frutales-en-maceta',
      'calendario-de-siembra',
      'plagas-y-enfermedades',
      'herramientas-y-comparativas',
      'compostaje-sostenibilidad',
    ]),
    intencion: z.enum(['informativa', 'transaccional', 'comparativa']),
    keywords: z.array(z.string()),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    pilar: z.boolean().default(false),
    faq: z.array(z.object({ pregunta: z.string(), respuesta: z.string() })).optional(),
  }),
});

export const collections = { articulos };
