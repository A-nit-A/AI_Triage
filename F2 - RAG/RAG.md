# El RAG (Retrieval-Augmented Generation) 

Es una técnica que combina la generación de texto de grandes modelos de lenguaje (como ChatGPT, Gemini o Claude) con la recuperación de información específica desde una base de datos o base de conocimiento. En términos prácticos, esta técnica mezcla las habilidades conversacionales de la inteligencia artificial con la capacidad de consultar documentos precisos antes de entregar una respuesta al usuario.  

Su utilidad principal radica en solucionar las limitaciones de conocimiento de los modelos de inteligencia artificial tradicionales, aportando los siguientes beneficios:

- **Erradicar las alucinaciones**: Es ideal para aplicaciones donde se requiere exactitud, ya que evita que el modelo de lenguaje invente respuestas (alucine) obligándolo a fundamentar su contestación en los documentos extraídos.
- **Acceso a información actualizada y privada**: Los modelos genéricos suelen tener un conocimiento estático (por ejemplo, desconocer un cambio de presidente reciente o noticias futuras) o ignorar datos internos de una empresa. RAG permite que el modelo busque la última versión de la información o consulte datos de nicho al instante.
- **Personalización sin reentrenamiento**: Permite adaptar el conocimiento del modelo a un caso de uso particular y mantener sus datos al día sin tener que recurrir a los procesos de reentrenamiento de la IA, los cuales son sumamente caros y requieren de servidores gigantes.

En resumen, el RAG funciona como un puente que le permite al modelo de lenguaje leer tus documentos relevantes justo antes de responder, asegurando una interacción inteligente, actualizada y totalmente confiable.

En la técnica de RAG, el flujo de trabajo para que la inteligencia artificial responda con información precisa se divide en tres macroprocesos: Indexing (Indexación), Retrieval (Recuperación) y Generation (Generación).


## INDEXING

Este es el proceso de preparación y carga de tu base de datos o documentos para que el sistema los pueda entender.  En esta fase inicial, se toman todos los documentos de la base de conocimiento (por ejemplo, archivos PDF, páginas web, documentos de Word, etc.) y se procesan para convertirlos en un formato que la IA pueda entender y consultar eficientemente. Este proceso implica dividir los documentos en fragmentos más pequeños (chunks), generar representaciones numéricas de su contenido (embeddings) y almacenarlos en una base de datos especializada llamada vector store (base de datos vectorial). Esta base de datos permite realizar búsquedas rápidas basadas en la similitud semántica del contenido.

### División en fragmentos

Primero, los documentos de texto se dividen en partes más pequeñas conocidas como chunks o pedacitos. Esto se hace porque los modelos de lenguaje tienen un límite en su "ventana de contexto" (la cantidad de información que pueden leer a la vez) y porque extraer pedazos específicos ayuda a que la información seleccionada sea mucho más relevante para el usuario.

Para crear los chunks (fragmentos de texto) de manera efectiva en un sistema RAG, se deben considerar los siguientes aspectos técnicos y estructurales:

- **Mantener un tamaño equilibrado**: Los documentos extensos no pueden procesarse por completo debido a que los modelos de lenguaje tienen una "ventana de contexto" limitada. Por ello, el tamaño de cada chunk no debe ser ni muy grande ni muy pequeño. Si el fragmento es excesivo, se dificulta la selección de datos exactos, pero si es muy diminuto, se vuelve complicado realizar una búsqueda de información que tenga sentido. Un ejemplo práctico es establecer un tamaño de fragmento de 1,000 unidades.
- **Realizar divisiones lógicas**: Es crucial evitar cortar el texto a la mitad de una palabra o de una frase. Para lograr esto, se emplean herramientas (como divisores de oraciones o divisores de texto recursivos de librerías como LangChain) que intentan separar la información agrupándola por párrafos o privilegiando los cortes donde hay un punto seguido.
- **Aplicar solapamiento (Chunk Overlap)**: A la hora de realizar los cortes, se debe incluir un margen de superposición, lo cual significa que una cantidad determinada de caracteres del final de un chunk se incluirá al principio del siguiente. Esta técnica es indispensable para que las ideas no pierdan su contexto si una oración importante llega a dividirse entre dos fragmentos separados.

Las herramientas y librerías destacadas para facilitar la división de documentos en chunks son:

- **LangChain**: Es un framework que ofrece procesos automáticos y librerías especializadas para la división de textos. Una de sus herramientas más utilizadas es el Recursive Character Text Splitter, el cual intenta dividir la información agrupándola en párrafos y privilegia hacer los cortes donde hay un punto seguido, evitando así cortar oraciones o palabras por la mitad.
- **LlamaIndex**: Es otra herramienta que permite leer documentos (como PDFs) y fragmentarlos. LlamaIndex utiliza herramientas como el Sentence Splitter (divisor de oraciones), con el cual se puede configurar de manera exacta el tamaño de cada chunk (por ejemplo, 1,000 caracteres) y la cantidad de solapamiento (chunk overlap) entre un fragmento y el siguiente.


### Conversión a números (Embeddings)

Cada uno de estos fragmentos de texto se procesa a través de un modelo de embeddings. Este modelo convierte las palabras y oraciones en series de números (vectores) que logran capturar matemáticamente el significado y contexto del texto.

### Almacenamiento
Los números resultantes se guardan en una base de datos vectorial para que queden listos para ser consultados.




## Retrieval (Recuperación)

Es el proceso donde el sistema busca y extrae la información exacta que necesita para responder la duda del usuario. Cuando un usuario realiza una consulta, el sistema primero analiza esa pregunta y la convierte en un vector numérico. Luego, busca en la base de datos vectorial los fragmentos de documentos que sean más relevantes semánticamente para la consulta. Estos fragmentos recuperados se consideran el "contexto" relevante para la pregunta del usuario.

- **Transformación de la pregunta**: Cuando el usuario hace una consulta, esta pregunta también se transforma en números (embeddings) utilizando el mismo modelo.
- **Comparación matemática**: Al estar la pregunta y los documentos en formato numérico, el sistema utiliza fórmulas matemáticas (como el producto punto) para comparar y calcular la distancia entre los números de la consulta y los de la base de datos.
- **Selección**: El sistema asume que los números que matemáticamente más se parecen son los más relevantes. De esta forma, selecciona el fragmento o los fragmentos de la base de datos que mayor similitud tengan con la pregunta del usuario.




## Generación

Es el paso final donde la inteligencia artificial formula la respuesta para el usuario. Finalmente, el modelo de lenguaje grande recibe la consulta original del usuario junto con los fragmentos de documentos recuperados en la fase anterior. El modelo utiliza esta información contextual para generar una respuesta precisa y fundamentada, evitando alucinaciones y proporcionando información actualizada basada en los documentos proporcionados.

- **Unión de información**: El fragmento de texto altamente relevante que se recuperó en el paso anterior se junta con la pregunta original del usuario.
- **Instrucción al modelo (Prompting)**: Se le envía toda esta información a un modelo de lenguaje (como GPT-4) acompañado de un prompt o instrucción. Esta instrucción le pide al modelo que actúe de manera servicial y que responda a la pregunta del usuario basándose únicamente en el texto de referencia que se le acaba de entregar.
- **Respuesta final**: El modelo procesa estos datos y genera una respuesta articulada y correcta. Gracias a este proceso, se evita que el modelo de lenguaje "alucine" o invente respuestas, asegurando que la información entregada esté fundamentada en tu base de datos.