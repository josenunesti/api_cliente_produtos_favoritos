import uuid
from django.db import models


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=False, default='')
    email = models.EmailField(max_length=200, blank=False, default='')
    create_at = models.DateTimeField(auto_now_add=True, blank=False)
    deleted = models.IntegerField(blank=False, default=0)


class Product(models.Model):
    id_product = models.UUIDField(blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    id_client = models.ForeignKey('Client', on_delete=models.CASCADE, db_index=True)
