
from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from pydantic import EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)


class DestinationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)
    description: str | None = None

class PackageNestedResponse(BaseModel):
    id: int
    title: str
    price: float
    duration_days: int

    model_config = ConfigDict(from_attributes=True)

class DestinationResponse(BaseModel):
    id: int
    name: str
    country: str
    description: str | None
    packages: list[PackageNestedResponse] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class PackageCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    price: float = Field(gt=0)
    duration_days: int = Field(gt=0)
    destination_id: int = Field(gt=0)


class PackageResponse(BaseModel):
    id: int
    title: str
    price: float
    duration_days: int
    destination_id: int

    model_config = ConfigDict(from_attributes=True)

class BookingCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    travel_date: date
    number_of_people: int = Field(gt=0, le=20)
    package_id: int = Field(gt=0)



class BookingUpdate(BaseModel):
    customer_name: str | None = Field(
        default=None, min_length=2, max_length=100
    )
    travel_date: date | None = None
    number_of_people: int | None = Field(
        default=None, gt=0, le=20
    )


class BookingResponse(BaseModel):
    id: int
    customer_name: str
    travel_date: date
    number_of_people: int
    total_price: float
    status: str
    package_id: int

    model_config = ConfigDict(from_attributes=True)