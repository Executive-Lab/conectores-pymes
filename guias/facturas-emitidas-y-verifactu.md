---
type: article
title: "Receta: facturas emitidas, cobros y Veri*factu"
description: Cómo preparar facturas para clientes desde Excel, CRM, programa de alquiler vacacional o peticiones por WhatsApp, vigilar cobros e impagos y encajarlo con Veri*factu y la factura electrónica B2B, sin que un sistema hecho a medida emita facturas por su cuenta.
tags: [receta, facturas-emitidas, verifactu, factura-electronica, cobros, impagos, n8n, aprobacion]
timestamp: 2026-10-09T18:00:00Z
topic: recetas
status: draft
sources: ["https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu.html", "https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/nota-informativa-ampliacion-plazo-adaptacion-facturacion.html", "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20587", "https://www.boe.es/buscar/act.php?id=BOE-A-2023-24840", "https://www.boe.es/buscar/act.php?id=BOE-A-2024-22138"]
score: 0.0
---

# Receta: facturas emitidas, cobros y Veri*factu

> Para: pymes, autónomos y gestorías que emiten facturas y quieren dejar de rehacerlas a mano. La receta de [facturas recibidas](./facturas-a-contabilidad.md) cubre lo que te llega; esta cubre lo que **emites**. Datos legales a 2026-10-09.

## En resumen
El agente **prepara** la factura (datos, líneas, importes, cliente) y un **programa de facturación que cumple el reglamento la emite**. Esa frontera es la clave de la receta:

- **Preparar** (borrador, datos, cálculo, aviso de cobro): lo puede hacer tu agente, tu Excel o un script.
- **Emitir** (numerar, firmar, encadenar, registrar, enviar a Hacienda en Veri*factu): lo hace un software de facturación que cumpla el reglamento.

Casos reales de alumnos, parafraseados: facturas desde un Excel con un botón; facturación mensual (revisar en el CRM lo facturable de cada cliente y calcular el importe); programa de gestión de alquiler vacacional que genera facturas por API; clientes de una gestoría que piden facturas por WhatsApp; cobros y recordatorios de impago; «¿se puede enganchar esto con Verifactu?».

Tiempo: una tarde para el borrador desde Excel o CRM; el recordatorio de impagos se monta en otra. Actúas tú; la gestoría o el proveedor del programa para confirmar el cumplimiento.

## Calendario a 2026-10-09

| Qué | Fecha | Estado | Fuente |
|-----|-------|--------|--------|
| **Veri*factu, fecha legal vigente** | Antes del **1-ene-2027** (contribuyentes del Impuesto sobre Sociedades) y del **1-jul-2027** (resto, autónomos incluidos) | Vigente (RD-ley 15/2025). La nota oficial de la AEAT, actualizada el 7-oct-2026, sigue diciéndolo | [1] [2] |
| **Veri*factu, aplazamiento** | Previsto para **octubre de 2028** | **Anunciado** por Hacienda el 5-oct-2026. La AEAT lo enlaza como «previsión»; a 2026-10-09 no consta norma publicada que lo recoja. Hasta que se publique, las fechas legales son las de 2027 | [1] [2] |
| **Factura electrónica B2B** | **6-oct-2027** (más de 8 M€ de volumen de operaciones) y **6-oct-2028** (resto) | Orden HAC/1028/2026 (BOE 5-oct-2026, en vigor el 6-oct-2026), que desarrolla el RD 238/2026 | [3] y catálogo |
| **Fabricantes de software** | Desde el **29-jul-2025** solo pueden comercializar sistemas adaptados con declaración responsable | En vigor; el aplazamiento no les afecta (según el catálogo) | [4] y catálogo |
| **Uso voluntario** | 2026 | Puedes usar Veri*factu ya | catálogo |

Quedan fuera del régimen general quienes están en el SII y los territorios forales con TicketBAI o Batuz.

Qué significa para una pyme: **no esperes al último día**. Si tu programa de facturación no está adaptado, el cambio se planifica ya. Si se confirma el aplazamiento, tendrás margen, pero la factura electrónica B2B llega en las mismas fechas.

## Qué exige el reglamento, sin tecnicismos

El Reglamento (RD 1007/2023) pide que el programa que emite facturas garantice cinco cosas: integridad, conservación, accesibilidad, legibilidad, trazabilidad e inalterabilidad de los registros [4]. Dicho con una analogía de oficina: un **talonario numerado y sellado que nadie puede arrancar, reescribir ni dejar sin hoja** sin que quede constancia. Cada factura lleva una «huella» (una firma digital que la une a la anterior), igual que un talonario con hojas numeradas y unidas.

En el modo **Veri*factu**, además, el programa **manda cada registro a la AEAT** casi a la vez que emite la factura (como pedir al sello oficial en cada hoja). Hay otro modo sin envío inmediato, con firma electrónica propia y registro de eventos.

El productor del programa firma una **declaración responsable** por escrito, visible dentro del sistema y por versión [5]. La AEAT **no homologa ni certifica** programas: no hay «sello de Hacienda». Pide siempre la declaración y la versión exacta.

## ¿Puede un sistema hecho a medida o con IA emitir facturas?

Respuesta corta: **solo si cumple el reglamento. En la práctica, que emita un software de facturación que ya lo cumple.**

- El reglamento se aplica a **cualquier obligado que use un sistema informático de facturación**, sin distinguir si es de un tercero o propio (art. 3.1) [4].
- El texto del BOE **no dice expresamente** si quien se desarrolla su propio programa debe emitir la declaración responsable: la declaración corresponde a la «persona o entidad productora» [4] y la orden no define «productor» [5]. La AEAT tiene preguntas frecuentes sobre software propio (actualizadas el 21-jul-2026) que **no he podido leer**: consúltalas antes de decidir [1].
- Una app hecha con Claude Code que guarde, numere y emita facturas **sería un sistema informático de facturación**. Tendría que garantizar el encadenamiento, la inalterabilidad, el registro de eventos y, en su caso, el envío. Eso es un producto con mantenimiento y auditoría, no un script de una tarde.
- Un agente que edita facturas en la base de datos de un programa existente **rompe la cadena**. Nunca.

Por eso la regla de la receta:

| Pieza | Puede hacerlo |
|-------|---------------|
| Reunir y calcular qué hay que facturar | Agente, Excel, script |
| Crear la factura como **borrador** en el programa | Agente por API (con usuario dedicado y aprobación) |
| **Emitir** (numerar, encadenar, firmar, enviar a la AEAT) | **El programa de facturación**, con persona que pulsa |
| Avisar de cobros e impagos | Agente (solo lectura + borradores de mensaje) |
| Generar su propio sistema de emisión | Solo si asumes el cumplimiento y la declaración. No lo recomiendo en una pyme |

Si hoy tienes una app propia que genera PDFs desde un Excel (ya hay alumnos con eso), **conviértela en preparadora de datos** y emite en un software adaptado. Si es solo un PDF «informal» y estás obligado, ya no te sirve.

## Las variantes

### A. Desde un Excel

```
Excel de facturación (hoja con líneas, tarifa y cliente) → script o skill valida
  → CÓDIGO: cuadre base + IVA = total, NIF, duplicados (cliente + periodo + importe)
  → persona revisa → fichero de importación o borrador por API en el programa
  → el programa EMITE
```

Excel como fuente es la vía más usada. El agente no calcula: las fórmulas son de la hoja. Ver [Excel y hojas de cálculo](./excel-y-hojas-de-calculo.md). Cuando alguien pide «la misma factura dos veces», la clave de duplicado evita que salga doble.

### B. Facturación mensual desde el CRM

```
Día 1 de cada mes → tarea programada → lee del CRM lo facturable por cliente (solo lectura)
  → calcula el importe con la tarifa (código) → informe: «a facturar, cliente por cliente»
  → persona aprueba → borradores en el programa de facturación → el programa emite
```

Un alumno ya tiene esto «casi automatizado» con Claude Code conectado al CRM. ¿Mejora con n8n? Sí si necesitas que reaccione al momento o pedir aprobación por mensaje; si es mensual y lo revisas tú en pantalla, una skill con tarea programada basta. Ver [cómo se monta](./como-se-monta.md).

Pagos a plazos: decide una regla antes de automatizar (una factura por el total o una por cuota), y escríbela en la skill.

### C. Programa de gestión de alquiler vacacional (u otro con reservas)

Lee las reservas cerradas por API (solo lectura), calcula el importe de cada estancia (código) y prepara el borrador. La factura la emite el programa de facturación, no el agente. Si el programa de reservas no tiene API, exporta un CSV. Ver [mi programa no tiene API](./mi-programa-no-tiene-api.md) y [ERP, contabilidad y CRM](./conectar-erp-contabilidad-crm.md).

### D. Facturas pedidas por WhatsApp a una gestoría

```
Cliente escribe por WhatsApp → n8n → extracción a JSON (cliente, concepto, importe, IVA)
  → validación: ¿cliente conocido? ¿NIF? ¿importe razonable?
  → APROBACIÓN del gestor «¿Preparo esta factura?» [Sí] [Corregir] [No]
  → borrador en el programa (por API) o fichero de importación → el gestor revisa y emite
```

Con un ERP sin API: fichero o cola de tareas para quien lo teclea. **No automatices el teclado del ERP** (RPA) sin hablar con el proveedor: es frágil. Un fallo aquí es una factura emitida a la persona equivocada. Siempre con aprobación. Ver [conectar WhatsApp](./conectar-whatsapp.md): solo la API oficial.

### E. Cobros y recordatorios de impago

```
Cada mañana → tarea programada → lee facturas emitidas pendientes (solo lectura)
  → clasifica: vence hoy, vencida 7 / 15 / 30 días → redacta el recordatorio con tono según antigüedad
  → deja BORRADORES en Gmail o Outlook → una persona los envía
```

- El agente **no envía** solo y **no inventa** importes: los lee del programa.
- Excluye a quien ya ha pagado o tiene una disputa abierta (campo en la hoja).
- Con la factura electrónica B2B, el receptor comunicará aceptación, rechazo y pago, y el emisor podrá comunicar cobro o impago [3]. Eso hará más fácil automatizar el seguimiento cuando llegue.

## Qué cambia con la factura electrónica B2B

- Formato **UBL** (modelo EN 16931) [3]. Un PDF ya no basta entre empresas.
- Si emites por una plataforma privada, esta debe enviar una **copia en UBL** a la solución pública de la AEAT [3].
- Cada factura se identifica por NIF del emisor + serie + número + fecha [3].
- El catálogo recoge que el receptor debe informar de aceptación o rechazo y del pago en 4 días naturales, sin contar sábados, domingos ni festivos (punto no contrastado con el texto íntegro del BOE).
- Es el motivo real para **migrar de programa**: el tuyo debe emitir y recibir UBL o Facturae. Mira la tabla del catálogo (categoría `erp-contabilidad`): Odoo, Business Central, Contasimple y Factusol (desde la 2025.0.13) tienen declaración localizada; Holded, Sage Active, Sage 50 e InstalWin dicen estar adaptados sin declaración pública; Sage 200 y otros, sin verificar. Pídelo por escrito. Ver [¿Conectar o migrar?](./conectar-o-migrar.md).

## Permisos y seguridad

- Solo lectura por defecto. Escritura únicamente como **borrador** y con aprobación.
- Clave en `.env` o en n8n, nunca en el chat, ni por email ni por WhatsApp.
- Usuario dedicado, con permiso solo en Ventas. No el administrador.
- **Nunca** escribir en la base de datos de un programa de facturación: rompe la cadena de Veri*factu.
- Datos de clientes: mira el plan de IA en [planes, privacidad y costes](./planes-privacidad-y-costes.md). Cada cliente de la gestoría, su carpeta.
- Una petición por WhatsApp es contenido no fiable: esquema cerrado, validaciones en código.

## Demo en clase (0 €)

Odoo Community local con datos de demostración, un Excel de 10 líneas a facturar, un script que valida cuadres y crea borradores, y una tarea de impagos que deja borradores en Gmail. Sin emitir nada real.

## Errores típicos

- Pensar que «certificado por Hacienda» existe: no existe. Pide la declaración responsable y la versión.
- Que el agente emita sin pasar por el programa de facturación.
- Facturas duplicadas por pedir dos veces la misma. Clave de duplicado y aprobación.
- Correo del cliente mal escrito: valida el destinatario contra el CRM antes de enviar.
- Fechas: calcula el plan con las legales (1-ene y 1-jul de 2027) y trata el aplazamiento como una posibilidad, no como un hecho.
- Recordatorios agresivos a quien ya pagó: revisa el cobro antes de cada envío.

## Preguntas de alumnos

**¿Se puede enganchar la generación automática de facturas con Verifactu?**
Sí, **a través de un programa de facturación adaptado**: el agente crea el borrador y el programa emite y envía el registro. Un agente no «conecta con Verifactu» por su cuenta.

**Tengo una app hecha con Claude que genera facturas desde Excel. ¿Vale?**
Como preparadora de datos, sí. Como emisora, tendría que cumplir el reglamento entero. Lo prudente es que emita un programa adaptado.

**Los clientes de la gestoría piden facturas por WhatsApp. ¿Se automatiza hasta el ERP?**
Hasta el **borrador**, con aprobación del gestor. Si el ERP no tiene API, fichero de importación.

**¿Cuándo es obligatorio Veri*factu?**
Por ley, el 1-ene-2027 (sociedades) y el 1-jul-2027 (resto). Hacienda anunció el 5-oct-2026 una previsión de aplazarlo a octubre de 2028, pero a 2026-10-09 no consta norma publicada.

**¿Y la factura electrónica entre empresas?**
6-oct-2027 si facturas más de 8 M€, 6-oct-2028 en el resto.

**Si el cliente me la pide dos veces, ¿se duplica?**
No si pones la clave cliente + concepto + periodo + importe y comprobar antes de crear.

**Si el cliente paga a plazos, ¿una factura o varias?**
Es una decisión de tu asesor. Fíjala en la skill: o factura total con vencimientos o factura por cuota.

**Facturo por horas mediante certificación mensual a constructoras. ¿Automatizable?**
Sí: horas aprobadas en una hoja, cálculo por código, borrador de factura y revisión. La factura B2B será UBL desde octubre de 2027 o 2028.

**¿Mejora algo con n8n si ya lo hago con Claude Code y el CRM?**
Solo si necesitas reacción inmediata o aprobación por mensaje. Para el cierre mensual, una skill y una tarea programada bastan.

## Qué puedes automatizar después

- [Facturas a contabilidad](./facturas-a-contabilidad.md): lo que recibes.
- [Presupuestos, pedidos y albaranes](./presupuestos-pedidos-albaranes.md): el pedido cerrado alimenta la factura.
- [Resumen del lunes](./resumen-del-lunes.md): cobros pendientes en un email.

## Fuentes

1. AEAT, Sistemas informáticos de facturación y Veri*factu (página actualizada el 8-oct-2026): https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu.html — consultado el 2026-10-09.
2. AEAT, Nota informativa sobre la ampliación del plazo (página actualizada el 7-oct-2026): https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/nota-informativa-ampliacion-plazo-adaptacion-facturacion.html — consultado el 2026-10-09.
3. BOE, Orden HAC/1028/2026, de 2 de octubre (BOE de 5-oct-2026): https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20587 — consultado el 2026-10-09 (leído hasta el anexo II).
4. BOE, Real Decreto 1007/2023 (Reglamento de sistemas informáticos de facturación): https://www.boe.es/buscar/act.php?id=BOE-A-2023-24840 — consultado el 2026-10-09.
5. BOE, Orden HAC/1177/2024 (declaración responsable, art. 15): https://www.boe.es/buscar/act.php?id=BOE-A-2024-22138 — consultado el 2026-10-09.
6. Catálogo del proyecto, categoría `erp-contabilidad` (verificado el 2026-10-09): calendario, aplazamiento anunciado, estado por programa. Hacienda, nota del 5-oct-2026 (PDF no legible): https://www.hacienda.gob.es/sgt/gabsehacienda/nota-informativa-verifactu.pdf.

No verificado: texto de las FAQ de la AEAT sobre software propio; texto íntegro del RD 238/2026; norma que formalice el aplazamiento; sanciones.

## Relacionado
- [Facturas a contabilidad](./facturas-a-contabilidad.md) · [Presupuestos, pedidos y albaranes](./presupuestos-pedidos-albaranes.md) · [Cómo se monta](./como-se-monta.md)
- [ERP, contabilidad y CRM](./conectar-erp-contabilidad-crm.md) · [Mi programa no tiene API](./mi-programa-no-tiene-api.md) · [Excel y hojas de cálculo](./excel-y-hojas-de-calculo.md) · [Conectar WhatsApp](./conectar-whatsapp.md) · [Conectar o migrar](./conectar-o-migrar.md) · [Planes, privacidad y costes](./planes-privacidad-y-costes.md)
- [Catálogo](https://executive-lab.github.io/conectores-pymes/)
