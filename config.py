import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_aleatoria'
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    
    # Configuración para producción
    DEBUG = False
    TESTING = False
