import reflex as rx

from peluqueria.styles.styles import Colors


class ServicesState(rx.State):
    list_services: list[dict[str, str]] = [
        {
            "img": "serv_1.webp",
            "title": "Corte y Peinado",
            "text": "Cortes de precisión y peinados adaptados para realzar tus rasgos únicos y tu estilo personal.",
        },
        {
            "img": "serv_2.webp",
            "title": "Color y Mechas",
            "text": "Fórmulas de color personalizadas para crear dimensión, profundidad y resultados vibrantes y duraderos.",
        },
        {
            "img": "serv_3.webp",
            "title": "Tratamiento y Terapia",
            "text": "Tratamientos rejuvenecedores para restaurar la salud del cabello, su brillo y vitalidad usando productos premium.",
        },
        {
            "img": "serv_4.webp",
            "title": "Extensiones",
            "text": "Extensiones de cabello de calidad premium aplicadas con precisión para obtener un largo y volumen de aspecto natural.",
        },
        {
            "img": "serv_5.webp",
            "title": "Servicios para Novias",
            "text": "Paquetes completos para novias que incluyen pruebas, peinado el día de la boda y colocación de accesorios.",
        },
        {
            "img": "serv_6.webp",
            "title": "Tratamiento de Keratina",
            "text": "Tratamientos alisadores que eliminan el frizz y añaden un brillo increíble y facilidad de manejo.",
        },
    ]


def service_card(service) -> rx.Component:
    return rx.card(
        rx.inset(
            rx.image(
                src=f"/img/{service['img']}",
                width="100%",
                height="auto",
            ),
            side="top",
            pb="current",
        ),
        rx.heading(service["title"], as_="h4", size="3"),
        rx.text(service["text"], color=Colors.PARAGRAPH_COLOR.value),
        transition="all 0.3s ease",
        _hover={
            "transform": "scale(1.02)",
        },
    )


def services() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Nuestros ",
            rx.text.span("Servicios ", color=Colors.PRIMARY_COLOR.value),
            "Premium",
            as_="h2",
        ),
        rx.text(
            "Descubre nuestra gama de servicios de peluquería de lujo diseñados para transformar tu imagen y elevar tu confianza",
            color=Colors.PARAGRAPH_COLOR.value,
        ),
        rx.grid(
            rx.foreach(ServicesState.list_services, service_card),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(2, 1fr)",
                "repeat(3, 1fr)",
            ],
        ),
        align="center",
        id="services",
    )
