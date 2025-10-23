import reflex as rx
from app.states.profile_state import BookingState
from app.components.header import header
from app.components.calendar import calendar_component
from app.components.confirmation_modal import confirmation_modal
from app.components.login_prompt_modal import login_prompt_modal


def profile_page() -> rx.Component:
    return rx.el.main(
        header(),
        confirmation_modal(),
        login_prompt_modal(),
        rx.el.div(
            rx.cond(
                BookingState.current_professional,
                rx.el.div(
                    rx.el.div(
                        rx.el.button(
                            rx.icon("arrow-left", class_name="h-5 w-5 mr-2"),
                            "Volver",
                            on_click=rx.redirect("/"),
                            class_name="flex items-center text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 font-medium mb-6 transition-colors",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "user", class_name="h-32 w-32 text-white/60"
                                    ),
                                    class_name="w-full h-64 bg-gradient-to-br from-gray-200 to-gray-400 rounded-2xl flex items-center justify-center mb-6",
                                ),
                                class_name="md:w-1/3",
                            ),
                            rx.el.div(
                                rx.el.h1(
                                    BookingState.current_professional["name"],
                                    class_name="text-3xl font-bold text-gray-800 mb-2",
                                ),
                                rx.el.p(
                                    BookingState.current_professional["title"],
                                    class_name="text-lg font-medium text-blue-600 dark:text-blue-400 mb-4",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        BookingState.current_professional["area"],
                                        class_name="inline-block bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium dark:bg-blue-900 dark:text-blue-300",
                                    ),
                                    class_name="mb-6",
                                ),
                                rx.el.p(
                                    BookingState.current_professional["description"],
                                    class_name="text-gray-600 leading-relaxed",
                                ),
                                class_name="md:w-2/3 md:pl-8",
                            ),
                            class_name="flex flex-col md:flex-row items-start mb-12",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "Reservar una cita",
                                class_name="text-2xl font-bold text-gray-800 mb-6",
                            ),
                            calendar_component(),
                        ),
                        class_name="max-w-4xl mx-auto",
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Profesional no encontrado",
                            class_name="text-2xl font-bold text-gray-800 mb-4",
                        ),
                        rx.el.p(
                            "El profesional que buscas no existe o no está disponible.",
                            class_name="text-gray-600 mb-6",
                        ),
                        rx.el.button(
                            "Volver al inicio",
                            on_click=rx.redirect("/"),
                            class_name="bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold px-6 py-3 rounded-xl hover:from-blue-600 hover:to-green-400 transition-colors",
                        ),
                        class_name="text-center max-w-md mx-auto",
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-20",
                ),
            )
        ),
        class_name="font-['JetBrains_Mono'] bg-gray-50 dark:bg-blue-950 min-h-screen",
    )