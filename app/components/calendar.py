import reflex as rx
from app.states.profile_state import BookingState


def time_slot(slot: rx.Var) -> rx.Component:
    return rx.el.button(
        slot["time"],
        on_click=lambda: BookingState.select_time(slot["time"]),
        class_name=rx.cond(
            slot["booked"],
            "px-4 py-2 bg-gray-200 text-gray-400 rounded-lg cursor-not-allowed",
            rx.cond(
                BookingState.selected_time == slot["time"],
                "px-4 py-2 bg-gradient-to-r from-blue-700 to-green-500 text-white rounded-lg hover:from-blue-600 hover:to-green-400 transition-colors",
                "px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition-colors",
            ),
        ),
        disabled=slot["booked"],
    )


def calendar_component() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Selecciona una fecha",
                    class_name="text-lg font-semibold text-gray-800",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("arrow-left"),
                        on_click=BookingState.prev_month,
                        class_name="p-2 rounded-md hover:bg-gray-100",
                    ),
                    rx.el.span(
                        BookingState.month_and_year,
                        class_name="text-md font-semibold text-gray-700 w-32 text-center",
                    ),
                    rx.el.button(
                        rx.icon("arrow-right"),
                        on_click=BookingState.next_month,
                        class_name="p-2 rounded-md hover:bg-gray-100",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.foreach(
                    BookingState.available_dates,
                    lambda date: rx.el.button(
                        rx.el.span(date.to_string().split("-")[2]),
                        on_click=lambda: BookingState.select_date(date),
                        class_name=rx.cond(
                            BookingState.selected_date == date,
                            "w-10 h-10 bg-gradient-to-r from-blue-700 to-green-500 text-white rounded-full hover:from-blue-600 hover:to-green-400 transition-colors text-sm flex items-center justify-center",
                            "w-10 h-10 bg-white border border-gray-200 text-gray-700 rounded-full hover:bg-blue-50 hover:border-blue-300 transition-colors text-sm flex items-center justify-center",
                        ),
                    ),
                ),
                class_name="grid grid-cols-7 gap-2 mb-6",
            ),
            class_name="mb-8",
        ),
        rx.cond(
            BookingState.selected_date != "",
            rx.el.div(
                rx.el.h3(
                    "Horarios disponibles",
                    class_name="text-lg font-semibold text-gray-800 mb-4",
                ),
                rx.el.div(
                    rx.foreach(BookingState.time_slots, time_slot),
                    class_name="grid grid-cols-3 md:grid-cols-4 gap-3 mb-6",
                ),
                rx.cond(
                    BookingState.selected_time != "",
                    rx.el.div(
                        rx.el.div(
                            rx.el.h4(
                                "Confirmar reserva",
                                class_name="text-md font-semibold text-gray-800 mb-2",
                            ),
                            rx.el.p(
                                f"Fecha: {BookingState.formatted_selected_date}",
                                class_name="text-sm text-gray-600 mb-1",
                            ),
                            rx.el.p(
                                f"Hora: {BookingState.selected_time}",
                                class_name="text-sm text-gray-600 mb-4",
                            ),
                            rx.el.button(
                                "Confirmar Cita",
                                on_click=BookingState.confirm_booking,
                                class_name="w-full bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold px-6 py-3 rounded-xl hover:from-blue-600 hover:to-green-400 transition-colors shadow-lg",
                            ),
                            class_name="bg-blue-50 p-4 rounded-xl border border-blue-200 dark:bg-gray-800 dark:border-gray-700",
                        ),
                        class_name="mt-6",
                    ),
                ),
            ),
        ),
        class_name="bg-white p-6 rounded-2xl shadow-md border border-gray-100",
    )