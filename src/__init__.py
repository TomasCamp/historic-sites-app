from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from src.config import config_by_name


db = SQLAlchemy()
login_manager = LoginManager()
session = Session()


def create_app():
    app = Flask(__name__)
    env_setting = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config_by_name[env_setting])

    db.init_app(app)
    login_manager.init_app(app)
    session.init_app(app)

    @app.cli.command("reset-db")
    def reset_db():
        """Elimina y vuelve a crear todas las tablas de la base de datos."""
        print("🗑️ Eliminando tablas existentes...")
        db.drop_all()
        print("🏗️ Creando nueva estructura de tablas...")
        db.create_all()
        print("✨ Base de datos reseteada con éxito.")

    @app.cli.command("seed-db")
    def seed_db():
        """Ejecuta las funciones de carga de datos iniciales (seeds)."""
        from src.models.seeds import init_seeds

        print("🌱 Iniciando la carga de datos de prueba (seeds)...")
        init_seeds()
        print("✅ Datos de prueba cargados con éxito.")

    @app.route("/")
    def index():
        return "¡Estructura base funcionando perfectamente!"

    return app
