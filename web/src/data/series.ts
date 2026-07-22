/**
 * Series temáticas para agrupar las fichas de cultivo por tipo de planta.
 * Sirven para enlazar entre sí guías relacionadas (todas las hortalizas de
 * fruto, todas las aromáticas…) con navegación "de la misma serie", mejorando
 * el enlazado interno y el descubrimiento de contenido.
 *
 * Los `slugs` son ids exactos de artículos existentes. El componente que las
 * consume filtra por los que realmente existen, así que añadir aquí un slug
 * que aún no exista no rompe nada.
 */
export interface Serie {
  slug: string;
  nombre: string;
  descripcion: string;
  articulos: string[];
}

export const series: Serie[] = [
  {
    slug: 'hortalizas-de-fruto',
    nombre: 'Hortalizas de fruto',
    descripcion: 'Tomate, pimiento, berenjena y otras hortalizas que dan fruto.',
    articulos: [
      'como-cultivar-tomates-en-maceta-balcon',
      'como-cultivar-pimientos-en-maceta',
      'como-cultivar-berenjenas-en-maceta',
      'como-cultivar-calabacines-espacio-reducido',
      'como-cultivar-pepinos-huerto-vertical',
      'como-cultivar-guindillas-chiles-en-maceta',
    ],
  },
  {
    slug: 'hortalizas-de-hoja',
    nombre: 'Hortalizas de hoja',
    descripcion: 'Lechuga, espinaca, acelga y demás verduras de hoja.',
    articulos: [
      'como-cultivar-lechugas-huerto-urbano',
      'como-cultivar-espinacas-en-maceta',
      'como-cultivar-acelgas-en-maceta',
      'como-cultivar-canonigos-en-maceta',
      'como-cultivar-escarola-en-maceta',
      'como-cultivar-apio-en-maceta',
    ],
  },
  {
    slug: 'coles',
    nombre: 'Coles y brásicas',
    descripcion: 'Brócoli, coliflor y kale: la familia de las coles.',
    articulos: [
      'como-cultivar-brocoli-en-maceta',
      'como-cultivar-coliflor-en-maceta',
      'como-cultivar-kale-col-rizada-en-maceta',
    ],
  },
  {
    slug: 'raices-y-bulbos',
    nombre: 'Raíces y bulbos',
    descripcion: 'Zanahoria, rábano, ajo, cebolla y otras de raíz o bulbo.',
    articulos: [
      'como-cultivar-zanahorias-en-maceta',
      'como-cultivar-rabanitos-en-balcon',
      'como-cultivar-remolacha-en-maceta',
      'como-cultivar-ajos-en-maceta',
      'como-cultivar-cebollas-en-maceta',
      'como-cultivar-patatas-en-saco-balcon',
      'como-cultivar-puerros-en-maceta',
      'como-cultivar-jengibre-en-casa',
    ],
  },
  {
    slug: 'legumbres',
    nombre: 'Legumbres',
    descripcion: 'Guisantes y judías verdes en maceta.',
    articulos: ['como-cultivar-guisantes-en-maceta', 'como-cultivar-judias-verdes-en-maceta'],
  },
  {
    slug: 'aromaticas',
    nombre: 'Aromáticas en maceta',
    descripcion: 'Albahaca, perejil, romero y todas las hierbas aromáticas.',
    articulos: [
      'como-cultivar-albahaca-en-maceta',
      'como-cultivar-perejil-en-maceta',
      'como-cultivar-cilantro-en-maceta',
      'como-cultivar-menta-en-maceta',
      'como-cultivar-romero-en-balcon',
      'como-cultivar-tomillo-en-maceta',
      'como-cultivar-oregano-en-maceta',
      'como-cultivar-cebollino-en-maceta',
      'como-cultivar-salvia-en-maceta',
      'como-cultivar-eneldo-en-maceta',
      'como-cultivar-manzanilla-en-maceta',
      'como-cultivar-laurel-en-maceta',
    ],
  },
  {
    slug: 'frutales-en-maceta',
    nombre: 'Frutales en maceta',
    descripcion: 'Fresas, cítricos y frutales enanos para balcón.',
    articulos: [
      'como-cultivar-fresas-en-balcon',
      'como-cultivar-arandanos-en-maceta',
      'como-cultivar-frambuesas-moras-en-maceta',
      'como-cultivar-granado-enano-en-maceta',
      'como-cultivar-higuera-en-maceta',
      'como-cultivar-kiwi-en-maceta',
      'como-cultivar-limonero-en-maceta',
      'como-cultivar-naranjo-enano-en-maceta',
      'como-cultivar-uva-parra-en-maceta',
      'como-cultivar-aguacate-desde-hueso',
    ],
  },
];

/** Devuelve la serie a la que pertenece un artículo, o undefined. */
export function getSerieDe(articuloId: string): Serie | undefined {
  return series.find((s) => s.articulos.includes(articuloId));
}
