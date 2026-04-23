# INSTALAR LLAMA3 CON OLLAMA 

## INSTALAR OLLAMA EN LINUX

Ollama tiene un script de instalación oficial que hace todo el trabajo. Abre un terminal y ejecuta el siguiente comando:

>`curl -fsSL https://ollama.com/install.sh | sh`  

**Nota: Este comando descargará e instalará Ollama, y lo configurará como un servicio en segundo plano.**


### DESCARGAR Y EJECUTAR LLAMA3

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

### CREAR ACCESOS DIRECTOS PARA INICIAR Y DETENER OLLAMA (LINUX MINT)

Como el comando para iniciar Ollama requiere permisos de administrador (usamos sudo), si creamos un acceso directo normal, fallaría silenciosamente porque no tendría dónde pedirte la contraseña. Para solucionarlo, usaremos un comando llamado pkexec, que hace que Linux Mint te muestre una ventanita gráfica pidiendo tu contraseña, igual que cuando instalas un programa nuevo.

Aquí tienes los pasos para crear el lanzador en Cinnamon:
#### CREAR EL LANZADOR EN EL ESCRITORIO PARA INICIAR OLLAMA

Ve al escritorio de tu Linux Mint, haz clic derecho en cualquier espacio vacío y selecciona Crear un nuevo lanzador aquí... (o Create a new launcher here...).

Se abrirá una ventana con las propiedades del lanzador. Rellénalo con estos datos:

    Nombre: Iniciar Ollama
    
    Comando: pkexec systemctl start ollama
    
    Comentario: Enciende el motor de IA local.
    
    (Opcional) Si haces clic en el icono del cohete a la izquierda, puedes elegir el icono que más te guste de la galería de Linux Mint (por ejemplo, un cerebro, un chip o un engranaje).
    
    Haz clic en Aceptar.

#### CREAR EL LANZADOR EN EL ESCRITORIO PARA APAGAR OLLAMA

Ya que tienes un botón para encenderlo, lo ideal es tener otro para apagarlo y liberar la memoria cuando termines. 
Puedes repetir exactamente los mismos pasos de arriba, pero cambiando los datos a esto:

    Nombre: Apagar Ollama

    Comando: pkexec systemctl stop ollama

    Comentario: Apaga el motor de IA local.

## INSTALAR OLLAMA EN WINDOWS

Instalar Llama 3 usando Ollama en Windows 11 es un proceso muy directo, ya que Ollama cuenta con un instalador nativo que hace casi todo el trabajo pesado. 

Aquí tienes el paso a paso detallado:

### Paso 1: Descargar Ollama
1. Abre tu navegador web y ve a la página oficial: **[ollama.com/download](https://ollama.com/download)**.
2. Haz clic en el botón grande que dice **"Download for Windows"**. Esto descargará un archivo llamado `OllamaSetup.exe`.

### Paso 2: Instalar el programa
1. Ve a tu carpeta de Descargas y haz doble clic en **`OllamaSetup.exe`**.
2. Haz clic en **"Install"** y espera a que termine el proceso. No te pedirá configuraciones complejas.
3. Una vez instalado, es posible que veas el icono de Ollama (una pequeña llama) en la bandeja del sistema, en la esquina inferior derecha de la barra de tareas. Esto indica que el motor de Ollama se está ejecutando en segundo plano.

### Paso 3: Abrir la terminal de Windows
Para indicarle a Ollama qué modelo queremos, necesitamos usar la línea de comandos.
1. Haz clic en el menú **Inicio** de Windows 11.
2. Escribe **`cmd`** o **`PowerShell`** y presiona la tecla Enter para abrir la consola.

### Paso 4: Descargar y ejecutar Llama 3
1. En la ventana negra o azul que se acaba de abrir, escribe el siguiente comando y presiona Enter:
   ```bash
   ollama run llama3
   ```
2. **Espera a que se descargue:** Como es la primera vez que ejecutas este modelo, Ollama empezará a descargarlo. La versión estándar de Llama 3 (de 8 mil millones de parámetros) pesa alrededor de **4.7 GB**, por lo que tardará unos minutos dependiendo de la velocidad de tu conexión a internet.

### Paso 5: ¡Empieza a chatear!
1. Una vez finalizada la descarga, verás que en la pantalla aparece algo como `>>>`. Ese es el indicador de que Llama 3 está listo para escucharte.
2. Escribe cualquier pregunta o instrucción (en español o inglés) y presiona Enter. La IA te responderá directamente en la consola.
3. Cuando quieras cerrar el chat y salir, simplemente escribe **`/bye`** y presiona Enter.

## CREAR ACCESOS DIRECTOS PARA INICIAR Y DETENER OLLAMA (WINDOWS)

En Windows, Ollama se instala por defecto como una aplicación en segundo plano que se inicia automáticamente al encender el ordenador (aparece en la bandeja del sistema, junto al reloj). 

Si prefieres tener el control total y abrir o cerrar Ollama solo cuando lo necesites para ahorrar memoria RAM, puedes crear dos accesos directos muy sencillos en tu escritorio.

Aquí tienes los pasos exactos:

### 1. Crear el acceso directo para DETENER Ollama

Para parar Ollama, necesitamos un comando que cierre la aplicación de forma segura.

1. Haz clic derecho en un espacio vacío de tu Escritorio.
2. Selecciona **Nuevo** > **Acceso directo**.
3. En la casilla de "Escriba la ubicación del elemento", copia y pega exactamente el siguiente comando:
   ```cmd
   taskkill /F /IM "ollama app.exe" /IM "ollama.exe"
   ```
4. Haz clic en **Siguiente**.
5. Ponle un nombre fácil de reconocer, por ejemplo: **`Detener Ollama`**.
6. Haz clic en **Finalizar**.

### 2. Crear el acceso directo para INICIAR Ollama

Para volver a iniciarlo, solo necesitamos apuntar al archivo ejecutable de la aplicación.

1. Haz clic derecho en un espacio vacío de tu Escritorio.
2. Selecciona **Nuevo** > **Acceso directo**.
3. En la casilla de ubicación, copia y pega la ruta estándar de instalación de Ollama en Windows:
   ```cmd
   %LOCALAPPDATA%\Programs\Ollama\ollama app.exe
   ```
4. Haz clic en **Siguiente**.
5. Ponle un nombre, por ejemplo: **`Iniciar Ollama`**.
6. Haz clic en **Finalizar**.

---

### Consejo extra: Evitar que Ollama se inicie con Windows
Si vas a usar estos botones manuales, lo ideal es evitar que Ollama arranque solo cada vez que enciendes el PC. Para hacerlo:

1. Busca el icono de Ollama (la llamita) en la bandeja del sistema (esquina inferior derecha de tu pantalla, quizá dentro de la flechita de iconos ocultos).
2. Haz clic derecho sobre el icono.
3. Desmarca la opción **"Run at startup"** (Ejecutar al inicio).
4. A partir de ahora, Ollama estará completamente apagado al encender tu PC, y solo consumirá recursos cuando hagas doble clic en tu nuevo acceso directo de **Iniciar Ollama**.

---

## Nota sobre el rendimiento

Para que la versión estándar de Llama 3 funcione con fluidez, lo ideal es tener al menos **8 GB de memoria RAM** (recomendable 16 GB). Si tienes una tarjeta gráfica dedicada (NVIDIA o AMD), Ollama la detectará automáticamente para generar las respuestas mucho más rápido.

Se pede utilizar un modelo más ligero si no se dispone de los recursos necesarios cmo por ejemplo qwen2.5:3b. Para ello, se puede utilizar el siguiente comando:

> ollama run qwen2.5:3b

- Se descargará aproximadamente 1.9 GB (que es el tamaño del modelo cuantizado para 3B).

- Se verificará la integridad del archivo.

- Y por último levantará un chat interactivo inmediatamente para que puedas probarlo.

**Comandos adicionales**

- Ver modelos instalados: Si quieres ver cuánto espacio ocupa o qué otros modelos tienes.

   > ollama list

- Borrar modelos sobrantes: Para liberar RAM y espacio en disco.

   > ollama rm llama3 (o el nombre exacto que aparezca en tu lista).

- Actualizar: Los modelos reciben mejoras frecuentemente. 

   >  ollama pull qwen2.5:3b   








