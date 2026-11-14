CREATE DATABASE IF NOT EXISTS gestion_inventarios
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE gestion_inventarios;

-- =========================================
-- TABLA: roles
-- =========================================

CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL,

    CONSTRAINT uq_roles_nombre_rol
        UNIQUE (nombre_rol)
) ENGINE=InnoDB;

-- =========================================
-- TABLA: usuarios
-- =========================================

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_usuarios_correo
        UNIQUE (correo),

    INDEX idx_usuarios_rol_id (rol_id),

    CONSTRAINT fk_usuarios_rol
        FOREIGN KEY (rol_id)
        REFERENCES roles(id_rol)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =========================================
-- TABLA: categorias
-- =========================================

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria_padre_id INT NULL,

    CONSTRAINT uq_categorias_nombre_padre
        UNIQUE (nombre, categoria_padre_id),

    INDEX idx_categorias_padre_id (categoria_padre_id),

    CONSTRAINT fk_categorias_padre
        FOREIGN KEY (categoria_padre_id)
        REFERENCES categorias(id_categoria)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =========================================
-- TABLA: productos
-- =========================================

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    codigo VARCHAR(50) NOT NULL,
    categoria_id INT NOT NULL,
    existencia_actual INT NOT NULL DEFAULT 0,
    existencia_minima INT NOT NULL DEFAULT 0,
    estado BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_productos_codigo
        UNIQUE (codigo),

    INDEX idx_productos_estado (estado),
    INDEX idx_productos_categoria_estado (categoria_id, estado),

    CONSTRAINT fk_productos_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categorias(id_categoria)
        ON DELETE RESTRICT,

    CONSTRAINT chk_productos_existencia_actual
        CHECK (existencia_actual >= 0),

    CONSTRAINT chk_productos_existencia_minima
        CHECK (existencia_minima >= 0)
) ENGINE=InnoDB;

-- =========================================
-- TABLA: movimientos
-- =========================================

CREATE TABLE movimientos (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    usuario_id INT NOT NULL,
    tipo_movimiento ENUM('ENTRADA', 'SALIDA') NOT NULL,
    cantidad INT NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    existencia_resultante INT NOT NULL,

    INDEX idx_movimientos_usuario_id (usuario_id),
    INDEX idx_movimientos_fecha (fecha),
    INDEX idx_movimientos_producto_fecha (producto_id, fecha),

    CONSTRAINT fk_movimientos_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id_producto)
        ON DELETE RESTRICT,

    CONSTRAINT fk_movimientos_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id_usuario)
        ON DELETE RESTRICT,

    CONSTRAINT chk_movimientos_cantidad
        CHECK (cantidad > 0),

    CONSTRAINT chk_movimientos_existencia_resultante
        CHECK (existencia_resultante >= 0)
) ENGINE=InnoDB;

-- =========================================
-- TABLA: auditoria
-- =========================================

CREATE TABLE auditoria (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    accion VARCHAR(50) NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    detalle VARCHAR(255) NULL,

    INDEX idx_auditoria_modulo (modulo),
    INDEX idx_auditoria_fecha (fecha),
    INDEX idx_auditoria_usuario_modulo_fecha
        (usuario_id, modulo, fecha),

    CONSTRAINT fk_auditoria_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id_usuario)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =========================================
-- DATOS INICIALES: ROLES
-- =========================================

INSERT INTO roles (nombre_rol)
VALUES
    ('Administrador'),
    ('Usuario');