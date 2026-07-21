from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateField
from wtforms.validators import Optional
from wtforms.widgets import ListWidget, CheckboxInput
from src.models.historic_site.enum import Province
from src.services.tag_service import list_all_tags
from src.services.historic_site_service import list_all_conservation_statuses


class HistoricSiteFilterForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Nombre", validators=[Optional()])
    city = StringField("Ciudad", validators=[Optional()])
    province = SelectField(
        "Provincia", choices=[("", "Todas")] + [(p.value, p.value) for p in Province]
    )
    tags = SelectMultipleField(
        "Etiquetas",
        coerce=int,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    conservation_status_id = SelectField("Estado de Conservación", coerce=int)
    registered_at_start = DateField("Registrado Desde", validators=[Optional()])
    registered_at_end = DateField("Registrado Hasta", validators=[Optional()])
    is_visible = SelectField(
        "Estado de Visibilidad",
        choices=[("", "Todos"), ("1", "Visible"), ("0", "Oculto")],
        default="",
    )

    sort_by = SelectField(
        "Ordenar por",
        choices=[
            ("registered_desc", "Más recientes"),
            ("registered_asc", "Más antiguos"),
            ("name_asc", "Nombre A-Z"),
            ("name_desc", "Nombre Z-A"),
            ("city_asc", "Ciudad A-Z"),
            ("city_desc", "Ciudad Z-A"),
        ],
        default="name_asc",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tags.choices = [(t.id, t.name) for t in list_all_tags()]
        self.conservation_status_id.choices = [(0, "Todos")] + [
            (c_s.id, c_s.name) for c_s in list_all_conservation_statuses()
        ]
        self.conservation_status_id.default = 0
