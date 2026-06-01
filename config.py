import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar-esta-clave-en-produccion-2026'
    
    # En Render el disco es efímero; usar 'null' para sesiones basadas en cookies firmadas
    # En local usamos 'filesystem' para debug cómodo
    SESSION_TYPE = 'null' if os.environ.get('RENDER') else 'filesystem'
    SESSION_FILE_DIR = os.path.join(BASE_DIR, 'flask_session')
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Configuración para producción
    DEBUG = False
    TESTING = False
