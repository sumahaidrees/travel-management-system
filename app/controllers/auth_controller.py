from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    password_hash,
)
from app.models import User
from app.schemas import UserCreate, UserLogin


def register_user(data: UserCreate, db: Session):
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=password_hash.hash(data.password),
    )
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email is already registered")

    return user


def login_user(data: UserLogin, db: Session):
    user = db.query(User).filter(User.email == data.email).first()

    if user is None or not password_hash.verify(
        data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = jwt.encode(
        {"sub": str(user.id), "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {"access_token": token, "token_type": "bearer"}
