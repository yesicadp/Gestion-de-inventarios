
from flask import Blueprint, jsonify

from app.database.connection import obtener_conexion
from app.modules.authentication.decorators import requiere_token

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.get("/api/inventario")
@requiere_token
def consultar_inventario(datos_usuario):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id_producto,
                p.codigo,
                p.nombre,
                c.nombre AS categoria,
                p.existencia_actual,
                p.existencia_minima,
                CASE
                    WHEN p.existencia_actual <= p.existencia_minima
                    THEN 1
                    ELSE 0
                END AS existencia_baja
            FROM productos p
            LEFT JOIN categorias c
                ON p.categoria_id = c.id_categoria
            WHERE p.estado = 1
            ORDER BY p.nombre
        """)

        productos = cursor.fetchall()
        total_bajos = sum(
            1 for producto in productos
            if producto["existencia_baja"] == 1
        )

        return jsonify({
            "mensaje": "Inventario consultado correctamente",
            "total": len(productos),
            "total_existencias_bajas": total_bajos,
            "productos": productos
        }), 200

    except Exception:
        return jsonify({
            "mensaje": "No fue posible consultar el inventario"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()
