# SQL-INJECTION

# Laboratorio de Ciberseguridad: Explotación de Vulnerabilidad SQL Injection (SQLi)

Entorno de pruebas controlado (Sandbox) diseñado para la demostración técnica de vulnerabilidades de seguridad en bases de datos relacionales. El sistema permite auditar la evasión de mecanismos de autenticación mediante la inyección directa de sentencias lógicas en el backend.

**Institución:** Instituto Politécnico Nacional (IPN) - ESCOM  
**Asignatura:** Bases de Datos  
**Autor:** Juárez Bobadilla Miguel Isaí  

---

## Evolución y Metodología de la Práctica

El desarrollo de este laboratorio se fundamenta en una metodología de ingeniería estructurada, abarcando desde el diseño de la arquitectura vulnerable hasta la ejecución documentada del vector de ataque.

### Fase 1: Arquitectura y Levantamiento del Entorno

Para garantizar un entorno reproducible, aislado y libre de conflictos de dependencias, se implementó una arquitectura basada en contenedores (Docker). 

* **Backend:** Desarrollo en `Python` utilizando el microframework `Flask` para la gestión de peticiones HTTP.
* **Persistencia:** Motor `SQLite` configurado en memoria, garantizando la volatilidad de los datos para reiniciar el estado de la prueba en cada ejecución.
* **Orquestación:** Despliegue automatizado mediante `docker-compose`, mapeando el servicio al puerto local `8080`.

Durante el despliegue inicial, el sistema construye dinámicamente la entidad `usuarios` (id, usuario, password, rol) y aprovisiona un registro oculto con privilegios de administrador.

### Fase 2: Análisis de la Vulnerabilidad (Código Falla)

La vulnerabilidad crítica (Clasificación CWE-89) reside en la capa de acceso a datos del backend (`app.py`). El sistema procesa los datos del cliente sin aplicar sanitización ni utilizar *Prepared Statements* (Consultas Parametrizadas). 

El texto crudo capturado en el formulario HTML se concatena de forma directa en la instrucción DML, permitiendo la manipulación de la consulta:

```sql
-- Estructura SQL vulnerable implementada en el backend:
SELECT * FROM usuarios WHERE usuario = '{usuario_input}' AND password = '{password_input}'= '{password_input}'
# Laboratorio de Ciberseguridad: Explotación de Vulnerabilidad SQL Injection (SQLi)

Entorno de pruebas controlado (Sandbox) diseñado para la demostración técnica de vulnerabilidades de seguridad en bases de datos relacionales. El sistema permite auditar la evasión de mecanismos de autenticación mediante la inyección directa de sentencias lógicas en el backend, así como su posterior remediación aplicando buenas prácticas de desarrollo seguro.

**Institución:** Instituto Politécnico Nacional (IPN) - ESCOM
**Asignatura:** Bases de Datos
**Autor:** Juárez Bobadilla Miguel Isaí

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Objetivos](#objetivos)
3. [Fundamento Teórico](#fundamento-teórico)
4. [Metodología](#evolución-y-metodología-de-la-práctica)
   - [Fase 1: Arquitectura y Levantamiento del Entorno](#fase-1-arquitectura-y-levantamiento-del-entorno)
   - [Fase 2: Análisis de la Vulnerabilidad](#fase-2-análisis-de-la-vulnerabilidad-código-falla)
   - [Fase 3: Vector de Ataque (Explotación)](#fase-3-vector-de-ataque-explotación)
   - [Fase 4: Remediación](#fase-4-remediación-implementación-segura)
5. [Cómo Ejecutar el Proyecto](#cómo-ejecutar-el-proyecto)
6. [Conclusiones](#conclusiones)
7. [Referencias](#referencias)

---

## Descripción General

Este proyecto documenta, de forma íntegra y reproducible, el ciclo de vida completo de una vulnerabilidad de tipo **SQL Injection (CWE-89)**: desde el diseño de un sistema deliberadamente inseguro, pasando por su explotación controlada, hasta la aplicación de la corrección correspondiente. El objetivo no es ofensivo, sino pedagógico: comprender a fondo por qué ocurre esta clase de fallas para poder prevenirlas en sistemas reales.

## Objetivos

- Comprender el origen técnico de las vulnerabilidades de inyección SQL en aplicaciones web.
- Levantar un entorno aislado y reproducible mediante contenedores.
- Documentar el comportamiento de una consulta SQL construida por concatenación de cadenas.
- Explicar el razonamiento lógico detrás de un vector de evasión de autenticación.
- Aplicar y justificar la remediación mediante *Prepared Statements* (consultas parametrizadas).

## Fundamento Teórico

La inyección SQL ocurre cuando una aplicación construye una consulta hacia la base de datos concatenando directamente datos proporcionados por el usuario, sin separar el **código** (la instrucción SQL) de los **datos** (lo que escribió el usuario). El motor de base de datos no tiene forma de distinguir entre ambos, por lo que interpreta como parte de la sentencia cualquier carácter especial (comillas, operadores lógicos, comentarios) que el atacante incluya en el campo de entrada.

Esta clase de vulnerabilidad está catalogada bajo **CWE-89: Improper Neutralization of Special Elements used in an SQL Command**, y es consistentemente listada como uno de los riesgos más críticos en el [OWASP Top 10](https://owasp.org/www-project-top-ten/).

---

## Evolución y Metodología de la Práctica

El desarrollo de este laboratorio se fundamenta en una metodología de ingeniería estructurada, abarcando desde el diseño de la arquitectura vulnerable hasta la ejecución documentada del vector de ataque y su corrección.

### Fase 1: Arquitectura y Levantamiento del Entorno

Para garantizar un entorno reproducible, aislado y libre de conflictos de dependencias, se implementó una arquitectura basada en contenedores (Docker).

- **Backend:** Desarrollo en `Python` utilizando el microframework `Flask` para la gestión de peticiones HTTP.
- **Persistencia:** Motor `SQLite` configurado en memoria, garantizando la volatilidad de los datos para reiniciar el estado de la prueba en cada ejecución.
- **Orquestación:** Despliegue automatizado mediante `docker-compose`, mapeando el servicio al puerto local `8080`.

Durante el despliegue inicial, el sistema construye dinámicamente la entidad `usuarios` (id, usuario, password, rol) y aprovisiona un registro oculto con privilegios de administrador.

### Fase 2: Análisis de la Vulnerabilidad (Código Falla)

La vulnerabilidad crítica (Clasificación CWE-89) reside en la capa de acceso a datos del backend (`app.py`). El sistema procesa los datos del cliente sin aplicar sanitización ni utilizar *Prepared Statements* (Consultas Parametrizadas).

El texto crudo capturado en el formulario HTML se concatena de forma directa en la instrucción DML, permitiendo la manipulación de la consulta:

```sql
-- Estructura SQL vulnerable implementada en el backend:
SELECT * FROM usuarios WHERE usuario = '{usuario_input}' AND password = '{password_input}'
```

El problema central es que `{usuario_input}` y `{password_input}` se insertan tal cual el usuario los escribió, sin ningún tratamiento previo. Cualquier carácter de control SQL (como una comilla simple) rompe la estructura que el desarrollador tenía en mente.

### Fase 3: Vector de Ataque (Explotación)

> *(Sección a completar con tu evidencia real: capturas de pantalla, payload exacto utilizado y respuesta del servidor.)*

Conceptualmente, el atacante no necesita conocer la contraseña: le basta con alterar la **lógica booleana** de la cláusula `WHERE` para que siempre se evalúe como verdadera, o para anular por completo la verificación de la contraseña.

Un payload clásico para el campo `usuario` sería de la forma:

```
' OR '1'='1' --
```

Al insertarse en la plantilla original, la consulta que finalmente recibe el motor de base de datos queda estructurada así:

```sql
SELECT * FROM usuarios WHERE usuario = '' OR '1'='1' --' AND password = '...'
```

El razonamiento del ataque se descompone en tres elementos:

| Fragmento | Función |
|---|---|
| `'` | Cierra prematuramente la cadena de `usuario`, rompiendo la sintaxis esperada. |
| `OR '1'='1'` | Introduce una condición que siempre es verdadera, sin importar el valor real. |
| `--` | Comenta el resto de la sentencia original (incluida la verificación de `password`), neutralizándola. |

Como la cláusula `WHERE` se evalúa como verdadera para cualquier fila, el motor retorna el primer registro de la tabla `usuarios` —típicamente la cuenta administrativa— concediendo acceso sin conocer credenciales válidas.

**Evidencia documentada (a completar):**
- Captura de la solicitud HTTP enviada.
- Captura de la respuesta del servidor / sesión iniciada.
- Registro de la consulta efectivamente ejecutada (logs de SQLite/Flask).

### Fase 4: Remediación (Implementación Segura)

> *(Sección a completar con tu código de corrección real.)*

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

Medidas complementarias recomendadas:

- **Hash de contraseñas** (p. ej. bcrypt/argon2) en lugar de texto plano.
- **Principio de mínimo privilegio** en la cuenta de base de datos usada por la aplicación.
- **Validación de entrada** como capa adicional (defensa en profundidad), nunca como única protección.
- **WAF / Logging** para detectar patrones de inyección en producción.

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

> *(Ajusta esta sección según los comandos reales de tu `docker-compose.yml`.)*

## Conclusiones

Este laboratorio evidencia que una vulnerabilidad de inyección SQL no requiere herramientas sofisticadas para ser explotada: basta con comprender cómo el backend construye sus consultas. Al mismo tiempo, demuestra que la remediación es, en la mayoría de los casos, sencilla de implementar mediante consultas parametrizadas. La práctica refuerza la importancia de tratar toda entrada del usuario como no confiable por defecto, principio fundamental del desarrollo seguro de software.
