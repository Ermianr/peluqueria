from typing import TypedDict

import httpx
import reflex as rx

from peluqueria.components.route_guard import employee_only_guard
from peluqueria.settings import Settings
from peluqueria.styles.styles import SOLID_BUTTON
from peluqueria.views.dashboard.sidebar.sidebar import sidebar


class User(TypedDict):
    first_name: str
    last_name: str
    email: str
    phone: str
    id: str
    role: str
    created_at: str
    updated_at: str
    is_active: bool


class UsersManageState(rx.State):
    users: list[User] = []

    @rx.event
    async def get_users(self):
        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.get("/users")

                if response.status_code == 200:
                    self.users = response.json()
                    yield rx.toast.success("Usuarios cargados correctamente")
                else:
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}"
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


class ModalState(rx.State):
    user_id: str = ""
    select_state: str = "Activo"
    select_bool_state: bool = True

    @rx.event
    def change_select(self, value: str) -> None:
        self.select_state = value
        if self.select_state == "Activo":
            self.select_bool_state = True
        else:
            self.select_bool_state = False

    @rx.event
    def set_user_id(self, id: str) -> None:
        self.user_id = id

    @rx.event
    async def update_user(self, form_data: dict):
        sanitized_request = {}

        for key, value in form_data.items():
            if value:
                if key in ("first_name", "last_name"):
                    sanitized_request[key] = str(value).capitalize()
                else:
                    sanitized_request[key] = value

        sanitized_request["is_active"] = self.select_bool_state

        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.patch(
                    f"/users/{self.user_id}", json=sanitized_request
                )

                if response.status_code == 200:
                    yield rx.toast.success("Usuario actualizado correctamente")
                    yield rx.redirect("/dashboard")
                else:
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}"
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")

    @rx.event
    async def delete_user(self):
        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.delete(f"/users/{self.user_id}")

                if response.status_code == 200:
                    yield rx.toast.success("Usuario eliminado correctamente")
                    yield rx.redirect("/dashboard")
                else:
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}"
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


def modal(
    id: str, first_name: str, last_name: str, email: str, phone: str, is_active: bool
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Gestionar",
                style=SOLID_BUTTON,
                padding_y="0.5rem",
                on_click=ModalState.set_user_id(id),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Gestionar Usuario",
            ),
            rx.dialog.description(
                f"{first_name} {last_name} - ID ({id})", margin_bottom="1rem"
            ),
            rx.form(
                rx.flex(
                    rx.input(placeholder=first_name, name="first_name"),
                    rx.input(
                        placeholder=last_name,
                        name="last_name",
                    ),
                    rx.input(
                        placeholder=email,
                        name="email",
                    ),
                    rx.input(
                        placeholder=phone,
                        name="phone",
                    ),
                    rx.select(
                        ["Activo", "Inactivo"],
                        value=ModalState.select_state,
                        on_change=ModalState.change_select,
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
                        delete_user_alert(),
                        rx.dialog.close(
                            rx.button("Editar", type="submit", cursor="pointer"),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=ModalState.update_user,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )


def delete_user_alert() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button("Eliminar Permanentemente", color_scheme="red", cursor="pointer"),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Eliminar usuario"),
            rx.alert_dialog.description(
                "¿Estás seguro? Una vez borrado no tendrá recuperación, se recomienda inactivar el usuario para no perder datos",
                size="2",
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
                        "Eliminar permanentemente",
                        color_scheme="red",
                        variant="solid",
                        cursor="pointer",
                        on_click=ModalState.delete_user,
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )


@rx.page(
    route="/dashboard/users",
    title="Dashboard | Gestión de Usuarios",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
    on_load=UsersManageState.get_users,
)
def users_manage() -> rx.Component:
    content = rx.hstack(
        sidebar(),
        rx.box(
            users_table(),
            margin_left="16em",
            width="100%",
            max_width="calc(100vw - 16em)",
        ),
    )
    return employee_only_guard(content)


def show_user(user) -> rx.Component:
    return rx.table.row(
        rx.table.row_header_cell(f"{user['first_name']} {user['last_name']}"),
        rx.table.cell(user["email"]),
        rx.table.cell(user["phone"]),
        rx.table.cell(user["created_at"]),
        rx.table.cell(user["updated_at"]),
        rx.table.cell(user["is_active"]),
        rx.table.cell(
            modal(
                user["id"],
                user["first_name"],
                user["last_name"],
                user["email"],
                user["phone"],
                user["is_active"],
            )
        ),
        align="center",
    )


def users_table() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.heading("Administrar Usuarios"),
            rx.text("Una forma sencilla de administrar usuarios y ver sus datos"),
            padding="2rem",
        ),
        rx.separator(),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Nombre Completo"),
                        rx.table.column_header_cell("Email"),
                        rx.table.column_header_cell("Teléfono"),
                        rx.table.column_header_cell("Creado en"),
                        rx.table.column_header_cell("Actualizado en"),
                        rx.table.column_header_cell("Activo"),
                        rx.table.column_header_cell("Acciones"),
                    ),
                ),
                rx.table.body(rx.foreach(UsersManageState.users, show_user)),
                width="100%",
            ),
            padding_x="2rem",
            padding_y="1rem",
        ),
        width="100%",
        direction="column",
        spacing="3",
    )
