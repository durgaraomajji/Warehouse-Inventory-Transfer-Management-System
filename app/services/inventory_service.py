from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse


def create_inventory(
    warehouse_id: int,
    product_id: int,
    quantity: int,
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

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id,
        Inventory.product_id == product_id
    ).first()

    if inventory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inventory already exists"
        )

    new_inventory = Inventory(
        warehouse_id=warehouse_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory


def get_inventory(
    warehouse_id: int,
    product_id: int,
    db: Session
):

    inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id,
        Inventory.product_id == product_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found"
        )

    return inventory


def increase_stock(
    warehouse_id: int,
    product_id: int,
    quantity: int,
    db: Session
):

    inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id,
        Inventory.product_id == product_id
    ).first()

    if inventory is None:

        inventory = Inventory(
            warehouse_id=warehouse_id,
            product_id=product_id,
            quantity=quantity
        )

        db.add(inventory)

    else:

        inventory.quantity += quantity

    db.commit()
    db.refresh(inventory)

    return inventory


def decrease_stock(
    warehouse_id: int,
    product_id: int,
    quantity: int,
    db: Session
):

    inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id,
        Inventory.product_id == product_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found"
        )

    if inventory.quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )

    inventory.quantity -= quantity

    db.commit()
    db.refresh(inventory)

    return inventory


def update_inventory(
    warehouse_id: int,
    product_id: int,
    quantity: int,
    db: Session
):

    inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id,
        Inventory.product_id == product_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found"
        )

    inventory.quantity = quantity

    db.commit()
    db.refresh(inventory)

    return inventory


def delete_inventory(
    warehouse_id: int,
    product_id: int,
    db: Session
):

    inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id,
        Inventory.product_id == product_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found"
        )

    db.delete(inventory)
    db.commit()

    return {
        "message": "Inventory deleted successfully"
    }


def get_inventory_by_warehouse(
    warehouse_id: int,
    db: Session
):

    return db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id
    ).all()


def get_all_inventory(
    db: Session
):

    return db.query(Inventory).all()