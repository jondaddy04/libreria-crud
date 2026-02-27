"""
database.py  –  Capa de acceso a datos
Maneja toda la comunicación con MySQL (XAMPP)
"""

import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    """Retorna una conexión activa a MySQL."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn


# ──────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────
def insertar_libro(titulo, autor, genero, año, precio, stock, isbn):
    sql = """
        INSERT INTO libros (titulo, autor, genero, año, precio, stock, isbn)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (titulo, autor, genero, año, precio, stock, isbn or None))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return nuevo_id


# ──────────────────────────────────────────
# READ
# ──────────────────────────────────────────
def obtener_todos():
    sql = "SELECT id, titulo, autor, genero, año, precio, stock, isbn FROM libros ORDER BY id DESC"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def buscar_libros(texto):
    sql = """
        SELECT id, titulo, autor, genero, año, precio, stock, isbn
        FROM libros
        WHERE titulo LIKE %s OR autor LIKE %s OR genero LIKE %s OR isbn LIKE %s
        ORDER BY titulo
    """
    like = f"%{texto}%"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (like, like, like, like))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def obtener_por_id(libro_id):
    sql = "SELECT id, titulo, autor, genero, año, precio, stock, isbn FROM libros WHERE id = %s"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (libro_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


# ──────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────
def actualizar_libro(libro_id, titulo, autor, genero, año, precio, stock, isbn):
    sql = """
        UPDATE libros
        SET titulo=%s, autor=%s, genero=%s, año=%s, precio=%s, stock=%s, isbn=%s
        WHERE id=%s
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (titulo, autor, genero, año, precio, stock, isbn or None, libro_id))
    conn.commit()
    afectados = cursor.rowcount
    cursor.close()
    conn.close()
    return afectados


# ──────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────
def eliminar_libro(libro_id):
    sql = "DELETE FROM libros WHERE id = %s"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (libro_id,))
    conn.commit()
    afectados = cursor.rowcount
    cursor.close()
    conn.close()
    return afectados
