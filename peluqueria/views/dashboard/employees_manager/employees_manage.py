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


class DeleteModalState(rx.State):
    user_id: str = ""
    user_name: str = ""

    @rx.event
    def set_user_data(self, user_id: str, user_name: str) -> None:
        self.user_id = user_id
        self.user_name = user_name

    @rx.event
    async def delete_user(self):
        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                print(f"Intentando eliminar usuario con ID: {self.user_id}")
                print(
                    f"URL completa: {Settings.API_BACKEND_URL}/employees/{self.user_id}"
                )

                response = await client.delete(f"/employees/{self.user_id}")

                print(f"Código de respuesta: {response.status_code}")
                print(f"Respuesta completa: {response.text}")

                if response.status_code == 200:
                    yield rx.toast.success("Empleado eliminado correctamente")
                    yield UsersManageState.get_users
                else:
                    error_msg = f"Error {response.status_code}"
                    try:
                        error_detail = response.json().get(
                            "detail", "Error desconocido"
                        )
                        error_msg = f"Error {response.status_code}: {error_detail}"
                    except:
                        pass
                    yield rx.toast.error(error_msg)
        except httpx.RequestError as e:
            print(f"Error de conexión: {e}")
            yield rx.toast.error("Error: Error de conexión al servidor")
        except Exception as e:
            print(f"Error inesperado: {e}")
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


def delete_employee_button(
    user_id: str, first_name: str, last_name: str
) -> rx.Component:
    full_name = f"{first_name} {last_name}"
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(
                "Eliminar",
                color_scheme="red",
                variant="solid",
                cursor="pointer",
                padding_y="0.5rem",
                on_click=DeleteModalState.set_user_data(user_id, full_name),
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Eliminar empleado"),
            rx.alert_dialog.description(
                f"¿Estás seguro de que deseas eliminar a {full_name}? "
                "Esta acción no se puede deshacer y se perderán "
                "todos los datos asociados.",
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
                        on_click=DeleteModalState.delete_user,
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


def show_user(user: dict) -> rx.Component:
    return rx.table.row(
        rx.table.row_header_cell(f"{user['first_name']} {user['last_name']}"),
        rx.table.cell(user["email"]),
        rx.table.cell(user["phone"]),
        rx.table.cell(user["created_at"]),
        rx.table.cell(user["updated_at"]),
        rx.table.cell(user["is_active"]),
        rx.table.cell(
            delete_employee_button(
                user["id"],
                user["first_name"],
                user["last_name"],
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
                        rx.table.column_header_cell("Eliminar"),
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
