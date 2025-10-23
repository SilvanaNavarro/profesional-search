import reflex as rx


def hero_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            class_name="absolute inset-0 bg-gradient-to-r from-orange-50 via-white to-orange-50 opacity-80"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Encuentra y Reserva Profesionales de Confianza",
                    class_name="text-4xl md:text-5xl lg:text-6xl font-extrabold text-gray-800 text-center leading-tight",
                ),
                rx.el.p(
                    "Accede a una red exclusiva de expertos en Arquitectura, Trabajo Social, Contabilidad y Derecho. Agenda tu cita de forma rápida, segura y sencilla.",
                    class_name="mt-6 max-w-2xl mx-auto text-center text-lg text-gray-600 font-medium",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.el.button(
                            "Buscar un Profesional",
                            rx.icon("search", class_name="ml-2 h-5 w-5"),
                            class_name="bg-orange-500 text-white font-semibold px-8 py-3 rounded-xl shadow-lg hover:bg-orange-600 transition-all duration-300 transform hover:scale-105 flex items-center",
                        ),
                        href="/search",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Regístrate como Profesional",
                            rx.icon("user-plus", class_name="ml-2 h-5 w-5"),
                            class_name="bg-gray-700 text-white font-semibold px-8 py-3 rounded-xl shadow-lg hover:bg-gray-800 transition-all duration-300 transform hover:scale-105 flex items-center",
                        ),
                        href="/register-professional",
                    ),
                    class_name="mt-10 flex flex-col sm:flex-row justify-center items-center gap-4",
                ),
                class_name="max-w-4xl mx-auto",
            ),
            class_name="relative container mx-auto px-4 sm:px-6 lg:px-8 z-10",
        ),
        class_name="relative flex items-center justify-center min-h-[60vh] py-20 bg-gray-50 overflow-hidden",
    )