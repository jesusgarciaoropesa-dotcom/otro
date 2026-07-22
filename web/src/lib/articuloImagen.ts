/**
 * Extrae la primera imagen incrustada en el cuerpo de un artículo (la <figure>
 * que abre cada guía). Sirve para que las tarjetas de listado muestren la foto
 * real del artículo en vez de una imagen genérica de categoría.
 *
 * Devuelve la ruta tal cual aparece en el Markdown (p. ej. "/images/articulos/
 * culo-negro-tomate.jpg"), o `undefined` si el artículo no tiene ninguna imagen.
 */
const IMG_SRC_RE = /<img[^>]+src="([^"]+)"/;

export function primeraImagen(body?: string): string | undefined {
  if (!body) return undefined;
  const match = body.match(IMG_SRC_RE);
  return match?.[1];
}

/**
 * Imagen de tarjeta para un artículo: su foto propia si la tiene, y si no,
 * la imagen de la categoría como respaldo.
 */
export function imagenTarjeta(body: string | undefined, imagenCategoria: string): string {
  return primeraImagen(body) ?? imagenCategoria;
}
