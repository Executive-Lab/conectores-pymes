# Plantillas para pedir acceso

Adáptalas: cambia lo que va entre `<…>`, quita lo que no aplique y no añadas peticiones que no hagan falta. Siempre: solo lectura, usuario dedicado, nada abierto a internet y la pregunta de coste.

## A. Programa instalado (Sage 50/200, Contasol local, Presto, InstalWin, TPV local…) → informático o distribuidor

> Hola `<nombre>`. Quiero automatizar `<informes de ventas y cobros / la entrada de facturas>` con una herramienta de IA. Necesito que lea datos de `<programa y versión>`. Por orden de preferencia:
>
> 1. ¿El fabricante o vosotros tenéis **API o módulo de integración** para este programa, o versión en la nube con API? ¿Qué cuesta?
> 2. Si no, ¿puede el programa **exportar automáticamente** cada noche `<facturas, clientes, stock>` a CSV o Excel en una carpeta?
> 3. Si no, ¿me podéis crear un **usuario de base de datos de solo lectura** limitado a `<estas vistas>`, accesible solo por VPN?
>
> No necesito escribir nada en el programa. No quiero abrir puertos a internet ni usar el usuario administrador. ¿Qué opción veis y cuánto costaría?

## B. Google Workspace → administrador

> Hola `<nombre>`. Necesito autorizar una aplicación con **permisos de solo lectura** `<gmail.readonly / drive.file / spreadsheets.readonly / calendar.events.readonly>`. En Controles de API, déjala en "Datos específicos de Google" y, si se puede, limítala a `<esta carpeta u hoja>` compartiéndola con una cuenta de servicio sin delegación de dominio. Pantalla de consentimiento "Interna".

## C. Microsoft 365 → administrador

> Hola `<nombre>`. Necesito registrar una app en **Entra ID** con permisos delegados de solo lectura (`User.Read`, `Mail.Read`, `Files.Read`…) o, si va sin usuario, `Sites.Selected` con rol "read" solo en el sitio `<nombre>`. Necesitaré el consentimiento de administrador y "Asignación requerida" solo para mi usuario. Nada de permisos de escritura sobre todo el tenant.

## D. Herramienta web que lleva otra persona (gestoría, agencia, socio)

> Hola `<nombre>`. ¿Me puedes crear en `<herramienta>` una **clave de API o un usuario de integración de solo lectura** a nombre de "rsc-lectura"? Es para informes automáticos. Si la herramienta no permite limitar permisos, dímelo antes y lo hablamos.

## E. Gestoría (cuando el programa es suyo)

> Hola `<nombre>`. Estamos automatizando nuestros informes internos. ¿Podéis dejarnos cada `<semana / mes>` en una carpeta compartida `<balance, mayor de clientes y proveedores, modelos presentados>` en Excel? Si vuestro programa permite dar a la empresa un acceso de solo lectura a sus propios datos, también nos sirve.

## F. WhatsApp Business → proveedor BSP o Tech Provider

> Hola. Queremos dar de alta nuestro número en la WhatsApp Business Platform en **coexistencia**, para seguir usando la app en el móvil. ¿Lo hacéis? ¿Qué cuesta al mes y por conversación? ¿Nos dais acceso por API y webhook, o solo por vuestro panel? Necesitamos un usuario del sistema con acceso solo a nuestra WABA.

## Lo que NO se acepta

- La contraseña del administrador o el usuario de otra persona.
- Abrir el puerto de la base de datos o del escritorio remoto a internet.
- Una clave que lo puede todo cuando existe una opción limitada.
- Credenciales enviadas por email o WhatsApp: se pegan directamente en `01-TOOLS/<X>/.env`.
