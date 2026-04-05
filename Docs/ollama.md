# OLLAMA

Es una herramienta de código abierto diseñada para ejecutar, administrar e interactuar con Modelos de Lenguaje Grande (LLMs, por sus siglas en inglés) directamente de forma local en tu propio ordenador (Windows, macOS o Linux). 

Básicamente, empaqueta todo lo necesario (los pesos del modelo, la configuración y el motor de ejecución) en una aplicación fácil de usar, eliminando la complejidad técnica que solía requerir instalar este tipo de inteligencias artificiales.

## ¿Para qué sirve?

Ollama sirve para que cualquier usuario o desarrollador pueda tener su propia IA al estilo de ChatGPT funcionando en su máquina, sin depender de la nube. Sus usos principales incluyen:

* **Ejecutar IAs sin internet:** Puedes chatear, generar texto o programar con la ayuda de la IA estando totalmente desconectado de la red.
* **Proteger la privacidad de tus datos:** Al ejecutarse localmente, la información que compartes con el modelo (documentos, código de tu empresa, datos personales) nunca sale de tu ordenador. 
* **Ahorrar costes de API:** Los desarrolladores pueden usar Ollama para hacer pruebas y construir aplicaciones basadas en IA sin tener que pagar por cada consulta a servicios como los de OpenAI o Google.
* **Probar diferentes modelos fácilmente:** Te permite descargar y cambiar entre decenas de modelos de IA con un solo comando.

## Características y ventajas principales

* **Facilidad de uso:** Se instala como cualquier otro programa y se utiliza mediante comandos muy sencillos en la terminal (por ejemplo, ejecutando `ollama run llama3` ya tienes un chat funcionando).
* **Catálogo de modelos:** Permite descargar los modelos de código abierto más avanzados y populares del momento, como **Llama 3** (de Meta), **Mistral**, **Gemma** (de Google), **Qwen** o **Phi** (de Microsoft).
* **Integración y API:** Ollama incluye una API REST, lo que significa que puedes conectar la IA local a otras aplicaciones, interfaces gráficas (como Open WebUI) o extensiones de código en programas como Visual Studio Code.
* **Optimización de hardware:** Está diseñado para aprovechar al máximo los recursos de tu ordenador, usando tanto el procesador (CPU) como la tarjeta gráfica (GPU) para que las respuestas sean lo más rápidas posible.

En resumen, Ollama ha democratizado el acceso a la inteligencia artificial, permitiendo que cualquiera pueda tener un modelo potente corriendo de forma privada y gratuita en su propia casa.


## RECURSOS OLLAMA

1. La Fuente Oficial (El Estándar de Oro)

Ollama destaca precisamente por tener una curva de aprendizaje mínima. Sus sitios oficiales deben ser siempre la primera parada:

- Sitio web principal: ollama.com

        Tiene el botón de descarga directa para Windows, macOS y Linux.Es literalmente un instalador de "Siguiente > Siguiente".

- El Repositorio de GitHub: github.com/ollama/ollama

        El archivo Readme (la página principal del repositorio) es un tutorial en sí mismo. Muestra los comandos básicos en la terminal (ej. ollama run llama3), cómo gestionar modelos y cómo usar su API local.

- La Biblioteca de Modelos: ollama.com/library

        Aquí los alumnos pueden buscar qué IA quieren instalar (Llama 3, Mistral, Phi-3). Muestra los requisitos de RAM y el comando exacto para descargar cada uno.

2. Plataformas de Tutoriales Escritos (Para seguir a tu ritmo)


    Medium.com (Búsqueda recomendada: 

        "Ollama tutorial español"): * Medium está lleno de artículos de la comunidad tecnológica. Hay excelentes guías que explican no solo la instalación, sino también la integración con Python (que es justo lo que haréis en clase).

    Dev.to (Etiqueta: #ollama):

        Una comunidad fantástica para desarrolladores. Los tutoriales aquí suelen ir más al grano con el código y los posibles errores de instalación que puedan surgir en Windows (especialmente con WSL - Windows Subsystem for Linux, si deciden usarlo).

3. Videotutoriales en YouTube (Ideales para lo visual)

Se recomiendo buscar y filtrar videos de estos perfiles:

    Canales de divulgación IA (Ej. DotCSV o Carlos Santana): Aunque suelen hacer divulgación general, a menudo publican tutoriales sobre cómo correr modelos en local.

    Canales de programación y DevOps (Ej. Pelado Nerd): Son excelentes para explicar qué pasa "por debajo" cuando instalas herramientas en la terminal.

    "Cómo instalar Ollama Windows/Mac" o "Primeros pasos con Ollama y Python". Los videos de menos de 10 minutos suelen ser los más efectivos.