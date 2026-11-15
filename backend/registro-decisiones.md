# Registro de decisiones del backend

Este archivo documenta las decisiones técnicas del backend, el motivo de cada decisión y el propósito que cumple.

## DEC-001: Usar Flask para la API

- Fecha: 2026-09-06
- Estado: Aprobada
- Decisión: Utilizar Flask para construir la API REST.
- ¿Por qué?: El proyecto está desarrollado en Python y Flask permite crear rutas HTTP de forma sencilla.
- ¿Para qué?: Para recibir solicitudes del frontend y devolver respuestas en formato JSON.
- Alternativas consideradas: FastAPI, Django REST Framework.

## DEC-002: Usar JWT para autenticación

- Fecha: 2026-09-06
- Estado: Aprobada
- Decisión: Utilizar tokens JWT después de validar el inicio de sesión.
- ¿Por qué?: El token permite identificar al usuario en solicitudes posteriores sin guardar una sesión tradicional en el servidor.
- ¿Para qué?: Para proteger las rutas que solo deben consultar usuarios autenticados.
- Alternativas consideradas: Sesiones tradicionales, API keys.

## DEC-003: Guardar la clave JWT en variables de entorno

- Fecha: 2026-09-06
- Estado: Aprobada
- Decisión: Leer `JWT_SECRET_KEY` desde el archivo `.env` mediante `python-dotenv`.
- ¿Por qué?: La clave secreta no debe quedar escrita directamente en el código ni publicarse en Git.
- ¿Para qué?: Para firmar y validar tokens JWT manteniendo la configuración separada del código.
- Alternativas consideradas: Escribir la clave en `main.py`.

## DEC-004: Proteger rutas con un decorador

- Fecha: 2026-09-06
- Estado: Aprobada
- Decisión: Usar el decorador `requiere_token` para validar el encabezado `Authorization`.
- ¿Por qué?: Permite reutilizar la misma validación en varias rutas protegidas.
- ¿Para qué?: Para aceptar únicamente solicitudes que envíen un token JWT válido.
- Formato esperado: `Authorization: Bearer TOKEN`.

## DEC-005: Habilitar CORS para pruebas locales

- Fecha: 2026-09-06
- Estado: Aprobada
- Decisión: Usar Flask-CORS para permitir la comunicación entre el frontend local y la API.
- ¿Por qué?: El frontend y el backend pueden ejecutarse en puertos diferentes durante el desarrollo.
- ¿Para qué?: Para que el navegador permita las solicitudes del frontend hacia la API.
- Nota: En producción se debe limitar el origen permitido en lugar de permitir cualquier origen.

## DEC-006: Separar la autenticación en un módulo

- Fecha: 2026-09-06
- Estado: Aprobada
- Decisión: Organizar la autenticación en el módulo `modules/authentication`, separando las rutas de login y la validación de tokens.
- ¿Por qué?: Evita concentrar toda la lógica en `main.py` y facilita el mantenimiento del proyecto.
- ¿Para qué?: Para que `routes.py` gestione el login y `decorators.py` valide los tokens JWT.
- Alternativas consideradas: Mantener toda la lógica de autenticación en `main.py`.
- Consecuencias: El proyecto queda más organizado y permite reutilizar el decorador `requiere_token` en diferentes rutas.

## DEC-007: Auditoría automática desde la aplicación

- Fecha: 2026-11-14
- Estado: Propuesta
- Decisión: Cada ruta que crea, edita, desactiva o mueve existencias llama a `registrar_auditoria` con el mismo cursor, antes del commit. No se usan triggers.
- ¿Por qué?: La base de datos no conoce el usuario autenticado (viene del token JWT) y los triggers no existen en el esquema actual. Guardar la auditoría en la misma transacción garantiza que acción y registro se guarden juntos o ninguno.
- ¿Para qué?: Cumplir HU-18 y HU-19 sin depender de que alguien registre las acciones manualmente.
- Consecuencias: Quien modifique la base de datos directamente por SQL no genera auditoría. Las nuevas rutas de escritura deben llamar a `registrar_auditoria`.

## DEC-008: Permisos por rol validados en el backend

- Fecha: 2026-11-14
- Estado: Propuesta
- Decisión: El decorador `requiere_admin` (`shared/security/permisos.py`) reutiliza `requiere_token` y exige el rol Administrador para crear y editar productos, crear categorías y consultar la auditoría. Consultar, buscar y registrar movimientos queda para cualquier usuario autenticado.
- ¿Por qué?: Ocultar botones en el frontend no protege la API.
- Consecuencias: Un usuario normal recibe 403. El frontend actual muestra "Tu sesión no está autorizada" ante 401 y 403.

## DEC-009: Ampliar las rutas sin cambiar el formato JSON existente

- Fecha: 2026-11-14
- Estado: Propuesta
- Decisión: Se conservan las claves que el frontend ya lee (`mensaje`, `total`, `productos`, `categorias`, `total_existencias_bajas`, `existencia_actual`...). Los filtros, la paginación y los campos nuevos son opcionales o se agregan sin quitar nada.
- ¿Por qué?: El dashboard, el listado y el formulario de productos ya consumen esos nombres.
- Consecuencias: Las fechas de movimientos y auditoría se devuelven en ISO 8601 (jsonify las convertía a formato HTTP/GMT, lo que desplazaba la hora en el navegador).

## DEC-010: Regla de existencia baja

- Fecha: 2026-11-14
- Estado: Propuesta
- Decisión: Un producto activo tiene existencia baja cuando `existencia_actual <= existencia_minima`.
- ¿Por qué?: Es el criterio que ya usaba `GET /api/inventario` y el dashboard. La HU-12 dice "por debajo del mínimo", que sería `<`.
- Consecuencias: Si el equipo prefiere `<`, hay que cambiar `EXISTENCIA_BAJA_SQL` en `inventory/routes.py`.

## Plantilla para nuevas decisiones

## DEC-XXX: Título de la decisión

- Fecha: AAAA-MM-DD
- Estado: Propuesta / Aprobada / Rechazada
- Decisión: ¿Qué se decidió?
- ¿Por qué?: ¿Qué problema o necesidad motivó la decisión?
- ¿Para qué?: ¿Qué objetivo cumple?
- Alternativas consideradas: ¿Qué otras opciones se evaluaron?
- Consecuencias: ¿Qué ventajas, costos o riesgos produce?
