# 2. Estructura del proyecto

## Arquitectura general

El sistema utiliza una **arquitectura monolítica modular organizada por capas**, que separa las responsabilidades de presentación, lógica de negocio, acceso a datos y persistencia.

Esta arquitectura permite mantener los componentes organizados, facilitar el mantenimiento y evitar la complejidad adicional de una arquitectura distribuida.

```text
Navegador (Usuario)
        |
        v
Frontend (HTML / CSS / JavaScript)
        |
        | Solicitudes HTTP
        v
Backend (Python / Flask)
        |
        v
Módulos y lógica de negocio
        |
        v
Acceso a datos
        |
        v
Base de datos (MySQL)
```

## Organización de carpetas del repositorio

La estructura del repositorio `Gestion-de-inventarios` se organiza de la siguiente manera:

```text
Gestion-de-inventarios/
├── .vscode/
│
├── frontend/
│   ├── assets/
│   │   ├── icons/
│   │   └── img/
│   │
│   ├── css/
│   │   ├── base/
│   │   │   └── global.css
│   │   └── components/
│   │       ├── auth.css
│   │       ├── categorias.css
│   │       ├── dashboard.css
│   │       ├── producto-formulario.css
│   │       └── productos.css
│   │
│   ├── js/
│   │   ├── auth.js
│   │   ├── categorias.js
│   │   ├── dashboard.js
│   │   ├── producto-formulario.js
│   │   ├── productos.js
│   │   ├── components/
│   │   ├── services/
│   │   └── utils/
│   │
│   └── pages/
│       ├── categorias.html
│       ├── dashboard.html
│       ├── login.html
│       ├── producto-formulario.html
│       └── productos.html
│
├── backend/
│   ├── app/
│   │   ├── config/
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── connection.py
│   │   │
│   │   ├── main.py
│   │   │
│   │   ├── modules/
│   │   │   ├── authentication/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── decorators.py
│   │   │   │   └── routes.py
│   │   │   ├── categories/
│   │   │   │   └── routes.py
│   │   │   ├── configuraciones/
│   │   │   ├── inventory/
│   │   │   │   └── routes.py
│   │   │   ├── movements/
│   │   │   │   └── routes.py
│   │   │   ├── products/
│   │   │   │   └── routes.py
│   │   │   ├── roles/
│   │   │   └── users/
│   │   │
│   │   └── shared/
│   │       ├── exceptions/
│   │       ├── security/
│   │       └── utilities/
│   │
│   ├── tests/
│   ├── registro-decisiones.md
│   └── requirements.txt
│
├── database/
│   ├── migrations/
│   ├── scripts/
│   │   ├── pruebas-sprint-3.sql
│   │   └── verificacion-sprint-4.sql
│   ├── schema.sql
│   └── seed-usuarios-prueba.sql
│
├── documentation/
│   ├── evidencias/
│   │   ├── sprint-3/
│   │   └── sprint-4/
│   ├── mockups/
│   ├── 01-presentacion-proyecto.md
│   ├── 02-estructura-proyecto.md
│   ├── 03-logica-proyecto.md
│   ├── 04-arquitectura.md
│   ├── 05-modelo-desarrollo.md
│   ├── 06-historias-usuario.md
│   ├── 07-avances-proyecto.md
│   └── Diagrama E R.png
│
├── .gitignore
└── README.md
```

La estructura anterior representa los archivos y directorios identificados en el repositorio durante la revisión. Algunas carpetas contienen únicamente archivos `.gitkeep` para conservar su organización inicial.

## Componentes principales por capa

### Frontend

Es la capa de presentación encargada de proporcionar la interfaz de interacción entre el usuario y el sistema.

Está desarrollada mediante HTML, CSS y JavaScript.

Su organización contempla:

- **pages/:** contiene las páginas HTML del sistema, como inicio de sesión, productos, categorías y dashboard.
- **css/:** contiene los estilos generales y los estilos específicos de los componentes.
- **js/:** contiene los scripts que gestionan la interacción y el comportamiento de las páginas.
- **assets/:** está destinada a almacenar recursos gráficos, imágenes e iconos.

### Backend

Es la capa encargada de recibir las solicitudes HTTP, procesar la información y ejecutar las operaciones correspondientes.

Está desarrollado en Python utilizando Flask.

Su organización contempla:

- **main.py:** punto de entrada de la aplicación y registro de las rutas.
- **config/:** directorio destinado a la configuración.
- **database/:** contiene la conexión y los componentes relacionados con el acceso a MySQL.
- **modules/:** organiza las funcionalidades por módulos.
- **shared/:** agrupa componentes compartidos, como excepciones, seguridad y utilidades.
- **tests/:** directorio destinado a las pruebas del backend.

Los módulos identificados son:

| Módulo | Responsabilidad |
|---|---|
| `authentication` | Autenticación y protección de rutas. |
| `categories` | Consulta y registro de categorías. |
| `inventory` | Consulta de existencias. |
| `movements` | Registro y consulta de movimientos. |
| `products` | Registro, consulta y actualización de productos. |
| `users` | Directorio destinado a funcionalidades de usuarios. |
| `roles` | Directorio destinado a funcionalidades de roles. |
| `configuraciones` | Directorio destinado a configuraciones del sistema. |

La existencia de un directorio no significa que todas sus funcionalidades estén implementadas. Los endpoints disponibles se documentan en `04-arquitectura.md`.

### Base de datos

Se utiliza MySQL para almacenar y administrar la información del sistema.

La carpeta `database/` contiene:

- **schema.sql:** script de creación de la estructura de la base de datos.
- **seed-usuarios-prueba.sql:** script para la carga de usuarios de prueba.
- **migrations/:** directorio destinado a futuras migraciones.
- **scripts/:** contiene scripts de pruebas y verificación de la base de datos.

### Documentación

La carpeta `documentation/` centraliza los documentos relacionados con el análisis, diseño, arquitectura, planificación y seguimiento del proyecto.

Incluye:

- Documentación de presentación y estructura.
- Descripción de la lógica del sistema.
- Arquitectura del proyecto.
- Modelo de desarrollo.
- Historias de usuario.
- Avances por Sprint.
- Diagrama entidad-relación.
- Mockups de las interfaces.
- Evidencias de las pruebas realizadas.

## Organización de responsabilidades

La separación por capas permite distribuir las responsabilidades de la siguiente manera:

| Componente | Responsabilidad |
|---|---|
| Frontend | Presentación e interacción con el usuario. |
| Backend | Procesamiento de solicitudes y lógica de negocio. |
| Base de datos | Almacenamiento, integridad y consulta de información. |
| Documentación | Registro de decisiones, diseños y avances del proyecto. |

## Consideraciones de diseño

La organización del proyecto busca mantener una separación clara de responsabilidades, facilitar el trabajo colaborativo y permitir que los componentes evolucionen sin afectar innecesariamente a las demás capas.

La estructura modular del backend permite organizar las funcionalidades por dominio, mientras que la separación entre frontend, backend y base de datos facilita el mantenimiento y la evolución del sistema.

Los módulos y directorios que todavía no cuentan con funcionalidades implementadas se mantienen como parte de la organización prevista para el crecimiento del proyecto.
