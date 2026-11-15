"""Permisos por rol. Se apoya en requiere_token (módulo authentication) sin modificarlo.

Roles del sistema: "Administrador" (acceso total) y "Usuario" (consulta, movimientos y búsqueda).
El rol se lee del token JWT, que lo firma el backend al iniciar sesión.
"""
from functools import wraps

from flask import jsonify

from app.modules.authentication.decorators import requiere_token

ROL_ADMINISTRADOR = "Administrador"


def requiere_admin(funcion):
    """Exige token válido Y rol Administrador. La vista recibe datos_usuario como primer argumento."""

    @requiere_token
    @wraps(funcion)
    def decorador(datos_usuario, *args, **kwargs):
        if datos_usuario.get("rol") != ROL_ADMINISTRADOR:
            return jsonify({
                "mensaje": "Solo un administrador puede realizar esta acción"
            }), 403

        return funcion(datos_usuario, *args, **kwargs)

    return decorador
