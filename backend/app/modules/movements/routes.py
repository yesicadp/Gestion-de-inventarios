from flask import Blueprint, jsonify, request

from app.database.connection import obtener_conexion
from app.modules.authentication.decorators import requiere_token
from app.shared.utilities.auditoria import registrar_auditoria
from app.shared.utilities.consultas import (
    datos_paginacion,
    entero_opcional,
    fecha_iso,
    paginacion,
    rango_fechas,
    texto_opcional,
    tipo_movimiento_opcional,
)

movements_bp = Blueprint("movements", __name__)


@movements_bp.get("/api/movimientos")
@requiere_token
def listar_movimientos(datos_usuario):
    # Filtros opcionales (se validan antes de abrir la conexión):
    #   producto_id=N  usuario_id=N  tipo=ENTRADA|SALIDA
    #   desde=AAAA-MM-DD  hasta=AAAA-MM-DD (incluye todo ese día)
    #   q=texto (nombre o código del producto)
    #   pagina=N&por_pagina=N (si no se envían, devuelve todo el historial)
    producto_id = entero_opcional("producto_id")
    usuario_id = entero_opcional("usuario_id")
    tipo = tipo_movimiento_opcional()
    desde, hasta_exclusivo = rango_fechas()
    texto = texto_opcional("q")
    pagina = paginacion()

    condiciones = []
    parametros = []

    if producto_id is not None:
        condiciones.append("m.producto_id = %s")
        parametros.append(producto_id)

    if usuario_id is not None:
        condiciones.append("m.usuario_id = %s")
        parametros.append(usuario_id)

    if tipo:
        condiciones.append("m.tipo_movimiento = %s")
        parametros.append(tipo)

    if desde:
        condiciones.append("m.fecha >= %s")
        parametros.append(desde)

    if hasta_exclusivo:
        condiciones.append("m.fecha < %s")
        parametros.append(hasta_exclusivo)

    if texto:
        condiciones.append("(p.nombre LIKE %s OR p.codigo LIKE %s)")
        parametros += [f"%{texto}%", f"%{texto}%"]

    donde = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        limite = ""
        parametros_consulta = list(parametros)

        if pagina is not None:
            numero, por_pagina = pagina
            limite = "LIMIT %s OFFSET %s"
            parametros_consulta += [por_pagina, (numero - 1) * por_pagina]

        cursor.execute(f"""
            SELECT
                m.id_movimiento,
                m.producto_id,
                p.codigo,
                p.nombre AS producto,
                m.usuario_id,
                u.nombre AS usuario,
                m.tipo_movimiento,
                m.cantidad,
                m.motivo,
                m.fecha,
                m.existencia_resultante
            FROM movimientos m
            INNER JOIN productos p
                ON m.producto_id = p.id_producto
            INNER JOIN usuarios u
                ON m.usuario_id = u.id_usuario
            {donde}
            ORDER BY m.fecha DESC, m.id_movimiento DESC
            {limite}
        """, parametros_consulta)

        movimientos = cursor.fetchall()

        for movimiento in movimientos:
            movimiento["fecha"] = fecha_iso(movimiento["fecha"])

        respuesta = {
            "mensaje": "Movimientos consultados correctamente",
            "total": len(movimientos),
            "movimientos": movimientos
        }

        if pagina is not None:
            cursor.execute(f"""
                SELECT COUNT(*) AS total
                FROM movimientos m
                INNER JOIN productos p
                    ON m.producto_id = p.id_producto
                {donde}
            """, parametros)
            total = cursor.fetchone()["total"]
            respuesta["total"] = total
            respuesta.update(datos_paginacion(pagina[0], pagina[1], total))

        return jsonify(respuesta), 200

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
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "Envía los datos del movimiento en formato JSON"
        }), 400

    producto_id = datos.get("producto_id")
    tipo = str(datos.get("tipo_movimiento", "")).strip().upper()
    cantidad = datos.get("cantidad")
    motivo = datos.get("motivo")

    if isinstance(producto_id, bool) or not isinstance(producto_id, int) or producto_id <= 0:
        return jsonify({
            "mensaje": "producto_id debe ser un entero positivo"
        }), 400

    if tipo not in ("ENTRADA", "SALIDA"):
        return jsonify({
            "mensaje": "El tipo de movimiento debe ser entrada o salida"
        }), 400

    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({
            "mensaje": "La cantidad debe ser un número entero mayor que cero"
        }), 400

    if not isinstance(motivo, str) or not motivo.strip():
        return jsonify({
            "mensaje": "El motivo del movimiento es obligatorio"
        }), 400

    motivo = motivo.strip()

    if len(motivo) > 255:
        return jsonify({
            "mensaje": "El motivo no puede superar los 255 caracteres"
        }), 400

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        conexion.start_transaction()

        # FOR UPDATE bloquea la fila del producto hasta el commit: dos salidas simultáneas
        # no pueden leer la misma existencia ni dejar el stock en negativo.
        cursor.execute("""
            SELECT id_producto, codigo, nombre, existencia_actual, existencia_minima, estado
            FROM productos
            WHERE id_producto = %s
            FOR UPDATE
        """, (producto_id,))

        producto = cursor.fetchone()

        if producto is None:
            conexion.rollback()
            return jsonify({
                "mensaje": "El producto no existe"
            }), 404

        if not producto["estado"]:
            conexion.rollback()
            return jsonify({
                "mensaje": "El producto está inactivo; no admite movimientos"
            }), 409

        existencia_anterior = producto["existencia_actual"]

        if tipo == "ENTRADA":
            nueva_existencia = existencia_anterior + cantidad
        else:
            nueva_existencia = existencia_anterior - cantidad

            if nueva_existencia < 0:
                conexion.rollback()
                return jsonify({
                    "mensaje": "No hay existencias suficientes para esa salida",
                    "existencia_disponible": existencia_anterior,
                    "cantidad_solicitada": cantidad
                }), 400

        usuario_id = datos_usuario.get("usuario_id")

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
            usuario_id,
            tipo,
            cantidad,
            motivo,
            nueva_existencia
        ))

        movimiento_id = cursor.lastrowid

        registrar_auditoria(
            cursor,
            usuario_id,
            "movimientos",
            tipo,
            f"{producto['codigo']}: {existencia_anterior} -> {nueva_existencia} ({motivo})"
        )

        cursor.execute(
            "SELECT fecha FROM movimientos WHERE id_movimiento = %s",
            (movimiento_id,)
        )
        fecha = cursor.fetchone()["fecha"]

        # Un solo commit: existencia, movimiento y auditoría se guardan juntos o no se guarda nada.
        conexion.commit()

        existencia_baja = 1 if nueva_existencia <= producto["existencia_minima"] else 0

        return jsonify({
            "mensaje": "Movimiento registrado correctamente",
            "tipo_movimiento": tipo,
            "cantidad": cantidad,
            "existencia_resultante": nueva_existencia,
            "movimiento": {
                "id_movimiento": movimiento_id,
                "producto_id": producto_id,
                "codigo": producto["codigo"],
                "producto": producto["nombre"],
                "usuario_id": usuario_id,
                "tipo_movimiento": tipo,
                "cantidad": cantidad,
                "motivo": motivo,
                "fecha": fecha_iso(fecha),
                "existencia_anterior": existencia_anterior,
                "existencia_resultante": nueva_existencia,
                "existencia_minima": producto["existencia_minima"],
                "existencia_baja": existencia_baja
            }
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
