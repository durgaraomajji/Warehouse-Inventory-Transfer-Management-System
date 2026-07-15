from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseResponse
)
from app.services.warehouse_service import (
    create_warehouse,
    get_all_warehouses,
    get_warehouse_by_id,
    update_warehouse,
    delete_warehouse
)
from app.dependencies import admin_required

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)


@router.post(
    "/",
    response_model=WarehouseResponse,
    status_code=201
)
def add_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return create_warehouse(warehouse, db)


@router.get(
    "/",
    response_model=list[WarehouseResponse]
)
def read_warehouses(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return get_all_warehouses(db)


@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def read_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return get_warehouse_by_id(warehouse_id, db)


@router.put(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def edit_warehouse(
    warehouse_id: int,
    warehouse: WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return update_warehouse(
        warehouse_id,
        warehouse,
        db
    )


@router.delete(
    "/{warehouse_id}"
)
def remove_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return delete_warehouse(
        warehouse_id,
        db
    )