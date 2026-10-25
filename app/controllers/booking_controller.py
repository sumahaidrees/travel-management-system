from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Booking, Package, User
from datetime import datetime, timedelta, timezone
from app.schemas import BookingCreate, BookingUpdate


def create_booking(data: BookingCreate, db: Session, current_user: User):
    package = db.query(Package).filter(Package.id == data.package_id).first()
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    booking = Booking(
        **data.model_dump(),
        total_price=package.price * data.number_of_people,
        user_id=current_user.id,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_bookings(db: Session, current_user: User):
    query = db.query(Booking)

    if current_user.role != "admin":
        query = query.filter(Booking.user_id == current_user.id)

    return query.all()


def get_booking(booking_id: int, db: Session, current_user: User):
    query = db.query(Booking).filter(Booking.id == booking_id)

    if current_user.role != "admin":
        query = query.filter(Booking.user_id == current_user.id)

    booking = query.first()

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking



def update_booking(
    booking_id: int,
    data: BookingUpdate,
    db: Session,
    current_user: User,
):
    booking = get_booking(booking_id, db, current_user)

    if booking.status in ("cancelled", "completed"):
        raise HTTPException(
        status_code=400,
        detail="Cancelled or completed bookings cannot be updated",
    )
    updates = data.model_dump(exclude_unset=True)

    if "number_of_people" in updates and (
        updates["number_of_people"] is None or updates["number_of_people"] < 1
    ):
        raise HTTPException(status_code=422, detail="Number of people must be at least 1")
    if "customer_name" in updates and not updates["customer_name"]:
        raise HTTPException(status_code=422, detail="Customer name cannot be empty")
    if "travel_date" in updates and updates["travel_date"] is None:
        raise HTTPException(status_code=422, detail="Travel date cannot be null")
    if "status" in updates:
        raise HTTPException(status_code=422, detail="Use the cancel endpoint to cancel a booking")

    for field, value in updates.items():
        setattr(booking, field, value)

    package = db.get(Package, booking.package_id)
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    booking.total_price = package.price * booking.number_of_people
    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(booking_id: int, db: Session, current_user: User):
    booking = get_booking(booking_id, db, current_user)

    if booking.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Booking is already cancelled",
        )

    if booking.status == "completed":
        raise HTTPException(
            status_code=400,
            detail="Completed bookings cannot be cancelled",
        )

    now = datetime.now(timezone.utc)
    created_at = booking.created_at

    # Handle timestamps without timezone information
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    if now - created_at > timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail="Booking can only be cancelled within 24 hours of creation",
        )

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking cancelled successfully",
        "booking_id": booking.id,
        "status": booking.status,
    }