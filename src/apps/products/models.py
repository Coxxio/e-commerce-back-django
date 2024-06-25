from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator

from src.apps.files.models import FilesModel
from src.apps.categories.models import CategoryModel
from src.common.models.BaseModel import BaseModel


class ProductModel(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=False)
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
    # images = models.many