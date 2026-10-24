from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Destination
from app.schemas import DestinationCreate


def create_destination(data: DestinationCreate, db: Session):
    destination = Destination(**data.model_dump())
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination


def get_destinations(db: Session):
    return db.query(Destination).all()


def get_destination(destination_id: int, db: Session):
    destination = db.get(Destination, destination_id)
    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination


def update_destination(
    destination_id: int,
    data: DestinationCreate,
    db: Session,
):
    destination = get_destination(destination_id, db)
    destination.name = data.name
    destination.country = data.country
    destination.description = data.description
    db.commit()
    db.refresh(destination)
    return destination


def delete_destination(destination_id: int, db: Session):
    destination = get_destination(destination_id, db)
    db.delete(destination)
    db.commit()
    return {"message": "Destination deleted successfully"}


def get_destination_packages(destination_id: int, db: Session):
    destination = get_destination(destination_id, db)
    return [
        {
            "id": package.id,
            "title": package.title,
            "price": float(package.price),
            "duration_days": package.duration_days,
        }
        for package in destination.packages
    ]
