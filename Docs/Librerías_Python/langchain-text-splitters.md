# Langchain-Text-Splitters

**LangChain-Text-Splitters** es una biblioteca de Python (anteriormente integrada en el núcleo de LangChain) diseñada específicamente para segmentar textos largos en fragmentos más pequeños o "chunks".

Esta pieza es fundamental en aplicaciones de **RAG (Retrieval-Augmented Generation)**, ya que los modelos de lenguaje (LLMs) tienen un límite de tokens y, para recuperar información relevante, es mucho más eficiente buscar en fragmentos específicos que en documentos enteros.


## Características Principales

  * **Preservación del contexto:** No corta el texto de forma arbitraria; intenta mantener juntas las oraciones o párrafos que tienen sentido semántico.
  * **Overlap (Solapamiento):** Permite que el final de un fragmento se repita al inicio del siguiente. Esto evita que se pierda el contexto crítico que podría quedar justo en el punto de corte.
  * **Adaptabilidad:** Ofrece diferentes estrategias dependiendo del tipo de contenido (código, Markdown, texto plano, etc.).
  * **Medición por Tokens o Caracteres:** Puedes decidir el tamaño del fragmento basándote en la longitud del texto o en el conteo de tokens (usando librerías como `tiktoken`).



## Funciones y Clases Principales para RAG

Para construir un sistema RAG, estas son las herramientas que más utilizarás:

1.  **`RecursiveCharacterTextSplitter`**: Es la función "por defecto" y más recomendada. Divide el texto usando una lista de caracteres (como `\n\n`, `\n`, `     ` y `""`) de forma recursiva hasta que los fragmentos tienen el tamaño deseado.
2.  **`CharacterTextSplitter`**: Una versión más simple que divide basándose en un carácter específico definido por el usuario.
3.  **`MarkdownHeaderTextSplitter`**: Ideal para RAG con documentación técnica. Divide el texto basándose en los encabezados (`#`, `##`, `###`), manteniendo la estructura jerárquica del documento.
4.  **`TokenTextSplitter`**: Divide el texto asegurándose de que cada fragmento no exceda un número específico de tokens, lo cual es vital para no sobrepasar los límites de la API de OpenAI o Anthropic.


## Documentación Oficial

Puedes profundizar en todas las estrategias de partición y ver ejemplos avanzados aquí:

> **Documentación de LangChain Text Splitters:** [https://python.langchain.com/docs/modules/data\_connection/document\_transformers/](https://www.google.com/search?q=https://python.langchain.com/docs/modules/data_connection/document_transformers/)

> **Repositorio en GitHub:** [langchain-text-splitters](https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters)