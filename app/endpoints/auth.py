from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.auth_controller import login_user, register_user
from app.core.security import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(data, db)


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(data, db)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
