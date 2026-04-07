# Langchain-Ollama

La librería **`langchain-ollama`** es el puente oficial que conecta el ecosistema de **LangChain** con **Ollama**. Su función principal es permitirte ejecutar Modelos de Lenguaje Grandes (LLMs) de forma **local** (en tu propia computadora) e integrarlos fácilmente en aplicaciones complejas, cadenas y agentes.


## Características Principales

* **Ejecución Local:** Permite usar modelos como Llama 3, Mistral o Phi-3 sin depender de APIs de pago (como OpenAI) ni enviar datos a la nube.
* **Integración Nativa:** Está diseñada específicamente para el nuevo estándar de LangChain (`langchain-core`), lo que garantiza compatibilidad con herramientas modernas como LangGraph.
* **Soporte Multimodal:** No solo maneja texto; si el modelo lo permite (como LAVA), puedes procesar imágenes.
* **Streaming y JSON Mode:** Soporta respuestas en tiempo real (palabra por palabra) y puede forzar al modelo a responder en formato JSON, algo vital para que los agentes extraigan datos estructurados.

## Funciones Clave para Crear Agentes

Para que un agente funcione, necesita un "cerebro" (el modelo), "manos" (herramientas) y un "sistema de razonamiento". Aquí las funciones esenciales:

### 1. `ChatOllama`
Es la clase principal para instanciar el modelo. Para agentes, es crucial activar el parámetro `format="json"` o usar modelos que soporten **Tool Calling**.

### 2. `bind_tools()`
Esta es la función más importante para agentes modernos. "Vincula" una lista de herramientas (funciones de Python) al modelo para que este sepa que puede usarlas.

### 3. `create_react_agent` (o LangGraph)
Aunque LangChain tiene funciones *legacy*, la forma estándar actual de crear agentes es mediante **LangGraph**. Se utiliza para definir el ciclo de: *Razonamiento -> Acción -> Observación*.

### 4. `OllamaEmbeddings`
Aunque los agentes razonan con el chat, a menudo necesitan memoria o buscar documentos. Esta función convierte texto en vectores localmente para alimentar la base de datos del agente.


## Ejemplo Rápido de Agente

Para crear un agente que use herramientas con Ollama, el flujo lógico es:
1.  **Definir la herramienta:** Una función decorada con `@tool`.
2.  **Preparar el Prompt:** Usar un `ChatPromptTemplate` que indique al agente cómo actuar.
3.  **Ejecutar el Loop:** Usar un ejecutor que procese la salida del modelo y llame a la función de Python correspondiente.


## Documentación Oficial

Puedes encontrar todos los detalles técnicos y guías de migración aquí:
> **[LangChain Ollama Partner Package](https://python.langchain.com/docs/integrations/chat/ollama/)**