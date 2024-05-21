from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)  # String(32) - лимит по символам
