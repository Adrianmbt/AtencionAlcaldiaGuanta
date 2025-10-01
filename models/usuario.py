class Usuario:
    def __init__(self, id=None, usuario=None, clave=None, nombre=None, cedula=None, rol=None):
        self.id = id
        self.usuario = usuario
        self.clave = clave
        self.nombre = nombre
        self.cedula = cedula
        self.rol = rol
    
    @staticmethod
    def get_by_id(cursor, user_id):
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            return Usuario(
                id=result['id'],
                usuario=result['usuario'],
                clave=result['clave'],
                nombre=result['nombre'],
                cedula=result['cedula'],
                rol=result['rol']
            )
        return None
    
    @staticmethod
    def get_by_username(cursor, username):
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (username,))
        result = cursor.fetchone()
        if result:
            return Usuario(
                id=result['id'],
                usuario=result['usuario'],
                clave=result['clave'],
                nombre=result['nombre'],
                cedula=result['cedula'],
                rol=result['rol']
            )
        return None