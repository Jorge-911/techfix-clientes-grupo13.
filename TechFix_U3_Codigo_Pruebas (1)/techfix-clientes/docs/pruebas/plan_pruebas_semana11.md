# Ingeniería de Software · Semana 11 · Avance 3

## Plan
Se probará Gestión de clientes de TechFix Manager: validación de datos, registro y persistencia, rechazo de duplicados, corrección autorizada y flujo del usuario. Se considerará aprobado el alcance de este plan cuando los 10 casos estén ejecutados y aprobados (100 %), incluido CP-I01, sin fallos abiertos en registro, integridad o permisos. Un caso bloqueado o no ejecutado impide la aprobación.

Estado inicial: los 10 casos están No ejecutados. Son especificaciones para implementar y automatizar en la Semana 12; no se presentan como pruebas ya realizadas. La estructura de la Semana 10 aún no contiene el registro funcional de clientes.

## Datos D1
Identificación: TEST-CLI-001; nombres: Ana Prueba; teléfono: 0990000001; correo: ana.prueba@example.com; dirección: Calle de Prueba 100.

## Reglas propuestas
- RN-P01: Identificación y nombres son obligatorios, incluso cuando contienen solo espacios.
- RN-P02: Si se proporciona correo, debe tener formato válido. No se exige correo obligatorio.
- RN-P03: Quitar espacios exteriores de identificación y aplicar unicidad al valor normalizado.
- RN-P04: Verificar permiso antes de cualquier modificación, también con acceso directo a una dirección.
- RN-P05: Los mensajes exactos del plan son contratos propuestos para la interfaz y la validación.

## Casos de prueba

### CP-U01 — Rechazar identificación vacía

**Nivel:** Unitaria

**Requisito:** RF-01; RNF-08

**Prioridad:** Alta

**Precondiciones:** Función de validación aislada, sin base de datos ni servidor.

**Entrada:** Datos D1, reemplazando identificación por tres espacios.

**Pasos:** 1. Pasar el valor a la validación de identificación. 2. Evaluar el resultado.

**Esperado:** Devuelve rechazo y el error «La identificación es obligatoria». No devuelve una identificación válida.

**Reglas:** RN-P01

**Estado:** No ejecutado.

### CP-U02 — Rechazar nombres vacíos

**Nivel:** Unitaria

**Requisito:** RF-01; RNF-08

**Prioridad:** Alta

**Precondiciones:** Función de validación de nombres aislada.

**Entrada:** Datos D1, con nombres = "".

**Pasos:** 1. Invocar la validación de nombres. 2. Revisar el error obtenido.

**Esperado:** Devuelve rechazo y el error «Los nombres son obligatorios».

**Reglas:** RN-P01

**Estado:** No ejecutado.

### CP-U03 — Rechazar correo mal formado

**Nivel:** Unitaria

**Requisito:** RF-01; RNF-08

**Prioridad:** Media

**Precondiciones:** Validador de correo aislado; sin consultas a datos.

**Entrada:** Correo: ana.prueba@ (resto de campos de D1).

**Pasos:** 1. Enviar el correo al validador. 2. Comprobar el resultado.

**Esperado:** Rechaza el valor y devuelve «Ingrese un correo electrónico válido».

**Reglas:** RN-P02

**Estado:** No ejecutado.

### CP-U04 — Normalizar identificación válida

**Nivel:** Unitaria

**Requisito:** RF-01; RNF-08

**Prioridad:** Alta

**Precondiciones:** Función de normalización aislada.

**Entrada:** Identificación: "  TEST-CLI-001  ".

**Pasos:** 1. Invocar la normalización. 2. Comparar exactamente el valor retornado.

**Esperado:** Devuelve "TEST-CLI-001", sin espacios al inicio ni al final y sin alterar los caracteres internos.

**Reglas:** RN-P03

**Estado:** No ejecutado.

### CP-U05 — Denegar modificación sin permiso

**Nivel:** Unitaria

**Requisito:** RF-18 parcial; RNF-02; RNF-10

**Prioridad:** Alta

**Precondiciones:** Regla de autorización aislada con usuario simulado; sin autenticación real ni base de datos.

**Entrada:** Usuario autenticado simulado; permiso cambiar_cliente = falso.

**Pasos:** 1. Evaluar si el usuario puede modificar clientes. 2. Inspeccionar la decisión de autorización.

**Esperado:** La regla devuelve falso. No autoriza la modificación.

**Reglas:** RN-P04

**Estado:** No ejecutado.

### CP-I01 — Persistir y recuperar un cliente válido

**Nivel:** Integración

**Requisito:** RF-01

**Prioridad:** Crítica

**Precondiciones:** Servicio, DAO y ORM conectados a una base exclusiva de pruebas, con esquema creado. No existe D1. Contexto de usuario autorizado.

**Entrada:** D1 completo.

**Pasos:** 1. Contar clientes: N. 2. Registrar D1 mediante el servicio y confirmar la transacción. 3. Descartar el objeto en memoria. 4. Consultar de nuevo con DAO/ORM por identificación.

**Esperado:** Existen N+1 clientes; la búsqueda retorna exactamente una fila con clave primaria no nula y los cinco campos iguales a D1.

**Reglas:** RN-P01; RN-P03

**Estado:** No ejecutado.

### CP-I02 — Evitar cliente duplicado

**Nivel:** Integración

**Requisito:** RF-01; RNF-08

**Prioridad:** Alta

**Precondiciones:** Base de pruebas con D1 ya registrado una sola vez. Usuario autorizado.

**Entrada:** D1 repetido, con identificación "  TEST-CLI-001  ".

**Pasos:** 1. Contar filas existentes. 2. Intentar registrar el duplicado mediante el servicio. 3. Consultar nuevamente la cantidad y D1.

**Esperado:** El servicio rechaza con «Ya existe un cliente con esta identificación». La cantidad total no aumenta; permanece una sola fila TEST-CLI-001 y sus datos originales.

**Reglas:** RN-P03

**Estado:** No ejecutado.

### CP-I03 — Guardar corrección autorizada

**Nivel:** Integración

**Requisito:** RF-18 parcial

**Prioridad:** Alta

**Precondiciones:** D1 persistido. Usuario con permiso cambiar_cliente. Guardar su clave primaria original.

**Entrada:** Nuevo teléfono: 0990000002. Los demás datos de D1 se conservan.

**Pasos:** 1. Solicitar actualización del teléfono por el servicio. 2. Confirmar la transacción. 3. Recuperar el cliente nuevamente con DAO/ORM.

**Esperado:** El teléfono recuperado es 0990000002; se conserva la clave primaria, la cantidad de clientes y los otros cuatro campos.

**Reglas:** RN-P04

**Estado:** No ejecutado.

### CP-A01 — Registrar, consultar y corregir desde la interfaz

**Nivel:** Aceptación

**Requisito:** RF-01; RF-18 parcial; RNF-04

**Prioridad:** Alta

**Precondiciones:** Aplicación iniciada; usuario de prueba con permisos de alta, consulta y modificación; D1 no existe.

**Entrada:** D1; luego teléfono 0990000002.

**Pasos:** 1. Iniciar sesión. 2. Abrir Clientes > Nuevo. 3. Completar D1 y guardar. 4. Buscar TEST-CLI-001 y abrir su detalle. 5. Editar teléfono y guardar. 6. Recargar y consultar el detalle.

**Esperado:** Se muestra «Cliente registrado correctamente». La búsqueda presenta un único cliente. Tras editar aparece «Cliente actualizado correctamente» y, al recargar, se muestra 0990000002; los otros datos no cambian.

**Reglas:** RN-P04; RN-P05

**Estado:** No ejecutado.

### CP-A02 — Impedir edición a un usuario no autorizado

**Nivel:** Aceptación

**Requisito:** RF-18 parcial; RNF-02; RNF-10

**Prioridad:** Alta

**Precondiciones:** D1 existe con teléfono 0990000001. Dos cuentas: una sin permiso cambiar_cliente y otra autorizada.

**Entrada:** Cuenta sin permiso; intento de cambiar teléfono a 0990000002 desde la URL de edición de D1.

**Pasos:** 1. Iniciar sesión con la cuenta sin permiso. 2. Abrir directamente la dirección de edición. 3. Intentar guardar si existe formulario. 4. Consultar D1 con la cuenta autorizada.

**Esperado:** La interfaz muestra «No tiene permiso para modificar clientes» y no permite guardar. La consulta autorizada mantiene 0990000001 y todos los demás datos originales.

**Reglas:** RN-P04; RN-P05

**Estado:** No ejecutado.

## Caso crítico
CP-I01: verifica la persistencia y recuperación completa de un cliente; automatizar primero en Semana 12.

## Fuentes y límites
SRS suministrado: U1_EstudioDeCaso_Grupo13 ...pdf, pp. 7-8. RF-18 se cubre solo para clientes. RN-P son reglas propuestas. No se ejecutaron pruebas. Identificación TEST-CLI-001 es textual ficticia, no cédula válida. Restablecer datos antes de cada caso.
