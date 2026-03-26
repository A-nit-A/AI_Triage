# INSTALAR LLAMA3 CON OLLAMA EN LINUX

## INSTALAR OLLAMA

Ollama tiene un script de instalación oficial que hace todo el trabajo. Abre un terminal y ejecuta el siguiente comando:

>`curl -fsSL https://ollama.com/install.sh | sh`  

**Nota: Este comando descargará e instalará Ollama, y lo configurará como un servicio en segundo plano.**


## DESCARGAR Y EJECUTAR LLAMA3

Una vez que la instalación de Ollama termine, se puede descargar y ejecutar Llama 3 directamente.  
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

Al ejecutar esto, el sistema eliminará el enlace que hace que Ollama se encienda solo al arrancar Linux. Tranquilo, esto no desinstala ni borra nada, solo le dice al sistema: "no enciendas esto hasta que yo te lo pida". A partir de ahora, cada vez que enciendas tu PC, Ollama estará apagado por defecto. Cuando quieras volver a chatear con Llama 3, solo tendrás que hacer este paso previo en la terminal:

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





