from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Destination, Package
from app.schemas import PackageCreate


def create_package(data: PackageCreate, db: Session):
    destination = db.get(Destination, data.destination_id)
    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    package = Package(**data.model_dump())
    db.add(package)
    db.commit()
    db.refresh(package)
    return package


def get_packages(db: Session):
    return db.query(Package).all()


def get_package(package_id: int, db: Session):
    package = db.get(Package, package_id)
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return package


def update_package(package_id: int, data: PackageCreate, db: Session):
    package = get_package(package_id, db)
    destination = db.get(Destination, data.destination_id)
    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    package.title = data.title
    package.price = data.price
    package.duration_days = data.duration_days
    package.destination_id = data.destination_id
    db.commit()
    db.refresh(package)
    return package


def delete_package(package_id: int, db: Session):
    package = get_package(package_id, db)
    db.delete(package)
    db.commit()
    return {"message": "Package deleted successfully"}
