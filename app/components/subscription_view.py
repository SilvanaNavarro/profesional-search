import reflex as rx
from app.states.subscription_state import SubscriptionState


def plan_card(plan: dict) -> rx.Component:
    return rx.el.div(
        rx.el.h3(plan["name"], class_name="text-2xl font-bold text-gray-800"),
        rx.el.p(plan["price"], class_name="text-4xl font-extrabold my-4"),
        rx.el.ul(
            rx.foreach(
                plan["features"],
                lambda feature: rx.el.li(
                    rx.icon("check", class_name="h-5 w-5 text-green-500 mr-3"),
                    feature,
                    class_name="flex items-center text-gray-600",
                ),
            ),
            class_name="space-y-3 mb-8",
        ),
        rx.el.button(
            rx.cond(
                SubscriptionState.current_subscription.plan == plan["type"],
                "Plan Actual",
                "Seleccionar Plan",
            ),
            on_click=lambda: SubscriptionState.change_plan(plan["type"]),
            is_loading=rx.cond(
                SubscriptionState.current_subscription.plan != plan["type"],
                SubscriptionState.is_loading,
                False,
            ),
            disabled=SubscriptionState.current_subscription.plan == plan["type"],
            class_name=rx.cond(
                SubscriptionState.current_subscription.plan == plan["type"],
                "w-full bg-gray-200 text-gray-500 font-semibold py-3 rounded-lg cursor-not-allowed",
                "w-full bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold py-3 rounded-lg hover:from-blue-600 hover:to-green-400 transition-shadow shadow-lg",
            ),
            width="100%",
        ),
        class_name="bg-white p-8 rounded-2xl shadow-lg border-2",
        border_color=rx.cond(
            SubscriptionState.current_subscription.plan == plan["type"],
            "#1d4ed8",
            "#e5e7eb",
        ),
    )


def subscription_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Plan y Suscripción", class_name="text-3xl font-bold text-gray-800 mb-2"
        ),
        rx.el.p(
            "Elige el plan que mejor se adapte a tus necesidades para crecer en nuestra plataforma.",
            class_name="text-gray-500 mb-12",
        ),
        rx.el.div(
            rx.foreach(SubscriptionState.plans, plan_card),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
        ),
        class_name="p-8",
    )