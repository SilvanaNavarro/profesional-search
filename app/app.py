import reflex as rx
from app.state import State
from app.states.profile_state import BookingState
from app.states.page_state import SearchState
from app.states.payment_state import PaymentState
from app.components.header import header
from app.components.hero import hero_section
from app.components.carousel import professional_carousel
from app.components.video import video_section
from app.pages.profile import profile_page
from app.pages.about import about_page
from app.pages.contact import contact_page
from app.pages.login import login_page
from app.pages.search import search_page
from app.pages.verify_email import verify_email_page


def index() -> rx.Component:
    return rx.el.main(
        header(),
        hero_section(),
        professional_carousel(),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "¿Eres un profesional?",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Únete a nuestra creciente red de expertos y expande tu alcance.",
                        class_name="mt-2 text-lg text-gray-500",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Regístrate como Profesional",
                            rx.icon("user-plus", class_name="ml-2 h-5 w-5"),
                            class_name="mt-6 bg-gray-700 text-white font-semibold px-8 py-3 rounded-xl shadow-lg hover:bg-gray-800 transition-all duration-300 transform hover:scale-105 flex items-center",
                        ),
                        href="/register-professional",
                    ),
                    class_name="text-center",
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8",
            ),
            class_name="py-20 bg-white",
        ),
        video_section(),
        class_name="font-['JetBrains_Mono'] bg-white",
        on_mount=State.rotate_area,
    )


from fastapi import FastAPI

api = FastAPI()


@api.post("/webhook/mercadopago")
def webhook(payload: dict) -> dict:
    import logging
    from app.payment_service import PaymentService
    from app.db import Booking, User, Professional
    from app.email_service import send_booking_confirmation_email
    from sqlmodel import select

    logging.info("Webhook recibido de Mercado Pago")
    if payload.get("type") == "payment":
        payment_id = payload["data"]["id"]
        logging.info(f"Procesando notificacicdn para el pago ID: {payment_id}")
        payment_service = PaymentService()
        payment_info = payment_service.get_payment(payment_id)
        if not payment_info or payment_info["status"] != 200:
            logging.error("No se pudo obtener la informacicdn del pago.")
            return {"status": "error", "message": "Payment not found"}
        payment = payment_info["response"]
        booking_id = payment.get("external_reference")
        payment_status = payment.get("status")
        if not booking_id:
            logging.error("No se encontrcd external_reference en el pago.")
            return {"status": "error", "message": "Missing external reference"}
        with rx.session() as session:
            booking = session.get(Booking, int(booking_id))
            if not booking:
                logging.error(f"No se encontrcd la reserva con ID: {booking_id}")
                return {"status": "error", "message": "Booking not found"}
            if booking.payment_status == "approved":
                logging.warning(
                    f"La reserva {booking_id} ya fue aprobada. Ignorando notificacicdn."
                )
                return {"status": "ok", "message": "Already processed"}
            booking.payment_status = payment_status
            session.add(booking)
            session.commit()
            logging.info(f"Reserva {booking_id} actualizada a estado: {payment_status}")
            if payment_status == "approved":
                user = session.get(User, booking.user_id)
                professional = session.get(Professional, booking.professional_id)
                if user and professional:
                    logging.info(f"Enviando email de confirmacicdn a {user.email}")
                    send_booking_confirmation_email(
                        to_email=user.email,
                        user_name=user.name,
                        professional_name=professional.name,
                        date=booking.date,
                        time=booking.time,
                    )
    return {"status": "ok"}


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
    api_transformer=api,
)
app.add_page(index, route="/")
app.add_page(
    profile_page, route="/profile/[id]", on_load=BookingState.load_professional
)
app.add_page(about_page, route="/about")
app.add_page(contact_page, route="/contact")
app.add_page(login_page, route="/login")
app.add_page(verify_email_page, route="/verify-email")
app.add_page(search_page, route="/search", on_load=SearchState.load_professionals)
from app.pages.register import register_page

app.add_page(register_page, route="/register")
from app.pages.register_professional import register_professional_page

app.add_page(register_professional_page, route="/register-professional")
from app.pages.payment_status import (
    payment_success_page,
    payment_failure_page,
    payment_pending_page,
)

app.add_page(payment_success_page, route="/payment-success")
app.add_page(payment_failure_page, route="/payment-failure")
app.add_page(
    payment_success_page,
    route="/payment-success",
    on_load=PaymentState.load_payment_details,
)
app.add_page(
    payment_failure_page,
    route="/payment-failure",
    on_load=PaymentState.load_payment_details,
)
app.add_page(
    payment_pending_page,
    route="/payment-pending",
    on_load=PaymentState.load_payment_details,
)
from app.db import User, Professional, Booking
from sqlmodel import SQLModel

with rx.session() as session:
    SQLModel.metadata.create_all(session.get_bind())