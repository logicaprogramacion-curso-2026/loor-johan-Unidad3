from pregunta import Pregunta

class PreguntaDAO:
    def __init__(self, db):
        self.db = db
        self.crear_tabla()

    def crear_tabla(self):
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pregunta TEXT, opcion_a TEXT, opcion_b TEXT, opcion_c TEXT,
                opcion_d TEXT, respuesta_correcta TEXT, dificultad TEXT, tema TEXT
            )
        ''')
        self.db.conn.commit()

    def insertar_muchas(self, preguntas):
        for p in preguntas:
            self.db.cursor.execute(
                '''INSERT INTO preguntas (pregunta, opcion_a, opcion_b, opcion_c,
                   opcion_d, respuesta_correcta, dificultad, tema)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (p.pregunta, p.opcion_a, p.opcion_b, p.opcion_c, p.opcion_d,
                 p.respuesta_correcta, p.dificultad, p.tema)
            )
        self.db.conn.commit()
        print(f"{len(preguntas)} preguntas insertadas correctamente.")

    def obtener_todas(self):
        self.db.cursor.execute("SELECT * FROM preguntas")
        return [Pregunta(id=f[0], pregunta=f[1], opcion_a=f[2], opcion_b=f[3],
                          opcion_c=f[4], opcion_d=f[5], respuesta_correcta=f[6],
                          dificultad=f[7], tema=f[8]) for f in self.db.cursor.fetchall()]

    def contar_preguntas(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM preguntas")
        return self.db.cursor.fetchone()[0]

    def estadisticas_por_tema(self):
        self.db.cursor.execute("SELECT tema, COUNT(*) FROM preguntas GROUP BY tema")
        return self.db.cursor.fetchall()
