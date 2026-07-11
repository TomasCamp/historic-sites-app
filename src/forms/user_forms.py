from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, EmailField, PasswordField
from src.services import user_service
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


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
        super().__init__(*args, **kwargs)

        roles = user_service.list_all_roles()

        self.role_id.choices = [("", "Todos")] + [
            (str(role.id), role.name) for role in roles
        ]


class UserCreateForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired("El campo nombre es obligatorio."),
            Length(3, 60, "El campo nombre debe tener entre 3 y 60 caracteres."),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            DataRequired("El campo apellido es obligatorio."),
            Length(3, 60, "El campo apellido debe tener entre 3 y 60 caracteres."),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("El campo email es obligatorio."),
            Length(3, 120, "El campo email debe tener entre 3 y 120 caracteres."),
            Email("El formato del campo email debe ser válido."),
        ],
    )
    role_id = SelectField(
        "Rol", validators=[DataRequired("Debe seleccionar un rol para el usuario.")]
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired("El campo contraseña es obligatorio."),
            Length(6, 64, "El campo contraseña debe tener entre 6 y 64 caracteres."),
            Regexp(
                r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).*$",
                message="El campo contraseña debe tener al menos una mayúscula, una minúscula y un número.",
            ),
        ],
    )
    password_confirm = PasswordField(
        "Repetir Contraseña",
        validators=[
            DataRequired("El campo repetir contraseña es obligatorio."),
            EqualTo("password", "Las contraseñas no coinciden."),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        roles = user_service.list_all_roles()

        self.role_id.choices = [("", "Seleccione un rol...")] + [
            (str(role.id), role.name) for role in roles
        ]


class UserUpdateForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired("El campo nombre es obligatorio."),
            Length(3, 60, "El campo nombre debe tener entre 3 y 60 caracteres."),
            Regexp(
                r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$",
                message="El campo nombre solo puede contener letras y espacios.",
            ),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            DataRequired("El campo apellido es obligatorio."),
            Length(3, 60, "El campo apellido debe tener entre 3 y 60 caracteres."),
            Regexp(
                r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$",
                message="El campo apellido solo puede contener letras y espacios.",
            ),
        ],
    )
    role_id = SelectField(
        "Rol", validators=[DataRequired("Debe seleccionar un rol para el usuario.")]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        roles = user_service.list_all_roles()

        self.role_id.choices = [("", "Seleccione un rol...")] + [
            (str(role.id), role.name) for role in roles
        ]
