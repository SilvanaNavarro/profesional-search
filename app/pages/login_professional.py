import reflex as rx
from app.components.header import header
from app.states.professional_auth_state import ProfessionalAuthState


def login_professional_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Acceso Profesionales",
                    class_name="text-3xl font-bold text-gray-800 text-center",
                ),
                rx.el.p(
                    "Inicia sesión para gestionar tu perfil y agenda.",
                    class_name="mt-2 text-gray-600 text-center",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Correo Electrónico",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="email",
                                placeholder="tu@email.com",
                                type="email",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
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
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                            ),
                        ),
                        rx.cond(
                            ProfessionalAuthState.error_message != "",
                            rx.el.div(
                                rx.icon(
                                    "flag_triangle_right", class_name="h-4 w-4 mr-2"
                                ),
                                ProfessionalAuthState.error_message,
                                class_name="bg-red-100 border border-red-200 text-red-700 px-4 py-2 rounded-lg text-sm flex items-center",
                            ),
                        ),
                        rx.el.button(
                            "Iniciar Sesión",
                            type="submit",
                            class_name="w-full bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold px-6 py-3 rounded-xl hover:from-blue-600 hover:to-green-400 transition-colors shadow-lg",
                        ),
                        class_name="space-y-6 w-full",
                    ),
                    on_submit=ProfessionalAuthState.login,
                    reset_on_submit=False,
                    class_name="mt-8 w-full",
                ),
                rx.el.p(
                    "¿No tienes cuenta? ",
                    rx.el.a(
                        "Regístrate aquí",
                        href="/register-professional",
                        class_name="font-semibold text-blue-600 hover:underline dark:text-blue-400",
                    ),
                    class_name="text-center text-sm text-gray-600 pt-4",
                ),
                class_name="bg-white p-10 rounded-2xl shadow-xl border border-gray-100 max-w-md w-full",
            ),
            class_name="flex items-center justify-center min-h-[80vh]",
        ),
        class_name="font-['JetBrains_Mono'] bg-gray-50 dark:bg-blue-950",
    )