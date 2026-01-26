import uvicorn
from fastapi import FastAPI
from app.routers import purchase_order
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from app.core.exceptions import register_exception_handlers

app = FastAPI()
app.include_router(purchase_order.router, prefix="/api")
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


handler = Mangum(app)

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8084, workers=1)