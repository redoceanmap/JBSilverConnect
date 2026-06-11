from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.reservation.adapter.inbound.api.schemas.reservation_schema import (
    CreateReservationRequest,
    ReservationResponse,
)
from jb.apps.reservation.app.dtos.reservation_dto import CreateReservationCommand
from jb.apps.reservation.app.ports.input.create_reservation_use_case import (
    CreateReservationUseCase,
)
from jb.apps.reservation.dependencies.reservation_provider import (
    get_create_reservation_use_case,
)

reservation_router = APIRouter(prefix="/reservation", tags=["reservation"])


@reservation_router.post("/tickets", response_model=ReservationResponse)
async def create_reservation(
    body: CreateReservationRequest,
    usecase: CreateReservationUseCase = Depends(get_create_reservation_use_case),
) -> ReservationResponse:
    view = await usecase.execute(
        CreateReservationCommand(user_id=body.user_id, purpose=body.purpose)
    )
    return ReservationResponse(
        ticket_number=view.ticket_number,
        purpose=view.purpose,
        message=view.message,
    )
