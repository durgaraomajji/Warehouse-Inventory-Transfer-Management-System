from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(product: ProductCreate, db: Session):

    existing_product = db.query(Product).filter(
        Product.sku == product.sku
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SKU already exists"
        )

    new_product = Product(
        product_name=product.product_name,
        sku=product.sku,
        stock_quantity=product.stock_quantity,
        unit_price=product.unit_price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_all_products(db: Session):

    return db.query(Product).all()


def get_product_by_id(product_id: int, db: Session):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if (
        product_data.sku is not None
        and product_data.sku != product.sku
    ):

        existing_sku = db.query(Product).filter(
            Product.sku == product_data.sku
        ).first()

        if existing_sku:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SKU already exists"
            )

    update_data = product_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(product_id: int, db: Session):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }


def search_products(search: str, db: Session):

    return db.query(Product).filter(
        (Product.product_name.ilike(f"%{search}%")) |
        (Product.sku.ilike(f"%{search}%"))
    ).all()