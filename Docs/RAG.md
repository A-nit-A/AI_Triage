# RAG (Retrieval-Augmented Generation) 

Es una técnica que combina la generación de texto de grandes modelos de lenguaje (como ChatGPT, Gemini o Claude) con la recuperación de información específica desde una base de datos o base de conocimiento. En términos prácticos, esta técnica mezcla las habilidades conversacionales de la inteligencia artificial con la capacidad de consultar documentos precisos antes de entregar una respuesta al usuario.  

Su utilidad principal radica en solucionar las limitaciones de conocimiento de los modelos de inteligencia artificial tradicionales, aportando los siguientes beneficios:

- **Erradicar las alucinaciones**: Es ideal para aplicaciones donde se requiere exactitud, ya que evita que el modelo de lenguaje invente respuestas (alucine) obligándolo a fundamentar su contestación en los documentos extraídos.
- **Acceso a información actualizada y privada**: Los modelos genéricos suelen tener un conocimiento estático (por ejemplo, desconocer un cambio de presidente reciente o noticias futuras) o ignorar datos internos de una empresa. RAG permite que el modelo busque la última versión de la información o consulte datos de nicho al instante.
- **Personalización sin reentrenamiento**: Permite adaptar el conocimiento del modelo a un caso de uso particular y mantener sus datos al día sin tener que recurrir a los procesos de reentrenamiento de la IA, los cuales son sumamente caros y requieren de servidores gigantes.

En resumen, el RAG funciona como un puente que le permite al modelo de lenguaje leer tus documentos relevantes justo antes de responder, asegurando una interacción inteligente, actualizada y totalmente confiable.

En la técnica de RAG, el flujo de trabajo para que la inteligencia artificial responda con información precisa se divide en tres macroprocesos: Indexing (Indexación), Retrieval (Recuperación) y Generation (Generación).

## INDEXING

Este es el proceso de preparación y carga de tu base de datos o documentos para que el sistema los pueda entender.  En esta fase inicial, se toman todos los documentos de la base de conocimiento (por ejemplo, archivos PDF, páginas web, documentos de Word, etc.) y se procesan para convertirlos en un formato que la IA pueda entender y consultar eficientemente. Este proceso implica dividir los documentos en fragmentos más pequeños (chunks), generar representaciones numéricas de su contenido (embeddings) y almacenarlos en una base de datos especializada llamada vector store (base de datos vectorial). Esta base de datos permite realizar búsquedas rápidas basadas en la similitud semántica del contenido.

### DIVISIÓN DE FRAGMENTOS

Primero, los documentos de texto se dividen en partes más pequeñas conocidas como chunks o pedacitos. Esto se hace porque los modelos de lenguaje tienen un límite en su "ventana de contexto" (la cantidad de información que pueden leer a la vez) y porque extraer pedazos específicos ayuda a que la información seleccionada sea mucho más relevante para el usuario.

Para crear los chunks (fragmentos de texto) de manera efectiva en un sistema RAG, se deben considerar los siguientes aspectos técnicos y estructurales:

- **Mantener un tamaño equilibrado**: Los documentos extensos no pueden procesarse por completo debido a que los modelos de lenguaje tienen una "ventana de contexto" limitada. Por ello, el tamaño de cada chunk no debe ser ni muy grande ni muy pequeño. Si el fragmento es excesivo, se dificulta la selección de datos exactos, pero si es muy diminuto, se vuelve complicado realizar una búsqueda de información que tenga sentido. Un ejemplo práctico es establecer un tamaño de fragmento de 1,000 unidades.
- **Realizar divisiones lógicas**: Es crucial evitar cortar el texto a la mitad de una palabra o de una frase. Para lograr esto, se emplean herramientas (como divisores de oraciones o divisores de texto recursivos de librerías como LangChain) que intentan separar la información agrupándola por párrafos o privilegiando los cortes donde hay un punto seguido.
- **Aplicar solapamiento (Chunk Overlap)**: A la hora de realizar los cortes, se debe incluir un margen de superposición, lo cual significa que una cantidad determinada de caracteres del final de un chunk se incluirá al principio del siguiente. Esta técnica es indispensable para que las ideas no pierdan su contexto si una oración importante llega a dividirse entre dos fragmentos separados.

Las herramientas y librerías destacadas para facilitar la división de documentos en chunks son:

- **LangChain**: Es un framework que ofrece procesos automáticos y librerías especializadas para la división de textos. Una de sus herramientas más utilizadas es el Recursive Character Text Splitter, el cual intenta dividir la información agrupándola en párrafos y privilegia hacer los cortes donde hay un punto seguido, evitando así cortar oraciones o palabras por la mitad.
- **LlamaIndex**: Es otra herramienta que permite leer documentos (como PDFs) y fragmentarlos. LlamaIndex utiliza herramientas como el Sentence Splitter (divisor de oraciones), con el cual se puede configurar de manera exacta el tamaño de cada chunk y la cantidad de solapamiento (chunk overlap) entre un fragmento y el siguiente.

### CONVERSIÓN A NÚMEROS (Embeddings)

La fase de embeddings es el proceso mediante el cual los fragmentos de texto (chunks) o documentos se transforman en representaciones numéricas, conocidas matemáticamente como vectores. Dado que las máquinas no entienden español ni ningún otro idioma humano, necesitan convertir las frases en listas de números para poder procesar la información.  

Esta fase funciona de la siguiente manera:

- **Captura del significado**: Un modelo de embeddings no asigna números al azar, sino que está entrenado para capturar matemáticamente el significado semántico de las palabras y oraciones. Puedes imaginar el resultado como un "mapa" o un espacio vectorial multidimensional.
- **Coordenadas de similitud**: En este mapa, los conceptos que comparten significado se ubican cerca unos de otros. Por ejemplo, si el texto menciona "manzanas" y "peras", el modelo les asignará coordenadas numéricas muy similares, agrupándolas en la misma zona. Lo mismo ocurre con conceptos como "rey" y "reina". Por el contrario, un concepto completamente distinto, como "mecánica cuántica", recibirá números que lo ubicarán muy lejos de las frutas.
- **Alta complejidad (Dimensiones)**: Para lograr capturar todos los matices del lenguaje, los modelos no usan solo dos o tres coordenadas. Un modelo de embeddings moderno (como los de OpenAI) puede utilizar miles de valores para un solo fragmento, por ejemplo, 1,536 dimensiones o números distintos, los cuales suelen ser valores que oscilan entre el -1 y el 1.
- **Matemáticas con el lenguaje**: Esta conversión numérica es tan profunda que permite encontrar relaciones lógicas haciendo cálculos. Por ejemplo, en este espacio vectorial, si tomas los números que representan la palabra "rey", le restas los de la palabra "hombre" y le sumas los de "mujer", el resultado numérico es equivalente a la palabra "reina".

#### ¿Por qué es fundamental en un sistema RAG? 
Tener los textos convertidos a embeddings es lo que hace posible que la IA encuentre respuestas exactas a una velocidad increíble. Cuando el usuario realiza una pregunta, esta consulta también se transforma en números utilizando el mismo modelo.
A partir de ahí, el sistema ya no busca coincidencias exactas de palabras, sino que utiliza fórmulas matemáticas (como el **producto punto** o la **similitud coseno**) para medir la distancia entre los números de la pregunta y los números de los documentos. Asumiendo que los vectores matemáticamente más cercanos son semánticamente los más relevantes, el sistema extrae el fragmento exacto que necesitas y se lo entrega al modelo de lenguaje para que redacte tu respuesta

**El producto punto**: Es una métrica directa que se utiliza para calcular la distancia espacial exacta entre el vector de la pregunta original y los vectores de los fragmentos de texto almacenados en tu base de datos.
**La similitud coseno**: Es otro algoritmo para calcular la distancia entre diferentes puntos en la base de datos. Al ejecutar una búsqueda con similitud coseno, el sistema no solo devuelve el texto recuperado, sino también un "score" (puntuación) de confianza o similitud. Si este score es muy bajo, le indica al sistema que la información encontrada no es lo suficientemente relevante, lo cual es un mecanismo vital para evitar que el modelo de lenguaje termine alucinando o inventando respuestas

#### Modelos de embeddings especializados

Existen modelos de embeddings especializados para ciertas industrias, incluyendo el ámbito legal y el técnico o de programación.
Aunque los modelos de uso general (como los de OpenAI) son muy populares, utilizar un modelo especializado puede mejorar significativamente la forma en que el sistema entiende la información. Esto se debe a que:

**En documentos legales**: Si administras exclusivamente archivos legales, un modelo de embeddings entrenado específicamente para este sector logrará capturar mucho mejor los significados específicos y los matices de la terminología jurídica, algo que un modelo general podría pasar por alto. Los textos legales son un reto enorme para la IA. Utilizan un vocabulario muy rígido, frases extremadamente largas, referencias cruzadas (ej. "en virtud del artículo 4.2 b") y la sutil diferencia entre un "debe" y un "puede" cambia por completo el sentido del documento.

- **Voyage-Law-2 (de Voyage AI)**: Es uno de los modelos comerciales más potentes ahora mismo para el sector legal.
- **LEGAL-BERT / CaseLawBERT**: Son modelos open-source (de código abierto) basados en la arquitectura clásica de BERT, pero entrenados exclusivamente con textos legales desde cero.


**En documentos técnicos o código**: Para áreas como la programación, existen modelos que comprenden la importancia de elementos técnicos que un modelo amplio ignoraría. Por ejemplo, en el código, un carácter invisible como el "tab" (tabulación) tiene un significado estructural crucial que un modelo especializado sí logra interpretar correctamente.

- **Qwen3-Embedding / Familia Qwen2.5-Coder**: Son de lo mejor en el panorama open-source actual para entender código y documentos técnicos.

- **jina-embeddings-v2-base-code**: Un modelo de código abierto de Jina AI entrenado específicamente para tareas de búsqueda de código.

**Un detalle clave que a veces se olvida**
Para entornos hiper-especializados como el legal o la programación, la forma en la que "troceas" los documentos (chunking) es casi tan importante como el modelo de embeddings. Por ejemplo, al vectorizar código, es un error fatal cortar una función por la mitad; y en textos legales, siempre es mejor dividir semánticamente por artículos o cláusulas completas que por un número fijo de palabras.

### ALMACENAMIENTO

La fase de almacenamiento es el paso donde los fragmentos de texto (chunks) que ya fueron convertidos a representaciones matemáticas (embeddings) se guardan de manera estructurada para que el sistema pueda consultarlos e interpretarlos de forma rápida.
Para que esta fase funcione de manera eficiente, el proceso depende de tecnologías y estructuras específicas:

- **Bases de datos vectoriales**: A diferencia de las bases tradicionales (SQL), la información se almacena en motores diseñados nativamente para comprender e indexar listas de números multidimensionales, destacando opciones como **Chroma DB** o **Qdrant**. Aunque en pruebas de concepto pequeñas se puede llegar a guardar temporalmente en una tabla común o un DataFrame de **Pandas**, en entornos reales es indispensable contar con una base de datos vectorial.
    
- **Estructura de la información (Point Struct)**: Al momento de insertar la información en la base de datos (operación a menudo llamada upsert), no se guardan únicamente los números al azar. Cada fragmento se encapsula con tres elementos fundamentales:
    - **El vector**: La representación numérica (por ejemplo, miles de dimensiones) del texto.
    - **El Payload (Carga útil)**: Es el contenido real que entienden los humanos. Contiene el texto original del chunk y sus metadatos (como el nombre del archivo y el número de página), lo cual es vital para que la IA, después de hacer la coincidencia matemática, pueda leer la información y citar sus fuentes.
    - **El ID único**: Un identificador generado criptográficamente (como un hash MD5 o un UUID) que se le asigna a cada fragmento para evitar que la base de datos se llene de información duplicada si se procesa el mismo archivo más de una vez.
- **Velocidad de búsqueda**: Para poder manejar gigabytes de datos sin colapsar, estas bases de datos agrupan los vectores utilizando algoritmos de indexación avanzados (como HNSW, Hierarchical Navigable Small World). Esto transforma las búsquedas de un modo lineal a un modo logarítmico, permitiendo encontrar el dato exacto entre miles de archivos casi instantáneamente.
- **Persistencia en disco duro**: Un parámetro crítico en la fase de almacenamiento es configurar la base de datos para que persista (guarde) la información en el disco físico del servidor o computadora, y no solamente en la memoria RAM. Si los datos solo residieran en memoria, al apagar el script se perderían todas las horas de indexación y el costo invertido en la API que generó los embeddings. Al persistirlos, la base de conocimiento se carga en milisegundos en usos futuros

## RETRIEVAL (Recuperación)

Es el proceso donde el sistema busca y extrae la información exacta que necesita para responder la duda del usuario. Cuando un usuario realiza una consulta, el sistema primero analiza esa pregunta y la convierte en un vector numérico. Luego, busca en la base de datos vectorial los fragmentos de documentos que sean más relevantes semánticamente para la consulta. Estos fragmentos recuperados se consideran el "contexto" relevante para la pregunta del usuario.

- **Transformación de la pregunta**: Cuando el usuario realiza una pregunta, el sistema toma ese texto y lo transforma en una lista de números o vectores (embeddings) utilizando el mismo modelo que se empleó en la fase de indexación. Esto se hace porque las máquinas necesitan comparar "números con números" para encontrar información.
- **Comparación matemática**: Una vez que la pregunta está en formato numérico, el sistema busca en la base de datos vectorial y compara el vector de la pregunta con los vectores de todos los fragmentos de texto (chunks) almacenados. Para medir qué tan cerca o lejos están estos puntos en el espacio vectorial, utiliza fórmulas matemáticas como el producto punto o la similitud coseno.
- **Selección por relevancia semántica**: El sistema asume que los números que matemáticamente más se parecen son los más relevantes. De esta forma, selecciona el fragmento o los fragmentos de la base de datos que mayor similitud o score más alto tengan con la pregunta del usuario.

- **Recuperación y entrega**: Finalmente, el sistema extrae esos fragmentos altamente relevantes de la base de datos y los deja listos para entregárselos al modelo de lenguaje (junto con la pregunta original del usuario), dando paso así a la fase final de generación de la respuesta.
  
**En resumen**, la fase de retrieval actúa como un buscador matemático ultra rápido que, en lugar de buscar coincidencias exactas de palabras, busca ideas o significados similares utilizando geometría y vectores para encontrar el documento exacto que el modelo de IA necesita leer

## GENERACIÓN

Es el paso final donde la inteligencia artificial formula la respuesta para el usuario. Finalmente, el modelo de lenguaje grande recibe la consulta original del usuario junto con los fragmentos de documentos recuperados en la fase anterior. El modelo utiliza esta información contextual para generar una respuesta precisa y fundamentada, evitando alucinaciones y proporcionando información actualizada basada en los documentos proporcionados.

- **Construcción del Contexto**: El sistema toma el fragmento o los fragmentos de texto altamente relevantes que extrajo de la base de datos en el paso anterior y los junta con la pregunta original del usuario.
- **Diseño del Prompt (Instrucciones Estrictas)**: Toda esta información se ensambla en un prompt o instrucción maestra. Aquí radica el secreto del RAG: se le exige al modelo que actúe como un asistente servicial, pero con la regla inquebrantable de responder única y exclusivamente basándose en el texto de referencia proporcionado. También se le suele instruir explícitamente que evite inventar datos si no los encuentra en el texto y que, de ser posible, cite las fuentes exactas de su respuesta.
- **Instrucción al modelo (Prompting)**: Este paquete completo (las instrucciones, el contexto recuperado y la pregunta) se envía a un Modelo de Lenguaje Grande o LLM (como GPT-4, Llama 3, Mistral o Gemini). Al tener la información real justo a su lado (como en un examen a libro abierto), la IA no necesita depender de su memoria de entrenamiento predeterminada.
- **Respuesta final**: El modelo lee esos párrafos precisos, procesa la respuesta y la articula perfectamente en lenguaje natural para el usuario.

**En resumen**, gracias a estas restricciones impuestas en la fase de generación, se logra erradicar el problema de las alucinaciones, asegurando que la IA se base en hechos reales y en la documentación entregada, en lugar de en su imaginación.

## EVOLUCIÓN DE LOS RAG

El salto de los sistemas RAG tradicionales (lo que ahora llamamos RAG 1.0) a RAG 2.0 y arquitecturas avanzadas como MemoRAG representa la evolución natural para solucionar los "puntos ciegos" que tenían los primeros sistemas.

Para entender su evolución, hay que mirar cuál era el problema original: el RAG clásico era como un estudiante buscando en un libro de texto usando solo el índice. Cortaba los documentos en trozos (chunks), buscaba los más parecidos a la pregunta y se los daba a la IA. Funcionaba muy bien para datos concretos ("¿Cuál es el capital de la empresa?"), pero fracasaba estrepitosamente en preguntas que requerían ver la imagen completa ("¿Cuál es el tono general de todas las comunicaciones de este cliente?").

Aquí tienes cómo estas nuevas arquitecturas resuelven esos problemas:

### RAG 2.0: El enfoque "End-to-End" (De principio a fin)

El término RAG 2.0 (popularizado por empresas como Contextual AI) no es una herramienta nueva, sino un cambio total de paradigma en cómo se construye el sistema.

- **Optimización conjunta (El gran cambio)**: En RAG 1.0, usabas un modelo de embeddings (como los que vimos antes) y un LLM (como GPT-4 o Gemini) por separado. Eran como dos extraños trabajando juntos. En RAG 2.0, el buscador (retriever) y el generador (LLM) se entrenan o se ajustan juntos. El LLM aprende qué tipo de documentos necesita recuperar, y el buscador aprende cómo el LLM prefiere recibir la información.

- **Flujos de trabajo Agénticos**: En lugar de ser un proceso lineal (Pregunta -> Buscar -> Responder), RAG 2.0 introduce agentes. Si el sistema recupera información que no responde del todo a la pregunta, el propio agente "se da cuenta", reformula la búsqueda automáticamente, vuelve a buscar, y solo te responde cuando está seguro de tener la respuesta correcta.

- **GraphRAG integrado**: Muchos sistemas RAG 2.0 incorporan Grafos de Conocimiento. No solo buscan por similitud de palabras, sino que entienden las relaciones. Saben que "Persona A" es "CEO" de "Empresa B", y pueden seguir ese hilo lógico.

### MemoRAG: La revolución de la "Memoria Global"

MemoRAG es una arquitectura específica (surgida a finales de 2024) que ataca directamente el problema de no poder ver el "bosque completo por culpa de los árboles". Introduce un paso intermedio brillante.

- **El modelo de memoria dual**: En lugar de ir directamente a buscar trozos de texto, MemoRAG utiliza un modelo más pequeño y eficiente para leer y comprimir toda tu base de datos en una "memoria global".

- **Generación de "pistas" (Clues)**: Cuando haces una pregunta compleja, MemoRAG primero consulta su memoria global y genera una "pista" o un borrador mental de la respuesta.

- **Búsqueda guiada**: Luego, utiliza esa pista para decirle al buscador exactamente qué trozos de texto originales necesita extraer para validar y enriquecer la respuesta.

Un ejemplo práctico de la evolución:
Imagina que tienes un repositorio legal con 500 sentencias de un mismo juez.

RAG 1.0: Si preguntas "¿Qué opina este juez sobre los delitos fiscales?", buscará los 5 trozos de texto donde más se mencionen esas palabras. Te dará una respuesta sesgada basada solo en esos 5 párrafos aislados.

MemoRAG: Su memoria global recuerda la tendencia general de las 500 sentencias. Generará una pista como "Este juez suele ser severo, pero aplica atenuantes si hay confesión". Luego, buscará los casos exactos que demuestran esto y te dará una respuesta que refleja la realidad de todo el repositorio, no solo de unos pocos fragmentos.

En resumen: pasamos de sistemas que buscan a ciegas (RAG 1.0), a sistemas que piensan antes de buscar y aprenden en conjunto (RAG 2.0 y MemoRAG).