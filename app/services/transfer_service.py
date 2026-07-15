from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.transfer import Transfer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.schemas.transfer import TransferCreate, TransferUpdate


def create_transfer(
    transfer: TransferCreate,
    db: Session
):

    if transfer.from_warehouse == transfer.to_warehouse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source and destination warehouses cannot be the same"
        )

    source_warehouse = db.query(Warehouse).filter(
        Warehouse.id == transfer.from_warehouse
    ).first()

    if source_warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source warehouse not found"
        )

    destination_warehouse = db.query(Warehouse).filter(
        Warehouse.id == transfer.to_warehouse
    ).first()

    if destination_warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination warehouse not found"
        )

    product = db.query(Product).filter(
        Product.id == transfer.product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    source_inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == transfer.from_warehouse,
        Inventory.product_id == transfer.product_id
    ).first()

    if source_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not available in source warehouse"
        )

    if source_inventory.quantity < transfer.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )

    new_transfer = Transfer(
        from_warehouse=transfer.from_warehouse,
        to_warehouse=transfer.to_warehouse,
        product_id=transfer.product_id,
        quantity=transfer.quantity,
        transfer_date=transfer.transfer_date,
        status="Pending"
    )

    db.add(new_transfer)
    db.commit()
    db.refresh(new_transfer)

    return new_transfer


def get_all_transfers(
    db: Session
):

    return db.query(Transfer).all()


def get_transfer_by_id(
    transfer_id: int,
    db: Session
):

    transfer = db.query(Transfer).filter(
        Transfer.id == transfer_id
    ).first()

    if transfer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transfer not found"
        )

    return transfer


def get_transfers_by_status(
    status_value: str,
    db: Session
):

    return db.query(Transfer).filter(
        Transfer.status == status_value
    ).all()
    
def update_transfer(
    transfer_id: int,
    transfer_data: TransferUpdate,
    db: Session
):

    transfer = db.query(Transfer).filter(
        Transfer.id == transfer_id
    ).first()

    if transfer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transfer not found"
        )

    if transfer_data.status:

        if transfer_data.status == "Cancelled":

            transfer.status = "Cancelled"

            db.commit()
            db.refresh(transfer)

            return transfer

        if transfer_data.status == "Approved":

            transfer.status = "Approved"

            db.commit()
            db.refresh(transfer)

            return transfer

        if transfer_data.status == "Completed":

            source_inventory = db.query(Inventory).filter(
                Inventory.warehouse_id == transfer.from_warehouse,
                Inventory.product_id == transfer.product_id
            ).first()

            if source_inventory is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Source inventory not found"
                )

            if source_inventory.quantity < transfer.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient stock"
                )

            destination_inventory = db.query(Inventory).filter(
                Inventory.warehouse_id == transfer.to_warehouse,
                Inventory.product_id == transfer.product_id
            ).first()

            source_inventory.quantity -= transfer.quantity

            if destination_inventory:

                destination_inventory.quantity += transfer.quantity

            else:

                destination_inventory = Inventory(
                    warehouse_id=transfer.to_warehouse,
                    product_id=transfer.product_id,
                    quantity=transfer.quantity
                )

                db.add(destination_inventory)

            transfer.status = "Completed"

            db.commit()
            db.refresh(transfer)

            return transfer

    update_data = transfer_data.model_dump(exclude_unset=True)

    update_data.pop("status", None)

    for key, value in update_data.items():
        setattr(transfer, key, value)

    db.commit()
    db.refresh(transfer)

    return transfer


def delete_transfer(
    transfer_id: int,
    db: Session
):

    transfer = db.query(Transfer).filter(
        Transfer.id == transfer_id
    ).first()

    if transfer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transfer not found"
        )

    db.delete(transfer)
    db.commit()

    return {
        "message": "Transfer deleted successfully"
    }
    
   