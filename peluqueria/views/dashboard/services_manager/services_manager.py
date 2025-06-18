from typing import TypedDict

import httpx
import reflex as rx

from peluqueria.settings import Settings
from peluqueria.styles.styles import SOLID_BUTTON
from peluqueria.views.dashboard.sidebar.sidebar import sidebar


class Service(TypedDict):
    name: str
    description: str | None
    duration_minutes: int
    price: int
    id: str
    created_at: str
    updated_at: str


class ServiceManageState(rx.State):
    services: list[Service] = []

    @rx.event
    async def get_services(self):
        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.get("/services")

                if response.status_code == 200:
                    self.services = response.json()
                    yield rx.toast.success("Servicios cargados correctamente")
                else:
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}"
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


class ModalState(rx.State):
    service_id: str = ""

    @rx.event
    def set_service_id(self, id: str) -> None:
        self.service_id = id

    @rx.event
    async def update_service(self, form_data: dict):
        sanitized_request = {}

        for key, value in form_data.items():
            if value:
                sanitized_request[key] = value

        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.patch(
                    f"/services/{self.service_id}", json=sanitized_request
                )

                if response.status_code == 200:
                    yield rx.toast.success("Servicio actualizado correctamente")
                    yield rx.redirect("/dashboard/services")
                else:
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}"
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


def modal(
    id: str, name: str, description: str, duration_minutes: str, price: str
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Gestionar",
                style=SOLID_BUTTON,
                padding_y="0.5rem",
                on_click=ModalState.set_service_id(id),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Gestionar Servicio",
            ),
            rx.dialog.description(
                f"{name} ({description}) - ID ({id})", margin_bottom="1rem"
            ),
            rx.form(
                rx.flex(
                    rx.input(placeholder=name, name="name"),
                    rx.input(
                        placeholder=str(description),
                        name="description",
                    ),
                    rx.input(
                        placeholder="Precio",
                        name="price",
                        type="number",
                    ),
                    rx.input(
                        placeholder="Duración en minutos",
                        name="duration_minutes",
                        type="number",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                color_scheme="gray",
                                cursor="pointer",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button("Editar", type="submit", cursor="pointer"),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=ModalState.update_service,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )


@rx.page(
    route="/dashboard/services",
    title="Dashboard | Gestión de Servicios",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
    on_load=ServiceManageState.get_services,
)
def services_manage() -> rx.Component:
    return rx.hstack(sidebar(), services_table())


def show_service(service: dict) -> rx.Component:
    return rx.table.row(
        rx.table.row_header_cell(service["name"]),
        rx.table.cell(service["description"]),
        rx.table.cell(service["duration_minutes"]),
        rx.table.cell(service["price"]),
        rx.table.cell(service["created_at"]),
        rx.table.cell(service["updated_at"]),
        rx.table.cell(
            modal(
                service.get("id", ""),
                service.get("name", ""),
                service.get("description", ""),
                service.get("duration_minutes", ""),
                service.get("price", ""),
            )
        ),
        align="center",
    )


def services_table() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.heading("Administrar Servicios"),
            rx.text("Controlar los servicios disponibles para el usuario"),
            padding="2rem",
        ),
        rx.separator(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nombre del servicio"),
                    rx.table.column_header_cell("Descripción"),
                    rx.table.column_header_cell("Duración"),
                    rx.table.column_header_cell("Precio"),
                    rx.table.column_header_cell("Creado en"),
                    rx.table.column_header_cell("Actualizado en"),
                    rx.table.column_header_cell("Acciones"),
                ),
            ),
            rx.table.body(rx.foreach(ServiceManageState.services, show_service)),
            width="100%",
        ),
        width="100%",
        direction="column",
        spacing="2",
    )
