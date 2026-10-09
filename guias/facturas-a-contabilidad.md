---
type: article
title: "Receta: facturas y tickets a contabilidad, sin teclear"
description: Cómo montar la entrada de facturas (email, carpeta, WhatsApp o papel) con extracción por IA, validación, aprobación humana y registro en el programa contable, por API como borrador o con el fichero de importación oficial.
tags: [receta, facturas, contabilidad, ocr, n8n, aprobacion, verifactu]
timestamp: 2026-10-09T13:30:00Z
topic: recetas
status: draft
sources: []
score: 0.0
---

# Receta: facturas y tickets a contabilidad

## En resumen
Las facturas llegan por email, a una carpeta, por WhatsApp o en papel (foto). El sistema extrae proveedor, NIF, fecha, número, base, tipo y cuota de IVA, retención y total; los valida (cuadres, NIF, duplicados); propone la cuenta contable; **una persona aprueba**; y se registra **como borrador** por la API del programa o con su **fichero de importación oficial**. Nunca se escribe directamente en la base de datos de un programa contable: rompe la integridad, el soporte y la cadena de Veri\*factu.

## Arquitectura

```
[email / carpeta / WhatsApp]  → n8n (trigger) → extracción a JSON con esquema fijo (Claude, Mistral OCR o el OCR del ERP)
                              → validaciones (cuadre base+IVA=total, NIF, duplicado por proveedor+número)
                              → propuesta de cuenta y de IVA (skill con el plan de cuentas de 02-DOCS)
                              → APROBACIÓN: Slack o Telegram "¿Contabilizo?" [Sí] [No] (Send and Wait)
                              → SaaS: crear BORRADOR por API (Holded, Odoo, Sage Active…)
                                Escritorio: añadir línea al fichero de importación del día (Sage 50, Contasol, A3…)
                              → mover el PDF a "procesadas" y registrar quién aprobó
```

El proyecto de demostración "Aprobación de facturas con validación humana en Slack" (n8n + Drive + Mistral OCR + Gemini + Sheets) es exactamente esta arquitectura con Sheets como destino. Sirve de plantilla.

## Piezas

1. **Disparador continuo: n8n** (Gmail o Outlook Trigger, Drive o OneDrive Trigger, WhatsApp Trigger, Local File Trigger).
2. **Extracción**: salida a un esquema JSON fijo, nunca texto libre (ver la skill `structured-extraction` de RSC). Odoo y Holded tienen su propia digitalización de facturas (Odoo cobra por crédito): compárala antes de construir.
3. **Conocimiento**: plan de cuentas, proveedores habituales y su cuenta, y reglas de IVA, en `02-DOCS/wiki/contabilidad/`. Lo lee la skill `/contabilizar` cuando se revisa por lotes en Claude Code.
4. **Aprobación**: n8n "Send and Wait" (Slack, Telegram o email). Sin respuesta en X horas, la factura se queda pendiente: no se toma como "no".
5. **Registro**: según el programa (tabla).

## Registro según el programa

| Programa | Cómo se escribe | Permisos |
|----------|-----------------|----------|
| **Holded** | API v2: documento de compra como borrador | Token con escritura **solo** en Compras; otro token de lectura para el resto |
| **Odoo** | `account.move` en estado borrador (JSON-2, o MCP con herramienta de escritura expuesta a mano) | Usuario bot con grupo de facturación limitado; clave con caducidad de 3 meses |
| **Sage Active** | API GraphQL (scope de escritura solo si hace falta) | Usuario dedicado; app con OAuth |
| **Contasol / Factusol Nube** | API de DELSOL con acceso por empresa y área | Acceso de API limitado al área de compras |
| **Contasol local, Sage 50, A3, Sage Despachos** | **Fichero de importación oficial** generado en `01-TOOLS/<X>/out/` → una persona lo importa | El agente no toca el programa |
| **Haddock (hostelería)** | Haddock procesa las facturas y las manda a Holded; se lee desde Holded | Clave de Holded exclusiva para Haddock |

## Variante en Claude Code (por lotes)

Para un despacho que prefiere revisar en pantalla: `/contabilizar <carpeta>` → la skill extrae todas las facturas, muestra una tabla con propuesta de cuenta y dudas marcadas, el contable corrige en el chat y la skill genera el fichero de importación o los borradores. Las herramientas que escriben, en `permissions.ask`. Es la "revisión por excepción" que piden los despachos.

## Seguridad

- Las facturas son **contenido no fiable**: un PDF puede traer texto que intenta dar instrucciones al agente. La extracción va a un esquema cerrado y las validaciones son código, no criterio del modelo.
- Escribir, solo en **borrador** o en **fichero**, siempre con aprobación.
- Duplicados: clave proveedor + número + importe.
- Datos personales de los clientes del despacho: cada cliente, su carpeta. Nunca la base de datos entera de la gestoría.

## Demo en clase (0 €)

Odoo Community (facturas de proveedor en borrador por JSON-2) + n8n self-hosted + Telegram (bot gratis para la aprobación) + 5 PDFs de ejemplo. Variante de escritorio: generar un fichero de importación de asientos y enseñar cómo lo importa una persona.

## Errores típicos

- Facturas de varias páginas o tickets arrugados: probar con los peores casos reales desde el principio.
- IVA mixto o recargo de equivalencia: casos que la regla simple no cubre. Se marcan para revisión.
- Tomar "sin respuesta" como "no": la factura se pierde. Debe quedar pendiente y avisar.
- Confiar en la cuenta propuesta sin el histórico del proveedor: guarda la cuenta usada por proveedor.

## Relacionado
- [Cómo se monta](./como-se-monta.md) · [Catálogo: ERP y contabilidad](https://executive-lab.github.io/conectores-pymes/) · [¿Conectar o migrar?](./conectar-o-migrar.md)
