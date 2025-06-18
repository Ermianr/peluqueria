import reflex as rx

from peluqueria.styles.styles import SOLID_BUTTON


def appointment_dashboard() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.flex(
                rx.heading("Gestionar Citas", as_="h1"),
                rx.el.button(
                    rx.icon("plus"),
                    "Agendar cita",
                    style=SOLID_BUTTON,
                    padding_y="0.8rem",
                ),
                justify="between",
                align="center",
            ),
            rx.text("Aquí podrás gestionar tus citas de diferentes formas"),
            rx.separator(),
        ),
        width="100%",
    )


def appointments_table() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.heading("Administrar Usuarios"),
            rx.text("Una forma sencilla de administrar usuarios y ver sus datos"),
            padding="2rem",
        ),
        rx.separator(),
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
            rx.table.body(),
            width="100%",
        ),
        width="100%",
        direction="column",
        spacing="2",
    )
