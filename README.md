## 5. Demostración Visual de la Vulnerabilidad (Pruebas)

Para comprobar el funcionamiento del sistema y su posterior vulneración, se documentaron los resultados en dos fases: el comportamiento normal esperado y la ejecución de la inyección.

### Fase A: Comportamiento Normal del Sistema

**Paso 1: Ingreso de credenciales erróneas**
<div align="center">
  <img loading="lazy" src="/Pruebas/IMAGENES/Prueba_Credenciales_Aleatorias.png" alt="Ingreso de credenciales aleatorias" width="800"/>
  <br>
  <em>Figura 1: Formulario recibiendo datos no registrados.</em>
</div>

<br>

**Paso 2: Rechazo del acceso**
<div align="center">
  <img loading="lazy" src="/Pruebas/IMAGENES/_Rechazo_Normal_Del_Sistema.png" alt="Rechazo del sistema" width="800"/>
  <br>
  <em>Figura 2: El sistema niega el acceso.</em>
</div>

### Fase B: Ejecución del Ataque (SQL Injection)

**Paso 3: Inyección de código malicioso**
<div align="center">
  <img loading="lazy" src="/Pruebas/IMAGENES/_Ingreso_Inyeccion_SQL.png" alt="Inyección de código SQL" width="800"/>
  <br>
  <em>Figura 3: Inserción de la sentencia lógica SQL.</em>
</div>

<br>

**Paso 4: Vulneración Exitosa**
<div align="center">
  <img loading="lazy" src="/Pruebas/IMAGENES/_Vulneracion_Exitosa_Acceso_Admin.png" alt="Acceso de administrador concedido" width="800"/>
  <br>
  <em>Figura 4: Bypass exitoso del login.</em>
</div>
