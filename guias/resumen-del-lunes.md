---
type: article
title: "Receta: el resumen del lunes (ventas, caja, cobros, stock en un email)"
description: Cómo montar en el arnés un informe semanal automático que lee 1-3 fuentes, lo resume con IA y lo manda por email, según dónde vivan los datos (nube, PC de la oficina o n8n).
tags: [receta, informe, kpi, routine, cron, solo-lectura]
timestamp: 2026-10-09T13:15:00Z
topic: recetas
status: draft
sources: []
score: 0.0
---

# Receta: el resumen del lunes

## En resumen
Cada lunes a las 7:30 llega un email con: ventas de la semana frente a la anterior, caja y saldo, facturas pendientes de cobro y de pago (con antigüedad), stock bajo mínimos y pedidos abiertos. Tres alertas como mucho, cada una con el dato que la justifica. Ni una cifra inventada: si una fuente falla, el email lo dice.

## Arquitectura

```
[disparador semanal] → skill /resumen-semanal → lee 01-TOOLS/<ERP> + 01-TOOLS/<BANCO o EXCEL>
                                              → calcula, compara con la semana anterior (02-DOCS/raw/resumenes/)
                                              → redacta el email → lo manda (o deja borrador) → guarda la copia
```

La **skill** es la misma en todas las variantes. Solo cambian el disparador y dónde viven los datos.

## 1. La skill (`.claude/skills/resumen-semanal/SKILL.md`)

Contenido mínimo:

- **Fuentes y qué sacar de cada una**: p. ej. Holded (facturas emitidas y recibidas, pagos), Excel de stock (hoja y columnas), banco (si hay).
- **Definiciones**: qué es "venta" (base imponible de facturas emitidas, sin IVA), "pendiente de cobro" (vencidas o por vencer en 15 días), "stock bajo" (por debajo del mínimo de la columna X).
- **Formato del email**: asunto `Resumen semana <n> · <empresa>`, 5 bloques fijos y 3 alertas como mucho.
- **Reglas**: solo lectura; si una fuente falla, decirlo y no estimar; cifras con su origen; guardar los datos de la semana en `02-DOCS/raw/resumenes/<fecha>.json` para comparar.
- `disable-model-invocation: true`: se lanza con `/resumen-semanal`, no por sorpresa.

Pruébala a mano dos o tres lunes y ajusta las definiciones con el dueño. **Después** elige el disparador.

## 2. El disparador, según dónde vivan los datos

### A. Datos en la nube (Holded, Odoo Online, Sheets, Gmail, HubSpot…) → routine

1. Sube el proyecto a un repo privado de GitHub. `01-TOOLS/*/.env` no se sube: está ignorado.
2. En claude.ai/code/routines (o con `/schedule`): prompt `/resumen-semanal`, repo, horario `30 7 * * 1` (evita las :00 en punto) y entorno cloud.
3. Secretos: la clave de Holded como variable o *network secret* del entorno, y `api.holded.com` en *Allowed domains*. Los scripts de `01-TOOLS` tienen que leer la clave de la variable de entorno si no hay `.env`.
4. **Conectores**: deja solo los necesarios. Para enviar, Gmail (envía sin preguntar: es lo que quieres) o, más prudente, solo crear borrador.
5. Requiere plan Pro, Max, Team o Enterprise. Frecuencia mínima: 1 hora.

### B. Datos en un PC de la oficina (Sage 50, Contasol local, Excel en disco, ICG…) → `claude -p` + cron en ese PC

1. En el PC (o servidor) que ve la base de datos: Claude Code y el proyecto con `01-TOOLS/<PROGRAMA>/` (usuario de BD de solo lectura o carpeta de exportación).
2. Tarea programada (Programador de tareas de Windows, launchd o cron), los lunes a las 7:30:
   `claude -p "/resumen-semanal" --allowedTools "Read,Bash(python3 01-TOOLS/*),Bash(./01-TOOLS/*)" --permission-mode dontAsk`
3. El envío, con un script `01-TOOLS/GMAIL/enviar_resumen.py` (app de Google con un scope de solo envío) o dejando el informe en OneDrive o Drive.
4. Ojo: un `-p` carga el `.mcp.json` del proyecto sin pedir aprobación. Usa solo proyectos de confianza.

### C. Ya usas n8n → flujo semanal

Schedule Trigger → nodos HTTP o nativos de las fuentes → nodo de IA (Claude) con el prompt de la skill → Gmail. Útil si el resto de automatizaciones ya viven en n8n. La lógica de negocio se duplica (prompt en n8n y skill), así que mantén **una** definición y cópiala.

## 3. Variantes por herramienta (ver catálogo)

| Si tienes… | Fuente | Vía |
|------------|--------|-----|
| Holded | API v2, token de **solo lectura** en Ventas, Compras y Tesorería | Routine (A) |
| Odoo | API JSON-2 o MCP nativo (Odoo 20) con usuario bot de solo lectura | Routine (A) |
| Sage 50 / Contasol local / ICG | Usuario SQL de solo lectura sobre vistas, o exportación nocturna | Cron local (B) |
| Solo Excel y email | Mover el Excel a OneDrive o Sheets (lectura por Graph o Sheets API) | Routine (A) |
| TPV Revo / Ágora | Informes v3 de Revo (token propio) / Integration Services de Ágora | (A) para Revo y (B) para Ágora, que es local |

## 4. Permisos y seguridad

- Todo de **solo lectura**. La única escritura es el email al dueño.
- Si la clave no se puede acotar (p. ej. Clientify o Mailchimp), deja la llamada en un flujo de n8n y que el resumen la consuma.
- Nada de datos de clientes en el email que no hagan falta (nombres de morosos solo si el dueño lo pide).

## 5. Demo en clase (0 €)

Odoo Community en Docker con datos de demostración + Google Sheets como "stock" + Gmail personal. Skill `/resumen-semanal` lanzada a mano, y después la misma con `/schedule` en vivo.

## 6. Errores típicos

- Definir mal "venta" o "cobro": dos semanas de ajustes con el dueño son normales.
- Comparar con la semana anterior sin haber guardado la anterior: guarda siempre el JSON.
- Routine sin el dominio en *Allowed domains*: devuelve 403 y el "verde" no significa éxito. Revisa la transcripción.
- Hora a las :00 en punto: arranca con retraso.

## Relacionado
- [Cómo se monta](./como-se-monta.md) · [Catálogo](https://executive-lab.github.io/conectores-pymes/) · [Conectar una plataforma](./conectar-una-plataforma-con-rsc.md)
