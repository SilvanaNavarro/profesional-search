import reflex as rx
from app.components.header import header
from app.states.auth_state import AuthState


def register_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Crear una Cuenta",
                    class_name="text-3xl font-bold text-gray-800 text-center",
                ),
                rx.el.p(
                    "Completa tus datos para unirte a ProfessionalBook.",
                    class_name="mt-2 text-gray-600 text-center",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Nombre Completo",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="name",
                                placeholder="Tu nombre y apellido",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Fecha de Cumpleaños",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="birthdate",
                                type="date",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "RUT",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="rut",
                                placeholder="12.345.678-9",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="email",
                                placeholder="tu@email.com",
                                type="email",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Teléfono (Opcional)",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="phone",
                                placeholder="+56 9 1234 5678",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Contraseña",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="password",
                                placeholder="••••••••",
                                type="password",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Confirmar Contraseña",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="confirm_password",
                                placeholder="••••••••",
                                type="password",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500",
                            ),
                        ),
                        class_name="space-y-4",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            rx.icon("flag_triangle_right", class_name="h-4 w-4 mr-2"),
                            AuthState.error_message,
                            class_name="bg-red-100 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm flex items-center mt-6",
                        ),
                    ),
                    rx.el.button(
                        "Crear Cuenta",
                        type="submit",
                        class_name="w-full bg-orange-500 text-white font-semibold py-3 rounded-xl hover:bg-orange-600 transition-colors shadow-lg mt-6",
                    ),
                    on_submit=AuthState.handle_registration,
                    reset_on_submit=False,
                    class_name="mt-8 w-full",
                ),
                rx.el.p(
                    "¿Ya tienes cuenta? ",
                    rx.el.a(
                        "Inicia sesión aquí",
                        href="/login",
                        class_name="font-semibold text-orange-500 hover:underline",
                    ),
                    class_name="text-center text-sm text-gray-600 pt-6",
                ),
                class_name="bg-white p-10 rounded-2xl shadow-xl border border-gray-100 max-w-lg w-full",
            ),
            class_name="flex items-center justify-center min-h-[90vh] py-10",
        ),
        class_name="font-['JetBrains_Mono'] bg-gray-50",
    )