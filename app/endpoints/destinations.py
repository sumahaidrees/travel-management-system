from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_admin_user

from app.controllers.destination_controller import (
    create_destination,
    delete_destination,
    get_destination,
    get_destination_packages,
    get_destinations,
    update_destination,
)
from app.database import get_db
from app.models import User
from app.schemas import DestinationCreate, DestinationResponse

router = APIRouter(tags=["destinations"])


@router.post(
    "/destinations",
    response_model=DestinationResponse,
)
def create(
    data: DestinationCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    return create_destination(data, db)


@router.get("/destinations", response_model=list[DestinationResponse])
def list_all(db: Session = Depends(get_db)):
    return get_destinations(db)


@router.get(
    "/destinations/{destination_id}",
    response_model=DestinationResponse,
)
def get_one(destination_id: int, db: Session = Depends(get_db)):
    return get_destination(destination_id, db)


@router.put(
    "/destinations/{destination_id}",
    response_model=DestinationResponse,
)
def update(
    destination_id: int,
    data: DestinationCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    return update_destination(destination_id, data, db)


@router.delete("/destinations/{destination_id}")
def delete(destination_id: int, db: Session = Depends(get_db),_admin: User = Depends(get_admin_user),):
    return delete_destination(destination_id, db)


@router.get("/destinations/{destination_id}/packages")
def list_packages(destination_id: int, db: Session = Depends(get_db)):
    return get_destination_packages(destination_id, db)
