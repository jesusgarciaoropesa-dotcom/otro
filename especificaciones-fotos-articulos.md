# Especificaciones de fotos para el interior de los artículos

Referencia para generar (con Gemini, ChatGPT/DALL-E o cualquier otra IA) las fotos que se van insertando poco a poco dentro del cuerpo de los artículos. El objetivo es que todas parezcan tomadas en el mismo balcón/terraza que ya aparece en el hero de la portada (`web/public/images/hero-huerto.jpg`), para dar sensación de continuidad y credibilidad.

## Bloque de estilo maestro (copiar siempre, tal cual, en cada prompt)

"Fotografía realista, con aspecto de foto tomada con un móvil de gama alta, no una ilustración. El escenario es siempre el mismo balcón de un piso alto en una ciudad: suelo de tarima de madera oscura, barandilla de madera oscura con balaustres metálicos oscuros a la izquierda del encuadre, y detrás de la barandilla una vista de fondo desenfocada de una ciudad (mezcla de edificios modernos altos y edificios más antiguos con tejados de teja), bajo un cielo despejado con luz cálida de atardecer. A la derecha del encuadre hay una pared de ladrillo visto de tono rojizo-anaranjado, con un jardín vertical instalado en ella (bolsillos de fieltro oscuro organizados en cuadrícula, llenos de aromáticas como albahaca, menta y orégano), un grifo exterior montado en la pared con un programador de riego por goteo conectado, y una pequeña mesa plegable de madera con herramientas de jardinería (pala pequeña, tijeras de podar, guantes, pulverizador) y un compostador pequeño de tapa verde oscura cerca. Hay macetas de terracota de distintos tamaños repartidas por el suelo de tarima, y una jardinera de barandilla con flores en el borde izquierdo. La luz es cálida, natural y brillante, viniendo de un lateral, con el cielo y el perfil de la ciudad ligeramente desenfocados al fondo. Ningún texto ni logotipo superpuesto en la imagen."

## Cómo adaptar el bloque a cada situación

Después de pegar el bloque de estilo maestro completo (nunca resumido ni abreviado), añade a continuación qué cambia en esa foto en concreto:

- **Qué planta o elemento protagoniza el primer plano**: por ejemplo, "en primer plano, ocupando la mayor parte del encuadre, una tomatera cargada de tomates cherry rojos, apoyada en un tutor de caña" o "en primer plano, una hoja de limonero con una larva de minador visible a contraluz".
- **Encuadre**: indica si quieres plano general del balcón (para fotos de portada de artículo) o primer plano/macro de una sola planta, hoja o plaga (para ilustrar un problema concreto dentro del texto).
- **Época del año, solo si es relevante para el contenido**: por defecto deja la luz cálida de atardecer de siempre; solo cambia a "luz de invierno más fría y baja" si el artículo trata específicamente sobre cuidados de invierno.

No cambies nunca: el suelo de tarima oscura, la barandilla de madera con balaustres metálicos, la pared de ladrillo con el jardín vertical, el grifo con programador de riego, la mesa con herramientas y el compostador, ni el estilo de luz cálida de atardecer. Son los elementos que hacen que todas las fotos parezcan del mismo balcón real.

## Formato de archivo

- Proporción recomendada: 4:5 (vertical) o 16:9 (horizontal), según si la foto va en el cuerpo del texto o como imagen ancha entre dos secciones.
- Guarda cada foto en `web/public/images/articulos/<slug-del-articulo>/` con un nombre descriptivo (por ejemplo `tomatera-entutorada.jpg`).
- Al insertarla en el `.md`, usa este formato para que se aplique el estilo con bordes redondeados, sombra y pie de foto:

```html
<figure><img src="/images/articulos/<slug>/nombre-foto.jpg" alt="Descripción real de la foto" /><figcaption>Descripción breve que se lee bajo la foto</figcaption></figure>
```
