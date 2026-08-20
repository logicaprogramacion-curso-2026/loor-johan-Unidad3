"""
pregunta.py

Define la clase Pregunta: la unidad básica de datos del sistema de
evaluación. Representa una pregunta de opción múltiple, verdadero/falso,
emparejamiento o completar espacios.
"""


class Pregunta:
    """Representa una pregunta del banco de preguntas.

    Atributos:
        id (int | None): identificador único. Si es None, el DAO lo
            genera automáticamente al insertar.
        tipo (str): tipo de pregunta (ej. "multiple", "vf", "emparejar",
            "completar").
        enunciado (str): texto de la pregunta.
        opciones (list[str]): lista de opciones disponibles (puede estar
            vacía para preguntas de completar).
        respuesta_correcta (str): respuesta correcta esperada.
        puntaje (int | float): puntos que otorga la pregunta si se
            responde correctamente. Debe ser >= 0.
        retroalimentacion (str): mensaje que se muestra al usuario tras
            responder. Cadena vacía si no se proporciona.
    """

    def __init__(self, id=None, tipo="", enunciado="", opciones=None,
                 respuesta_correcta="", puntaje=0, retroalimentacion=""):
        self.id = id
        self.tipo = tipo
        self.enunciado = enunciado
        self.opciones = opciones if opciones is not None else []
        self.respuesta_correcta = respuesta_correcta
        self.puntaje = puntaje
        self.retroalimentacion = retroalimentacion

    def to_dict(self):
        """Devuelve la pregunta como diccionario (útil para exportar)."""
        return {
            "id": self.id,
            "tipo": self.tipo,
            "enunciado": self.enunciado,
            "opciones": self.opciones,
            "respuesta_correcta": self.respuesta_correcta,
            "puntaje": self.puntaje,
            "retroalimentacion": self.retroalimentacion,
        }

    def __repr__(self):
        return (f"Pregunta(id={self.id!r}, tipo={self.tipo!r}, "
                f"enunciado={self.enunciado[:40]!r}...)")

    def __eq__(self, other):
        if not isinstance(other, Pregunta):
            return NotImplemented
        return self.to_dict() == other.to_dict()
