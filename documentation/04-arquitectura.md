# 4. Arquitectura del proyecto

## Estilo arquitectónico elegido

**Monolito organizado por módulos y capas.**

### Justificación

- El equipo es pequeño y trabaja en un solo repositorio; un monolito reduce la complejidad de despliegue y coordinación frente a una arquitectura de microservicios.
- La separación de responsabilidades facilita que los subequipos de frontend, backend y base de datos trabajen con interfaces definidas.
- La organización modular permite mantener separadas las funcionalidades de autenticación, productos, categorías, inventario y movimientos.
- Es un estilo apropiado para el alcance del proyecto, evitando sobreingeniería.

## Estructura arquitectónica

El sistema se organiza en los siguientes componentes:

| Componente | Responsabilidad | Tecnología |
|---|---|---|
| Presentación | Interfaz de usuario, formularios, tablas y validaciones de entrada | HTML, CSS y JavaScript |
| API / Aplicación | Exponer endpoints REST, recibir solicitudes y coordinar operaciones | Python y Flask |
| Módulos funcionales | Implementar las operaciones de autenticación, productos, categorías, inventario y movimientos | Python |
| Acceso a datos | Gestionar la conexión y las consultas a la base de datos | MySQL Connector |
| Base de datos | Almacenar usuarios, roles, categorías, productos, movimientos y auditoría | MySQL |

## Organización del backend

El backend se encuentra organizado dentro de `backend/app/`:

- `config/`: espacio destinado a la configuración de la aplicación.
- `database/`: conexión y acceso a la base de datos.
- `modules/`: módulos funcionales del sistema.
  - `authentication/`: autenticación y validación de tokens.
  - `categories/`: consulta y registro de categorías.
  - `configuraciones/`: carpeta del módulo de configuraciones.
  - `inventory/`: consulta de existencias.
  - `movements/`: consulta y registro de movimientos.
  - `products/`: consulta, registro y actualización de productos.
  - `roles/`: carpeta del módulo de roles.
  - `users/`: carpeta del módulo de usuarios.
- `shared/`: espacio destinado a componentes compartidos.
- `main.py`: creación de la aplicación Flask y registro de los módulos que exponen rutas.

La existencia de una carpeta no implica que todas las operaciones del módulo estén implementadas. Los módulos `roles`, `users` y `configuraciones` no exponen actualmente endpoints en el código revisado.

## Comunicación entre capas

- El frontend se comunica con el backend mediante solicitudes HTTP.
- El backend procesa las solicitudes y aplica las validaciones correspondientes.
- La persistencia se realiza en MySQL mediante el conector de Python.
- La API devuelve respuestas en formato JSON.
- Las rutas protegidas requieren un token JWT enviado en el encabezado `Authorization` con el esquema `Bearer`.

## Endpoints identificados en el backend

Los siguientes endpoints corresponden a las rutas registradas en el código fuente revisado.

| Método HTTP | Endpoint | Funcionalidad | Protección |
|---|---|---|---|
| GET | `/` | Verificar que la API está funcionando | Pública |
| GET | `/api/health` | Consultar el estado de disponibilidad de la API | Pública |
| POST | `/api/auth/login` | Iniciar sesión y obtener un token JWT | Pública |
| GET | `/api/perfil` | Consultar el perfil asociado al token | JWT |
| GET | `/api/productos` | Consultar el listado de productos | JWT |
| POST | `/api/productos` | Registrar un producto | JWT |
| GET | `/api/productos/{id_producto}` | Consultar un producto por su identificador | JWT |
| PUT | `/api/productos/{id_producto}` | Actualizar la información de un producto | JWT |
| GET | `/api/categorias` | Consultar las categorías | JWT |
| POST | `/api/categorias` | Registrar una categoría o subcategoría | JWT |
| GET | `/api/inventario` | Consultar existencias y productos con existencia baja | JWT |
| GET | `/api/movimientos` | Consultar el historial de movimientos | JWT |
| POST | `/api/movimientos` | Registrar una entrada o salida de inventario | JWT |

**Nota:** `{id_producto}` representa un identificador entero que se incluye en la URL. Las rutas protegidas utilizan el decorador `requiere_token`, que valida el token JWT. Esta validación no equivale por sí sola a una autorización diferenciada por rol.

## Autenticación y seguridad

El módulo de autenticación implementa:

- Inicio de sesión mediante correo electrónico y contraseña.
- Verificación de contraseñas utilizando bcrypt.
- Generación de tokens JWT con algoritmo HS256.
- Duración del token de 30 minutos.
- Validación del token mediante el encabezado `Authorization: Bearer`.

Las rutas protegidas verifican que el token exista, tenga un formato válido y no haya expirado.

**Alcance actual:** no se identificó un endpoint de cierre de sesión ni una implementación de autorización por rol dentro del decorador de protección revisado.

## Persistencia y modelo de datos

La aplicación utiliza MySQL como sistema de almacenamiento. Las principales entidades son:

- `roles`
- `usuarios`
- `categorias`
- `productos`
- `movimientos`
- `auditoria`

Las relaciones, restricciones e índices se encuentran definidos en `database/schema.sql`.

## Estado de implementación

La arquitectura modular y las rutas descritas corresponden a los archivos presentes en el backend revisado. Las carpetas de usuarios, roles y configuraciones existen, pero sus operaciones mediante API se encuentran pendientes de implementación.

La automatización de auditoría y su integración con el backend también permanecen pendientes.

Las funcionalidades previstas que todavía no cuentan con endpoints deben entenderse como parte del alcance del proyecto y no como operaciones actualmente disponibles.
