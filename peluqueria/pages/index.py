import reflex as rx

from peluqueria.components.footer import footer
from peluqueria.components.navbar import navbar
from peluqueria.state.global_state import AuthState
from peluqueria.utils import lang
from peluqueria.views.home.about.about import about
from peluqueria.views.home.contact.contact import contact
from peluqueria.views.home.hero.hero import hero
from peluqueria.views.home.services.services import services


@rx.page(
    route="/",
    title="Inicio | Peluquería",
    description="Reserva tu cita en nuestra peluquería y luce el estilo que mereces. Cortes, color y más, con atención personalizada.",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
    on_load=AuthState.home_state,
)
def index() -> rx.Component:
    return rx.vstack(
        lang(),
        navbar(),
        hero(),
        rx.vstack(
            services(),
            about(),
            contact(),
            max_width="85%",
            margin_y="2rem",
            spacing="8",
        ),
        footer(),
        spacing="0",
        align="center",
    )
