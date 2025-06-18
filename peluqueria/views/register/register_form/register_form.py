import re

import httpx
import reflex as rx

from peluqueria.components.form_field_password import form_field_password
from peluqueria.components.form_field_state import form_field_state
from peluqueria.constants import EMAIL_REGEX, PHONE_REGEX
from peluqueria.settings import Settings
from peluqueria.styles.styles import SOLID_BUTTON, Colors


class RegisterState(rx.State):
    loading: bool = False

    initial_first_name_error_state: str = "none"

    initial_last_name_error_state: str = "none"

    initial_email_error_state: str = "none"

    initial_phone_error_state: str = "none"

    initial_password_error_state: str = "none"

    @rx.event
    async def handle_submit(self, form_data: dict):
        self.loading = True
        valid_first_name: bool = False
        valid_last_name: bool = False
        valid_email: bool = False
        valid_phone: bool = False
        valid_password: bool = False

        if len(form_data.get("first_name") or "") >= 3:
            valid_first_name = True
            self.initial_first_name_error_state = "none"
        else:
            valid_first_name = False
            self.initial_first_name_error_state = "block"

        if len(form_data.get("last_name") or "") >= 3:
            valid_last_name = True
            self.initial_last_name_error_state = "none"
        else:
            valid_last_name = False
            self.initial_last_name_error_state = "block"

        if re.match(EMAIL_REGEX, form_data.get("email") or ""):
            valid_email = True
            self.initial_email_error_state = "none"
        else:
            valid_email = False
            self.initial_email_error_state = "block"

        if re.match(PHONE_REGEX, form_data.get("phone") or ""):
            valid_phone = True
            self.initial_phone_error_state = "none"
        else:
            valid_phone = False
            self.initial_phone_error_state = "block"

        if len(form_data.get("password") or "") >= 8:
            valid_password = True
            self.initial_password_error_state = "none"
        else:
            valid_password = False
            self.initial_password_error_state = "block"

        if (
            valid_first_name
            and valid_last_name
            and valid_email
            and valid_phone
            and valid_password
        ):
            form_data["first_name"] = form_data["first_name"].capitalize()
            form_data["last_name"] = form_data["last_name"].capitalize()
            try:
                async with httpx.AsyncClient(
                    base_url=Settings.API_BACKEND_URL
                ) as client:
                    response = await client.post(
                        "/users",
                        json=form_data,
                        timeout=10.0,
                    )

                if response.status_code == 201:
                    yield rx.toast.success("Usuario creado exitosamente.")
                    yield rx.redirect("/ingreso")
                    self.loading = False
                elif response.status_code == 409:
                    yield rx.toast.error("Error: Este usuario ya existe.")
                    self.loading = False
            except httpx.RequestError as e:
                print(f"Error: Error de conexión: {e}")
                self.loading = False
            except Exception:
                yield rx.toast.error("Error: Error inesperado")
        else:
            yield rx.toast.error(
                "Error: Por favor verifique los datos e inténtalo nuevamente."
            )
            self.loading = False


def register_form() -> rx.Component:
    return rx.center(
        rx.vstack(
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
                        "Mínimo 3 caracteres.",
                    ),
                    form_field_state(
                        "Apellido",
                        "Apellido",
                        "text",
                        "last_name",
                        RegisterState.initial_last_name_error_state,
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
                        "Por favor, ingresa un número de teléfono Colombiano valido.",
                    ),
                    margin_bottom="0.5rem",
                ),
                rx.box(
                    form_field_password(
                        rx.text(
                            "Contraseña ",
                            rx.text(
                                "(Mínimo 8 caracteres)",
                                color=Colors.PARAGRAPH_COLOR.value,
                                as_="span",
                            ),
                        ),
                        "Contraseña",
                        "password",
                        "password",
                        RegisterState.initial_password_error_state,
                        "Por favor ingrese una contraseña de mínimo 8 caracteres.",
                    ),
                    margin_bottom="1rem",
                ),
                rx.separator(margin_bottom="1rem"),
                rx.text(
                    "¿Ya tienes una cuenta? ",
                    rx.link(
                        "Ingresa desde aquí",
                        href="/ingreso",
                        color=Colors.PRIMARY_COLOR.value,
                    ),
                    margin_bottom="1rem",
                    size="2",
                ),
                rx.button(
                    rx.cond(RegisterState.loading, rx.spinner(size="2"), "Registrarse"),
                    type="submit",
                    style=SOLID_BUTTON,
                    padding_y="1.2rem",
                    disabled=RegisterState.loading,
                ),
                on_submit=RegisterState.handle_submit,
                reset_on_submit=True,
            ),
            width=rx.breakpoints(initial="80%", md="40%"),
        ),
        margin_y="2rem",
        min_height="60vh",
        width="100%",
    )
