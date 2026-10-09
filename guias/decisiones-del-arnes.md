---
type: article
title: Decisiones del arnés: skill, agente, comando o automatización; uno o varios arneses
description: Guía para alumnos que ordena las cinco decisiones que más se repiten (qué pieza uso, cuántos arneses, varias máquinas, trabajo desatendido y tokens) con una regla clara para cada una.
tags: [guia-alumnos, arnes, skills, agentes, automatizaciones, seguridad, tokens]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Decisiones del arnés: skill, agente, comando o automatización; uno o varios arneses

> Para: alumnos de Executive Lab que ya tienen (o van a montar) su arnés RSC y dudan de qué pieza crear.
> Conseguirás: una regla para cada decisión, para dejar de preguntarte «¿esto es una skill o un agente?» y no acabar con un Frankenstein.

## Overview

Desde abril es la duda número uno en clase y en el foro. Las preguntas se repiten: «¿skill o agente?», «¿un arnés o varios?», «¿qué pasa si cambio de ordenador?», «¿cómo lo dejo trabajando solo?», «¿cómo encadeno varios arneses?», «se me acaban los tokens».
Parte de la confusión viene de que el equipo ha dado dos respuestas que parecen opuestas: «arneses modulares» y «mantenerlo todo junto». **No se contradicen.** Hablan de capas distintas:
- **Dentro de un arnés: modular.** Una skill por tarea, cada una pequeña y con nombre claro.
- **Entre arneses: junto.** Un arnés por empresa o contexto de datos. Si el contexto es el mismo, el arnés es el mismo.

Lectura: 15 minutos. Actúas tú; para servidor o equipo, tu informático ([texto listo](#qué-pedir-a-tu-informático)). Un arnés RSC es la carpeta de tu proyecto con `01-TOOLS/` (conexiones: una carpeta por proveedor, con su `.env` y scripts) y `02-DOCS/` (la wiki de la empresa) [5]. Lo demás son piezas que se enchufan a ella.

## Antes de empezar

- Claude Code instalado y tu arnés abierto en una carpeta. Si aún no conectas herramientas, empieza por [conectar una plataforma](./conectar-una-plataforma-con-rsc.md).
- Para dejar tareas solas, un plan con rutinas en la nube (Pro, Max, Team o Enterprise; en *research preview*, pueden cambiar) [3]. Los nombres son los de Claude Code; en Codex no verificado.

## Las piezas, de una en una

Cada una con su analogía de oficina. Todas están en la documentación oficial [1][2][4][6].

| Pieza | Qué es | Analogía de oficina | Cómo se crea |
|-------|--------|---------------------|--------------|
| **Skill** | Una carpeta con un `SKILL.md`: instrucciones para una tarea. Claude la carga cuando toca, o tú la llamas con `/nombre` | El **procedimiento escrito** en el cajón: «cómo cerramos el mes». Quien lo lee lo hace igual cada vez | `.claude/skills/<nombre>/SKILL.md` (solo este proyecto) o `~/.claude/skills/` (todos tus proyectos) [1] |
| **Comando** (`/algo`) | Antes eran ficheros en `.claude/commands/`. Ahora son lo mismo que una skill: ambos crean `/nombre` | El **atajo del teclado** para lanzar un procedimiento | Crea una skill. Para que solo la lances tú y Claude no la use sola, pon `disable-model-invocation: true` [1] |
| **Subagente** | Un asistente con su propia ventana de contexto, sus herramientas y sus permisos. Trabaja y devuelve solo un resumen | Un **empleado temporal con su propia mesa**: le das el encargo, se encierra a revisar 200 facturas y vuelve con una nota de una página | Fichero `.md` en `.claude/agents/` con `name` y `description` [2] |
| **Hook** | Una orden que Claude Code ejecuta **siempre** en un momento fijo (antes de escribir un fichero, al terminar...). No es una petición, es una regla | El **cerrojo o la alarma de la puerta**: salta siempre, no depende de que alguien se acuerde | Bloque `hooks` en `.claude/settings.json` [4] |
| **Tarea programada** | Claude Code lanza un prompt a una hora o con un evento | El **recordatorio del calendario que además hace el trabajo** | Rutina en la nube (`/schedule`), tarea de escritorio o `/loop` en una sesión [3] |
| **Automatización** (n8n, Make) | Un flujo de pasos fijos entre aplicaciones, que corre en su propio servidor | La **secretaria con reloj** que cada mañana abre el correo, copia al Excel y avisa. No piensa, sigue la lista | En la plataforma elegida |
| **Script en `01-TOOLS`** | Un programa pequeño (Python o bash) que usa la clave de `.env` y hace una cosa: leer, consultar, exportar | La **ventanilla con su formulario**: siempre pregunta lo mismo y devuelve datos | `01-TOOLS/<PROVEEDOR>/` con `test_connection` primero [5] |
| **MCP** | Un enchufe estándar para que el agente use una herramienta externa | Una **regleta** donde conectas el programa del proveedor | `claude mcp add` o `.mcp.json` [6]. Ver [MCP y API](./mcp-api-y-demas-sin-tecnicismos.md) |

Dos aclaraciones de clase: un **plugin** es un paquete de skills (y más) para compartirlas [1]; y «agente» se usa para todo, así que pregunta si es un subagente, una automatización con IA dentro o el propio arnés trabajando. Un subagente es un trabajador desechable dentro de tu sesión, no «un arnés pequeño»; puede lanzar otros hasta tres niveles [2].

## Árbol de preguntas

Recórrelo de arriba abajo. Para en la primera respuesta que encaje.

```
1. ¿Lo haces una vez o de vez en cuando?
   └─ Sí → No crees nada. Pídeselo al arnés. Si sale bien y se repite → pregunta 2.
2. ¿Se repite con los mismos pasos, sin pensar?
   └─ Sí → ¿Tiene que pasar solo, a una hora o cuando llega algo (correo, pedido)?
        ├─ Sí, sin tu ordenador encendido → automatización (n8n/Make) o rutina en la nube.
        └─ No, lo lanzas tú → script en 01-TOOLS (y una skill que lo llame).
3. ¿Necesita criterio (leer, decidir, redactar, comparar)?
   └─ Sí → skill. ¿Lee mucho y no quieres llenar tu conversación? → que delegue en un subagente.
4. ¿Tiene que ocurrir SIEMPRE, sin depender de que Claude se acuerde?
   └─ Sí → hook o regla de permisos, no una skill (una skill se puede olvidar).
5. ¿Escribe en un sistema (ERP, correo, CRM, banco)?
   └─ Sí → solo con aprobación humana, empezando en solo lectura. Nunca desatendido sin red de seguridad.
6. ¿Necesita una herramienta nueva?
   └─ Primero la conexión (carpeta en 01-TOOLS y test_connection). Después la skill.
```

Dos reglas para desempatar: **skill o subagente** → empieza por la skill y, si llena tu conversación de papeles, conviértela (diez minutos). **Arnés o automatización** → ¿qué parte piensa? Si todo son pasos fijos entre aplicaciones, n8n o Make es más barato y estable; lo habitual es mezclar: n8n mueve datos y llama al arnés solo en el paso con criterio.

## Uno o varios arneses

**Regla: un arnés por empresa o por contexto de datos. Separa solo si cambian los datos, los permisos o el equipo.**

| Si... | Entonces | Ejemplo |
|-------|----------|---------|
| Mismos datos, mismas claves, mismo equipo | **Un arnés**, varias skills | Finanzas, compras y comercial de tu misma pyme |
| Cambian los **datos** (otra empresa, otro cliente, datos que no deben mezclarse) | **Arnés separado** | Un grupo con cuatro empresas con clientes y contabilidad distintos |
| Cambian los **permisos** (una clave con acceso a nóminas que el resto no debe ver) | **Arnés separado** | RRHH aparte del resto |
| Cambia el **equipo** (otra persona o un externo trabaja ahí) | **Arnés separado** | Un freelance al que das solo la parte de contenido |
| Solo cambia el **tipo de tarea** (contenido, finanzas, informes) | **No separes.** Una skill por tarea | Contenido y finanzas de la misma empresa |

Por qué no separar por tipo de tarea: cada arnés duplica el contexto de empresa (dos copias acaban contradiciéndose) y cada conexión se configura y rota dos veces. Las skills se separan por nombre y descripción, no por carpeta. Por qué sí separar cuando cambian datos, permisos o equipo: es el archivador con llave de RRHH. Quien no debe ver algo, no lo tiene delante.

### Cómo compartir contexto entre arneses sin duplicarlo

1. **Una carpeta «madre»** con el contexto común (manual de marca, reglas), por ejemplo un repositorio `contexto-empresa` solo con markdown. Solo esa se edita.
2. **Los demás la leen, no la copian.** Claude Code admite directorios adicionales además del de trabajo [7]. Dile a tu agente: *«Añade contexto-empresa como directorio adicional de solo lectura»*.
3. **Skills comunes:** en `~/.claude/skills/` (todos tus proyectos) o como plugin [1]. Lo de tu carpeta personal no viaja con el repositorio.
4. **El arnés que se carga es el de la carpeta donde abres la sesión.** Claude no «sabe» qué otros tienes.
5. **Lo privado de un arnés no va en la carpeta madre.**

### Encadenar arneses («redacción, diseño, publicación»)

Antes de coordinar tres arneses, mira si no son **tres skills de un mismo arnés** llamadas en orden. Casi siempre lo son. Si de verdad son arneses separados, usa **entrega por ficheros**: el primero deja su resultado en una carpeta acordada, una persona lo revisa (el semáforo) y el segundo lo lee. Sin agentes que se hablan entre sí: es más lento, pero ves qué pasó en cada paso.

## Varias máquinas y equipo

El arnés es una **carpeta**. Para llevarla de un ordenador a otro, o compartirla, se usa **git** (el control de versiones: guarda cada cambio con fecha y autor, como el historial de un documento) y **GitHub** (el sitio donde se guarda la copia central).

Cambiar de ordenador:
1. En el ordenador viejo, guarda y sube los cambios (*commit* y *push*). Pídeselo al arnés: *«Guarda todo y súbelo a GitHub»*.
2. En el nuevo, instala Claude Code y clona el repositorio.
3. Vuelve a crear los `.env` **a mano**, desde tu gestor de contraseñas. No viajan por git.
4. Lanza `test_connection` de cada herramienta. Si dice OK, estás al día.
5. Revisa lo que vive fuera del proyecto: las skills y subagentes de tu carpeta personal `~/.claude/` [1][2] y los MCP de ámbito local o de usuario [6]. Esos no van en el repositorio.

Dos máquinas a la vez: cada una en su **rama** (o en un *worktree*, segunda carpeta de trabajo del mismo repositorio). Las skills `worktrees` y `ftd` del arnés RSC preguntan por la rama antes de escribir código [5]. Drive o Dropbox **no** sustituyen a git: pueden pisar ficheros al sincronizar.

**Qué se sube y qué no:**

| Se sube | No se sube |
|---------|-----------|
| `.claude/skills/`, `.claude/agents/` | `.env` (claves) |
| `01-TOOLS/*/` scripts, `README.md`, `.env.example`, `CREDENTIALS.md` | `out/` (datos personales extraídos) |
| `02-DOCS/` (la wiki), `.mcp.json` sin claves | `keys/`, ficheros con claves o contraseñas |
| `.gitignore` | Exportaciones de clientes, facturas, CSV con datos personales |

`.env`, `keys/` y `out/` van siempre en el `.gitignore` de cada tool [5]. Comprueba el `.gitignore` **antes** del primer *push* a GitHub, y usa un repositorio **privado**. Una clave que se subió una vez hay que darla por perdida: revócala y crea otra.

En `.mcp.json` no escribas claves. Claude Code permite referencias como `${VARIABLE}` que se leen del entorno [6].

Para un equipo, cada persona crea **su propio `.env`** con **su propia clave**. Así sabes quién hizo qué y puedes revocar a uno sin tocar al resto.

## Trabajo desatendido con seguridad

«Desatendido» significa que nadie mira mientras se ejecuta. Es lo contrario a la aprobación humana, así que se exige más cuidado.

### Dónde se ejecuta: tres opciones [3][8]

| Opción | ¿Hace falta el ordenador encendido? | Acceso a tus ficheros | Permisos |
|--------|-------------------------------------|------------------------|----------|
| **Rutina en la nube** (`/schedule`) | No | No: clona el repositorio limpio, sin `.env` ni `out/` | Se ejecuta autónomo, sin preguntar |
| **Tarea de escritorio** | Sí, con la app abierta y el equipo despierto. Si duerme, se salta la ejecución | Sí | Eliges el modo por tarea. Si hace falta una aprobación, se queda parada esperándote |
| **`/loop`** | Sí, y con la sesión abierta | Sí | Los de la sesión. Caduca a los 7 días |

Respuesta directa a una duda de clase: la tarea de escritorio **sí** necesita el ordenador despierto; la rutina en la nube **no**, pero no ve tu carpeta local. Un mini PC siempre encendido sirve para tareas de escritorio, pero su `.env` vive allí.

La rutina en la nube usa **todas las herramientas de un conector, incluidas las de escribir, sin pedir permiso**, y por defecto incluye todos tus conectores: quita los que no necesite. Las variables de entorno las ve cualquiera que use ese entorno [3].

### Qué sí y qué no

- **Sí, sola:** resúmenes desde datos leídos, informes y borradores que revisa una persona, avisos de incidencias, ordenar la wiki, descargas de solo lectura.
- **No, sin aprobación humana:** enviar correos o WhatsApp a clientes, emitir o anular facturas, escribir en ERP, contabilidad o CRM, borrar datos, pagos, y datos personales sensibles sin revisar tu plan de IA ([planes y privacidad](./planes-privacidad-y-costes.md)).

Patrón seguro: **la tarea desatendida prepara, una persona aprueba.** El borrador queda en una carpeta o en borradores. No se envía.

### Candados que debes poner antes

1. **Solo lectura por defecto.** Usuario o aplicación dedicada con el permiso mínimo, nunca tu cuenta ni la de administrador.
2. **Reglas de permisos.** En `.claude/settings.json`, reglas `deny` (bloquean siempre), `ask` (preguntan) y `allow` (dejan pasar). Se evalúan en ese orden y la primera que coincide manda [7]. Bloquea la lectura de claves con `Read(./.env)` [7].
3. **Modo `dontAsk`** en lo desatendido de lectura: deniega lo que pediría permiso y deja pasar solo lo ya permitido [7]. **Nunca `bypassPermissions`** en tu equipo: la documentación lo reserva para contenedores o máquinas virtuales aisladas [7].
4. **Hooks como cerrojo.** Un hook `PreToolUse` que sale con código 2 detiene la acción antes de que se evalúen los permisos [4][7]. Es la forma de decir «nunca borres» sin depender de que Claude lo recuerde.
5. **Condición de parada.** Si «nunca acaba», no es un bucle misterioso: falta decir cuándo está terminada. Añade `maxTurns` a los subagentes y `tools` acotadas [2].
6. **Rama o *worktree*** si toca ficheros [8], nunca producción. Y **registro** de cada ejecución en `02-DOCS` o `out/`: si no puedes reconstruir qué pasó, no era seguro dejarla sola.

Dos riesgos: la **inyección de instrucciones** (un correo o web que el agente lee puede traer órdenes escondidas; la documentación pide conectar solo servidores de confianza [6]; leer correo y poder enviar es la combinación peligrosa) y las **skills y MCP de terceros** (no los instales sin que el arnés te cuente qué hacen).

## Cómo no hacer un Frankenstein

Un Frankenstein es un proyecto con piezas de todos los tamaños, cosidas sin orden, que nadie se atreve a tocar. Se evita con cinco hábitos:
1. **Una carpeta, un propósito.** Las conexiones en `01-TOOLS/<PROVEEDOR>/` (una por proveedor), el conocimiento en `02-DOCS/`, las skills en `.claude/skills/`. Nada suelto en la raíz [5].
2. **Una skill por tarea.** Nombre en verbo + objeto («cerrar-mes», «redactar-propuesta»). Si la descripción necesita «y también», son dos skills.
3. **Descripción clara y skills cortas.** Las descripciones de todas tus skills están siempre cargadas; si dos se parecen, Claude puede dudar. Escribe primero para qué sirve y cuándo se usa. `SKILL.md` por debajo de 500 líneas; lo largo, en ficheros de apoyo [1].
4. **Orden en la raíz.** Nada suelto fuera de `01-TOOLS`, `02-DOCS` y `.claude`.
5. **Sin herramientas especulativas.** Una tool entra en `01-TOOLS` cuando hay una operación recurrente que la necesita [5].

Revisión y poda, una vez al mes (30 minutos):
- Skills y subagentes sin usar: archívalos o bórralos. Dos casi iguales: fusiónalas.
- Una skill sin criterio, siempre igual: pásala a script en `01-TOOLS`.
- Una skill que lee mucho y satura la conversación: candidata a subagente.
- Una regla que se olvida: hook o regla de permisos.
- Pídele al arnés: *«Audita mis skills: sin usar, duplicadas y descripciones ambiguas. No cambies nada, solo propón.»* La skill `harness` audita el espacio de trabajo.

Si ya tienes un Frankenstein, **no lo rehagas de cero**: audita, ordena carpetas, pasa lo fijo a scripts y reescribe las skills una a una, empezando por la que más usas.

## Ahorrar tokens y límites

Un token es un trozo de texto que el modelo lee o escribe, como las palabras que cobra un traductor. Tu plan tiene un límite de tokens y se agota. En Team y Enterprise la documentación habla de una ventana de cinco horas y otra semanal [9]. Para Pro y Max, los plazos exactos no los he verificado aquí.

**Qué consume más** [9]: una conversación muy larga (Claude reenvía todo el historial en cada petición); volver tras una pausa larga (la caché dura una hora en suscripción y cinco minutos con créditos de uso); usar el modelo más potente para todo; subagentes y equipos de agentes (cada uno con su ventana; unos siete veces más tokens en modo plan); tareas programadas y `/loop` olvidados; MCP con resultados enormes (aviso desde 10.000 tokens [6]); pensamiento extendido en tareas simples; peticiones vagas («mejora todo»).

**Cómo reducirlo:**

| Hábito | Para qué sirve |
|--------|----------------|
| `/clear` al cambiar de tarea | No arrastras contexto inútil |
| `/usage` y `/context` | Ves qué consume (por skills, subagentes y MCP) |
| Modelo adecuado (`/model`) y `/effort` bajo en lo simple | Sonnet para lo normal, Opus solo para lo difícil; subagentes sencillos con `model: haiku` |
| Modo plan y prompts concretos con criterio de «terminado» | Menos rehacer, lecturas y bucles |
| Mover instrucciones largas de `CLAUDE.md` a skills | `CLAUDE.md` se carga siempre; la skill, solo cuando se usa. Recomienda menos de 200 líneas |
| Delegar lo voluminoso a subagentes | Los logs quedan en su ventana y vuelve solo el resumen |
| Desactivar MCP sin uso (`/mcp`) | Menos definiciones en contexto |
| Un script en `01-TOOLS` en lugar de que el modelo «lea y calcule» | Lo mecánico lo hace código, gratis. El modelo recibe solo el resultado |
| Hooks que filtran salidas largas y tareas fijas en n8n/Make | Un `grep ERROR` ahorra miles de tokens; n8n/Make no gastan tokens de tu plan, salvo el paso con IA |

Cuando se agota el límite: espera a que se reinicie, pide créditos de uso (`/usage-credits`) o cambia de modelo si el límite es por modelo [9]. Ojo con Codex u otras herramientas: pasar a créditos de API puede generar un gasto inesperado.

## Qué pedir a tu informático

Solo si quieres tareas en servidor o compartir el arnés en equipo. Copia y pega:

> Hola. Montamos un proyecto con Claude Code que lee datos de la empresa en **solo lectura**. Necesito: (1) un repositorio **privado** en GitHub con acceso por persona; (2) una cuenta de servicio o API con **permiso mínimo de lectura** por herramienta, revocable de forma individual; (3) si hay tareas sin supervisión, una máquina virtual o contenedor aislado. ¿Quién puede darlo de alta y cuánto tarda?

Más textos en [hablar con el informático](./hablar-con-el-informatico.md).

## Qué puedes automatizar después

Recetas existentes: [resumen del lunes](./resumen-del-lunes.md), [fuente única](./fuente-unica.md), [facturas a contabilidad](./facturas-a-contabilidad.md) y [cómo se monta una receta](./como-se-monta.md).

## Preguntas de alumnos

**1. Creo skills que quizá deberían ser agentes. ¿Cómo lo sé?**
Si la tarea lee mucho material y solo te interesa el resultado: subagente. Si es un procedimiento que sigues en la conversación: skill. Ante la duda, skill; se convierte después.

**2. Mi arnés tiene herramientas de trabajos sin relación entre sí. ¿Todo junto o uno por tarea?**
Con los mismos datos, permisos y equipo: un arnés, una skill por tarea. Separa solo si cambia alguno de los tres.

**3. Tengo cuatro empresas. ¿Un supercerebro?**
Un arnés por empresa si los datos no deben mezclarse. Lo común (método, tono) va en una carpeta única que los demás leen, sin copias.

**4. ¿Qué pasa con mi trabajo si cambio de ordenador? ¿Puedo usar el mismo arnés en dos a la vez?**
Si está en git y subido a GitHub, clonas y recreas los `.env` a mano. En dos a la vez, cada máquina en su rama. Ver [Varias máquinas y equipo](#varias-máquinas-y-equipo).

**5. ¿Cómo dejo a Claude trabajando solo? ¿Necesito el portátil encendido?**
Con una rutina en la nube, no, pero solo ve lo que está en el repositorio y corre sin pedir permiso. Con una tarea de escritorio, sí. Empieza por tareas de lectura que dejen borradores.

**6. ¿Cuándo uso n8n o Make y cuándo el arnés?**
n8n o Make para pasos fijos entre aplicaciones y a una hora, sin que tu ordenador esté encendido. El arnés cuando hay que leer, decidir o redactar. Se combinan: la automatización mueve los datos y llama al arnés en el paso con criterio.

## Errores típicos

- Un arnés nuevo por tarea, copiando en cada uno el contexto de empresa.
- Todo en un solo arnés cuando hay datos de varias empresas o permisos distintos.
- Reglas de seguridad («nunca borres») dentro de una skill: es un hook o un permiso.
- Rutina en la nube con todos los conectores activos y permiso de escritura.
- Subir `.env` u `out/` a GitHub. Un `/loop` olvidado (gasta y caduca a los 7 días [3]).
- Agente que lee correo y responde sin revisión humana. Skills de terceros sin leer. `bypassPermissions` en tu equipo.

## Fuentes

1. Anthropic, Claude Code: Skills — https://code.claude.com/docs/en/skills (consultado el 2026-10-09)
2. Anthropic, Claude Code: Subagents — https://code.claude.com/docs/en/sub-agents (consultado el 2026-10-09)
3. Anthropic, Claude Code: Routines — https://code.claude.com/docs/en/routines y Scheduled tasks (`/loop`) — https://code.claude.com/docs/en/scheduled-tasks (consultado el 2026-10-09)
4. Anthropic, Claude Code: Hooks guide — https://code.claude.com/docs/en/hooks-guide (consultado el 2026-10-09)
5. Proyecto oportunidades-alumnos, `01-TOOLS/README.md` y skills `harness`, `worktrees`, `parallel` y `ftd` del arnés RSC (lectura local, 2026-10-09)
6. Anthropic, Claude Code: MCP — https://code.claude.com/docs/en/mcp (consultado el 2026-10-09)
7. Anthropic, Claude Code: Permissions — https://code.claude.com/docs/en/permissions (consultado el 2026-10-09)
8. Anthropic, Claude Code Desktop: Scheduled tasks — https://code.claude.com/docs/en/desktop-scheduled-tasks (consultado el 2026-10-09)
9. Anthropic, Claude Code: Manage costs — https://code.claude.com/docs/en/costs (consultado el 2026-10-09)

## Related

- [Conectar una plataforma](./conectar-una-plataforma-con-rsc.md)
- [MCP y API](./mcp-api-y-demas-sin-tecnicismos.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
