from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from flask_mysqldb import MySQL
from flask_session import Session
from config import Config
from models.usuario import Usuario
from models.persona import Persona
from models.ayuda import Ayuda  # Agregamos importación del modelo Ayuda
import os
import logging
from datetime import datetime, timedelta

# Crear directorios necesarios
if not os.path.exists('flask_session'):
    os.makedirs('flask_session')

if not os.path.exists('logs'):
    os.makedirs('logs')

app = Flask(__name__)
app.config.from_object(Config)

# Configurar MySQL
mysql = MySQL(app)
Session(app)

# Configurar logging
logging.basicConfig(
    filename='logs/auth_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Decorador para requerir login
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    return redirect(url_for('auth_login'))

@app.route('/auth/login', methods=['POST'])
def auth_login():
    try:
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND clave = %s", (usuario, clave))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            session['user_id'] = user['id']
            session['usuario'] = user['usuario']
            session['nombre'] = user['nombre']
            session['rol'] = user['rol']
            return redirect(url_for('dashboard'))
        else:
            error_message = "Usuario o contraseña incorrectos"
            return render_template('login.html', error_message=error_message)
    except Exception as e:
        logging.error(f'Error en login: {str(e)}')
        error_message = "Ha ocurrido un error en el sistema"
        return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        cursor = mysql.connection.cursor()
        
        # Obtener estadísticas del dashboard
        stats = {}
        
        # Total de ciudadanos
        cursor.execute("SELECT COUNT(*) as total FROM persona")
        stats['total_ciudadanos'] = cursor.fetchone()['total']
        
        # Total de casos
        cursor.execute("SELECT COUNT(*) as total FROM ayudas")
        stats['total_casos'] = cursor.fetchone()['total']
        
        # Casos pendientes
        cursor.execute("SELECT COUNT(*) as total FROM ayudas WHERE estado = 'Pendiente'")
        stats['casos_pendientes'] = cursor.fetchone()['total']
        
        # Casos entregados
        cursor.execute("SELECT COUNT(*) as total FROM ayudas WHERE estado = 'Entregado'")
        stats['casos_entregados'] = cursor.fetchone()['total']
        
        # Inversión total
        cursor.execute("SELECT COALESCE(SUM(COALESCE(valor_inversion_social, valayuda, 0)), 0) as total FROM ayudas")
        stats['inversion_total'] = cursor.fetchone()['total']
        
        # Casos por motivo (para gráfico de torta)
        cursor.execute("""
            SELECT 
                COALESCE(motivo_caso, 'Sin clasificar') as motivo,
                COUNT(*) as cantidad 
            FROM ayudas 
            GROUP BY COALESCE(motivo_caso, 'Sin clasificar')
        """)
        stats['casos_por_motivo'] = cursor.fetchall()
        
        # Casos remitidos
        cursor.execute("SELECT COUNT(*) as total FROM ayudas WHERE remitido = 'Sí'")
        stats['casos_remitidos'] = cursor.fetchone()['total']
        
        # Histórico de necesidades (últimos 6 meses)
        cursor.execute("""
            SELECT 
                DATE_FORMAT(FechaSolicitud, '%Y-%m') as mes,
                COUNT(*) as cantidad
            FROM ayudas
            WHERE FechaSolicitud >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(FechaSolicitud, '%Y-%m')
            ORDER BY mes
        """)
        stats['historico_necesidades'] = cursor.fetchall()
        
        # Mapa de necesidades (casos por comuna)
        cursor.execute("""
            SELECT 
                p.comuna,
                COUNT(a.id) as cantidad
            FROM ayudas a
            JOIN persona p ON a.idP = p.id
            GROUP BY p.comuna
            ORDER BY cantidad DESC
        """)
        stats['mapa_necesidades'] = cursor.fetchall()
        
        # Entidades a las que se remitieron casos
        cursor.execute("""
            SELECT 
                COALESCE(entidad_remision, 'Sin especificar') as entidad,
                COUNT(*) as cantidad
            FROM ayudas
            WHERE remitido = 'Sí'
            GROUP BY COALESCE(entidad_remision, 'Sin especificar')
        """)
        stats['entidades_remision'] = cursor.fetchall()
        
        cursor.close()
        
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        logging.error(f'Error en dashboard: {str(e)}')
        return render_template('dashboard.html', stats={})

@app.route('/ciudadano', methods=['GET', 'POST'])
@login_required
def ciudadano():
    cursor = mysql.connection.cursor()
    
    # Obtener ID del ciudadano si se está editando
    ciudadano_id = request.args.get('id')
    ciudadano = None
    buscar = request.args.get('buscar', '')
    
    if ciudadano_id:
        # Obtener datos del ciudadano a editar
        ciudadano = Persona.get_by_id(cursor, ciudadano_id)
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            id = request.form.get('id')
            nombre = request.form.get('nombre')
            cedula = request.form.get('cedula')
            direccion = request.form.get('direccion')
            telefono = request.form.get('telefono')
            comuna = request.form.get('comuna')
            
            if id:  # Editar ciudadano existente
                cursor.execute("""
                    UPDATE persona 
                    SET nombre = %s, cedula = %s, direccion = %s, telefono = %s, comuna = %s 
                    WHERE id = %s
                """, (nombre, cedula, direccion, telefono, comuna, id))
                success_message = "Ciudadano actualizado correctamente"
            else:  # Agregar nuevo ciudadano
                cursor.execute("""
                    INSERT INTO persona (nombre, cedula, direccion, telefono, comuna) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre, cedula, direccion, telefono, comuna))
                success_message = "Ciudadano registrado correctamente"
                
                # Obtener el ID del ciudadano recién creado
                nuevo_ciudadano_id = cursor.lastrowid
            
            mysql.connection.commit()
            
            # Si es un nuevo ciudadano, redirigir a casos con el ID
            if not id:
                return redirect(url_for('casos', 
                                      idP=nuevo_ciudadano_id, 
                                      show_modal='true',
                                      success=f'Ciudadano registrado. Ahora puede crear un caso.'))
            else:
                return redirect(url_for('ciudadano', success_message=success_message))
        except Exception as e:
            logging.error(f'Error al guardar ciudadano: {str(e)}')
            mysql.connection.rollback()
            error_message = "Ha ocurrido un error al guardar el ciudadano"
            return redirect(url_for('ciudadano', error_message=error_message))
    else:
        # Obtener listado de ciudadanos
        if buscar:
            cursor.execute("""
                SELECT * FROM persona 
                WHERE nombre LIKE %s OR cedula LIKE %s OR comuna LIKE %s
            """, (f'%{buscar}%', f'%{buscar}%', f'%{buscar}%'))
        else:
            cursor.execute("SELECT * FROM persona")
        
        resultados = cursor.fetchall()
        personas = [
            Persona(
                id=row['id'],
                nombre=row['nombre'],
                cedula=row['cedula'],
                direccion=row['direccion'],
                telefono=row['telefono'],
                comuna=row['comuna']
            ) for row in resultados
        ]
        
        # Obtener mensajes de éxito o error
        success_message = request.args.get('success_message')
        error_message = request.args.get('error_message')
        
        cursor.close()
        
        return render_template('ciudadano.html',
                             personas=personas,
                             ciudadano=ciudadano,
                             buscar=buscar,
                             success_message=success_message,
                             error_message=error_message)

# Ruta para eliminar ciudadano
@app.route('/ciudadano/eliminar/<int:id>')
@login_required
def eliminar_ciudadano(id):
    try:
        cursor = mysql.connection.cursor()
        
        # Verificar si el ciudadano tiene ayudas asociadas
        cursor.execute("SELECT COUNT(*) as total FROM ayudas WHERE idP = %s", (id,))
        total_ayudas = cursor.fetchone()['total']
        
        if total_ayudas > 0:
            error_message = "No se puede eliminar el ciudadano porque tiene casos asociados"
            return redirect(url_for('ciudadano', error_message=error_message))
        
        # Eliminar ciudadano
        cursor.execute("DELETE FROM persona WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        
        success_message = "Ciudadano eliminado correctamente"
        return redirect(url_for('ciudadano', success_message=success_message))
    except Exception as e:
        logging.error(f'Error al eliminar ciudadano: {str(e)}')
        mysql.connection.rollback()
        error_message = "Ha ocurrido un error al eliminar el ciudadano"
        return redirect(url_for('ciudadano', error_message=error_message))

# Ruta para el módulo de casos (ayudas) - RENOVADO
@app.route('/casos', methods=['GET', 'POST'])
@login_required
def casos():
    cursor = mysql.connection.cursor()
    
    # Obtener ID de la ayuda si se está editando
    ayuda_id = request.args.get('id')
    ayuda = None
    
    if ayuda_id:
        # Obtener datos de la ayuda a editar
        ayuda = Ayuda.get_by_id(cursor, ayuda_id)
    
    # Obtener listado de ciudadanos para el selector
    cursor.execute("SELECT id, nombre, cedula, comuna FROM persona ORDER BY nombre")
    ciudadanos = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario renovado
            id = request.form.get('id')
            idP = request.form.get('idP')
            motivo_caso = request.form.get('motivo_caso')
            especificacion_caso = request.form.get('especificacion_caso')
            valor_inversion_social = request.form.get('valor_inversion_social') or 0
            descayuda = request.form.get('descayuda')
            estado = request.form.get('estado')
            
            idUs = session['user_id']  # ID del usuario logueado
            fecha_solicitud = datetime.now().strftime('%Y-%m-%d')
            fecha_entrega = datetime.now().strftime('%Y-%m-%d') if estado == 'Entregado' else None
            
            if id:  # Editar caso existente
                # Verificar si la tabla tiene las nuevas columnas
                cursor.execute("SHOW COLUMNS FROM ayudas LIKE 'motivo_caso'")
                tiene_nuevas_columnas = cursor.fetchone() is not None
                
                if tiene_nuevas_columnas:
                    cursor.execute("""
                        UPDATE ayudas 
                        SET idP = %s, idUs = %s, motivo_caso = %s, especificacion_caso = %s, 
                            valor_inversion_social = %s, FechaSolicitud = %s, FechaEntrega = %s, 
                            descayuda = %s, estado = %s 
                        WHERE id = %s
                    """, (idP, idUs, motivo_caso, especificacion_caso, valor_inversion_social, 
                          fecha_solicitud, fecha_entrega, descayuda, estado, id))
                else:
                    # Compatibilidad con estructura antigua
                    cursor.execute("""
                        UPDATE ayudas 
                        SET idP = %s, idUs = %s, tpayuda = %s, valayuda = %s, 
                            FechaSolicitud = %s, FechaEntrega = %s, descayuda = %s, estado = %s 
                        WHERE id = %s
                    """, (idP, idUs, especificacion_caso, valor_inversion_social, 
                          fecha_solicitud, fecha_entrega, descayuda, estado, id))
                
                success_message = "Caso actualizado correctamente"
            else:  # Agregar nuevo caso
                # Verificar si la tabla tiene las nuevas columnas
                cursor.execute("SHOW COLUMNS FROM ayudas LIKE 'motivo_caso'")
                tiene_nuevas_columnas = cursor.fetchone() is not None
                
                if tiene_nuevas_columnas:
                    cursor.execute("""
                        INSERT INTO ayudas (idP, idUs, motivo_caso, especificacion_caso, valor_inversion_social, 
                                          FechaSolicitud, FechaEntrega, descayuda, estado, remitido) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (idP, idUs, motivo_caso, especificacion_caso, valor_inversion_social, 
                          fecha_solicitud, fecha_entrega, descayuda, estado, 'No'))
                else:
                    # Compatibilidad con estructura antigua
                    cursor.execute("""
                        INSERT INTO ayudas (idP, idUs, tpayuda, valayuda, FechaSolicitud, FechaEntrega, descayuda, estado) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (idP, idUs, especificacion_caso, valor_inversion_social, 
                          fecha_solicitud, fecha_entrega, descayuda, estado))
                
                success_message = "Caso registrado correctamente"
            
            mysql.connection.commit()
            
            # Redirigir para evitar reenvío del formulario
            return redirect(url_for('casos', success=success_message))
        except Exception as e:
            logging.error(f'Error al guardar caso: {str(e)}')
            mysql.connection.rollback()
            error_message = "Ha ocurrido un error al guardar el caso"
            return redirect(url_for('casos', error=error_message))
    else:
        # Obtener listado de casos con compatibilidad
        cursor.execute("SHOW COLUMNS FROM ayudas LIKE 'motivo_caso'")
        tiene_nuevas_columnas = cursor.fetchone() is not None
        
        if tiene_nuevas_columnas:
            cursor.execute("""
                SELECT a.*, p.nombre as nombre_persona, p.cedula as cedula_persona 
                FROM ayudas a 
                JOIN persona p ON a.idP = p.id
                ORDER BY a.id DESC
            """)
        else:
            cursor.execute("""
                SELECT a.*, p.nombre as nombre_persona, p.cedula as cedula_persona 
                FROM ayudas a 
                JOIN persona p ON a.idP = p.id
                ORDER BY a.id DESC
            """)
        
        resultados = cursor.fetchall()
        
        # Obtener mensajes de éxito o error
        success_message = request.args.get('success')
        error_message = request.args.get('error')
        
        cursor.close()
        
        return render_template('casos.html',
                             ayudas=resultados,
                             ayuda=ayuda,
                             ciudadanos=ciudadanos,
                             success_message=success_message,
                             error_message=error_message)

# Ruta para eliminar caso
@app.route('/casos/eliminar/<int:id>')
@login_required
def eliminar_caso(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM ayudas WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        
        success_message = "Caso eliminado correctamente"
        return redirect(url_for('casos', success=success_message))
    except Exception as e:
        logging.error(f'Error al eliminar caso: {str(e)}')
        mysql.connection.rollback()
        error_message = "Ha ocurrido un error al eliminar el caso"
        return redirect(url_for('casos', error=error_message))

# Ruta para aprobar caso
@app.route('/aprobar_caso/<int:id>')
@login_required
def aprobar_caso(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE ayudas SET estado = 'Aprobado' WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        
        success_message = "Recursos aprobados correctamente"
        return redirect(url_for('casos', success=success_message))
    except Exception as e:
        logging.error(f'Error al aprobar caso: {str(e)}')
        mysql.connection.rollback()
        error_message = "Ha ocurrido un error al aprobar el caso"
        return redirect(url_for('casos', error=error_message))

# Nueva ruta para remitir caso
@app.route('/remitir_caso', methods=['POST'])
@login_required
def remitir_caso():
    try:
        caso_id = request.form.get('caso_id')
        entidad_remision = request.form.get('entidad_remision')
        otra_entidad = request.form.get('otra_entidad')
        
        # Si seleccionó "Otra Entidad", usar el campo personalizado
        if entidad_remision == 'Otra Entidad' and otra_entidad:
            entidad_remision = otra_entidad
        
        cursor = mysql.connection.cursor()
        
        # Verificar si la tabla tiene las nuevas columnas
        cursor.execute("SHOW COLUMNS FROM ayudas LIKE 'remitido'")
        tiene_columna_remitido = cursor.fetchone() is not None
        
        if tiene_columna_remitido:
            cursor.execute("""
                UPDATE ayudas 
                SET remitido = 'Sí', entidad_remision = %s, fecha_remision = %s 
                WHERE id = %s
            """, (entidad_remision, datetime.now().strftime('%Y-%m-%d'), caso_id))
        else:
            # Si no tiene las nuevas columnas, solo actualizar el estado
            cursor.execute("""
                UPDATE ayudas 
                SET estado = 'Remitido' 
                WHERE id = %s
            """, (caso_id,))
        
        mysql.connection.commit()
        cursor.close()
        
        success_message = f"Caso remitido exitosamente a {entidad_remision}"
        return redirect(url_for('casos', success=success_message))
    except Exception as e:
        logging.error(f'Error al remitir caso: {str(e)}')
        mysql.connection.rollback()
        error_message = "Ha ocurrido un error al remitir el caso"
        return redirect(url_for('casos', error=error_message))

# Añadir caché para archivos estáticos
@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        if request.path.startswith('/static/'):
            # Caché para archivos estáticos (1 mes)
            response.headers['Cache-Control'] = 'public, max-age=2592000'
        else:
            # No caché para contenido dinámico
            response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=True)