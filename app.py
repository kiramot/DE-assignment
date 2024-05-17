from flask import Flask, request, jsonify
import pandas as pd
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Load product reference data
product_reference_file = 'data/reference/ProductReference.csv'
product_df = pd.read_csv(product_reference_file)

# Load transaction data from files
def load_transactions():
    transaction_folder = 'data/transactions'
    all_files = [os.path.join(transaction_folder, f) for f in os.listdir(transaction_folder) if f.endswith('.csv')]
    transaction_df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    return transaction_df

transaction_df = load_transactions()

@app.route('/assignment/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = transaction_df[transaction_df['transactionId'] == transaction_id].iloc[0]
    product = product_df[product_df['productId'] == transaction['productId']].iloc[0]
    response = {
        "transactionId": transaction['transactionId'],
        "productName": product['productName'],
        "transactionAmount": transaction['transactionAmount'],
        "transactionDatetime": transaction['transactionDatetime']
    }
    return jsonify(response)

@app.route('/assignment/transactionSummaryByProducts/<int:last_n_days>', methods=['GET'])
def get_summary_by_products(last_n_days):
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    filtered_df = transaction_df[pd.to_datetime(transaction_df['transactionDatetime']) >= cutoff_date]
    summary = filtered_df.groupby('productId')['transactionAmount'].sum().reset_index()
    summary = summary.merge(product_df[['productId', 'productName']], on='productId')
    response = {
        "summary": [{"productName": row['productName'], "totalAmount": row['transactionAmount']} for _, row in summary.iterrows()]
    }
    return jsonify(response)

@app.route('/assignment/transactionSummaryByManufacturingCity/<int:last_n_days>', methods=['GET'])
def get_summary_by_city(last_n_days):
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    filtered_df = transaction_df[pd.to_datetime(transaction_df['transactionDatetime']) >= cutoff_date]
    merged_df = filtered_df.merge(product_df, on='productId')
    summary = merged_df.groupby('productManufacturingCity')['transactionAmount'].sum().reset_index()
    response = {
        "summary": [{"cityName": row['productManufacturingCity'], "totalAmount": row['transactionAmount']} for _, row in summary.iterrows()]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
