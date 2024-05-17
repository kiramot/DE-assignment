import json
import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    transaction_id = int(event['pathParameters']['transaction_id'])
    
    # Load product reference data from S3
    product_reference_bucket = 'product-reference-bucket'
    product_reference_key = 'ProductReference.csv'
    product_obj = s3.get_object(Bucket=product_reference_bucket, Key=product_reference_key)
    product_df = pd.read_csv(product_obj['Body'])
    
    # Load transaction data from S3
    transaction_bucket = 'transaction-data-bucket'
    transaction_objs = s3.list_objects_v2(Bucket=transaction_bucket)['Contents']
    
    all_transactions = []
    for obj in transaction_objs:
        transaction_file = obj['Key']
        transaction_obj = s3.get_object(Bucket=transaction_bucket, Key=transaction_file)
        transaction_df = pd.read_csv(transaction_obj['Body'])
        all_transactions.append(transaction_df)
    
    transaction_df = pd.concat(all_transactions, ignore_index=True)
    
    # Find transaction by ID
    transaction = transaction_df[transaction_df['transactionId'] == transaction_id].iloc[0]
    product = product_df[product_df['productId'] == transaction['productId']].iloc[0]
    
    response = {
        "transactionId": transaction['transactionId'],
        "productName": product['productName'],
        "transactionAmount": transaction['transactionAmount'],
        "transactionDatetime": transaction['transactionDatetime']
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
