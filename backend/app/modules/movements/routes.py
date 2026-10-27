
from flask import Blueprint, jsonify, request

from app.database.connection import obtener_conexion
from app.modules.authentication.decorators import requiere_token

movements_bp = Blueprint("movements", __name__)


@movements_bp.get("/api/movimientos")
@requiere_token
def listar_movimientos(datos_usuario):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                m.id_movimiento,
                m.producto_id,
                p.nombre AS producto,
                m.usuario_id,
                m.tipo_movimiento,
                m.cantidad,
                m.motivo,
                m.fecha,
                m.existencia_resultante
            FROM movimientos m
            INNER JOIN productos p
                ON m.producto_id = p.id_producto
            ORDER BY m.fecha DESC, m.id_movimiento DESC
        """)

        movimientos = cursor.fetchall()

        return jsonify({
            "mensaje": "Movimientos consultados correctamente",
            "total": len(movimientos),
            "movimientos": movimientos
        }), 200

    except Exception:
        return jsonify({
            "mensaje": "No fue posible consultar los movimientos"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


@movements_bp.post("/api/movimientos")
@requiere_token
def registrar_movimiento(datos_usuario):
    conexion = None
    cursor = None

    try:
        datos = request.get_json(silent=True) or {}

        producto_id = datos.get("producto_id")
        tipo = str(datos.get("tipo_movimiento", "")).strip().lower()
        cantidad = datos.get("cantidad")
        motivo = str(datos.get("motivo", "")).strip()

        if not producto_id or tipo not in ("entrada", "salida"):
            return jsonify({
                "mensaje": "Indica un producto y un tipo válido: entrada o salida"
            }), 400

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            return jsonify({
                "mensaje": "La cantidad debe ser un número entero mayor que cero"
            }), 400

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        conexion.start_transaction()

        cursor.execute("""
            SELECT existencia_actual
            FROM productos
            WHERE id_producto = %s AND estado = 1
            FOR UPDATE
        """, (producto_id,))

        producto = cursor.fetchone()

        if producto is None:
            conexion.rollback()
            return jsonify({
                "mensaje": "El producto no existe o está inactivo"
            }), 404

        existencia_actual = producto["existencia_actual"]

        if tipo == "entrada":
            nueva_existencia = existencia_actual + cantidad
        else:
            nueva_existencia = existencia_actual - cantidad

            if nueva_existencia < 0:
                conexion.rollback()
                return jsonify({
                    "mensaje": "No hay existencias suficientes para esa salida"
                }), 400

        cursor.execute("""
            UPDATE productos
            SET existencia_actual = %s
            WHERE id_producto = %s
        """, (nueva_existencia, producto_id))

        cursor.execute("""
            INSERT INTO movimientos (
                producto_id,
                usuario_id,
                tipo_movimiento,
                cantidad,
                motivo,
                existencia_resultante
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            producto_id,
            datos_usuario.get("usuario_id"),
            tipo,
            cantidad,
            motivo,
            nueva_existencia
        ))

        conexion.commit()

        return jsonify({
            "mensaje": "Movimiento registrado correctamente",
            "tipo_movimiento": tipo,
            "cantidad": cantidad,
            "existencia_resultante": nueva_existencia
        }), 201

    except Exception:
        if conexion is not None:
            conexion.rollback()

        return jsonify({
            "mensaje": "No fue posible registrar el movimiento. Verifica los datos y la estructura de la base de datos."
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
