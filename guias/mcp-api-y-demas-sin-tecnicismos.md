---
type: article
title: MCP, API, base de datos y RPA, sin tecnicismos
description: Explica con analogías de oficina qué es cada forma de conectar una herramienta (API, MCP, app autorizada, base de datos de solo lectura, exportación, webhook, RPA, conectores) y cuándo usar cuál, para alumnos sin perfil técnico.
tags: [guia-alumnos, mcp, api, conectores, conceptos]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# MCP, API, base de datos y RPA, sin tecnicismos

> Para: alumnos de Executive Lab que se han perdido con las siglas y quieren saber qué diferencia hay entre un MCP y una API.
> Conseguirás: entender cada pieza con una imagen de oficina, saber si tu programa tiene API y elegir entre conector, MCP, script o n8n/Make.

## Overview

Casi todas las dudas son la misma: «¿qué diferencia hay entre un MCP y una API?», «me he perdido con lo del MCP», «¿se puede crear un MCP para cualquier herramienta?». La respuesta corta: **una API es la ventanilla de un programa; un MCP es un manual de uso de esa ventanilla escrito para agentes de IA**. Una no sustituye a la otra. Muchos MCP funcionan por dentro llamando a una API.

Lo que necesitas saber, en cinco líneas:

1. Un programa se conecta por **una** de estas vías: API, MCP, app autorizada (OAuth), exportación a carpeta, base de datos de solo lectura o RPA.
2. Si hay MCP oficial o conector, es lo más rápido. Si no, API. Si tampoco, exportación. El RPA es el último recurso.
3. Un conector de claude.ai o ChatGPT es un MCP con botón «Conectar». Lo haces tú en minutos.
4. Los scripts de `01-TOOLS/` son para lo que ningún conector cubre o para lo que debe repetirse sin ti.
5. n8n o Make solo hacen falta cuando algo debe **ocurrir solo, a una hora o ante un aviso**, sin que tú abras el agente.

Las cinco vías de conexión con sus pasos están en la [guía base](./conectar-una-plataforma-con-rsc.md). Aquí no se repiten: aquí se entienden.

## Antes de empezar

No necesitas plan ni permisos especiales para leer este manual. Para probar lo que cuenta:

- Un conector en claude.ai o ChatGPT: una cuenta de esas herramientas. En planes de equipo, el administrador de la organización tiene que activarlo antes [1][2][4].
- Un MCP en Claude Code: Claude Code instalado y, si el MCP pide inicio de sesión, abrir la terminal una vez [3].
- Datos de clientes o personales: mira antes qué plan de IA usas en [planes, privacidad y costes](./planes-privacidad-y-costes.md).

## La oficina de la empresa: una analogía para todo

Imagina que tu empresa es una oficina y el agente de IA es un empleado nuevo muy capaz que no conoce tus archivadores.

| Concepto | Analogía de oficina |
|---|---|
| **API** | La **ventanilla** del archivo de otro departamento. Tu programa se acerca, pide «dame las facturas de marzo» con un formulario fijo y recibe la respuesta. Sin ventanilla, nadie de fuera entra. |
| **Clave de API** | La **llave de esa ventanilla**. Quien la tiene, pasa. Va en el cajón con llave (`.env`), nunca en una nota pegada en el chat. |
| **MCP** | El **manual de procedimientos** pegado junto a la ventanilla: «aquí se piden facturas, aquí se piden clientes, esto no se toca». Lo escribe el fabricante y lo entiende cualquier agente. Es un estándar abierto, como un USB-C para IA [5]. |
| **OAuth / app autorizada** | El **pase de visitante con el nombre de la empresa**. En vez de darle la llave maestra, el administrador firma un pase que dice «esta aplicación puede mirar solo esto». Se retira cuando quieras. Así funcionan Google, Microsoft y Meta. |
| **Base de datos de solo lectura** | El **cristal del archivador**: el agente ve los papeles, pero no puede abrir el cajón. Lo prepara tu informático. |
| **Exportación a carpeta** | El **buzón de salida**: cada noche el programa deja un Excel o CSV en una carpeta y el agente lo lee. Sin acceso directo al programa. |
| **Webhook** | El **timbre**. En lugar de ir a preguntar cada cinco minutos si hay pedidos nuevos, el programa llama a tu puerta cuando llega uno. |
| **RPA** | Un **becario que mira la pantalla y hace clic**. Vale para cualquier programa, pero se pierde si cambias el color de un botón. |
| **Conector de claude.ai o ChatGPT** | Un **enchufe homologado con botón**. Lo pulsas, inicias sesión y el agente ya puede ver esa herramienta. Es un MCP con la instalación hecha [1][4]. |
| **Base de datos (Supabase, etc.)** | El **archivador propio**, ordenado en fichas. No es una libreta de notas como Obsidian: es donde una aplicación guarda sus datos de forma estructurada. |

## API frente a MCP, sin rodeos

- **Quién la usa.** La API la usa un programador o un flujo (Make, n8n). El MCP lo usa un agente de IA.
- **Qué incluye.** La API es una lista de peticiones posibles. Al agente le falta saber cuándo usar cada una. El MCP le trae esa lista con descripciones: «esta sirve para buscar clientes». Por eso el agente «busca solo».
- **Qué hace falta.** Para usar una API sueles necesitar clave, documentación y alguien que escriba el código o el flujo. Para usar un MCP necesitas la dirección del servidor y, normalmente, iniciar sesión.
- **Ojo con el riesgo.** Un MCP puede **escribir**: crear, borrar, enviar. Aprueba tú las acciones de escritura [1].

Si usas Claude o ChatGPT con Gmail, Drive o Calendar, **ya has usado MCP sin saberlo**: esos conectores funcionan con ese estándar [1][5].

### ¿Se puede crear un MCP para cualquier herramienta?

Técnicamente casi siempre, **si la herramienta tiene API, base de datos accesible o exportación** que el MCP pueda usar. Si el programa está cerrado y no ofrece nada, el MCP no tiene nada a lo que agarrarse. Es como escribir el manual de una ventanilla que no existe. Y aunque se pueda, la pregunta útil no es «¿se puede?», sino «¿merece la pena frente a una exportación nocturna?». Para eso está [conectar o migrar](./conectar-o-migrar.md).

## ¿Cómo sé si mi programa tiene API? Cinco comprobaciones

1. **Busca en el panel.** Entra como administrador y mira en Ajustes, Configuración o Integraciones. Palabras clave: «API», «clave de API», «token», «desarrolladores», «webhooks». Si hay un botón para generar una clave, tiene API.
2. **Busca en la web del fabricante.** Escribe en el buscador «nombre del programa + API» o «nombre del programa + developers». Una página de documentación para desarrolladores es buena señal. «Integraciones» con logos (Zapier, Make, n8n) también.
3. **Pregunta al soporte**, con esta frase: *«¿Tiene API pública o webhooks? ¿La documentación está publicada? ¿Hay MCP oficial?»* Que te contesten por escrito.
4. **Mira el catálogo de Executive Lab**: [conectividad de plataformas](https://executive-lab.github.io/conectores-pymes/). Ahí está verificado qué vía tiene cada programa.
5. **Comprueba el plan.** Algunas herramientas tienen API solo en planes altos o como módulo de pago. Que no la veas no significa que no exista: puede ser cuestión de plan. Si el programa **se instala en un ordenador o servidor** (escritorio, on-premise), asume que no hay API pública hasta que el fabricante o el distribuidor digan lo contrario.

Ante la duda, usa tu agente: *«Averigua si [programa] tiene API o MCP oficial y dime qué vía de conexión me recomiendas.»* (skill `conectar-herramienta`).

## ¿Y si no la tiene?

No te quedas parado: hay exportación a carpeta, usuario de base de datos de solo lectura, módulo del distribuidor, RPA y, a veces, cambiar de herramienta. Lo tienes ordenado, con pros y contras, en [mi programa no tiene API](./mi-programa-no-tiene-api.md).

## Conector, MCP en Claude Code o script: qué es cada cosa

Los tres usan las mismas ideas. Cambia **dónde** los activas y **quién los mantiene**.

### Conectores en claude.ai

Es el enchufe con botón. En la web de Claude, abre **Customize > Connectors** (o «+» > Conectores > Gestionar). Eliges un servicio del directorio, pulsas Conectar e inicias sesión [1][2]. También puedes añadir un **conector personalizado** pegando la dirección de un MCP remoto: funciona en todos los planes, aunque el plan gratuito permite solo uno [1][2].

- **Planes de equipo** (Team y Enterprise): un propietario de la organización activa el conector y cada persona inicia su sesión. Si «no te aparece el conector», suele ser esto [1][2].
- Claude hereda los permisos que tú tienes en esa herramienta [2]. Puedes desactivar herramientas sueltas para dejarlo en solo lectura [1].
- Las conexiones salen de los servidores de Anthropic: un servidor dentro de tu red necesita permitir esas direcciones [1].

### Conectores y apps en ChatGPT

OpenAI usa hoy varios nombres a la vez: **conectores**, **apps** y, para lo que añade un desarrollador, **servidores MCP personalizados** [4][6]. Se gestionan en los ajustes de Apps de ChatGPT. Los MCP personalizados requieren el **modo desarrollador**. En Business solo lo activan administradores y propietarios; en Enterprise/Edu, el administrador decide quién [4]. En Pro hay un acceso limitado a lecturas [4]. ChatGPT pide confirmación antes de acciones que escriben [4][6]. Los nombres y planes cambian a menudo: confirma siempre en tu pantalla.

### MCP en Claude Code

Aquí el conector lo añades tú desde la terminal o un fichero. Es lo que montamos en el arnés:

```
claude mcp add --transport http <nombre> <dirección-del-servidor>
```

Luego, si pide inicio de sesión, escribe `/mcp` dentro de Claude Code y sigue el navegador (o `claude mcp login <nombre>`) [3]. Tres alcances: solo tú en este proyecto (por defecto), compartido con el equipo en `.mcp.json`, o todos tus proyectos [3]. Es la fricción que algunos alumnos notan: hay que abrir la terminal una vez.

Solo conecta MCP de fabricantes de confianza. Un MCP que lee contenido externo (correos, webs) puede recibir instrucciones ocultas dentro de ese contenido [3].

### Scripts en `01-TOOLS/`

Un script es una receta escrita para **tu** caso, con su clave en `.env` y un `test_connection`. Se usa cuando no hay MCP ni conector, cuando quieres controlar exactamente qué se lee, o cuando el proceso debe repetirse siempre igual.

### Cuándo usar cuál

| Situación | Usa |
|---|---|
| Quiero ver mi Gmail, Drive o Calendar desde el chat | Conector de claude.ai o ChatGPT |
| El fabricante tiene MCP oficial y trabajo con Claude Code | MCP en Claude Code |
| Tengo API con clave pero no MCP | Script en `01-TOOLS/` |
| Programa instalado sin API | Exportación o base de datos de solo lectura, leídas por un script |
| Quiero que algo ocurra solo cada mañana o al recibir un aviso | n8n o Make (ver abajo) |

## Cuándo hace falta n8n o Make, y cuándo basta el agente

Piensa en el agente como un **empleado al que le pides cosas**, y en n8n o Make como el **reloj y el timbre** de la oficina.

- **Basta con el agente** cuando eres tú quien lo pide: resúmenes, informes, consultas, borradores. Es el caso de la mayoría de ideas. Si tu ERP tiene API, normalmente basta un script o MCP y el agente: no necesitas Make para consultar.
- **Hace falta n8n o Make** cuando:
  - debe ejecutarse **sin ti** a una hora fija o cuando llegue un evento (webhook);
  - conecta varias herramientas con pasos fijos y quieres verlos dibujados;
  - necesita reintentos, registro y aprobación por Slack o WhatsApp.
- **Lo mejor suele ser combinar**: el flujo se dispara solo y el agente hace la parte que requiere criterio (leer, clasificar, redactar). Mira [resumen del lunes](./resumen-del-lunes.md) y [leads y atención](./leads-y-atencion.md).

Si dudas, empieza solo con el agente. Cuando te descubras repitiendo la misma petición cada día, ese es el momento de automatizarlo (y [fuente única](./fuente-unica.md) te ayuda a ordenar los datos antes).

## Tabla final: todas las vías comparadas

| Vía | Qué es | Cuándo | Quién lo monta | Riesgo |
|---|---|---|---|---|
| **API con clave** | Ventanilla con llave | SaaS con apartado «API» | Tú, 15 minutos | Medio: una clave filtrada abre mucho. Solo lectura y en `.env` |
| **MCP oficial** | Manual de la ventanilla para agentes | El fabricante lo publica | Tú, 5 minutos | Medio: puede escribir. Aprueba cada escritura |
| **App autorizada (OAuth)** | Pase de visitante limitado | Google, Microsoft, Meta | El administrador de la cuenta | Bajo si pides solo lectura y limitas carpetas |
| **Base de datos de solo lectura** | Cristal del archivador | Programa instalado sin API | Tu informático | Medio: nunca escribir; acceso solo por VPN |
| **Exportación a carpeta** | Buzón de salida | Programa que exporta Excel o CSV | Tú o tu informático | Bajo: datos con retraso, sin acceso al programa |
| **Webhook** | Timbre que avisa | Reaccionar a un evento al instante | Quien monta el flujo (n8n, Make) | Bajo: valida de quién viene el aviso |
| **RPA** | Becario que hace clic | Último recurso, sin otra vía | Tú con ayuda de Executive Lab | Alto: se rompe, es lento, usa una sesión real |
| **Conector claude.ai / ChatGPT** | Enchufe con botón | Servicios del directorio | Tú o el administrador | Medio: hereda tus permisos |

## Preguntas de alumnos

**¿Qué diferencia hay entre un MCP y una API?**
La API es la ventanilla del programa. El MCP es el manual que explica al agente cómo usarla. Con MCP el agente decide solo qué pedir.

**Me he perdido con lo del MCP. ¿Para qué sirve?**
Para que tu agente use una herramienta sin que copies y pegues. Si ya has conectado Gmail o Drive a Claude o ChatGPT, ya lo has usado.

**¿El MCP es lo que montamos con cualquier conector de cualquier programa?**
No. Solo existe MCP donde alguien lo ha construido. Si no hay, se usa API, exportación o un script.

**¿Se puede crear un MCP para cualquier herramienta?**
Si hay API, base de datos accesible o exportación, sí. Si el programa es cerrado, no hay nada que conectar. Y no siempre compensa.

**¿Cómo sé si mi programa tiene API?**
Haz las cinco comprobaciones de arriba. Lo más rápido: buscar «API» o «Integraciones» en el panel y preguntar al soporte por escrito.

**Mi ERP tiene API. ¿Basta con Make o necesito una skill o agente a medida?**
Para consultar y analizar, basta un script o MCP con el agente. Make sirve para lo que debe correr solo. Muchas veces se usan juntos.

**No me aparece el conector de Microsoft 365 en Claude. ¿Qué hago?**
En planes de equipo, el propietario de la organización debe activarlo antes y cada persona inicia sesión después [1][2]. Pídeselo a quien administre vuestra cuenta de Claude.

**Autenticar un MCP en Claude Code me obliga a abrir la terminal. ¿Es normal?**
Sí. Escribe `/mcp` dentro de Claude Code, sigue el navegador y ya está [3]. Si prefieres no usar la terminal, un conector de claude.ai suele valer.

**¿Un agente con acceso de escritura podría borrar datos?**
Sí, si le das permiso. Por eso: empieza en solo lectura, usa una credencial dedicada y aprueba tú cada escritura.

## Errores típicos

- Pensar que «tiene API» y «tiene MCP» es lo mismo.
- Dar al agente la clave de administrador o tu usuario personal en lugar de uno dedicado.
- Pegar la clave en el chat o mandarla por email o WhatsApp. Va en `.env`.
- Dejar todas las herramientas de un conector activas, incluidas las que borran o envían.
- Escribir directamente en la base de datos de un programa contable o ERP.
- Montar un flujo en n8n o Make para algo que solo necesitabas preguntar al agente una vez.
- Usar un MCP de un tercero desconocido con acceso a tu correo o a tu n8n.
- Querer RPA antes de preguntar si el programa exporta a Excel.

## Fuentes

Todas consultadas el 2026-10-09.

1. Anthropic, «Get started with custom connectors using remote MCP»: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
2. Anthropic, «Use connectors to extend Claude's capabilities»: https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
3. Anthropic, «Connect Claude Code to tools via MCP»: https://code.claude.com/docs/en/mcp
4. OpenAI, «Developer mode and MCP apps in ChatGPT»: https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
5. Model Context Protocol, «What is MCP?»: https://modelcontextprotocol.io/docs/getting-started/intro
6. OpenAI, «MCP and connectors» (documentación para desarrolladores): https://developers.openai.com/api/docs/mcp

## Related

- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md): las cinco vías y los pasos.
- [Mi programa no tiene API](./mi-programa-no-tiene-api.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Conectar o migrar](./conectar-o-migrar.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
- Recetas: [resumen del lunes](./resumen-del-lunes.md), [leads y atención](./leads-y-atencion.md), [fuente única](./fuente-unica.md)
