from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateField,
    TextAreaField,
    IntegerField,
    FileField,
    HiddenField,
)
from wtforms.validators import (
    Optional,
    DataRequired,
    Length,
    Regexp,
    NumberRange,
    InputRequired,
)
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.widgets import ListWidget, CheckboxInput
from src.models.historic_site.enum import Province
from src.services.tag_service import list_all_tags
from src.services.historic_site_service import (
    list_all_conservation_statuses,
    list_all_categorys,
)
from datetime import date


class HistoricSiteFilterForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Nombre", validators=[Optional()])
    city = StringField("Ciudad", validators=[Optional()])
    province = SelectField(
        "Provincia",
        choices=[("", "Todas")] + [(p.value, p.value) for p in Province],
        default="",
    )
    tags = SelectMultipleField(
        "Etiquetas",
        coerce=int,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    conservation_status_id = SelectField(
        "Estado de Conservación", coerce=int, choices=[(0, "Todos")], default=0
    )
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
    page = IntegerField(default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tags.choices = [(t.id, t.name) for t in list_all_tags()]
        self.conservation_status_id.choices += [
            (c_s.id, c_s.name) for c_s in list_all_conservation_statuses()
        ]


class PublicHistoricSiteFilterForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Nombre", validators=[Optional()])
    city = StringField("Ciudad", validators=[Optional()])
    province = SelectField(
        "Provincia",
        choices=[("", "Todas")] + [(p.value, p.value) for p in Province],
        default="",
    )
    tags = SelectMultipleField(
        "Etiquetas",
        coerce=int,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    conservation_status_id = SelectField(
        "Estado de Conservación", coerce=int, choices=[(0, "Todos")], default=0
    )

    sort_by = SelectField(
        "Ordenar por",
        choices=[
            ("name_asc", "Nombre A-Z"),
            ("name_desc", "Nombre Z-A"),
            ("city_asc", "Ciudad A-Z"),
            ("city_desc", "Ciudad Z-A"),
        ],
        default="name_asc",
    )
    page = IntegerField(default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tags.choices = [(t.id, t.name) for t in list_all_tags()]
        self.conservation_status_id.choices += [
            (c_s.id, c_s.name) for c_s in list_all_conservation_statuses()
        ]


class HistoricSiteCreateForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired("El campo nombre es obligatorio."),
            Length(3, 100, "El campo nombre debe tener entre 3 y 100 caracteres."),
            Regexp(
                r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\.,;\:\(\)\"\'-]+$",
                message="El campo nombre solo puede contener letras, espacios, números y los siguientes simbolos: .,;:()\"'",
            ),
        ],
    )
    short_description = StringField(
        "Descripción Corta",
        validators=[
            DataRequired("El campo descripción corta es obligatorio."),
            Length(
                3,
                255,
                "El campo descripción corta debe tener entre 3 y 255 caracteres.",
            ),
            Regexp(
                r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\.,;\:\(\)\"\'-]+$",
                message="El campo descripción corta solo puede contener letras, espacios, números y los siguientes simbolos: .,;:()\"'",
            ),
        ],
    )
    full_description = TextAreaField(
        "Descripción Completa",
        validators=[
            DataRequired("El campo descripción completa es obligatorio."),
            Length(
                min=10,
                message="La descripción completa debe tener al menos 10 caracteres.",
            ),
            Regexp(
                r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\.,;\:\(\)\"\'-]+$",
                message="El campo descripción completa solo puede contener letras, espacios, números y los siguientes simbolos: .,;:()\"'",
            ),
        ],
    )
    city = StringField(
        "Ciudad",
        validators=[
            DataRequired("El campo ciudad es obligatorio."),
            Length(2, 60, "La ciudad debe tener entre 2 y 60 caracteres."),
            Regexp(
                r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\'-]+$",
                message="La campo ciudad solo puede contener letras y espacios.",
            ),
        ],
    )
    province = SelectField(
        "Provincia",
        validators=[DataRequired("Debe seleccionar una provincia.")],
        choices=[("", "Seleccione una provincia...")]
        + [(p.value, p.value) for p in Province],
    )
    inauguration_year = IntegerField(
        "Fecha de Inauguración",
        validators=[
            DataRequired("El año de inauguración es obligatorio."),
            NumberRange(
                min=1,
                max=date.today().year,
                message=f"El año debe estar entre 1 y {date.today().year}.",
            ),
        ],
    )
    cover_image = FileField(
        "Imagen de Portada",
        validators=[
            FileRequired("Debe adjuntar una imagen de portada."),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Solo se permiten imágenes (jpg, jpeg, png, webp).",
            ),
        ],
    )
    category_id = SelectField(
        "Categoría",
        coerce=int,
        validators=[
            InputRequired("Debe seleccionar una categoría."),
            NumberRange(min=1, message="Debe seleccionar una categoría."),
        ],
    )
    conservation_status_id = SelectField(
        "Estado de Conservación",
        coerce=int,
        validators=[
            InputRequired("Debe seleccionar un estado de conservación."),
            NumberRange(min=1, message="Debe seleccionar un estado de conservación."),
        ],
    )
    tags = SelectMultipleField(
        "Etiquetas",
        coerce=int,
        validators=[Optional()],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    latitude = HiddenField(
        "Latitud",
        validators=[
            DataRequired("Por favor, seleccione la ubicación en el mapa."),
        ],
    )
    longitude = HiddenField(
        "Longitud",
        validators=[
            DataRequired("Por favor, seleccione la ubicación en el mapa."),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tags.choices = [(t.id, t.name) for t in list_all_tags()]
        self.conservation_status_id.choices = [(0, "Seleccione estado...")] + [
            (c_s.id, c_s.name) for c_s in list_all_conservation_statuses()
        ]
        self.category_id.choices = [(0, "Seleccione categoría...")] + [
            (c.id, c.name) for c in list_all_categorys()
        ]


class HistoricSiteUpdateForm(HistoricSiteCreateForm):
    cover_image = FileField(
        "Imagen de Portada",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Solo se permiten imágenes (jpg, jpeg, png, webp).",
            ),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        obj = kwargs.get("obj")
        if obj and not self.is_submitted():
            self.tags.data = [t.id for t in obj.tags]


class ChangeEventPageForm(FlaskForm):
    class Meta:
        csrf = False

    page = IntegerField(NumberRange(min=1), default=1)
