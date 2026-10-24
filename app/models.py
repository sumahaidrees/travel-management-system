from sqlalchemy import String, Integer, ForeignKey, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import date
from sqlalchemy import Date
from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    role = Column(String(20), default="user", nullable=False)

    bookings = relationship("Booking", back_populates="user")



class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


    packages: Mapped[list["Package"]] = relationship(
        back_populates="destination"
    )


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)

    destination_id: Mapped[int] = mapped_column(
        ForeignKey("destinations.id"),
        nullable=False
    )

  
    destination: Mapped["Destination"] = relationship(
        back_populates="packages"
    )



class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="bookings")

    customer_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    travel_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    number_of_people: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    total_price: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )

    package_id: Mapped[int] = mapped_column(
        ForeignKey("packages.id"), nullable=False
    )
