import reflex as rx

from peluqueria.styles.styles import NAVBAR_LINK


class NavbarLinkState(rx.State):
    @rx.event
    async def go_to_section(self, section: str):
        return rx.redirect(section)


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium", style=NAVBAR_LINK),
        on_click=NavbarLinkState.go_to_section(url),
    )
