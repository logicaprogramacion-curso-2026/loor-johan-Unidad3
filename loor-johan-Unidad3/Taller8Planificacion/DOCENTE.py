class docente:
    def __init__(self,
                 nombre,
                 email,        
                 direccion=None, 
                 telefono=None):
        self.nombre = nombre
        self.email = email
        self.direccion = direccion
        self.telefono = telefono