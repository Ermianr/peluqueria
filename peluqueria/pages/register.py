import reflex as rx

from peluqueria.components.footer import footer
from peluqueria.components.navbar import navbar
from peluqueria.components.route_guard import anonymous_only_guard
from peluqueria.state.global_state import AuthState
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
    on_load=AuthState.check_auth_protect_login,
)
def register() -> rx.Component:
    content = rx.vstack(
        lang(),
        navbar(),
        rx.box(register_form(), width="100%"),
        footer(),
        spacing="0",
        align="center",
    )
    return anonymous_only_guard(content)
