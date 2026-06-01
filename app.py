from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from config import Config
from models.usuario import Usuario
from models.persona import Persona
from models.ayuda import Ayuda
import os
import logging
import sqlite3
from datetime import datetime, timedelta
from init_db import init_db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if os.environ.get('RENDER'):
    DB_PATH = '/var/data/alc.db'
else:
    DB_PATH = os.path.join(BASE_DIR, 'alc.db')

# Inicializar base de datos si no existe
init_db(force=False)

os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

app = Flask(__name__)
app.config.from_object(Config)

# Configurar logging: en producción (Render) usa stdout; en local, archivo
if os.environ.get('RENDER'):
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(
        filename=os.path.join(BASE_DIR, 'logs', 'auth_errors.log'),
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Función para obtener conexión a SQLite
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    try:
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['usuario'] = user['usuario']
            session['nombre'] = user['nombre']
            session['rol'] = user['rol']
            if is_ajax:
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
            return redirect(url_for('dashboard'))
        else:
            error_message = "Usuario o contraseña incorrectos"
            if is_ajax:
                return jsonify({'success': False, 'error_message': error_message}), 401
            return render_template('login.html', error_message=error_message)
    except Exception as e:
        logging.error(f'Error en login: {str(e)}')
        error_message = "Ha ocurrido un error en el sistema"
        if is_ajax:
            return jsonify({'success': False, 'error_message': error_message}), 500
        return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
        
        # Histórico de necesidades (últimos 6 meses) - SQLite
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', FechaSolicitud) as mes,
                COUNT(*) as cantidad
            FROM ayudas
            WHERE FechaSolicitud >= date('now', '-6 months')
            GROUP BY strftime('%Y-%m', FechaSolicitud)
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
        
        conn.close()
        
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        logging.error(f'Error en dashboard: {str(e)}')
        return render_template('dashboard.html', stats={})

@app.route('/ciudadano', methods=['GET', 'POST'])
@login_required
def ciudadano():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    ciudadano_id = request.args.get('id')
    ciudadano = None
    buscar = request.args.get('buscar', '')
    
    if ciudadano_id:
        ciudadano = Persona.get_by_id(cursor, ciudadano_id)
    
    if request.method == 'POST':
        try:
            id = request.form.get('id')
            nombre = request.form.get('nombre')
            cedula = request.form.get('cedula')
            direccion = request.form.get('direccion')
            telefono = request.form.get('telefono')
            comuna = request.form.get('comuna')
            
            if id:
                cursor.execute("""
                    UPDATE persona 
                    SET nombre = ?, cedula = ?, direccion = ?, telefono = ?, comuna = ? 
                    WHERE id = ?
                """, (nombre, cedula, direccion, telefono, comuna, id))
                success_message = "Ciudadano actualizado correctamente"
            else:
                cursor.execute("""
                    INSERT INTO persona (nombre, cedula, direccion, telefono, comuna) 
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, cedula, direccion, telefono, comuna))
                success_message = "Ciudadano registrado correctamente"
                nuevo_ciudadano_id = cursor.lastrowid
            
            conn.commit()
            
            if not id:
                return redirect(url_for('casos', 
                                      idP=nuevo_ciudadano_id, 
                                      show_modal='true',
                                      success='Ciudadano registrado. Ahora puede crear un caso.'))
            else:
                return redirect(url_for('ciudadano', success_message=success_message))
        except Exception as e:
            logging.error(f'Error al guardar ciudadano: {str(e)}')
            conn.rollback()
            error_message = "Ha ocurrido un error al guardar el ciudadano"
            return redirect(url_for('ciudadano', error_message=error_message))
    else:
        if buscar:
            cursor.execute("""
                SELECT * FROM persona 
                WHERE nombre LIKE ? OR cedula LIKE ? OR comuna LIKE ?
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
        
        success_message = request.args.get('success_message')
        error_message = request.args.get('error_message')
        
        conn.close()
        
        return render_template('ciudadano.html',
                             personas=personas,
                             ciudadano=ciudadano,
                             buscar=buscar,
                             success_message=success_message,
                             error_message=error_message)

@app.route('/ciudadano/eliminar/<int:id>')
@login_required
def eliminar_ciudadano(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM ayudas WHERE idP = ?", (id,))
        total_ayudas = cursor.fetchone()['total']
        
        if total_ayudas > 0:
            error_message = "No se puede eliminar el ciudadano porque tiene casos asociados"
            conn.close()
            return redirect(url_for('ciudadano', error_message=error_message))
        
        cursor.execute("DELETE FROM persona WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        
        success_message = "Ciudadano eliminado correctamente"
        return redirect(url_for('ciudadano', success_message=success_message))
    except Exception as e:
        logging.error(f'Error al eliminar ciudadano: {str(e)}')
        conn.rollback()
        error_message = "Ha ocurrido un error al eliminar el ciudadano"
        return redirect(url_for('ciudadano', error_message=error_message))

@app.route('/casos', methods=['GET', 'POST'])
@login_required
def casos():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    ayuda_id = request.args.get('id')
    ayuda = None
    
    if ayuda_id:
        ayuda = Ayuda.get_by_id(cursor, ayuda_id)
    
    cursor.execute("SELECT id, nombre, cedula, comuna FROM persona ORDER BY nombre")
    ciudadanos = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            id = request.form.get('id')
            idP = request.form.get('idP')
            motivo_caso = request.form.get('motivo_caso')
            especificacion_caso = request.form.get('especificacion_caso')
            valor_inversion_social = request.form.get('valor_inversion_social') or 0
            descayuda = request.form.get('descayuda')
            estado = request.form.get('estado')
            
            idUs = session['user_id']
            fecha_solicitud = datetime.now().strftime('%Y-%m-%d')
            fecha_entrega = datetime.now().strftime('%Y-%m-%d') if estado == 'Entregado' else None
            
            if id:
                cursor.execute("""
                    UPDATE ayudas 
                    SET idP = ?, idUs = ?, motivo_caso = ?, especificacion_caso = ?, 
                        valor_inversion_social = ?, FechaSolicitud = ?, FechaEntrega = ?, 
                        descayuda = ?, estado = ? 
                    WHERE id = ?
                """, (idP, idUs, motivo_caso, especificacion_caso, valor_inversion_social, 
                      fecha_solicitud, fecha_entrega, descayuda, estado, id))
                success_message = "Caso actualizado correctamente"
            else:
                cursor.execute("""
                    INSERT INTO ayudas (idP, idUs, motivo_caso, especificacion_caso, valor_inversion_social, 
                                      FechaSolicitud, FechaEntrega, descayuda, estado, remitido) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (idP, idUs, motivo_caso, especificacion_caso, valor_inversion_social, 
                      fecha_solicitud, fecha_entrega, descayuda, estado, 'No'))
                success_message = "Caso registrado correctamente"
            
            conn.commit()
            return redirect(url_for('casos', success=success_message))
        except Exception as e:
            logging.error(f'Error al guardar caso: {str(e)}')
            conn.rollback()
            error_message = "Ha ocurrido un error al guardar el caso"
            return redirect(url_for('casos', error=error_message))
    else:
        cursor.execute("""
            SELECT a.*, p.nombre as nombre_persona, p.cedula as cedula_persona 
            FROM ayudas a 
            JOIN persona p ON a.idP = p.id
            ORDER BY a.id DESC
        """)
        
        resultados = cursor.fetchall()
        
        success_message = request.args.get('success')
        error_message = request.args.get('error')
        
        conn.close()
        
        return render_template('casos.html',
                             ayudas=resultados,
                             ayuda=ayuda,
                             ciudadanos=ciudadanos,
                             success_message=success_message,
                             error_message=error_message)

@app.route('/casos/eliminar/<int:id>')
@login_required
def eliminar_caso(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ayudas WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        
        success_message = "Caso eliminado correctamente"
        return redirect(url_for('casos', success=success_message))
    except Exception as e:
        logging.error(f'Error al eliminar caso: {str(e)}')
        conn.rollback()
        error_message = "Ha ocurrido un error al eliminar el caso"
        return redirect(url_for('casos', error=error_message))

@app.route('/aprobar_caso/<int:id>')
@login_required
def aprobar_caso(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ayudas SET estado = 'Aprobado' WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        
        success_message = "Recursos aprobados correctamente"
        return redirect(url_for('casos', success=success_message))
    except Exception as e:
        logging.error(f'Error al aprobar caso: {str(e)}')
        conn.rollback()
        error_message = "Ha ocurrido un error al aprobar el caso"
        return redirect(url_for('casos', error=error_message))

@app.route('/remitir_caso', methods=['POST'])
@login_required
def remitir_caso():
    try:
        caso_id = request.form.get('caso_id')
        entidad_remision = request.form.get('entidad_remision')
        otra_entidad = request.form.get('otra_entidad')
        
        if entidad_remision == 'Otra Entidad' and otra_entidad:
            entidad_remision = otra_entidad
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE ayudas 
            SET remitido = 'Sí', entidad_remision = ?, fecha_remision = ? 
            WHERE id = ?
        """, (entidad_remision, datetime.now().strftime('%Y-%m-%d'), caso_id))
        
        conn.commit()
        conn.close()
        
        success_message = f"Caso remitido exitosamente a {entidad_remision}"
        return redirect(url_for('casos', success=success_message))
    except Exception as e:
        logging.error(f'Error al remitir caso: {str(e)}')
        conn.rollback()
        error_message = "Ha ocurrido un error al remitir el caso"
        return redirect(url_for('casos', error=error_message))

@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        if request.path.startswith('/static/'):
            response.headers['Cache-Control'] = 'public, max-age=2592000'
        else:
            response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=True)
