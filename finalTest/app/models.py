from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    transactionId: int
    productId: int
    transactionAmount: float
    transactionDatetime: datetime

class Product(BaseModel):
    productId: int
    productName: str
    productManufacturingCity: str
