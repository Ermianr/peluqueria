import reflex as rx

from peluqueria.styles.styles import Colors


class AboutBadgesState(rx.State):
    list_badges: list[dict[str, str]] = [
        {"icon": "medal", "title": "Excelencia", "text": "Servicio premiado"},
        {
            "icon": "user-round",
            "title": "Experiencia",
            "text": "Profesionales certificados",
        },
        {"icon": "heart", "title": "Ambiente", "text": "Atmosfera de lujo"},
    ]


def badge(badges) -> rx.Component:
    return rx.hstack(
        rx.flex(
            rx.icon(badges["icon"], color=Colors.CUSTOM_WHITE.value),
            padding="1rem",
            border_radius="50%",
            bg=Colors.PRIMARY_COLOR.value,
            align="center",
        ),
        rx.box(
            rx.heading(badges["title"], as_="h4", size="4"),
            rx.text(badges["text"]),
        ),
        align="center",
    )


def about() -> rx.Component:
    return rx.flex(
        rx.image(
            src="/img/team.webp",
            width="100%",
            height="auto",
            border_radius="1rem",
        ),
        rx.vstack(
            rx.heading(
                "Sobre ",
                rx.text.span("Nuestro Salón", color=Colors.PRIMARY_COLOR.value),
                color="black",
                as_="h2",
            ),
            rx.text(
                "Fundado en 2010, nuestro salón se ha establecido como un destino de primer nivel para quienes buscan servicios excepcionales de peluquería en un ambiente lujoso. Creemos que cada cliente merece una atención personalizada y resultados que superen sus expectativas.",
                color=Colors.PARAGRAPH_COLOR.value,
            ),
            rx.text(
                "Nuestro equipo de estilistas altamente capacitados combina la experiencia técnica con la visión artística para crear looks que realzan tu belleza natural mientras reflejan tu estilo personal. Nos educamos continuamente en las últimas técnicas y tendencias para ofrecerte lo mejor en cuidado del cabello.",
                color=Colors.PARAGRAPH_COLOR.value,
            ),
            rx.heading("Nuestra misión", as_="h3"),
            rx.text(
                "Transformar no solo tu cabello, sino también tu confianza a través de un servicio excepcional, excelencia técnica y un compromiso de crear una experiencia relajante y rejuvenecedora para cada cliente que cruza nuestras puertas.",
                color=Colors.PARAGRAPH_COLOR.value,
            ),
            rx.grid(
                rx.foreach(
                    AboutBadgesState.list_badges,
                    badge,
                ),
                gap="1rem",
                grid_template_columns=[
                    "1fr",
                    "repeat(2, 1fr)",
                    "repeat(3, 1fr)",
                ],
            ),
            width="85%",
        ),
        align="center",
        spacing="6",
        direction=rx.breakpoints(
            initial="column",
            md="row",
        ),
    )
