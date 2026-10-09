---
type: article
title: Cómo se monta una automatización en el arnés (skill, comando, routine, loop, agentes, n8n)
description: Guía para alumnos y formadores — qué pieza de Claude Code o n8n usar para cada parte de una automatización, dónde corre, qué secretos ve y dónde va la aprobación humana.
tags: [recetas, claude-code, skills, routines, n8n, aprobaciones]
timestamp: 2026-10-09T13:00:00Z
topic: recetas
status: draft
sources: ["https://code.claude.com/docs/en/skills.md", "https://code.claude.com/docs/en/routines.md", "https://code.claude.com/docs/en/scheduled-tasks.md", "https://code.claude.com/docs/en/sub-agents.md", "https://code.claude.com/docs/en/headless.md", "https://code.claude.com/docs/en/hooks.md"]
score: 0.0
---

# Cómo se monta una automatización en el arnés

> Para: alumnos de Executive Lab y formadores. Datos de la documentación oficial de Claude Code a 2026-10-09: revisa antes de cada edición del curso.

## En resumen
Toda automatización del arnés tiene cuatro piezas:

1. **La skill: el QUÉ.** Qué datos mirar, qué calcular, con qué formato y qué reglas seguir. Es un fichero `.claude/skills/<nombre>/SKILL.md` y no cambia según cómo se dispare.
2. **Los conectores: de DÓNDE salen los datos.** `01-TOOLS/<HERRAMIENTA>/` (clave en `.env` y scripts), MCP en `.mcp.json` o conectores de claude.ai. Ver el [catálogo](https://executive-lab.github.io/conectores-pymes/).
3. **El disparador: CUÁNDO y DÓNDE corre.** Tú a mano, una routine en la nube, un cron en un PC o un flujo de n8n.
4. **La aprobación: quién dice "sí" antes de escribir.** Sin persona delante no hay quien apruebe, así que hay que diseñarlo.

Regla de oro: **escribe primero la skill y pruébala a mano.** Cuando funcione, elige el disparador. Así cambiar de mecanismo no obliga a rehacer nada.

## Las piezas

| Pieza | Qué es | Dónde se define | Dónde corre | ¿Ve `01-TOOLS/*/.env`? | ¿Conectores de claude.ai? | Aprobación humana |
|-------|--------|-----------------|-------------|------------------------|---------------------------|-------------------|
| **Skill** | Instrucciones que el agente carga cuando hacen falta, o con `/nombre` | `.claude/skills/<nombre>/SKILL.md` | Donde corra la sesión | Sí, en local | Si la sesión los tiene | La de la sesión |
| **Comando** | Una skill que solo lanzas tú (`/nombre`), con `disable-model-invocation: true`. Los antiguos `.claude/commands/` siguen funcionando, pero ya son lo mismo | Igual que una skill | Igual | Igual | Igual | Igual |
| **Subagente** | Un "ayudante" con su propio contexto y herramientas limitadas (p. ej. solo lectura) | `.claude/agents/<nombre>.md` (`tools:` / `disallowedTools:`) | Dentro de tu sesión | Sí | No confirmado | La de la sesión |
| **`/loop`** | Repite un prompt cada X minutos **mientras la sesión está abierta** | Se lanza en la sesión | Tu equipo | Sí | Sí | Sí (estás delante) |
| **Routine** (`/schedule`) | Agente programado **en la nube**: cron (mínimo cada hora), llamada a su API (`/fire`) o evento de GitHub | claude.ai/code/routines o `/schedule` | Nube de Anthropic, sobre un clon limpio del repo | **No**: los ficheros no versionados no existen allí | **Sí, todos por defecto**, y pueden escribir sin preguntar | **No hay persona** |
| **`claude -p` + cron** | Claude Code sin interfaz, lanzado por el programador de tareas de Windows, launchd o cron | Script en el PC o servidor | Ese PC | **Sí** | Solo con login de claude.ai | No hay: lo que pediría permiso se deniega |
| **GitHub Action** | `anthropics/claude-code-action` con `schedule` | `.github/workflows/*.yml` | Runner de GitHub | No (usa GitHub Secrets) | No | No: abre un PR y lo revisa una persona |
| **n8n** | Flujo siempre activo: webhooks, WhatsApp, email, carpetas, horarios | Tu instancia de n8n | Servidor de n8n | No: las credenciales viven en n8n | No (MCP propio) | **Sí**: nodo "Send and Wait" en Slack, Telegram o email |
| **Hook** | Regla que salta antes o después de una herramienta (p. ej. bloquear un comando) | `.claude/settings.json` | Con la sesión | — | — | Puede **denegar** (pero si caduca, no bloquea) |

## Cuál elegir

| Necesito… | Usa | Por qué |
|-----------|-----|---------|
| Probar o hacer algo de vez en cuando | **Skill o comando a mano** | Estás delante y apruebas lo que escribe |
| Que lo vigile mientras trabajo (un envío, una importación) | **`/loop`** | Muere al cerrar la sesión y caduca a los 7 días |
| Un informe programado con datos en la nube (Holded, Odoo Online, Sheets, Gmail, Notion) | **Routine** semanal o diaria | No necesita tu equipo encendido |
| Un informe programado con datos en un PC de la oficina (Sage 50, Contasol local, Excel local) | **`claude -p` + cron en ese PC** | Es el único que ve la base de datos y el `.env` locales |
| Reaccionar al momento (llega un WhatsApp, un email, un formulario, una factura a una carpeta) | **n8n** | Las routines y Claude Code no "escuchan" de forma continua |
| Un agente de WhatsApp siempre activo | **n8n** (WhatsApp Trigger + nodo de agente) o un servicio propio con el Agent SDK | Claude Code no es un servidor de mensajería |
| Revisar y mantener todo lo anterior | **Claude Code a mano**, con el MCP de n8n y las skills | El arnés construye y mantiene; n8n ejecuta lo continuo |

## Secretos según el mecanismo

- **En local** (skill a mano, `/loop`, `claude -p`): en `01-TOOLS/<X>/.env`, ignorado en git.
- **Routine**: en las variables del entorno cloud. Las ve cualquiera que use ese entorno; en Pro y Max, mejor como *network secrets*. Además hay que añadir el dominio de la API (p. ej. `api.holded.com`) a *Allowed domains* o la llamada falla. Los scripts de `01-TOOLS` tienen que aceptar la clave también desde una variable de entorno, porque allí no hay `.env`.
- **n8n**: en las credenciales de n8n. Es el sitio de las claves que no se pueden acotar: el agente llega solo a flujos concretos, nunca a la clave.
- **GitHub Action**: GitHub Secrets.

## Aprobaciones sin persona delante

En una routine o en un `claude -p` nadie puede pulsar "sí". Tres patrones, de más simple a más completo:

1. **No darle herramientas que escriban.** Quita los conectores que no hagan falta en la routine (todos vienen activados) y deja solo los de lectura. El resultado es un informe, un borrador o un fichero.
2. **Borrador + persona.** Escribe en estado borrador (factura borrador en Holded u Odoo, borrador de Gmail, PR en GitHub, fichero de importación en `out/`) y una persona lo valida.
3. **Aprobación por mensaje (n8n).** n8n prepara la acción, manda "¿Lo hago?" por Slack, Telegram o email con dos botones y espera. Solo ejecuta si la respuesta es "sí".

## Las recetas

| Receta | Para | Mecanismo recomendado |
|--------|------|-----------------------|
| [Resumen del lunes](./resumen-del-lunes.md) | Ver la empresa en un email: ventas, caja, cobros, stock | Skill + routine (nube) o cron local |
| [Facturas a contabilidad](./facturas-a-contabilidad.md) | Dejar de teclear facturas y tickets | n8n + extracción + aprobación + borrador o fichero de importación |
| [WhatsApp a pedidos y reservas](./whatsapp-a-pedidos.md) | Que los pedidos y reservas entren solos | n8n siempre activo + Cloud API + ERP o Sheets |
| [Leads y atención al cliente](./leads-y-atencion.md) | Responder rápido y bien a cada contacto | n8n + skill de propuesta + aprobación |
| [Fuente única de la operación](./fuente-unica.md) | Saber qué está hecho, qué falta y quién | Wiki `02-DOCS` + MCP de lectura + routine diaria + subagentes |

## Relacionado
- [Cómo conectar una plataforma](./conectar-una-plataforma-con-rsc.md) · [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
