# USAR DOCKER PARA TENER LLAMA3 CORRIENDO EN LOCAL


## INSTALAR DOCKER EN LINUX


> Actualiza los repositorios  
>
>> `sudo apt update`  
>
> Instala Docker  
>
>> `sudo apt install docker.io -y`  
>
> Añade tu usuario al grupo "docker" para no tener que usar "sudo" todo el tiempo  
>
>> `sudo usermod -aG docker $USER`  

**IMPORTANTE** Para que el último comando haga efecto, tienes que cerrar sesión en tu usuario de Linux Mint y volver a entrar (o reiniciar el equipo). Si no lo haces, Docker te dará un error de permisos.


## Crear una imagen personalizada (El modelo "dentro" del Docker)


>CREAR EL "MOLDE" (DOCKERFILE) PARA TU IMAGEN
>
>Crea una carpeta "Llama3_Docker" y entra en ella 
>
>> `mkdir Llama3_Docker && cd Llama3_Docker`
>
>Crea un archivo llamado Dockerfile (sin ninguna extensión) usando un editor de texto de terminal como nano
>
>> `nano Dockerfile`
>
>Pega este código dentro:  
>
>> `# Usamos la imagen oficial de Ollama`  
>> `FROM ollama/ollama:latest`     
>> `# Exponemos el puerto por defecto`  
>> `EXPOSE 11434`  
>> `# Truco para descargar el modelo durante la construcción de la imagen`  
>> `RUN nohup bash -c "ollama serve & sleep 5 && ollama pull llama3"`  
>> `# Comando para iniciar el servidor al arrancar el contenedor`  
>> `ENTRYPOINT ["ollama", "serve"]`  
>
>Guarda y cierra (en nano es Ctrl+O, Enter, y luego Ctrl+X).

>CONSTRUIR LA IMAGEN PERSONALIZADA  
>
>Ahora le decimos a Docker que lea ese archivo y construya la imagen. Esto tardará un rato, porque aquí es donde se va a descargar Llama 3 por única vez.
>
>En la misma terminal, ejecuta:
>
>> `docker build -t ollama-llama3 .`
>
>(No te olvides del punto . al final, le indica a Docker que busque el archivo en la carpeta actual).

>CREAR UNA IMAGEN PARA LLEVARLA A OTRO PC
>
>Una vez termine, ya tienes la imagen en tu Linux Mint. Para llevártela a un PC con Windows u otro Linux, tenemos que exportarla a un archivo único (un .tar):
>
>> `docker save -o imagen-llama3.tar ollama-llama3`
>
>Esto creará un archivo llamado imagen-llama3.tar en tu carpeta (que pesará esos ~5.5 GB). Ese es el archivo que te puedes llevar en un pendrive.

>CÓMO USARLA EN LOS OTROS EQUIPOS
>
>Abrir una terminal en la carpeta del pendrive y cargar la imagen:
>
>> `docker load -i imagen-llama3.tar`
>
>Una vez cargada, solo tienen que ejecutarla con:
>
>> `docker run -d -p 11434:11434 --name ollama mi-ollama-llama3`
>
>¡Y listo! Ya podrán usar Llama 3 al instante escribiendo 
>
>> `docker exec -it ollama ollama run llama3`
>
>O conectando cualquier aplicación (como el cliente web Open-WebUI) al puerto 11434 de esa máquina.

Recuerda que si el ordenador de destino tiene una tarjeta gráfica NVIDIA, deberás añadir el parámetro --gpus all al hacer el docker run para que el modelo funcione de forma fluida. De lo contrario, usará solo el procesador (CPU) y será mucho más lento.


El factor GPU (NVIDIA)

Para que el modelo llama3 no vaya lento como una tortuga, querrás usar la tarjeta gráfica. Aquí es donde cambian los requisitos:

    En Linux: Necesitas instalar el NVIDIA Container Toolkit. Esto permite que el contenedor Docker "hable" directamente con los drivers de tu tarjeta de video.

    En Windows: Necesitas tener instalado Docker Desktop y que esté configurado para usar el backend de WSL 2 (Windows Subsystem for Linux). Windows gestiona el paso de la GPU al contenedor de forma automática si los drivers están al día.

Crear el archivo docker-compose.yml

En el equipo destino (donde ya has cargado tu imagen .tar), crea un archivo llamado docker-compose.yml y pega este contenido:
YAML

version: '3.8'

services:
  ollama:
    # Usamos exactamente el nombre de la imagen que te trajiste en el pendrive
    image: ollama-llama3
    container_name: ollama-local
    ports:
      - "11434:11434"
    restart: unless-stopped
    
    # -------------------------------------------------------------
    # ACELERACIÓN POR TARJETA GRÁFICA (GPU)
    # Si el PC destino tiene una gráfica NVIDIA y tiene instalados 
    # los drivers de NVIDIA Container Toolkit, quita el símbolo '#' 
    # de las siguientes 6 líneas para que el modelo vaya a la velocidad de la luz:
    # -------------------------------------------------------------
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]

2. Cómo levantarlo

Una vez tengas el archivo guardado en una carpeta, abre la terminal (o el PowerShell si estás en el Windows destino) en esa misma ubicación y ejecuta:
Bash

docker compose up -d

(El -d es para que se ejecute en segundo plano y te devuelva el control de la terminal).

Con esto, el servidor de Ollama con Llama 3 ya estará corriendo en el puerto 11434 de ese ordenador, listo para recibir peticiones. Para apagarlo, solo tendrían que ejecutar docker compose down.


¡Excelente elección! Al añadirle una interfaz gráfica, el uso del modelo pasa de ser una pantalla negra con texto a una experiencia exactamente igual a la de usar ChatGPT en el navegador.

Aquí tienes el archivo docker-compose.yml actualizado. He configurado ambos servicios para que se hablen entre ellos automáticamente de forma interna.
El archivo docker-compose.yml completo

Sustituye el contenido de tu archivo por este:
YAML

services:
  ollama:
    image: mi-ollama-llama3
    container_name: ollama-local
    ports:
      - "11434:11434"
    restart: unless-stopped
    # -------------------------------------------------------------
    # ACELERACIÓN POR GPU (Descomentar si hay NVIDIA)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]
    # -------------------------------------------------------------

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    environment:
      # Esto le dice a la interfaz cómo conectarse al contenedor de Ollama
      - 'OLLAMA_BASE_URL=http://ollama:11434'
    volumes:
      # Guarda el historial de chats y usuarios para no perderlos al reiniciar
      - open-webui-data:/app/backend/data
    restart: unless-stopped
    depends_on:
      - ollama

volumes:
  open-webui-data:

Cómo usarlo en el equipo destino

    Abre la terminal en la carpeta donde tienes este docker-compose.yml y ejecuta:
    Bash

    docker compose up -d

    Abre el navegador web en ese ordenador y entra en la dirección: http://localhost:3000

    La primera vez que entres, te pedirá crear una cuenta de administrador (nombre, email y contraseña). Como todo se ejecuta localmente en tu ordenador, no necesitas un email real, es solo para crear tu usuario local.

    Una vez dentro, verás un desplegable en la parte superior. Selecciona llama3 ¡y empieza a chatear!

    Aquí tienes los pasos para descargar y empaquetar la interfaz gráfica, tal y como hicimos con Llama 3:
1. Descargar y empaquetar Open WebUI (En tu Linux Mint)

Abre la terminal en tu equipo original y ejecuta estos comandos uno por uno:
Bash

# 1. Descargamos la imagen oficial de Open WebUI desde internet
docker pull ghcr.io/open-webui/open-webui:main

# 2. La empaquetamos en un archivo .tar (esto creará un archivo de unos 1.5 GB)
docker save -o open-webui.tar ghcr.io/open-webui/open-webui:main

2. Preparar el pendrive (El "Kit" completo)

Ahora tienes todo lo necesario. En tu pendrive debes copiar estos tres archivos:

    imagen-llama3.tar (El modelo de Ollama que creamos al principio).

    open-webui.tar (La interfaz gráfica que acabamos de empaquetar).

    docker-compose.yml (El archivo de texto con la configuración de ambos).

3. Instalarlo en el equipo destino (Windows o Linux)

Cuando llegues al otro ordenador, conecta el pendrive, abre una terminal (o PowerShell en Windows) dentro de la carpeta del pendrive y ejecuta estos pasos:
Bash

# 1. Cargamos el modelo Llama 3 en el Docker de este equipo
docker load -i imagen-llama3.tar

# 2. Cargamos la interfaz gráfica
docker load -i open-webui.tar

# 3. Levantamos los dos servicios a la vez usando el archivo de configuración
docker compose up -d

¡Y ya está! Como las imágenes ya están cargadas en la memoria de Docker gracias a los archivos .tar, el comando docker compose las detectará instantáneamente y no intentará conectarse a internet para descargarlas.

Solo tendrás que abrir el navegador en ese equipo, entrar a http://localhost:3000 y disfrutar de tu propia IA privada y portátil.