from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length, Regexp


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


class TagCreateForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El campo nombre es obligatorio."),
            Length(min=2, max=40, message="Debe tener entre 2 y 40 caracteres."),
            Regexp(
                r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ ]+$",
                message="El campo nombre solo puede contener letras, números y espacios.",
            ),
        ],
    )
