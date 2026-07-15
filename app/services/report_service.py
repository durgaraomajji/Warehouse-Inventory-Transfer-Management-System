from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.transfer import Transfer
from app.models.warehouse import Warehouse


def warehouse_inventory_report(
    page: int,
    limit: int,
    db: Session
):

    offset = (page - 1) * limit

    inventory = (
        db.query(
            Inventory,
            Warehouse.warehouse_name,
            Product.product_name,
            Product.sku
        )
        .join(
            Warehouse,
            Inventory.warehouse_id == Warehouse.id
        )
        .join(
            Product,
            Inventory.product_id == Product.id
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return inventory


def search_products(
    search: str,
    page: int,
    limit: int,
    db: Session
):

    offset = (page - 1) * limit

    products = (
        db.query(Product)
        .filter(
            (Product.product_name.ilike(f"%{search}%")) |
            (Product.sku.ilike(f"%{search}%"))
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return products


def transfer_report(
    status: str,
    page: int,
    limit: int,
    db: Session
):

    offset = (page - 1) * limit

    transfers = (
        db.query(Transfer)
        .filter(Transfer.status == status)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return transfers


def get_all_transfers(
    page: int,
    limit: int,
    db: Session
):

    offset = (page - 1) * limit

    return (
        db.query(Transfer)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_dashboard(db: Session):

    total_products = db.query(Product).count()

    total_warehouses = db.query(Warehouse).count()

    total_inventory = db.query(Inventory).count()

    total_transfers = db.query(Transfer).count()

    return {
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "total_inventory_records": total_inventory,
        "total_transfers": total_transfers
    }