-- Usuarios de prueba para poder probar el login real hoy mismo.
-- Contraseñas en texto plano (SOLO para que el equipo las use al probar):
--   admin@inventario.com    / Admin123!
--   usuario@inventario.com  / Usuario123!
-- El hash ya está generado con bcrypt, así es como se guardaría siempre
-- (nunca se guarda la contraseña en texto plano en la base de datos).

USE gestion_inventarios;

INSERT INTO usuarios (nombre, correo, password_hash, rol_id, estado)
VALUES
    ('Admin Demo', 'admin@inventario.com',
     '$2b$12$IFEhBuu1lzXvJtv4XakgyO7euRpSDYUzLm1NhAc3PNSgzRoKzejuq',
     (SELECT id_rol FROM roles WHERE nombre_rol = 'Administrador'), TRUE),
    ('Usuario Demo', 'usuario@inventario.com',
     '$2b$12$a2Zw1Fo.T.eKp0Z60qsVCemAkH1N5CaV8h3Gd7AoTbkZ2F8fctY0S',
     (SELECT id_rol FROM roles WHERE nombre_rol = 'Usuario'), TRUE);