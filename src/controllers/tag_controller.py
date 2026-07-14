from flask import Blueprint, render_template, request
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
