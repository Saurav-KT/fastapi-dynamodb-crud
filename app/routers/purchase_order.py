from fastapi import APIRouter, status
from app.model.purchase_order import OrderCreateRequest, OrderResponse, OrderUpdateRequest
from app.services.purchase_order import create_order, delete_order, get_order, update_order
from app.utils.response import success_response, SuccessResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("", response_model=SuccessResponse)
async def create_purchase_order(purchase: OrderCreateRequest):
    purchase_order = purchase.model_dump()
    create_order(purchase_order)

    return success_response(
        message="Order created successfully",
        status_code=status.HTTP_201_CREATED
    )


@router.get(
    "/{order_number}/{customer_id}",
    response_model=SuccessResponse[OrderResponse]
)
def get_purchase_order(order_number: str, customer_id: int):
    order = get_order(order_number, customer_id)

    return success_response(
        data=order,
        status_code=status.HTTP_200_OK
    )


@router.delete("/{order_number}/{customer_id}", response_model=SuccessResponse)
async def delete_purchase_order(order_number: str, customer_id: int):
    delete_order(order_number,customer_id)

    return success_response(
        message="Order deleted successfully",
        status_code=status.HTTP_200_OK
    )

@router.put("/{order_number}/{customer_id}")
async def update_purchase_order(order_number:str, customer_id: int, payload: OrderUpdateRequest):
    update_order(order_number,customer_id,payload)
    return success_response(
        message="Order updated successfully",
        status_code=status.HTTP_200_OK
    )



