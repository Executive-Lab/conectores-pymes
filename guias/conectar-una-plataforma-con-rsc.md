# Cómo conectar una plataforma a tu arnés RSC

> Para: alumnos de Executive Lab, sin necesidad de saber programar.
> Qué plataforma va por qué vía: [catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/).

## En resumen

"Conectar" una herramienta significa que tu agente pueda **leer** (y, solo si tú lo apruebas, **escribir**) en ella sin que tú copies y pegues. En RSC cada herramienta conectada vive en una carpeta: `01-TOOLS/<HERRAMIENTA>/`. Dentro están la llave (`.env`), una prueba que confirma que la llave funciona (`test_connection`) y los scripts que la usan. Algunas herramientas se conectan además como **MCP** (un enchufe estándar para agentes) en `.mcp.json`.

Hay cinco vías. Siempre se intenta la primera que funcione.

## Las cinco vías, de mejor a peor

| # | Vía | Cuándo | Quién lo hace | Esfuerzo |
|---|-----|--------|---------------|----------|
| 1 | **MCP oficial** | El fabricante publica un servidor MCP | Tú, en 5 minutos | Mínimo |
| 2 | **API con clave en tu panel** | La herramienta es web (SaaS) y te deja crear una clave de API | Tú, en 15 minutos | Bajo |
| 3 | **API con app autorizada (OAuth)** | Google Workspace, Microsoft 365, Meta (WhatsApp, Instagram, Ads), Google Ads | Quien administra la cuenta de la empresa | Medio |
| 4 | **Software instalado (escritorio o servidor)** | Sage 50/200, Contasol, Presto, Instalwin, A3, TPV local… | Tu informático o tu distribuidor | Medio-alto |
| 5 | **RPA (un robot que usa la pantalla)** | No hay ninguna de las anteriores | Tú + Executive Lab, con mucho cuidado | Alto y frágil |

### 1. MCP oficial

El fabricante ya ha hecho el enchufe. Se añade a `.mcp.json` (o como conector en claude.ai) y el agente ve sus herramientas. Normalmente te pide iniciar sesión (OAuth) la primera vez.

Ojo: un MCP puede **escribir** (crear, borrar, enviar). Configura Claude Code para que te pida aprobación en cada acción que escribe (`permissions.ask` en `.claude/settings.json`) y deja libres solo las de lectura.

### 2. API con clave en tu panel

La mayoría de SaaS tienen un apartado "API", "Integraciones" o "Desarrolladores" donde generas una clave. Pasos en RSC:

1. Dile a tu agente: *"Conecta Holded a mi arnés: crea `01-TOOLS/HOLDED` a partir de la plantilla, con un `test_connection` de solo lectura."*
2. Genera la clave en el panel de la herramienta. Si deja elegir permisos, marca **solo lectura**.
3. Pégala tú en `01-TOOLS/HOLDED/.env`. **Nunca la pegues en el chat.**
4. Ejecuta `./test_connection.sh`. Tiene que decir `OK`.

Si la clave da acceso total (pasa en varias herramientas españolas), trátala como la llave de la oficina: un uso, guardada solo en `.env`, y revócala cuando ya no la necesites.

### 3. API con app autorizada (OAuth)

Google, Microsoft y Meta no dan "una clave": hay que **registrar una aplicación** y que el administrador de la cuenta le dé permisos (*scopes*) concretos. Lo hace quien administra tu Google Workspace o Microsoft 365. Pídele **los scopes de solo lectura** que necesitas y, en Microsoft, que limite el acceso a los sitios o carpetas concretos. Texto para pedirlo: [hablar con el informático](./hablar-con-el-informatico.md).

### 4. Software instalado (escritorio o servidor)

Si tu programa se instala en un ordenador o servidor de la oficina, normalmente **no tiene API pública**. Opciones, de mejor a peor:

1. **Módulo o API del fabricante o del distribuidor** (a veces de pago). Pregunta primero por esto.
2. **Exportación automática de ficheros**: el programa deja cada noche un CSV, Excel o BC3 en una carpeta, y el arnés lee esa carpeta. Simple y seguro.
3. **Usuario de base de datos de solo lectura**: el informático crea un usuario que solo puede leer las tablas o vistas que necesitas, accesible por VPN y nunca abierto a internet.

### 5. RPA (robot que usa el navegador o el escritorio)

El agente mueve el ratón y teclea como una persona. Funciona con cualquier cosa, pero se rompe cuando cambia la pantalla, es lento y, mal hecho, es peligroso. Por ejemplo: dejar que ChatGPT controle tu Chrome con tu sesión abierta de administrador. Solo como último recurso, y con:

- un **usuario dedicado** con el rol mínimo, nunca el tuyo;
- tareas cortas y repetibles, con aprobación humana antes de guardar nada;
- registro de lo que hizo.

## Elegir la vía en cuatro preguntas

1. ¿El fabricante tiene **MCP oficial**? → Vía 1.
2. ¿Entras por **navegador** y en el panel hay **"API" o "Integraciones"**? → Vía 2 (si es Google, Microsoft o Meta → Vía 3).
3. ¿El programa está **instalado** en un PC o servidor de la oficina? → Vía 4: escribe a tu informático o distribuidor.
4. ¿Nada de lo anterior? → Pregunta si se puede **exportar a Excel/CSV**. Si tampoco → Vía 5 (RPA) o cambiar de herramienta.

## Reglas de seguridad (permisos acotados)

1. **Empieza siempre en solo lectura.** El 80 % del valor (informes, resúmenes, alertas) solo necesita leer.
2. **Una credencial por uso, a nombre del arnés.** Nada de usar tu usuario personal ni la cuenta de administrador. Ponle un nombre claro (`rsc-lectura`) para reconocerla y revocarla.
3. **El mínimo acceso que funcione**: scopes de lectura, claves restringidas, rol de "solo consulta", una carpeta y no todo el Drive.
4. **Las llaves solo en `01-TOOLS/<X>/.env`.** Nunca en el chat, en un email, en WhatsApp ni en git (RSC ya las ignora en git).
5. **Escribir requiere tu aprobación.** Crear facturas, mandar mensajes o mover dinero siempre pasa por un "¿lo hago?" (botón en Slack o WhatsApp, o confirmación en Claude Code).
6. **Datos de clientes con cuidado (RGPD).** Lo que extraigas va a `out/`, que no se sube a git. Si mandas datos personales a un proveedor de IA, revisa que tengas contrato de encargo de tratamiento.
7. **Revoca y rota.** Si una llave se filtra o alguien se va, se revoca en el panel y se genera otra. Anótalo en `CREDENTIALS.md`.

## Relacionado

- [Hablar con el informático](./hablar-con-el-informatico.md): textos listos para pedir acceso.
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/): vía, dificultad y permisos de cada plataforma.
