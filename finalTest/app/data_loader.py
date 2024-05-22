import os
import csv
import time
from datetime import datetime, timedelta
from threading import Thread
from typing import Dict, List, Any
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)

class DataLoader:
    def __init__(self, transaction_folder: str, reference_file: str):
        self.transaction_folder = transaction_folder
        self.reference_file = reference_file
        self.transactions: List[Dict[str, Any]] = []
        self.products: Dict[int, Dict[str, str]] = {}
        self.load_reference_data()
        self.load_transaction_data()
        self.start_transaction_watcher()

    def load_reference_data(self):
        with open(self.reference_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                productId = int(row['productId'])
                self.products[productId] = {
                    'productName': row['productName'],
                    'productManufacturingCity': row['productManufacturingCity']
                }
        logging.info(f"Loaded products: {self.products}")

    def load_transaction_data(self):
        self.transactions = []  # Clear existing transactions
        for filename in os.listdir(self.transaction_folder):
            if filename.endswith(".csv"):
                self.load_transaction_file(os.path.join(self.transaction_folder, filename))
        logging.info(f"Loaded transactions: {self.transactions}")

    def load_transaction_file(self, filepath: str):
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaction = {
                    'transactionId': int(row['transactionId']),
                    'productId': int(row['productId']),
                    'transactionAmount': float(row['transactionAmount']),
                    'transactionDatetime': datetime.strptime(row['transactionDatetime'], '%Y-%m-%d %H:%M:%S')
                }
                self.transactions.append(transaction)

    def start_transaction_watcher(self):
        def watch_transactions():
            while True:
                self.load_transaction_data()
                time.sleep(300)  # Check for new files every 5 minutes

        watcher_thread = Thread(target=watch_transactions, daemon=True)
        watcher_thread.start()

    def get_transaction_by_id(self, transaction_id: int) -> Dict[str, Any]:
        for transaction in self.transactions:
            if transaction['transactionId'] == transaction_id:
                product = self.products[transaction['productId']]
                return {
                    'transactionId': transaction['transactionId'],
                    'productName': product['productName'],
                    'transactionAmount': transaction['transactionAmount'],
                    'transactionDatetime': transaction['transactionDatetime'].strftime('%Y-%m-%d %H:%M:%S')
                }
        return None

    def get_summary_by_product(self, last_n_days: int) -> List[Dict[str, Any]]:
        cutoff_date = datetime.now() - timedelta(days=last_n_days)
        logging.info(f"Cutoff date for products: {cutoff_date}")
        summary = defaultdict(float)
        for transaction in self.transactions:
            logging.info(f"Processing transaction: {transaction}")
            if transaction['transactionDatetime'] >= cutoff_date:
                product_name = self.products[transaction['productId']]['productName']
                summary[product_name] += transaction['transactionAmount']
        logging.info(f"Product summary: {summary}")
        return [{'productName': k, 'totalAmount': v} for k, v in summary.items()]

    def get_summary_by_city(self, last_n_days: int) -> List[Dict[str, Any]]:
        cutoff_date = datetime.now() - timedelta(days=last_n_days)
        logging.info(f"Cutoff date for cities: {cutoff_date}")
        summary = defaultdict(float)
        for transaction in self.transactions:
            logging.info(f"Processing transaction: {transaction}")
            if transaction['transactionDatetime'] >= cutoff_date:
                city_name = self.products[transaction['productId']]['productManufacturingCity']
                summary[city_name] += transaction['transactionAmount']
        logging.info(f"City summary: {summary}")
        return [{'cityName': k, 'totalAmount': v} for k, v in summary.items()]
