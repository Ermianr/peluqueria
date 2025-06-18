import reflex as rx

from peluqueria.styles.styles import Colors


class SidebarState(rx.State):
    active_text: str = "Gestión de Usuarios"


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, color=Colors.CUSTOM_WHITE.value),
            rx.text(text, size="2", color=Colors.CUSTOM_WHITE.value),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": Colors.PRIMARY_COLOR.value,
                    "color": Colors.PARAGRAPH_COLOR.value,
                },
                "bg": rx.cond(
                    SidebarState.active_text == text,
                    Colors.PRIMARY_COLOR.value,
                    "transparent",
                ),
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
        on_click=lambda: SidebarState.set_active_text(text),  # type: ignore
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Resumen General", "layout-dashboard", "/dashboard"),
        sidebar_item("Gestión de Citas", "square-library", "/dashboard"),
        sidebar_item("Gestión de Servicios", "calendar-cog", "/dashboard/services"),
        sidebar_item("Gestión de Personal", "contact-round", "/dashboard"),
        sidebar_item("Gestión de Usuarios", "user-round", "/dashboard"),
        spacing="1",
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "divine",
                        size="7",
                        weight="bold",
                        color=Colors.CUSTOM_WHITE.value,
                    ),
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(),
                spacing="5",
                position="sticky",
                left="0px",
                top="0px",
                padding_x="1em",
                padding_y="1.5em",
                bg="black",
                align="start",
                min_height="100vh",
                width="16em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(rx.icon("align-justify", size=30)),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(rx.icon("x", size=30)),
                                width="100%",
                            ),
                            sidebar_items(),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg="black",
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )
