# ChromaDB

ChromaDB es una base de datos vectorial de código abierto diseñada específicamente para construir aplicaciones de Inteligencia Artificial (IA).

A diferencia de las bases de datos que almacenan texto simple, ChromaDB almacena vectores (también conocidos como embeddings). Un embedding es una representación matemática de un dato (como un fragmento de texto, una imagen o un audio) convertida en una larga lista de números. Los modelos de IA utilizan estos vectores para entender el "significado" o el contexto detrás del texto.

Si dos frases tienen un significado similar (por ejemplo, "perro juguetón" y "cachorro feliz"), sus vectores estarán ubicados muy cerca el uno del otro en este espacio matemático multidimensional. ChromaDB se encarga de almacenar millones de estos vectores y de buscar rápidamente cuáles están más cerca entre sí.

## ¿En qué se diferencia de una base de datos SQL?

La diferencia principal radica en cómo almacenan la información y cómo la buscan.

**Bases de Datos SQL** (como PostgreSQL o MySQL):

- **Estructura**: Guardan la información en tablas rígidas con filas y columnas.

- **Búsqueda**: Utilizan coincidencia exacta o palabras clave. Si buscas WHERE título LIKE '%perro%', la base de datos solo te devolverá resultados que contengan la palabra exacta "perro". Si un documento habla de un "cachorro" o un "sabueso", SQL no lo encontrará a menos que le programes reglas complejas.

**ChromaDB** (Base de Datos Vectorial):

- **Estructura**: Guarda listas de números (vectores) junto con metadatos.

- **Búsqueda**: Utiliza similitud semántica. No busca palabras exactas, sino conceptos similares. Si buscas "animales domésticos de cuatro patas", ChromaDB calculará el vector de tu pregunta y encontrará los vectores más cercanos a él, devolviéndote documentos sobre "perros" o "gatos", incluso si las palabras exactas de tu búsqueda no aparecen en el texto.

**En resumen**: Se usan bases de datos vectoriales como ChromaDB para RAG porque los LLMs no pueden leer una biblioteca entera de documentos cada vez que les haces una pregunta (sería lentísimo y muy costoso). ChromaDB actúa como un bibliotecario ultrarrápido que, basándose en el "significado" de tu pregunta, va a la estantería, saca solo las 3 o 4 páginas que contienen la respuesta correcta, y se las entrega al LLM para que te explique la solución.

## ¿Porqué ChromaDB usa SQLite entonces?

Para entender por qué ChromaDB usa SQLite, primero hay que aclarar un detalle arquitectónico clave: ChromaDB no usa SQLite para buscar los vectores (embeddings). La búsqueda de similitud vectorial la maneja un motor especializado (típicamente hnswlib). Entonces, ¿para qué usa SQLite? Lo utiliza exclusivamente para almacenar y consultar los metadatos, los IDs y los documentos asociados a esos vectores.

Principales por las que los creadores de ChromaDB eligieron SQLite para esta tarea:

- **Fricción cero** (Developer Experience)

El objetivo principal de ChromaDB en sus inicios fue ser la base de datos vectorial más fácil de usar para los desarrolladores. Al integrar SQLite, puedes usar ChromaDB simplemente haciendo un pip install chromadb en Python.

No requiere configuración: No necesitas levantar un servidor Docker, ni configurar credenciales, ni instalar dependencias pesadas como PostgreSQL o MySQL. Funciona directamente "out of the box".

- **Arquitectura Embebida** (Embedded)

SQLite es una base de datos "embebida", lo que significa que se ejecuta dentro del mismo proceso que tu aplicación.

Esto hace que ChromaDB sea ideal para prototipado rápido, entornos locales, notebooks de Jupyter (como Google Colab) y aplicaciones de escritorio. No hay latencia de red al comunicarse con la base de datos de metadatos porque todo ocurre en la memoria o en el disco local de tu máquina.

- **Filtrado eficiente de Metadatos**

En las aplicaciones de Inteligencia Artificial (como RAG - Retrieval-Augmented Generation), casi nunca buscas solo por similitud vectorial. Normalmente quieres hacer búsquedas combinadas: "Búscame los vectores más similares a X, pero solo si el documento es del año 2023 y el autor es 'Juan'".

SQLite es increíblemente maduro, rápido y eficiente haciendo este tipo de filtrado estructurado (cláusulas WHERE). ChromaDB usa SQLite para pre-filtrar o post-filtrar los resultados según los metadatos antes de devolverte la respuesta final.

- **Persistencia simple basada en archivos**

Cuando le indicas a ChromaDB que guarde los datos en disco de forma persistente, SQLite guarda toda la información relacional y los metadatos en un único archivo estándar (.sqlite3). Esto hace que hacer copias de seguridad, migraciones o compartir la base de datos con un compañero sea tan fácil como copiar y pegar un archivo.

**En resumen**, ChromaDB usa una arquitectura híbrida inteligente. Usa algoritmos en C++ (hnswlib) para la matemática pesada de los vectores, y usa SQLite porque es el estándar de oro para guardar datos estructurados localmente sin complicarle la vida al desarrollador.
