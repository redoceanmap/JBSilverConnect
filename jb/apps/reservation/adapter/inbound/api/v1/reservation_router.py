from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.reservation.adapter.inbound.api.schemas.reservation_schema import (
    CreateReservationRequest,
    ReservationResponse,
)
from jb.apps.reservation.app.dtos.reservation_dto import (
    CancelReservationCommand,
    CreateReservationCommand,
    ListReservationsQuery,
    ReservationView,
)
from jb.apps.reservation.app.ports.input.cancel_reservation_use_case import (
    CancelReservationUseCase,
)
from jb.apps.reservation.app.ports.input.create_reservation_use_case import (
    CreateReservationUseCase,
)
from jb.apps.reservation.app.ports.input.list_queue_use_case import ListQueueUseCase
from jb.apps.reservation.app.ports.input.list_reservations_use_case import (
    ListReservationsUseCase,
)
from jb.apps.reservation.dependencies.reservation_provider import (
    get_cancel_reservation_use_case,
    get_create_reservation_use_case,
    get_list_queue_use_case,
    get_list_reservations_use_case,
)

reservation_router = APIRouter(prefix="/reservation", tags=["reservation"])


def _to_response(view: ReservationView) -> ReservationResponse:
    return ReservationResponse(
        reservation_id=view.reservation_id,
        ticket_number=view.ticket_number,
        purpose=view.purpose,
        message=view.message,
        status=view.status,
        branch_name=view.branch_name,
        note=view.note,
    )


@reservation_router.post("/tickets", response_model=ReservationResponse)
async def create_reservation(
    body: CreateReservationRequest,
    usecase: CreateReservationUseCase = Depends(get_create_reservation_use_case),
) -> ReservationResponse:
    view = await usecase.execute(
        CreateReservationCommand(
            user_id=body.user_id,
            purpose=body.purpose,
            branch_name=body.branch_name,
            note=body.note,
        )
    )
    return _to_response(view)


@reservation_router.get("/tickets", response_model=list[ReservationResponse])
async def list_reservations(
    user_id: str = "user_kim_sonja",
    usecase: ListReservationsUseCase = Depends(get_list_reservations_use_case),
) -> list[ReservationResponse]:
    views = await usecase.execute(ListReservationsQuery(user_id=user_id))
    return [_to_response(view) for view in views]


@reservation_router.get("/queue", response_model=list[ReservationResponse])
async def list_queue(
    usecase: ListQueueUseCase = Depends(get_list_queue_use_case),
) -> list[ReservationResponse]:
    """창구(어드민)용 — 전체 활성 번호표를 번호순으로 조회한다."""
    views = await usecase.execute()
    return [_to_response(view) for view in views]


@reservation_router.post(
    "/tickets/{reservation_id}/cancel", response_model=ReservationResponse
)
async def cancel_reservation(
    reservation_id: str,
    usecase: CancelReservationUseCase = Depends(get_cancel_reservation_use_case),
) -> ReservationResponse:
    view = await usecase.execute(CancelReservationCommand(reservation_id=reservation_id))
    return _to_response(view)
