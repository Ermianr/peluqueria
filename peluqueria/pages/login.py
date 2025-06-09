import reflex as rx

from peluqueria.components.footer import footer
from peluqueria.components.navbar import navbar
from peluqueria.utils import lang
from peluqueria.views.login.login_form.login_form import login_form


@rx.page(
    route="/ingreso",
    title="Iniciar Sesión | Peluquería",
    description="Inicia sesión en tu cuenta y gestiona tus citas de peluquería fácilmente. ¡Acceso rápido y seguro!",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
)
def register() -> rx.Component:
    return rx.vstack(
        lang(), navbar(), login_form(), footer(), spacing="0", align="center"
    )
