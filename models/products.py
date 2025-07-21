from pydantic import BaseModel, Field
from typing import List


class Size(BaseModel):
    size: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class Product(BaseModel):
    name: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)
    sizes: List[Size]
