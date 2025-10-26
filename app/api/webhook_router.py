from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Request
from sqlmodel import Session
from app.db import get_session, Booking, User, Professional
from app.payment_service import PaymentService
from app.email_service import send_booking_confirmation_email
from pydantic import BaseModel, Field
import os, hmac, hashlib, logging

router = APIRouter()


class MPData(BaseModel):
    id: str


class MPPayload(BaseModel):
    type: str
    data: MPData


@router.post("/mercadopago")
async def handle_webhook(
    payload: MPPayload,
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """
    Procesa las notificaciones de pago enviadas por Mercado Pago.
    Actualiza el estado de la reserva y env\x01a un correo de confirmaci\x01n
    al usuario en caso de pago aprobado.
    """
    secret = os.getenv("MP_WEBHOOK_SECRET")
    signature_header = request.headers.get("x-signature")
    if not signature_header or not secret:
        logging.warning("Webhook: Falta la firma o el secreto.")
        raise HTTPException(status_code=400, detail="Falta la firma o el secreto")
    parts = {p.split("=")[0]: p.split("=")[1] for p in signature_header.split(",")}
    ts = parts.get("ts")
    v1 = parts.get("v1")
    if not ts or not v1:
        logging.error("Webhook: Formato de firma inv\x01lido.")
        raise HTTPException(status_code=400, detail="Formato de firma inv\x01lido")
    body = await request.body()
    manifest = f"id:{payload.data.id};type:{payload.type};ts:{ts};"
    expected_signature = hmac.new(
        secret.encode(), manifest.encode(), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(v1, expected_signature):
        logging.error("Webhook: Firma inv\x01lida.")
        raise HTTPException(status_code=403, detail="Firma inv\x01lida")
    try:
        if payload.type != "payment":
            logging.info(f"Webhook: Evento ignorado '{payload.type}'")
            return {"status": "ignored", "message": "Evento no relevante"}
        payment_id = payload.data.id
        logging.info(f"Procesando notificaci\x01n para el pago ID: {payment_id}")
        payment_service = PaymentService()
        payment_info = payment_service.get_payment(payment_id)
        if not payment_info or payment_info["status"] != 200:
            logging.error(
                f"No se pudo obtener la informaci\x01n del pago ID: {payment_id}"
            )
            raise HTTPException(
                status_code=404, detail="Pago no encontrado en Mercado Pago"
            )
        payment = payment_info["response"]
        booking_id_str = payment.get("external_reference")
        payment_status = payment.get("status")
        if not booking_id_str:
            logging.error(f"Pago {payment_id} sin external_reference.")
            raise HTTPException(status_code=400, detail="Falta external_reference")
        booking = session.get(Booking, int(booking_id_str))
        if not booking:
            logging.error(f"No se encontr\x01 la reserva con ID: {booking_id_str}")
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        if booking.payment_status == "approved":
            logging.warning(
                f"Reserva {booking.id} ya fue aprobada. Ignorando notificaci\x01n."
            )
            return {"status": "ok", "message": "Pago ya procesado"}
        booking.payment_status = payment_status
        session.add(booking)
        session.commit()
        logging.info(f"Reserva {booking.id} actualizada a estado: {payment_status}")
        if payment_status == "approved":
            user = session.get(User, booking.user_id)
            professional = session.get(Professional, booking.professional_id)
            if user and professional:
                logging.info(f"Encolando email de confirmaci\x01n para {user.email}")
                background_tasks.add_task(
                    send_booking_confirmation_email,
                    to_email=user.email,
                    user_name=user.name,
                    professional_name=professional.name,
                    date=booking.date,
                    time=booking.time,
                )
        return {"status": "ok", "message": f"Pago {payment_status}"}
    except Exception as e:
        session.rollback()
        logging.exception("Error procesando webhook de Mercado Pago")
        raise HTTPException(status_code=500, detail="Error interno del servidor")