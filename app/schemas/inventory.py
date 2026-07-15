from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class InventoryCreate(BaseModel):
    warehouse_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=0)



class InventoryUpdate(BaseModel):
    quantity: int = Field(..., ge=0)


# 
class InventoryResponse(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)