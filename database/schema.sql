CREATE DATABASE IF NOT EXISTS gestion_inventarios
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE gestion_inventarios;

CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (rol_id)
        REFERENCES roles(id_rol)
        ON DELETE RESTRICT
);

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria_padre_id INT NULL,

    FOREIGN KEY (categoria_padre_id)
        REFERENCES categorias(id_categoria)
        ON DELETE RESTRICT,

    UNIQUE (nombre, categoria_padre_id)
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    categoria_id INT NOT NULL,
    existencia_actual INT NOT NULL DEFAULT 0,
    existencia_minima INT NOT NULL DEFAULT 0,
    estado BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (categoria_id)
        REFERENCES categorias(id_categoria)
        ON DELETE RESTRICT,

    CHECK (existencia_actual >= 0),
    CHECK (existencia_minima >= 0)
);

CREATE TABLE movimientos (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    usuario_id INT NOT NULL,
    tipo_movimiento ENUM('ENTRADA', 'SALIDA') NOT NULL,
    cantidad INT NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    existencia_resultante INT NOT NULL,

    FOREIGN KEY (producto_id)
        REFERENCES productos(id_producto)
        ON DELETE RESTRICT,

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id_usuario)
        ON DELETE RESTRICT,

    CHECK (cantidad > 0),
    CHECK (existencia_resultante >= 0)
);

CREATE TABLE auditoria (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    accion VARCHAR(50) NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    detalle VARCHAR(255),

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id_usuario)
        ON DELETE RESTRICT
);


-- INDICES ADICIONALES

CREATE INDEX idx_usuarios_rol_id
ON usuarios (rol_id);

CREATE INDEX idx_categorias_padre_id
ON categorias (categoria_padre_id);

CREATE INDEX idx_productos_estado
ON productos (estado);

CREATE INDEX idx_productos_categoria_estado
ON productos (categoria_id, estado);

CREATE INDEX idx_movimientos_usuario_id
ON movimientos (usuario_id);

CREATE INDEX idx_movimientos_fecha
ON movimientos (fecha);

CREATE INDEX idx_movimientos_producto_fecha
ON movimientos (producto_id, fecha);

CREATE INDEX idx_auditoria_modulo
ON auditoria (modulo);

CREATE INDEX idx_auditoria_fecha
ON auditoria (fecha);

CREATE INDEX idx_auditoria_usuario_modulo_fecha
ON auditoria (usuario_id, modulo, fecha);


INSERT INTO roles (nombre_rol)
VALUES
    ('Administrador'),
    ('Usuario');
