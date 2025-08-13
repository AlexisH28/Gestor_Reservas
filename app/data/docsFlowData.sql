
-- SCRIPT DE DATOS DE PRUEBA (MOCK DATA)

USE coworking_db;

-- Limpiar datos existentes (en orden correcto debido a foreign keys)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE reservations;
TRUNCATE TABLE rooms;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

-- DATOS DE USUARIOS

-- Insertar usuarios de prueba
-- Nota: Las contraseñas están hasheadas usando bcrypt
-- Contraseña original para todos: "Password123!"

INSERT INTO users (nombre, email, contraseña_hash, rol, is_active, created_at) VALUES
-- Administradores
('Carlos Administrador', 'admin@coworking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'admin', TRUE, '2024-01-15 08:00:00'),
('María Gestora', 'maria.admin@coworking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'admin', TRUE, '2024-01-16 09:30:00'),

-- Usuarios regulares - Campus Norte
('Juan Pérez', 'juan.perez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-20 10:15:00'),
('Ana García', 'ana.garcia@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-21 11:45:00'),
('Luis Martínez', 'luis.martinez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-22 14:20:00'),
('Carmen López', 'carmen.lopez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-23 16:30:00'),

-- Usuarios regulares - Campus Sur
('Roberto Silva', 'roberto.silva@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-24 09:00:00'),
('Patricia Morales', 'patricia.morales@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-25 12:10:00'),
('Diego Ramírez', 'diego.ramirez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-26 13:45:00'),
('Sofía Herrera', 'sofia.herrera@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-27 15:30:00'),

-- Usuarios del Campus Centro
('Fernando Castro', 'fernando.castro@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-28 10:20:00'),
('Alejandra Vega', 'alejandra.vega@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-29 11:15:00'),
('Miguel Ortega', 'miguel.ortega@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', TRUE, '2024-01-30 14:40:00'),

-- Usuarios inactivos (para pruebas)
('Usuario Inactivo', 'inactivo@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', FALSE, '2024-01-31 16:00:00'),
('Test Deshabilitado', 'test.disabled@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdPKO4jlU5o3GVm', 'user', FALSE, '2024-02-01 08:30:00');
}
-- DATOS DE SALAS

INSERT INTO rooms (nombre, sede, capacidad, recursos, is_active, created_at) VALUES

-- Campus Norte
('Sala Reuniones A', 'Campus Norte', 8, 
    '{"proyector": true, "wifi": true, "pizarra": true, "aire_acondicionado": true, "video_conferencia": true}', 
    TRUE, '2024-01-10 09:00:00'),

('Sala Reuniones B', 'Campus Norte', 12, 
    '{"proyector": true, "wifi": true, "pizarra": false, "aire_acondicionado": true, "video_conferencia": false, "tv": true}', 
    TRUE, '2024-01-10 09:30:00'),

('Aula Magna Norte', 'Campus Norte', 50, 
    '{"proyector": true, "wifi": true, "pizarra": true, "aire_acondicionado": true, "video_conferencia": true, "sonido": true}', 
    TRUE, '2024-01-10 10:00:00'),

('Sala Trabajo Colaborativo', 'Campus Norte', 6, 
    '{"wifi": true, "pizarra": true, "aire_acondicionado": false}', 
    TRUE, '2024-01-10 10:30:00'),

-- Campus Sur
('Sala Ejecutiva', 'Campus Sur', 4, 
    '{"proyector": true, "wifi": true, "aire_acondicionado": true, "video_conferencia": true}', 
    TRUE, '2024-01-11 08:00:00'),

('Sala Capacitaciones', 'Campus Sur', 20, 
    '{"proyector": true, "wifi": true, "pizarra": true, "aire_acondicionado": true, "computador": true}', 
    TRUE, '2024-01-11 08:30:00'),

('Sala Creativa', 'Campus Sur', 10, 
    '{"wifi": true, "pizarra": true, "aire_acondicionado": true}', 
    TRUE, '2024-01-11 09:00:00'),

('Auditorio Sur', 'Campus Sur', 80, 
    '{"proyector": true, "wifi": true, "aire_acondicionado": true, "video_conferencia": true, "sonido": true, "tv": true}', 
    TRUE, '2024-01-11 09:30:00'),

-- Campus Centro
('Sala Boardroom', 'Campus Centro', 6, 
    '{"proyector": false, "wifi": true, "aire_acondicionado": true, "video_conferencia": true, "tv": true}', 
    TRUE, '2024-01-12 10:00:00'),

('Sala Innovación', 'Campus Centro', 15, 
    '{"proyector": true, "wifi": true, "pizarra": true, "aire_acondicionado": true}', 
    TRUE, '2024-01-12 10:30:00'),

('Sala Focus', 'Campus Centro', 4, 
    '{"wifi": true, "aire_acondicionado": true}', 
    TRUE, '2024-01-12 11:00:00'),

('Centro de Conferencias', 'Campus Centro', 100, 
    '{"proyector": true, "wifi": true, "aire_acondicionado": true, "video_conferencia": true, "sonido": true, "tv": true, "computador": true}', 
    TRUE, '2024-01-12 11:30:00'),

-- Salas deshabilitadas (para pruebas)
('Sala Mantenimiento', 'Campus Norte', 8, 
    '{"wifi": true}', 
    FALSE, '2024-01-13 12:00:00'),

('Sala Renovación', 'Campus Sur', 12, 
    '{"proyector": true, "wifi": true}', 
    FALSE, '2024-01-13 12:30:00');


-- DATOS DE RESERVAS

-- Reservas pasadas (para estadísticas)
INSERT INTO reservations (usuario_id, sala_id, fecha, hora_inicio, hora_fin, estado, created_at) VALUES
-- Enero 2024 - Reservas pasadas
(3, 1, '2024-01-25', '09:00:00', '10:00:00', 'confirmada', '2024-01-20 08:30:00'),
(4, 2, '2024-01-25', '10:00:00', '11:00:00', 'confirmada', '2024-01-20 09:15:00'),
(5, 1, '2024-01-25', '14:00:00', '15:00:00', 'confirmada', '2024-01-20 10:45:00'),
(3, 3, '2024-01-26', '11:00:00', '12:00:00', 'confirmada', '2024-01-21 14:20:00'),
(6, 5, '2024-01-26', '13:00:00', '14:00:00', 'confirmada', '2024-01-21 15:30:00'),
(7, 6, '2024-01-26', '15:00:00', '16:00:00', 'cancelada', '2024-01-21 16:10:00'),

-- Febrero 2024 - Más reservas pasadas
(8, 7, '2024-02-01', '09:00:00', '10:00:00', 'confirmada', '2024-01-28 10:00:00'),
(9, 8, '2024-02-01', '11:00:00', '12:00:00', 'confirmada', '2024-01-28 11:15:00'),
(10, 9, '2024-02-02', '10:00:00', '11:00:00', 'confirmada', '2024-01-29 09:30:00'),
(11, 10, '2024-02-02', '14:00:00', '15:00:00', 'confirmada', '2024-01-29 12:45:00'),
(12, 11, '2024-02-03', '09:00:00', '10:00:00', 'cancelada', '2024-01-30 08:20:00'),
(13, 12, '2024-02-03', '16:00:00', '17:00:00', 'confirmada', '2024-01-30 14:10:00'),

-- Marzo 2024
(3, 1, '2024-03-05', '10:00:00', '11:00:00', 'confirmada', '2024-03-01 09:00:00'),
(4, 2, '2024-03-05', '13:00:00', '14:00:00', 'confirmada', '2024-03-01 10:30:00'),
(5, 5, '2024-03-06', '11:00:00', '12:00:00', 'confirmada', '2024-03-02 08:45:00'),
(6, 6, '2024-03-06', '15:00:00', '16:00:00', 'confirmada', '2024-03-02 11:20:00');

-- Reservas futuras (desde agosto 2024 en adelante)
INSERT INTO reservations (usuario_id, sala_id, fecha, hora_inicio, hora_fin, estado, created_at) VALUES

-- Agosto 2024 - Reservas actuales y futuras
(3, 1, '2024-08-13', '09:00:00', '10:00:00', 'confirmada', '2024-08-10 08:30:00'),
(4, 1, '2024-08-13', '10:00:00', '11:00:00', 'confirmada', '2024-08-10 09:15:00'),
(5, 1, '2024-08-13', '14:00:00', '15:00:00', 'confirmada', '2024-08-10 10:00:00'),
(6, 2, '2024-08-13', '11:00:00', '12:00:00', 'confirmada', '2024-08-10 11:30:00'),
(7, 2, '2024-08-13', '15:00:00', '16:00:00', 'confirmada', '2024-08-10 12:15:00'),

-- 14 de Agosto
(8, 3, '2024-08-14', '08:00:00', '09:00:00', 'confirmada', '2024-08-11 09:00:00'),
(9, 5, '2024-08-14', '09:00:00', '10:00:00', 'confirmada', '2024-08-11 10:20:00'),
(10, 6, '2024-08-14', '13:00:00', '14:00:00', 'confirmada', '2024-08-11 11:45:00'),
(11, 7, '2024-08-14', '14:00:00', '15:00:00', 'confirmada', '2024-08-11 13:30:00'),
(12, 9, '2024-08-14', '16:00:00', '17:00:00', 'confirmada', '2024-08-11 14:15:00'),

-- 15 de Agosto (hoy)
(3, 4, '2024-08-15', '10:00:00', '11:00:00', 'confirmada', '2024-08-12 08:45:00'),
(13, 8, '2024-08-15', '11:00:00', '12:00:00', 'confirmada', '2024-08-12 09:30:00'),
(4, 10, '2024-08-15', '13:00:00', '14:00:00', 'confirmada', '2024-08-12 10:20:00'),
(5, 11, '2024-08-15', '15:00:00', '16:00:00', 'confirmada', '2024-08-12 11:10:00'),

-- 16 de Agosto (mañana)
(6, 1, '2024-08-16', '08:00:00', '09:00:00', 'confirmada', '2024-08-12 12:00:00'),
(7, 2, '2024-08-16', '09:00:00', '10:00:00', 'confirmada', '2024-08-12 13:15:00'),
(8, 1, '2024-08-16', '11:00:00', '12:00:00', 'confirmada', '2024-08-12 14:30:00'),
(9, 5, '2024-08-16', '14:00:00', '15:00:00', 'confirmada', '2024-08-12 15:45:00'),
(10, 6, '2024-08-16', '16:00:00', '17:00:00', 'pendiente', '2024-08-12 16:20:00'),

-- Próxima semana (19-23 Agosto)
(11, 3, '2024-08-19', '10:00:00', '11:00:00', 'confirmada', '2024-08-12 17:00:00'),
(12, 8, '2024-08-19', '14:00:00', '15:00:00', 'confirmada', '2024-08-12 17:30:00'),
(13, 12, '2024-08-20', '09:00:00', '10:00:00', 'confirmada', '2024-08-12 18:00:00'),
(3, 7, '2024-08-20', '13:00:00', '14:00:00', 'confirmada', '2024-08-12 18:15:00'),
(4, 9, '2024-08-21', '11:00:00', '12:00:00', 'confirmada', '2024-08-12 18:30:00'),

-- Reservas con cancelaciones recientes
(5, 4, '2024-08-22', '10:00:00', '11:00:00', 'cancelada', '2024-08-12 19:00:00'),
(6, 10, '2024-08-22', '15:00:00', '16:00:00', 'cancelada', '2024-08-12 19:15:00'),

-- Septiembre - Reservas más distantes
(7, 1, '2024-09-02', '09:00:00', '10:00:00', 'confirmada', '2024-08-12 20:00:00')