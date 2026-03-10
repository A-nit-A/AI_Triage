# USAR DOCKER PARA TENER LLAMA3 CORRIENDO EN LOCAL

## Crear una imagen personalizada (El modelo "dentro" del Docker)

Esta es la mejor opción si quieres un único archivo (o imagen) que contenga todo. Al llevarte esta imagen a otro PC, el modelo ya estará allí.

Para esto, crea un archivo llamado Dockerfile con el siguiente contenido:
Dockerfile

# Usamos la imagen oficial de Ollama
FROM ollama/ollama:latest

# Exponemos el puerto por defecto
EXPOSE 11434

# Truco para descargar el modelo durante la construcción de la imagen
RUN nohup bash -c "ollama serve & sleep 5 && ollama pull llama3"

# Comando para iniciar el servidor al arrancar el contenedor
ENTRYPOINT ["ollama", "serve"]

Pasos para crearla y moverla:

    Construye la imagen: docker build -t ollama-llama3 .

    Guarda la imagen en un archivo: docker save ollama-llama3 > ollama-llama3.tar

    En el otro equipo, cárgala: docker load < ollama-llama3.tar

    Ejecuta: docker run -d --name ollama-ready -p 11434:11434 ollama-llama3

## Usar un volumen externo (Carpeta en un USB/Disco)

Si no quieres reconstruir la imagen cada vez que cambies de modelo, puedes guardar los modelos en una carpeta de tu disco duro (o un pendrive) y "conectarla" al Docker en cualquier ordenador.

    Descarga el modelo una vez:
    Bash

    docker run -d -v ./mis_modelos:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    docker exec -it ollama ollama pull llama3

    Para llevarlo a otro PC:
    Copia la carpeta ./mis_modelos al nuevo equipo y ejecuta el mismo comando apuntando a esa carpeta. Docker detectará que llama3 ya existe en esa ruta y no descargará nada.

Comparativa rápida
Característica	Imagen Personalizada (Opción 1)	Volumen Externo (Opción 2)
Portabilidad	Un solo archivo .tar pesado.	Una carpeta con archivos sueltos.
Facilidad	Solo haces docker run y listo.	Debes copiar la carpeta y mapear la ruta.
Actualización	Debes crear una imagen nueva si quieres otro modelo.	Solo descargas el nuevo modelo a la carpeta.
Nota importante sobre el hardware

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

