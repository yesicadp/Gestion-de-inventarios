# 6. Historias de usuario

**Formato:** Como [rol], quiero [funcionalidad], para [beneficio u objetivo].

## Roles del sistema

- **Administrador:** rol previsto para acceder a las funcionalidades administrativas del sistema.
- **Usuario:** rol previsto para acceder a las funcionalidades operativas de consulta y movimientos.

**Nota sobre los permisos:** aunque los roles están definidos en la base de datos y se incluyen en el token JWT, el decorador `requiere_token` actualmente valida la autenticación, pero no implementa restricciones diferenciadas por rol. Por lo tanto, los roles descritos en las historias representan el comportamiento esperado y no implican que todos los permisos estén aplicados en el backend.

## Estados de implementación

- **Implementada:** la funcionalidad principal está disponible en el código revisado.
- **Parcialmente implementada:** existe una parte funcional, pero faltan uno o más criterios de aceptación.
- **Pendiente:** no se encontró una implementación funcional correspondiente en el backend revisado.

---

## Módulo: Autenticación

### HU-01 — Iniciar sesión

Como **Usuario o Administrador**, quiero iniciar sesión con mi correo o usuario y contraseña, para acceder a las funcionalidades del sistema según mi rol.

*Criterios de aceptación:*
- Si las credenciales son correctas, el sistema redirige al panel principal.
- Si son incorrectas, el sistema muestra un mensaje de error sin indicar cuál dato falló (usuario o contraseña).
- El menú y las opciones disponibles varían según el rol autenticado.

**Estado: Parcialmente implementada.**

El backend cuenta con `POST /api/auth/login`, que recibe las credenciales, valida la contraseña mediante bcrypt y genera un token JWT. Se utiliza el correo electrónico como identificador. La redirección al panel y la visualización diferenciada de opciones según el rol no se verificaron como parte de este endpoint.

### HU-02 — Cerrar sesión

Como **Usuario o Administrador**, quiero cerrar mi sesión, para proteger el acceso a mi cuenta cuando termino de usar el sistema.

*Criterios de aceptación:*
- Al cerrar sesión, se invalida la sesión o token y se redirige a la pantalla de inicio de sesión.

**Estado: Pendiente.**

No se identificó un endpoint de cierre de sesión ni un mecanismo de invalidación de tokens en el backend revisado. Los tokens JWT tienen una vigencia de 30 minutos.

---

## Módulo: General

### HU-03 — Ver panel principal (dashboard)

Como **Usuario o Administrador**, quiero ver un panel con un resumen general del inventario (totales, alertas y últimos movimientos), para tener visibilidad rápida del estado del sistema al ingresar.

*Criterios de aceptación:*
- Muestra el total de productos, existencias bajas, movimientos del día y categorías activas.
- Muestra una lista de alertas de productos con existencias por debajo del mínimo.
- Muestra los últimos movimientos registrados.

**Estado: Pendiente.**

No se identificó un endpoint específico para el dashboard ni una implementación de los indicadores descritos en el backend revisado.

---

## Módulo: Productos

### HU-04 — Consultar listado de productos

Como **Usuario**, quiero ver el listado de productos con búsqueda y filtros (categoría y estado), para encontrar la información que necesito sin revisar todo el catálogo.

*Criterios de aceptación:*
- La búsqueda filtra por nombre o código.
- Se puede filtrar por categoría y por estado (activo/inactivo).
- El listado es paginado.

**Estado: Parcialmente implementada.**

Existe `GET /api/productos`, que consulta y devuelve el listado de productos con su categoría, existencia actual, existencia mínima y estado. No se identificaron parámetros de búsqueda, filtros ni paginación en esta ruta.

### HU-05 — Registrar nuevo producto

Como **Administrador**, quiero registrar un nuevo producto con su categoría, existencia inicial y existencia mínima, para incorporarlo al inventario.

*Criterios de aceptación:*
- Campos obligatorios: nombre, código/SKU, categoría y existencia inicial.
- No permite guardar si el código ya existe.
- El producto queda visible de inmediato en el listado.

**Estado: Parcialmente implementada.**

Existe `POST /api/productos`, que valida los datos recibidos y registra el producto. La operación contempla la validación de duplicidad del código mediante las restricciones de la base de datos. No se identificó una comprobación de rol Administrador en el decorador de autenticación.

### HU-06 — Editar producto

Como **Administrador**, quiero editar la información de un producto existente, para mantener sus datos actualizados.

*Criterios de aceptación:*
- Se pueden modificar todos los campos excepto el código/SKU, o aplicar la regla que defina el equipo.
- Los cambios quedan reflejados en el listado y en el inventario.

**Estado: Parcialmente implementada.**

Existe `PUT /api/productos/{id_producto}`, que permite actualizar información del producto. La restricción de acceso exclusivo al Administrador no está implementada en el decorador de autenticación revisado.

### HU-07 — Desactivar producto

Como **Administrador**, quiero desactivar un producto en lugar de eliminarlo, para dejar de gestionarlo sin perder su historial de movimientos.

*Criterios de aceptación:*
- Un producto inactivo no aparece disponible para nuevos movimientos.
- El historial de movimientos previos se conserva.

**Estado: Parcialmente implementada.**

La actualización de productos contempla el campo `estado`, y el registro de movimientos verifica que el producto esté activo. No se identificó una ruta independiente de desactivación ni una restricción de rol Administrador.

---

## Módulo: Categorías

### HU-08 — Crear categorías y subcategorías

Como **Administrador**, quiero crear categorías y subcategorías, para organizar y clasificar los productos.

*Criterios de aceptación:*
- Una categoría puede tener cero o más subcategorías.
- El nombre de categoría es obligatorio y no se puede repetir en el mismo nivel.

**Estado: Parcialmente implementada.**

Existe `POST /api/categorias`, que permite registrar categorías y asociar una categoría padre mediante `categoria_padre_id`. El backend valida el nombre y evita nombres duplicados. No se identificó una restricción de acceso exclusiva para el Administrador.

### HU-09 — Editar o eliminar categoría

Como **Administrador**, quiero editar o eliminar una categoría, para mantener la clasificación actualizada.

*Criterios de aceptación:*
- No se puede eliminar una categoría que tenga productos asociados sin antes reasignarlos o confirmarlo explícitamente.

**Estado: Pendiente.**

No se identificaron endpoints para editar o eliminar categorías en el backend revisado.

### HU-10 — Ver productos agrupados por categoría

Como **Usuario**, quiero ver los productos agrupados por categoría, para ubicarlos más fácilmente al buscar algo específico.

*Criterios de aceptación:*
- Al seleccionar una categoría, se listan solo los productos asociados a ella y sus subcategorías.

**Estado: Parcialmente implementada.**

El listado de productos incluye información de la categoría asociada. Sin embargo, no se identificó un filtro por categoría ni una operación que agrupe los productos por categoría y subcategorías.

---

## Módulo: Inventario

### HU-11 — Consultar existencias actuales

Como **Usuario**, quiero consultar las existencias actuales de cada producto, para saber cuánto stock hay disponible antes de tomar una decisión.

*Criterios de aceptación:*
- Muestra existencia actual, existencia mínima configurada y estado (disponible/bajo mínimo).
- Permite buscar por producto.

**Estado: Parcialmente implementada.**

Existe `GET /api/inventario`, que devuelve las existencias actuales, mínimas y un indicador de existencia baja para productos activos. No se identificó un parámetro de búsqueda por producto en esta ruta.

### HU-12 — Alertas de existencia baja

Como **Usuario o Administrador**, quiero ver una alerta cuando un producto tenga existencias por debajo del mínimo configurado, para reponer stock a tiempo.

*Criterios de aceptación:*
- La alerta se calcula automáticamente comparando la existencia actual con la mínima.
- Es visible tanto en el panel principal como en la consulta de inventario.

**Estado: Parcialmente implementada.**

El endpoint `GET /api/inventario` calcula el indicador de existencia baja comparando la existencia actual con la mínima y devuelve el total de productos en esa condición. La condición implementada considera existencia baja cuando la cantidad actual es menor o igual al mínimo. No se verificó su visualización en un dashboard.

---

## Módulo: Movimientos

### HU-13 — Registrar entrada de inventario

Como **Usuario**, quiero registrar una entrada de inventario, para aumentar la existencia de un producto cuando llega mercancía.

*Criterios de aceptación:*
- Requiere producto, cantidad (mayor que cero) y motivo.
- Al guardar, la existencia del producto se incrementa automáticamente.

**Estado: Implementada en el backend.**

Existe `POST /api/movimientos`, que permite registrar movimientos de tipo entrada, valida que la cantidad sea un entero mayor que cero y actualiza la existencia del producto dentro de una transacción. También registra el movimiento y su existencia resultante. La autorización diferenciada por rol no está implementada en el decorador revisado.

### HU-14 — Registrar salida de inventario

Como **Usuario**, quiero registrar una salida de inventario, para disminuir la existencia de un producto cuando se despacha o se consume.

*Criterios de aceptación:*
- No permite registrar una salida mayor a la existencia disponible.
- Al guardar, la existencia del producto se disminuye automáticamente.

**Estado: Implementada en el backend.**

Existe `POST /api/movimientos`, que permite registrar movimientos de tipo salida. El backend verifica la existencia disponible, evita salidas superiores al stock y actualiza la existencia dentro de una transacción. También registra el movimiento y su existencia resultante. La autorización diferenciada por rol no está implementada en el decorador revisado.

### HU-15 — Consultar historial de movimientos

Como **Usuario o Administrador**, quiero consultar el historial de movimientos de uno o varios productos, para conocer su trazabilidad en el tiempo.

*Criterios de aceptación:*
- Se puede filtrar por producto, tipo de movimiento (entrada/salida) y rango de fechas.
- Cada registro muestra fecha, usuario, producto, tipo, cantidad y existencia resultante.

**Estado: Parcialmente implementada.**

Existe `GET /api/movimientos`, que devuelve los movimientos registrados con información del producto, usuario, tipo, cantidad, motivo, fecha y existencia resultante. No se identificaron parámetros para filtrar por producto, tipo o rango de fechas.

---

## Módulo: Búsqueda

### HU-16 — Buscar productos por nombre o código

Como **Usuario**, quiero buscar productos por nombre o código, para encontrarlos rápidamente sin recorrer todo el listado.

*Criterios de aceptación:*
- La búsqueda responde con coincidencias parciales, no solo exactas.

**Estado: Pendiente.**

No se identificaron parámetros de búsqueda por nombre o código en el endpoint de listado de productos.

### HU-17 — Filtrar información por criterios combinados

Como **Usuario**, quiero filtrar productos y movimientos por categoría, estado o rango de fechas, para acotar la información que reviso.

*Criterios de aceptación:*
- Los filtros se pueden combinar entre sí (por ejemplo: categoría + estado).

**Estado: Pendiente.**

No se identificaron mecanismos de filtros combinados en los endpoints de productos y movimientos revisados.

---

## Módulo: Auditoría

### HU-18 — Registro automático de auditoría

Como **Administrador**, quiero que cada operación relevante (creación, edición y movimiento) registre automáticamente el usuario y la fecha, para garantizar trazabilidad sin depender de que alguien lo indique manualmente.

*Criterios de aceptación:*
- El registro se genera del lado del servidor y no puede editarse desde el frontend.

**Estado: Pendiente.**

La base de datos cuenta con la tabla `auditoria` y sus relaciones e índices. Sin embargo, no se identificó una integración del backend que registre automáticamente las operaciones en dicha tabla.

### HU-19 — Consultar registro de auditoría

Como **Administrador**, quiero consultar el registro de auditoría de las operaciones del sistema, para saber quién hizo qué y cuándo.

*Criterios de aceptación:*
- Es accesible únicamente para el rol Administrador.
- Permite filtrar por usuario, módulo y rango de fechas.

**Estado: Pendiente.**

No se identificó un endpoint para consultar los registros de auditoría ni mecanismos de filtrado o autorización por rol para esta funcionalidad.

---

## Módulo: Usuarios y permisos (solo Administrador)

### HU-20 — Crear usuario con rol asignado

Como **Administrador**, quiero crear cuentas de usuario asignándoles un rol (Administrador o Usuario), para controlar quién accede al sistema y con qué permisos.

*Criterios de aceptación:*
- No se puede crear un usuario con un correo ya registrado.
- El rol asignado determina las opciones que ve el usuario al iniciar sesión.

**Estado: Pendiente.**

La base de datos contiene las tablas `usuarios` y `roles`, y el inicio de sesión consulta la relación entre ambas. No se identificó un endpoint para crear usuarios ni para asignar roles.

### HU-21 — Editar datos y rol de un usuario

Como **Administrador**, quiero editar los datos y el rol de un usuario existente, para mantener actualizada la información de acceso del equipo.

**Estado: Pendiente.**

No se identificó un endpoint para actualizar usuarios o modificar sus roles.

### HU-22 — Desactivar usuario

Como **Administrador**, quiero desactivar un usuario, para revocar su acceso sin eliminar su historial de acciones en el sistema.

*Criterios de aceptación:*
- Un usuario inactivo no puede iniciar sesión.
- Sus acciones previas se conservan en la auditoría.

**Estado: Parcialmente implementada.**

El inicio de sesión verifica el campo `estado` del usuario y rechaza el acceso cuando está inactivo. No se identificó un endpoint para desactivar usuarios ni una integración de auditoría para conservar automáticamente el historial de acciones.

### HU-23 — Ver listado de usuarios y roles

Como **Administrador**, quiero ver la lista de usuarios del sistema y su rol asignado, para tener visibilidad de quién tiene acceso.

**Estado: Pendiente.**

No se identificó un endpoint para consultar el listado de usuarios y sus roles.

---

## Resumen del estado de las historias de usuario

Los estados se asignan con base en la revisión del código fuente del backend incluido en el proyecto.

| Estado | Cantidad |
|---|---:|
| Implementadas en el backend | 2 |
| Parcialmente implementadas | 12 |
| Pendientes | 9 |
| **Total** | **23** |

**Consideraciones:**

- Que una historia esté implementada en el backend no significa que se haya verificado todo su flujo desde la interfaz de usuario.
- Las historias parcialmente implementadas cuentan con una parte funcional, pero no cumplen todos sus criterios de aceptación.
- Las historias pendientes se conservan porque representan funcionalidades previstas para el alcance del proyecto.
- La autorización diferenciada por roles, el cierre de sesión, la auditoría automática y la administración de usuarios continúan como aspectos pendientes.
- La clasificación debe actualizarse cuando se implementen y prueben nuevas funcionalidades.
