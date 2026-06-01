import sqlite3
import os
import re

def import_data_from_sql(sql_file):
    """Importar datos desde un archivo SQL a SQLite"""
    
    if not os.path.exists(sql_file):
        print(f"Error: El archivo {sql_file} no existe.")
        return False
    
    # Verificar si la base de datos existe
    if not os.path.exists('alc.db'):
        print("La base de datos no existe. Ejecuta init_db.py primero.")
        return False
    
    conn = sqlite3.connect('alc.db')
    cursor = conn.cursor()
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraer inserciones de usuarios
        usuarios_pattern = r"INSERT INTO `usuarios` \([^)]+\) VALUES\n(.*?);"
        usuarios_match = re.search(usuarios_pattern, content, re.DOTALL)
        if usuarios_match:
            values = usuarios_match.group(1)
            # Limpiar y convertir a formato SQLite
            values = re.sub(r'`', '', values)
            values = re.sub(r'\n', ' ', values)
            values = re.sub(r'\s+', ' ', values).strip()
            
            # Insertar datos de usuarios
            cursor.execute("DELETE FROM usuarios")
            cursor.execute(f"INSERT INTO usuarios (id, usuario, clave, nombre, cedula, rol) VALUES {values}")
            print(f"Importados {cursor.rowcount} usuarios")
        
        # Extraer inserciones de persona
        persona_pattern = r"INSERT INTO `persona` \([^)]+\) VALUES\n(.*?);"
        persona_match = re.search(persona_pattern, content, re.DOTALL)
        if persona_match:
            values = persona_match.group(1)
            values = re.sub(r'`', '', values)
            values = re.sub(r'\n', ' ', values)
            values = re.sub(r'\s+', ' ', values).strip()
            
            cursor.execute("DELETE FROM persona")
            cursor.execute(f"INSERT INTO persona (id, nombre, cedula, direccion, telefono, comuna) VALUES {values}")
            print(f"Importados {cursor.rowcount} personas")
        
        # Extraer inserciones de ayudas
        ayudas_pattern = r"INSERT INTO `ayudas` \([^)]+\) VALUES\n(.*?);"
        ayudas_match = re.search(ayudas_pattern, content, re.DOTALL)
        if ayudas_match:
            values = ayudas_match.group(1)
            values = re.sub(r'`', '', values)
            values = re.sub(r'\n', ' ', values)
            values = re.sub(r'\s+', ' ', values).strip()
            
            cursor.execute("DELETE FROM ayudas")
            cursor.execute(f"INSERT INTO ayudas (id, idP, idUs, motivo_caso, especificacion_caso, valor_inversion_social, tpayuda, valayuda, FechaSolicitud, FechaEntrega, descayuda, estado, remitido, entidad_remision, fecha_remision) VALUES {values}")
            print(f"Importados {cursor.rowcount} ayudas")
        
        conn.commit()
        print("\nDatos importados correctamente.")
        return True
        
    except Exception as e:
        print(f"Error al importar datos: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    sql_file = 'respaldo base de datos/alc.sql'
    if os.path.exists(sql_file):
        import_data_from_sql(sql_file)
    else:
        print(f"El archivo {sql_file} no existe.")
        print("Por favor, asegúrate de que el archivo de respaldo esté en la ubicación correcta.")
