# RECURSOS OLLAMA

1. La Fuente Oficial (El Estándar de Oro)

Ollama destaca precisamente por tener una curva de aprendizaje mínima. Sus sitios oficiales deben ser siempre la primera parada:

- Sitio web principal: ollama.com

    Por qué usarlo: Tiene el botón de descarga directa para Windows, macOS y Linux.Es literalmente un instalador de "Siguiente > Siguiente".

- El Repositorio de GitHub: github.com/ollama/ollama

        Por qué usarlo: El archivo Readme (la página principal del repositorio) es un tutorial en sí mismo. Muestra los comandos básicos en la terminal (ej. ollama run llama3), cómo gestionar modelos y cómo usar su API local.

- La Biblioteca de Modelos: ollama.com/library

        Por qué usarlo: Aquí los alumnos pueden buscar qué IA quieren instalar (Llama 3, Mistral, Phi-3). Muestra los requisitos de RAM y el comando exacto para descargar cada uno.

2. Plataformas de Tutoriales Escritos (Para seguir a su ritmo)

Para los alumnos que prefieren leer tutoriales paso a paso con capturas de pantalla, estas plataformas son ideales:

    Medium.com (Búsqueda recomendada: "Ollama tutorial español"): * Medium está lleno de artículos de la comunidad tecnológica. Hay excelentes guías que explican no solo la instalación, sino también la integración con Python (que es justo lo que haréis en clase).

    Dev.to (Etiqueta: #ollama):

        Una comunidad fantástica para desarrolladores. Los tutoriales aquí suelen ir más al grano con el código y los posibles errores de instalación que puedan surgir en Windows (especialmente con WSL - Windows Subsystem for Linux, si deciden usarlo).

3. Videotutoriales en YouTube (Ideales para lo visual)

A veces, ver a alguien abriendo la terminal y ejecutando los comandos es la forma más rápida de perderle el miedo. Te recomiendo buscar y filtrar videos de estos perfiles:

    Canales de divulgación IA (Ej. DotCSV o Carlos Santana): Aunque suelen hacer divulgación general, a menudo publican tutoriales sobre cómo correr modelos en local.

    Canales de programación y DevOps (Ej. Pelado Nerd): Son excelentes para explicar qué pasa "por debajo" cuando instalas herramientas en la terminal.

    Término de búsqueda recomendado para tus alumnos: "Cómo instalar Ollama Windows/Mac" o "Primeros pasos con Ollama y Python". Los videos de menos de 10 minutos suelen ser los más efectivos.

Consejos para la instalación en el aula:

- El problema del peso: Los modelos (como llama3) pesan entre 4 y 5 GB. Si tienes a 20 alumnos descargando esto a la vez en la red Wi-Fi del centro, la red puede colapsar. Te sugiero que les pidas que lo traigan descargado de casa el día antes.

- Hardware: Recuérdales que Ollama funciona en CPU, pero irá mucho más rápido si tienen una tarjeta gráfica (GPU) dedicada, o procesadores Apple Silicon (M1/M2/M3) en el caso de Mac.


# GUÍA DE INSTALACIÓN DE OLLAMA

🚀 Guía de Preparación: Instala tu propia IA Local con Ollama

Para nuestra próxima clase sobre Automatización con Agentes de IA, vamos a necesitar que tu ordenador tenga un "cerebro" instalado. Usaremos Ollama, una herramienta que nos permite ejecutar modelos de lenguaje (LLMs) directamente en nuestro equipo, sin depender de internet ni enviar datos a servidores externos.

⚠️ MUY IMPORTANTE: El modelo de IA que vamos a usar pesa unos 4.7 GB. Por favor, haz este proceso en tu casa usando tu conexión Wi-Fi antes del día de la clase. Si todos lo descargamos a la vez en el aula, ¡colapsaremos la red!
Paso 1: Descargar e Instalar Ollama

    Entra en la página oficial: ollama.com/download

    Selecciona tu sistema operativo (Windows, macOS o Linux) y descarga el instalador.

    Ejecuta el archivo descargado. Es una instalación sencilla, solo tienes que darle a "Siguiente" o "Install".

    Sabrás que está instalado porque verás el icono de una llama (el animal) en la barra de tareas (Windows, abajo a la derecha) o en la barra de menús (Mac, arriba a la derecha).

Paso 2: Abrir la Terminal

Ollama no tiene una interfaz gráfica tradicional con botones; se comunica a través de la consola de comandos de tu ordenador.

    En Windows: Pulsa la tecla Windows, escribe cmd o PowerShell y dale a Enter.

    En Mac: Pulsa Cmd + Espacio, escribe Terminal y dale a Enter.

    En Linux: Abre tu emulador de terminal favorito (suele ser Ctrl + Alt + T).

Paso 3: Descargar y Ejecutar el Modelo de IA

Ahora vamos a decirle a Ollama que descargue "Llama 3" (un modelo muy potente creado por Meta). En la terminal que acabas de abrir, escribe el siguiente comando y pulsa Enter:
Bash

ollama run llama3

¿Qué va a pasar ahora?

    Ollama empezará a descargar el modelo. Verás una barra de progreso. Ten paciencia, son varios gigabytes.

    Cuando termine la descarga, verás que el cursor cambia y aparece algo como >>>.

    ¡Felicidades! Ya estás hablando con tu IA local. Escribe "Hola, ¿qué tal?" y comprueba que te responde.

Paso 4: Salir y Preparar el Entorno de Programación

Para salir del chat de la IA y volver a tu terminal normal, simplemente escribe:
Bash

/bye

(Nota: Aunque salgas del chat, Ollama sigue ejecutándose en segundo plano, listo para cuando lo llamemos desde nuestro código en clase).

Por último, asegúrate de tener instalado Python y crea un entorno virtual para el proyecto. Instala las librerías que usaremos ejecutando este comando:
Bash

pip install langchain langchain-chroma langchain-huggingface langchain-ollama langchain-text-splitters sentence-transformers

💡 Plan B: ¿Tu ordenador va muy lento?

Llama 3 requiere unos 8 GB de memoria RAM. Si tu ordenador tiene menos recursos, se queda "congelado" o va extremadamente lento al responder, cierra la terminal, vuelve a abrirla y prueba a descargar un modelo más ligero diseñado para equipos modestos. Usa este comando en su lugar:
Bash

ollama run qwen2.5:1.5b

(Este modelo pesa menos de 1 GB y funciona muy rápido, ideal para aprender los conceptos).