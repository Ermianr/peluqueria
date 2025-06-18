import re

import reflex as rx

from peluqueria.components.form_field_password import form_field_password
from peluqueria.components.form_field_state import form_field_state
from peluqueria.constants import EMAIL_REGEX
from peluqueria.state.global_state import AuthState
from peluqueria.styles.styles import SOLID_BUTTON, Colors


class LoginState(rx.State):
    form_data: dict = {}

    initial_email_error_state: str = "none"

    initial_password_error_state: str = "none"

    @rx.event
    async def handle_submit(self, form_data: dict):
        valid_email = False
        valid_password = False

        if re.match(EMAIL_REGEX, form_data.get("email") or ""):
            valid_email = True
            self.initial_email_error_state = "none"
        else:
            valid_email = False
            self.initial_email_error_state = "block"

        if len(form_data.get("password") or "") >= 8:
            valid_password = True
            self.initial_password_error_state = "none"
        else:
            valid_password = False
            self.initial_password_error_state = "block"

        if valid_email and valid_password:
            auth_state = await self.get_state(AuthState)
            async for action in auth_state.login(
                form_data["email"], form_data["password"]
            ):
                yield action


def login_form() -> rx.Component:
    return rx.center(
        rx.vstack(
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
                        "Por favor, ingresa un correo electrónico valido.",
                    ),
                    margin_bottom="0.5rem",
                ),
                rx.box(
                    form_field_password(
                        "Contraseña",
                        "Contraseña",
                        "password",
                        "password",
                        LoginState.initial_password_error_state,
                        "Por favor ingrese una contraseña de mínimo 8 caracteres.",
                    ),
                    margin_bottom="1rem",
                ),
                rx.separator(margin_bottom="1rem"),
                rx.text(
                    "¿No tienes una cuenta? ",
                    rx.link(
                        "Regístrate desde aquí",
                        href="/registro",
                        color=Colors.PRIMARY_COLOR.value,
                    ),
                    margin_bottom="1rem",
                    size="2",
                ),
                rx.button(
                    rx.cond(AuthState.loading, rx.spinner(size="2"), "Iniciar Sesión"),
                    type="submit",
                    style=SOLID_BUTTON,
                    padding_y="1.2rem",
                    disabled=AuthState.loading,
                ),
                on_submit=LoginState.handle_submit,
            ),
            width=rx.breakpoints(initial="80%", md="40%"),
        ),
        margin_y="2rem",
        min_height="60vh",
        width="100%",
    )
