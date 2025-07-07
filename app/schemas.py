from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    country: str
    query: str

class Product(BaseModel):
    link: str
    price: float
    currency: str
    productName: str

class SearchResponse(BaseModel):
    results: List[Product]
