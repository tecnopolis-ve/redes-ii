
# Subastas WebApp Readme

Esta es la documentación del proyecto web Subastas, una plataforma abierta a todo el público y especialmente dirigida a aquellas pequeñas empresas que se dedican a la venta de obras de arte y otros objetos de colección para que puedan contar con una plataforma tecnológica que les permita fácil y rápido llegar a más clientes así como gestionar de forma eficiente sus eventos y demás procesos relativos al negocio.

## Pasos previos

Es necesario tener **Docker** y **Docker composer** instalado en el equipo donde se ejecutará la aplicación, esta plataforma permite simplificar la portabilidad y ofrecer un marco de trabajo unificado para todos los miembros del equipo de desarrollo.

`curl -sSL https://get.docker.com | sh`

`sudo usermod -aG docker ${USER}`

`sudo apt-get install haveged -y`

## Comandos más comunes (Linux)

### Inicializar el contenedor
Inicializar el contenedor para poder levantar los servicios

`docker-compose up -d`

Una vez levantado el contenedor, se deberá crear una base de datos vacía llamada `subastarte_db`, luego de la creación de la base de datos, se deberán ejecutar en orden los siguientes comandos:

### Generar archivos de migración inicial
`docker-compose exec web python manage.py migrate`

### Creación de un superusuario

Se desplegará un asistente que te guiará por todo el proceso.

`docker-compose exec web python manage.py createsuperuser`

### Ejecución de las migraciones
*Nota: [nombre] es siempre opcional.*

 1. `docker-compose exec web python manage.py makemigrations [nombre]`
 2. `docker-compose exec web python manage.py migrate [nombre]`

### Comandos varios

Levantar el contenedor:
`docker-compose start`

Reiniciar el contenedor:
`docker-compose restart`

Detener el contenedor:
`docker-compose stop`


