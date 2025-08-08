from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm  # ⬅️ додай цей рядок

from src.database.session import get_db
from src.database.models.users import User, UserGroup, RoleEnum, RefreshToken
from src.schemas.users import (
    UserRegisterSchema,
    UserLoginSchema,
    UserResponseSchema,
    TokenSchema,
)
from src.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from src.config.dependencies import oauth2_scheme
from src.config.settings import settings

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    data: UserRegisterSchema,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = pwd_context.hash(data.password)

    reader_group = db.query(UserGroup).filter_by(name=RoleEnum.reader).first()
    if not reader_group:
        reader_group = UserGroup(name=RoleEnum.reader)
        db.add(reader_group)
        db.commit()
        db.refresh(reader_group)

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed,
        group_id=reader_group.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Authenticate user and return tokens",
)
@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Authenticate user and return tokens",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.group.name
    })
    refresh_token_str = create_refresh_token(
        {"sub": str(user.id)}
    )

    refresh_record = RefreshToken.create(
        token=refresh_token_str,
        user_id=user.id,
        ttl_minutes=settings.LOGIN_TIME_DAYS * 24 * 60,
    )
    db.add(refresh_record)
    db.commit()

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token_str,
        token_type="bearer",
    )

@router.post(
    "/refresh",
    response_model=TokenSchema,
    summary="Refresh access token",
)
def refresh(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_refresh_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    stored = db.query(RefreshToken).filter_by(token=token, user_id=user_id).first()
    if not stored or stored.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or not found",
        )

    access_token = create_access_token({"sub": str(user_id)})
    return TokenSchema(
        access_token=access_token,
        refresh_token=token,
        token_type="bearer",
    )

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
)
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    deleted = db.query(RefreshToken).filter_by(token=token).delete()
    db.commit()
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token",
        )
    return {"message": "Successfully logged out"}

