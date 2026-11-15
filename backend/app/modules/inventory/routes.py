from flask import Blueprint, jsonify

from app.database.connection import obtener_conexion
from app.modules.authentication.decorators import requiere_token
from app.shared.utilities.consultas import (
    booleano_opcional,
    entero_opcional,
    texto_opcional,
)

inventory_bp = Blueprint("inventory", __name__)

# Regla única de "existencia baja": existencia actual menor o igual al mínimo configurado.
EXISTENCIA_BAJA_SQL = "p.existencia_actual <= p.existencia_minima"


@inventory_bp.get("/api/inventario")
@requiere_token
def consultar_inventario(datos_usuario):
    # Filtros opcionales (se validan antes de abrir la conexión):
    #   q=texto               busca en nombre o código del producto
    #   categoria_id=N        incluye la categoría y sus subcategorías directas
    #   existencia_baja=1|0   solo productos con existencia baja (1) o sin alerta (0)
    texto = texto_opcional("q")
    categoria_id = entero_opcional("categoria_id")
    existencia_baja = booleano_opcional("existencia_baja")

    condiciones = ["p.estado = 1"]
    parametros = []

    if texto:
        condiciones.append("(p.nombre LIKE %s OR p.codigo LIKE %s)")
        parametros += [f"%{texto}%", f"%{texto}%"]

    if categoria_id is not None:
        condiciones.append("(p.categoria_id = %s OR c.categoria_padre_id = %s)")
        parametros += [categoria_id, categoria_id]

    if existencia_baja == 1:
        condiciones.append(EXISTENCIA_BAJA_SQL)
    elif existencia_baja == 0:
        condiciones.append(f"NOT ({EXISTENCIA_BAJA_SQL})")

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(f"""
            SELECT
                p.id_producto,
                p.codigo,
                p.nombre,
                p.categoria_id,
                c.nombre AS categoria,
                p.existencia_actual,
                p.existencia_minima,
                CASE
                    WHEN {EXISTENCIA_BAJA_SQL}
                    THEN 1
                    ELSE 0
                END AS existencia_baja
            FROM productos p
            LEFT JOIN categorias c
                ON p.categoria_id = c.id_categoria
            WHERE {" AND ".join(condiciones)}
            ORDER BY p.nombre
        """, parametros)

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
