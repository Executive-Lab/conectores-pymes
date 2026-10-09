# Conectores para pymes

Catálogo vivo para conectar las herramientas de una pyme a un arnés de IA. Para cada herramienta (ERP, contabilidad, TPV, CRM, email, ofimática, mensajería, publicidad, ecommerce…) dice qué vía usar (MCP, API, puente o RPA), con qué permisos, qué pedir al informático, cómo probarla gratis, cuánto cuesta y si compensa conectarla o migrar.

Está pensado para dueños de pymes y para los alumnos de Executive Lab. Lo mantiene Executive Lab y se revisa solo cada semana.

**Web:** https://executive-lab.github.io/conectores-pymes/

> Información orientativa. Los planes, precios y MCP cambian cada mes: verifica en la fuente antes de decidir.

## Cómo se usa la web

- **Buscador y filtros.** Busca por nombre o por alias (por ejemplo «ContaPlus» encuentra Sage 50 y «Outlook» encuentra Microsoft 365). Filtra por categoría, dificultad, veredicto o «solo con demo gratis».
- **Mis herramientas.** Elige las herramientas que usa tu empresa. Verás cuántas son fáciles, medias o difíciles, cuáles piden informático o distribuidor y cuáles conviene valorar migrar. La selección va en la dirección de la página (`?h=holded,whatsapp-business`), así que puedes copiar el enlace y compartirlo.
- **Fichas.** Cada ficha muestra la dificultad, la vía principal, el estado del MCP, la demo, el coste y el veredicto. Al desplegarla verás la API, el MCP, otras vías, el RPA, los permisos acotados, qué pedir al informático, la demo, el coste, la migración, Verifactu (si aplica), las fuentes numeradas, la confianza y la fecha de verificación.
- **Guías.** [Cómo conectar una plataforma](guias/conectar-una-plataforma-con-rsc.md), [cómo hablar con tu informático](guias/hablar-con-el-informatico.md) y [¿conectar o migrar?](guias/conectar-o-migrar.md).
- **API pública.** Todo el catálogo está en [`catalogo.json`](https://executive-lab.github.io/conectores-pymes/catalogo.json) y el formato de cada ficha en [`esquema.json`](https://executive-lab.github.io/conectores-pymes/esquema.json). Cada plataforma trae un bloque `derivados` con la vía principal, el veredicto corto (`conectar`, `puente` o `migrar`), si hay demo gratis, si pide informático y la URL de su ficha.

## Qué hay en el repositorio

```
datos/
  esquema.json              JSON Schema (draft 2020-12) de una plataforma
  plataformas/<id>.json     una ficha por herramienta: la única fuente de verdad
  categorias/<id>.json      hallazgos, normativa y asistentes de IA de cada categoría
  cambios/<fecha>.md        registro de lo que cambia en cada verificación
guias/                      las guías en markdown
scripts/
  validar.py                comprueba los datos (sale con error si algo falla)
  construir.py              genera la web en sitio/
  seleccionar.py            elige qué fichas revisar en la verificación semanal
.github/workflows/
  publicar.yml              valida, construye y publica la web en GitHub Pages
  verificar.yml             verificación semanal con Claude, que abre un pull request
```

Los scripts solo usan Python 3 y su librería estándar: no hay que instalar nada.

```bash
python3 scripts/validar.py      # comprueba los datos
python3 scripts/construir.py    # genera sitio/ (index.html, catalogo.json, esquema.json y guias/)
```

Para ver la web en local: `python3 -m http.server -d sitio 8000` y abre http://localhost:8000.

## La skill `conectar-herramienta`

En [`skill/conectar-herramienta/`](skill/conectar-herramienta/SKILL.md) está el **método** convertido en una skill de Claude Code (formato compatible con [RSC](https://github.com/ericrisco/rsc-harness)): vías (MCP, API, app OAuth, puente, RPA), permisos acotados, qué pedir y a quién, cómo probarlo gratis y si conviene conectar, migrar o construir. Usa este catálogo (`catalogo.json`) como fuente de datos.

Para usarla en tu proyecto: copia la carpeta a `.claude/skills/conectar-herramienta/` y dile a tu agente *«conecta mi <herramienta>»*.

## Cómo contribuir

1. Edita el JSON de la plataforma en `datos/plataformas/<id>.json` (o crea uno nuevo copiando otro de la misma categoría). El `id` va en minúsculas con guiones y coincide con el nombre del fichero.
2. Cada dato nuevo necesita una **fuente primaria** en `fuentes`. Pon `verificado_el` con la fecha de hoy (AAAA-MM-DD). Lo que no puedas confirmar, márcalo como «no verificado».
3. Ejecuta `python3 scripts/validar.py` y corrige lo que diga.
4. Abre un pull request explicando qué cambia y por qué.

Las reglas completas están en [CONTRIBUTING.md](CONTRIBUTING.md). Si solo quieres avisar de un error o pedir una herramienta, abre un issue.

## Verificación semanal

Cada lunes a las 06:17 UTC el workflow **Verificación semanal** (`verificar.yml`):

1. Elige con `scripts/seleccionar.py` las 10 fichas con el `verificado_el` más antiguo.
2. Lanza Claude con [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action). Claude solo puede buscar en la web, leer páginas y ficheros, y editar `datos/plataformas/` y `datos/cambios/`. No puede ejecutar comandos.
3. Claude re-verifica con fuentes primarias el MCP, la API, los permisos, los precios, la demo y Verifactu. Cambia solo lo que haya cambiado, pone la fecha de hoy en `verificado_el`, añade las fuentes nuevas, marca «no verificado» lo que no puede confirmar y deja un resumen en `datos/cambios/<fecha>.md`.
4. Se ejecuta `validar.py`, los cambios se suben a una rama `verificacion/<fecha>-<n>` y se abre un **issue** con el resumen y el enlace para **crear el PR con un clic**. Nunca se escribe directamente en `main`. Si la validación falla, el issue lo avisa y el job termina en error.
5. Una persona crea el PR desde el enlace, lo revisa y lo fusiona; entonces el workflow **Publicar web** actualiza la web.

También se puede lanzar a mano desde la pestaña **Actions** → **Verificación semanal** → **Run workflow**, con un campo opcional `ids` (por ejemplo `holded,sage-50`) para verificar solo esas fichas.

## Puesta en marcha (una sola vez)

1. **Secreto de Claude.** En *Settings → Secrets and variables → Actions* crea **uno** de estos dos secretos (vale también como secreto de la organización):
   - `ANTHROPIC_API_KEY`: una clave de la API de Anthropic (se paga por uso).
   - `CLAUDE_CODE_OAUTH_TOKEN`: el token de una suscripción de Claude (Pro, Max, Team o Enterprise). Se genera en tu ordenador con `claude setup-token`.

   Si falta, la verificación semanal se para al principio con un mensaje que explica qué configurar. La web se sigue publicando igual.
2. **GitHub Pages.** En *Settings → Pages*, elige *Source: GitHub Actions*. Después lanza una vez **Publicar web** desde Actions (o haz un push a `main`).
3. **Recomendado:** protege la rama `main` (pull request obligatorio) para que nada llegue a la web sin revisión.

No hace falta permitir que GitHub Actions cree pull requests (la organización lo tiene bloqueado): el workflow solo sube una rama y abre un issue; el PR lo crea una persona.

## Licencia

- **Código** (`scripts/`, `.github/`): [MIT](LICENSE).
- **Datos y guías** (`datos/`, `guias/`): [CC BY 4.0](LICENSE-datos.md). Puedes reutilizarlos, también con fines comerciales, citando «Conectores para pymes, de Executive Lab» y enlazando a https://executive-lab.github.io/conectores-pymes/.
