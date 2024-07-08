from rest_framework import serializers

from .ImageSerializer import ImageSerializer
from src.apps.categories.api.serializers.CategorySerializer import CategorySerializer

from ...models import ProductModel, ImageModel


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = ProductModel
        fields = '__all__'


    def to_representation(self, instance):
        try:
            imagesModel = ImageModel.objects.values().filter(product=instance.id)
            images = ImageSerializer(imagesModel, many=True).data
        except ImageModel.DoesNotExist:
            images = {}
        return {
            'id': str(instance.id),
            'name': instance.name,
            'description': instance.description,
            'price': instance.price,
            'stock': instance.stock,
            'createdAt': instance.createdAt,
            'updatedAt': instance.updatedAt,
            'category': CategorySerializer(instance.category).data,
            'images': images,
        }
