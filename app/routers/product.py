from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import warehouse_manager_required
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from app.services.product_service import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
    search_products
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return create_product(product, db)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def read_products(
    search: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):

    if search:
        return search_products(search, db)

    return get_all_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return get_product_by_id(product_id, db)


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def edit_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return update_product(
        product_id,
        product,
        db
    )


@router.delete(
    "/{product_id}"
)
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return delete_product(
        product_id,
        db
    )