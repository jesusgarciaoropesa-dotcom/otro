# Descargables

- `calendario-siembra-balcon-interior.pdf`: calendario de siembra en maceta para el interior peninsular (2 páginas), pensado para regalar a cambio del correo (newsletter).
  Se regenera con `python3 descargables/generar_calendario.py` (usa los datos de la calculadora `web/src/data/calculadora-cultivos.ts`, así que si cambian, el PDF cambia igual).
- Está fuera de `web/` a propósito: no se publica hasta tener el formulario de la newsletter (Brevo o MailerLite). Cuando esté, se sube el PDF al servicio de correo (o a `web/public/descargables/`) y se pone el formulario en la web.
