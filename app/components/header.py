import reflex as rx
from app.states.theme_state import ThemeState


def header() -> rx.Component:
    nav_links = [
        {"name": "Sobre Nosotros", "href": "/about"},
        {"name": "Contáctanos", "href": "/contact"},
        {"name": "¿Eres Profesional?", "href": "/register-professional"},
        {"name": "Buscar Profesionales", "href": "/search"},
    ]
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon(
                        "briefcase",
                        class_name="h-8 w-8 text-blue-600 dark:text-blue-400",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "ProfessionalBook",
                            class_name="text-xl font-bold text-gray-800 dark:text-white",
                        ),
                        rx.el.span(
                            "Conectamos talento con oportunidades",
                            class_name="text-xs text-gray-500 dark:text-gray-400",
                        ),
                        class_name="flex flex-col ml-2",
                    ),
                    class_name="flex items-center",
                ),
                href="/",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.foreach(
                        nav_links,
                        lambda link: rx.el.a(
                            link["name"],
                            href=link["href"],
                            class_name="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors px-3 py-2 rounded-md",
                        ),
                    ),
                    rx.el.button(
                        rx.icon(
                            rx.color_mode_cond("moon", "sun"), class_name="h-5 w-5"
                        ),
                        on_click=rx.toggle_color_mode,
                        class_name="p-2 rounded-md text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700",
                    ),
                    rx.el.a(
                        rx.icon("user", class_name="h-4 w-4 mr-2"),
                        "Log in",
                        href="/login",
                        class_name="flex items-center bg-gradient-to-r from-blue-800 to-green-500 text-white font-semibold px-4 py-2 rounded-lg hover:from-blue-700 hover:to-green-400 transition-colors shadow-sm",
                    ),
                    class_name="hidden md:flex items-center space-x-4",
                ),
                rx.el.button(
                    rx.icon("menu", class_name="h-6 w-6"),
                    class_name="md:hidden p-2 rounded-md text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700",
                ),
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-20",
        ),
        class_name="bg-white/80 dark:bg-blue-900/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-200 dark:border-gray-700",
    )