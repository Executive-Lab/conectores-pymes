---
type: article
title: Cómo hablar con tu informático (o tu distribuidor) para conectar tus herramientas
description: Guía para alumnos — qué pedir, con qué palabras y qué no aceptar, según tengas una herramienta web, Google/Microsoft, un programa instalado o WhatsApp.
tags: [guia-alumnos, informatico, seguridad, plantillas]
timestamp: 2026-10-09T10:30:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Cómo hablar con tu informático (o tu distribuidor) para conectar tus herramientas

> Para: alumnos de Executive Lab. Copia el texto que te toque, cambia lo que va entre `<…>` y envíalo.

## En resumen
La mayoría de las veces no necesitas a nadie: si tu herramienta es web, la clave la generas tú (ver [cómo conectar una plataforma](./conectar-una-plataforma-con-rsc.md)). Necesitas a tu informático en tres casos:

- **Google Workspace o Microsoft 365**, porque hace falta un administrador.
- **Programas instalados** en la oficina (Sage 50/200, Contasol, Presto, Instalwin, A3, TPV local…).
- Cualquier cosa que **otra persona controla**: gestoría, distribuidor, agencia.

Tu informático no tiene por qué saber qué es un "arnés de IA". Pídele cosas concretas y conocidas: **una credencial de solo lectura, a nombre de una integración, con el mínimo acceso**.

## Antes de escribir: cinco datos

1. Nombre exacto y versión del programa (por ejemplo "Sage 200 2025", "Contasol 2026").
2. Dónde está instalado: nube del fabricante, servidor de la oficina o el PC de alguien.
3. Quién lo mantiene: informático propio, distribuidor o el fabricante.
4. Qué datos necesitas, en concreto: "facturas emitidas y recibidas de los últimos 12 meses", no "todo".
5. Si solo vas a **leer** o también a **escribir**. Empieza por leer.

## Plantillas

### A. Programa instalado (Sage, Contasol, Presto, Instalwin, TPV local…)

> Hola `<nombre>`. Quiero automatizar `<informes de ventas y cobros / la entrada de facturas>` con una herramienta de IA. Necesito que lea datos de `<programa y versión>`. Por orden de preferencia:
>
> 1. ¿El fabricante o vosotros tenéis **API o módulo de integración** para este programa? ¿Qué cuesta?
> 2. Si no, ¿puede el programa **exportar automáticamente** cada noche `<facturas, clientes, stock>` a CSV o Excel en una carpeta?
> 3. Si no, ¿me podéis crear un **usuario de base de datos de solo lectura**, limitado a `<estas tablas o vistas>`, accesible solo por VPN?
>
> No necesito escribir nada en el programa. No quiero abrir puertos a internet ni usar el usuario administrador. ¿Qué opción veis y cuánto costaría?

### B. Google Workspace (administrador de la cuenta)

> Hola `<nombre>`. Voy a conectar una herramienta de automatización a Google. Necesito que, como administrador de Workspace, autorices una aplicación con estos **permisos de solo lectura**: `<gmail.readonly / drive.readonly / spreadsheets.readonly / calendar.readonly>`. Si se puede, limítalo a `<esta carpeta de Drive o este buzón>`. No necesita permisos de escritura ni de administración. ¿Me dices cuándo lo tienes?

### C. Microsoft 365 (Outlook, Excel, OneDrive, SharePoint, Teams)

> Hola `<nombre>`. Necesito registrar una aplicación en **Entra ID** para que una herramienta lea `<estos correos / este Excel / este sitio de SharePoint>`. Pido **permisos delegados de solo lectura** (`Mail.Read`, `Files.Read`…) o, si tiene que funcionar sin mí, **permisos de aplicación limitados** (por ejemplo `Sites.Selected` solo para el sitio `<nombre>`). Necesitaré el consentimiento de administrador. Nada de permisos de escritura sobre todo el tenant. ¿Lo vemos?

### D. Herramienta web que lleva otra persona (gestoría, agencia, socio)

> Hola `<nombre>`. ¿Me puedes crear en `<Holded / Odoo / HubSpot…>` una **clave de API o un usuario de integración de solo lectura**, a nombre de "rsc-lectura"? La voy a usar para generar informes automáticos. Si la herramienta no permite limitar permisos, dímelo antes y lo hablamos.

### E. WhatsApp Business

Aquí no es tu informático: es Meta. La **app** WhatsApp Business del móvil no tiene API. Para automatizar hay que pasar a la **WhatsApp Business Platform (Cloud API)**, directamente con Meta o con un proveedor (BSP). Pregunta al proveedor:

> ¿Puedo seguir usando la app en el móvil a la vez que la API ("coexistencia") con el mismo número? ¿Cuánto cuesta al mes y por conversación? ¿Me dais acceso por API o solo por vuestro panel?

No uses "trucos" no oficiales (programas que leen WhatsApp Web): Meta puede **bloquear tu número**.

## Si te dicen "eso no se puede"

Pregunta:

1. "¿Se puede **exportar** a Excel o CSV, aunque sea a mano?" Si sí, ya hay por dónde empezar.
2. "¿El fabricante tiene **partners o integradores** que lo conecten?"
3. "¿Hay **versión en la nube** del programa?" Suelen traer API.
4. "¿Qué haría falta para que fuese **solo lectura y sin abrir nada a internet**?"

## Lo que NO debes aceptar

- Que te den la **contraseña del administrador** o el usuario de otra persona.
- **Abrir el puerto de la base de datos a internet** "para que funcione".
- Una clave que lo puede todo cuando solo necesitas leer, si existe una opción limitada.
- Mandar contraseñas o claves por **email o WhatsApp**. Se pegan directamente en `01-TOOLS/<X>/.env`.

## Mini glosario

| Palabra | Qué es, en una línea |
|---------|----------------------|
| API | La puerta por la que un programa habla con otro sin pantalla. |
| Clave de API | La llave de esa puerta. Quien la tiene, entra. |
| Scope / permiso | Lo que esa llave deja hacer: leer facturas, enviar emails… |
| Solo lectura | Puede mirar, no puede cambiar nada. |
| OAuth | Forma de dar permiso a una app sin darle tu contraseña ("Iniciar sesión con Google"). |
| Usuario de integración | Un usuario que no es una persona, creado solo para la conexión. |
| MCP | Enchufe estándar para que un agente de IA use una herramienta. |
| Webhook | Aviso automático que una herramienta manda cuando pasa algo. |
| VPN | Túnel privado para llegar a la red de la oficina sin abrirla a internet. |
| RPA | Robot que usa la pantalla como una persona. Último recurso. |

## Relacionado
- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md).
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/): qué pedir para cada plataforma concreta.
