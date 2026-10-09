---
type: article
title: "Receta: leads y atención al cliente con propuesta en menos de 24 h"
description: Cómo montar la entrada de leads o consultas (formulario, email, anuncios) con ficha automática en el CRM, propuesta o respuesta redactada por IA a partir del conocimiento del negocio y envío solo tras aprobación.
tags: [receta, leads, crm, atencion-cliente, n8n, routine, aprobacion]
timestamp: 2026-10-09T14:00:00Z
topic: recetas
status: draft
sources: []
score: 0.0
---

# Receta: leads y atención al cliente

## Overview

Entra un contacto (formulario web, email, anuncio de Meta o Google, WhatsApp). Se crea o actualiza su ficha en el CRM. La IA lo califica y redacta la propuesta o la respuesta **con el conocimiento del negocio** (catálogo, precios, casos, tono). Una persona la revisa y la envía, o la aprueba con un botón. Se registra todo en la ficha.

## Arquitectura

```
[formulario web / email / anuncio] → n8n: trigger → crear o actualizar la ficha en el CRM (HubSpot, Notion, Odoo, Zoho, Clientify…)
                                   → redactar la propuesta: llamada a una routine (API /fire) o nodo de IA con el prompt de la skill
                                   → BORRADOR en el CRM, en Notion o en el borrador de Gmail
                                   → aviso al comercial: "Propuesta lista para <cliente>" [Revisar] [Enviar]
                                   → enviada → registrar en la ficha → seguimiento en X días si no responde
```

## Piezas

1. **Conocimiento del negocio** en `02-DOCS/wiki/negocio/`: catálogo (rutas, hoteles, experiencias…), precios, preguntas frecuentes, tono, casos de éxito. Es lo que hace que la propuesta no sea genérica. Se mantiene en el arnés.
2. **Skill `/propuesta`**: estructura de la propuesta, reglas (nunca inventar precios ni disponibilidad: si falta un dato, se marca), idioma del cliente y longitud.
3. **CRM con MCP oficial** (HubSpot, Zoho, Notion, monday, GoHighLevel) o API (Clientify: su clave da acceso total, así que va solo en n8n).
4. **Disparador**:
   - **n8n** para la entrada en tiempo real.
   - Para redactar, dos opciones. (a) Un nodo de IA en n8n con el prompt de la skill: simple. (b) n8n llama al endpoint `/fire` de una **routine** que ejecuta `/propuesta` con el repo del arnés y los conectores de claude.ai: más potente, porque usa la skill y la wiki tal cual.
5. **Aprobación**: el envío nunca es automático al principio. Después de unas semanas, solo los casos simples con aprobación por botón.

## Ojo con las routines

- Llevan **todos** los conectores de claude.ai activados por defecto, y pueden escribir **sin preguntar**. Para esta receta, deja el CRM o Notion (escribir borrador) y **quita Gmail** o déjalo solo para borradores. Que envíe una persona.
- No ven `01-TOOLS/*/.env`: los secretos van en el entorno cloud.
- Límite: 30 ejecuciones por hora por rutina desde la API. Si entran más leads, se encolan en n8n.

## Calificación de leads

Preguntas mínimas (presupuesto, plazo, necesidad, decisor), una puntuación con criterio escrito en la skill y una etiqueta en el CRM. Los "calientes" avisan al comercial al momento; el resto entra en una secuencia (MailerLite, ActiveCampaign o Klaviyo, todos con MCP oficial).

## Seguridad

- Los textos de formularios y emails son **contenido no fiable**. El agente no obedece instrucciones que vengan en ellos.
- Usuario de CRM dedicado ("IA") con permisos de crear y editar contactos y negocios, sin borrar ni exportar.
- RGPD: base legal para tratar el lead y aviso de privacidad en el formulario.

## Demo en clase (0 €)

Formulario de Wix o WordPress (gratis) → n8n → HubSpot Free (MCP oficial) → propuesta con la skill y una wiki de 5 rutas de ejemplo → aviso por Telegram.

## Errores típicos

- Propuestas que inventan precios o fechas: regla dura en la skill y datos de `02-DOCS`.
- Duplicar contactos: buscar por email o teléfono antes de crear.
- Enviar en automático desde el primer día: perder un cliente por una propuesta mala cuesta más que el tiempo ahorrado.

## Related

- [Cómo se monta](./como-se-monta.md) · [WhatsApp a pedidos](./whatsapp-a-pedidos.md) · [Catálogo: CRM](https://executive-lab.github.io/conectores-pymes/)
