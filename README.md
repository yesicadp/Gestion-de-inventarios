# Sistema de Gestión de Inventarios

## Descripción general

El proyecto consiste en el desarrollo de un sistema web para la gestión y el control de inventarios, diseñado para facilitar la administración de productos y mantener la información organizada, actualizada y disponible de manera centralizada.

El sistema busca ofrecer una solución para procesos como el registro y consulta de productos, la administración de categorías, el control de existencias y el seguimiento de entradas y salidas de inventario.

El desarrollo se organiza mediante la metodología Scrum, utilizando Sprints para planificar, implementar y revisar progresivamente las funcionalidades del sistema.

## Objetivo general

Desarrollar un sistema web de gestión de inventarios que permita administrar de manera organizada y eficiente la información de los productos, sus existencias y sus movimientos.

## Objetivos específicos

- Diseñar una solución web para registrar, consultar y administrar productos.
- Implementar funcionalidades para el control de entradas y salidas de inventario.
- Mantener la información organizada y centralizada.
- Facilitar la consulta de existencias y el estado de los productos.
- Diseñar una arquitectura organizada, mantenible y escalable.
- Aplicar Scrum para planificar y realizar seguimiento al desarrollo.

## Alcance

El proyecto contempla el análisis, diseño y desarrollo de una aplicación web para la gestión y el control básico de inventarios.

Los módulos funcionales contemplados son:

- **Autenticación:** control de acceso al sistema.
- **Usuarios y roles:** administración de usuarios y asignación de roles.
- **Productos:** registro, consulta, modificación y desactivación.
- **Categorías:** clasificación de productos mediante categorías y subcategorías.
- **Inventario:** consulta de existencias disponibles.
- **Movimientos:** registro e historial de entradas y salidas.
- **Búsqueda:** localización y filtrado de productos y movimientos.
- **Auditoría:** seguimiento de las operaciones realizadas en el sistema.

El alcance inicial no contempla facturación electrónica, contabilidad, comercio electrónico ni integraciones con plataformas externas.

## Arquitectura del sistema

El proyecto utiliza una arquitectura monolítica por capas, que organiza las responsabilidades de la aplicación y facilita su mantenimiento.

La estructura contempla:

- **Presentación:** interfaz web con la que interactúa el usuario.
- **Lógica de negocio:** procesamiento de las operaciones y aplicación de las reglas del inventario.
- **Acceso a datos:** comunicación con la base de datos.
- **Base de datos:** almacenamiento persistente de la información mediante MySQL.

## Funcionamiento general

1. El usuario accede al sistema mediante un navegador.
2. La interfaz presenta las opciones disponibles.
3. Las solicitudes se procesan en el backend.
4. La lógica de negocio aplica las reglas correspondientes.
5. La capa de acceso a datos consulta o modifica la información almacenada en MySQL.
6. El sistema devuelve los resultados para su visualización en la interfaz.

## Base de datos

La persistencia de la información se realiza mediante **MySQL**.

Actualmente, la base de datos `gestion_inventarios` cuenta con las siguientes tablas:

| Tabla | Responsabilidad |
|---|---|
| `roles` | Almacenar los roles del sistema. |
| `usuarios` | Gestionar las cuentas de usuario. |
| `categorias` | Clasificar los productos. |
| `productos` | Almacenar la información y las existencias de los productos. |
| `movimientos` | Registrar las entradas y salidas de inventario. |
| `auditoria` | Almacenar información relacionada con las operaciones del sistema. |

La estructura incluye claves primarias y foráneas, restricciones de integridad e índices para organizar y proteger la información.

**Nota sobre auditoría:** la tabla y sus relaciones están creadas, pero la implementación del registro automático de operaciones y su integración con el sistema se encuentran pendientes de verificación.

## Pruebas de base de datos

Se realizaron pruebas manuales mediante scripts SQL para verificar las operaciones de inventario.

En las pruebas del Sprint 3 se verificó:

- Registro de una entrada de productos.
- Registro de una salida de productos.
- Actualización de las existencias.
- Consulta de los movimientos registrados.
- Reversión de los cambios mediante `ROLLBACK`, conservando los datos originales.

Los scripts de verificación se encuentran en `database/scripts/`.

## Estructura del repositorio

```text
Gestion-de-inventarios/
├── backend/
├── frontend/
├── database/
│   ├── migrations/
│   ├── scripts/
│   │   ├── pruebas-sprint-3.sql
│   │   └── verificacion-sprint-4.sql
│   ├── schema.sql
│   └── seed-usuarios-prueba.sql
├── documentation/
│   ├── 01-presentacion-proyecto.md
│   ├── 02-estructura-proyecto.md
│   ├── 03-logica-proyecto.md
│   ├── 04-arquitectura.md
│   ├── 05-modelo-desarrollo.md
│   ├── 06-historias-usuario.md
│   ├── 07-avances-proyecto.md
│   └── diagrama-er.png
└── README.md
```

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

## Estado del proyecto

El proyecto cuenta con una estructura de base de datos implementada y verificada, documentación de planificación y arquitectura, y pruebas manuales de operaciones de inventario.

Se encuentran pendientes la integración del registro automático de auditoría y la verificación de las funcionalidades correspondientes a los demás módulos.

## Tecnologías principales

- **Backend:** Python.
- **Base de datos:** MySQL.
- **Frontend:** aplicación web.
- **Metodología:** Scrum.
- **Control de versiones:** Git y GitHub.
