import os
from datetime import datetime, timedelta
import csv
import random

# Configuration
transactions_folder = 'transactions'
num_files = 3
transactions_per_file = 10  # Adjusted to 10 transactions per file
start_date = datetime.now() - timedelta(days=5)  # Start date for transactions

# Ensure the transactions folder exists
os.makedirs(transactions_folder, exist_ok=True)

# Generate transaction files
for i in range(num_files):
    file_name = f'Transaction_{start_date.strftime("%Y%m%d%H%M%S")}.csv'
    file_path = os.path.join(transactions_folder, file_name)
    start_date += timedelta(minutes=5)  # Increment the start date for the next file
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['transactionId', 'productId', 'transactionAmount', 'transactionDatetime'])
        
        for j in range(transactions_per_file):
            transaction_id = i * transactions_per_file + j + 1
            product_id = random.choice([10, 20, 30])
            transaction_amount = round(random.uniform(100.0, 2000.0), 2)
            transaction_datetime = start_date + timedelta(minutes=j)
            
            writer.writerow([transaction_id, product_id, transaction_amount, transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')])
            
    print(f'Generated {file_path}')
