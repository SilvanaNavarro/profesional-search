import reflex as rx
from app.states.auth_state import AuthState
from app.components.header import header


class VerifyEmailState(rx.State):
    code: str = ""


def verify_email_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Verifica tu Correo Electrónico",
                    class_name="text-3xl font-bold text-gray-800 text-center",
                ),
                rx.el.p(
                    f"Hemos enviado un código de 6 dígitos a {AuthState.user_email}. Por favor, ingrésalo a continuación.",
                    class_name="mt-4 max-w-md mx-auto text-center text-gray-600",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="_ _ _ _ _ _",
                        on_change=VerifyEmailState.set_code,
                        class_name="w-full text-center tracking-[1.5em] text-2xl font-semibold p-4 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                        max_length=6,
                    ),
                    rx.el.button(
                        "Verificar Cuenta",
                        on_click=lambda: AuthState.verify_email(VerifyEmailState.code),
                        class_name="w-full bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold py-3 rounded-xl hover:from-blue-600 hover:to-green-400 transition-colors shadow-lg mt-6",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            AuthState.error_message,
                            class_name="text-red-600 text-sm text-center mt-2",
                        ),
                    ),
                    class_name="mt-8 max-w-sm mx-auto",
                ),
                class_name="bg-white p-10 rounded-2xl shadow-xl border border-gray-100",
            ),
            class_name="container mx-auto px-4 py-16",
        ),
        class_name="font-['JetBrains_Mono'] bg-white dark:bg-blue-950 min-h-screen",
    )