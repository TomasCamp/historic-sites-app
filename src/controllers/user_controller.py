from flask import Blueprint, render_template, request
from flask_login import login_required
from src.controllers.decorators import permission_required
from src.services import user_service
from src.forms import user_forms

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("/")
@login_required
@permission_required("user_index")
def index():
    form = user_forms.UserFilterForm(request.args)

    filters = {}
    if form.validate():
        filters = form.data
    print(form.errors)

    users = user_service.list_filtered_users(**filters)

    return render_template("users/index.html", users=users, form=form)
