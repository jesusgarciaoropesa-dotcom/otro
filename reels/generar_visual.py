#!/usr/bin/env python3
"""
Carrusel de MiHuertoUrbano en ESTILO VISUAL (se intercala con el estilo de foto de siempre).

    python3 reels/generar_visual.py reels/config/<slug>-visual.json
    -> reels/salida/<slug>-carrusel/01.jpg … (1080x1350)

Las fotos siguen siendo las protagonistas, pero cada lámina ENSEÑA algo distinto con una pieza:
sello con el dato, comparación con dos fotos, filas con barras, pasos junto a una foto, recuadro
sobre la foto o tarjetas con foto. Todo el texto sale del artículo (nada inventado).

Tipos de lámina ("tipo"); "destacado" = palabras del título resaltadas:
  portada  {foto, titulo, destacado?, sello?:{arriba?, cifra, abajo?}, posicion?}
  versus   {titulo, destacado?, texto?, izquierda:{foto, titulo, items:[..], bien?:true}, derecha:{…}, conclusion?}
  filas    {titulo, destacado?, texto?, filas:[{grande, unidad?, barra? (0-100), linea?, detalle?, valor?, valor_pie?, destacar?}] (2-4), fuente?}
  pasos    {titulo, destacado?, foto, posicion?, pasos:[{titulo, texto?}] (3-5)}
  foto     {foto, posicion?, titulo, destacado?, texto?, recuadro?:{titulo, items:[..] (2-4)}}
  tarjetas {titulo, destacado?, tarjetas:[{foto, posicion?, etiqueta?, titulo, texto?}] (3-4)}
  cierre   {foto, titulo, destacado?, guardar?, palabra, palabra_texto?}
"""
import base64, html, json, mimetypes, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FONTS = REPO / "web/node_modules/@fontsource-variable"
PUBLIC = REPO / "web/public"
W, H = 1080, 1350


def e(t):
    return html.escape(str(t if t is not None else ""))


def uri(path: Path) -> str:
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def foto(valor: str) -> str:
    for cand in (PUBLIC / valor.lstrip("/"), PUBLIC / "images/articulos" / Path(valor).name, REPO / valor):
        if cand.exists():
            return uri(cand)
    sys.exit(f"ERROR: no encuentro la foto '{valor}'")


def dest(titulo, d, clase="dest"):
    t = e(titulo)
    if d and e(d) in t:
        t = t.replace(e(d), f'<span class="{clase}">{e(d)}</span>', 1)
    return t


def negrita(t):
    import re
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", e(t))


def fuente(nombre, archivo):
    return f"@font-face{{font-family:{nombre};src:url({uri(FONTS / archivo)}) format('woff2');font-weight:100 900}}"


CSS = """
:root{--hoja:#3f6b3a;--hojao:#24401f;--tierra:#a8562f;--mostaza:#d9a441;--crema:#faf3e6;--tinta:#1f2a1c}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;background:var(--crema);color:var(--tinta)}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.velo{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,30,18,.55) 0%,rgba(20,30,18,0) 28%,rgba(20,30,18,0) 48%,rgba(20,30,18,.88) 100%)}
.marca{position:absolute;top:52px;left:60px;font-family:Fraunces;font-weight:800;font-size:30px;color:var(--hojao);z-index:3}
.marca.cl{color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.4)}
.pag{position:absolute;top:56px;right:60px;font-size:24px;font-weight:700;background:rgba(255,255,255,.88);color:var(--hojao);padding:6px 16px;border-radius:20px;z-index:3}
h1,h2{font-family:Fraunces;font-weight:800;letter-spacing:-.02em;line-height:1.04}
h1{font-size:96px}h2{font-size:70px}
.dest{color:var(--mostaza)}
.caja{background:var(--mostaza);color:var(--hojao);padding:0 .16em;border-radius:14px;box-decoration-break:clone;-webkit-box-decoration-break:clone;white-space:nowrap}
.cab{position:absolute;left:60px;right:60px;top:125px}
.sub{font-size:33px;line-height:1.32;color:#4b5547;margin-top:18px}
.zona{position:absolute;left:60px;right:60px;top:var(--top,330px);bottom:120px;display:flex;flex-direction:column;justify-content:center;gap:22px}
.pie{position:absolute;bottom:46px;left:60px;right:60px;display:flex;justify-content:space-between;font-size:25px;font-weight:700;color:#7d8778}
.pie b{color:var(--hoja)}
.pie.cl{color:#dfe6d8}.pie.cl b{color:var(--mostaza)}
.chip{position:absolute;left:60px;bottom:56px;background:#fff;color:var(--hojao);border-radius:40px;padding:12px 26px;font-size:28px;font-weight:800;box-shadow:0 8px 24px rgba(0,0,0,.18)}
.sello{position:absolute;right:60px;top:170px;width:250px;height:250px;border-radius:50%;background:var(--mostaza);color:var(--hojao);display:grid;place-items:center;text-align:center;font-weight:800;transform:rotate(-10deg);box-shadow:0 18px 40px rgba(0,0,0,.3)}
.sello b{display:block;font-family:Fraunces;font-size:70px;line-height:.95}
.sello span{font-size:24px;line-height:1.15;display:block}
/* versus */
.vf{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.vf .c{background:#fff;border-radius:30px;overflow:hidden;box-shadow:0 14px 40px rgba(36,64,31,.14)}
.vf .im{height:420px;background-size:cover;background-position:center;position:relative}
.vf .mk{position:absolute;top:18px;left:18px;width:74px;height:74px;border-radius:50%;display:grid;place-items:center;font-size:44px;font-weight:900;color:#fff}
.vf .b{padding:26px 28px}
.vf h3{font-family:Fraunces;font-size:42px;line-height:1.05}
.vf ul{list-style:none;margin-top:14px;display:flex;flex-direction:column;gap:10px;font-size:28px;line-height:1.3;color:#4b5547}
.vf li::before{content:"·";font-weight:900;margin-right:10px;color:var(--hoja)}
.res{background:var(--hojao);color:#fff;border-radius:26px;padding:26px 32px;font-size:32px;font-weight:600;line-height:1.3}
.res b{color:var(--mostaza)}
/* filas */
.fila{display:grid;grid-template-columns:190px 1fr auto;align-items:center;gap:26px;background:#fff;border-radius:28px;padding:38px 34px;box-shadow:0 10px 30px rgba(36,64,31,.10)}
.fila.top{outline:5px solid var(--mostaza)}
.fila .g{font-family:Fraunces;font-size:74px;font-weight:800;line-height:1;color:var(--hojao)}
.fila .g small{font-family:Inter;font-size:22px;font-weight:700;color:#7d8778;display:block;margin-top:6px}
.barra{height:22px;border-radius:12px;background:#eee6d6;overflow:hidden}.barra i{display:block;height:100%;background:linear-gradient(90deg,#f1d68f,var(--mostaza))}
.fila .ln{font-size:27px;color:#7d8778;font-weight:600;margin-top:10px}
.fila .dt{font-size:28px;color:#4b5547;line-height:1.3;margin-top:6px}
.fila .v{text-align:right;font-family:Fraunces;font-size:56px;font-weight:800;color:var(--hoja);line-height:1;white-space:nowrap}
.fila .v small{display:block;font-family:Inter;font-size:21px;color:#7d8778;font-weight:700;margin-top:4px}
.fuente{position:absolute;left:60px;right:60px;bottom:100px;font-size:22px;color:#8a9285}
/* pasos */
.pf{display:grid;grid-template-columns:400px 1fr;gap:34px;height:100%}
.pf .im{border-radius:30px;background-size:cover;background-position:center;box-shadow:0 14px 40px rgba(36,64,31,.18)}
.pp{display:flex;flex-direction:column;justify-content:center;gap:26px}
.p{display:flex;gap:20px;align-items:flex-start}
.p .n{width:66px;height:66px;border-radius:50%;background:var(--hoja);color:#fff;font-family:Fraunces;font-weight:800;font-size:36px;display:grid;place-items:center;flex:none}
.p b{display:block;font-size:34px;line-height:1.15;color:var(--hojao);margin-top:8px}
.p span{display:block;font-size:26px;line-height:1.32;color:#55604f;margin-top:6px}
/* foto con recuadro */
.rec{position:absolute;left:60px;top:150px;max-width:640px;background:rgba(255,255,255,.95);border-radius:30px;padding:30px 34px;box-shadow:0 18px 40px rgba(0,0,0,.25);display:flex;flex-direction:column;gap:16px}
.rec p{font-size:22px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--tierra)}
.rec div{display:flex;gap:16px;align-items:center;font-size:31px;font-weight:700;color:var(--hojao);line-height:1.2}
.rec i{font-style:normal;width:50px;height:50px;border-radius:50%;background:var(--mostaza);display:grid;place-items:center;flex:none;font-family:Fraunces;font-weight:800}
.abajo{position:absolute;left:60px;right:60px;bottom:110px;color:#fff}
.abajo .sub{color:#eef2e8}
/* tarjetas */
.el{display:grid;grid-template-columns:210px 1fr;gap:26px;align-items:center;background:#fff;border-radius:28px;padding:16px;box-shadow:0 10px 30px rgba(36,64,31,.10)}
.el .im{height:190px;border-radius:20px;background-size:cover;background-position:center}
.el small{font-size:22px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--tierra)}
.el b{display:block;font-family:Fraunces;font-size:42px;line-height:1.05;color:var(--hojao);margin-top:4px}
.el span{display:block;font-size:28px;color:#55604f;margin-top:6px;line-height:1.25}
/* cierre */
.cta{position:absolute;left:60px;right:60px;bottom:120px;background:var(--mostaza);color:var(--hojao);border-radius:34px;padding:36px 40px}
.cta b{font-family:Fraunces;font-size:62px;display:block;line-height:1.05}
.cta span{font-size:30px;font-weight:600;display:block;margin-top:8px}
.guardar{position:absolute;left:60px;right:60px;bottom:390px;color:#fff;font-size:31px;font-weight:600;display:flex;gap:16px;align-items:center}
"""


def bgstyle(s, clave="foto", pos_clave="posicion"):
    return f"background-image:url({foto(s[clave])});background-position:{s.get(pos_clave, 'center')}"


def lamina(s, i, n, palabra_cfg):
    t = s.get("tipo")
    pag = f'<div class="pag">{i}/{n}</div>'
    sigue = f'<div class="pie"><span>Huerto en balcón</span><b>Sigue 👉</b></div>'
    if t == "portada":
        sello = ""
        if s.get("sello"):
            x = s["sello"]
            sello = f'<div class="sello"><div>{f"<span>{e(x.get("arriba"))}</span>" if x.get("arriba") else ""}<b>{e(x.get("cifra"))}</b>{f"<span>{e(x.get("abajo"))}</span>" if x.get("abajo") else ""}</div></div>'
        return f'''<div class="bg" style="{bgstyle(s)}"></div><div class="velo"></div><div class="marca cl">MiHuertoUrbano.xyz</div>{pag}{sello}
          <div style="position:absolute;left:60px;right:60px;bottom:150px"><h1 style="color:#fff;text-shadow:0 3px 16px rgba(0,0,0,.5)">{dest(s["titulo"], s.get("destacado"), "caja")}</h1></div>
          <div class="chip">Desliza 👉</div>'''
    if t == "cierre":
        pal = (s.get("palabra") or palabra_cfg or "").upper()
        return f'''<div class="bg" style="{bgstyle(s)}"></div><div class="velo" style="background:linear-gradient(180deg,rgba(20,30,18,.45),rgba(20,30,18,.25) 35%,rgba(20,30,18,.9))"></div>
          <div class="marca cl">MiHuertoUrbano.xyz</div>{pag}
          <div style="position:absolute;left:60px;right:60px;top:170px"><h1 style="color:#fff;font-size:88px;text-shadow:0 3px 16px rgba(0,0,0,.5)">{dest(s["titulo"], s.get("destacado"))}</h1></div>
          <div class="guardar"><span style="font-size:52px">🔖</span>{e(s.get("guardar") or "Guárdalo para cuando lo necesites")}</div>
          <div class="cta"><b>Comenta «{e(pal)}»</b><span>{e(s.get("palabra_texto") or "y te paso la guía completa por privado")}</span></div>'''
    if t == "foto":
        rec = ""
        if s.get("recuadro"):
            r = s["recuadro"]
            rec = f'<div class="rec"><p>{e(r.get("titulo"))}</p>' + "".join(f'<div><i>{k}</i>{e(x)}</div>' for k, x in enumerate(r.get("items", [])[:4], 1)) + "</div>"
        return f'''<div class="bg" style="{bgstyle(s)}"></div><div class="velo"></div><div class="marca cl">MiHuertoUrbano.xyz</div>{pag}{rec}
          <div class="abajo"><h2 style="color:#fff">{dest(s["titulo"], s.get("destacado"))}</h2>{f'<p class="sub">{e(s["texto"])}</p>' if s.get("texto") else ""}</div>
          <div class="pie cl"><span>Huerto en balcón</span><b>Sigue 👉</b></div>'''
    cab = f'<div class="cab"><h2>{dest(s["titulo"], s.get("destacado"))}</h2>{f"<p class=sub>{e(s.get("texto"))}</p>" if s.get("texto") else ""}</div>'
    top = 330 if s.get("texto") else 270
    if t == "versus":
        def col(c, bien):
            mk = '<span class="mk" style="background:#3f8a3a">✓</span>' if bien else '<span class="mk" style="background:#c0453a">✗</span>'
            return (f'<div class="c"><div class="im" style="{bgstyle(c)}">{mk}</div><div class="b"><h3>{e(c.get("titulo"))}</h3>'
                    f'<ul>{"".join(f"<li>{e(x)}</li>" for x in c.get("items", [])[:4])}</ul></div></div>')
        iz, de = s.get("izquierda", {}), s.get("derecha", {})
        cuerpo = f'<div class="vf">{col(iz, iz.get("bien", True))}{col(de, de.get("bien", False))}</div>'
        if s.get("conclusion"):
            cuerpo += f'<div class="res">{negrita(s["conclusion"])}</div>'
        return f'<div class="marca">MiHuertoUrbano.xyz</div>{pag}{cab}<div class="zona" style="--top:{top}px">{cuerpo}</div>{sigue}'
    if t == "filas":
        fs = ""
        for f in s.get("filas", [])[:4]:
            barra = f'<div class="barra"><i style="width:{max(0, min(100, float(f["barra"])))}%"></i></div>' if f.get("barra") is not None else ""
            fs += (f'<div class="fila{" top" if f.get("destacar") else ""}"><div class="g">{e(f.get("grande"))}{f"<small>{e(f.get("unidad"))}</small>" if f.get("unidad") else ""}</div>'
                   f'<div>{barra}{f"<p class=ln>{e(f.get("linea"))}</p>" if f.get("linea") else ""}{f"<p class=dt>{e(f.get("detalle"))}</p>" if f.get("detalle") else ""}</div>'
                   f'<div class="v">{e(f.get("valor"))}{f"<small>{e(f.get("valor_pie"))}</small>" if f.get("valor_pie") else ""}</div></div>')
        fu = f'<p class="fuente">{e(s["fuente"])}</p>' if s.get("fuente") else ""
        return f'<div class="marca">MiHuertoUrbano.xyz</div>{pag}{cab}<div class="zona" style="--top:{top}px">{fs}</div>{fu}{sigue}'
    if t == "pasos":
        ps = "".join(f'<div class="p"><span class="n">{k}</span><div><b>{e(p.get("titulo"))}</b>{f"<span>{e(p.get("texto"))}</span>" if p.get("texto") else ""}</div></div>'
                     for k, p in enumerate(s.get("pasos", [])[:5], 1))
        return f'<div class="marca">MiHuertoUrbano.xyz</div>{pag}{cab}<div class="zona" style="--top:{top}px;justify-content:stretch"><div class="pf"><div class="im" style="{bgstyle(s)}"></div><div class="pp">{ps}</div></div></div>{sigue}'
    if t == "tarjetas":
        ts = "".join(f'<div class="el"><div class="im" style="{bgstyle(c)}"></div><div>{f"<small>{e(c.get("etiqueta"))}</small>" if c.get("etiqueta") else ""}<b>{e(c.get("titulo"))}</b>{f"<span>{e(c.get("texto"))}</span>" if c.get("texto") else ""}</div></div>'
                     for c in s.get("tarjetas", [])[:4])
        return f'<div class="marca">MiHuertoUrbano.xyz</div>{pag}{cab}<div class="zona" style="--top:{top}px">{ts}</div>{sigue}'
    sys.exit(f"ERROR: tipo de lámina desconocido '{t}'")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    slides = cfg["slides"]
    if slides[0].get("tipo") != "portada" or slides[-1].get("tipo") != "cierre":
        sys.exit("La primera lámina tiene que ser 'portada' y la última 'cierre'")
    out = REPO / "reels/salida" / f"{cfg['slug']}-carrusel"
    out.mkdir(parents=True, exist_ok=True)
    css = fuente("Fraunces", "fraunces/files/fraunces-latin-full-normal.woff2") + fuente("Inter", "inter/files/inter-latin-wght-normal.woff2") + CSS
    from playwright.sync_api import sync_playwright
    avisos = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(slides, 1):
            pg.set_content(f"<html><head><meta charset='utf-8'><style>{css}</style></head><body><div class='s'>{lamina(s, i, len(slides), cfg.get('palabra'))}</div></body></html>")
            pg.wait_for_timeout(200)
            sale = pg.evaluate("""(() => { const z = document.querySelector('.zona'); const pie = document.querySelector('.pie');
              if (z && z.scrollHeight > z.clientHeight + 2) return true;
              const c = document.querySelector('.cab'); if (c && z && c.getBoundingClientRect().bottom > z.getBoundingClientRect().top + 4) return true;
              const ab = document.querySelector('.abajo, .rec'); if (ab && pie && document.querySelector('.abajo') && document.querySelector('.abajo').getBoundingClientRect().bottom > pie.getBoundingClientRect().top) return true;
              return false; })()""")
            if sale:
                avisos += 1
                print(f"AVISO: la lámina {i} ({s.get('tipo')}) tiene demasiado contenido; acórtala", file=sys.stderr)
            pg.screenshot(path=str(out / f"{i:02d}.jpg"), type="jpeg", quality=92)
        b.close()
    print(f"✅ Carrusel visual: {out} · {len(slides)} láminas · avisos: {avisos}")


if __name__ == "__main__":
    main()
