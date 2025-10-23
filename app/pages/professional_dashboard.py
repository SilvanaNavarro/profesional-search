import reflex as rx
from app.states.professional_auth_state import ProfessionalAuthState
from app.states.professional_dashboard_state import DashboardState
from app.components.schedule_view import schedule_view
from app.components.review_view import reviews_view
from app.components.profile_settings_view import profile_settings_view
from app.components.subscription_view import subscription_view


def dashboard_sidebar() -> rx.Component:
    nav_items = [
        {"label": "Dashboard", "icon": "layout-dashboard", "view": "dashboard"},
        {"label": "Agenda", "icon": "calendar", "view": "schedule"},
        {"label": "Reseñas", "icon": "star", "view": "reviews"},
        {"label": "Perfil", "icon": "user-circle", "view": "profile"},
        {"label": "Plan y Suscripción", "icon": "credit-card", "view": "subscription"},
    ]
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("briefcase", class_name="h-8 w-8 text-blue-600"),
                        rx.el.span("Panel Profesional", class_name="text-lg font-bold"),
                        class_name="flex items-center gap-3",
                    ),
                    href="/professional-dashboard",
                ),
                class_name="flex h-20 items-center border-b px-6",
            ),
            rx.el.nav(
                rx.foreach(
                    nav_items,
                    lambda item: rx.el.button(
                        rx.icon(item["icon"], class_name="h-5 w-5 mr-3"),
                        item["label"],
                        on_click=lambda: DashboardState.set_current_view(item["view"]),
                        class_name=rx.cond(
                            DashboardState.current_view == item["view"],
                            "flex items-center w-full text-left px-3 py-2.5 rounded-lg text-white bg-gradient-to-r from-blue-700 to-green-500 font-semibold shadow-md",
                            "flex items-center w-full text-left px-3 py-2.5 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 font-medium transition-colors",
                        ),
                    ),
                ),
                class_name="flex flex-col gap-2 p-4",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("log-out", class_name="h-5 w-5 mr-3"),
                    "Cerrar Sesión",
                    on_click=ProfessionalAuthState.logout,
                    class_name="flex items-center w-full text-left px-3 py-2.5 rounded-lg text-gray-600 hover:bg-red-50 hover:text-red-600 font-medium transition-colors",
                ),
                class_name="mt-auto p-4 border-t",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex flex-col w-64 border-r bg-white dark:bg-gray-900",
    )


def metric_card(icon: str, title: str, value: rx.Var, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-8 w-8 {color}"),
            class_name="p-3 bg-gray-100 rounded-full",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-3xl font-bold text-gray-800"),
            class_name="mt-2",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-md border border-gray-100 hover:shadow-lg transition-shadow",
    )


def dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            f"Bienvenido, {ProfessionalAuthState.professional_name}!",
            class_name="text-3xl font-bold text-gray-800 mb-8",
        ),
        rx.el.div(
            metric_card(
                "calendar-check",
                "Citas Confirmadas",
                DashboardState.total_bookings.to_string(),
                "text-green-500",
            ),
            metric_card(
                "clock",
                "Pendientes (Semana)",
                DashboardState.pending_bookings_week.to_string(),
                "text-yellow-500",
            ),
            metric_card(
                "star",
                "Valoración Promedio",
                DashboardState.average_rating.to_string(),
                "text-blue-500",
            ),
            metric_card(
                "message-square",
                "Total Reseñas",
                DashboardState.total_reviews.to_string(),
                "text-indigo-500",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        class_name="p-8",
    )


def professional_dashboard_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            dashboard_sidebar(),
            rx.el.div(
                rx.match(
                    DashboardState.current_view,
                    ("dashboard", dashboard_view()),
                    ("schedule", schedule_view()),
                    ("reviews", reviews_view()),
                    ("profile", profile_settings_view()),
                    ("subscription", subscription_view()),
                    rx.el.div(rx.el.p("Vista no implementada"), class_name="p-8"),
                ),
                class_name="flex-1 bg-gray-50 overflow-auto",
            ),
            class_name="flex h-screen font-['JetBrains_Mono'] bg-white",
        ),
        on_mount=ProfessionalAuthState.check_session,
    )