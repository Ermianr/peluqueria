import reflex as rx

from peluqueria.components.form_field import form_field
from peluqueria.components.social_icon import social_icon
from peluqueria.styles.styles import CUSTOM_INPUT, SOLID_BUTTON, Colors


def info_field(icon: str, title: str, text: str) -> rx.Component:
    return rx.hstack(
        rx.icon(icon, color=Colors.PRIMARY_COLOR.value),
        rx.box(
            rx.heading(title, as_="h4", size="3", weight="medium"),
            rx.text(text, color=Colors.PARAGRAPH_COLOR.value),
        ),
        align="center",
    )


def time_field(days: str, hours: str) -> rx.Component:
    return rx.flex(
        rx.text(days, color=Colors.PARAGRAPH_COLOR.value),
        rx.text(hours, weight="medium"),
        justify="between",
        width="100%",
    )


def contact() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Ponte en ",
            rx.text.span("Contacto", color=Colors.PRIMARY_COLOR.value),
            as_="h2",
        ),
        rx.text(
            "Nos encantaria saber de tí. Envíanos un mensaje con cualquier pregunta"
        ),
        rx.flex(
            rx.hstack(
                rx.form(
                    rx.flex(
                        form_field("Nombre Completo", "Tu nombre", "text", "full-name"),
                        form_field("Correo Electrónico", "Tu correo", "email", "email"),
                        direction=rx.breakpoints(
                            initial="column",
                            md="row",
                        ),
                        spacing="3",
                        margin_bottom="1rem",
                    ),
                    rx.hstack(
                        form_field("Número de Teléfono", "Tu teléfono", "tel", "phone"),
                        margin_bottom="1rem",
                    ),
                    rx.flex(
                        rx.el.label("Tu Mensaje", html_for="message"),
                        rx.el.textarea(
                            placeholder="Cuéntanos sobre lo que estás pensando...",
                            resize="none",
                            rows=10,
                            name="message",
                            id="message",
                            required=True,
                            style=CUSTOM_INPUT,
                        ),
                        direction="column",
                        spacing="1",
                        margin_bottom="1rem",
                    ),
                    rx.button(
                        "Enviar Mensaje",
                        type="submit",
                        style=SOLID_BUTTON,
                        padding_y="1.2rem",
                    ),
                    width="100%",
                ),
                width=rx.breakpoints(initial="100%", md="50%"),
            ),
            rx.vstack(
                rx.image(
                    src="/img/map_placeholder.webp",
                    width="100%",
                    height="10rem",
                    object_fit="cover",
                    border_radius="2rem",
                ),
                rx.vstack(
                    rx.heading("Información de contacto", as_="h3", size="5"),
                    info_field("map-pin", "Dirección", "Cali, Calle 17 #50 - 50"),
                    info_field("phone", "Teléfono", "300 000000 - 654321"),
                    info_field("mail", "Correo", "divine@gmail.com"),
                ),
                rx.vstack(
                    rx.heading("Horario de atención", as_="h3", size="5"),
                    time_field("Lunes - Viernes", "9:00 AM - 8:00 PM"),
                    time_field("Sábado", "9:00 AM - 6:00 PM"),
                    time_field("Domingo", "10:00 AM - 5:00 PM"),
                    width="100%",
                ),
                rx.vstack(
                    rx.heading("Síguenos", as_="h3", size="5"),
                    rx.hstack(
                        social_icon("instagram"),
                        social_icon("facebook"),
                        social_icon("twitter"),
                    ),
                ),
                width=rx.breakpoints(initial="100%", md="50%"),
            ),
            direction=rx.breakpoints(
                initial="column",
                md="row",
            ),
            width="100%",
            spacing="8",
        ),
        align="center",
        width="100%",
    )
