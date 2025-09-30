from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    item: str
    amount: float
    time: datetime
    description: str  # New required field

class OrderCreate(OrderBase):
    customer_id: str

class OrderUpdate(BaseModel):
    item: Optional[str] = None
    amount: Optional[float] = None
    time: Optional[datetime] = None

class Order(OrderBase):
    id: str
    customer_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
