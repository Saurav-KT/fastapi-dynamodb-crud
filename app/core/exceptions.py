from fastapi import Request, status

from app.utils.exception import (
    OrderNotFoundError,
    DuplicateOrderError,
    TableNotFoundError,
    PermissionDeniedError
)
from app.utils.response import error_response


def register_exception_handlers(app):

    @app.exception_handler(OrderNotFoundError)
    async def order_not_found(
        request: Request,
        exc: OrderNotFoundError
    ):
        return error_response(
            message=str(exc) or "Order not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    @app.exception_handler(DuplicateOrderError)
    async def duplicate_order(
        request: Request,
        exc: DuplicateOrderError
    ):
        return error_response(
            message=str(exc) or "Duplicate order",
            status_code=status.HTTP_409_CONFLICT
        )


    @app.exception_handler(TableNotFoundError)
    async def table_not_found(
        request: Request,
        exc: TableNotFoundError
    ):
        return error_response(
            message="Service configuration error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @app.exception_handler(PermissionDeniedError)
    async def permission_denied(
        request: Request,
        exc: PermissionDeniedError
    ):
        return error_response(
            message="Permission denied",
            status_code=status.HTTP_403_FORBIDDEN
        )

    @app.exception_handler(Exception)
    async def global_exception(
        request: Request,
        exc: Exception
    ):
        print("UNHANDLED ERROR:", exc)  # CloudWatch

        return error_response(
            message="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
