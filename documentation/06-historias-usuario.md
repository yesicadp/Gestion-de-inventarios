# 6. Historias de usuario

Formato: **Como** [rol] **quiero** [funcionalidad] **para** [beneficio/objetivo].

Roles del sistema: **Administrador** (acceso total) y **Usuario** (acceso operativo — consulta, movimientos, búsqueda).

---

## Módulo: Autenticación

**HU-01 — Iniciar sesión**
Como **Usuario o Administrador**, quiero iniciar sesión con mi correo/usuario y contraseña, para acceder a las funcionalidades del sistema según mi rol.
*Criterios de aceptación:*
- Si las credenciales son correctas, el sistema redirige al panel principal.
- Si son incorrectas, el sistema muestra un mensaje de error sin indicar cuál dato falló (usuario o contraseña).
- El menú y las opciones disponibles varían según el rol autenticado.

**HU-02 — Cerrar sesión**
Como **Usuario o Administrador**, quiero cerrar mi sesión, para proteger el acceso a mi cuenta cuando termino de usar el sistema.
*Criterios de aceptación:*
- Al cerrar sesión, se invalida la sesión/token y se redirige a la pantalla de login.

---

## Módulo: General

**HU-03 — Ver panel principal (dashboard)**
Como **Usuario o Administrador**, quiero ver un panel con un resumen general del inventario (totales, alertas, últimos movimientos), para tener visibilidad rápida del estado del sistema al ingresar.
*Criterios de aceptación:*
- Muestra el total de productos, existencias bajas, movimientos del día y categorías activas.
- Muestra una lista de alertas de productos con existencias por debajo del mínimo.
- Muestra los últimos movimientos registrados.

---

## Módulo: Productos

**HU-04 — Consultar listado de productos**
Como **Usuario**, quiero ver el listado de productos con búsqueda y filtros (categoría, estado), para encontrar la información que necesito sin revisar todo el catálogo.
*Criterios de aceptación:*
- La búsqueda filtra por nombre o código.
- Se puede filtrar por categoría y por estado (activo/inactivo).
- El listado es paginado.

**HU-05 — Registrar nuevo producto**
Como **Administrador**, quiero registrar un nuevo producto con su categoría, existencia inicial y existencia mínima, para incorporarlo al inventario.
*Criterios de aceptación:*
- Campos obligatorios: nombre, código/SKU, categoría, existencia inicial.
- No permite guardar si el código ya existe.
- El producto queda visible de inmediato en el listado.

**HU-06 — Editar producto**
Como **Administrador**, quiero editar la información de un producto existente, para mantener sus datos actualizados.
*Criterios de aceptación:*
- Se pueden modificar todos los campos excepto el código/SKU (o definir regla del equipo).
- Los cambios quedan reflejados inmediatamente en el listado y en el inventario.

**HU-07 — Desactivar producto**
Como **Administrador**, quiero desactivar un producto en lugar de eliminarlo, para dejar de gestionarlo sin perder su historial de movimientos.
*Criterios de aceptación:*
- Un producto inactivo no aparece disponible para nuevos movimientos.
- El historial de movimientos previos se conserva.

---

## Módulo: Categorías

**HU-08 — Crear categorías y subcategorías**
Como **Administrador**, quiero crear categorías y subcategorías, para organizar y clasificar los productos.
*Criterios de aceptación:*
- Una categoría puede tener cero o más subcategorías.
- El nombre de categoría es obligatorio y no se puede repetir en el mismo nivel.

**HU-09 — Editar o eliminar categoría**
Como **Administrador**, quiero editar o eliminar una categoría, para mantener la clasificación actualizada.
*Criterios de aceptación:*
- No se puede eliminar una categoría que tenga productos asociados sin antes reasignarlos o confirmarlo explícitamente.

**HU-10 — Ver productos agrupados por categoría**
Como **Usuario**, quiero ver los productos agrupados por categoría, para ubicarlos más fácilmente al buscar algo específico.
*Criterios de aceptación:*
- Al seleccionar una categoría, se listan solo los productos asociados a ella (y sus subcategorías).

---

## Módulo: Inventario

**HU-11 — Consultar existencias actuales**
Como **Usuario**, quiero consultar las existencias actuales de cada producto, para saber cuánto stock hay disponible antes de tomar una decisión.
*Criterios de aceptación:*
- Muestra existencia actual, existencia mínima configurada y estado (disponible / bajo mínimo).
- Permite buscar por producto.

**HU-12 — Alertas de existencia baja**
Como **Usuario o Administrador**, quiero ver una alerta cuando un producto tenga existencias por debajo del mínimo configurado, para reponer stock a tiempo.
*Criterios de aceptación:*
- La alerta se calcula automáticamente comparando existencia actual vs. mínimo.
- Es visible tanto en el panel principal como en la consulta de inventario.

---

## Módulo: Movimientos

**HU-13 — Registrar entrada de inventario**
Como **Usuario**, quiero registrar una entrada de inventario, para aumentar la existencia de un producto cuando llega mercancía.
*Criterios de aceptación:*
- Requiere producto, cantidad (mayor a 0) y motivo.
- Al guardar, la existencia del producto se incrementa automáticamente.

**HU-14 — Registrar salida de inventario**
Como **Usuario**, quiero registrar una salida de inventario, para disminuir la existencia de un producto cuando se despacha o se consume.
*Criterios de aceptación:*
- No permite registrar una salida mayor a la existencia disponible.
- Al guardar, la existencia del producto se disminuye automáticamente.

**HU-15 — Consultar historial de movimientos**
Como **Usuario o Administrador**, quiero consultar el historial de movimientos de uno o varios productos, para conocer su trazabilidad en el tiempo.
*Criterios de aceptación:*
- Se puede filtrar por producto, tipo de movimiento (entrada/salida) y rango de fechas.
- Cada registro muestra fecha, usuario, producto, tipo, cantidad y existencia resultante.

---

## Módulo: Búsqueda

**HU-16 — Buscar productos por nombre o código**
Como **Usuario**, quiero buscar productos por nombre o código, para encontrarlos rápidamente sin recorrer todo el listado.
*Criterios de aceptación:*
- La búsqueda responde con coincidencias parciales, no solo exactas.

**HU-17 — Filtrar información por criterios combinados**
Como **Usuario**, quiero filtrar productos y movimientos por categoría, estado o rango de fechas, para acotar la información que reviso.
*Criterios de aceptación:*
- Los filtros se pueden combinar entre sí (ej. categoría + estado).

---

## Módulo: Auditoría

**HU-18 — Registro automático de auditoría**
Como **Administrador**, quiero que cada operación relevante (creación, edición, movimiento) registre automáticamente el usuario y la fecha, para garantizar trazabilidad sin depender de que alguien lo indique manualmente.
*Criterios de aceptación:*
- El registro se genera del lado del servidor (no editable desde el frontend).

**HU-19 — Consultar registro de auditoría**
Como **Administrador**, quiero consultar el registro de auditoría de las operaciones del sistema, para saber quién hizo qué y cuándo.
*Criterios de aceptación:*
- Accesible solo para el rol Administrador.
- Permite filtrar por usuario, módulo y rango de fechas.

---

## Módulo: Usuarios y permisos (solo Administrador)

**HU-20 — Crear usuario con rol asignado**
Como **Administrador**, quiero crear cuentas de usuario asignándoles un rol (Administrador o Usuario), para controlar quién accede al sistema y con qué permisos.
*Criterios de aceptación:*
- No se puede crear un usuario con un correo ya registrado.
- El rol asignado determina de inmediato qué opciones ve el usuario al iniciar sesión.

**HU-21 — Editar datos y rol de un usuario**
Como **Administrador**, quiero editar los datos y el rol de un usuario existente, para mantener actualizada la información de acceso del equipo.

**HU-22 — Desactivar usuario**
Como **Administrador**, quiero desactivar un usuario, para revocar su acceso sin eliminar su historial de acciones en el sistema.
*Criterios de aceptación:*
- Un usuario inactivo no puede iniciar sesión.
- Sus acciones previas se conservan en la auditoría.

**HU-23 — Ver listado de usuarios y roles**
Como **Administrador**, quiero ver la lista de usuarios del sistema y su rol asignado, para tener visibilidad de quién tiene acceso.