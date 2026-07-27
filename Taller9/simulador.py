import random

class Simulador:
    def iniciar_simulacion(self, preguntas, cantidad):
        seleccion = random.sample(preguntas, min(cantidad, len(preguntas)))
        puntaje = 0

        for p in seleccion:
            print(f"\n[{p.tema} - {p.dificultad}] {p.pregunta}")
            print(f"A) {p.opcion_a}\nB) {p.opcion_b}\nC) {p.opcion_c}\nD) {p.opcion_d}")
            respuesta = input("Tu respuesta (A/B/C/D): ").strip().upper()

            if respuesta == p.respuesta_correcta:
                puntaje += 1
                print("Correcto!")
            else:
                print(f"Incorrecto. Era: {p.respuesta_correcta}")

        print(f"\nPuntaje final: {puntaje}/{len(seleccion)}")
        return puntaje, len(seleccion)
