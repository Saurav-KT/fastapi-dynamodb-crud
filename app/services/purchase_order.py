from boto3.dynamodb.conditions import ConditionAttributeBase
from botocore.exceptions import ClientError
from app.utils.exception import DuplicateOrderError, OrderNotFoundError, TableNotFoundError, PermissionDeniedError

from .config import tbl_purchase_order

def create_order(order_dict):
    try:

        tbl_purchase_order.put_item(
            Item=order_dict,
            ConditionExpression="attribute_not_exists(order_number)"
        )
        return order_dict
    except ClientError as e:
        print("DYNAMODB ERROR:", e.response)
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise DuplicateOrderError(f"Order {order_dict["order_number"]} already exists")
        raise


def get_order(order_number: str):

    try:
        response= tbl_purchase_order.get_item(Key={"order_number": order_number}
                                               )
        item= response.get["items"]
        if not item:
            raise OrderNotFoundError("Order not found")

        return item

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise TableNotFoundError("Table not found")
        else:
            raise




def delete_order(order_number: str):
    try:
        tbl_purchase_order.delete_item(
            Key={"order_number": order_number},
            ConditionExpression="attribute_exists(#on)",
            ExpressionAttributeNames={
                "#on": "order_number"
            }
        )
        return True


    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ConditionalCheckFailedException":
            raise OrderNotFoundError("Order not found")
        elif error_code == "AccessDeniedException":
            raise PermissionDeniedError("Access denied")
        elif error_code == "ResourceNotFoundException":
            raise TableNotFoundError("Table not found")

        else:

            raise


