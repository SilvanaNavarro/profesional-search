import reflex as rx
from app.states.profile_settings_state import ProfileSettingsState


def form_group(label: str, input_component: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        input_component,
        class_name="w-full",
    )


def profile_settings_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Configuración de Perfil",
            class_name="text-3xl font-bold text-gray-800 mb-2",
        ),
        rx.el.p(
            "Actualiza tu información personal y de seguridad.",
            class_name="text-gray-500 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3("Foto de Perfil", class_name="text-xl font-semibold mb-4"),
                rx.el.div(
                    rx.image(
                        src=rx.get_upload_url(
                            ProfileSettingsState.professional.photo_profile_path
                        ),
                        class_name="h-32 w-32 rounded-full object-cover border-4 border-white shadow-lg",
                    ),
                    rx.upload.root(
                        rx.el.button(
                            rx.icon("upload", class_name="mr-2"),
                            "Cambiar Foto",
                            class_name="bg-white text-gray-700 font-semibold px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-sm",
                        ),
                        id="profile_photo_upload",
                        multiple=False,
                        accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]},
                        on_drop=ProfileSettingsState.handle_profile_pic_upload(
                            rx.upload_files(upload_id="profile_photo_upload")
                        ),
                        class_name="mt-4",
                    ),
                    rx.foreach(
                        rx.selected_files("profile_photo_upload"),
                        lambda file: rx.el.div(
                            file, class_name="text-sm text-gray-500 mt-2"
                        ),
                    ),
                    class_name="flex flex-col items-center",
                ),
                class_name="bg-white p-6 rounded-2xl shadow-md border border-gray-100 text-center",
            ),
            rx.el.div(
                rx.el.h3(
                    "Descripción de Servicios", class_name="text-xl font-semibold mb-4"
                ),
                rx.el.textarea(
                    on_change=ProfileSettingsState.set_new_description,
                    placeholder="Describe los servicios que ofreces...",
                    class_name="w-full h-40 p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500",
                    default_value=ProfileSettingsState.new_description,
                ),
                rx.el.button(
                    "Guardar Descripción",
                    on_click=ProfileSettingsState.save_description,
                    class_name="mt-4 bg-blue-600 text-white font-semibold px-5 py-2.5 rounded-lg hover:bg-blue-700 transition-colors",
                ),
                class_name="bg-white p-6 rounded-2xl shadow-md border border-gray-100 mt-8",
            ),
            rx.el.div(
                rx.el.h3("Cambiar Contraseña", class_name="text-xl font-semibold mb-4"),
                rx.el.div(
                    form_group(
                        "Contraseña Actual",
                        rx.el.input(
                            type="password",
                            on_change=ProfileSettingsState.set_current_password,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500",
                        ),
                    ),
                    form_group(
                        "Nueva Contraseña",
                        rx.el.input(
                            type="password",
                            on_change=ProfileSettingsState.set_new_password,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500",
                        ),
                    ),
                    form_group(
                        "Confirmar Nueva Contraseña",
                        rx.el.input(
                            type="password",
                            on_change=ProfileSettingsState.set_confirm_new_password,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500",
                        ),
                    ),
                    class_name="space-y-4",
                ),
                rx.cond(
                    ProfileSettingsState.error_message != "",
                    rx.el.p(
                        ProfileSettingsState.error_message,
                        class_name="text-red-500 text-sm mt-2",
                    ),
                ),
                rx.el.button(
                    "Cambiar Contraseña",
                    on_click=ProfileSettingsState.change_password,
                    class_name="mt-4 bg-blue-600 text-white font-semibold px-5 py-2.5 rounded-lg hover:bg-blue-700 transition-colors",
                ),
                class_name="bg-white p-6 rounded-2xl shadow-md border border-gray-100 mt-8",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start",
        ),
        class_name="p-8",
    )