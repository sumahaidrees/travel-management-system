from pydantic import BaseModel, ConfigDict, Field


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
