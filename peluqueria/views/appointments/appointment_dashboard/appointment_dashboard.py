from datetime import datetime, timezone
from typing import TypedDict

import httpx
import reflex as rx

from peluqueria.components.route_guard import authenticated_only_guard
from peluqueria.constants import HTTP_200_OK, HTTP_201_CREATED
from peluqueria.settings import Settings
from peluqueria.state.global_state import AuthState
from peluqueria.styles.styles import SOLID_BUTTON


def appointment_date_cell(appointment_date: str) -> rx.Component:
    return rx.text(
        appointment_date,
        size="2",
    )


class Service(TypedDict):
    id: str
    name: str
    description: str
    duration_minutes: int
    price: int
    img_path: str


class Employee(TypedDict):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str
    created_at: str
    updated_at: str
    is_active: bool


class Apppointment(TypedDict):
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


class AppointmentManageState(rx.State):
    appointments: list[Apppointment] = []

    @rx.event
    async def get_appointments(self):
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


class ServiceState(rx.State):
    services: list[Service] = []

    @rx.event
    async def get_services(self):
        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.get("/services")

                if response.status_code == HTTP_200_OK:
                    self.services = response.json()
                else:
                    yield rx.toast.error(
                        f"Error: Error al cargar servicios {response.status_code}",
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


class EmployeeState(rx.State):
    employees: list[Employee] = []

    @rx.event
    async def get_employees(self):
        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.get("/employees")

                if response.status_code == HTTP_200_OK:
                    self.employees = response.json()
                else:
                    yield rx.toast.error(
                        f"Error: Error al cargar empleados {response.status_code}",
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


class CreateModalState(rx.State):
    is_modal_open: bool = False
    selected_services: list[str] = []  # noqa: RUF012

    @rx.var
    def selected_services_count(self) -> int:
        return len(self.selected_services)

    def is_service_selected(self, service_id: str) -> bool:
        return service_id in self.selected_services

    @rx.var
    def selected_services_display_data(self) -> list[dict]:
        """Obtener información de display para servicios seleccionados."""
        return [
            {
                "id": service_id,
                "display_name": f"Servicio {service_id}",
            }
            for service_id in self.selected_services
        ]

    @rx.event
    def open_modal(self):
        self.is_modal_open = True
        self.selected_services = []
        return [ServiceState.get_services, EmployeeState.get_employees]

    @rx.event
    def close_modal(self):
        self.is_modal_open = False
        self.selected_services = []

    @rx.event
    def toggle_service(self, service_id: str):
        if service_id in self.selected_services:
            self.selected_services.remove(service_id)
        else:
            self.selected_services.append(service_id)

    @rx.event
    def clear_services(self):
        self.selected_services = []

    @rx.event
    async def create_service(self, form_data: dict):
        try:
            if not self.selected_services:
                yield rx.toast.error("Error: Debe seleccionar al menos un servicio")
                return

            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                yield rx.toast.error("Error: Debe iniciar sesión para crear una cita")
                yield rx.redirect("/ingreso")
                return

            user_id = auth_state.user_data.get("id", "")
            if not user_id:
                yield rx.toast.error("Error: No se pudo obtener el ID del usuario")
                return

            form_data["user_id"] = user_id
            form_data["service_ids"] = self.selected_services

            if "appointment_date" in form_data:
                appointment_date_str = form_data["appointment_date"]
                appointment_date = datetime.fromisoformat(appointment_date_str)
                form_data["appointment_date"] = appointment_date.isoformat() + "Z"

            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.post(
                    "/appointments",
                    json=form_data,
                    headers={"Authorization": f"Bearer {auth_state.access_token}"},
                )

                if response.status_code == HTTP_201_CREATED:
                    yield rx.toast.success("Cita creada correctamente")
                    self.is_modal_open = False
                    self.selected_services = []
                    yield AppointmentManageState.get_appointments
                else:
                    error_detail = (
                        response.text if response.text else "Error desconocido"
                    )
                    yield rx.toast.error(
                        f"Error {response.status_code}: {error_detail}",
                    )
        except httpx.RequestError as e:
            yield rx.toast.error(f"Error de conexión: {e!s}")
        except Exception as e:
            yield rx.toast.error(f"Error inesperado: {e!s}")


def service_chip(service: Service) -> rx.Component:
    return rx.badge(
        f"{service['name']} - ${service['price']}",
        rx.icon("circle-plus", size=16),
        color_scheme="gray",
        radius="full",
        size="3",
        cursor="pointer",
        style={"_hover": {"opacity": 0.75}},
        on_click=CreateModalState.toggle_service(service["id"]),
    )


def selected_service_chip(
    service_id: str,
    service_name: str,
    service_price: int,
) -> rx.Component:
    return rx.badge(
        f"{service_name} - ${service_price}",
        rx.icon("circle-check", size=16, color="white"),
        color_scheme="green",
        radius="full",
        size="3",
        cursor="pointer",
        style={"_hover": {"opacity": 0.75}},
        on_click=CreateModalState.toggle_service(service_id),
    )


def selected_service_badge(
    service_id: str,
    service_name: str,
    service_price: int,
) -> rx.Component:
    """Badge para mostrar un servicio seleccionado."""
    return rx.badge(
        f"{service_name} - ${service_price}",
        rx.icon("circle-x", size=16, color="white"),
        color_scheme="green",
        radius="full",
        size="3",
        cursor="pointer",
        style={"_hover": {"opacity": 0.75}},
        on_click=CreateModalState.toggle_service(service_id),
    )


def selected_services_display() -> rx.Component:
    """Mostrar los servicios seleccionados como badges."""
    return rx.cond(
        CreateModalState.selected_services_count > 0,
        rx.flex(
            rx.text("Servicios seleccionados:", size="2", weight="bold"),
            rx.flex(
                rx.foreach(
                    CreateModalState.selected_services_display_data,
                    lambda service_data: rx.badge(
                        service_data["display_name"],
                        rx.icon("circle-x", size=16, color="white"),
                        color_scheme="green",
                        radius="full",
                        size="3",
                        cursor="pointer",
                        style={"_hover": {"opacity": 0.75}},
                        on_click=CreateModalState.toggle_service(service_data["id"]),
                    ),
                ),
                wrap="wrap",
                spacing="2",
            ),
            direction="column",
            spacing="2",
            width="100%",
        ),
    )


def services_selector() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.hstack(
                rx.icon("package", size=20),
                rx.heading(
                    f"Servicios ({CreateModalState.selected_services_count})",
                    size="4",
                ),
                spacing="1",
                align="center",
            ),
            rx.button(
                "Limpiar",
                size="2",
                variant="soft",
                color_scheme="tomato",
                cursor="pointer",
                on_click=CreateModalState.clear_services,
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        selected_services_display(),
        rx.flex(
            rx.text("Servicios disponibles:", size="2", weight="bold"),
            rx.flex(
                rx.foreach(
                    ServiceState.services,
                    service_chip,
                ),
                wrap="wrap",
                spacing="2",
                justify_content="start",
            ),
            direction="column",
            spacing="2",
            width="100%",
        ),
        justify_content="start",
        align_items="start",
        width="100%",
        spacing="3",
    )


def create_service() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Crear una cita",
            ),
            rx.dialog.description(
                "Crea una cita y disfruta de nuestros servicios",
                margin_bottom="1rem",
            ),
            rx.form(
                rx.flex(
                    services_selector(),
                    rx.select.root(
                        rx.select.trigger(placeholder="Selecciona un empleado"),
                        rx.select.content(
                            rx.select.group(
                                rx.select.label("Selecciona el empleado disponible"),
                                rx.foreach(
                                    EmployeeState.employees,
                                    lambda employee: rx.select.item(
                                        f"{employee['first_name']} "
                                        f"{employee['last_name']}",
                                        value=employee["id"],
                                    ),
                                ),
                            ),
                        ),
                        name="employee_id",
                        required=True,
                    ),
                    rx.input(
                        type="datetime-local",
                        name="appointment_date",
                        required=True,
                        placeholder="Selecciona fecha y hora",
                        min=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                type="button",
                                color_scheme="gray",
                                cursor="pointer",
                                on_click=CreateModalState.close_modal,
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Crear",
                                type="submit",
                                cursor="pointer",
                            ),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=CreateModalState.create_service,
                reset_on_submit=False,
            ),
            max_width="500px",
        ),
        open=CreateModalState.is_modal_open,
    )


def appointments_table() -> rx.Component:
    content = rx.flex(
        rx.box(
            rx.flex(
                rx.heading("Gestionar Citas", as_="h1"),
                rx.button(
                    rx.icon("plus"),
                    "Agendar cita",
                    style=SOLID_BUTTON,
                    padding_y="0.5rem",
                    on_click=CreateModalState.open_modal,
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.text("Una forma sencilla de administrar citas y ver su información"),
            padding="2rem",
        ),
        rx.separator(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nombre del Estilista"),
                    rx.table.column_header_cell("Servicios"),
                    rx.table.column_header_cell("Fecha del Servicio"),
                    rx.table.column_header_cell("Costo Total"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    AppointmentManageState.appointments,
                    lambda appointment: rx.table.row(
                        rx.table.cell(appointment["employee_name"]),
                        rx.table.cell(
                            rx.flex(
                                rx.foreach(
                                    appointment["service_names"],
                                    lambda service_name: rx.badge(
                                        service_name,
                                        color_scheme="blue",
                                        size="2",
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
                            rx.text(
                                f"${appointment['total_cost']:.2f}",
                                size="2",
                                weight="bold",
                                color="green",
                            ),
                        ),
                    ),
                ),
            ),
            width="100%",
        ),
        create_service(),
        width="100%",
        direction="column",
        spacing="2",
        padding_x="4rem",
        padding_y="2rem",
        on_mount=[AuthState.check_auth, AppointmentManageState.get_appointments],
    )

    return authenticated_only_guard(content)
