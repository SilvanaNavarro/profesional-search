import reflex as rx
from app.components.header import header
from app.states.page_state import ContactState


def contact_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Ponte en Contacto",
                        class_name="text-4xl md:text-5xl font-extrabold text-gray-800 text-center",
                    ),
                    rx.el.p(
                        "¿Tienes preguntas o sugerencias? Estamos aquí para ayudarte.",
                        class_name="mt-4 max-w-xl mx-auto text-center text-lg text-gray-600 font-medium",
                    ),
                ),
                rx.el.div(
                    rx.el.form(
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Nombre Completo",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    placeholder="Tu nombre",
                                    name="name",
                                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Email",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    placeholder="tu@email.com",
                                    name="email",
                                    type="email",
                                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Teléfono (Opcional)",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    placeholder="+56 9 1234 5678",
                                    name="phone",
                                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Mensaje",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.textarea(
                                    placeholder="Escribe tu mensaje aquí...",
                                    name="message",
                                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 h-32 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                                ),
                            ),
                            rx.el.button(
                                "Enviar Mensaje",
                                type="submit",
                                class_name="w-full bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold px-6 py-3 rounded-xl hover:from-blue-600 hover:to-green-400 transition-colors shadow-lg",
                            ),
                            class_name="space-y-6",
                        ),
                        on_submit=ContactState.handle_submit,
                        reset_on_submit=True,
                        class_name="mt-12",
                    ),
                    class_name="max-w-xl mx-auto",
                ),
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-16",
        ),
        class_name="font-['JetBrains_Mono'] bg-white dark:bg-blue-950 min-h-screen",
    )