"""Apoyo para pruebas SIN MySQL: una base SQLite temporal con el mismo esquema de database/schema.sql.

Solo traduce %s -> ? y descarta FOR UPDATE. Sirve para probar la lógica de las rutas; el bloqueo de filas
(FOR UPDATE) y las transacciones concurrentes solo se pueden probar contra MySQL real.
"""
import sqlite3
import sys
import types

try:  # si mysql-connector está instalado se usa el real; si no, se simula solo lo que el código importa
    import mysql.connector  # noqa: F401
except ImportError:
    mysql = types.ModuleType("mysql")
    conector = types.ModuleType("mysql.connector")

    class IntegrityError(Exception):
        errno = 1062

    conector.IntegrityError = IntegrityError
    conector.connect = lambda **kw: (_ for _ in ()).throw(RuntimeError("sin MySQL en pruebas"))
    mysql.connector = conector
    sys.modules["mysql"] = mysql
    sys.modules["mysql.connector"] = conector

DDL = """
CREATE TABLE roles (id_rol INTEGER PRIMARY KEY AUTOINCREMENT, nombre_rol TEXT NOT NULL UNIQUE);
CREATE TABLE usuarios (id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, correo TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL, rol_id INTEGER NOT NULL REFERENCES roles(id_rol), estado INTEGER NOT NULL DEFAULT 1);
CREATE TABLE categorias (id_categoria INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL,
  categoria_padre_id INTEGER NULL REFERENCES categorias(id_categoria), UNIQUE (nombre, categoria_padre_id));
CREATE TABLE productos (id_producto INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, codigo TEXT NOT NULL UNIQUE,
  categoria_id INTEGER NOT NULL REFERENCES categorias(id_categoria), existencia_actual INTEGER NOT NULL DEFAULT 0,
  existencia_minima INTEGER NOT NULL DEFAULT 0, estado INTEGER NOT NULL DEFAULT 1,
  CHECK (existencia_actual >= 0), CHECK (existencia_minima >= 0));
CREATE TABLE movimientos (id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER NOT NULL REFERENCES productos(id_producto),
  usuario_id INTEGER NOT NULL REFERENCES usuarios(id_usuario), tipo_movimiento TEXT NOT NULL CHECK (tipo_movimiento IN ('ENTRADA','SALIDA')),
  cantidad INTEGER NOT NULL CHECK (cantidad > 0), motivo TEXT NOT NULL, fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  existencia_resultante INTEGER NOT NULL CHECK (existencia_resultante >= 0));
CREATE TABLE auditoria (id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT, usuario_id INTEGER NOT NULL REFERENCES usuarios(id_usuario),
  modulo TEXT NOT NULL, accion TEXT NOT NULL, fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, detalle TEXT);
INSERT INTO roles (nombre_rol) VALUES ('Administrador'), ('Usuario');
INSERT INTO usuarios (nombre, correo, password_hash, rol_id) VALUES
  ('Admin Demo', 'admin@x.com', 'x', 1), ('Usuario Demo', 'user@x.com', 'x', 2);
"""


class _Cursor:
    def __init__(self, con):
        self._c = con.cursor()

    def execute(self, sql, params=()):
        self._c.execute(sql.replace("%s", "?").replace("FOR UPDATE", ""), tuple(params))

    def fetchone(self):
        f = self._c.fetchone()
        return dict(f) if f else None

    def fetchall(self):
        return [dict(f) for f in self._c.fetchall()]

    @property
    def lastrowid(self):
        return self._c.lastrowid

    def close(self):
        self._c.close()


class _Conexion:
    def __init__(self, ruta):
        self._con = sqlite3.connect(ruta)
        self._con.row_factory = sqlite3.Row
        self._con.execute("PRAGMA foreign_keys = ON")
        self._abierta = True

    def cursor(self, dictionary=False):
        return _Cursor(self._con)

    def start_transaction(self):
        pass  # sqlite abre la transacción al primer INSERT/UPDATE

    def is_connected(self):
        return self._abierta

    def commit(self):
        self._con.commit()

    def rollback(self):
        self._con.rollback()

    def close(self):
        self._abierta = False
        self._con.close()


def crear_base(ruta):
    con = sqlite3.connect(ruta)
    con.executescript(DDL)
    con.commit()
    con.close()
    return lambda: _Conexion(ruta)
