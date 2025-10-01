from datetime import datetime

class Ayuda:
    def __init__(self, id=None, idP=None, idUs=None, motivo_caso=None, especificacion_caso=None, 
                 valor_inversion_social=None, fecha_solicitud=None, fecha_entrega=None, 
                 descayuda=None, estado=None, remitido=None):
        self.id = id
        self.idP = idP  # ID de la persona
        self.idUs = idUs  # ID del usuario
        self.motivo_caso = motivo_caso  # Motivo del caso (nuevo campo)
        self.especificacion_caso = especificacion_caso  # Especificación del caso (antes tpayuda)
        self.valor_inversion_social = valor_inversion_social  # Valor de inversión social (antes valayuda)
        self.fecha_solicitud = fecha_solicitud
        self.fecha_entrega = fecha_entrega
        self.descayuda = descayuda  # Descripción de la ayuda
        self.estado = estado
        self.remitido = remitido  # Nuevo campo para control de remisión
    
    @staticmethod
    def get_all(cursor):
        cursor.execute("""
            SELECT a.*, p.nombre as nombre_persona, p.cedula as cedula_persona 
            FROM ayudas a 
            JOIN persona p ON a.idP = p.id
        """)
        results = cursor.fetchall()
        return [
            Ayuda(
                id=row['id'],
                idP=row['idP'],
                idUs=row['idUs'],
                motivo_caso=row.get('motivo_caso', row.get('tpayuda', '')),  # Compatibilidad
                especificacion_caso=row.get('especificacion_caso', row.get('tpayuda', '')),
                valor_inversion_social=row.get('valor_inversion_social', row.get('valayuda', 0)),
                fecha_solicitud=row['FechaSolicitud'],
                fecha_entrega=row['FechaEntrega'],
                descayuda=row['descayuda'],
                estado=row['estado'],
                remitido=row.get('remitido', 'No')
            ) for row in results
        ]
    
    @staticmethod
    def get_by_id(cursor, ayuda_id):
        cursor.execute("""
            SELECT a.*, p.nombre as nombre_persona, p.cedula as cedula_persona 
            FROM ayudas a 
            JOIN persona p ON a.idP = p.id 
            WHERE a.id = %s
        """, (ayuda_id,))
        result = cursor.fetchone()
        if result:
            return Ayuda(
                id=result['id'],
                idP=result['idP'],
                idUs=result['idUs'],
                motivo_caso=result.get('motivo_caso', result.get('tpayuda', '')),
                especificacion_caso=result.get('especificacion_caso', result.get('tpayuda', '')),
                valor_inversion_social=result.get('valor_inversion_social', result.get('valayuda', 0)),
                fecha_solicitud=result['FechaSolicitud'],
                fecha_entrega=result['FechaEntrega'],
                descayuda=result['descayuda'],
                estado=result['estado'],
                remitido=result.get('remitido', 'No')
            )
        return None
    
    @staticmethod
    def get_by_persona_id(cursor, persona_id):
        cursor.execute("""
            SELECT a.*, p.nombre as nombre_persona, p.cedula as cedula_persona 
            FROM ayudas a 
            JOIN persona p ON a.idP = p.id 
            WHERE a.idP = %s
        """, (persona_id,))
        results = cursor.fetchall()
        return [
            Ayuda(
                id=row['id'],
                idP=row['idP'],
                idUs=row['idUs'],
                motivo_caso=row.get('motivo_caso', row.get('tpayuda', '')),
                especificacion_caso=row.get('especificacion_caso', row.get('tpayuda', '')),
                valor_inversion_social=row.get('valor_inversion_social', row.get('valayuda', 0)),
                fecha_solicitud=row['FechaSolicitud'],
                fecha_entrega=row['FechaEntrega'],
                descayuda=row['descayuda'],
                estado=row['estado'],
                remitido=row.get('remitido', 'No')
            ) for row in results
        ]