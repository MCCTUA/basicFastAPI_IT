from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.user import User, UserCreate
from app.services import user_service
from app.core.limiter import limiter

router = APIRouter()


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")  # จำกัดการเรียกใช้งาน 5 ครั้งต่อนาที
async def login_access_token(
    request: Request,  # จำเป็นต้องรับ Request เข้ามาเพื่อให้ Limiter ทำงาน
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = await user_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/register", response_model=User)
async def register_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    user = await user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await user_service.create_user(db, user=user_in)
    return user


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    refresh_token: str,
) -> Any:
    # In a real application, you should verify the refresh token and check if it's in the database or blacklist
    # For simplicity, we just decode it and create a new access token
    try:
        payload = security.jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            token_data, expires_delta=access_token_expires
        ),
        "refresh_token": refresh_token,  # Return the same refresh token or rotate it
        "token_type": "bearer",
    }


# logout ต้องไปทำเพิ่ม เนื่องจาก JWT เมื่อออกแล้วจะใช้ได้จนกว่าจะหมดอายุเองไม่สามารถไปทำลายได้ เราต้องทำ "Token Blocklist" เอง ให้ค้นหาวิธีการ โดยใช้ Keyword "python jwt revoke token postgresql"
@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}
