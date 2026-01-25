from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

# Define a Generic Success Response
T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    message: str | None=None
    status_code: int
    data: Optional[T] = None  # Data is optional (useful for 204 No Content)


# Utility function for standardized responses
def success_response(message: str=None,status_code: int = status.HTTP_200_OK, data: Optional[T] = None):
    """
    Standard method to return structured API responses.

    :param message: Response message
    :param data: Response data (optional)
    :param status_code: HTTP status code (default: 200 OK)
    :return: JSONResponse
    """
    response_content = SuccessResponse(message=message,status_code=status_code, data=data).model_dump(exclude_none=True,mode="json")  # Remove None fields
    return JSONResponse(status_code=status_code, content=response_content)
