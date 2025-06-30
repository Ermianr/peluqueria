from typing import TypedDict

import httpx
import reflex as rx

from peluqueria.constants import HTTP_200_OK
from peluqueria.settings import Settings
from peluqueria.state.global_state import AuthState


class AppointmentStats(TypedDict):
    completed: int
    pending: int
    confirmed: int
    cancelled: int


class ChartsState(rx.State):
    completed_appointments: int = 0
    pending_appointments: int = 0
    confirmed_appointments: int = 0
    cancelled_appointments: int = 0
    is_loading: bool = False

    @rx.var
    def total_appointments(self) -> int:
        return (
            self.completed_appointments
            + self.pending_appointments
            + self.confirmed_appointments
            + self.cancelled_appointments
        )

    @rx.event
    async def load_appointment_stats(self):
        self.is_loading = True
        try:
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                return

            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.get(
                    "/appointments",
                    headers={"Authorization": f"Bearer {auth_state.access_token}"},
                )

                if response.status_code == HTTP_200_OK:
                    appointments = response.json()

                    completed = 0
                    pending = 0
                    confirmed = 0
                    cancelled = 0

                    for appointment in appointments:
                        state = appointment.get("state", "").lower()
                        if state == "completed":
                            completed += 1
                        elif state == "pending":
                            pending += 1
                        elif state == "confirmed":
                            confirmed += 1
                        elif state == "cancelled":
                            cancelled += 1

                    self.completed_appointments = completed
                    self.pending_appointments = pending
                    self.confirmed_appointments = confirmed
                    self.cancelled_appointments = cancelled
                else:
                    yield rx.toast.error("Error al cargar estadísticas de citas")
        except Exception:
            yield rx.toast.error("Error de conexión al cargar estadísticas")
        finally:
            self.is_loading = False


def simple_chart_bar(
    title: str,
    value,
    max_value,
    color: str = "blue",
) -> rx.Component:
    return rx.flex(
        rx.text(title, size="2", weight="medium", margin_bottom="0.5rem"),
        rx.flex(
            rx.box(
                width=rx.cond(
                    max_value > 0,
                    ((value * 100) / max_value).to_string() + "%",
                    "0%",
                ),
                height="1.5rem",
                background=f"var(--{color}-9)",
                border_radius="0.25rem",
                transition="width 0.5s ease",
            ),
            width="100%",
            height="1.5rem",
            background=f"var(--{color}-3)",
            border_radius="0.25rem",
            overflow="hidden",
        ),
        rx.flex(
            rx.text(value, size="1", weight="bold"),
            rx.text("de " + max_value.to_string(), size="1", color="gray"),
            justify="between",
            margin_top="0.25rem",
        ),
        direction="column",
        width="100%",
    )


def dashboard_charts() -> rx.Component:
    return rx.cond(
        ChartsState.is_loading,
        rx.center(
            rx.spinner(size="3"),
            padding="2rem",
        ),
        rx.flex(
            rx.card(
                rx.flex(
                    rx.flex(
                        rx.heading("Distribución de Citas", size="4"),
                        rx.button(
                            rx.icon("refresh-cw", size=16),
                            variant="ghost",
                            size="2",
                            on_click=ChartsState.load_appointment_stats,
                            disabled=ChartsState.is_loading,
                        ),
                        justify="between",
                        align="center",
                        margin_bottom="1rem",
                        width="100%",
                    ),
                    rx.cond(
                        ChartsState.total_appointments > 0,
                        rx.flex(
                            simple_chart_bar(
                                "Citas Completadas",
                                ChartsState.completed_appointments,
                                ChartsState.total_appointments,
                                "green",
                            ),
                            simple_chart_bar(
                                "Citas Confirmadas",
                                ChartsState.confirmed_appointments,
                                ChartsState.total_appointments,
                                "blue",
                            ),
                            simple_chart_bar(
                                "Citas Pendientes",
                                ChartsState.pending_appointments,
                                ChartsState.total_appointments,
                                "orange",
                            ),
                            simple_chart_bar(
                                "Citas Canceladas",
                                ChartsState.cancelled_appointments,
                                ChartsState.total_appointments,
                                "red",
                            ),
                            direction="column",
                            spacing="3",
                        ),
                        rx.text(
                            "No hay datos de citas disponibles",
                            size="2",
                            color="gray",
                            text_align="center",
                        ),
                    ),
                    direction="column",
                    spacing="3",
                ),
                padding="1.5rem",
                width="100%",
            ),
            direction="column",
            spacing="4",
            width="100%",
            on_mount=ChartsState.load_appointment_stats,
        ),
    )
