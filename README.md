# Historic Sites App

Sistema corporativo de gestión y catalogación de patrimonio histórico, desarrollado con una arquitectura híbrida que combina Server-Side Rendering (SSR) para la administración interna y una API REST pública para el consumo externo de datos.

---

## Tecnologías Utilizadas

Este proyecto fue desarrollado utilizando las mejores prácticas de la industria para el ecosistema de Python:

* **[Python](https://www.python.org/)** (v3.11+) - Lenguaje principal.
* **[Flask](https://flask.palletsprojects.com/)** - Micro-framework ágil para el desarrollo web.
* **[Poetry](https://python-poetry.org/)** - Gestor de dependencias y entornos virtuales.
* **[PostgreSQL](https://www.postgresql.org/)** - Sistema de gestión de bases de datos relacionales.
* **[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)** - ORM para la abstracción y manejo de la base de datos.
* **[Flask-Login](https://flask-login.readthedocs.io/)** - Gestión de sesiones de usuario y autenticación.
* **[Flask-WTF](https://flask-wtf.readthedocs.io/)** - Validación de formularios y protección CSRF.

---

## Arquitectura del Proyecto

El proyecto sigue el patrón **MVC (Modelo-Vista-Controlador)** estructurado mediante el uso de **Application Factory** y **Blueprints** en Flask. Esto permite mantener un código altamente escalable, desacoplado y modular.

```text
mi_proyecto_flask/
├── src/                  # Código fuente de la aplicación
│   ├── controllers/      # Controladores (Rutas y Blueprints)
│   ├── models/           # Modelos de SQLAlchemy (Capa de datos)
│   ├── services/         # Lógica de negocio independiente
│   ├── forms/            # Validaciones con WTForms
│   ├── templates/        # Vistas (Jinja2 Templates)
│   ├── static/           # Archivos estáticos (CSS, JS)
│   ├── config.py         # Configuración dinámica por entornos
│   └── __init__.py       # Inicialización de la App Factory
├── app.py                # Punto de entrada de la aplicación
├── pyproject.toml        # Configuración de Poetry
└── .env                  # Plantilla de variables de entorno
```

## Requisitos e Instalación
Siga estos pasos para clonar y ejecutar el proyecto localmente.

### Prerrequisitos
- Tener instalado Python 3.11 o superior.
- Tener instalado Poetry.
- Un servidor PostgreSQL activo.

### Pasos
Clonar el repositorio:

```Bash
git clone https://github.com/TomasCamp/historic-sites-app.git
cd historic-sites-app
```

Instalar las dependencias con Poetry:

```Bash
poetry install
```

Configurar las variables de entorno:

Cree el archivo .env y complete los campos correspondientes con sus credenciales locales:

```Plaintext
FLASK_ENV=development
SECRET_KEY=su_clave_secreta_aqui
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_bd
```

Preparar la base de datos:
```Bash
poetry run flask reset-db
poetry run flask seed-db
```

Ejecutar la aplicación:

```Bash
poetry run python app.py
```
La aplicación estará disponible en http://127.0.0.1:5000.
