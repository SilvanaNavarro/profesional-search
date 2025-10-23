import reflex as rx
from typing import Literal


class ThemeState(rx.State):
    appearance: str = "light"

    @rx.var
    def icon(self) -> str:
        return "moon" if self.appearance == "light" else "sun"

    @rx.event
    def toggle_dark_mode(self):
        self.appearance = "dark" if self.appearance == "light" else "light"