import reflex as rx

from peluqueria.state.global_state import AuthState
from peluqueria.styles.styles import SOLID_BUTTON


class RouteGuardType:
    ANONYMOUS_ONLY = "anonymous_only"
    AUTHENTICATED_ONLY = "authenticated_only"
    EMPLOYEE_ONLY = "employee_only"


def route_guard(
    protected_content: rx.Component,
    guard_type: str = RouteGuardType.AUTHENTICATED_ONLY,
    redirect_path: str = "/ingreso",
    title: str = "Acceso Restringido",
    message: str = "No tienes permisos para acceder a esta página",
    button_text: str = "Iniciar Sesión",
) -> rx.Component:
    def get_guard_condition():
        if guard_type == RouteGuardType.ANONYMOUS_ONLY:
            return ~AuthState.is_authenticated
        if guard_type == RouteGuardType.EMPLOYEE_ONLY:
            return AuthState.is_authenticated & AuthState.is_employee
        return AuthState.is_authenticated

    def get_access_denied_content() -> rx.Component:
        return rx.flex(
            rx.flex(
                rx.flex(
                    rx.heading(title, as_="h1"),
                    justify="center",
                    align="center",
                    width="100%",
                ),
                rx.text(
                    message,
                    text_align="center",
                ),
                rx.button(
                    button_text,
                    style=SOLID_BUTTON,
                    padding_y="0.5rem",
                    margin_top="1rem",
                    on_click=rx.redirect(redirect_path),
                ),
                padding="2rem",
                direction="column",
                text_align="center",
                align="center",
            ),
            width="100%",
            direction="column",
            spacing="2",
            padding_x="4rem",
            padding_y="2rem",
            justify="center",
            align="center",
            min_height="60vh",
        )

    return rx.cond(
        get_guard_condition(),
        protected_content,
        get_access_denied_content(),
    )


def anonymous_only_guard(
    protected_content: rx.Component,
    redirect_path: str = "/dashboard",
    title: str = "Ya tienes sesión iniciada",
    message: str = "Ya has iniciado sesión. Serás redirigido.",
    button_text: str = "Ir al Dashboard",
) -> rx.Component:
    return route_guard(
        protected_content=protected_content,
        guard_type=RouteGuardType.ANONYMOUS_ONLY,
        redirect_path=redirect_path,
        title=title,
        message=message,
        button_text=button_text,
    )


def authenticated_only_guard(
    protected_content: rx.Component,
    redirect_path: str = "/ingreso",
    title: str = "Acceso Restringido",
    message: str = "Debe iniciar sesión para acceder a esta página",
    button_text: str = "Iniciar Sesión",
) -> rx.Component:
    return route_guard(
        protected_content=protected_content,
        guard_type=RouteGuardType.AUTHENTICATED_ONLY,
        redirect_path=redirect_path,
        title=title,
        message=message,
        button_text=button_text,
    )


def employee_only_guard(
    protected_content: rx.Component,
    redirect_path: str = "/",
    title: str = "Acceso Solo para Empleados",
    message: str = "Solo los empleados pueden acceder a esta página",
    button_text: str = "Volver al Inicio",
) -> rx.Component:
    return route_guard(
        protected_content=protected_content,
        guard_type=RouteGuardType.EMPLOYEE_ONLY,
        redirect_path=redirect_path,
        title=title,
        message=message,
        button_text=button_text,
    )


def customer_restricted_guard(
    protected_content: rx.Component,
    redirect_path: str = "/",
    title: str = "Acceso Restringido",
    message: str = "Los clientes no pueden acceder a esta página",
    button_text: str = "Volver al Inicio",
) -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated & (~AuthState.is_customer),
        protected_content,
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.heading(title, as_="h1"),
                    justify="center",
                    align="center",
                    width="100%",
                ),
                rx.text(
                    message,
                    text_align="center",
                ),
                rx.button(
                    button_text,
                    style=SOLID_BUTTON,
                    padding_y="0.5rem",
                    margin_top="1rem",
                    on_click=rx.redirect(redirect_path),
                ),
                padding="2rem",
                direction="column",
                text_align="center",
                align="center",
            ),
            width="100%",
            direction="column",
            spacing="2",
            padding_x="4rem",
            padding_y="2rem",
            justify="center",
            align="center",
            min_height="60vh",
        ),
    )
