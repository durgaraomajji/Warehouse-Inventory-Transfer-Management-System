from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import date, datetime

class TransferCreate(BaseModel):
    from_warehouse: int = Field(..., gt=0)
    to_warehouse: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    transfer_date: date

class TransferUpdate(BaseModel):
    from_warehouse: Optional[int] = Field(default=None, gt=0)
    to_warehouse: Optional[int] = Field(default=None, gt=0)
    product_id: Optional[int] = Field(default=None, gt=0)
    quantity: Optional[int] = Field(default=None, gt=0)
    transfer_date: Optional[date] = None

    status: Optional[
        Literal[
            "Pending",
            "Approved",
            "Completed",
            "Cancelled"
        ]
    ] = None


class TransferResponse(BaseModel):
    id: int
    from_warehouse: int
    to_warehouse: int
    product_id: int
    quantity: int
    transfer_date: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)