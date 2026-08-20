class docente_dao:
    def __init__(self, db):
        self.db = db
        self.crear_tabla()

    def crear_tabla(self):
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS docente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                correo TEXT
            )
        ''')
        self.db.conn.commit()

    def insertar_tabla(self, docente):
        """Inserta los datos de un objeto docente en la base de datos."""
        query = '''
            INSERT INTO docente (nombre, direccion, telefono, correo)
            VALUES (?, ?, ?, ?)
        '''
        
        correo = getattr(docente, 'correo', getattr(docente, 'email', None))
        
        valores = (
            docente.nombre,
            docente.direccion,
            docente.telefono,
            correo
        )
        
        self.db.cursor.execute(query, valores)
        self.db.conn.commit() 
        print(f"Docente '{docente.nombre}' guardado exitosamente en la base de datos.")