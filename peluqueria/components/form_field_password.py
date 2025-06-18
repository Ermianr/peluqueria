import reflex as rx

from peluqueria.styles.styles import CUSTOM_INPUT


def form_field_password(
    label,
    placeholder: str,
    type_input,
    name: str,
    error_state: str,
    error_message: str,
) -> rx.Component:
    return rx.flex(
        rx.el.label(label, html_for=name),
        rx.el.input(
            placeholder=placeholder,
            type=type_input,
            name=name,
            id=name,
            style=CUSTOM_INPUT,
        ),
        rx.text(error_message, display=error_state, color="red"),
        direction="column",
        spacing="1",
        width="100%",
    )
