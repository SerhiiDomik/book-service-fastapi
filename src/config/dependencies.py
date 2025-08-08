from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.config.settings import Settings
from src.security.interfaces import JWTAuthManagerInterface
from src.security.token_manager import JWTAuthManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_settings() -> Settings:
    return settings


def get_jwt_auth_manager(
    settings: Settings = Depends(get_settings),
) -> JWTAuthManagerInterface:
    return JWTAuthManager(
        secret_key_access=settings.SECRET_KEY_ACCESS,
        secret_key_refresh=settings.SECRET_KEY_REFRESH,
        algorithm=settings.JWT_SIGNING_ALGORITHM,
    )
