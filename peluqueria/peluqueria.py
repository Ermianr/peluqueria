import reflex as rx

from peluqueria.components.navbar import navbar
from peluqueria.styles.styles import BASE
from peluqueria.views.about.about import about
from peluqueria.views.hero.hero import hero
from peluqueria.views.services.services import services
from peluqueria.views.contact.contact import contact


def index() -> rx.Component:
    return rx.vstack(
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
        spacing="0",
        align="center"
    )


app: rx.App = rx.App(
    theme=rx.theme(
        appearance="light",
    ),
    style=BASE, # type: ignore
    stylesheets=["/css/normalize.css"]
)
app.add_page(index)
