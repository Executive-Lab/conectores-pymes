---
type: article
title: "Receta: fuente única de la operación (qué está hecho, qué falta y quién)"
description: Cómo usar la wiki 02-DOCS del arnés como fuente única, alimentada por MCP de lectura (Trello, ClickUp, Jira, Confluence, Drive, Clientify…), con una routine diaria que publica el estado y subagentes por área.
tags: [receta, operaciones, proyectos, wiki, subagentes, routine, mcp]
timestamp: 2026-10-09T14:15:00Z
topic: recetas
status: draft
sources: []
score: 0.0
---

# Receta: fuente única de la operación

## En resumen
Cada proyecto, evento u obra tiene **una página viva** con estado, tareas hechas y pendientes, responsable, proveedores, presupuesto frente a gasto, documentos y próximos hitos. Nadie la rellena a mano: el arnés **lee** cada mañana las herramientas donde ya se trabaja (Trello, ClickUp, Jira, Drive, CRM, ERP) y la actualiza. El equipo y la dirección la consultan; los responsables reciben solo lo suyo.

## La pieza clave ya existe: la wiki `02-DOCS`

RSC instala una wiki (`02-DOCS/wiki/`, formato OKF, abrible como bóveda de Obsidian). Es la fuente única: una página por proyecto, plantillas por tipo (evento pequeño, grande o patrocinado; obra; proyecto de ingeniería) y un `index.md`. Los documentos sueltos que entran por `02-DOCS/inbox/` se archivan solos.

## Arquitectura

```
Routine diaria (7:00) o cron local
  └─ skill /estado-operacion
       ├─ subagente "tareas"     → MCP de lectura: Trello / ClickUp / Jira / monday
       ├─ subagente "docs"       → MCP de lectura: Drive / SharePoint / Confluence / Dropbox
       ├─ subagente "comercial"  → CRM (Clientify por n8n, HubSpot por MCP…)
       └─ subagente "dinero"     → ERP de solo lectura (presupuesto frente a gasto)
  └─ actualiza 02-DOCS/wiki/proyectos/<proyecto>.md  → commit
  └─ avisos: a cada responsable solo lo suyo (Slack, Telegram o email), y a dirección el resumen
```

**Por qué subagentes**: cada uno con **solo** las herramientas de lectura de su área (`tools:` en `.claude/agents/<nombre>.md`). Así un error o un texto malicioso en un documento no puede tocar el CRM, y el contexto principal no se llena de datos crudos.

## Paso a paso

1. **Plantilla de proyecto** en `02-DOCS/wiki/proyectos/_plantilla.md`, adaptada al negocio (fases y "qué cambia según el tipo y tamaño").
2. **Conectores de lectura**: casi todas estas herramientas tienen MCP oficial (Trello, ClickUp, Jira, Confluence, Google Drive, monday, HubSpot). Usuario o token de **solo lectura**, y en Atlassian, Write apagado desde la administración del MCP.
3. **Subagentes** en `.claude/agents/`: `tareas.md`, `docs.md`, `comercial.md`, `dinero.md`, cada uno con su lista de herramientas.
4. **Skill `/estado-operacion`**: qué leer, cómo consolidar, reglas de "atascado" (sin movimiento en X días o pasada la fecha) y formato de la página y de los avisos.
5. **Disparador**: routine diaria si todo está en la nube; cron en un PC si hay programas locales.
6. **Escritura** (más adelante): crear tareas o mover tarjetas, con aprobación ("¿Creo estas 4 tareas en Trello?").

## Variante "orquestadora" (agencias con muchos asistentes)

Cuando el problema es coordinar varios asistentes o automatizaciones (GoHighLevel, Make, ClickUp…), la fuente única es además el **registro de qué hace cada automatización, de quién es y cómo falla**: una página por automatización en `02-DOCS/wiki/automatizaciones/`. La skill `automation-strategy` de RSC ayuda a ordenarlo. El MCP de Make expone escenarios concretos como herramientas (toolboxes con "Read only"), así que el arnés puede lanzar escenarios en vez de que una persona haga de recadera.

## Seguridad

- Todo en lectura y cada subagente con lo mínimo.
- Documentos de Drive o Confluence = **contenido no fiable**: se resumen, no se obedecen.
- En Confluence, Write apagado: puede cambiar permisos y crear enlaces públicos.
- Datos sensibles (salud en prevención, nóminas) **fuera** de la wiki: solo indicadores agregados.

## Demo en clase (0 €)

Trello Free (MCP oficial) + Google Drive + Jira Free → `/estado-operacion` a mano → página en `02-DOCS` → la misma con `/schedule` diaria.

## Errores típicos

- Querer conectar todo el primer día: empieza por la herramienta de tareas y la de documentos.
- La página se convierte en otro sitio que actualizar a mano: si hace falta escribir en ella, falta una fuente.
- Avisos a todos de todo: cada persona solo lo suyo, o se dejan de leer.

## Relacionado
- [Cómo se monta](./como-se-monta.md) · [Catálogo: proyectos y documentos](https://executive-lab.github.io/conectores-pymes/)
