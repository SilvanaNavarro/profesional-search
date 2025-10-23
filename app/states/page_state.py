import reflex as rx
from typing import TypedDict, Literal


class ContactForm(TypedDict):
    name: str
    email: str
    phone: str
    message: str


class LoginState(rx.State):
    email: str = ""
    password: str = ""
    error_message: str = ""

    @rx.event
    async def handle_login(self):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        success = await auth_state.login(self.email, self.password)
        if success:
            self.error_message = ""
            if auth_state.return_url:
                return_url = auth_state.return_url
                async with auth_state:
                    auth_state.return_url = ""
                return rx.redirect(return_url)
            return rx.redirect("/")
        else:
            with rx.session() as session:
                from app.db import User
                from sqlmodel import select

                user = session.exec(
                    select(User).where(User.email == self.email)
                ).first()
                if user and (not user.verified):
                    async with auth_state:
                        auth_state.user_email = self.email
                    await auth_state.send_verification_code()
                    return rx.redirect("/verify-email")
            self.error_message = auth_state.error_message


class ContactState(rx.State):
    form_data: ContactForm = {"name": "", "email": "", "phone": "", "message": ""}
    form_submitted: bool = False

    @rx.event
    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        print(f"Contact form submitted: {self.form_data}")
        self.form_submitted = True
        self.form_data = {"name": "", "email": "", "phone": "", "message": ""}
        return rx.toast.success("¡Mensaje enviado con éxito!")


class SearchState(rx.State):
    professionals: list[dict] = []
    selected_area: str = "Todos"
    AREAS: list[str] = [
        "Todos",
        "Arquitectura",
        "Trabajo Social",
        "Contadores",
        "Abogados",
    ]

    @rx.event
    def load_professionals(self):
        from app.state import professionals_data

        if self.selected_area == "Todos":
            self.professionals = professionals_data
        else:
            self.professionals = [
                p for p in professionals_data if p["area"] == self.selected_area
            ]

    @rx.event
    def set_selected_area(self, area: str):
        self.selected_area = area
        return SearchState.load_professionals