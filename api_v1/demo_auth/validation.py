from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from starlette import status
from api_v1.demo_auth.crud import users_db
from api_v1.demo_auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth import utils as auth_utils
from users.schemas import UserSchema


http_bearer = HTTPBearer(auto_error=False)


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchema:
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {ex}"
        )

    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r}. Expected {token_type!r}"
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user not found"
    )


def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)

    return get_user_by_token_sub(payload)


def get_current_auth_user_for_refresh(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)

    return get_user_by_token_sub(payload)
