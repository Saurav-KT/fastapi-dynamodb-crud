import boto3

dynamodb= boto3.resource('dynamodb', region_name="us-east-1")
tbl_purchase_order= dynamodb.Table('purchase_order')

