import reflex as rx

from peluqueria.components.navbar import navbar
from peluqueria.views.about.about import about
from peluqueria.views.hero.hero import hero
from peluqueria.views.services.services import services
from peluqueria.views.contact.contact import contact
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
        hero(),
        rx.vstack(
            services(),
            about(),
            contact(),
            max_width="85%",
            margin_top="2rem",
            spacing="8",
        ),
        footer(),
        spacing="0",
        align="center"
    )