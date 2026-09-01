# 4. Avances de arquitectura

## Estilo arquitectónico elegido

**Monolito organizado por capas.**

### Justificación
- El equipo es pequeño y trabaja en un solo repositorio; un monolito reduce la complejidad de despliegue y coordinación frente a una arquitectura de microservicios.
- La separación por capas (presentación → negocio → acceso a datos) mantiene el código organizado y facilita que cada subequipo (frontend / backend / base de datos) trabaje con una interfaz clara hacia las demás capas.
- Es un estilo apropiado para el alcance del proyecto (gestión básica de inventario), evitando sobre-ingeniería.

## Capas del sistema

| Capa | Responsabilidad | Tecnología |
|---|---|---|
| Presentación | Interfaz de usuario, formularios, tablas, validaciones de entrada básicas | HTML, CSS, JavaScript |
| API / Aplicación | Exponer endpoints REST, autenticación, orquestar la lógica de negocio | Python (framework por definir: Flask o Django) |
| Negocio | Reglas del inventario (validaciones de existencia, permisos por rol) | Python |
| Acceso a datos | Consultas y persistencia | Python + conector MySQL |
| Base de datos | Almacenamiento de la información | MySQL |

## Comunicación entre capas

- El frontend se comunica con el backend **exclusivamente vía HTTP/JSON**, consumiendo una API REST — no hay acceso directo del frontend a la base de datos.
- La API expone un conjunto de endpoints por módulo (ej. `/products`, `/categories`, `/inventory`, `/movements`, `/users`, `/auth`).
- El formato de intercambio de datos es JSON en ambas direcciones.

## Decisiones pendientes

| Decisión | Estado | Notas |
|---|---|---|
| Framework backend (Flask vs Django) | Pendiente | Lo definirá el equipo de backend según necesidades de la API |
| Mecanismo de autenticación (sesión vs JWT) | Pendiente | Afecta al frontend (manejo de token) y a la API |
| Modelo entidad-relación definitivo | Pendiente | Ver `08-evidencias-funcionamiento.md` y carpeta `database/` |
| Despliegue (hosting de frontend/backend/BD) | Pendiente | Definir antes de la entrega final |
