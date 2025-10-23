import reflex as rx
from app.states.profile_state import BookingState


def login_prompt_modal() -> rx.Component:
    return rx.el.div(
        rx.cond(
            BookingState.show_login_prompt,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "log_in",
                            class_name="h-16 w-16 text-orange-500 mx-auto mb-4",
                        ),
                        rx.el.h2(
                            "Iniciar Sesión para Reservar",
                            class_name="text-2xl font-bold text-gray-800 text-center mb-4",
                        ),
                        rx.el.p(
                            "Para confirmar tu cita, necesitas iniciar sesión o crear una cuenta.",
                            class_name="text-gray-600 text-center mb-6",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Profesional:", class_name="font-medium text-gray-500"
                            ),
                            rx.el.p(
                                BookingState.current_professional["name"],
                                class_name="font-semibold text-gray-800 text-lg",
                            ),
                            rx.el.p(
                                "Fecha:", class_name="font-medium text-gray-500 mt-2"
                            ),
                            rx.el.p(
                                f"⏰ {BookingState.selected_date} a las {BookingState.selected_time}",
                                class_name="font-semibold text-gray-800 text-lg",
                            ),
                            class_name="bg-orange-50 p-4 rounded-xl border border-orange-200 mb-6 text-center",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancelar",
                                on_click=BookingState.close_login_prompt,
                                class_name="bg-gray-200 text-gray-700 font-semibold px-6 py-3 rounded-xl hover:bg-gray-300 transition-colors",
                            ),
                            rx.el.button(
                                "Iniciar Sesión o Registrarse",
                                on_click=BookingState.redirect_to_login,
                                class_name="bg-orange-500 text-white font-semibold px-6 py-3 rounded-xl hover:bg-orange-600 transition-colors shadow-lg",
                            ),
                            class_name="flex justify-center gap-4",
                        ),
                        class_name="bg-white p-8 rounded-2xl shadow-2xl max-w-md mx-auto",
                    ),
                    class_name="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50",
                )
            ),
        )
    )