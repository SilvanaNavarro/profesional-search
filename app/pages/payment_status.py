import reflex as rx
from app.components.header import header
from app.states.payment_state import PaymentState


def booking_details_card() -> rx.Component:
    return rx.cond(
        PaymentState.payment_details.contains("professional_name"),
        rx.el.div(
            rx.el.h3(
                "Detalles de la Cita",
                class_name="text-xl font-semibold text-gray-700 mb-4 text-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span("Profesional:", class_name="text-gray-500"),
                    rx.el.span(
                        PaymentState.payment_details["professional_name"],
                        class_name="font-semibold text-gray-800",
                    ),
                    class_name="flex justify-between",
                ),
                rx.el.div(
                    rx.el.span("Fecha:", class_name="text-gray-500"),
                    rx.el.span(
                        PaymentState.payment_details["date"],
                        class_name="font-semibold text-gray-800",
                    ),
                    class_name="flex justify-between mt-2",
                ),
                rx.el.div(
                    rx.el.span("Hora:", class_name="text-gray-500"),
                    rx.el.span(
                        PaymentState.payment_details["time"],
                        class_name="font-semibold text-gray-800",
                    ),
                    class_name="flex justify-between mt-2",
                ),
                rx.el.div(
                    rx.el.span("Estado del Pago:", class_name="text-gray-500"),
                    rx.el.span(
                        PaymentState.payment_details["status"].to(str).capitalize(),
                        class_name="font-semibold text-gray-800",
                    ),
                    class_name="flex justify-between mt-2",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-200 mt-6",
            ),
            class_name="w-full max-w-md mx-auto mb-8",
        ),
    )


def status_page_layout(
    icon: str,
    title: str,
    message: str,
    button_text: str,
    button_href: str,
    bg_color: str,
    icon_color: str,
) -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(icon, class_name=f"h-20 w-20 {icon_color} mx-auto mb-6"),
                    rx.el.h1(
                        title,
                        class_name="text-4xl font-bold text-gray-800 text-center mb-4",
                    ),
                    rx.el.p(
                        message,
                        class_name="text-lg text-gray-600 text-center max-w-lg mx-auto mb-8",
                    ),
                    booking_details_card(),
                    rx.el.a(
                        rx.el.button(
                            button_text,
                            class_name="bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold px-8 py-3 rounded-xl hover:from-blue-600 hover:to-green-400 transition-colors shadow-lg",
                        ),
                        href=button_href,
                    ),
                    class_name="text-center",
                ),
                class_name=f"p-12 rounded-2xl shadow-xl border border-gray-100 {bg_color}",
            ),
            class_name="flex items-center justify-center min-h-[80vh]",
        ),
        class_name="font-['JetBrains_Mono'] bg-white dark:bg-blue-950",
        on_mount=PaymentState.load_payment_details,
    )


def payment_success_page() -> rx.Component:
    return status_page_layout(
        icon="check_circle_2",
        title="¡Pago Exitoso!",
        message="Tu cita ha sido confirmada. Recibirás un correo electrónico con los detalles. Gracias por confiar en ProfessionalBook.",
        button_text="Volver al Inicio",
        button_href="/",
        bg_color="bg-green-50",
        icon_color="text-green-500",
    )


def payment_failure_page() -> rx.Component:
    return status_page_layout(
        icon="x_circle",
        title="Pago Fallido",
        message="Hubo un problema al procesar tu pago. Por favor, intenta nuevamente o contacta a soporte si el problema persiste.",
        button_text="Intentar de Nuevo",
        button_href="/search",
        bg_color="bg-red-50",
        icon_color="text-red-500",
    )


def payment_pending_page() -> rx.Component:
    return status_page_layout(
        icon="clock_4",
        title="Pago Pendiente",
        message="Tu pago está siendo procesado. Te notificaremos por correo electrónico una vez que se complete la transacción.",
        button_text="Ver mis Citas",
        button_href="/dashboard",
        bg_color="bg-yellow-50",
        icon_color="text-yellow-500",
    )