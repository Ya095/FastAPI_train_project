from typing import TYPE_CHECKING
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base


if TYPE_CHECKING:
    from core.models.order import Order
    from core.models.product import Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
            name="idx_unique_order_product"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    count: Mapped[int] = mapped_column(default=1, server_default="1")
    unit_price: Mapped[int] = mapped_column(default=0, server_default="0")

    # association between Assocation -> Order
    order: Mapped["Order"] = relationship(back_populates="products_details",)
    # association between Assocation -> Product
    product: Mapped["Product"] = relationship(back_populates="orders_details",)


# order_product_association_table = Table(
#     "order_product_association",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("order_id", ForeignKey("order.id"), nullable=False),
#     Column("product_id", ForeignKey("product.id"), nullable=False),
#     UniqueConstraint("order_id", "product_id", name="idx_unique_order_product")
# )

