import reflex as rx
import asyncio
import logging
import random
import re
import bcrypt
from app.db import User
from sqlmodel import select


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def is_valid_rut(rut: str) -> bool:
    rut = rut.upper().replace(".", "").replace("-", "")
    if not re.match("^[0-9]{7,8}[0-9K]$", rut):
        return False
    body, verifier = (rut[:-1], rut[-1])
    try:
        reversed_digits = map(int, reversed(body))
        factors = [2, 3, 4, 5, 6, 7, 2, 3]
        s = sum((d * f for d, f in zip(reversed_digits, factors)))
        res = -s % 11
        if str(res) == verifier:
            return True
        elif verifier == "K" and res == 10:
            return True
        return False
    except ValueError as e:
        logging.exception(f"Error validating RUT: {e}")
        return False


class AuthState(rx.State):
    is_logged_in: bool = False
    is_verified: bool = False
    user_email: str = ""
    verification_code: str = ""
    error_message: str = ""
    return_url: str = ""

    @rx.event
    def handle_registration(self, form_data: dict):
        self.error_message = ""
        name = form_data.get("name")
        birthdate = form_data.get("birthdate")
        rut = form_data.get("rut")
        email = form_data.get("email")
        phone = form_data.get("phone")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        if not all([name, birthdate, rut, email, password, confirm_password]):
            self.error_message = "Todos los campos obligatorios deben ser completados."
            return
        if password != confirm_password:
            self.error_message = "Las contraseñas no coinciden."
            return
        if not re.match("[^@]+@[^@]+\\.[^@]+", email):
            self.error_message = "Formato de email inválido."
            return
        if not is_valid_rut(rut):
            self.error_message = "RUT inválido."
            return
        with rx.session() as session:
            existing_email = session.exec(
                select(User).where(User.email == email)
            ).first()
            if existing_email:
                self.error_message = "El email ya está registrado."
                return
            existing_rut = session.exec(select(User).where(User.rut == rut)).first()
            if existing_rut:
                self.error_message = "El RUT ya está registrado."
                return
            new_user = User(
                name=name,
                birthdate=birthdate,
                rut=rut,
                email=email,
                phone=phone,
                password_hash=hash_password(password),
            )
            session.add(new_user)
            session.commit()
        self.user_email = email
        yield AuthState.send_verification_code()
        return rx.redirect("/verify-email")

    @rx.event
    async def login(self, email: str, password: str) -> bool:
        with rx.session() as session:
            user = session.exec(select(User).where(User.email == email)).first()
        if user and check_password(password, user.password_hash):
            self.user_email = user.email
            self.is_logged_in = True
            self.is_verified = user.verified
            self.error_message = ""
            if not self.is_verified:
                await self.send_verification_code()
            return True
        self.error_message = "Email o contraseña incorrectos."
        return False

    @rx.event
    async def send_verification_code(self):
        from app.email_service import send_verification_email

        self.verification_code = str(random.randint(100000, 999999))
        logging.info(
            f"Generated verification code {self.verification_code} for {self.user_email}"
        )
        try:
            success = send_verification_email(self.user_email, self.verification_code)
            if success:
                yield rx.toast.success(
                    f"C\x0800f3digo de verificaci\x0800f3n enviado a {self.user_email}"
                )
            else:
                yield rx.toast.warning(
                    "Servicio de email no configurado. Usando m\x0800e9todo alternativo."
                )
                yield rx.toast.info(
                    f"C\x0800f3digo de verificaci\x0800f3n: {self.verification_code}"
                )
        except Exception as e:
            logging.exception(f"Failed to send verification email: {e}")
            yield rx.toast.error("Error al enviar el email. Int\x0800e9ntalo de nuevo.")
            yield rx.toast.info(
                f"C\x0800f3digo de verificaci\x0800f3n: {self.verification_code}"
            )

    @rx.event
    def verify_email(self, code: str):
        if code == self.verification_code:
            with rx.session() as session:
                user = session.exec(
                    select(User).where(User.email == self.user_email)
                ).first()
                if user:
                    user.verified = True
                    session.add(user)
                    session.commit()
                    self.is_verified = True
                    self.error_message = ""
                    if self.return_url:
                        return_url = self.return_url
                        self.return_url = ""
                        return rx.redirect(return_url)
                    return rx.redirect("/")
                else:
                    self.error_message = "Usuario no encontrado"
        else:
            self.error_message = "Código de verificación incorrecto."
            return rx.toast.error(self.error_message)

    @rx.event
    def logout(self):
        self.is_logged_in = False
        self.is_verified = False
        self.user_email = ""
        self.verification_code = ""
        self.error_message = ""
        return rx.redirect("/")