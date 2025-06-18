import reflex as rx

from peluqueria.components.footer import footer
from peluqueria.components.navbar import navbar
from peluqueria.utils import lang
from peluqueria.views.appointments.appointment_dashboard.appointment_dashboard import (
    appointment_dashboard,
)


@rx.page(
    route="/citas",
    title="Citas | Peluquería",
    description="Reserva tu cita en nuestra peluquería y luce el estilo que mereces. Cortes, color y más, con atención personalizada.",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
)
def appointments() -> rx.Component:
    return rx.vstack(
        lang(),
        navbar(),
        rx.box(
            appointment_dashboard(),
            width="100%",
        ),
        footer(),
        spacing="0",
        align="center",
    )
