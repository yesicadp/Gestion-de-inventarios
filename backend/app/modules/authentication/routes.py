import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from app.database.connection import obtener_conexion

load_dotenv()

authentication_bp = Blueprint("authentication", __name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


@authentication_bp.post("/api/auth/login")
def iniciar_sesion():
    data = request.get_json() or {}
    correo = (data.get("username") or "").strip().lower()
    password = data.get("password") or ""

    if not correo or not password:
        return jsonify({"mensaje": "Correo y contraseña son obligatorios"}), 400

    conexion = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT u.id_usuario, u.nombre, u.correo, u.password_hash,
                   u.estado, r.nombre_rol
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.id_rol
            WHERE u.correo = %s
            """,
            (correo,),
        )
        usuario = cursor.fetchone()
        cursor.close()

        # Mismo mensaje genérico si el correo no existe o la contraseña falla,
        # para no revelar cuál de los dos fue el error.
        credenciales_invalidas = jsonify({"mensaje": "Credenciales inválidas"}), 401

        if not usuario:
            return credenciales_invalidas

        if not usuario["estado"]:
            return jsonify({"mensaje": "El usuario está inactivo"}), 401

        password_valido = bcrypt.checkpw(
            password.encode("utf-8"),
            usuario["password_hash"].encode("utf-8"),
        )
        if not password_valido:
            return credenciales_invalidas

        datos_token = {
            "usuario_id": usuario["id_usuario"],
            "usuario": usuario["nombre"],
            "rol": usuario["nombre_rol"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        }
        token = jwt.encode(datos_token, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "token": token,
            "usuario": {
                "id": usuario["id_usuario"],
                "nombre": usuario["nombre"],
                "correo": usuario["correo"],
                "rol": usuario["nombre_rol"],
            },
        }), 200

    except Exception as error:
        # No exponemos el detalle del error de BD al cliente, solo lo dejamos
        # visible en consola del servidor para depurar en desarrollo.
        print(f"[auth/login] Error de base de datos: {error}")
        return jsonify({"mensaje": "No se pudo procesar el inicio de sesión"}), 500
    finally:
        if conexion is not None:
            conexion.close()