import reflex as rx
from app.components.header import header
from app.states.professional_register_state import ProfessionalRegisterState


def upload_component(
    id: str, text: str, handler: rx.event.EventSpec, file_path_var: rx.Var
) -> rx.Component:
    return rx.el.div(
        rx.el.label(text, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud_upload", class_name="h-8 w-8 text-gray-400"),
                rx.el.p(
                    "Arrastra o haz click para seleccionar archivo",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:bg-gray-50 transition-colors",
            ),
            id=id,
            multiple=False,
            accept={
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
                "application/pdf": [".pdf"],
            },
            class_name="w-full cursor-pointer",
        ),
        rx.foreach(
            rx.selected_files(id),
            lambda file: rx.el.div(file, class_name="text-sm text-gray-500 mt-1"),
        ),
        rx.cond(
            file_path_var != "",
            rx.el.div(
                rx.icon("file_check", class_name="h-5 w-5 text-green-500 mr-2"),
                rx.el.span(file_path_var, class_name="text-sm text-gray-700"),
                class_name="flex items-center mt-2 p-2 bg-green-50 rounded-md border border-green-200",
            ),
            rx.el.button(
                "Subir",
                on_click=handler(rx.upload_files(upload_id=id)),
                size="1",
                class_name="mt-2 bg-blue-100 text-blue-600 px-2 py-1 rounded-md text-xs hover:bg-blue-200",
            ),
        ),
    )


def register_professional_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Registro para Profesionales",
                    class_name="text-3xl font-bold text-gray-800 text-center",
                ),
                rx.el.p(
                    "Únete a nuestra red de expertos y ofrece tus servicios.",
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
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Carrera o Profesión",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="career",
                                placeholder="Ej: Arquitecto, Abogado",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
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
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Descripción de Servicios",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.textarea(
                                name="description_services",
                                placeholder="Describe brevemente los servicios que ofreces...",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 h-24 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
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
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
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
                        rx.el.div(
                            rx.el.label(
                                "Confirmar Contraseña",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="confirm_password",
                                placeholder="••••••••",
                                type="password",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                            ),
                        ),
                        upload_component(
                            "profile_pic",
                            "Foto de Perfil",
                            ProfessionalRegisterState.handle_profile_pic_upload,
                            ProfessionalRegisterState.photo_profile_path,
                        ),
                        upload_component(
                            "id_card",
                            "Foto de Carnet de Identidad",
                            ProfessionalRegisterState.handle_id_card_upload,
                            ProfessionalRegisterState.photo_id_card_path,
                        ),
                        upload_component(
                            "certificate",
                            "Certificado de Carrera",
                            ProfessionalRegisterState.handle_certificate_upload,
                            ProfessionalRegisterState.certificate_path,
                        ),
                        class_name="space-y-4",
                    ),
                    rx.cond(
                        ProfessionalRegisterState.error_message != "",
                        rx.el.div(
                            rx.icon("flag_triangle_right", class_name="h-4 w-4 mr-2"),
                            ProfessionalRegisterState.error_message,
                            class_name="bg-red-100 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm flex items-center mt-6",
                        ),
                    ),
                    rx.el.button(
                        rx.cond(
                            ProfessionalRegisterState.processing,
                            rx.spinner(class_name="mr-2"),
                            "Enviar Registro",
                        ),
                        type="submit",
                        class_name="w-full bg-gradient-to-r from-blue-700 to-green-500 text-white font-semibold py-3 rounded-xl hover:from-blue-600 hover:to-green-400 transition-colors shadow-lg mt-6 flex items-center justify-center",
                        disabled=ProfessionalRegisterState.processing,
                    ),
                    on_submit=ProfessionalRegisterState.handle_registration,
                    reset_on_submit=False,
                    class_name="mt-8 w-full",
                ),
                rx.el.p(
                    "¿Ya tienes una cuenta? ",
                    rx.el.a(
                        "Inicia sesión aquí",
                        href="/login-professional",
                        class_name="font-semibold text-blue-600 hover:underline dark:text-blue-400",
                    ),
                    class_name="text-center text-sm text-gray-600 dark:text-gray-300 pt-6",
                ),
                class_name="bg-white p-10 rounded-2xl shadow-xl border border-gray-100 max-w-2xl w-full",
            ),
            class_name="flex items-center justify-center min-h-[90vh] py-10",
        ),
        class_name="font-['JetBrains_Mono'] bg-white dark:bg-blue-950",
    )