from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from src.services import user_service


class UserFilterForm(FlaskForm):
    email = StringField("Email")
    active = SelectField(
        "Estado", choices=[("", "Todos"), ("1", "Activo"), ("0", "Suspendido")]
    )
    role_id = SelectField("Rol")
    sort_by = SelectField(
        "Ordenar por",
        choices=[
            ("created_at_desc", "Más recientes"),
            ("created_at_asc", "Más antiguos"),
        ],
        default="created_at_desc",
    )

    def __init__(self, *args, **kwargs):
        kwargs["meta"] = {"csrf": False}
        super(UserFilterForm, self).__init__(*args, **kwargs)

        roles = user_service.list_all_roles()

        self.role_id.choices = [("", "Todos")] + [
            (str(role.id), role.name) for role in roles
        ]
