# 5. Modelo de desarrollo

## Metodología de trabajo

El desarrollo del Sistema de Gestión de Inventarios se organiza mediante la metodología ágil **Scrum**, un marco de trabajo que permite planificar, desarrollar y revisar progresivamente las funcionalidades del proyecto.

El trabajo se divide en ciclos de desarrollo denominados **Sprints**, durante los cuales se seleccionan actividades y funcionalidades prioritarias para avanzar en la construcción del sistema.

Esta metodología facilita la organización del equipo, el seguimiento de las actividades y la identificación de aspectos que requieren ajustes o mejoras.

## Organización del trabajo

El equipo contempla diferentes responsabilidades para distribuir las actividades de desarrollo:

| Rol o área | Responsabilidades |
|---|---|
| Product Owner | Definir requerimientos, organizar historias de usuario y priorizar funcionalidades. |
| Scrum Master | Facilitar la organización del trabajo, coordinar el seguimiento y apoyar la ejecución de los Sprints. |
| Desarrollo Backend | Implementar la API REST, la lógica de negocio y la conexión con MySQL. |
| Desarrollo Frontend | Construir las interfaces web e integrar las funcionalidades con la API. |
| Base de datos | Diseñar, implementar y verificar la estructura de almacenamiento y sus relaciones. |

Los integrantes colaboran en el desarrollo del producto, aunque tengan responsabilidades principales distribuidas por áreas.

## Artefactos de Scrum

### Product Backlog

El Product Backlog contiene las funcionalidades y requerimientos identificados para el sistema, organizados mediante historias de usuario y criterios de aceptación.

Entre las funcionalidades contempladas se encuentran:

- Inicio de sesión.
- Registro, consulta y actualización de productos.
- Desactivación de productos.
- Gestión de categorías.
- Gestión de proveedores.
- Registro de entradas y salidas.
- Consulta de movimientos.
- Consulta de existencias.
- Alertas de bajo stock.
- Gestión de usuarios.
- Dashboard.

Las historias de usuario se encuentran documentadas en `06-historias-usuario.md`.

### Sprint Backlog

El Sprint Backlog corresponde al conjunto de actividades seleccionadas para trabajar durante un Sprint.

Permite identificar las tareas, responsables y resultados esperados para cada iteración.

### Incremento del producto

El incremento corresponde al resultado del trabajo realizado durante un Sprint. Puede incluir funcionalidades implementadas, ajustes técnicos, pruebas y documentación que contribuyan al avance del sistema.

## Planificación inicial de Sprints

La propuesta inicial del proyecto contempló la siguiente organización:

| Sprint | Objetivo y actividades principales |
|---|---|
| Sprint 0 — Planeación | Definir requisitos, tecnologías, repositorio, Product Backlog, historias de usuario, base de datos e interfaces iniciales. |
| Sprint 1 — Base del sistema | Crear el proyecto Flask, configurar MySQL, organizar la estructura del proyecto, preparar la base de datos e implementar el inicio de sesión y la estructura inicial de la página. |
| Sprint 2 — Productos | Registrar, consultar, editar y desactivar productos; gestionar categorías. |
| Sprint 3 — Inventario | Registrar entradas y salidas, actualizar existencias, consultar movimientos y validar disponibilidad. |
| Sprint 4 — Funciones adicionales | Contemplar proveedores, usuarios y roles, alertas de bajo stock y dashboard. |
| Sprint 5 — Pruebas y entrega | Realizar pruebas, corregir errores, integrar el proyecto, documentar y preparar la presentación. |

Esta planificación corresponde a la propuesta inicial y puede ajustarse de acuerdo con las necesidades del proyecto y las decisiones del equipo.

## Eventos de Scrum

El modelo de trabajo contempla los siguientes eventos:

### Sprint Planning

Se realiza al inicio de cada Sprint para establecer el objetivo, seleccionar las historias de usuario y definir las actividades que se desarrollarán durante la iteración.

### Daily Scrum

Es una reunión breve de seguimiento en la que los integrantes comparten sus avances, las actividades que realizarán y los posibles impedimentos que puedan afectar el trabajo.

### Sprint Review

Se realiza al finalizar el Sprint para presentar y revisar los resultados obtenidos, verificar las funcionalidades desarrolladas y recibir observaciones.

### Sprint Retrospective

Permite analizar el desarrollo del Sprint, identificar aspectos positivos, dificultades y oportunidades de mejora para las siguientes iteraciones.

La descripción de estos eventos corresponde al modelo de trabajo definido para el proyecto; no implica que todas las reuniones se hayan realizado o documentado.

## Seguimiento y control del proyecto

El seguimiento de las actividades se realiza mediante:

- Historias de usuario y criterios de aceptación.
- Organización de tareas por Sprint.
- Control de versiones mediante Git y GitHub.
- Registro de cambios en el repositorio.
- Documentación técnica y funcional.
- Evidencias de pruebas y verificaciones.

El documento `07-avances-proyecto.md` contiene el registro de los avances documentados y las actividades pendientes.

## Estado de desarrollo documentado

Dentro de las actividades verificadas se encuentran:

- Planeación y documentación inicial del proyecto.
- Definición de la arquitectura y estructura modular.
- Diseño del modelo entidad-relación.
- Implementación y revisión de la estructura de la base de datos.
- Verificación de las relaciones entre productos, usuarios y movimientos.
- Pruebas manuales de entradas, salidas y transacciones en el Sprint 3.
- Revisión de la estructura de auditoría e índices en el Sprint 4.
- Actualización de la documentación técnica y funcional.

La implementación automática de auditoría y otras funcionalidades pendientes se encuentran identificadas en la documentación de historias de usuario y avances del proyecto.

## Herramientas de trabajo

| Herramienta | Uso |
|---|---|
| Git | Control de versiones del código fuente. |
| GitHub | Almacenamiento del repositorio y trabajo colaborativo. |
| Visual Studio Code | Edición y desarrollo del proyecto. |
| MySQL | Administración y almacenamiento de la información. |
| MySQL Workbench | Administración y verificación de la base de datos. |
| Draw.io | Elaboración de diagramas. |

## Conclusión

La aplicación de Scrum permite organizar el desarrollo del Sistema de Gestión de Inventarios en entregas progresivas, facilitando la distribución de responsabilidades, el seguimiento de las actividades y la revisión de los resultados.

La documentación de historias de usuario, avances, arquitectura y evidencias permite mantener trazabilidad sobre el trabajo realizado, identificar funcionalidades pendientes y orientar las siguientes actividades del proyecto.
