import redis
import json
from . import base
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)


class ProductRedisCache(base.BaseCacheProduct):

    def __init__(self, ttl=None):
        self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        self.ttl = ttl

    def get_product(self, id_product: str):
        data = self.redis.get(str(id_product))
        if data is not None:
            return json.loads(data)

    def set_product(self, product: dict):
        id_product = product.pop("id")
        product_dump = json.dumps(product)
        self.redis.set(name=id_product, value=product_dump, ex=self.ttl)
