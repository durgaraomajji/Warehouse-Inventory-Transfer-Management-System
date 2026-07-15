from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Date,
    String,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    from_warehouse = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    to_warehouse = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    transfer_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="Pending"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships

    source_warehouse = relationship(
        "Warehouse",
        foreign_keys=[from_warehouse],
        back_populates="outgoing_transfers"
    )

    destination_warehouse = relationship(
        "Warehouse",
        foreign_keys=[to_warehouse],
        back_populates="incoming_transfers"
    )

    product = relationship(
        "Product",
        back_populates="transfers"
    )