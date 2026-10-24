from fastapi import FastAPI

from app import models as _models
from app.database import Base, engine
from app.endpoints import auth, bookings, destinations, packages

app = FastAPI(title="Travel Agency Management System")

app.include_router(auth.router)
app.include_router(destinations.router)
app.include_router(packages.router)
app.include_router(bookings.router)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
