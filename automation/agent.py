# agent.py
# Agente de Triaje de Emails — TechPyme
# =======================================

"""
Requisitos previos
------------------
1. Ollama instalado y ejecutándose:  ollama serve
2. Modelo descargado:                ollama pull llama3
3. Base de datos ChromaDB creada:    python rag.py   (genera Project/chroma_db/)
4. Fichero de correos:               correos.json    (en el mismo directorio que agent.py)

Uso
---
    python agent.py                             # usa correos.json y llama3 por defecto
    python agent.py --correos ruta.json          # fichero de correos alternativo
    python agent.py --modelo mistral             # modelo Ollama alternativo
    python agent.py --prompt mi_prompt.txt       # system prompt alternativo
    python agent.py -c correos.json -m llama3.2 -p prompt.txt  # combinando opciones
"""

import os
import sys
import csv
import json
import time
import subprocess
import argparse
from datetime import datetime

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ─────────────────────────────────────────────────────────────────
#  Constantes
# ─────────────────────────────────────────────────────────────────
SCRIPT_DIR        = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_DB     = os.path.join(SCRIPT_DIR, "chroma_db")
MODELO            = "llama3"
EMBEDDING_MODEL      = "paraphrase-multilingual-MiniLM-L12-v2"
ARCHIVO_ESCALADOS    = os.path.join(SCRIPT_DIR, "correos_escalados.csv")
ARCHIVO_RESPONDIDOS  = os.path.join(SCRIPT_DIR, "correos_respondidos.csv")
CORREOS_JSON         = os.path.join(SCRIPT_DIR, "correos.json")
SYSTEM_PROMPT_FILE   = os.path.join(SCRIPT_DIR, "system_prompt.txt")




# ─────────────────────────────────────────────────────────────────
#  Paso 1 — Verificar que Ollama está activo
# ─────────────────────────────────────────────────────────────────
def verificar_ollama() -> None:
    print("Verificando Ollama...")
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print("Ollama está activo.")
            print("   Modelos disponibles:")
            for line in result.stdout.strip().split("\n"):
                print(f"   {line}")
        else:
            print("Ollama no responde. Ábre una terminal y ejecuta: ollama serve")
            sys.exit(1)
    except FileNotFoundError:
        print("Ollama no está instalado. Descárgalo en: https://ollama.ai")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Timeout al contactar Ollama. Asegúrate de que está ejecutándose en segundo plano.")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────────
#  Paso 2 — Cargar el fichero de correos
# ─────────────────────────────────────────────────────────────────
def cargar_correos(ruta_json: str) -> list[dict]:
    """Carga y devuelve la lista de correos desde el JSON indicado."""
    if not os.path.exists(ruta_json):
        raise FileNotFoundError(
            f"No se encontró el fichero de correos '{ruta_json}'.\n"
            "Coloca correos.json en el mismo directorio que agent.py."
        )
    with open(ruta_json, "r", encoding="utf-8") as f:
        correos = json.load(f)
    print(f"Cargados {len(correos)} correos desde '{ruta_json}'.")
    return correos


# ─────────────────────────────────────────────────────────────────
#  Paso 2b — Cargar el System Prompt desde fichero
# ─────────────────────────────────────────────────────────────────
def cargar_system_prompt(ruta: str) -> str:
    """Lee el system prompt desde un fichero de texto y lo devuelve como cadena."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(
            f"No se encontró el fichero de system prompt '{ruta}'.\n"
            "Crea el fichero o especifica uno con --prompt."
        )
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
    print(f"System Prompt cargado desde '{ruta}'.")
    return contenido


# ─────────────────────────────────────────────────────────────────
#  Paso 3 — Conectar con la base de conocimiento RAG (ChromaDB)
# ─────────────────────────────────────────────────────────────────
def cargar_rag(modelo: str = MODELO, prompt_file: str = SYSTEM_PROMPT_FILE):
    """Devuelve una tupla (retriever, cadena_rag)."""

    # ── 3a. Embeddings ──────────────────────────────────────────
    if not os.path.exists(DIRECTORIO_DB):
        raise FileNotFoundError(
            f"No se encontró la base de datos en '{DIRECTORIO_DB}'.\n"
            "Ejecuta primero:  python rag.py"
        )

    print("Cargando modelo de embeddings...")
    modelo_txt = os.path.join(DIRECTORIO_DB, "embedding_model.txt")
    if os.path.exists(modelo_txt):
        with open(modelo_txt, "r", encoding="utf-8") as f:
            embedding_model_name = f.read().strip()
        print(f"Modelo de embeddings leído de la base de datos: '{embedding_model_name}'")
    else:
        embedding_model_name = EMBEDDING_MODEL
        print(f"Aviso: no se encontró '{modelo_txt}'. Usando modelo por defecto: '{embedding_model_name}'")
    embeddings_model = HuggingFaceEmbeddings(model_name=embedding_model_name)

    print("Conectando con la base de conocimiento RAG...")
    vectorstore = Chroma(
        persist_directory=DIRECTORIO_DB,
        embedding_function=embeddings_model
    )
    # k=2 significa que recuperará los 2 fragmentos más relevantes
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    print(f"Base de conocimiento cargada. Fragmentos disponibles: {vectorstore._collection.count()}")

    # ── 3b. LLM ─────────────────────────────────────────────────
    print(f"Despertando a la IA local (Ollama / {modelo})...")
    llm = ChatOllama(model=modelo, temperature=0)
    respuesta_test = llm.invoke("Di solo 'OK' en español.")
    print(f"Modelo '{modelo}' activo. Respuesta de prueba: '{respuesta_test.content.strip()}'")

    # ── 3c. Prompt ───────────────────────────────────────────────
    instrucciones_agente = cargar_system_prompt(prompt_file)

    prompt = ChatPromptTemplate.from_messages([
        ("system", instrucciones_agente),
        ("human", "Asunto del correo: {asunto}\n\nMensaje del cliente:\n{mensaje}")
    ])
    print("System Prompt configurado.")


    # ── 3d. Cadena RAG (LCEL) ────────────────────────────────────
    def formatear_docs(docs):
        result = "\n\n".join(doc.page_content for doc in docs)
        # print("Context: ", result)
        return result

    rag_chain = (
        {
            "context": (lambda x: x["mensaje"]) | retriever | formatear_docs,
            "asunto":  RunnablePassthrough() | (lambda x: x["asunto"]),
            "mensaje": RunnablePassthrough() | (lambda x: x["mensaje"])
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    print("Cadena RAG construida. El agente está listo.")
    print(f"correo  →  [ChromaDB retriever]  →  [{modelo}]  →  decisión\n")
    return rag_chain


# ─────────────────────────────────────────────────────────────────
#  Paso 4 — Bucle de triaje
# ─────────────────────────────────────────────────────────────────
def ejecutar_triaje(correos: list[dict], rag_chain) -> None:
    """Procesa cada correo y graba escalados y respondidos en sus respectivos CSV."""

    # Crear los CSV con cabecera si no existen
    if not os.path.exists(ARCHIVO_ESCALADOS):
        with open(ARCHIVO_ESCALADOS, mode="w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["timestamp", "id", "remitente", "asunto", "cuerpo", "motivo"])
        print(f"Creado archivo '{ARCHIVO_ESCALADOS}' con cabecera.")

    if not os.path.exists(ARCHIVO_RESPONDIDOS):
        with open(ARCHIVO_RESPONDIDOS, mode="w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["timestamp", "id", "remitente", "asunto", "cuerpo", "respuesta"])
        print(f"Creado archivo '{ARCHIVO_RESPONDIDOS}' con cabecera.")

    print(f"Procesando {len(correos)} correos entrantes...")
    print("=" * 60)

    for correo in correos:
        print(f"\nCorreo #{correo['id']} | De: {correo['remitente']}")
        print(f"Asunto: {correo['asunto']}")
        print(f"   Procesando...", end=" ", flush=True)

        decision_ia = rag_chain.invoke({
            "asunto":  correo["asunto"],
            "mensaje": correo["cuerpo"]
        }).strip()

        if "ESCALAR_A_HUMANO" in decision_ia:
            print("Atención!")
            print("DECISIÓN: Derivado a agente humano.")
            print(f"Guardando en {ARCHIVO_ESCALADOS}...")
            with open(ARCHIVO_ESCALADOS, mode="a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    correo["id"],
                    correo["remitente"],
                    correo["asunto"],
                    correo["cuerpo"],
                    "Requiere atención humana"
                ])
        else:
            print("Respuesta automática generada:")
            for linea in decision_ia.split("\n"):
                print(f"{linea}")
            with open(ARCHIVO_RESPONDIDOS, mode="a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    correo["id"],
                    correo["remitente"],
                    correo["asunto"],
                    correo["cuerpo"],
                    decision_ia
                ])

        print("-" * 60)

    print("\n Triaje completado.")


# ─────────────────────────────────────────────────────────────────
#  Paso 5 — Mostrar resumen de los CSV de resultados
# ─────────────────────────────────────────────────────────────────
def _mostrar_csv(ruta: str, etiqueta: str, col_detalle: int) -> None:
    """Imprime un resumen de cualquiera de los dos CSV de resultados."""
    print(f"\n Contenido de '{ruta}':")
    print("=" * 60)
    try:
        with open(ruta, newline="", encoding="utf-8") as f:
            filas = list(csv.reader(f))
        if len(filas) <= 1:
            print(f"   (vacío — ningún correo {etiqueta})")
        else:
            datos = filas[1:]
            print(f"   Correos {etiqueta}: {len(datos)}\n")
            for fila in datos:
                print(f"   Fecha {fila[0]}")
                print(f"   De: {fila[2]}  |  Asunto: {fila[3]}")
                print(f"   {fila[col_detalle][:120]}...")
                print()
    except FileNotFoundError:
        print("   Archivo no encontrado.")


# ─────────────────────────────────────────────────────────────────
#  Punto de entrada
# ─────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agent.py",
        description="Agente de triaje de emails para TechPyme.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-c", "--correos",
        default=CORREOS_JSON,
        metavar="RUTA",
        help=f"Ruta al fichero JSON con los correos a procesar\n(por defecto: {CORREOS_JSON})"
    )
    parser.add_argument(
        "-m", "--modelo",
        default=MODELO,
        metavar="NOMBRE",
        help=f"Modelo Ollama a usar como LLM\n(por defecto: {MODELO})"
    )
    parser.add_argument(
        "-p", "--prompt",
        default=SYSTEM_PROMPT_FILE,
        metavar="RUTA",
        help=f"Ruta al fichero de texto con el system prompt\n(por defecto: {SYSTEM_PROMPT_FILE})"
    )
    args = parser.parse_args()

    verificar_ollama()
    rag_chain = cargar_rag(modelo=args.modelo, prompt_file=args.prompt)
    
    print("\nIniciando monitorización cada 10 segundos... (Presiona Ctrl+C para detener)")
    try:
        while True:
            try:
                correos = cargar_correos(args.correos)
                if correos:
                    ejecutar_triaje(correos, rag_chain)
                    os.remove(args.correos)
                    print(f"\n[INFO] Archivo '{args.correos}' eliminado exitosamente tras ser procesado.")
            except FileNotFoundError:
                pass # Silenciar el FileNotFoundError para no llenar la terminal cada 10 seg
            
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nMonitorización detenida por el usuario.")

    # Mostrar resultados
    # _mostrar_csv(ARCHIVO_ESCALADOS, "escalados", 5)
    # _mostrar_csv(ARCHIVO_RESPONDIDOS, "respondidos", 5) 

if __name__ == "__main__":
    main()
