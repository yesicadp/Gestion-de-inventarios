# Decisiones técnicas del backend

Este documento registra las decisiones tomadas durante el desarrollo del backend, junto con su contexto y las razones que las sustentan.

## Registro de decisiones

### DEC-001: Framework del backend

- **Estado:** Aprobada
- **Fecha:** 2026-09-05
- **Decisión:** Utilizar Flask para construir la API REST.
- **Contexto:** El proyecto requiere un backend en Python que exponga endpoints HTTP y permita organizar la aplicación por módulos.
- **Razones:**
  - Está definido en la documentación de arquitectura del proyecto.
  - El equipo ya inició la preparación del entorno con Flask.
  - Es suficiente para el alcance actual del sistema.
- **Alternativas consideradas:** FastAPI y Django.
- **Consecuencias:** La API se organizará mediante Flask y sus extensiones, manteniendo separadas la configuración, las rutas, la lógica de negocio y el acceso a datos.

### DEC-002: Control de dependencias

- **Estado:** Aprobada
- **Fecha:** 2026-09-05
- **Decisión:** Declarar las dependencias del backend en `backend/requirements.txt`.
- **Contexto:** El entorno virtual ya existe, pero el proyecto necesita una instalación reproducible para todos los integrantes.
- **Razones:**
  - Permite reinstalar el entorno de forma consistente.
  - Hace explícitos los componentes usados por el backend.
  - Facilita la incorporación de nuevos integrantes al proyecto.
- **Alternativas consideradas:** Instalar paquetes manualmente sin archivo de dependencias.
- **Consecuencias:** Toda dependencia nueva debe agregarse también a `backend/requirements.txt`.

## Plantilla para nuevas decisiones

### DEC-XXX: Título de la decisión

- **Estado:** Propuesta / Aprobada / Rechazada / Reemplazada
- **Fecha:** AAAA-MM-DD
- **Decisión:** Describir brevemente qué se decidió.
- **Contexto:** Explicar el problema o la necesidad.
- **Razones:**
  - Razón principal.
  - Razón adicional.
- **Alternativas consideradas:** Enumerar las opciones evaluadas.
- **Consecuencias:** Indicar qué efectos tendrá la decisión.
