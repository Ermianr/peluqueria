import reflex as rx

from peluqueria.state.global_state import AuthState


def protect_auth_login(page: rx.Component):
    return rx.cond(
        AuthState.loading_auth,
        rx.fragment(),
        rx.cond(
            AuthState.is_authenticated,
            rx.fragment(),
            page,
        ),
    )
