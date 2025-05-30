import reflex as rx

from peluqueria.styles.styles import BASE
from peluqueria.pages.index import index
from peluqueria.pages.register import register

app: rx.App = rx.App(
    theme=rx.theme(
        appearance="light",
    ),
    style=BASE, # type: ignore
    stylesheets=["/css/normalize.css"]
)