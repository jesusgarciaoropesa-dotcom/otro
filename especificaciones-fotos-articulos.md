# Especificaciones de fotos para el interior de los artículos

Referencia para generar (con Gemini, ChatGPT/DALL-E o cualquier otra IA) las fotos que se van insertando poco a poco dentro del cuerpo de los artículos. El objetivo es que todas parezcan tomadas en el mismo balcón/terraza que ya aparece en el hero de la portada (`web/public/images/hero-huerto.jpg`), para dar sensación de continuidad y credibilidad.

## Método correcto: edición de imagen, no generación desde texto

Generar cada foto desde cero solo con una descripción de texto **no funciona** para mantener el mismo balcón: aunque el texto sea idéntico, el modelo no recuerda la escena anterior y reinterpreta libremente detalles como la posición del grifo, la pared o el fondo de edificios cada vez. Ya lo hemos comprobado con las dos primeras pruebas: aunque ambas seguían el mismo bloque de texto, la barandilla, la posición de los elementos y el perfil de la ciudad salieron distintos en cada una.

La solución es la misma que usamos para los carruseles de Canva: no regenerar la escena entera cada vez, sino partir siempre de **una única foto de referencia fija** y pedirle al modelo que la **edite**, cambiando solo el elemento en primer plano y dejando el resto de la imagen intacto.

Pasos a seguir:

1. **Elige una foto base** de las que ya tienes (puede ser directamente `hero-huerto.jpg`, o la primera prueba de plano general que generaste, la que más te guste) y guárdala aparte como "foto de referencia oficial del balcón".
2. **Adjunta esa foto de referencia como imagen de entrada** en el chat de Gemini (no solo la describas en texto: súbela como archivo cada vez que vayas a generar una foto nueva).
3. Usa un prompt de edición, no de generación, del tipo: "Edita esta imagen exacta. No cambies nada del entorno: mantén exactamente igual la barandilla, la pared de ladrillo con el jardín vertical, el grifo con el programador de riego, la mesa con las herramientas, el compostador y el fondo de edificios de la ciudad, tal y como están en la imagen adjunta. Lo único que quiero que cambies es [qué planta o elemento protagoniza el primer plano]. Mantén el mismo encuadre y la misma luz de la foto original."

## Cómo adaptar el prompt de edición a cada situación

Lo único que cambia entre una foto y otra es esta frase final:

- **Qué planta o elemento protagoniza el primer plano**: por ejemplo, "sustituye la planta en primer plano por una tomatera cargada de tomates cherry rojos, apoyada en un tutor de caña" o "en primer plano, una hoja de limonero con una larva de minador visible a contraluz".
- **Encuadre**: indica si quieres plano general del balcón (para fotos de portada de artículo) o un acercamiento/macro a una sola planta, hoja o plaga (para ilustrar un problema concreto dentro del texto). Si es un macro muy cerrado, puede que ya no se vea el resto del balcón, y no pasa nada.
- **Época del año, solo si es relevante para el contenido**: por defecto deja la luz cálida de atardecer de la foto de referencia; solo pide "cambia la luz a un tono más frío de invierno" si el artículo trata específicamente sobre cuidados de invierno.

## Bloque de estilo maestro (solo como respaldo, si alguna vez generas sin imagen de referencia)

Si por lo que sea tienes que generar una foto nueva desde texto puro sin poder adjuntar la imagen de referencia, usa este bloque como red de seguridad, sabiendo que el resultado será menos consistente que editando la foto de referencia:

"Fotografía realista, con aspecto de foto tomada con un móvil de gama alta, no una ilustración. El escenario es siempre el mismo balcón de un piso alto en una ciudad: suelo de tarima de madera oscura, barandilla de madera oscura maciza con balaustres metálicos verticales (no barrotes metálicos finos) a la izquierda del encuadre, y detrás de la barandilla una vista de fondo desenfocada de una ciudad (mezcla de edificios modernos altos y edificios más antiguos con tejados de teja), bajo un cielo despejado con luz cálida de atardecer. A la derecha del encuadre hay una pared de ladrillo visto de tono rojizo-anaranjado, con un jardín vertical instalado en ella (bolsillos de fieltro oscuro organizados en cuadrícula, llenos de aromáticas como albahaca, menta y orégano), un grifo exterior montado en la pared con un programador de riego por goteo conectado, y una pequeña mesa plegable de madera con herramientas de jardinería (pala pequeña, tijeras de podar, guantes, pulverizador) y un compostador pequeño de tapa verde oscura cerca. Hay macetas de terracota de distintos tamaños repartidas por el suelo de tarima, y una jardinera de barandilla con flores en el borde izquierdo. La luz es cálida, natural y brillante, viniendo de un lateral, con el cielo y el perfil de la ciudad ligeramente desenfocados al fondo. Ningún texto ni logotipo superpuesto en la imagen."

## Formato de archivo

- Proporción recomendada: 4:5 (vertical) o 16:9 (horizontal), según si la foto va en el cuerpo del texto o como imagen ancha entre dos secciones.
- Guarda cada foto en `web/public/images/articulos/<slug-del-articulo>/` con un nombre descriptivo (por ejemplo `tomatera-entutorada.jpg`).
- Al insertarla en el `.md`, usa este formato para que se aplique el estilo con bordes redondeados, sombra y pie de foto:

```html
<figure><img src="/images/articulos/<slug>/nombre-foto.jpg" alt="Descripción real de la foto" /><figcaption>Descripción breve que se lee bajo la foto</figcaption></figure>
```
