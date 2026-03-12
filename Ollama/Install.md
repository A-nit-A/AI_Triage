# INSTALAR LLAMA3 CON OLLAMA Y ACCEDER USANDO OPEN WEBUI EN LINUX

## INSTALAR OLLAMA

Ollama tiene un script de instalación oficial que hace todo el trabajo por ti.  
Abre tu terminal (puedes usar Ctrl + Alt + T) y ejecuta el siguiente comando:

>`curl -fsSL https://ollama.com/install.sh | sh`  

**Nota: Este comando descargará e instalará Ollama, y lo configurará como un servicio en segundo plano.**


## DESCARGAR Y EJECUTAR LLAMA3

Una vez que la instalación de Ollama termine, puedes descargar y ejecutar Llama 3 directamente.  
En la misma terminal, escribe:

>`ollama run llama3`


- Ollama descargará los pesos del modelo (la versión de 8B parámetros pesa unos 4.7 GB, así que tardará un poco dependiendo de tu conexión).  
- Una vez descargado, verás un prompt en la terminal donde ya puedes chatear con Llama 3 para probar que funciona.
- Para salir de ese chat en la terminal, simplemente escribe /bye o presiona Ctrl + D. Ollama seguirá ejecutándose en segundo plano.

### DETENER EL SERVICIO DE OLLAMA POR COMPLETO

El script que usamos en el paso anterior instaló Ollama como un servicio de tu sistema Linux. Para apagarlo totalmente y liberar todos los recursos de tu PC antes de cerrar la terminal, ejecuta este comando:

>`sudo systemctl stop ollama`

### COMANDOS EXTRA QUE TE SERÁN MUY ÚTILES

> #Para encenderlo de nuevo:  
>
>`sudo systemctl start ollama`
>
> #Para ver si está encendido o apagado:  
>
>`sudo systemctl status ollama`  
> #(pulsa la tecla q para salir de esa pantalla).
>
> #Para reiniciarlo (si alguna vez se queda pillado):  
>
>`sudo systemctl restart ollama`


### DESACTIVAR EL ARRANQUE AUTOMÁTICO

Abre tu terminal y ejecuta el siguiente comando:

>`sudo systemctl disable ollama`

Al ejecutar esto, el sistema eliminará el enlace que hace que Ollama se encienda solo al arrancar Linux Mint. Tranquilo, esto no desinstala ni borra nada, solo le dice al sistema: "no enciendas esto hasta que yo te lo pida". A partir de ahora, cada vez que enciendas tu PC, Ollama estará apagado por defecto. Cuando quieras volver a chatear con Llama 3, solo tendrás que hacer este paso previo en la terminal:

>`sudo systemctl start ollama`

## CREAR ACCESOS DIRECTOS PARA INICIAR Y DETENER OLLAMA (LINUX MINT)

Como el comando para iniciar Ollama requiere permisos de administrador (usamos sudo), si creamos un acceso directo normal, fallaría silenciosamente porque no tendría dónde pedirte la contraseña. Para solucionarlo, usaremos un comando llamado pkexec, que hace que Linux Mint te muestre una ventanita gráfica pidiendo tu contraseña, igual que cuando instalas un programa nuevo.

Aquí tienes los pasos para crear el lanzador en Cinnamon:
### CREAR EL LANZADOR EN EL ESCRITORIO PARA INICIAR OLLAMA

Ve al escritorio de tu Linux Mint, haz clic derecho en cualquier espacio vacío y selecciona Crear un nuevo lanzador aquí... (o Create a new launcher here...).

Se abrirá una ventana con las propiedades del lanzador. Rellénalo con estos datos:

    Nombre: Iniciar Ollama
    
    Comando: pkexec systemctl start ollama
    
    Comentario: Enciende el motor de IA local.
    
    (Opcional) Si haces clic en el icono del cohete a la izquierda, puedes elegir el icono que más te guste de la galería de Linux Mint (por ejemplo, un cerebro, un chip o un engranaje).
    
    Haz clic en Aceptar.

### CREAR EL LANZADOR EN EL ESCRITORIO PARA APAGAR OLLAMA

Ya que tienes un botón para encenderlo, lo ideal es tener otro para apagarlo y liberar la memoria cuando termines. 
Puedes repetir exactamente los mismos pasos de arriba, pero cambiando los datos a esto:

    Nombre: Apagar Ollama

    Comando: pkexec systemctl stop ollama

    Comentario: Apaga el motor de IA local.


## PREPARAR E INSTALAR OPEN WEBUI (Vía Docker)

Ya que mencionaste que vas a usar Open WebUI, la forma más recomendada y limpia de instalarlo en Linux Mint es utilizando Docker.

### INSTALAR DOCKER (si no lo tienes)  

Abre una ventana de terminal y ejecuta los siguientes comandos:

> `sudo apt update`  
> `sudo apt install docker.io`

### EJECUTAR Open WebUI

Este es el comando oficial de Docker para ejecutar Open WebUI y conectarlo automáticamente a tu instancia local de Ollama:

> `sudo docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`

### ACCEDER A LA INTERFAZ

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


