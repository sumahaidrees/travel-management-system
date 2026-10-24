from pydantic import BaseModel, ConfigDict, Field


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
