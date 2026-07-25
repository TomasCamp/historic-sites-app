from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from src.controllers.decorators import permission_required
from src.services import historic_site_service, storage_service, tag_service
from src.forms import historic_site_forms

bp = Blueprint("historic_sites", __name__, url_prefix="/historic_sites")


@bp.get("/")
@login_required
@permission_required("historic_site_index")
def index():
    """Muestra el listado de historic_sites con opciones."""
    form = historic_site_forms.HistoricSiteFilterForm(request.args)

    filters = {}
    if form.validate():
        filters = form.data

    print(form.errors)
    historic_sites = historic_site_service.list_filtered_historic_sites(**filters)

    return render_template(
        "historic_sites/index.html", historic_sites=historic_sites, form=form
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("historic_site_create")
def create():
    """Muestra el formulario y procesa la creación de un nuevo historic_site."""
    form = historic_site_forms.HistoricSiteCreateForm()

    if form.validate_on_submit():
        user_data = form.data.copy()
        user_data.pop("csrf_token", None)
        cover_image = user_data.pop("cover_image")
        tag_ids = user_data.pop("tags")

        # Validar Tags
        tags = []
        for tag_id in tag_ids:
            tag = tag_service.get_tag_by_id(tag_id)
            if not tag:
                flash("La etiqueta seleccionada no es válida.", "danger")
                return render_template("historic_sites/create.html", form=form)
            tags.append(tag)

        # Subir imagen
        image_data = storage_service.upload_image(cover_image)

        historic_site = historic_site_service.create_historic_site(
            user_id=current_user.id, **image_data, **user_data
        )
        for tag in tags:
            historic_site_service.assign_tag_to_historic_site(
                tag, historic_site, current_user.id
            )

        flash("Sitio historico creado correctamente.", "success")
        return redirect(url_for("historic_sites.index"))
    else:
        for field_name, error_messages in form.errors.items():
            for error in error_messages:
                flash(error, "danger")

    return render_template("historic_sites/create.html", form=form)
