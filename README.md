# Proyecto SIATA niveles de lluvia
Creado por: Maryangela Balcarcel
ID: 490985

Este proyecto se va a desplegar desde dos contenedores, uno desde el cuál se va a visualizar el login (api.py) y el otro la información de los niveles en que se encuentra el agua.
Para llevar el proyecto a cabo se crean los archivos Dockerfile's en los que se van poner los comandos donde para crear las imagenes que va a contener la página web. Para que el usuario no ejecute comando a comando los archivos docker, se creó un archivo .sh en donde se encuentran las líneas que se van a ejecutar para crear las dos imagenes y posteriormente ponerlas a correr.
De igual forma, el archivo api.py contiene el código de la página web en donde se hace el login: los usuarios se enuentran en el archivo de las bases de datos .csv, y el archivo front.py se encarga de la parte gráfica junto con la correcta ejecución del filtrado de los datos. Cada archivo .py contiene el requirements'Api-Front' donde se encuentran las librerías que necesitan de por sí para que estén en funcionamiento.

El archivo DockerfileApi se interpreta de la siguiente forma: (De igual forma, se induce el DockerfileFront ya que contienen la misma estructura)

'FROM ubuntu'. Especifica la imagen base en la que se basará la nueva imagen. En este caso, se utilizará la imagen base de Ubuntu.

'RUN apt update'
'RUN apt install python3.10 -y'
'RUN apt install python3-pip -y' Estas línea ejecuta comandos dentro de la imagen durante la construcción. En este caso, se está actualizando el sistema operativo Ubuntu (apt update), instalando Python 3.10 (apt install python3.10 -y), y luego instalando pip para Python 3 (apt install python3-pip -y). 

'WORKDIR /api' Se establece el directorio de trabajo dentro de la imagen donde se copiarán los archivos y se ejecutarán los comandos. En este caso, el directorio de trabajo se establece como /api.

'COPY api.py .' Copia el archivo api.py desde el contexto de construcción (donde se encuentra el Dockerfile) al directorio de trabajo (/api) dentro de la imagen.

'COPY requirementsApi.txt .' Copia el archivo requirementsApi.txt desde el contexto de construcción al directorio de trabajo dentro de la imagen. 

'RUN pip3 install -r requirementsApi.txt' Ejecuta el comando pip3 install dentro de la imagen para instalar las dependencias especificadas en el archivo requirementsApi.txt. Las dependencias se instalan utilizando pip para Python 3. 

'CMD ["python3.10", "api.py"]' Especifica el comando que se ejecutará cuando se inicie un contenedor a partir de esta imagen. En este caso, se ejecutará el archivo api.py utilizando el intérprete de Python 3.10 (python3.10). 

El archivo despliegue_contenedor.sh Contiene los siguientes comandos:
#!/bin/bash
Los comandos docker build constuyen la imagen. -f para indicar que se creará a partir del archivo en cuestión, -t para indicar el nombre que recibirá la imagen.
sudo docker build . -f DockerfileApi -t api:01
sudo docker build . -f DockerfileFront -t front:01
El docker run ejecuta las imagenes, -p para indicar desde qué puerto van a estar corriendo.
sudo docker run -d -p 5000:5000 -p 8089:8089 api:01
sudo docker run -d -v /home/ubuntu/usuarios.csv -p 80:80 front:01

Para verificar que ambas imagenes están corriendo correctamente se ejecuta el comando 'sudo docker ps' y se deben mostrar las dos imagenes en estado 'Up' más el puerto por el que están ejecutándose.
En caso de presentarse un error, se debe correr la imagen que se lista como 'Exited' en modo iterativo, y ver cuáles son los conflictos que denota el código.

# Pasos para desplegar la aplicacion web
1. Se crea una maquina virtual
2. Clonar el repositorio con el proyecto
3. Se instalan previamente los programas necesarios para el despliegue de la aplicacion (sudo apt install docker-compose)
4. Se ejecuta en archivo .csv con el comando 'bash despliegue_contenedor.csv'
5. Se visualiza la página con la IP pública de la instancia

# Inconvenientes
Se presenta un error de URL dado por una equívoca redirección al servidor que contiene el login, esto se produce por problemas en el código del front.py ya que es el archivo que no logra tener estado Up.
