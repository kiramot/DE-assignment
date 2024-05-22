from pydantic import BaseModel
from typing import List

class TransactionDetailResponse(BaseModel):
    transactionId: int
    productName: str
    transactionAmount: float
    transactionDatetime: str

class SummaryItem(BaseModel):
    productName: str
    totalAmount: float

class SummaryResponse(BaseModel):
    summary: List[SummaryItem]
