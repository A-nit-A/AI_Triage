# AUTOMATIZACIONES USANDO AGENTES DE IA

**El Agente de "Triaje" para Atención al Cliente (E-commerce o Clínica)**

El problema: Una pequeña tienda online o clínica recibe decenas de correos y mensajes de WhatsApp al día. El dueño pierde 2 horas diarias respondiendo dudas básicas o derivando mensajes al departamento correcto.
La misión del Agente: Actuar como el primer filtro inteligente.

**Trigger** (Disparador): Entra un nuevo correo electrónico.

Herramientas del Agente: 
- Lector de correo 
- Acceso a una base de datos de FAQs (RAG)
- Conexión al sistema de tickets.

**Flujo de decisión**

1. Lee el correo y determina la intención (Ej: "¿Dónde está mi pedido?", "Quiero hacer una devolución", "Colaboración de marketing").

2. Si es una duda frecuente (ej. horarios, políticas de envío), el agente redacta y envía la respuesta usando la base de conocimiento.

3. Si es un problema complejo (ej. producto defectuoso), etiqueta el correo como "Urgente - Soporte" y notifica al encargado humano con un resumen del problema.


## TUTORIAL - APUNTES - GUIA - DOCUMENTACIÓN

¡Excelente elección! El caso del Agente de Triaje es ideal porque muestra un problema muy evidente y su solución tiene un efecto "wow" inmediato. Además, hacerlo con una IA local y RAG (Generación Aumentada por Recuperación) eleva el nivel técnico de la clase y enseña sobre privacidad de datos (ya que la información de la empresa no sale del ordenador).

Para asegurar el éxito en un entorno de aula, te recomiendo encarecidamente simular la entrada de correos. Configurar conexiones reales a Gmail o Outlook por IMAP en clase suele dar muchos problemas por las contraseñas de aplicación y la verificación en dos pasos. Es mejor que el agente lea "correos" desde un archivo JSON o una carpeta local.

Aquí tienes la hoja de ruta paso a paso para montar el ejemplo con tus alumnos:
Fase 1: Preparación del Entorno Local (El motor de la IA)

El primer paso es que los alumnos instalen el modelo que correrá en sus propios ordenadores.

    Instalar Ollama: Es la herramienta más sencilla para correr modelos locales. Los alumnos deben descargarla de su web oficial e instalarla (disponible para Windows, Mac y Linux).

    Descargar el Modelo LLM: Abrir la terminal y ejecutar un modelo ligero pero capaz. Para ordenadores de estudiantes, recomiendo llama3 o mistral (necesitarán unos 8GB de RAM). El comando sería: ollama run llama3.

    Instalar librerías de Python: En su entorno virtual, deberán instalar el ecosistema que conectará Python con Ollama y gestionará el RAG.

        pip install langchain langchain-community chromadb sentence-transformers

Fase 2: Creación de la Base de Conocimiento (RAG)

Aquí el agente aprenderá sobre la empresa para poder responder.

    El Documento Fuente: Crear un archivo de texto (faqs.txt) con las políticas de la empresa ficticia (ej. "Los envíos tardan 48h", "Se aceptan devoluciones en los primeros 14 días", "Nuestro horario es de 9:00 a 18:00").

    Carga y Fragmentación (Chunking): Usar LangChain para leer el archivo y dividirlo en fragmentos pequeños (chunks) que la IA pueda procesar fácilmente.

    Embeddings Locales: Usar sentence-transformers (modelos de HuggingFace que corren en local) para convertir esos fragmentos de texto en vectores matemáticos.

    Base de Datos Vectorial: Guardar esos vectores en ChromaDB (una base de datos que se ejecuta localmente en la misma carpeta del proyecto) para que la IA pueda buscar en ellos más tarde.

Fase 3: La Lógica del Agente (El Cerebro)

Este es el núcleo de la clase. El script de Python deberá tomar decisiones basándose en el "correo" entrante.

    El Prompt del Sistema (System Prompt): Definir el comportamiento del agente. Por ejemplo: "Eres un asistente de atención al cliente. Tu trabajo es leer el correo del cliente y buscar la respuesta en el contexto proporcionado. Si la respuesta no está en el contexto, o si el cliente está enfadado, debes clasificar el correo como 'ESCALAR_A_HUMANO' y no inventar nada."

    La Cadena de Ejecución (Chain): Construir la secuencia en LangChain:

        Recibir el correo del cliente.

        Buscar en ChromaDB los párrafos de faqs.txt que más se parezcan a la duda del cliente.

        Pasarle al LLM local (Ollama) el correo del cliente y los párrafos encontrados.

Fase 4: Bucle de Automatización (El Trigger)

Poner a trabajar al agente de forma continua.

    Entrada de Datos: Crear un archivo correos_entrantes.json con 3 o 4 casos de prueba:

        Un correo fácil (pregunta por el horario).

        Un correo sobre un envío (pregunta por devoluciones).

        Un correo complejo/queja (producto roto, que debería ser escalado).

    El Bucle (Loop): Un script en Python que lea el JSON, pase cada correo por la cadena del Agente (Fase 3), e imprima por pantalla el resultado: la respuesta redactada para el cliente o la etiqueta de "ESCALAR_A_HUMANO".

## PROYECTO EJEMPLO

### FASE 2 - RAG

Aquí tienes todo lo necesario para ejecutar la Fase 2. He optimizado el código utilizando las librerías más actualizadas y un modelo de embeddings (transformador de texto a vectores) ligero que funciona muy bien en español.
1. Preparar las librerías necesarias

Asegúrate de que tus alumnos instalan estos paquetes en su entorno virtual. En su terminal, deben ejecutar:
Bash

pip install langchain langchain-chroma langchain-huggingface langchain-text-splitters sentence-transformers

2. Crear el archivo de texto (La "memoria" de la empresa)

Diles a los alumnos que creen un archivo llamado faqs.txt en la misma carpeta donde pondrán su script de Python. Dentro de este archivo, que peguen el siguiente texto de ejemplo:
Plaintext

Nuestra tienda online se llama "TechPyme".
El horario de atención al cliente es de lunes a viernes, de 9:00 a 18:00 horas.
Los envíos estándar tardan entre 48 y 72 horas laborables en llegar a la península. No hacemos envíos a las islas.
El coste del envío estándar es de 4,99 euros. Los envíos son gratis para pedidos superiores a 50 euros.
Aceptamos devoluciones durante los primeros 14 días tras la recepción del pedido.
Para procesar una devolución, el artículo debe estar en su embalaje original y sin usar.
Si un cliente recibe un producto defectuoso o roto, debe contactarnos inmediatamente y nosotros asumimos los gastos de envío de la devolución.
No ofrecemos soporte técnico para productos que no hayan sido comprados directamente en nuestra tienda.

3. El código Python: Creación de la Base de Datos RAG

Ahora, pídeles que creen un archivo llamado crear_rag.py y peguen este código. Lo he comentado detalladamente para que puedas explicarlo línea a línea en clase:
Python

import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def montar_base_conocimiento():
    print("1. Cargando el documento de FAQs...")
    # Usamos utf-8 para no tener problemas con acentos en español
    loader = TextLoader("faqs.txt", encoding="utf-8")
    documentos = loader.load()

    print("2. Dividiendo el texto en fragmentos (chunks)...")
    # Rompemos el texto en trozos pequeños para que la búsqueda sea precisa
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,    # Cada trozo tendrá unos 200 caracteres
        chunk_overlap=50   # Solapamos 50 caracteres para no perder contexto entre trozos
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"   -> Documento dividido en {len(chunks)} fragmentos.")

    print("3. Descargando/Cargando el modelo de Embeddings local...")
    # Usamos un modelo ligero multilingüe de HuggingFace (ideal para español y ordenadores sin GPU potente)
    embeddings_model = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

    print("4. Creando la base de datos vectorial Chroma...")
    # Carpeta donde se guardará la base de datos en el disco duro
    directorio_db = "./chroma_db" 
    
    # Creamos la base de datos y le insertamos los fragmentos ya vectorizados
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=directorio_db
    )

    print(f"¡Éxito! Base de conocimiento creada y guardada en la carpeta '{directorio_db}'.")

if __name__ == "__main__":
    montar_base_conocimiento()

¿Qué sucederá al ejecutar esto?

Cuando tus alumnos ejecuten python crear_rag.py por primera vez:

    El script descargará automáticamente el modelo de embeddings (pesa muy poco, unos cientos de megabytes).

    Leerá el archivo faqs.txt.

    Creará una nueva carpeta en su proyecto llamada chroma_db. ¡Esta carpeta es su base de datos local!

Una vez ejecutado este paso, el conocimiento de la empresa ya está estructurado y listo para ser consultado.

### FASE 3 Y 4

Antes de ejecutar este código, recuérdales que Ollama debe estar abierto y ejecutándose en segundo plano (pueden probar abriendo su terminal y escribiendo ollama run llama3 para asegurarse de que el modelo está descargado y listo).

Aquí tienes los pasos finales para completar la automatización:
1. Actualizar librerías (Importante)

Para conectar LangChain con Ollama de la forma más moderna y estable, pídeles que instalen este paquete adicional en su terminal:
Bash

pip install langchain-ollama

2. Crear los "Correos Simulados"

Para no complicar la clase con conexiones reales a Gmail, vamos a simular la bandeja de entrada. Que creen un archivo llamado correos.json en la misma carpeta con este contenido:
JSON

[
  {
    "id": 1,
    "remitente": "carlos@email.com",
    "asunto": "Duda sobre el envío",
    "cuerpo": "Hola, hice un pedido ayer de 60 euros. ¿Cuánto tardará en llegar a Madrid y cuánto cuesta el envío? Gracias."
  },
  {
    "id": 2,
    "remitente": "laura@email.com",
    "asunto": "Producto roto",
    "cuerpo": "¡Estoy indignada! Me acaba de llegar el paquete y el cristal está completamente destrozado. Exijo una solución inmediata o pondré una reclamación."
  },
  {
    "id": 3,
    "remitente": "pedro@email.com",
    "asunto": "Problema técnico",
    "cuerpo": "Buenas tardes, compré este router en Amazon hace un mes y no logro configurarlo. ¿Me podéis dar soporte técnico?"
  }
]

3. El Cerebro del Agente (Fases 3 y 4)

Ahora, que creen un archivo llamado agente_triaje.py y peguen el siguiente código. Este script une la base de datos que creamos antes, el modelo local de IA, y el bucle que lee los correos:
Python

import json
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def iniciar_agente():
    print("1. Conectando con la base de conocimiento local...")
    embeddings_model = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings_model)
    
    # Configuramos el "recuperador" para que traiga los 2 fragmentos más relevantes
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    print("2. Despertando a la IA local (Ollama)...")
    # Usamos llama3 (o el modelo que hayan descargado). Temperature=0 para que sea preciso y no invente.
    llm = ChatOllama(model="llama3", temperature=0)

    print("3. Configurando las instrucciones del Agente (System Prompt)...")
    instrucciones = """
    Eres un asistente de atención al cliente de la tienda TechPyme. 
    Tu objetivo es leer el correo del cliente y responder basándote ÚNICAMENTE en el siguiente contexto de la empresa:
    
    <contexto>
    {context}
    </contexto>
    
    REGLAS ESTRICTAS:
    1. Si el cliente está muy enfadado o tiene un producto roto, responde EXACTAMENTE con la palabra: ESCALAR_A_HUMANO.
    2. Si la respuesta no está en el contexto, responde EXACTAMENTE con la palabra: ESCALAR_A_HUMANO.
    3. Si puedes responder con el contexto, redacta un correo amable, profesional y conciso respondiendo a su duda.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", instrucciones),
        ("human", "Asunto: {asunto}\nMensaje: {mensaje}")
    ])

    # Unimos el LLM, el Prompt y el Recuperador de información (RAG)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    print("4. Iniciando bandeja de entrada...\n")
    print("-" * 50)
    
    # Leemos el archivo JSON simulando que nos conectamos a un servidor de correo
    with open('correos.json', 'r', encoding='utf-8') as f:
        correos = json.load(f)

    # Bucle de automatización (El Agente trabajando)
    for correo in correos:
        print(f"📥 Procesando correo de: {correo['remitente']}")
        print(f"   Asunto: {correo['asunto']}")
        
        # Le pasamos el asunto y el mensaje a nuestro agente
        respuesta = rag_chain.invoke({
            "asunto": correo["asunto"],
            "mensaje": correo["cuerpo"]
        })
        
        decision_ia = respuesta["answer"].strip()
        
        if "ESCALAR_A_HUMANO" in decision_ia:
            print("   ⚠️ DECISIÓN: Derivado a un agente humano (Etiqueta de urgencia o falta de info).")
        else:
            print("   ✅ DECISIÓN: Respuesta automática generada:")
            print(f"      {decision_ia}")
            
        print("-" * 50)

if __name__ == "__main__":
    iniciar_agente()

El momento de la verdad en clase

Cuando tus alumnos ejecuten python agente_triaje.py, verán cómo la terminal cobra vida.

    Para Carlos, la IA buscará en ChromaDB, verá que los pedidos de más de 50€ son gratis y tardan 48-72h, y le redactará un correo amable.

    Para Laura (producto roto e indignada), la IA detectará el problema según sus reglas y dirá ESCALAR_A_HUMANO.

    Para Pedro (soporte técnico externo), la IA verá en el contexto que no dan soporte a productos de Amazon, y aplicará la regla correspondiente.


## PROPUESTA DE EJERCICIO

🏆 El Reto Final: "Creando el Registro de Urgencias"

El Escenario (Para plantear a los alumnos):

    "Vuestro Agente de Triaje funciona de maravilla, pero hay un problema: cuando decide 'ESCALAR_A_HUMANO', simplemente lo imprime por pantalla y el correo se pierde. El equipo humano de atención al cliente necesita que todos esos correos problemáticos (quejas, roturas, dudas no resueltas) se guarden automáticamente en un archivo Excel/CSV para revisarlos a primera hora de la mañana."

La Misión:
Modificar el script agente_triaje.py para que, cuando la decisión de la IA sea ESCALAR_A_HUMANO, el programa cree (o actualice) un archivo llamado correos_escalados.csv y guarde en él: el remitente, el asunto y el cuerpo del mensaje.

Pistas (Para darles si se atascan):

    Necesitarán importar la librería nativa de Python para manejar CSVs: import csv.

    Deben usar la función open() con el modo 'a' (Append / Añadir) para que los correos nuevos se sumen al final del archivo sin borrar los anteriores.

    El código debe ir justo debajo del if "ESCALAR_A_HUMANO" in decision_ia:.

👨‍🏫 La Solución (Para el profesor)

Los alumnos solo tendrán que añadir unas 5 líneas de código a su script actual. Así es como debe quedar la parte final del código (he resaltado los cambios):

1. Al principio del archivo agente_triaje.py, deben añadir el import:
Python

import json
import csv  # <-- ¡NUEVO IMPORT!
from langchain_chroma import Chroma
# ... (resto de imports)

2. En la parte final del bucle (donde se toma la decisión), el código debe quedar así:
Python

        # ... (código anterior donde se invoca a la IA)
        decision_ia = respuesta["answer"].strip()
        
        if "ESCALAR_A_HUMANO" in decision_ia:
            print("   ⚠️ DECISIÓN: Derivado a un agente humano.")
            print("   💾 Guardando registro en CSV para el equipo de soporte...")
            
            # --- INICIO DE LA SOLUCIÓN DEL RETO ---
            with open('correos_escalados.csv', mode='a', newline='', encoding='utf-8') as archivo_csv:
                escritor = csv.writer(archivo_csv)
                # Guardamos: Remitente, Asunto, Mensaje Original
                escritor.writerow([correo['remitente'], correo['asunto'], correo['cuerpo']])
            # --- FIN DE LA SOLUCIÓN ---
            
        else:
            print("   ✅ DECISIÓN: Respuesta automática generada:")
            print(f"      {decision_ia}")
            
        print("-" * 50)

¿Por qué este reto es tan valioso didácticamente?

    Simula una "Herramienta" (Tool Use): En el mundo real de los Agentes IA (con frameworks avanzados como LangChain Tools o CrewAI), los agentes tienen "manos" para escribir en bases de datos, enviar mensajes por Slack o crear tickets en Jira. Escribir en un CSV es la versión simplificada y perfecta para entender este concepto.

    Cierra el ciclo del caso de uso: Demuestra que la IA no viene a reemplazar al humano, sino a quitarle el trabajo repetitivo (correos de envíos/horarios) y a organizarle el trabajo importante (dejándole un Excel limpito con los clientes que de verdad necesitan su atención).

Con esto tienes una clase súper completa: instalación local, vectorización de datos (RAG), toma de decisiones (LLM) y ejecución de acciones (CSV).
