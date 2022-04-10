import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from typing import Optional, Tuple
from datetime import datetime, timedelta

from settings import settings
from .code import INVALID_TOKEN, INVALID_AUTH, INVALID_AUTH_SCHEMA


__all__ = ["create_access_token", "JWTBearer", "token_decode"]

def token_decode(token):
    try:
        access_token = token.replace("Bearer ", "")
        payload = jwt.decode(
            access_token,
            key=settings.APP_SECRET_KEY,
            algorithms=["HS256"],
        )
    except (ExpiredSignatureError, DecodeError):
        raise
    return payload

def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = {}

    if data is not None:
        to_encode = data.copy()

    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})

    encoded_jwt = jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if credentials:
            user_id, valid = self.verify_jwt(credentials.credentials)

            if not credentials.scheme == "Bearer":
                raise HTTPException(**INVALID_AUTH_SCHEMA)
            if not valid:
                raise HTTPException(**INVALID_TOKEN)
            if user_id is None:
                raise HTTPException(**INVALID_AUTH)
            return str(user_id)
        else:
            raise HTTPException(**INVALID_AUTH)

    @staticmethod
    def verify_jwt(token: str) -> Tuple[Optional[int], bool]:
        valid: bool = False
        user_id: Optional[int] = None

        try:
            payload = token_decode(token)
            user_id = payload.get("id")
        except Exception:
            pass

        if user_id:
            valid = True

        return user_id, valid
