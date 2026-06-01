import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if os.environ.get('RENDER'):
    DB_PATH = '/var/data/alc.db'
else:
    DB_PATH = os.path.join(BASE_DIR, 'alc.db')

def init_db(force=False):
    """Inicializar la base de datos SQLite con la estructura original.
    
    Args:
        force: Si True, elimina la DB existente y la recrea (útil en CI/build).
               Si False y la DB existe, no hace nada.
    """
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    if os.path.exists(DB_PATH):
        if force:
            try:
                os.remove(DB_PATH)
                print("Base de datos existente eliminada.")
            except Exception as e:
                print(f"No se pudo eliminar la base de datos: {e}")
        else:
            print("La base de datos ya existe. Use force=True para recrearla.")
            return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario VARCHAR(40) NOT NULL UNIQUE,
            clave VARCHAR(60) NOT NULL,
            nombre VARCHAR(150) NOT NULL,
            cedula VARCHAR(30) NOT NULL,
            rol VARCHAR(60) NOT NULL
        )
    ''')

    # Crear tabla de persona
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persona (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(200) NOT NULL,
            cedula VARCHAR(30) NOT NULL,
            direccion TEXT NOT NULL,
            telefono VARCHAR(30) NOT NULL,
            comuna VARCHAR(200) NOT NULL
        )
    ''')

    # Crear tabla de ayudas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ayudas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idP INTEGER NOT NULL,
            idUs INTEGER NOT NULL,
            motivo_caso TEXT NOT NULL DEFAULT 'Ayudas Sociales',
            especificacion_caso TEXT NOT NULL DEFAULT '',
            valor_inversion_social REAL DEFAULT 0.00,
            tpayuda TEXT NOT NULL DEFAULT '',
            valayuda REAL DEFAULT 0,
            FechaSolicitud DATE NOT NULL,
            FechaEntrega DATE DEFAULT NULL,
            descayuda TEXT NOT NULL,
            estado VARCHAR(40) NOT NULL,
            remitido TEXT NOT NULL DEFAULT 'No',
            entidad_remision TEXT DEFAULT NULL,
            fecha_remision DATE DEFAULT NULL,
            FOREIGN KEY (idP) REFERENCES persona(id),
            FOREIGN KEY (idUs) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()

    # Insertar usuario por defecto
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (id, usuario, clave, nombre, cedula, rol) 
        VALUES (1, 'Adrianmbt', 'adrianmbt1', 'Adrian M. Bello', '19674244', 'Administrador')
    ''')

    conn.commit()
    conn.close()

    print("Base de datos inicializada correctamente.")
    print(f"Archivo: {DB_PATH}")
    print("Usuario por defecto: Adrianmbt / adrianmbt1")

if __name__ == '__main__':
    # Cuando se ejecuta directamente (ej: build command de Render),
    # crea la DB si no existe. No destruye datos existentes.
    init_db(force=False)
