import reflex as rx

from peluqueria.components.navbar_link import navbar_link
from peluqueria.components.social_icon import social_icon
from peluqueria.styles.styles import Colors
from datetime import datetime

def footer_items_1() -> rx.Component:
    return rx.flex(
        rx.heading(
            "NAVEGACIÓN", size="4", weight="bold", as_="h3", color=Colors.CUSTOM_WHITE.value
        ),
        navbar_link("Inicio", "/#"),
        navbar_link("Servicios", "/#"),
        navbar_link("Nosotros", "/#"),
        navbar_link("Contacto", "/#"),
        spacing="4",
        text_align=rx.breakpoints(
            initial="center",
            lg="start"
        ),
        direction="column"
    )

def socials() -> rx.Component:
    return rx.flex(
        social_icon("instagram"),
        social_icon("facebook"),
        social_icon("twitter"),
        spacing="4",
    )   

def footer() -> rx.Component:
    return rx.el.footer(
        rx.vstack(
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            "divine",
                            size="7",
                            weight="bold",
                            color=Colors.CUSTOM_WHITE.value
                        ),
                        align_items="center",
                    ),
                    rx.text(
                        f"© {datetime.now().year} divine, Inc",
                        size="3",
                        white_space="nowrap",
                        weight="medium",
                        color=Colors.PARAGRAPH_COLOR.value
                    ),
                    spacing="4",
                    align_items=rx.breakpoints(
                        initial="center",
                        lg="start"
                    ),
                ),
                footer_items_1(),
                justify="center",
                spacing="9",
                flex_direction=rx.breakpoints(
                    initial="column",
                    lg="row"
                ),
                width="100%",
            ),
            rx.divider(bg=Colors.PARAGRAPH_COLOR.value),
            rx.hstack(
                socials(),
                justify="end",
                width="100%",
            ),
            spacing="5",
            width="100%",
            padding="2rem"
        ),
        width="100%",
        bg="black",
        margin_top="2rem"
    )