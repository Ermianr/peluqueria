import reflex as rx

from peluqueria.styles.styles import OUTLINE_WHITE, SOLID_BUTTON, Colors


def hero() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "Eleva Tu Estilo en Nuestro ",
                rx.text.span("Salón Premium", color=Colors.PRIMARY_COLOR.value),
                color=Colors.CUSTOM_WHITE.value,
                size=rx.breakpoints(initial="8", md="9"),
                text_align="center",
            ),
            rx.text(
                "Experimenta la perfecta combinación de arte y lujo. Nuestros estilistas expertos crean looks personalizados que realzan tu belleza natural y confianza.",
                color=Colors.CUSTOM_WHITE.value,
                size=rx.breakpoints(
                    initial="4",
                    md="6",
                ),
                text_align="center",
            ),
            rx.hstack(
                rx.link(
                    rx.el.button("Explorar Servicios", style=SOLID_BUTTON),
                    href="/ingreso",
                ),
                rx.link(
                    rx.el.button("Agendar Cita", style=OUTLINE_WHITE),
                    href="/ingreso",
                ),
            ),
            align="center",
            width=rx.breakpoints(initial="90%", lg="50%"),
            spacing="5",
        ),
        min_height="100vh",
        width="100%",
        bg="linear-gradient(to right, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0)) , url('/img/banner.webp') no-repeat center center / cover;",
    )
