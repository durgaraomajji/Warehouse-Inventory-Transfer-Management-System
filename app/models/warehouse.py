from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)

    warehouse_name = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )

    location = Column(
        String(200),
        nullable=False
    )

    manager_name = Column(
        String(100),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    inventories = relationship(
        "Inventory",
        back_populates="warehouse",
        cascade="all, delete-orphan"
    )

    outgoing_transfers = relationship(
        "Transfer",
        foreign_keys="Transfer.from_warehouse",
        back_populates="source_warehouse"
    )

    incoming_transfers = relationship(
        "Transfer",
        foreign_keys="Transfer.to_warehouse",
        back_populates="destination_warehouse"
    )