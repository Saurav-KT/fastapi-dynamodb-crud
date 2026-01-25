from fastapi import APIRouter, HTTPException, status
from app.model.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse
from app.services.purchase_order import create_order,delete_order
from app.utils.response import success_response, SuccessResponse
from app.utils.exception import DuplicateOrderError, OrderNotFoundError, TableNotFoundError,PermissionDeniedError

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.post("", response_model=SuccessResponse[PurchaseOrderResponse])
async def create_purchase_order(purchase: PurchaseOrderCreate):
    try:
        purchase_order = purchase.model_dump()
        order = create_order(purchase_order)
        if order:
            return success_response("order created successfully", status_code=status.HTTP_201_CREATED)

    except DuplicateOrderError as e:
        # Duplicate order
        raise HTTPException(
            status_code=409,  # Conflict
            detail=str(e)
        )

# @router.get("/{order_number}", response_model=SuccessResponse[PurchaseOrderResponse])
# def get_purchase_order(order_number:str):
#     response = table.get_item(
#         Key={"empId": emp_id}
#     )
#     return response.get("Item")

@router.delete("/{order_number}", response_model=SuccessResponse)
async def delete_purchase_order(order_number: str):
    try:
       is_deleted= delete_order(order_number)
       if is_deleted:
           return success_response("Order deleted successfully", status_code=status.HTTP_200_OK)


    except OrderNotFoundError:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="Order not found"
       )

    except PermissionDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    except TableNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service configuration error"
        )

