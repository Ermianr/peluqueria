import reflex as rx

from peluqueria.styles.styles import CUSTOM_INPUT


def form_field(label: str, placeholder: str, type_input, name: str) -> rx.Component:
    return rx.flex(
        rx.el.label(label, html_for=name),
        rx.el.input(
            placeholder=placeholder,
            type=type_input,
            name=name,
            id=name,
            style=CUSTOM_INPUT,
        ),
        direction="column",
        spacing="1",
        width="100%",
    )
