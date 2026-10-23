# Aurum Hair Studio — vista previa

Prototipo responsive basado en la imagen de referencia proporcionada. La página reproduce la dirección visual y mantiene texto, navegación, búsqueda y avisos de funciones futuras como elementos HTML accesibles. **No es todavía una tienda operativa**: no hay catálogo real, inventario, cuentas ni pagos.

## Vista previa local

Desde la carpeta del proyecto:

```powershell
& 'C:\Users\Jhon\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m http.server 8000
```

Abre `http://localhost:8000/`. También puede servirse con cualquier servidor estático.

## Publicar en GitHub Pages

El repositorio incluye `.github/workflows/pages.yml`. Al subir la rama `main`, abre **Settings → Pages → Build and deployment** y elige **GitHub Actions**. El flujo publica la carpeta raíz; la dirección final tendrá la forma `https://USUARIO.github.io/NOMBRE-REPOSITORIO/`. Los enlaces a recursos son relativos para funcionar bajo esa ruta.

## Imágenes y rendimiento

Las miniaturas se extrajeron de `design/reference.png`. La portada es una sola escena panorámica, creada a partir de la composición de referencia, con una versión WebP para escritorio y otra más pequeña para móvil. El archivo maestro está en `design/panorama-master.png`; la página solo descarga la versión correspondiente a la pantalla. Para regenerar los recursos:

El logo de `assets/aurum-logo-transparent.png` procede de `design/aurum-logo-original.png`, proporcionado por el usuario. Solo se retiró el fondo negro; se mantienen la forma y tipografía originales.

```powershell
& 'C:\Users\Jhon\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/optimize_images.py
```

El retrato principal se precarga porque aparece de inmediato. Las imágenes de las tarjetas usan `loading="lazy"` y `decoding="async"`. No hay frameworks, librerías, fuentes ni scripts externos. La captura original se conserva solo como material de diseño; la página no la descarga.

## Guía de desarrollo por fases

### Fase 1 — Base visual y técnica (esta entrega)

**Pilares:** identidad visual, diseño adaptable, accesibilidad, velocidad y despliegue reproducible. Definir tokens de color y tipografía, construir la portada, preparar imágenes WebP, documentar el proyecto y publicar una vista previa. **Criterio de cierre:** la portada se lee y navega correctamente en móvil y escritorio, sin errores de carga.

### Fase 2 — Catálogo real

Definir categorías, marcas, variantes, precios, disponibilidad e imágenes de producto. Diseñar fichas y listados con filtros y búsqueda. Sustituir las tarjetas ilustrativas actuales por datos verificados. **Criterio de cierre:** cada producto tiene información completa, fotografías optimizadas y un destino útil desde navegación y búsqueda.

### Fase 3 — Compra y confianza

Elegir plataforma o backend de comercio, integrar bolsa, checkout, pagos, costos de envío y políticas. Añadir cuentas solo si aportan valor. Revisar seguridad, privacidad y cumplimiento legal del mercado donde opere la tienda. **Criterio de cierre:** se puede completar una compra de prueba de extremo a extremo y se reflejan correctamente inventario y confirmaciones.

### Fase 4 — Optimización continua

Medir Core Web Vitals en dispositivos reales; optimizar imágenes por tamaño de pantalla, caché y carga diferida. Auditar accesibilidad, SEO, analítica y conversión. **Objetivos orientativos:** LCP menor de 2,5 s, INP menor de 200 ms y CLS menor de 0,1 en el percentil 75. Revisar resultados después de cada incorporación de contenido.

## Estructura

```text
index.html                 Portada semántica
styles.css                 Diseño y puntos de quiebre
script.js                  Menú, búsqueda y avisos
assets/                    Imágenes WebP y favicon
design/reference.png       Referencia original, fuera de la carga de la página
scripts/optimize_images.py Generador de imágenes ligeras
.github/workflows/pages.yml Publicación con GitHub Actions
```
