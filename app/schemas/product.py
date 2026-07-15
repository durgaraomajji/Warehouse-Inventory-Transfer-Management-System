from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=150)
    sku: str = Field(..., min_length=3, max_length=50)
    stock_quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)

class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    sku: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    stock_quantity: Optional[int] = Field(
        default=None,
        gt=0
    )

    unit_price: Optional[float] = Field(
        default=None,
        gt=0
    )


class ProductResponse(BaseModel):
    id: int
    product_name: str
    sku: str
    stock_quantity: int
    unit_price: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)