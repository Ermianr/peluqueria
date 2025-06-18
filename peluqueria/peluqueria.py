import reflex as rx

from peluqueria.api.main import fastapi_app
from peluqueria.pages.appointments import appointments
from peluqueria.pages.dashboard import users_manage
from peluqueria.pages.index import index
from peluqueria.pages.login import login
from peluqueria.pages.register import register
from peluqueria.styles.styles import BASE

app: rx.App = rx.App(
    theme=rx.theme(
        appearance="light",
    ),
    style=BASE,  # type: ignore
    stylesheets=["/css/normalize.css"],
    api_transformer=fastapi_app,
)
