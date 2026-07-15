from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    UserCreate,
    UserResponse,
    Token
)
from app.services.auth_service import (
    register_user,
    login_user,
    get_user_by_id,
    get_all_users
)
from app.oauth2 import get_current_user
from app.dependencies import admin_required

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(user, db)


@router.post(
    "/login",
    response_model=Token
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(user_credentials, db)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_logged_in_user(
    current_user=Depends(get_current_user)
):
    return current_user


@router.get(
    "/users",
    response_model=list[UserResponse]
)
def users(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return get_all_users(db)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return get_user_by_id(user_id, db)