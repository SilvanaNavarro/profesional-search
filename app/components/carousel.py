import reflex as rx
from app.state import State


def professional_card(professional: rx.Var) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="h-16 w-16 text-white/50"),
                    class_name="h-48 w-full bg-gradient-to-br from-gray-200 to-gray-400 flex items-center justify-center",
                )
            ),
            rx.el.div(
                rx.el.h3(
                    professional["name"], class_name="text-lg font-bold text-gray-800"
                ),
                rx.el.p(
                    professional["title"],
                    class_name="text-sm font-medium text-blue-600 dark:text-blue-400",
                ),
                rx.el.p(
                    professional["description"],
                    class_name="mt-2 text-sm text-gray-600 line-clamp-3",
                ),
                class_name="p-5",
            ),
            rx.el.div(
                rx.el.span(
                    "Ver Perfil",
                    rx.icon("arrow-right", class_name="ml-2 h-4 w-4"),
                    class_name="inline-flex items-center text-sm font-semibold text-blue-600 dark:text-blue-400",
                ),
                class_name="p-5 mt-auto border-t border-gray-100",
            ),
            class_name="bg-white rounded-2xl shadow-md hover:shadow-2xl transition-shadow duration-300 flex flex-col h-full overflow-hidden group",
            style={
                "box-shadow": "0 4px 8px rgba(0,0,0,0.05), 0 6px 20px rgba(0,0,0,0.04)"
            },
        ),
        href=f"/profile/{professional['id']}",
    )


def professional_carousel() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Profesionales Destacados",
                    class_name="text-3xl font-bold text-gray-800",
                ),
                rx.el.p(
                    f"Explora nuestros expertos en: {State.current_area}",
                    class_name="mt-2 text-lg text-gray-500",
                ),
                class_name="text-center mb-12",
            ),
            rx.el.div(
                rx.foreach(State.featured_professionals, professional_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8",
                key=State.current_area,
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8",
        ),
        class_name="py-20 bg-gray-50 dark:bg-gray-800",
    )