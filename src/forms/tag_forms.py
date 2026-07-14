from flask_wtf import FlaskForm
from wtforms import StringField, SelectField


class TagFilterForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Nombre")
    sort_by = SelectField(
        "Ordenar por",
        choices=[
            ("created_at_desc", "Más recientes"),
            ("created_at_asc", "Más antiguos"),
            ("name_asc", "A-Z"),
            ("name_desc", "Z-A"),
        ],
        default="name_asc",
    )
