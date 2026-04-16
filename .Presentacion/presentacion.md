# AI TRIAGE - Agente de Triaje de Emails para TechPyme

Una pequeña tienda online recibe decenas de correos al día. El dueño pierde 2 horas diarias respondiendo dudas básicas o derivando mensajes al departamento correcto.

Nuestro cliente nos pide automatizar este proceso. Para ello crearémos un agente de triaje de emails que actuará como el primer filtro inteligente.

# SOLUCIÓN

- Instalamos un modelo de IA que corra en local.
- Crearemos un RAG con las FAQs de la empresa.
- Programaremos un agente que leerá los correos y decidirá si responderlos o escalarlos en función de si la respuesta está en el RAG o no.

# ARQUITECTURA

## MODELO DE IA LOCAL

## RAG

### ¿QUE ES UN RAG?

**RAG (Retrieval-Augmented Generation)** es una técnica que permite a un modelo de lenguaje (LLM) buscar información relevante en una base de datos propia *antes* de responder. Así el agente:
- ✅ Responde con datos reales de la empresa (no inventa)
- ✅ Puede actualizarse sin reentrenar el modelo
- ✅ Funciona 100% en local (los datos no salen del ordenador)

### CREAR EL UN RAG

Crear un RAG usando LangChain y ChromaDB:

- Instalar las librerias necesarias.
- Cargar el documento con las FAQs.
- Fragmentar el documento - Chunking.
- Modelo de Embeddings.
- Crear la base de datos vectorial - ChromaDB.

## AGENTE

### ¿QUE ES UN AGENTE?

### PROGRAMAR EL AGENTE

- Instalar las librerias adicionales para el uso del agente.
- Comprobar que el modelo local de IA está disponible y ejecutándose.
- Simulación de los emails con un fichero json.
- Conectar con el RAG.
- Definir el prompt del sistema.
- Construir la cadena RAG.
- Ejecutar el agente.


# RAG 2.0


