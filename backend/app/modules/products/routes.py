from flask import Blueprint, jsonify, request
from mysql.connector import IntegrityError

from app.database.connection import obtener_conexion
from app.modules.authentication.decorators import requiere_token
from app.shared.security.permisos import requiere_admin
from app.shared.utilities.auditoria import registrar_auditoria
from app.shared.utilities.consultas import (
    entero_opcional,
    estado_opcional,
    texto_opcional,
)

products_bp = Blueprint("products", __name__)


@products_bp.get("/api/productos")
@requiere_token
def listar_productos(datos_usuario):
    # Búsqueda y filtros opcionales, combinables (se validan antes de abrir la conexión):
    #   q=texto               busca en nombre o código
    #   categoria_id=N        incluye la categoría y sus subcategorías directas
    #   estado=activo|inactivo|todos   (también 1 / 0)
    texto = texto_opcional("q")
    categoria_id = entero_opcional("categoria_id")
    estado = estado_opcional()

    condiciones = []
    parametros = []

    if texto:
        condiciones.append("(p.nombre LIKE %s OR p.codigo LIKE %s)")
        parametros += [f"%{texto}%", f"%{texto}%"]

    if categoria_id is not None:
        condiciones.append("(p.categoria_id = %s OR c.categoria_padre_id = %s)")
        parametros += [categoria_id, categoria_id]

    if estado is not None:
        condiciones.append("p.estado = %s")
        parametros.append(estado)

    donde = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(f"""
            SELECT
                p.id_producto,
                p.nombre,
                p.codigo,
                p.categoria_id,
                c.nombre AS categoria,
                p.existencia_actual,
                p.existencia_minima,
                p.estado
            FROM productos p
            INNER JOIN categorias c
                ON p.categoria_id = c.id_categoria
            {donde}
            ORDER BY p.id_producto DESC
        """, parametros)

        productos = cursor.fetchall()

        return jsonify({
            "mensaje": "Productos consultados correctamente",
            "total": len(productos),
            "productos": productos
        }), 200

    except Exception:
        return jsonify({
            "mensaje": "Error al consultar los productos"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


@products_bp.post("/api/productos")
@requiere_admin
def registrar_producto(datos_usuario):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "Debes enviar los datos del producto en formato JSON"
        }), 400

    nombre = datos.get("nombre")
    codigo = datos.get("codigo")
    categoria_id = datos.get("categoria_id")
    existencia_actual = datos.get("existencia_actual", 0)
    existencia_minima = datos.get("existencia_minima", 0)
    estado = datos.get("estado", 1)

    if not isinstance(nombre, str) or not nombre.strip():
        return jsonify({
            "mensaje": "El nombre del producto es obligatorio"
        }), 400

    if not isinstance(codigo, str) or not codigo.strip():
        return jsonify({
            "mensaje": "El codigo del producto es obligatorio"
        }), 400

    try:
        if isinstance(categoria_id, bool):
            raise ValueError

        categoria_id = int(categoria_id)

        if isinstance(existencia_actual, bool):
            raise ValueError

        existencia_actual = int(existencia_actual)

        if isinstance(existencia_minima, bool):
            raise ValueError

        existencia_minima = int(existencia_minima)

        if isinstance(estado, bool):
            estado = int(estado)

        if isinstance(estado, str) and estado not in ("0", "1"):
            raise ValueError

        estado = int(estado)

    except (ValueError, TypeError):
        return jsonify({
            "mensaje": (
                "Categoria y existencias deben ser numeros enteros; "
                "el estado debe ser 0 o 1"
            )
        }), 400

    if categoria_id <= 0:
        return jsonify({
            "mensaje": "La categoria debe ser valida"
        }), 400

    if existencia_actual < 0 or existencia_minima < 0:
        return jsonify({
            "mensaje": "Las existencias no pueden ser negativas"
        }), 400

    if estado not in (0, 1):
        return jsonify({
            "mensaje": "El estado debe ser 1 (activo) o 0 (inactivo)"
        }), 400

    nombre = nombre.strip()
    codigo = codigo.strip()

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_categoria
            FROM categorias
            WHERE id_categoria = %s
        """, (categoria_id,))

        if cursor.fetchone() is None:
            return jsonify({
                "mensaje": "La categoria seleccionada no existe"
            }), 400

        cursor.execute("""
            SELECT id_producto
            FROM productos
            WHERE codigo = %s
        """, (codigo,))

        if cursor.fetchone() is not None:
            return jsonify({
                "mensaje": "Ya existe un producto con ese codigo"
            }), 409

        cursor.execute("""
            INSERT INTO productos (
                nombre,
                codigo,
                categoria_id,
                existencia_actual,
                existencia_minima,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nombre,
            codigo,
            categoria_id,
            existencia_actual,
            existencia_minima,
            estado
        ))

        producto_id = cursor.lastrowid

        registrar_auditoria(
            cursor,
            datos_usuario.get("usuario_id"),
            "productos",
            "CREAR",
            f"Producto {codigo}: {nombre} (existencia inicial {existencia_actual})"
        )

        conexion.commit()

        return jsonify({
            "mensaje": "Producto registrado correctamente",
            "producto": {
                "id_producto": producto_id,
                "nombre": nombre,
                "codigo": codigo,
                "categoria_id": categoria_id,
                "existencia_actual": existencia_actual,
                "existencia_minima": existencia_minima,
                "estado": estado
            }
        }), 201

    except IntegrityError as error:
        if conexion is not None:
            conexion.rollback()

        if error.errno == 1062:
            return jsonify({
                "mensaje": "Ya existe un producto con ese codigo"
            }), 409

        return jsonify({
            "mensaje": "No se pudo registrar el producto por una restricción de la base de datos"
        }), 400

    except Exception:
        if conexion is not None:
            conexion.rollback()

        return jsonify({
            "mensaje": "Error interno al registrar el producto"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


@products_bp.get("/api/productos/<int:id_producto>")
@requiere_token
def consultar_producto(datos_usuario, id_producto):   
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id_producto,
                p.nombre,
                p.codigo,
                p.categoria_id,
                c.nombre AS categoria,
                p.existencia_actual,
                p.existencia_minima,
                p.estado
            FROM productos p
            INNER JOIN categorias c
                ON p.categoria_id = c.id_categoria
            WHERE p.id_producto = %s
        """, (id_producto,))

        producto = cursor.fetchone()

        if producto is None:
            return jsonify({
                "mensaje": "El producto no existe"
            }), 404

        return jsonify({
            "mensaje": "Producto consultado correctamente",
            "producto": producto
        }), 200

    except Exception:
        return jsonify({
            "mensaje": "Error al consultar el producto"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


@products_bp.put("/api/productos/<int:id_producto>")
@requiere_admin
def actualizar_producto(datos_usuario, id_producto):    
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "Debes enviar los datos en formato JSON"
        }), 400

    nombre = datos.get("nombre")
    codigo = datos.get("codigo")
    categoria_id = datos.get("categoria_id")
    existencia_actual = datos.get("existencia_actual")
    existencia_minima = datos.get("existencia_minima")
    estado = datos.get("estado")

    if not isinstance(nombre, str) or not nombre.strip():
        return jsonify({
            "mensaje": "El nombre del producto es obligatorio"
        }), 400

    if not isinstance(codigo, str) or not codigo.strip():
        return jsonify({
            "mensaje": "El código del producto es obligatorio"
        }), 400

    try:
        if any(isinstance(valor, bool) for valor in (
            categoria_id, existencia_actual, existencia_minima, estado
        )):
            raise ValueError

        categoria_id = int(categoria_id)
        existencia_actual = int(existencia_actual)
        existencia_minima = int(existencia_minima)
        estado = int(estado)

    except (ValueError, TypeError):
        return jsonify({
            "mensaje": "Categoría y existencias deben ser enteros; el estado debe ser 0 o 1"
        }), 400

    if categoria_id <= 0:
        return jsonify({
            "mensaje": "La categoría debe ser válida"
        }), 400

    if existencia_actual < 0 or existencia_minima < 0:
        return jsonify({
            "mensaje": "Las existencias no pueden ser negativas"
        }), 400

    if estado not in (0, 1):
        return jsonify({
            "mensaje": "El estado debe ser 1 (activo) o 0 (inactivo)"
        }), 400

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_producto, nombre, codigo, categoria_id,
                   existencia_actual, existencia_minima, estado
            FROM productos
            WHERE id_producto = %s
        """, (id_producto,))

        anterior = cursor.fetchone()

        if anterior is None:
            return jsonify({
                "mensaje": "El producto no existe"
            }), 404

        cursor.execute("""
            SELECT id_categoria
            FROM categorias
            WHERE id_categoria = %s
        """, (categoria_id,))

        if cursor.fetchone() is None:
            return jsonify({
                "mensaje": "La categoría seleccionada no existe"
            }), 400

        cursor.execute("""
            SELECT id_producto
            FROM productos
            WHERE codigo = %s AND id_producto != %s
        """, (codigo.strip(), id_producto))

        if cursor.fetchone() is not None:
            return jsonify({
                "mensaje": "Ya existe otro producto con ese código"
            }), 409

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                codigo = %s,
                categoria_id = %s,
                existencia_actual = %s,
                existencia_minima = %s,
                estado = %s
            WHERE id_producto = %s
        """, (
            nombre.strip(),
            codigo.strip(),
            categoria_id,
            existencia_actual,
            existencia_minima,
            estado,
            id_producto
        ))

        nuevos = {
            "nombre": nombre.strip(),
            "codigo": codigo.strip(),
            "categoria_id": categoria_id,
            "existencia_actual": existencia_actual,
            "existencia_minima": existencia_minima,
            "estado": estado
        }
        cambios = []

        for campo, valor_nuevo in nuevos.items():
            valor_anterior = anterior[campo]

            if campo == "estado":
                valor_anterior = int(bool(valor_anterior))

            if valor_anterior != valor_nuevo:
                cambios.append(f"{campo} {valor_anterior} -> {valor_nuevo}")

        if cambios:
            if anterior["estado"] and estado == 0:
                accion = "DESACTIVAR"
            elif not anterior["estado"] and estado == 1:
                accion = "ACTIVAR"
            else:
                accion = "EDITAR"

            registrar_auditoria(
                cursor,
                datos_usuario.get("usuario_id"),
                "productos",
                accion,
                f"Producto {anterior['codigo']}: " + "; ".join(cambios)
            )

        conexion.commit()

        return jsonify({
            "mensaje": "Producto actualizado correctamente"
        }), 200

    except IntegrityError:
        if conexion is not None:
            conexion.rollback()

        return jsonify({
            "mensaje": "No se pudo actualizar el producto por una restricción de la base de datos"
        }), 409

    except Exception:
        if conexion is not None:
            conexion.rollback()

        return jsonify({
            "mensaje": "Error interno al actualizar el producto"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()
