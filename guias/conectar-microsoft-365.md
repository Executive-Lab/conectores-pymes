---
type: article
title: Conectar Microsoft 365 (Outlook, Teams, SharePoint, OneDrive y Excel)
description: Cómo activar el conector de Microsoft 365 en Claude sin esperar 10 días, qué hacer si tu empresa solo autoriza Copilot, y cómo montar Outlook, SharePoint y Excel con Power Automate, n8n o Microsoft Graph con permisos de solo lectura.
tags: [guia-alumnos, microsoft-365, outlook, sharepoint, excel, power-automate, entra-id, solo-lectura]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Conectar Microsoft 365 (Outlook, Teams, SharePoint, OneDrive y Excel)

> Para: dueños y directivos con Microsoft 365 de empresa que quieren que su agente lea correo, calendario, ficheros y Teams.
> Conseguirás: el conector activo en días y no en semanas, una petición lista para tu administrador y las alternativas si IT solo deja Copilot.

## Overview

- **Qué puedes hacer.** Que Claude lea tu correo de Outlook, tu calendario, Teams, OneDrive y SharePoint, y que lea Excel guardado en la nube. También montar recetas (resumen del lunes, briefing diario) con Outlook en lugar de Gmail.
- **Cuánto tarda.** Para ti, 5 minutos. El cuello de botella es una persona: el **administrador global del tenant** (el «tenant» es la oficina digital de tu empresa dentro de Microsoft) tiene que dar un permiso único. Un alumno tardó más de 10 días porque nadie sabía quién ni cómo. Con el texto de más abajo, se resuelve en una conversación.
- **Quién actúa.** Tú, el administrador de Microsoft 365 y, en planes Team o Enterprise de Claude, el propietario de la organización en Claude.
- **Vía recomendada.** El conector oficial «Microsoft 365» de Claude [1]. Si IT solo autoriza Copilot, vías de la tabla de abajo.

## Antes de empezar

1. **Cuenta de empresa.** Necesitas un tenant de Microsoft Entra ligado a un plan Microsoft Business. Las cuentas personales (Outlook.com, Hotmail) **no pueden conectarse** al conector de Claude [1].
2. **Plan de Claude.** El conector está disponible en todos los planes (Free, Pro, Max, Team y Enterprise) [1]. En Team y Enterprise, un **Owner** de la organización de Claude debe añadirlo antes.
3. **Un administrador global de Microsoft Entra** que dé el consentimiento una vez [1].
4. **Datos personales.** Si vas a leer correos de clientes, mira antes qué plan usas: [planes, privacidad y costes](./planes-privacidad-y-costes.md).

## Las vías, de mejor a peor

| # | Vía | Para qué sirve | Quién lo hace | Coste | Dificultad |
|---|-----|----------------|---------------|-------|------------|
| 1 | Conector «Microsoft 365» de Claude | Leer correo, calendario, Teams, OneDrive y SharePoint desde el chat | Tú + administrador global (una vez) | Incluido en tu plan de Claude | Baja |
| 2 | Complemento «Claude for Excel» | Trabajar dentro del Excel abierto (Pro, Max, Team, Enterprise) [2] | Tú; el admin puede desplegarlo | Incluido en el plan | Baja |
| 3 | Power Automate (conectores estándar) | Flujos con Outlook, Excel, SharePoint, Teams dentro de Microsoft | Tú o IT | Estándar incluido en M365; premium desde 13 €/usuario/mes [3] | Media |
| 4 | n8n o script con Microsoft Graph y app registrada | Procesos programados, sitios concretos de SharePoint | IT registra la app; tú el flujo | 0 € de API extra [3] | Media-alta |
| 5 | MCP Work IQ de Microsoft (preview) | Leer y escribir con servidores MCP de Microsoft | IT | Exige licencia Microsoft 365 Copilot | Alta |

## Paso a paso: activar el conector de Claude

### A. Si eres tú quien administra (o tienes al administrador al lado)

1. **Team o Enterprise:** un Owner abre Organization settings > Connectors > Add > All available > Microsoft 365 > «Add to your team». Si no lo hace, los miembros no ven el conector. Esto explica casos de alumnos que «no encuentran» el conector aunque son administradores de Microsoft: son administradores de Microsoft, pero no Owner de Claude [1].
2. **Free, Pro, Max:** no hay paso de organización. Entra en Customize > Connectors, pulsa «Connect» en Microsoft 365 e inicia sesión.
3. El **administrador global** acepta los permisos y marca la casilla de conceder acceso **en nombre de toda la organización** [1].
4. Los demás usuarios del mismo tenant ya no ven pantalla de consentimiento: solo inician sesión [1].

Dile a tu agente: *«Conecta mi Microsoft 365 en solo lectura y dime qué tengo que pedir a mi administrador.»*

### B. Si el administrador no tiene cuenta de Claude (el caso de los 10 días)

Es la ruta manual en Entra ID [1]:

1. El administrador crea **dos entidades de servicio** (service principals) con Microsoft Graph Explorer (`POST https://graph.microsoft.com/v1.0/servicePrincipals`) para estas aplicaciones:
   - `M365 MCP Client for Claude`, appId `08ad6f98-a4f8-4635-bb8d-f1a3044760f0`.
   - `M365 MCP Server for Claude`, appId `07c030f6-5743-41b7-ba00-0a6e85f37c17`.
2. Visita la URL de consentimiento de cada una: `https://login.microsoftonline.com/{tenant-id}/adminconsent?client_id={appId}` [1][4].
3. Un Owner activa el conector en Claude (Team/Enterprise), o cada miembro pulsa Connect.

### Qué ve el administrador

- Una pantalla de consentimiento con la lista de permisos **delegados** (Claude actúa como el usuario y no ve nada que ese usuario no vea) y la casilla de «en nombre de la organización» [1].
- Después, en **Entra admin center > Aplicaciones empresariales**, dos aplicaciones nuevas: «M365 MCP Client for Claude» y «M365 MCP Server for Claude». En «Permisos» puede revocar scopes sueltos; el scope revocado da error «Failed to call tool» [1].
- Sin consentimiento, los usuarios ven un error que dice que un administrador debe conceder permisos [1].
- **Si el administrador no es global:** Microsoft permite dar consentimiento de permisos delegados a roles como Cloud Application Administrator o Application Administrator [4]. Anthropic documenta el rol de administrador global para este conector; si tu admin no lo es, pruébalo: no está verificado.

### Acelerar la aprobación: flujo de solicitud

Un administrador global puede activar el **flujo de consentimiento de administrador**: Entra ID > Aplicaciones empresariales > Consentimiento y permisos > Configuración de consentimiento de administrador. Así los usuarios pulsan «solicitar aprobación» y los revisores reciben un email [5]. Pide que ese email llegue a una persona que lo mire.

## Permisos: qué marcar y qué no

Todos los permisos son delegados [1].

| Bloque | Permisos de lectura (por defecto) |
|---|---|
| Correo | Mail.Read, Mail.ReadBasic, Mail.Read.Shared, MailboxFolder.Read, MailboxItem.Read, MailboxSettings.Read |
| Calendario | Calendars.Read, Calendars.Read.Shared |
| Teams | Chat.Read, ChatMember.Read, ChatMessage.Read, Channel.ReadBasic.All, ChannelMessage.Read.All |
| Reuniones | OnlineMeetings.Read, transcripciones, resúmenes con IA, grabaciones |
| Ficheros | Files.Read, Files.Read.All, Sites.Read.All |

**Solo lee o también escribe.** Por defecto solo lee. Las herramientas de escritura son opcionales: requieren que el administrador global apruebe los permisos de escritura (Mail.Send, Mail.ReadWrite, Calendars.ReadWrite, Files.ReadWrite.All, ChatMessage.Send, ChannelMessage.Send, Chat.Create…) **y** que un Owner las active en Organization settings > Connectors [1]. Las organizaciones que ya usaban el conector las tienen bloqueadas por defecto. Con escritura, Claude puede enviar y redactar correos, gestionar eventos (los invitados reciben aviso automático), editar ficheros de OneDrive y SharePoint y enviar mensajes de Teams. Sigue mi regla: empieza sin escritura y activa solo lo que necesites, con aprobación humana en cada acción [1].

**Limitaciones que debes conocer** [1]:

- La búsqueda en SharePoint cubre **todo el tenant**. No se puede limitar a un sitio concreto con este conector. Para eso, vía 4 (más abajo).
- La búsqueda de correo no incluye el archivo en línea (Online Archive).
- Lee Word, Excel, PowerPoint, PDF y texto. No lee OneNote.
- Mail.Read lee todas las carpetas del buzón y Chat.Read todos los chats del usuario: no se pueden acotar [3].

**Restringir quién lo usa.** En Entra, en las dos aplicaciones empresariales, pon «Asignación requerida» en Sí y asigna un grupo (por ejemplo, «IA-lectura»). Las dos deben tener las mismas asignaciones [1].

Sobre los ejemplos de clase que dicen que «Outlook no deja crear borradores»: eran verdad con el conector solo de lectura. Hoy hay escritura opcional [1]. En tu empresa depende de que el administrador la apruebe.

## Si en tu empresa solo está autorizado Copilot

La IA «única autorizada» no te deja sin opciones. De menos a más gestión:

1. **Copilot y agentes de Copilot.** Lo que la licencia permite: agentes declarativos de Microsoft 365 Copilot con MCP como plugin y Copilot Studio [3]. El rendimiento es el motivo de queja habitual de alumnos; no lo repito aquí.
2. **Power Automate.** Los conectores estándar vienen con Microsoft 365. IT suele aprobarlo con más facilidad que n8n. Cuidado: las acciones premium y el disparador HTTP piden licencia de pago [3].
3. **Complemento Claude for Excel**, si IT permite el complemento [2]. Un alumno vio que depende de la política de seguridad de la empresa.
4. **Datos en local.** Exporta tú un Excel o PDF y trabájalo en tu ordenador. Ojo con datos de clientes: es sacar datos de la empresa y puede incumplir la política.
5. **Pedir que autoricen otra IA.** No uses la IA sin permiso («shadow AI»): es el riesgo que más preocupa a IT. Llévales datos: qué datos tocará, solo lectura, usuario dedicado, plan con contrato y privacidad, cómo se revoca. Usa el texto de la sección siguiente, pensado también para IT.

## Qué pedir a tu informático (texto para el administrador)

> Hola `<nombre>`. Quiero conectar el **conector oficial «Microsoft 365» de Claude** (Anthropic) a mi cuenta para que el asistente lea mi correo, calendario y ficheros de **solo lectura**. Para eso hace falta que un **administrador global de Entra ID** dé el consentimiento de administrador una vez.
>
> Pasos, según la documentación de Anthropic:
> 1. Entra en https://login.microsoftonline.com/`<tenant-id>`/adminconsent?client_id=08ad6f98-a4f8-4635-bb8d-f1a3044760f0 y en la misma URL con client_id=07c030f6-5743-41b7-ba00-0a6e85f37c17 (son «M365 MCP Client for Claude» y «M365 MCP Server for Claude»; si no existen como aplicaciones empresariales, hay que crearlas antes como entidades de servicio con Graph Explorer).
> 2. Los permisos son **delegados** (actúa como el usuario, nunca ve más que él). Los de lectura incluyen Mail.Read, Calendars.Read, Files.Read.All, Sites.Read.All, Chat.Read y ChannelMessage.Read.All. **No apruebes los de escritura** (Mail.Send, Mail.ReadWrite, Files.ReadWrite.All…) por ahora.
> 3. En las dos aplicaciones empresariales, pon «Asignación requerida = Sí» y asigna solo a `<mi usuario / grupo IA-lectura>`.
> 4. Si algún permiso te parece excesivo, puedes revocarlo en Permisos de la aplicación; el conector funcionará sin esa parte.
>
> Mi información queda sujeta al plan de Claude `<Team / Enterprise / Pro>`, sin entrenar con los datos y con contrato de encargo de tratamiento. Si hay política de «solo Copilot», dime qué necesitas para que lo evaluéis: puedo prepararte la ficha de seguridad. ¿Cuándo lo tendrías?

Si tu necesidad es leer un sitio de SharePoint concreto sin ver todo el tenant, pídelo con la plantilla de la vía 4 (más abajo) y no con esta.

## Vía 4: Power Automate o n8n con Microsoft Graph (acceso acotado)

Una «app registrada» es un carnet de empleado para un programa: tiene nombre, permisos y se puede dar de baja sin tocar el tuyo. La crea el administrador en **Entra ID > Registros de aplicaciones**, gratis [3].

**Dos tipos de permiso** [3]:

- **Delegado:** la app actúa como un usuario y nunca ve más que él. Es más seguro. Úsalo mientras haya una persona.
- **De aplicación:** sin usuario, con alcance de todo el tenant salvo que se acote. Todos requieren consentimiento de administrador.

**Permisos de solo lectura recomendados** [3]: `User.Read`, `Mail.Read` (o `Mail.ReadBasic`), `Calendars.Read` y `Files.Read` en lugar de `Files.Read.All`.

**SharePoint limitado a un sitio: Sites.Selected** [6]:

1. El administrador consiente `Sites.Selected`. Por sí solo **no da acceso a nada**.
2. Un administrador con `Sites.FullControl.All` concede el rol a la app en el sitio concreto: `POST /sites/{siteId}/permissions` con `"roles": ["read"]` y la identidad de la aplicación. Los roles son read, write, owner y fullcontrol [6].
3. La app pide un token con ese scope. Si falta alguno de los tres pasos, no hay acceso [6].
4. Revocar: `DELETE` del permiso, o quitar el consentimiento en Entra [6].

Para bajar a lista, carpeta o fichero: `Lists.SelectedOperations.Selected`, `ListItems.SelectedOperations.Selected` o `Files.SelectedOperations.Selected`. Conceder permisos a una carpeta o fichero rompe la herencia de permisos de SharePoint [6].

**Buzones sin usuario.** Usa RBAC for Applications de Exchange Online con un ámbito que limite los buzones, y retira el permiso sin acotar en Entra: si no, se suman los dos y el límite no sirve [3].

**Buenas prácticas** [3]: certificado mejor que secreto; «Asignación requerida = Sí»; el secreto, en `01-TOOLS/MICROSOFT-365/.env` y nunca en el chat.

Dile a tu agente: *«Prepara `01-TOOLS/MICROSOFT-365` con un `test_connection` de solo lectura contra Microsoft Graph y dime qué le pido a IT.»*

**Plantilla para IT (vía 4):**

> Necesito registrar en Entra ID una aplicación «rsc-lectura» para un flujo de lectura. Permisos delegados `User.Read`, `Mail.Read`, `Calendars.Read`, `Files.Read`. Para SharePoint, `Sites.Selected` con rol **read** solo en el sitio `<nombre del sitio>`. Consentimiento de administrador y «Asignación requerida = Sí» para `<usuario o grupo>`. Credencial: certificado o secreto con caducidad de 6 meses, que me entregaréis por canal seguro. Nada de permisos de escritura ni de `.All` sin acotar.

## Outlook en vez de Gmail en las recetas

Las recetas ([resumen del lunes](./resumen-del-lunes.md), briefing diario) leen correo y calendario. Con Microsoft 365 se hace igual, cambiando la fuente:

- **Desde el chat de Claude:** con el conector, pídele el resumen del correo y del calendario de la semana. Funciona en solo lectura.
- **Desde Power Automate:** los conectores de Outlook y Calendario son estándar. Hay un matiz importante: el conector **«Outlook.com»** es solo para cuentas personales y ya no admite cuentas de trabajo; para empresa se usa el conector **«Office 365 Outlook»** [7].
- **Desde n8n:** usa el nodo Microsoft Outlook (con app registrada como arriba).
- **Borradores de respuesta:** con el conector en lectura no se pueden crear. Es una decisión de permisos, no un fallo [1].

## Cuenta personal o cuenta de empresa

| Cosa | Cuenta personal (Outlook.com) | Cuenta de empresa |
|---|---|---|
| Conector de Claude | No admite [1] | Sí, con consentimiento del administrador |
| Power Automate, correo | Conector «Outlook.com» [7] | Conector «Office 365 Outlook» [7] |
| SharePoint, Teams, consentimiento de admin | No existen | Sí |
| Graph con correo y OneDrive | Sí, limitado (ficha del catálogo) | Sí |

Por eso la conexión «OAuth de Outlook» que no funcionaba a un alumno en clase fallaba con su cuenta personal: pide tenant corporativo.

## Excel en OneDrive o SharePoint como fuente de datos

- **Guarda el Excel en OneDrive o SharePoint.** Graph y los MCP solo ven la nube [3]. Un Excel en el disco de tu PC o en un servidor de ficheros local necesita antes moverse a OneDrive o a una carpeta sincronizada.
- **Cómo lo leen los flujos.** La API de Graph lee el libro (tablas, rangos). Pon los datos en **tablas de Excel** con nombre: son más estables que rangos de celdas.
- **Complemento «Claude for Excel»** [2]: disponible en Pro, Max, Team y Enterprise, ya sin etiqueta beta. Funciona en Excel web, Windows y Mac recientes. El admin lo despliega en el Centro de administración de Microsoft 365 (Configuración > Aplicaciones integradas > Complementos > «Claude for Microsoft 365»). No admite macros ni VBA ni tablas de datos, y avisa antes de sobrescribir.
- **Riesgo.** Un Excel de un tercero puede esconder instrucciones para manipular al agente (inyección de instrucciones). Úsalo solo con hojas de confianza y trabaja sobre una copia [2].
- **Datos sensibles.** Anonimiza antes o revisa tu plan. Los consumos largos en Excel gastan mucho límite de uso.

## Pruébalo gratis

1. **Sin pagar:** si tu empresa ya tiene Microsoft 365, con el conector no hay coste extra más allá de tu plan de Claude [1].
2. **Una cuenta personal** sirve para probar Graph con correo, calendario y OneDrive personal, pero no para el conector de Claude ni SharePoint (ficha del catálogo).
3. **Power Automate:** el Developer Plan (Power Apps) es gratis, incluye conectores premium y 750 ejecuciones al mes, pero pide cuenta de trabajo o educativa y no sirve para producción (ficha del catálogo).
4. **Prueba de Microsoft 365 Business de 1 mes:** habitual, no verificado.

## Qué puedes automatizar después

- [Resumen del lunes](./resumen-del-lunes.md) con correo y calendario de Outlook.
- [Fuente única](./fuente-unica.md): un Excel en SharePoint como verdad única.
- [Leads y atención](./leads-y-atencion.md): correo entrante a hoja de seguimiento.
- [Facturas a contabilidad](./facturas-a-contabilidad.md): facturas adjuntas en Outlook a carpeta o Excel.
- Power BI sobre el mismo Excel: consulta [Power BI](https://executive-lab.github.io/conectores-pymes/). Rol Viewer más Build solo en el modelo necesario (catálogo).

## Preguntas de alumnos

**1. Tengo Microsoft 365, ¿cómo conecto el chat de IA al correo, SharePoint y Teams?**
Con el conector «Microsoft 365» de Claude, tras el consentimiento del administrador global (ver paso a paso) [1].

**2. Soy administrador de Microsoft 365 y el conector no me aparece en Claude. ¿Es un fallo?**
Normalmente no. En Team y Enterprise lo debe añadir un Owner de Claude (Organization settings > Connectors). Ser administrador de Microsoft no basta [1]. Si aun así falla, la ruta manual en Entra ID.

**3. ¿Puedo hacer lo mismo con Outlook y Excel que con Gmail y Google Sheets?**
Sí, con conector, Power Automate o n8n. Cambian la fuente y los permisos (apartados de Outlook y Excel).

**4. ¿Funciona el conector con mi cuenta personal de Outlook?**
No [1]. Exige tenant de empresa con plan Business.

**5. ¿El conector solo lee o puede crear borradores y enviar?**
Por defecto solo lee. La escritura es opcional y la aprueban el administrador global y el Owner [1].

**6. ¿Con Power Automate o con n8n?**
Si IT rara vez permite n8n y ya pagas Microsoft 365, Power Automate se aprueba mejor. n8n no tiene licencia por usuario. Con Microsoft 365 tienes los conectores estándar; premium cuesta 13 €/usuario/mes [3].

**7. ¿Puede el agente leer solo una carpeta o un sitio de SharePoint?**
Con el conector de Claude, no: busca en todo el tenant [1]. Con una app propia y `Sites.Selected`, sí [6].

**8. ¿Los documentos deben estar en la nube o puede acceder a los servidores de la empresa?**
Graph y los MCP solo ven la nube. Los servidores locales necesitan exportación a una carpeta sincronizada o un puente [3].

**9. ¿Entrena Microsoft o Claude con mis datos?**
Depende del plan. Mira [planes, privacidad y costes](./planes-privacidad-y-costes.md). En Claude for Excel los datos se borran del backend en 30 días [2].

**10. En mi empresa solo se permite Copilot. ¿Qué hago?**
Lo que cabe en Copilot y Power Automate, y presenta la petición a IT con el texto de arriba. Evita herramientas sin permiso.

## Errores típicos

- Pedir «acceso a Microsoft 365» sin más: el administrador no sabe qué tocar. Da nombre del conector, permisos y appIds.
- Creer que ser administrador de Microsoft equivale a ser Owner en Claude.
- Usar una cuenta personal y esperar que funcione el conector.
- Conceder `Sites.Selected` y olvidar el paso de dar el rol al sitio: la app no ve nada [6].
- Dejar el permiso sin acotar junto al acotado en Entra: se suman [3].
- Aprobar escritura el primer día.
- Pegar secretos o el tenant en el chat. Van en `.env`.
- Dejar que el agente obedezca instrucciones escondidas en correos o Excel recibidos.

## Fuentes

1. Anthropic, «Enable and use the Microsoft 365 connector», https://support.claude.com/en/articles/12542951-enable-and-use-the-microsoft-365-connector, consultado el 2026-10-09.
2. Anthropic, «Use Claude for Excel», https://claude.com/docs/office-agents/excel, consultado el 2026-10-09.
3. Catálogo del proyecto, fichas `microsoft-365` y `power-automate`, verificadas el 2026-10-09 (fuentes: Microsoft Learn, https://learn.microsoft.com/en-us/graph/auth/auth-concepts).
4. Microsoft, «Grant tenant-wide admin consent», https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/grant-admin-consent, consultado el 2026-10-09.
5. Microsoft, «Configure the admin consent workflow», https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/configure-admin-consent-workflow, consultado el 2026-10-09.
6. Microsoft, «Overview of Selected Permissions in OneDrive and SharePoint», https://learn.microsoft.com/en-us/graph/permissions-selected-overview, consultado el 2026-10-09.
7. Microsoft, «Outlook.com connector», https://learn.microsoft.com/en-us/connectors/outlook/, consultado el 2026-10-09.

## Related

- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Conectar o migrar](./conectar-o-migrar.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
