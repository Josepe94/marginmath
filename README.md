# Web de calculadoras en inglés (MarginMath, nombre provisional)

Web estática con 6 calculadoras para pequeñas empresas, freelancers y fundadores SaaS: margen, markup, tarifa freelance, punto de equilibrio, LTV:CAC y subida de precios. Gana dinero con **afiliados SaaS** y, más adelante, con **anuncios**. Coste: 0 € (o unos 10 €/año con dominio propio).

Cada calculadora incluye fórmula, ejemplo resuelto, preguntas frecuentes con datos estructurados (FAQ schema), enlaces internos y bloque de afiliado. Todo funciona en el navegador: sin servidor, sin cookies, sin mantenimiento técnico.

## Publicar (15 minutos)

1. GitHub → *New repository* → público → nombre `marginmath` (o tu marca).
2. Sube **todo el contenido de esta carpeta** (incluida `docs/`).
3. *Settings → Pages* → Source: *Deploy from a branch* → rama `main`, carpeta **`/docs`** → Save.
4. En 1-2 minutos estará en `https://TU_USUARIO.github.io/marginmath/`.
5. Abre `build.py`, cambia `base_url` por esa dirección y rellena `owner_name`, `owner_nif` y `contact_email` (el aviso legal lo exige la LSSI). Ejecuta `python3 build.py` y vuelve a subir `docs/`. O pídeselo a Claude.
6. **Google Search Console** (gratis): añade la propiedad, verifica con la etiqueta meta (campo `google_site_verification` de `build.py`) y envía `sitemap.xml`.

**Dominio propio (recomendado, ~10 €/año):** posiciona mejor que un subdominio de github.io y te lo llevas si cambias de hosting. Cómpralo, ponlo en *Settings → Pages → Custom domain* y actualiza `base_url`.

## Afiliados (solicitar cuando la web esté publicada)

Rellena la `url` de cada oferta en `build.py`. Las ofertas sin URL no se muestran, así que nunca hay enlaces rotos.

| Hueco en la web | Dónde aparece | Programas candidatos |
|---|---|---|
| `accounting` | Margen, punto de equilibrio | Software de contabilidad con programa de afiliados (p. ej. FreshBooks, QuickBooks) |
| `invoicing` | Markup, tarifa freelance | Facturación para freelancers |
| `crm` | Subida de precios | HubSpot (30 % hasta 12 meses, cookie de 180 días) |
| `analytics` | LTV:CAC | Analítica SaaS (Baremetrics, ChartMogul…) |
| `email` | Reserva | Kit (30 % durante 24 meses) |

Comprueba las condiciones actuales de cada programa antes de solicitarlo; cambian a menudo.

**Anuncios:** cuando Search Console muestre unas 1.000 sesiones al mes de EE. UU., Reino Unido, Canadá o Australia, solicita Journey by Mediavine (o AdSense antes). Antes de activar anuncios hay que añadir un banner de consentimiento de cookies y actualizar la política de privacidad.

## Crecer sin calentarse la cabeza

- **Regla de calidad:** 1-2 calculadoras nuevas al mes como máximo, cada una con fórmula, ejemplo y FAQ. Nada de cientos de páginas generadas (Google lo penaliza).
- **Ideas para las siguientes**, en orden: CAC payback, burn rate y runway, MRR growth, discount, gross vs net revenue, invoice late fee y sales commission.
- **Tarea programada mensual** (te la puedo configurar): Claude lee el informe de Search Console que exportes, detecta búsquedas sin calculadora y te propone la siguiente ya construida.
- **Regla de corte:** si a los 6 meses no llega a 100 clics/mes en Search Console, se reconsidera el nicho.

## Archivos

- `build.py`: configuración (marca, URL, afiliados, datos legales) y contenido de las páginas.
- `assets/`: estilos, lógica de las calculadoras y favicon.
- `docs/`: la web generada (lo que publica GitHub Pages).
- `test/calc.test.js`: comprueba cada calculadora contra los ejemplos publicados (`node test/calc.test.js`).
