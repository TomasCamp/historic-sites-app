from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
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


@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
@permission_required("user_update")
def update(id: int):
    """Muestra el formulario y procesa la actualización de un usuario."""
    user = user_service.get_user_by_id(id)

    if not user:
        flash("El usuario buscado no existe.", "danger")
        return redirect(url_for("users.index"))

    form = user_forms.UserUpdateForm(request.form, obj=user)

    if form.validate_on_submit():
        user_data = form.data.copy()
        user_data.pop("csrf_token", None)
        user_service.update_user(id, **user_data)
        flash("Usuario editado correctamente.", "success")
        return redirect(url_for("users.index"))
    else:
        for field_name, error_messages in form.errors.items():
            for error in error_messages:
                flash(error, "danger")

    return render_template("users/update.html", form=form, user=user)


@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@permission_required("user_delete")
def delete(id: int):
    """Procesa la eliminación lógica de un usuario."""
    user = user_service.get_user_by_id(id)

    if not user:
        flash("El usuario buscado no existe.", "danger")
    elif current_user == user:
        flash("El usuario no se puede eliminar a si mismo.", "danger")
    else:
        user_service.delete_user(id)
        flash("El usuario fue eliminado correctamente.", "success")

    return redirect(url_for("users.index"))


@bp.route("/toggle-status/<int:id>", methods=["POST"])
@login_required
@permission_required("user_update")
def toggle_status(id: int):
    """Invierte el estado activo/inactivo de un usuario."""
    user = user_service.get_user_by_id(id)

    if not user:
        flash("El usuario buscado no existe.", "danger")
    elif current_user == user:
        flash("El usuario no se puede cambiar el estado a si mismo.", "danger")
    else:
        nuevo_estado = not user.is_active
        user_service.update_user_status(id, nuevo_estado)

        mensaje = (
            "Usuario activado correctamente."
            if nuevo_estado
            else "Usuario desactivado correctamente."
        )
        flash(mensaje, "success")

    return redirect(url_for("users.index"))
