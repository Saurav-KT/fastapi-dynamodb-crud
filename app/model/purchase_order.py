from pydantic import Field, BaseModel, ConfigDict, field_serializer
from uuid import uuid4, UUID
from decimal import Decimal

class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes= True)

class Item(BaseModel):
    item_number: str
    qty: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)


class PurchaseOrderCreate(BaseModel):
    order_number: str = Field(..., description="purchase order number")
    customer_id: int = Field(..., description="unique customer id")
    items: list[Item] = Field(..., description="list of purchase item")
    total: Decimal | None = Field(default=None, description="total purchase amount")
    payment_id: UUID = Field(..., description="payment reference id")

    @field_serializer("payment_id")
    def serialize_uuid(self, v: UUID):
        return str(v)


class PurchaseOrderResponse(ORMBaseModel):
    order_number: str = Field(..., description="purchase order number")
    customer_id: int = Field(..., description="unique customer id")
    items: list[Item] = Field(..., description="list of purchase item")
    total: Decimal | None = Field(default=None, description="total purchase amount")
    payment_id: UUID = Field(..., description="payment reference id")
