from src.security.token_manager import JWTAuthManager
from src.config.settings import settings

jwt_manager = JWTAuthManager(
    secret_key_access=settings.SECRET_KEY_ACCESS,
    secret_key_refresh=settings.SECRET_KEY_REFRESH,
    algorithm=settings.JWT_SIGNING_ALGORITHM
)

def create_access_token(data: dict) -> str:
    return jwt_manager.create_access_token(data)

def create_refresh_token(data: dict) -> str:
    return jwt_manager.create_refresh_token(data)

def decode_access_token(token: str) -> dict:
    return jwt_manager.decode_access_token(token)

def decode_refresh_token(token: str) -> dict:
    return jwt_manager.decode_refresh_token(token)
