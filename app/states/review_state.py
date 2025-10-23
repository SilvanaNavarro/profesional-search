import reflex as rx
from typing import TypedDict
from sqlmodel import select, func
from app.db import Review, User
from app.states.professional_auth_state import ProfessionalAuthState


class ReviewData(TypedDict):
    user_name: str
    rating: int
    comment: str
    created_at: str


class RatingDistribution(TypedDict):
    name: str
    value: int


class ReviewState(rx.State):
    reviews: list[ReviewData] = []
    filtered_reviews: list[ReviewData] = []
    average_rating: float = 0.0
    total_reviews: int = 0
    rating_distribution: list[RatingDistribution] = []
    current_filter: str = "all"

    @rx.event
    async def load_reviews(self):
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in:
            return
        professional_id = auth_state.professional_id
        with rx.session() as session:
            db_reviews = session.exec(
                select(Review, User.name)
                .join(User, Review.user_id == User.id)
                .where(Review.professional_id == professional_id)
                .order_by(Review.created_at.desc())
            ).all()
            self.reviews = [
                {
                    "user_name": user_name,
                    "rating": review.rating,
                    "comment": review.comment,
                    "created_at": review.created_at,
                }
                for review, user_name in db_reviews
            ]
            self.total_reviews = len(self.reviews)
            if self.total_reviews > 0:
                self.average_rating = round(
                    sum((r["rating"] for r in self.reviews)) / self.total_reviews, 1
                )
            else:
                self.average_rating = 0.0
            self._calculate_rating_distribution()
            self.apply_filter()

    def _calculate_rating_distribution(self):
        distribution = {i: 0 for i in range(1, 6)}
        for review in self.reviews:
            distribution[review["rating"]] += 1
        self.rating_distribution = [
            {"name": f"{i} Stars", "value": distribution[i]} for i in range(1, 6)
        ]

    @rx.event
    def set_filter(self, filter_type: str):
        self.current_filter = filter_type
        self.apply_filter()

    @rx.event
    def apply_filter(self):
        if self.current_filter == "all":
            self.filtered_reviews = self.reviews
        elif self.current_filter == "positive":
            self.filtered_reviews = [r for r in self.reviews if r["rating"] >= 4]
        elif self.current_filter == "negative":
            self.filtered_reviews = [r for r in self.reviews if r["rating"] <= 2]

    @rx.event
    async def on_dashboard_load(self):
        auth_state = await self.get_state(ProfessionalAuthState)
        if auth_state.is_logged_in:
            return ReviewState.load_reviews