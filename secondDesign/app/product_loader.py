import pandas as pd
import os

class ProductLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.products = {}
        self.load_products()

    def load_products(self):
        try:
            df = pd.read_csv(self.file_path)
            for _, row in df.iterrows():
                self.products[row['productId']] = {
                    'productName': row['productName'],
                    'productManufacturingCity': row['productManufacturingCity']
                }
        except Exception as e:
            print(f"Error loading products from file: {e}")

    def get_product(self, product_id: int):
        return self.products.get(product_id)

product_loader = ProductLoader('../data/ProductReference.csv')

