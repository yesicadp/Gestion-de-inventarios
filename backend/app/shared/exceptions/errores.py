"""Errores de validación de la solicitud (parámetros de consulta, filtros, etc.)."""
from flask import jsonify


class ErrorValidacion(Exception):
    """Se lanza ANTES de abrir la conexión a la base de datos; Flask lo convierte en JSON."""

    def __init__(self, mensaje, codigo=400):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo


def registrar_manejadores(app):
    @app.errorhandler(ErrorValidacion)
    def _error_validacion(error):
        return jsonify({"mensaje": error.mensaje}), error.codigo
