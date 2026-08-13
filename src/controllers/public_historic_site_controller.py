from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.services import (
    historic_site_service,
    change_event_service,
)
from src.forms import historic_site_forms

bp = Blueprint("historic_sites", __name__, url_prefix="/historic_sites")


@bp.get("/")
def index():
    """Muestra el listado de historic_sites."""
    form = historic_site_forms.PublicHistoricSiteFilterForm(request.args)

    filters = {}
    if form.validate():
        filters = form.data

    historic_sites = historic_site_service.list_filtered_historic_sites(**filters)

    return render_template(
        "public/historic_sites/index.html", historic_sites=historic_sites, form=form
    )


@bp.get("/<int:id>")
def show(id: int):
    """Muestra todos los datos de un historic_site."""
    historic_site = historic_site_service.get_historic_site_by_id(id)
    if not historic_site:
        flash("El sitio historico buscado no existe.", "danger")
        return redirect(url_for("admin_historic_sites.index"))

    pageForm = historic_site_forms.ChangeEventPageForm(request.args)

    change_events = change_event_service.list_all_change_events_of_site(
        id, pageForm.page.data
    )

    return render_template(
        "public/historic_sites/show.html",
        historic_site=historic_site,
        change_events=change_events,
    )
