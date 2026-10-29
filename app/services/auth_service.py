from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User

password_hash = PasswordHash.recommended()


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def register(self, email: str, password: str) -> User:
        user = User(email=email, password_hash=password_hash.hash(password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.get_user_by_email(email)
        if user is None or not password_hash.verify(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_access_token(user: User) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes,
        )
        return jwt.encode(
            {"sub": str(user.id), "exp": expires_at},
            settings.token_secret(),
            algorithm="HS256",
        )

    @staticmethod
    def user_id_from_token(token: str) -> int:
        payload = jwt.decode(
            token,
            settings.token_secret(),
            algorithms=["HS256"],
            options={"require": ["exp", "sub"]},
        )
        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject.isdecimal():
            raise jwt.InvalidTokenError("Invalid user identifier.")
        return int(subject)
