# Sistema de Gestión de Inventarios

## Descripción general

El proyecto consiste en el desarrollo de un sistema web para la gestión y el control de inventarios, diseñado para facilitar la administración de productos y mantener la información organizada, actualizada y disponible de manera centralizada.

El sistema busca ofrecer una solución para procesos como el registro y consulta de productos, la administración de categorías, el control de existencias y el seguimiento de entradas y salidas de inventario.

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

## Funcionamiento general

1. El usuario accede al sistema mediante un navegador.
2. El frontend presenta formularios, tablas, filtros y opciones según los permisos del usuario.
3. El frontend envía solicitudes HTTP a la API REST.
4. La API verifica la autenticación, los permisos y los datos recibidos.
5. Cada solicitud se dirige al módulo correspondiente.
6. La capa de negocio aplica las reglas del inventario.
7. La capa de acceso a datos consulta o modifica la información almacenada en MySQL.
8. La API devuelve una respuesta en formato JSON y el frontend actualiza la interfaz.

## Módulos del sistema

| Módulo | Responsabilidad principal | Funciones |
|---|---|---|
| Autenticación | Controlar el acceso | Inicio y cierre de sesión |
| Usuarios y permisos | Administrar roles y autorizaciones | Crear usuarios, asignar roles y validar permisos |
| Productos | Administrar productos | Registrar, consultar, modificar y desactivar |
| Categorías | Clasificar productos | Crear categorías y subcategorías |
| Inventario | Consultar existencias | Mostrar cantidades actuales y alertas |
| Movimientos | Registrar cambios de inventario | Entradas, salidas e historial |
| Existencias | Actualizar cantidades | Incrementar o disminuir el inventario |
| Búsqueda | Localizar información | Buscar y filtrar productos y movimientos |
| Auditoría | Facilitar el seguimiento | Registrar usuario, fecha y operación |

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

Esta estructura corresponde a una propuesta inicial de organización modular y no necesariamente representa la totalidad de los archivos implementados actualmente.

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

**Nota sobre auditoría:** la tabla y sus relaciones están creadas, pero la implementación del registro automático de operaciones y su integración con el sistema se encuentran pendientes de verificación e implementación.

## Pruebas de base de datos

Se realizaron pruebas manuales mediante scripts SQL para verificar las operaciones de inventario.

En las pruebas del Sprint 3 se verificó:

- Registro de una entrada de productos.
- Registro de una salida de productos.
- Actualización de las existencias.
- Consulta de los movimientos registrados.
- Reversión de los cambios mediante `ROLLBACK`, conservando los datos originales.

Los scripts de verificación se encuentran en `database/scripts/`.

## Documentación

La documentación técnica y funcional del proyecto se encuentra en la carpeta `documentation/`.

Incluye:

- Presentación del proyecto.
- Estructura del repositorio.
- Lógica del sistema.
- Arquitectura.
- Modelo de desarrollo.
- Historias de usuario.
- Avances por Sprint.
- Diagrama entidad-relación.
- Evidencias de las pruebas de base de datos.

## Estado del proyecto

El proyecto cuenta con una estructura de base de datos implementada y verificada, documentación de planificación y arquitectura, y pruebas manuales de operaciones de inventario.

Se encuentran pendientes la integración del registro automático de auditoría y la verificación de las funcionalidades correspondientes a los demás módulos.

## Tecnologías principales

- **Backend:** Python.
- **Base de datos:** MySQL.
- **Frontend:** aplicación web.
- **Metodología:** Scrum.
- **Control de versiones:** Git y GitHub.
