import reflex as rx
from app.db import Professional
from app.states.professional_auth_state import ProfessionalAuthState
from app.states.auth_state import hash_password, check_password
import logging


class ProfileSettingsState(rx.State):
    professional: Professional | None = None
    new_description: str = ""
    current_password: str = ""
    new_password: str = ""
    confirm_new_password: str = ""
    error_message: str = ""
    success_message: str = ""

    @rx.event
    async def load_professional_data(self):
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in:
            return
        with rx.session() as session:
            self.professional = session.get(Professional, auth_state.professional_id)
            if self.professional:
                self.new_description = self.professional.description_services

    @rx.event
    async def handle_profile_pic_upload(self, files: list[rx.UploadFile]):
        auth_state = await self.get_state(ProfessionalAuthState)
        if not files or not auth_state.is_logged_in:
            return
        file = files[0]
        upload_data = await file.read()
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.name
        with file_path.open("wb") as f:
            f.write(upload_data)
        with rx.session() as session:
            db_professional = session.get(Professional, auth_state.professional_id)
            if db_professional:
                db_professional.photo_profile_path = file.name
                session.add(db_professional)
                session.commit()
                session.refresh(db_professional)
                self.professional = db_professional
        yield rx.toast.success("Foto de perfil actualizada.")
        yield rx.clear_selected_files("profile_photo_upload")

    @rx.event
    async def save_description(self):
        self.error_message = ""
        self.success_message = ""
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in or not self.professional:
            self.error_message = "No estás autenticado."
            return
        with rx.session() as session:
            db_professional = session.get(Professional, self.professional.id)
            if db_professional:
                db_professional.description_services = self.new_description
                session.add(db_professional)
                session.commit()
                session.refresh(db_professional)
                self.professional = db_professional
                self.success_message = "Descripción actualizada con éxito."
                yield rx.toast.success(self.success_message)
            else:
                self.error_message = "No se pudo encontrar al profesional."
                yield rx.toast.error(self.error_message)

    @rx.event
    async def change_password(self):
        self.error_message = ""
        self.success_message = ""
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in or not self.professional:
            self.error_message = "No estás autenticado."
            return
        if self.new_password != self.confirm_new_password:
            self.error_message = "Las nuevas contraseñas no coinciden."
            yield rx.toast.error(self.error_message)
            return
        if not check_password(self.current_password, self.professional.password_hash):
            self.error_message = "La contraseña actual es incorrecta."
            yield rx.toast.error(self.error_message)
            return
        with rx.session() as session:
            db_professional = session.get(Professional, self.professional.id)
            if db_professional:
                db_professional.password_hash = hash_password(self.new_password)
                session.add(db_professional)
                session.commit()
                self.success_message = "Contraseña cambiada con éxito."
                self.current_password = ""
                self.new_password = ""
                self.confirm_new_password = ""
                yield rx.toast.success(self.success_message)
            else:
                self.error_message = "No se pudo encontrar al profesional."
                yield rx.toast.error(self.error_message)