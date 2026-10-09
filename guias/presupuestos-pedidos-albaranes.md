---
type: article
title: "Receta: presupuestos, pedidos y albaranes sin copiar a mano"
description: Cómo montar en el arnés la entrada de pedidos (WhatsApp, correo), los presupuestos asistidos y el cruce pedido-albarán-factura, con el agente preparando y una persona aprobando, y los cálculos hechos por código u hoja.
tags: [receta, pedidos, presupuestos, albaranes, n8n, aprobacion, excel, construccion, industria]
timestamp: 2026-10-09T18:00:00Z
topic: recetas
status: draft
sources: []
score: 0.0
---

# Receta: presupuestos, pedidos y albaranes sin copiar a mano

> Para: pymes que reciben pedidos por WhatsApp o correo, preparan presupuestos de obra o de servicio, o casan albaranes con facturas. Es el hueco más grande de las peticiones: 104 alumnos lo piden y el sector más numeroso es industria, construcción e instalaciones.

## Overview

Lo que dicen los alumnos, parafraseado:

- «Los pedidos llegan por WhatsApp o por correo, alguien los copia a mano en un Excel y luego en el programa de gestión» (varios distribuidores).
- «Cada cliente pide de una manera, y cuando falta la persona que los pasa es una locura.»
- Presupuestos de obra a partir de ejemplos anteriores y tarifas (Excel con fórmulas y Holded; Rentman en eventos).
- Cruzar pedidos, ofertas, albaranes y facturas; casar los albaranes de un TPV o ERP con las facturas mensuales.
- Escandallos y stock en hostelería. Órdenes de trabajo y partes para operarios. «Aún imprimimos albaranes.»

Hay tres variantes. Todas comparten una **regla de oro**:

1. **El agente prepara y una persona aprueba.** Nada se envía al cliente ni se graba definitivo sin un «sí» humano.
2. **Los cálculos los hace el código o la hoja, no el modelo de cabeza.** Un modelo de lenguaje es un buen lector y un mal calculador: puede leer «20 m de cable de 2,5» y entenderlo, pero el importe lo calcula una fórmula de Excel o un script con tu tarifa. El formador de clase lo dijo claro: no te fíes del cálculo del modelo.

Tiempo de montaje: una tarde para la variante A con Excel, una o dos semanas de pruebas con pedidos reales hasta que los clientes «raros» salgan bien. Actúas tú; el informático solo si el programa de gestión no tiene API (ver [mi programa no tiene API](./mi-programa-no-tiene-api.md)).

## Las tres variantes

| Variante | Qué resuelve | Mecanismo | Fuentes típicas | Riesgo |
|----------|--------------|-----------|-----------------|--------|
| **A. Pedido entrante a borrador** | Que el pedido de WhatsApp o correo entre solo como borrador | n8n siempre activo + extracción a JSON + aprobación | WhatsApp Business (Cloud API), Gmail u Outlook, Excel de clientes y precios | Medio: se escribe un borrador |
| **B. Presupuesto asistido** | Presupuestos de obra, instalación o evento a partir de ejemplos y tarifas | Skill en Claude Code, lanzada a mano; el importe sale de una hoja con fórmulas | Excel de tarifas, presupuestos anteriores, Presto (ficheros BC3), Holded o Rentman | Bajo: el resultado es un borrador para revisar |
| **C. Cruce pedido-albarán-factura** | Detectar diferencias entre lo pedido, lo recibido y lo facturado | Skill + script de cruce, tarea programada mensual | Exportaciones del ERP o TPV, PDF de albaranes y facturas, Excel | Bajo: solo lee y genera un informe |

Elige por dolor: si pierdes horas copiando, A; si tardas días en presupuestar, B; si a fin de mes no cuadra nada, C. Empieza por **C** si quieres la opción más segura: no escribe en ninguna parte.

## La skill y el mecanismo (válido para las tres)

Escribe primero la skill y pruébala a mano; después elige el disparador. Así lo explica [Cómo se monta](./como-se-monta.md).

La skill (`.claude/skills/<nombre>/SKILL.md`) lleva:

- **Esquema fijo de salida** (JSON): cliente, referencia, líneas (artículo, cantidad, unidad), fecha de entrega, notas, y un campo `dudas`.
- **Catálogo y reglas** en `02-DOCS/wiki/operaciones/`: tarifas, equivalencias («tubo corrugado 20» es el artículo X), condiciones por cliente.
- **Qué NO hace**: no inventa precios, no inventa artículos, no calcula importes. Si el artículo no existe, lo marca en `dudas`.
- `disable-model-invocation: true` si la lanzas tú a mano.

| Si el disparo es… | Usa |
|-------------------|-----|
| Un pedido que llega en cualquier momento | **n8n** (Gmail, Outlook o WhatsApp Trigger). Claude Code no «escucha» |
| Un presupuesto que preparas tú | **Skill a mano** |
| Un cruce mensual con datos en la nube | **Routine** (`/schedule`) |
| Un cruce mensual con datos en un PC de la oficina | **`claude -p` + cron** en ese PC |

## Variante A: pedido entrante a borrador

```
[WhatsApp / correo / formulario] → n8n (trigger)
  → extracción a JSON con esquema fijo (texto, nota de voz transcrita o foto)
  → CÓDIGO: casar cliente y artículos contra el catálogo (Excel o ERP), calcular importes con la tarifa
  → validaciones: artículo existe, unidad coherente, cantidad razonable, pedido duplicado
  → APROBACIÓN: Slack, Telegram o email «¿Creo el pedido?» [Sí] [Corregir] [No] (Send and Wait)
  → crear BORRADOR en el ERP (por API) o una fila en el Excel de pedidos
  → responder al cliente «recibido» solo tras la aprobación
```

Pasos:

1. **Una sola puerta de entrada.** Un número de WhatsApp Business con la Cloud API oficial, o un buzón `pedidos@`. Nunca librerías no oficiales de WhatsApp (riesgo de que Meta bloquee el número). Ver [conectar WhatsApp](./conectar-whatsapp.md).
2. **Un catálogo limpio.** Hoja con código, descripción, unidad, precio y sinónimos habituales. Sin esto, la extracción falla en silencio.
3. **Extracción a esquema cerrado.** El modelo devuelve JSON; no redacta texto libre.
4. **Casado y cálculo por código.** Un nodo de n8n o un script busca el artículo por código o sinónimo y multiplica cantidad por precio. Si no casa, va a `dudas`.
5. **Aprobación.** La persona que hoy copia los pedidos pasa a **revisar excepciones**: ve el pedido original junto al borrador y pulsa un botón. Sin respuesta en X horas, el pedido queda pendiente y avisa; nunca se descarta.
6. **Escritura como borrador.** En un ERP SaaS (Holded, Odoo, Business Central) por API con un usuario dedicado. En un programa de escritorio sin API, un **fichero de importación** en `01-TOOLS/<X>/out/` o la fila en el Excel que ya usas. Nunca directamente en la base de datos.

Para el problema «cada cliente pide de una manera»: guarda en la wiki una ficha por cliente (cómo pide, abreviaturas, formato habitual). Así el conocimiento deja de vivir en la cabeza de una persona y la ausencia de esa persona deja de ser «una locura».

Ya hay alumnos que montaron pedidos B2B por webhook a n8n con validación en una app y exportación al operador logístico: es esta variante.

## Variante B: presupuesto asistido

```
Briefing o petición del cliente → /presupuesto → la skill lee ejemplos anteriores y la tarifa
  → propone partidas y cantidades (con las dudas marcadas)
  → las cantidades entran en la HOJA con fórmulas (o en un script) → la hoja calcula los importes
  → la skill redacta el texto de la oferta con los números de la hoja
  → una persona revisa → se pasa a Holded, Rentman o PDF
```

- **Excel con fórmulas.** Es el patrón que ya usan varios alumnos: briefing, una hoja con fórmulas condicionales y el importe sale solo. Deja esa hoja como **única fuente de cálculo**. El agente rellena entradas y lee resultados; no recalcula. Ver [Excel y hojas de cálculo](./excel-y-hojas-de-calculo.md).
- **Presto y mediciones (obra).** Presto exporta e importa ficheros **BC3**, el formato estándar de bases de precios y presupuestos de construcción. El agente puede leer un BC3 exportado como entrada y proponer capítulos y partidas. Un MCP comunitario de Presto existe, pero su autor reconoce que no está probado contra un sistema real: solo lectura y con cuidado.
- **Plano a presupuesto.** Medir un plano con IA sirve como **primera estimación**. Las mediciones las revisa quien firma la oferta.
- **Holded.** Con la API se crea el presupuesto como borrador; la persona lo revisa y lo envía desde Holded. Ver [ERP, contabilidad y CRM](./conectar-erp-contabilidad-crm.md).
- **Rentman (eventos).** No verificado en fuente oficial: pregúntale al proveedor si tiene API y qué permisos da; mientras tanto, trabaja con exportaciones.
- **Escandallos (hostelería).** Receta, ingredientes y precio de compra en una hoja; el margen lo calcula la hoja. El agente avisa de subidas de precio leyendo las facturas, pero no calcula el coste.
- **Filtrar curiosos.** Antes de presupuestar, un formulario con 4-5 preguntas (zona, plazo, rango de presupuesto) y la skill puntúa; tú decides.

## Variante C: cruce pedido-albarán-factura

```
Exportación pedidos + albaranes + facturas del mes (ERP, TPV, correo)
  → script de cruce (código): casa por proveedor, referencia, importe y fecha
  → informe: lo que cuadra, lo que falta, lo que difiere (precio, cantidad), duplicados
  → la skill redacta el resumen y propone acciones («reclamar al proveedor X por 3 líneas»)
  → una persona decide
```

- La clave es **código determinista**: casar por proveedor + número + importe, con tolerancia de céntimos. El modelo explica las diferencias; no decide si cuadran.
- Fuentes de albaranes en papel: foto o escáner con extracción a esquema, como en [facturas a contabilidad](./facturas-a-contabilidad.md). Mismas validaciones.
- Para casar albaranes de un TPV o ERP con las facturas mensuales y pasarlas a contabilidad: cruce aquí; el registro contable, en la receta de facturas recibidas.
- Es de **solo lectura**: la mejor primera automatización del bloque.

## Permisos y seguridad

- Empieza en **solo lectura**. Escribe solo borradores y con aprobación humana.
- La clave del ERP va en `01-TOOLS/<X>/.env` o en las credenciales de n8n, **nunca** en el chat, por email ni por WhatsApp.
- Usuario o aplicación **dedicada** con permiso mínimo (solo Ventas, por ejemplo). No la cuenta del dueño.
- Un pedido o PDF es **contenido no fiable**: puede traer texto que intente dar órdenes al agente. Esquema cerrado y validaciones en código.
- Datos de clientes y trabajadores: mira antes el plan de IA en [planes, privacidad y costes](./planes-privacidad-y-costes.md).
- No escribas en la base de datos del programa. Si no hay API, [puente por exportación](./mi-programa-no-tiene-api.md).

## Demo en clase (0 €)

Odoo Community en Docker + Google Sheets como catálogo + n8n self-hosted + Telegram para la aprobación + 5 pedidos de ejemplo en formatos distintos (uno con una nota de voz). Variante C: dos CSV con diferencias plantadas y un script de cruce.

## Errores típicos

- Dejar que el modelo multiplique y sume. Un error de un cero en una oferta de obra sale caro.
- Catálogo sin sinónimos: «mag. 16A», «magnetotérmico 16» y «PIA 16» son tres artículos para el sistema.
- Tomar «sin respuesta» como «no» o como «sí».
- Pedidos duplicados cuando el cliente escribe por WhatsApp y luego por correo: clave cliente + referencia + fecha.
- Querer automatizar el cliente más raro el primer día. Empieza por los tres que más pedidos mandan.
- Responder al cliente con precios antes de que nadie revise.
- Montar todo a la vez. Una variante, un mes, y después la siguiente.

## Preguntas de alumnos

**¿Puede un GPT hacerme los presupuestos de obra a partir de mis ejemplos?**
Puede proponer partidas y redactar. El importe lo debe calcular tu hoja o un script con tu tarifa. Mejor un proyecto o una skill con tus ejemplos que un GPT suelto.

**Tengo muchísimas variables para calcular presupuestos. ¿Agiliza el modelo los cálculos?**
Agiliza lo que no es calcular: leer la petición, elegir partidas, dejar la hoja rellena. Las fórmulas, en Excel.

**Los pedidos me llegan por WhatsApp y por correo y los copio a mano.**
Variante A. Entrada única, extracción a JSON, casado por código y borrador aprobado por ti.

**Cada cliente pide de una manera. ¿Cómo lo evito?**
Una ficha por cliente en la wiki y sinónimos en el catálogo. El agente aprende de eso, no de memoria.

**Mi programa de gestión no tiene API. ¿Puedo seguir?**
Sí: fichero de importación o Excel intermedio, con una persona que importa. Ver la guía enlazada arriba.

**¿Puedo cruzar pedidos, ofertas, albaranes y facturas?**
Variante C, con un script de cruce y un informe. Solo lectura.

**Aún imprimimos albaranes. ¿Por dónde empiezo?**
Escanea o fotografía los albaranes a una carpeta, extrae a esquema y cruza con los pedidos. Reduce el papel antes de cambiar de programa.

**¿Los escandallos de un restaurante en un proyecto con skills o en un GPT?**
Datos y márgenes en una hoja con fórmulas; la skill lee y avisa. Sirve cualquiera de los dos, pero el cálculo no va dentro del chat.

**¿Qué hago si el modelo se equivoca con un artículo?**
Por eso hay aprobación y campo `dudas`. Cada corrección se apunta en el catálogo para que no se repita.

## Qué puedes automatizar después

- [Facturas a contabilidad](./facturas-a-contabilidad.md) (recibidas) y [facturas emitidas y Veri*factu](./facturas-emitidas-y-verifactu.md): el albarán o el pedido cerrado alimenta la factura.
- [Resumen del lunes](./resumen-del-lunes.md): pedidos abiertos y stock bajo.
- [WhatsApp a pedidos](./whatsapp-a-pedidos.md) y [Leads y atención](./leads-y-atencion.md).

## Fuentes

1. Catálogo del proyecto, categoría `erp-contabilidad` (verificado el 2026-10-09): escritura por base de datos prohibida; MCP de Presto no probado; ficheros BC3 para demos.
2. [Cómo se monta una automatización](./como-se-monta.md) y [facturas a contabilidad](./facturas-a-contabilidad.md): mecanismos, aprobación y registro por borrador o fichero.
3. Peticiones y casos de alumnos del fichero `operaciones.txt` (clases, foro, perfiles e informes de proceso, parafraseados).
4. Rentman: no consultado en fuente oficial en esta redacción.

## Related

- [Cómo se monta](./como-se-monta.md) · [Facturas a contabilidad](./facturas-a-contabilidad.md) · [Facturas emitidas y Veri*factu](./facturas-emitidas-y-verifactu.md)
- [ERP, contabilidad y CRM](./conectar-erp-contabilidad-crm.md) · [Mi programa no tiene API](./mi-programa-no-tiene-api.md) · [Excel y hojas de cálculo](./excel-y-hojas-de-calculo.md) · [Conectar Microsoft 365](./conectar-microsoft-365.md) · [Conectar WhatsApp](./conectar-whatsapp.md) · [MCP, API y demás](./mcp-api-y-demas-sin-tecnicismos.md) · [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo](https://executive-lab.github.io/conectores-pymes/)
