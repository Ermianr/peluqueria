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
    email_value: str = ""

    initial_password_error_state: str = "none"
    password_value: str = ""

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
            self.initial_password_error_state = "none"
        else:
            self.initial_password_error_state = "block"

    @rx.event
    async def handle_submit(self, form_data: dict):
        self.email_value = ""
        self.password_value = ""

        if (
            re.match(EMAIL_REGEX, form_data.get("email") or "")
            and len(form_data.get("password") or "") >= 8
        ):
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
                        LoginState.email_value,
                        LoginState.set_email_value,  # type: ignore
                        LoginState.email_validation,
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
                        LoginState.password_value,
                        LoginState.password_validation,
                        "Por favor ingrese una contraseña de mínimo 8 caracteres.",
                    ),
                    margin_bottom="1rem",
                ),
                rx.separator(margin_bottom="1rem"),
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
        height="60vh",
        width="100%",
    )
