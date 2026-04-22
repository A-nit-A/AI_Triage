# LangChain-Chroma

La librería `langchain-chroma` es el paquete de integración oficial que permite utilizar **ChromaDB** (una base de datos de vectores de código abierto) dentro del ecosistema de **LangChain**.

Su propósito principal es actuar como **memoria a largo plazo** para modelos de lenguaje, permitiendo almacenar y buscar fragmentos de texto basados en su significado semántico (embeddings), lo cual es el corazón de cualquier sistema **RAG** (Retrieval-Augmented Generation).


## Principales Características

  * **Persistencia sencilla:** Permite guardar tus datos en el disco local con una sola línea de código, sin necesidad de configurar servidores complejos.
  * **Velocidad:** Está optimizada para realizar búsquedas de "vecinos más cercanos" (similitud) de forma extremadamente rápida.
  * **Integración Nativa:** Al ser un paquete dedicado, se conecta perfectamente con las herramientas de LangChain como `Document`, `Embeddings` y `Retrievers`.
  * **In-Memory por defecto:** Puedes usarla en la memoria RAM para pruebas rápidas o scripts temporales.


## Funciones clave para crear un sistema RAG

Para construir un sistema RAG, generalmente seguirás este flujo utilizando las funciones de `langchain_chroma`:

### 1\. Creación y Almacenamiento

  * **`Chroma.from_documents()`**: Es la función más común. Toma una lista de objetos `Document`, calcula sus embeddings y los guarda en la base de datos.
  * **`Chroma.from_texts()`**: Similar a la anterior, pero acepta directamente una lista de strings (texto plano).

### 2\. Búsqueda y Recuperación

  * **`vectorstore.similarity_search()`**: Busca los fragmentos más parecidos a una pregunta del usuario. Devuelve los documentos que contienen la información relevante.
  * **`vectorstore.as_retriever()`**: Convierte la base de datos en un objeto "Retriever". Este es el paso crucial para conectar Chroma con una cadena de LangChain (Chain) que genere la respuesta final.

### 3\. Gestión de Datos

  * **`Chroma(persist_directory=...)`**: Se usa para cargar una base de datos que ya existe en tu disco duro.
  * **`vectorstore.add_documents()`**: Permite añadir más información a una base de datos ya creada sin tener que empezar de cero.

### Documentación Oficial

Puedes encontrar todos los detalles técnicos, parámetros y guías de migración en el sitio oficial de LangChain:

  > **Integración de Chroma en LangChain:** [python.langchain.com/docs/integrations/vectorstores/chroma/](https://python.langchain.com/docs/integrations/vectorstores/chroma/)   

  > **Repositorio de la librería:** [GitHub - langchain-chroma](https://www.google.com/search?q=https://github.com/langchain-ai/langchain-chroma)