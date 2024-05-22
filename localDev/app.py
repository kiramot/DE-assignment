from flask import Flask, jsonify
from data_store import DataStore
from watcher import start_watching
import threading

app = Flask(__name__)
data_store = DataStore()

@app.route('/assignment/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = data_store.get_transaction(transaction_id)
    return jsonify(transaction)

@app.route('/assignment/transactionSummaryByProducts/<int:last_n_days>', methods=['GET'])
def get_transaction_summary_by_products(last_n_days):
    summary = data_store.get_transaction_summary_by_product(last_n_days)
    return jsonify({"summary": summary})

@app.route('/assignment/transactionSummaryByManufacturingCity/<int:last_n_days>', methods=['GET'])
def get_transaction_summary_by_city(last_n_days):
    summary = data_store.get_transaction_summary_by_city(last_n_days)
    return jsonify({"summary": summary})

if __name__ == '__main__':
    data_store.load_product_file('ProductReference.csv')
    transaction_dir = 'transactions/'
    watcher_thread = threading.Thread(target=start_watching, args=(transaction_dir, data_store))
    watcher_thread.start()
    app.run(host='0.0.0.0', port=8080)
