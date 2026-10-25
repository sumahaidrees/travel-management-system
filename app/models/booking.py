from datetime import date, datetime,timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="bookings")
    customer_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    default=lambda: datetime.now(timezone.utc),
)
    travel_date: Mapped[date] = mapped_column(Date, nullable=False)
    number_of_people: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default="confirmed", nullable=False
    )
    package_id: Mapped[int] = mapped_column(
        ForeignKey("packages.id"), nullable=False
    )
