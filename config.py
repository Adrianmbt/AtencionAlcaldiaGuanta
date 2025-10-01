import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_aleatoria'
    SESSION_TYPE = 'filesystem'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'alc'
    MYSQL_CURSORCLASS = 'DictCursor'
    SESSION_PERMANENT = False
    
    # Configuraciones de rendimiento
    MYSQL_POOL_SIZE = 20
    MYSQL_POOL_RECYCLE = 3600
    
    # Configuración para producción
    DEBUG = False
    TESTING = False