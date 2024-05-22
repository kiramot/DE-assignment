import os
import uvicorn
import threading
from fastapi import FastAPI
from services import app as services_app
from transaction_loader import TransactionLoader
from data_generator import start_data_generation

# Create FastAPI app instance
app = FastAPI()

# Mount services
app.mount("/assignment", services_app)

# Define the folder path for storing transaction CSV files
transactions_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'transactions')

# Create an instance of TransactionLoader
transaction_loader = TransactionLoader(transactions_folder)

if __name__ == "__main__":
    # Start data generation in a background thread
    data_generation_thread = threading.Thread(target=start_data_generation, args=(transactions_folder,), daemon=True)
    data_generation_thread.start()
    
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8080)
