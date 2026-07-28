export interface Categoria {
  slug: string;
  nombre: string;
  descripcion: string;
  /** Párrafo introductorio propio de la categoría, para dar contenido
   *  indexable a la página de listado (y no dejarla como página "thin"). */
  intro?: string;
  emoji: string;
}

export const categorias: Categoria[] = [
  {
    slug: 'primeros-pasos',
    nombre: 'Primeros Pasos',
    descripcion: 'Guías básicas para empezar tu huerto urbano desde cero, sin experiencia previa.',
    intro:
      'Empezar un huerto urbano en un balcón o una terraza no requiere experiencia ni un gran presupuesto: solo entender bien unas pocas decisiones clave. En esta sección reunimos las guías para arrancar de cero, desde cuánta luz necesitas y qué maceta y sustrato elegir, hasta los errores más habituales de principiante y cómo evitarlos. Si es tu primera vez con las manos en la tierra, este es el mejor punto de partida antes de decidir qué plantar.',
    emoji: '🌱',
  },
  {
    slug: 'riego-automatico',
    nombre: 'Riego Automático',
    descripcion: 'Sistemas de riego por goteo, temporizadores y soluciones para no depender de regar a mano.',
    intro:
      'El riego es la causa número uno de fracaso en el huerto de balcón: las macetas se secan rápido y un olvido en pleno verano puede echar a perder semanas de trabajo. Automatizarlo con un sistema de goteo y un programador es la inversión que más aumenta la tasa de éxito, sobre todo si viajas o no eres constante regando a mano. Aquí encontrarás cómo montar un riego por goteo paso a paso, qué temporizador elegir y cómo dejar las plantas atendidas durante las vacaciones.',
    emoji: '💧',
  },
  {
    slug: 'cultivo-vertical',
    nombre: 'Cultivo Vertical',
    descripcion: 'Torres, paredes verdes e hidroponía para aprovechar cada centímetro de tu balcón.',
    intro:
      'Cuando el suelo escasea, la solución es crecer hacia arriba. El cultivo vertical multiplica la producción de un balcón pequeño aprovechando paredes, barandillas y estructuras en altura, sin necesitar más metros cuadrados. En esta sección verás cómo montar jardines verticales con palets, torres de cultivo e hidroponía casera, y qué plantas rinden mejor en cada sistema para sacar el máximo partido a un espacio reducido.',
    emoji: '🧱',
  },
  {
    slug: 'que-plantar',
    nombre: 'Qué Plantar',
    descripcion: 'Fichas de cultivo de hortalizas y aromáticas adaptadas a espacios pequeños.',
    intro:
      'No todas las hortalizas se comportan igual en una maceta que en el suelo de un huerto. En esta sección tienes fichas de cultivo detalladas de hortalizas, aromáticas y verduras adaptadas al balcón: qué maceta piden, cuánta luz necesitan, cómo se riegan y cuándo se cosechan. Elige cultivos agradecidos para tu espacio y tu nivel de sol, y acierta desde la primera siembra en lugar de aprender a base de decepciones.',
    emoji: '🥬',
  },
  {
    slug: 'frutales-en-maceta',
    nombre: 'Frutales en Maceta',
    descripcion: 'Frutales enanos y de maceta que sí puedes cultivar en una terraza.',
    intro:
      'Tener fruta propia en un balcón no es un imposible: con variedades enanas o de porte compacto, una maceta grande y sol suficiente, muchos frutales dan cosecha en terraza. En esta sección verás cuáles fructifican de verdad en maceta —de las fresas y frutos rojos a los cítricos enanos, la higuera o el granado— y cómo cuidarlos, podarlos y trasplantarlos para que produzcan año tras año.',
    emoji: '🍋',
  },
  {
    slug: 'calendario-de-siembra',
    nombre: 'Calendario de Siembra',
    descripcion: 'Qué sembrar cada mes del año según la estación.',
    intro:
      'Sembrar en su momento es una de las claves para no llevarse decepciones: cada cultivo tiene su ventana de temperatura, y adelantarse o retrasarse hace que germine mal o se suba a flor antes de producir. Aquí tienes qué sembrar, trasplantar y cosechar mes a mes en un huerto de balcón de clima mediterráneo, con guías específicas para cada mes del año y un calendario completo para planificar toda la temporada de un vistazo.',
    emoji: '📅',
  },
  {
    slug: 'plagas-y-enfermedades',
    nombre: 'Plagas y Enfermedades',
    descripcion: 'Diagnóstico y soluciones naturales para los problemas más comunes del huerto urbano.',
    intro:
      'Pulgón, mosca blanca, araña roja, oídio, hojas amarillas o frutos con manchas: tarde o temprano todo huerto de balcón se topa con algún problema. En esta sección te ayudamos a identificar qué le pasa a tu planta a partir de los síntomas y a resolverlo con soluciones naturales, sin recurrir a pesticidas agresivos. Diagnóstico claro, tratamientos ecológicos y prevención para que un susto no se convierta en la pérdida de la cosecha.',
    emoji: '🐛',
  },
  {
    slug: 'herramientas-y-comparativas',
    nombre: 'Herramientas y Comparativas',
    descripcion: 'Las mejores macetas, kits, sustratos y sistemas de riego, comparados.',
    intro:
      'Antes de comprar cualquier cosa para tu huerto, merece la pena saber en qué fijarse para no gastar de más ni quedarte corto. En esta sección comparamos macetas, sustratos, kits de principiante, sistemas de riego y herramientas básicas, explicando qué diferencia a unos de otros y cuál conviene según tu balcón y tu presupuesto. Recomendaciones honestas y prácticas para acertar a la primera con cada compra.',
    emoji: '🛠️',
  },
  {
    slug: 'compostaje-sostenibilidad',
    nombre: 'Compostaje y Sostenibilidad',
    descripcion: 'Compost casero y hábitos sostenibles para tu huerto en un piso sin jardín.',
    intro:
      'Un huerto urbano también es una forma de cerrar el círculo: convertir los restos de la cocina en abono en lugar de tirarlos a la basura. En esta sección te enseñamos a hacer compost casero incluso en un piso sin jardín —con vermicompostera o compostera de balcón—, a reutilizar y reciclar en el huerto y a adoptar hábitos más sostenibles que, de paso, reducen lo que gastas en sustrato y fertilizantes.',
    emoji: '♻️',
  },
];

export function getCategoria(slug: string): Categoria | undefined {
  return categorias.find((c) => c.slug === slug);
}

export function getCategoriaImagen(slug: string): string {
  return `/images/categorias/${slug}.jpg`;
}
