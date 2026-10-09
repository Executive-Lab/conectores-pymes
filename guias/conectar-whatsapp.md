---
type: article
title: Conectar WhatsApp a tu negocio y a tu agente
description: Manual para dueños de pyme que usan la app WhatsApp Business y quieren que n8n, Make o su agente lean y respondan mensajes sin que Meta les bloquee el número.
tags: [guia-alumnos, whatsapp, cloud-api, coexistencia, n8n, make, telegram]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Conectar WhatsApp a tu negocio y a tu agente

> Para: dueños y directivos de pyme que hoy atienden clientes con la app WhatsApp Business en el móvil.
> Conseguirás: saber qué vía es legal y estable, seguir usando tu móvil y que pedidos, reservas y leads entren solos en tu sistema, con una persona al mando.

## En resumen
La app WhatsApp Business **no tiene API**. Una API es una ventanilla por la que otro programa pide o entrega datos, y esa ventanilla no existe en la app [1]. Para automatizar hay que usar la **WhatsApp Business Platform** (la «Cloud API» de Meta), que sí la tiene.

Desde la **coexistencia** puedes dar de alta tu número actual en la Platform y **seguir usando la app en el móvil** [2]. Es la vía recomendada para casi todos los alumnos.

- **Cuánto tarda:** probar gratis, una tarde. Producción con número real, de 2 a 7 días (verificación y plantillas).
- **Quién actúa:** tú (el administrador de tu empresa en Meta), más un proveedor (BSP) o una herramienta con alta de coexistencia, como Make [5]. Tu informático, solo si quieres alojar n8n.
- **Quién escucha 24 h:** no es Claude Code. Lo hace **n8n** o **Make**. Claude Code construye y mantiene el flujo.
- **Lo que no hay que hacer:** usar librerías no oficiales ni escanear un QR con un robot. Meta puede bloquear el número, a veces para siempre [8].

## Antes de empezar

1. **Un Meta Business portfolio** (antes Business Manager) a nombre de tu empresa, con tú como administrador.
2. **Un número** que ya use WhatsApp Business o uno nuevo. Con coexistencia, la app debe ser la versión 2.24.17 o superior [2].
3. **Método de pago** en Meta (tarjeta), porque las plantillas se cobran por mensaje [3].
4. **Verificación del negocio** (CIF, web, documento de la empresa). No es obligatoria para empezar, pero sube el límite de envío. Un portfolio nuevo parte de 250 destinatarios únicos al día para mensajes que inicias tú. Con la empresa verificada, o con un envío sostenido de buena calidad, sube a 2.000 y luego escala sola [4].
5. **Decide qué automatizas:** pedidos, reservas, leads, avisos. Si no lo sabes, mira antes [Cómo se monta](./como-se-monta.md).

## Las vías, de mejor a peor

| Vía | Para qué sirve | Quién lo hace | Coste | Dificultad |
|-----|----------------|---------------|-------|-----------|
| **Cloud API + coexistencia**, con n8n o Make | Automatizar y seguir con la app en el móvil | Tú + BSP o Make | 0 € fijo + plantillas + BSP si lo hay | Media |
| **Cloud API directa con Meta**, número nuevo o dedicado | Bot completo sin app en ese número | Tú | 0 € fijo + plantillas | Media |
| **BSP con bandeja compartida** (Twilio, 360dialog, Vonage, respond.io…) | Equipo atendiendo desde una bandeja web | Tú | Cuota del BSP + plantillas | Baja-media |
| **App sin automatizar**: respuestas rápidas, etiquetas y catálogo | Ordenar la atención sin IA | Tú | 0 € | Fácil |
| **Librerías no oficiales o robot sobre WhatsApp Web** | Nada: no la uses | Nadie | Perder el número | No aplica |

## App frente a Platform: qué se puede y qué no

| | App WhatsApp Business | Platform (Cloud API) |
|--|----------------------|----------------------|
| API y webhooks | No | Sí [1] |
| Leer chats con un programa | No | Solo lo que llega **desde que conectas**, por webhook. No hay endpoint de historial |
| Respuestas automáticas con IA | Solo mensaje de ausencia y saludo | Sí, con escalado a una persona [6] |
| Listas de difusión, llamadas, canales | Sí | No en la API [2] |
| Escribir primero a un cliente | Sí, un cliente a la vez | Solo con **plantilla aprobada** [6] |
| Varios agentes a la vez | Hasta 4 dispositivos vinculados (no verificado en esta consulta) | Los que quiera tu software |

## Coexistencia: requisitos y límites actuales

Requisitos [2]:

- App Business 2.24.17 o superior.
- El alta la hace un **Solution Partner o Tech Provider** con *Embedded Signup*, un asistente de Meta que se abre dentro de la web del partner. No puedes hacerla tú solo en el panel de Meta. Make ofrece este alta dentro de su conector, pero no en todos los países [5].
- Un webhook (una dirección que recibe los mensajes). n8n o Make ya lo tienen.

Límites [2]:

- Tope de envío de **20 mensajes por segundo**.
- Los **grupos no se sincronizan**: el agente solo ve chats 1:1.
- Se desactivan listas de difusión, mensajes temporales, «ver una vez» y ubicación en tiempo real en chats 1:1. Las listas existentes quedan en solo lectura.
- Se desvinculan los WhatsApp de Windows y otros dispositivos acompañantes.
- Importa los chats 1:1 de los **últimos 180 días**. Los archivos solo de los últimos 14 días. Si no sincronizas el historial en 24 horas, hay que repetir el alta.
- Si **no abres la app en unos 14 días**, el número se desconecta de la API.

Lo que escribas tú a mano desde la app también llega a tu flujo. Tenlo en cuenta: el agente verá chats privados que no son de negocio si usas el número para todo. **Usa un número solo de empresa.**

## Proveedor (BSP) o conexión directa con Meta

- **Directa con Meta:** gratis, sin intermediario, y tú controlas el token. Pero **sin coexistencia**: el número pasa a ser solo de API y pierdes la app en él [2].
- **BSP o Tech Provider:** necesario para la coexistencia. Te da bandeja compartida, soporte y alta guiada. Cobra una cuota propia, **no verificada aquí**, que varía por proveedor. Pide precio por escrito.
- **Verificación del negocio:** se hace en el portfolio de Meta con tus datos fiscales. Si te dio de alta un partner, él también puede verificarla por ti [4].
- Pide siempre que el portfolio y el número **sean tuyos**, no del proveedor. Si un día cambias, te llevas el número.

### Precios vigentes (España, 2026-10-09)

Meta cobra **por mensaje de plantilla entregado**, según categoría y país del destinatario [3]:

- **Marketing** (ofertas, novedades), **Utilidad** (confirmar un pedido, un recordatorio de cita) y **Autenticación** (códigos).
- **Dentro de la ventana de 24 h** que abre el cliente al escribirte, los mensajes de servicio son gratis. Las plantillas de utilidad dentro de la ventana también lo eran hasta ahora [3].
- Los mensajes que llegan de un anuncio **Click-to-WhatsApp** o del botón de tu página de Facebook abren una ventana de **72 horas gratis** [3].
- Meta subió el precio de marketing en España el 1-jul-2026 [3]. Importes aproximados en EUR sin IVA, **de terceros, no verificados en Meta**: marketing 0,051-0,059 € y utilidad o autenticación unos 0,017 €.
- **Cambio de octubre de 2026 (no verificado en la página de Meta):** según varios proveedores, desde el 1-oct-2026 los primeros 1.000 mensajes de servicio al mes por número siguen gratis y el resto se cobra, y las plantillas de utilidad dentro de la ventana también se cobran [7]. Comprueba la tarifa en tu WhatsApp Manager antes de lanzar un volumen alto.
- Lo que envías tú desde la app en coexistencia sigue siendo gratis (según la ficha del catálogo).

## Paso a paso

1. **Prueba gratis, sin tocar tu número.** En developers.facebook.com crea una app de tipo Negocio y añade el producto WhatsApp. Meta te da un número de prueba (+1 555…) con plantilla `hello_world`, y envía a un máximo de 5 números verificados. Tus clientes no pueden escribirle.
2. **Conecta n8n o Make:**
   - **n8n:** nodo **WhatsApp Business Cloud** (enviar mensaje, enviar plantilla, *enviar y esperar respuesta*, subir y descargar archivos) y **WhatsApp Trigger** para recibir [9]. El nodo «Enviar y esperar respuesta» sirve de **botón de aprobación** antes de que el agente ejecute una acción [9].
   - **Make:** app oficial **WhatsApp Business Cloud**, con módulos instantáneos (webhook) para recibir y módulos para enviar mensajes y plantillas. Su conexión recomendada admite alta normal o de coexistencia. La conexión antigua con token se mantiene hasta abril de 2027 [5].
3. **Crea un usuario del sistema** (System User) en el portfolio de Meta, dedicado a esta integración, con acceso **solo** a esa cuenta de WhatsApp y a esa app, y los permisos `whatsapp_business_messaging` y `whatsapp_business_management`. Un token por integración.
4. **El token va a las credenciales de n8n o Make, o a `01-TOOLS/WHATSAPP/.env`.** Nunca al chat, ni por email, ni por WhatsApp. No hay token de solo lectura: quien lo tenga puede enviar y recibir. Si el agente solo debe leer, dale **el flujo del webhook** y no el token.
5. **Producción:** alta del número real en coexistencia por el partner, verificación del negocio, plantillas aprobadas con días de antelación.
6. **El agente de Claude Code** no escucha WhatsApp. Sirve para generar y revisar el flujo, redactar plantillas, probar con datos de ejemplo y leer los resultados que n8n deja en una hoja o carpeta.

Dile a tu agente: *«Conecta mi WhatsApp Business en solo lectura: crea `01-TOOLS/WHATSAPP` con una prueba de conexión, usa el número de prueba de Meta y recibe mensajes solo por el WhatsApp Trigger de n8n. No envíes nada sin mi aprobación.»*

## Plantillas, ventana de 24 horas y opt-in

- **Opt-in:** solo puedes escribir a quien te dio su teléfono y aceptó recibir mensajes tuyos. Eres tú quien guarda la prueba (casilla del formulario, pedido, mensaje del cliente). Ofrece una baja clara y respétala [6].
- **Ventana de 24 horas:** cuando un cliente te escribe, tienes 24 h para responder **con texto libre**. Cada mensaje suyo la reinicia [3].
- **Fuera de la ventana** solo se envía una **plantilla**, un texto con huecos que Meta aprueba antes. Meta puede pausar o rechazar plantillas cuando quiera [6].
- **Automatización permitida**, siempre con salida clara a una persona (teléfono, email o «hablar con alguien») [6].
- **Política de IA (15-ene-2026):** no se permiten asistentes de IA generalistas como producto principal. Un bot de atención de tu propia empresa sí está permitido, según Meta citada por la prensa [8]. Los textos oficiales de las condiciones no los pude abrir.

## Lo que nunca hay que hacer

- **Librerías no oficiales** (whatsapp-web.js, Baileys, whatsmeow) y los servidores que las envuelven: escanean un QR como si fueran WhatsApp Web. Incumplen las condiciones y Meta puede bloquear el número, a veces sin recuperación. Pasa incluso con poco volumen.
- **Automatizar la app con el móvil o un robot** (clics, accesibilidad de Android, «granjas» de móviles). Mismo riesgo y se rompe con cada actualización.
- **Plantillas o plataformas de «WhatsApp fácil»** sin preguntar qué hay debajo. Si piden escanear un QR con tu móvil, es no oficial. Evolution API y Builderbot incluyen ese modo, y también uno con la API oficial de Meta: elige este último.
- **Escribir en frío** a listas compradas o sin opt-in.
- **Pegar el token en el chat** o dejarlo en un Excel.

## Permisos: qué marcar y qué no

- **Marca:** `whatsapp_business_messaging` y `whatsapp_business_management`, en un usuario del sistema dedicado y solo sobre tu cuenta de WhatsApp.
- **No marques:** permisos de anuncios, de páginas ni de otras cuentas. No uses tu usuario personal ni el de administrador.
- **No se puede acotar:** no existe «solo lectura», ni limitar a ciertos contactos. El token vale hasta que lo revocas. Rótalo si alguien deja la empresa.
- **Valida la firma** de los webhooks con el *app secret* para que nadie falsifique mensajes.
- **Los mensajes de los clientes son contenido no fiable.** El agente no obedece lo que «diga» un mensaje. Dale herramientas mínimas y escrituras acotadas.
- **Datos personales:** mira antes qué plan de IA usas, en [Planes, privacidad y costes](./planes-privacidad-y-costes.md).

## Qué pedir a tu informático

> Hola. Necesito dar de alta nuestro número de WhatsApp en la WhatsApp Business Platform **en modo coexistencia**, a través de un BSP o Tech Provider, para seguir usando la app en el móvil. El portfolio de Meta y el número deben quedar a nombre de la empresa. Crea un usuario del sistema con acceso solo a esa cuenta de WhatsApp y los permisos `whatsapp_business_messaging` y `whatsapp_business_management`. Guarda el token en un gestor de secretos y no me lo envíes por email ni por chat. Valida la firma de los webhooks. Nada de librerías no oficiales (whatsapp-web.js, Baileys). Pídeme, si hace falta, el CIF y los documentos de verificación del negocio.

Más textos: [Hablar con el informático](./hablar-con-el-informatico.md).

## Telegram como alternativa para avisos y aprobaciones internas

Telegram es la forma fácil de avisar **a tu equipo** (no a tus clientes). Su Bot API es gratis, sin verificación y se conecta en 5 minutos. Dificultad: fácil.

1. En Telegram, habla con **@BotFather** y crea un bot de empresa. Te da un token.
2. Deja activado el **privacy mode** y desactiva que lo metan en grupos ajenos (`/setjoingroups`).
3. En n8n usa los nodos **Telegram** y **Telegram Trigger**, filtrando por el ID del chat autorizado.
4. Úsalo para: «ha entrado un pedido nuevo», «un cliente pide hablar con alguien», «¿apruebo esta factura? Sí o No» y «ha fallado una automatización».

Límites: el token controla todo el bot, no hay solo lectura y el bot no lee el historial anterior. **No uses** MCP que entran en tu cuenta personal de Telegram. Datos según la ficha del catálogo.

## Pruébalo gratis

Número de prueba de Meta + n8n (self-hosted gratis, desde 20 €/mes en la nube) + una hoja de Google. Demo de clase: «¿Me guardas 2 pollos para las 14:00?» → el flujo descuenta el contador y confirma. Sin coste de plantillas con `hello_world`.

## Casos de alumnos

- **Pedidos y reservas** (hostelería, distribución, comida por encargo): el asistente toma el pedido, lee stock o disponibilidad, crea un **borrador** o una fila y avisa al negocio. Receta completa en [WhatsApp a pedidos y reservas](./whatsapp-a-pedidos.md). Este manual no la repite.
- **Seguimiento de leads** (formularios, portales inmobiliarios, anuncios): el cliente rellena un formulario con la casilla de opt-in, el flujo le abre un chat con una **plantilla de utilidad**, responde dudas dentro de la ventana y pasa el lead a comercial. Si viene de un anuncio Click-to-WhatsApp, tienes 72 h gratis [3]. Ver [Leads y atención](./leads-y-atencion.md).
- **Gestoría con peticiones de factura por WhatsApp:** el flujo recibe el mensaje, un agente extrae cliente, concepto e importe y lo deja en una hoja o en un **fichero de importación** del programa. Una persona lo revisa. Si el ERP no tiene API, **nunca** se escribe en su base de datos: se usa el fichero de importación oficial (regla de [Conectar o migrar](./conectar-o-migrar.md)). Se responde al cliente «recibido, lo revisamos» y la factura la emite el humano. Cuidado con RGPD y con quién es el responsable del dato.

## Qué puedes automatizar después

- [WhatsApp a pedidos y reservas](./whatsapp-a-pedidos.md)
- [Leads y atención](./leads-y-atencion.md)
- [Resumen del lunes](./resumen-del-lunes.md), con avisos por Telegram.
- [Facturas a contabilidad](./facturas-a-contabilidad.md), para el caso de la gestoría.

## Preguntas de alumnos

**1. ¿Se puede conectar n8n con WhatsApp?** Sí, con el nodo oficial WhatsApp Business Cloud y el WhatsApp Trigger [9].

**2. ¿Y Make?** Sí, con su app oficial WhatsApp Business Cloud y sus módulos instantáneos para recibir [5].

**3. Meta me pide credenciales y no las consigo.** Necesitas un portfolio de Meta, un usuario del sistema con los dos permisos y un método de pago. Empieza por el número de prueba de Meta, que no pide verificación. Si te atascas, que lo haga el partner del alta.

**4. ¿Puedo automatizar el WhatsApp de mi tienda sin perder el móvil?** Sí, con coexistencia. Tienes límites: sin listas de difusión y con la app abierta cada pocos días [2].

**5. ¿Puedo usar un truco con QR para no pasar por Meta?** No. Es el atajo que más números bloquea. Si alguien te lo ofrece, es no oficial.

**6. Los clientes de mi gestoría piden facturas por WhatsApp. ¿Se llega hasta el ERP?** Se recibe y se prepara solo. La emisión pasa por una persona y por el fichero de importación del programa, no por la base de datos.

**7. Mis clientes rellenan un formulario. ¿Puedo seguirles por WhatsApp?** Sí, si aceptaron recibirlo (opt-in) y con una plantilla aprobada. Fuera de las 24 h solo valen plantillas [6].

**8. ¿Cómo me entero de que una automatización ha fallado?** Un flujo de error en n8n que te escribe un mensaje por Telegram.

**9. ¿Puedo hacer un bot de voz o que reciba audios y fotos?** La API recibe audios, fotos y documentos como archivos. El flujo los descarga con el nodo de media [9] y los transcribe. La voz de salida como llamada no está soportada en la API en coexistencia [2].

**10. ¿Qué pasa si el bot la lía con un cliente?** La responsabilidad es de tu empresa. Pon un texto que avise de que es un asistente, salida a una persona y revisión de lo que promete. Pausa el bot cuando contestes tú a mano.

## Errores típicos

- Montar el bot sobre la app con un truco y perder el número.
- Usar el número personal del dueño para todo: el agente verá chats privados.
- No abrir la app durante dos semanas y quedarte sin conexión [2].
- Lanzar sin plantillas aprobadas. Pídelas con días de antelación.
- Bot que no se calla cuando contestas tú: falta la pausa por chat.
- No guardar la prueba del opt-in.
- Calcular costes con la tarifa de la ventana gratuita y no con la de plantillas.
- El BSP es el dueño del portfolio y no puedes irte.

## Fuentes

1. Meta, WhatsApp Business Platform, Cloud API: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/ — consultado el 2026-10-09 (a través de la ficha del catálogo).
2. Meta, Onboarding de usuarios de la app (coexistencia): https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users — consultado el 2026-10-09.
3. Meta, Precios: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing — consultado el 2026-10-09.
4. Meta, Límites de mensajería: https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits — consultado el 2026-10-09.
5. Make, app WhatsApp Business Cloud: https://apps.make.com/whatsapp-business-cloud — consultado el 2026-10-09.
6. WhatsApp, Política de empresa: https://whatsappbusiness.com/policy/ — consultado el 2026-10-09.
7. Cambio de octubre de 2026, de terceros (no verificado en Meta): https://help.meetergo.com/en/integrations/automation/whatsapp-pricing y https://sendpulse.com/blog/whatsapp-service-message-pricing — consultado el 2026-10-09.
8. TechCrunch, cambio de condiciones de IA: https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform/ — consultado el 2026-10-09 (resumen de prensa).
9. n8n, nodo WhatsApp Business Cloud: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.whatsapp/ y https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.whatsapptrigger/ — consultado el 2026-10-09.
10. Telegram, Bot API: https://core.telegram.org/bots/api — consultado el 2026-10-09 (datos de la ficha del catálogo `telegram`, no releída en la web).

## Relacionado
- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Conectar o migrar](./conectar-o-migrar.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
