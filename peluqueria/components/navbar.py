import reflex as rx

from peluqueria.components.navbar_link import navbar_link
from peluqueria.state.global_state import AuthState
from peluqueria.styles.styles import OUTLINE_BUTTON, SIMPLE_BUTTON, Colors


def navbar_desktop():
    return rx.desktop_only(
        rx.hstack(
            rx.hstack(
                rx.link(
                    rx.heading(
                        "divine",
                        size="7",
                        weight="bold",
                        color=Colors.CUSTOM_WHITE.value,
                    ),
                    href="/",
                ),
                rx.spacer(),
                rx.spacer(),
                rx.hstack(
                    navbar_link("Inicio", "/"),
                    navbar_link("Servicios", "#services"),
                    navbar_link("Nosotros", "#about"),
                    navbar_link("Contacto", "#contact"),
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
                        color=Colors.CUSTOM_WHITE.value,
                    ),
                    rx.el.button(
                        "Cerrar Sesión",
                        style=OUTLINE_BUTTON,
                        on_click=AuthState.logout,
                    ),
                    spacing="4",
                    justify="end",
                    align_items="center",
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
    )


def navbar_mobile():
    return rx.mobile_and_tablet(
        rx.hstack(
            rx.hstack(
                rx.link(
                    rx.heading(
                        "divine",
                        size="6",
                        weight="bold",
                        color=Colors.CUSTOM_WHITE.value,
                    ),
                    href="/",
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
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.menu.item(
                            rx.text(
                                f"Hola, {AuthState.user_data.get('first_name', 'Usuario')}",
                                color=Colors.CUSTOM_WHITE.value,
                            )
                        ),
                        None,
                    ),
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.menu.item("Cerrar Sesión", on_click=AuthState.logout),
                        [
                            rx.menu.item(
                                rx.link(
                                    "Registrarse",
                                    href="/registro",
                                    text_decoration="none",
                                ),
                                key="registrarse",
                            ),
                            rx.menu.item(
                                rx.link(
                                    "Iniciar Sesión",
                                    href="/ingreso",
                                    text_decoration="none",
                                ),
                                key="ingreso",
                            ),
                        ],
                    ),
                    color_scheme="amber",
                    background="black",
                    color=Colors.CUSTOM_WHITE.value,
                ),
                justify="end",
            ),
            justify="between",
            align_items="center",
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
