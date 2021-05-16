import requests
import json

from typing import List

from .base import BaseApiProduct, BaseCacheProduct
from ..models import Product
import os

URL_API_PRODUCT = os.environ.get("URL_API_PRODUCT", "http://challenge-api.luizalabs.com/api/product/")


class ProductChallengeApi(BaseApiProduct):

    def __init__(self, cache_product: BaseCacheProduct = None):
        self.cache_product = cache_product

    def _get_product_from_api(self, id_product: str) -> dict:
        url = f"{URL_API_PRODUCT}{id_product}/"
        response = requests.request("GET", url)
        product_data = json.loads(response.text)
        if "error_message" in product_data:
            return None

        return product_data

    def get_all_product(self, list_product: List[Product]) -> list:
        data = []
        for product in list_product:
            product_data = self.get_product(product)
            data.append(product_data)

        return data

    def get_product(self, product: Product) -> dict:

        product_data = None
        if self._cache_enable():
            product_data = self.cache_product.get_product(product.id_product)

        if product_data is None:
            product_data = self._get_product_from_api(product.id_product)
            if self._cache_enable():
                self.cache_product.set_product(product_data)

        return {
            "id_product": product.id_product,
            "title": product_data["title"],
            "title": product_data["title"],
            "image": product_data["image"],
            "price": product_data["price"],
            "review_score": product_data["reviewScore"] if "reviewScore" in product_data else None,
            "create_at": product.create_at
        }

    def exist_product(self, id_product: str) -> bool:
        if self.cache_product is not None:
            product_data = self.cache_product.get_product(id_product)
            if product_data is not None:
                return True

        product_data = self._get_product_from_api(id_product)
        if product_data is not None:
            self.cache_product.set_product(product_data)
            return True
        else:
            return False

    def _cache_enable(self) -> bool:
        return self.cache_product is not None