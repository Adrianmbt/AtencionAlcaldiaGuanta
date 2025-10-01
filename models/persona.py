class Persona:
    def __init__(self, id=None, nombre=None, cedula=None, direccion=None, telefono=None, comuna=None):
        self.id = id
        self.nombre = nombre
        self.cedula = cedula
        self.direccion = direccion
        self.telefono = telefono
        self.comuna = comuna
    
    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT * FROM persona")
        results = cursor.fetchall()
        return [
            Persona(
                id=row['id'],
                nombre=row['nombre'],
                cedula=row['cedula'],
                direccion=row['direccion'],
                telefono=row['telefono'],
                comuna=row['comuna']
            ) for row in results
        ]
    
    @staticmethod
    def get_by_id(cursor, persona_id):
        cursor.execute("SELECT * FROM persona WHERE id = %s", (persona_id,))
        result = cursor.fetchone()
        if result:
            return Persona(
                id=result['id'],
                nombre=result['nombre'],
                cedula=result['cedula'],
                direccion=result['direccion'],
                telefono=result['telefono'],
                comuna=result['comuna']
            )
        return None
    
    @staticmethod
    def get_by_cedula(cursor, cedula):
        cursor.execute("SELECT * FROM persona WHERE cedula = %s", (cedula,))
        result = cursor.fetchone()
        if result:
            return Persona(
                id=result['id'],
                nombre=result['nombre'],
                cedula=result['cedula'],
                direccion=result['direccion'],
                telefono=result['telefono'],
                comuna=result['comuna']
            )
        return None