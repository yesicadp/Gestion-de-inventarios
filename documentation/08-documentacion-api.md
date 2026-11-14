# 8. Documentación de la API (rutas, parámetros y respuestas)

Base local: `http://127.0.0.1:5000`. Formato: JSON UTF-8.

## Convenciones

- **Autenticación:** todas las rutas, salvo `POST /api/auth/login` y `GET /api/health`, exigen el encabezado `Authorization: Bearer <token>` (el token se obtiene en el login y dura 30 minutos).
- **Roles:** `Administrador` (acceso total) y `Usuario` (consulta, búsqueda y movimientos). El rol se lee del token y se valida en el backend.
- **Errores:** siempre `{ "mensaje": "texto" }` con el código HTTP correspondiente.
- **Fechas:** ISO 8601 sin zona horaria, por ejemplo `2026-11-14T10:30:00`. Los filtros `desde` y `hasta` usan `AAAA-MM-DD` y `hasta` incluye todo ese día.
- **Estado:** `1` (activo) o `0` (inactivo) al enviar datos; al consultar, el campo `estado` viene como lo guarda MySQL.

| Código | Cuándo |
|---|---|
| 200 / 201 | Consulta o actualización correcta / recurso creado |
| 400 | Datos o parámetros inválidos (la respuesta incluye el motivo en `mensaje`) |
| 401 | Falta el token, es inválido o expiró |
| 403 | El rol del usuario no permite esta acción |
| 404 | El recurso no existe |
| 409 | Conflicto: código o nombre duplicado, o producto inactivo |
| 500 | Error interno (el detalle queda en el log del servidor) |

## Resumen de rutas y permisos

| Método y ruta | Permiso | Descripción |
|---|---|---|
| `GET /api/productos` | Todos | Lista con búsqueda y filtros |
| `GET /api/productos/<id>` | Todos | Un producto |
| `POST /api/productos` | **Admin** | Crea un producto |
| `PUT /api/productos/<id>` | **Admin** | Edita un producto (incluye activar/desactivar con `estado`) |
| `GET /api/categorias` | Todos | Lista de categorías |
| `POST /api/categorias` | **Admin** | Crea una categoría o subcategoría |
| `GET /api/inventario` | Todos | Existencias de productos activos y alertas de existencia baja |
| `GET /api/movimientos` | Todos | Historial con filtros y paginación opcional |
| `POST /api/movimientos` | Todos | Registra una entrada o salida |
| `GET /api/auditoria` | **Admin** | Consulta el registro de auditoría |

## Productos

### `GET /api/productos`

Parámetros opcionales, combinables entre sí:

| Parámetro | Valores | Efecto |
|---|---|---|
| `q` | texto | Busca en nombre **o** código (coincidencia parcial) |
| `categoria_id` | entero | Productos de esa categoría y de sus subcategorías directas |
| `estado` | `activo`, `inactivo`, `todos` (también `1`/`0`) | Filtra por estado. Sin el parámetro devuelve todos |

```json
{
  "mensaje": "Productos consultados correctamente",
  "total": 1,
  "productos": [
    { "id_producto": 1, "nombre": "Teclado USB", "codigo": "PROD-001", "categoria_id": 2,
      "categoria": "Teclados", "existencia_actual": 7, "existencia_minima": 5, "estado": 1 }
  ]
}
```

### `GET /api/productos/<id>`
Devuelve `{ "mensaje": "...", "producto": { ...mismos campos... } }`. `404` si no existe.

### `POST /api/productos` (Administrador)
Cuerpo: `nombre`, `codigo`, `categoria_id` (obligatorios); `existencia_actual`, `existencia_minima` (opcionales, por defecto 0, no negativos); `estado` (opcional, por defecto 1).
Respuesta `201`: `{ "mensaje": "Producto registrado correctamente", "producto": { ... } }`.
Errores: `400` datos inválidos o categoría inexistente, `409` código repetido, `403` no es administrador.
Se registra la auditoría (`productos` / `CREAR`).

### `PUT /api/productos/<id>` (Administrador)
Cuerpo: `nombre`, `codigo`, `categoria_id`, `existencia_actual`, `existencia_minima`, `estado` (todos obligatorios). Respuesta `200`: `{ "mensaje": "Producto actualizado correctamente" }`.
Errores: `400`, `404` producto inexistente, `409` código usado por otro producto.
Auditoría solo si hubo cambios: acción `EDITAR`, `DESACTIVAR` (estado 1 a 0) o `ACTIVAR` (0 a 1), con el detalle de cada campo cambiado (`existencia_minima 5 -> 8`).

## Categorías

### `GET /api/categorias`
`{ "mensaje": "...", "total": 2, "categorias": [ { "id_categoria": 1, "nombre": "Periféricos", "categoria_padre_id": null } ] }`

### `POST /api/categorias` (Administrador)
Cuerpo: `nombre` (obligatorio), `categoria_padre_id` (opcional). Respuesta `201`: `{ "mensaje": "...", "categoria": { "id_categoria", "nombre", "categoria_padre_id" } }`.
Errores: `400` nombre vacío, `404` categoría padre inexistente, `409` nombre repetido. Auditoría: `categorias` / `CREAR`.

## Inventario

### `GET /api/inventario`
Solo productos **activos**. Parámetros opcionales:

| Parámetro | Valores | Efecto |
|---|---|---|
| `q` | texto | Busca en nombre o código |
| `categoria_id` | entero | Categoría y sus subcategorías directas |
| `existencia_baja` | `1` o `0` | `1` solo los que tienen existencia baja; `0` solo los que no |

**Regla de existencia baja:** `existencia_actual <= existencia_minima` (un producto en el mínimo exacto ya cuenta como bajo).

```json
{
  "mensaje": "Inventario consultado correctamente",
  "total": 2,
  "total_existencias_bajas": 1,
  "productos": [
    { "id_producto": 2, "codigo": "PROD-002", "nombre": "Mouse", "categoria_id": 1, "categoria": "Periféricos",
      "existencia_actual": 3, "existencia_minima": 5, "existencia_baja": 1 }
  ]
}
```
`total_existencias_bajas` cuenta dentro de los productos devueltos (el dashboard lo llama sin filtros).

## Movimientos

### `GET /api/movimientos`
Más reciente primero. Parámetros opcionales, combinables:

| Parámetro | Valores | Efecto |
|---|---|---|
| `producto_id`, `usuario_id` | entero | Filtra por producto o por quién lo registró |
| `tipo` | `ENTRADA`, `SALIDA` | Filtra por tipo |
| `desde`, `hasta` | `AAAA-MM-DD` | Rango de fechas (`hasta` incluye ese día) |
| `q` | texto | Busca en nombre o código del producto |
| `pagina`, `por_pagina` | enteros (`por_pagina` máx. 100) | Si se envía alguno, pagina; si no, devuelve todo |

```json
{
  "mensaje": "Movimientos consultados correctamente",
  "total": 3,
  "pagina": 1, "por_pagina": 10, "total_paginas": 1,
  "movimientos": [
    { "id_movimiento": 9, "producto_id": 1, "codigo": "PROD-001", "producto": "Teclado USB",
      "usuario_id": 2, "usuario": "Usuario Demo", "tipo_movimiento": "SALIDA", "cantidad": 3,
      "motivo": "Venta", "fecha": "2026-11-14T10:30:00", "existencia_resultante": 7 }
  ]
}
```
`pagina`, `por_pagina` y `total_paginas` solo aparecen cuando se pagina; en ese caso `total` es el total de coincidencias, no el de la página.

### `POST /api/movimientos` (cualquier usuario autenticado)
Cuerpo: `producto_id` (entero), `tipo_movimiento` (`ENTRADA` o `SALIDA`, se acepta en minúsculas), `cantidad` (entero mayor que 0), `motivo` (texto obligatorio, máx. 255).

Todo ocurre en una sola transacción: se bloquea la fila del producto, se valida, se actualiza `existencia_actual`, se inserta el movimiento con el usuario del token, la fecha y la existencia resultante, y se registra la auditoría. Si algo falla, no se guarda nada.

Respuesta `201`:
```json
{
  "mensaje": "Movimiento registrado correctamente",
  "tipo_movimiento": "SALIDA", "cantidad": 3, "existencia_resultante": 7,
  "movimiento": { "id_movimiento": 9, "producto_id": 1, "codigo": "PROD-001", "producto": "Teclado USB",
    "usuario_id": 2, "tipo_movimiento": "SALIDA", "cantidad": 3, "motivo": "Venta",
    "fecha": "2026-11-14T10:30:00", "existencia_anterior": 10, "existencia_resultante": 7,
    "existencia_minima": 5, "existencia_baja": 0 }
}
```
Errores: `400` datos inválidos o **salida mayor a la existencia** (incluye `existencia_disponible` y `cantidad_solicitada`), `404` producto inexistente, `409` producto inactivo.
Auditoría: `movimientos` / `ENTRADA` o `SALIDA`.

## Auditoría

### `GET /api/auditoria` (solo Administrador)
Más reciente primero. Siempre paginada (por defecto página 1 y 50 por página; máximo 100). Parámetros opcionales:

| Parámetro | Valores | Efecto |
|---|---|---|
| `usuario_id` | entero | Acciones de un usuario |
| `modulo` | `productos`, `categorias`, `movimientos` | Filtra por módulo |
| `accion` | `CREAR`, `EDITAR`, `DESACTIVAR`, `ACTIVAR`, `ENTRADA`, `SALIDA` | Filtra por acción |
| `desde`, `hasta` | `AAAA-MM-DD` | Rango de fechas |
| `q` | texto | Busca en el detalle |
| `pagina`, `por_pagina` | enteros | Paginación |

```json
{
  "mensaje": "Auditoría consultada correctamente",
  "total": 6, "pagina": 1, "por_pagina": 50, "total_paginas": 1,
  "auditoria": [
    { "id_auditoria": 6, "usuario_id": 2, "usuario": "Usuario Demo", "modulo": "movimientos",
      "accion": "SALIDA", "fecha": "2026-11-14T10:30:00", "detalle": "PROD-001: 10 -> 7 (Venta)" }
  ]
}
```

### Qué se audita automáticamente
Creación de productos y categorías, edición/activación/desactivación de productos y cada movimiento (entrada o salida). El registro se guarda en la misma transacción que la operación. Las operaciones rechazadas (validación, permisos, stock insuficiente) no generan registro.

## Cómo probar

- Pruebas automáticas (no necesitan MySQL): `cd backend` y `python -m unittest discover -s tests -t . -v`.
- Pruebas manuales: abrir `backend/pruebas.http` en VS Code con la extensión *REST Client* y enviar los bloques en orden.
