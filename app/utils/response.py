from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

# Define a Generic Success Response
T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    success: bool
    message: str | None=None
    status_code: int
    data: Optional[T] = None  # Data is optional (useful for 204 No Content)


# Utility function for standardized responses
def success_response(
    message: Optional[str] = None,
    status_code: int = status.HTTP_200_OK,
    data: Optional[T] = None
):
    return JSONResponse(
        status_code=status_code,
        content=SuccessResponse(
            success=True,
            message=message,
            status_code=status_code,
            data=data
        ).model_dump(exclude_none=True, mode="json")
    )

def error_response(
    message: Optional[str] = None,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
):
    return JSONResponse(
        status_code=status_code,
        content=SuccessResponse(
            success=False,
            message=message,
            status_code=status_code
        ).model_dump(exclude_none=True, mode="json")
    )