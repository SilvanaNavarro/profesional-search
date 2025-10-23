import reflex as rx
from app.db import Professional
from sqlmodel import select
from app.states.auth_state import check_password
import logging


class ProfessionalAuthState(rx.State):
    is_logged_in: bool = False
    professional_email: str = ""
    professional_id: int = 0
    professional_name: str = ""
    error_message: str = ""

    @rx.event
    def login(self, form_data: dict):
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.error_message = "Email y contraseña son requeridos."
            return
        with rx.session() as session:
            professional = session.exec(
                select(Professional).where(Professional.email == email)
            ).first()
        if professional and check_password(password, professional.password_hash):
            self.is_logged_in = True
            self.professional_id = professional.id
            self.professional_name = professional.name
            self.professional_email = professional.email
            self.error_message = ""
            return rx.redirect("/professional-dashboard")
        else:
            self.error_message = "Email o contraseña incorrectos."
            return

    @rx.event
    def logout(self):
        self.is_logged_in = False
        self.professional_id = 0
        self.professional_name = ""
        self.professional_email = ""
        self.error_message = ""
        return rx.redirect("/")

    @rx.event
    def check_session(self):
        if not self.is_logged_in:
            return rx.redirect("/login-professional")