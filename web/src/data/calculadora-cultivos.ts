// Datos para la calculadora "¿Qué puedo plantar en mi balcón?".
// - luz: mínimo de sol que necesita el cultivo. 'pleno' = necesita 6h+ de sol;
//   'media' = se apaña con 3-5h o sol de media jornada; 'sombra' = tolera poca luz.
//   Un balcón con mucho sol puede con todo; uno de sombra solo con los de 'sombra'.
// - meses: meses recomendados de siembra o plantación (clima mediterráneo/España;
//   ajustar 2-3 semanas según zona). 1 = enero ... 12 = diciembre.
// - familia: familia botánica. Sirve para la compatibilidad: no conviene juntar
//   cultivos de la misma familia (agotan lo mismo y comparten plagas).
// - facil: apto para principiantes (rápido, resistente y poco exigente).
// - dias: días orientativos desde la siembra/plantación hasta la cosecha (omitido
//   en frutales y perennes, que tardan meses o años).
// - buenas: cultivos con los que se lleva bien (asociación favorable).
// - slug: enlaza a la ficha de cultivo correspondiente.

export type NivelLuz = 'pleno' | 'media' | 'sombra';
export type TipoCultivo = 'hortaliza' | 'hoja' | 'raiz' | 'aromatica' | 'fruta';

export interface Cultivo {
  nombre: string;
  slug: string;
  luz: NivelLuz;
  tipo: TipoCultivo;
  meses: number[];
  familia: string;
  facil: boolean;
  dias?: number;
  buenas?: string[];
  nota: string;
}

export const cultivos: Cultivo[] = [
  // Hortalizas de fruto (mucho sol)
  { nombre: 'Tomate cherry', slug: 'como-cultivar-tomates-en-maceta-balcon', luz: 'pleno', tipo: 'hortaliza', meses: [2, 3, 4, 5], familia: 'Solanáceas', facil: true, dias: 90, buenas: ['Albahaca', 'Zanahorias', 'Lechuga', 'Cebollas'], nota: 'Necesita mucho sol y un buen tutor.' },
  { nombre: 'Pimiento', slug: 'como-cultivar-pimientos-en-maceta', luz: 'pleno', tipo: 'hortaliza', meses: [2, 3, 4], familia: 'Solanáceas', facil: false, dias: 110, buenas: ['Albahaca', 'Zanahorias', 'Cebollas'], nota: 'De semillero a principios de año, a pleno sol.' },
  { nombre: 'Berenjena', slug: 'como-cultivar-berenjenas-en-maceta', luz: 'pleno', tipo: 'hortaliza', meses: [2, 3, 4], familia: 'Solanáceas', facil: false, dias: 110, buenas: ['Judías verdes', 'Albahaca'], nota: 'Cultivo de calor, quiere sol y maceta grande.' },
  { nombre: 'Pepino', slug: 'como-cultivar-pepinos-huerto-vertical', luz: 'pleno', tipo: 'hortaliza', meses: [4, 5], familia: 'Cucurbitáceas', facil: true, dias: 60, buenas: ['Judías verdes', 'Lechuga', 'Eneldo'], nota: 'Trepadora: aprovéchala en vertical.' },
  { nombre: 'Calabacín', slug: 'como-cultivar-calabacines-espacio-reducido', luz: 'pleno', tipo: 'hortaliza', meses: [4, 5], familia: 'Cucurbitáceas', facil: true, dias: 55, buenas: ['Judías verdes', 'Albahaca'], nota: 'Ocupa bastante; una maceta grande por planta.' },
  { nombre: 'Judías verdes', slug: 'como-cultivar-judias-verdes-en-maceta', luz: 'pleno', tipo: 'hortaliza', meses: [5, 6, 7], familia: 'Leguminosas', facil: true, dias: 60, buenas: ['Zanahorias', 'Pepino', 'Lechuga', 'Fresas'], nota: 'Siembra directa con la tierra ya templada.' },

  // Hojas (toleran menos sol)
  { nombre: 'Lechuga', slug: 'como-cultivar-lechugas-huerto-urbano', luz: 'media', tipo: 'hoja', meses: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], familia: 'Compuestas', facil: true, dias: 55, buenas: ['Zanahorias', 'Rabanitos', 'Fresas'], nota: 'Cosecha hoja a hoja; tolera media sombra.' },
  { nombre: 'Espinacas', slug: 'como-cultivar-espinacas-en-maceta', luz: 'sombra', tipo: 'hoja', meses: [2, 3, 8, 9, 10], familia: 'Quenopodiáceas', facil: true, dias: 50, buenas: ['Fresas', 'Lechuga'], nota: 'Cultivo de frío que aguanta poca luz.' },
  { nombre: 'Acelgas', slug: 'como-cultivar-acelgas-en-maceta', luz: 'media', tipo: 'hoja', meses: [2, 3, 4, 8, 9], familia: 'Quenopodiáceas', facil: true, dias: 60, buenas: ['Cebollas', 'Zanahorias'], nota: 'Muy productiva y resistente.' },
  { nombre: 'Kale (col rizada)', slug: 'como-cultivar-kale-col-rizada-en-maceta', luz: 'media', tipo: 'hoja', meses: [2, 3, 8, 9], familia: 'Brásicas', facil: true, dias: 60, buenas: ['Cebollas', 'Remolacha', 'Aromáticas'], nota: 'Mejora de sabor con el frío.' },
  { nombre: 'Rúcula', slug: 'mejores-hortalizas-para-balcones-pequenos', luz: 'media', tipo: 'hoja', meses: [3, 4, 5, 8, 9, 10], familia: 'Brásicas', facil: true, dias: 40, buenas: ['Lechuga', 'Zanahorias'], nota: 'Ciclo corto, ideal para ir cortando.' },
  { nombre: 'Canónigos', slug: 'como-cultivar-canonigos-en-maceta', luz: 'media', tipo: 'hoja', meses: [8, 9, 10, 11], familia: 'Valerianáceas', facil: true, dias: 55, buenas: ['Lechuga', 'Rabanitos'], nota: 'De frío; resiste como pocas y va en poco fondo.' },
  { nombre: 'Escarola', slug: 'como-cultivar-escarola-en-maceta', luz: 'media', tipo: 'hoja', meses: [8, 9, 10], familia: 'Compuestas', facil: true, dias: 90, buenas: ['Zanahorias', 'Cebollas'], nota: 'De otoño; blanquea el centro para quitar amargor.' },

  // Raíces
  { nombre: 'Rabanitos', slug: 'como-cultivar-rabanitos-en-balcon', luz: 'media', tipo: 'raiz', meses: [3, 4, 5, 6, 7, 8, 9, 10], familia: 'Brásicas', facil: true, dias: 28, buenas: ['Lechuga', 'Zanahorias', 'Pepino'], nota: 'El más rápido: listo en 3-4 semanas.' },
  { nombre: 'Zanahorias', slug: 'como-cultivar-zanahorias-en-maceta', luz: 'media', tipo: 'raiz', meses: [2, 3, 4, 5, 6, 7, 8, 9], familia: 'Umbelíferas', facil: true, dias: 90, buenas: ['Cebollas', 'Puerros', 'Lechuga', 'Rabanitos'], nota: 'Necesita maceta honda.' },
  { nombre: 'Ajos', slug: 'como-cultivar-ajos-en-maceta', luz: 'pleno', tipo: 'raiz', meses: [10, 11, 12], familia: 'Liliáceas', facil: true, dias: 240, buenas: ['Zanahorias', 'Lechuga', 'Fresas', 'Tomate cherry'], nota: 'Se plantan los dientes en otoño.' },
  { nombre: 'Cebollas', slug: 'como-cultivar-cebollas-en-maceta', luz: 'pleno', tipo: 'raiz', meses: [1, 2, 3], familia: 'Liliáceas', facil: true, dias: 150, buenas: ['Zanahorias', 'Lechuga', 'Remolacha'], nota: 'Más fácil desde bulbito que desde semilla.' },
  { nombre: 'Patatas en saco', slug: 'como-cultivar-patatas-en-saco-balcon', luz: 'pleno', tipo: 'raiz', meses: [2, 3, 4], familia: 'Solanáceas', facil: true, dias: 100, buenas: ['Judías verdes', 'Lechuga'], nota: 'En saco de cultivo, aporcando a medida que crece.' },
  { nombre: 'Remolacha', slug: 'como-cultivar-remolacha-en-maceta', luz: 'media', tipo: 'raiz', meses: [3, 4, 5, 8, 9, 10], familia: 'Quenopodiáceas', facil: true, dias: 75, buenas: ['Cebollas', 'Lechuga'], nota: 'Aclara las plántulas; sus hojas también se comen.' },
  { nombre: 'Guisantes', slug: 'como-cultivar-guisantes-en-maceta', luz: 'media', tipo: 'hortaliza', meses: [1, 2, 10, 11], familia: 'Leguminosas', facil: true, dias: 90, buenas: ['Zanahorias', 'Rabanitos'], nota: 'Cultivo de clima fresco, trepa por una caña.' },
  { nombre: 'Brócoli', slug: 'como-cultivar-brocoli-en-maceta', luz: 'media', tipo: 'hortaliza', meses: [2, 8, 9], familia: 'Brásicas', facil: true, dias: 90, buenas: ['Cebollas', 'Remolacha', 'Aromáticas'], nota: 'De otoño-invierno; da rebrotes tras la pella.' },
  { nombre: 'Coliflor', slug: 'como-cultivar-coliflor-en-maceta', luz: 'media', tipo: 'hortaliza', meses: [7, 8, 9], familia: 'Brásicas', facil: false, dias: 100, buenas: ['Cebollas', 'Remolacha', 'Aromáticas'], nota: 'De otoño-invierno; quiere maceta grande y riego constante.' },
  { nombre: 'Puerros', slug: 'como-cultivar-puerros-en-maceta', luz: 'pleno', tipo: 'hortaliza', meses: [2, 3, 4], familia: 'Liliáceas', facil: false, dias: 150, buenas: ['Zanahorias', 'Cebollas'], nota: 'Ciclo largo; aporca el tallo para el fuste blanco.' },
  { nombre: 'Guindillas y chiles', slug: 'como-cultivar-guindillas-chiles-en-maceta', luz: 'pleno', tipo: 'hortaliza', meses: [2, 3, 4], familia: 'Solanáceas', facil: false, dias: 110, buenas: ['Albahaca', 'Zanahorias'], nota: 'De semillero a principios de año, a pleno sol y calor.' },
  { nombre: 'Apio', slug: 'como-cultivar-apio-en-maceta', luz: 'media', tipo: 'hortaliza', meses: [3, 4, 5], familia: 'Umbelíferas', facil: false, dias: 130, buenas: ['Puerros', 'Tomate cherry'], nota: 'Exigente en agua: riego constante para tallos tiernos.' },

  // Aromáticas
  { nombre: 'Albahaca', slug: 'como-cultivar-albahaca-en-maceta', luz: 'pleno', tipo: 'aromatica', meses: [4, 5, 6], familia: 'Labiadas', facil: true, dias: 60, buenas: ['Tomate cherry', 'Pimiento'], nota: 'De calor; pinza las flores para que siga dando hoja.' },
  { nombre: 'Perejil', slug: 'como-cultivar-perejil-en-maceta', luz: 'sombra', tipo: 'aromatica', meses: [3, 4, 5, 6, 7, 9], familia: 'Umbelíferas', facil: true, dias: 70, buenas: ['Tomate cherry'], nota: 'Tolera bien la media sombra.' },
  { nombre: 'Cilantro', slug: 'como-cultivar-cilantro-en-maceta', luz: 'media', tipo: 'aromatica', meses: [3, 4, 9], familia: 'Umbelíferas', facil: false, dias: 45, buenas: ['Espinacas'], nota: 'Con calor florece y pierde sabor.' },
  { nombre: 'Menta', slug: 'como-cultivar-menta-en-maceta', luz: 'sombra', tipo: 'aromatica', meses: [3, 4, 5, 9], familia: 'Labiadas', facil: true, nota: 'Siempre en maceta individual: es invasiva.' },
  { nombre: 'Cebollino', slug: 'como-cultivar-cebollino-en-maceta', luz: 'media', tipo: 'aromatica', meses: [3, 4, 9], familia: 'Liliáceas', facil: true, dias: 80, buenas: ['Zanahorias', 'Fresas'], nota: 'Se corta y rebrota una y otra vez.' },
  { nombre: 'Romero', slug: 'como-cultivar-romero-en-balcon', luz: 'pleno', tipo: 'aromatica', meses: [4, 5], familia: 'Labiadas', facil: true, buenas: ['Kale (col rizada)', 'Brócoli'], nota: 'Casi imposible de matar; sol y poco riego.' },
  { nombre: 'Tomillo', slug: 'como-cultivar-tomillo-en-maceta', luz: 'pleno', tipo: 'aromatica', meses: [4, 5], familia: 'Labiadas', facil: true, buenas: ['Kale (col rizada)', 'Brócoli'], nota: 'Mediterránea, resiste sol y sequía.' },
  { nombre: 'Orégano', slug: 'como-cultivar-oregano-en-maceta', luz: 'pleno', tipo: 'aromatica', meses: [4, 5], familia: 'Labiadas', facil: true, nota: 'Muy resistente; se seca fácil para conservar.' },
  { nombre: 'Laurel', slug: 'como-cultivar-laurel-en-maceta', luz: 'media', tipo: 'aromatica', meses: [3, 4], familia: 'Lauráceas', facil: true, nota: 'Arbusto longevo y de muy bajo mantenimiento.' },
  { nombre: 'Salvia', slug: 'como-cultivar-salvia-en-maceta', luz: 'pleno', tipo: 'aromatica', meses: [4, 5], familia: 'Labiadas', facil: true, buenas: ['Kale (col rizada)', 'Brócoli'], nota: 'Mediterránea de sol y poca agua; pódala en primavera.' },
  { nombre: 'Eneldo', slug: 'como-cultivar-eneldo-en-maceta', luz: 'pleno', tipo: 'aromatica', meses: [3, 4, 5, 9], familia: 'Umbelíferas', facil: true, dias: 55, buenas: ['Pepino', 'Lechuga'], nota: 'Siembra directa: hace raíz pivotante y odia el trasplante.' },
  { nombre: 'Manzanilla', slug: 'como-cultivar-manzanilla-en-maceta', luz: 'pleno', tipo: 'aromatica', meses: [3, 4, 5], familia: 'Compuestas', facil: true, dias: 70, nota: 'Rústica; sus flores se secan para infusión y atraen polinizadores.' },

  // Frutas
  { nombre: 'Fresas', slug: 'como-cultivar-fresas-en-balcon', luz: 'media', tipo: 'fruta', meses: [2, 3, 9, 10], familia: 'Rosáceas', facil: true, buenas: ['Lechuga', 'Espinacas', 'Ajos', 'Cebollino'], nota: 'Perfectas para cultivo vertical.' },
  { nombre: 'Frambuesas y moras', slug: 'como-cultivar-frambuesas-moras-en-maceta', luz: 'media', tipo: 'fruta', meses: [11, 12, 1, 2], familia: 'Rosáceas', facil: true, nota: 'Se plantan en reposo, en maceta grande.' },
  { nombre: 'Arándanos', slug: 'como-cultivar-arandanos-en-maceta', luz: 'media', tipo: 'fruta', meses: [11, 12, 1, 2], familia: 'Ericáceas', facil: false, nota: 'Necesita sustrato ácido y agua sin cal.' },
  { nombre: 'Limonero enano', slug: 'como-cultivar-limonero-en-maceta', luz: 'pleno', tipo: 'fruta', meses: [3, 4, 5], familia: 'Rutáceas', facil: false, nota: 'Frutal de maceta que sí da fruto en balcón.' },
  { nombre: 'Naranjo enano', slug: 'como-cultivar-naranjo-enano-en-maceta', luz: 'pleno', tipo: 'fruta', meses: [3, 4, 5], familia: 'Rutáceas', facil: false, nota: 'Cítrico compacto para terraza soleada.' },
  { nombre: 'Uva (parra)', slug: 'como-cultivar-uva-parra-en-maceta', luz: 'pleno', tipo: 'fruta', meses: [11, 12, 1, 2], familia: 'Vitáceas', facil: false, nota: 'Se planta en reposo; da sombra y racimos en terraza soleada.' },
  { nombre: 'Kiwi', slug: 'como-cultivar-kiwi-en-maceta', luz: 'pleno', tipo: 'fruta', meses: [11, 12, 1, 2], familia: 'Actinidiáceas', facil: false, nota: 'Trepadora vigorosa; elige variedad autofértil para balcón.' },
];

export const meses = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre',
];
