import uuid
from time import time
from typing import Annotated
import secrets
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo_auth", tags=["Demo Auth"])

security = HTTPBasic()


#### самая простая аутентификация
@router.get("/basic-auth")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }


#### аутентификация basic (логин/пароль)
username_to_password = {
    "admin": "admin",
    "John": "12345",

}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password!",
        headers={"WWW-Authenticate": "Basic"}
    )
    correct_password = username_to_password.get(credentials.username)
    if not correct_password:
        raise unauthed_exc

    # secrets (сравнение паролей)
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8")
    ):
        raise unauthed_exc

    return credentials.username


@router.get("/basic-auth-username")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username)
):
    return {
        "message": f"Hi, {auth_username}",
        "username": auth_username,
    }


#### аутентификация по заголовку и токену
static_auth_token_to_user = {
    "fdasdr2f8q8gh8v3q493qvb": "admin",
    "ddafjgjobae942-924g2b2d": "John"
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token")
):
    if static_token not in static_auth_token_to_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid"
        )

    return static_auth_token_to_user[static_token]


@router.get("/some-http-header-auth")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token)
):
    return {
        "message": f"Hi, {username}",
        "username": username,
    }


#### аутентификация через куки
cookie = {}
cookie_session_id_key = "some-string-aaafff"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
    session_id: str = Cookie(alias=cookie_session_id_key)
) -> dict:
    if session_id not in cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    return cookie[session_id]


# в начале нужна хоть какая-то аутентификация (любым способом)
@router.post("/login-cookie")
def demo_auth_login_set_cookie(
    responce: Response,
    auth_username: str = Depends(get_auth_user_username),
    # username: str = Depends(get_username_by_static_auth_token)
):
    session_id = generate_session_id()
    cookie[session_id] = {
        "username": auth_username,
        "login_at": int(time()),
    }
    responce.set_cookie(cookie_session_id_key, session_id)

    return {
        "result": "ok"
    }


@router.get("/check-cookei")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data)
):
    username = user_session_data["username"]
    return {
        "message": f"Hello, {username}!",
        **user_session_data,
    }
