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
