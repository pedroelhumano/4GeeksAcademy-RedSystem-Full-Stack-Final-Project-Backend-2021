# RedSystem - Final Project 4GeeksAcademy Backend

### Descripción
<p>Proyecto basado en una empresa ficticia de telecomunicaciones la cual se encargá de administrar sus contratos de trabajo, donde cada contrato tiene además órdenes específicas o actividades por hacer.</p>

### Características
- Sistema de usuarios.
- CRUD completo
- Encriptación con JWT
- Frontend creado con React
- Validación del RUN/RUT
- Responsive
- Manejo de tokens
- Formulario de contacto

### Instrucciones para ejecutar

Este repositorio debe ejecutarse en conjunto con el repositorio `4GA-RedSystem-Full-Stack-Final-Project-Frontend`
- Ejecutar el proyecto desde gitpod.
- Ejecutar los comandos
```
pipenv shell
pipenv install flask-jwt-extended
```
- Borrar la BD: Ejecutar el siguiente comando en la terminal
```
psql
```
- Entrará en un terminal diferente, que solo recibe peticiones SQL. Ejecutar los siguientes comandos, uno a la vez
```
UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'example';
ALTER DATABASE example CONNECTION LIMIT 1;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'example';
DROP DATABASE example;
EXIT
```
- Luego eliminar TODA la carpeta migrations
- Luego hacer lo que dice el archivo gitpod.yml
```
psql -U gitpod -c 'CREATE DATABASE example;';
psql -U gitpod -c 'CREATE EXTENSION unaccent;' -d example;
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
```
- Ejecutar el proyecto
```
pipenv run start
```
- Colocar los puertos como públicos

<hr/>

### Main Developers
[![Contribuidores](https://contrib.rocks/image?repo=wotanCode/4GeeksAcademy-RedSystem-Full-Stack-Final-Project-Backend-2021&max=500&columns=5)](https://github.com/wotanCode/4GeeksAcademy-RedSystem-Full-Stack-Final-Project-Backend-2021/graphs/contributors)
