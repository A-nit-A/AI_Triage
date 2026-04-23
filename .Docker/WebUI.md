# PREPARAR E INSTALAR OPEN WEBUI (Vía Docker)

Ya que mencionaste que vas a usar Open WebUI, la forma más recomendada y limpia de instalarlo en Linux Mint es utilizando Docker.

## INSTALAR DOCKER (si no lo tienes)  

Abre una ventana de terminal y ejecuta los siguientes comandos:

> `sudo apt update`  
> `sudo apt install docker.io`

## EJECUTAR Open WebUI

Este es el comando oficial de Docker para ejecutar Open WebUI y conectarlo automáticamente a tu instancia local de Ollama:

> `sudo docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`

## ACCEDER A LA INTERFAZ

Una vez que el contenedor de Docker esté en marcha, abre tu navegador web (Firefox, Chrome, Brave, etc.) y ve a la siguiente dirección:

> `http://localhost:3000`

La primera vez que entres, te pedirá que crees una cuenta de administrador (es una cuenta local, tus datos no salen de tu equipo). Una vez dentro, en la parte superior verás un desplegable para seleccionar el modelo; ahí te aparecerá Llama 3 listo para usarse.

**Recuerda que si instalaste Open WebUI con el parámetro --restart always en Docker, la interfaz web sí estará siempre disponible, pero si desactivaste el arranque automático de Ollama te dirá que no puede conectar con el modelo hasta que inicies Ollama.**

## PROBLEMAS DE CONEXIÓN

### COMPROBAR LA URL EN LOS AJUSTES Open WebUI

Dentro del contenedor de Docker, la palabra "localhost" significa el propio contenedor, no tu ordenador.

En Open WebUI, ve a Ajustes (icono del engranaje abajo a la izquierda) > Conexiones (Connections).

Mira la URL debajo de Ollama API.

    Asegúrate de que NO diga http://localhost:11434 ni http://127.0.0.1:11434.

    Debe decir exactamente esto:
    http://host.docker.internal:11434

Haz clic en el icono de guardar/recargar al lado de la URL. Si funciona, dejará de darte el error.

### OLLAMA BLOQUEA LAS CONEXIONES EXTERNAS

Ollama está configurado en modo estricto y bloquea cualquier petición que no venga de tu propio terminal.

Abre tu terminal y ejecuta:

Edita la configuración de Ollama:

>`sudo systemctl edit ollama.service`

Asegúrate de que el archivo quede exactamente con esto en la parte **superior**

>`[Service]`   
>`Environment="OLLAMA_HOST=0.0.0.0"`

Guarda el archivo (Si es el editor Nano: Ctrl+O, luego Enter, y finalmente Ctrl+X).

Aplica los cambios reiniciando Ollama:

>`sudo systemctl daemon-reload`  
>`sudo systemctl restart ollama`

Comprobación final

Para asegurarnos de que el modelo Llama 3 realmente está listo y Ollama funciona, ejecuta esto en tu terminal:

>`ollama list`

Debería aparecer llama3 en la lista. Si no aparece, descárgalo con ollama run llama3.