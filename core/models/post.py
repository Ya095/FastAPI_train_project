from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from core.models.base import Base


# если сейчас идет проверка, а не выполнение кода
# что бы избежать циклических импортов
if TYPE_CHECKING:
    from user import User


class Post(Base):
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="",         # значение для алхимии
        server_default=""   # значение для бд (не обязательно, но все же лучше писать)
    )
    # внешний ключ
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )
    user: Mapped["User"] = relationship(back_populates="posts")
