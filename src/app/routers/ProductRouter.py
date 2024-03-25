from fastapi import APIRouter, status, Depends
from auth.JWTBearer import JWTBearer
from typing import List
from routers.schemas import ProductRequest, ProductResponse
from uuid import UUID
from services.Interfaces.IProductService import IProductService


class ProductRouter:
    def __init__(self, service: IProductService):

        self.router = APIRouter(
            prefix="/products",
            tags=["Products"],
            dependencies=[Depends(JWTBearer())]
        )
        self.service = service

        @self.router.get("/", response_model=List[ProductResponse])
        async def get_all_products(offset: int = 0, limit: int = 100) -> List[ProductResponse]:
            """
            Retrieve a list of products.

            - `offset`: Optional integer. Number of records to skip.
            - `limit`: Optional integer. Maximum number of records to retrieve.

            Returns:
            - List of `ProductResponse` objects.
            """
            res = await self.service.all(offset, limit)
            return res

        @self.router.get("/{id}", response_model=ProductResponse, responses={404: {"description": "Item not found"}})
        async def get_product_by_id(id: UUID) -> ProductResponse:
            """
            Retrieve a product by its ID.

            - `id`: UUID. ID of the product to retrieve.

            Returns:
            - `ProductResponse` object.
            """
            res = await self.service.one(id)
            return res

        @self.router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
        async def create_product(product: ProductRequest) -> ProductResponse:
            """
            Create a new product.

            - `product`: `ProductRequest` object containing product data.

            Returns:
            - `ProductResponse` object of the created product.
            """
            res = await self.service.create(product)
            return res

        @self.router.delete("/{id}", responses={404: {"description": "Item not found"}})
        async def delete_product(id: UUID) -> str:
            """
            Delete a product by its ID.

            - `id`: UUID. ID of the product to delete.

            Returns:
            - Success message.
            """
            res = await self.service.delete(id)
            return res

        @self.router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ProductResponse, responses={404: {"description": "Item not found"}})
        async def update_product_stock(id: UUID, stock: int) -> ProductResponse:
            """
            Update the stock of a product.

            - `id`: UUID. ID of the product to update.
            - `stock`: Integer. New stock value.

            Returns:
            - `ProductResponse` object of the updated product.
            """
            res = await self.service.update_stock(id, stock)
            return res
