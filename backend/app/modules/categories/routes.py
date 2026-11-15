from flask import Blueprint, jsonify, request

from app.database.connection import obtener_conexion
from app.modules.authentication.decorators import requiere_token
from app.shared.security.permisos import requiere_admin
from app.shared.utilities.auditoria import registrar_auditoria

categories_bp = Blueprint("categories", __name__)


@categories_bp.get("/api/categorias")
@requiere_token
def listar_categorias(datos_usuario):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_categoria, nombre, categoria_padre_id
            FROM categorias
            ORDER BY id_categoria DESC
        """)
        categorias = cursor.fetchall()

        return jsonify({
            "mensaje": "Categorías consultadas correctamente",
            "total": len(categorias),
            "categorias": categorias
        }), 200

    except Exception:
        return jsonify({
            "mensaje": "No fue posible consultar las categorías"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


@categories_bp.post("/api/categorias")
@requiere_admin
def registrar_categoria(datos_usuario):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"mensaje": "Envía los datos en formato JSON"}), 400

    nombre = datos.get("nombre")
    categoria_padre_id = datos.get("categoria_padre_id")

    if not isinstance(nombre, str) or not nombre.strip():
        return jsonify({"mensaje": "El nombre de la categoría es obligatorio"}), 400

    nombre = nombre.strip()
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        if categoria_padre_id is not None:
            try:
                categoria_padre_id = int(categoria_padre_id)
                if categoria_padre_id <= 0:
                    raise ValueError
            except (TypeError, ValueError):
                return jsonify({
                    "mensaje": "categoria_padre_id debe ser un entero positivo"
                }), 400

            cursor.execute(
                "SELECT id_categoria FROM categorias WHERE id_categoria = %s",
                (categoria_padre_id,)
            )
            if cursor.fetchone() is None:
                return jsonify({
                    "mensaje": "La categoría padre no existe"
                }), 404

        cursor.execute(
            "SELECT id_categoria FROM categorias WHERE LOWER(nombre) = LOWER(%s)",
            (nombre,)
        )
        if cursor.fetchone() is not None:
            return jsonify({"mensaje": "Ya existe una categoría con ese nombre"}), 409

        cursor.execute("""
            INSERT INTO categorias (nombre, categoria_padre_id)
            VALUES (%s, %s)
        """, (nombre, categoria_padre_id))

        nuevo_id = cursor.lastrowid

        registrar_auditoria(
            cursor,
            datos_usuario.get("usuario_id"),
            "categorias",
            "CREAR",
            f"Categoría {nuevo_id}: {nombre}"
        )

        conexion.commit()

        return jsonify({
            "mensaje": "Categoría registrada correctamente",
            "categoria": {
                "id_categoria": nuevo_id,
                "nombre": nombre,
                "categoria_padre_id": categoria_padre_id
            }
        }), 201

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        return jsonify({
            "mensaje": "No fue posible registrar la categoría"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


@categories_bp.delete("/api/categorias/<int:id_categoria>")
@requiere_admin
def eliminar_categoria(datos_usuario, id_categoria):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Verificar que la categoría exista
        cursor.execute(
            "SELECT id_categoria, nombre FROM categorias WHERE id_categoria = %s",
            (id_categoria,)
        )
        categoria = cursor.fetchone()

        if categoria is None:
            return jsonify({
                "mensaje": "La categoría no existe"
            }), 404

        # Verificar si tiene productos asociados
        cursor.execute(
            "SELECT id_producto FROM productos WHERE categoria_id = %s LIMIT 1",
            (id_categoria,)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                "mensaje": "No se puede eliminar la categoría porque tiene productos asociados"
            }), 409

        # Verificar si tiene subcategorías
        cursor.execute(
            "SELECT id_categoria FROM categorias WHERE categoria_padre_id = %s LIMIT 1",
            (id_categoria,)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                "mensaje": "No se puede eliminar la categoría porque tiene subcategorías asociadas"
            }), 409

        # Eliminar categoría
        cursor.execute(
            "DELETE FROM categorias WHERE id_categoria = %s",
            (id_categoria,)
        )

        registrar_auditoria(
            cursor,
            datos_usuario.get("usuario_id"),
            "categorias",
            "ELIMINAR",
            f"Categoría {id_categoria}: {categoria['nombre']}"
        )

        conexion.commit()

        return jsonify({
            "mensaje": "Categoría eliminada correctamente"
        }), 200

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()

        return jsonify({
            "mensaje": "No fue posible eliminar la categoría"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()