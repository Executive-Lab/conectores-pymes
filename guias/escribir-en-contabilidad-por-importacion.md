---
type: article
title: "Escribir en contabilidad sin tocar la base de datos: ficheros de importación oficiales"
description: La vía segura de escritura en contabilidad — el agente prepara el fichero de importación oficial de cada programa (A3 SUENLACE.DAT, Sage 50, Sage 200, ContaSOL, ContaPlus, Holded, Odoo, a3innuva Importia) y una persona lo revisa e importa. Formatos, riesgos y qué cambia con la factura electrónica B2B.
tags: [contabilidad, importacion, a3, sage, contasol, holded, odoo, verifactu, factura-electronica]
timestamp: 2026-10-09T16:45:00Z
topic: guias
status: draft
sources: ["https://taasupportportal.wolterskluwer.com/es/es-es/articulo/enlace-contable-3554295", "https://sage50c.sage.es/help50c/Content/ADDONS/importacion-exportacion-asientos/importacion-asientos.htm", "https://sage200c.sage.es/help/content/Maestros/importacion-excel.htm", "https://ayudacontasol.sdelsol.com/docs/c2105-c%C3%B3mo-puedo-importar-desde-mi-programa-de-gesti%C3%B3n-apuntes-contables", "https://help.holded.com/en/articles/6895995-import-and-export-your-accounting-entries", "https://www.odoo.com/documentation/18.0/applications/essentials/export_import_data.html", "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7295"]
score: 0.0
---

# Escribir en contabilidad sin tocar la base de datos

> Para: alumnos con asesoría o contabilidad propia, sus gestorías y formadores. Es la "vía 4" de [Mi programa no tiene API](./mi-programa-no-tiene-api.md) y el último paso de la receta [Facturas a contabilidad](./facturas-a-contabilidad.md).
> Verificado el 2026-10-09. Las posiciones exactas de los formatos de ancho fijo cambian según la versión: genera siempre un fichero de muestra desde el propio programa y compáralo.

## Overview

El agente **no escribe** en el programa contable. Lee las facturas o los tickets, propone los asientos, y **genera el fichero de importación oficial** del programa en `01-TOOLS/<PROGRAMA>/out/`. Una persona lo revisa, pasa la validación del programa e importa con su botón. Así:

- no se rompe la integridad del programa ni su soporte;
- no se toca la cadena de registros de Veri\*factu;
- siempre hay una persona que dice "sí" antes de que algo entre en los libros.

## Formatos por programa

| Programa | Formato | Qué importa | ¿De pago? | Riesgos principales |
|----------|---------|-------------|-----------|---------------------|
| **A3 (a3asesor eco/con)** | **SUENLACE.DAT**: ASCII de ancho fijo, registros de 512 bytes. Tipo en la posición 15: 0 apunte sin IVA, 1 factura con IVA, 2 rectificativa, 9 detalle de IVA, C alta de cuentas, V/B vencimientos, A/D analítica | Asientos, facturas emitidas y recibidas con IVA y SII, rectificativas, cuentas, vencimientos y analítica | No (función estándar). Los importadores de Excel a enlace son aparte | Si una cuenta no existe, **la crea sola**: un error de tecleo genera subcuentas nuevas. Pasar siempre el **Chequeo**. Ejemplos oficiales en la instalación: `SUENLAC5.TXT` y `SUENLAC5.EJE` |
| **a3innuva Contabilidad** | **Importia** (Excel con asistente de columnas y plantillas .zip) o **API** con asientos y facturas en estado **Draft** | Facturas expedidas y recibidas, asientos, plan contable, enlace de nómina | Sí: Importia y Conectia (API) son suscripciones aparte | Reimportar sin "deshacer" duplica. Un código de operación de IVA erróneo clasifica mal |
| **Sage 50 (España)** | Add-on de **Importación/Exportación de asientos**: tres ficheros (subcuentas, diario y observaciones) en .txt de ancho fijo, .csv o .dbf, estructura compatible ContaPlus | Asientos (con IVA en el diario), subcuentas y observaciones. **No** importa facturas como documentos de venta | No: add-on gratuito con la licencia (se activa en Add-ons) | Importar en orden: cuentas → asientos → observaciones. Si las cuentas son más cortas, rellena con ceros y puede ir a una subcuenta equivocada. No hay plantilla vacía: exporta un asiento de muestra y copia su estructura |
| **Sage 200 (España)** | **Gestor de importaciones** con guías Excel (asientos, "Plugin Facturas") | Clientes y artículos (oficial). Asientos y facturas como asientos, con guías o plugins | Probablemente sí (guías del partner) | Tipo de factura vacío tras importar → libros de IVA incompletos. Con su módulo Veri\*factu no se importan facturas certificadas por otro software |
| **ContaSOL** (y FactuSOL → ContaSOL) | Libros Excel con nombre fijo: **APU** (diario), **FRE + LFR** (recibidas), **FAC + LFA** (emitidas), **PLA + LPL** (plantillas). También ASCII de ContaPlus y el Conector ASCII | Asientos, facturas (libros de IVA), maestros, apertura | No (Utilidades > Importaciones) | Dígitos de cuenta distintos dan error. Campos demasiado largos se descartan **sin avisar** y un texto en un campo numérico se guarda como 0. El Conector escribe directo en la carpeta DATOS: copia de seguridad antes |
| **ContaPlus** (heredado) | XDiario, XSubCta y XDatAsi (.txt de ancho fijo o .dbf) | Asientos, subcuentas y comentarios | No | Sin soporte oficial desde hace años y con tablas no oficiales. Sigue siendo un formato de intercambio que aceptan Sage 50 y ContaSOL, pero el IVA puede no llegar bien a los libros y al 303 |
| **Holded** | Plantillas Excel/CSV: Diario, Cuentas, Ventas, Compras, Contactos | Asientos, plan de cuentas, facturas de venta y compra, contactos | No | Ampliar los dígitos de cuenta **antes** de crear datos. Los contactos deben existir (vinculación por NIF). No se documenta cómo deshacer |
| **Odoo** | Importador genérico (CSV/XLSX) sobre `account.move` y sus líneas | Asientos, facturas, contactos, extractos | No | **Las importaciones son permanentes**: usar "Test" y lotes pequeños, con External ID para no duplicar. Los asientos quedan en **borrador** (bien para revisar). Con Veri\*factu activo, publicar una factura de cliente la envía a la AEAT |

## Reglas para el agente

1. **Fichero de muestra primero**: antes de generar nada, pide al usuario un fichero exportado desde su programa (o los ejemplos oficiales, p. ej. `SUENLAC5.EJE`) y replica su estructura exacta.
2. **Cuentas existentes**: el fichero solo usa cuentas del plan contable actual. Si falta una, se marca para revisión y **no** se inventa.
3. **Cuadres**: base + cuota = total en cada factura, debe = haber en cada asiento. Si no cuadra, no sale.
4. **Duplicados**: registro de lotes (proveedor + número + importe + lote) en `01-TOOLS/<PROGRAMA>/out/lotes.csv`.
5. **La persona importa**: pasa la validación del programa (Chequeo en A3, "Test" en Odoo) y guarda una copia de seguridad antes.
6. **Nunca emitir**: el agente no crea facturas **emitidas** en un programa de facturación (en a3factura, un POST de factura **la emite** y genera el registro Veri\*factu). Prepara datos o borradores; emite una persona desde el programa adaptado.

## Qué cambia con la factura electrónica B2B

El **RD 238/2026** y la **Orden HAC/1028/2026** (BOE del 5-10-2026) hacen obligatoria la factura electrónica entre empresas: **6-10-2027** para quien factura más de 8 M€ y **6-10-2028** para el resto. Formato estructurado EN 16931 (UBL, CII, EDIFACT o Facturae); la solución pública de la AEAT usa UBL. Convive con Veri\*factu (1-1-2027 sociedades y 1-7-2027 resto, con posible aplazamiento anunciado).

Efectos en esta vía:

1. **Los ficheros de importación contable no son facturas** y no cambian. Siguen siendo la forma correcta de que una persona valide el asiento.
2. **Las facturas recibidas llegarán en XML estructurado.** El agente podrá leer NIF, bases y cuotas **sin OCR** y pasarlos al fichero de importación, guardando el XML como justificante. La receta de facturas mejora mucho.
3. **Facturas emitidas**: el agente no genera ni firma UBL o Facturae por su cuenta, ni llama a endpoints de emisión. Deja datos o borradores para que se emitan desde el programa adaptado o la plataforma.
4. **Una factura ya emitida en otro sistema solo entra en contabilidad.** No se reemite importándola en el módulo de facturación de otro programa: se duplicarían registros.
5. **Comunicar estados** (aceptación, rechazo, pago en 4 días hábiles) será una escritura nueva y obligatoria. Buena candidata a automatizar, con aprobación humana.

## Related

- [Facturas a contabilidad](./facturas-a-contabilidad.md) · [Facturas emitidas y Veri\*factu](./facturas-emitidas-y-verifactu.md) · [Mi programa no tiene API](./mi-programa-no-tiene-api.md) · [Kit puente técnico](./kit-puente-tecnico.md) · fichas `a3asesor`, `a3innuva-contabilidad`, `sage-50`, `sage-200`, `contasol-factusol`, `holded` y `odoo` del [catálogo](https://executive-lab.github.io/conectores-pymes/)
