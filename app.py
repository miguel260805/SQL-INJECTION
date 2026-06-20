from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Función paso a paso para crear una base de datos falsa al iniciar
def inicializar_bd():
    if os.path.exists('biblioteca.db'):
        os.remove('biblioteca.db')
    conexion = sqlite3.connect('biblioteca.db')
    cursor = conexion.cursor()
    cursor.execute('CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT, password TEXT, rol TEXT)')
    # Insertamos al administrador secreto
    cursor.execute('INSERT INTO usuarios (usuario, password, rol) VALUES ("admin_escom", "clave_super_secreta_123", "Administrador de Sistemas")')
    conexion.commit()
    conexion.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        usuario_input = request.form['usuario']
        password_input = request.form['password']
        
        conexion = sqlite3.connect('biblioteca.db')
        cursor = conexion.cursor()
        
        # VULNERABILIDAD SQL INJECTION:
        # Concatenamos el texto del formulario directo a la consulta SQL sin sanitizar
        consulta_sql = f"SELECT * FROM usuarios WHERE usuario = '{usuario_input}' AND password = '{password_input}'"
        
        try:
            cursor.execute(consulta_sql)
            usuario_encontrado = cursor.fetchone()
            
            if usuario_encontrado:
                mensaje = f"<h3 style='color: green;'>¡Acceso Concedido! Bienvenido {usuario_encontrado[1]}. Tu rol es: {usuario_encontrado[3]}</h3>"
            else:
                mensaje = "<h3 style='color: red;'>Usuario o contraseña incorrectos.</h3>"
        except sqlite3.Error as error:
            # Mostramos el error de sintaxis en pantalla, lo cual es terrible en la vida real pero excelente para tu demostración
            mensaje = f"<h3 style='color: orange;'>Error de Base de Datos SQL: {error}</h3>"
            
    # El diseño HTML de la página
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Acceso al Sistema BiblioTech</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #2c3e50; color: #333; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { background: #ecf0f1; padding: 30px; border-radius: 8px; text-align: center; width: 300px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
            input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #bdc3c7; border-radius: 4px; }
            button { background-color: #2980b9; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Acceso a Biblioteca</h2>
            <form method="POST">
                <input type="text" name="usuario" placeholder="Usuario" required>
                <input type="password" name="password" placeholder="Contraseña">
                <button type="submit">Entrar</button>
            </form>
            <div>{{ mensaje|safe }}</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, mensaje=mensaje)

if __name__ == '__main__':
    inicializar_bd()
    # Levantamos el servidor en el puerto 80 del contenedor
    app.run(host='0.0.0.0', port=80)