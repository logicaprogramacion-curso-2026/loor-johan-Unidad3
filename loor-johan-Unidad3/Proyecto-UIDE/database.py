"""
database.py

Capa de acceso a la base de datos SQLite del sistema (Capa 1: Datos).
Se encarga únicamente de abrir la conexión y crear el esquema si no
existe. La lógica de inserción/consulta de preguntas vive en
pregunta_dao.py.
"""

import sqlite3

NOMBRE_BD_POR_DEFECTO = "preguntas.db"


def conectar(ruta_bd=NOMBRE_BD_POR_DEFECTO):
    """Abre (o crea) la base de datos SQLite y devuelve la conexión.
    Usa row_factory = sqlite3.Row para poder acceder a las columnas por
    nombre (fila["campo"])."""
    conexion = sqlite3.connect(ruta_bd)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_bd(ruta_bd=NOMBRE_BD_POR_DEFECTO):
    """Crea la tabla 'preguntas' si todavía no existe."""
    conexion = conectar(ruta_bd)
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preguntas (
                id INTEGER PRIMARY KEY,
                tipo TEXT NOT NULL,
                enunciado TEXT NOT NULL,
                opciones TEXT,
                respuesta_correcta TEXT NOT NULL,
                puntaje REAL NOT NULL DEFAULT 0,
                retroalimentacion TEXT DEFAULT ''
            )
        """)
        conexion.commit()
    finally:
        conexion.close()


if __name__ == "__main__":
    # Permite inicializar la base de datos manualmente:
    #   python database.py
    inicializar_bd()
    print(f"Base de datos '{NOMBRE_BD_POR_DEFECTO}' inicializada correctamente.")
