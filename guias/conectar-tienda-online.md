---
type: article
title: Conectar tu tienda online, tus marketplaces y tus envíos
description: Cómo dar a tu agente acceso de solo lectura a pedidos, productos, clientes, pagos y envíos (Shopify, PrestaShop, WooCommerce, marketplaces, Stripe, Redsys, PayPal y transportistas) y cuándo escribir con aprobación.
tags: [guia-alumnos, ecommerce, shopify, prestashop, woocommerce, marketplaces, pagos, envios, rgpd]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Conectar tu tienda online, tus marketplaces y tus envíos

> Para: dueños y equipos de comercio y ecommerce, sin necesidad de saber programar.
> Qué conseguirás: que tu agente lea pedidos, stock, pagos y envíos por ti (resumen del lunes, conciliación) y que solo cambie precios o fichas cuando tú lo apruebes.

## En resumen
Una tienda online son cuatro cajones: **catálogo** (productos y stock), **pedidos y clientes**, **cobros** (Stripe, Redsys, PayPal) y **envíos** (transportistas). Cada cajón tiene su propia llave. Esta guía te dice cuál usar y con qué permisos. Para entender los términos (MCP, API, clave), mira [MCP, API y demás sin tecnicismos](./mcp-api-y-demas-sin-tecnicismos.md). Para el método general, [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md).

- **Tiempo:** 15-30 minutos por plataforma si eres tú quien administra la tienda. Amazon, TikTok Shop y Redsys son más lentos (altas y aprobaciones).
- **Quién actúa:** tú (propietario o administrador de la tienda) en Shopify, WooCommerce y Stripe. Tu informático o agencia, en PrestaShop si no tienes acceso a Parámetros avanzados. Tu banco, en Redsys. Tu comercial, en SEUR, MRW y Correos Express.
- **Vía recomendada:** empieza por Shopify, PrestaShop o WooCommerce en **solo lectura**, lanza el [resumen del lunes](./resumen-del-lunes.md) y añade pagos y envíos después.

## Antes de empezar

- Un **usuario o aplicación dedicada** para el agente (`ia-lectura`). Nunca tu cuenta de propietario.
- La clave va en el `.env` de la carpeta `01-TOOLS/<HERRAMIENTA>/`. **Nunca en el chat, en un email ni en WhatsApp.**
- Mira qué plan de IA usas antes de dar datos de clientes: [planes, privacidad y costes](./planes-privacidad-y-costes.md).
- Si vas a probar una escritura, hazlo antes en una **copia de pruebas** (staging) o en sandbox.

## Las vías, de mejor a peor

Una **API** es una ventanilla por la que otro programa pide datos. Un **MCP** es un enchufe estándar para que el agente use esa ventanilla sin código. Todo lo de la tabla se verificó el 2026-10-09.

| Plataforma | Vía | MCP oficial | Solo lectura real | Quién actúa | Coste |
|---|---|---|---|---|---|
| Shopify | Conector oficial de Claude o app en Dev Dashboard | Sí | Sí: scopes `read_*`; el conector trae la escritura apagada [1][2] | Propietario | Plan Basic 24 €/mes (anual) |
| PrestaShop | Módulo MCP oficial o clave del webservice | Sí (módulo, tienda 8.2+ o 9) | Sí: rol Viewer o clave solo GET [3][4] | Administrador o informático | 0 € licencia; hosting aparte |
| WooCommerce | Clave REST de Lectura (mejor que el MCP) | Sí, en vista previa para desarrolladores | Clave REST sí; el MCP no tiene modo lectura [5] | Administrador | 0 € plugin; hosting aparte |
| Amazon Seller | SP-API con app privada | Sí, de ejemplo (sin soporte) | No: los roles no separan leer de escribir [6] | Usuario principal | Plan Profesional 39 €/mes |
| Mercado Libre | API con OAuth | Solo documentación | Scope `read` sí; MCP comunitario de lectura [7] | Administrador de la cuenta | API gratis; comisión por venta |
| TikTok Shop | API con OAuth y firma | No (solo comunitarios) | Parcial, no verificado [8] | Propietario de la tienda | API gratis; comisión por venta |
| Stripe | Clave de agente (`rk_`) o MCP | Sí | Sí [9] | Administrador | 1,5 % + 0,25 € por cobro |
| Redsys | Portal del banco y notificación online | No | No: una sola clave por comercio [10] | Tu banco | Según banco |
| PayPal | App REST dedicada o MCP | Sí | No: sin clave de solo lectura [11] | Titular de la cuenta business | Comisión por transacción |
| Sendcloud | MCP oficial por toolsets | Sí | Parcial: se filtra por toolsets [12] | Tú | Free 0 €; Lite 28 €/mes |
| SEUR, MRW, Correos Express | API con contrato | No | No documentado [13] | Tu comercial | Contrato con el transportista |

## Paso a paso: pedidos, productos y clientes en solo lectura

Dile a tu agente: *«Conecta mi tienda (Shopify, PrestaShop o WooCommerce) en solo lectura»*. La skill `conectar-herramienta` creará `01-TOOLS/<TIENDA>/` con un `test_connection`. Tú generas la llave en el panel y la pegas en `.env`.

### Shopify

1. **Vía rápida:** instala el *Shopify connector for Claude* desde el directorio de conectores de Claude (no está en la tienda de apps de Shopify). Te lleva a tu panel de Shopify para aprobar el acceso [1].
2. Entra con una **cuenta de personal limitada**, no con la del propietario. Lo que el conector puede hacer depende de esa cuenta.
3. Aprueba solo lectura. Por defecto lee y no escribe; la escritura requiere tu aprobación. Productos, colecciones e inventario admiten escritura. Pedidos, clientes y analítica son solo lectura [2].
4. **Vía con clave** (si prefieres scripts): crea una app en el **Dev Dashboard** con scopes `read_products`, `read_orders` y `read_inventory`. Añade `read_customers` solo si lo necesitas y `read_all_orders` para pedidos de más de 60 días. Desde el 1-ene-2026 ya no se crean apps personalizadas antiguas desde el panel [2]. El token de esta vía caduca a las 24 horas.
5. Guarda Client ID y secreto en `.env`. Prueba con `test_connection`.

Límites: no se puede limitar por colección. En el plan Basic, los datos personales de clientes (nombre, email, teléfono, dirección) pueden venir recortados según el plan [2].

### PrestaShop

1. Entra en el back office como administrador. Activa **Parámetros avanzados > Webservice > «Activar el webservice»** (viene desactivado) [3].
2. **Añadir clave nueva** con nombre `IA-lectura`. Marca **solo GET y HEAD** en `orders`, `products`, `stock_availables` y, solo si hace falta, `customers`. La clave no caduca y no filtra por campo: si ve clientes, ve todos sus datos [3].
3. El webservice responde en XML. Pide JSON con `output_format=JSON` [3].
4. **Vía MCP oficial:** instala el módulo gratuito *PrestaShop MCP Server* (necesita PrestaShop 8.2+ o 9, HTTPS y los módulos Account, EventBus y MBO). Da de alta a tu agente en **Members** con rol **Viewer** (solo lectura) [4].
5. Prefiere OAuth al token estático: el token estático no caduca [4]. Apaga en «Modules & Features» las herramientas que no uses.
6. En la oferta Hosted (alojada) **no está verificado** que permita activar el webservice o instalar el módulo. Pregúntalo a PrestaShop antes de contar con ello.

### WooCommerce

1. Crea un usuario de WordPress `ia-lectura` **sin rol de administrador**.
2. Ve a **WooCommerce > Ajustes > Avanzado > API REST > Añadir clave**. Elige ese usuario y permiso **Lectura**. Copia el secreto: se ve una sola vez [5].
3. Esa clave no se limita por recurso: una clave de lectura ve también clientes y pedidos con datos personales, y no caduca. Revócala cuando no la uses.
4. **MCP integrado (vista previa):** viene apagado. Se activa en Ajustes > Avanzado > Características. Usa una contraseña de aplicación de WordPress sobre HTTPS, no las claves REST. **No tiene modo de solo lectura**: cada acción respeta los permisos del usuario [5]. Por eso, para empezar, usa la clave REST de Lectura y deja el MCP para una copia de pruebas.

### Dile a tu agente

*«Conecta mi Shopify en solo lectura con una app dedicada y dame el resumen de ventas de la semana.»*
*«Conecta mi WooCommerce con una clave de Lectura y exporta los pedidos de este mes a Excel.»*

## Marketplaces y sus limitaciones

- **Amazon:** necesitas plan Profesional (39 €/mes) y un perfil de desarrollador privado que Amazon revisa y no da plazos [6]. Pide solo los roles de pedidos, finanzas y precios; no pidas los roles restringidos salvo que necesites el nombre o la dirección del comprador. El refresh token lo autoriza el usuario principal. El `client_secret` hay que rotarlo: si vence, se bloquean todas las llamadas. Las cuotas de desarrollador anunciadas en 2025 se cancelaron en 2026 según Amazon [6].
- **Mercado Libre:** el MCP oficial solo busca documentación; **no lee tus pedidos** [7]. Para tus datos hay MCP comunitarios de lectura, no revisados por Mercado Libre. La app la crea y autoriza el administrador de la cuenta. Ojo: **no opera en España**. Necesitas cuenta en cada país, normalmente con sociedad o socio local [7].
- **TikTok Shop:** no hay MCP oficial de la tienda (el oficial es de publicidad). La API pide app key, app secret y firma en cada llamada. Su documentación no se pudo leer sin navegador, así que los detalles de permisos son **no verificados** [8]. Los MCP comunitarios leen y escriben sin modo de solo lectura.

Un comercio con miles de referencias (por ejemplo, repuestos para Mercado Libre) debe empezar por **exportar el catálogo a Excel** y medir rotación ahí; mira [Excel y hojas de cálculo](./excel-y-hojas-de-calculo.md).

## Pagos para conciliar

Conciliar es cruzar lo que cobraste con lo que vendiste. Lee los cobros y los pedidos y busca diferencias.

- **Stripe:** crea una **clave restringida con etiqueta Agent**, con Read en cobros, clientes, facturas y saldo y None en el resto. **Desde el 31-oct-2026 el MCP de Stripe rechaza las claves `sk_` y las `rk_` sin etiqueta Agent**: revisa tu configuración antes [9]. El MCP pide confirmación humana para reembolsos.
- **Redsys:** no tiene consulta por API. Los datos salen del Portal de Administración (exportación .xlsx) o de la notificación online que el banco envía a una URL tuya. Su clave firma también devoluciones, así que **no debe entrar nunca en el chat** [10]. Pide al banco un usuario del portal solo de consulta.
- **PayPal:** crea una app REST dedicada con solo *Transaction Search*. No hay claves de solo lectura. Según terceros, su MCP puede reembolsar o aceptar disputas sin confirmación obligatoria [11]. Pruébalo en sandbox.

Para pasar las ventas a facturas, mira [facturas emitidas y Verifactu](./facturas-emitidas-y-verifactu.md) y [conectar ERP, contabilidad y CRM](./conectar-erp-contabilidad-crm.md).

## Envíos

- **Sendcloud:** la vía más fácil. Crea una integración «Sendcloud API» solo para el arnés. Conecta su MCP limitado a los toolsets de seguimiento e informes (`?toolsets=parcel-tracking,parcel-statuses,analytics,reporting`). **Crear un envío se factura**, así que deja esas herramientas con confirmación [12].
- **SEUR, MRW y Correos Express:** hay que ser cliente con contrato. Pide a tu comercial credenciales exclusivas para la integración y la documentación de la API. No hay MCP. Alternativa: sube tu contrato a Sendcloud [13]. MRW tiene entorno de pruebas (sagec-test). De Correos Express no hay documentación pública.

## Caso guiado: el resumen del lunes de la tienda

Dile a tu agente: *«Cada lunes a las 8:00, con mi tienda y mis pagos en solo lectura, prepárame ventas de la semana, stock bajo y pedidos retrasados.»*

1. **Ventas:** pedidos de los últimos 7 días, total, ticket medio y comparación con la semana anterior.
2. **Stock:** productos por debajo del mínimo que tú fijes.
3. **Envíos:** pedidos pagados sin seguimiento o con incidencia.
4. **Cobros:** pagos de Stripe o PayPal sin pedido, y pedidos sin pago.
5. **Salida:** un documento en `out/` y un aviso por el canal que uses. Los datos de clientes no salen del arnés.

Receta completa: [resumen del lunes](./resumen-del-lunes.md). Para atender leads y mensajes: [leads y atención](./leads-y-atencion.md) y [conectar WhatsApp](./conectar-whatsapp.md).

## Escribir con cuidado

Leer es seguro. Escribir en la tienda cambia lo que ven tus clientes.

- **Siempre con aprobación humana.** Configura `permissions.ask` para toda acción que escribe.
- **Lotes pequeños.** Empieza con 5 productos, revisa el resultado y sigue. Shopify avisa de que los lotes grandes pueden parar a medias [2].
- **Precios, stock y fichas:** el agente te enseña «antes y después» en una tabla. Tú dices sí o no.
- **Copia antes de tocar.** Exporta el catálogo a CSV y guárdalo.
- **Borrar:** nunca sin tu confirmación. En WooCommerce el borrado va a la papelera salvo que se fuerce [5].
- **Reembolsos, cancelaciones y pagos:** a mano, tú. Shopify no deja hacerlos por el conector [2].
- **Imágenes de catálogo:** para un comercio de 75.000 productos, la subida por API existe (PrestaShop tiene herramienta de imágenes en su MCP [4]), pero **Freepik Spaces no sube resultados por sí solo a la tienda**. El proceso real: generar las imágenes, guardarlas con el código de producto en el nombre y subirlas por lotes con un script revisado. Empieza con 20 productos y mide coste y calidad antes de escalar. Qué herramienta de imágenes elegir: no verificado aquí.

## Datos de clientes (RGPD)

- Pide solo lo necesario. Si el informe no necesita nombre ni email, no concedas `read_customers` ni la clave de `customers`.
- Lo que extraigas va a `out/`, que no se sube a git.
- Si mandas datos personales a un proveedor de IA, necesitas contrato de encargo de tratamiento y un plan adecuado: [planes, privacidad y costes](./planes-privacidad-y-costes.md).
- En Amazon, los datos del comprador exigen un token especial (RDT) y roles restringidos [6]. No los pidas si no hacen falta.
- Anonimiza antes de analizar (por ejemplo, ID de cliente en lugar de nombre).

## Qué pedir a tu informático

> Necesito acceso de **solo lectura** a pedidos, productos y stock de la tienda para un agente de IA. Por favor: (1) en [Shopify: crea en el Dev Dashboard una app «IA-lectura» solo con scopes read_*] / [PrestaShop: activa el webservice y crea una clave «IA-lectura» solo con GET en orders, products y stock_availables] / [WooCommerce: crea un usuario «ia-lectura» sin rol de administrador y una clave REST con permiso Lectura]; (2) entrégame la clave por un gestor de secretos, no por email ni WhatsApp; (3) dime si la tienda tiene copia de pruebas.

## Pruébalo gratis

- **Shopify:** tienda de desarrollo desde el Dev Dashboard (solo pagos de prueba). Alternativa: 3 días de prueba y luego 1 €/mes durante 3 meses [2].
- **PrestaShop y WooCommerce:** software libre; instálalos en local o en un hosting de pruebas con API y MCP incluidos.
- **Stripe, PayPal, Redsys:** sandbox gratuito.
- **MRW:** entorno de pruebas sagec-test. Sendcloud: plan Free.

## Qué puedes automatizar después

- [Resumen del lunes](./resumen-del-lunes.md).
- [Leads y atención](./leads-y-atencion.md).
- [Facturas emitidas y Verifactu](./facturas-emitidas-y-verifactu.md).
- **Carritos abandonados:** detectarlos y proponer el aviso. PrestaShop tiene disparadores de carritos en Make [3]. Si ya usas Klaviyo, ese flujo suele vivir allí. **Klaviyo no está verificado en este manual.**
- **Meta Ads:** el catálogo apunta a que sus MCP piden permisos amplios y casi nunca tienen solo lectura. Usa un usuario dedicado con rol limitado [14]. **No verificado aquí.**
- **Coste de una importación antes de comprar:** una hoja con precio, transporte, aranceles y margen. Mira [Excel y hojas de cálculo](./excel-y-hojas-de-calculo.md).

## Preguntas de alumnos

**¿Se pueden subir imágenes generadas directamente a la tienda por API?**
Sí, la tienda lo permite (PrestaShop tiene API e imágenes en su MCP). Lo que no hace la herramienta de imágenes es subirlas sola. Hay que montar el paso intermedio, en lotes y con aprobación.

**Tengo 75.000 productos. ¿Lo hago todo de una vez?**
No. Empieza con 20, mide, y sigue por lotes. Un error repetido 75.000 veces es muy caro de deshacer.

**¿Qué stack uso para un equipo de agentes que gestione mi ecommerce?**
Empieza con un solo agente en solo lectura: tienda, pagos y envíos. Añade más áreas cuando el resumen del lunes funcione.

**¿Puedo conectar WooCommerce con Excel?**
Sí. Con una clave REST de Lectura exportas pedidos y productos. WooCommerce también exporta CSV de productos en el núcleo [5].

**Si el cliente paga a plazos, ¿la factura es por el total o por cuota?**
Es una decisión contable, no técnica. Pregúntaselo a tu gestoría antes de automatizar.

**Mi correo de cliente está mal escrito. ¿Se duplican los contactos?**
Puede ocurrir. Por eso el agente propone y tú apruebas antes de crear contactos o facturas.

**¿Puedo ver cuánto me cuesta una importación antes de comprar?**
Sí, con una hoja de cálculo que el agente rellene. Los costes reales de aduana los debe confirmar tu agente de aduanas.

**¿Puedo vender en Mercado Libre desde España?**
No directamente: la plataforma no opera en España [7].

**¿Mi MCP de Stripe de clase dejará de funcionar?**
Si usa claves `sk_` o `rk_` sin etiqueta Agent, sí, a partir del 31-oct-2026 [9].

## Errores típicos

- Usar la cuenta de propietario o de administrador para el agente.
- Pegar la clave en el chat.
- Dar a la clave de Redsys, PayPal o Amazon más alcance del necesario: no tienen modo de solo lectura.
- Activar el MCP de WooCommerce en producción pensando que es solo lectura.
- Subir cambios de precio a todo el catálogo sin revisión previa.
- Creer que el MCP oficial de Mercado Libre lee tus pedidos.
- Usar librerías no oficiales de WhatsApp para atender clientes (riesgo de bloqueo del número).
- Dejar claves antiguas sin revocar.

## Fuentes

Consultado el 2026-10-09. Las marcadas «catálogo» vienen de las fichas verificadas del proyecto.

1. Shopify, conector para Claude: https://help.shopify.com/en/manual/ai-powered-tools/connecting-ai-tools/shopify-connector-for-claude (web, 2026-10-09)
2. Shopify, tokens de acceso, Dev Dashboard y precios: https://shopify.dev/docs/apps/build/dev-dashboard/get-api-access-tokens ; https://www.shopify.com/es/precios (catálogo)
3. PrestaShop, webservice y Admin API: https://devdocs.prestashop-project.org/9/webservice/ ; https://apps.make.com/prestashop (catálogo)
4. PrestaShop MCP Server, seguridad: https://docs.mcp.prestashop.com/en/0-getting-started/security/ (web, 2026-10-09)
5. WooCommerce, MCP: https://developer.woocommerce.com/docs/features/mcp/ (web, 2026-10-09) ; claves REST: https://developer.woocommerce.com/docs/apis/rest-api/authentication/ (catálogo)
6. Amazon SP-API y MCP de ejemplo: https://github.com/amzn/selling-partner-api-samples (catálogo)
7. Mercado Libre, API y MCP: ficha del catálogo (`mercado-libre`)
8. TikTok Shop, Partner Center: https://partner.tiktokshop.com (catálogo, sin leer documentación oficial)
9. Stripe MCP: https://mcp.stripe.com (catálogo)
10. Redsys, Portal de Administración: https://canales.redsys.es/portal (catálogo)
11. PayPal MCP: https://mcp.paypal.com (catálogo)
12. Sendcloud MCP: https://mcp.sendcloud.com/mcp (catálogo)
13. SEUR, MRW y Correos Express: fichas del catálogo (`seur`, `mrw`, `correos-express`)
14. Categoría `ads-ecommerce-bi` del catálogo (hallazgos sobre Meta y mínimo privilegio)

## Relacionado
- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Conectar WhatsApp](./conectar-whatsapp.md)
- [Conectar ERP, contabilidad y CRM](./conectar-erp-contabilidad-crm.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
