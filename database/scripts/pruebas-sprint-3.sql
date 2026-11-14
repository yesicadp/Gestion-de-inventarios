USE gestion_inventarios;

-- PRUEBA SPRINT 3: ENTRADAS Y SALIDAS
-- Se utiliza una transacción para revertir todos los cambios.

SET @producto_id = (
    SELECT id_producto
    FROM productos
    WHERE codigo = 'DEMO-001'
);

SET @usuario_id = (
    SELECT id_usuario
    FROM usuarios
    WHERE correo = 'admin@inventario.com'
);

-- Consultar stock inicial
SELECT codigo, nombre, existencia_actual
FROM productos
WHERE id_producto = @producto_id;

START TRANSACTION;

-- Registrar entrada de 5 unidades
UPDATE productos
SET existencia_actual = existencia_actual + 5
WHERE id_producto = @producto_id;

INSERT INTO movimientos (
    producto_id, usuario_id, tipo_movimiento,
    cantidad, motivo, existencia_resultante
)
SELECT
    @producto_id, @usuario_id, 'ENTRADA',
    5, 'Prueba de entrada Sprint 3', existencia_actual
FROM productos
WHERE id_producto = @producto_id;

-- Registrar salida de 3 unidades
UPDATE productos
SET existencia_actual = existencia_actual - 3
WHERE id_producto = @producto_id
AND existencia_actual >= 3;

INSERT INTO movimientos (
    producto_id, usuario_id, tipo_movimiento,
    cantidad, motivo, existencia_resultante
)
SELECT
    @producto_id, @usuario_id, 'SALIDA',
    3, 'Prueba de salida Sprint 3', existencia_actual
FROM productos
WHERE id_producto = @producto_id;

-- Verificar movimientos y stock resultante
SELECT *
FROM movimientos
WHERE producto_id = @producto_id
ORDER BY id_movimiento DESC;

SELECT codigo, existencia_actual
FROM productos
WHERE id_producto = @producto_id;

-- Revertir las pruebas
ROLLBACK;

-- Confirmar que el stock original se conserva
SELECT codigo, existencia_actual
FROM productos
WHERE id_producto = @producto_id;