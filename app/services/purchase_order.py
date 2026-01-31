from boto3.dynamodb.conditions import ConditionAttributeBase
from botocore.exceptions import ClientError
from app.utils.exception import DuplicateOrderError, OrderNotFoundError, TableNotFoundError, PermissionDeniedError
from model.purchase_order import OrderUpdateRequest

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


def get_order(order_number: str, customer_id: int):

    try:
        response= tbl_purchase_order.get_item(
            Key={
                "order_number": order_number,
                "customer_id": customer_id
            }
                                               )
        item= response.get("Item")
        if not item:
            raise OrderNotFoundError(f"Order {order_number}/{customer_id} not found")

        return item

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise TableNotFoundError("Table not found")
        else:
            raise

# UPDATE
def update_order(order_number: str, customer_id: int, order: OrderUpdateRequest):

    try:
        response = tbl_purchase_order.update_item(
            Key={
                "order_number": order_number,
                "customer_id": customer_id
            },
            UpdateExpression="SET #items = :items, #total = :total",
            ExpressionAttributeNames={
                "#items": "items",
                "#total": "total"
            },
            ExpressionAttributeValues={
                ":items": [
                    {
                        "item_number": item.item_number,
                        "qty": item.qty,
                        "price": item.price
                    }
                    for item in order.items
                ],
                ":total": order.total
            },
            ConditionExpression="attribute_exists(order_number) AND attribute_exists(customer_id)",
            ReturnValues="UPDATED_NEW"
        )
        return response["Attributes"]
    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "ConditionalCheckFailedException":
            # record does not exist
            raise OrderNotFoundError("Order not found")

        else:
            raise


def delete_order(order_number: str, customer_id: int):
    try:
        tbl_purchase_order.delete_item(
            Key={"order_number": order_number, "customer_id": customer_id},
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


