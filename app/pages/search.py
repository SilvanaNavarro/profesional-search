import reflex as rx
from app.components.header import header
from app.components.carousel import professional_card
from app.states.page_state import SearchState


def search_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Buscar Profesionales",
                    class_name="text-4xl font-bold text-gray-800 text-center",
                ),
                rx.el.p(
                    "Filtra por área para encontrar al experto que necesitas.",
                    class_name="mt-2 text-lg text-gray-500 text-center",
                ),
                rx.el.div(
                    rx.foreach(
                        SearchState.AREAS,
                        lambda area: rx.el.button(
                            area,
                            on_click=lambda: SearchState.set_selected_area(area),
                            class_name=rx.cond(
                                SearchState.selected_area == area,
                                "px-4 py-2 bg-gradient-to-r from-blue-700 to-green-500 text-white rounded-lg font-medium shadow-md",
                                "px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-blue-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700",
                            ),
                        ),
                    ),
                    class_name="flex justify-center space-x-2 md:space-x-4 mt-8",
                ),
                class_name="mb-12",
            ),
            rx.el.div(
                rx.foreach(SearchState.professionals, professional_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8",
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="font-['JetBrains_Mono'] bg-gray-50 min-h-screen",
    )