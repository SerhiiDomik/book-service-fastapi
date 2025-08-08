import enum
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database.session import Base
from src.security.utils import generate_secure_token


class RoleEnum(str, enum.Enum):
    reader = "reader"
    writer = "writer"
    admin = "admin"


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(RoleEnum), unique=True, nullable=False)

    users = relationship("User", back_populates="group")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey("user_groups.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    group = relationship("UserGroup", back_populates="users")

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(512), unique=True, nullable=False, default=generate_secure_token)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")

    @classmethod
    def create(cls, token: str, user_id: int, *, ttl_minutes: int = 60 * 24 * 7):
        expire = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
        return cls(token=token, user_id=user_id, expires_at=expire)
