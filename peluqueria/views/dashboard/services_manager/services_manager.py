from typing import TypedDict

import httpx
import reflex as rx

from peluqueria.components.route_guard import employee_only_guard
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


class UpdateModalState(rx.State):
    service_id: str = ""

    @rx.event
    def set_service_id(self, id: str) -> None:
        self.service_id = id

    @rx.event
    async def update_service(self, form_data: dict):
        sanitized_request = {key: value for key, value in form_data.items() if value}

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
                        f"Error: Error en la consulta {response.status_code}",
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


class CreateModalState(rx.State):
    img: str = ""
    img_path: str = ""

    @rx.event
    async def update_image(self, files: list[rx.UploadFile]):
        if files:
            file = files[0]
            data = await file.read()
            path = rx.get_upload_dir() / file.name  # type: ignore
            self.img_path = str(path)
            with path.open("wb") as f:
                f.write(data)
            self.img = file.name  # type: ignore

    @rx.event
    def clean_image(self):
        path = rx.get_upload_dir() / self.img
        path.unlink() if self.img else None
        self.img = ""
        self.img_path = ""

    @rx.event
    def soft_clean_image(self):
        self.img = ""
        self.img_path = ""

    @rx.event
    async def create_service(self, form_data: dict):
        if not self.img_path:
            yield rx.toast.error("Error: Debes subir una imagen del servicio")
            self.clean_image()
            return

        form_data["img_path"] = self.img_path

        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.post("/services", json=form_data)

                if response.status_code == 201:
                    self.soft_clean_image()
                    yield rx.toast.success("Servicio creado correctamente")
                    yield rx.redirect("/dashboard/services")
                else:
                    self.clean_image()
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}",
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
            self.clean_image()
        except Exception:
            self.clean_image()
            yield rx.toast.error("Error: Error inesperado")


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
    content = rx.hstack(
        sidebar(),
        rx.box(
            services_table(),
            margin_left="16em",
            width="100%",
            max_width="calc(100vw - 16em)",
        ),
    )
    return employee_only_guard(content)


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
            ),
        ),
        align="center",
    )


def services_table() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.box(
                rx.heading("Administrar Servicios"),
                rx.text("Controlar los servicios disponibles para el usuario"),
            ),
            create_service(),
            align="center",
            justify="between",
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
        spacing="3",
        padding_x="2rem",
        padding_y="1rem",
    )


def modal(
    id: str,
    name: str,
    description: str,
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Gestionar",
                style=SOLID_BUTTON,
                padding_y="0.5rem",
                on_click=UpdateModalState.set_service_id(id),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Gestionar Servicio",
            ),
            rx.dialog.description(
                f"{name} ({description}) - ID ({id})",
                margin_bottom="1rem",
            ),
            rx.form(
                rx.flex(
                    rx.input(placeholder=name, name="name"),
                    rx.input(
                        placeholder=description,
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
                on_submit=UpdateModalState.update_service,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )


def create_service() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Crear servicio",
                style=SOLID_BUTTON,
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Crear un servicio",
            ),
            rx.dialog.description(
                "Crea un servicio y dale acceso al usuario a él",
                margin_bottom="1rem",
            ),
            rx.form(
                rx.flex(
                    rx.input(placeholder="Nombre del servicio", name="name"),
                    rx.input(
                        placeholder="Descripción del servicio",
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
                    upload_component(),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                type="button",
                                color_scheme="gray",
                                cursor="pointer",
                                on_click=CreateModalState.clean_image,
                            ),
                        ),
                        rx.dialog.close(
                            rx.button("Crear", type="submit", cursor="pointer"),
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
            max_width="450px",
        ),
    )


def upload_component():
    return rx.vstack(
        rx.upload(
            rx.text("Arrastra imágenes aquí o haz clic para seleccionar"),
            id="subida_imagenes",
            accept={
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
                "image/gif": [".gif"],
                "image/webp": [".webp"],
            },
            multiple=True,
            max_files=1,
            border="2px dashed #ccc",
            padding="2rem",
            on_drop=CreateModalState.update_image(
                rx.upload_files(upload_id="subida_imagenes")  # type: ignore
            ),
        ),
        rx.button(
            "Limpiar imagen",
            type="button",
            on_click=[
                CreateModalState.clean_image(),
                rx.clear_selected_files("subida_imagen"),
            ],
        ),
        rx.cond(
            CreateModalState.img != "",
            rx.vstack(
                rx.image(src=rx.get_upload_url(CreateModalState.img), width="10rem"),
                rx.text(f"Nombre: {CreateModalState.img}", color="blue"),
            ),
        ),
    )
