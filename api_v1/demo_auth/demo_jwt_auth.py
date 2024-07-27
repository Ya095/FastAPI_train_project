from api_v1.demo_auth.helpers import (
    create_access_token, create_refresh_token
)
from api_v1.demo_auth.validation import http_bearer, get_current_auth_user, get_current_auth_user_for_refresh
from api_v1.demo_auth.crud import users_db
from users.schemas import UserSchema
from auth import utils as auth_utils
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Form, HTTPException, status

router = APIRouter(prefix="/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


def validate_auth_user(
    username: str = Form(),
    password: str = Form()
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(password, user.password):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive"
        )

    return user


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive"
    )


@router.post("/login", response_model=TokenInfo, response_model_exclude_none=True)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(user: UserSchema = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)

    return TokenInfo(
        access_token=access_token
    )


@router.get("/users/me")
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_auth_user)
):
    return {
        "username": user.username,
        "email": user.email
    }