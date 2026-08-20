"""
main.py

Interfaz de línea de comandos (CLI) del sistema de evaluación automática
(Capa 3: Presentación). Menú en bucle para importar preguntas, listarlas
e iniciar un examen.

Ejecutar con:
    python main.py
"""

import gestor
import simulador
from pregunta_dao import PreguntaDAO


def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Importar preguntas desde archivo")
    print("2. Listar preguntas")
    print("3. Iniciar examen")
    print("4. Salir")


def opcion_importar(dao):
    nombre_archivo = input("Ingrese el nombre del archivo (ej. preguntas.json): ").strip()
    print("Procesando archivo...")
    try:
        resultado = gestor.importar_preguntas(nombre_archivo, dao)
    except (FileNotFoundError, ValueError) as error:
        print(f"No se pudo importar el archivo: {error}")
        return

    print("\nResumen:")
    print(f"- Insertadas: {resultado['insertadas']}")
    print(f"- Omitidas (duplicados): {resultado['omitidas']}")
    print(f"- Errores: {resultado['errores']}")
    if resultado["mensajes"]:
        print("Detalles de errores:")
        for mensaje in resultado["mensajes"]:
            print(f"  - {mensaje}")
    input("Presione Enter para continuar...")


def opcion_listar(dao):
    preguntas = dao.listar_todas()
    if not preguntas:
        print("No hay preguntas cargadas todavía.")
    else:
        print(f"\nTotal de preguntas: {len(preguntas)}")
        for pregunta in preguntas:
            print(f"  [{pregunta.id}] ({pregunta.tipo}) {pregunta.enunciado}")
    input("Presione Enter para continuar...")


def opcion_examen(dao):
    entrada = input("¿Cuántas preguntas desea en el examen? (Enter = 5): ").strip()
    try:
        cantidad = int(entrada) if entrada else 5
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        print("Cantidad inválida, se usarán 5 preguntas.")
        cantidad = 5
    simulador.iniciar_examen(dao, cantidad)
    input("Presione Enter para continuar...")


def main():
    dao = PreguntaDAO()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion_importar(dao)
        elif opcion == "2":
            opcion_listar(dao)
        elif opcion == "3":
            opcion_examen(dao)
        elif opcion == "4":
            print("¡Hasta luego!")
            dao.cerrar()
            break
        else:
            print("Opción inválida, intente nuevamente.")


if __name__ == "__main__":
    main()
