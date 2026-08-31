# 3. Lógica del proyecto

## Funcionamiento general

1. El usuario accede al sistema mediante un navegador web.
2. El **frontend** presenta formularios, tablas, filtros y opciones según el rol del usuario autenticado.
3. El frontend envía solicitudes HTTP a la **API REST** (backend en Python).
4. La API verifica la autenticación (sesión/token), los permisos del rol y valida los datos recibidos.
5. Cada solicitud se dirige al módulo correspondiente (productos, categorías, inventario, movimientos, etc.).
6. La **capa de negocio** aplica las reglas del inventario (por ejemplo: no permitir existencias negativas, validar existencia mínima).
7. La **capa de acceso a datos** consulta o modifica la información almacenada en **MySQL**.
8. La API devuelve una respuesta en formato **JSON** y el frontend actualiza la interfaz sin recargar la página completa.

## Procesos principales del sistema

### Autenticación
- El usuario ingresa credenciales (correo/usuario + contraseña).
- El backend valida las credenciales y retorna una sesión/token junto con el rol del usuario.
- El frontend guarda la sesión y adapta el menú/las acciones visibles según el rol (Administrador o Usuario).

### Gestión de productos
- Registro de un nuevo producto con su categoría, existencia inicial y existencia mínima.
- Consulta, edición y desactivación (baja lógica, no eliminación física) de productos existentes.
- Cada producto queda asociado a una categoría y, opcionalmente, a un proveedor.

### Clasificación por categorías
- Las categorías pueden tener subcategorías.
- Un producto pertenece a una categoría (o subcategoría), lo que permite agrupar y filtrar.

### Consulta de inventario
- Muestra las existencias actuales de cada producto.
- Compara la existencia actual contra la existencia mínima configurada para generar alertas de "stock bajo".

### Movimientos de inventario (entradas y salidas)
- Al registrar un movimiento, el sistema:
  1. Valida que el producto exista y esté activo.
  2. Si es salida, valida que haya existencia suficiente.
  3. Actualiza la existencia del producto (incrementa en entradas, disminuye en salidas).
  4. Guarda el movimiento en el historial, con usuario, fecha, tipo y cantidad.

### Búsqueda y filtrado
- Disponible sobre productos, categorías y movimientos.
- Combina texto libre (nombre/código) con filtros estructurados (categoría, estado, rango de fechas).

### Auditoría
- Cada operación relevante (creación, edición, movimiento, cambios de usuario) registra: usuario que la ejecutó, fecha/hora y tipo de operación.
- Permite consultar el historial de cambios para trazabilidad.

## Reglas de negocio clave (propuestas iniciales)
- Un producto no puede tener existencia negativa.
- No se pueden registrar movimientos sobre productos inactivos.
- Solo el rol **Administrador** puede gestionar usuarios, roles y eliminar/desactivar productos o categorías.
- El rol **Usuario** puede consultar inventario, registrar movimientos y buscar/filtrar, pero no gestionar usuarios.
- Toda acción de creación, edición o movimiento debe quedar registrada para auditoría.