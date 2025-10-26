import reflex as rx
from app.state import State
from app.states.theme_state import ThemeState
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
                        class_name="text-3xl font-bold text-gray-800 dark:text-white",
                    ),
                    rx.el.p(
                        "Ùnete a nuestra creciente red de expertos y expande tu alcance.",
                        class_name="mt-2 text-lg text-gray-500 dark:text-gray-300",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Regístrate como Profesional",
                            rx.icon("user-plus", class_name="ml-2 h-5 w-5"),
                            class_name="mt-6 bg-gradient-to-r from-blue-800 to-green-500 text-white font-semibold px-8 py-3 rounded-xl shadow-lg hover:from-blue-700 hover:to-green-400 transition-all duration-300 transform hover:scale-105 flex items-center",
                        ),
                        href="/register-professional",
                    ),
                    class_name="text-center bg-white dark:bg-gray-800 p-10 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700",
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8",
            ),
            class_name="py-20 bg-gray-50 dark:bg-blue-900",
        ),
        video_section(),
        class_name="font-['JetBrains_Mono'] bg-white dark:bg-blue-950",
        on_mount=State.rotate_area,
    )


from fastapi import FastAPI
from app.api import webhook_router

api = FastAPI()
api.include_router(webhook_router.router, prefix="/webhook", tags=["MercadoPago"])
app = rx.App(
    theme=rx.theme(appearance="light", accent_color="grass"),
    stylesheets=["/styles.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(
    profile_page, route="/profile/[id]", on_load=BookingState.load_professional
)
app.add_page(about_page, route="/about")
app.add_page(contact_page, route="/contact")
app.add_page(login_page, route="/login")
from app.pages.login_professional import login_professional_page

app.add_page(login_professional_page, route="/login-professional")
from app.pages.professional_dashboard import professional_dashboard_page
from app.states.professional_dashboard_state import DashboardState
from app.states.schedule_state import ScheduleManagementState
from app.states.review_state import ReviewState
from app.states.profile_settings_state import ProfileSettingsState
from app.states.subscription_state import SubscriptionState

app.add_page(
    professional_dashboard_page,
    route="/professional-dashboard",
    on_load=[
        DashboardState.load_dashboard_data,
        ScheduleManagementState.load_schedule_data,
        ReviewState.on_dashboard_load,
        ProfileSettingsState.load_professional_data,
        SubscriptionState.load_subscription_data,
    ],
)
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
from app.db import (
    User,
    Professional,
    Booking,
    ProfessionalAvailability,
    Review,
    Subscription,
    ProfessionalMedia,
)
from sqlmodel import SQLModel
import os

if os.path.exists("reflex.db"):
    os.remove("reflex.db")
with rx.session() as session:
    SQLModel.metadata.create_all(session.get_bind())