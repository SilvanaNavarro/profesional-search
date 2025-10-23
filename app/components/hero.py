import reflex as rx


def hero_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            class_name="absolute inset-0 bg-gradient-to-r from-blue-50 via-white to-green-50 opacity-80 dark:from-blue-900/50 dark:via-blue-950/80 dark:to-green-900/50"
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
                            class_name="bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold px-8 py-3 rounded-xl shadow-lg hover:from-blue-600 hover:to-green-400 transition-all duration-300 transform hover:scale-105 flex items-center",
                        ),
                        href="/search",
                    ),
                    class_name="mt-10 flex justify-center",
                ),
                class_name="max-w-4xl mx-auto",
            ),
            class_name="relative container mx-auto px-4 sm:px-6 lg:px-8 z-10",
        ),
        class_name="relative flex items-center justify-center min-h-[60vh] py-20 bg-gray-50 dark:bg-blue-950 overflow-hidden",
    )