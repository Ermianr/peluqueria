from typing import TypedDict

import httpx
import reflex as rx

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
                response = await client.get("/employees")

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
                    f"/employees/{self.user_id}", json=sanitized_request
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
                response = await client.delete(f"/employees/{self.user_id}")

                if response.status_code == 200:
                    yield rx.toast.success("Usuario eliminado correctamente")
                    yield rx.redirect("/dashboard/employees")
                else:
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}"
                    )
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception:
            yield rx.toast.error("Error: Error inesperado")


class CreateModalState(rx.State):
    @rx.event
    async def create_user(self, form_data: dict):
        if form_data.get("password") != form_data.get("password2"):
            yield rx.toast.error("Error: Las contraseñas no coinciden")
            return
        else:
            form_data.pop("password2", None)

        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.post("/employees", json=form_data)

                if response.status_code == 201:
                    yield rx.toast.success("Empleado creado correctamente")
                    yield rx.redirect("/dashboard/employees")
                else:
                    yield rx.toast.error(
                        f"Error: Error en la consulta {response.status_code}",
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
    route="/dashboard/employees",
    title="Dashboard | Gestión de Empleados",
    meta=[
        {"char_set": "UTF-8"},
        {"name": "theme_color", "content": "black"},
    ],
    on_load=UsersManageState.get_users,
)
def employees_manage() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.box(
            users_table(),
            margin_left="16em",
            width="100%",
            max_width="calc(100vw - 16em)",
        ),
    )


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
        rx.flex(
            rx.box(
                rx.heading("Administrar Empleados"),
                rx.text("Crea, edita o elimina empleados de tu negocio"),
            ),
            create_employee(),
            align="center",
            justify="between",
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


def create_employee() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Crear empleado",
                style=SOLID_BUTTON,
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Crear un empleado",
            ),
            rx.dialog.description(
                "Crea un empleado y dale acceso",
                margin_bottom="1rem",
            ),
            rx.form(
                rx.flex(
                    rx.input(placeholder="Nombres del empleado", name="first_name"),
                    rx.input(
                        placeholder="Apellidos del empleado",
                        name="last_name",
                    ),
                    rx.input(
                        placeholder="Email del empleado",
                        name="email",
                        type="email",
                    ),
                    rx.input(
                        placeholder="Teléfono del empleado",
                        name="phone",
                        type="tel",
                    ),
                    rx.input(
                        placeholder="Contraseña del empleado",
                        name="password",
                        type="password",
                    ),
                    rx.input(
                        placeholder="Repite la contraseña del empleado",
                        name="password2",
                        type="password",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                type="button",
                                color_scheme="gray",
                                cursor="pointer",
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
                on_submit=CreateModalState.create_user,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )
