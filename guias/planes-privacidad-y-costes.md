---
type: article
title: Qué plan de IA pagar, qué pasa con tus datos y cuánto cuesta
description: Comparativa verificada de planes de Claude, ChatGPT, Gemini y Copilot (entrenamiento, retención, DPA, precio) con tabla de decisión por caso, para dueños y directivos de pymes.
tags: [guia-alumnos, privacidad, rgpd, planes, costes, tokens, ia-local]
timestamp: 2026-10-09T18:00:00Z
topic: guias
status: draft
sources: []
score: 0.0
---

# Qué plan de IA pagar, qué pasa con tus datos y cuánto cuesta

> Para: dueños y directivos que usan Claude, ChatGPT, Gemini o Copilot y dudan de qué plan contratar y qué datos pueden subir.
> Conseguirás: elegir plan por caso, saber qué se hace con tus datos y calcular el gasto mensual real.

**Fecha de consulta: 2026-10-09.** Precios, límites y condiciones cambian a menudo (este año ha habido varios cambios de precio y de política). Antes de pagar o de subir datos de clientes, repasa la fuente oficial de la sección Fuentes. Lo que no se ha podido confirmar en la fuente del proveedor va marcado como **no verificado**.

## En resumen
La contradicción de clase («la licencia importa poco» frente a «Enterprise es lo seguro») se resuelve así. Las dos frases son medias verdades.

- **Lo que importa es el contrato, no el nombre del plan.** Un plan personal te da una política de privacidad. Un plan de empresa o la API te dan además un **DPA** (*Data Processing Addendum*, contrato de encargado de tratamiento: el documento que dice que el proveedor solo trata tus datos por encargo tuyo, como una gestoría con su cláusula de confidencialidad). Sin DPA, el RGPD te complica subir datos personales de clientes.
- **Enterprise no es obligatorio para tener contrato.** Claude Team, ChatGPT Business y la API ya incluyen DPA y no entrenan por defecto (detalle abajo). Enterprise añade control: retención a medida, registros de auditoría, residencia de datos, SSO.
- **Tu mayor riesgo suele ser el humano.** Subir una nómina a una cuenta personal, o pegar datos de pacientes, es el fallo típico. Anonimizar antes de enviar reduce el riesgo en cualquier plan.

Tiempo para decidir: 20 minutos con esta guía. Quién actúa: tú; si hay Microsoft 365 o Google Workspace, tu informático, que activa y limita las funciones.

## Antes de empezar

1. Anota qué datos vas a mandar: ninguno personal, personales de clientes o empleados, o especiales (salud, nóminas, biometría).
2. Anota cuántas personas lo usarán. Muchos planes de empresa exigen **mínimo de asientos** (Team de Claude: 2; Business de ChatGPT: 2 según lo que cuentan los alumnos, ver nota de precios).
3. Pregunta a tu informático si ya pagáis Microsoft 365 o Google Workspace: puede que ya tengáis IA con contrato incluido.

## Las vías, de mejor a peor (para datos de clientes)

| Vía | Para qué sirve | Quién la hace | Coste | Dificultad |
|---|---|---|---|---|
| Plan de empresa (Claude Team/Enterprise, ChatGPT Business/Enterprise) | Chat con DPA y sin entrenar | Tú | Desde ~20-25 $ por usuario y mes | Baja |
| IA dentro de Microsoft 365 o Google Workspace | Chat y asistente sobre tus documentos, con contrato corporativo | Tu informático | Ver tablas | Media |
| API con DPA (y ZDR si lo necesitas) | Automatizaciones, agentes, apps propias | Tú o informático | Pago por tokens | Media |
| IA local | Datos que no pueden salir de tu red | Informático | Hardware (ver sección) | Alta |
| Plan personal con entrenamiento desactivado | Uso propio sin datos de terceros | Tú | 0-20 € | Baja |

## Paso a paso: elegir en 5 preguntas

1. ¿Subirás datos personales de terceros (clientes, empleados, pacientes)? Si sí, descarta Free y planes personales: necesitas DPA.
2. ¿Son datos de salud, nóminas o biométricos? Mira la fila de «datos de salud o nóminas» en la tabla final.
3. ¿Sois 2 o más? Plan de equipo. ¿Eres uno solo? Mira la pregunta «privacidad siendo yo solo» en las preguntas de alumnos.
4. ¿Tenéis ya Microsoft 365 o Workspace? Empieza por lo que ya pagáis.
5. ¿Vas a automatizar? Entonces la API se cobra aparte de cualquier suscripción de chat.

**Dile a tu agente:** *«Revisa en `02-DOCS` qué datos manejo y dime qué plan de IA me corresponde según `planes-privacidad-y-costes.md`»*. El agente no sustituye a tu asesor legal: te ayuda a ordenar la información.

## Claude (Anthropic)

| Plan | Precio (sin impuestos) [1] | Mínimo | Entrena por defecto | Contrato |
|---|---|---|---|---|
| Free | 0 | 1 | Solo si activas «mejorar Claude» (ver nota) [2] | Términos de consumidor, sin DPA [3] |
| Pro | 17 $/mes con pago anual; 20 $/mes mensual | 1 | Igual que Free [2] | Sin DPA [3] |
| Max | Desde 100 $/mes (solo mensual) | 1 | Igual que Free [2] | Sin DPA [3] |
| Team | Estándar 20 $/asiento anual (25 $ mensual); Premium 100 $ anual (125 $ mensual) | 2 (hasta 150) | No, por defecto [1] | DPA incluido en términos comerciales [3] |
| Enterprise | 20 $/asiento anual más uso a tarifas de API (según la página de precios) [1] | No indicado | No | DPA [3] |
| API | Por tokens (ver costes) [1] | 0 | No [3] | DPA [3] |

- **Entrenamiento en planes personales.** Anthropic dice que usa tus chats para entrenar si aceptas la opción de mejora del modelo; los chats incógnito y el contenido bruto de conectores quedan fuera [2]. El valor por defecto de esa casilla **no está indicado en la página oficial**; en 2025 se anunció como opt-out. Entra tú mismo en `claude.ai/settings/data-privacy-controls` y comprueba que está apagada. Apagarla no deshace lo ya entrenado.
- **Retención personal.** Con entrenamiento activo, hasta 5 años en formato desidentificado. Los chats borrados desaparecen de sus sistemas en 30 días. Los chats marcados por seguridad se guardan hasta 2 años [4].
- **Retención comercial.** API: borrado en 30 días salvo excepción. Los «modelos cubiertos» (serie Fable/Mythos 5) exigen 30 días de retención por seguridad aunque tengas ZDR [5]. En chats y proyectos de Enterprise la retención es indefinida salvo que el admin la fije; el mínimo configurable es 30 días [5].
- **ZDR (retención cero).** Significa que el proveedor no guarda tus prompts ni respuestas tras devolverte la respuesta: como una ventanilla que atiende y no archiva copia. Se pide **a ventas de Anthropic**, se activa por organización y no es automático. No cubre las interfaces de Claude Team y Enterprise ni la Consola [5]. Sigue guardando resultados del clasificador de seguridad.
- **Residencia en la UE.** La documentación menciona un parámetro `inference_geo` para residencia de datos en la API, pero las regiones y garantías no constan: **no verificado**. Pregunta a tu contacto comercial o al Trust Center.
- **Funciones.** Team incluye Claude Code, Cowork, SSO, controles de conectores y facturación central. Faltan SCIM, registros de auditoría y retención personalizada, que son de Enterprise [1]. Pro incluye Claude Code y proyectos ilimitados [1].
- **Aviso sobre HIPAA.** La página de precios dice que Team no es «HIPAA-ready» y Enterprise sí [1]. Es un marco de EE. UU., pero sirve de pista sobre lo que el proveedor promete para salud.

## ChatGPT (OpenAI)

Los datos de privacidad vienen de páginas oficiales de OpenAI y de su documentación de API. **Los precios de ChatGPT no se han podido confirmar en la página oficial** a fecha de consulta: son orientativos.

| Plan | Precio orientativo (no verificado oficialmente) [6] | Entrena por defecto | DPA |
|---|---|---|---|
| Free | 0 | Sí (se puede desactivar) [7] | No |
| Go | ~8 €/mes (si existe en tu país, comprueba) [6] | Sí, plan personal [7] | No |
| Plus | ~23 €/mes (IVA incluido) [6] | Sí (se puede desactivar) [7] | No |
| Pro | Dos niveles, ~103 € y ~229 €/mes [6] | Sí (se puede desactivar) [7] | No |
| Business | ~21 €/usuario anual, ~26 € mensual, mínimo 2 usuarios, fuentes discrepantes [6] | No por defecto [8] | Sí [8] |
| Enterprise | A medida, con ventas [6] | No por defecto [8] | Sí [8] |
| API | Por tokens, en dólares, factura aparte [9] | No por defecto [9] | Sí [8] |

- **Dónde se desactiva el entrenamiento (planes personales).** Ajustes, **Controles de datos**, apaga «Mejorar el modelo para todos». No es retroactivo. Si pulsas pulgar arriba o abajo en una respuesta, esa conversación se puede usar igualmente [7].
- **Retención.** En Business, el admin fija la retención; lo borrado desaparece de los sistemas en 30 días, salvo obligación legal [8]. En la API, los registros de abuso se guardan hasta 30 días [9].
- **ZDR.** Es una función **solo de la API**, no de ChatGPT. Hay que pedirla a ventas de OpenAI y aprobarla. Se configura por organización en Ajustes, Organización, Controles de datos. Endpoints elegibles: embeddings, audio, moderación, completions, realtime y algunas imágenes. No elegibles: conversaciones, asistentes, vector stores, ficheros, batches y agentes [9].
- **Residencia en la UE.** La API permite elegir Europa (EEE y Suiza) con `eu.api.openai.com`, pero exige ZDR u otro control de retención aprobado, y lleva un recargo del 10 % en modelos recientes [9]. Enterprise y Edu también pueden fijar el almacenamiento en Europa [8]. En Business **no consta residencia** en la fuente que vi: no verificado.
- **Funciones.** Según alumnos de clase, los agentes del espacio de trabajo («Workspace Agents») solo están en Business, Enterprise y Edu, no en Plus; el coste extra por créditos estaba sin anunciar. **No verificado hoy.** Los GPTs personalizados y los proyectos existen en planes de pago; si se pueden crear en Go o Free: no verificado.
- **Compartir un GPT con archivos de empresa.** Lo que subes como conocimiento de un GPT queda sujeto al plan donde lo creas. En una cuenta personal, aplica la política personal.

## Gemini (Google)

| Producto | Entrena por defecto | Retención | Contrato |
|---|---|---|---|
| Gemini con cuenta personal | Sí, si «Actividad de Gemini» está activa [10] | 18 meses por defecto (3, 18, 36 o indefinido). Con la actividad desactivada, 72 horas [10] | Términos de consumidor |
| Gemini en Google Workspace | No sin tu permiso previo [11] | El admin elige 3, 18 o 36 meses; por defecto 18 [11] | Cloud Data Processing Addendum [11] |

- **Cuenta personal.** Con la actividad activada, Google usa tus chats para mejorar y entrenar. Una parte la revisan personas, desvinculada de tu cuenta, y lo revisado se guarda hasta 3 años aunque borres la actividad [10]. Desactívalo en la configuración de Actividad de Gemini. Los chats temporales no los revisan, pero se guardan 72 horas [10]. El valor por defecto de la actividad **no está indicado** en la página oficial.
- **Workspace.** Google afirma que no revisan personas tus chats ni ficheros del Gemini de Workspace [11]. Residencia en la UE para Gemini en Workspace: **no verificado** (la página no lo trata).
- **Precios Workspace (sin impuestos, mensual, por usuario) [12].** Starter 6,80 €, Standard 13,60 €, Plus 21,10 €, Enterprise a consultar. Gemini va incluido (acceso básico en Starter, ampliado en el resto). Hay una oferta de lanzamiento con descuento a partir del 23 de octubre de 2026. Hasta 300 usuarios en Starter, Standard y Plus. El pago anual ahorra un 16 %.
- **Plan personal de pago (Google AI Pro, etc.):** precio y condiciones **no verificados**.
- **Notebook (NotebookLM).** En Workspace sus datos no siguen los ajustes de región del dominio [11]. Para clientes, comprueba con tu informático.

## Microsoft Copilot

Microsoft cambió el nombre: «Microsoft 365 Copilot» ahora se llama simplemente **Microsoft Copilot** [13].

| Producto | Entrena por defecto | Contrato | Precio orientativo |
|---|---|---|---|
| Copilot personal (en Microsoft 365 Personal/Familiar o Premium) | **No verificado** | Términos de consumidor | Personal ~99 €/año, Familiar ~129 €/año, Premium ~219 €/año según una guía [14]. Copilot Pro dejó de venderse (soporte hasta el 1-ago-2026) [14] |
| Copilot Chat (gratis con M365 empresa) | No: prompts, respuestas y datos de Graph no entrenan modelos base [13] | DPA de Microsoft [13] | Incluido en el plan [14] |
| Microsoft Copilot de pago (licencia sobre M365) | No [13] | DPA de Microsoft, RGPD [13] | Copilot Business ~18-21 €/usuario/mes (hasta 300 usuarios); versión estándar ~26-28 € [14] |

- **Precios de Microsoft:** vienen de guías de terceros que discrepan; **no verificados en la página oficial**. Pide presupuesto a tu partner de Microsoft.
- **Datos y UE.** El tráfico de usuarios UE se queda dentro del **EU Data Boundary** (frontera de datos de la UE), pero **los modelos de Anthropic como subencargado están excluidos de esa frontera** [13]. Si tu informático activa modelos de Anthropic dentro de Copilot, tus datos pueden salir de la UE. Es un interruptor de administrador.
- **Retención.** El historial de actividad se guarda según las políticas de retención de Purview que fije el admin; cada usuario puede borrar el suyo desde «Mi cuenta» [13].
- **Permisos.** Copilot solo muestra lo que cada usuario ya puede ver [13]. Si tu SharePoint está mal ordenado, Copilot enseñará a un empleado lo que sus permisos ya le permitían. Esto explica el miedo de clase a que el agente muestre sueldos. Ordena permisos antes de activarlo.
- **Agentes y conectores.** El admin decide qué agentes se permiten en el centro de administración de M365 [13].
- **Lo que decían los alumnos** («caro y flojo»): es opinión de clase, no dato verificado.

## Tabla final de decisión por caso

| Caso | Plan recomendado | Por qué | Lo que NO debes hacer |
|---|---|---|---|
| **Uso personal** (sin datos de terceros) | Claude Pro o ChatGPT Plus, con entrenamiento apagado | Barato, sin contrato | Pegar datos de clientes |
| **Datos de clientes** | Claude Team, ChatGPT Business, o API con DPA | DPA incluido y sin entrenar [3][8] | Usar Free, Plus o Pro |
| **Datos de salud o nóminas** | Enterprise o API con DPA, residencia UE y ZDR si el proveedor la ofrece; o IA local; anonimiza siempre | Datos de categoría especial (art. 9 RGPD): exige base legal y evaluación de impacto | Subirlos sin anonimizar a un plan sin contrato |
| **Equipo de 2-10 personas** | Claude Team (2 mín.) o ChatGPT Business (2 mín.). Si ya tenéis Workspace, el Gemini incluido | Contrato desde 2 asientos, coste lineal | Compartir una sola cuenta entre directivos |
| **Empresa con IT y Microsoft 365** | Microsoft Copilot con permisos ordenados, más API o Team para automatizaciones | Contrato Microsoft ya firmado, EU Data Boundary [13] | Activar modelos de Anthropic sin revisar la frontera de datos |

Compartir cuenta entre directivos para «acumular contexto» rompe las condiciones de uso y mezcla datos. Usa un proyecto compartido en un plan de equipo.

## IA local: cuándo compensa

IA local es un modelo de lenguaje que corre en un ordenador tuyo, sin enviar nada a internet. Es como contratar a un empleado interno en vez de una gestoría externa.

**Compensa cuando:** los datos no pueden salir de tu red (clínicas, despachos), el volumen de uso es alto y constante, o necesitas funcionar sin conexión.

**No compensa cuando:** usas pocas consultas, necesitas la máxima calidad, o no hay nadie que lo mantenga.

**Coste orientativo (no verificado hoy, cifras de clase):** un alumno citó entre 6.000 y 30.000 € de inversión; otro, más de 4.000 € para un equipo capaz. La calidad de un modelo local pequeño es inferior a la de un modelo de frontera.

**Límites:** hay que actualizar, vigilar la seguridad y mantener el equipo. El modelo no se actualiza solo.

**Anonimizar antes de enviar.** Sustituye nombres, DNI, IBAN, teléfonos y direcciones por códigos (por ejemplo CLIENTE_01), guarda la tabla de equivalencias en tu equipo y revierte al recibir el resultado. Hazlo con **código determinista** (reglas fijas, expresiones regulares), no pidiéndoselo a un modelo: un alumno comprobó que un modelo no es fiable para esto. Aun así, una agenda con nombre, cargo y empresa puede identificar a alguien: anonimizar bien es difícil.

Los modelos de proveedores chinos (DeepSeek, Qwen) tienen condiciones distintas según los sirvas tú o uses su API; **no verificado hoy**. Si lo ejecutas en local, los datos no salen.

## Cómo calcular el coste mensual real

**Suscripción:** precio fijo por persona con límites de uso por ventana de 5 horas y por semana. No pagas más al agotarlos: te quedas sin uso hasta que se reinicia. En Claude, Cowork y Claude Code gastan mucho más que el chat.

**API (pago por uso):** pagas por **tokens**, que son trozos de texto (una palabra son 1-2 tokens). Precios de Claude por millón de tokens, entrada/salida [1]:

| Modelo | Entrada | Salida |
|---|---|---|
| Haiku 5.5 | 0,10 $ | 0,50 $ |
| Sonnet 5.5 | 2 $ | 10 $ |
| Opus 5.5 | 4 $ | 20 $ |
| Fable 5.1 | 10 $ | 50 $ |

La lectura de caché y el proceso por lotes (batch, -50 %) abaratan. Los precios están en dólares y sin IVA.

**Fórmula:** coste = (tokens de entrada × precio entrada + tokens de salida × precio salida) × tareas al mes.

**Ejemplo (cálculo propio con los precios de arriba):** una tarea con 20.000 tokens de entrada y 2.000 de salida cuesta 0,06 $ con Sonnet, 0,12 $ con Opus y 0,003 $ con Haiku. Con 440 tareas al mes (20 al día, 22 días): ~26 $ con Sonnet, ~53 $ con Opus.

**Qué compensa:**
- Uso diario personal e interactivo: suscripción.
- Automatización de volumen predecible (leer facturas, clasificar emails): API con modelo pequeño.
- Agentes de programación a jornada completa: plan Max o Premium, porque el equivalente en API suele salir más caro. Esta comparación no está verificada con cifras.

**Cómo no quemar los límites:**
1. Usa el modelo pequeño para tareas simples y el grande solo para razonar.
2. Planifica antes de pedir tareas grandes: un proyecto grande sin plan se corta a mitad.
3. Abre conversaciones nuevas en lugar de arrastrar un hilo largo; cada mensaje reenvía todo el historial.
4. No cruces hojas enormes de Excel con el chat: pásale un resumen o procésalas con un script.
5. Pon un tope de gasto en la API, y alertas de consumo.
6. Apunta mensualmente cada suscripción y para las que no usas.

**Ojo con el baneo:** usar tu suscripción personal en herramientas de terceros puede incumplir las condiciones y hacer que te cierren la cuenta. Para automatizar, usa API con su clave.

## Marco legal mínimo (lenguaje llano)

- **RGPD** (Reglamento 2016/679). Si metes datos personales en una IA, el proveedor es tu **encargado de tratamiento**. Necesitas un DPA firmado, una base legal para tratar esos datos y decir a tus clientes que usas proveedores. Los datos de salud y biométricos tienen protección reforzada (art. 9). Transferir datos fuera de la UE exige garantías (cláusulas contractuales tipo, SCC); Anthropic [3] y OpenAI [8] ofrecen DPA con ellas. Texto: https://eur-lex.europa.eu/eli/reg/2016/679/oj. Autoridad en España: la AEPD, https://www.aepd.es.
- **AI Act** (Reglamento UE 2024/1689). Clasifica los sistemas de IA por riesgo. Si usas IA de otros, eres **«responsable del despliegue»**. Fechas según la Comisión [15]: 2 feb 2025 prohibiciones y **alfabetización en IA** (tu equipo debe saber usarla); 2 ago 2025 reglas de modelos de propósito general; 2 ago 2026 aplicación general y transparencia; 2 dic 2027 sistemas de alto riesgo del anexo III (empleo, educación, biometría); 2 ago 2028 anexo I. El «Ómnibus de IA» retrasó esas fechas de alto riesgo y entró en vigor el 27 jul 2026 [15]. Usar IA para decidir contrataciones o evaluar empleados es alto riesgo. Texto: https://eur-lex.europa.eu/eli/reg/2024/1689/oj.
- Este apartado no es asesoramiento jurídico. Para salud, nóminas o decisiones sobre personas, consulta con un abogado o DPO. Comprueba la versión vigente en los enlaces oficiales.

## Preguntas de alumnos

1. **¿Entrenan con mis datos los planes de pago?** Depende. Planes personales (Plus, Pro, Max): pueden entrenar si la opción está activa; apágala. Planes de empresa y API de Claude y OpenAI: no entrenan por defecto [1][8][9].
2. **¿Puedo tener privacidad siendo solo yo, si el plan de empresa pide varias licencias?** Claude Team y ChatGPT Business piden 2 asientos [1][6]. Alternativa para uno: la API con DPA, que no tiene mínimo [3]. En plan personal, apaga el entrenamiento, pero no tendrás DPA.
3. **¿Team o Enterprise de Claude garantiza el entorno empresarial?** Ambos incluyen DPA y no entrenan. Enterprise añade auditoría, SCIM, retención personalizada y control de red [1].
4. **¿Qué licencia protege los datos de clientes cumpliendo el RGPD?** La que incluya DPA (Team, Business, Enterprise, API), más base legal tuya y datos mínimos. El plan no te exime de tus obligaciones.
5. **¿Puedo subir datos de salud a ChatGPT?** En planes personales, no. En Enterprise o API con DPA, residencia en la UE y ZDR es posible, pero necesitas evaluación de impacto. Si hay duda, anonimiza o usa IA local.
6. **Si Enterprise protege, ¿por qué grandes empresas hacen su propia solución?** Por control total, integración y costes a gran escala. Es decisión de arquitectura, no prueba de que Enterprise sea inseguro. No verificado en fuentes.
7. **¿Usar la API es más privado y barato que la suscripción?** Más privado: sí, con DPA y ZDR. Más barato: depende del volumen (ver fórmula). Se paga aparte de la suscripción de chat.
8. **¿Qué privacidad tiene Copilot en versión empresa?** Los datos no entrenan modelos base, cumple RGPD y EU Data Boundary, salvo modelos de Anthropic [13]. Revisa los permisos de SharePoint.
9. **¿Cambiar de plan hace perder memoria y GPTs?** **No verificado.** Exporta tus instrucciones y memoria a un fichero antes de bajar de plan.
10. **¿Tonto pagar Claude y ChatGPT a la vez?** No si cada uno te da algo distinto. Sí si pagas tres o cuatro sin medir uso. Revisa cada mes cuál has usado.

## Errores típicos

- Creer que «de pago» equivale a «con contrato». Plus y Pro no tienen DPA.
- Fiarse de un precio de blog: pide siempre la página oficial y suma el IVA.
- Subir datos de clientes a una cuenta personal «solo para probar».
- Pensar que ZDR se activa desde ajustes: se pide a ventas [5][9].
- Activar Copilot sin ordenar permisos de SharePoint.
- Usar la suscripción personal para automatizar en lugar de la API.
- Dar por hecho que la IA anonimiza bien: usa reglas deterministas.

## Fuentes

Todas consultadas el 2026-10-09.

1. Precios de Claude: https://claude.com/pricing
2. Anthropic, ¿se usan mis datos para entrenar?: https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training 
3. Anthropic, DPA: https://privacy.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa
4. Anthropic, retención consumidor: https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data
5. Anthropic, retención comercial y ZDR: https://privacy.claude.com/en/articles/8956058-i-have-a-zero-data-retention-agreement-with-anthropic-what-products-does-it-apply-to y https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
6. Precios de ChatGPT (guía de terceros, no oficial): https://geotoolbox.ai/es/blog/precio-chatgpt. Página oficial: https://chatgpt.com/pricing
7. OpenAI, controles de datos: https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt
8. OpenAI, privacidad empresarial (vía búsqueda): https://openai.com/enterprise-privacy/ y https://openai.com/business-data/
9. OpenAI, datos de la API, ZDR y residencia: https://developers.openai.com/api/docs/guides/your-data
10. Google, privacidad de las apps de Gemini: https://support.google.com/gemini/answer/13594961
11. Google, privacidad de IA generativa en Workspace: https://knowledge.workspace.google.com/admin/gemini/generative-ai-in-google-workspace-privacy-hub
12. Precios de Google Workspace: https://workspace.google.com/pricing
13. Microsoft Learn, datos y privacidad de Copilot: https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-privacy
14. Precios de Copilot (guías de terceros, no oficiales): https://www.primend.com/blog/microsoft-365-copilot-gets-even-more-accessible/ y https://office-watch.com/2026/microsoft-365-plans-overview/
15. Comisión Europea, marco de la IA: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

## Relacionado
- [Conectar una plataforma con RSC](./conectar-una-plataforma-con-rsc.md)
- [Hablar con el informático](./hablar-con-el-informatico.md)
- [Conectar o migrar](./conectar-o-migrar.md)
- [Conectividad de plataformas](https://executive-lab.github.io/conectores-pymes/)
