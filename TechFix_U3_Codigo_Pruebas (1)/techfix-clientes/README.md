# TechFix Manager — Gestión de clientes

Ingeniería de Software · Grupo 13 · Unidad 3, semanas 9–12.
Integrante identificado en el documento base: Jorge Rafael Manobanda Alba.

## Alcance
Registro, búsqueda por identificación exacta, consulta de detalle y corrección autorizada de clientes. Campos: identificación, nombres, teléfono, correo y dirección. Implementa el alcance de RF-01 y la parte de clientes de RF-18 del documento facilitado. RN-P del plan son reglas de implementación propuestas. No se incluye equipos, ventas, inventario ni reparaciones.

Capas: formularios/plantillas y vistas → servicios → DAO y ORM → SQLite. La identificación es textual; no hay validación de dígito verificador de cédula. Se conserva el modelo incremental del proyecto.

## Instalación Windows (PowerShell)
Desde la carpeta que contiene este README:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/manage.py migrate
.\.venv\Scripts\python.exe src/manage.py createsuperuser
.\.venv\Scripts\python.exe src/manage.py runserver
```
Crear una contraseña propia, no incluirla en Git. Abrir http://127.0.0.1:8000/ e iniciar sesión. El superusuario permite probar el flujo autorizado. Para CP-A02 crear además una cuenta con permiso view_cliente sin change_cliente; se puede administrar usuarios añadiendo el admin de Django o desde manage.py shell. No usar datos reales para estas pruebas.

En Linux: `python3 -m venv .venv` y `.venv/bin/python`.
La configuración es de desarrollo. DJANGO_SECRET_KEY permite conservar una clave privada estable entre reinicios. Sin esa variable se genera una clave temporal. No se carga .env automáticamente.

## Estructura
| Archivo/carpeta | Función |
|---|---|
| src/clientes/models.py | Modelo Cliente y unicidad |
| src/clientes/services.py | Validación, autorización y transacciones |
| src/clientes/dao.py | Guardado y consulta por ORM |
| src/clientes/forms.py | Formulario validado |
| src/clientes/views.py y templates/ | Pantallas y solicitudes HTTP |
| src/clientes/migrations/ | Esquema versionado |
| src/clientes/tests/test_clientes.py | Diez pruebas automáticas |
| docs/pruebas/ | Plan de Semana 11 |
| docs/evidencias/ | Salida real local y pendientes |
| .github/workflows/ci.yml | Comprobaciones y pruebas por push y PR |

## Pruebas
```powershell
.\.venv\Scripts\python.exe src/manage.py test clientes --verbosity 2 --noinput
```
El runner crea una base SQLite exclusiva de pruebas. No usa los clientes de la base de desarrollo. CP-I01 usa TransactionTestCase para permitir que se confirme la transacción del servicio. La suite tiene cinco unitarias del plan, tres de integración del plan y dos pruebas HTTP adicionales. Las adicionales NO reemplazan CP-A01 y CP-A02, que requieren recorrido en navegador y registro de evidencia.

Resultado local observado: 10 pruebas, OK, código de salida 0. CP-I01 también fue ejecutado por separado: 1 prueba, OK. La salida íntegra está en docs/evidencias/ejecucion_local_semana12.txt.

## GitHub Flow
main conserva la base revisada; cada cambio se desarrolla en una rama. La rama inicial es feature/estructura-clientes y la de este avance es feature/automatizar-clientes. Guardar commits pequeños, subir rama, abrir PR, revisar diferencias, esperar CI verde y fusionar. Los commits iniciales mantienen su autoría de preparación asistida. Configurar el nombre y correo propios para nuevos commits.

## CI
El workflow instala las dependencias, revisa Django y migraciones, ejecuta CP-I01 por separado y después la suite. Un comando fallido detiene el job con error. Se activa por push, pull_request y workflow_dispatch.

## Estado real
- Implementación, migración, pruebas y workflow: preparados.
- Verificación local de configuración, migraciones y diez pruebas: satisfactoria.
- CP-A01 y CP-A02 en navegador: pendientes.
- Repositorio remoto accesible, pull request y ejecución Actions: pendientes.
- PDF madre de la Unidad 2: no suministrado en este trabajo; integrar cuando esté disponible.

## Publicación del historial
El paquete incluye techfix-clientes.bundle con main y ramas. Ver PASOS_GITHUB.md, fuera de esta carpeta. No crear un historial nuevo si se desea conservar las evidencias de semanas previas.

## Fuentes
- https://docs.djangoproject.com/en/5.2/topics/testing/overview/
- https://docs.djangoproject.com/en/5.2/topics/testing/tools/
- https://docs.github.com/en/get-started/using-github/github-flow
- https://docs.github.com/en/actions/tutorials/build-and-test-code/python
