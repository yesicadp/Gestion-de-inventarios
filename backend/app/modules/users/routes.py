
import bcrypt
import mysql.connector
import re

from flask import Blueprint, jsonify, request

from app.database.connection import obtener_conexion
from app.shared.security.permisos import requiere_admin
from app.shared.utilities.auditoria import registrar_auditoria
from mysql.connector.errors import IntegrityError


users_bp = Blueprint("users", __name__)


@users_bp.get("/api/usuarios")
@requiere_admin
def consultar_usuarios(datos_usuario):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                u.id_usuario,
                u.nombre,
                u.correo,
                u.rol_id,
                r.nombre_rol,
                u.estado
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id_rol
            ORDER BY u.id_usuario DESC
        """)

        usuarios = cursor.fetchall()

        return jsonify({
            "mensaje": "Usuarios consultados correctamente",
            "usuarios": usuarios
        }), 200

    except Exception as error:
        print(f"Error al consultar usuarios: {error}")
        return jsonify({
            "mensaje": "No fue posible consultar los usuarios"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()


@users_bp.post("/api/usuarios")
@requiere_admin
def crear_usuario(datos_usuario):
    datos = request.get_json() or {}

    nombre = (datos.get("nombre") or "").strip()
    correo = (datos.get("correo") or "").strip().lower()
    password = datos.get("password") or ""
    rol_id = datos.get("rol_id")

    if not nombre or not correo or not password or rol_id is None:
        return jsonify({
            "mensaje": "Todos los campos son obligatorios"
        }), 400

    if len(nombre) > 100:
        return jsonify({
            "mensaje": "El nombre no puede superar los 100 caracteres"
        }), 400

    if len(correo) > 150 or "@" not in correo:
        return jsonify({
            "mensaje": "El correo electrónico no es válido"
        }), 400

    if len(password) < 8:
        return jsonify({
            "mensaje": "La contraseña debe tener mínimo 8 caracteres"
        }), 400

    try:
        rol_id = int(rol_id)
    except (ValueError, TypeError):
        return jsonify({
            "mensaje": "El rol seleccionado no es válido"
        }), 400

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_rol, nombre_rol
            FROM roles
            WHERE id_rol = %s
        """, (rol_id,))

        rol = cursor.fetchone()

        if rol is None:
            return jsonify({
                "mensaje": "El rol seleccionado no existe"
            }), 400

        if rol["nombre_rol"] not in ("Administrador", "Usuario"):
            return jsonify({
                "mensaje": "El rol seleccionado no está permitido"
            }), 400

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, password_hash, rol_id)
            VALUES (%s, %s, %s, %s)
        """, (nombre, correo, password_hash, rol_id))

        id_usuario = cursor.lastrowid

        registrar_auditoria(
            cursor,
            datos_usuario.get("usuario_id"),
            "usuarios",
            "CREAR",
            f"Usuario {id_usuario}: {nombre} ({correo}), rol: {rol['nombre_rol']}"
        )

        conexion.commit()

        return jsonify({
            "mensaje": "Usuario creado correctamente",
            "usuario": {
                "id_usuario": id_usuario,
                "nombre": nombre,
                "correo": correo,
                "rol_id": rol_id,
                "nombre_rol": rol["nombre_rol"],
                "estado": True
            }
        }), 201

    except IntegrityError as error:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()

        if error.errno == 1062:
            return jsonify({
                "mensaje": "Ya existe un usuario registrado con ese correo"
            }), 409

        print(f"Error de integridad al crear usuario: {error}")
        return jsonify({
            "mensaje": "No fue posible crear el usuario"
        }), 500

    except Exception as error:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()

        print(f"Error al crear usuario: {error}")
        return jsonify({
            "mensaje": "No fue posible crear el usuario"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()


@users_bp.put("/api/usuarios/<int:id_usuario>")
@requiere_admin
def editar_usuario(datos_usuario, id_usuario):
    datos = request.get_json() or {}

    nombre = (datos.get("nombre") or "").strip()
    correo = (datos.get("correo") or "").strip().lower()
    rol_id = datos.get("rol_id")
    password = datos.get("password") or ""

    if not nombre or not correo or rol_id is None:
        return jsonify({
            "mensaje": "Nombre, correo y rol son obligatorios"
        }), 400

    if len(nombre) > 100:
        return jsonify({
            "mensaje": "El nombre no puede superar los 100 caracteres"
        }), 400

    if len(correo) > 150 or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
        return jsonify({
            "mensaje": "El correo electrónico no es válido"
        }), 400

    if password and len(password) < 8:
        return jsonify({
            "mensaje": "La contraseña debe tener al menos 8 caracteres"
        }), 400

    if isinstance(rol_id, bool) or not str(rol_id).isdigit():
        return jsonify({
            "mensaje": "El rol seleccionado no es válido"
        }), 400

    rol_id = int(rol_id)

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_usuario, nombre, correo, rol_id, estado
            FROM usuarios
            WHERE id_usuario = %s
            FOR UPDATE
        """, (id_usuario,))

        usuario = cursor.fetchone()

        if usuario is None:
            return jsonify({
                "mensaje": "El usuario no existe"
            }), 404

        cursor.execute("""
            SELECT id_rol, nombre_rol
            FROM roles
            WHERE id_rol = %s
        """, (rol_id,))

        rol = cursor.fetchone()

        if rol is None or rol["nombre_rol"] not in ("Administrador", "Usuario"):
            return jsonify({
                "mensaje": "El rol seleccionado no está permitido"
            }), 400

        # Evitar dejar el sistema sin administradores activos.
        if (
            usuario["estado"]
            and usuario["rol_id"] != rol_id
            and rol["nombre_rol"] != "Administrador"
        ):
            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM usuarios u
                INNER JOIN roles r ON u.rol_id = r.id_rol
                WHERE r.nombre_rol = 'Administrador'
                AND u.estado = TRUE
            """)

            total_admins = cursor.fetchone()["total"]

            if total_admins <= 1:
                return jsonify({
                    "mensaje": "No puedes quitar el rol al último administrador activo"
                }), 409

        if password:
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            cursor.execute("""
                UPDATE usuarios
                SET nombre = %s,
                    correo = %s,
                    rol_id = %s,
                    password_hash = %s
                WHERE id_usuario = %s
            """, (nombre, correo, rol_id, password_hash, id_usuario))
        else:
            cursor.execute("""
                UPDATE usuarios
                SET nombre = %s,
                    correo = %s,
                    rol_id = %s
                WHERE id_usuario = %s
            """, (nombre, correo, rol_id, id_usuario))

        registrar_auditoria(
            cursor,
            datos_usuario.get("usuario_id"),
            "usuarios",
            "EDITAR",
            f"Usuario {id_usuario}: datos actualizados. Rol: {rol['nombre_rol']}"
        )

        conexion.commit()

        return jsonify({
            "mensaje": "Usuario actualizado correctamente"
        }), 200

    except IntegrityError as error:
        if conexion is not None:
            conexion.rollback()

        if error.errno == 1062:
            return jsonify({
                "mensaje": "Ya existe un usuario con ese correo"
            }), 409

        print(f"Error de integridad al editar usuario: {error}")
        return jsonify({
            "mensaje": "No fue posible actualizar el usuario"
        }), 500

    except Exception as error:
        if conexion is not None:
            conexion.rollback()

        print(f"Error al editar usuario: {error}")
        return jsonify({
            "mensaje": "No fue posible actualizar el usuario"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()


@users_bp.patch("/api/usuarios/<int:id_usuario>/estado")
@requiere_admin
def cambiar_estado_usuario(datos_usuario, id_usuario):
    datos = request.get_json() or {}
    nuevo_estado = datos.get("estado")

    if not isinstance(nuevo_estado, bool):
        return jsonify({
            "mensaje": "El estado debe ser verdadero o falso"
        }), 400

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT u.id_usuario, u.nombre, u.estado,
                   u.rol_id, r.nombre_rol
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id_rol
            WHERE u.id_usuario = %s
            FOR UPDATE
        """, (id_usuario,))

        usuario = cursor.fetchone()

        if usuario is None:
            return jsonify({
                "mensaje": "El usuario no existe"
            }), 404

        if usuario["estado"] == nuevo_estado:
            return jsonify({
                "mensaje": "El usuario ya tiene ese estado"
            }), 400

        if not nuevo_estado:
            if usuario["id_usuario"] == datos_usuario.get("usuario_id"):
                return jsonify({
                    "mensaje": "No puedes desactivar tu propia cuenta"
                }), 409

            if usuario["nombre_rol"] == "Administrador":
                cursor.execute("""
                    SELECT COUNT(*) AS total
                    FROM usuarios u
                    INNER JOIN roles r ON u.rol_id = r.id_rol
                    WHERE r.nombre_rol = 'Administrador'
                    AND u.estado = TRUE
                """)

                total_admins = cursor.fetchone()["total"]

                if total_admins <= 1:
                    return jsonify({
                        "mensaje": "No puedes desactivar al último administrador activo"
                    }), 409

        cursor.execute("""
            UPDATE usuarios
            SET estado = %s
            WHERE id_usuario = %s
        """, (nuevo_estado, id_usuario))

        accion = "ACTIVAR" if nuevo_estado else "DESACTIVAR"

        registrar_auditoria(
            cursor,
            datos_usuario.get("usuario_id"),
            "usuarios",
            accion,
            f"Usuario {id_usuario}: {usuario['nombre']}"
        )

        conexion.commit()

        return jsonify({
            "mensaje": "Usuario activado correctamente"
            if nuevo_estado else "Usuario desactivado correctamente"
        }), 200

    except Exception as error:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()

        print(f"Error al cambiar estado del usuario: {error}")

        return jsonify({
            "mensaje": "No fue posible cambiar el estado del usuario"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()
