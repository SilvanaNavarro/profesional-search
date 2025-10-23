import reflex as rx
from app.payment_service import PaymentService, ProfessionalInfo, UserInfo
from app.db import User, Booking
from sqlmodel import select
import logging


class PaymentState(rx.State):
    processing_payment: bool = False
    payment_details: dict = {}

    @rx.event
    async def create_checkout_session(self, booking_id: int, price: float):
        from app.states.auth_state import AuthState
        from app.states.profile_state import BookingState

        self.processing_payment = True
        auth_state = await self.get_state(AuthState)
        booking_state = await self.get_state(BookingState)
        if not auth_state.is_logged_in or not booking_state.current_professional:
            self.processing_payment = False
            yield rx.toast.error("Error: Debes iniciar sesión.")
            return
        with rx.session() as session:
            user = session.exec(
                select(User).where(User.email == auth_state.user_email)
            ).first()
            booking = session.get(Booking, booking_id)
        if not user or not booking:
            self.processing_payment = False
            yield rx.toast.error("Error al obtener datos de usuario o reserva.")
            return
        professional_info = ProfessionalInfo(
            name=booking_state.current_professional["name"],
            title=booking_state.current_professional["title"],
        )
        user_info = UserInfo(name=user.name, email=user.email)
        payment_service = PaymentService()
        preference = payment_service.create_payment_preference(
            booking_id=booking_id,
            professional_info=professional_info,
            user_info=user_info,
            price=price,
        )
        if preference and "init_point" in preference:
            booking.payment_id = preference["id"]
            with rx.session() as session:
                session.add(booking)
                session.commit()
            init_point = preference.get(
                "sandbox_init_point", preference.get("init_point")
            )
            self.processing_payment = False
            yield rx.redirect(init_point)
            return
        else:
            self.processing_payment = False
            yield rx.toast.error(
                "No se pudo iniciar el proceso de pago. Intenta de nuevo."
            )
            return

    @rx.event
    def load_payment_details(self):
        booking_id = self.router.page.params.get("external_reference")
        if not booking_id:
            return
        with rx.session() as session:
            booking = session.get(Booking, int(booking_id))
            if booking:
                professional = session.get(Professional, booking.professional_id)
                user = session.get(User, booking.user_id)
                self.payment_details = {
                    "professional_name": professional.name if professional else "N/A",
                    "user_name": user.name if user else "N/A",
                    "date": booking.date,
                    "time": booking.time,
                    "status": booking.payment_status,
                }