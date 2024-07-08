from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from src.apps.users.enums.UserRole import UserEnum
from src.common.permissions.roles import IsAuthAndRoles

from ..serializers.ProductSerializer import ProductSerializer
from ..serializers.ImageSerializer import ImageSerializer
from ...models import ProductModel, ImageModel


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = ProductModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthAndRoles([UserEnum.ADMIN, UserEnum.SUPER_ADMIN])]

    def get(self, req):
        products = self.get_queryset()
        serializer = ProductSerializer(products, many=True)
        return Response(
            {
                'msg': "Ok",
                'data': serializer.data,
                'statusCode': 200
            },
            status.HTTP_200_OK
        )

    # Create
    @transaction.atomic
    def post(self, request):
        # try:
        sid = transaction.savepoint()
        data = request.data.copy()
        data['name'] = str.capitalize(data['name'])
        Product_serializer = ProductSerializer(data=data)
        if Product_serializer.is_valid():
            Product_serializer.save()
            for file_name, file_data in request.FILES.items():
                image = {}
                image = {'url': None, 'product': None}
                image['url'] = file_data
                image['product'] = Product_serializer.data['id']
                imageSerializer = ImageSerializer(data=image)
                if imageSerializer.is_valid():
                    imageSerializer.save()
            transaction.savepoint_commit(sid)
            return Response(
                {
                    'status': 201,
                    'msg': 'CREATED',
                    'data': Product_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            transaction.savepoint_rollback(sid)
            return Response(
                {
                    'status': 400,
                    'msg': 'Error',
                    'errors': Product_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # except:
        transaction.savepoint_rollback(sid)
            # return Response(
            #     {
            #         'status': 400,
            #         'msg': 'Error creating product',
            #     },
            #     status=status.HTTP_400_BAD_REQUEST)
