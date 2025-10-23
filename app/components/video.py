import reflex as rx


def video_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "¿Cómo funciona ProfessionalBook?",
                    class_name="text-3xl font-bold text-gray-800 text-center",
                ),
                rx.el.p(
                    "Descúbrelo en menos de 2 minutos.",
                    class_name="mt-2 text-lg text-gray-500 text-center",
                ),
                class_name="mb-12",
            ),
            rx.el.div(
                rx.el.iframe(
                    src="https://www.youtube.com/embed/dQw4w9WgXcQ",
                    frame_border="0",
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
                    allow_full_screen=True,
                    class_name="w-full h-full aspect-video",
                ),
                class_name="max-w-4xl mx-auto bg-gray-900 rounded-2xl shadow-2xl overflow-hidden border-4 border-gray-300",
                style={
                    "box-shadow": "0 10px 25px rgba(0,0,0,0.1), 0 8px 10px rgba(0,0,0,0.08)"
                },
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8",
        ),
        class_name="py-20 bg-white",
    )