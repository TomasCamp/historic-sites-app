from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import current_user, login_user
from src.services.user_service import authenticate_user
from src.forms.auth_form import LoginForm


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Muestra el formulario y procesa el inicio de sesión de los usuarios."""
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(email=form.email.data, password=form.password.data)

        if user:
            login_user(user, remember=form.remember_me.data)

            flash("La sesión se inició con éxito.", "success")

            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))

        flash("Email y/o contraseña incorrectos.", "danger")
    else:
        for field_name, error_messages in form.errors.items():
            for error in error_messages:
                flash(error, "danger")

    return render_template("auth/login.html", form=form)
