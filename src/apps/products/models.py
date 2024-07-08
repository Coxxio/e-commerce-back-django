from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator

from src.apps.categories.models import CategoryModel
from src.common.models.BaseModel import BaseModel
    
class ProductModel(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.CharField(max_length=500, blank=False, null=False)
    stock = models.IntegerField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(1)
        ],
    )
    price = models.FloatField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(1.0)
        ],
    )
    enable = models.BooleanField(default=True)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True
    )

class ImageModel(BaseModel):
    url = models.FileField(upload_to='public/products/')
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, null=False
    )