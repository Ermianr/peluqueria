import httpx
import reflex as rx

from peluqueria.settings import Settings
from peluqueria.views.home.services.services import ServicesState


class AuthState(rx.State):
    access_token: str = rx.Cookie(
        name="plqid",
        path="/",
        max_age=60 * 60 * 24 * 3,
        secure=True,
        same_site="strict",
    )
    is_authenticated: bool = False
    user_data: dict = {}
    loading: bool = False
    loading_auth: bool = True

    @rx.var
    def user_role(self) -> str:
        return self.user_data.get("role", "")

    @rx.var
    def is_customer(self) -> bool:
        return self.user_role == "customer"

    @rx.var
    def is_employee(self) -> bool:
        return self.user_role == "employee"

    # Obtener datos del usuario
    @rx.event
    async def get_user_data(self):
        if not self.access_token:
            self.user_data = {}
            self.is_authenticated = False
            return

        self.loading = True

        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                response = await client.get(
                    "/auth/me",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    timeout=10.0,
                )

                if response.status_code == 200:
                    self.user_data = response.json()
                    self.is_authenticated = True
                else:
                    self.user_data = {}
                    self.is_authenticated = False
                    self.access_token = ""
        except Exception as e:
            print(f"Error obteniendo datos del usuario: {e}")
            self.user_data = {}
            self.is_authenticated = False
            self.access_token = ""
        finally:
            self.loading = False

    @rx.event
    async def login(self, email: str, password: str):
        self.loading = True

        try:
            async with httpx.AsyncClient(base_url=Settings.API_BACKEND_URL) as client:
                form_data = {"username": email, "password": password}

                response = await client.post(
                    "/auth/login",
                    data=form_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10.0,
                )

                if response.status_code == 200:
                    self.user_data = response.json()
                    self.is_authenticated = True
                    self.access_token = self.user_data["access_token"]
                    await self.get_user_data()
                    print(f"Acceso exitoso: {self.user_data}")
                    if self.user_data.get("role") == "customer":
                        yield rx.toast.success("Ingreso exitoso")
                        yield rx.redirect("/citas")
                    else:
                        yield rx.toast.success("Ingreso exitoso")
                        yield rx.redirect("/dashboard")
                else:
                    error_detail = response.json().get("detail", "Error de ingreso")
                    yield rx.toast.error(f"Error: {error_detail}")
                    self.is_authenticated = False
                    self.user_data = {}
        except httpx.RequestError:
            yield rx.toast.error("Error: Error de conexión al servidor")
            self.is_authenticated = False
            self.user_data = {}
        except Exception:
            yield rx.toast.error("Error: Error inesperado")
            self.is_authenticated = False
            self.user_data = {}
        finally:
            self.loading = False

    @rx.event
    async def logout(self):
        self.loading = True
        self.access_token = ""
        rx.remove_cookie("plqid")
        self.user_data = {}
        self.is_authenticated = False
        self.loading = False
        yield rx.toast.success("Sesión cerrada")
        yield rx.redirect("/")

    @rx.event
    async def check_auth(self) -> None:
        await self.get_user_data()

    @rx.event
    def check_auth_protect_login(self):
        self.loading_auth = False
        if self.is_authenticated:
            return rx.redirect("/")

    @rx.event
    async def home_state(self):
        self.check_auth_protect_login()
        get_services = await self.get_state(ServicesState)
        await get_services.get_services()
