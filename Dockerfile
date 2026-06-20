# Usamos una imagen ligera de Python
FROM python:3.9-slim

# Creamos nuestro directorio de trabajo
WORKDIR /app

# Instalamos Flask (el servidor web para Python)
RUN pip install flask

# Copiamos nuestro código al contenedor
COPY app.py .

# Exponemos el puerto
EXPOSE 80

# Comando para ejecutar la app
CMD ["python", "app.py"]