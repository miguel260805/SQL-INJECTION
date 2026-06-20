# SQL-INJECTION
# Laboratorio de Ciberseguridad: Explotación de Vulnerabilidad SQL Injection (SQLi)

Entorno de pruebas controlado (Sandbox) diseñado para la demostración técnica de vulnerabilidades de seguridad en bases de datos relacionales. El sistema permite auditar la evasión de mecanismos de autenticación mediante la inyección directa de sentencias lógicas en el backend, documentando el ciclo completo desde la falla hasta su remediación.

**Institución:** Instituto Politécnico Nacional (IPN) - ESCOM
**Asignatura:** Bases de Datos
**Autor:** Juárez Bobadilla Miguel Isaí

---

## Enlaces del Proyecto

* **Código Fuente:** [Repositorio en GitHub](https://github.com/miguel260805/SQL-INJECTION)

---

## Tecnologías Implementadas

* **Backend:** Python con el microframework Flask.
* **Persistencia:** SQLite en memoria (entorno volátil y reproducible).
* **Orquestación:** Docker y `docker-compose`, mapeado al puerto local `8080`.
* **Clasificación de la Vulnerabilidad:** CWE-89 (Improper Neutralization of Special Elements used in an SQL Command).

---

## Evolución y Metodología de la Práctica

El desarrollo de este laboratorio se fundamenta en una metodología de ingeniería estructurada, abarcando desde el diseño de la arquitectura vulnerable hasta la ejecución documentada del vector de ataque y su corrección.

### Fase 1: Arquitectura y Levantamiento del Entorno

Para garantizar un entorno reproducible, aislado y libre de conflictos de dependencias, se implementó una arquitectura basada en contenedores (Docker).

* **Backend:** Desarrollo en `Python` utilizando el microframework `Flask` para la gestión de peticiones HTTP.
* **Persistencia:** Motor `SQLite` configurado en memoria, garantizando la volatilidad de los datos para reiniciar el estado de la prueba en cada ejecución.
* **Orquestación:** Despliegue automatizado mediante `docker-compose`, mapeando el servicio al puerto local `8080`.

Durante el despliegue inicial, el sistema construye dinámicamente la entidad `usuarios` (id, usuario, password, rol) y aprovisiona un registro oculto con privilegios de administrador.

<div align="center">
  <img loading="lazy" src="Imagenes/Documentacion/arquitectura.png" alt="Arquitectura del entorno" width="700"/>
  <br>
  <em>Figura 1: Arquitectura del entorno de pruebas (Flask + SQLite + Docker).</em>
</div>

### Fase 2: Análisis de la Vulnerabilidad (Código Falla)

La vulnerabilidad crítica (Clasificación CWE-89) reside en la capa de acceso a datos del backend (`app.py`). El sistema procesa los datos del cliente sin aplicar sanitización ni utilizar *Prepared Statements* (Consultas Parametrizadas).

El texto crudo capturado en el formulario HTML se concatena de forma directa en la instrucción DML, permitiendo la manipulación de la consulta:

```sql
-- Estructura SQL vulnerable implementada en el backend:
SELECT * FROM usuarios WHERE usuario = '{usuario_input}' AND password = '{password_input}'
```

El problema central es que `{usuario_input}` y `{password_input}` se insertan tal cual el usuario los escribió, sin ningún tratamiento previo. Cualquier carácter de control SQL (como una comilla simple) rompe la estructura que el desarrollador tenía en mente.

<div align="center">
  <img loading="lazy" src="Imagenes/Documentacion/codigo-vulnerable.png" alt="Código vulnerable" width="700"/>
  <br>
  <em>Figura 2: Fragmento de app.py donde se concatena la entrada del usuario sin sanitizar.</em>
</div>

### Fase 3: Vector de Ataque (Explotación)

El atacante no necesita conocer la contraseña: le basta con alterar la **lógica booleana** de la cláusula `WHERE` para que siempre se evalúe como verdadera, anulando por completo la verificación de la contraseña.

Un payload clásico para el campo `usuario` tiene la forma:

```
' OR '1'='1' --
```

Al insertarse en la plantilla original, la consulta que finalmente recibe el motor de base de datos queda estructurada así:

```sql
SELECT * FROM usuarios WHERE usuario = '' OR '1'='1' --' AND password = '...'
```

| Fragmento | Función |
|---|---|
| `'` | Cierra prematuramente la cadena de `usuario`, rompiendo la sintaxis esperada. |
| `OR '1'='1'` | Introduce una condición que siempre es verdadera, sin importar el valor real. |
| `--` | Comenta el resto de la sentencia original (incluida la verificación de `password`), neutralizándola. |

Como la cláusula `WHERE` se evalúa como verdadera para cualquier fila, el motor retorna el primer registro de la tabla `usuarios` —típicamente la cuenta administrativa— concediendo acceso sin conocer credenciales válidas.

<div align="center">
  <img loading="lazy" src="Imagenes/Documentacion/explotacion.png" alt="Evidencia de explotación" width="700"/>
  <br>
  <em>Figura 3: Acceso obtenido al inyectar el payload en el formulario de login.</em>
</div>

### Fase 4: Remediación (Implementación Segura)

La corrección estructural consiste en separar el **código SQL** de los **datos del usuario**, delegando al driver de base de datos el escapado seguro mediante **Prepared Statements** (consultas parametrizadas). De este modo, el contenido ingresado por el usuario nunca se interpreta como sintaxis SQL, sin importar qué caracteres contenga.

```python
# Antes (vulnerable):
query = f"SELECT * FROM usuarios WHERE usuario = '{usuario_input}' AND password = '{password_input}'"
cursor.execute(query)

# Después (remediado):
query = "SELECT * FROM usuarios WHERE usuario = ? AND password = ?"
cursor.execute(query, (usuario_input, password_input))
```

Con esta implementación, el payload `' OR '1'='1' --` deja de tener efecto: el motor de base de datos lo trata como un valor literal de texto a buscar en la columna `usuario`, no como código ejecutable.

**Medidas complementarias:**

* **Hash de contraseñas** (p. ej. bcrypt/argon2) en lugar de texto plano.
* **Principio de mínimo privilegio** en la cuenta de base de datos usada por la aplicación.
* **Validación de entrada** como capa adicional (defensa en profundidad), nunca como única protección.

<div align="center">
  <img loading="lazy" src="Imagenes/Documentacion/remediacion.png" alt="Código remediado" width="700"/>
  <br>
  <em>Figura 4: Consulta parametrizada bloqueando el payload de inyección.</em>
</div>

---

## Galería del Sistema

<details>
<summary>Ver capturas de pantalla del laboratorio</summary>

| Formulario de Login (Vulnerable) | Acceso No Autorizado Obtenido |
|:---:|:---:|
| <img loading="lazy" src="Imagenes/Documentacion/login.png" alt="Login" width="400"/> | <img loading="lazy" src="Imagenes/Documentacion/acceso.png" alt="Acceso obtenido" width="400"/> |

| Consulta Vulnerable en Logs | Consulta Remediada en Logs |
|:---:|:---:|
| <img loading="lazy" src="Imagenes/Documentacion/log-vulnerable.png" alt="Log vulnerable" width="400"/> | <img loading="lazy" src="Imagenes/Documentacion/log-remediado.png" alt="Log remediado" width="400"/> |

</details>

---

## Cómo Ejecutar el Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/miguel260805/SQL-INJECTION.git
cd SQL-INJECTION

# Levantar el entorno con Docker
docker-compose up --build

# La aplicación quedará disponible en:
# http://localhost:8080
```

---

## Conclusiones

Este laboratorio evidencia que una vulnerabilidad de inyección SQL no requiere herramientas sofisticadas para ser explotada: basta con comprender cómo el backend construye sus consultas. Al mismo tiempo, demuestra que la remediación es, en la mayoría de los casos, sencilla de implementar mediante consultas parametrizadas. La práctica refuerza la importancia de tratar toda entrada del usuario como no confiable por defecto, principio fundamental del desarrollo seguro de software.
