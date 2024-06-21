from django.db import models

from src.common.models.BaseModel import BaseModel


class CategoryModel(BaseModel):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': f'Category already registered'
        }
    )
    img = models.FileField(upload_to="public/category/", null=True)

    def save(self, *args, **kwargs):
        # Convierte a mayúsculas la primera antes de guardar
        self.name = str.capitalize(self.name) if self.name else None
        super().save(*args, **kwargs)
