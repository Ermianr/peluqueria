import reflex as rx

from peluqueria.styles.styles import CUSTOM_INPUT


def form_field_state(
    label: str,
    placeholder: str,
    type_input,
    name: str,
    initial_error_state: str,
    value: str,
    set_value,
    event,
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
            value=value,
            on_blur=event,
            on_change=set_value,
        ),
        rx.text(error_message, display=initial_error_state, color="red"),
        direction="column",
        spacing="1",
        width="100%",
    )
