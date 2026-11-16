// Después de construir la web: los enlaces a Amazon escritos en Markdown salen sin
// rel="sponsored". Google pide marcar así los enlaces de afiliado, así que aquí se les
// añade (y que se abran en otra pestaña), igual que los botones "Ver precio en Amazon".
import fs from 'node:fs';
import path from 'node:path';

const raiz = path.resolve('dist');
let archivos = 0, enlaces = 0;
const recorrer = (dir) => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const ruta = path.join(dir, e.name);
    if (e.isDirectory()) recorrer(ruta);
    else if (e.name.endsWith('.html')) {
      const antes = fs.readFileSync(ruta, 'utf-8');
      const despues = antes.replace(/<a\b([^>]*\bhref="https:\/\/www\.amazon\.es\/[^"]*"[^>]*)>/g, (m, attrs) => {
        if (/\brel=/.test(attrs)) return m;
        enlaces++;
        return `<a${attrs} target="_blank" rel="sponsored noopener">`;
      });
      if (despues !== antes) { fs.writeFileSync(ruta, despues); archivos++; }
    }
  }
};
recorrer(raiz);
console.log(`Enlaces de afiliado marcados: ${enlaces} en ${archivos} páginas`);
