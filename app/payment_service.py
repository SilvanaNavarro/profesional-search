import reflex as rx
import mercadopago
import os
import logging
from typing import TypedDict


class ProfessionalInfo(TypedDict):
    name: str
    title: str


class UserInfo(TypedDict):
    name: str
    email: str


class PaymentService:
    def __init__(self):
        self.sdk = None
        access_token = os.environ.get("MERCADOPAGO_ACCESS_TOKEN")
        if not access_token:
            logging.error("MERCADOPAGO_ACCESS_TOKEN no está configurado.")
        else:
            self.sdk = mercadopago.SDK(access_token)

    def create_payment_preference(
        self,
        booking_id: int,
        professional_info: ProfessionalInfo,
        user_info: UserInfo,
        price: float,
    ) -> dict | None:
        if not self.sdk:
            logging.error("Mercado Pago SDK no inicializado.")
            return None
        base_url = "http://localhost:3000"
        preference_data = {
            "items": [
                {
                    "title": f"Reserva con {professional_info['name']} - {professional_info['title']}",
                    "quantity": 1,
                    "unit_price": price,
                    "currency_id": "CLP",
                }
            ],
            "payer": {"name": user_info["name"], "email": user_info["email"]},
            "back_urls": {
                "success": f"{base_url}/payment-success",
                "failure": f"{base_url}/payment-failure",
                "pending": f"{base_url}/payment-pending",
            },
            "external_reference": str(booking_id),
            "statement_descriptor": "PROFESSIONALBOOK",
        }
        try:
            result = self.sdk.preference().create(preference_data)
            if result["status"] == 201:
                logging.info(
                    f"Preferencia de pago creada para booking_id: {booking_id}"
                )
                return result["response"]
            else:
                logging.error(f"Error al crear preferencia MP: {result}")
                return None
        except Exception as e:
            logging.exception(f"Excepción al crear preferencia MP: {e}")
            return None

    def get_payment(self, payment_id: str) -> dict | None:
        if not self.sdk:
            logging.error("Mercado Pago SDK no inicializado.")
            return None
        try:
            payment_info = self.sdk.payment().get(payment_id)
            return payment_info
        except Exception as e:
            logging.exception(
                f"Error al obtener información del pago ID {payment_id}: {e}"
            )
            return None