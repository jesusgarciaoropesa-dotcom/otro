# Guía del proyecto — MiHuertoUrbano

Web de nicho (blog) sobre **huerto urbano en balcón y terraza**, hecha con
**Astro + Tailwind + Pagefind**. Este archivo describe la forma de trabajar del
proyecto para que cualquier sesión de Claude Code lo entienda desde el principio.

> **Regla de oro:** lo que perdura es lo que se guarda (commit + push) en el
> repositorio. Los chats son temporales; el repositorio es la memoria del
> proyecto. Todo lo importante (contenido, método de reels, decisiones) debe
> quedar en archivos aquí, no solo en la conversación.

---

## Estructura del repositorio

- `web/` — el sitio Astro.
  - `web/src/content/articulos/*.md` — los artículos del blog (215+).
  - `web/src/pages/` — páginas (inicio, categorías, buscador, contacto, etc.).
  - `web/src/components/`, `web/src/layouts/` — plantillas y componentes.
  - `web/public/images/articulos/` — imágenes propias de los artículos.
  - `web/public/images/logo-full.png` — logo (regadera + ciudad).
- `reels/` — generador de reels para Instagram/Facebook (ver más abajo).
- `plan-nicho-huerto-urbano-balcon.md` — estrategia de negocio y de contenidos.
- `especificaciones-fotos-articulos.md` — guía para las fotos.

## Marca

- Colores (en `web/src/styles`): hoja `#3f6b3a`, hoja oscuro `#24401f`,
  tierra `#a8562f`, **mostaza/dorado `#d9a441`**, crema `#faf3e6`.
- Tipografías: **Fraunces** (titulares, serif) e **Inter** (texto).
- Tono: cercano, de tú, práctico. Nombre público: **MiHuertoUrbano**.
- Redes: Instagram `@mihuertourbano.xyz`, Facebook `MiHuertoUrbano`.

---

## Cómo añadir un artículo nuevo

1. Crea `web/src/content/articulos/<slug>.md`. El `<slug>` es la URL.
2. Frontmatter obligatorio (esquema en `web/src/content.config.ts`):

   ```yaml
   ---
   title: "Título del artículo"
   description: "Meta descripción para Google (~155 caracteres)."
   categoria: "que-plantar"        # ver lista de categorías abajo
   intencion: "informativa"        # informativa | transaccional | comparativa
   keywords: ["palabra clave 1", "palabra clave 2"]
   pubDate: 2026-09-02
   # opcionales:
   # updatedDate: 2026-09-10
   # pilar: true                   # true si es guía-pilar
   # faq:
   #   - pregunta: "..."
   #     respuesta: "..."
   ---
   ```

3. **Categorías válidas** (usar exactamente una de estas):
   `primeros-pasos`, `riego-automatico`, `cultivo-vertical`, `que-plantar`,
   `frutales-en-maceta`, `calendario-de-siembra`, `plagas-y-enfermedades`,
   `herramientas-y-comparativas`, `compostaje-sostenibilidad`.

4. Imágenes propias: guárdalas en `web/public/images/articulos/` y enlázalas
   con `<figure><img width="1200" height="670" src="/images/articulos/..."
   alt="..." /><figcaption>...</figcaption></figure>` (indicar width/height
   evita saltos de maquetación).

5. Comprueba que compila antes de publicar:

   ```bash
   cd web && npm install && npm run build
   ```

## Cómo hacer un reel para Instagram/Facebook

El método está en **`reels/COMO-HACER-REELS.md`**. Resumen:

```bash
cp reels/config/aguacate-riego.json reels/config/<nuevo>.json   # editar textos y foto
python3 reels/generar_reel.py reels/config/<nuevo>.json          # -> reels/salida/<nuevo>.mp4
```

Fórmula de 5 diapositivas: gancho → motivo → solución 1 → tranquiliza → CTA.

---

## Estilo de respuestas en grupos de Facebook

Cuando se responde a dudas en grupos (huerto/plantas):

- Tono cercano, de tú, experto pero sencillo. Nada de sonar a bot.
- **Máximo 2 emojis por comentario** (mejor 0-1). Nada de un emoji por línea.
- Para listas de pasos, usar **guiones** (`-`), no emojis como viñetas.
- Responder **útil primero**. En grupos ajenos, **no meter enlace** las primeras
  veces (parece spam); soltar el enlace solo si alguien pregunta o es el grupo propio.
- No corregir la especie de la planta de forma tajante en público; si hay duda,
  dar el truco para que la persona lo compruebe.
- No afirmar más de lo que se ve en una foto: si no se puede saber la causa exacta,
  decirlo y dar el manejo que sirve igualmente.

## Publicación (importante)

- El sitio se despliega solo con **GitHub Actions** (`.github/workflows/deploy-web.yml`)
  a la rama **`gh-pages`**, que es lo que sirve la web pública.
- El despliegue **solo se dispara al hacer push a la rama por defecto del repo
  (`claude/niche-website-monetization-t1fpxb`) o a `main`**, y solo si cambian
  archivos dentro de `web/`.
- Consecuencia: el trabajo hecho en otra rama (p. ej. una rama de sesión
  `claude/...`) **no se publica** hasta que se integra en la rama de despliegue.
  Para publicar cambios, hay que llevarlos a esa rama.

## Comandos útiles

```bash
cd web && npm run dev      # servidor local de desarrollo
cd web && npm run build    # compilar (incluye índice de búsqueda Pagefind)
```
