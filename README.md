# Sistema de Gestión de Inventarios
Descripción general:

El proyecto consiste en el desarrollo de un sistema web para la gestión y control de inventarios, diseñado para facilitar la administración de productos y mantener la información del inventario organizada, actualizada y disponible de manera centralizada.

El sistema busca brindar una solución sencilla y eficiente para procesos como el registro de productos, consulta de existencias, actualización de información y control de entradas y salidas de inventario. De esta manera, se pretende reducir errores asociados al manejo manual de la información y facilitar el seguimiento de los productos disponibles.

El proyecto será desarrollado aplicando la metodología Scrum, permitiendo organizar el trabajo en iteraciones, definir requerimientos mediante historias de usuario y realizar entregas progresivas de las funcionalidades del sistema.

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

El sistema permitirá administrar la información asociada a los productos, incluyendo su registro, actualización, consulta y clasificación. Asimismo, permitirá consultar las existencias disponibles y mantener actualizadas las cantidades de inventario a partir del registro de movimientos de entrada y salida de productos.

Dentro del alcance funcional se contempla el desarrollo de los siguientes módulos y funcionalidades principales:

- Gestión de productos: registro, consulta, modificación y organización de los productos almacenados en el sistema.
- Clasificación de productos: organización de los productos mediante categorías y/o subcategorías para facilitar su búsqueda y administración.
- Consulta de inventario: visualización de las existencias actuales de cada producto.
- Movimientos de inventario: registro de entradas y salidas de productos, permitiendo mantener un historial de los movimientos realizados.
- Actualización de existencias: modificación de las cantidades disponibles de acuerdo con los movimientos registrados.
- Búsqueda y consulta: mecanismos de búsqueda y filtrado que permitan localizar productos e información del inventario de manera eficiente.
- Gestión de usuarios y permisos: control del acceso a las funcionalidades del sistema de acuerdo con los roles definidos para el proyecto.
- Persistencia de la información: almacenamiento de los datos del inventario y sus movimientos en una base de datos.
- Interfaz de usuario: desarrollo de una interfaz web clara, intuitiva y consistente que facilite la interacción con las funcionalidades principales del sistema.

El sistema estará orientado a usuarios encargados de la administración y control del inventario. Las funcionalidades disponibles para cada usuario dependerán de los roles y permisos establecidos durante el diseño del sistema.

El proyecto no contempla, dentro de su alcance inicial, funcionalidades relacionadas con facturación electrónica, contabilidad, comercio electrónico, integración con plataformas externas, control financiero o procesos empresariales que no estén directamente relacionados con la gestión básica del inventario. Estas funcionalidades podrán considerarse como posibles ampliaciones futuras.

El desarrollo se realizará bajo la metodología Scrum, mediante ciclos incrementales denominados Sprints. En cada Sprint se priorizarán, diseñarán, desarrollarán y validarán determinadas funcionalidades, permitiendo obtener incrementos funcionales del producto y realizar ajustes de acuerdo con los resultados de las revisiones y las necesidades identificadas durante el desarrollo.

## Funcionamiento general
El usuario accede al sistema mediante un navegador.
El frontend presenta formularios, tablas, filtros y opciones según los permisos del usuario.
El frontend envía solicitudes HTTP a la API REST.
La API verifica la autenticación, los permisos y los datos recibidos.
Cada solicitud se dirige al módulo correspondiente.
La capa de negocio aplica las reglas del inventario.
La capa de acceso a datos consulta o modifica la información almacenada en MySQL.
La API devuelve una respuesta en formato JSON y el frontend actualiza la interfaz.


Módulo	                Responsabilidad principal	                Funciones
Autenticación	          Controlar el acceso	                      Inicio y cierre de sesión
Usuarios y permisos	    Administrar roles y autorizaciones	      Crear usuarios, asignar roles y validar permisos
Productos	              Administrar productos	                    Registrar, consultar, modificar y desactivar
Categorías	            Clasificar productos	                    Crear categorías y subcategorías
Inventario	            Consultar existencias	                    Mostrar cantidades actuales y alertas
Movimientos	            Registrar cambios de inventario	          Entradas, salidas e historial
Existencias	            Actualizar cantidades	                    Incrementar o disminuir el inventario
Búsqueda	              Localizar información	                    Buscar y filtrar productos y movimientos
Auditoría	              Facilitar el seguimiento	                Registrar usuario, fecha y operación

## estructuracion modular inicial 

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


## Base de datos

La persistencia de la información del sistema se realizará mediante **MySQL**.

La estructura inicial de la base de datos contempla las siguientes entidades principales:

* **Usuarios:** gestión de las cuentas y acceso de los usuarios.
* **Roles:** definición de los roles y permisos de acceso.
* **Productos:** información y estado de los productos registrados.
* **Categorías:** clasificación de los productos, incluyendo categorías y subcategorías.
* **Proveedores:** información asociada a los proveedores de los productos.
* **Movimientos:** registro de las entradas y salidas de inventario.

La base de datos permitirá mantener centralizada la información del inventario y conservar el historial de los movimientos realizados.

## Estado actual

La estructura detallada de la base de datos se encuentra en proceso de definición. Posteriormente se incorporarán:

* Modelo entidad-relación.
* Definición de tablas, campos y relaciones.
* Claves primarias y foráneas.
* Restricciones e índices.
* Script SQL para la creación de la base de datos.
* Procedimientos almacenados, en caso de ser necesarios.