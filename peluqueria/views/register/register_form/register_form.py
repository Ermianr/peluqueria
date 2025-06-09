import re

import httpx
import reflex as rx

from peluqueria.components.form_field_password import form_field_password
from peluqueria.components.form_field_state import form_field_state
from peluqueria.constants import EMAIL_REGEX, PHONE_REGEX
from peluqueria.styles.styles import SOLID_BUTTON, Colors


class RegisterState(rx.State):
    form_data: dict = {}

    initial_first_name_error_state: str = "none"
    first_name_value = ""

    initial_last_name_error_state: str = "none"
    last_name_value = ""

    initial_email_error_state: str = "none"
    email_value: str = ""

    initial_phone_error_state: str = "none"
    phone_value: str = ""

    initial_password_error_state: str = "none"
    password_value = ""

    @rx.event
    def first_name_validation(self) -> None:
        if len(self.first_name_value) > 2:
            self.initial_first_name_error_state: str = "none"
        else:
            self.initial_first_name_error_state: str = "block"

    @rx.event
    def last_name_validation(self) -> None:
        if len(self.last_name_value) > 2:
            self.initial_last_name_error_state: str = "none"
        else:
            self.initial_last_name_error_state: str = "block"

    @rx.event
    def email_validation(self) -> None:
        if len(self.email_value) == 0:
            self.initial_email_error_state = "block"
        elif re.match(EMAIL_REGEX, self.email_value):
            self.initial_email_error_state = "none"
        else:
            self.initial_email_error_state = "block"

    @rx.event
    def phone_validation(self) -> None:
        if len(self.phone_value) == 0:
            self.initial_phone_error_state = "block"
        elif re.match(PHONE_REGEX, self.phone_value):
            self.initial_phone_error_state = "none"
        else:
            self.initial_phone_error_state = "block"

    @rx.event
    def password_validation(self, value: str) -> None:
        self.password_value = value
        if len(self.password_value) >= 8:
            self.initial_password_error_state: str = "none"
        else:
            self.initial_password_error_state: str = "block"

    @rx.event
    async def handle_submit(self, form_data: dict):
        self.first_name_value = ""
        self.last_name_value = ""
        self.email_value = ""
        self.phone_value = ""
        self.password_value = ""
        print(self.form_data)
        if (
            re.match(EMAIL_REGEX, form_data.get("phone") or "")
            and re.match(PHONE_REGEX, form_data.get("email") or "")
            and len(form_data.get("first_name") or "") >= 3
            and len(form_data.get("last_name") or "") >= 3
            and len(form_data.get("password") or "") >= 8
        ):
            self.form_data = form_data
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "http://localhost:8000/users/",
                        json=self.form_data,
                        timeout=10.0,
                    )

                if response.status_code == 201:
                    print("Usuario creado correctamente")
                    yield rx.toast.success("Usuario creado exitosamente.")
                else:
                    print(f"Error: {response.status_code}")
            except httpx.RequestError as e:
                print(f"Error de conexión: {e}")
        else:
            yield rx.toast.error(
                "Por favor verifique los datos e inténtalo nuevamente."
            )


def register_form() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.heading("Crear nueva cuenta", as_="h1"),
            rx.text(
                "Crea una cuenta y comienza a agendar tus citas",
                color=Colors.PARAGRAPH_COLOR.value,
            ),
        ),
        rx.separator(),
        rx.form(
            rx.flex(
                form_field_state(
                    "Nombre",
                    "Nombre",
                    "text",
                    "first_name",
                    RegisterState.initial_first_name_error_state,
                    RegisterState.first_name_value,
                    RegisterState.set_first_name_value,  # type: ignore
                    RegisterState.first_name_validation,
                    "Mínimo 3 caracteres.",
                ),
                form_field_state(
                    "Apellido",
                    "Apellido",
                    "text",
                    "last_name",
                    RegisterState.initial_last_name_error_state,
                    RegisterState.last_name_value,
                    RegisterState.set_last_name_value,  # type: ignore
                    RegisterState.last_name_validation,
                    "Mínimo 3 caracteres.",
                ),
                direction=rx.breakpoints(
                    initial="column",
                    md="row",
                ),
                spacing="3",
                margin_bottom="0.5rem",
            ),
            rx.box(
                form_field_state(
                    "Correo electrónico",
                    "Tu correo",
                    "email",
                    "email",
                    RegisterState.initial_email_error_state,
                    RegisterState.email_value,
                    RegisterState.set_email_value,  # type: ignore
                    RegisterState.email_validation,
                    "Por favor, ingresa un correo electrónico valido.",
                ),
                margin_bottom="0.5rem",
            ),
            rx.box(
                form_field_state(
                    "Número de Teléfono",
                    "Número de Teléfono",
                    "tel",
                    "phone",
                    RegisterState.initial_phone_error_state,
                    RegisterState.phone_value,
                    RegisterState.set_phone_value,  # type: ignore
                    RegisterState.phone_validation,
                    "Por favor, ingresa un número de teléfono Colombiano valido.",
                ),
                margin_bottom="0.5rem",
            ),
            rx.box(
                form_field_password(
                    "Contraseña",
                    "Contraseña",
                    "password",
                    "password",
                    RegisterState.initial_password_error_state,
                    RegisterState.password_value,
                    RegisterState.password_validation,
                    "Por favor ingrese una contraseña de mínimo 8 caracteres.",
                ),
                margin_bottom="0.5rem",
            ),
            rx.separator(margin_bottom="1rem"),
            rx.button(
                "Registrarse",
                type="submit",
                style=SOLID_BUTTON,
                padding_y="1.2rem",
            ),
            on_submit=RegisterState.handle_submit,
            width="100%",
        ),
        width="40%",
        margin_top="2rem",
    )
