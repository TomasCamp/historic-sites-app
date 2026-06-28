import os
from datetime import timedelta


class Config:
    """Configuración base común para todos los entornos."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-por-defecto-insegura")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Configuración de Flask-Session
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""

    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción."""

    DEBUG = False


config_by_name = {"development": DevelopmentConfig, "production": ProductionConfig}
