from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime, timedelta
import logging

from models import TransactionDetailResponse, SummaryResponse  # Import your models here
from product_loader import product_loader
from transaction_loader import transaction_loader

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/assignment/transaction/{transaction_id}", response_model=TransactionDetailResponse)
def get_transaction(transaction_id: int):
    try:
        with transaction_loader.lock:
            for transaction in transaction_loader.transactions:
                if transaction['transactionId'] == transaction_id:
                    product = product_loader.get_product(transaction['productId'])
                    if product:
                        logger.info(f"Transaction found: {transaction}")
                        return TransactionDetailResponse(
                            transactionId=transaction['transactionId'],
                            productName=product['productName'],
                            transactionAmount=transaction['transactionAmount'],
                            transactionDatetime=transaction['transactionDatetime']
                        )
        logger.error(f"Transaction with ID {transaction_id} not found")
        raise HTTPException(status_code=404, detail="Transaction not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error retrieving transaction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/assignment/transactionSummaryByProducts/{last_n_days}", response_model=SummaryResponse)
def get_transaction_summary_by_products(last_n_days: int):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=last_n_days)
        summary = {}
        
        with transaction_loader.lock:
            for transaction in transaction_loader.transactions:
                transaction_datetime = datetime.strptime(transaction['transactionDatetime'], '%Y-%m-%d %H:%M:%S')
                if start_date <= transaction_datetime <= end_date:
                    product = product_loader.get_product(transaction['productId'])
                    if product:
                        if product['productName'] not in summary:
                            summary[product['productName']] = 0
                        summary[product['productName']] += transaction['transactionAmount']
        
        logger.info(f"Summary by products: {summary}")
        return SummaryResponse(summary=[{'productName': k, 'totalAmount': v} for k, v in summary.items()])
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error generating summary by products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/assignment/transactionSummaryByManufacturingCity/{last_n_days}", response_model=SummaryResponse)
def get_transaction_summary_by_manufacturing_city(last_n_days: int):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=last_n_days)
        summary = {}
        
        with transaction_loader.lock:
            for transaction in transaction_loader.transactions:
                transaction_datetime = datetime.strptime(transaction['transactionDatetime'], '%Y-%m-%d %H:%M:%S')
                if start_date <= transaction_datetime <= end_date:
                    product = product_loader.get_product(transaction['productId'])
                    if product:
                        city = product['productManufacturingCity']
                        if city not in summary:
                            summary[city] = 0
                        summary[city] += transaction['transactionAmount']
        
        logger.info(f"Summary by manufacturing city: {summary}")
        return SummaryResponse(summary=[{'cityName': k, 'totalAmount': v} for k, v in summary.items()])
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error generating summary by manufacturing city: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
