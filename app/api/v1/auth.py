from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth_service import AuthService

from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
async def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):

    try:

        user = AuthService.register(
            request=request,
            db=db
        )

        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post(
    "/login",
    response_model=MessageResponse
)
async def login(
    request: UserLoginRequest
):
    return {
        "message": "Login endpoint"
    }