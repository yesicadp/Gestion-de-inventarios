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

## Plantilla para nuevas decisiones

## DEC-XXX: Título de la decisión

- Fecha: AAAA-MM-DD
- Estado: Propuesta / Aprobada / Rechazada
- Decisión: ¿Qué se decidió?
- ¿Por qué?: ¿Qué problema o necesidad motivó la decisión?
- ¿Para qué?: ¿Qué objetivo cumple?
- Alternativas consideradas: ¿Qué otras opciones se evaluaron?
- Consecuencias: ¿Qué ventajas, costos o riesgos produce?
