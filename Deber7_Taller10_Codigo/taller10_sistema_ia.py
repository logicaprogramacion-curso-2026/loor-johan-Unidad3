import math

def evaluar_area(texto_actividad, palabras_clave):
    """
    Cuenta cuántas palabras clave del área están presentes en la descripción
    y retorna un puntaje del 1 al 5.
    """
    coincidencias = sum(1 for palabra in palabras_clave if palabra in texto_actividad.lower())
    
    # Asigna un puntaje de 1 a 5 según la cantidad de palabras encontradas
    if coincidencias == 0:
        return 1, "Insuficiente: No se evidencian criterios de esta área."
    elif coincidencias == 1:
        return 2, "Básico: Se detecta una presencia mínima o indirecta."
    elif coincidencias == 2:
        return 3, "Aceptable: Cumple con los elementos esenciales."
    elif coincidencias == 3:
        return 4, "Sobresaliente: Integra varios elementos clave del área."
    else:
        return 5, "Ejemplar: Implementación completa y avanzada."

def main():
    print("=" * 60)
    print("  TALLER 10: SISTEMA DE IA FORMATIVA DOCENTE (ALGORITMO LOCAL)")
    print("=" * 60)

    # 1. Entrada de datos
    nombre_docente = input("1. Nombre del Docente: ").strip()
    disciplina = input("2. Disciplina / Materia: ").strip()
    actividad = input("3. Descripción de la Actividad: ").strip()

    if not nombre_docente or not disciplina or not actividad:
        print("\n[Error] Todos los campos son obligatorios.")
        return

    # 2. Diccionarios de palabras clave por área de evaluación
    claves_empoderamiento = [
        "autonomía", "autoevaluación", "metacognición", "reflexión", 
        "investigación", "propio", "decisión", "auto"
    ]
    
    claves_recursos = [
        "digital", "multimedia", "interactivo", "plataforma", 
        "app", "vídeo", "software", "web", "simulador", "ia"
    ]
    
    claves_evaluacion = [
        "rúbrica", "criterio", "retroalimentación", "feedback", 
        "ponderación", "evaluación", "formar", "indicadores"
    ]

    # 3. Procesamiento y cálculo de puntajes
    score1, diag1 = evaluar_area(actividad, claves_empoderamiento)
    score2, diag2 = evaluar_area(actividad, claves_recursos)
    score3, diag3 = evaluar_area(actividad, claves_evaluacion)

    promedio = round((score1 + score2 + score3) / 3, 1)

    # 4. Presentación del Informe
    print("\n" + "=" * 60)
    print("           INFORME DE DIAGNÓSTICO FORMATIVO")
    print("=" * 60)
    print(f"Docente:    {nombre_docente}")
    print(f"Disciplina: {disciplina}")
    print("-" * 60)
    print("--- PUNTAJES DE EVALUACIÓN (ESCALA 1-5) ---")
    print(f"1. Empoderamiento del Estudiante: {score1}/5 -> {diag1}")
    print(f"2. Recursos Digitales:           {score2}/5 -> {diag2}")
    print(f"3. Evaluación Formativa:          {score3}/5 -> {diag3}")
    print(f"\nPROMEDIO GENERAL: {promedio}/5")
    print("-" * 60)
    
    # 5. Recomendaciones dinámicas según los puntajes
    print("--- RECOMENDACIONES DE MEJORA ---")
    if score1 < 3:
        print("- Permite que los estudiantes elijan el formato de sus entregables para fomentar la autonomía.")
    if score2 < 3:
        print("- Integra herramientas interactivas o plataformas digitales para enriquecer la actividad.")
    if score3 < 3:
        print("- Añade una rúbrica explícita con criterios claros antes de iniciar la tarea.")
    if score1 >= 3 and score2 >= 3 and score3 >= 3:
        print("- Mantener la estructura actual e incorporar mecanismos de coevaluación entre pares.")
        
    print("=" * 60)

if __name__ == "__main__":
    main()