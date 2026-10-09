---
type: article
title: Tu Excel como fuente de datos para la IA
description: Cómo trabajar bien con Excel y hojas de cálculo junto a la IA (que no se invente datos, estructurar el fichero, cruzar y limpiar, llevarlo a la nube) y cuándo el Excel se queda corto, para dueños y directivos de pymes.
tags: [guia-alumnos, excel, google-sheets, microsoft-365, power-bi, datos, solo-lectura]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Tu Excel como fuente de datos para la IA

> Para: dueños y directivos cuyo negocio vive en Excel y correo, sin necesidad de programar.
> Conseguirás: que la IA analice tus hojas sin inventarse cifras, un Excel que entienda, el fichero en la nube para que un agente lo lea, y criterio para saber cuándo toca dar el salto a una base de datos.

## En resumen
- **Por qué importa.** Entre los alumnos con datos, 33 de 88 trabajan con «Excel y correo», y 16 lo dicen tal cual: «todo en Excel y email». Excel es el primer «sistema» de la pyme. Si tu agente lee bien tu Excel, ya tienes medio arnés montado.
- **Dónde está el valor.** La conexión es sencilla (5 minutos). Lo difícil es **trabajar bien**: que los cálculos sean fiables, que la hoja esté ordenada y que no se cuelen datos sensibles.
- **Quién actúa.** Tú. Si el Excel está en Microsoft 365 o Google Workspace, el administrador solo interviene para permitir un complemento o un conector.
- **Vía recomendada.** Excel en la nube (OneDrive, SharePoint o Drive) + una tabla limpia por hoja + IA que **calcule con código** y no «de cabeza» + totales de control que compruebas tú.

## Antes de empezar

1. **Haz una copia** del Excel y trabaja sobre la copia. Es tu red de seguridad.
2. **Decide dónde vive**: en la nube (mejor) o en el disco de tu PC. Un agente solo ve la nube; un Excel local hay que subirlo cada vez o moverlo.
3. **Mira qué datos tiene.** Si hay DNI, nóminas o datos de clientes, lee antes [planes, privacidad y costes](./planes-privacidad-y-costes.md) y la sección de datos sensibles más abajo.
4. **Plan de IA.** Para el chat basta cualquiera. Para complementos dentro de Excel, depende del plan (tabla siguiente).

## Las vías, de mejor a peor

Los datos de planes están verificados el 2026-10-09 salvo donde digo «no verificado».

| # | Vía | Para qué sirve | Quién lo hace | Coste | Dificultad |
|---|-----|----------------|---------------|-------|------------|
| 1 | Subir el Excel al chat de Claude o ChatGPT y pedir que **calcule con código** | Análisis puntuales, revisiones, limpieza | Tú | Tu plan actual | Baja |
| 2 | Complemento **Claude para Excel** | Trabajar dentro del libro abierto, con citas a celdas. Disponible de forma general en Pro, Max, Team y Enterprise; en Excel web, Windows y Mac recientes [1] | Tú; el admin puede desplegarlo | Incluido en tu plan | Baja |
| 3 | **ChatGPT para Excel** (y Google Sheets) | Lo mismo desde ChatGPT. Según un resumen de búsqueda, disponible en todos los planes con límites de uso según plan; no verificado en la ayuda oficial de OpenAI [2] | Tú; el admin puede desplegarlo con manifiesto | Según plan | Baja |
| 4 | **Copilot en Excel** | Chat y modo agente en el libro. Puede no estar incluido en tu suscripción: depende de la licencia y de la organización [3]. La función `=COPILOT()` está en beta y exige licencia premium de Copilot; no disponible aún en el EEE, según Microsoft [4] | Tú + IT | Licencia Copilot aparte (precio no verificado) | Media |
| 5 | **Gemini en Google Sheets** | Panel de Gemini y función `=AI()` dentro de la hoja | Tú | Según edición de Workspace: la función `=AI()` se anunció para Business Standard y Plus, Enterprise Standard y Plus [5]. Business Starter (6,80 €/usuario/mes en el catálogo) no aparece: confírmalo en tu consola | Baja |
| 6 | Excel en OneDrive/SharePoint o Drive + agente (conector, Power Automate, n8n, Claude Code) | Que un agente lo lea sin que lo subas cada vez | Tú o IT | 0 € de API extra | Media |

**Funciona en el Excel de empresa?** Claude para Excel sí, es un complemento de Microsoft 365 que el admin despliega desde el Centro de administración (Configuración > Aplicaciones integradas > Complementos > «Claude para Microsoft 365»). No funciona en Excel 2016 y 2019 de licencia perpetua, ni en iPad ni en Android [1]. Un alumno vio que dependía de la política de seguridad de la empresa: es una decisión de IT, no un fallo.

**Y para Google Sheets?** Existe «Claude for Sheets», un complemento gratuito de Google Workspace Marketplace que añade las funciones `=CLAUDE()`, pero funciona con **tu clave de API de Anthropic** y se factura por uso; su ficha se actualizó por última vez en abril de 2025 [6]. Los resúmenes de búsqueda no confirman un complemento de Sheets al estilo del de Excel. Para ChatGPT, mira la fila 3.

## Paso a paso: tu primer análisis fiable

La IA se inventa cifras cuando «lee» la tabla como si fuera texto y suma de cabeza. Es como pedirle a un becario que sume 3.000 facturas mentalmente. La solución es la misma que con el becario: dale una calculadora.

1. **Prepara el fichero** (sección siguiente: una tabla por hoja, cabeceras, sin celdas combinadas).
2. **Pide que calcule con código.** Frase exacta: *«Analiza este Excel escribiendo y ejecutando código (Python). No calcules de cabeza. Enséñame el código y el resultado.»* En ChatGPT y Claude, el análisis con código se activa al subir el fichero con la herramienta de análisis disponible. Si tu plan no la tiene, la IA estimará: desconfía.
3. **Exige totales de control.** Antes de analizar, que te diga: número de filas, suma de las columnas de importes, mínimos y máximos. **Compáralos tú con Excel** (barra de estado al seleccionar la columna). Si no coinciden, para.
4. **Haz la auditoría en dos pasadas.**
   - *Pasada 1:* la IA propone las inconsistencias que encuentra (duplicados, fechas imposibles, importes negativos, IDs repetidos) **y el código que las detecta**.
   - *Pasada 2:* en una conversación **nueva**, otra IA o el mismo modelo revisa solo la lista de hallazgos contra el fichero. Descarta todo hallazgo que no venga con la fila exacta.
5. **No hagas una tercera auditoría «por si acaso».** Una alumna preguntó si la IA inventará errores si siempre debe dar un resultado. Sí puede: cuando no hay nada que encontrar, dile explícitamente *«si no hay errores, responde "sin hallazgos"»*. Dos pasadas con evidencia son mejor que cinco sin ella.
6. **Que cite las filas.** Cada afirmación lleva el número de fila o la celda. Lo que no se puede citar, no se cree.
7. **Cambios, siempre en una copia** y con una hoja «Cambios» que liste lo que se tocó.

Dile a tu agente: *«Lee `datos/ventas.xlsx` en solo lectura, calcula con código y dame filas, sumas de control y los 5 hallazgos con su fila.»*

## Estructura el Excel para que la IA lo entienda

| Regla | Mal | Bien |
|---|---|---|
| Una tabla por hoja | Tres tablas en una hoja, con títulos entre medias | Una hoja = una tabla; otra hoja para resúmenes |
| Cabeceras en la fila 1 | Logotipo, fecha y título arriba; cabecera en la fila 7 | Cabecera única, en la fila 1, sin saltos |
| Sin celdas combinadas | «Cliente» combinado sobre tres columnas | Una columna por dato, repetida en cada fila |
| Un dato por celda | «Madrid - 28001 - 2 pisos» | Tres columnas |
| Un ID por fila | Nombre de cliente escrito de tres maneras | Código de cliente o artículo único |
| Formatos fijos | Fechas como texto, importes con «€» escrito | Fecha real, número real, moneda en la cabecera |
| Sin totales dentro de los datos | Fila «TOTAL» en mitad | Los totales en otra hoja o tabla dinámica |
| Colores sin significado | «Los rojos son impagados» | Una columna «Estado» con el valor escrito |

**Truco:** convierte el rango en **tabla de Excel** (Ctrl+T) con nombre. Graph, Power Automate y la IA la leen con más fiabilidad que un rango de celdas [7]. Si el Excel ya está hecho un lío, pídele a la IA: *«Propón una versión limpia de esta hoja y dime qué cambia, sin tocar el original.»* Sirve para corregir datos mal estructurados.

Una pyme de transporte marítimo tiene su Excel de tarifas y costes como pieza crítica. Cuando solo una persona lo entiende, añade una hoja «Léeme» con qué significa cada columna: ayuda a la IA y a tu equipo.

## Llevar el Excel a la nube

Un agente solo lee lo que está en la nube. Con el Excel en el disco, tendrías que subirlo en cada conversación.

- **Microsoft 365:** guarda el libro en **OneDrive** (personal de la empresa) o **SharePoint** (compartido). Cómo conectar el conector de Claude, los permisos y Sites.Selected: [Conectar Microsoft 365](./conectar-microsoft-365.md). Un Excel en un servidor de ficheros local necesita moverse o sincronizarse antes [7].
- **Google Workspace:** sube el fichero a **Drive**, o conviértelo a Google Sheets (Archivo > Guardar como Hojas de cálculo de Google). Revisa después fórmulas especiales y macros, que no se convierten igual. El MCP oficial y los conectores de Google existen; la escritura está acotada y el MCP hereda todos los permisos de quien lo autoriza [8].
- **Permiso mínimo.** Dedica una carpeta (por ejemplo, «IA-lectura») y comparte con la cuenta del agente solo esa. Rol **Lector**.
- **Mira cuántas filas.** Un Excel enorme no cabe en un chat. Un alumno gastó el 90 % del límite de su plan Pro en dos horas cruzando facturas y extractos bancarios. Con ficheros grandes, que el agente los procese con código en tu ordenador y solo te cuente los resultados.

## Cruzar dos Excel y limpiar

- **Cuenta de explotación desde dos ficheros** (por ejemplo, ventas y gastos). Pide: *«Une los dos ficheros por el código de cuenta. Dime qué filas de cada uno no tienen pareja.»* Revisa primero las filas sin pareja: ahí viven los errores.
- **Comisiones contra el CRM.** Exporta el Excel del operador y el del CRM, y cruza por un ID común (contrato o cliente). Si no hay ID, el cruce por nombre falla: crea una columna «clave» (NIF o referencia) antes. Si el CRM no tiene API, la exportación a Excel es la vía buena (ver [conectar o migrar](./conectar-o-migrar.md)).
- **Duplicados.** Pide primero un **informe** («¿qué filas parecen duplicadas y por qué?») y decide tú qué fila se queda. Nunca «borra duplicados» sin informe.
- **PDF o Word a plantilla Excel.** Se puede: la IA extrae los datos y los coloca en celdas concretas de una plantilla. Da la plantilla con las celdas marcadas y pide una hoja de «Origen» que diga de qué página sale cada dato. Si el PDF es un escaneo, revisa los números con más cuidado.
- **Facturas a Excel y gestoría:** [facturas a contabilidad](./facturas-a-contabilidad.md).

## Pedidos por correo o WhatsApp que alguien copia a mano

Es el caso más repetido: llega el pedido por WhatsApp o correo, y alguien lo teclea en un Excel y luego en el programa de gestión. Receta: la IA lee el mensaje, extrae cliente, artículos y cantidades, los anota en el Excel con una columna «Revisar» y tú apruebas antes de pasar nada al programa. Mira [presupuestos, pedidos y albaranes](./presupuestos-pedidos-albaranes.md) y [WhatsApp a pedidos](./whatsapp-a-pedidos.md). Nunca uses librerías no oficiales de WhatsApp: Meta puede bloquear tu número.

## Datos sensibles: anonimiza antes

- Revisa tu **plan** antes de subir datos personales: [planes, privacidad y costes](./planes-privacidad-y-costes.md). En Claude para Excel, las entradas y salidas se borran del servidor en 30 días, y no hereda la retención personalizada de tu organización [1].
- **Anonimiza antes.** Cambia nombres, NIF, IBAN y emails por códigos («Cliente 0042») y guarda la **tabla de equivalencias en otro fichero** que no subes. Después, con esa tabla, revierte los códigos en el resultado.
- **No pegues** claves ni contraseñas en una hoja que la IA vaya a leer.
- **Inyección de instrucciones.** Un Excel ajeno (de un proveedor, descargado) puede esconder órdenes para engañar al agente. Úsalo solo con hojas de confianza y en copia [1].
- Hay quien ha creado un anonimizador de Excel que funciona en el navegador, para que los datos no salgan del ordenador. Es una buena idea: pregunta a tu agente si puede montarte uno.

## Permisos: qué marcar y qué no

- **Empieza en solo lectura.** Para analizar no hace falta escribir.
- **Escribir en el libro** (complementos o conectores con escritura) solo con aprobación humana y sobre copia.
- **Cuenta dedicada** para el agente, nunca tu cuenta de administrador.
- **Microsoft:** `Files.Read` mejor que `Files.Read.All`; SharePoint con `Sites.Selected` y rol `read` en el sitio concreto. Detalle en el manual de Microsoft 365.
- **Google:** `drive.file` o `spreadsheets.readonly`; cuenta de servicio sin delegación de dominio con solo esa hoja compartida como Lector [8].
- **Power BI sobre el mismo Excel:** usuario con rol **Viewer** y permiso **Build** solo en el modelo necesario. Pro: 14 $/usuario/mes anual; prueba de 60 días según terceros [9].

## Qué pedir a tu informático

> Hola `<nombre>`. Quiero usar el complemento oficial «Claude para Microsoft 365» (Anthropic) en Excel. Necesito que lo despliegues desde el Centro de administración de Microsoft 365 (Configuración > Aplicaciones integradas > Complementos) solo para `<mi usuario / grupo IA-lectura>`. Si la Tienda de Office está bloqueada, puede desplegarse con el manifiesto XML. Antes dime si hay una política que lo impida. Los libros estarán en OneDrive/SharePoint, y los datos personales irán anonimizados. ¿Lo vemos esta semana?

## Pruébalo gratis

1. **Chat:** sube una copia anonimizada de tu Excel a tu plan actual y pide el análisis con código. Sin coste extra.
2. **Complementos:** Claude para Excel exige un plan de pago (Pro o superior) [1]. En ChatGPT y Gemini, depende del plan: comprueba el tuyo.
3. **Google:** una cuenta de Gmail personal sirve para probar con Sheets; para Gemini en Sheets en la empresa hace falta la edición adecuada (ver tabla).
4. **Power BI:** prueba gratuita de Fabric y de Pro de 60 días (según terceros), con email de empresa [9].

## Cuándo el Excel se queda corto

Señales de que ya no basta, aunque la IA lo lea bien:

1. **Varias personas editan a la vez** y aparecen versiones («Pedidos_final_v3»).
2. **Más de 50.000 filas**, o fórmulas que tardan minutos.
3. **Necesitas permisos distintos**: que ventas vea pedidos y no márgenes.
4. **Copias y pegas entre hojas** cada semana. Si son más de 3-4 horas a la semana, hay ahorro serio.
5. **Quieres alertas, historial o una app** que escriba datos sola.
6. **Tu Excel «calcula la empresa»** y solo una persona lo entiende: riesgo de continuidad.

Qué hacer, de menos a más:

- **Ordenar el Excel** y llevarlo a la nube (lo de arriba). Vale para casi todos.
- **Base de datos ligera**: Airtable (hoja con relaciones, sin programar) o Supabase (base de datos real, más técnica; la monta tu agente con ayuda). Sirve cuando el dolor es compartir y validar datos.
- **ERP o programa de gestión** (Holded, Odoo…): cuando el Excel hace de facturación, stock y contabilidad. Antes de migrar, haz la cuenta: [conectar o migrar](./conectar-o-migrar.md).
- **Mientras tanto**, un Excel ordenado en la nube es la «fuente única» perfecta: [fuente única](./fuente-unica.md).

## Qué puedes automatizar después

- [Fuente única](./fuente-unica.md): un Excel o Sheets como verdad única de un área.
- [Resumen del lunes](./resumen-del-lunes.md): cifras de tu Excel cada semana.
- [Facturas a contabilidad](./facturas-a-contabilidad.md): facturas del correo a una hoja.
- [Presupuestos, pedidos y albaranes](./presupuestos-pedidos-albaranes.md).
- [Leads y atención](./leads-y-atencion.md): del correo a una hoja de seguimiento.
- Informes y cuadros de mando en Power BI sobre el mismo fichero.

## Preguntas de alumnos

**1. El análisis de mi Excel con GPT es poco fiable y se inventa datos. ¿Cómo lo evito?**
Pídele que calcule con código y te enseñe el código, exige totales de control (filas y sumas) que compruebas tú, y haz auditoría en dos pasadas con cita de fila.

**2. Si siempre da un output, ¿en la tercera auditoría inventará errores?**
Puede. Por eso: máximo dos pasadas, cada hallazgo con su fila, y la instrucción «si no hay errores, responde "sin hallazgos"».

**3. ¿El complemento de Claude funciona solo desde Chrome o también en el Excel de empresa?**
Funciona en Excel web, Windows y Mac recientes con Microsoft 365, en Pro, Max, Team y Enterprise [1]. El admin lo despliega; si la política de seguridad lo bloquea, hay que pedirlo a IT.

**4. ¿Existe el complemento de Claude o ChatGPT para Google Sheets?**
ChatGPT: según OpenAI hay versión para Excel y Sheets [2] (no verificado en la ayuda primaria). Claude: complemento «Claude for Sheets» con clave de API y pago por uso [6]. Gemini viene dentro de Sheets según la edición [5].

**5. ¿Puedo hacer lo mismo con Outlook y Excel que con Gmail y Google Sheets?**
Sí. Cambian conector y permisos: mira [Conectar Microsoft 365](./conectar-microsoft-365.md).

**6. ¿Se puede automatizar una cuenta de explotación a partir de dos ficheros Excel?**
Sí: cruce por código de cuenta, informe de filas sin pareja y revisión humana antes de dar la cuenta por buena.

**7. ¿Se puede pasar un PDF o Word a las celdas de una plantilla Excel?**
Sí, con plantilla marcada y hoja de «Origen». Vale con Power Automate, n8n o con tu agente. Revisa las cifras.

**8. ¿Hay riesgo de filtración al enlazar Claude con un Excel de empresa?**
El riesgo real es doble: lo que subes (revisa tu plan) y un Excel ajeno con instrucciones ocultas [1]. Anonimiza y usa copias.

**9. Las extensiones de Excel agotan los límites y fallan en tareas largas. ¿Qué hago?**
Divide en pasos, trabaja con una hoja cada vez, usa código para lo pesado y guarda la lista de resultados. El complemento compacta la conversación solo cuando se alarga [1].

**10. ¿Es mejor el complemento de ChatGPT o la web de ChatGPT para modificar un Excel?**
El complemento edita el libro abierto, con avisos de sobreescritura; la web sirve para análisis puntuales sobre una copia. Para cambios importantes, la copia es lo más seguro. Mi criterio: no verificado oficialmente.

## Errores típicos

- Pedir «analiza esto» sin decir «con código» y fiarse de la suma que da.
- No comparar los totales de control con los de Excel.
- Subir el Excel original con datos de clientes sin anonimizar.
- Celdas combinadas, tablas dobles en una hoja y cabeceras a media hoja.
- Pedir «borra duplicados» sin informe previo.
- Cruzar dos ficheros por nombre de cliente en vez de por ID.
- Trabajar sobre el original y no sobre una copia.
- Abrir un Excel de un proveedor desconocido con el complemento escribiendo.
- Dejar el Excel en el PC y esperar que el agente lo vea.
- Construir una empresa entera en un Excel que solo entiende una persona.

## Fuentes

1. Anthropic, «Use Claude for Excel», https://claude.com/docs/office-agents/excel, consultado el 2026-10-09.
2. OpenAI, «ChatGPT for Excel», resultados de búsqueda sobre https://help.openai.com/en/articles/20001063-chatgpt-for-excel-and-google-sheets , consultado el 2026-10-09. No verificado en fuente primaria.
3. Microsoft, «Get started with Copilot in Excel», https://support.microsoft.com/en-us/office/get-started-with-copilot-in-excel-d7110502-0334-4b4f-a175-a73abdfc118a, consultado el 2026-10-09.
4. Microsoft, «COPILOT function», https://support.microsoft.com/office/copilot-function-5849821b-755d-4030-a38b-9e20be0cbf62, consultado el 2026-10-09 (resumen de búsqueda).
5. Google, Workspace Updates, «Generate data with Gemini in Google Sheets», https://workspaceupdates.googleblog.com/2025/06/generate-data-with-gemini-in-google-sheets.html, consultado el 2026-10-09. Es de junio de 2025: confirma tu edición hoy.
6. Anthropic, «Google Sheets add-on», https://docs.anthropic.com/claude/docs/google-sheets-add-on, y la ficha en Google Workspace Marketplace, consultado el 2026-10-09.
7. Catálogo del proyecto, ficha `microsoft-365`, verificada el 2026-10-09 (Microsoft Learn, https://learn.microsoft.com/en-us/graph/auth/auth-concepts).
8. Catálogo del proyecto, ficha `google-workspace`, verificada el 2026-10-09 (https://developers.google.com/workspace/guides/configure-mcp-servers).
9. Catálogo del proyecto, ficha `power-bi`, verificada el 2026-10-09 (https://www.microsoft.com/en-us/power-platform/products/power-bi/pricing).

## Relacionado
- [Conectar Microsoft 365](./conectar-microsoft-365.md)
- [Cómo conectar una plataforma a tu arnés RSC](./conectar-una-plataforma-con-rsc.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Conectar o migrar](./conectar-o-migrar.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
