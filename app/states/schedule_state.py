import reflex as rx
from datetime import datetime, timedelta
import calendar
from app.db import ProfessionalAvailability, Booking
from sqlmodel import select, and_
from app.states.professional_auth_state import ProfessionalAuthState


class ScheduleManagementState(rx.State):
    current_month_display: datetime = datetime.now()
    selected_date: str = ""
    time_slots_for_day: list[dict] = []

    @rx.var
    def month_and_year(self) -> str:
        return self.current_month_display.strftime("%B %Y").capitalize()

    @rx.var
    def calendar_days(self) -> list[dict]:
        year = self.current_month_display.year
        month = self.current_month_display.month
        month_calendar = calendar.monthcalendar(year, month)
        days = []
        for week in month_calendar:
            for day in week:
                if day == 0:
                    days.append({"day": "", "date_str": ""})
                else:
                    date_obj = datetime(year, month, day)
                    days.append(
                        {"day": str(day), "date_str": date_obj.strftime("%Y-%m-%d")}
                    )
        return days

    @rx.event
    async def load_schedule_data(self):
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in:
            return
        professional_id = auth_state.professional_id
        start_of_month = self.current_month_display.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(
            days=1
        )
        with rx.session() as session:
            pass

    @rx.event
    def next_month(self):
        self.current_month_display = self.current_month_display + timedelta(days=32)
        self.current_month_display = self.current_month_display.replace(day=1)
        self.selected_date = ""
        self.time_slots_for_day = []
        return ScheduleManagementState.load_schedule_data

    @rx.event
    def prev_month(self):
        self.current_month_display = self.current_month_display - timedelta(days=1)
        self.current_month_display = self.current_month_display.replace(day=1)
        self.selected_date = ""
        self.time_slots_for_day = []
        return ScheduleManagementState.load_schedule_data

    @rx.event
    async def select_date(self, date: str):
        self.selected_date = date
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in:
            self.time_slots_for_day = []
            return
        professional_id = auth_state.professional_id
        default_slots = [
            (datetime.strptime("09:00", "%H:%M") + timedelta(minutes=30 * i)).strftime(
                "%H:%M"
            )
            for i in range(18)
        ]
        with rx.session() as session:
            db_availability = session.exec(
                select(ProfessionalAvailability).where(
                    ProfessionalAvailability.professional_id == professional_id,
                    ProfessionalAvailability.date == date,
                )
            ).all()
            availability_map = {slot.time_slot: slot for slot in db_availability}
            processed_slots = []
            for time_str in default_slots:
                slot_info = {"time": time_str, "status": "available"}
                if time_str in availability_map:
                    db_slot = availability_map[time_str]
                    if db_slot.is_booked:
                        slot_info["status"] = "booked"
                    elif not db_slot.is_available:
                        slot_info["status"] = "blocked"
                processed_slots.append(slot_info)
            self.time_slots_for_day = processed_slots

    @rx.event
    async def toggle_time_slot(self, time: str):
        if not self.selected_date:
            return
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in:
            return
        professional_id = auth_state.professional_id
        with rx.session() as session:
            availability = session.exec(
                select(ProfessionalAvailability).where(
                    ProfessionalAvailability.professional_id == professional_id,
                    ProfessionalAvailability.date == self.selected_date,
                    ProfessionalAvailability.time_slot == time,
                )
            ).first()
            if availability:
                if availability.is_booked:
                    return rx.toast.error(
                        "Este horario ya está reservado y no se puede modificar."
                    )
                availability.is_available = not availability.is_available
                session.add(availability)
            else:
                new_availability = ProfessionalAvailability(
                    professional_id=professional_id,
                    date=self.selected_date,
                    time_slot=time,
                    is_available=False,
                    is_booked=False,
                )
                session.add(new_availability)
            session.commit()
        return ScheduleManagementState.select_date(self.selected_date)