"""Conexión a la base de datos MySQL.

Lee la configuración desde variables de entorno (ver .env.example en la raíz):
DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD.
"""
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    """Abre y devuelve una nueva conexión a MySQL. Quien la use debe cerrarla."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "gestion_inventarios"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
    )