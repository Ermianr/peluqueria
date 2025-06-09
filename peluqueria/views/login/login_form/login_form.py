import re

import reflex as rx

from peluqueria.components.form_field_password import form_field_password
from peluqueria.components.form_field_state import form_field_state
from peluqueria.constants import EMAIL_REGEX
from peluqueria.styles.styles import SOLID_BUTTON, Colors


class LoginState(rx.State):
    form_data: dict = {}

    initial_email_error_state: str = "none"
    email_value: str = ""

    initial_password_error_state: str = "none"
    password_value = ""

    @rx.event
    def email_validation(self) -> None:
        if len(self.email_value) == 0:
            self.initial_email_error_state = "block"
        elif re.match(EMAIL_REGEX, self.email_value):
            self.initial_email_error_state = "none"
        else:
            self.initial_email_error_state = "block"

    @rx.event
    def password_validation(self, value: str) -> None:
        self.password_value = value
        if len(self.password_value) >= 8:
            self.initial_password_error_state: str = "none"
        else:
            self.initial_password_error_state: str = "block"

    @rx.event
    async def handle_submit(self, form_data: dict):
        pass


def login_form() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.heading("Iniciar Sesión", as_="h1"),
            rx.text(
                "Iniciar sesión para gestionar tus citas",
                color=Colors.PARAGRAPH_COLOR.value,
            ),
        ),
        rx.separator(),
        rx.form(
            rx.box(
                form_field_state(
                    "Correo Electrónico",
                    "Correo Electrónico",
                    "email",
                    "email",
                    LoginState.initial_email_error_state,
                    LoginState.email_value,
                    LoginState.set_email_value,  # type: ignore
                    LoginState.email_validation,
                    "Por favor, ingresa un correo electrónico valido.",
                ),
                margin_bottom="0.5rem",
            ),
            rx.box(
                form_field_password(
                    "Contrasñea",
                    "Contraseña",
                    "password",
                    "password",
                    LoginState.initial_email_error_state,
                    LoginState.password_value,
                    LoginState.password_validation,
                    "Por favor ingrese una contraseña de mínimo 8 caracteres.",
                )
            ),
            rx.separator(margin_bottom="1rem"),
            rx.button(
                "Registrarse",
                type="submit",
                style=SOLID_BUTTON,
                padding_y="1.2rem",
            ),
            on_submit=LoginState.handle_submit,
            width="100%",
        ),
        width="40%",
        margin_top="2rem",
    )
