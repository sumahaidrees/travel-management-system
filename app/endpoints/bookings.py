from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.booking_controller import (
    cancel_booking,
    create_booking,
    get_booking,
    get_bookings,
    update_booking,
)
from app.core.security import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import BookingCreate, BookingResponse, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingResponse)
def create(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_booking(data, db, current_user)


@router.get("", response_model=list[BookingResponse])
def list_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_bookings(db, current_user)


@router.get("/{booking_id}", response_model=BookingResponse)
def get_one(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_booking(booking_id, db, current_user)


@router.patch("/{booking_id}", response_model=BookingResponse)
def update(
    booking_id: int,
    data: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_booking(booking_id, data, db, current_user)


@router.patch("/{booking_id}/cancel")
def cancel(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cancel_booking(booking_id, db, current_user)
