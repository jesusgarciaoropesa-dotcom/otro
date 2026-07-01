export interface Categoria {
  slug: string;
  nombre: string;
  descripcion: string;
  emoji: string;
}

export const categorias: Categoria[] = [
  {
    slug: 'primeros-pasos',
    nombre: 'Primeros Pasos',
    descripcion: 'Guías básicas para empezar tu huerto urbano desde cero, sin experiencia previa.',
    emoji: '🌱',
  },
  {
    slug: 'riego-automatico',
    nombre: 'Riego Automático',
    descripcion: 'Sistemas de riego por goteo, temporizadores y soluciones para no depender de regar a mano.',
    emoji: '💧',
  },
  {
    slug: 'cultivo-vertical',
    nombre: 'Cultivo Vertical',
    descripcion: 'Torres, paredes verdes e hidroponía para aprovechar cada centímetro de tu balcón.',
    emoji: '🧱',
  },
  {
    slug: 'que-plantar',
    nombre: 'Qué Plantar',
    descripcion: 'Fichas de cultivo de hortalizas y aromáticas adaptadas a espacios pequeños.',
    emoji: '🥬',
  },
  {
    slug: 'frutales-en-maceta',
    nombre: 'Frutales en Maceta',
    descripcion: 'Frutales enanos y de maceta que sí puedes cultivar en una terraza.',
    emoji: '🍋',
  },
  {
    slug: 'calendario-de-siembra',
    nombre: 'Calendario de Siembra',
    descripcion: 'Qué sembrar cada mes del año según la estación.',
    emoji: '📅',
  },
  {
    slug: 'plagas-y-enfermedades',
    nombre: 'Plagas y Enfermedades',
    descripcion: 'Diagnóstico y soluciones naturales para los problemas más comunes del huerto urbano.',
    emoji: '🐛',
  },
  {
    slug: 'herramientas-y-comparativas',
    nombre: 'Herramientas y Comparativas',
    descripcion: 'Las mejores macetas, kits, sustratos y sistemas de riego, comparados.',
    emoji: '🛠️',
  },
  {
    slug: 'compostaje-sostenibilidad',
    nombre: 'Compostaje y Sostenibilidad',
    descripcion: 'Compost casero y hábitos sostenibles para tu huerto en un piso sin jardín.',
    emoji: '♻️',
  },
];

export function getCategoria(slug: string): Categoria | undefined {
  return categorias.find((c) => c.slug === slug);
}
