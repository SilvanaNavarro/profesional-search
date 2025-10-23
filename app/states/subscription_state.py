import reflex as rx
from app.db import Subscription, Professional, PlanType
from app.states.professional_auth_state import ProfessionalAuthState
from sqlmodel import select
from typing import TypedDict
import logging


class Plan(TypedDict):
    name: str
    price: str
    features: list[str]
    type: PlanType


class SubscriptionState(rx.State):
    current_subscription: Subscription | None = None
    is_loading: bool = False
    plans: list[Plan] = [
        {
            "name": "Básico",
            "price": "Gratis",
            "features": [
                "Ver reseñas y valoraciones",
                "Acceder a agenda",
                "Bloquear y disponibilizar horarios",
            ],
            "type": PlanType.BASICO,
        },
        {
            "name": "Profesional",
            "price": "$15.000 / mes",
            "features": [
                "Todo lo del plan Básico",
                "Publicidad en redes sociales",
                "Subir videos promocionales",
                "Galería de fotos de trabajos",
            ],
            "type": PlanType.PROFESIONAL,
        },
        {
            "name": "Senior",
            "price": "$30.000 / mes",
            "features": [
                "Todo lo del plan Profesional",
                "Visibilidad en banner principal",
                "Aparecer en búsquedas de Google (SEO)",
                "Badge 'Profesional Destacado'",
            ],
            "type": PlanType.SENIOR,
        },
    ]

    @rx.var
    def current_plan_details(self) -> Plan | None:
        if self.current_subscription:
            for plan in self.plans:
                if plan["type"] == self.current_subscription.plan:
                    return plan
        return self.plans[0]

    @rx.event
    async def load_subscription_data(self):
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in:
            return
        with rx.session() as session:
            self.current_subscription = session.exec(
                select(Subscription).where(
                    Subscription.professional_id == auth_state.professional_id
                )
            ).first()

    @rx.event
    async def change_plan(self, new_plan_type: str):
        self.is_loading = True
        auth_state = await self.get_state(ProfessionalAuthState)
        if not auth_state.is_logged_in:
            self.is_loading = False
            yield rx.toast.error("Debes iniciar sesión.")
            return
        plan_price_map = {PlanType.PROFESIONAL: 15000, PlanType.SENIOR: 30000}
        price = plan_price_map.get(new_plan_type)
        if not price:
            with rx.session() as session:
                sub = session.exec(
                    select(Subscription).where(
                        Subscription.professional_id == auth_state.professional_id
                    )
                ).first()
                if sub:
                    sub.plan = PlanType.BASICO
                    session.add(sub)
                    session.commit()
                    session.refresh(sub)
                    self.current_subscription = sub
            self.is_loading = False
            yield rx.toast.success("Has cambiado al plan Básico.")
            return
        logging.info(f"Iniciando pago de ${price} para el plan {new_plan_type}")
        await asyncio.sleep(2)
        with rx.session() as session:
            sub = session.exec(
                select(Subscription).where(
                    Subscription.professional_id == auth_state.professional_id
                )
            ).first()
            if sub:
                sub.plan = new_plan_type
                session.add(sub)
                session.commit()
                session.refresh(sub)
                self.current_subscription = sub
        self.is_loading = False
        yield rx.toast.success(
            f"¡Felicidades! Ahora tienes el plan {new_plan_type.capitalize()}."
        )