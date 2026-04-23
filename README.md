# Agente de Triaje de Emails — Atención al Cliente TechPyme

Una pequeña tienda online recibe decenas de correos al día. El dueño pierde 2 horas diarias respondiendo dudas básicas o derivando mensajes al departamento correcto.

Nuestro cliente nos pide automatizar este proceso. Para ello crearémos un agente de triaje de emails que actuará como el primer filtro inteligente.

El agente responderá a los correos si consigue encontrar la respuesta en la base de datos creada a partir de las FAQs de TechPyme. Si no consigue encontrar la respuesta lo derivará al departamento de atención al cliente.

## Simulación

Para simplificar el proceso se simulará la entrada de correos. Se usará un archivo JSON con 4 casos de prueba: un correo fácil (pregunta por el horario), un correo sobre un envío (pregunta por devoluciones) y un correo complejo/queja (producto roto, que debería ser escalado).

- Los correos respondidos se almacenarán en un archivo CSV llamado correos_respondidos.csv

- Los correos escalados se almacenarán en un archivo CSV llamado correos_escalados.csv

- Al finalizar de procesar el archivo JSON se eliminará para no volver a procesarlo y permitir una nueva ejecución con otro archivo JSON.

## Estructura del Repositorio

A continuación se detalla la estructura principal del proyecto y el contenido de sus directorios:

- **`automation/`**: Contiene los scripts principales del agente de IA (`agent.py`, `rag.py`), la base de conocimiento y los datos generados durante la ejecución.
- **`challenge/`**: Incluye los retos y próximos pasos a desarrollar en el proyecto.
- **`docs/`**: Carpeta de documentación. Dentro se encuentra el directorio **`docs/web/`**, que contiene las páginas y recursos a los que accede **`index.html`**.
- **`how_to_do_it/`**: Contiene instrucciones o guías paso a paso sobre el desarrollo del proyecto.
- **`index.html`**: Es la página web principal de presentación del repositorio. Sirve como punto de entrada visual para entender el proyecto.
- **`main.py`**: Script principal que orquesta la ejecución del proyecto, inicializando la base de datos vectorial si es necesario y lanzando el agente.
