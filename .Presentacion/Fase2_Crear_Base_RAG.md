# Fase 2: Creación de la Base de Conocimiento RAG

---

En este notebook construiremos la **base de datos vectorial** que usará el agente de IA para responder preguntas frecuentes de clientes.

### ¿Qué es RAG?
**RAG (Retrieval-Augmented Generation)** es una técnica que permite a un modelo de lenguaje (LLM) buscar información relevante en una base de datos propia *antes* de responder. Así el agente:
- ✅ Responde con datos reales de la empresa (no inventa)
- ✅ Puede actualizarse sin reentrenar el modelo
- ✅ Funciona 100% en local (los datos no salen del ordenador)

### Flujo de esta fase:
```
Carga  →  Fragmentación  →  Embeddings  →  ChromaDB
(loader)   (chunking)       (vectores)     (BBDD local)
```

---

### 📋 Requisitos previos
- Python 3.10+
- Entorno virtual activo (`.venv`)
- Conexión a internet (solo para descargar el modelo de embeddings la primera vez)

---
## Paso 1 — Instalación de librerías

Instalamos todos los paquetes necesarios. Solo hay que ejecutar esto **una vez** por entorno.

| Librería | Para qué sirve |
|---|---|
| `langchain` | Framework orquestador del agente |
| `langchain-chroma` | Conector con ChromaDB |
| `langchain-huggingface` | Conector con modelos de HuggingFace |
| `langchain-text-splitters` | Herramienta para fragmentar texto |
| `sentence-transformers` | Motor de embeddings local (sin GPU) |

---
## Paso 2 — Cargar el documento con LangChain

Usamos `TextLoader` para leer el archivo `faqs.txt` y convertirlo en un objeto `Document` que LangChain puede procesar.

> 💡 LangChain tiene loaders para PDF, Word, páginas web, YouTube, bases de datos, etc.
> ⚠️ **Importante:** El archivo se encontrará en la misma carpeta que este notebook.

---
## Paso 3 — Fragmentar el texto (Chunking)

Dividimos el documento en **fragmentos pequeños (chunks)**. Esto es crucial para que la búsqueda sea precisa.

### ¿Por qué fragmentar?
Imagina que el agente busca información sobre devoluciones. Si pasáramos todo el documento, habría mucho "ruido". Fragmentando, recuperamos solo los párrafos exactos que hablan de devoluciones.

### Parámetros importantes:
- **`chunk_size=300`**: Cada fragmento tendrá ~300 caracteres (una idea completa)
- **`chunk_overlap=60`**: Los fragmentos se solapan 60 caracteres para no perder contexto entre trozos

---
## Paso 4 — Cargar el modelo de Embeddings (Vectorización del texto)

Los **embeddings** convierten el texto en vectores numéricos. Textos con significados similares producirán vectores parecidos, lo que permite la búsqueda semántica.

### Modelo elegido: `paraphrase-multilingual-MiniLM-L12-v2`
- ✅ **Multilingüe**: Funciona perfectamente en español
- ✅ **Ligero**: No necesita GPU potente (~130MB)
- ✅ **Local**: Una vez descargado, no necesita internet
- ✅ **Preciso**: Entiende sinónimos y variaciones del lenguaje

> ⏳ **Primera ejecución:** el modelo se descargará automáticamente (~130 MB). Las siguientes ejecuciones serán instantáneas.

---
## Paso 5 — Crear la Base de Datos Vectorial con ChromaDB

**ChromaDB** es nuestra base de datos vectorial. Almacena todos los fragmentos del documento junto con sus vectores, y permite hacer búsquedas semánticas ultra-rápidas.

### ¿Qué hace `from_documents`?
1. Toma cada `chunk` de texto
2. Le aplica el modelo de embeddings para obtener su vector
3. Guarda el par (texto + vector) en la base de datos
4. Persiste todo en la carpeta `./chroma_db` del disco

> ⚠️ Si ya existe una base de datos (segunda ejecución), la celda de limpieza de abajo borrará la anterior para crearla de nuevo.

---
## Paso 6 — Verificación y Prueba de la Base de Datos

¡La base de datos está lista! Vamos a probarla haciendo **búsquedas semánticas** para verificar que funciona correctamente.

Fíjate que las búsquedas funcionan aunque las palabras no coincidan exactamente con el texto del documento. Eso es el poder de los embeddings 🧠

---
## Paso 7 — Cómo cargar la base de datos existente (para el Agente)

El agente de triaje (Fase 3) no necesita recrear la base de datos. Simplemente la **carga desde disco**. Así es como se hace:

---
## 📊 Resumen de la Fase 2

| Paso | Acción | Resultado |
|------|--------|----------|
| 1 | Instalación de librerías | Entorno listo |
| 2 | Carga del documento `faqs.txt`| 1 documento LangChain |
| 4 | Fragmentación (chunking) | ~15 fragmentos de ~300 chars |
| 4 | Modelo de embeddings | `MiniLM-L12-v2` multilingüe cargado |
| 5 | Creación de ChromaDB | Carpeta `./chroma_db` en disco |
| 6 | Verificación | Búsquedas semánticas correctas |
| 7 | Carga desde disco | Método para el Agente (Fase 3) |

---

### 🔜 Siguiente paso: Fase 3 — El Cerebro del Agente
Con la base de datos lista, el siguiente notebook conectará:
- 🗄️ **Esta ChromaDB** (el conocimiento de TechPyme)
- 🤖 **Ollama/LLaMA3** (la IA local que razona)
- 📬 **correos.json** (los emails de clientes a procesar)

Para lanzar el agente completo ver el notebook de Fase 3.
