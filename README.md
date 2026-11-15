# Sistema de Gestión de Inventarios

## Descripción general

El proyecto consiste en el desarrollo de un sistema web para la gestión y el control de inventarios, diseñado para facilitar la administración de productos y mantener la información organizada, actualizada y disponible de manera centralizada.

El sistema contempla procesos como el registro y consulta de productos, la administración de categorías, el control de existencias y el seguimiento de entradas y salidas de inventario.

El desarrollo se organiza mediante la metodología Scrum, utilizando Sprints para planificar, implementar y revisar progresivamente las funcionalidades del sistema.

## Objetivo general

Desarrollar un sistema web de gestión de inventarios que permita administrar productos, controlar existencias y registrar los movimientos de inventario de manera organizada y eficiente.

## Objetivos específicos

- Diseñar una solución web que permita registrar, consultar, actualizar y administrar productos.
- Implementar funcionalidades para el control de entradas y salidas de inventario.
- Mantener la información organizada y centralizada.
- Facilitar la consulta de existencias y el estado de los productos.
- Diseñar una arquitectura organizada, mantenible y escalable.
- Aplicar Scrum para planificar y realizar seguimiento al desarrollo.

## Alcance

El sistema contempla la gestión de productos, categorías, usuarios, roles, existencias y movimientos de inventario. También considera el seguimiento de las operaciones mediante el módulo de auditoría.

La gestión de proveedores fue contemplada en la descripción inicial del proyecto; sin embargo, actualmente no existe una tabla de proveedores en el esquema implementado de la base de datos.

Las funcionalidades descritas corresponden al alcance general del proyecto. Su disponibilidad actual depende del estado de implementación de cada módulo.

## Funcionamiento general

1. El usuario accede al sistema mediante un navegador.
2. El frontend presenta las interfaces para interactuar con las funcionalidades disponibles.
3. El frontend envía solicitudes HTTP a la API REST.
4. La API valida la autenticación y los datos recibidos en las rutas protegidas.
5. Cada solicitud se dirige al módulo correspondiente.
6. La lógica del backend aplica las operaciones y reglas de inventario implementadas.
7. La capa de acceso a datos consulta o modifica la información almacenada en MySQL.
8. La API devuelve una respuesta en formato JSON para su procesamiento por el frontend.

**Nota:** el backend utiliza autenticación mediante tokens JWT. La autorización diferenciada por roles todavía no se encuentra implementada en el mecanismo de protección de rutas revisado.

## Módulos del sistema

| Módulo | Responsabilidad principal | Estado actual |
|---|---|---|
| Autenticación | Inicio de sesión y validación de tokens | Parcialmente implementado |
| Usuarios y permisos | Administración de cuentas, roles y autorizaciones | Pendiente de endpoints de administración |
| Productos | Registrar, consultar y actualizar productos | Implementado parcialmente |
| Categorías | Consultar y registrar categorías y subcategorías | Implementado parcialmente |
| Inventario | Consultar existencias y alertas de stock bajo | Implementado |
| Movimientos | Registrar entradas, salidas y consultar historial | Implementado |
| Existencias | Actualizar cantidades según los movimientos | Implementado en las operaciones de movimientos |
| Búsqueda | Buscar y filtrar productos y movimientos | Pendiente de filtros específicos |
| Auditoría | Registrar y consultar operaciones del sistema | Estructura de base de datos implementada; integración pendiente |

## Estructuración modular inicial

La siguiente estructura representa la organización modular inicial propuesta para el proyecto:

```text
inventario/
├── frontend/
│   ├── pages/
│   ├── css/
│   ├── js/
│   └── assets/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config/
│   │   ├── database/
│   │   ├── shared/
│   │   │   ├── exceptions/
│   │   │   ├── security/
│   │   │   └── utilities/
│   │   └── modules/
│   │       ├── configuraciones/
│   │       ├── authentication/
│   │       ├── users/
│   │       ├── roles/
│   │       ├── products/
│   │       ├── categories/
│   │       ├── inventory/
│   │       └── movements/
│   └── tests/
│
├── database/
│   ├── migrations/
│   └── scripts/
│
└── documentation/
```

Esta estructura corresponde a una propuesta inicial de organización modular. La estructura real del backend se encuentra en `backend/app/` y utiliza Flask.

Los módulos `authentication`, `categories`, `inventory`, `movements` y `products` cuentan con rutas registradas en la aplicación. Las carpetas `users`, `roles` y `configuraciones` existen, pero no tienen endpoints registrados en el backend revisado.

## API REST — Endpoints implementados

El backend utiliza Python y Flask para exponer los servicios mediante una API REST. Las siguientes rutas fueron identificadas en el código fuente:

| Método HTTP | Endpoint | Funcionalidad | Acceso |
|---|---|---|---|
| GET | `/` | Verificar funcionamiento de la API | Público |
| GET | `/api/health` | Consultar estado de la API | Público |
| POST | `/api/auth/login` | Iniciar sesión y generar token JWT | Público |
| GET | `/api/perfil` | Consultar perfil del usuario autenticado | JWT |
| GET | `/api/productos` | Consultar productos | JWT |
| POST | `/api/productos` | Registrar un producto | JWT |
| GET | `/api/productos/{id_producto}` | Consultar un producto por identificador | JWT |
| PUT | `/api/productos/{id_producto}` | Actualizar un producto | JWT |
| GET | `/api/categorias` | Consultar categorías | JWT |
| POST | `/api/categorias` | Registrar categorías y subcategorías | JWT |
| GET | `/api/inventario` | Consultar existencias y productos con stock bajo | JWT |
| GET | `/api/movimientos` | Consultar historial de movimientos | JWT |
| POST | `/api/movimientos` | Registrar entradas y salidas | JWT |

**Consideraciones sobre la API:**

- `{id_producto}` representa el identificador entero del producto.
- Las rutas protegidas requieren un token JWT enviado mediante el encabezado `Authorization: Bearer`.
- El token tiene una vigencia de 30 minutos.
- La autenticación utiliza contraseñas protegidas mediante bcrypt y tokens JWT con algoritmo HS256.
- La protección de rutas valida la autenticación, pero no aplica actualmente una autorización diferenciada por rol.
- No se identificaron endpoints para administración de usuarios, roles, consulta de auditoría ni cierre de sesión.

## Base de datos

La persistencia de la información del sistema se realiza mediante **MySQL**.

La base de datos `gestion_inventarios` cuenta actualmente con seis tablas principales:

| Tabla | Responsabilidad |
|---|---|
| `roles` | Almacenar los roles del sistema. |
| `usuarios` | Gestionar las cuentas de usuario. |
| `categorias` | Clasificar los productos. |
| `productos` | Almacenar la información y las existencias de los productos. |
| `movimientos` | Registrar las entradas y salidas de inventario. |
| `auditoria` | Almacenar información relacionada con las operaciones del sistema. |

La estructura contempla:

- Modelo entidad-relación.
- Definición de tablas, campos y relaciones.
- Claves primarias y foráneas.
- Restricciones de integridad.
- Índices para consultas.
- Scripts SQL para creación, pruebas y verificación.

El esquema incorpora índices secundarios para las relaciones, búsquedas por estado, fechas y consultas relacionadas con auditoría.

**Nota sobre auditoría:** la tabla y sus relaciones están creadas, pero la implementación del registro automático de operaciones y su integración con el backend se encuentran pendientes.

## Pruebas de base de datos

Se realizaron pruebas manuales mediante scripts SQL para verificar las operaciones de inventario.

En las pruebas del Sprint 3 se verificó:

- Registro de una entrada de productos.
- Registro de una salida de productos.
- Actualización de las existencias.
- Consulta de los movimientos registrados.
- Reversión de los cambios mediante `ROLLBACK`, conservando los datos originales.

Como resultado de la prueba:

- Existencia inicial: 20 unidades.
- Después de una entrada de 5 unidades: 25 unidades.
- Después de una salida de 3 unidades: 22 unidades.
- Después del `ROLLBACK`: 20 unidades.

En el Sprint 4 se verificó la estructura de auditoría, sus relaciones, los índices y la ausencia de triggers, procedimientos y funciones almacenadas.

Los scripts de verificación se encuentran en `database/scripts/`.

## Documentación

La documentación técnica y funcional del proyecto se encuentra en la carpeta `documentation/`.

Incluye:

- Presentación del proyecto.
- Estructura del repositorio.
- Lógica del sistema.
- Arquitectura.
- Modelo de desarrollo.
- Historias de usuario y criterios de aceptación.
- Avances por Sprint.
- Diagrama entidad-relación.
- Evidencias de las pruebas de base de datos.

## Estado del proyecto

El proyecto cuenta con:

- Estructura de base de datos implementada y verificada.
- Operaciones de registro y consulta de productos.
- Consulta y registro de categorías.
- Consulta de existencias.
- Registro de entradas y salidas de inventario.
- Consulta del historial de movimientos.
- Autenticación mediante JWT.
- Documentación de planificación, arquitectura y funcionalidades.
- Pruebas manuales de operaciones de inventario.
- Evidencias organizadas de los Sprints 3 y 4.

Se encuentran pendientes:

- Implementación del cierre de sesión y mecanismos de invalidación de tokens.
- Autorización diferenciada por roles.
- Administración de usuarios y roles mediante API.
- Búsquedas y filtros específicos.
- Funcionalidades de dashboard.
- Endpoints de edición y eliminación de categorías.
- Registro automático de auditoría e integración con el backend.
- Consulta de registros de auditoría.

El estado detallado de las funcionalidades se encuentra en `documentation/06-historias-usuario.md`.

## Tecnologías principales

- **Backend:** Python y Flask.
- **Base de datos:** MySQL.
- **Autenticación:** JWT y bcrypt.
- **Comunicación:** API REST y JSON.
- **Frontend:** aplicación web.
- **Metodología:** Scrum.
- **Control de versiones:** Git y GitHub.

## Organización del repositorio

```text
Gestion-de-inventarios/
├── backend/
├── database/
│   ├── scripts/
│   └── schema.sql
├── documentation/
│   ├── mockups/
│   ├── evidencias/
│   └── documentación del proyecto
└── README.md
```

Para conocer los detalles de la arquitectura, las historias de usuario, el modelo de datos y los avances de cada Sprint, consulta los documentos de la carpeta `documentation/`.
