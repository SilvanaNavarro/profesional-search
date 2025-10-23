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
    all_professionals_db: list[dict] = []
    selected_area: str = "Todos"
    search_name: str = ""
    search_city: str = ""
    search_radius: int = 50
    AREAS: list[str] = [
        "Todos",
        "Arquitectura",
        "Trabajo Social",
        "Contadores",
        "Abogados",
    ]

    @rx.var
    def cities(self) -> list[str]:
        if not self.all_professionals_db:
            self.load_professionals()
        all_cities = {p.get("city") for p in self.all_professionals_db if p.get("city")}
        return sorted(list(all_cities))

    @rx.event
    def load_professionals(self):
        from app.state import map_professional_to_dict, professionals_data
        from app.db import Professional as ProfessionalDB
        from sqlmodel import select

        if not self.all_professionals_db:
            with rx.session() as session:
                db_professionals = session.exec(
                    select(ProfessionalDB).where(ProfessionalDB.verified == True)
                ).all()
                if db_professionals:
                    self.all_professionals_db = [
                        map_professional_to_dict(p) for p in db_professionals
                    ]
                else:
                    self.all_professionals_db = professionals_data
        temp_professionals = self.all_professionals_db
        if self.selected_area != "Todos":
            temp_professionals = [
                p for p in temp_professionals if p["area"] == self.selected_area
            ]
        if self.search_name:
            temp_professionals = [
                p
                for p in temp_professionals
                if self.search_name.lower() in p["name"].lower()
            ]
        if self.search_city:
            temp_professionals = [
                p for p in temp_professionals if p.get("city") == self.search_city
            ]
        self.professionals = temp_professionals

    @rx.event
    def set_selected_area(self, area: str):
        self.selected_area = area
        self.load_professionals()

    @rx.event
    def set_search_name(self, name: str):
        self.search_name = name
        self.load_professionals()

    @rx.event
    def set_search_city(self, city: str):
        self.search_city = city
        self.load_professionals()

    @rx.event
    def set_search_radius(self, radius: list[int]):
        self.search_radius = radius[0]

    @rx.event
    def clear_filters(self):
        self.selected_area = "Todos"
        self.search_name = ""
        self.search_city = ""
        self.search_radius = 50
        self.load_professionals()