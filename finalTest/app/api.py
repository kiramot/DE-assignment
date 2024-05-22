from fastapi import FastAPI, HTTPException
from .data_loader import DataLoader

app = FastAPI()
data_loader = DataLoader(transaction_folder='transactions', reference_file='reference/ProductReference.csv')

@app.get("/assignment/transaction/{transaction_id}")
async def get_transaction(transaction_id: int):
    transaction = data_loader.get_transaction_by_id(transaction_id)
    if transaction:
        return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")

@app.get("/assignment/transactionSummaryByProducts/{last_n_days}")
async def get_transaction_summary_by_products(last_n_days: int):
    summary = data_loader.get_summary_by_product(last_n_days)
    return {"summary": summary}

@app.get("/assignment/transactionSummaryByManufacturingCity/{last_n_days}")
async def get_transaction_summary_by_city(last_n_days: int):
    summary = data_loader.get_summary_by_city(last_n_days)
    return {"summary": summary}
