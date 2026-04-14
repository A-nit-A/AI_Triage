# Agente de Triaje de Emails — Atención al Cliente TechPyme

El problema: Una pequeña tienda online o clínica recibe decenas de correos y mensajes de WhatsApp al día. El dueño pierde 2 horas diarias respondiendo dudas básicas o derivando mensajes al departamento correcto.
La misión del Agente: Actuar como el primer filtro inteligente.

## Flujo del agente

1. Lee el correo y determina la intención (Ej: "¿Dónde está mi pedido?", "Quiero hacer una devolución", "Colaboración de marketing").

2. Si es una duda frecuente (ej. horarios, políticas de envío), el agente redacta y envía la respuesta usando la base de conocimiento (faqs.txt).

3. Si es un problema complejo (ej. producto defectuoso), etiqueta el correo como "Urgente - Soporte" y notifica al encargado humano con un resumen del problema.

## Hoja de ruta

Hoja de ruta paso a paso para crear el agente de triaje de emails.

### Fase 1: Preparación del Entorno Local (El motor de la IA)

El primer paso es instalar el modelo que correrá en local en el ordenador de TechPyme.

    **Instalar Ollama**, e  s la herramienta más sencilla para correr modelos locales. Los alumnos deben descargarla de su web oficial e instalarla (disponible para Windows, Mac y Linux).

    **Descargar el Modelo LLM**, abrir la terminal y ejecutar un modelo ligero pero capaz. Se recomienda llama3 o mistral (se necesitarán unos 8GB de RAM). El comando sería: ollama run llama3.

    **Instalar librerías de Python**, se instalará el ecosistema que conectará Python con Ollama y gestionará el RAG.

### Fase 2: Creación de la Base de Conocimiento (RAG)

Aquí el agente aprenderá sobre la empresa para poder responder.

    **El Documento Fuente**, partimos de un archivo de texto (faqs.txt) con las políticas de la empresa ficticia (ej. "Los envíos tardan 48h", "Se aceptan devoluciones en los primeros 14 días", "Nuestro horario es de 9:00 a 18:00").

    **Carga y Fragmentación (Chunking)**, se usa LangChain para leer el archivo y dividirlo en fragmentos pequeños (chunks) que la IA pueda procesar fácilmente.

    **Embeddings Locales**, se usa sentence-transformers (modelos de HuggingFace que corren en local) para convertir esos fragmentos de texto en vectores matemáticos.

    **Base de Datos Vectorial**, se guardan esos vectores en ChromaDB (una base de datos que se ejecuta localmente en la misma carpeta del proyecto) para que la IA pueda buscar en ellos más tarde.

### Fase 3: La Lógica del Agente (El Cerebro)

El script de Python deberá tomar decisiones basándose en el "correo" entrante.

    **El Prompt del Sistema (System Prompt)**, se define el comportamiento del agente. Por ejemplo: "Eres un asistente de atención al cliente. Tu trabajo es leer el correo del cliente y buscar la respuesta en el contexto proporcionado. Si la respuesta no está en el contexto, o si el cliente está enfadado, debes clasificar el correo como 'ESCALAR_A_HUMANO' y no inventar nada."

    **La Cadena de Ejecución (Chain)**, se construye la secuencia en LangChain:

        Recibir el correo del cliente.

        Buscar en ChromaDB los párrafos de faqs.txt que más se parezcan a la duda del cliente.

        Pasarle al LLM local (Ollama) el correo del cliente y los párrafos encontrados.

    **Respuesta del Agente**, se genera la respuesta usando el LLM local y los párrafos encontrados:

        Si la respuesta está en el contexto, el agente redacta y envía la respuesta usando la base de conocimiento.

        Si es un problema complejo (ej. producto defectuoso), etiqueta el correo como "Urgente - Soporte" y notifica al encargado humano con un resumen del problema.

Para simplificar el proceso se simulará la entrada de correos. Se creará un archivo JSON con 3 o 4 casos de prueba: un correo fácil (pregunta por el horario), un correo sobre un envío (pregunta por devoluciones) y un correo complejo/queja (producto roto, que debería ser escalado).

Los correos respondidos se almacenarán en un archivo JSON llamado respuestas.json

Los correos escalados se almacenarán en un archivo JSON llamado escalados.json



        


