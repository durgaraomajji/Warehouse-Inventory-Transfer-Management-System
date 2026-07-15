from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_name = Column(
        String(150),
        nullable=False,
        index=True
    )

    sku = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    stock_quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    unit_price = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    inventories = relationship(
        "Inventory",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    transfers = relationship(
        "Transfer",
        back_populates="product"
    )