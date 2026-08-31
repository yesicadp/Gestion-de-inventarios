# 1. Presentación del proyecto

## Descripción general

El proyecto consiste en el desarrollo de un sistema web para la gestión y control de inventarios, diseñado para facilitar la administración de productos y mantener la información del inventario organizada, actualizada y disponible de manera centralizada.

El sistema busca brindar una solución sencilla y eficiente para procesos como el registro de productos, consulta de existencias, actualización de información y control de entradas y salidas de inventario, reduciendo errores asociados al manejo manual de la información.

El proyecto se desarrolla aplicando la metodología **Scrum**, organizando el trabajo en iteraciones (sprints), definiendo requerimientos mediante historias de usuario y realizando entregas progresivas de las funcionalidades del sistema.

## Objetivo general

Desarrollar un sistema web de gestión de inventarios que permita administrar de manera organizada y eficiente la información relacionada con los productos, sus existencias y los movimientos de inventario, facilitando el control y seguimiento de los recursos disponibles.

## Objetivos específicos

- Diseñar una solución web que permita registrar, consultar, actualizar y administrar productos.
- Implementar funcionalidades para el control de entradas y salidas de inventario.
- Mantener la información del inventario organizada y centralizada.
- Facilitar la consulta de las existencias disponibles y el estado de los productos.
- Diseñar una arquitectura que permita que el sistema sea organizado, mantenible y escalable.
- Aplicar la metodología Scrum para planificar, desarrollar y realizar seguimiento al proyecto.

## Alcance

El proyecto contempla el análisis, diseño, desarrollo y puesta en funcionamiento de una aplicación web para la gestión y control básico de inventarios, orientada a facilitar el registro, consulta y seguimiento de los productos y de los movimientos que afectan sus existencias.

Dentro del alcance funcional se contemplan los siguientes módulos:

| Módulo | Responsabilidad principal |
|---|---|
| Autenticación | Controlar el acceso al sistema |
| Usuarios y permisos | Administrar roles y autorizaciones |
| Productos | Registrar, consultar, modificar y desactivar productos |
| Categorías | Clasificar productos mediante categorías y subcategorías |
| Inventario | Consultar existencias actuales y alertas |
| Movimientos | Registrar entradas, salidas e historial |
| Búsqueda | Localizar productos y movimientos |
| Auditoría | Registrar usuario, fecha y operación de cada acción relevante |

## Roles del sistema

| Rol | Descripción |
|---|---|
| **Administrador** | Acceso total: gestión de usuarios y roles, gestión completa de productos y categorías, consulta de inventario, movimientos y auditoría. |
| **Usuario** | Acceso operativo: consulta de productos e inventario, registro de movimientos de entrada/salida, búsqueda y filtrado. No gestiona usuarios ni roles. |

## Equipo de trabajo

| Integrante | Frente | Responsabilidad |
|---|---|---|
| _Yesica_ | Frontend | HTML, CSS, JavaScript — interfaz de usuario y consumo de la API |
| _Rowinzon_ | Backend | Python (API REST) — lógica de negocio y endpoints |
| _Maicol_ | Base de datos | Diseño e implementación en MySQL |