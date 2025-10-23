import reflex as rx
import logging
import re
from app.db import Professional
from app.states.auth_state import is_valid_rut
from sqlmodel import select
import asyncio


class ProfessionalRegisterState(rx.State):
    form_data: dict = {}
    error_message: str = ""
    processing: bool = False
    photo_profile_path: str = ""
    photo_id_card_path: str = ""
    certificate_path: str = ""

    @rx.event
    async def handle_registration(self, form_data: dict):
        self.processing = True
        self.error_message = ""
        self.form_data = form_data
        name = form_data.get("name")
        career = form_data.get("career")
        rut = form_data.get("rut")
        description = form_data.get("description_services")
        if not all([name, career, rut, description]):
            self.error_message = "Todos los campos de texto son obligatorios."
            self.processing = False
            return
        if not is_valid_rut(rut):
            self.error_message = "El RUT ingresado no es válido."
            self.processing = False
            return
        if (
            not self.photo_profile_path
            or not self.photo_id_card_path
            or (not self.certificate_path)
        ):
            self.error_message = "Debe subir todos los archivos requeridos."
            self.processing = False
            return
        with rx.session() as session:
            existing_rut = session.exec(
                select(Professional).where(Professional.rut == rut)
            ).first()
            if existing_rut:
                self.error_message = "El RUT ya está registrado como profesional."
                self.processing = False
                return
            new_professional = Professional(
                name=name,
                career=career,
                rut=rut,
                description_services=description,
                photo_profile_path=self.photo_profile_path,
                photo_id_card_path=self.photo_id_card_path,
                certificate_path=self.certificate_path,
            )
            session.add(new_professional)
            session.commit()
        yield rx.toast.success("Registro enviado. Será revisado por un administrador.")
        self.form_data = {}
        self.photo_profile_path = ""
        self.photo_id_card_path = ""
        self.certificate_path = ""
        self.processing = False
        yield rx.redirect("/")
        return

    async def _handle_upload(self, files: list[rx.UploadFile], field_to_update: str):
        if not files:
            yield rx.toast.error("No se seleccionó ningún archivo.")
            return
        file = files[0]
        upload_data = await file.read()
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.name
        with file_path.open("wb") as f:
            f.write(upload_data)
        if field_to_update == "profile":
            self.photo_profile_path = file.name
        elif field_to_update == "id_card":
            self.photo_id_card_path = file.name
        elif field_to_update == "certificate":
            self.certificate_path = file.name
        yield rx.toast.success(f"Archivo '{file.name}' subido con éxito.")
        if field_to_update == "profile":
            yield rx.clear_selected_files("profile_pic")
        elif field_to_update == "id_card":
            yield rx.clear_selected_files("id_card")
        elif field_to_update == "certificate":
            yield rx.clear_selected_files("certificate")

    @rx.event
    async def handle_profile_pic_upload(self, files: list[rx.UploadFile]):
        async for event in self._handle_upload(files, "profile"):
            yield event

    @rx.event
    async def handle_id_card_upload(self, files: list[rx.UploadFile]):
        async for event in self._handle_upload(files, "id_card"):
            yield event

    @rx.event
    async def handle_certificate_upload(self, files: list[rx.UploadFile]):
        async for event in self._handle_upload(files, "certificate"):
            yield event