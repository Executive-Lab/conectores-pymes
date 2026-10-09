---
type: article
title: ¿Por dónde empiezo? Qué guía leer según lo que usas y lo que quieres
description: Puerta de entrada para alumnos. En tres preguntas te lleva a la guía de conexión y a la receta que te tocan, sin leer las 20 páginas.
tags: [guia-alumnos, inicio, mapa, recetas, conectores]
timestamp: 2026-10-09T22:30:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# ¿Por dónde empiezo?

> Para: alumnos de Executive Lab que quieren conectar su empresa a la IA y no saben qué leer primero.
> Conseguirás: saber en 5 minutos qué guía y qué receta son las tuyas y cuál es tu primer paso esta semana.

## En resumen
Hay más de 15 guías y 8 recetas. No tienes que leerlas todas. Responde tres preguntas:

1. ¿Qué quieres conseguir primero?
2. ¿Dónde viven hoy tus datos?
3. ¿Quién tiene que mover ficha?

Si no sabes qué es una API o un MCP, lee antes [MCP, API y demás, sin tecnicismos](./mcp-api-y-demas-sin-tecnicismos.md). Son 10 minutos y te ahorran horas.

## 1. ¿Qué quieres conseguir primero?

Elige **una sola cosa**. La primera automatización debe ser de **solo lectura**: tu agente lee y te informa, no toca nada.

| Si quieres… | Tu receta | Por qué empezar aquí |
|-------------|-----------|----------------------|
| Ver cada lunes cómo va la empresa (ventas, caja, cobros, stock) | [Resumen del lunes](./resumen-del-lunes.md) | Es la que más piden los alumnos y la más segura: solo lee |
| Dejar de copiar pedidos a mano, preparar presupuestos, casar albaranes | [Presupuestos, pedidos y albaranes](./presupuestos-pedidos-albaranes.md) | La segunda más pedida, sobre todo en industria, construcción y distribución |
| Que las facturas de proveedor lleguen a la contabilidad sin teclear | [Facturas a contabilidad](./facturas-a-contabilidad.md) | El agente prepara y tú apruebas |
| Facturar a tus clientes, controlar cobros e impagos | [Facturas emitidas y Veri\*factu](./facturas-emitidas-y-verifactu.md) | Ojo: emite tu programa de facturación, no la IA |
| Responder antes a los leads y a los clientes | [Leads y atención](./leads-y-atencion.md) | — |
| Recibir pedidos o reservas por WhatsApp | [WhatsApp a pedidos](./whatsapp-a-pedidos.md) | Antes, lee [Conectar WhatsApp](./conectar-whatsapp.md) |
| Que lo que sabe tu empresa no esté solo en la cabeza de dos personas | [Fuente única](./fuente-unica.md) | — |

## 2. ¿Dónde viven hoy tus datos?

| Si tus datos están en… | Tu guía | Dificultad habitual |
|------------------------|---------|---------------------|
| Excel y correo («todo en Excel y email») | [Tu Excel como fuente de datos](./excel-y-hojas-de-calculo.md) | Fácil: empieza por llevar el Excel a la nube |
| Gmail, Google Drive, Sheets | [Conectar Google Workspace](./conectar-google-workspace.md) | Fácil, salvo que tengas varias cuentas |
| Outlook, Teams, SharePoint, OneDrive | [Conectar Microsoft 365](./conectar-microsoft-365.md) | Fácil para ti; necesitas que el administrador dé un permiso una vez |
| WhatsApp Business | [Conectar WhatsApp](./conectar-whatsapp.md) | Media: hay que pasar a la API oficial |
| Holded, Odoo, Sage, A3, SAP, Business Central, HubSpot, Salesforce… | [Conectar tu ERP, contabilidad o CRM](./conectar-erp-contabilidad-crm.md) | Depende del programa: mira su ficha en el [catálogo](https://executive-lab.github.io/conectores-pymes/) |
| El TPV del bar o del restaurante (Ágora, Revo, ICG/HioPos) y los escandallos (Haddock) | [Conectar el TPV y la gestión de un restaurante](./conectar-tpv-hosteleria.md) | Media: casi siempre por exportación o por informe del TPV |
| Tu tienda online (Shopify, PrestaShop, WooCommerce), marketplaces, pagos y envíos | [Conectar tu tienda online](./conectar-tienda-online.md) | Fácil-media: casi todas tienen API o MCP |
| Meta Ads, Instagram, Google Ads, Metricool | [Conectar Meta Ads y tus redes](./conectar-meta-ads-y-redes.md) | Media: hay que dar acceso de solo lectura a la cuenta publicitaria |
| Un programa instalado en el ordenador de la oficina, sin API | [Mi programa no tiene API](./mi-programa-no-tiene-api.md), y para tu informático el [kit puente técnico](./kit-puente-tecnico.md) | Media-alta: se lee por exportación o con una base de datos de solo lectura |
| Quieres que la IA **escriba** en tu contabilidad | [Escribir en contabilidad por importación](./escribir-en-contabilidad-por-importacion.md) | Nunca directamente en la base de datos: siempre por fichero de importación |

¿No sabes si tu programa tiene API? En [MCP, API y demás](./mcp-api-y-demas-sin-tecnicismos.md) hay 5 comprobaciones. ¿Te planteas cambiar de programa? Lee [¿Conectar o migrar?](./conectar-o-migrar.md).

## 3. ¿Quién tiene que mover ficha?

| Situación | Qué hacer |
|-----------|-----------|
| Tú administras la herramienta (eres el dueño de la cuenta) | Hazlo tú. Dile a tu agente: *«Conecta mi <herramienta> en solo lectura»* |
| Hay un administrador de Microsoft o de Google en tu empresa | Mándale el texto de tu guía (sección «Qué pedir a tu informático») |
| El programa lo instaló un informático o un distribuidor | Usa [Cómo hablar con tu informático](./hablar-con-el-informatico.md): plantillas listas para copiar |
| Vas a subir datos de clientes, nóminas o salud | Antes de nada, [qué plan de IA pagar y qué pasa con tus datos](./planes-privacidad-y-costes.md) |

## Tu primer paso esta semana

1. Elige **una** receta de la tabla 1.
2. Conecta **una** fuente de la tabla 2, en solo lectura.
3. Monta la receta con tu agente. Si usas el arnés RSC, la skill `conectar-herramienta` te guía.
4. Cuando funcione una semana seguida, añade la segunda fuente.

## Cuando ya tengas algo funcionando

- ¿Skill, agente, automatización? ¿Un arnés o varios? → [Decisiones del arnés](./decisiones-del-arnes.md)
- ¿Cómo se monta para que corra solo? → [Cómo se monta una automatización](./como-se-monta.md)
- ¿Dónde se explicó algo en clase? → Índice de clases y directos

## Relacionado
- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md) · [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
