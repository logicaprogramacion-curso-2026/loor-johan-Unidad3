"""
simulador.py

Capa de lógica (Capa 2): toma preguntas ya cargadas en la base de datos,
las presenta al usuario, compara sus respuestas y calcula el puntaje
final con retroalimentación. Cumple el entregable mínimo de la semana 8:
examen de al menos 5 preguntas con puntaje y retroalimentación.
"""

import random

LETRAS = "abcdefgh"


def iniciar_examen(dao, cantidad=5):
    """Selecciona 'cantidad' preguntas al azar de la base de datos,
    las presenta por consola, calcula el puntaje obtenido y muestra
    retroalimentación por pregunta y un resumen final."""
    preguntas = dao.listar_todas()

    if not preguntas:
        print("No hay preguntas cargadas. Importe un banco de preguntas primero.")
        return

    if len(preguntas) < cantidad:
        print(f"Solo hay {len(preguntas)} pregunta(s) cargada(s); "
              f"se usarán todas en lugar de {cantidad}.")
        cantidad = len(preguntas)

    seleccionadas = random.sample(preguntas, cantidad)
    puntaje_obtenido = 0
    puntaje_total = 0

    print(f"\n--- Examen: {cantidad} pregunta(s) ---\n")
    for numero, pregunta in enumerate(seleccionadas, start=1):
        puntaje_total += pregunta.puntaje
        print(f"Pregunta {numero} ({pregunta.tipo}): {pregunta.enunciado}")

        if pregunta.opciones:
            for letra, opcion in zip(LETRAS, pregunta.opciones):
                print(f"  {letra}) {opcion}")

        respuesta = input("Tu respuesta: ")
        es_correcta = comparar_respuesta(pregunta, respuesta)

        if es_correcta:
            puntaje_obtenido += pregunta.puntaje
            print("✔ ¡Correcto!")
        else:
            print(f"✘ Incorrecto. Respuesta correcta: {pregunta.respuesta_correcta}")

        if pregunta.retroalimentacion:
            print(f"   {pregunta.retroalimentacion}")
        print()

    print("--- Resultado final ---")
    print(f"Puntaje obtenido: {puntaje_obtenido} / {puntaje_total}")
    if puntaje_total > 0:
        porcentaje = (puntaje_obtenido / puntaje_total) * 100
        print(f"Porcentaje: {porcentaje:.1f}%")


def comparar_respuesta(pregunta, respuesta):
    """Compara la respuesta del usuario con la respuesta correcta,
    normalizando mayúsculas/minúsculas y espacios. Para preguntas de
    opción múltiple también acepta la letra de la opción (A, B, C...)."""
    respuesta_normalizada = str(respuesta).strip().lower()
    correcta_normalizada = str(pregunta.respuesta_correcta).strip().lower()

    if respuesta_normalizada == correcta_normalizada:
        return True

    if pregunta.opciones and respuesta_normalizada in LETRAS:
        indice = LETRAS.index(respuesta_normalizada)
        if 0 <= indice < len(pregunta.opciones):
            return pregunta.opciones[indice].strip().lower() == correcta_normalizada

    return False
