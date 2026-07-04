from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from flask_session import Session
from flask_bcrypt import Bcrypt
from src.config import config_by_name


db = SQLAlchemy()
login_manager = LoginManager()
session = Session()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    env_setting = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config_by_name[env_setting])

    db.init_app(app)
    login_manager.init_app(app)
    session.init_app(app)
    bcrypt.init_app(app)

    from src.services.user_service import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    # Configurar redirección si alguien no está logeado.
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Se debe iniciar sesión para acceder."
    login_manager.login_message_category = "danger"

    # Comandos para estructurar e instanciar la BD
    @app.cli.command("reset-db")
    def reset_db():
        from src import models

        """Elimina y vuelve a crear todas las tablas de la base de datos."""
        print("🗑️ Eliminando tablas existentes...")
        db.drop_all()
        print("🏗️ Creando nueva estructura de tablas...")
        db.create_all()
        print("✨ Base de datos reseteada con éxito.")

    @app.cli.command("seed-db")
    def seed_db():
        """Ejecuta las funciones de carga de datos iniciales (seeds)."""
        from src.seeds import init_seeds

        print("🌱 Iniciando la carga de datos de prueba (seeds)...")
        init_seeds()
        print("✅ Datos de prueba cargados con éxito.")

    @app.route("/")
    @login_required
    def index():
        return render_template("home.html", user=current_user)

    # Registro de blueprints
    from src.controllers.auth_controller import bp as auth_bp

    app.register_blueprint(auth_bp)

    return app
