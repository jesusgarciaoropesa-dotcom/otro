# Fotos pendientes — lista de seguimiento

Checklist de trabajo para ir sustituyendo fotos "prestadas" (compartidas entre
varios artículos) por fotos propias del mismo estilo. Complementa la estrategia
de `especificaciones-fotos-articulos.md`.

## Cómo trabajamos las fotos

1. Claude da los **prompts** (uno por artículo).
2. Tú las generas (Gemini / ChatGPT-DALL·E / la IA que uses) y las mandas al chat.
3. Claude las procesa: recorte a **1200×670 + logo**, las guarda en
   `web/public/images/articulos/` y actualiza `src`, `alt` y pie en el artículo.

**Regla de estilo** (añadir al final de cada prompt):
> Fotografía realista estilo móvil, luz natural suave, balcón urbano mediterráneo,
> muy detallada, colores naturales, sin texto ni marcas de agua. Formato horizontal.

---

## ✅ Hechas (sesión anterior)

- [x] Hojas del aguacate marrones
- [x] Habas en maceta
- [x] Rúcula en maceta
- [x] Repollo / col en maceta
- [x] Destallar la tomatera (el chupón)
- [x] Tamaño de maceta por hortaliza
- [x] Semillas que no germinan

## 🔴 Tanda 1 — prioritarias (prompts ya dados)

- [ ] `brocoli-coliflor-no-forma-cabeza` — brócoli espigado sin cabeza formada
- [ ] `proteger-huerto-calor-extremo-verano` — malla de sombreo en verano
- [ ] `atraer-polinizadores-balcon` — abeja en flor de calabacín (macro)
- [ ] `acolchado-mulching-huerto-balcon` — tierra cubierta con acolchado de paja
- [ ] `reutilizar-restos-cocina-abonar-huerto` — restos de cocina para compost (cenital)
- [ ] `test-germinacion-semillas-viejas` — semillas germinando en servilleta húmeda
- [ ] `como-prevenir-plagas-huerto-urbano-sin-pesticidas` — trampa amarilla + repelente
- [ ] `errores-comunes-empezar-huerto-urbano` — planta sana vs. planta mustia

## 🟡 Próximas tandas (candidatas, pedir prompts cuando toque)

Artículos con foto prestada y tema concreto que se beneficiarían de foto propia:

- [ ] `oidio-huerto-urbano-como-eliminarlo` — hoja con oídio (polvo blanco) en primer plano
- [ ] `manchas-blancas-hojas-plantas-que-son` — comparativa de manchas blancas en hoja
- [ ] `como-revivir-planta-marchita-maceta` — planta muy mustia siendo recuperada
- [ ] `como-cambiar-planta-a-maceta-mas-grande` — trasplante a maceta mayor, cepellón visible
- [ ] `como-hacer-sustrato-casero-macetas` — mezcla de sustrato con las manos
- [ ] `reutilizar-tierra-macetas-regenerar-sustrato` — tierra vieja siendo cribada/regenerada
- [ ] `cada-cuanto-abonar-huerto-maceta` — aplicar abono a una maceta
- [ ] `patatas-saco-balcon` (owner) vs `mejores-sacos-cultivo-grow-bags-balcon` — patatas en saco
- [ ] `atraer-polinizadores-balcon` ya en tanda 1

> Nota: muchos otros artículos comparten foto pero son **resúmenes mensuales**
> ("qué plantar en junio/julio…") o comparativas donde reutilizar una foto
> representativa es aceptable; no es prioritario cambiarlas.
