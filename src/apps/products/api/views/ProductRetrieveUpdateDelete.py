from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers.ProductSerializer import ProductSerializer
from ..serializers.ImageSerializer import ImageSerializer
from ...models import ProductModel, ImageModel


class ProductsRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get(self, req, id=None):
        product = ProductModel.objects.filter(id=id).first()
        if product:
            product_serializer = ProductSerializer(product)
            return Response(
                {
                    'msg': "Ok",
                    'data': product_serializer.data,
                    'statusCode': 200
                },
                status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'msg': 'product not found',
                    'statusCode': 404
                },
                status.HTTP_404_NOT_FOUND
            )

    def put(self, request, id=None):
        sid = transaction.savepoint()
        data = request.data.copy()
        data['name'] = str.capitalize(data['name'])
        product = ProductModel.objects.filter(id=id).first()
        if product:
            if request.FILES.items != 0:
                ImageModel.objects.filter(product=id).delete()
            product_serializer = ProductSerializer(product, data, partial=True)
            if product_serializer.is_valid():
                product_serializer.save()
                for file_name, file_data in request.FILES.items():
                    image = {}
                    image = {'url': None, 'product': None}
                    image['url'] = file_data
                    image['product'] = product_serializer.data['id']
                    imageSerializer = ImageSerializer(data=image)
                    if imageSerializer.is_valid():
                        imageSerializer.save()
                    transaction.savepoint_commit(sid)
                return Response(
                    {
                        'msg': 'Products updated successfully',
                        'statusCode': 200
                    },
                    status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'msg': 'Error',
                        'errors': product_serializer.errors,
                        'statusCode': 400
                    },
                    status.HTTP_400_BAD_REQUEST
                )
        else:
            transaction.savepoint_rollback(sid)
            return Response(
                {
                    'msg': 'product not found',
                    'statusCode': 404
                },
                status.HTTP_404_NOT_FOUND
            )


    def delete(self, req, id=None):
        product = ProductModel.objects.filter(id=id).first()
        if product:
            try:
                product.img.delete()
            except(AttributeError):
                pass
            finally:
                product.delete()
                return Response(
                    {
                        'msg': "Ok",
                        'statusCode': 200
                    },
                    status.HTTP_200_OK
                )
        else:
            return Response(
                {
                    'msg': 'product not found',
                    'statusCode': 404
                },
                status.HTTP_404_NOT_FOUND
            )
