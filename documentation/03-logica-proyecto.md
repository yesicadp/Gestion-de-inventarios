# 3. Lógica del proyecto

## Funcionamiento general

El sistema utiliza una arquitectura monolítica modular por capas, en la que el frontend interactúa con el backend mediante solicitudes HTTP y este se comunica con la base de datos MySQL.

El funcionamiento general contempla los siguientes pasos:

1. El usuario accede al sistema mediante un navegador web.
2. El frontend presenta las interfaces disponibles.
3. El frontend envía solicitudes HTTP a la API REST.
4. El backend recibe y procesa las solicitudes.
5. La lógica de negocio realiza las validaciones correspondientes.
6. La capa de acceso a datos consulta o modifica la información almacenada en MySQL.
7. El backend devuelve una respuesta en formato JSON para que el frontend actualice la información presentada.

## Procesos principales del sistema

### Autenticación y gestión de usuarios

El sistema cuenta con un mecanismo de autenticación mediante credenciales de usuario.

**Funcionalidades implementadas:**

- Inicio de sesión mediante correo y contraseña.
- Verificación de credenciales.
- Protección de contraseñas mediante bcrypt.
- Generación de tokens JWT para identificar al usuario autenticado.
- Validación de tokens en las rutas protegidas.
- Consulta del perfil del usuario autenticado.

**Funcionalidades pendientes:**

- Cierre de sesión con invalidación del token.
- Administración de usuarios mediante endpoints.
- Asignación y modificación de roles desde la API.
- Control de permisos diferenciados según el rol del usuario.

Los roles definidos en la base de datos permiten establecer la estructura de usuarios del sistema. Sin embargo, la autorización diferenciada por roles todavía no está implementada en el mecanismo de protección de rutas.

### Gestión de productos

Este proceso permite administrar la información de los productos registrados en el inventario.

**Operaciones implementadas en el backend:**

- Registrar nuevos productos.
- Consultar la lista de productos.
- Consultar un producto por su identificador.
- Actualizar la información de un producto.
- Validar la información recibida y evitar códigos duplicados.

La estructura de productos contempla información como código, nombre, categoría, existencias actuales, existencias mínimas y estado.

**Pendiente:** completar y verificar las funcionalidades adicionales de administración, incluyendo la desactivación de productos desde la interfaz.

Cada producto se encuentra asociado a una categoría mediante una relación definida en la base de datos.

### Clasificación por categorías

Este proceso permite organizar los productos mediante categorías y subcategorías.

**Operaciones implementadas en el backend:**

- Consultar categorías.
- Registrar categorías.
- Registrar subcategorías mediante la relación con una categoría padre.

La estructura de la base de datos contempla una relación jerárquica entre categorías, permitiendo organizar los productos de acuerdo con su clasificación.

**Pendiente:** implementar y verificar las operaciones de modificación y eliminación de categorías.

### Consulta de inventario

Este proceso permite consultar las cantidades disponibles de los productos.

La información contempla:

- Existencia actual.
- Existencia mínima.
- Estado del producto.
- Identificación de productos con stock bajo.

El backend dispone de un endpoint para consultar el inventario y determinar cuáles productos presentan existencias iguales o inferiores al mínimo establecido.

### Movimientos de inventario

Este proceso permite registrar entradas y salidas de productos, manteniendo actualizadas las existencias.

El funcionamiento implementado en el backend es:

1. Identificar el producto relacionado con el movimiento.
2. Validar el tipo de movimiento y la cantidad recibida.
3. Verificar que la cantidad sea mayor que cero.
4. Comprobar que una salida no supere las existencias disponibles.
5. Actualizar las existencias del producto.
6. Registrar el movimiento asociado al producto y al usuario.
7. Almacenar la fecha, el motivo y la existencia resultante.
8. Confirmar la transacción en la base de datos.

El registro de movimientos se realiza mediante transacciones para mantener la coherencia entre la actualización de existencias y el almacenamiento del movimiento.

La tabla `movimientos` almacena información como:

- Producto relacionado.
- Usuario responsable.
- Tipo de movimiento.
- Cantidad.
- Motivo.
- Fecha.
- Existencia resultante.

El backend dispone de operaciones para registrar movimientos y consultar su historial.

**Pruebas de base de datos:** durante el Sprint 3 se realizaron pruebas manuales mediante SQL para verificar entradas, salidas y reversión de cambios utilizando `ROLLBACK`.

Estas pruebas permitieron comprobar el comportamiento de las operaciones directamente en la base de datos, sin representar una validación completa del flujo desde la interfaz web.

### Búsqueda y filtrado

El sistema contempla mecanismos para facilitar la localización de información relacionada con productos, categorías y movimientos.

Se consideran criterios como:

- Nombre del producto.
- Código del producto.
- Categoría.
- Estado del producto.
- Tipo de movimiento.
- Fechas de los movimientos.

**Estado actual:** aunque existen consultas para obtener productos y movimientos, no se identificaron endpoints específicos para aplicar todos los filtros descritos. Su implementación y verificación permanecen pendientes.

### Auditoría

La base de datos cuenta con una tabla `auditoria`, destinada a almacenar información relacionada con las operaciones realizadas en el sistema.

Su estructura contempla:

- Usuario asociado a la operación.
- Módulo.
- Acción realizada.
- Fecha.
- Detalle de la operación.

Durante el Sprint 4 se verificaron la estructura de la tabla, sus relaciones e índices.

**Estado actual:** el registro automático de operaciones y su integración con el backend están pendientes. Tampoco se identificaron endpoints para consultar los registros de auditoría.

## Reglas de negocio

Las siguientes reglas orientan el funcionamiento del sistema y se encuentran respaldadas por validaciones del backend o restricciones de la base de datos, según corresponda:

| Regla | Implementación |
|---|---|
| Un producto no puede tener existencias negativas. | Restricción CHECK en la base de datos. |
| La cantidad de un movimiento debe ser mayor que cero. | Validación en el backend y restricción CHECK. |
| Una salida no puede superar las existencias disponibles. | Validación en el backend. |
| Los movimientos deben estar asociados a un producto y a un usuario. | Relaciones y claves foráneas. |
| Los productos pueden organizarse mediante categorías y subcategorías. | Relación entre categorías y productos. |
| Las existencias deben mantenerse coherentes con los movimientos registrados. | Actualización transaccional en el backend. |
| El acceso a las funcionalidades debe depender de los roles y permisos definidos. | Pendiente de implementación completa. |
| Las operaciones relevantes deben contar con mecanismos de auditoría. | Estructura creada; registro automático pendiente. |

## Consideraciones de implementación

La base de datos incorpora restricciones de integridad para proteger la información y evitar registros inconsistentes, incluyendo validaciones sobre existencias y cantidades de movimientos.

El backend implementa operaciones para la autenticación, gestión de productos, categorías, consulta de inventario y movimientos.

Las pruebas realizadas durante el Sprint 3 permitieron verificar manualmente operaciones de entrada y salida mediante SQL. Durante el Sprint 4 se revisó la estructura de auditoría y los índices de la base de datos.

La implementación de permisos diferenciados por roles, la integración automática de auditoría, los filtros específicos y la verificación de los procesos funcionales restantes continúan pendientes.

Para consultar el detalle de las rutas disponibles y su estado de implementación, revisar `04-arquitectura.md`.
