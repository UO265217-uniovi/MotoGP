-- BORRADO DE BASE DE DATOS PREVIA (Para reiniciar limpio)
DROP DATABASE IF EXISTS UO265217_DB;
CREATE DATABASE UO265217_DB;
USE UO265217_DB;

-- 1. TABLA DISPOSITIVOS (Catálogo fijo: PC, Tablet, Móvil)
CREATE TABLE dispositivos (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_dispositivo VARCHAR(50) NOT NULL
);

-- 2. TABLA PREGUNTAS (Para cargar el test dinámicamente)
CREATE TABLE preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enunciado TEXT NOT NULL,
    respuesta_a VARCHAR(255) NOT NULL,
    respuesta_b VARCHAR(255) NOT NULL,
    respuesta_c VARCHAR(255) NOT NULL,
    respuesta_d VARCHAR(255) NOT NULL,
    correcta CHAR(1) NOT NULL CHECK (correcta IN ('a','b','c','d'))
);

-- 3. TABLA USUARIOS (Datos demográficos anónimos)
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    profesion VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    genero VARCHAR(20) NOT NULL,
    pericia INT NOT NULL CHECK (pericia BETWEEN 0 AND 10)
);

-- 4. TABLA PRUEBAS_USABILIDAD (La sesión general del test)
CREATE TABLE pruebas_usabilidad (
    id_prueba INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_dispositivo INT NOT NULL,
    tiempo_total DECIMAL(10,4) NOT NULL, -- Tiempo exacto en segundos
    completado BOOLEAN DEFAULT TRUE,
    comentarios_usuario TEXT,
    propuestas_mejora TEXT,
    valoracion INT CHECK (valoracion BETWEEN 0 AND 10),
    puntuacion INT DEFAULT 0, -- Nota final del test
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo)
);

-- 5. TABLA RESPUESTAS_USUARIO (Detalle de cada pregunta contestada)
CREATE TABLE respuestas_usuario (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_prueba INT NOT NULL,
    id_pregunta INT NOT NULL,
    respuesta_escogida CHAR(1) NOT NULL,
    es_correcta BOOLEAN NOT NULL,

    FOREIGN KEY (id_prueba) REFERENCES pruebas_usabilidad(id_prueba),
    FOREIGN KEY (id_pregunta) REFERENCES preguntas(id)
);

-- 6. TABLA OBSERVACIONES (Notas del facilitador/profesor)
CREATE TABLE observaciones (
    id_observacion INT AUTO_INCREMENT PRIMARY KEY,
    id_prueba INT NOT NULL,
    comentario TEXT NOT NULL,
    
    FOREIGN KEY (id_prueba) REFERENCES pruebas_usabilidad(id_prueba)
);