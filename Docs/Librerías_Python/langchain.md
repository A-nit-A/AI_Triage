# LangChain

**LangChain** es una de las librerías más populares en el ecosistema de Python para trabajar con **Modelos de Lenguaje de Gran Tamaño (LLMs)** como GPT-4, Claude o Llama.

Su propósito principal es actuar como un "pegamento" o **framework de orquestación**. En lugar de usar un LLM como un chat aislado, LangChain te permite conectar estos modelos con tus propios datos, otras herramientas y flujos de trabajo complejos para crear aplicaciones con "razonamiento".


## Principales Características
LangChain se basa en la idea de construir "cadenas" (chains) de operaciones. Aquí están sus pilares:

* **Model I/O (Entrada/Salida):** Estandariza la forma en que envías instrucciones al modelo. Incluye la gestión de **Prompts** (plantillas) y la normalización de las respuestas que devuelven los distintos proveedores.
* **RAG (Retrieval Augmented Generation):** Es su función estrella. Permite que el modelo consulte documentos externos (PDFs, bases de datos, webs) para responder preguntas basadas en información que no estaba en su entrenamiento original.
* **Chains (Cadenas):** Permite secuenciar tareas. Por ejemplo: "Paso 1: Resume este texto -> Paso 2: Tradúcelo al inglés -> Paso 3: Envíalo por email".
* **Memory (Memoria):** Los LLMs por naturaleza no "recuerdan" mensajes anteriores. LangChain facilita añadir un historial de conversación para que la IA mantenga el contexto en un chat.
* **Agents (Agentes):** Es el nivel más avanzado. Aquí, el modelo decide qué herramientas usar (como buscar en Google, ejecutar código Python o consultar una calculadora) para resolver una tarea específica.


## Funciones y componentes esenciales que Langchain aporta al ecosistema RAG   

Langchain se ha convertido en el estándar de la industria para construir sistemas de **Generación Aumentada por Recuperación (RAG)** porque ofrece piezas modulares que automatizan el flujo de datos desde documentos crudos hasta respuestas inteligentes.


### 1. Carga y Procesamiento de Datos (Ingesta)
Antes de que la IA pueda leer tus archivos, Langchain debe transformarlos en un formato procesable.

* **Document Loaders:** Funciones para importar datos de casi cualquier fuente (PDFs, Notion, Google Drive, páginas web o bases de datos SQL).
* **Text Splitters:** Dado que los modelos tienen un límite de "contexto", estas funciones dividen documentos largos en fragmentos (*chunks*) más pequeños. El más común es el `RecursiveCharacterTextSplitter`, que intenta mantener párrafos y oraciones juntas para no perder el significado.


### 2. Indexación y Almacenamiento (Vector Stores)
Para encontrar la información rápidamente, Langchain convierte el texto en números (vectores).

* **Embeddings:** Se integra con modelos (OpenAI, HuggingFace, Cohere) para transformar texto en vectores matemáticos que representan conceptos.
* **Vector Stores:** Proporciona una interfaz unificada para conectar con bases de datos vectoriales como **Chroma, Pinecone, FAISS o Weaviate**. Aquí es donde se guardan los fragmentos de texto "indexados".


### 3. Recuperación Intuitiva (Retrievers)
Esta es quizás la parte más potente. Un **Retriever** no es solo una búsqueda; es una lógica para extraer lo más relevante.

* **Similarity Search:** La función básica que busca los fragmentos más parecidos a la pregunta del usuario.
* **MultiQueryRetriever:** Genera variaciones de la pregunta del usuario para obtener mejores resultados desde distintos ángulos.
* **Contextual Compression:** Filtra y resume los fragmentos recuperados para que solo pase lo realmente importante al LLM, ahorrando costos y mejorando la precisión.


### 4. Orquestación del Flujo (Chains y LCEL)
Langchain une la pregunta, la información recuperada y el modelo de lenguaje.

* **RetrievalQA Chain:** Una función "pre-construida" que toma una pregunta, busca en la base de datos y entrega una respuesta final.
* **LCEL (LangChain Expression Language):** Un lenguaje declarativo que permite encadenar funciones de forma personalizada usando el símbolo `|`. Por ejemplo:
    > `chain = setup_and_retrieval | prompt | model | output_parser`
* **Memory:** Permite que el sistema RAG recuerde preguntas anteriores de la conversación para que el usuario pueda hacer preguntas de seguimiento (ej. "¿Puedes darme más detalles sobre *eso*?").


### 5. El "Cerebro" (Prompts y LLMs)
Finalmente, Langchain gestiona cómo se le presenta la información al modelo.

* **Prompt Templates:** Plantillas predefinidas que le dicen al modelo: *"Usa los siguientes fragmentos de contexto para responder la pregunta. Si no sabes la respuesta, di que no sabes"*.
* **Chat Models:** Una interfaz estándar para llamar a diferentes modelos (GPT-4, Claude, Llama 3) sin cambiar el resto de tu código.


### Resumen del Flujo RAG en Langchain

| Etapa | Componente Clave |
| :--- | :--- |
| **Preparación** | `DocumentLoaders` + `TextSplitters` |
| **Almacenamiento** | `Embeddings` + `VectorStore` |
| **Búsqueda** | `Retriever` |
| **Generación** | `ChatPromptTemplate` + `LLM` |

## Documentación Oficial

Puedes encontrar guías detalladas, tutoriales y la referencia de la API en el sitio oficial:

> [**LangChain Documentation (python.langchain.com)**](https://python.langchain.com/v0.2/docs/introduction/)