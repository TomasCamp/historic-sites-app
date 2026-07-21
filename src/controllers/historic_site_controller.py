from flask import Blueprint, render_template, request
from flask_login import login_required
from src.controllers.decorators import permission_required
from src.services import historic_site_service
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
