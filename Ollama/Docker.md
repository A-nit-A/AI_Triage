# USAR DOCKER PARA TENER LLAMA3 CORRIENDO EN LOCAL


## INSTALAR DOCKER EN LINUX


> Actualiza los repositorios  
> `sudo apt update`  
>
> Instala Docker  
> `sudo apt install docker.io -y`  
>
> Añade tu usuario al grupo "docker" para no tener que usar "sudo" todo el tiempo  
> `sudo usermod -aG docker $USER`  

**IMPORTANTE** Para que el último comando haga efecto, tienes que cerrar sesión en tu usuario de Linux Mint y volver a entrar (o reiniciar el equipo). Si no lo haces, Docker te dará un error de permisos.


## Crear una imagen personalizada (El modelo "dentro" del Docker)


>CREAR EL "MOLDE" (DOCKERFILE) PARA TU IMAGEN
>
>Crea una carpeta "Llama3_Docker" y entra en ella 
> 
>`mkdir Llama3_Docker && cd Llama3_Docker`
>
>Crea un archivo llamado Dockerfile (sin ninguna extensión) usando un editor de texto de terminal como nano
>
>`nano Dockerfile`
>
>Pega este código dentro:  
>
>`# Usamos la imagen oficial de Ollama`  
>`FROM ollama/ollama:latest`     
>`# Arrancamos el servidor de ollama de fondo, esperamos 3 segundos y descargamos Llama 3`    
>`RUN nohup bash -c "ollama serve &" && sleep 3 && ollama pull llama3`
>
>Guarda y cierra (en nano es Ctrl+O, Enter, y luego Ctrl+X).

>CONSTRUIR LA IMAGEN PERSONALIZADA  
>
>Ahora le decimos a Docker que lea ese archivo y construya la imagen. Esto tardará un rato, porque aquí es donde se va a descargar Llama 3 por única vez.
>
>En la misma terminal, ejecuta:
>
>`docker build -t mi-ollama-llama3 .`
>
>(No te olvides del punto . al final, le indica a Docker que busque el archivo en la carpeta actual).

>CREAR UNA IMAGEN PARA LLEVARLA A OTRO PC
>
>Una vez termine, ya tienes la imagen en tu Linux Mint. Para llevártela a un PC con Windows u otro Linux, tenemos que exportarla a un archivo único (un .tar):
>
>`docker save -o imagen-llama3.tar mi-ollama-llama3`
>
>Esto creará un archivo llamado imagen-llama3.tar en tu carpeta (que pesará esos ~5.5 GB). Ese es el archivo que te puedes llevar en un pendrive.

>CÓMO USARLA EN LOS OTROS EQUIPOS
>
>Abrir una terminal en la carpeta del pendrive y cargar la imagen:
>
>`docker load -i imagen-llama3.tar`
>
>Una vez cargada, solo tienen que ejecutarla con:
>
>`docker run -d -p 11434:11434 --name ollama mi-ollama-llama3`
>
>¡Y listo! Ya podrán usar Llama 3 al instante escribiendo 
>
>`docker exec -it ollama ollama run llama3`
>
>O conectando cualquier aplicación (como el cliente web Open-WebUI) al puerto 11434 de esa máquina.



\# Usamos la imagen oficial de Ollama
FROM ollama/ollama:latest

\# Exponemos el puerto por defecto
EXPOSE 11434

\# Truco para descargar el modelo durante la construcción de la imagen
RUN nohup bash -c "ollama serve & sleep 5 && ollama pull llama3"

\# Comando para iniciar el servidor al arrancar el contenedor
ENTRYPOINT ["ollama", "serve"]

Pasos para crearla y moverla:

    Construye la imagen: docker build -t ollama-llama3 .

    Guarda la imagen en un archivo: docker save ollama-llama3 > ollama-llama3.tar

    En el otro equipo, cárgala: docker load < ollama-llama3.tar

    Ejecuta: docker run -d --name ollama-ready -p 11434:11434 ollama-llama3



Recuerda que si el ordenador de destino tiene una tarjeta gráfica NVIDIA, deberás añadir el parámetro --gpus all al hacer el docker run para que el modelo funcione de forma fluida. De lo contrario, usará solo el procesador (CPU) y será mucho más lento.

¿Te gustaría que te ayude a preparar un archivo docker-compose.yml para gestionar esto de forma más automática?

Sí, el sistema es compatible con ambos, pero hay un par de matices importantes sobre cómo interactúa Docker con el hardware dependiendo del sistema operativo.

Aquí tienes el desglose de lo que necesitas saber para que funcione igual de bien en Windows que en Linux:
1. Compatibilidad de la Imagen

La imagen de Docker que construyas (el archivo .tar o la imagen en el registro) es agnóstica al sistema operativo. Puedes construirla en Linux y cargarla en Windows (o viceversa) sin problemas, siempre y cuando la arquitectura del procesador sea la misma (por ejemplo, ambos sean x86_64).
2. El factor GPU (NVIDIA)

Para que el modelo llama3 no vaya lento como una tortuga, querrás usar la tarjeta gráfica. Aquí es donde cambian los requisitos:

    En Linux: Necesitas instalar el NVIDIA Container Toolkit. Esto permite que el contenedor Docker "hable" directamente con los drivers de tu tarjeta de video.

    En Windows: Necesitas tener instalado Docker Desktop y que esté configurado para usar el backend de WSL 2 (Windows Subsystem for Linux). Windows gestiona el paso de la GPU al contenedor de forma automática si los drivers están al día.

3. Diferencias en las rutas de archivos

Si decides usar la Opción 2 (la de la carpeta externa/pendrive), ten cuidado con cómo escribes la ruta en la terminal:

    En Windows (PowerShell):
    docker run -v C:\mi_carpeta\ollama:/root/.ollama ...

    En Linux/Bash:
    docker run -v /home/usuario/ollama:/root/.ollama ...

4. Recomendación de Docker Compose

Para evitar líos de comandos distintos en cada equipo, lo ideal es usar un archivo docker-compose.yml. Este archivo centraliza la configuración:
YAML

services:
  ollama:
    image: ollama-llama3:latest  # La imagen que creaste
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

Resumen de compatibilidad
Componente	    Windows (WSL2)	            Linux
Motor Docker	Docker Desktop	            Docker Engine / Portainer
Acceso a GPU	Nativo                      vía WSL2	Requiere NVIDIA Container Toolkit
Rendimiento	    Muy alto (casi nativo)	    Nativo
Portabilidad	Total (archivo .tar)	    Total (archivo .tar)

