from database import database
from pregunta_dao import PreguntaDAO
from gestor import Gestor
from simulador import Simulador

db = database("preguntas.db")
dao = PreguntaDAO(db)
gestor = Gestor()

while True:
    print("\n1. Cargar preguntas desde JSON")
    print("2. Ver estadisticas")
    print("3. Iniciar simulacion")
    print("4. Salir")
    opcion = input("Opcion: ").strip()

    if opcion == "1":
        preguntas = gestor.cargar_desde_json("preguntas.json")
        dao.insertar_muchas(preguntas)

    elif opcion == "2":
        print(f"Total de preguntas: {dao.contar_preguntas()}")
        for tema, total in dao.estadisticas_por_tema():
            print(f"  {tema}: {total}")

    elif opcion == "3":
        preguntas = dao.obtener_todas()
        if not preguntas:
            print("Primero carga preguntas (opcion 1).")
        else:
            cantidad = int(input(f"Cuantas preguntas (max {len(preguntas)})? "))
            Simulador().iniciar_simulacion(preguntas, cantidad)

    elif opcion == "4":
        db.cerrar()
        break

    else:
        print("Opcion invalida.")
