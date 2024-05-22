import pandas as pd
from datetime import datetime, timedelta

class DataStore:
    def __init__(self):
        self.transactions = pd.DataFrame(columns=["transactionId", "productId", "transactionAmount", "transactionDatetime"])
        self.products = pd.DataFrame(columns=["productId", "productName", "productManufacturingCity"])

    def load_transaction_file(self, filepath):
        df = pd.read_csv(filepath)
        self.transactions = pd.concat([self.transactions, df], ignore_index=True)

    def load_product_file(self, filepath):
        self.products = pd.read_csv(filepath)

    def get_transaction(self, transaction_id):
        transaction = self.transactions[self.transactions["transactionId"] == transaction_id].iloc[0]
        product = self.products[self.products["productId"] == transaction["productId"]].iloc[0]
        return {
            "transactionId": transaction["transactionId"],
            "productName": product["productName"],
            "transactionAmount": transaction["transactionAmount"],
            "transactionDatetime": transaction["transactionDatetime"]
        }

    def get_transaction_summary_by_product(self, last_n_days):
        cutoff_date = datetime.now() - timedelta(days=last_n_days)
        recent_transactions = self.transactions[pd.to_datetime(self.transactions["transactionDatetime"]) >= cutoff_date]
        summary = recent_transactions.groupby("productId")["transactionAmount"].sum().reset_index()
        summary = summary.merge(self.products, on="productId")
        return summary[["productName", "transactionAmount"]].to_dict(orient="records")

    def get_transaction_summary_by_city(self, last_n_days):
        cutoff_date = datetime.now() - timedelta(days=last_n_days)
        recent_transactions = self.transactions[pd.to_datetime(self.transactions["transactionDatetime"]) >= cutoff_date]
        summary = recent_transactions.merge(self.products, on="productId").groupby("productManufacturingCity")["transactionAmount"].sum().reset_index()
        return summary[["productManufacturingCity", "transactionAmount"]].to_dict(orient="records")
