from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import warehouse_manager_required
from app.services.report_service import (
    warehouse_inventory_report,
    search_products,
    transfer_report,
    get_all_transfers,
    get_dashboard
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/inventory")
def inventory_report(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return warehouse_inventory_report(
        page,
        limit,
        db
    )


@router.get("/products/search")
def product_search(
    search: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return search_products(
        search,
        page,
        limit,
        db
    )


@router.get("/transfers")
def transfers_report(
    status: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return transfer_report(
        status,
        page,
        limit,
        db
    )


@router.get("/transfers/all")
def all_transfers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return get_all_transfers(
        page,
        limit,
        db
    )


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return get_dashboard(db)