# 7. Avances del proyecto

## Estado actual

**Última actualización:** 13/11/2026

**Estado general:** Desarrollo de funcionalidades y documentación de los sprints.

## Historial de avances por sprint

### Sprint 0 — Documentación y planificación

**Objetivo:** Definir alcance, arquitectura, estructura de carpetas, mockups e historias de usuario.

**Completado:**

- [x] Descripción general, objetivos y alcance del proyecto.
- [x] Estructura de carpetas del repositorio (frontend / backend / database / documentation).
- [x] Arquitectura definida (monolito por capas).
- [x] Mockups de las pantallas principales (9 pantallas).
- [x] Historias de usuario (23 historias, 8 módulos).
- [x] Modelo entidad-relación de la base de datos.
- [x] Definición del framework backend.

### Sprint 1 — Autenticación y gestión de usuarios

**Estado:** Pendiente de documentar avances y resultados.

### Sprint 3 — Gestión de inventario y movimientos

**Objetivo:** Verificar la estructura de la base de datos y el registro de entradas y salidas de productos.

**Completado:**

- [x] Revisión de las tablas productos y movimientos.
- [x] Verificación de las relaciones entre productos, usuarios y movimientos.
- [x] Prueba manual de registro de entradas y salidas mediante SQL.
- [x] Verificación de los campos fecha, motivo y existencia resultante.
- [x] Creación del script `pruebas-sprint-3.sql`.
- [x] Ejecución de pruebas con transacciones y rollback para conservar los datos originales.

**Resultado de las pruebas:**

Se realizó una prueba con el producto DEMO-001:

- Stock inicial: 20 unidades.
- Entrada: 5 unidades.
- Stock después de la entrada: 25 unidades.
- Salida: 3 unidades.
- Stock después de la salida: 22 unidades.
- Resultado del rollback: stock restaurado a 20 unidades.

**Evidencias:**

Las capturas de las pruebas se encuentran en `documentation/evidencias/sprint-3/`:

- `01-estructura-productos.png`
- `02-estructura-movimientos.png`
- `03-relaciones-tablas.png`
- `04-stock-inicial-producto.png`
- `05-entrada-salida-movimientos.png`
- `06-rollback-stock-restaurado.png`

### Sprint 4 — Auditoría y optimización de base de datos

**Objetivo:** Revisar la estructura de auditoría, sus relaciones e índices, y actualizar el script de creación de la base de datos.

**Completado:**

- [x] Revisión de la tabla auditoria.
- [x] Verificación de la relación entre auditoría y usuarios.
- [x] Verificación de los campos módulo, acción, fecha y detalle.
- [x] Revisión de los índices de las tablas.
- [x] Actualización de `database/schema.sql` con las restricciones e índices existentes.
- [x] Creación del script `verificacion-sprint-4.sql`.
- [x] Verificación de la estructura de la base de datos.

**Pendiente:**

- [ ] Implementar y verificar el registro automático de acciones en auditoría.
- [ ] Verificar la integración de auditoría con las operaciones del sistema.

**Resultado de la revisión:**

Se confirmó que la tabla de auditoría cuenta con su estructura, relación con usuarios e índices. Sin embargo, no se encontraron triggers, procedimientos, funciones ni referencias en el backend que permitan confirmar el registro automático de acciones.

**Evidencias:**

Las capturas de las verificaciones se encuentran en `documentation/evidencias/sprint-4/`:

- `07-estructura-auditoria.png`
- `08-relacion-auditoria-usuarios.png`
- `09-indices-base-datos.png`
- `10-verificacion-triggers.png`
- `11-verificacion-procedimientos.png`
- `12-verificacion-funciones.png`
- `13-registros-auditoria.png`

## Archivos relevantes

- `database/schema.sql`
- `database/scripts/pruebas-sprint-3.sql`
- `database/scripts/verificacion-sprint-4.sql`
- `documentation/diagrama-er.png`
- `documentation/evidencias/sprint-3/`
- `documentation/evidencias/sprint-4/`

## Próximas actividades

- Completar la documentación técnica del proyecto.
- Revisar y actualizar el README.
- Verificar la integración de las funcionalidades pendientes.
- Documentar los resultados de las pruebas y los avances restantes.
