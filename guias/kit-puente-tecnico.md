---
type: article
title: "Kit puente, parte técnica: leer un programa de escritorio en solo lectura"
description: Para el informático del alumno y para formadores — cómo montar el puente estándar (copia nocturna, login de solo lectura sobre vistas, MCP de base de datos, túnel sin puertos abiertos) para Sage 50/200, Contasol local, ICG, Prevengos, CONTPAQi, a3ERP, y cuándo pagar una API unificada (Chift) en vez de montarlo.
tags: [kit-puente, sql-server, access, mcp, dbhub, tailscale, cloudflare, solo-lectura, informatico]
timestamp: 2026-10-09T16:30:00Z
topic: guias
status: draft
sources: ["https://github.com/bytebase/dbhub", "https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/overview", "https://tailscale.com/kb/1324/grants", "https://developers.cloudflare.com/cloudflare-one/applications/non-http/", "https://support.claude.com/en/articles/11175166", "https://docs.chift.eu/platform/advanced/local-agent", "https://docs.n8n.io/2-0-breaking-changes", "https://support.microsoft.com/kb/2019698"]
score: 0.0
---

# Kit puente, parte técnica

> Para: el informático del alumno, o el formador que lo acompaña. La versión para el dueño de la pyme es [Mi programa no tiene API](./mi-programa-no-tiene-api.md) (vías 2 y 3).
> Verificado el 2026-10-09. Las versiones y los precios cambian: compruébalos antes de instalar.

## En resumen
Objetivo: que el agente **lea** los datos de un programa de escritorio (SQL Server o Access) **sin poder escribir**, **sin abrir puertos** y **sin perder el soporte** del fabricante. Para escribir no se usa el puente: se usa el [fichero de importación oficial](./escribir-en-contabilidad-por-importacion.md).

La garantía real de "solo lectura" está **en la base de datos** (un login con permisos mínimos y vistas curadas). El "modo solo lectura" de los servidores MCP es casi siempre un filtro de sentencias: ayuda, pero no basta.

## Arquitectura estándar

```
[Servidor o PC del ERP]                                          [Agente]
  SQL Server (producción)
     └─ backup nocturno → restaurar en ERP_IA (copia)      ┌─ Claude Code en el portátil ── Tailscale (grant solo al puerto del MCP)
           └─ esquema "ia": vistas curadas                 │
                └─ login ia_lectura (SELECT en "ia")       │
                     └─ DBHub (readonly, SQL predefinido) ─┤
                        escuchando en 127.0.0.1            └─ Conector de claude.ai / n8n en la nube ── Cloudflare Tunnel + Access
```

## Paso a paso

### 0. Permiso previo

Pregunta al distribuidor (Sage, ICG, Prevengos, CONTPAQi, Wolters Kluwer) si crear un login y vistas afecta al soporte. Si afecta, trabaja **solo con la copia** (paso 1). Pídelo por escrito: hay una plantilla en [Mi programa no tiene API](./mi-programa-no-tiene-api.md).

### 1. Aislar los datos: copia nocturna

- **SQL Server, Express incluido**: SQL Server Express **no tiene SQL Server Agent**. Microsoft documenta el patrón con el Programador de tareas de Windows + `sqlcmd`: backup de producción y `RESTORE` en una base aparte `ERP_IA` cada noche, fuera de horario.
- **Access** (.mdb o .accdb, p. ej. Factusol local): copia del fichero fuera de horario y conversión de la copia a SQLite. **Nunca** se conecta un MCP al `.mdb` vivo.
- Conectar a producción solo si hace falta tiempo real, y entonces con el login del paso 2 y límites de filas y tiempo.

### 2. Login de solo lectura sobre vistas

En la base que va a leer el agente:

1. Esquema `ia` con **vistas curadas**: solo las columnas necesarias. Sin IBAN, sin datos de salud, sin nóminas.
2. Login `ia_lectura`, que **no** sea `sa`, ni `db_owner`, ni `sysadmin`.
3. `GRANT SELECT ON SCHEMA::ia TO ia_lectura` (gracias a la cadena de propiedad no hace falta dar permiso sobre las tablas) y añadir `db_denydatawriter`. En la copia `ERP_IA` vale con `db_datareader`.
4. **Prueba de aceptación**: con `ia_lectura`, un `SELECT` funciona y un `INSERT` o un `UPDATE` **falla**. Sin esta prueba no se entrega.

### 3. El servidor MCP de base de datos

| Opción | Cuándo | Solo lectura | Limitar tablas | Notas |
|--------|--------|--------------|----------------|-------|
| **DBHub** (Bytebase, MIT) — recomendado para el kit | SQL Server, PostgreSQL, MySQL/MariaDB, Oracle, SQLite | `readonly=true` por herramienta en `dbhub.toml`: solo deja SELECT, SHOW, DESCRIBE, EXPLAIN y PRAGMA. Es un filtro: combínalo con el login del paso 2 | Con **herramientas de SQL predefinido** y parámetros tipados; se puede quitar `execute_sql` | npx o Docker, varios orígenes en un TOML, `max_rows`, túnel SSH. Por HTTP, token bearer compartido. No admite autenticación integrada de Windows |
| **SQL MCP Server** de Microsoft (Data API builder 2.x, MIT, GA) | SQL Server, Azure SQL, PostgreSQL, MySQL | Permisos por rol en el servidor (p. ej. `anonymous:read`) y sin SQL libre | Solo ve las entidades declaradas en `dab-config.json` | Por HTTP, por defecto todo entra como **anónimo**: hay que poner JWT o Entra ID, o Cloudflare Access delante. Necesita .NET |
| **mcpFirebird** (MIT) | Firebird | `allowedOperations=['SELECT']`, sin SQL libre | `allowedTables` | Madurez baja-media |
| Access | — | — | — | No hay MCP maduro: **copia → SQLite → DBHub** |

El ejemplo antiguo de Microsoft `MssqlMcp` ya no existe (404). Los MCP de SQL Server sin modo de solo lectura (p. ej. `mssql_mcp_server`) **no** van en el kit.

Plantilla de `dbhub.toml` por programa: una herramienta por pregunta de negocio ("ventas por día", "facturas pendientes", "stock bajo mínimos"), con su `SELECT` sobre las vistas del esquema `ia`. Así el agente no improvisa SQL contra el ERP.

### 4. Red: sin puertos abiertos

**Regla:** el 1433 (y cualquier puerto de base de datos o del MCP) **nunca** se abre en el router. Los servidores MS-SQL expuestos a internet son un vector clásico de ransomware en pymes.

| Si el agente es… | Usa | Cómo se acota | Coste orientativo |
|------------------|-----|---------------|-------------------|
| Claude Code en el portátil del dueño | **Tailscale** | Etiqueta `tag:erp` en el servidor y un *grant* que solo permita al usuario del dueño llegar **al puerto del MCP** (no al 1433) | Standard, unos 8 $/usuario/mes. El plan Personal es solo para uso no comercial |
| Un conector remoto de claude.ai, Cowork o n8n en la nube | **Cloudflare Tunnel + Access** delante del endpoint HTTP del MCP | Aplicación de Access con política por email y *service tokens* para máquinas. El MCP escucha en 127.0.0.1 y valida el JWT de Access | Zero Trust gratis hasta 50 usuarios según Cloudflare (verificar). Requiere un dominio en Cloudflare |

**Importante:** los conectores remotos de claude.ai salen de la infraestructura de Anthropic y **no llegan a una VPN ni a Tailscale**. Si el alumno quiere usar el puente desde claude.ai o Cowork, hace falta el túnel de Cloudflare.

### 5. En el arnés

`01-TOOLS/<PROGRAMA>/` con:

- `.env`: URL del MCP y token, sin la contraseña de la base de datos (esa se queda en el servidor del ERP).
- `test_connection`: llama a la herramienta "ventas por día" de ayer.
- `CREDENTIALS.md`: quién creó el login, dónde está la copia y cuándo se rota el token (cada trimestre).

Más la entrada en `.mcp.json`.

## Plan B: carpeta de exportación

Si no hay base de datos accesible: exportación nocturna a CSV en una carpeta (con el Programador de tareas y `sqlcmd`/`bcp` sobre vistas, o con la exportación del propio programa) y el arnés lee la carpeta.

- **n8n 2.0 desactiva por defecto** el *Local File Trigger* (y *Execute Command*). Para usarlo hay que reactivarlo a propósito y limitar rutas con `N8N_RESTRICT_FILE_ACCESS_TO`. Mantén n8n actualizado: ha habido CVE que saltaban esa restricción.
- Escribe a `.tmp` y renombra al final: un fichero a medio escribir dispara el evento antes de tiempo.
- Los eventos de fichero no son fiables sobre carpetas de red (SMB/NFS) ni sobre volúmenes de Docker en Windows.
- Valida el esquema de cada CSV y avisa si cambia: una actualización del programa rompe el parser en silencio.
- Exporta solo las columnas necesarias (RGPD).

## Cuándo pagar en vez de montar: APIs unificadas

| Servicio | Cobertura española | Local o nube | MCP | Precio | Ojo |
|----------|--------------------|--------------|-----|--------|-----|
| **Chift** | Holded, Contasol (solo Nube), a3ERP (beta), Sage 200 ES, Odoo, Ágora, Revo, BDP Net, Cegid Retail, Business Central | **Las dos**: Sage 200 ES y a3ERP con agente local de Windows (conexión saliente, sin puertos) | Sí, oficial | No público (B2B; negociar como academia) | Pide permisos amplios (lectura y escritura). No cubre Sage 50 ES, a3innuva, Factusol local ni ICG |
| Apideck | Holded y Odoo | Nube | Sí | Desde 599 €/mes | Caro para una pyme |
| Unified.to | Holded, Odoo, Sage 200 (beta) | Nube | Sí | Desde 750 $/mes | — |
| Merge, Codat, Rutter | Nada español verificado | — | — | — | No encajan |

Para un alumno suelto, **el puente propio sale más barato**. Para Executive Lab como academia, Chift merece una conversación: un acuerdo cubriría de golpe Sage 200 ES, a3ERP, Ágora y Revo.

## RPA, si no queda otra

| Herramienta | Coste | Para qué |
|-------------|-------|----------|
| Power Automate para escritorio | App gratis en Windows 10/11 para flujos lanzados a mano. Premium 15 $/usuario/mes; desatendido (Process) 150 $/bot/mes | Proceso estable en un ERP de Windows, también sobre RDP o Citrix con el agente para escritorios virtuales |
| Claude *computer use* | Tokens (cada captura suma unos 1.000-1.800 de entrada) | Tareas de poco volumen, en VM aislada y con confirmación humana |
| Windows-MCP (comunitario) | Gratis | Solo prototipos en VM: tiene acceso total al sistema; quitar PowerShell, Registro y sistema de ficheros con `--exclude-tools` |
| pywinauto | Gratis | Un paso concreto en un script de `01-TOOLS` (p. ej. pulsar "Exportar") |

Lo ideal: que el robot **solo exporte**, y que el resto lo haga el arnés sobre el fichero.

## El kit, empaquetado

Todo lo anterior está listo para copiar en **[kit-puente/](https://github.com/Executive-Lab/conectores-pymes/tree/main/kit-puente)** del repositorio público:

- `sqlserver/`: login `ia_lectura`, usuario, esquema `ia` y vistas de plantilla (idempotente), prueba de aceptación y copia nocturna. Ojo: la restauración nocturna **borra** usuario y vistas de la copia, así que el script los vuelve a crear y repite la prueba.
- `access/`: Access → SQLite.
- `dbhub/`: `dbhub.toml` con herramientas de SQL predefinido. DBHub escucha en `0.0.0.0` por defecto: indica siempre `--host`. `execute_sql` no se puede quitar según la documentación: va en `readonly` con tope de filas.
- `red/`: *grants* de Tailscale y `cloudflared` + Access.
- `01-TOOLS-plantilla/`: `.env.example` y `test_connection.sh`.

Pendiente: plantillas de vistas **por programa** (Sage 50, Sage 200, ICG, Prevengos, CONTPAQi, a3ERP), validadas con cada distribuidor. Los esquemas de tablas no son públicos.

## Relacionado
- [Mi programa no tiene API](./mi-programa-no-tiene-api.md) (versión para el dueño) · [Escribir en contabilidad por importación](./escribir-en-contabilidad-por-importacion.md) · [Catálogo](https://executive-lab.github.io/conectores-pymes/)
