-- SCRIPT DE CREACIÓN DE ESTRUCTURA DE BASE DE DATOS

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS coworking_db;
USE coworking_db;

-- Configurar charset y collation
ALTER DATABASE coworking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- TABLA: USUARIOS

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    contraseña_hash VARCHAR(255) NOT NULL,
    rol ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_users_email (email),
    INDEX idx_users_nombre (nombre),
    INDEX idx_users_rol (rol),
    INDEX idx_users_active (is_active),
    INDEX idx_users_created (created_at)
);


-- TABLA: SALAS

DROP TABLE IF EXISTS rooms;

CREATE TABLE rooms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    sede VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL CHECK (capacidad > 0),
    recursos JSON NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_rooms_nombre (nombre),
    INDEX idx_rooms_sede (sede),
    INDEX idx_rooms_capacidad (capacidad),
    INDEX idx_rooms_active (is_active),
    INDEX idx_rooms_sede_nombre (sede, nombre),
    
    -- Constraint único para nombre-sede
    UNIQUE KEY uk_rooms_nombre_sede (nombre, sede)
);


-- TABLA: RESERVAS

DROP TABLE IF EXISTS reservations;

CREATE TABLE reservations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    sala_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado ENUM('pendiente', 'confirmada', 'cancelada') NOT NULL DEFAULT 'confirmada',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    
    -- Llaves foráneas
    CONSTRAINT fk_reservations_usuario 
        FOREIGN KEY (usuario_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_reservations_sala 
        FOREIGN KEY (sala_id) REFERENCES rooms(id) ON DELETE CASCADE,
    
    -- Índices
    INDEX idx_reservations_usuario (usuario_id),
    INDEX idx_reservations_sala (sala_id),
    INDEX idx_reservations_fecha (fecha),
    INDEX idx_reservations_estado (estado),
    INDEX idx_reservations_fecha_hora (fecha, hora_inicio),
    INDEX idx_reservations_sala_fecha (sala_id, fecha),
    
    -- Constraint único para evitar solapamiento de reservas
    UNIQUE KEY uk_reservations_sala_fecha_hora (sala_id, fecha, hora_inicio),
    
    -- Constraints de validación
    CONSTRAINT chk_reservations_horario 
        CHECK (hora_fin > hora_inicio),
    CONSTRAINT chk_reservations_fecha_actual 
        CHECK (fecha >= CURDATE())
);

-- PROCEDIMIENTOS ALMACENADOS

-- Procedimiento para obtener disponibilidad de una sala en una fecha
DELIMITER //

CREATE PROCEDURE GetRoomAvailability(
    IN p_sala_id INT,
    IN p_fecha DATE
)
BEGIN
    -- Mostrar slots ocupados
    SELECT 
        TIME_FORMAT(hora_inicio, '%H:%i') as hora_inicio,
        TIME_FORMAT(hora_fin, '%H:%i') as hora_fin,
        estado
    FROM reservations 
    WHERE sala_id = p_sala_id 
        AND fecha = p_fecha 
        AND estado IN ('confirmada', 'pendiente')
    ORDER BY hora_inicio;
END //

-- Procedimiento para validar si un horario está disponible
CREATE PROCEDURE ValidateTimeSlot(
    IN p_sala_id INT,
    IN p_fecha DATE,
    IN p_hora_inicio TIME,
    IN p_hora_fin TIME,
    OUT p_available BOOLEAN
)
BEGIN
    DECLARE slot_count INT DEFAULT 0;
    
    SELECT COUNT(*) INTO slot_count
    FROM reservations 
    WHERE sala_id = p_sala_id 
        AND fecha = p_fecha 
        AND estado IN ('confirmada', 'pendiente')
        AND (
            (hora_inicio < p_hora_fin AND hora_fin > p_hora_inicio)
        );
    
    SET p_available = (slot_count = 0);
END //

-- Procedimiento para obtener estadísticas del sistema
CREATE PROCEDURE GetSystemStats()
BEGIN
    SELECT 
        (SELECT COUNT(*) FROM users WHERE is_active = 1) as usuarios_activos,
        (SELECT COUNT(*) FROM users WHERE is_active = 0) as usuarios_inactivos,
        (SELECT COUNT(*) FROM rooms WHERE is_active = 1) as salas_activas,
        (SELECT COUNT(*) FROM rooms WHERE is_active = 0) as salas_inactivas,
        (SELECT COUNT(*) FROM reservations WHERE fecha >= CURDATE()) as reservas_futuras,
        (SELECT COUNT(*) FROM reservations WHERE fecha < CURDATE()) as reservas_pasadas,
        (SELECT COUNT(*) FROM reservations WHERE estado = 'cancelada') as reservas_canceladas;
END //

DELIMITER ;


-- TRIGGERS

-- Trigger para actualizar updated_at en users
DELIMITER //

CREATE TRIGGER tr_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END //

-- Trigger para actualizar updated_at en rooms
CREATE TRIGGER tr_rooms_updated_at
    BEFORE UPDATE ON rooms
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END //

-- Trigger para actualizar updated_at en reservations
CREATE TRIGGER tr_reservations_updated_at
    BEFORE UPDATE ON reservations
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END //

DELIMITER ;

-- ===================================================================
-- CONFIGURACIÓN DE PERMISOS (opcional)
-- ===================================================================

-- Crear usuario específico para la aplicación (opcional)
-- CREATE USER 'coworking_app'@'localhost' IDENTIFIED BY 'tu_password_segura';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON coworking_db.* TO 'coworking_app'@'localhost';
-- FLUSH PRIVILEGES;

-- ===================================================================
-- VERIFICACIÓN DE ESTRUCTURA
-- ===================================================================

-- Mostrar estructura creada
SHOW TABLES;

-- Verificar constraints
SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS 
WHERE TABLE_SCHEMA = 'coworking_db'
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;

SHOW CREATE TABLE users;
SHOW CREATE TABLE rooms;
SHOW CREATE TABLE reservations;

-- ===================================================================
-- FIN DEL SCRIPT
-- ===================================================================

SELECT 'Base de datos creada exitosamente!' as mensaje;