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
                    class_name="text-4xl font-bold text-gray-800 dark:text-white text-center",
                ),
                rx.el.p(
                    "Encuentra al experto perfecto para tus necesidades.",
                    class_name="mt-2 text-lg text-gray-500 dark:text-gray-400 text-center",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Buscar por nombre...",
                            on_change=SearchState.set_search_name.debounce(500),
                            default_value=SearchState.search_name,
                            class_name="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                        ),
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        class_name="relative w-full md:w-1/3",
                    ),
                    rx.el.select(
                        rx.el.option("Todas las ciudades", value=""),
                        rx.foreach(
                            SearchState.cities,
                            lambda city: rx.el.option(city, value=city),
                        ),
                        on_change=SearchState.set_search_city,
                        default_value=SearchState.search_city,
                        class_name="w-full md:w-auto px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                    ),
                    rx.el.button(
                        "Limpiar Filtros",
                        on_click=SearchState.clear_filters,
                        class_name="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-200 dark:hover:bg-gray-500",
                    ),
                    class_name="flex flex-col md:flex-row items-center gap-4 mb-6 p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm",
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
                    class_name="flex flex-wrap justify-center gap-2 md:gap-4 mb-8",
                ),
                rx.el.p(
                    f"{SearchState.professionals.length()} resultados encontrados",
                    class_name="text-center text-gray-600 dark:text-gray-400 mb-8",
                ),
                rx.el.div(
                    rx.foreach(SearchState.professionals, professional_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8",
                ),
                class_name="mb-12",
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="font-['JetBrains_Mono'] bg-gray-50 dark:bg-blue-950 min-h-screen",
    )