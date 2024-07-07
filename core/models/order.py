from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import func
from datetime import datetime


if TYPE_CHECKING:
    from core.models.product import Product
    from core.models.order_product_association import OrderProductAssociation


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now
    )
    product: Mapped[list["Product"]] = relationship(
        secondary="order_product_association",
        back_populates="order"
    )

    # association between Parent -> Association -> Child
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order",
    )
