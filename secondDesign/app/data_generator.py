import os
import csv
import random
from datetime import datetime, timedelta

def start_data_generation(folder_path):
    # Ensure that the 'data/transactions' directory exists, create it if it doesn't
    transaction_dir = os.path.join(folder_path, 'transactions')
    if not os.path.exists(transaction_dir):
        os.makedirs(transaction_dir)

    file_path = os.path.join(transaction_dir, f"Transaction_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    try:
        with open(file_path, 'a', newline='') as csvfile:  # Use 'a' mode for appending
            fieldnames = ['transactionId', 'productId', 'transactionAmount', 'transactionDatetime']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Check if file exists to determine whether to write header
            write_header = not os.path.exists(file_path)

            # Write CSV header only if the file doesn't exist
            if write_header:
                writer.writeheader()
            
            # Generate synthetic data
            for i in range(20):
                transaction_id = i + 1
                product_id = random.choice([10, 20, 30])
                transaction_amount = random.uniform(100, 5000)
                transaction_datetime = datetime.now() - timedelta(minutes=random.randint(1, 10000))
                writer.writerow({
                    'transactionId': transaction_id,
                    'productId': product_id,
                    'transactionAmount': transaction_amount,
                    'transactionDatetime': transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')
                })
        print(f"Synthetic transaction data generated and saved to {file_path}")
    except Exception as e:
        print(f"Error occurred while generating transaction data: {e}")

# Test the function
start_data_generation('../data')
