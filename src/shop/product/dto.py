from pydantic import BaseModel

from .domain import ProductQuantityActions

class GetProductsDto(BaseModel):
    skip: int = 0
    limit: int = 5

class GetProductDto(BaseModel):
    id: str

class UpdateProductQuantityDto(GetProductDto):
    action: ProductQuantityActions
    amount: int
