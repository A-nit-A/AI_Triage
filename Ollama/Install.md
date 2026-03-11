# INSTALAR LLAMA3 CON OLLAMA Y ACCEDER USANDO OPEN WEBUI

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

### Detener el servicio de Ollama por completo

El script que usamos en el paso anterior instaló Ollama como un servicio de tu sistema Linux. Para apagarlo totalmente y liberar todos los recursos de tu PC antes de cerrar la terminal, ejecuta este comando:

>`sudo systemctl stop ollama`

### Comandos extra que te serán muy útiles

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


### Desactivar el arranque automático

Abre tu terminal y ejecuta el siguiente comando:

>`sudo systemctl disable ollama`

Al ejecutar esto, el sistema eliminará el enlace que hace que Ollama se encienda solo al arrancar Linux Mint. Tranquilo, esto no desinstala ni borra nada, solo le dice al sistema: "no enciendas esto hasta que yo te lo pida".

### Tu nuevo flujo de trabajo

A partir de ahora, cada vez que enciendas tu PC, Ollama estará apagado por defecto.

Cuando quieras entrar a Open WebUI a chatear con Llama 3, solo tendrás que hacer este paso previo en la terminal:

>`sudo systemctl start ollama`


Como el comando para iniciar Ollama requiere permisos de administrador (usamos sudo), si creamos un acceso directo normal, fallaría silenciosamente porque no tendría dónde pedirte la contraseña. Para solucionarlo, usaremos un comando llamado pkexec, que hace que Linux Mint te muestre una ventanita gráfica pidiendo tu contraseña, igual que cuando instalas un programa nuevo.

Aquí tienes los pasos para crear el lanzador en Cinnamon:
1. Crear el lanzador en el escritorio

    Ve al escritorio de tu Linux Mint, haz clic derecho en cualquier espacio vacío y selecciona Crear un nuevo lanzador aquí... (o Create a new launcher here...).

    Se abrirá una ventana con las propiedades del lanzador. Rellénalo con estos datos:

        Nombre: Iniciar Ollama

        Comando: pkexec systemctl start ollama

        Comentario: Enciende el motor de IA local.

    (Opcional) Si haces clic en el icono del cohete a la izquierda, puedes elegir el icono que más te guste de la galería de Linux Mint (por ejemplo, un cerebro, un chip o un engranaje).

    Haz clic en Aceptar.

2. Añadirlo al menú de inicio (Cinnamon te preguntará)

Justo después de darle a Aceptar, Cinnamon suele mostrar un mensaje preguntando: "¿Desea añadir este lanzador al menú de aplicaciones?".

    Responde que Sí.

De esta forma, no solo lo tendrás en el escritorio, sino que si pulsas la tecla "Super" (la tecla de Windows) y escribes "Ollama", te aparecerá directamente en el menú, ¡como cualquier otro programa!
💡 Un consejo extra: El botón de "Apagar Ollama"

Ya que tienes un botón para encenderlo, lo ideal es tener otro para apagarlo y liberar la memoria cuando termines.

Puedes repetir exactamente los mismos pasos de arriba, pero cambiando los datos a esto:

    Nombre: Apagar Ollama

    Comando: pkexec systemctl stop ollama

    Comentario: Apaga el motor de IA local.

¡Y listo! Ahora tienes el control total de los recursos de tu PC a un solo clic de distancia. Cuando vayas a usar Open WebUI, le das doble clic a "Iniciar Ollama", pones tu contraseña en la ventanita gráfica, y a disfrutar.



Una vez ejecutado, ya puedes ir a tu navegador, entrar a http://localhost:3000 y usar tu IA con normalidad. (Recuerda que si instalaste Open WebUI con el parámetro --restart always en Docker, la interfaz web sí estará siempre disponible, pero te dirá que no puede conectar con el modelo hasta que inicies Ollama con el comando de arriba).



## PREPARAR E INSTALAR OPEN WEBUI (Vía Docker)

Ya que mencionaste que vas a usar Open WebUI, la forma más recomendada y limpia de instalarlo en Linux Mint es utilizando Docker.

A. Instalar Docker (si no lo tienes):
Bash

sudo apt update
sudo apt install docker.io

B. Ejecutar Open WebUI:
Este es el comando oficial de Docker para ejecutar Open WebUI y conectarlo automáticamente a tu instancia local de Ollama:
Bash

sudo docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

4. Acceder a la interfaz

Una vez que el contenedor de Docker esté en marcha, abre tu navegador web (Firefox, Chrome, Brave, etc.) y ve a la siguiente dirección:

http://localhost:3000

La primera vez que entres, te pedirá que crees una cuenta de administrador (es una cuenta local, tus datos no salen de tu equipo). Una vez dentro, en la parte superior verás un desplegable para seleccionar el modelo; ahí te aparecerá Llama 3 listo para usarse.