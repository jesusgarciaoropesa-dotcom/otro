# Descargables

- `calendario-siembra-balcon-interior.pdf`: guía-calendario de siembra en maceta para el interior peninsular
  (10 páginas: portada, cómo usarla y tipos de luz, clima del interior con heladas de AEMET Toledo,
  calendario anual de los 44 cultivos, mes a mes, los 10 más fáciles, diario de siembra y enlaces con QR).
  Se regala a cambio del correo (Brevo, lista "Calendario de siembra", doble confirmación) desde la caja
  `web/src/components/CalendarioDescarga.astro`. Al confirmar, Brevo abre
  `https://mihuertourbano.xyz/descargables/calendario-siembra-balcon-interior.pdf`.
- Se regenera con `python3 descargables/calendario/generar.py` (HTML + CSS con las fuentes y colores de la web,
  pasado a PDF con Chromium/Playwright; necesita `cd web && npm install` para las fuentes y `pip install qrcode`).
  Usa los datos de la calculadora `web/src/data/calculadora-cultivos.ts`: si cambian, el PDF cambia igual.
  El script deja la copia publicada en `web/public/descargables/`.
