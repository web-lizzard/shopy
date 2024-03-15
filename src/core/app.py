from fastapi import FastAPI
from server import product_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(product_router)

    return app