# from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from core.models.base import Base
from .mixins import UserRelationMixin


# если сейчас идет проверка, а не выполнение кода
# что бы избежать циклических импортов
# if TYPE_CHECKING:
#     from user import User


class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="",         # значение для алхимии
        server_default=""   # значение для бд (не обязательно, но все же лучше писать)
    )
