-- ============================================
-- BASE DE DATOS: LIBRERÍA CRUD
-- Autor: Jonathan Zamora Cruz
-- Universidad Bancaria de México
-- ============================================

CREATE DATABASE IF NOT EXISTS libreria_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE libreria_db;

-- --------------------------------------------
-- TABLA: libros
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS libros (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    titulo      VARCHAR(200)   NOT NULL,
    autor       VARCHAR(150)   NOT NULL,
    genero      VARCHAR(80)    NOT NULL,
    año         YEAR           NOT NULL,
    precio      DECIMAL(10,2)  NOT NULL,
    stock       INT            NOT NULL DEFAULT 0,
    isbn        VARCHAR(20)    UNIQUE,
    created_at  DATETIME       DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME       DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- --------------------------------------------
-- DATOS DE EJEMPLO
-- --------------------------------------------
INSERT INTO libros (titulo, autor, genero, año, precio, stock, isbn) VALUES
('Cien Años de Soledad',       'Gabriel García Márquez', 'Realismo Mágico', 1967, 299.00, 15, '978-0-06-088328-7'),
('El Principito',              'Antoine de Saint-Exupéry','Fábula',          1943, 199.00, 25, '978-0-15-601219-5'),
('1984',                       'George Orwell',           'Distopía',        1949, 249.00, 10, '978-0-45-228285-3'),
('Don Quijote de la Mancha',   'Miguel de Cervantes',     'Clásico',         1605, 350.00,  8, '978-8-41-370497-8'),
('Harry Potter y la Piedra Filosofal', 'J.K. Rowling',   'Fantasía',        1997, 280.00, 20, '978-0-43-970818-8'),
('El Alquimista',              'Paulo Coelho',            'Ficción',         1988, 220.00, 18, '978-0-06-231609-7'),
('Sapiens',                    'Yuval Noah Harari',       'Historia',        2011, 320.00, 12, '978-0-06-231609-8'),
('Drácula',                    'Bram Stoker',             'Terror',          1897, 180.00,  5, '978-0-14-143984-3');
