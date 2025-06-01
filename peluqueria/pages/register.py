import reflex as rx

from peluqueria.components.navbar import navbar
from peluqueria.views.register.register_form.register_form import register_form
from peluqueria.components.footer import footer
from peluqueria.utils import lang

@rx.page(
        route="/registro",
        title="Registrarse | Peluquería",
        description="Crea tu cuenta y agenda tus citas de peluquería en segundos. ¡Fácil, rápido y sin complicaciones!",
        meta= [
            {"char_set": "UTF-8"},
        ]
)
def register() -> rx.Component:
    return rx.vstack(
        lang(),
        navbar(),
        register_form(),
        footer(),
        spacing="0",
        align="center"
    )