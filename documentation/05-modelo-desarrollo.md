# 5. Modelo de desarrollo

## Metodología: Scrum

El proyecto se desarrolla bajo la metodología ágil **Scrum**, organizando el trabajo en ciclos incrementales (Sprints). En cada Sprint se priorizan, diseñan, desarrollan y validan funcionalidades específicas, permitiendo obtener incrementos funcionales del producto y ajustar el trabajo según los resultados de las revisiones.

## Roles Scrum del equipo

| Rol Scrum | Integrante(s) | Notas |
|---|---|---|
| Product Owner | _(definir)_ | Prioriza el backlog y representa las necesidades del "cliente" (profesor/enunciado) |
| Scrum Master | _(definir)_ | Facilita las ceremonias y remueve impedimentos |
| Equipo de desarrollo | Todo el grupo | Subdividido en frontend, backend y base de datos |

## Artefactos

- **Product Backlog**: lista priorizada de historias de usuario (ver `06-historias-usuario.md`).
- **Sprint Backlog**: subconjunto de historias comprometidas para el sprint en curso.
- **Incremento**: funcionalidad entregada y validada al final de cada sprint.

## Ceremonias

| Ceremonia | Frecuencia | Propósito |
|---|---|---|
| Sprint Planning | Al inicio de cada sprint | Seleccionar y estimar historias de usuario del backlog |
| Daily / seguimiento | Según disponibilidad del equipo (recomendado 2-3 veces por semana) | Sincronizar avances y bloqueos |
| Sprint Review | Al final de cada sprint | Demostrar el incremento funcional |
| Sprint Retrospective | Al final de cada sprint | Identificar mejoras para el siguiente sprint |

## Planificación de sprints (propuesta inicial)

| Sprint | Enfoque principal |
|---|---|
| Sprint 0 | Documentación base, arquitectura, mockups, historias de usuario, definición de base de datos |
| Sprint 1 | Autenticación, gestión de usuarios y roles |
| Sprint 2 | Gestión de productos y categorías |
| Sprint 3 | Inventario, movimientos y alertas de existencia |
| Sprint 4 | Búsqueda, auditoría, pulido general y evidencias finales |

## Herramientas de gestión

| Herramienta | Uso |
|---|---|
| GitHub | Repositorio de código y documentación, control de versiones |
| _(Trello / Jira / GitHub Projects — definir)_ | Tablero del backlog y seguimiento de historias de usuario |
| _(Definir)_ | Comunicación del equipo |

## Definición de "Terminado" (Definition of Done)

Una historia de usuario se considera terminada cuando:
- La funcionalidad está implementada y accesible desde la interfaz.
- Fue probada manualmente por al menos un integrante distinto a quien la desarrolló.
- No rompe funcionalidades existentes.
- Está documentada (si aplica) y su código está en la rama principal del repositorio.
