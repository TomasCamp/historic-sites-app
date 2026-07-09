from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from src.controllers.decorators import permission_required
from src.services import user_service
from src.forms import user_forms

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("/")
@login_required
@permission_required("user_index")
def index():
    """Muestra el listado de usuarios con opciones."""
    form = user_forms.UserFilterForm(request.args)

    filters = {}
    if form.validate():
        filters = form.data
    print(form.errors)

    users = user_service.list_filtered_users(**filters)

    return render_template("users/index.html", users=users, form=form)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("user_create")
def create():
    """Muestra el formulario y procesa la creación de un nuevo usuario."""
    form = user_forms.UserCreateForm()

    if form.validate_on_submit():
        user_data = form.data.copy()
        user_data.pop("password_confirm", None)
        user_data.pop("csrf_token", None)
        new_user = user_service.create_user(**user_data)
        if new_user:
            flash("Usuario creado correctamente.", "success")
            return redirect(url_for("users.index"))
        flash("El email ingresado ya pertenece a un usuario registrado.", "danger")
    else:
        for field_name, error_messages in form.errors.items():
            for error in error_messages:
                flash(error, "danger")

    return render_template("users/create.html", form=form)
