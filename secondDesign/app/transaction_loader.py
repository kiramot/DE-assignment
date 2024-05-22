import os
import time
import threading
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionLoader:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.transactions = []
        self.lock = threading.Lock()
        self.start_transaction_listener()

    def start_transaction_listener(self):
        def listen_for_transactions():
            while True:
                files = os.listdir(self.folder_path)
                for file in files:
                    if file.startswith("Transaction_") and file.endswith(".csv"):
                        file_path = os.path.join(self.folder_path, file)
                        self.load_transactions(file_path)
                time.sleep(300)  # Sleep for 5 minutes

        threading.Thread(target=listen_for_transactions, daemon=True).start()

    def load_transactions(self, file_path):
        try:
            # Define column names
            columns = ['transactionId', 'productId', 'transactionAmount', 'transactionDatetime']
            
            # Read CSV file with specified column names
            df = pd.read_csv(file_path, names=columns)
            
            logger.info(f"Loaded CSV file {file_path}:\n{df.head()}")  # Log the first few rows of the DataFrame
            
            with self.lock:
                for _, row in df.iterrows():
                    transaction = {
                        'transactionId': row['transactionId'],
                        'productId': row['productId'],
                        'transactionAmount': row['transactionAmount'],
                        'transactionDatetime': row['transactionDatetime']
                    }
                    self.transactions.append(transaction)
                    logger.info(f"Added transaction to memory: {transaction}")
            
            # Move file removal logic here
            os.remove(file_path)
            logger.info(f"Removed file {file_path}")
            
        except FileNotFoundError:
            logger.error(f"File {file_path} not found.")
            
        except Exception as e:
            logger.error(f"Error loading transactions from file {file_path}: {e}")



# Assuming the transaction files are located directly inside the data/transactions folder
transaction_loader = TransactionLoader('../data/transactions')
