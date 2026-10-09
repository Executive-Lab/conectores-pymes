---
type: article
title: "Receta: WhatsApp a pedidos y reservas"
description: Cómo montar un asistente de WhatsApp que toma pedidos o reservas, consulta stock o disponibilidad y los registra en el ERP o en una hoja, con la Cloud API oficial, n8n y escalado a una persona.
tags: [receta, whatsapp, pedidos, reservas, n8n, cloud-api]
timestamp: 2026-10-09T13:45:00Z
topic: recetas
status: draft
sources: ["https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started", "https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.whatsapptrigger/"]
score: 0.0
---

# Receta: WhatsApp a pedidos y reservas

## En resumen
El cliente escribe por WhatsApp. El asistente entiende el pedido o la reserva, consulta stock o disponibilidad, confirma con el cliente, lo registra (pedido en borrador en el ERP o fila en la hoja) y avisa al negocio. Si no entiende algo o el cliente lo pide, pasa la conversación a una persona.

## Lo que hay que saber antes

1. **La app WhatsApp Business no tiene API.** Hay que pasar el número a la **WhatsApp Business Platform (Cloud API)**. Con la **coexistencia** se sigue usando la app en el móvil, pero el alta la hace un proveedor (BSP). Ver el [catálogo](https://executive-lab.github.io/conectores-pymes/).
2. **Nada de "trucos"** que leen WhatsApp Web (whatsapp-web.js, Baileys): Meta bloquea el número, a veces para siempre.
3. **Política de Meta (desde el 15-1-2026)**: no se permiten asistentes de IA generalistas. Un bot de atención del propio negocio sí, y con escalado a una persona.
4. **Ventana de 24 h**: tras el último mensaje del cliente, respuestas libres. Fuera de esa ventana, solo plantillas aprobadas (de pago).
5. **Claude Code no es el servidor**: no "escucha" WhatsApp. El que está siempre activo es **n8n** (o un servicio propio con el Agent SDK). Claude Code construye y mantiene el flujo.

## Arquitectura

```
Cliente → WhatsApp (Cloud API) → n8n: WhatsApp Trigger
        → nodo de agente IA con herramientas de LECTURA (stock, horarios, carta o catálogo)
        → ¿pedido o reserva completo? → crear BORRADOR (ERP) o fila (Sheets) → confirmar al cliente
        → ¿duda, queja o "quiero hablar con alguien"? → avisar a una persona (Telegram o Slack) y pausar el bot en ese chat
        → resumen diario al dueño
```

## Variantes

| Negocio | Registro | Lectura | Nota |
|---------|----------|---------|------|
| Asador o comida por encargo (stock limitado: "quedan 150 pollos") | Google Sheets con contador por franja horaria | La misma hoja | El contador se descuenta **en el mismo paso** que confirma, nunca antes, para no vender de más |
| Distribución con Business Central | Pedido de venta **borrador** (MCP oficial de BC o API) | Artículos y precios de cliente (solo lectura) | Una persona valida el pedido en BC |
| Restaurante con TPV y sistema de reservas | API del sistema de reservas o Sheets | Disponibilidad | Si el TPV es local (Ágora o ICG), las reservas no van al TPV |
| Leads de anuncios Click-to-WhatsApp | CRM (HubSpot, Odoo CRM, Notion) | Ficha del lead | Calificar con preguntas cortas y pasar a comercial |
| Alquiler vacacional (huéspedes) | PMS si tiene API; si no, Sheets | Reserva y check-in | Plantillas aprobadas para mensajes fuera de la ventana |

## Paso a paso

1. **Probar gratis**: app en developers.facebook.com → número de prueba de la Cloud API (gratis, hasta 5 destinatarios verificados) → n8n WhatsApp Trigger.
2. **Skill de conocimiento** en el arnés: carta o catálogo, precios, horarios y políticas en `02-DOCS/wiki/negocio/`. Claude Code genera a partir de ahí el prompt del nodo de agente de n8n. Una sola fuente.
3. **Herramientas del agente en n8n**: solo **lectura** (stock, disponibilidad), más **una** acción de escritura acotada (crear borrador o fila).
4. **Escalado**: palabra clave o duda → aviso a una persona y el bot deja de responder en ese chat hasta que lo reactiven.
5. **Producción**: alta del número real en coexistencia con un BSP; usuario del sistema con acceso solo a esa WABA; token en las credenciales de n8n.

## Permisos y seguridad

- El token de WhatsApp envía y recibe: no hay scope de solo lectura. Vive solo en n8n.
- Los mensajes de los clientes son **contenido no fiable**: el agente no ejecuta lo que "diga" un mensaje. Herramientas mínimas y escrituras acotadas.
- Nada de datos de otros clientes en las respuestas.

## Coste orientativo

Cloud API sin cuota fija. Las respuestas dentro de la ventana de 24 h son gratis o casi; las plantillas de utilidad cuestan unos 0,017 € y las de marketing unos 0,05-0,06 € en España (verificar: Meta cambió precios en julio y octubre de 2026). A eso se suma el BSP si se usa coexistencia, y n8n (0 € self-hosted, desde 20 €/mes en cloud).

## Demo en clase (0 €)

Número de prueba de Meta + n8n self-hosted + Google Sheets como stock. Caso del asador: "¿Me guardas 2 pollos para las 14:00?" → descuenta el contador y confirma.

## Errores típicos

- Montarlo sobre la app con un "truco" y perder el número.
- Bot que no sabe callarse cuando el dueño contesta a mano: hace falta la pausa por chat.
- Plantillas no aprobadas el día del lanzamiento: se piden con días de antelación.

## Relacionado
- [Cómo se monta](./como-se-monta.md) · [Hablar con el informático (plantilla F, BSP)](./hablar-con-el-informatico.md)
