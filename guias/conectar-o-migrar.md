---
type: article
title: ¿Conectar o migrar? Cuándo compensa cambiar de herramienta
description: Guía para alumnos — señales de que una herramienta frena el arnés, cuándo NO conviene cambiar, cómo hacer la cuenta y cómo migrar sin perder datos ni el ejercicio contable.
tags: [guia-alumnos, migracion, erp, decision]
timestamp: 2026-10-09T11:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# ¿Conectar o migrar? Cuándo compensa cambiar de herramienta

> Para: alumnos de Executive Lab que tienen un programa "cerrado" (ERP o contabilidad antiguos, TPV, software instalado) y dudan entre conectarlo como sea o cambiarlo.
> El veredicto de cada plataforma está en el [catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/).

## En resumen
El arnés solo es tan bueno como los datos a los que llega. Si tu programa principal no deja sacar datos (sin API, sin exportación, sin base de datos accesible), cada automatización pasa por copiar y pegar o por un robot frágil: es un palo en las ruedas. A veces la respuesta es **conectarlo con un puente** (exportación nocturna, usuario de base de datos de solo lectura, módulo del distribuidor). Otras veces es **migrar** a algo que se conecta de serie. Esta guía ayuda a decidir.

## Señales de que tu herramienta frena (cuantas más, más sentido tiene migrar)

1. **No hay forma de sacar datos** sin una persona: ni API, ni exportación automática, ni base de datos accesible. Solo queda RPA.
2. **Versión sin soporte**: el fabricante ya no la actualiza, o solo funciona en un PC concreto de la oficina.
3. **El puente cuesta más que el cambio**: pagas a un integrador, un módulo o horas de consultoría cada año por algo que otra herramienta trae de serie.
4. **Copias y pegas a diario** entre ese programa y otros. Si son más de 3-4 horas por semana, en un año suma más de 150 horas.
5. **Normativa que viene y no está cubierta**: facturación con Veri\*factu, factura electrónica entre empresas. Si el fabricante no lo adapta, o lo cobra aparte, tendrás que moverte igual.
6. **Solo una persona sabe usarlo**, o los datos acaban fuera, en Excel paralelos.
7. **No crece contigo**: más usuarios, otra sede, acceso desde el móvil.

## Señales de que NO conviene migrar (todavía)

1. **Es software sectorial con funciones únicas**: Presto (mediciones y BC3 en obra), Prevengos (obligaciones legales de prevención), Instalwin (instaladoras), un TPV integrado con su hardware. Los ERP generalistas no lo cubren igual. **Conecta con puente.**
2. **Tu gestoría trabaja con ese programa** (Sage, A3, Contasol) e intercambiáis ficheros. Si cambias tú solo, rompes el flujo con ella. Decidid juntos.
3. **Estás a mitad del ejercicio contable.** Migrar contabilidad a mitad de año complica el cierre. La ventana buena es el **1 de enero**, o el inicio del trimestre si solo es facturación.
4. **El dolor es pequeño.** Si una exportación nocturna a Excel resuelve el 80 % de lo que quieres (informes, resumen del lunes), no migres por el 20 % restante.
5. **No hay nadie que lidere el cambio** dentro de la empresa durante 1-3 meses.

## Haz la cuenta (a 2 años)

**Coste de quedarte** (al año):
- horas de copia-pega × coste de la hora;
- más lo que pagas por puentes, módulos o consultoría para conectarlo;
- más el riesgo normativo (adaptación obligatoria, sanciones).

**Coste de migrar** (una vez, más la diferencia de cuotas):
- licencias del primer año menos lo que dejas de pagar;
- implantación (consultor o partner) y migración de datos;
- formación y semanas de menor productividad;
- riesgo: datos que no pasan bien, módulos sectoriales que el destino no tiene.

**Regla práctica:** si migrar se paga solo en **18-24 meses** y tienes **ventana** (inicio de ejercicio o renovación de licencia), migra. Si no, **conecta con puente** y vuelve a hacer la cuenta en la próxima renovación.

## Si migras: siete pasos para no perder nada

1. **Inventario**: qué datos (clientes, artículos, facturas, contabilidad) y qué procesos dependen del programa.
2. **Elige el destino pensando en el arnés**: que tenga API documentada y, a ser posible, MCP. Comprueba en el catálogo que se conecta "Fácil".
3. **Exporta el histórico** y **conserva el sistema antiguo en solo lectura**. Tienes que guardar la contabilidad y las facturas durante años: no lo borres.
4. **Arranca en una fecha limpia**: inicio de ejercicio o de trimestre. Saldos iniciales y no movimiento a movimiento, salvo que el destino lo importe bien.
5. **Un mes en paralelo** con un proceso real (por ejemplo la facturación) antes de apagar nada.
6. **Conecta el destino al arnés desde el primer día** (`01-TOOLS/<DESTINO>/` y `test_connection`). Así el valor se ve enseguida.
7. **Forma al equipo** y fija quién es el responsable del nuevo sistema.

## La tercera vía: construirlo tú

En la comunidad hay alumnos que, en vez de conectar o migrar, **sustituyen** su programa por uno propio hecho con Claude Code: un CRM a medida, un ERP sencillo, el punto de venta de un obrador, o el reemplazo de una plataforma de 1.000 €/mes. A veces es muy buena idea y a veces sale caro de mantener.

Compensa si se cumplen todas estas condiciones:

- **El alcance es pequeño y estable**: una función concreta, no "todo el ERP".
- **Alguien lo mantiene**: código en un repositorio, copias de seguridad, actualizaciones de seguridad y alguien que lo entienda si tú no estás.
- **Empiezas leyendo** los datos del sistema viejo (exportación o puente) y conviven un tiempo.
- **No factura**: si emite facturas, tu programa también tiene que cumplir Veri\*factu y la factura electrónica. Casi nunca compensa construir la facturación: conéctala.

No compensa si el programa es sectorial y tiene obligaciones legales (prevención de riesgos, nóminas, contabilidad oficial) o si solo lo entiende una persona.

## Destinos típicos

| Si tienes… | Destinos a valorar | Por qué |
|------------|--------------------|---------|
| ERP o contabilidad de escritorio, cerrado, sin soporte | Odoo, Holded, Business Central, Sage Active | En la nube y con API documentada. Los veredictos detallados están en el catálogo. |
| Excel como "ERP" | Primero Google Sheets o Excel en OneDrive (ya conectables). Después un ERP si el volumen lo pide | Mover el Excel a la nube ya lo hace accesible al arnés, sin coste. |
| App WhatsApp Business para pedidos o reservas | WhatsApp Business Platform (Cloud API), directamente con Meta o un proveedor | No es cambiar de herramienta: es pasar a la versión con API. |
| Notion o Airtable usado como CRM | Un CRM con API y MCP (HubSpot, Zoho, Clientify…) cuando haya más de 2-3 comerciales o pipeline real | Mientras sea pequeño, Notion o Airtable se conectan bien y no hace falta cambiar. |

## Relacionado
- [Catálogo de conectividad](https://executive-lab.github.io/conectores-pymes/): veredicto conectar o migrar por plataforma.
- [Cómo conectar una plataforma](./conectar-una-plataforma-con-rsc.md) · [Hablar con el informático](./hablar-con-el-informatico.md).
