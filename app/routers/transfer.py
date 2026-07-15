from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import warehouse_manager_required
from app.schemas.transfer import (
    TransferCreate,
    TransferUpdate,
    TransferResponse
)
from app.services.transfer_service import (
    create_transfer,
    get_all_transfers,
    get_transfer_by_id,
    get_transfers_by_status,
    update_transfer,
    delete_transfer
)

router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"]
)


@router.post(
    "/",
    response_model=TransferResponse,
    status_code=201
)
def add_transfer(
    transfer: TransferCreate,
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return create_transfer(
        transfer,
        db
    )


@router.get(
    "/",
    response_model=list[TransferResponse]
)
def read_transfers(
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):

    if status:
        return get_transfers_by_status(
            status,
            db
        )

    return get_all_transfers(db)


@router.get(
    "/{transfer_id}",
    response_model=TransferResponse
)
def read_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return get_transfer_by_id(
        transfer_id,
        db
    )


@router.put(
    "/{transfer_id}",
    response_model=TransferResponse
)
def edit_transfer(
    transfer_id: int,
    transfer: TransferUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return update_transfer(
        transfer_id,
        transfer,
        db
    )


@router.delete(
    "/{transfer_id}"
)
def remove_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(warehouse_manager_required)
):
    return delete_transfer(
        transfer_id,
        db
    )