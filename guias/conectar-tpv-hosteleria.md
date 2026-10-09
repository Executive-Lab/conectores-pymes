---
type: article
title: Conectar el TPV y la gestión de un restaurante
description: Cómo sacar ventas, tickets, cierres y costes de tu TPV (Ágora, Revo, ICG/HioPos) y de Haddock o Excel, en solo lectura, para un resumen semanal con alertas de margen; para dueños de bares, restaurantes, catering y obradores.
tags: [guia-alumnos, hosteleria, tpv, agora, revo, hiopos, haddock, escandallos, solo-lectura]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Conectar el TPV y la gestión de un restaurante

> Para: dueños y directivos de bares, restaurantes, catering y obradores que quieren ver ventas, costes y márgenes sin copiar datos a mano.
> Conseguirás: elegir la vía para leer tu TPV, montar escandallos fiables y recibir cada lunes un resumen con alertas de margen. El agente solo lee: nunca escribe en el TPV.

## En resumen
Lo que piden los alumnos de hostelería, en resumen: un cuadro de mando que junte el TPV y el Excel, con alertas cuando bajan los márgenes de los escandallos; stock y mermas; reservas por teléfono y WhatsApp; casar los albaranes con las facturas mensuales y pasarlos a la contabilidad; presupuestos de catering desde el correo; y ventas por producto.

Casi todo sale de **dos fuentes**: lo que vendes (el TPV) y lo que te cuesta (facturas de compra y escandallos). Un **escandallo** es la ficha de coste de un plato: ingredientes, cantidades y precio de cada uno, para saber cuánto cuesta y qué margen deja.

- **Cuánto tarda:** la petición al distribuidor, un día. Que te lo activen, de días a un par de semanas. El resumen del lunes, una tarde cuando ya hay datos.
- **Quién actúa:** tú redactas la petición; **el distribuidor o el fabricante del TPV** activa la puerta (en hostelería casi nunca es de autoservicio) [1][2]; tu agente la usa.
- **Vía recomendada:** si tu TPV tiene API (Revo, Ágora), leerla con una clave exclusiva. Si no (ICG/HioPos), una **exportación programada** de ventas a una carpeta. Los costes, desde la exportación de Haddock o desde un Excel limpio.

Una **API** es una ventanilla por la que otro programa pide datos al tuyo. Una **exportación programada** es un empleado que deja cada noche un informe en una carpeta.

## Antes de empezar

- Saber qué TPV tienes y **quién te lo instaló** (el distribuidor). Sin él, casi nada se activa.
- Una carpeta de proyecto con el arnés RSC (`01-TOOLS/`, `02-DOCS/`). Si no la tienes, empieza por [Cómo conectar una plataforma con RSC](./conectar-una-plataforma-con-rsc.md).
- Decidir **qué datos** quieres (ver más abajo). Pedir poco acelera la respuesta.
- Si en los tickets hay datos de clientes (nombre, tarjeta fidelidad), mira antes qué plan de IA usas: [planes, privacidad y costes](./planes-privacidad-y-costes.md).

## Los TPV, de un vistazo

| TPV | Vía | Quién lo activa | Coste (según catálogo) | Dificultad |
|-----|-----|-----------------|------------------------|------------|
| **Ágora** (IGT) | API REST local (módulo *Integration Services*, Ágora 6.0.6 o superior). Vive en la red del local, no en la nube | **Distribuidor** de Ágora | Planes desde 34 €/mes por local; instalación aparte; no confirmado si la integración va incluida | Media |
| **Revo XEF / RETAIL** (Cegid) | API REST en la nube con informes v3, webhooks y límite de 120 peticiones por minuto [3] | **Revo** (te da un `client-token`) y tú (token de cuenta) | Precios no publicados; la API no tiene coste publicado | Media |
| **ICG / HioPos** | **Sin API pública**. Exportación por FTP o acceso de solo lectura a la base de datos, siempre vía distribuidor | **Distribuidor** de ICG/HioPos | No publicado | Difícil |
| **Haddock** (costes, escandallos) | La API es **solo de entrada** (los TPV le envían ventas). No hay API de lectura. Sí exporta documentos y productos a Excel o CSV desde la web [4] | Tú, desde la web | 149, 248 o 299 €/mes según plan | Difícil por API; fácil por exportación |
| **Kross Booking** (PMS de alojamientos) | API limitada, sin documentación pública | El proveedor | Desde 4 a 6 €/mes por unidad | Difícil |

Datos y matices por TPV:

- **Ágora.** El token se genera en *Ágora Server Config > Herramientas > Activar módulos adicionales > Configurar servicios de integración* [1]. No hay prueba gratuita ni versión de evaluación pública: pide al distribuidor un servidor de demostración. El token **da acceso completo** y no hay token de solo lectura documentado. Se acota por red (ver Permisos).
- **Revo.** El `client-token` se pide con el formulario de integraciones de Revo. Los informes v3 incluyen, entre otros, `products`, `orders`, `receipts`, `payments`, `invoices` y `turns` (turnos) [3]. La documentación no los llama «ventas por producto» ni «cierres»: prueba cuál encaja en el entorno de pruebas (`integrations.revoxef.works`). Tampoco hay MCP oficial; el de unified.to es de terceros y de pago por uso.
- **ICG/HioPos.** No hay API pública ni MCP [5]. Si Haddock ya recibe tus ventas de HioPos, es porque el distribuidor configuró una exportación por FTP: la misma puerta puede alimentar al arnés. En FrontRest o ICGManager (Windows) puede haber una base de datos local; el distribuidor decide si se te da un usuario de solo lectura.
- **Haddock.** La credencial de su API solo sirve para **escribir** ventas. Para leer tus costes, exporta a Excel o CSV (facturas, líneas de producto, resumen de IVA y formato Holded). La exportación de **escandallos** no está confirmada en su ayuda: pregúntalo al soporte.
- **Kross Booking.** Es para alojamiento (apartamentos, hotel), no para reservas de mesa. Solo te interesa si tu restaurante tiene también habitaciones.

Ninguno ofrece hoy un MCP oficial ni un token de solo lectura. La seguridad se pone **fuera**: en la red, en una clave exclusiva y en que el agente solo llame a consultas.

Si tu caso es «mi TPV no tiene API», lee [Mi programa no tiene API](./mi-programa-no-tiene-api.md). La parte técnica para tu informático está en [Kit puente, parte técnica](./kit-puente-tecnico.md).

## Qué datos sacar y cómo

| Dato | Para qué sirve | Mejor vía |
|------|----------------|-----------|
| **Ventas por producto** (unidades e importe, por día) | Mix de ventas, platos estrella, base del cálculo de margen | API (Revo, Ágora) o exportación programada |
| **Tickets** (líneas, hora, mesa, medio de pago) | Horas punta, ticket medio, anulaciones | API o exportación; pesan mucho: pide solo el rango que necesitas |
| **Cierres de caja** | Cuadrar cobros, detectar descuadres | API o informe por correo del propio TPV |
| **Stock** | Mermas y pedidos | Normalmente **no** sale del TPV: sale de Haddock, de otro programa de stock o de un Excel de inventario |

Las tres maneras de recibirlo, de mejor a peor:

1. **API** (Revo, Ágora): el agente pide el dato cuando lo necesita. Lo más flexible; exige clave y alguien que la active.
2. **Exportación programada**: el TPV o el distribuidor deja cada noche un CSV o Excel en una carpeta que el arnés lee. Es lo más sencillo y seguro, y la única vía en muchos ICG/HioPos.
3. **Informe por correo**: casi todos los TPV pueden enviarte el cierre del día por email. El agente lee esa bandeja. Es frágil si cambia el formato, pero no pide nada al distribuidor.

Regla de oro: **empieza por ventas por producto y cierres**. Son los datos más útiles y los que menos riesgo tienen.

## Escandallos: en Haddock o en Excel

Hay dos caminos. Elige uno, no los dos a la vez.

**A. Si ya tienes Haddock.** Haddock lee las facturas de compra y mantiene los precios de los ingredientes. El agente no puede leer su API, pero sí su exportación a Excel o CSV [4]. Exporta cada mes (o cada semana) y deja el fichero en una carpeta.

**B. Si usas Excel.** Una hoja `ingredientes` (nombre, unidad, precio, fecha del último precio) y una hoja `escandallos` (plato, ingrediente, cantidad). Reglas para que la IA no se invente cifras: una tabla limpia por hoja, los cálculos **con fórmulas o código** (no «de cabeza») y un total de control que compruebas tú. Los detalles están en [Tu Excel como fuente de datos](./excel-y-hojas-de-calculo.md).

La alerta de margen funciona así:

- **Margen del plato** = (precio de venta sin IVA − coste del escandallo) ÷ precio de venta sin IVA.
- El coste se recalcula con el **último precio de compra** de cada ingrediente.
- Salta una alerta si el margen baja de tu umbral (por ejemplo, 5 puntos por debajo del objetivo) o si un ingrediente sube más de un porcentaje que tú fijas.
- Cada alerta lleva el dato que la justifica: «el aceite subió de X a Y; el plato Z pasa del A % al B %».

## Paso a paso

1. **Elige tus tres datos** de la tabla anterior (ventas por producto, cierres, y costes).
2. **Pide al distribuidor** lo que toque con el texto de abajo.
3. **Guarda la clave** solo en `01-TOOLS/<TPV>/.env` (nunca en el chat, ni por email, ni por WhatsApp).
4. **Prueba la conexión** con una consulta de **un solo día** y compara con el cierre que ves en el TPV.
5. **Monta el resumen del lunes** (caso guiado, más abajo).

Dile a tu agente:

> *«Conecta mi TPV Revo en solo lectura: crea `01-TOOLS/REVO` con un `test_connection` que lea solo los informes de ventas de ayer. La clave la pongo yo en `.env`.»*

> *«Mi TPV es ICG/HioPos y no tiene API. Prepárame la petición al distribuidor para una exportación diaria de ventas y un script que lea esa carpeta en solo lectura.»*

El agente usará la skill `conectar-herramienta` para decidir la vía y acotar permisos.

## Caso guiado: el resumen del lunes del restaurante

**Objetivo.** Cada lunes a las 7:30, un correo con ventas de la semana, margen por plato, alertas de coste y reservas de la semana. Es una versión de la receta [El resumen del lunes](./resumen-del-lunes.md): léela para ver cómo se programa.

**Fuentes (todas de solo lectura).**

1. **Ventas del TPV**: ventas por producto y cierres de la semana (API o carpeta de exportación).
2. **Escandallos y costes**: la exportación de Haddock o tu Excel de escandallos.
3. **Reservas**: la agenda de reservas que uses (hoja compartida, correo de confirmaciones o el sistema de reservas, si exporta). Cómo llegan las reservas de WhatsApp: [Conectar WhatsApp](./conectar-whatsapp.md).

**Lo que contiene el correo.**

- Ventas de la semana frente a la anterior, y por día.
- Los 5 platos que más venden y los 5 que menos.
- Margen por plato (ventas por producto × escandallo). Los 3 platos con peor margen.
- Hasta **tres alertas**, cada una con su dato: margen bajo el umbral, ingrediente que sube, descuadre de caja.
- Reservas de la semana y mesas sin confirmar.
- Una línea final: «fuentes que han fallado», si alguna. Si una fuente falla, el correo lo dice y no estima.

**Cómo se monta.**

1. Crea la skill `/resumen-semanal` con tus definiciones: qué es «venta» (sin IVA), qué es «plato con margen bajo» (tu umbral), qué reservas cuentan.
2. Cruza ventas y escandallos **por código** (script o hoja), no con el modelo de lenguaje: las cuentas las hace el código y la IA redacta.
3. Guarda cada semana los datos en `02-DOCS/raw/resumenes/` para comparar.
4. Pruébalo a mano tres lunes. Después, prográmalo: Revo (en la nube) funciona con una *routine*; Ágora (local) con una tarea programada en el ordenador del local (`claude -p` más cron o el Programador de tareas) [1].
5. El correo se envía como **borrador** o al dueño. No se escribe nada en el TPV.

Dile a tu agente:

> *«Crea la skill resumen-semanal para mi restaurante: ventas por producto del TPV, escandallos de Haddock (exportación) y reservas de la semana. Solo lectura, máximo tres alertas, y si una fuente falla, dilo.»*

## Qué más puedes automatizar después

- **Albaranes con facturas mensuales y contabilidad.** El agente casa los albaranes con las facturas y prepara el **fichero de importación** de tu programa contable; una persona lo revisa e importa. Mira [Presupuestos, pedidos y albaranes](./presupuestos-pedidos-albaranes.md) y [Escribir en contabilidad por importación](./escribir-en-contabilidad-por-importacion.md).
- **Presupuestos de catering desde el correo.** El agente lee la petición, propone el presupuesto con tus tarifas (en Excel) y tú lo apruebas antes de enviarlo. Misma receta.
- **Reservas por WhatsApp.** Por la vía oficial: [Conectar WhatsApp](./conectar-whatsapp.md). Las reservas entran en tu agenda con una persona al mando.
- **Stock y mermas.** Si llevas un Excel de inventario, compara existencias contra ventas y avisa de las diferencias.

## La regla de oro: nunca escribas en el TPV

- El agente **lee**. No crea tickets, no cambia precios, no toca la carta ni el stock del TPV.
- Un fallo ahí afecta a la sala en pleno servicio, a la caja y a las obligaciones fiscales (el TPV es un sistema de facturación: con Veri\*factu, los plazos son 1-1-2027 para sociedades y 1-7-2027 para el resto, y Hacienda ha anunciado una posible ampliación) [6].
- Si necesitas cambiar la carta o los precios, hazlo tú en el TPV, con el distribuidor si hace falta. El agente puede **preparar** el cambio en una hoja.
- Un token que lee y escribe (Ágora y Revo no tienen de solo lectura) es una llave maestra: úsala solo con un agente que llame a consultas de lectura.

## Permisos: qué marcar y qué no

- **Clave exclusiva** para el arnés en cada TPV, nunca la del dueño ni la del administrador. Así se revoca sin afectar al resto.
- **Revo:** no uses el token de la cuenta maestra (ve los informes de toda la cadena). Crea uno solo para el arnés y revócalo si no lo usas.
- **Ágora:** el puerto 8984 **nunca abierto a Internet**. El cortafuegos de Windows solo deja entrar desde el equipo del agente. Un agente o *proxy* local solo reenvía las consultas de exportación (lectura).
- **ICG/HioPos:** si hay base de datos, un usuario de solo lectura sobre **vistas** de ventas, nunca el administrador. Con FTP, el TPV solo escribe y el arnés solo lee.
- **Haddock:** si usas su exportación, un usuario con el rol más bajo que vea compras. No se puede tener un token de solo lectura.

## Qué pedir al distribuidor del TPV

Copia, adapta el TPV y envía por correo (la clave nunca por correo):

> Asunto: Exportación de datos de ventas de nuestro TPV (solo lectura)
>
> Hola, [nombre]:
>
> Somos [local o grupo] y usamos [Ágora / Revo / ICG-HioPos] en [n.º de locales] local(es). Queremos recibir los datos de ventas en un informe propio, **sin modificar nada en el TPV**.
>
> Os pedimos:
> 1. Que nos activéis [el módulo Integration Services en Ágora / el client-token de API en Revo / una exportación automática diaria de ventas por fichero o FTP en ICG-HioPos].
> 2. La documentación de los datos de **ventas por producto, tickets y cierres de caja**.
> 3. Una credencial **exclusiva** para este uso. Si es posible de solo lectura. Si no, confirmadnos por escrito qué puede hacer.
> 4. Que el acceso quede restringido a la red del local o al equipo que indiquemos, **nunca abierto a Internet**.
> 5. Que confirméis que esto no afecta al soporte ni a la licencia, y el **coste** (puntual o mensual).
> 6. Si hay un entorno de demostración para probarlo antes.
>
> Gracias. Un saludo.

Para otros informáticos o gestorías, usa también [Hablar con el informático](./hablar-con-el-informatico.md).

## Pruébalo gratis

- **Ágora, ICG/HioPos, Haddock, Revo:** no hay prueba gratuita pública. Pide una demo o un entorno de pruebas al distribuidor o a la marca.
- **El resumen del lunes sin tocar el TPV:** empieza con un **Excel** exportado a mano de las ventas de la semana (todos los TPV lo permiten) y tu hoja de escandallos. Si el informe te sirve, pides después la conexión automática.
- **Kross Booking:** demo de 30 días por formulario; no consta si incluye la API.

## Preguntas de alumnos

1. **¿Cómo conecto mi TPV Ágora para sacar ventas?** Con el módulo Integration Services, que activa tu distribuidor. Recibes un token y el servidor del local debe estar encendido. No hay documentación pública: se pide al distribuidor [1].
2. **¿Y si mi TPV es HioPos?** No tiene API pública. Pide al distribuidor una exportación automática de ventas (así lo hace Haddock). Si no la da, valora el acceso de solo lectura a la base de datos [5].
3. **¿Puedo hacer alertas de margen con Haddock y Excel?** Sí: exporta costes de Haddock a Excel o CSV, cruza con las ventas del TPV por código y fija el umbral de margen. Haddock no ofrece API de lectura [4].
4. **¿Qué es mejor para escandallos: un proyecto con skills o GPTs?** Da igual la herramienta si el cálculo lo hace código u hoja y la IA solo lo explica. Lo importante es una tabla limpia de ingredientes y platos.
5. **¿Puede la IA reservar mesa por WhatsApp y apuntarla en mi sistema?** Sí, por la vía oficial de Meta (no apps no oficiales) y con una persona al mando. Depende de que tu sistema de reservas acepte entrada de datos: si no, entra en una hoja compartida.
6. **Quiero que entren los albaranes en el ERP, casarlos con las facturas y pasarlos a contabilidad.** El agente casa y prepara el fichero de importación; tú lo apruebas e importas. No escribe en la base de datos [ver receta de albaranes].
7. **¿Puede el agente cambiar los precios de la carta en el TPV?** No. Solo lectura. El agente prepara el cambio en una hoja y lo aplicas tú.
8. **Tengo dos restaurantes: ¿qué plan de IA pago?** Mira [planes, privacidad y costes](./planes-privacidad-y-costes.md): depende de si trabajas con datos de clientes y de cuántas personas usan la IA.
9. **¿Puedo sustituir SaaS de pago por herramientas propias?** A veces sí para informes (el resumen del lunes). Para lo que escribe en el TPV o la contabilidad, no compensa.

## Errores típicos

- **Pedir «acceso a todo» al distribuidor.** Pide solo ventas, cierres y productos, con una credencial exclusiva.
- **Abrir el puerto del TPV a Internet** para «probar». Nunca. Usa el equipo local o un túnel.
- **Dar al agente el token de la cuenta maestra** o el del administrador.
- **Dejar que la IA calcule márgenes de cabeza.** Calcula con código u hoja y compara con un total de control.
- **Comparar ventas con IVA contra costes sin IVA.** Define una vez qué es «venta» y no lo cambies.
- **Confiar en un escandallo con precios de hace seis meses.** Fecha el último precio de cada ingrediente.
- **Pasar la clave por el chat, el correo o WhatsApp.** Va en `.env`.

## Fuentes

1. Guías de Ágora (token y conector Haddock): https://help.deliverect.com/en/articles/7979177-igt-agora-obtain-the-api-token y https://support.haddock.app/en/article/agora-connector-new-and-recommended-17aizdf/ (consultado el 2026-10-09; la ficha del catálogo, no una documentación oficial pública de Ágora).
2. Precios e integraciones de Ágora: https://www.agorapos.com/pricing/ (consultado el 2026-10-09, según ficha del catálogo).
3. API de Revo XEF, informes v3: https://api.revo.works/sections/xef.html (consultado el 2026-10-09).
4. Exportación de Haddock (documentos, productos, Excel o CSV): https://support.haddock.app/en/article/export-faq-1dt1xab/ y https://pos-api.haddock.app/docs (consultado el 2026-10-09).
5. HioPos y Haddock (exportación por FTP): https://support.haddock.app/en/article/hiopos-connect-pos-tnuuwm/ y https://www.hiopos.com/es/ (consultado el 2026-10-09; sin documentación pública de API).
6. Veri\*factu, nota de la Agencia Tributaria: https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/nota-informativa-ampliacion-plazo-adaptacion-facturacion.html (consultado el 2026-10-09, según ficha del catálogo).

## Relacionado
- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md)
- [Mi programa no tiene API](./mi-programa-no-tiene-api.md)
- [Kit puente, parte técnica](./kit-puente-tecnico.md)
- [Escribir en contabilidad por importación](./escribir-en-contabilidad-por-importacion.md)
- [Tu Excel como fuente de datos](./excel-y-hojas-de-calculo.md)
- [Conectar WhatsApp](./conectar-whatsapp.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Conectar o migrar](./conectar-o-migrar.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Receta: el resumen del lunes](./resumen-del-lunes.md)
- [Receta: presupuestos, pedidos y albaranes](./presupuestos-pedidos-albaranes.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
