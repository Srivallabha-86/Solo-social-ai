from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenRead, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=TokenRead, status_code=201)
async def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
) -> TokenRead:
    service = AuthService(db)
    if service.get_user_by_email(payload.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    try:
        user = service.register(payload.email, payload.password)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from exc
    return TokenRead(
        access_token=service.create_access_token(user),
        user=UserRead.model_validate(user),
    )


@router.post("/login", response_model=TokenRead)
async def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenRead:
    service = AuthService(db)
    user = service.authenticate(payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenRead(
        access_token=service.create_access_token(user),
        user=UserRead.model_validate(user),
    )


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
