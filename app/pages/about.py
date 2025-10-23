import reflex as rx
from app.components.header import header


def info_card(icon: str, title: str, text: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-10 w-10 text-orange-500 mb-4"),
        rx.el.h3(title, class_name="text-xl font-bold text-gray-800 mb-2"),
        rx.el.p(text, class_name="text-gray-600 leading-relaxed"),
        class_name="bg-white p-8 rounded-2xl shadow-md border border-gray-100",
    )


def about_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Sobre ProfessionalBook",
                        class_name="text-4xl md:text-5xl font-extrabold text-gray-800 text-center",
                    ),
                    rx.el.p(
                        "Conectando talento con oportunidades, de forma simple y segura.",
                        class_name="mt-4 max-w-2xl mx-auto text-center text-lg text-gray-600 font-medium",
                    ),
                    class_name="py-16 bg-orange-50 rounded-3xl",
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8 pt-8",
            ),
            rx.el.div(
                rx.el.div(
                    info_card(
                        "goal",
                        "Nuestra Misión",
                        "Facilitar el acceso a profesionales calificados, eliminando barreras y simplificando el proceso de reserva para que encuentres la ayuda que necesitas, cuando la necesitas.",
                    ),
                    info_card(
                        "eye",
                        "Nuestra Visión",
                        "Ser la plataforma líder y de mayor confianza en Latinoamérica para la conexión entre clientes y profesionales, impulsando el crecimiento y la colaboración.",
                    ),
                    info_card(
                        "gem",
                        "Nuestros Valores",
                        "Compromiso con la calidad, integridad en cada interacción, innovación constante para mejorar la experiencia y una profunda vocación de servicio.",
                    ),
                    class_name="grid md:grid-cols-3 gap-8 mt-16",
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-16",
            ),
        ),
        class_name="font-['JetBrains_Mono'] bg-gray-50",
    )