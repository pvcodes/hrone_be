from pydantic import BaseModel, Field
from typing import List


class OrderItem(BaseModel):
    productId: str = Field(..., min_length=1)
    qty: int = Field(..., gt=0)


class Order(BaseModel):
    userId: str = Field(..., min_length=1)
    items: List[OrderItem] = Field(..., min_length=1)
