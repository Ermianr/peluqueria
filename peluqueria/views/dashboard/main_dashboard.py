from datetime import datetime, timezone
from typing import TypedDict

import httpx
import reflex as rx

from peluqueria.components.route_guard import employee_only_guard
from peluqueria.settings import Settings
from peluqueria.views.dashboard.components.charts import dashboard_charts
from peluqueria.views.dashboard.sidebar.sidebar import sidebar

HTTP_OK = 200


class DashboardMetrics(TypedDict):
    total_appointments: int
    total_users: int
    total_employees: int
    most_used_service: str
    appointments_today: int
    active_users: int


class MainDashboardState(rx.State):
    total_appointments: int = 0
    total_users: int = 0
    total_employees: int = 0
    most_used_service: str = "N/A"
    appointments_today: int = 0
    active_users: int = 0
    is_loading: bool = False

    @rx.event
    async def load_dashboard_metrics(self):
        self.is_loading = True
        try:
            async with httpx.AsyncClient(
                base_url=Settings.API_BACKEND_URL,
            ) as client:
                appointments_response = await client.get("/appointments")
                users_response = await client.get("/users")
                employees_response = await client.get("/employees")

                responses = [
                    appointments_response,
                    users_response,
                    employees_response,
                ]
                if all(r.status_code == HTTP_OK for r in responses):
                    appointments = appointments_response.json()
                    users = users_response.json()
                    employees = employees_response.json()

                    active_users = len([u for u in users if u.get("is_active", False)])

                    service_usage = {}
                    for appointment in appointments:
                        service_name = appointment.get("service_name", "Unknown")
                        current_count = service_usage.get(service_name, 0)
                        service_usage[service_name] = current_count + 1

                    most_used_service = "N/A"
                    if service_usage:
                        most_used_service = max(
                            service_usage,
                            key=lambda x: service_usage[x],
                        )

                    today = datetime.now(tz=timezone.utc).date().isoformat()
                    appointments_today = len(
                        [a for a in appointments if a.get("date", "").startswith(today)]
                    )

                    self.total_appointments = len(appointments)
                    self.total_users = len(users)
                    self.total_employees = len(employees)
                    self.most_used_service = most_used_service
                    self.appointments_today = appointments_today
                    self.active_users = active_users
                    yield rx.toast.success("Métricas cargadas correctamente")
                else:
                    yield rx.toast.error("Error al cargar algunas métricas")
        except httpx.RequestError:
            yield rx.toast.error("Error de conexión al servidor")
        except Exception as e:
            yield rx.toast.error(f"Error inesperado: {e!s}")
        finally:
            self.is_loading = False


def metric_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.box(
                rx.icon(icon, size=24, color=color),
                padding="0.75rem",
                background=f"var(--{color}-3)",
                border_radius="0.5rem",
            ),
            rx.flex(
                rx.text(title, size="2", color="gray"),
                rx.text(value, size="6", weight="bold"),
                direction="column",
                justify="center",
                spacing="1",
            ),
            align="center",
            spacing="3",
        ),
        padding="1.5rem",
        background="white",
        border="1px solid var(--gray-6)",
        border_radius="0.75rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        _hover={"box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)"},
        transition="all 0.2s ease",
    )


def metrics_grid() -> rx.Component:
    return rx.grid(
        metric_card(
            "Total de Citas",
            MainDashboardState.total_appointments.to_string(),  # type: ignore
            "calendar",
            "blue",
        ),
        metric_card(
            "Citas Hoy",
            MainDashboardState.appointments_today.to_string(),  # type: ignore
            "calendar-check",
            "green",
        ),
        metric_card(
            "Total Usuarios",
            MainDashboardState.total_users.to_string(),  # type: ignore
            "users",
            "purple",
        ),
        metric_card(
            "Usuarios Activos",
            MainDashboardState.active_users.to_string(),  # type: ignore
            "user-check",
            "cyan",
        ),
        metric_card(
            "Total Empleados",
            MainDashboardState.total_employees.to_string(),  # type: ignore
            "user-cog",
            "orange",
        ),
        metric_card(
            "Servicio Más Usado",
            MainDashboardState.most_used_service,
            "star",
            "yellow",
        ),
        columns="3",
        spacing="4",
        width="100%",
    )


def quick_actions() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.heading("Acciones Rápidas", size="5", margin_bottom="1rem"),
            rx.flex(
                rx.link(
                    rx.button(
                        rx.icon("plus", size=16),
                        "Nueva Cita",
                        color_scheme="blue",
                        size="3",
                    ),
                    href="/appointments",
                ),
                rx.link(
                    rx.button(
                        rx.icon("users", size=16),
                        "Ver Usuarios",
                        color_scheme="purple",
                        size="3",
                        variant="outline",
                    ),
                    href="/dashboard",
                ),
                rx.link(
                    rx.button(
                        rx.icon("settings", size=16),
                        "Servicios",
                        color_scheme="green",
                        size="3",
                        variant="outline",
                    ),
                    href="/dashboard/services",
                ),
                spacing="3",
                wrap="wrap",
            ),
            direction="column",
        ),
        padding="2rem",
        background="white",
        border="1px solid var(--gray-6)",
        border_radius="0.75rem",
    )


def recent_activity() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.heading("Actividad Reciente", size="5", margin_bottom="1rem"),
            rx.cond(
                MainDashboardState.is_loading,
                rx.flex(
                    rx.spinner(size="3"),
                    rx.text("Cargando actividad..."),
                    align="center",
                    spacing="2",
                ),
                rx.text(
                    "Próximamente: Historial de actividades recientes",
                    color="gray",
                    size="3",
                ),
            ),
            direction="column",
        ),
        padding="2rem",
        background="white",
        border="1px solid var(--gray-6)",
        border_radius="0.75rem",
    )


def dashboard_content() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.flex(
                rx.heading("Dashboard Principal", size="7", weight="bold"),
                rx.button(
                    rx.cond(
                        MainDashboardState.is_loading,
                        rx.spinner(size="3"),
                        rx.icon("refresh-cw", size=16),
                    ),
                    "Actualizar",
                    on_click=MainDashboardState.load_dashboard_metrics,
                    disabled=MainDashboardState.is_loading,
                    color_scheme="gray",
                    variant="outline",
                    size="3",
                ),
                justify="between",
                align="center",
                margin_bottom="2rem",
            ),
            padding="2rem",
        ),
        metrics_grid(),
        rx.grid(
            quick_actions(),
            recent_activity(),
            columns="2",
            spacing="4",
            margin_top="2rem",
        ),
        dashboard_charts(),
        direction="column",
        width="100%",
        padding_x="2rem",
        padding_y="1rem",
        spacing="3",
        margin_left="16em",
    )


@rx.page(
    route="/dashboard/main",
    title="Dashboard Principal | Peluquería",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
    on_load=MainDashboardState.load_dashboard_metrics,
)
def main_dashboard() -> rx.Component:
    content = rx.hstack(sidebar(), dashboard_content())
    return employee_only_guard(content)
