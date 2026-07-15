from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from src.controllers.decorators import permission_required
from src.services import tag_service
from src.forms import tag_forms

bp = Blueprint("tags", __name__, url_prefix="/tags")


@bp.get("/")
@login_required
@permission_required("tag_index")
def index():
    """Muestra el listado de tags con opciones."""
    form = tag_forms.TagFilterForm(request.args)

    filters = {}
    if form.validate():
        filters = form.data

    tags = tag_service.list_filtered_tags(**filters)

    return render_template("tags/index.html", tags=tags, form=form)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("tag_create")
def create():
    """Muestra el formulario y procesa la creación de un nuevo tag."""
    form = tag_forms.TagCreateForm()

    if form.validate_on_submit():
        tag_data = form.data.copy()
        tag_data.pop("csrf_token", None)
        if tag_service.create_tag(**tag_data):
            flash("Etiqueta creada correctamente.", "success")
            return redirect(url_for("tags.index"))
        else:
            flash("Ya existe una etiqueta igual o parecida.", "danger")
    else:
        for field_name, error_messages in form.errors.items():
            for error in error_messages:
                flash(error, "danger")

    return render_template("tags/create.html", form=form)
