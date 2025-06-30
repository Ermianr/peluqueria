import reflex as rx

from peluqueria.api.main import fastapi_app, lifespan
from peluqueria.pages.appointments import appointments
from peluqueria.pages.appointments_dashboard import appointments_dashboard
from peluqueria.pages.dashboard import main_dashboard
from peluqueria.pages.index import index
from peluqueria.pages.login import login
from peluqueria.pages.register import register
from peluqueria.styles.styles import BASE
from peluqueria.views.dashboard import (
    employees_manage,
    services_manage,
    users_manage,
)

app: rx.App = rx.App(
    theme=rx.theme(
        appearance="light",
    ),
    style=BASE,  # type: ignore
    stylesheets=["/css/normalize.css"],
    api_transformer=fastapi_app,
)

app.register_lifespan_task(lifespan)
