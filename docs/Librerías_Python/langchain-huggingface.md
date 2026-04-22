# Langchain-Huggingface

La librería `langchain-huggingface` es un paquete de integración diseñado para unir el ecosistema de **LangChain** con las herramientas y modelos de **Hugging Face**. 

Básicamente, permite utilizar los miles de modelos de lenguaje (LLMs) y modelos de embedding alojados en el Hugging Face Hub directamente dentro de los flujos de trabajo de LangChain de una manera optimizada y estandarizada.


## Principales Características

* **Integración Nativa:** Sustituye a las integraciones antiguas que estaban dispersas en `langchain-community`, ofreciendo un mantenimiento más robusto.
* **Flexibilidad de Ejecución:** Permite ejecutar modelos de forma local (usando `transformers` y `accelerate`) o de forma remota mediante el **Hugging Face Inference API**.
* **Compatibilidad con Cuantización:** Soporta fácilmente la carga de modelos en bits reducidos (4-bit, 8-bit) para ahorrar memoria RAM/VRAM.
* **Estandarización de Salida:** Los modelos siguen las interfaces `BaseLLM` o `ChatModel` de LangChain, facilitando el intercambio de modelos sin cambiar todo el código.



## Funciones Clave para crear RAG

Para un sistema de Generación Aumentada por Recuperación (RAG), esta librería aporta los dos componentes críticos:

### 1. Generación de Embeddings
Para convertir texto en vectores y guardarlos en una base de datos:
* `HuggingFaceEmbeddings`: La clase estándar para ejecutar modelos de embedding (como los de la serie BGE o E5) localmente.
* `HuggingFaceInferenceAPIEmbeddings`: Para obtener los vectores llamando a la API de Hugging Face sin descargar el modelo.

### 2. Modelos de Lenguaje (LLM)
Para razonar sobre los documentos recuperados y generar la respuesta:
* `HuggingFacePipeline`: Permite cargar modelos para inferencia local. Es ideal si tienes una GPU potente.
* `ChatHuggingFace`: Una capa que adapta modelos de Hugging Face al formato de "Mensajes" (System, User, AI) propio de LangChain.
* `HuggingFaceEndpoint`: Para conectar con "Inference Endpoints" dedicados en la nube.




## Documentación Oficial

Puedes encontrar todos los detalles técnicos, guías de instalación y ejemplos de uso en el siguiente enlace:

> **[Documentación de langchain-huggingface en Python](https://python.langchain.com/docs/integrations/platforms/huggingface/)**