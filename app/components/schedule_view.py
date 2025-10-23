import reflex as rx
from app.states.schedule_state import ScheduleManagementState


def calendar_day(day: dict) -> rx.Component:
    return rx.el.div(
        rx.cond(
            day["day"],
            rx.el.button(
                day["day"],
                on_click=lambda: ScheduleManagementState.select_date(day["date_str"]),
                class_name=rx.cond(
                    ScheduleManagementState.selected_date == day["date_str"],
                    "w-10 h-10 flex items-center justify-center rounded-full bg-blue-600 text-white font-semibold",
                    "w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 font-medium text-gray-700",
                ),
            ),
            rx.el.div(class_name="w-10 h-10"),
        )
    )


def time_slot_card(slot: dict) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.p(slot["time"], class_name="font-semibold"),
            rx.icon(
                rx.match(
                    slot["status"],
                    ("available", "circle_check"),
                    ("blocked", "circle_x"),
                    ("booked", "lock"),
                    "help_circle",
                ),
                class_name="h-5 w-5",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        on_click=lambda: ScheduleManagementState.toggle_time_slot(slot["time"]),
        class_name=rx.cond(
            slot["status"] == "available",
            "p-3 rounded-lg border bg-green-50 border-green-200 text-green-800 hover:bg-green-100 transition-colors w-full text-left",
            rx.cond(
                slot["status"] == "blocked",
                "p-3 rounded-lg border bg-red-50 border-red-200 text-red-800 hover:bg-red-100 transition-colors w-full text-left",
                "p-3 rounded-lg border bg-blue-50 border-blue-200 text-blue-800 cursor-not-allowed w-full text-left",
            ),
        ),
        disabled=slot["status"] == "booked",
    )


def schedule_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Gestión de Agenda", class_name="text-3xl font-bold text-gray-800 mb-2"
        ),
        rx.el.p(
            "Configura tu disponibilidad, bloquea fechas y visualiza tus citas.",
            class_name="text-gray-500 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Calendario", class_name="text-xl font-semibold mb-4"),
                    rx.el.div(
                        rx.el.div(
                            rx.el.button(
                                rx.icon("arrow-left"),
                                on_click=ScheduleManagementState.prev_month,
                                class_name="p-2 rounded-md hover:bg-gray-100",
                            ),
                            rx.el.span(
                                ScheduleManagementState.month_and_year,
                                class_name="font-semibold text-lg w-40 text-center",
                            ),
                            rx.el.button(
                                rx.icon("arrow-right"),
                                on_click=ScheduleManagementState.next_month,
                                class_name="p-2 rounded-md hover:bg-gray-100",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        class_name="flex justify-between items-center mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"],
                            lambda day: rx.el.div(
                                day,
                                class_name="text-center font-medium text-sm text-gray-500",
                            ),
                        ),
                        class_name="grid grid-cols-7 gap-2 mb-2",
                    ),
                    rx.el.div(
                        rx.foreach(ScheduleManagementState.calendar_days, calendar_day),
                        class_name="grid grid-cols-7 gap-2",
                    ),
                    class_name="p-6 bg-white rounded-2xl shadow-md border border-gray-100",
                )
            ),
            rx.cond(
                ScheduleManagementState.selected_date != "",
                rx.el.div(
                    rx.el.h3(
                        f"Horarios para {ScheduleManagementState.selected_date}",
                        class_name="text-xl font-semibold mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ScheduleManagementState.time_slots_for_day, time_slot_card
                        ),
                        class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(class_name="h-3 w-3 rounded-full bg-green-200"),
                            rx.el.p("Disponible", class_name="text-sm"),
                            class_name="flex items-center gap-2",
                        ),
                        rx.el.div(
                            rx.el.div(class_name="h-3 w-3 rounded-full bg-red-200"),
                            rx.el.p("Bloqueado", class_name="text-sm"),
                            class_name="flex items-center gap-2",
                        ),
                        rx.el.div(
                            rx.el.div(class_name="h-3 w-3 rounded-full bg-blue-200"),
                            rx.el.p("Reservado", class_name="text-sm"),
                            class_name="flex items-center gap-2",
                        ),
                        class_name="flex gap-4 mt-4 text-gray-600",
                    ),
                    class_name="p-6 bg-white rounded-2xl shadow-md border border-gray-100 h-fit",
                ),
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start",
        ),
        class_name="p-8",
    )