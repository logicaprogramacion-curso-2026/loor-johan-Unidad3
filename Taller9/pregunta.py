class Pregunta:
    def __init__(self, pregunta, opcion_a, opcion_b, opcion_c, opcion_d,
                 respuesta_correcta, dificultad, tema, id=None):
        self.id = id
        self.pregunta = pregunta
        self.opcion_a = opcion_a
        self.opcion_b = opcion_b
        self.opcion_c = opcion_c
        self.opcion_d = opcion_d
        self.respuesta_correcta = respuesta_correcta.upper()
        self.dificultad = dificultad
        self.tema = tema

    def __str__(self):
        return (f"[{self.id}] ({self.tema} - {self.dificultad}) {self.pregunta}\n"
                f"  A) {self.opcion_a}\n  B) {self.opcion_b}\n"
                f"  C) {self.opcion_c}\n  D) {self.opcion_d}")
