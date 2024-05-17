import json
import boto3
import pandas as pd
from datetime import datetime, timedelta

s3 = boto3.client('s3')

def lambda_handler(event, context):
    last_n_days = int(event['pathParameters']['last_n_days'])
    
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
    
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    filtered_df = transaction_df[pd.to_datetime(transaction_df['transactionDatetime']) >= cutoff_date]
    merged_df = filtered_df.merge(product_df, on='productId')
    summary = merged_df.groupby('productManufacturingCity')['transactionAmount'].sum().reset_index()
    
    response = {
        "summary": [{"cityName": row['productManufacturingCity'], "totalAmount": row['transactionAmount']} for _, row in summary.iterrows()]
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
