import reflex as rx

from peluqueria.styles.styles import NAVBAR_LINK


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium", style=NAVBAR_LINK),
        href=url,
        text_decoration="none",
    )
