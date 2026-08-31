# 2. Estructura del proyecto

## Arquitectura general

El sistema se desarrolla como un **monolito organizado por capas**, separando responsabilidades entre presentación (frontend), lógica de negocio y acceso a datos (backend), y persistencia (base de datos). Esta decisión se tomó por tratarse de un proyecto de grupo con alcance acotado, donde un monolito por capas es más sencillo de coordinar entre subequipos que una arquitectura distribuida, sin sacrificar organización interna ni mantenibilidad.

```
Navegador (Usuario)
        │
        ▼
  Frontend (HTML/CSS/JS)
        │  HTTP / JSON
        ▼
  API REST (Python)
        │
        ▼
  Capa de negocio (reglas del inventario)
        │
        ▼
  Capa de acceso a datos
        │
        ▼
  Base de datos (MySQL)
```

## Organización de carpetas del repositorio

```
inventario/
├── frontend/                    # A cargo del equipo de frontend
│   ├── pages/                   # Una vista por pantalla (login.html, productos.html, ...)
│   ├── css/
│   │   ├── base/                 # Reset, variables, tipografía
│   │   └── components/           # Botones, tablas, modales, formularios
│   ├── js/
│   │   ├── services/             # Llamadas a la API (fetch)
│   │   ├── components/           # Lógica de UI reutilizable
│   │   └── utils/
│   └── assets/
│       ├── img/
│       └── icons/
│
├── backend/                     # A cargo del equipo de backend
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
├── database/                    # A cargo del equipo de base de datos
│   ├── migrations/
│   └── scripts/
│
└── documentation/                # Documentación del proyecto (este set de archivos)
    ├── 01-presentacion-proyecto.md
    ├── 02-estructura-proyecto.md
    ├── 03-logica-proyecto.md
    ├── 04-arquitectura.md
    ├── 05-modelo-desarrollo.md
    ├── 06-historias-usuario.md
    ├── 07-avances-proyecto.md
    ├── 08-evidencias-funcionamiento.md
    └── mockups/
        ├── 01-login.svg
        ├── 02-dashboard.svg
        ├── 03-productos-listado.svg
        ├── 04-producto-formulario.svg
        ├── 05-categorias.svg
        ├── 06-inventario-existencias.svg
        ├── 07-movimientos-registro.svg
        ├── 08-historial-movimientos.svg
        └── 09-usuarios-roles.svg
```

## Componentes principales por capa

### Frontend (HTML / CSS / JavaScript)
- **pages/**: una página por pantalla funcional (login, dashboard, productos, categorías, inventario, movimientos, usuarios).
- **css/base**: estilos globales compartidos (tipografía, colores, espaciados).
- **css/components**: estilos de piezas reutilizables (botón, tabla, tarjeta, formulario).
- **js/services**: un archivo por módulo del backend (ej. `productsService.js`) que centraliza las llamadas `fetch` a la API — evita repetir URLs y manejo de errores en cada página.
- **js/components**: comportamiento de interfaz reutilizable (validación de formularios, manejo de tablas, modales).

### Backend (Python)
- **app/modules/**: un submódulo por dominio funcional (`products`, `categories`, `inventory`, `movements`, `users`, `roles`, `authentication`), cada uno típicamente con sus propias rutas, controlador y lógica de negocio.
- **app/shared/**: código transversal (seguridad/autenticación de tokens, manejo de excepciones, utilidades comunes).
- **app/database/**: configuración de conexión y acceso a MySQL.

### Base de datos (MySQL)
- **migrations/**: scripts versionados de creación/modificación de tablas.
- **scripts/**: scripts auxiliares (carga de datos de prueba, respaldo, etc.).