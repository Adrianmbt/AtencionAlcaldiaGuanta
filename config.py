import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar-esta-clave-en-produccion-2026'
    
    # Usar 'filesystem' siempre. En Render guardamos las sesiones en el disco persistente
    SESSION_TYPE = 'filesystem'
    if os.environ.get('RENDER'):
        SESSION_FILE_DIR = '/var/data/flask_session'
    else:
        SESSION_FILE_DIR = os.path.join(BASE_DIR, 'flask_session')
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Configuración para producción
    DEBUG = False
    TESTING = False
