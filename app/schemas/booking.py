from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

class BookingCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    travel_date: date
    number_of_people: int = Field(gt=0, le=20)
    package_id: int = Field(gt=0)
    @field_validator("travel_date")
    @classmethod
    def validate_travel_date(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Travel date cannot be in the past")
        return value


class BookingUpdate(BaseModel):
    customer_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    travel_date: date | None = None
    number_of_people: int | None = Field(
        default=None,
        gt=0,
        le=20,
    )

    model_config = ConfigDict(extra="forbid")
    @field_validator("travel_date")
    @classmethod
    def validate_travel_date(cls, value: date | None) -> date | None:
        if value is not None and value < date.today():
            raise ValueError("Travel date cannot be in the past")
        return value


class BookingResponse(BaseModel):
    id: int
    customer_name: str
    travel_date: date
    number_of_people: int
    total_price: float
    status: str
    package_id: int

    model_config = ConfigDict(from_attributes=True)
