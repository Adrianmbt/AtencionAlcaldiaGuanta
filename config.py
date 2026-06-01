import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clave secreta para firmar las cookies de sesión
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar-esta-clave-en-produccion-2026'

    # Sesiones basadas en cookies firmadas (no requiere disco ni librería extra)
    SESSION_PERMANENT = False

    # Configuración para producción
    DEBUG = False
    TESTING = False
