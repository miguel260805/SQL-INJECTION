# SQL-INJECTION
# Práctica: Vulnerabilidad de Inyección SQL (SQLi)

**Institución:** ESCOM - IPN | **Asignatura:** Bases de Datos
**Desarrollador:** Juárez Bobadilla Miguel Isaí

---

## 1. ¿Cómo se creó y qué hace este proyecto?
Este proyecto nació como una práctica de laboratorio para demostrar de forma controlada cómo funciona un ataque de Inyección SQL (SQLi). 

El sistema simula un portal de acceso (login) para una biblioteca. Su funcionamiento consiste en recibir un usuario y contraseña a través de un formulario HTML, consultar esos datos en una base de datos y, dependiendo del resultado, otorgar o denegar el acceso. La finalidad del proyecto es mostrar visualmente cómo un atacante puede evadir esta seguridad escribiendo código SQL directamente en la caja de texto.

## 2. ¿Qué hace el código Python (`app.py`)?
El archivo `app.py` es el corazón del proyecto. Hace tres cosas fundamentales paso a paso:
1. **Prepara la base de datos:** Al iniciar, utiliza la librería `sqlite3` para crear una base de datos local en memoria. Crea una tabla llamada `usuarios` e inserta un administrador con una contraseña secreta.
2. **Levanta el servidor web:** Utiliza el framework `Flask` para montar la página web y mostrar el formulario HTML en el navegador.
3. **Genera la vulnerabilidad:** Recibe lo que el usuario escribe en el formulario y lo pega (concatena) directamente en la consulta SQL. Como no filtra los caracteres especiales, permite que el texto ingresado altere la instrucción original de la base de datos.

## 3. Dockerización: ¿Cómo, por qué y para qué?
* **¿Por qué fue necesario?** Para evitar el problema de "en mi máquina sí funciona". Si el profesor intenta correr el proyecto de Python puro, tendría que instalar Python, instalar Flask y configurar su entorno.
* **¿Para qué sirve?** Docker empaqueta la aplicación con todo lo que necesita para funcionar de manera aislada. 
* **¿Cómo se hizo?** Se crearon dos archivos:
  * `Dockerfile`: Le dice a Docker que descargue una imagen de Python, instale Flask y copie nuestro archivo `app.py`.
  * `docker-compose.yml`: Se encarga de levantar ese contenedor y conectar el puerto 80 del contenedor al puerto `8080` de nuestra computadora para poder verlo en el navegador.

## 4. ¿Cómo arranca el proyecto?
Para levantar el servidor y la base de datos, solo necesitas tener Docker Desktop abierto y ejecutar (dando clic derecho en el archivo `docker-compose.yml` y seleccionando "Compose Up"):

```bash
docker-compose up -d
