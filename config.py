import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clave secreta para firmar las cookies de sesión
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar-esta-clave-en-produccion-2026'

    # Sesiones basadas en cookies firmadas (no requiere disco ni librería extra)
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'  # Cambiar a 'signed_cookie' para producción en Render
    SESSION_COOKIE_SECURE = True  # Solo enviar cookies por HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Evitar acceso a cookies desde JavaScript
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protección contra CSRF

    # Configuración para producción
    DEBUG = False
    TESTING = False
