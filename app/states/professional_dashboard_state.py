import reflex as rx
from app.db import Booking
from sqlmodel import select, func
from app.states.professional_auth_state import ProfessionalAuthState
from datetime import datetime, timedelta


class DashboardState(rx.State):
    current_view: str = "dashboard"
    total_bookings: int = 0
    pending_bookings_week: int = 0
    average_rating: float = 0.0
    total_reviews: int = 0

    @rx.event
    async def load_dashboard_data(self):
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in:
            return
        with rx.session() as session:
            from app.db import Review

            professional_id = auth_state.professional_id
            self.total_bookings = session.exec(
                select(func.count(Booking.id)).where(
                    Booking.professional_id == professional_id,
                    Booking.payment_status == "approved",
                )
            ).one()
            today = datetime.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            self.pending_bookings_week = session.exec(
                select(func.count(Booking.id)).where(
                    Booking.professional_id == professional_id,
                    Booking.payment_status == "approved",
                    func.date(Booking.date) >= start_of_week,
                    func.date(Booking.date) <= end_of_week,
                )
            ).one()
            self.total_reviews = session.exec(
                select(func.count(Review.id)).where(
                    Review.professional_id == professional_id
                )
            ).one()
            avg_rating_query = session.exec(
                select(func.avg(Review.rating)).where(
                    Review.professional_id == professional_id
                )
            ).one()
            self.average_rating = (
                round(avg_rating_query, 1) if avg_rating_query else 0.0
            )

    @rx.event
    def set_current_view(self, view: str):
        self.current_view = view