from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate


def create_warehouse(warehouse: WarehouseCreate, db: Session):

    existing_warehouse = db.query(Warehouse).filter(
        Warehouse.warehouse_name == warehouse.warehouse_name
    ).first()

    if existing_warehouse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Warehouse already exists"
        )

    new_warehouse = Warehouse(
        warehouse_name=warehouse.warehouse_name,
        location=warehouse.location,
        manager_name=warehouse.manager_name,
        is_active=warehouse.is_active
    )

    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)

    return new_warehouse


def get_all_warehouses(db: Session):

    return db.query(Warehouse).all()


def get_warehouse_by_id(warehouse_id: int, db: Session):

    warehouse = db.query(Warehouse).filter(
        Warehouse.id == warehouse_id
    ).first()

    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )

    return warehouse


def update_warehouse(
    warehouse_id: int,
    warehouse_data: WarehouseUpdate,
    db: Session
):

    warehouse = db.query(Warehouse).filter(
        Warehouse.id == warehouse_id
    ).first()

    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )

    if (
        warehouse_data.warehouse_name is not None
        and warehouse_data.warehouse_name != warehouse.warehouse_name
    ):
        existing = db.query(Warehouse).filter(
            Warehouse.warehouse_name == warehouse_data.warehouse_name
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Warehouse name already exists"
            )

    update_data = warehouse_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(warehouse, key, value)

    db.commit()
    db.refresh(warehouse)

    return warehouse


def delete_warehouse(
    warehouse_id: int,
    db: Session
):

    warehouse = db.query(Warehouse).filter(
        Warehouse.id == warehouse_id
    ).first()

    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )

    db.delete(warehouse)
    db.commit()

    return {
        "message": "Warehouse deleted successfully"
    }