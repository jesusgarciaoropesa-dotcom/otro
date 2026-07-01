// Configuración central de afiliación. Cuando tengas tu cuenta de Amazon
// Afiliados (Amazon Associates), sustituye este valor por tu tag real
// (ej. "mihuertourbano-21") y todos los enlaces del sitio quedarán activos.
export const AMAZON_TAG = 'TU-TAG-AQUI-21';

/**
 * Genera una URL de búsqueda en Amazon España con el tag de afiliado ya
 * incluido, para usar como CTA en artículos de tipo comparativa/compra
 * ("Ver precio en Amazon") sin depender de un ASIN concreto por producto.
 */
export function amazonSearchUrl(query: string): string {
  const params = new URLSearchParams({ k: query, tag: AMAZON_TAG });
  return `https://www.amazon.es/s?${params.toString()}`;
}
