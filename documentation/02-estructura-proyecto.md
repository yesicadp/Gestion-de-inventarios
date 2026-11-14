# 2. Estructura del proyecto

## Arquitectura general

El sistema utiliza una **arquitectura monolítica organizada por capas**, que separa las responsabilidades de presentación, lógica de negocio, acceso a datos y persistencia.

Esta arquitectura se seleccionó teniendo en cuenta el alcance del proyecto y la organización del equipo de desarrollo. Permite mantener los componentes organizados, facilitar el mantenimiento y evitar la complejidad adicional de una arquitectura distribuida.

```text
Navegador (Usuario)
        |
        v
Frontend (HTML / CSS / JavaScript)
        |
        | Solicitudes HTTP
        v
Backend (Python)
        |
        v
Capa de negocio
        |
        v
Capa de acceso a datos
        |
        v
Base de datos (MySQL)
```

## Organización de carpetas del repositorio

La estructura general del repositorio se organiza de la siguiente manera:

```text
Gestion-de-inventarios/
├── .vscode/
├── backend/
├── frontend/
├── database/
│   ├── migrations/
│   │   └── .gitkeep
│   ├── scripts/
│   │   ├── .gitkeep
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
├── .gitignore
└── README.md
```

## Componentes principales por capa

### Frontend

Es la capa de presentación encargada de proporcionar la interfaz de interacción entre el usuario y el sistema.

Contempla las pantallas, formularios, tablas, filtros y demás elementos visuales necesarios para utilizar las funcionalidades de inventario.

### Backend

Es la capa encargada de procesar las solicitudes recibidas desde el frontend y ejecutar la lógica de negocio.

Sus responsabilidades contemplan:

- Procesar las solicitudes del sistema.
- Validar los datos recibidos.
- Aplicar las reglas de negocio.
- Gestionar las operaciones relacionadas con productos, categorías, usuarios y movimientos.
- Comunicarse con la base de datos.
- Devolver las respuestas correspondientes al frontend.

### Base de datos

Se utiliza MySQL para almacenar y administrar la información del sistema.

La carpeta `database/` contiene los siguientes elementos:

- **schema.sql:** script de creación de la estructura de la base de datos.
- **seed-usuarios-prueba.sql:** script para la carga de usuarios de prueba.
- **migrations/:** directorio destinado a almacenar futuras migraciones.
- **scripts/:** contiene scripts de pruebas y verificación de la base de datos.

### Documentación

La carpeta `documentation/` centraliza los documentos relacionados con el análisis, diseño, arquitectura, planificación y seguimiento del proyecto.

Incluye el diagrama entidad-relación y los documentos correspondientes a los diferentes aspectos del sistema.

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

La estructura detallada de los directorios internos del frontend y backend se documentará de acuerdo con su implementación efectiva en el repositorio.
