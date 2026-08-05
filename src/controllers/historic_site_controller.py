from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from src.controllers.decorators import permission_required
from src.services import (
    historic_site_service,
    storage_service,
    tag_service,
    change_event_service,
)
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
        historic_site_data = form.data.copy()
        historic_site_data.pop("csrf_token", None)
        cover_image = historic_site_data.pop("cover_image")
        tag_ids = historic_site_data.pop("tags")

        # Validar Tags
        tags = []
        for tag_id in tag_ids:
            tag = tag_service.get_tag_by_id(tag_id)
            if not tag:
                flash("Una etiqueta seleccionada no es válida.", "danger")
                return render_template("historic_sites/create.html", form=form)
            tags.append(tag)

        # Subir imagen
        image_data = storage_service.upload_image(cover_image)

        historic_site = historic_site_service.create_historic_site(
            user_id=current_user.id, **image_data, **historic_site_data
        )
        historic_site_service.assign_tags_to_historic_site(
            tags, historic_site, current_user.id
        )

        flash("Sitio historico creado correctamente.", "success")
        return redirect(url_for("historic_sites.index"))
    else:
        for field_name, error_messages in form.errors.items():
            for error in error_messages:
                flash(error, "danger")

    return render_template("historic_sites/create.html", form=form)


@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
@permission_required("historic_site_update")
def update(id: int):
    """Muestra el formulario y procesa la actualización de un historic_site."""
    historic_site = historic_site_service.get_historic_site_by_id(id)

    if not historic_site:
        flash("El sitio historico buscado no existe.", "danger")
        return redirect(url_for("historic_sites.index"))

    form = historic_site_forms.HistoricSiteUpdateForm(obj=historic_site)

    if form.validate_on_submit():
        historic_site_data = form.data.copy()
        historic_site_data.pop("csrf_token", None)
        cover_image = historic_site_data.pop("cover_image", None)
        tag_ids = historic_site_data.pop("tags", None)

        # Validar Tags
        tags = []
        for tag_id in tag_ids:
            tag = tag_service.get_tag_by_id(tag_id)
            if not tag:
                flash("Una etiqueta seleccionada no es válida.", "danger")
                return render_template("historic_sites/update.html", form=form)
            tags.append(tag)

        is_changed = any(
            getattr(historic_site, key, None) != value
            for key, value in historic_site_data.items()
        )

        # Subir imagen
        image_data = {
            "cover_image_url": historic_site.cover_image_url,
            "cover_image_public_id": historic_site.cover_image_public_id,
        }

        if bool(cover_image and cover_image.filename):
            is_changed = True
            if not storage_service.delete_image(historic_site.cover_image_public_id):
                flash("Hubo un error al cambiar de imagen.", "danger")
                return render_template("historic_sites/update.html", form=form)
            image_data = storage_service.upload_image(cover_image)

        tag_changed = historic_site_service.assign_tags_to_historic_site(
            tags, historic_site, current_user.id
        )
        if is_changed or tag_changed:
            if is_changed:
                historic_site_service.update_historic_site(
                    historic_site_id=id,
                    user_id=current_user.id,
                    **image_data,
                    **historic_site_data,
                )
            flash("Sitio historico editado correctamente.", "success")
            return redirect(url_for("historic_sites.index"))
        else:
            flash("No hubo cambios detectados.", "danger")
    else:
        for field_name, error_messages in form.errors.items():
            for error in error_messages:
                flash(error, "danger")

    return render_template("historic_sites/update.html", form=form)


@bp.route("/toggle-status/<int:id>", methods=["POST"])
@login_required
@permission_required("historic_site_update")
def toggle_status(id: int):
    """Invierte el estado visible/oculto de un historic_site."""
    historic_site = historic_site_service.get_historic_site_by_id(id)

    if not historic_site:
        flash("El sitio historico buscado no existe.", "danger")
    else:
        is_visible = historic_site_service.change_visibility_historic_site(
            historic_site, current_user.id
        )

        message = (
            "El sitio historico se hizo visible correctamente."
            if is_visible
            else "El sitio historico se ocultó correctamente."
        )
        flash(message, "success")

    return redirect(url_for("historic_sites.index"))


@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@permission_required("historic_site_delete")
def delete(id: int):
    """Elimina lógicamente un historic_site."""

    if historic_site_service.delete_historic_site(id, current_user.id):
        flash("El sitio historico fue borrado correctamente.", "success")
    else:
        flash("El sitio historico buscado no existe.", "danger")

    return redirect(url_for("historic_sites.index"))


@bp.get("/<int:id>")
@login_required
@permission_required("historic_site_show")
def show(id: int):
    """Muestra todos los datos de un historic_site."""
    historic_site = historic_site_service.get_historic_site_by_id(id)
    if not historic_site:
        flash("El sitio historico buscado no existe.", "danger")
        return redirect(url_for("historic_sites.index"))

    pageForm = historic_site_forms.ChangeEventPageForm(request.args)

    change_events = change_event_service.list_all_change_events_of_site(
        id, pageForm.page.data
    )

    return render_template(
        "historic_sites/show.html",
        historic_site=historic_site,
        change_events=change_events,
    )
