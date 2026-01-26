from fastapi import APIRouter, status
from app.model.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse
from app.services.purchase_order import create_order, delete_order, get_order
from app.utils.response import success_response, SuccessResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("", response_model=SuccessResponse)
async def create_purchase_order(purchase: PurchaseOrderCreate):
    purchase_order = purchase.model_dump()
    create_order(purchase_order)

    return success_response(
        message="Order created successfully",
        status_code=status.HTTP_201_CREATED
    )


@router.get(
    "/{order_number}",
    response_model=SuccessResponse[PurchaseOrderResponse]
)
def get_purchase_order(order_number: str):
    order = get_order(order_number)

    return success_response(
        data=order,
        status_code=status.HTTP_200_OK
    )


@router.delete("/{order_number}", response_model=SuccessResponse)
async def delete_purchase_order(order_number: str):
    delete_order(order_number)

    return success_response(
        message="Order deleted successfully",
        status_code=status.HTTP_200_OK
    )
