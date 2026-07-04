from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def permission_required(permission_name: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Se debe iniciar sesión para acceder.", "danger")
                return redirect(url_for("auth.login"))

            if not current_user.has_permission(permission_name):
                flash(
                    "No cuenta con los permisos para acceder a esa sección.", "danger"
                )
                return redirect(url_for("index"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
