import reflex as rx

from peluqueria.components.footer import footer
from peluqueria.components.navbar import navbar
from peluqueria.utils import lang
from peluqueria.views.register.register_form.register_form import register_form


@rx.page(
    route="/registro",
    title="Registrarse | Peluquería",
    description="Crea tu cuenta y agenda tus citas de peluquería en segundos. ¡Fácil, rápido y sin complicaciones!",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
)
def register() -> rx.Component:
    return rx.vstack(
        lang(),
        navbar(),
        rx.box(register_form(), width="100%"),
        footer(),
        spacing="0",
        align="center",
    )
