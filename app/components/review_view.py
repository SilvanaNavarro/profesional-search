import reflex as rx
from app.states.review_state import ReviewState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 2px 6px 0px rgba(0,0,0,0.05)",
        "padding": "0.5rem 0.75rem",
    },
    "item_style": {},
    "label_style": {},
    "separator": ": ",
}


def star_rating(rating: rx.Var[int]) -> rx.Component:
    return rx.el.div(
        rx.foreach(
            rx.Var.range(5),
            lambda i: rx.icon(
                "star",
                class_name=rx.cond(
                    i < rating, "text-yellow-400 fill-yellow-400", "text-gray-300"
                ),
                size=20,
            ),
        ),
        class_name="flex items-center gap-1",
    )


def review_card(review: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(review["user_name"], class_name="font-semibold text-gray-800"),
                star_rating(review["rating"]),
                class_name="flex items-center justify-between",
            ),
            rx.el.p(
                review["comment"],
                class_name="text-gray-600 mt-2 text-sm leading-relaxed",
            ),
            rx.el.p(
                str(rx.Var.create(review["created_at"])).split("T")[0],
                class_name="text-xs text-gray-400 mt-3 text-right",
            ),
            class_name="flex-1",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-md border border-gray-100 flex",
    )


def review_stats() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Estadísticas de Valoraciones", class_name="text-xl font-semibold mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Valoración Promedio",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    rx.el.div(
                        rx.el.p(
                            ReviewState.average_rating.to_string(),
                            class_name="text-3xl font-bold text-gray-800",
                        ),
                        rx.icon(
                            "star", class_name="text-yellow-400 fill-yellow-400 h-7 w-7"
                        ),
                        class_name="flex items-center gap-2 mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Total de Reseñas",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    rx.el.p(
                        ReviewState.total_reviews.to_string(),
                        class_name="text-3xl font-bold text-gray-800 mt-1",
                    ),
                ),
                class_name="grid grid-cols-2 gap-6",
            ),
            class_name="p-6 bg-white rounded-2xl shadow-md border border-gray-100",
        ),
        rx.el.div(
            rx.el.h3(
                "Distribución de Estrellas", class_name="text-xl font-semibold mb-4"
            ),
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(vertical=False, class_name="opacity-25"),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.x_axis(data_key="name", custom_attrs={"fontSize": "12px"}),
                rx.recharts.y_axis(custom_attrs={"fontSize": "12px"}),
                rx.recharts.bar(
                    data_key="value",
                    stroke="#2563eb",
                    fill="#60a5fa",
                    radius=[4, 4, 0, 0],
                ),
                data=ReviewState.rating_distribution,
                height=300,
                class_name="font-sans",
            ),
            class_name="p-6 bg-white rounded-2xl shadow-md border border-gray-100 mt-8",
        ),
        class_name="lg:col-span-1 h-fit sticky top-8",
    )


def reviews_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Reseñas y Valoraciones", class_name="text-3xl font-bold text-gray-800 mb-2"
        ),
        rx.el.p(
            "Visualiza los comentarios y valoraciones de tus clientes.",
            class_name="text-gray-500 mb-8",
        ),
        rx.el.div(
            rx.el.div(review_stats(), class_name="hidden lg:block"),
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        "Todas",
                        on_click=lambda: ReviewState.set_filter("all"),
                        class_name=rx.cond(
                            ReviewState.current_filter == "all",
                            "px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold",
                            "px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50",
                        ),
                    ),
                    rx.el.button(
                        "Positivas (4-5 ★)",
                        on_click=lambda: ReviewState.set_filter("positive"),
                        class_name=rx.cond(
                            ReviewState.current_filter == "positive",
                            "px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold",
                            "px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50",
                        ),
                    ),
                    rx.el.button(
                        "Negativas (1-2 ★)",
                        on_click=lambda: ReviewState.set_filter("negative"),
                        class_name=rx.cond(
                            ReviewState.current_filter == "negative",
                            "px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold",
                            "px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50",
                        ),
                    ),
                    class_name="flex items-center gap-3 mb-6",
                ),
                rx.el.div(
                    rx.foreach(ReviewState.filtered_reviews, review_card),
                    class_name="space-y-6",
                ),
                class_name="lg:col-span-2",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start",
        ),
        class_name="p-8",
    )