from flask import Blueprint, jsonify, request

from app.database.connection import obtener_conexion
from app.modules.authentication.decorators import requiere_token

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
            ORDER BY nombre
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
@requiere_token
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

        conexion.commit()
        nuevo_id = cursor.lastrowid

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

