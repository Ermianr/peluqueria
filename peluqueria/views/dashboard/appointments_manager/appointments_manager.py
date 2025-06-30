from typing import TypedDict

import httpx
import reflex as rx

from peluqueria.components.route_guard import employee_only_guard
from peluqueria.constants import HTTP_200_OK, HTTP_204_NO_CONTENT
from peluqueria.settings import Settings
from peluqueria.state.global_state import AuthState
from peluqueria.styles.styles import SOLID_BUTTON


class Appointment(TypedDict):
    id: str
    appointment_date: str
    created_at: str
    updated_at: str
    user_id: str
    employee_id: str
    service_ids: list[str]
    employee_name: str
    service_names: list[str]
    user_name: str
    state: str
    total_cost: float


class AppointmentsManagerState(rx.State):
    appointments: list[Appointment] = []  # noqa: RUF012
    loading: bool = False

    @rx.event
    async def get_appointments(self):
        self.loading = True
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
                    self.appointments = response.json()
                    yield rx.toast.success("Citas cargadas correctamente")
                else:
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}",
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")
        finally:
            self.loading = False

    @rx.event
    async def delete_appointment(self, appointment_id: str):
        try:
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                return

            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.delete(
                    f"/appointments/{appointment_id}",
                    headers={"Authorization": f"Bearer {auth_state.access_token}"},
                )

                if response.status_code == HTTP_204_NO_CONTENT:
                    yield rx.toast.success("Cita eliminada correctamente")
                    yield AppointmentsManagerState.get_appointments
                else:
                    yield rx.toast.error(
                        f"Error: No se pudo eliminar la cita {response.status_code}",
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")

    @rx.event
    async def complete_appointment(self, appointment_id: str):
        try:
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                return

            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.patch(
                    f"/appointments/{appointment_id}",
                    json={"state": "completed"},
                    headers={"Authorization": f"Bearer {auth_state.access_token}"},
                )

                if response.status_code == HTTP_200_OK:
                    yield rx.toast.success("Cita marcada como completada")
                    yield AppointmentsManagerState.get_appointments
                else:
                    yield rx.toast.error(
                        f"Error: No se pudo actualizar la cita {response.status_code}",
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


def appointment_date_cell(appointment_date: str) -> rx.Component:
    return rx.text(appointment_date, size="2")


def state_badge(state: str) -> rx.Component:
    return rx.cond(
        state == "pending",
        rx.badge("Pendiente", color_scheme="orange", size="2"),
        rx.cond(
            state == "confirmed",
            rx.badge("Confirmada", color_scheme="blue", size="2"),
            rx.cond(
                state == "completed",
                rx.badge("Completada", color_scheme="green", size="2"),
                rx.cond(
                    state == "cancelled",
                    rx.badge("Cancelada", color_scheme="red", size="2"),
                    rx.badge(state, color_scheme="gray", size="2"),
                ),
            ),
        ),
    )


def delete_appointment_alert(appointment_id: str) -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(
                rx.icon("trash-2", size=16),
                color_scheme="red",
                variant="soft",
                size="2",
                cursor="pointer",
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Eliminar Cita"),
            rx.alert_dialog.description(
                "¿Estás seguro de que quieres eliminar esta cita? "
                "Esta acción no se puede deshacer.",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        cursor="pointer",
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Eliminar",
                        color_scheme="red",
                        cursor="pointer",
                        on_click=AppointmentsManagerState.delete_appointment(
                            appointment_id,
                        ),
                    ),
                ),
                spacing="3",
                justify="end",
            ),
        ),
    )


def appointment_actions(appointment: Appointment) -> rx.Component:
    return rx.flex(
        rx.cond(
            appointment["state"] != "completed",
            rx.button(
                rx.icon("check", size=16),
                "Completar",
                color_scheme="green",
                variant="soft",
                size="2",
                cursor="pointer",
                on_click=AppointmentsManagerState.complete_appointment(
                    appointment["id"],
                ),
            ),
            rx.text("Completada", color="green", size="2", weight="bold"),
        ),
        delete_appointment_alert(appointment["id"]),
        spacing="2",
        align="center",
    )


def appointments_table() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.flex(
                rx.heading("Gestionar Citas", as_="h1"),
                rx.button(
                    rx.icon("refresh-cw"),
                    "Actualizar",
                    style=SOLID_BUTTON,
                    padding_y="0.5rem",
                    on_click=AppointmentsManagerState.get_appointments,
                    disabled=AppointmentsManagerState.loading,
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.text("Administra las citas de los clientes y cambia su estado"),
            padding="2rem",
        ),
        rx.separator(),
        rx.cond(
            AppointmentsManagerState.loading,
            rx.center(
                rx.spinner(size="3"),
                padding="2rem",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Cliente"),
                        rx.table.column_header_cell("Estilista"),
                        rx.table.column_header_cell("Servicios"),
                        rx.table.column_header_cell("Fecha"),
                        rx.table.column_header_cell("Estado"),
                        rx.table.column_header_cell("Costo Total"),
                        rx.table.column_header_cell("Acciones"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        AppointmentsManagerState.appointments,
                        lambda appointment: rx.table.row(
                            rx.table.cell(appointment["user_name"]),
                            rx.table.cell(appointment["employee_name"]),
                            rx.table.cell(
                                rx.flex(
                                    rx.foreach(
                                        appointment["service_names"],
                                        lambda service_name: rx.badge(
                                            service_name,
                                            color_scheme="blue",
                                            size="1",
                                        ),
                                    ),
                                    wrap="wrap",
                                    spacing="1",
                                ),
                            ),
                            rx.table.cell(
                                appointment_date_cell(appointment["appointment_date"]),
                            ),
                            rx.table.cell(
                                state_badge(appointment["state"]),
                            ),
                            rx.table.cell(
                                rx.text(
                                    f"${appointment['total_cost']:.2f}",
                                    size="2",
                                    weight="bold",
                                    color="green",
                                ),
                            ),
                            rx.table.cell(
                                appointment_actions(appointment),
                            ),
                        ),
                    ),
                ),
                width="100%",
                overflow_x="auto",
            ),
        ),
        width="100%",
        direction="column",
        spacing="3",
        padding_x="2rem",
        padding_y="1rem",
        margin_left="16em",
        max_width="calc(100vw - 16em)",
        on_mount=AppointmentsManagerState.get_appointments,
    )


def appointments_manager() -> rx.Component:
    content = appointments_table()
    return employee_only_guard(content)
