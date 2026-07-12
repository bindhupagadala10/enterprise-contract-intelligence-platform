from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.db.models.user import User
from app.schemas.user import UserRegisterRequest

password_hash = PasswordHash.recommended()


class AuthService:

    @staticmethod
    def register(
        request: UserRegisterRequest,
        db: Session,
    ):

        existing_user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:
            raise ValueError("Email already registered.")

        user = User(
            name=request.name,
            email=request.email,
            hashed_password=password_hash.hash(
                request.password
            ),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user