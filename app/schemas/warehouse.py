from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class WarehouseCreate(BaseModel):
    warehouse_name: str = Field(..., min_length=3, max_length=100)
    location: str = Field(..., min_length=3, max_length=200)
    manager_name: str = Field(..., min_length=3, max_length=100)
    is_active: bool = True

class WarehouseUpdate(BaseModel):
    warehouse_name: Optional[str] = Field(None, min_length=3, max_length=100)
    location: Optional[str] = Field(None, min_length=3, max_length=200)
    manager_name: Optional[str] = Field(None, min_length=3, max_length=100)
    is_active: Optional[bool] = None

class WarehouseResponse(BaseModel):
    id: int
    warehouse_name: str
    location: str
    manager_name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)