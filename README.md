# SQL-INJECTION

# Demostración de Vulnerabilidad - Inyección SQL (SQLi)

Entorno de pruebas controlado enfocado en la demostración técnica de vulnerabilidades de seguridad en bases de datos relacionales. El sistema permite explorar cómo se ejecuta y explota una inyección SQL evadiendo la autenticación mediante la manipulación directa de consultas de backend.

**Institución:** ESCOM - IPN | **Práctica:** Laboratorio de Inyección SQL

## Equipo de Desarrollo

* Juárez Bobadilla Miguel Isaí

---

## Evolución y Metodología de la Práctica

El desarrollo de este laboratorio se llevó a cabo siguiendo un enfoque estructurado de ciberseguridad ofensiva básica, partiendo desde el levantamiento de un entorno vulnerable hasta la explotación de la falla.

### Fase 1: Arquitectura y Levantamiento del Entorno
Para garantizar que la prueba sea reproducible sin conflictos de dependencias, se construyó una arquitectura 100% "dockerizada". Se definieron las siguientes herramientas:

* **Backend:** Construido en `Python` utilizando el microframework `Flask`.
* **Base de Datos:** Motor `SQLite` persistido en memoria para asegurar la destrucción y recreación del estado en cada prueba.
* **Orquestación:** Configuración mediante `docker-compose` para levantar el contenedor web mapeado al puerto `8080`.

Al inicializar, el sistema crea dinámicamente la entidad `usuarios` (id, usuario, password, rol) e inserta un registro administrativo base.

### Fase 2: Análisis de la Vulnerabilidad (Código Falla)
La falla crítica de seguridad radica en la capa del backend (archivo `app.py`). El sistema sufre de validación nula de entradas, ya que concatena el texto crudo del formulario directamente hacia el motor de la base de datos en lugar de utilizar *Prepared Statements*.

```sql
-- Estructura vulnerable implementada en el código:
SELECT * FROM usuarios WHERE usuario = '{usuario_input}' AND password = '{password_input}'
