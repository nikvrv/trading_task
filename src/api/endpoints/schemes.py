from pydantic import BaseModel
from typing import Literal


class OrderInput(BaseModel):
    stocks: str
    quantity: float

    class Config:
        from_attributes = True


class OrderOutput(BaseModel):
    id: int
    stocks: str
    quantity: float
    status: Literal["pending", "executed", "canceled"]

    class Config:
        from_attributes = True


class Error(BaseModel):
    code: int
    message: str

    class Config:
        from_attributes = True
