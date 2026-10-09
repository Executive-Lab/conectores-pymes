---
type: article
title: Mi programa no tiene API: cómo conectarlo igualmente (el kit puente)
description: Qué hacer cuando tu ERP, contabilidad, TPV o software sectorial no tiene API, de la vía más segura a la más frágil, para dueños de pymes y sus informáticos.
tags: [guia-alumnos, sin-api, kit-puente, erp, tpv, rpa, base-de-datos, exportacion]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Mi programa no tiene API: cómo conectarlo igualmente

> Para: dueños y directivos con un programa instalado o antiguo (ERP, contabilidad, TPV, software de prevención, channel manager) que «no se puede conectar».
> Conseguirás: elegir en 10 minutos la vía más segura para sacar datos de tu programa (y, si hace falta, meterlos) sin romper nada.

## Overview

Una **API** es una ventanilla por la que otro programa pide datos a tu programa. Muchos programas de pyme no la tienen. Eso no significa que no se puedan conectar: significa que hay que usar **otra puerta**. Este es el «kit puente»: seis puertas, ordenadas de mejor a peor.

- **Cuánto tarda:** una carta al fabricante, un día. Una exportación programada, una tarde con tu informático. Una base de datos de solo lectura, una o dos semanas. RPA, semanas de pruebas.
- **Quién actúa:** tú redactas la petición; tu distribuidor o tu informático monta la puerta; tu agente (Claude Code con el arnés) la usa.
- **Vía recomendada:** casi siempre la 2 (exportación a carpeta) para **leer** y la 4 (fichero de importación) para **escribir**. La base de datos de solo lectura (3) es la segunda opción para leer. El RPA (5) es el último recurso.

Regla de oro: **leer es fácil y seguro; escribir se hace con aprobación humana y por el camino oficial del programa**. Nunca escribas directamente en la base de datos.

## Diagrama de decisión

```
¿Tu programa es de pago por suscripción en la nube (SaaS)?
├─ Sí → casi seguro tiene API o MCP. Mira el catálogo y la guía "Conectar una plataforma". Aquí no hace falta puente.
└─ No (instalado, antiguo o "a medida") ↓

1. ¿Hay versión en la nube del mismo fabricante con API? (Contasol/Factusol Nube, Sage Active, Presto Server/Cloud)
   ├─ Sí → pásate a esa versión. Fin.
   └─ No ↓
2. ¿El fabricante o distribuidor ofrece módulo, API o exportación automática? (Ágora Integration Services, Revo client-token…)
   ├─ Sí → pídelo (vía 1). Fin.
   └─ No / no contestan ↓
3. ¿Puede el programa guardar solo, cada noche, un CSV/Excel/BC3/XML en una carpeta?
   ├─ Sí → vía 2. Fin para leer.
   └─ No ↓
4. ¿Usa una base de datos conocida (SQL Server, MySQL, Access) y el fabricante permite leerla?
   ├─ Sí → vía 3: usuario de solo lectura sobre vistas, por VPN. Fin para leer.
   └─ No ↓
5. ¿Solo necesitas ESCRIBIR (facturas, asientos, pedidos)?
   ├─ Sí → vía 4: el agente prepara un fichero y una persona lo importa.
   └─ No ↓
6. ¿La tarea es corta, repetitiva y con riesgo bajo?
   ├─ Sí → vía 5: RPA con usuario dedicado y aprobación humana.
   └─ No → vía 6: ¿migrar o construir algo propio? Haz la cuenta.
```

## Antes de empezar

- **Averigua qué programa y qué versión tienes.** Menú «Ayuda > Acerca de» o la factura del proveedor. Sin versión exacta, nadie te puede contestar.
- **Averigua quién lo mantiene:** tu informático, tu distribuidor o tu gestoría. Si el programa es de la gestoría, la petición la haces tú a la gestoría.
- **Datos personales o de salud:** mira antes qué plan de IA usas ([planes-privacidad-y-costes.md](./planes-privacidad-y-costes.md)).

## Las vías, de mejor a peor

| # | Vía | Para qué sirve | Quién lo hace | Coste | Dificultad |
|---|-----|----------------|---------------|-------|------------|
| 1 | Pedir módulo, API o exportación al fabricante | Leer y a veces escribir, con soporte | Tú + distribuidor | Puede ser gratis o de pago (según fabricante) | Baja |
| 2 | Exportación programada a carpeta | Leer informes, ventas, listados | Tú o tu informático | Normalmente incluido | Baja-media |
| 3 | Usuario de BD de solo lectura sobre vistas, por VPN | Leer casi todo, casi en tiempo real | Tu informático (con permiso del fabricante) | Horas de informático | Media-alta |
| 4 | Fichero de importación | Escribir (asientos, facturas, pedidos) | El agente prepara, una persona importa | Incluido | Media |
| 5 | RPA de navegador o de escritorio | Último recurso para leer o escribir | Tú + informático | Licencias y mantenimiento | Alta, frágil |
| 6 | Migrar o construir algo propio | Resolver el problema de raíz | Tú + consultor o Claude Code | Según el caso | Alta |

## Paso a paso

### Vía 1. Pregunta al fabricante o al distribuidor

Es gratis y a veces la respuesta es «sí, hay módulo». Dos ejemplos del catálogo: en Ágora, la API existe pero la activa el distribuidor con el módulo Integration Services; en Revo, el client-token lo emite Revo con un formulario. Sin preguntar, no te enteras. Preguntar también deja constancia por escrito de que no pierdes el soporte.

Texto listo para copiar (cambia lo que va entre corchetes):

> Asunto: Consulta sobre integración de [programa] versión [versión]
>
> Hola. Somos clientes con licencia [número o CIF]. Queremos conectar [programa] con una herramienta propia de análisis, **solo para leer datos** ([ventas / facturas / clientes / obras]).
> 1. ¿Existe un módulo, API, webservice o exportación automática? ¿Con qué versión y licencia?
> 2. Si no, ¿pueden dejarnos un **usuario de base de datos de solo lectura** sobre vistas, sin perder el soporte? Confirmadnoslo por escrito.
> 3. ¿Hay documentación técnica? ¿Cuánto cuesta (alta, cuota, horas)?
> 4. ¿Tienen una versión en la nube con API?
> Gracias. [Nombre, teléfono]

### Vía 2. Exportación automática a una carpeta (la recomendada)

La idea: el programa **deja solo un fichero** (CSV, Excel, BC3, XML) en una carpeta cada noche. El arnés lee esa carpeta. Es como pedir que te dejen cada mañana el informe en la bandeja de entrada.

1. **Elige qué sale.** Pocas cosas y útiles: ventas del día, facturas pendientes, stock, obras abiertas.
2. **Busca la función en tu programa.** Casi todos exportan a Excel o CSV desde sus listados. Presto exporta BC3 (el formato estándar de obras, que es texto y se procesa sin Presto). Contasol/Factusol exporta a PDF o XLSX. InstalWin importa y exporta Excel y exporta asientos. HioPos puede exportar por FTP, pero lo configura el distribuidor.
3. **Prográmalo.** Si el programa no tiene planificador, tu informático lo puede lanzar con el Programador de tareas de Windows o con un script. Si no se puede automatizar, la exportación manual semanal ya sirve para empezar.
4. **Elige la carpeta.** Una carpeta en un servidor o sincronizada con OneDrive o Google Drive. El programa solo escribe; el arnés solo lee.
Dile a tu agente: *«Conecta mi [programa] con una exportación programada a carpeta, en solo lectura. Tengo los ficheros en [ruta]».*

Limitación: el dato llega con retraso (el de anoche) y no puedes filtrar por campos más finos que lo que el programa deja exportar.

### Vía 3. Usuario de base de datos de solo lectura sobre vistas, por VPN

Aquí el agente **mira** la base de datos del programa, como quien lee por la ventana. Varios programas del catálogo usan SQL Server (Sage 50, Prevengos, HioPos en FrontRest y ICGManager) o Access (Factusol). Se lee solo si el fabricante lo permite: en Prevengos, por ejemplo, leer la base de datos queda fuera del soporte de Nedatec. **Pregunta antes.**

Qué se monta:

- Un **usuario nuevo y exclusivo** para el agente. Ni el administrador (`sa`) ni el usuario del programa.
- Permiso **solo de lectura** (SELECT) sobre **vistas**: consultas guardadas que enseñan solo las columnas necesarias. Es como dar un cristal con ventanas recortadas en vez de la llave del archivo.
- Acceso **por VPN** (un túnel privado). El puerto de la base de datos (1433, 3306, 5432…) **nunca se abre a internet**.
- Mejor aún: leer de una **copia nocturna** de la base de datos. Así tampoco molestas al programa en horas de trabajo.
- Para Access o ficheros locales, trabaja siempre sobre una copia.

**Por qué nunca se escribe en la base de datos del programa:**

1. El programa guarda sus propias cuentas por dentro (saldos, numeración, relaciones). Si metes datos a mano, los números dejan de cuadrar y nadie lo nota hasta el cierre.
2. En facturación, saltarte el programa rompe la cadena de registros de Veri*factu.
3. Pierdes el soporte del fabricante. Y una actualización puede cambiar el esquema.
4. Si el agente se equivoca, no hay marcha atrás.

Prueba obligada: tras crear el usuario, comprobad que un `SELECT` funciona y que un `INSERT` **falla**.

Para tu informático, el montaje paso a paso (copia nocturna, vistas, servidor MCP de solo lectura, túnel sin abrir puertos) y cuándo compensa pagar una API unificada está en el [kit puente técnico](./kit-puente-tecnico.md).

### Vía 4. Importación en vez de escritura

Para meter datos, el agente **no toca el programa**. Prepara un fichero con el formato de importación del programa, y una persona lo revisa y lo importa con el botón oficial.

- **Asientos contables:** Sage 50 tiene un add-on **gratuito** de importación de asientos (documentado en la ayuda de Sage). A3 (a3asesor) usa el fichero SUENLACE.DAT. ContaSOL importa libros Excel (diario, facturas emitidas y recibidas). Holded y Odoo importan Excel o CSV. Factusol pasa las facturas como asientos a Contasol. Formatos, riesgos y qué cambia con la factura electrónica: [escribir en contabilidad por importación](./escribir-en-contabilidad-por-importacion.md).
- **Presupuestos de obra:** BC3 para Presto; InstalWin importa BC3 con un módulo de pago único.
- **Facturas y pedidos:** pregunta a tu distribuidor qué formato acepta la importación.

El fichero se guarda en `01-TOOLS/<HERRAMIENTA>/out/`. El agente nunca importa solo. Es el mismo patrón que [facturas-a-contabilidad.md](./facturas-a-contabilidad.md).

### Vía 5. RPA de navegador o de escritorio

**RPA** es un robot que usa el programa como lo usaría una persona: mueve el ratón, pulsa botones, copia lo que ve. Sirve cuando no hay otra puerta. Es **frágil**: si cambia una pantalla, un aviso emergente o la resolución, el robot se pierde. Un alumno lo vivió con un ERP web: el agente por navegador iba lento y no conseguía cargar facturas de forma fiable.

**Cuándo sí:**
- Tarea corta, repetitiva y con poco riesgo (consultar un dato, descargar un informe).
- Programa antiguo sin exportación, sin base de datos accesible y sin importación.
- Un portal con usuario y contraseña (inmobiliarios, YouTube Studio) del que solo necesitas leer tus propios datos y cuyas condiciones lo permiten.

**Cuándo no:**
- Para escribir en contabilidad o facturación sin que nadie revise.
- Con datos de salud o personales sensibles.
- Si el proceso es largo o crítico, o si hay una vía 2, 3 o 4 posible.
- Si las condiciones de uso del portal prohíben los robots. Léelas antes.

**Herramientas que existen hoy** (verificadas el 2026-10-09):

| Herramienta | Para qué | Nota |
|-------------|----------|------|
| Power Automate para escritorio (Microsoft) | Automatizar aplicaciones Windows por clics y teclado, con grabadora y selección de elementos de pantalla | Pensada para aplicaciones sin API. La ventana debe estar en primer plano, así que choca si alguien usa ese PC [1] |
| Uso de ordenador de Claude (*computer use*) | Que Claude vea la pantalla y maneje un escritorio | Función beta. Anthropic recomienda máquina virtual aislada, no dar datos sensibles, lista de dominios permitidos y confirmación humana en acciones importantes [2] |
| Playwright MCP (Microsoft) | Que el agente maneje un navegador | `npx @playwright/mcp@latest`, licencia Apache-2.0. No es una frontera de seguridad. Guarda la sesión iniciada en un perfil: bórralo al acabar [3] |
| Claude en Chrome | Que Claude actúe en tu navegador | Beta en planes de pago. Pide permiso por sitio y aprobación antes de descargar o introducir datos sensibles. Anthropic aconseja un perfil de navegador aparte para cuentas sensibles [4] |
| UiPath (RPA clásico) | Robots de escritorio y navegador | Existe edición gratuita, pero las condiciones (uso comercial, robots sin vigilancia) varían: confirma en UiPath antes de usarla. No verificado en fuente oficial [5] |

**Precauciones (todas, no una):**
1. **Usuario dedicado** en el programa y en Windows, con rol de solo consulta y sin permisos de administrador.
2. **Máquina aparte** (un PC o una máquina virtual) para el robot. No tu PC de trabajo.
3. **Aprobación humana** antes de guardar, enviar o pagar.
4. **Tareas cortas** y con un registro de lo que hace.
5. **Acceso remoto sin abrir puertos:** el escritorio remoto (puerto 3389) nunca a internet. VPN o pasarela con doble factor [ver ficha de acceso remoto del catálogo].
6. **La contraseña va en `.env`**, nunca en el chat. Un robot con la sesión de otra persona puede hacer todo lo que esa persona puede.
7. **Lo que el robot lee es dato, no órdenes.** Si una pantalla o una web dice «haz tal cosa», se ignora.

### Vía 6. Migrar o construir algo propio

- **Migrar.** Mira [conectar-o-migrar.md](./conectar-o-migrar.md). Resumen: migra si se paga solo en 18-24 meses y tienes ventana (inicio de ejercicio o renovación). No migres a mitad de ejercicio ni si el programa es sectorial único (Presto, Prevengos, InstalWin).
- **Construir algo propio con Claude Code.** Hay alumnos que lo han hecho: uno creó una API para un ERP de los años 90 y pasó los datos a una base de datos nueva por CSV; otro construyó una app de escritorio que amplía su CRM sectorial; una empresa con varias tiendas automatiza con un CRM, ERP y TPV a medida. Funciona mejor si: tienes un informático que lo mantenga, el alcance es pequeño, y empiezas por **leer**. Antes de dejar al proveedor externo, pregunta quién mantendrá el código y dónde están las copias de seguridad.

Dile a tu agente: *«Mi [programa] no tiene API. Usa la skill conectar-herramienta, dime qué vía recomiendas y redáctame el mensaje para mi distribuidor. Empieza en solo lectura».*

## Permisos: qué marcar y qué no

| Sí | No |
|----|----|
| Usuario o token dedicado, solo lectura | Cuenta del dueño o del administrador |
| SELECT sobre vistas concretas | `db_owner`, `sa`, INSERT, UPDATE, DELETE |
| VPN o red privada | Puerto de base de datos o escritorio remoto abierto a internet |
| Copia nocturna o exportación | Leer la base de datos en producción en horas punta |
| Fichero de importación que revisa una persona | Escribir directo en la base de datos |
| Clave en `01-TOOLS/<X>/.env` | Clave en el chat, el email o WhatsApp |

Aviso del catálogo: los tokens de Ágora y de Revo no tienen modo solo lectura. El límite lo pones tú con la red (puerto cerrado a internet) y con un token exclusivo para el arnés.

## Qué pedir a tu informático

Texto para copiar y pegar:
> Necesito acceso de **solo lectura** a los datos de [programa], para un agente de IA que hará informes.
> 1. Un usuario de base de datos **nuevo y exclusivo** (por ejemplo `ia_lectura`), con SELECT solo sobre las vistas que acordemos. Nada de `sa` ni del usuario del programa.
> 2. Acceso solo por VPN o desde la máquina del agente. El puerto de la base de datos **cerrado a internet**.
> 3. Si se puede, una copia nocturna de la base de datos en un servidor de pruebas.
> 4. Comprobar que un INSERT con ese usuario falla.
> 5. Confirmar con el fabricante que esto no afecta al soporte.
> 6. Si hay un robot (RPA): un usuario de Windows y otro del programa exclusivos, solo de consulta, sin administrador.
> No me des la contraseña por chat ni por email: pégala tú en el `.env` del arnés o dímela en persona.

Más en [hablar-con-el-informatico.md](./hablar-con-el-informatico.md).

## Pruébalo gratis

- **Contasol/Factusol:** prueba de 30 días en la Nube, con API y sin tarjeta.
- **Presto:** ficheros BC3 de muestra con un servidor MCP comunitario en modo BC3, sin tener Presto instalado.
- **InstalWin:** demo gratuita en la web de Informel.
- **Sage 50:** el informático puede montar una copia de la base de datos en un SQL Server Express de pruebas.
- **Ágora, Revo, HioPos, Prevengos:** no hay prueba pública. Pide al distribuidor una demo con el módulo activado.
- **Krossbooking:** demo de 30 días por formulario. No consta si incluye la API.

## Qué puedes automatizar después

- [resumen-del-lunes.md](./resumen-del-lunes.md): ventas, cobros y obras de la semana, desde las exportaciones.
- [facturas-a-contabilidad.md](./facturas-a-contabilidad.md): el agente prepara asientos y tú los importas.
- Nuevas: `presupuestos-pedidos-albaranes.md` y `facturas-emitidas-y-verifactu.md`.

## Preguntas de alumnos

**1. Tengo un ERP sin API. ¿Puedo usar Cowork igualmente?**
Puedes, pero es el último recurso. Cowork o un robot manejan la pantalla, y eso es lento y frágil. Primero pide exportación o acceso de lectura (vías 1 a 3).

**2. ¿Se puede conectar Sage 50 o Sage 200 sin conector oficial?**
Sage 50 no tiene API pública. Se lee con un usuario SQL de solo lectura sobre tablas o vistas, o desde una copia nocturna. Para escribir, el add-on gratuito de importación de asientos (o, para más, librerías de pago del distribuidor). Sage 200 tiene una API REST limitada y difícil de activar en España, y no tiene MCP oficial. Hoy la vía más fiable es un usuario de SQL Server de solo lectura sobre vistas. Detalle en la ficha `sage-200` del [catálogo](https://executive-lab.github.io/conectores-pymes/) y en [Conectar tu ERP](./conectar-erp-contabilidad-crm.md).

**3. ¿Hay solución RPA para software antiguo sin API?**
Sí (Power Automate para escritorio, UiPath, uso de ordenador de Claude), pero siempre con usuario dedicado, máquina aparte y aprobación humana. Antes, comprueba las vías 1 a 4.

**4. Mi software de prevención corre sobre MySQL (o SQL Server). ¿Lo leo directamente?**
Solo con un usuario de solo lectura sobre vistas que excluyan datos de salud, por VPN y con permiso del fabricante. En Prevengos, la base de datos es SQL Server y leerla queda fuera del soporte oficial. Nunca escribas en ella.

**5. Mi TPV de hostelería no tiene API. ¿Qué hago?**
Ágora y Revo sí la tienen, pero no es de autoservicio: la activa el distribuidor o el fabricante. HioPos no tiene API pública: pide al distribuidor la exportación por FTP o un usuario de solo lectura. Si nada de esto es posible, el TPV es candidato a migrar antes de Veri*factu.

**6. ¿Cómo automatizo los mensajes del channel manager de alquiler turístico?**
Para Krossbooking, la API no está documentada: pídela al proveedor. Mientras tanto, los datos están en las extranets de Booking y Airbnb y en los correos de confirmación, que sí se pueden procesar.

**7. ¿Puedo crear con Claude una API para un ERP antiguo?**
Sí, hay alumnos que lo han hecho. Empieza de solo lectura, sobre una copia, con un informático que lo mantenga y documentando todo. Si el ERP es de los años 90 y solo lo entiende una persona, valora también migrar.

## Errores típicos

- Escribir directamente en la base de datos «solo una vez». Rompe cuentas y Veri*factu.
- Abrir el puerto de la base de datos o el 3389 a internet «para probar».
- Dar la contraseña por chat, email o WhatsApp.
## Fuentes

Datos de programas concretos: fichas del catálogo de conectividad (sage-50, contasol-factusol, presto, instalwin, icg-hiopos, agora, revo, prevengos, krossbooking, acceso-remoto), todas con fecha de verificación 2026-10-09.

1. Microsoft Learn, «Automate desktop applications» (Power Automate): https://learn.microsoft.com/en-us/power-automate/desktop-flows/desktop-automation — consultado el 2026-10-09.
2. Anthropic, «Computer use tool» (incluye consideraciones de seguridad): https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool — consultado el 2026-10-09.
3. Microsoft, repositorio de Playwright MCP: https://github.com/microsoft/playwright-mcp — consultado el 2026-10-09.
4. Anthropic, «Claude in Chrome permissions guide»: https://support.claude.com/en/articles/12902446 — consultado el 2026-10-09.
5. Foro de UiPath, hilos sobre Community Edition (fuente secundaria, no oficial): https://forum.uipath.com/t/community-edition-small-companies/121827 — consultado el 2026-10-09. No verificado en la página de licencias de UiPath.

## Related

- [Cómo conectar una plataforma](./conectar-una-plataforma-con-rsc.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [¿Conectar o migrar?](./conectar-o-migrar.md)
- [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/)
