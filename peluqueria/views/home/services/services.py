import os

import httpx
import reflex as rx

from peluqueria.settings import Settings
from peluqueria.styles.styles import Colors


class ServicesState(rx.State):
    list_services: list[dict[str, str]] = []

    @rx.event
    async def get_services(self):
        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.get("/services")
                if response.status_code == 200:
                    self.list_services = [
                        {
                            "title": service["name"],
                            "text": service["description"],
                            "img": os.path.basename(service["img_path"]),
                        }
                        for service in response.json()
                    ]
                else:
                    print(f"Error al cargar los servicios: {response.status_code}")
        except httpx.RequestError:
            print("Error de conexión al servidor")
        except Exception:
            print("Error inesperado al cargar los servicios")


def service_card(service) -> rx.Component:
    return rx.card(
        rx.inset(
            rx.image(
                src=rx.get_upload_url(service["img"]),
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
