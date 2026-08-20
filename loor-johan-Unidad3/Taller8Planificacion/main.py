from docente import docente
from database import database
from docente_dao import docente_dao

# 1. Inicializar la base de datos
database_pe = database()

# 2. Crear el DAO pasando la conexión
docente_dao = docente_dao(database_pe)

# 3. Crear la tabla si no existe
docente_dao.crear_tabla()

# 4. Crear e insertar el objeto docente
docente_1 = docente("Johan Loor", "Florida Norte", "094351766", "joloorgo@uide.edu.ec")
docente_dao.insertar(docente_1)

# 5. Listar los docentes registrados para verificar
print("\n--- Docentes en la base de datos ---")
docentes = docente_dao.obtener_todos()
for doc in docentes:
    print(f"ID: {doc[0]} | Nombre: {doc[1]} | Dirección: {doc[2]} | Teléfono: {doc[3]} | Email: {doc[4]}")

# 6. Cerrar conexión
database_pe.cerrar()