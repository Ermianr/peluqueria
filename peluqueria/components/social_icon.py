import reflex as rx

from peluqueria.styles.styles import Colors


def social_icon(icon: str) -> rx.Component:
    return rx.flex(
        rx.icon(
            icon,
            size=18,
        ),
        padding="0.5rem",
        cursor="pointer",
        border_radius="50%",
        border=f"1px solid {Colors.PARAGRAPH_COLOR.value}",
        color=Colors.PARAGRAPH_COLOR.value,
        transition="all 0.3s ease",
        _hover={
            "background": Colors.PRIMARY_COLOR.value,
            "border": f"1px solid {Colors.PRIMARY_COLOR.value}",
            "color": Colors.CUSTOM_WHITE.value,
        },
        align="center"
    )
    