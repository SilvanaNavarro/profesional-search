import reflex as rx
from app.states.profile_state import BookingState


def confirmation_modal() -> rx.Component:
    return rx.el.div(
        rx.cond(
            BookingState.show_confirmation,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "check_check",
                            class_name="h-16 w-16 text-green-500 mx-auto mb-4",
                        ),
                        rx.el.h2(
                            "¡Cita Confirmada!",
                            class_name="text-2xl font-bold text-gray-800 text-center mb-4",
                        ),
                        rx.el.p(
                            f"Tu cita con {BookingState.current_professional['name']} ha sido reservada para:",
                            class_name="text-gray-600 text-center mb-2",
                        ),
                        rx.el.div(
                            rx.el.p(
                                f"📅 {BookingState.selected_date}",
                                class_name="text-lg font-semibold text-gray-800",
                            ),
                            rx.el.p(
                                f"🕒 {BookingState.selected_time}",
                                class_name="text-lg font-semibold text-gray-800",
                            ),
                            class_name="bg-green-50 p-4 rounded-xl border border-green-200 mb-6 text-center",
                        ),
                        rx.el.p(
                            "Recibirás un email de confirmación con todos los detalles.",
                            class_name="text-sm text-gray-500 text-center mb-6",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cerrar",
                                on_click=BookingState.close_confirmation,
                                class_name="bg-orange-500 text-white font-semibold px-8 py-3 rounded-xl hover:bg-orange-600 transition-colors shadow-lg",
                            ),
                            class_name="text-center",
                        ),
                        class_name="bg-white p-8 rounded-2xl shadow-2xl max-w-md mx-auto",
                    ),
                    class_name="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50",
                )
            ),
        )
    )