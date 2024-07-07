from sqlalchemy.orm import Mapped, relationship
from core.models.base import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from core.models.order import Order
    from core.models.order_product_association import OrderProductAssociation


class Product(Base):
    # __tablename__ = "product"

    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]
    order: Mapped[list["Order"]] = relationship(
        secondary="order_product_association",
        back_populates="product"
    )

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )
