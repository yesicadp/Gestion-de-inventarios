
from flask import Blueprint, jsonify

from app.database.connection import obtener_conexion
from app.shared.security.permisos import requiere_admin


roles_bp = Blueprint("roles", __name__)


@roles_bp.get("/api/roles")
@requiere_admin
def consultar_roles(datos_usuario):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_rol, nombre_rol
            FROM roles
            ORDER BY id_rol ASC
        """)

        roles = cursor.fetchall()

        return jsonify({
            "mensaje": "Roles consultados correctamente",
            "roles": roles
        }), 200

    except Exception as error:
        print(f"Error al consultar roles: {error}")
        return jsonify({
            "mensaje": "No fue posible consultar los roles"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()
