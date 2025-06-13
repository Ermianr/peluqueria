import reflex as rx

from peluqueria.components.navbar_link import navbar_link
from peluqueria.state.global_state import AuthState
from peluqueria.styles.styles import OUTLINE_BUTTON, SIMPLE_BUTTON, Colors


def navbar_desktop():
    return (
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.heading(
                        "divine",
                        size="7",
                        weight="bold",
                        color=Colors.CUSTOM_WHITE.value,
                    ),
                    rx.spacer(),
                    rx.spacer(),
                    rx.hstack(
                        navbar_link("Inicio", "/#"),
                        navbar_link("Servicios", "/#"),
                        navbar_link("Nosotros", "/#"),
                        navbar_link("Contacto", "/#"),
                        spacing="5",
                    ),
                    align_items="center",
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.hstack(
                        rx.text(
                            "Hola, ",
                            AuthState.user_data.get("first_name", "Usuario"),
                            color=Colors.CUSTOM_WHITE,
                        ),
                        rx.el.button(
                            "Cerrar Sesión",
                            style=OUTLINE_BUTTON,
                            on_click=AuthState.logout,
                        ),
                        spacing="4",
                        justify="end",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.el.button("Registrarse", style=SIMPLE_BUTTON),
                            href="/registro",
                        ),
                        rx.link(
                            rx.el.button("Iniciar Sesión", style=OUTLINE_BUTTON),
                            href="/ingreso",
                        ),
                        spacing="4",
                        justify="end",
                    ),
                ),
                justify="between",
                align_items="center",
            ),
        ),
    )


def navbar_mobile():
    return (
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.heading(
                        "divine",
                        size="6",
                        weight="bold",
                        color=Colors.CUSTOM_WHITE.value,
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30, color=Colors.CUSTOM_WHITE.value)
                    ),
                    rx.menu.content(
                        rx.menu.item("Inicio"),
                        rx.menu.item("Servicios"),
                        rx.menu.item("Nosotros"),
                        rx.menu.item("Contacto"),
                        rx.menu.separator(),
                        rx.menu.item(rx.link("Registrarse", href="/registro")),
                        rx.menu.item(rx.link("Iniciar Sesión", href="/ingreso")),
                        color_scheme="amber",
                        background="black",
                        color=Colors.CUSTOM_WHITE.value,
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
    )


def navbar() -> rx.Component:
    return rx.box(
        navbar_desktop(),
        navbar_mobile(),
        bg="black",
        padding_y="1.3rem",
        padding_x="2rem",
        position="sticky",
        top="0",
        z_index="5",
        width="100%",
    )
