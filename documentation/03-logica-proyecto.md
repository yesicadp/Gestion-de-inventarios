# 3. Lógica del proyecto

## Funcionamiento general

El sistema sigue una arquitectura monolítica por capas, en la que el frontend interactúa con el backend y este se comunica con la base de datos MySQL.

El funcionamiento general contempla los siguientes pasos:

1. El usuario accede al sistema mediante un navegador web.
2. El frontend presenta las opciones disponibles para interactuar con el inventario.
3. El frontend envía solicitudes al backend.
4. El backend recibe y procesa las solicitudes.
5. La lógica de negocio aplica las validaciones y reglas correspondientes.
6. La capa de acceso a datos consulta o modifica la información almacenada en MySQL.
7. El backend devuelve los resultados al frontend para su visualización.

## Procesos principales del sistema

### Autenticación y gestión de usuarios

Este proceso contempla el control de acceso al sistema mediante credenciales de usuario.

Las funcionalidades previstas incluyen:

- Inicio y cierre de sesión.
- Validación de credenciales.
- Administración de usuarios.
- Asignación de roles.
- Control de permisos según el rol del usuario.

Los roles definidos en la estructura de la base de datos permiten diferenciar los tipos de usuario del sistema.

### Gestión de productos

Permite administrar la información de los productos registrados en el inventario.

Las operaciones contempladas son:

- Registrar nuevos productos.
- Consultar productos existentes.
- Modificar información de los productos.
- Desactivar productos.
- Consultar las existencias actuales y mínimas.

Cada producto se encuentra asociado a una categoría.

### Clasificación por categorías

Permite organizar los productos mediante categorías y subcategorías.

La estructura de la base de datos contempla la relación jerárquica entre categorías, facilitando la clasificación y consulta de los productos.

### Consulta de inventario

Permite consultar las cantidades disponibles de los productos.

La información contempla:

- Existencia actual.
- Existencia mínima.
- Estado del producto.
- Identificación de productos con existencias inferiores al mínimo establecido.

### Movimientos de inventario

Este proceso contempla el registro de entradas y salidas de productos.

El funcionamiento previsto es:

1. Identificar el producto relacionado con el movimiento.
2. Validar el tipo de movimiento y la cantidad.
3. Verificar que una salida no supere las existencias disponibles.
4. Actualizar las existencias del producto.
5. Registrar el movimiento asociado al usuario.
6. Conservar la información del movimiento para su consulta posterior.

La tabla `movimientos` almacena información como el producto, usuario, tipo de movimiento, cantidad, motivo, fecha y existencia resultante.

Se realizaron pruebas manuales mediante SQL para verificar operaciones de entrada y salida utilizando transacciones y rollback.

### Búsqueda y filtrado

El sistema contempla mecanismos para facilitar la localización de información relacionada con productos, categorías y movimientos.

Se consideran criterios como:

- Nombre del producto.
- Código del producto.
- Categoría.
- Estado del producto.
- Tipo de movimiento.
- Fechas de los movimientos.

### Auditoría

La base de datos cuenta con una tabla `auditoria`, destinada a almacenar información relacionada con las operaciones realizadas en el sistema.

Su estructura contempla:

- Usuario asociado a la operación.
- Módulo.
- Acción realizada.
- Fecha.
- Detalle de la operación.

**Estado actual:** la estructura de auditoría y sus relaciones están creadas y verificadas. Sin embargo, el registro automático de las operaciones y su integración con el backend se encuentran pendientes.

## Reglas de negocio

Las siguientes reglas orientan el funcionamiento esperado del sistema:

- Un producto no puede tener existencias negativas.
- La cantidad de un movimiento debe ser mayor que cero.
- Una salida no puede superar las existencias disponibles.
- Los movimientos deben estar asociados a un producto y a un usuario.
- Los productos pueden organizarse mediante categorías y subcategorías.
- Las existencias actuales deben mantenerse coherentes con los movimientos registrados.
- El acceso a las funcionalidades debe depender de los roles y permisos definidos.
- Las operaciones relevantes deben contar con mecanismos de auditoría.

## Consideraciones de implementación

La estructura de la base de datos incorpora restricciones de integridad para proteger la información, incluyendo validaciones sobre existencias y cantidades de movimientos.

Las pruebas realizadas en el Sprint 3 permitieron verificar manualmente operaciones de entrada y salida mediante SQL. Estas pruebas no representan una validación completa de los procesos desde la interfaz de la aplicación.

La integración automática de auditoría y la verificación de los procesos funcionales restantes continúan pendientes.
