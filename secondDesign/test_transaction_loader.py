from app.transaction_loader import TransactionLoader
import os

# Define the folder path for storing transaction CSV files
transactions_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'transactions')

# Create an instance of TransactionLoader
transaction_loader = TransactionLoader(transactions_folder)

# Load all transactions from CSV files in the folder
for file in os.listdir(transactions_folder):
    if file.startswith("Transaction_") and file.endswith(".csv"):
        transaction_file_path = os.path.join(transactions_folder, file)
        transaction_loader.load_transactions(transaction_file_path)

print(transaction_loader.transactions)
