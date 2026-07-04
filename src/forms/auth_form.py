from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField(
        label="Email:",
        validators=[
            DataRequired("El campo email es obligatorio."),
            Email("El formato de Email debe ser válido."),
        ],
    )
    password = PasswordField(
        label="Contraseña:", validators=[DataRequired("El campo email es obligatorio.")]
    )
    remember_me = BooleanField(label="Recordarme")
