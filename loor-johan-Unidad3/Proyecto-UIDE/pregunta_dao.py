"""
pregunta_dao.py

Data Access Object (DAO) para la entidad Pregunta. Aísla toda la lógica
de SQL del resto de la aplicación (Capa 1: Datos).
"""

import json
import sqlite3

from database import conectar, inicializar_bd
from pregunta import Pregunta


class PreguntaDAO:
    """Gestiona el acceso a la tabla 'preguntas' de la base de datos."""

    def __init__(self, ruta_bd="preguntas.db"):
        self.ruta_bd = ruta_bd
        inicializar_bd(self.ruta_bd)
        self.conexion = conectar(self.ruta_bd)

    def _siguiente_id(self):
        """Calcula el siguiente id disponible como MAX(id) + 1."""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT MAX(id) AS max_id FROM preguntas")
        max_id = cursor.fetchone()["max_id"]
        return 1 if max_id is None else max_id + 1

    def insertar(self, pregunta):
        """Inserta una Pregunta en la base de datos.

        - Si pregunta.id es None, se genera automáticamente.
        - Si el id ya existe, no se inserta y se devuelve False.
        - Si se inserta correctamente, se devuelve True.
        """
        if pregunta.id is None:
            pregunta.id = self._siguiente_id()

        cursor = self.conexion.cursor()
        cursor.execute("SELECT 1 FROM preguntas WHERE id = ?", (pregunta.id,))
        if cursor.fetchone() is not None:
            return False

        try:
            cursor.execute(
                """INSERT INTO preguntas
                   (id, tipo, enunciado, opciones, respuesta_correcta,
                    puntaje, retroalimentacion)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    pregunta.id,
                    pregunta.tipo,
                    pregunta.enunciado,
                    json.dumps(pregunta.opciones, ensure_ascii=False),
                    pregunta.respuesta_correcta,
                    pregunta.puntaje,
                    pregunta.retroalimentacion,
                ),
            )
            self.conexion.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def listar_todas(self):
        """Devuelve todas las preguntas almacenadas como objetos Pregunta."""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM preguntas ORDER BY id")
        preguntas = []
        for fila in cursor.fetchall():
            opciones = json.loads(fila["opciones"]) if fila["opciones"] else []
            preguntas.append(Pregunta(
                id=fila["id"],
                tipo=fila["tipo"],
                enunciado=fila["enunciado"],
                opciones=opciones,
                respuesta_correcta=fila["respuesta_correcta"],
                puntaje=fila["puntaje"],
                retroalimentacion=fila["retroalimentacion"],
            ))
        return preguntas

    def cerrar(self):
        """Cierra la conexión a la base de datos."""
        self.conexion.close()
