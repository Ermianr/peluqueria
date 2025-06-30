import reflex as rx

from peluqueria.components.route_guard import employee_only_guard
from peluqueria.views.dashboard.appointments_manager.appointments_manager import (
    appointments_manager,
)
from peluqueria.views.dashboard.sidebar.sidebar import sidebar


@rx.page(
    route="/dashboard/appointments",
    title="Gestión de Citas | Dashboard",
    description="Administra las citas de los clientes.",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
)
def appointments_dashboard() -> rx.Component:
    content = rx.hstack(
        sidebar(),
        appointments_manager(),
        width="100%",
        min_height="100vh",
        spacing="0",
    )
    return employee_only_guard(content)
