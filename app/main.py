
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models
from app.models import Destination, Package
from app.schemas import (
    DestinationCreate,
    DestinationResponse,
    PackageCreate,
    PackageResponse,
)
from app.schemas import BookingUpdate
from app.models import Booking
from app.schemas import BookingCreate, BookingResponse
from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.schemas import UserCreate, UserResponse

import os
import jwt
from app.schemas import UserLogin 
from datetime import datetime, timedelta, timezone


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials




app = FastAPI(title="Travel Agency Management System")
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing from .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_hash = PasswordHash.recommended()



@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=password_hash.hash(data.password)
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    return user

@app.post("/auth/login")
def login_user(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if user is None or not password_hash.verify(
        data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token = jwt.encode(
        {
            "sub": str(user.id),
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user_id = int(user_id)

    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive"
        )

    return user


def get_admin_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


@app.get("/auth/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user



@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)






# # Home and database check





# DESTINATION CRUD


@app.post("/destinations", response_model=DestinationResponse)
def create_destination(
    data: DestinationCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    destination = Destination(**data.model_dump())

    db.add(destination)
    db.commit()
    db.refresh(destination)

    return destination



@app.get("/destinations", response_model=list[DestinationResponse])
def get_destinations(db: Session = Depends(get_db)):
    return db.query(Destination).all()


@app.get(
    "/destinations/{destination_id}",
    response_model=DestinationResponse,
)
def get_destination(
    destination_id: int,
    db: Session = Depends(get_db),
):
    destination = db.get(Destination, destination_id)

    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    return destination


@app.put(
    "/destinations/{destination_id}",
    response_model=DestinationResponse,
)
def update_destination(
    destination_id: int,
    data: DestinationCreate,
    db: Session = Depends(get_db),
):
    destination = db.get(Destination, destination_id)

    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    destination.name = data.name
    destination.country = data.country
    destination.description = data.description

    db.commit()
    db.refresh(destination)
    return destination


@app.delete("/destinations/{destination_id}")
def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),
):
    destination = db.get(Destination, destination_id)

    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    db.delete(destination)
    db.commit()
    return {"message": "Destination deleted successfully"}




@app.post("/packages", response_model=PackageResponse, status_code=201)
def create_package(
    data: PackageCreate,
    db: Session = Depends(get_db),
):
    destination = db.get(Destination, data.destination_id)

    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    package = Package(**data.model_dump())
    db.add(package)
    db.commit()
    db.refresh(package)
    return package


@app.get("/packages", response_model=list[PackageResponse])
def get_packages(db: Session = Depends(get_db)):
    return db.query(Package).all()


@app.get("/packages/{package_id}", response_model=PackageResponse)
def get_package(
    package_id: int,
    db: Session = Depends(get_db),
):
    package = db.get(Package, package_id)

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    return package


@app.put("/packages/{package_id}", response_model=PackageResponse)
def update_package(
    package_id: int,
    data: PackageCreate,
    db: Session = Depends(get_db),
):
    package = db.get(Package, package_id)

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    destination = db.get(Destination, data.destination_id)

    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    package.title = data.title
    package.price = data.price
    package.duration_days = data.duration_days
    package.destination_id = data.destination_id

    db.commit()
    db.refresh(package)
    return package


@app.delete("/packages/{package_id}")
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
):
    package = db.get(Package, package_id)

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    db.delete(package)
    db.commit()
    return {"message": "Package deleted successfully"}


@app.get("/destinations/{destination_id}/packages")
def get_destination_packages(
    destination_id: int,
    db: Session = Depends(get_db)
):
    destination = db.get(Destination, destination_id)

    if destination is None:
        raise HTTPException(
            status_code=404,
            detail="Destination not found"
        )

    return [
        {
            "id": package.id,
            "title": package.title,
            "price": float(package.price),
            "duration_days": package.duration_days
        }
        for package in destination.packages
    ]

@app.post("/bookings", response_model=BookingResponse)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    package = db.query(Package).filter(
        Package.id == data.package_id
    ).first()

    if package is None:
        raise HTTPException(
            status_code=404,
            detail="Package not found"
        )

    total_price = package.price * data.number_of_people

    booking = Booking(
        customer_name=data.customer_name,
        travel_date=data.travel_date,
        number_of_people=data.number_of_people,
        package_id=data.package_id,
        total_price=total_price,
        user_id=current_user.id
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@app.get("/bookings", response_model=list[BookingResponse])
def get_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).all()

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


@app.patch("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    data: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    updates = data.model_dump(exclude_unset=True)

    if "number_of_people" in updates:
        if updates["number_of_people"] is None or updates["number_of_people"] < 1:
            raise HTTPException(
                status_code=422,
                detail="Number of people must be at least 1"
            )

    if "customer_name" in updates and not updates["customer_name"]:
        raise HTTPException(
            status_code=422,
            detail="Customer name cannot be empty"
        )

    if "travel_date" in updates and updates["travel_date"] is None:
        raise HTTPException(
            status_code=422,
            detail="Travel date cannot be null"
        )

    if "status" in updates:
        raise HTTPException(
            status_code=422,
            detail="Use the cancel endpoint to cancel a booking"
        )

    for field, value in updates.items():
        setattr(booking, field, value)

    package = db.get(Package, booking.package_id)

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    booking.total_price = package.price * booking.number_of_people

    db.commit()
    db.refresh(booking)

    return booking



@app.patch("/bookings/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Booking is already cancelled"
        )

    booking.status = "cancelled"

    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking cancelled successfully",
        "booking_id": booking.id,
        "status": booking.status
    }
