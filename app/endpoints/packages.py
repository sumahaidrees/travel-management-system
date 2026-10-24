from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.package_controller import (
    create_package,
    delete_package,
    get_package,
    get_packages,
    update_package,
)
from app.database import get_db
from app.schemas import PackageCreate, PackageResponse

router = APIRouter(tags=["packages"])


@router.post("/packages", response_model=PackageResponse, status_code=201)
def create(data: PackageCreate, db: Session = Depends(get_db)):
    return create_package(data, db)


@router.get("/packages", response_model=list[PackageResponse])
def list_all(db: Session = Depends(get_db)):
    return get_packages(db)


@router.get("/packages/{package_id}", response_model=PackageResponse)
def get_one(package_id: int, db: Session = Depends(get_db)):
    return get_package(package_id, db)


@router.put("/packages/{package_id}", response_model=PackageResponse)
def update(
    package_id: int,
    data: PackageCreate,
    db: Session = Depends(get_db),
):
    return update_package(package_id, data, db)


@router.delete("/packages/{package_id}")
def delete(package_id: int, db: Session = Depends(get_db)):
    return delete_package(package_id, db)
