# Cómo contribuir

Gracias por ayudar a mantener el catálogo al día. Las fichas las leen dueños de pymes que van a tomar decisiones con ellas, así que cada dato tiene que poder comprobarse.

## Reglas de verificación

1. **Fuente primaria.** Cada dato nuevo o cambiado lleva una fuente primaria en `fuentes`: la documentación oficial del fabricante, su página de precios, su repositorio o directorio oficial de MCP, el registro del paquete (npm, PyPI) o, para normativa, el BOE y la sede de la AEAT. Blogs, comparadores y foros sirven de pista, no de prueba.
2. **Fecha.** Al revisar una ficha, pon `verificado_el` con la fecha de hoy en formato ISO (`2026-10-09`), aunque no cambie nada más.
3. **«No verificado».** Si no puedes confirmar algo en una fuente primaria, escríbelo con la etiqueta «no verificado». No inventes precios, fechas, nombres de paquetes ni URL. En los campos de valores cerrados (dificultad, `mcp.estado`, `api.existe`…), deja el valor que había y explica la duda en el texto.
4. **Esquema.** No añadas ni quites claves y respeta los valores permitidos de `datos/esquema.json`. El `id` no cambia nunca; si el producto cambia de nombre, añade el nombre nuevo a `alias`.
5. **Sin datos personales.** Este repositorio es público: nada de nombres de clientes, alumnos o empleados, correos ni teléfonos.
6. **Español claro.** Frases cortas, sin jerga innecesaria, con el mismo estilo que el resto de fichas.

## Pasos

1. Edita `datos/plataformas/<id>.json`, o crea uno nuevo copiando otro de la misma categoría.
2. Ejecuta `python3 scripts/validar.py` y corrige lo que diga.
3. Si quieres ver el resultado: `python3 scripts/construir.py` y abre `sitio/index.html`.
4. Abre un pull request que explique qué cambia, por qué y con qué fuente. Si el cambio es grande, añade un resumen en `datos/cambios/<fecha>.md`.

Al aceptar tu contribución, aceptas que los datos y las guías se publiquen bajo [CC BY 4.0](LICENSE-datos.md) y el código bajo [MIT](LICENSE).
