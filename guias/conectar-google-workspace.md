---
type: article
title: Conectar Google Workspace (Gmail, Drive, Calendar, Sheets)
description: Cómo activar los conectores de Google en Claude y ChatGPT, qué hacer con varias cuentas de Gmail, qué cambia entre @gmail.com y Workspace de empresa, y cómo montar Drive, Sheets, n8n y Apps Script con permisos de solo lectura.
tags: [guia-alumnos, google-workspace, gmail, drive, calendar, sheets, looker-studio, oauth, solo-lectura]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Conectar Google Workspace (Gmail, Drive, Calendar, Sheets)

> Para: dueños y directivos que trabajan con Gmail, Drive, Calendar y Sheets (cuenta personal o de empresa) y quieren que su agente lea correo, agenda y ficheros.
> Conseguirás: el conector activo en minutos, una solución para varias cuentas, una petición lista para tu administrador de Workspace y una base de datos ligera en Sheets sin sustos.

## Overview

- **Qué puedes hacer.** Que Claude o ChatGPT busquen y lean correos, eventos y ficheros de Drive; que preparen borradores y eventos; y que tus flujos (n8n, Apps Script) lean hojas de Sheets.
- **Cuánto tarda.** Con cuenta personal, 5 minutos y lo haces tú. Con Workspace de empresa, depende de una persona: el **administrador de Workspace** (la persona que entra en admin.google.com, el «portero» de tu oficina digital). Con el texto de más abajo se resuelve en una conversación.
- **Quién actúa.** Tú, tu administrador de Workspace y, en planes Team o Enterprise de Claude, el propietario (Owner) de la organización en Claude.
- **Vía recomendada.** Los conectores oficiales de Google en Claude [1]. Para procesos programados o carpetas concretas, n8n o Apps Script con una cuenta dedicada y solo lectura.

## Antes de empezar

1. **Plan de Claude.** Los conectores de Gmail, Calendar y Drive están en todos los planes (Free, Pro, Max, Team, Enterprise) [1]. En Team y Enterprise, un Owner debe activarlos antes de que cada persona se autentique [1].
2. **Qué cuenta de Google tienes.** @gmail.com personal o Workspace de empresa. Cambia bastante (apartado propio más abajo).
3. **Datos personales.** Si vas a leer correos de clientes, mira antes qué plan de IA usas: [planes, privacidad y costes](./planes-privacidad-y-costes.md).
4. **Regla de oro.** Empieza en solo lectura. Un correo puede traer texto que intente dar órdenes al agente: lo que lee es dato, no instrucción.

## Los conectores en Claude y en ChatGPT: qué leen y qué escriben

**Claude** (documentación oficial de Anthropic) [1]:

| Conector | Lee | Escribe |
|---|---|---|
| Gmail | Busca y lee correos, metadatos de adjuntos (no su contenido), etiquetas, hilos y borradores | Crea borradores. Enviar, responder y reenviar piden tu aprobación por defecto |
| Calendar | Eventos y calendarios (también compartidos), huecos libres comunes | Crea, modifica y borra eventos, gestiona invitados, responde invitaciones |
| Drive | Docs, Sheets, Slides, PDF, imágenes y ficheros Office (solo extrae texto), permisos y cambios recientes | Sube ficheros, crea carpetas, comparte, mueve y manda a la papelera (con aprobación por defecto) |
| Docs, Sheets y Slides | Comentarios y sugerencias de Docs | Crean ficheros nuevos y editan en vivo en un panel lateral (beta). Conectores aparte |

En Team y Enterprise, el Owner decide si los miembros pueden enviar, compartir o mover sin aprobar cada vez [1]. El conector solo accede a los datos de la cuenta de Google que has conectado [1].

**Limitaciones que oirás en clase.** Los alumnos vieron en la demo de Cowork un Gmail que no enviaba correos ni adjuntaba ficheros. La documentación actual da envío con aprobación, pero no habla de adjuntar ficheros a un correo nuevo [1]: no verificado. Y «la IA no sabe qué día es» se arregla conectando Calendar, o poniendo la fecha en las instrucciones.

**ChatGPT** (documentación de OpenAI):

- Gmail, Google Calendar y Drive son conectores integrados. Las fuentes de terceros los dan en planes de pago de consumo y en Business, Enterprise y Edu; en Business vienen activados por defecto y en Enterprise desactivados [2][3]. En su lanzamiento no estaban en el EEE, Suiza y Reino Unido para Plus y Pro: no verificado si sigue así hoy.
- **Escritura.** Las acciones de escritura de Google (Gmail con `gmail.modify`, Calendar con `calendar.events`) se añadieron el 13-mar-2026 y vienen **desactivadas**. Un administrador del workspace de ChatGPT las activa en Workspace settings > Apps > Manage actions [2]. En Plus o Pro sin administrador, el conector sigue siendo de lectura (no verificado en fuente oficial).
- Los Workspace Agents (agentes de equipo) están solo en Business, Enterprise y Education, no en Plus (visto en clase).

## Cuenta personal @gmail.com frente a Google Workspace de empresa

| Cosa | @gmail.com personal | Workspace de empresa |
|---|---|---|
| Conectores de Claude | Funcionan. Tú das el permiso en la pantalla de Google [1] | Funcionan. El administrador puede bloquearlos o aprobarlos [1] |
| Quién manda | Nadie más. Sin consola de administración | El administrador en admin.google.com |
| Apps autorizadas | Cada usuario acepta o no | El administrador marca la app como Trusted, Limited, Datos específicos o Bloqueada [4] |
| App OAuth propia (n8n, scripts) | Pantalla de consentimiento «Externa». En modo «Testing» el token caduca a los **7 días** y hay máximo 100 usuarios de prueba [5] | Pantalla «Interna»: solo tu dominio, sin verificación de Google [catálogo] |
| Scopes restringidos (`gmail.readonly`, `drive.readonly`) | Si publicas la app Externa, Google exige verificación, vídeo de demostración y evaluación de seguridad anual [6] | Con app Interna no hace falta |
| MCP oficial de Google | No verificado para cuenta personal. Pide alta en el Developer Preview Program [7] | Sí, pero es Developer Preview [7] |
| Cambiar la contraseña | Rompe los tokens con scopes de Gmail [5] | Igual [5] |

Traducción práctica:

- **Los tokens que caducan** (bloqueo real en cuentas Gmail gratuitas): es el modo «Testing» de una app Externa. Soluciones: usar Workspace con app Interna, o usar los conectores oficiales de Claude, que no tienen ese límite.
- **Verificar tu app OAuth** es solo para apps que usarán otras personas. Para uso propio no la publiques: no compensa.
- Si tu empresa trabaja con cuentas @gmail.com de varios empleados, la ficha del catálogo recomienda valorar el paso a Workspace Business Starter (6,80 €/usuario/mes sin IVA, plan flexible, consultado el 2026-10-09) [8].

## Las vías, de mejor a peor

| # | Vía | Para qué sirve | Quién lo hace | Coste | Dificultad |
|---|-----|----------------|---------------|-------|------------|
| 1 | Conectores de Google en Claude o ChatGPT | Preguntar y redactar desde el chat | Tú (+ administrador en Workspace) | Incluido en tu plan | Baja |
| 2 | Drive sincronizado como carpeta del arnés | Que Cowork o Claude Code lean ficheros de Drive como locales | Tú | 0 € | Baja |
| 3 | n8n, Make o Zapier con nodos de Google | Flujos programados, triggers, adjuntos a carpetas | Tú (+ administrador para app Interna) | 0 € de API | Media |
| 4 | Apps Script dentro de Workspace | Mini-automatizaciones sobre una hoja o un correo | Tú | 0 € | Media |
| 5 | Cuenta de servicio sobre una carpeta u hoja | Acceso fijo, sin personas, a lo que compartas | Administrador + tú | 0 € | Media-alta |
| 6 | MCP oficial de Google (Developer Preview) | Leer y escribir por MCP remoto propio | Administrador | 0 € | Alta |

## Paso a paso: activar el conector en Claude

1. **Team o Enterprise:** un Owner abre Organization settings > Connectors y activa Gmail, Calendar y Drive. Si no, los miembros no pueden conectarse [1].
2. **Free, Pro, Max:** abre un chat, pulsa el signo «+» > Connectors y conecta cada uno con tu cuenta de Google [1].
3. Si Google muestra «Acceso bloqueado: el administrador de tu institución debe revisar Claude», es tu administrador de Workspace quien tiene que aprobarlo (texto de abajo) [1].
4. Prueba con una pregunta de lectura: «¿Qué reuniones tengo mañana?».

Dile a tu agente: *«Conecta mi Google Workspace en solo lectura y dime qué tengo que pedir a mi administrador.»*

## Permisos: qué marcar y qué no

- **Scopes de lectura estrechos** para tus propios flujos [8]: `drive.file` (solo ve ficheros que crea la app o que tú eliges), `gmail.metadata` o `gmail.readonly`, `spreadsheets.readonly` y `calendar.events.readonly`.
- **Lo que no se puede acotar** [8]: `gmail.readonly` da todo el buzón (no hay scope por etiqueta); `calendar.readonly` da todos tus calendarios; el MCP oficial hereda todos los permisos de quien lo autoriza.
- **Escritura**: mejor dejarla en «pedir aprobación». Bloquea en la consola los scopes de alto riesgo (enviar correo, borrar ficheros) [4][8].
- **Hojas o carpetas concretas**: no des acceso a todo el Drive; usa una cuenta de servicio (más abajo).

## Qué pedir al administrador de Google Workspace

Pásale este texto tal cual:

> Hola `<nombre>`. Quiero usar los **conectores oficiales de Google de Claude** (Anthropic) con mi cuenta de empresa `<mi@correo>`, en **solo lectura** al principio. Google me bloquea con «el administrador debe revisar Claude». Lo resuelves una vez en admin.google.com:
>
> 1. Menú > Seguridad > Acceso y control de datos > Controles de API > **Administrar el acceso de aplicaciones de terceros**.
> 2. «Añadir aplicación» > «Nombre de la aplicación OAuth» > busca **Claude** y márcala como **De confianza** (Trusted). Una sola aprobación cubre Gmail, Calendar, Drive y la edición de Docs, Sheets y Slides. Tarda unos 15 minutos en aplicarse.
> 3. Si prefieres acotar: en lugar de «De confianza», elige **Datos específicos de Google** y autoriza solo scopes de lectura: `gmail.readonly`, `drive.readonly`, `calendar.readonly` (y `spreadsheets.readonly` si lo vamos a usar). Se puede aplicar solo a una unidad organizativa o a mi usuario.
> 4. Para flujos con n8n o scripts: crea (o déjame crear) un proyecto de Google Cloud con pantalla de consentimiento **Interna**, que no necesita verificación de Google. Para una hoja o carpeta concreta, mejor una **cuenta de servicio sin delegación de dominio**, con la hoja o carpeta compartida como **Lector**.
> 5. **No** actives la delegación de todo el dominio: permitiría suplantar a cualquier usuario.
> 6. Si usamos ChatGPT, lo mismo con la aplicación OpenAI/ChatGPT, y que no activen las acciones de escritura todavía.
>
> Mis datos van bajo el plan `<Team / Enterprise / Pro>` de Claude. Si hay política de «solo Gemini», dime qué necesitas para evaluarlo y te preparo la ficha de seguridad. ¿Cuándo lo tendrías?

Aviso: los cambios en la consola pueden tardar hasta 24 horas [4].

## Varias cuentas de Gmail: el conector solo autoriza una

La documentación dice que Claude accede a «la cuenta de Google que has conectado» [1] y no ofrece conectar varias a la vez (no verificado que no exista una función oculta; en clase se comprobó que solo admite una). Opciones, de más simple a más compleja:

1. **Reenvío o consolidación.** En cada cuenta secundaria, activa el reenvío a la principal (Gmail > Configuración > Reenvío y correo POP/IMAP) con una etiqueta o filtro que las distinga. Tu agente lee un solo buzón. Es lo más simple y no cuesta nada. Contra: respondes desde la principal salvo que configures «Enviar como».
2. **Dos arneses (dos carpetas de proyecto).** Un proyecto por cuenta o por negocio, cada uno con su sesión de Claude conectada a su cuenta de Google y su propia carpeta `01-TOOLS/`. Útil si las cuentas son de empresas distintas y no quieres mezclar datos. Contra: dos sitios que mantener. Comprueba en tu plan si puedes tener sesiones con cuentas distintas.
3. **Delegación de Gmail.** Una cuenta da acceso delegado a otra. Que el conector de Claude lea el buzón delegado: no verificado.
4. **n8n con una credencial por cuenta.** Cada nodo de Gmail usa su propia credencial. Sirve para flujos programados, no para el chat.
5. **Cuenta de servicio con delegación de dominio (solo Workspace).** Puede leer buzones de usuarios del mismo dominio, pero Google recomienda evitarla: limita scopes y no limita a qué usuarios suplanta [8]. Último recurso y con el administrador.

Recomendación: reenvío para ver, dos arneses para separar.

## Google Drive sincronizado como carpeta de Cowork o Claude Code

Cowork y Claude Code trabajan con una carpeta del ordenador. «Google Drive para escritorio» crea una unidad de Drive en el explorador o en Finder y copia los cambios entre la nube y el ordenador [9]. Para el agente es una carpeta más.

- **Cómo.** Instala Drive para escritorio, elige la carpeta de trabajo (por ejemplo, `Drive/Empresa/RAW`) y apunta tu arnés a esa ruta.
- **Ficheros de Google.** Los Docs y Sheets suelen aparecer como accesos directos (`.gdoc`, `.gsheet`), no como contenido: el agente no los lee. Exporta a `.docx`, `.xlsx` o PDF, o usa el conector de Drive para esos. Comportamiento habitual, no verificado en esta consulta.
- **Stream o mirror.** Drive permite elegir entre transmitir o tener copia local completa [9]. Para que el agente vea los ficheros, usa copia local o márcalos como disponibles sin conexión. Detalle no verificado en la fuente consultada.
- **Riesgo.** Si el agente tiene escritura, puede modificar o borrar ficheros que se sincronizan con la nube y con tu equipo. Trabaja sobre una subcarpeta, no sobre todo Drive, y usa carpeta aparte (`out/`) para lo que genera. Si la carpeta es compartida, no pongas en ella la clave `.env`.
- **Misma carpeta en dos máquinas.** El arnés puede ir en Git y los datos pesados en Drive. No pongas `.env` en una carpeta sincronizada.

## n8n o Apps Script con permisos de solo lectura

**n8n con app propia.** Crea en Google Cloud un cliente OAuth con los scopes de lectura de arriba. En Workspace, con pantalla Interna, no caduca a los 7 días. En @gmail.com Externa en Testing, sí [5]. Cambiar la contraseña de Gmail también invalida el token si incluye scopes de Gmail [5]: reconecta la credencial en n8n.

**Cuenta de servicio (la vía más acotada).** Es un «empleado robot» con su propio email [10]:

1. En Google Cloud: IAM y administración > Cuentas de servicio > Crear. Anota su email.
2. Crea una clave JSON y guárdala solo en `01-TOOLS/GOOGLE/.env` (se descarga una sola vez) [10].
3. En la hoja o carpeta, pulsa Compartir, añade el email como **Lector** y desmarca «Notificar» [10].
4. No hace falta rol de administrador ni delegación de dominio [10]. La cuenta solo ve lo que le compartes.

**Apps Script.** Corre dentro de tu cuenta y es ideal para prototipos (un alumno hizo uno en un día). Para limitarlo a leer, declara los scopes en el manifiesto `appsscript.json` (campo `oauthScopes`, por ejemplo `spreadsheets.readonly`) en lugar de dejar que Google los deduzca; scopes demasiado amplios pueden fallar la revisión si publicas el script [11]. Sintaxis exacta del campo: no verificada aquí; consúltala en la referencia del manifiesto.

Dile a tu agente: *«Prepara `01-TOOLS/GOOGLE` con una cuenta de servicio de solo lectura sobre la hoja `<nombre>` y un `test_connection`.»*

## Google Sheets como base de datos ligera y Looker Studio

Sheets sirve como base de datos de una pyme mientras haya **pocas personas escribiendo y pocas miles de filas**. Reglas:

- **Una pestaña por tabla**, una fila de cabecera, una fila por registro, sin celdas combinadas ni totales en medio.
- **Una columna `id`** única y otra `actualizado`. El agente no debe buscar por posición de fila.
- **Una pestaña de entrada** (formularios, flujos) y otra **de lectura** (fórmulas y resúmenes).
- **Lectura por defecto**: la cuenta de servicio como Lector. Si hay que escribir, que sea en una pestaña concreta, con aprobación.
- **Copia de seguridad.** Historial de versiones de Sheets más una exportación mensual.
- **Cuándo migrar.** Muchas escrituras simultáneas, relaciones complejas o cientos de miles de filas: pasa a una base de datos real. Ver [conectar o migrar](./conectar-o-migrar.md).

**Looker Studio** (desde abril de 2026 vuelve a llamarse **Data Studio**) [catálogo] es el escaparate: dibuja gráficos sobre una hoja. La relación importante:

- La API de Data Studio **solo busca y gestiona informes y fuentes; no devuelve los datos de los informes** [12]. Tu agente no puede «leer el dashboard».
- Por tanto, conecta tu agente a la **fuente** (la hoja, GA4 o BigQuery) y deja Data Studio como visor. Pide lectura en la fuente, no acceso a la API de Data Studio [12].
- GA4 tiene MCP oficial local y experimental, de solo lectura (`analytics.readonly`). Pide que añadan el email de la cuenta de servicio como **Lector** solo en la propiedad GA4 de la web [13]. La cuenta demo de Google no sirve para la Data API [13].
- Si cambias la estructura de la hoja (columnas, nombres de pestaña), los gráficos de Data Studio se rompen. Avisa al equipo.

## Pruébalo gratis

1. **Cuenta @gmail.com y conectores de Claude:** funcionan en todos los planes, incluido Free [1].
2. **APIs de Google y nodos de n8n:** 0 €, con la salvedad del token de 7 días en modo Testing [5][8].
3. **Controles de administrador:** prueba de Google Workspace de 14 días (ficha del catálogo, consultada el 2026-10-09) [8].
4. **MCP oficial de Google:** pide cuenta Workspace y alta gratuita en el Developer Preview Program [7].

## Qué puedes automatizar después

- [Resumen del lunes](./resumen-del-lunes.md): correo y calendario de la semana.
- [Leads y atención](./leads-y-atencion.md): correo entrante a una hoja de seguimiento.
- [Facturas a contabilidad](./facturas-a-contabilidad.md): adjuntos de Gmail a carpetas de Drive por cliente.
- [Fuente única](./fuente-unica.md): una hoja de Sheets como verdad única.

## Preguntas de alumnos

**1. ¿Puedo conectar más de una cuenta de Gmail a Claude?**
No con el conector: solo una. Usa reenvío a una cuenta principal o un arnés por cuenta (apartado de varias cuentas).

**2. ¿El conector de Gmail envía correos o solo lee?**
Lee, crea borradores y, con tu aprobación, envía, responde y reenvía [1]. En ChatGPT, la escritura la activa un administrador del workspace [2].

**3. ¿Los conectores de Google están en todos los planes de Claude?**
Sí, de Free a Enterprise. En Team y Enterprise, el Owner los activa antes [1].

**4. ¿Cowork trata una carpeta de Drive sincronizada como una carpeta normal?**
Sí para los ficheros normales (PDF, Word, Excel). Los Docs y Sheets nativos son accesos directos y hay que exportarlos o leerlos con el conector (apartado de Drive).

**5. En mi cuenta gratuita de Gmail el token caduca y hay que reconectar. ¿Por qué?**
Porque es una app OAuth Externa en modo Testing: el token dura 7 días [5]. Usa los conectores de Claude, o Workspace con app Interna.

**6. ¿Existe una extensión de Claude o ChatGPT para Google Sheets?**
El conector de Claude crea y edita Sheets en un panel lateral (beta) [1]. Equivalente exacto del complemento de Excel: no verificado.

**7. ¿Se pueden guardar adjuntos de correo en carpetas de Drive según el cliente?**
Sí, con n8n: trigger de Gmail, extraer adjunto, nodo de Drive. Pruébalo primero con una carpeta de prueba.

**8. ¿Es seguro darle acceso a mis emails?**
Depende del plan (datos de entrenamiento) y de los permisos. Empieza en solo lectura, con cuenta o buzón acotado y mira [planes, privacidad y costes](./planes-privacidad-y-costes.md). Ojo con las instrucciones escondidas en correos.

**9. ¿Puede el agente leer solo una carpeta de Drive o una hoja?**
Con el conector de Claude, no se puede acotar. Con cuenta de servicio y compartiendo solo esa carpeta o hoja como Lector, sí [8][10].

**10. ¿Puede leer Claude un dashboard de Looker Studio?**
No por la API [12]. Conecta la fuente de datos.

## Errores típicos

- Pedir al administrador «acceso a Google» sin más. Dale el nombre de la app, los scopes y el menú.
- Creer que ser Owner en Claude te da permiso en Google. Son dos paneles distintos.
- Publicar la app OAuth «Externa» para uso propio: te lleva a la verificación de Google.
- Dar delegación de dominio para leer una sola hoja.
- Sincronizar todo Drive con un agente que puede escribir.
- Poner `.env` o claves JSON en una carpeta de Drive.
- Esperar que el conector envíe adjuntos o lea imágenes de dentro de documentos [1].
- Cambiar la contraseña de Gmail y no reconectar el flujo [5].

## Fuentes

1. Anthropic, «Use Google Workspace connectors», https://support.claude.com/en/articles/10166901-use-google-workspace-connectors, consultado el 2026-10-09.
2. OpenAI, «Google app data controls FAQ» y notas de versión de ChatGPT Business, https://help.openai.com/en/articles/10408842-google-app-for-chatgpt-data-controls-faq y https://help.openai.com/en/articles/11391654-chatgpt-business-release-notes (vistos en resultados de búsqueda; la página directa no se pudo abrir), consultado el 2026-10-09.
3. Guías de terceros sobre conectores de ChatGPT, p. ej. https://www.usecarly.com/blog/chatgpt-connectors/, consultado el 2026-10-09 (fuente secundaria).
4. Google, «Control which apps access Google Workspace data», https://knowledge.workspace.google.com/admin/apps/control-which-apps-access-google-workspace-data, consultado el 2026-10-09.
5. Google, «Using OAuth 2.0 to access Google APIs», https://developers.google.com/identity/protocols/oauth2, consultado el 2026-10-09.
6. Google, «Restricted scope verification», https://support.google.com/cloud/answer/13464321, consultado el 2026-10-09.
7. Google, «Configure Workspace MCP servers», https://developers.google.com/workspace/guides/configure-mcp-servers, consultado el 2026-10-09.
8. Catálogo del proyecto, ficha `google-workspace`, verificada el 2026-10-09 (fuentes: https://workspace.google.com/intl/es/pricing y las citadas en la ficha).
9. Google, «Drive for desktop», https://support.google.com/a/users/answer/13022292, consultado el 2026-10-09.
10. Google, «Create access credentials», https://developers.google.com/workspace/guides/create-credentials, consultado el 2026-10-09.
11. Google, «Manifests (Apps Script)», https://developers.google.com/apps-script/concepts/manifests, consultado el 2026-10-09.
12. Catálogo del proyecto, ficha `data-studio`, y https://developers.google.com/looker-studio/integrate/api, verificada el 2026-10-09.
13. Catálogo del proyecto, ficha `google-analytics`, y https://github.com/googleanalytics/google-analytics-mcp, verificada el 2026-10-09.

## Related

- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md)
- [Conectar Microsoft 365](./conectar-microsoft-365.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Conectar o migrar](./conectar-o-migrar.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
