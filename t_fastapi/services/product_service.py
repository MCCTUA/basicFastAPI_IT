from .base_service import BaseService
from src.models.products import Products

class ProductService(BaseService[Products]):
    pass

product_service = ProductService(Products)