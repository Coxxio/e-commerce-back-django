from rest_framework import serializers


from ...models import ImageModel


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageModel
        fields = '__all__'
        
        
    def to_representation(self, instance):
        return {
            "url": instance['url']
        }