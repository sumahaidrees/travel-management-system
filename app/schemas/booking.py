from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BookingCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    travel_date: date
    number_of_people: int = Field(gt=0, le=20)
    package_id: int = Field(gt=0)


class BookingUpdate(BaseModel):
    customer_name: str | None = Field(None, min_length=2, max_length=100)
    travel_date: date | None = None
    number_of_people: int | None = Field(None, gt=0, le=20)


class BookingResponse(BaseModel):
    id: int
    customer_name: str
    travel_date: date
    number_of_people: int
    total_price: float
    status: str
    package_id: int

    model_config = ConfigDict(from_attributes=True)
