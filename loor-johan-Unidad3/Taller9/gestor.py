import json
from pregunta import Pregunta

class Gestor:
    def cargar_desde_json(self, ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        preguntas = []
        for item in data["cuestionario"]["preguntas"]:
            op = item["opciones"]
            preguntas.append(Pregunta(
                pregunta=item["pregunta"],
                opcion_a=op["A"], opcion_b=op["B"], opcion_c=op["C"], opcion_d=op["D"],
                respuesta_correcta=item["respuesta_correcta"],
                dificultad=item["dificultad"],
                tema=item["tema"]
            ))
        print(f"Carga desde JSON: {len(preguntas)} preguntas cargadas")
        return preguntas
