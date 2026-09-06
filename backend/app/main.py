import jwt

from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def requiere_token(funcion):
    @wraps(funcion)
    def decorador(*args, **kwargs):
        encabezado = request.headers.get("Authorization")

        if not encabezado:
            return jsonify({
                "mensaje": "Falta el encabezado Authorization"
            }), 401

        partes = encabezado.split()

        if len(partes) != 2 or partes[0] != "Bearer":
            return jsonify({
                "mensaje": "Formato de token inválido"
            }), 401

        token = partes[1]

        try:
            datos_usuario = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({
                "mensaje": "El token ha expirado"
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "mensaje": "El token no es válido"
            }), 401

        return funcion(datos_usuario, *args, **kwargs)

    return decorador

@app.get("/")
def inicio():
    return jsonify({"mensaje": "API de inventarios funcionando"}), 200

@app.get("/api/health")
def estado():
    return jsonify({
        "status": "ok",
        "mensaje": "La API esta disponible"
    }), 200

@app.post("/api/auth/login")
def iniciar_sesion():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Aquí puedes agregar la lógica de autenticación, por ejemplo, verificar el usuario y la contraseña en una base de datos.
    if username == "admin" and password == "password":
        datos_token = {
        "usuario": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

        token = jwt.encode(
        datos_token,
        SECRET_KEY,
        algorithm="HS256"
    )
        return jsonify({"mensaje": "Inicio de sesión exitoso", "token": token}), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

@app.get("/api/perfil")
@requiere_token
def perfil(datos_usuario):
    return jsonify({
        "mensaje": "Acceso autorizado",
        "usuario": datos_usuario["usuario"]
    }), 200

if __name__ == "__main__":
    app.run(debug=True)