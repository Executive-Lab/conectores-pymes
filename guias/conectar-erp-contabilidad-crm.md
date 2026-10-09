---
type: article
title: Conectar tu ERP, tu contabilidad o tu CRM
description: Manual para alumnos con 18 productos de ERP, contabilidad y CRM (Holded, Sage, Odoo, Business Central, SAP, HubSpot, Salesforce...): qué vía usar, qué permisos dar y qué pedir a tu informático o gestoría.
tags: [guia-alumnos, erp, contabilidad, crm, solo-lectura, verifactu]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Conectar tu ERP, tu contabilidad o tu CRM

> Para: dueños y directivos de pyme que usan Holded, Sage, Contasol, Odoo, Business Central, SAP, un CRM u otro programa de gestión.
> Conseguirás: saber qué vía te toca, dar a tu agente un acceso de solo lectura y no romper la contabilidad por el camino.

## Overview

En clase salen unos veinte programas distintos y el curso no se ata a ninguno. Este manual ordena todos con el mismo criterio. Una **API** es una ventanilla por la que otro programa pide datos. Un **MCP** es un enchufe estándar para que el agente use esa ventanilla sin que programes nada.

Resumen de lo que hay (datos del catálogo, verificados el 2026-10-09):

- **Con MCP oficial hoy**: Business Central, Odoo 20, HubSpot, Zoho CRM, monday CRM, GoHighLevel y Salesforce [3][2][4][5].
- **Con API de autoservicio pero sin MCP oficial**: Holded, Sage Active, Clientify, SAP Business One. Se conectan con una clave o una app, tú mismo.
- **Con puente**: Sage 50, Sage 200, Sage Despachos, Contasol/Factusol local, CONTPAQi, Contasimple. Aquí manda tu informático, tu distribuidor o tu gestoría.
- **Tiempo**: 15 minutos a una tarde si el producto es de autoservicio. Semanas si hay que pedir credenciales a un partner.
- **Vía recomendada**: MCP oficial o API con un usuario dedicado, **solo lectura**. Escribir viene después y con tu aprobación.

Guía base: [conectar una plataforma](./conectar-una-plataforma-con-rsc.md). Textos para pedir cosas: [hablar con el informático](./hablar-con-el-informatico.md).

## Antes de empezar

1. Averigua qué tienes: nombre y versión exactos (menú Ayuda > Acerca de) y si es web, instalado en la oficina o mixto.
2. Averigua quién lo administra: tú, un informático, un distribuidor o tu gestoría. Si el programa es de la gestoría (Sage Despachos), le pides a ella, no a tu informático.
3. Un usuario o app **dedicada** para el agente (`IA-lectura`). Nunca tu cuenta ni la de administrador.
4. Si el producto tiene datos personales, revisa antes tu plan de IA: [planes, privacidad y costes](./planes-privacidad-y-costes.md).

## Las vías, de mejor a peor

| Producto | Vía principal | MCP oficial | Solo lectura posible | Quién actúa | Demo gratis | Dificultad |
|---|---|---|---|---|---|---|
| Holded | API v2 con token | No (comunitarios) | Sí, por módulo | Tú (rol Developer) | 14 días | Media |
| Sage 50 | BD SQL de solo lectura | No | Sí, con login SQL | Informático + distribuidor | Bajo petición | Difícil |
| Sage 200 | SQL de solo lectura; API con programa de desarrolladores | No | Sí, con login SQL | Partner de Sage | Bajo petición | Difícil |
| Sage Despachos | Exportaciones de la gestoría | No | Sí, por exportación | Tu gestoría | No público | Difícil |
| Sage Active | API GraphQL con OAuth | No (sin fecha) | Sí, scope de lectura | Tú o tu admin | 30 días | Media |
| Contasol / Factusol | API de la Nube DELSOL; si es local, copia de la BD | No | Sí, por empresa y área (Nube) | Tú + alta de fabricante | 30 días (Nube) | Media (Difícil en local) |
| Contasimple | API OAuth con credenciales a pedir | No | No | Tú + Contasimple | Plan Básico gratis | Media |
| Odoo | API JSON-2 o MCP nativo | Sí (Odoo 20, saas-19.4) | Con usuario bot de permisos mínimos | Tú o tu informático | Community gratis | Fácil |
| Business Central | MCP oficial u OAuth con Entra | Sí | Sí, configuración MCP con Allow Read | Admin de Microsoft 365 | 30 días | Media |
| SAP Business One | Service Layer (OData v4) | No (comunitarios) | Sí, usuario B1 de solo lectura | Partner de SAP | Bajo petición | Media |
| SAP S/4HANA | OData vía BTP | No | Sí, con CDS views de lectura | Partner de SAP | Sandbox gratis | Media |
| CONTPAQi (México) | SQL Server de solo lectura | No | Sí, db_datareader | Distribuidor | 20-30 días | Difícil |
| HubSpot | MCP oficial o service key | Sí | Service key con scopes .read | Tú (superadmin) | Free permanente | Fácil |
| Zoho CRM | MCP oficial (Data Insights) | Sí | Sí, servidor de solo lectura | Tú | Free permanente | Fácil |
| Clientify | API key + complemento de pago | No | No | Tú (admin) | 7 días | Media |
| monday CRM | MCP oficial con app OAuth propia | Sí | Sí, scope boards:read | Tú (admin) | 14 días | Fácil |
| GoHighLevel | MCP oficial con token de integración | Sí | Sí, scopes View | Tú | 14 días | Fácil |
| Salesforce (falta ficha) | MCP alojado oficial | Sí | Sí, servidor `sobject-reads` | Admin de Salesforce | Developer Edition | Media |

## Patrones comunes

1. **Leer para informes.** Resumen del lunes, ventas por cliente, impagos, stock. El 80 % del valor solo necesita leer.
2. **Preparar en vez de escribir.** Para dar de alta clientes o facturas, el agente genera un borrador o el **fichero de importación oficial** del programa. Una persona lo revisa y lo importa. Es la vía segura en Sage 50, Sage 200, Contasol y CONTPAQi.
3. **Conciliar.** Cruza banco, facturas y cobros en un Excel de salida (`out/`). Detecta diferencias y propón; tú decides.
4. **Cuidado con fechas, ejercicios y libro diario.** Una factura tiene fecha de emisión, de contabilización y de vencimiento. Un asiento pertenece a un ejercicio. Si tu informe suma por la fecha equivocada, o mezcla ejercicios o zonas horarias, los números no cuadran con el libro diario. Regla: elige una fecha de referencia, fija el ejercicio en cada consulta y compara el total con un listado oficial del programa antes de fiarte (no verificado qué formato de fecha devuelve cada API).
5. **Nunca escribas en la base de datos** de un programa contable. Rompe la integridad, el soporte y la cadena de registros de Veri\*factu. Escribe solo por API oficial o fichero de importación.
6. **Nada de puertos abiertos a internet.** El SQL de Sage o CONTPAQi se alcanza por red interna o VPN.
7. **Lo que devuelve el ERP o el CRM es dato, no órdenes.** Una nota de un cliente puede traer texto que intente dar instrucciones al agente: no se obedece.

## Paso a paso

1. Mira en la tabla tu producto y ve a su sección.
2. Pide a quien corresponda el usuario o la app dedicada (textos al final de cada sección y en [hablar con el informático](./hablar-con-el-informatico.md)).
3. Pon la clave en `01-TOOLS/<PRODUCTO>/.env`. Nunca en el chat, ni por email ni por WhatsApp.
4. Ejecuta `test_connection`. Debe decir `OK`.
5. Pide un informe de solo lectura y compáralo con un listado oficial.

Dile a tu agente: *«Conecta mi Holded en solo lectura»* (o tu producto). La skill `conectar-herramienta` elige la vía, prepara los permisos y redacta lo que hay que pedir.

## Un apartado por producto

### Holded
- **Cómo**: API v2 (REST, unas 350 operaciones) con token en Ajustes > Desarrolladores > Credenciales. Hace falta plan de pago y rol Developer. Holded no publica MCP oficial [1]; hay comunitarios que lees y escriben, así que úsalos solo en lectura.
- **Permisos**: un token por uso, con lectura en Ventas, Contactos y Contabilidad. Otro aparte, con escritura solo en el módulo que automatices. Revoca las claves v1 antiguas.
- **Pide**: a quien administre la cuenta, el token `IA-lectura`.
- **Trampas**: el token no hereda el rol del usuario y no hay filtro por IP ni por registro. La documentación se queja de ser escasa; prueba cada consulta contra un listado.

### Sage 50
- **Cómo**: no hay API pública ni MCP. Se lee el SQL Server Express que instala Sage 50, con un login propio de solo `SELECT` sobre vistas. Escribir exige el add-on de pago (eConnect, precio no publicado).
- **Pide**: al informático un login `ia_lectura`, accesible solo desde la máquina del arnés.
- **Trampas**: las actualizaciones pueden cambiar el esquema o la contraseña. Para crear asientos, usa el fichero de importación de asientos.

### Sage 200
- **Cómo**: API REST local con Swagger y OAuth, pero exige el «API 200 Developer Program» y el partner debe activar el servicio. La comunidad no consigue sacar el token. Confianza baja en la ficha.
- **Pide**: al partner si la API está activa y cuánto cuesta el programa. Mientras tanto, login SQL de solo lectura sobre vistas.
- **Trampas**: no hay MCP oficial. Unified.to y CData son de pago.

### Sage Despachos Connected
- **Cómo**: no hay API ni MCP. El programa es de tu gestoría.
- **Pide**: a la gestoría que exporte periódicamente modelos, balances y nóminas en Excel o PDF a una carpeta compartida.
- **Trampas**: la base de datos contiene los datos de todos los clientes del despacho. No se conecta entera.

### Sage Active
- **Cómo**: API GraphQL con OAuth 2.0, sin client credentials. Claves en «Your Sage Active» > Configuración > API pública. No hay MCP oficial; Sage ha dicho que lo evolucionará, sin fecha [6].
- **Permisos**: pide solo el scope de lectura y autoriza con un usuario dedicado.
- **Trampas**: hay que guardar el refresh token. Una regla de negocio fallida responde HTTP 200 con el error dentro. No se vende en territorios forales ni Canarias (según fuente secundaria).

### Contasol / Factusol
- **Cómo**: solo hay API si tienes los datos en la Nube de DELSOL. Alta de fabricante gratuita, y luego Archivo > Seguridad > Acceso por API, con empresa, área y permisos.
- **Pide**: acceso de solo lectura. Si estás en local, una copia nocturna de la base de datos o un export XLSX en una carpeta.
- **Trampas**: la documentación llega tras el alta. Pasar a la Nube del mismo programa es la forma de tener API sin cambiar de software.

### Contasimple
- **Cómo**: API OAuth2 cuyas credenciales (Client Id y Secret) se piden a Contasimple. No hay referencia pública de endpoints de negocio.
- **Trampas**: no se puede limitar a solo lectura y los términos prohíben dar acceso a terceros. Plan B: exportar a Excel.

### Odoo
- **Cómo**: API JSON-2 (Odoo 19 o superior) o MCP nativo en `https://<bd>.odoo.com/mcp` (Odoo 20, saas-19.4), con clave API [2]. En Odoo Online la API exige el plan Personalizado; la doc del MCP no aclara qué plan o edición hacen falta.
- **Permisos**: usuario interno `IA-bot` con grupos mínimos. La clave hereda lo que pueda hacer el usuario. «Readonly Tool» solo evita pedir confirmación, no es seguridad [2].
- **Trampas**: las claves caducan como máximo a los 3 meses; planifica la rotación. XML-RPC desaparece en Odoo 22.

### Business Central
- **Cómo**: MCP oficial en `https://mcp.businesscentral.dynamics.com` (solo BC online). Por defecto expone herramientas de lectura sobre las APIs que el usuario puede ver; escribir exige activar las herramientas de edición [3]. Claude necesita una app propia registrada en Entra.
- **Pide**: al admin la app, un usuario `IA` con permission sets de solo lectura y una configuración MCP propia con solo Allow Read. Pasa siempre `ConfigurationName`.
- **Trampas**: en Entra el permiso es siempre ReadWrite; el límite real son los permission sets. Make solo lo ofrece en su plan Enterprise.

### SAP Business One
- **Cómo**: Service Layer (OData v4), incluido en B1 10.0. Cada usuario de API consume una licencia. Los MCP son comunitarios.
- **Pide**: al partner un usuario B1 de solo lectura, accesible por red interna o VPN.
- **Trampas**: hay que comprar la licencia a un partner. Varios MCP guardan la contraseña en texto plano. Analítica con Claude Code: sí es posible, en solo lectura.

### SAP S/4HANA
- **Cómo**: OData vía SAP Gateway o Communication Arrangement. Sandbox gratis en SAP Business Accelerator Hub para practicar.
- **Trampas**: la SAP API Policy v4.2026a restringe que agentes de IA usen las APIs fuera de rutas avaladas (Joule, Integration Suite). Pide al partner confirmación escrita antes de conectar.

### CONTPAQi (México)
- **Cómo**: no hay API REST oficial. Se lee SQL Server con un usuario de solo lectura. El SDK de terceros es de pago. Confianza baja.
- **Trampas**: escribir por SQL se salta las reglas y el timbrado. El CFDI 4.0 sustituye a Veri\*factu.

### HubSpot
- **Cómo**: MCP remoto en `https://mcp.hubspot.com`, disponible para todas las cuentas desde el 13-abr-2026. Se crea una «MCP Auth App» en Desarrollo [4]. Para n8n o scripts, service key con scopes `.read`.
- **Permisos**: conecta con un usuario dedicado de solo ver. El MCP no tiene interruptor de solo lectura y puede crear y actualizar contactos, empresas, negocios y tickets [4].
- **Trampas**: si tienes activados los datos sensibles, el MCP bloquea las actividades.

### Zoho CRM
- **Cómo**: cuatro MCP oficiales. Instala solo **Data Insights**, el de solo lectura. La cuenta española suele estar en el centro de datos `.eu` (disponibilidad del MCP allí, no verificada).
- **Trampas**: gasta créditos de API compartidos con otras integraciones.

### Clientify
- **Cómo**: API v2 con key. Exige contratar el complemento «Acceso por API Key» (unos 12 €/mes en anual). No hay MCP.
- **Trampas**: la key da acceso a toda la cuenta y no tiene scopes. Guárdala en n8n y deja que el agente llegue solo a flujos concretos.

### monday CRM
- **Cómo**: MCP oficial en `https://mcp.monday.com/mcp`. Crea una app OAuth propia con solo `boards:read` y desactiva el conector genérico. Alternativa: el paquete local con `--read-only`.
- **Trampas**: el token personal no tiene scopes. Las llamadas MCP cuentan contra el límite diario de la API.

### GoHighLevel
- **Cómo**: token de integración privada (PIT) de **subcuenta**, solo con scopes View, más el `locationId`.
- **Trampas**: la documentación oficial se contradice sobre PIT y OAuth. Un PIT de agencia da acceso a todas las subcuentas. Rótalo cada trimestre.

### Salesforce (falta ficha en el catálogo)
- **Cómo**: Salesforce tiene servidores MCP alojados, con GA en abril de 2026 según fuentes secundarias. Un admin los activa en Setup > API Catalog > MCP Servers. El servidor `sobject-reads` es de solo lectura. Se autentica con una External Client App (OAuth con PKCE) y cada llamada va con los permisos del usuario [5].
- **Edición**: se cita Enterprise o superior; Developer Edition gratis para probar. No verificado en la documentación oficial: confírmalo con tu admin.
- **Pide**: al admin un usuario de integración con permisos mínimos y solo `sobject-reads`.
- **Falta ficha**: pendiente de añadir al catálogo con fuentes primarias.

## Veri\*factu y factura electrónica: qué implica al conectar

- Veri\*factu afecta a **quien emite facturas**. Si solo lees, no cambia nada. Si automatizas facturas emitidas, el programa debe estar adaptado y la factura debe pasar por él.
- **Nunca** crees facturas escribiendo en la base de datos: rompes la cadena de registros.
- Pide por escrito la **declaración responsable** del fabricante, con la versión exacta. La AEAT no homologa programas. Con declaración localizada en el catálogo: Odoo, Business Central, Contasimple y Factusol (desde 2025.0.13).
- Fechas: las legales hoy son 1-ene-2027 (Sociedades) y 1-jul-2027 (resto). El 5-oct-2026 Hacienda anunció una previsión de aplazamiento a octubre de 2028, aún sin norma. La factura electrónica B2B llega el 6-oct-2027 (más de 8 M€) y el 6-oct-2028 (resto), según el catálogo.
- Si tu programa no se adapta, mira [conectar o migrar](./conectar-o-migrar.md). Receta de emisión: [facturas emitidas y Veri\*factu](./facturas-emitidas-y-verifactu.md) (receta nueva, aún por escribir).

## Qué pedir a tu informático

> Necesito un acceso de **solo lectura** para un agente de IA a [producto]. Crea un usuario o app dedicada («IA-lectura»), con el mínimo permiso, sin usar mi cuenta ni la de administrador. Si hay base de datos, que solo pueda hacer `SELECT` sobre las vistas que acordemos y que no esté abierta a internet (red interna o VPN). Pásame la clave por un canal seguro, no por email ni WhatsApp. Dime también si tiene coste de licencia y cuándo caduca.

## Pruébalo gratis

Odoo Community en local (0 €), sandbox de SAP, plan Básico de Contasimple, Free de HubSpot y Zoho, prueba de 30 días de Business Central, 14 días de Holded, Developer Edition de Salesforce. Sage 50, Sage 200 y SAP B1 solo se prueban con un partner. Usa siempre una empresa de pruebas, nunca la real.

## Qué puedes automatizar después

- [Resumen del lunes](./resumen-del-lunes.md) · [Facturas a contabilidad](./facturas-a-contabilidad.md) · [Leads y atención](./leads-y-atencion.md) · [Fuente única](./fuente-unica.md) · [WhatsApp a pedidos](./whatsapp-a-pedidos.md).
- Nuevas: [presupuestos, pedidos y albaranes](./presupuestos-pedidos-albaranes.md) y [facturas emitidas y Veri\*factu](./facturas-emitidas-y-verifactu.md).

## Preguntas de alumnos

**¿Holded tiene API y qué limitaciones tiene?** Sí, API v2 con tokens por módulo, en cualquier plan de pago. No hay MCP oficial, no hay filtro por IP ni por registro, y hay un límite mensual de llamadas según plan.

**Mi reporting sobre Holded o Business Central da datos mal (fechas, libro diario).** Casi siempre es la fecha elegida o el ejercicio. Fija una fecha de referencia, filtra por ejercicio y cuadra el total con el listado oficial. Si sigue sin cuadrar, revisa si lees documentos de venta o asientos contables.

**¿Se puede conectar Sage 50 o 200?** Sí, con puente. En Sage 50, SQL de solo lectura. En Sage 200, SQL y, si el partner lo activa, la API. No hay MCP oficial en ninguno.

**Con SAP Business One, ¿se puede hacer analítica con Claude Code?** Sí. Usa el Service Layer con un usuario de solo lectura y un MCP comunitario en modo lectura, por VPN. Cada usuario consume licencia.

**¿Puedo dar al agente acceso solo de lectura a mi ERP?** Sí, pero pocas claves son de solo lectura de verdad. Lo son Holded v2, Sage Active y Contasol Nube. En Odoo, Business Central y SAP B1 el límite lo pone el usuario y su rol.

**¿Puedo limpiar datos sucios o duplicados del ERP?** Sí, sin escribir. El agente lee, detecta duplicados y genera un fichero de correcciones. Una persona lo revisa e importa.

**Alta de clientes en el ERP con Power Automate.** Depende del ERP. Con Business Central hay conector oficial (Premium). En el resto, usa la API con aprobación humana antes de crear. Si no hay API, genera el fichero de importación.

**Salesforce, HubSpot o un CRM propio sin API.** HubSpot y Salesforce tienen MCP oficial. En un CRM propio sin API, exporta a Excel o CSV de forma programada y lee la carpeta.

## Errores típicos

1. Dar al agente la clave de administrador o la del dueño.
2. Pegar la clave en el chat.
3. Fiarse de un «solo lectura» que es solo un aviso (Odoo «Readonly Tool», `confirm:true` de Holded).
4. Escribir en la base de datos de Sage o CONTPAQi.
5. Olvidar la caducidad de la clave (Odoo, máximo 3 meses).
6. Conectar Claude a SAP S/4HANA sin confirmar la API Policy.
7. Dar la base de datos de una gestoría entera.
8. Fiarse de un informe sin cuadrarlo con un listado oficial.

## Fuentes

Fichas del catálogo (`catalogo/datos/plataformas`, verificadas el 2026-10-09) para todos los productos, salvo Salesforce.

1. Holded, llms.txt: https://www.holded.com/llms.txt (consultado el 2026-10-09). Sin mención de MCP.
2. Odoo 20, servidor MCP: https://www.odoo.com/documentation/20.0/applications/productivity/ai/mcp_server.html (consultado el 2026-10-09).
3. Business Central, MCP: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/mcp-overview (consultado el 2026-10-09; doc del 2026-10-02).
4. HubSpot, MCP GA: https://developers.hubspot.com/changelog/remote-hubspot-mcp-server-is-now-generally-available (consultado el 2026-10-09).
5. Salesforce, MCP alojado (fuentes secundarias): https://salesforcetime.com/2026/07/15/how-to-connect-claude-with-salesforce-hosted-mcp-servers/ y https://www.cleanlist.ai/blog/2026-10-05-salesforce-mcp-server-review (consultados el 2026-10-09).
6. Sage Active, sin MCP: https://developer.sage.com/sageactive/ (403; búsqueda sin resultados de MCP, 2026-10-09). El dato de «sin fecha» viene de la ficha.

## Related

- [Conectar una plataforma](./conectar-una-plataforma-con-rsc.md) · [Hablar con el informático](./hablar-con-el-informatico.md) · [¿Conectar o migrar?](./conectar-o-migrar.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
