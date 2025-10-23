import reflex as rx
from typing import TypedDict
from datetime import datetime, timedelta
import calendar


class TimeSlot(TypedDict):
    time: str
    available: bool
    booked: bool


class BookingState(rx.State):
    selected_professional_id: int = 1
    selected_date: str = ""
    selected_time: str = ""
    booking_confirmed: bool = False
    show_confirmation: bool = False
    show_login_prompt: bool = False
    booked_slots: dict[str, list[str]] = {}
    current_month_display: datetime = datetime.now()

    @rx.var
    def current_professional(self) -> dict | None:
        from app.state import professionals_data

        for prof in professionals_data:
            if prof["id"] == self.selected_professional_id:
                return prof
        return None

    @rx.var
    def available_dates(self) -> list[str]:
        today = datetime.now()
        dates = []
        for i in range(60):
            date = today + timedelta(days=i)
            if date.weekday() < 5:
                dates.append(date.strftime("%Y-%m-%d"))
        return [
            d
            for d in dates
            if datetime.strptime(d, "%Y-%m-%d").month
            == self.current_month_display.month
        ]

    @rx.var
    def time_slots(self) -> list[TimeSlot]:
        if not self.current_professional:
            return []
        slots = []
        available_hours = self.current_professional["available_hours"]
        date_key = f"{self.selected_professional_id}_{self.selected_date}"
        booked_times = self.booked_slots.get(date_key, [])
        for time in available_hours:
            slots.append(
                {"time": time, "available": True, "booked": time in booked_times}
            )
        return slots

    @rx.var
    def month_and_year(self) -> str:
        return self.current_month_display.strftime("%B %Y").capitalize()

    @rx.event
    def next_month(self):
        self.current_month_display = self.current_month_display + timedelta(
            days=calendar.monthrange(
                self.current_month_display.year, self.current_month_display.month
            )[1]
        )

    @rx.event
    def prev_month(self):
        first_day_of_current_month = self.current_month_display.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        self.current_month_display = last_day_of_previous_month

    @rx.event
    def load_professional(self):
        self.current_month_display = datetime.now()
        prof_id = self.router.page.params.get("id")
        if prof_id:
            self.selected_professional_id = int(prof_id)
        else:
            self.selected_professional_id = 1
        query_date = self.router.page.params.get("date")
        query_time = self.router.page.params.get("time")
        self.selected_date = query_date if query_date else ""
        self.selected_time = query_time if query_time else ""
        self.booking_confirmed = False

    @rx.event
    def set_selected_professional(self, prof_id: str):
        self.selected_professional_id = int(prof_id)
        self.selected_date = ""
        self.selected_time = ""
        self.booking_confirmed = False

    @rx.event
    def select_date(self, date: str):
        self.selected_date = date
        self.selected_time = ""

    @rx.event
    def select_time(self, time: str):
        if self.selected_date:
            self.selected_time = time

    @rx.event
    async def confirm_booking(self):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_logged_in or not auth_state.is_verified:
            self.show_login_prompt = True
            return
        if self.selected_date and self.selected_time and self.current_professional:
            yield BookingState.initiate_payment_process()

    @rx.event
    async def initiate_payment_process(self):
        from app.states.auth_state import AuthState
        from app.states.payment_state import PaymentState
        from app.db import User, Booking
        from sqlmodel import select
        import datetime

        auth_state = await self.get_state(AuthState)
        if (
            not self.selected_date
            or not self.selected_time
            or (not self.current_professional)
        ):
            yield rx.toast.error("Por favor, selecciona una fecha y hora válidas.")
            return
        with rx.session() as session:
            user = session.exec(
                select(User).where(User.email == auth_state.user_email)
            ).first()
            if not user:
                yield rx.toast.error(
                    "Error de usuario. Intenta iniciar sesión de nuevo."
                )
                return
            new_booking = Booking(
                user_id=user.id,
                professional_id=self.current_professional["id"],
                date=self.selected_date,
                time=self.selected_time,
                created_at=datetime.datetime.now().isoformat(),
            )
            session.add(new_booking)
            session.commit()
            session.refresh(new_booking)
            booking_id = new_booking.id
        if booking_id:
            payment_state = await self.get_state(PaymentState)
            yield PaymentState.create_checkout_session(booking_id, 25000)

    @rx.event
    def close_confirmation(self):
        self.show_confirmation = False
        self.selected_date = ""
        self.selected_time = ""

    @rx.event
    def close_login_prompt(self):
        self.show_login_prompt = False

    @rx.event
    async def redirect_to_login(self):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        return_url = f"/profile/{self.selected_professional_id}?date={self.selected_date}&time={self.selected_time}"
        auth_state.return_url = return_url
        self.show_login_prompt = False
        return rx.redirect("/login")