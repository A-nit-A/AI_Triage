# =======================================================
# rag.py
# Construcción de la Base de Conocimiento RAG — TechPyme
# =======================================================


"""
Lee un fichero de texto (FAQs), lo divide en fragmentos, los vectoriza con un
modelo de embeddings de HuggingFace y persiste la base de datos vectorial en
la carpeta chroma_db/. También guarda el nombre del modelo usado en
chroma_db/embedding_model.txt para que agent.py pueda cargarlo automáticamente.

Requisitos previos
------------------
1. Fichero de texto con los documentos a indexar (por defecto: faqs.txt)
2. Conexión a internet en la primera ejecución para descargar el modelo de embeddings

Uso
---
    python rag.py                                # usa faqs.txt y el modelo por defecto
    python rag.py -f ruta/al/fichero.txt         # fichero alternativo
    python rag.py -m nombre-del-modelo           # modelo de embeddings alternativo
    python rag.py -f docs.txt -m all-MiniLM-L6-v2
"""

import os
import sys
import shutil
import argparse

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Obtener la ruta del fichero
def obtener_ruta_fichero() -> str | None:
    """
    Solicita al usuario la ruta de un fichero hasta que éste exista,
    o devuelve None si el usuario decide finalizar la ejecución.
    """
    while True:
        ruta = input(
            "El fichero no existe. Introduce la ruta del fichero a cargar "
            "(o pulsa Enter para salir): "
        ).strip()

        if ruta == "":
            print("Saliendo de la aplicación.")
            return None

        if os.path.isfile(ruta):
            return ruta

        print(f"⚠️  El fichero '{ruta}' tampoco existe. Inténtalo de nuevo.")

# Cargar el documento
def cargar_documento(ruta_fichero):
    print("Cargando el documento de FAQs: {ruta_fichero}")

    # Usamos utf-8 para no tener problemas con acentos y caracteres especiales en español
    loader = TextLoader(ruta_fichero, encoding="utf-8")
    documentos = loader.load()

    print(f"Documento cargado. Número de documentos: {len(documentos)}")
    return documentos
    
# Fragmentar el texto en chunks
def chunking_text(documentos):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,    # Cada fragmento tendrá ~300 chunks
        chunk_overlap=60,  # Solapamos 60 chunks para no perder contexto
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]  # Prioridad de separación
    )

    chunks = text_splitter.split_documents(documentos)

    print(f"Documento dividido en {len(chunks)} fragmentos.")
    print()
    return chunks

# Cargar el modelo de Embeddings
def load_embeddings_model(model_name):
#    if model_name is None:
#       model_name = "paraphrase-multilingual-MiniLM-L12-v2"

    print("Cargando el modelo de Embeddings (puede tardar en la primera ejecución)...")
    print(f"Modelo: {model_name}")
    print()

    try:
        print("Cargando el modelo de embeddings...")
        embeddings_model = HuggingFaceEmbeddings(model_name=model_name)

        print("Comprobando el modelo de embeddings...")
        texto_prueba = "¿Cuánto tarda el envío?"
        vector_prueba = embeddings_model.embed_query(texto_prueba)

        return embeddings_model

    except Exception as e:
        print(f"Error al cargar o verificar el modelo de embeddings: {e}")
        return None

# Obtener un modelo alternativo si el anterior falla
def obtener_modelo(model_name_fallido: str) -> str | None:
    """
    Solicita al usuario un modelo alternativo si el anterior falló.
    Devuelve el nuevo nombre, o None si el usuario decide salir.
    """
    while True:
        nuevo_modelo = input(
            f"El modelo '{model_name_fallido}' no pudo cargarse.\n"
            "Introduce el nombre de otro modelo de HuggingFace "
            "(o pulsa Enter para salir): "
        ).strip()

        if nuevo_modelo == "":
            print("Saliendo de la aplicación.")
            return None

        return nuevo_modelo

# Crear la base de datos
def crear_base_datos(chunks, embeddings_model, model_name, script_dir=None):
    # Directorio donde se persistirá la base de datos
    base = script_dir if script_dir else os.path.dirname(os.path.abspath(__file__))
    DIRECTORIO_DB = os.path.join(base, "chroma_db")

    # Si ya existe una base de datos previa, la eliminamos para empezar limpio
    if os.path.exists(DIRECTORIO_DB):
        shutil.rmtree(DIRECTORIO_DB)
        print(f"Base de datos anterior eliminada (para regenerarla limpia).")

    print(f"")
    print(f"Creando base de datos y vectorizando {len(chunks)} fragmentos...")
    print(f"(Esto puede tardar 1-2 minutos dependiendo del hardware)")

    try:
        # Creamos la base de datos vectorial Chroma con todos los fragmentos
        vectorstore = Chroma.from_documents(
            documents=chunks,              # Los fragmentos de texto
            embedding=embeddings_model,    # El modelo que los convierte en vectores
            persist_directory=DIRECTORIO_DB  # La carpeta donde se guardará en disco
        )

        print(f"")
        print(f"Base de conocimiento creada y guardada en la carpeta '{DIRECTORIO_DB}'.")
        print(f"Fragmentos indexados: {vectorstore._collection.count()}")

        # Guardamos el nombre del modelo de embeddings para que agent.py pueda cargarlo
        modelo_txt = os.path.join(DIRECTORIO_DB, "embedding_model.txt")
        with open(modelo_txt, "w", encoding="utf-8") as f:
            f.write(model_name)
        print(f"Modelo de embeddings guardado en '{modelo_txt}'.")

        # Verificamos que la carpeta existe en disco
        if os.path.exists(DIRECTORIO_DB):
            archivos = os.listdir(DIRECTORIO_DB)
            print(f"Archivos en disco: {archivos}")

        return vectorstore

    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
        return None

def main():

    # Parseo de argumentos
    parser = argparse.ArgumentParser(
        prog="rag.py",
        description="Sistema RAG: indexa un documento y crea la base de datos vectorial para usar con el ajente.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-f", "--fichero",
        default="faqs.txt",
        metavar="RUTA",
        help="Ruta al fichero de texto con los documentos a indexar\n(por defecto: faqs.txt)"
    )
    parser.add_argument(
        "-m", "--modelo",
        default="paraphrase-multilingual-MiniLM-L12-v2",
        metavar="NOMBRE",
        help="Nombre del modelo de embeddings de HuggingFace\n(por defecto: paraphrase-multilingual-MiniLM-L12-v2)"
    )
    args = parser.parse_args()

    script_dir   = os.path.dirname(os.path.abspath(__file__))
    ruta_fichero = os.path.join(script_dir, args.fichero)
    model_name   = args.modelo
    print(f"Ruta del fichero: {ruta_fichero}")
    print(f"Modelo: {model_name}")
    print() 

    # Comprobación de existencia del fichero
    if not os.path.isfile(ruta_fichero):
        print(f"El fichero '{ruta_fichero}' no existe.")
        ruta_fichero = obtener_ruta_fichero()

        if ruta_fichero is None:
            sys.exit(0)

    # Cargar el documento
    documentos = cargar_documento(ruta_fichero)

    # Fragmentar el texto en chunks
    chunks = chunking_text(documentos)

    # Cargar el modelo de embeddings y verificar que funciona
    embeddings_model = load_embeddings_model(model_name)

    # Si el modelo falla, pedimos otro
    while embeddings_model is None:
        model_name = obtener_modelo(model_name)
        if model_name is None:
            sys.exit(1)
        embeddings_model = load_embeddings_model(model_name)
    
    print(f"Modelo '{model_name}' listo.")

    # Crear la base de datos
    vectorstore = crear_base_datos(chunks, embeddings_model, model_name, script_dir)

    if vectorstore is None:
        sys.exit(2)

    print("Base de datos creada exitosamente.")
    print("Base de datos lista para usarse por parte del ajente.")


if __name__ == "__main__":
    main()